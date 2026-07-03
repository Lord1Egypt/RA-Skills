"""
AI SQL Generator.
Generates SQL from natural language using LLM prompts.
"""
import re
import logging
from typing import Dict, Optional, List
import nl_parser

logger = logging.getLogger(__name__)


def generate_sql(query: str, schema_text: str, dialect: str = "sqlite",
                 intent: Optional[Dict] = None) -> Dict:
    """
    Generate SQL from natural language.
    
    This is the main entry point. In skill runtime, this would call the LLM.
    For the skill framework, it builds the prompt and returns structured output.
    
    Args:
        query: Natural language query.
        schema_text: Formatted schema string.
        dialect: Target database dialect.
        intent: Pre-parsed intent (optional).
        
    Returns:
        Dict with generated SQL, explanation, and metadata.
    """
    if not intent:
        intent = nl_parser.parse_intent(query)
    
    prompt = nl_parser.build_nl_prompt(query, schema_text, dialect)
    
    # In production, this prompt is sent to the LLM.
    # The agent runtime handles the actual model call.
    # Here we return the prompt and metadata for the calling framework.
    
    explanation = _generate_explanation(intent, query)
    
    return {
        "prompt": prompt,
        "intent": intent["primary_intent"],
        "explanation": explanation,
        "dialect": dialect,
        "is_safe": True,
        "tables_used": intent.get("table_hints", []),
    }


def _generate_explanation(intent: Dict, query: str) -> str:
    """Generate a human-readable explanation of what the SQL will do."""
    primary = intent["primary_intent"]
    
    explanations = {
        "aggregate_count": "This query will count the number of matching records.",
        "aggregate_sum": "This query will sum up values matching the criteria.",
        "aggregate_avg": "This query will calculate the average value.",
        "select": "This query will select and display matching records.",
    }
    
    base = explanations.get(primary, "This query will retrieve the requested data.")
    
    if intent.get("requires_group"):
        base += " Results will be grouped by category."
    if intent.get("requires_join"):
        base += " Multiple tables will be joined."
    
    time_range = intent.get("time_range")
    if time_range:
        base += f" Time range: {time_range}."
    
    return base


def apply_dialect_fixes(sql: str, dialect: str) -> str:
    """
    Apply dialect-specific fixes to generated SQL.
    
    Args:
        sql: Generated SQL string.
        dialect: Target dialect.
        
    Returns:
        Fixed SQL string.
    """
    if dialect == "sqlite":
        # SQLite-specific fixes
        sql = re.sub(r'\bNOW\(\)', "datetime('now')", sql, flags=re.IGNORECASE)
        sql = re.sub(r"INTERVAL\s+'(\d+)\s+(DAY|MONTH|YEAR)'", 
                     lambda m: f"'+{m.group(1)} {m.group(2)}'", sql, flags=re.IGNORECASE)
        sql = re.sub(r'\bCURDATE\(\)', "date('now')", sql, flags=re.IGNORECASE)
        sql = re.sub(r'\bNOW\(\)\s*-\s*INTERVAL\s+(\d+)\s+DAY', 
                     lambda m: f"datetime('now', '-{m.group(1)} days')", sql, flags=re.IGNORECASE)
        # Fix BOOLEAN literal
        sql = re.sub(r'\bTRUE\b', '1', sql)
        sql = re.sub(r'\bFALSE\b', '0', sql)
        
    elif dialect == "mysql":
        # MySQL-specific fixes  
        sql = re.sub(r'\BNOW\(\)', 'NOW()', sql)  # already correct
        
    elif dialect == "postgresql":
        # PostgreSQL uses ILIKE for case-insensitive
        pass  # already handled in example prompts
    
    return sql


def validate_generated_sql(sql: str, dialect: str) -> List[str]:
    """
    Validate the generated SQL for common issues.
    Returns a list of warnings (empty = no issues).
    """
    warnings = []
    
    sql_upper = sql.upper().strip()
    
    # Check for write statements
    write_patterns = [r'^\s*INSERT\b', r'^\s*UPDATE\b', r'^\s*DELETE\b', 
                      r'^\s*DROP\b', r'^\s*ALTER\b', r'^\s*CREATE\b', r'^\s*TRUNCATE\b']
    for pattern in write_patterns:
        if re.match(pattern, sql_upper):
            warnings.append("DETECTED WRITE STATEMENT - Blocked in readonly mode")
    
    # Check for SELECT * without LIMIT
    if 'SELECT *' in sql_upper and 'LIMIT' not in sql_upper:
        warnings.append("SELECT * without LIMIT may return many rows")
    
    # Check for unqualified column names in JOINs
    if 'JOIN' in sql_upper:
        # Simple check: look for WHERE clause columns that might be ambiguous
        pass
    
    # Check for basic SQL syntax (very basic)
    if sql_upper.startswith('SELECT'):
        if 'FROM' not in sql_upper:
            warnings.append("Missing FROM clause in SELECT statement")
    
    return warnings
