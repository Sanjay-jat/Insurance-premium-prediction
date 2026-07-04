import pandas as pd
from sklearn.model_selection import train_test_split   
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score,classification_report
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer   
import numpy as np
from sklearn.model_selection import GridSearchCV


df = pd.read_csv("D:/vs code/csvfiles/insurance_premium_classification.csv")

print(df.head())

df_data=df.copy()

df_data["Bmi"] = df_data["weight_kg"] / ((df_data["height_cm"] / 100) ** 2)

def age_group(age):
    if age < 30:
        return 'Young'
    elif 30 <= age < 50:
        return 'Middle-aged'
    else:
        return 'Senior'
    
df_data['age_group'] = df_data['age'].apply(age_group)

def lifestyle_risk(row):
    if row['smoker'] == 'yes' and row['Bmi'] >30:
        return 'High Risk'
    elif row['smoker'] == 'yes' or row['Bmi'] >27:
        return 'Moderate Risk'
    else:
        return 'Low Risk'   
    
df_data['lifestyle_risk'] = df_data.apply(lifestyle_risk, axis=1)

df_data.drop(columns=["height_cm", "weight_kg"], inplace=True)
df_data = df_data[
    [
        "age",
        "sex",
        "smoker",
        "region",
        "Bmi",
        "age_group",
        "lifestyle_risk",
        "premium_category",
    ]
]
#print(df_data.head())

x=df_data.drop(columns=["premium_category"])
y=df_data["premium_category"]

#print(x.head())

categorical_features = ["sex", "smoker", "region", "age_group", "lifestyle_risk"]
numerical_features = ["age", "Bmi"] 

preprocessor=ColumnTransformer(
    transformers=[
        ("num", "passthrough", numerical_features),
        ("cat", OneHotEncoder(), categorical_features),
    ]
)
pipeline=Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(random_state=42))
    ]
)
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

pipeline.fit(x_train, y_train)

y_pred=pipeline.predict(x_test)
accuracy=accuracy_score(y_test, y_pred)
print("Accuracy:", accuracy)

import pickle
with open("models/insurance_classifier.pkl", "wb") as f:
    pickle.dump(pipeline, f)