from pydantic import BaseModel
from typing import List

class UserBase(BaseModel):
    user: str
    password: str
    email: str

class BlogBase(BaseModel):
    title: str
    content: str

class Blog(BlogBase):
    class Config():
        orm_mode = True

class ShowUser(BaseModel):
    user: str
    email: str
    blogs: List[Blog] = []
    class Config():
        orm_mode = True

class ShowBlog(BaseModel):
    title: str
    content: str
    # creator: ShowUser
    class Config():
        orm_mode = True