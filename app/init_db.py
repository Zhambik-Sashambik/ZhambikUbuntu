from app.db.db import SessionLocal, engine
from app.db import models, crud

def init_db():
    # Создаем таблицы (если их нет)
    models.Base.metadata.create_all(bind=engine)
    
    # Открываем сессию
    db = SessionLocal()
    try:
        # Проверяем, есть ли уже категории, чтобы не дублировать
        if not crud.get_categories(db):
            # Создаём категории
            cat1 = crud.create_category(db, "Python")
            cat2 = crud.create_category(db, "SQL")
            
            # Добавляем книги
            crud.create_book(db, "Изучаем Python", "Отличная книга для начинающих", 1500.0, cat1.id, "http://example.com/python")
            crud.create_book(db, "Python для анализа данных", "Продвинутые техники", 2000.0, cat1.id)
            crud.create_book(db, "PostgreSQL для начинающих", "Основы работы с БД", 1200.0, cat2.id)
            crud.create_book(db, "SQL запросы", "Практическое руководство", 1800.0, cat2.id)
            
            print("База данных инициализирована (добавлены категории и книги).")
        else:
            print("База данных уже содержит данные. Инициализация пропущена.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")
        # Если ошибка, откатываем изменения, чтобы не оставлять базу в неконсистентном состоянии
        db.rollback()
    finally:
        # ВАЖНО: закрываем сессию в любом случае
        db.close()

if __name__ == "__main__":
    init_db()