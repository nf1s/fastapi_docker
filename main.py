import uvicorn
from fastapi import FastAPI, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

SQLALCHEMY_DATABASE_URL = "postgresql://postgres:postgres@postgres/postgres"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, unique=True, index=True)
    last_name = Column(String)
    age = Column(Integer,)


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


class UserSchema(BaseModel):
    first_name: str
    last_name: str = None
    age: int

    class Config:
        orm_mode = True


@app.post("/user/", response_model=UserSchema)
async def create_user(user: UserSchema, db: Session = Depends(get_db)):
    _user = UserModel(
        first_name=user.first_name, last_name=user.last_name, age=user.age
    )
    db.add(_user)
    db.commit()
    db.refresh(_user)
    return _user


@app.get("/user/", response_model=UserSchema)
async def get_user(first_name: str, db: Session = Depends(get_db)):
    _user = db.query(UserModel).filter_by(first_name=first_name).first()
    return _user


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
