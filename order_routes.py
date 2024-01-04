from typing import List
from Routes.auth_routes import get_current_user
from fastapi import APIRouter, Depends
from Database.database import Session, get_db
from Models.models import Order
from Schemas.schemas import PizzaOrder, OrderResponse, GetYourOrder, UpdateField
from fastapi.exceptions import HTTPException

order_router = APIRouter(tags=["Order Details"])


@order_router.post('/place-order', response_model=GetYourOrder)
async def user(pizza_details: PizzaOrder, user_data: dict = Depends(get_current_user),
               session: Session = Depends(get_db)):
    if user_data is None:
        raise HTTPException(status_code=401, detail='Authentication failed')

    new_user = Order(
        quantity=pizza_details.quantity,
        pizza_size=pizza_details.pizza_size
    )

    session.add(new_user)
    session.commit()

    return new_user


@order_router.get('/list-all-orders', response_model=List[OrderResponse])
async def get_all_orders(user_data: dict = Depends(get_current_user),
                         session: Session = Depends(get_db)):
    if user_data is None:
        raise HTTPException(status_code=401, detail='Authentication failed')

    if user_data:
        if user_data.get('is_staff') == "True":
            query = session.query(Order).all()
            return query

        else:
            raise HTTPException(status_code=400, detail="Not a staff member")

    else:
        raise HTTPException(status_code=500, detail="Error getting logged-in user Information")


@order_router.get('/check-your-order-status/{order_id}', response_model=GetYourOrder)
async def check_your_order_status(order_id: int, user_data: dict = Depends(get_current_user),
                                  session: Session = Depends(get_db)):
    if user_data is None:
        raise HTTPException(status_code=401, detail='Authentication failed')

    order_id_check = session.query(Order).filter(Order.id == order_id).first()

    if order_id_check:
        return order_id_check

    else:
        raise HTTPException(status_code=404, detail=f"Order with {order_id} not found")


@order_router.put("/orders/{order_id}/update-field/")
async def update_order_field(
        order_id: int,
        field_update: UpdateField,
        user_data: dict = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    if user_data is None:
        raise HTTPException(status_code=401, detail='Authentication failed')

    order = db.query(Order).filter(Order.id == order_id).first()

    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.quantity = field_update.quantity
    order.pizza_size = field_update.pizza_size

    db.commit()

    return {"message": "Order updated successfully"}
