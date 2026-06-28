from sqlalchemy.orm import Session
from app.db import models

# Category CRUD
def create_category(db: Session, title: str):
    db_category = models.Category(title=title)
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category

def get_categories(db: Session):
    return db.query(models.Category).all()

# Book CRUD
def create_book(db: Session, title: str, description: str, price: float, category_id: int, url: str = ""):
    db_book = models.Book(title=title, description=description, price=price, url=url, category_id=category_id)
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

def get_books(db: Session):
    return db.query(models.Book).all()
    #  UPDATE (Обновление) 
def update_category(db: Session, category_id: int, new_title: str):
    """Обновляет название категории по её ID."""
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if category:
        category.title = new_title
        db.commit()
        db.refresh(category)
    return category

def update_book(db: Session, book_id: int, title: str = None, description: str = None, price: float = None, url: str = None):
    """Обновляет поля книги по её ID."""
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book:
        if title is not None:
            book.title = title
        if description is not None:
            book.description = description
        if price is not None:
            book.price = price
        if url is not None:
            book.url = url
        db.commit()
        db.refresh(book)
    return book

# DELETE (Удаление) 
def delete_category(db: Session, category_id: int):
    """Удаляет категорию по ID. Возвращает True, если удаление было успешным."""
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if category:
        db.delete(category)
        db.commit()
        return True
    return False

def delete_book(db: Session, book_id: int):
    """Удаляет книгу по ID. Возвращает True, если удаление было успешным."""
    book = db.query(models.Book).filter(models.Book.id == book_id).first()
    if book:
        db.delete(book)
        db.commit()
        return True
    return False