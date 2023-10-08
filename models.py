# models.py

from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Podcast(Base):
    __tablename__ = 'podcasts'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    description = Column(String)
    download_folder = Column(String)
    xml_url = Column(String)
    episodes = relationship("Episode", back_populates="podcast")

    def _list_xml_content(self):
        ...
class Config(Base):
    __tablename__ = 'config'
    id = Column(Integer, primary_key=True)
    root_download_folder = Column(String)


class Episode(Base):
    __tablename__ = 'episodes'

    id = Column(Integer, primary_key=True)
    number = Column(Integer)
    title = Column(String)
    description = Column(String)
    date_uploaded = Column(DateTime)
    link = Column(String)
    url = Column(String)
    file_path = Column(String)
    podcast_id = Column(Integer, ForeignKey('podcasts.id'))

    podcast = relationship("Podcast", back_populates="episodes")

class DownloadPath(Base):
    __tablename__ = 'download_paths'

    id = Column(Integer, primary_key=True)
    episode_id = Column(Integer, ForeignKey('episodes.id'))
    path = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

# Initialize the SQLite database engine
engine = create_engine('sqlite:///podcast_downloads.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
