# Workflow: Setup Database Layer

<required_reading>
Read before proceeding:
1. references/best-practices.md
2. references/async-patterns.md
</required_reading>

<process>
## Step 1: Install Dependencies

```bash
pip install sqlalchemy[asyncio] asyncpg alembic pydantic pydantic-settings
```

Or add to pyproject.toml/requirements.txt:
```
sqlalchemy[asyncio]>=2.0.0
asyncpg>=0.29.0
alembic>=1.13.0
pydantic>=2.0.0
pydantic-settings>=2.0.0
```

## Step 2: Create Database Configuration

Create `src/db/config.py`:
```python
from pydantic_settings import BaseSettings
from functools import lru_cache


class DatabaseSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str

    # Connection pool settings
    POOL_SIZE: int = 5
    MAX_OVERFLOW: int = 10
    POOL_TIMEOUT: int = 30
    POOL_RECYCLE: int = 1800  # 30 minutes

    @property
    def async_database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    @property
    def sync_database_url(self) -> str:
        """For Alembic migrations"""
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

    class Config:
        env_file = ".env"


@lru_cache
def get_db_settings() -> DatabaseSettings:
    return DatabaseSettings()
```

## Step 3: Create Base Model

Create `src/db/base.py`:
```python
from datetime import datetime
from typing import Any
from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all models."""

    # Common type annotation map
    type_annotation_map = {
        datetime: DateTime(timezone=True),
    }

    def to_dict(self) -> dict[str, Any]:
        """Convert model to dictionary."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class TimestampMixin:
    """Mixin for created_at and updated_at timestamps."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
```

## Step 4: Create Async Session Factory

Create `src/db/session.py`:
```python
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
    AsyncEngine,
)
from .config import get_db_settings


def create_engine() -> AsyncEngine:
    """Create async database engine with connection pooling."""
    settings = get_db_settings()

    return create_async_engine(
        settings.async_database_url,
        echo=False,  # Set True for SQL logging in dev
        pool_size=settings.POOL_SIZE,
        max_overflow=settings.MAX_OVERFLOW,
        pool_timeout=settings.POOL_TIMEOUT,
        pool_recycle=settings.POOL_RECYCLE,
        pool_pre_ping=True,  # Verify connections before use
    )


engine = create_engine()

async_session_factory = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autoflush=False,
)


async def get_session() -> AsyncSession:
    """Get async database session."""
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

## Step 5: Create FastAPI Dependency

Create `src/db/dependencies.py`:
```python
from typing import Annotated, AsyncGenerator
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .session import async_session_factory


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency for database session."""
    async with async_session_factory() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise


# Type alias for dependency injection
DBSession = Annotated[AsyncSession, Depends(get_db)]
```

## Step 6: Initialize Alembic

```bash
cd src
alembic init alembic
```

Update `alembic/env.py`:
```python
import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

# Import your models
from db.base import Base
from db.config import get_db_settings
# Import all models here to register them
# from models.user import User

config = context.config
settings = get_db_settings()

# Set database URL
config.set_main_option("sqlalchemy.url", settings.sync_database_url)

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Run migrations in 'online' mode with async engine."""
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

## Step 7: Create .env File

```env
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=your_database
```

## Step 8: Create Package Init Files

Create `src/db/__init__.py`:
```python
from .base import Base, TimestampMixin
from .session import engine, async_session_factory, get_session
from .dependencies import get_db, DBSession
from .config import get_db_settings, DatabaseSettings

__all__ = [
    "Base",
    "TimestampMixin",
    "engine",
    "async_session_factory",
    "get_session",
    "get_db",
    "DBSession",
    "get_db_settings",
    "DatabaseSettings",
]
```
</process>

<success_criteria>
Setup is complete when:
- [ ] All dependencies installed
- [ ] Database config with pydantic-settings
- [ ] Base model with TimestampMixin
- [ ] Async engine with connection pooling
- [ ] Session factory configured
- [ ] FastAPI dependency created
- [ ] Alembic initialized with async support
- [ ] .env file with database credentials
- [ ] Directory structure matches expected layout
</success_criteria>
