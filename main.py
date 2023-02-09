from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()

@app.get('/blog')
def index(limit: int = 10, published: bool = False, sort: Optional[str] = None):
    if published:
        return {'data': f'{limit} published blogs from the db'}
    return {'data': f'{limit} blogs from the db'}

@app.get('/blog/unpublished')
def unpublished():
    return {'data': 'all unpublished list'}

@app.get('/blog/{id}')
def show_blog(id: int):
    # fetch blog with given id
    return {'data': id}

@app.get('/blog/{id}/comments')
def show_comments(id, limit: int = 10, sort: Optional[str] = None):
    # fetch comments of blog with given id
    return {'data' : ['c1', 'c2', {limit}, {id}]}


class Blog(BaseModel):
    id: int
    title: str
    description: str
    published: Optional[bool] = False

@app.post('/blog')
def create_blog(request: Blog):
    # return request
    return {'data': f'blog is created as {request.title}'}


# if __name__ == '__main__':
#     uvicorn.run(app, host='127.0.0.1', port=9000)