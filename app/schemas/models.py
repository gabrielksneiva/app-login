from pydantic import BaseModel

class UserRegistry(BaseModel):
    username: str
    password: str
    email: str
    cep: str
    cpf: str

class User(BaseModel):
    username: str
    password: str

# def register(user: UserRegistry):
#     return {"username": user.username,
#             "password": user.password,
#             "email": user.email,
#             "cep": user.cep,
#             "cpf": user.cpf}