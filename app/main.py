from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.db.database import check_existing_username, check_user_credentials, insert_user, get_user_data, collection_update_one
import requests

app = FastAPI()

class User(BaseModel):
    username: str
    password: str
    email: str
    cep: str
    cpf: str

class Login(BaseModel):
    username:str
    password:str

def to_dict(username, password):
    {'username': username,
     'password': password}

@app.get('/user_info')
async def get_info(username: str):
    user_data = get_user_data(username)
    if user_data:
        return user_data
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


@app.post("/signup")
async def signup_user(user: User):
    if check_existing_username(user.username):
        raise HTTPException(status_code=400, detail="Username already exists")
    insert_user(user.dict())
    return {"type": "signup", "message": "User registered successfully"}

@app.post("/signin")
async def signin_user(data_login: Login):
    print("Received request data:", {"username":data_login.username, "password": data_login.password})

    user_data = check_user_credentials(data_login.username, data_login.password)
    if user_data:
        return {"type": "signin", "message": "Login successful"}
    
    raise HTTPException(status_code=401, detail="Invalid credentials")


@app.put("/users/{username}/update-address")
async def update_user_address(username: str):
    # Obter os dados do usuário do MongoDB
    user_data = get_user_data(username)
    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Obter o CEP do usuário
    cep = user_data.get("cep")
    if not cep:
        raise HTTPException(status_code=400, detail="User's CEP not found")
    
    # Fazer uma solicitação à API de CEP para obter as informações do endereço
    cep_response = requests.get(f"https://viacep.com.br/ws//{cep}/json/").json()
    if len(cep_response)<2:
        raise HTTPException(status_code=404, detail="CEP not found")
    # Atualizar os dados do usuário com as informações do endereço
    
    address_info = {
        "street": cep_response["logradouro"],
        "city": cep_response["localidade"],
        "state": cep_response['uf']
    }
    update_result = collection_update_one(username, address_info)

    # Verificar se a atualização foi bem-sucedida
    if type(update_result) == bool and update_result == True:
        return {"message": "User address updated successfully"}
    else:
        raise HTTPException(status_code=500, detail="Failed to update user address")

