from sqlalchemy import Column, String
import os
from LaylaRobot import BROADCAST_DB_URL as DB_URI
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

if DB_URI.startswith('postgres'):
    DB_URI = DB_URI.replace('postgres', 'postgresql', 1)


def start() -> scoped_session:
    engine = create_engine(DB_URI)
    BASE.metadata.bind = engine
    BASE.metadata.create_all(engine)
    return scoped_session(sessionmaker(bind=engine, autoflush=False))


try:
    BASE = declarative_base()
    SESSION = start()
except AttributeError as e:
    print("DB_URI is not configured. Features depending on the database might have issues.")
    print(str(e))


class broadcastbase(BASE):
    __tablename__ = "UserDB"
    chat_id = Column(String(14), primary_key=True)

    def __init__(self, chat_id):
        self.chat_id = chat_id


broadcastbase.__table__.create(checkfirst=True)


def add_to_broadcastbase(chat_id: int):
    __user = broadcastbase(str(chat_id))
    SESSION.add(__user)
    SESSION.commit()


def del_from_broadcastbase(chat_id: int):
    user = SESSION.query(broadcastbase).get(str(chat_id))
    SESSION.delete(user)
    SESSION.commit()


def full_broadcastbase():
    users = SESSION.query(broadcastbase).all()
    SESSION.close()
    return users


def present_in_broadcastbase(chat_id):
    try:
        return SESSION.query(broadcastbase).filter(
            broadcastbase.chat_id == str(chat_id)).one()
    except BaseException:
        return None
    finally:
        SESSION.close()
