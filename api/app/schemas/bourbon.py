from pydantic import BaseModel
from typing import Optional, List


class BourbonBase(BaseModel):
    name: str
    description: str
    proof: str


class BourbonCreate(BourbonBase):
    pass


class BourbonUpdate(BourbonCreate):
    pass


class BourbonInDB(BourbonUpdate):
    id: int
    name: str
    description: str
    proof: str

    class Config:
        orm_mode = True