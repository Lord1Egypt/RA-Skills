"""
SQL Query Optimizer.
Analyzes execution plans and provides index suggestions.
"""
import re
import logging
from typing import Dict, List, Optional

import executor

logger = logging.getLogger(__name__)


def analyze_explain_plan(explain_result: Optional[Dict], sql: str, dialect: str) -> Dict:
    """
    Analyze an EXPLAIN plan and extract optimization insights.
    
    Args:
        explain_result: Result from executor.explain_query().
        sql: The SQL statement.
        dialect: Database dialect.
        
    Returns:
        Dict with scanned rows estimate, warnings, suggestions.
    """
    result = {
        "scanned_rows_estimate": None,
        "warnings": [],
        "index_suggestions": [],
    }
    
    if not explain_result:
        return result
    
    raw_plan = explain_result.get("raw_plan", [])
    
    if dialect == "sqlite":
        return _analyze_sqlite_plan(raw_plan, sql, result)
    elif dialect == "postgresql":
        return _analyze_pg_plan(raw_plan, sql, result)
    elif dialect == "mysql":
        return _analyze_mysql_plan(explain_result, sql, result)
    
    return result


def _analyze_sqlite_plan(raw_plan: list, sql: str, result: Dict) -> Dict:
    """Analyze SQLite EXPLAIN QUERY PLAN output."""
    scan_keywords = ["SCAN", "TABLE SCAN", "FULL"]
    index_keywords = ["USING INDEX", "USING COVERING INDEX"]
    
    for entry in raw_plan:
        detail = entry.get("detail", "")
        
        if any(kw in detail for kw in scan_keywords):
            # Extract table name
            table_match = re.search(r'TABLE (\w+)', detail)
            if table_match:
                table = table_match.group(1)
                result["warnings"].append(f"Full table scan on '{table}'")
                
                # Suggest an index
                result["index_suggestions"].append({
                    "table": table,
                    "columns": [],
                    "reason": "Full table scan detected",
                    "estimated_improvement": "Significant (table scan → index lookup)",
                })
        
        if any(kw in detail for kw in index_keywords):
            # Good, using index
            pass
    
    if not result["warnings"]:
        result["warnings"].append("Query appears to use indexes efficiently")
    
    return result


def _analyze_pg_plan(raw_plan: list, sql: str, result: Dict) -> Dict:
    """Analyze PostgreSQL EXPLAIN JSON output."""
    try:
        # If raw plan is a list of tuples
        plan_text = ""
        if raw_plan and isinstance(raw_plan, list):
            for row in raw_plan:
                if isinstance(row, tuple) and len(row) > 0:
                    plan_text += str(row[0])
        
        if "Seq Scan" in plan_text:
            table_match = re.search(r'Seq Scan on (\w+)', plan_text)
            if table_match:
                table = table_match.group(1)
                result["warnings"].append(f"Sequential scan on '{table}'")
                result["index_suggestions"].append({
                    "table": table,
                    "columns": [],
                    "reason": "Sequential scan detected",
                    "estimated_improvement": "High for large tables",
                })
        
        if "cost=" in plan_text:
            cost_match = re.search(r'cost=(\d+\.?\d*)\.\.(\d+\.?\d*)', plan_text)
            if cost_match:
                result["scanned_rows_estimate"] = float(cost_match.group(2))
    
    except Exception as e:
        logger.warning("Error parsing PG plan: %s", e)
    
    return result


def _analyze_mysql_plan(explain_result: Dict, sql: str, result: Dict) -> Dict:
    """Analyze MySQL EXPLAIN output."""
    rows_data = explain_result.get("rows", [])
    
    for row in rows_data:
        if isinstance(row, dict):
            table = row.get("table", "")
            scan_type = row.get("type", "")
            rows_examined = row.get("rows", 0)
            
            if scan_type in ("ALL", "index"):
                result["warnings"].append(f"Full table/index scan on '{table}' (~{rows_examined} rows)")
                possible_keys = row.get("possible_keys", "")
                if not possible_keys:
                    result["index_suggestions"].append({
                        "table": table,
                        "columns": [],
                        "reason": f"No usable index for query (type={scan_type})",
                        "estimated_improvement": "High",
                    })
            elif scan_type == "ref" and rows_examined and rows_examined > 1000:
                result["warnings"].append(f"Large ref scan on '{table}' (~{rows_examined} rows)")
    
    return result


def suggest_index_columns(sql: str) -> List[Dict]:
    """
    Simple heuristic: suggest indexes for columns used in WHERE and JOIN conditions.
    """
    suggestions = []
    
    # Extract WHERE clause columns
    where_match = re.search(r'WHERE\s+(.+?)(?:ORDER BY|GROUP BY|LIMIT|$)', sql, re.IGNORECASE | re.DOTALL)
    if where_match:
        where_clause = where_match.group(1)
        # Find column references (table.column patterns)
        col_refs = re.findall(r'(\w+)\.(\w+)', where_clause)
        tables_columns = {}
        for table, col in col_refs:
            if table not in tables_columns:
                tables_columns[table] = set()
            tables_columns[table].add(col)
        
        for table, cols in tables_columns.items():
            suggestions.append({
                "table": table,
                "columns": list(cols),
                "reason": "WHERE/JOIN condition columns",
                "estimated_improvement": "Moderate to High",
            })
    
    return suggestions


def generate_optimized_sql(sql: str, suggestions: Dict) -> str:
    """
    Generate an optimized version of the SQL based on analysis.
    
    This is a simplified version; full optimization uses LLM.
    """
    optimized = sql
    
    # Replace SELECT * with explicit columns (when possible)
    if 'SELECT *' in optimized:
        # In a real scenario, we'd look up the table columns
        pass
    
    # Add LIMIT for SELECT without it
    if optimized.strip().upper().startswith('SELECT') and 'LIMIT' not in optimized.upper():
        # Check if it's a subquery (already has LIMIT)
        if "SELECT" in optimized.upper()[7:]:
            pass  # Skip for subqueries
        else:
            optimized = optimized.rstrip(';') + ' LIMIT 100'
    
    return optimized
