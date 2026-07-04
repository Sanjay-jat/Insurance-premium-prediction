import pickle
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "models" / "insurance_classifier.pkl"

with open(MODEL_PATH, "rb") as f:
    model = pickle.load(f)

Model_version='1.0.0'
def predict(user_input:dict):

    input_df=pd.DataFrame([user_input])
    output=model.predict(input_df)[0]
    return output
