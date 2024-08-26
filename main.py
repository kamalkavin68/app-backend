from dotenv import load_dotenv
load_dotenv("src/config/.env")
from src.database.dbConnect import *

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from src.routers.indexRouter import indexRouter


app = FastAPI()

origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(indexRouter)


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)