"""
AI insight generator for query results.
Interprets query results, identifies trends and anomalies.
"""
import logging
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


def generate_insight_prompt(query: str, columns: list, rows: list, 
                            sql: str, summary: Dict) -> str:
    """
    Build an LLM prompt to interpret query results.
    
    Args:
        query: The original natural language query.
        columns: Column names from the result.
        rows: Result rows (up to 20).
        sql: The generated SQL.
        summary: Numerical summary of results.
        
    Returns:
        Prompt string for LLM.
    """
    result_text = ""
    for i, row in enumerate(rows[:5]):
        row_parts = []
        for j, col in enumerate(columns):
            if j < len(row):
                row_parts.append(f"{col}={row[j]}")
        result_text += f"  Row {i+1}: {', '.join(row_parts)}\n"
    
    if len(rows) > 5:
        result_text += f"  ... and {len(rows) - 5} more rows\n"
    
    summary_text = ""
    for col, stats in summary.items():
        summary_text += f"  {col}: min={stats['min']}, max={stats['max']}, avg={stats['avg']:.2f}\n"
    
    prompt = f"""You are a data analyst. Interpret the following query results.

User query: {query}
Generated SQL: {sql}

Columns: {', '.join(columns)}
Total rows: {len(rows)}

Sample results:
{result_text}

Numerical summary:
{summary_text}

Provide a brief interpretation (2-3 sentences) in {_detect_language(query)}:
1. What the key finding is
2. Any notable trends or anomalies
3. A practical takeaway or recommendation

Keep it concise and actionable."""
    
    return prompt


def _detect_language(query: str) -> str:
    """Detect if query is in Chinese or English."""
    chinese_chars = sum(1 for c in query if '\u4e00' <= c <= '\u9fff')
    if chinese_chars > len(query) * 0.2:
        return "Chinese (中文)"
    return "English"


def generate_fallback_insight(query: str, columns: list, rows: list,
                               summary: Dict) -> str:
    """
    Generate a basic rule-based insight without LLM.
    """
    if not rows or not columns:
        return "No data available for analysis."
    
    parts = []
    
    # Check for time-based trends
    time_cols = [c for c in columns if any(t in str(c).lower() 
                  for t in ("date", "time", "day", "month", "year", "created", "updated"))]
    
    if time_cols:
        parts.append(f"Data spans {len(rows)} records across {len(time_cols)} temporal dimension(s).")
    
    # Check for numeric patterns
    if summary:
        for col, stats in summary.items():
            if stats["count"] > 0:
                if stats["min"] == 0 and stats["max"] > 0:
                    parts.append(f"'{col}' ranges from 0 to {stats['max']:.1f} (avg {stats['avg']:.1f}).")
                elif stats["count"] == len(rows):
                    parts.append(f"'{col}' average is {stats['avg']:.1f} (range: {stats['min']}–{stats['max']}).")
    
    if not parts:
        parts.append(f"Query returned {len(rows)} records with {len(columns)} columns.")
    
    return " ".join(parts)
