from pydantic import BaseModel, EmailStr, validator
from datetime import date
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserModel(BaseModel):
    username: str
    email: str
    password: str

    @validator('password', pre=True)
    def hash_password_validator(cls, value):
        return pwd_context.hash(value)
