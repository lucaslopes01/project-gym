from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from bson import ObjectId

# Criando uma instância do aplicativo FastAPI
app = FastAPI()

# Conectar ao banco de dados MongoDB (substitua a string de conexão conforme necessário)
client = MongoClient("mongodb://localhost:27017/")
db = client["mongo"]  # Substitua "sua_base_de_dados" pelo nome do seu banco de dados

# Definindo um modelo Pydantic para os dados do usuário
class UserCreate(BaseModel):
    email: str
    username: str

# Endpoint para criar um novo usuário
@app.post("/users/", response_model=dict)
async def create_user(user: UserCreate):
    # Verificar se o usuário já existe
    if db.users.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="Email already registered")

    # Inserir novo usuário no MongoDB
    user_data = {"email": user.email, "username": user.username}
    result = db.users.insert_one(user_data)
    
    # Retornar os dados do usuário recém-criado
    return {"id": str(result.inserted_id), **user_data}
