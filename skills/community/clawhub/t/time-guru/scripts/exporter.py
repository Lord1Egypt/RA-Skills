"""
Data exporter for time-guru.
Exports time entries as CSV or JSON.
"""
import csv
import json
import io
import os
import logging
from typing import Dict, List, Optional
from datetime import date

import store as time_logger

logger = logging.getLogger(__name__)


def export_csv(entries: list) -> str:
    """
    Export time entries as CSV.
    
    Args:
        entries: List of time entries.
        
    Returns:
        CSV string content.
    """
    output = io.StringIO()
    fieldnames = ["id", "date", "start", "end", "duration_minutes", "description",
                  "category", "project", "billable", "tags", "notes"]
    
    writer = csv.DictWriter(output, fieldnames=fieldnames, extrasaction="ignore")
    writer.writeheader()
    
    for entry in entries:
        row = {
            "id": entry.get("id", ""),
            "date": entry.get("date", entry.get("created_at", "")[:10]),
            "start": entry.get("start", ""),
            "end": entry.get("end", ""),
            "duration_minutes": entry.get("duration_minutes", 0),
            "description": entry.get("description", ""),
            "category": entry.get("category", ""),
            "project": entry.get("project", ""),
            "billable": "Yes" if entry.get("billable") else "No",
            "tags": ", ".join(entry.get("tags", [])),
            "notes": entry.get("notes", ""),
        }
        writer.writerow(row)
    
    return output.getvalue()


def export_json(entries: list, indent: int = 2) -> str:
    """Export entries as JSON."""
    return json.dumps(entries, ensure_ascii=False, indent=indent, default=str)


def export_to_file(entries: list, output_path: str, format: str = "csv"):
    """Export entries to a file."""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    if format == "csv":
        content = export_csv(entries)
    else:
        content = export_json(entries)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
    
    return output_path


def export_report(range_start: date, range_end: date, 
                   format: str = "csv", output_path: Optional[str] = None) -> Dict:
    """
    Export a range of time entries.
    
    Returns:
        Dict with export path and metadata.
    """
    entries = time_store.get_entries(range_start, range_end)
    
    if not entries:
        return {"exported": False, "message": "No entries in the specified range"}
    
    if not output_path:
        filename = f"time-guru-{range_start.isoformat()}-to-{range_end.isoformat()}.{format}"
        output_dir = os.path.expanduser("~/.openclaw/data/time-guru/exports")
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, filename)
    
    result_path = export_to_file(entries, output_path, format)
    
    return {
        "exported": True,
        "path": result_path,
        "format": format,
        "entry_count": len(entries),
        "date_range": f"{range_start} ~ {range_end}",
    }
