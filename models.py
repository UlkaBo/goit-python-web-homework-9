
from datetime import datetime, date, timedelta
#from faker import Faker

from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from db import Base, metadata, engine

class Abonent(Base):
    __tablename__ = 'abonents'
    abonent_id = Column('abonent_id', Integer, primary_key=True)
    name = Column('name', String(50), nullable=False)
    birthday = Column('birthday', DateTime, nullable=True)
    address = Column('address', String(100), nullable=True)

    phones = relationship("AbonentPhone", 
        back_populates="abonentp",
        cascade = "all, delete, delete-orphan")

class AbonentPhone(Base):
    __tablename__ = 'phones'

    phone_id = Column('phone_id', Integer, primary_key = True)
    phone = Column('phone', String(100), nullable=False)

    abonent_id = Column(Integer, ForeignKey('abonents.abonent_id'), nullable=True)
    abonentp = relationship("Abonent", back_populates = "phones")


if __name__ == '__main__':
    #x = engine.execute("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';")
    #print('___', x)
    Base.metadata.bind = engine
    Base.metadata.create_all(engine)
