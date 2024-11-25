from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from mangum import Mangum

app = FastAPI()

# In-memory storage for users
users = []

class User(BaseModel):
    id: Optional[int] = None
    name: str
    email: str

class UserCreate(BaseModel):
    name: str
    email: str

@app.get("/")
def read_root():
    return {"message": "Welcome to the User Management API"}

@app.get("/users", response_model=List[User])
def get_users():
    return users

@app.post("/users", response_model=User)
def create_user(user: UserCreate):
    new_user = User(id=len(users) + 1, **user.dict())
    users.append(new_user)
    return new_user

@app.get("/users/{user_id}", response_model=User)
def get_user(user_id: int):
    user = next((user for user in users if user.id == user_id), None)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Handler for Vercel
handler = Mangum(app)

