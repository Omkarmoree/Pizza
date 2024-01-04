from typing import Optional

from pydantic import BaseModel


class SignUpModel(BaseModel):
    username: str
    email: str
    password: str
    is_staff: str


class LoginModel(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    username: str
    password: str


class UserDetails(BaseModel):
    username: str


class PizzaOrder(BaseModel):
    quantity: int
    pizza_size: Optional[str] = "SMALL"


class OrderResponse(BaseModel):
    id: int
    quantity: int
    order_status: Optional[str] = "PENDING"
    pizza_size: Optional[str] = "SMALL"


class GetYourOrder(BaseModel):
    id: int
    order_status: Optional[str] = "PENDING"


class UpdateField(BaseModel):
    quantity: int
    pizza_size: Optional[str] = "SMALL"
