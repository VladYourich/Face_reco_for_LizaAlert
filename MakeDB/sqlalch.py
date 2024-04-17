import sqlite3
from sqlalchemy import create_engine, Column, Integer, String, BLOB, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker
from sqlalchemy.types import TypeDecorator, PickleType
# from enveronments import fill_callnames, СALLSIGN_ID, СALLSIGN_NAME
import numpy as np
import pickle

Base = declarative_base()

class PickleTypeDecorator(TypeDecorator):
    impl = BLOB

    def process_bind_param(self, value, dialect):
        if value is not None:
            return pickle.dumps(value)

    def process_result_value(self, value, dialect):
        if value is not None:
            return pickle.loads(value)

class Callsign(Base):
    __tablename__ = 'callsign'

    id = Column(Integer, primary_key=True)
    callname = Column(String, unique=True, nullable=False)

class Vector(Base):
    __tablename__ = 'vectors'

    id = Column(Integer, primary_key=True)
    vector = Column(PickleTypeDecorator)
    #vector = Column(BLOB, nullable=False)
    #img = Column(BLOB, unique=True, nullable=True)
    call_id = Column(Integer, ForeignKey('callsign.id'))
    call = relationship('Callsign', back_populates='vectors')

Callsign.vectors = relationship('Vector', order_by=Vector.call_id, back_populates='call')

# Создание базы данных
engine = create_engine('sqlite:///la.db', echo=False)
Base.metadata.create_all(bind=engine)

def sess():
    # Создание сессии для работы с базой данных
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def add_vector(id, callvector): #, callname

    ses = sess()

    # Добавление записей в таблицы
    #call = Callsign(callname=callname)
    vector = Vector(call_id=id, vector=callvector) #, call=call

    ses.add_all([vector]) #call, 
    ses.commit()

def add_many_vectors(items):
    ses = sess()
    # Добавление записей списком. Пример содержимого items
    # data_to_add = [
    #     {'callname': 'ГБ', 'vector': [0.7, 0.8, 0.9]},
    #     {'callname': 'Физрук', 'vector': [1.0, 1.1, 1.2]},
    # ]

    for data in items:
        call_id = get_id_for_calname(data['callname'])
        vector = Vector(vector=data['vector'], id=call_id)
        ses.add_all([vector])

    ses.commit()

def add_items_to_callsign(items):
    ses = sess()
    # Добавление записей списком. Пример содержимого items
    # data_to_add = [
    #     {'id': 1,'callname': 'ГБ'},
    #     {'id': 2,'callname': 'ВК74'},
    # ]

    for data in items:
        call = Callsign(id=data['id'], callname=data['callname'])
        ses.add_all([call])

    ses.commit()    

def get_vectors(callid) -> list:
    # Запрос к базе для получения списка значений vector с фильтром по callname
    #global СALLSIGN_ID
    ses = sess()

    vectors_for_callname = (
        ses.query(Vector.vector)
        #.join(Vector.call)
        .filter(Vector.call_id == callid)
        .all()
    )
    #print(f'Vectors for callname {СALLSIGN_ID[callid]}: {vectors_for_callname}')
    return vectors_for_callname

def get_id_for_calname(callname) -> int: 
    ses = sess()
    # Запрос к базе для получения получения всех позывных call_id
    result = (ses.query(Callsign.id).filter(Callsign.callname == callname).one())
    return result.id




