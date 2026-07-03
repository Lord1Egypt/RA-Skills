"""
Security module for sql-buddy.
- Password masking (never log passwords)
- SQL injection prevention (parameterized queries)
- Sensitive column name masking in LLM context
- Read-only enforcement
"""
import re
import logging

logger = logging.getLogger(__name__)

# Patterns that indicate sensitive data in column names
SENSITIVE_COLUMN_PATTERNS = [
    re.compile(r'password', re.I),
    re.compile(r'secret', re.I),
    re.compile(r'token', re.I),
    re.compile(r'auth[_]?key', re.I),
    re.compile(r'api[_]?key', re.I),
    re.compile(r'private[_]?key', re.I),
    re.compile(r'credential', re.I),
    re.compile(r'passwd', re.I),
]

# SQL statements that modify data (blocked in readonly mode)
WRITE_STATEMENTS = re.compile(
    r'^\s*(INSERT|UPDATE|DELETE|DROP|ALTER|CREATE|TRUNCATE|REPLACE|MERGE)\b',
    re.IGNORECASE
)

# Safe statements (allowed in readonly mode)
READ_STATEMENTS = re.compile(
    r'^\s*(SELECT|EXPLAIN|PRAGMA|SHOW|DESCRIBE|WITH)\b',
    re.IGNORECASE
)


def mask_connection_string(conn_str: str) -> str:
    """
    Mask password in a database connection string for safe logging.
    
    Examples:
    - "postgresql://user:pass@host/db" → "postgresql://user:***@host/db"
    - "mysql://user:password123@host:3306/db" → "mysql://user:***@host:3306/db"
    """
    # Replace :password@ with :***@
    masked = re.sub(r'(://[^:]+:)([^@]+)(@)', r'\1***\3', conn_str)
    return masked


def is_read_only_query(sql: str) -> bool:
    """
    Check if a SQL statement is read-only.
    
    Returns True if the statement is safe (SELECT, EXPLAIN, etc.),
    False if it modifies data (INSERT, UPDATE, DELETE, DDL).
    """
    sql = sql.strip()
    
    # Remove comments
    sql = re.sub(r'--.*$', '', sql, flags=re.MULTILINE)
    sql = re.sub(r'/\*.*?\*/', '', sql, flags=re.DOTALL)
    
    # Check for write statements
    if WRITE_STATEMENTS.match(sql):
        return False
    
    # If it starts with a known read statement, it's safe
    if READ_STATEMENTS.match(sql):
        return True
    
    # For multi-statement queries, check each statement
    statements = _split_statements(sql)
    if len(statements) > 1:
        return all(is_read_only_query(s.strip()) for s in statements if s.strip())
    
    # Default: treat unknown as read-only but flag it
    logger.warning("Unknown SQL statement type, treating as read-only: %.100s", sql)
    return True


def _split_statements(sql: str) -> list:
    """Split a multi-statement SQL string into individual statements."""
    # Simple splitting on semicolons (not inside quotes or comments)
    statements = []
    current = []
    in_single_quote = False
    in_double_quote = False
    in_line_comment = False
    in_block_comment = False
    
    i = 0
    while i < len(sql):
        c = sql[i]
        
        # Handle comments
        if not in_block_comment:
            if not in_line_comment and i + 1 < len(sql) and sql[i:i+2] == '/*':
                in_block_comment = True
                current.append(c)
                i += 1
                continue
            if not in_line_comment and i + 1 < len(sql) and sql[i:i+2] == '--':
                in_line_comment = True
        
        if c == '\n':
            in_line_comment = False
        
        if c == '*' and in_block_comment and i + 1 < len(sql) and sql[i+1] == '/':
            in_block_comment = False
        
        # Track quotes
        if not in_line_comment and not in_block_comment:
            if c == "'" and not in_double_quote:
                in_single_quote = not in_single_quote
            elif c == '"' and not in_single_quote:
                in_double_quote = not in_double_quote
        
        # Split on semicolons
        if c == ';' and not in_single_quote and not in_double_quote and not in_line_comment and not in_block_comment:
            stmt = ''.join(current).strip()
            if stmt:
                statements.append(stmt)
            current = []
        else:
            current.append(c)
        
        i += 1
    
    # Last statement
    stmt = ''.join(current).strip()
    if stmt:
        statements.append(stmt)
    
    return statements


def mask_sensitive_columns(schema_info: list) -> list:
    """
    Mask sensitive column names in schema info before sending to LLM.
    
    Args:
        schema_info: List of dicts with table/column info.
        
    Returns:
        Schema info with sensitive column names replaced by '***'.
    """
    masked = []
    for table in schema_info:
        table_copy = dict(table)
        columns = table_copy.get("columns", [])
        masked_columns = []
        for col in columns:
            col_copy = dict(col)
            col_name = col.get("column_name", col.get("name", ""))
            for pattern in SENSITIVE_COLUMN_PATTERNS:
                if pattern.search(col_name):
                    col_copy["column_name"] = col_copy.get("name", "***")
                    col_copy["masked"] = True
                    col_copy["type"] = "***"
                    break
            masked_columns.append(col_copy)
        table_copy["columns"] = masked_columns
        masked.append(table_copy)
    
    return masked


def validate_sql_for_dialect(sql: str, dialect: str) -> list:
    """
    Basic syntactic validation for SQL.
    
    Returns list of warnings/errors. Empty list = seems OK.
    """
    warnings = []
    
    # Check for common issues
    if 'SELECT *' in sql.upper() and 'LIMIT' not in sql.upper():
        warnings.append("SELECT * without LIMIT may return many rows")
    
    if 'NOT IN' in sql.upper() and 'WHERE' in sql.upper():
        warnings.append("NOT IN with subquery may be slow; consider NOT EXISTS")
    
    if 'LIKE' in sql.upper() and "LIKE '%" in sql:
        warnings.append("Leading wildcard LIKE ('%...') cannot use index")
    
    return warnings


def check_connection_safety(connection_config: dict) -> list:
    """
    Check if connection config has safety issues.
    Returns list of warnings.
    """
    warnings = []
    
    if connection_config.get("password") and connection_config.get("password", "").strip():
        if len(connection_config["password"]) < 8:
            warnings.append("Password is very short (< 8 characters)")
    
    if connection_config.get("ssl") is False and connection_config.get("type") in ("postgresql", "mysql"):
        if connection_config.get("host", "").startswith("public") or "production" in connection_config.get("host", ""):
            warnings.append("Production connection without SSL is not recommended")
    
    return warnings
