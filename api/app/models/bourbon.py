from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Bourbon(Base):
    __tablename__ = "bourbons"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    proof = Column(String)