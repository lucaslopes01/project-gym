
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from bson import ObjectId, json_util
from typing import List
import json

app = FastAPI()
client = MongoClient("mongodb://localhost:27017/")
db = client["treino"]  

# cria usuario
@app.post("/users", response_model=dict )
def create_user(user:str, sexo: str, dias_semana:int, foco_grupamento:str = None):
    # Verificar se o usuário já existe
    if db.users.find_one({"user": user, "sexo": sexo, "dias_semana":dias_semana, "foco_grupamento":foco_grupamento  }):
        raise HTTPException(status_code=400, detail="Email already registered")

    # jogar usuário no mongo
    user_data = {"user": user, "sexo": sexo, "dias_semana":dias_semana, "foco_grupamento":foco_grupamento  }
    result = db.users.insert_one(user_data)
    raise HTTPException(status_code=200, detail="user registered")
    
    # retorna os dados
    return {"id": str(result.inserted_id), **user_data}
@app.get("/users")
def get_users():
    # Retorna informações sobre todos os usuários no banco de dados
    #precisei tirar o id da lista pois tal quando trazia ele não conseguia iterar
    users = list(db.users.find({}, {'_id': False}))
    return users

@app.delete("/users", response_model=dict)
def delete_user(user: str):
    # faz a verificação pra ver se o usuário existe
    existing_user = db.users.find_one({"user": user})
    if not existing_user:
        raise HTTPException(status_code=404, detail=f"User {user} not found")

    db.users.delete_one({"user": user})
    return {"message": f"User {user} deleted successfully"}


@app.put("/users", response_model=dict)
def update_user(user:str, sexo: str, dias_semana:int, foco_grupamento:str):
    
    existing_user = db.users.find_one({"user": user})
    if not existing_user:
        raise HTTPException(status_code=404, detail=f"User {user} not found")

    
    updated_data = {"$set": {"user": user, "sexo": sexo, "dias_semana":dias_semana, "foco_grupamento":foco_grupamento}}
    db.users.update_one({"user": user}, updated_data)

    
    return {"user": user, "sexo": sexo, "dias_semana":dias_semana, "foco_grupamento":foco_grupamento}


