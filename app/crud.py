from typing import Optional
from sqlalchemy.orm import Session
from app.models import Task, Category
from app.schemas import TaskCreate, TaskUpdate, CategoryCreate


def get_tasks(db: Session, user_id: int, done: Optional[bool] = None, category_id: Optional[int] = None):
    query = db.query(Task).filter(Task.user_id == user_id)
    if done is not None:
        query = query.filter(Task.done == done)
    if category_id is not None:
        query = query.filter(Task.category_id == category_id)
    return query.order_by(Task.created_at.desc()).all()


def get_task(db: Session, task_id: int, user_id: int):
    return db.query(Task).filter(Task.id == task_id, Task.user_id == user_id).first()


def create_task(db: Session, user_id: int, task_data: TaskCreate):
    new_task = Task(
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        deadline=task_data.deadline,
        category_id=task_data.category_id,
    )
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


def update_task(db: Session, task_id: int, user_id: int, task_data: TaskUpdate):
    task = get_task(db, task_id, user_id)
    if not task:
        return None
    update_fields = task_data.model_dump(exclude_unset=True)
    for field, value in update_fields.items():
        setattr(task, field, value)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int, user_id: int):
    task = get_task(db, task_id, user_id)
    if not task:
        return False
    db.delete(task)
    db.commit()
    return True


def get_categories(db: Session, user_id: int):
    return db.query(Category).filter(Category.user_id == user_id).all()


def get_category(db: Session, category_id: int, user_id: int):
    return db.query(Category).filter(Category.id == category_id, Category.user_id == user_id).first()


def create_category(db: Session, user_id: int, category_data: CategoryCreate):
    new_category = Category(
        user_id=user_id,
        name=category_data.name,
    )
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


def delete_category(db: Session, category_id: int, user_id: int):
    category = get_category(db, category_id, user_id)
    if not category:
        return False
    db.delete(category)
    db.commit()
    return True