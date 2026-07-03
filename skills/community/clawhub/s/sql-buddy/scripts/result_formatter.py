"""
Result formatter for sql-buddy.
Formats query results as table, JSON, CSV, or Markdown.
"""
import csv
import json
import io
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)


def format_as_table(columns: list, rows: list, max_width: int = 60) -> str:
    """
    Format query results as an ASCII table.
    
    Args:
        columns: List of column names.
        rows: List of row values (list per row).
        max_width: Max width per column.
        
    Returns:
        ASCII table string.
    """
    if not columns:
        return "(no columns)"
    
    if not rows:
        return "(no rows returned)"
    
    # Calculate column widths
    col_widths = []
    for i, col in enumerate(columns):
        # Find the widest value
        max_val = len(str(col))
        for row in rows:
            if i < len(row):
                val_str = str(row[i]) if row[i] is not None else "NULL"
                max_val = max(max_val, len(val_str))
        
        col_widths.append(min(max_val + 2, max_width))
    
    # Build header
    header = "| " + " | ".join(str(col).ljust(col_widths[i] - 2) 
                              for i, col in enumerate(columns)) + " |"
    separator = "+" + "+".join("-" * w for w in col_widths) + "+"
    
    lines = [separator, header, separator]
    
    # Build rows
    for row in rows:
        row_str = []
        for i, col_idx in enumerate(range(len(columns))):
            if i < len(row):
                val = row[i] if row[i] is not None else "NULL"
                val_str = str(val)[:max_width]
            else:
                val_str = ""
            row_str.append(val_str.ljust(col_widths[i] - 2))
        
        lines.append("| " + " | ".join(row_str) + " |")
    
    lines.append(separator)
    
    return "\n".join(lines)


def format_as_json(columns: list, rows: list, indent: int = 2) -> str:
    """Format results as JSON array of objects."""
    result = []
    for row in rows:
        obj = {}
        for i, col in enumerate(columns):
            if i < len(row):
                obj[col] = row[i]
            else:
                obj[col] = None
        result.append(obj)
    
    return json.dumps(result, ensure_ascii=False, indent=indent, default=str)


def format_as_csv(columns: list, rows: list) -> str:
    """Format results as CSV."""
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(columns)
    for row in rows:
        # Ensure row matches column count
        padded_row = list(row) + [None] * (len(columns) - len(row))
        writer.writerow(padded_row[:len(columns)])
    
    return output.getvalue().strip()


def format_as_markdown(columns: list, rows: list) -> str:
    """Format results as Markdown table."""
    if not columns:
        return "_Empty result_"
    
    lines = []
    
    # Header
    lines.append("| " + " | ".join(str(c) for c in columns) + " |")
    lines.append("| " + " | ".join("---" for _ in columns) + " |")
    
    # Rows
    for row in rows:
        padded = [str(row[i]) if i < len(row) and row[i] is not None else "" 
                  for i in range(len(columns))]
        lines.append("| " + " | ".join(padded) + " |")
    
    return "\n".join(lines)


def format_results(columns: list, rows: list, output_format: str = "table",
                   truncated: bool = False) -> Dict:
    """
    Format query results in the specified format.
    
    Args:
        columns: List of column names.
        rows: List of row values.
        output_format: One of "table", "json", "csv", "markdown".
        truncated: Whether results were truncated.
        
    Returns:
        Dict with formatted text and metadata.
    """
    formatters = {
        "table": format_as_table,
        "json": format_as_json,
        "csv": format_as_csv,
        "markdown": format_as_markdown,
    }
    
    formatter = formatters.get(output_format, format_as_table)
    
    formatted = formatter(columns, rows)
    
    result = {
        "text": formatted,
        "format": output_format,
        "columns": columns,
        "row_count": len(rows),
        "truncated": truncated,
    }
    
    if output_format == "json":
        result["raw"] = format_as_json(columns, rows)
    elif output_format == "csv":
        result["raw"] = format_as_csv(columns, rows)
    
    return result


def summarize_results(columns: list, rows: list) -> Dict:
    """
    Generate a basic statistical summary of the results.
    
    Returns:
        Dict with numeric column aggregates.
    """
    if not rows or not columns:
        return {}
    
    summary = {}
    
    for i, col in enumerate(columns):
        col_values = [row[i] for row in rows if i < len(row) and row[i] is not None]
        
        if not col_values:
            continue
        
        # Check if numeric
        numeric_values = []
        for val in col_values:
            try:
                numeric_values.append(float(val))
            except (ValueError, TypeError):
                pass
        
        if numeric_values:
            summary[col] = {
                "min": min(numeric_values),
                "max": max(numeric_values),
                "avg": sum(numeric_values) / len(numeric_values),
                "count": len(numeric_values),
            }
    
    return summary
