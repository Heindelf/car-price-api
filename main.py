from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import os

# Cargar el modelo (Railway lo va a tener en la misma carpeta)
model = joblib.load("car_price_model.joblib")

app = FastAPI(title="Predicción Precio Auto")

class CarInput(BaseModel):
    year: int
    mileage: float

@app.get("/")
def home():
    return {"message": "API de predicción de precios de autos - activa"}

@app.post("/predict")
def predict(data: CarInput):
    pred = model.predict([[data.year, data.mileage]])[0]
    return {"price_usd": round(float(pred), 2)}