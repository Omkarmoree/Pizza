from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

engine = create_engine('postgresql+psycopg2://postgres:root@localhost/postgres')
Base = declarative_base()
Session = sessionmaker(bind=engine)


def get_db():
    session = Session()
    try:
        yield session
    finally:
        session.close()