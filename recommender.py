from __future__ import annotations
import json
import pickle
from pathlib import Path
from typing import List, Optional, Dict, Any

import numpy as np
from lightfm.data import Dataset
from scipy.special import expit  # para normalización opcional tipo sigmoide

ARTEFACTOS_DIR = Path("artefactos")

# ---------- Carga de artefactos ----------
with open(ARTEFACTOS_DIR / "modelo_lightfm.pkl", "rb") as f:
    model = pickle.load(f)

with open(ARTEFACTOS_DIR / "user_id_map.json", "r", encoding="utf-8") as f:
    user_id_map: Dict[str, int] = json.load(f)

with open(ARTEFACTOS_DIR / "item_id_map.json", "r", encoding="utf-8") as f:
    item_id_map: Dict[str, int] = json.load(f)

with open(ARTEFACTOS_DIR / "user_features.pkl", "rb") as f:
    user_features = pickle.load(f)

with open(ARTEFACTOS_DIR / "item_features.pkl", "rb") as f:
    item_features = pickle.load(f)

with open(ARTEFACTOS_DIR / "item_name_map.json", "r", encoding="utf-8") as f:
    item_name_map: Dict[str, str] = json.load(f)

with open(ARTEFACTOS_DIR / "schema.json", "r", encoding="utf-8") as f:
    schema: Dict[str, Any] = json.load(f)

inv_item_map = {v: k for k, v in item_id_map.items()}
n_items = len(item_id_map)

# Dataset “vacío” para construir features en cold-start con el MISMO vocabulario
dataset_cs = Dataset()
dataset_cs.fit(
    users=list(user_id_map.keys()) or ["__placeholder_user__"],
    items=list(item_id_map.keys()) or ["__placeholder_item__"],
    user_features=schema["user_features_vocab"],
    item_features=schema["item_features_vocab"],
)

# ---------- Utilidades ----------
def _build_user_features_coldstart(features_text: List[str]):
    """
    Construye la matriz de features para usuario NUEVO usando un user_id válido del mapping.
    IMPORTANTE: features_text deben existir en schema["user_features_vocab"].
    """
    # Tomamos cualquier user_id válido del mapping para satisfacer a LightFM
    dummy_user = next(iter(user_id_map.keys()))
    return dataset_cs.build_user_features([(dummy_user, features_text)], normalize=False)

def _normalize(scores: np.ndarray, mode: str) -> np.ndarray:
    mode = (mode or "none").lower()
    if mode == "sigmoid":
        return expit(scores)  # (0,1)
    if mode == "minmax":
        smin, smax = float(scores.min()), float(scores.max())
        if smax - smin < 1e-12:
            return np.ones_like(scores) * 0.5
        return (scores - smin) / (smax - smin)
    return scores  # none

# ---------- Recomendador ----------
def recommend(
    user_id: str,
    topn: int = 3,
    features: Optional[List[str]] = None,
    exclude_item_ids: Optional[List[str]] = None,
    normalize: str = "none",  # "none" | "sigmoid" | "minmax"
) -> List[Dict[str, Any]]:
    """
    - user_id: puede ser conocido o nuevo (cold-start).
    - features: SOLO para usuarios nuevos (p.ej. ["segmento=Backpacker","pais=PE","edad=18-25"]).
    - exclude_item_ids: opcional, para filtrar ítems ya consumidos, fuera de stock, etc.
    - normalize: normalización opcional de scores para presentación.
    """
    item_indices = np.arange(n_items)

    # Exclusiones de negocio (opcional)
    if exclude_item_ids:
        exclude_idx = {item_id_map[iid] for iid in exclude_item_ids if iid in item_id_map}
        mask = np.array([i not in exclude_idx for i in item_indices], dtype=bool)
        cand = item_indices[mask]
    else:
        cand = item_indices

    # Usuario CONOCIDO
    if user_id in user_id_map:
        u_idx = user_id_map[user_id]
        scores = model.predict(
            u_idx, cand, user_features=user_features, item_features=item_features
        )
    else:
        # Usuario NUEVO (cold-start)
        if not features:
            raise ValueError(
                "Usuario nuevo: debe enviar 'features' con el vocabulario del esquema."
            )
        user_features_cs = _build_user_features_coldstart(features)
        # Índice dummy (0) + features del usuario nuevo
        scores = model.predict(
            0, cand, user_features=user_features_cs, item_features=item_features
        )

    scores = _normalize(scores, normalize)

    # Top-N
    top_loc = np.argsort(-scores)[:topn]
    top_items_idx = cand[top_loc]
    result = []
    for loc, idx in enumerate(top_items_idx):
        item_id = inv_item_map[idx]
        result.append(
            {
                "rank": int(loc + 1),
                "item_id": item_id,
                "nombre": item_name_map.get(item_id, item_id),
                "score": float(scores[top_loc[loc]]),
            }
        )
    return result
