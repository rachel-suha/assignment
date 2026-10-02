import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from sqlalchemy.orm import sessionmaker, DeclarativeBase

load_dotenv()

_raw_url = os.getenv("DATABASE_URL", "")

# Fall back to local SQLite if no valid DATABASE_URL is configured
_SQLITE_FALLBACK = "sqlite:///./placementpro.db"
if not _raw_url or _raw_url.startswith("paste-") or "YOUR_" in _raw_url:
    database_url = _SQLITE_FALLBACK
else:
    database_url = _raw_url

url = make_url(database_url)
connect_args = {}

if url.drivername in {"postgres", "postgresql"}:
    url = url.set(drivername="postgresql+psycopg")
elif url.drivername == "sqlite":
    connect_args["check_same_thread"] = False

engine = create_engine(url, connect_args=connect_args, pool_pre_ping=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
