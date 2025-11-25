from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import os
import requests
import urllib.parse

# ENLACE DIRECTO DE TU MODELO EN GOOGLE DRIVE (cámbialo por el tuyo)
MODEL_URL = "https://drive.usercontent.google.com/download?id=1ABC123xyz&export=download&authuser=0"
MODEL_PATH = "car_price_model.joblib"

# Descargar el modelo la primera vez
if not os.path.exists(MODEL_PATH):
    print("Descargando modelo desde Google Drive...")
    response = requests.get(MODEL_URL)
    with open(MODEL_PATH, "wb") as f:
        f.write(response.content)
    print("Modelo descargado!")

# Cargar modelo
model = joblib.load(MODEL_PATH)

app = FastAPI(title="Predicción Precio Auto")

class CarInput(BaseModel):
    year: int
    mileage: float

@app.get("/")
def home():
    return {"message": "API activa - modelo cargado correctamente"}

@app.post("/predict")
def predict(data: CarInput):
    pred = model.predict([[data.year, data.mileage]])[0]
    return {"price_usd": round(float(pred), 2)}
