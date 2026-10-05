from pydantic import BaseModel, Field

class ApplicationCreate(BaseModel):
    company: str = Field(min_length=2, max_length=60)
    role: str = Field(min_length=2, max_length=80)
    status: str
    applied_date: str

class Application(ApplicationCreate):
    id: int
