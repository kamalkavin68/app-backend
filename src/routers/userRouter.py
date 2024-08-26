from fastapi import APIRouter, Form, HTTPException, status
from datetime import timedelta
from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from src.database.dbConnect import UserTable, get_db
from src.schema.users import UserModel
from src.services.auth.userAuthManager import *
from sqlalchemy.orm import Session
userRout = APIRouter(prefix="/user")


@userRout.post("/token")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],DBsession: Session = Depends(get_db)) -> Token:
    
    username = form_data.username
    password = form_data.password

    userFilter = DBsession.query(UserTable).filter_by(username=username).first()

    if userFilter:
        if verify_password(password, userFilter.hashedPassword):
            pass
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
    else:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": userFilter.username, 
              "email":userFilter.email, 
              "isActive": userFilter.isActive, 
              "displayName": userFilter.displayName},
            expires_delta=access_token_expires)
    return Token(access_token=access_token, token_type="bearer")



@userRout.get("/users/me/", response_model=User)
async def read_users_me(current_user: Annotated[User, Depends(get_current_active_user)],):
    return current_user


@userRout.get("/users/me/items/")
async def read_own_items(current_user: Annotated[User, Depends(validateToken)],):
    return [{"item_id": "Foo", "owner": current_user.username}]

@userRout.post("/create")
async def create_user(
    DBsession: Annotated[Session, Depends(get_db)],
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
):

    print(username, email)
    newUser = UserTable(
        displayName=None,
        username=username,
        email=email,
        dob=None,
        hashedPassword=pwd_context.hash(password),
        isActive=False,
        createdAt=datetime.now(),
        lastLogin=None,
        loginAttempt=0
    )
    userFilter = DBsession.query(UserTable).filter_by(username=username).first()
    emailFilter = DBsession.query(UserTable).filter_by(email=email).first()
    if userFilter:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"username: {username} already taken, try other name"
        )
    else:
        if emailFilter:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"email: {email} already taken, try other email"
            )
        else:
            DBsession.add(newUser)
            DBsession.commit()

    return {"detail":"User Registered Successful!"}
