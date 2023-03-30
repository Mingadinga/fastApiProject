import os
from fastapi import FastAPI
from dotenv import load_dotenv
from pydantic import BaseModel
from mysql.connector import Error
import mysql.connector

app = FastAPI()
load_dotenv()

connection = mysql.connector.connect(
    host=os.getenv("HOST"),
    database=os.getenv("DATABASE"),
    user=os.getenv("USERNAME"),
    password=os.getenv("PASSWORD"),
    ssl_ca=os.getenv("SSL_CERT")
)

# connection = MySQLdb.connect(
#   host= os.getenv("HOST"),
#   user=os.getenv("USERNAME"),
#   passwd= os.getenv("PASSWORD"),
#   db= os.getenv("DATABASE"),
#   ssl_mode = "VERIFY_IDENTITY",
#   ssl      = {
#     'ca': os.getenv("SSL_CERT")
#   }
# )





@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}

class User(BaseModel):
    name: str
    age: int

@app.post("/users/")
async def create_user(user: User):
    # MySQL 쿼리 실행
    cursor = connection.cursor()
    sql = "INSERT INTO users (name, age) VALUES (%s, %s)"
    val = (user.name, user.age)
    cursor.execute(sql, val)
    connection.commit()
    return {"message": "User created successfully"}

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    # MySQL 쿼리 실행
    cursor = connection.cursor()
    sql = "SELECT name, age FROM users WHERE id=%s"
    cursor.execute(sql, (user_id,))
    result = cursor.fetchone()
    if result:
        name, age = result
        return {"id": user_id, "name": name, "age": age}
    else:
        return {"message": "User not found"}
