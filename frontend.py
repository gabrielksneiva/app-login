import streamlit as st
import requests
from app.main import update_user_address
import pandas as pd

BASE_URL = "http://localhost:8000"
CEP_API_URL = "https://viacep.com.br/ws/"

def register_user():
    st.subheader("Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    email = st.text_input("Email")
    cep = st.text_input("CEP")
    cpf = st.text_input("CPF")
    if st.button("Register"):
        response = requests.post(f"{BASE_URL}/signup", json={"username": username, "password": password, "email": email, "cep": cep, "cpf": cpf}).json()
        if "message" in response:
            st.write(response["message"])
        else:
            st.error("An unexpected error occurred. Please try again later.")

def login_user():
    st.subheader("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        response = requests.post(f"{BASE_URL}/signin", json={"username": username, "password": password}).json()
        if response:
            user_data = requests.get(f"{BASE_URL}/user_info?username={username}").json()
        if len(user_data)>1:
            st.success("🎉 Login successful!")
            
            # Request to CEP API for address details
            cep_response = requests.get(f"https://viacep.com.br/ws/{user_data['cep']}/json/").json()
            if len(cep_response)>1:
                st.write("User Information:")
                user_info_table = {
                    "Username": user_data['username'],
                    "Email": user_data['email'],
                    "CEP": user_data['cep'],
                    "CPF": user_data['cpf'],
                    "Street": user_data['street'],
                    "City": user_data['city'],
                    "State": user_data['state']
                }
                user_info_table = pd.DataFrame({
                    "Attribute": ["Username", "Email", "CEP", "CPF", "Street", "City", "State"],
                    "": [user_data['username'], user_data['email'], user_data['cep'], user_data['cpf'], user_data['street'], user_data['city'], user_data['state']]
                })
                st.dataframe(user_info_table.set_index("Attribute"))
                user_update = requests.put(f"{BASE_URL}/users/{username}/update-address")
            else:
                st.warning("Could not retrieve address information for the provided CEP.")
        else:
            st.error("Invalid credentials")

def main():
    st.markdown("# Welcome to our Authentication System!")
    st.write("Please login or register to proceed.")

    page = st.radio("Navigation", ["Login", "Register"])

    if page == "Register":
        register_user()
    else:
        login_user()

if __name__ == "__main__":
    main()
