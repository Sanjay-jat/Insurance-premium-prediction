from fastapi import FastAPI
from fastapi.responses import JSONResponse
from schema.user_input import Insurance
from src.predict import predict,Model_version

import pandas as pd

app=FastAPI()

@app.get('/')
def home():
    return {"Insurance_premium_prediction_company"}

@app.get('/health')
def health_check():
    return {
        'status':'ok',
        'version':Model_version
    }
@app.post("/predict")
def predict_insurance_premium(data:Insurance):
    user_input={
        'Bmi': data.Bmi,
        'age_group': data.age_group,    
        'lifestyle_risk': data.lifestyle_risk,
        'age': data.age,
        'sex': data.sex,
        'smoker': data.smoker,
        'region': data.region
    }
    try:
        prediction = predict(user_input)
        return JSONResponse(status_code=200, content={'predicted_category': prediction})
    except Exception as e:
        return JSONResponse(status_code=500,content=str(e))
