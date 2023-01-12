from sqlalchemy import TIMESTAMP, Column, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from cfg import DB_CONNSTR

engine = create_engine(DB_CONNSTR) 
Base = declarative_base()

TABLENAME = 'tracks_historial'

class Historial(Base):
    __tablename__ = TABLENAME

    played_at = Column(TIMESTAMP, primary_key=True)
    track = Column(String(255), nullable=False)
    artist = Column(String(255), nullable=False)

