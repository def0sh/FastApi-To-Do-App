from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Users
from routers.auth import get_user_exception, get_current_user, verify_password, get_password_hash
from schemas import UserVerification

router = APIRouter(prefix='/users', tags=['users'])


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


@router.get('/')
async def read_all(db: Session = Depends(get_db)):
    return db.query(Users).with_entities(
        Users.id,
        Users.first_name,
        Users.username,
        Users.email).all()


@router.get('/user/{user_id}')
async def user(user_id: int, db: Session = Depends(get_db)):
    user_model = db.query(Users).filter(Users.id == user_id)\
        .with_entities(Users.id, Users.first_name,
                       Users.username,Users.email).first()
    if user_model is None:
        return 'Invalid user id'
    return user_model


@router.put('/user/password')
async def user_password_change(user_verification: UserVerification,
                               user: dict = Depends(get_current_user),
                               db:Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()

    if user_model is not None:
        if user_verification.username == user_model.username and verify_password(
                user_verification.password,user_model.hashed_password):

            user_model.hashed_password = get_password_hash(user_verification.new_password)
            db.add(user_model)
            db.commit()
            return 'Successful'
        return 'Invalid user or request'


@router.delete('/user')
async def delete_user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    if user is None:
        raise get_user_exception()
    user_model = db.query(Users).filter(Users.id == user.get('id')).first()
    if user_model is None:
        return 'Invalid user or request'
    db.query(Users).filter(Users.id == user.get('id')).delete()
    db.commit()

    return 'Delete Successful'





