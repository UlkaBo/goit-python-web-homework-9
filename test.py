from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from db import Base, metadata, session



class Test(Base):
    __tablename__ = 'testes'
    contact_id = Column('id', Integer, primary_key=True)
    note = Column('note', String(200), nullable=False)
    



def create_testes():
    c = Test(note = 'asd')
    session.add(c)
    session.commit()


create_testes()