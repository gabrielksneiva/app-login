from pymongo import MongoClient


client = MongoClient('mongodb://localhost:27017/')
db = client['my_database']
collection = db['users']


def check_existing_username(username: str) -> bool:
    """Verifica se um nome de usuário já existe no banco de dados."""
    return bool(collection.find_one({"username": username}))

def insert_user(user_data: dict) -> None:
    """Insere um novo usuário no banco de dados."""
    collection.insert_one(user_data)

def check_user_credentials(username: str, password: str) -> dict:
    """Verifica as credenciais de um usuário no banco de dados."""
    return collection.find_one({"username": username, "password": password})

from bson import ObjectId

def get_user_data(username: str) -> dict:
    """Obtém os dados do usuário com base no username."""
    user_data = collection.find_one({"username": username})
    if user_data:
        # Remove a senha e o _id do dicionário antes de retornar
        user_data.pop("password", None)
        user_data.pop("_id", None)
        return user_data
    else:
        return None


def collection_update_one(username:str, update_fields: dict)->bool:
    try:
        user_document = collection.find_one({"username": username})

        # Obtendo o _id do documento
        user_id = user_document["_id"]
        print(f'User_id = {user_id}')
        # Adiciona os campos de endereço com valores vazios se não estiverem presentes nas atualizações        
        update_query = {"$set": update_fields}
        result = collection.find_one_and_update({'username': username}, {'$set': update_fields})
        
        if len(result)> 1:
            return True
        else:
            print("Failed to update document: No document modified")
            return False
    except Exception as e:
        print(f"Error updating document: {e}")
        return False