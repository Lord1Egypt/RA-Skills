"""Database runtime for persistent D&D domain state."""

from __future__ import annotations

import os
from collections.abc import Generator, Iterator
from contextlib import contextmanager
from pathlib import Path

from sqlalchemy import Engine, create_engine, event
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from .._paths import get_runtime_subdir


class Base(DeclarativeBase):
    """Declarative base shared by all D&D domain models."""


def default_database_url() -> str:
    """Return the configured URL or the instance-local SQLite database URL."""
    configured = os.environ.get("DND_DATABASE_URL") or os.environ.get("DATABASE_URL")
    if configured:
        return configured
    database_path = get_runtime_subdir("dnd") / "dnd_dm.db"
    return f"sqlite+pysqlite:///{database_path.as_posix()}"


class Database:
    """Own a D&D database engine and its transactional session factory."""

    def __init__(self, url: str | None = None, *, echo: bool = False) -> None:
        self.url = url or default_database_url()
        connect_args = {"check_same_thread": False} if self.url.startswith("sqlite") else {}
        self.engine: Engine = create_engine(
            self.url,
            connect_args=connect_args,
            pool_pre_ping=True,
            echo=echo,
        )
        if self.engine.dialect.name == "sqlite":
            event.listen(self.engine, "connect", self._enable_sqlite_foreign_keys)
        self.session_factory = sessionmaker(
            bind=self.engine,
            autoflush=False,
            expire_on_commit=False,
        )

    @staticmethod
    def _enable_sqlite_foreign_keys(dbapi_connection, _connection_record) -> None:
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON")
        cursor.close()

    def create_schema(self) -> None:
        """Create the current schema directly, primarily for isolated tests."""
        from ..db import models  # noqa: F401

        Base.metadata.create_all(bind=self.engine)

    def upgrade_schema(self, revision: str = "head") -> None:
        """Upgrade a persistent database through the bundled Alembic migrations."""
        from .migration import upgrade_database

        upgrade_database(self.url, revision=revision)

    def drop_schema(self) -> None:
        """Drop all D&D tables. Intended for isolated tests only."""
        from ..db import models  # noqa: F401

        Base.metadata.drop_all(bind=self.engine)

    @contextmanager
    def transaction(self) -> Iterator[Session]:
        """Commit one unit of work, rolling it back if an exception escapes."""
        session = self.session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def dependency(self) -> Generator[Session, None, None]:
        """Yield a session for dependency-injection frameworks."""
        session = self.session_factory()
        try:
            yield session
        finally:
            session.close()

    def enable_postgresql_vector(self) -> None:
        """Install the optional pgvector column and index on PostgreSQL."""
        if self.engine.dialect.name != "postgresql":
            raise RuntimeError("pgvector initialization requires a PostgreSQL database")
        script = (Path(__file__).parent / "postgresql.sql").read_text(encoding="utf-8")
        statements = [statement.strip() for statement in script.split(";") if statement.strip()]
        with self.engine.begin() as connection:
            for statement in statements:
                connection.exec_driver_sql(statement)

    def dispose(self) -> None:
        """Release pooled database connections."""
        self.engine.dispose()


def sqlite_database_url(path: str | Path) -> str:
    """Build a SQLAlchemy SQLite URL from a filesystem path."""
    return f"sqlite+pysqlite:///{Path(path).expanduser().resolve().as_posix()}"
