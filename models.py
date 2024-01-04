from Database.database import Base
from sqlalchemy import Column, String, Integer, Text


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(25), unique=True)
    email = Column(String(80), unique=True)
    password = Column(Text, nullable=True)
    is_staff = Column(String)

    def __repr__(self):
        return f"<User {self.username}>"


class Order(Base):

    __tablename__ = 'orders'

    id = Column(Integer, primary_key=True)
    quantity = Column(Integer, nullable=True)
    order_status = Column(String, default="PENDING")
    pizza_size = Column(String, default="SMALL")

    def __repr__(self):
        return f"<Order {self.id}>"
