from fastapi import APIRouter

from src.routers.userRouter import userRout


indexRouter = APIRouter(prefix="/api/v1")
indexRouter.include_router(userRout)
