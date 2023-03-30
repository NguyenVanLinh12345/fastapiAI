from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, LargeBinary

from .database import Base

class Vector(Base):
    __tablename__='vector'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    path = Column(String)
    vector = Column(LargeBinary)