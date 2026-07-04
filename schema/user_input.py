from pydantic import BaseModel,Field,computed_field
from typing import Literal

class Insurance(BaseModel): 
    
    age: int = Field(..., gt=0, description="Age of the individual")
    sex: Literal['male', 'female'] = Field(..., description="Sex of the individual")
    weight_kg: float = Field(..., gt=0, description="Weight of the individual in kg")
    height_cm: float = Field(..., gt=0, description="Height of the individual in cm")
    smoker: Literal['yes', 'no'] = Field(..., description="Whether the individual is a smoker or not")
    region: Literal['northwest', 'northeast', 'southwest', 'southeast'] = Field(..., description="Region of the individual")

    @computed_field
    @property
    def Bmi(self) -> float:
        return self.weight_kg / ((self.height_cm / 100) ** 2)
    @computed_field
    @property
    def age_group(self) -> str:
        if self.age < 30:
            return 'Young'
        elif self.age < 60:
            return 'Middle-aged'
        else:
            return 'Senior'
        
    @computed_field
    @property   
    def lifestyle_risk(self) -> str:
        if self.smoker == 'yes' and self.Bmi > 30:
            return 'High Risk'
        elif self.smoker == 'yes' or self.Bmi > 27:
            return 'Moderate Risk'
        else:
            return 'Low Risk'
        