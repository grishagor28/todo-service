from datetime import datetime
from typing import Optional
from pydantic import BaseModel, field_validator

VALID_PRIORITIES = {"low", "medium", "high"}

class CategoryCreate(BaseModel):
    name: str

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, value):
        if not value.strip():
            raise ValueError("Название категории не может быть пустым")
        return value.strip()

class CategoryResponse(BaseModel):
    id: int
    name: str

    model_config = {"from_attributes": True}

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    priority: Optional[str] = "medium"
    deadline: Optional[datetime] = None
    category_id: Optional[int] = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, value):
        if not value.strip():
            raise ValueError("Название задачи не может быть пустым")
        return value.strip()

    @field_validator("priority")
    @classmethod
    def priority_must_be_valid(cls, value):
        if value not in VALID_PRIORITIES:
            raise ValueError("Приоритет должен быть: low, medium или high")
        return value

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    done: Optional[bool] = None
    priority: Optional[str] = None
    deadline: Optional[datetime] = None
    category_id: Optional[int] = None

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, value):
        if value is not None and not value.strip():
            raise ValueError("Название задачи не может быть пустым")
        if value is not None:
            return value.strip()
        return value

    @field_validator("priority")
    @classmethod
    def priority_must_be_valid(cls, value):
        if value is not None and value not in VALID_PRIORITIES:
            raise ValueError("Приоритет должен быть: low, medium или high")
        return value

class TaskResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str]
    done: bool
    priority: str
    deadline: Optional[datetime]
    category_id: Optional[int]
    category: Optional[CategoryResponse]
    created_at: datetime

    model_config = {"from_attributes": True}
