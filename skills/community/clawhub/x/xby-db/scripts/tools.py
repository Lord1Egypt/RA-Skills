from __future__ import annotations

from typing import Optional

from scripts.call_api import call_api
from scripts.config import settings

def db_tables(
    db_url: Optional[str] = None,
    schema: Optional[str] = None
) -> Dict[str, Any]:
    """
    List all tables in the database, optionally filtered by schema. Returns qualified table names.
    
    Args:
        db_url: Optional database URL override (e.g., sqlite:///./dev.db, postgresql://...)
        schema: Optional schema name filter (PostgreSQL only)
    
    Returns:
        
    """
    arguments = {
        "db_url": db_url,
        "schema": schema
    }
    
    return call_api("1777316659322883", "db_tables", arguments)

def db_describe_table(
    db_url: Optional[str] = None,
    schema: Optional[str] = None,
    table: str
) -> Dict[str, Any]:
    """
    Get column information for a specific table including column names, data types, and nullability.
    
    Args:
        db_url: Optional database URL override
        schema: Optional schema name (PostgreSQL only)
        table: Table name to describe
    
    Returns:
        
    """
    arguments = {
        "db_url": db_url,
        "schema": schema,
        "table": table
    }
    
    return call_api("1777316659322883", "db_describe_table", arguments)

def db_execute(
    db_url: Optional[str] = None,
    sql: str,
    args: Optional[null] = None,
    allow_write: Optional[bool] = None,
    row_limit: Optional[float] = None
) -> Dict[str, Any]:
    """
    Execute a SQL statement. Supports SELECT (read), INSERT/UPDATE/DELETE (write if enabled), and DDL (if enabled). Use named parameters with :param syntax.
    
    Args:
        db_url: Optional database URL override
        sql: SQL statement to execute (single statement only)
        args: Named parameters for the SQL statement (e.g., {name: 'John'})
        allow_write: Set to true to allow write operations (requires ALLOW_WRITES=true)
        row_limit: Maximum rows to return for SELECT queries
    
    Returns:
        
    """
    arguments = {
        "db_url": db_url,
        "sql": sql,
        "args": args,
        "allow_write": allow_write,
        "row_limit": row_limit
    }
    
    return call_api("1777316659322883", "db_execute", arguments)

def db_explain(
    db_url: Optional[str] = None,
    sql: str,
    args: Optional[null] = None,
    analyze: Optional[bool] = None
) -> Dict[str, Any]:
    """
    Get query execution plan and performance information using EXPLAIN. Helps analyze query performance and optimization opportunities.
    
    Args:
        db_url: Optional database URL override
        sql: SQL query to explain (typically a SELECT statement)
        args: Named parameters for the SQL statement (e.g., {name: 'John'})
        analyze: Run EXPLAIN ANALYZE to get actual execution statistics (executes the query)
    
    Returns:
        
    """
    arguments = {
        "db_url": db_url,
        "sql": sql,
        "args": args,
        "analyze": analyze
    }
    
    return call_api("1777316659322883", "db_explain", arguments)

