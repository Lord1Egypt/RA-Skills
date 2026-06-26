#!/usr/bin/env python3
"""
Windows Excel/WPS Reader via COM interface.
Usage: python win_excel_reader.py <filepath> [sheet_name]
"""

import sys
import json
import contextlib
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


@contextlib.contextmanager
def safe_com_session(app_name: str):
    """COM application safe context manager — ensures process cleanup."""
    app = None
    try:
        import win32com.client
        app = win32com.client.Dispatch(app_name)
        app.Visible = False
        app.DisplayAlerts = False
        yield app
    except ImportError:
        raise RuntimeError("pywin32 not installed. Run: pip install pywin32")
    except Exception as e:
        raise RuntimeError(f"COM session failed [{app_name}]: {e}") from e
    finally:
        if app:
            try:
                app.Quit()
            except Exception:
                pass


def read_excel_via_com(filepath: str, sheet_name=None) -> dict:
    """Read Excel/WPS spreadsheet via COM. Returns dict with sheets data."""
    filepath = str(Path(filepath).resolve())
    suffix = Path(filepath).suffix.lower()
    app_name = "KET.Application" if suffix == ".et" else "Excel.Application"

    result = {}
    with safe_com_session(app_name) as app:
        wb = app.Workbooks.Open(filepath)
        logger.info(f"Opened: {filepath}")

        sheets_to_read = [wb.Sheets(sheet_name)] if sheet_name else list(wb.Sheets)
        for ws in sheets_to_read:
            ws_name = ws.Name
            raw = ws.UsedRange.Value
            if raw is None:
                result[ws_name] = []
            elif isinstance(raw, tuple) and isinstance(raw[0], tuple):
                result[ws_name] = [list(row) for row in raw]
            else:
                result[ws_name] = [list(raw)]
            logger.info(f"Sheet '{ws_name}': {len(result[ws_name])} rows")
        wb.Close(False)

    return result


def read_excel_offline(filepath: str, sheet_name=None) -> dict:
    """Read Excel via openpyxl — no Office installation required."""
    import openpyxl
    filepath = str(Path(filepath).resolve())
    file_size_mb = Path(filepath).stat().st_size / 1e6
    read_only = file_size_mb > 50
    if read_only:
        logger.info(f"Large file ({file_size_mb:.1f}MB), using read_only mode")

    wb = openpyxl.load_workbook(filepath, data_only=True, read_only=read_only)
    result = {}
    sheets = [wb[sheet_name]] if sheet_name else wb.worksheets
    for ws in sheets:
        result[ws.title] = [list(r) for r in ws.iter_rows(values_only=True)]
        logger.info(f"Sheet '{ws.title}': {len(result[ws.title])} rows")
    wb.close()
    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python win_excel_reader.py <filepath> [sheet_name]")
        sys.exit(1)

    filepath = sys.argv[1]
    sheet_name = sys.argv[2] if len(sys.argv) > 2 else None

    try:
        data = read_excel_via_com(filepath, sheet_name)
        logger.info("COM read successful")
    except Exception as e:
        logger.warning(f"COM read failed ({e}), falling back to openpyxl")
        data = read_excel_offline(filepath, sheet_name)

    output = json.dumps(data, ensure_ascii=False, default=str, indent=2)
    print(output)
    out_path = Path(filepath).stem + "_data.json"
    Path(out_path).write_text(output, encoding='utf-8')
    logger.info(f"Saved to: {out_path}")


if __name__ == "__main__":
    main()
