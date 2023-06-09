from app import  models, schemas
from typing import List, Any
from fastapi import APIRouter,HTTPException,Depends
from fastapi.responses import JSONResponse
from app.database import SessionLocal
from sqlalchemy.orm import Session
from app.models import User
from app.crud import user
from app.apis import deps
from app.schemas.user import (
    UserRead,UserCreate,UserUpdate
)
from app.database import get_db
from app.core.security import get_password_hash

router = APIRouter()

@router.get("/", response_model=List[UserRead])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.User = Depends(deps.get_current_active_superuser)
) -> Any:
    """
    Retrieve users.
    """
    users = user.get_multi(db, skip=skip, limit=limit)
    return users



@router.post("/create/", response_model = UserCreate)
def create_user(user: UserCreate,  
                db: Session = Depends(get_db),
                current_user: models.User = Depends(deps.get_current_active_superuser)
                ):
                
    existing_user = db.query(User).filter(User.email == user.email).first()

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )
    db_obj = User(
            full_name = user.full_name,
            email = user.email,
            hashed_password = get_password_hash(user.password),
            is_superuser = user.is_superuser,
        )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return JSONResponse(content={"message": "User created successfully"})





