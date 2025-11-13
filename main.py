from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session
from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./ecolife.db")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)
Base = declarative_base()

app = FastAPI(title="EcoLife Carbon Tracker API")

# Database Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    activities = relationship("Activity", back_populates="user")

class Activity(Base):
    __tablename__ = "activities"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    electricity_kwh = Column(Float, default=0)
    travel_km = Column(Float, default=0)
    food_kg = Column(Float, default=0)
    carbon_kg = Column(Float, default=0)
    user = relationship("User", back_populates="activities")

Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Routes
@app.post("/users/")
def create_user(name: str, db: Session = Depends(get_db)):
    user = User(name=name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"message": "User created", "user_id": user.id}

@app.post("/activities/")
def log_activity(user_id: int, electricity_kwh: float = 0, travel_km: float = 0, food_kg: float = 0, db: Session = Depends(get_db)):
    carbon = electricity_kwh * 0.7 + travel_km * 0.12 + food_kg * 2.5
    activity = Activity(user_id=user_id, electricity_kwh=electricity_kwh, travel_km=travel_km, food_kg=food_kg, carbon_kg=carbon)
    db.add(activity)
    db.commit()
    return {"message": "Activity logged", "carbon_generated_kg": carbon}

@app.get("/summary/{user_id}")
def get_summary(user_id: int, db: Session = Depends(get_db)):
    total = db.query(Activity).filter(Activity.user_id == user_id).all()
    if not total:
        raise HTTPException(status_code=404, detail="User not found or no data")
    total_carbon = sum(a.carbon_kg for a in total)
    return {"user_id": user_id, "total_carbon_kg": total_carbon}
