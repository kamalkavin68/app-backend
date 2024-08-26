from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Sequence, Text, create_engine, Date
from datetime import datetime
import os

DATABASE1_URL = f"""mysql+pymysql://{os.getenv('DB1_MYSQL_USER')}:{os.getenv('DB1_MYSQL_PASS')}@{os.getenv('DB1_MYSQL_HOST')}:{os.getenv('DB1_MYSQL_PORT')}/{os.getenv('DB1_MYSQL_DB')}"""

Base = declarative_base()
DBengin = create_engine(DATABASE1_URL)


class UserTable(Base):
    __tablename__ = "users"

    id = Column(Integer, Sequence("user_seq"), primary_key=True)
    displayName =  Column(String(225), nullable=True)
    username = Column(String(225), unique=True)
    email = Column(String(225), unique=True)
    dob = Column(Date, nullable=True)
    hashedPassword = Column(Text)
    isActive = Column(Boolean, default=True)
    createdAt = Column(DateTime, default=datetime.now)
    lastLogin = Column(DateTime, nullable=True)
    loginAttempt = Column(Integer, nullable=True)

    # def __repr__(self):
    #     return f"<User(username={self.username}, email={self.email})>"

Base.metadata.create_all(DBengin)


def get_db():
    Session = sessionmaker(bind=DBengin)
    DBsession = Session()
    try:
        yield DBsession
    finally:
        DBsession.close()