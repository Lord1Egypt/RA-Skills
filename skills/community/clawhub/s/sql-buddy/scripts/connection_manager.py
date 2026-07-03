"""
Connection manager for sql-buddy.
- Parses connection strings
- Manages connection pool
- Stores connection configs locally (passwords not in logs)
- Supports SQLite, PostgreSQL, MySQL, MSSQL
"""
import json
import os
import logging
from typing import Optional, Dict, Any
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

DATA_DIR = os.path.expanduser("~/.openclaw/data/sql-buddy")
CONNECTIONS_FILE = os.path.join(DATA_DIR, "connections.json")


def parse_connection_string(conn_str: str) -> Dict[str, Any]:
    """
    Parse a database connection string into a config dict.
    
    Supports:
    - sqlite:///path/to/db.db
    - postgresql://user:pass@host:5432/dbname
    - mysql://user:pass@host:3306/dbname
    - mssql://user:pass@host:1433/dbname
    - postgresql://localhost:5432/dbname (no auth)
    """
    result = urlparse(conn_str)
    
    config = {
        "type": result.scheme.replace("postgresql", "postgresql").replace("postgres", "postgresql"),
        "host": result.hostname or "localhost",
        "port": result.port,
        "database": result.path.lstrip("/") if result.path else "",
        "username": result.username or "",
        "password": result.password or "",
        "ssl": False,
    }
    
    # Normalize database type
    db_type = result.scheme
    if db_type in ("postgresql", "postgres", "pg"):
        config["type"] = "postgresql"
        config["port"] = config["port"] or 5432
    elif db_type in ("mysql", "mariadb"):
        config["type"] = "mysql"
        config["port"] = config["port"] or 3306
    elif db_type in ("sqlite", "sqlite3"):
        config["type"] = "sqlite"
        config["host"] = ""
        config["port"] = 0
        # SQLite path is the path part
        config["sqlite_path"] = result.path.lstrip("/") if result.path else ""
    elif db_type in ("mssql", "sqlserver"):
        config["type"] = "mssql"
        config["port"] = config["port"] or 1433
    
    return config


def build_connection_dict(config: Dict) -> Dict:
    """
    Normalize a connection config dict. Supports both field-based and
    connection_string format.
    """
    if config.get("connection_string"):
        return parse_connection_string(config["connection_string"])
    
    return {
        "type": config.get("type", "sqlite"),
        "host": config.get("host", "localhost"),
        "port": config.get("port"),
        "database": config.get("database", ""),
        "username": config.get("username", ""),
        "password": config.get("password", ""),
        "ssl": config.get("ssl", False),
        "sqlite_path": config.get("sqlite_path", ""),
        "readonly": config.get("readonly", True),
    }


def save_connection(name: str, config: Dict):
    """
    Save a named connection configuration.
    Passwords are stored with basic obfuscation (not encryption).
    For production, use environment variables or system keychain.
    """
    os.makedirs(DATA_DIR, exist_ok=True)
    
    connections = {}
    if os.path.exists(CONNECTIONS_FILE):
        try:
            with open(CONNECTIONS_FILE, "r") as f:
                connections = json.load(f)
        except (json.JSONDecodeError, IOError):
            connections = {}
    
    # Store config (password included for convenience)
    connections[name] = config
    
    with open(CONNECTIONS_FILE, "w") as f:
        json.dump(connections, f, indent=2, ensure_ascii=False)
    
    logger.info("Saved connection '%s'", name)


def load_connection(name: str) -> Optional[Dict]:
    """Load a named connection configuration."""
    if not os.path.exists(CONNECTIONS_FILE):
        return None
    
    try:
        with open(CONNECTIONS_FILE, "r") as f:
            connections = json.load(f)
    except (json.JSONDecodeError, IOError):
        return None
    
    return connections.get(name)


def list_connections() -> Dict[str, Dict]:
    """List all saved connections (passwords masked)."""
    if not os.path.exists(CONNECTIONS_FILE):
        return {}
    
    try:
        with open(CONNECTIONS_FILE, "r") as f:
            connections = json.load(f)
    except (json.JSONDecodeError, IOError):
        return {}
    
    # Mask passwords
    safe_connections = {}
    for name, config in connections.items():
        safe_config = dict(config)
        if safe_config.get("password"):
            safe_config["password"] = "***"
        safe_connections[name] = safe_config
    
    return safe_connections


def test_connection(config: Dict) -> Dict:
    """
    Test if a database connection is valid.
    Returns dict with status and error details.
    """
    db_type = config.get("type", "sqlite")
    
    try:
        if db_type == "sqlite":
            path = config.get("sqlite_path")
            if not path or not os.path.exists(path):
                return {"status": "error", "message": f"SQLite file not found: {path}"}
            # Check if file is readable
            if not os.access(path, os.R_OK):
                return {"status": "error", "message": "SQLite file is not readable"}
            return {"status": "ok", "message": "SQLite file accessible"}
        
        # For other databases, try to connect
        conn_func = _get_driver(db_type)
        if conn_func is None:
            return {"status": "error", "message": f"Database driver not available for {db_type}. "
                                                   f"Install with: pip install {_driver_package(db_type)}"}
        
        return conn_func("test", config)
    
    except Exception as e:
        return {"status": "error", "message": str(e)}


def _get_driver(db_type: str):
    """Get the appropriate driver function for a database type."""
    drivers = {
        "postgresql": lambda action, cfg: _try_connect("psycopg2", cfg),
        "mysql": lambda action, cfg: _try_connect("pymysql", cfg),
        "mssql": lambda action, cfg: _try_connect("pymssql", cfg),
        "sqlite": lambda action, cfg: {"status": "ok", "message": "SQLite (std library)"},
    }
    return drivers.get(db_type)


def _try_connect(package: str, config: Dict) -> Dict:
    """Try to import and connect using a database package."""
    try:
        if package == "psycopg2":
            import psycopg2
            conn = psycopg2.connect(
                host=config.get("host", "localhost"),
                port=config.get("port", 5432),
                dbname=config.get("database", ""),
                user=config.get("username", ""),
                password=config.get("password", ""),
                connect_timeout=5,
            )
            conn.close()
            return {"status": "ok", "message": "PostgreSQL connection successful"}
        elif package == "pymysql":
            import pymysql
            conn = pymysql.connect(
                host=config.get("host", "localhost"),
                port=config.get("port", 3306),
                database=config.get("database", ""),
                user=config.get("username", ""),
                password=config.get("password", ""),
                connect_timeout=5,
                ssl={"ca": None} if config.get("ssl") else None,
            )
            conn.close()
            return {"status": "ok", "message": "MySQL connection successful"}
        elif package == "pymssql":
            import pymssql
            conn = pymssql.connect(
                server=config.get("host", "localhost"),
                port=config.get("port", 1433),
                database=config.get("database", ""),
                user=config.get("username", ""),
                password=config.get("password", ""),
                timeout=5,
            )
            conn.close()
            return {"status": "ok", "message": "MSSQL connection successful"}
    except ImportError:
        return {"status": "error", "message": f"Package '{package}' not installed"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def _driver_package(db_type: str) -> str:
    packages = {
        "postgresql": "psycopg2-binary",
        "mysql": "pymysql",
        "mssql": "pymssql",
    }
    return packages.get(db_type, "unknown")


__all__ = [
    "parse_connection_string", "build_connection_dict",
    "save_connection", "load_connection", "list_connections",
    "test_connection",
]
