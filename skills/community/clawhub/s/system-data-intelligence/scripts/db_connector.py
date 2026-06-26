#!/usr/bin/env python3
"""Database Connector - SQLite, MySQL, PostgreSQL, SQL Server via SQLAlchemy."""

import json
import logging
import argparse
from pathlib import Path
from contextlib import contextmanager
from typing import Optional
from urllib.parse import quote_plus

import pandas as pd

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

_DEFAULT_TIMEOUT = 30
_DEFAULT_CHUNK_SIZE = 10000


def build_url(dialect, host='localhost', port=None, database='', user='', password='', driver=None):
    dialect_part = f"{dialect}+{driver}" if driver else dialect
    cred = f"{quote_plus(user)}:{quote_plus(password)}@" if user else ''
    port_part = f":{port}" if port else ''
    return f"{dialect_part}://{cred}{host}{port_part}/{database}"


class DBConnector:
    def __init__(self, connection_url, connect_timeout=_DEFAULT_TIMEOUT):
        from sqlalchemy import create_engine
        self.url = connection_url
        self.engine = create_engine(connection_url, pool_pre_ping=True, pool_recycle=3600,
            connect_args={'connect_timeout': connect_timeout})

    def _safe_url(self):
        import re
        return re.sub(r'://([^:]+):([^@]+)@', r'://\1:***@', self.url)

    @contextmanager
    def connection(self):
        conn = self.engine.connect()
        try:
            yield conn
        finally:
            conn.close()

    def query(self, sql, params=None):
        from sqlalchemy import text
        with self.connection() as conn:
            return pd.read_sql(text(sql), conn, params=params)

    def query_chunked(self, sql, chunk_size=_DEFAULT_CHUNK_SIZE, params=None):
        from sqlalchemy import text
        with self.connection() as conn:
            for chunk in pd.read_sql(text(sql), conn, params=params, chunksize=chunk_size):
                yield chunk

    def list_tables(self):
        from sqlalchemy import inspect
        return inspect(self.engine).get_table_names()

    def table_schema(self, table_name):
        from sqlalchemy import inspect
        cols = inspect(self.engine).get_columns(table_name)
        return [{'name': c['name'], 'type': str(c['type']), 'nullable': c.get('nullable')} for c in cols]

    def close(self):
        self.engine.dispose()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('url')
    parser.add_argument('sql')
    parser.add_argument('-o', '--output')
    args = parser.parse_args()
    db = DBConnector(args.url)
    try:
        df = db.query(args.sql)
        if args.output:
            df.to_csv(args.output, index=False, encoding='utf-8-sig')
        else:
            print(df.to_string(max_rows=50))
    finally:
        db.close()


if __name__ == "__main__":
    main()
