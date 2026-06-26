#!/usr/bin/env python3
"""
WPS Document Extractor — handles WPS Spreadsheet (.et) and WPS Writer (.wps).
Usage: python wps_extractor.py <filepath>
"""

import sys
import json
import contextlib
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


@contextlib.contextmanager
def wps_com_session(app_name: str):
    """WPS COM session context manager."""
    app = None
    try:
        import win32com.client
        app = win32com.client.Dispatch(app_name)
        app.Visible = False
        if hasattr(app, 'DisplayAlerts'):
            app.DisplayAlerts = False
        yield app
    finally:
        if app:
            try:
                app.Quit()
            except Exception:
                pass


def extract_wps_spreadsheet(filepath: str) -> dict:
    """Extract data from WPS Spreadsheet (.et) via KET COM."""
    filepath = str(Path(filepath).resolve())
    result = {}
    with wps_com_session("KET.Application") as app:
        wb = app.Workbooks.Open(filepath)
        for ws in wb.Sheets:
            raw = ws.UsedRange.Value
            if raw is None:
                result[ws.Name] = []
            elif isinstance(raw, tuple) and isinstance(raw[0], tuple):
                result[ws.Name] = [list(row) for row in raw]
            else:
                result[ws.Name] = [list(raw)]
            logger.info(f"Sheet '{ws.Name}': {len(result[ws.Name])} rows")
        wb.Close(False)
    return result


def extract_wps_writer(filepath: str) -> dict:
    """Extract content from WPS Writer (.wps) via KWPS COM."""
    filepath = str(Path(filepath).resolve())
    result = {'text': '', 'tables': [], 'metadata': {}}
    with wps_com_session("KWPS.Application") as app:
        doc = app.Documents.Open(filepath)
        result['text'] = doc.Content.Text
        try:
            result['metadata'] = {
                'author': doc.BuiltInDocumentProperties("Author").Value,
                'pages': doc.ComputeStatistics(2),
            }
        except Exception:
            pass
        for table in doc.Tables:
            table_data = []
            for i in range(1, table.Rows.Count + 1):
                row = []
                for j in range(1, table.Columns.Count + 1):
                    try:
                        cell = table.Cell(i, j).Range.Text.rstrip('\r\x07')
                        row.append(cell)
                    except Exception:
                        row.append("")
                table_data.append(row)
            result['tables'].append(table_data)
        doc.Close(False)
    logger.info(f"Extracted: {len(result['text'])} chars, {len(result['tables'])} tables")
    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python wps_extractor.py <filepath>")
        sys.exit(1)

    filepath = sys.argv[1]
    suffix = Path(filepath).suffix.lower()

    if suffix == '.et':
        data = extract_wps_spreadsheet(filepath)
    elif suffix == '.wps':
        data = extract_wps_writer(filepath)
    else:
        logger.error(f"Unsupported WPS format: {suffix}")
        sys.exit(1)

    output = json.dumps(data, ensure_ascii=False, default=str, indent=2)
    print(output)
    out_path = Path(filepath).stem + "_extracted.json"
    Path(out_path).write_text(output, encoding='utf-8')
    logger.info(f"Saved to: {out_path}")


if __name__ == "__main__":
    main()
