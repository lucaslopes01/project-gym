

from fastapi import FastAPI, HTTPException
import uvicorn
from pymongo import MongoClient
from pydantic import BaseModel
from bson import ObjectId, json_util
from typing import List, Optional



app = FastAPI()
client = MongoClient("mongodb://localhost:27017/")
db = client["treino"]  



# cria usuario
@app.post("/user", response_model=dict )
def create_user(user:str, sex: str):
    # Verificar se o usuário já existe
    if db.users.find_one({"user": user}):
        raise HTTPException(status_code=400, detail="User already registered")

    # jogar usuário no mongo
    user_data = {"user": user, "sex": sex }
    result = db.users.insert_one(user_data)
    raise HTTPException(status_code=200, detail="User registered")
@app.post("/planilha")
def planilha(data:dict):
    result = list(db.users.find({'dias_semana':data['dias_semana']}, {'_id':False}))
    if result:
        return result[0]
    else:
        return 'não temos planilha para esses dias, vamos elaborar e enviar'
@app.get("/user")
def get_users():
    # Retorna informações sobre todos os usuários no banco de dados
    
    users = list(db.users.find({}))
    for user in users:
        user["_id"] = str(user["_id"])
    return users

@app.delete("/user", response_model=dict)
def delete_user(user: str):
    # faz a verificação pra ver se o usuário existe
    existing_user = db.users.find_one({"user": user})
    if not existing_user:
        raise HTTPException(status_code=404, detail=f"User {user} not found")

    db.users.delete_one({"user": user})
    return {"message": f"User {user} deleted successfully"}


@app.put("/user", response_model=dict)
def update_user(user:str, sex: str = None):
    
    existing_user = db.users.find_one({"user": user})
    if not existing_user:
        raise HTTPException(status_code=404, detail=f"User {user} not found")

    
    updated_data = {"$set": {"user": user, "sex": sex}}
    db.users.update_one({"user": user}, updated_data)

    
    return {"user": user, "sex": sex}

    #-----------------------------------------------//----------------------------------------------------------------------------------------------

    #endpoint para criar planilha de treino

    

@app.get("/spreadsheet")
def read_spreadsheet():
    spreadsheets = list(db.muscle.find({}, {'id': False}))


    return spreadsheets

@app.put("/spreadsheet", response_model=dict)
def update_spreadsheet(spreadsheet: str=None,  user: str=None, days_week: int=None, focus_muscle:str=None):
    existing_spreadsheet = db.muscle.find_one ({"spreadsheet": spreadsheet})
    if not existing_spreadsheet:
        raise HTTPException(status_code=400, detail=f"spreadsheet {spreadsheet} not found")
    updated_spreadsheet = {"$set": {"spreadsheet": spreadsheet, "user": user, "days_week":days_week, "focus_muscle":focus_muscle}}
    db.muscle.update_one({"spreadsheet": spreadsheet}, updated_spreadsheet)

    
    return {"spreadsheet": spreadsheet, "user": user, "days_week":days_week, "focus_muscle":focus_muscle}

@app.delete("/spreadsheet", response_model=dict)
def delete_spreadsheet(spreadsheet:str):

    existings_spreadsheet = db.muscle.find_one({"spreadsheet": spreadsheet})
    if not existings_spreadsheet:
        raise HTTPException(status_code=400, detail=f"spreadsheet {spreadsheet} not found")
    db.muscle.delete_one({"spreadsheet": spreadsheet})
    return {"message": f"spreadsheet {spreadsheet} deleted successfully"}



if __name__ == '__main__':
    
    uvicorn.run(app, host='0.0.0.0', port=8000)


