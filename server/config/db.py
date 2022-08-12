from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("mysql+pymysql://root:active36@localhost:3306/test")

meta = MetaData()
conn = engine.connect()
Base = declarative_base()
SessionLocal = sessionmaker(bind= engine, autocommit=False, autoflush=False)
# print (conn)

async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()