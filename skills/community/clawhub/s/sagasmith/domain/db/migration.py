"""Programmatic Alembic entry points for the bundled D&D schema."""

from __future__ import annotations

from pathlib import Path

from alembic import command
from alembic.config import Config


def alembic_config(database_url: str) -> Config:
    config = Config()
    migrations = Path(__file__).parent / "migrations"
    config.set_main_option("script_location", str(migrations))
    config.set_main_option("sqlalchemy.url", database_url.replace("%", "%%"))
    return config


def upgrade_database(database_url: str, *, revision: str = "head") -> None:
    command.upgrade(alembic_config(database_url), revision)


def current_revision(database_url: str) -> str | None:
    config = alembic_config(database_url)
    result: list[str | None] = []

    def capture(revision, _context) -> None:
        result.append(revision)

    config.attributes["on_version_apply"] = capture
    from sqlalchemy import create_engine, inspect

    engine = create_engine(database_url)
    try:
        if "alembic_version" not in inspect(engine).get_table_names():
            return None
        with engine.connect() as connection:
            row = connection.exec_driver_sql("SELECT version_num FROM alembic_version").first()
            return str(row[0]) if row else None
    finally:
        engine.dispose()
