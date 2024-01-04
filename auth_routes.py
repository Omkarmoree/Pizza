from datetime import timedelta, datetime
import jwt
from fastapi import APIRouter, Depends, status
from jose import JWTError
from Database.database import Session, get_db
from Schemas.schemas import SignUpModel
from Models.models import User
from fastapi.exceptions import HTTPException
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from typing import Annotated

auth_router = APIRouter(tags=["Authentication"])


SECRET_KEY = '5388a162b7db122b1d0f4caeb49b7b0f7613052bd572b79182b58927bf245bc9'
ALGO = 'HS256'

oauth2_bearer = OAuth2PasswordBearer(tokenUrl='token')
bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


@auth_router.post('/signup', response_model=SignUpModel, status_code=status.HTTP_200_OK)
async def signup(user: SignUpModel, session: Session = Depends(get_db)):
    db_email = session.query(User).filter(User.email == user.email).first()

    if db_email is not None:
        return HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )

    new_user = User(
        username=user.username,
        email=user.email,
        password=bcrypt_context.hash(user.password),
        is_staff=user.is_staff
    )

    session.add(new_user)
    session.commit()

    return new_user


def create_access_token(username: str, is_staff: str, expires: timedelta):
    encode = {'sub': username, 'is_staff': is_staff}
    expires = datetime.utcnow() + expires
    encode.update({'exp': expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGO)


@auth_router.post('/token')
async def login_for_access_token(from_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 session: Session = Depends(get_db)):
    user = session.query(User).filter(User.username == from_data.username).first()

    if not user:
        return False

    if not bcrypt_context.verify(from_data.password, user.password):
        return False

    if not user:
        raise HTTPException(status_code=404,
                            detail='could not validate user')

    token = create_access_token(user.username, user.is_staff, timedelta(minutes=20))

    return {'access_token': token, 'token_type': 'bearer'}


async def get_current_user(token: str = Depends(oauth2_bearer)) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGO])
        username: str = payload.get('sub')
        is_staff: str = payload.get('is_staff')

        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

        return {'is_staff': is_staff}

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
