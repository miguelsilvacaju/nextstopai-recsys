# Imagen base ligera con Python 3.11
FROM python:3.11-slim

# Evitar prompts de apt
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Dependencias de sistema para compilar/scipy/lightfm
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gfortran \
    libopenblas-dev liblapack-dev \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo
WORKDIR /app

# Instalar dependencias de Python primero (para mejor cache)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código y artefactos
COPY recommender.py main.py ./
COPY artefactos ./artefactos

# Puerto de la app
EXPOSE 8080

# Ejecutar Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
