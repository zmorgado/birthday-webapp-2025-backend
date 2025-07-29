
import logging
from fastapi import FastAPI, Depends, HTTPException
from fastapi.concurrency import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from typing import List
import sys
import os
import uvicorn


sys.path.append(os.path.dirname(os.path.abspath(__file__)))


from models import init_db, RSVP, SessionLocal
from config import Config


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        logger.info("Initializing database...")
        init_db()  # Initialize the database during startup
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.exception(f"Exception during startup: {e}")
        # Optionally, re-raise to crash the app if DB is critical
        raise
    yield  # Perform any cleanup if necessary


# Pass the lifespan handler to the FastAPI app
app = FastAPI(lifespan=lifespan)


# Add CORS middleware
origins = [
    "https://cumplepelusa.vercel.app",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Dependency to verify admin credentials
security = HTTPBasic()
def verify_admin(credentials: HTTPBasicCredentials = Depends(security)):
    if credentials.password != Config.ADMIN_PASSWORD:
        raise HTTPException(status_code=401, detail="Invalid password")


# Pydantic model for RSVP submissions
class RSVPRequest(BaseModel):
    name: str = Field(..., min_length=1, description="Name must be non-empty")
    dinner_confirmed: bool
    party_confirmed: bool


# Minimal root GET route for health check
@app.get("/")
async def root():
    return {"message": "API is running"}


@app.post("/rsvp")
async def submit_rsvp(rsvp: RSVPRequest, db: Session = Depends(get_db)):
    new_rsvp = RSVP(
        name=rsvp.name,
        dinner_confirmed=rsvp.dinner_confirmed,
        party_confirmed=rsvp.party_confirmed
    )
    db.add(new_rsvp)
    db.commit()
    return {"message": "RSVP submitted successfully"}

@app.get("/admin", dependencies=[Depends(verify_admin)])
async def admin_dashboard(db: Session = Depends(get_db)):
    rsvps = db.query(RSVP).all()
    return rsvps

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)