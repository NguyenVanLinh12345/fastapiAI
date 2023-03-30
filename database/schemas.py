from pydantic import BaseModel

class Info(BaseModel):
    id: int
    name: str
    path: str

    class Config:
        orm_mode = True