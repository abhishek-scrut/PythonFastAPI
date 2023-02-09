from fastapi import APIRouter, Depends, status, HTTPException
from .. import schemas, models, database
from typing import List
from sqlalchemy.orm import Session

# instanciate the router
router = APIRouter()

# define all the routes for the blog
@router.post('/blog', status_code=status.HTTP_201_CREATED, response_model=schemas.ShowBlog, tags=['Blog'])
def create_blog(request: schemas.Blog, db: Session = Depends(database.get_db)):
    new_blog = models.Blog(title=request.title, content=request.content, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@router.get('/blogs',status_code=status.HTTP_200_OK, response_model=List[schemas.ShowBlog], tags=['Blog'])
def get_all_blogs(db: Session = Depends(database.get_db)):
    blogs = db.query(models.Blog).all()
    return blogs

@router.get('/blogs/{blog_id}', status_code=status.HTTP_200_OK, response_model=schemas.ShowBlog, tags=['Blog'])
def get_blog(blog_id: int, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter_by(id=blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id {blog_id} not found')
    return blog

@router.delete('/blogs/{blog_id}', status_code=status.HTTP_204_NO_CONTENT, tags=['Blog'])
def delete_blog(blog_id: int, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter_by(id=blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id {blog_id} not found')
    db.delete(blog)
    db.commit()
    return blog

@router.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED, response_model=schemas.ShowBlog, tags=['Blog'])
def update_blog(blog_id: int, request: schemas.Blog, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter_by(id=blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'blog with id {blog_id} not found')
    blog.title = request.title
    blog.content = request.content
    db.commit()
    db.refresh(blog)
    return blog