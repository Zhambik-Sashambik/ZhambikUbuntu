from app.db.db import SessionLocal, engine
from app.db import models, crud

models.Base.metadata.create_all(bind=engine)
db = SessionLocal()

# Создаём категории
cat1 = crud.create_category(db, "Python")
cat2 = crud.create_category(db, "SQL")

# Добавляем книги
crud.create_book(db, "Изучаем Python", "Отличная книга для начинающих", 1500.0, cat1.id, "http://example.com/python")
crud.create_book(db, "Python для анализа данных", "Продвинутые техники", 2000.0, cat1.id)
crud.create_book(db, "PostgreSQL для начинающих", "Основы работы с БД", 1200.0, cat2.id)
crud.create_book(db, "SQL запросы", "Практическое руководство", 1800.0, cat2.id)

print("База данных инициализирована.")