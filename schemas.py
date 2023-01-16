from pydantic import BaseModel, Field


class Todo(BaseModel):
    title: str
    description: str
    priority: int = Field(gt=0, lt=6, description='The priority must be between 1-5')
    complete: bool


class UserVerification(BaseModel):
    username: str
    password: str
    new_password: str

