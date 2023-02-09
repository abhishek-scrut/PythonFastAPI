from fastapi import FastAPI
from . import models
from .database import engine
from .routers import blog, user

# instantiate app
app = FastAPI()

# bind to all database & create it
models.Base.metadata.create_all(bind=engine)

# include all the routes
app.include_router(blog.router)
app.include_router(user.router)

@app.get("/health", tags=['Status'])
async def root():
    return {"status": "active"}