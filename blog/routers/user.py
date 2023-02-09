from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, models, database
from ..hashing import Hash
from sqlalchemy.orm import Session

# instanciate the router
router = APIRouter()

# define all the routes for the user
@router.post('/user', status_code=status.HTTP_201_CREATED, tags=['User'])
def create_user(request: schemas.UserBase, db: Session = Depends(database.get_db)):
    new_user = models.User(name=request.user, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/users', status_code=status.HTTP_302_FOUND, tags=['User'])
def get_all_users(db: Session = Depends(database.get_db)):
    users = db.query(models.User).all()
    return users

@router.get('/users/{user_id}', status_code=status.HTTP_302_FOUND, tags=['User'])
def get_user(user_id: int, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter_by(id=user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'user with id {user_id} not found')
    return user