from sqlalchemy import Column, Integer,  DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
Base = declarative_base()


class BaseTable(Base):
    __abstract__ = True
    id = Column(Integer, unique=True, index=True,
                primary_key=True, nullable=False)
    date_created = Column(DateTime, index=True,
                          default=datetime.utcnow)
    date_modified = Column(DateTime, nullable=True,
                           default=datetime.utcnow)
