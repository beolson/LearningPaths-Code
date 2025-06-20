from fastapi import FastAPI
from openai import OpenAI

app = FastAPI()
openai_client = OpenAI(api_key="")

@app.get("/")
def root_controller():
    return {"status":"healthy"}

@app.get("/chat")
def chat_controller(propmt: str = "inspire me"):
    response = openai_client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": propmt}
        ],
    )
    statement = response.choices[0].message.content
    return {"statement": statement}


from pydantic import BaseModel, Field, EmailStr, field_validator

class UserCreate(BaseModel):
    username: str
    password: str

    @field_validator("password")
    def validate_password(cls, value):
        if len(value) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit")
        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain at least one uppercase letter")
        return value
    
@app.post("/users")
async def create_user_controller(user: UserCreate):
    return {"name": user.username, "message": "Account created successfully"}