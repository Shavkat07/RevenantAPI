from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from datetime import datetime

# 1. Базовая схема (общее для всех остальных)
class UserBase(BaseModel):
    username: constr(strip_whitespace=True, min_length=3, max_length=150)
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None

# 2. Схема создания нового пользователя
class UserCreate(UserBase):
    password: constr(min_length=6, max_length=128)

# 3. Схема обновления пользователя (все поля необязательные)
class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    password: Optional[str] = None

# 4. Схема входа в систему (логин)
class UserLogin(BaseModel):
    username: str  # можно заменить на EmailStr если вход по email
    password: str

# 5. Публичная схема (без пароля)
class UserPublic(UserBase):
    id: int
    is_active: bool
    is_superuser: bool

    class Config:
        orm_mode = True  # позволяет напрямую работать с SQLAlchemy моделью

# 6. Полная схема пользователя из БД (для внутреннего использования)
class UserInDB(UserPublic):
    date_joined: datetime
    last_login: Optional[datetime] = None
    is_staff: bool

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    sub: str  # обычно это user_id
    exp: int  # срок действия

