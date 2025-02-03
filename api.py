from fastapi import FastAPI, File, UploadFile
import pandas as pd
import pickle
from mlflow import MlflowClient, pyfunc
import os
import numpy as np



tags = [
    {
        "name": "Maths",
        "description": "Mathematical operations"
    },
    {
        "name": "Models",
        "description": "Data models"
    }
]


app = FastAPI(
    title="Test FastAPI",
    description="This is a test FastAPI application",
    version="0.1",
    openapi_tags = tags
)





@app.get("/", tags=["Maths"])
def default_route():
    return "Hello World"

@app.get("/square", tags=["Maths"])
def square( n: int=1):
    return n*n

from pydantic import BaseModel

class Data(BaseModel):
    name:str
    city:str

@app.post('/formulaire')
def formulaire(data: Data):

    data = dict(data)

    #Name
    name = data['name']

    #City

    city = data['city']

    return f"Helllo {name} from {city}"



    

# charger le model :
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

# structure de données pour la prédiction

class Prediction(BaseModel):
    Gender: str
    Age: int
    Graduated: str
    Profession: str
    Work_Experience: float
    Spending_Score: str
    Family_Size: float
    Segmentation: str


@app.post('/predict', tags=["Models"])
def predict(data: Prediction):
    data_dict = dict(data)

    df = pd.DataFrame([data_dict])

    pred = model.predict(df)

    prediction_value = int(pred[0])  

    return {prediction_value}

@app.post('/predict_file')
def upload_file(file:UploadFile=File(...)):
    df = pd.read_csv(file.file)

    if 'Gender' not in df.columns or 'Age' not in df.columns or 'Graduated' not in df.columns or 'Profession' not in df.columns or 'Work_Experience' not in df.columns or 'Spending_Score' not in df.columns or 'Family_Size' not in df.columns or 'Segmentation' not in df.columns:
        return False
    else:
        X = df.drop(["Ever_Married"], axis=1).dropna()
        pred = model.predict(X)

        return [int(x) for x in pred]

client = MlflowClient('https://quera-server-mlflow-cda209265623.herokuapp.com/')
model_path = client.get_registered_model('Ever_Married').latest_versions[0].source
model_mlflow = pyfunc.load_model(model_path)
@app.post('/predict_mlflow', tags=["Models"])
def predict_mlflow(data: Prediction):
    data_dict = dict(data)

    df = pd.DataFrame([data_dict])
    pred = model_mlflow.predict(df)

    prediction_value = int(pred[0])  

    return {prediction_value}

model_mnist_path = client.get_registered_model('Mnist_Felicien').latest_versions[0].source
model_mnist = pyfunc.load_model(model_mnist_path)
@app.post('/predict_mnist', tags=["Models"])
def predict_mnist(file:UploadFile=File(...)):
    #img
    img = file.file
    img = np.frombuffer(img.read(), np.uint8)
    img = img.reshape((1, 28, 28))

    pred = model_mnist.predict(img)

    prediction_value = int(pred[0])

    return {prediction_value}
