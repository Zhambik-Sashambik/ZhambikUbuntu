print("Hello, World!")

from app.db.db import SessionLocal
from app.db import crud

if __name__ == "__main__":
    db = SessionLocal()
    
    print("\n--- Данные из базы данных ---")
    
    # Выводим категории
    categories = crud.get_categories(db)
    print("Категории:")
    for cat in categories:
        print(f"- {cat.title}")
    
    # Выводим книги
    books = crud.get_books(db)
    print("\nКниги:")
    for book in books:
        print(f"- {book.title} ({book.price} руб.) -> {book.category.title}")
    
    db.close()