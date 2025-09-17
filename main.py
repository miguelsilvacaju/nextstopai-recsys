from typing import List, Optional
from fastapi import FastAPI, Query
from pydantic import BaseModel
from recommender import recommend, schema

app = FastAPI(title="Turismo Recsys API", version="1.0.0")

class RecommendBody(BaseModel):
    user_id: str
    topn: int = 3
    features: Optional[List[str]] = None
    exclude_item_ids: Optional[List[str]] = None
    normalize: str = "none"  # "none" | "sigmoid" | "minmax"

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/schema")
def get_schema():
    return {"user_features_vocab": schema["user_features_vocab"],
            "item_features_vocab": schema["item_features_vocab"]}

# GET simple (features por query repetida)
@app.get("/recomendar/{user_id}")
def recomendar_get(
    user_id: str,
    topn: int = 3,
    normalize: str = "none",
    features: Optional[List[str]] = Query(None, description="Solo para usuarios nuevos"),
    exclude: Optional[List[str]] = Query(None, alias="exclude", description="IDs a excluir"),
):
    recs = recommend(user_id=user_id, topn=topn, features=features,
                     exclude_item_ids=exclude, normalize=normalize)
    return {"user_id": user_id, "recomendaciones": recs}

# POST flexible (body JSON)
@app.post("/recomendar")
def recomendar_post(payload: RecommendBody):
    recs = recommend(user_id=payload.user_id, topn=payload.topn,
                     features=payload.features, exclude_item_ids=payload.exclude_item_ids,
                     normalize=payload.normalize)
    return {"user_id": payload.user_id, "recomendaciones": recs}
