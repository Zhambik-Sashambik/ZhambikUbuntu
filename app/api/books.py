from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from app.db.db import get_db
from app.db import crud
from app import schemas

router = APIRouter(prefix="/books", tags=["Books"])

@router.get("/", response_model=List[schemas.BookResponse])
def get_books(
    db: Session = Depends(get_db),
    category_id: Optional[int] = Query(None, description="Фильтр по ID категории")
):
    """Получить список всех книг, с возможностью фильтрации по категории"""
    if category_id:
        # Эту функцию нужно будет добавить в crud.py
        return crud.get_books_by_category(db, category_id)
    return crud.get_books(db)

@router.get("/{book_id}", response_model=schemas.BookResponse)
def get_book(book_id: int, db: Session = Depends(get_db)):
    """Получить книгу по ID"""
    db_book = crud.get_book(db, book_id)  # Эту функцию нужно будет добавить в crud.py
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.post("/", response_model=schemas.BookResponse, status_code=status.HTTP_201_CREATED)
def create_book(book: schemas.BookCreate, db: Session = Depends(get_db)):
    """Создать новую книгу"""
    # Проверяем, существует ли категория
    db_category = crud.get_category(db, book.category_id)
    if db_category is None:
        raise HTTPException(status_code=400, detail="Category does not exist")
    return crud.create_book(db, book.title, book.description, book.price, book.category_id, book.url)

@router.put("/{book_id}", response_model=schemas.BookResponse)
def update_book(book_id: int, book_update: schemas.BookUpdate, db: Session = Depends(get_db)):
    """Обновить книгу"""
    # Проверяем, существует ли категория (если она передана)
    if book_update.category_id is not None:
        db_category = crud.get_category(db, book_update.category_id)
        if db_category is None:
            raise HTTPException(status_code=400, detail="Category does not exist")

    db_book = crud.update_book(
        db, book_id,
        title=book_update.title,
        description=book_update.description,
        price=book_update.price,
        url=book_update.url,
        # Обновление категории нужно будет добавить в crud.py
    )
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    """Удалить книгу"""
    success = crud.delete_book(db, book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")
    return