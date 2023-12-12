
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
def create_user(user: str, email: str, dias_semana:int):
    # Verificar se o usuário já existe
    if db.users.find_one({"user": user, "email": email, "dias_semana":dias_semana  }):
        raise HTTPException(status_code=400, detail="Email already registered")

    # jogar usuário no mongo
    user_data = {"user": user, "email": email, "dias_semana":dias_semana}
    result = db.users.insert_one(user_data)
    raise HTTPException(status_code=200, detail="Email registered")
    
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
    # Verificar se o usuário existe
    existing_user = db.users.find_one({"user": user})
    if not existing_user:
        raise HTTPException(status_code=404, detail=f"User {user} not found")

    db.users.delete_one({"user": user})
    return {"message": f"User {user} deleted successfully"}


@app.put("/users", response_model=dict)
def update_user(user: str, email: str, dias_semana: int):
    
    existing_user = db.users.find_one({"user": user})
    if not existing_user:
        raise HTTPException(status_code=404, detail=f"User {user} not found")

    
    updated_data = {"$set": {"email": email, "dias_semana": dias_semana}}
    db.users.update_one({"user": user}, updated_data)

    
    return {"user": user, "email": email, "dias_semana": dias_semana}


