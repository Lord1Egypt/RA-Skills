"""MSSQL (SQL Server) driver adapter — STUB.

TODO: Implement MSSQL driver with pymssql or pyodbc.

This is a placeholder. Before using MSSQL connections:
1. pip install pymssql (or pyodbc)
2. Implement actual connection, schema discovery, and query execution
3. Update connection_manager.py to route mssql:// URIs to this module
"""
import logging
from typing import Optional, Dict, Any, List

logger = logging.getLogger(__name__)

DRIVER_AVAILABLE = False


def check_available() -> bool:
    """Check if pymssql is available."""
    try:
        import pymssql  # noqa: F401
        return True
    except ImportError:
        logger.warning("pymssql not installed — MSSQL driver is a stub")
        return False


def get_tables(config: Dict[str, Any]) -> List[str]:
    """Get all tables (stub — always returns empty)."""
    if not check_available():
        logger.warning("pymssql not installed, cannot query MSSQL")
        return []
    # TODO: Implement once pymssql is available
    # import pymssql
    # conn = pymssql.connect(...)
    raise NotImplementedError("MSSQL driver is a stub — implement with pymssql or pyodbc")
