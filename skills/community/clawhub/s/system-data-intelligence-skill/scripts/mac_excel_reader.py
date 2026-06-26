#!/usr/bin/env python3
"""
macOS Excel Reader via xlwings or AppleScript.
Usage: python mac_excel_reader.py <filepath> [sheet_name]
"""

import sys
import json
import logging
import subprocess
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)


def read_excel_xlwings(filepath: str, sheet_name=None) -> dict:
    """Read Excel via xlwings (requires Excel for Mac)."""
    import xlwings as xw
    filepath = str(Path(filepath).resolve())
    result = {}
    app = xw.App(visible=False)
    try:
        wb = app.books.open(filepath)
        logger.info(f"Opened: {filepath}")
        sheets = [wb.sheets[sheet_name]] if sheet_name else wb.sheets
        for ws in sheets:
            data = ws.used_range.value
            if data is None:
                result[ws.name] = []
            elif isinstance(data[0], list):
                result[ws.name] = data
            else:
                result[ws.name] = [data]
            logger.info(f"Sheet '{ws.name}': {len(result[ws.name])} rows")
        wb.close()
    finally:
        app.quit()
    return result


def read_excel_applescript(filepath: str, sheet_name: str = None) -> dict:
    """Read Excel via AppleScript fallback."""
    filepath = str(Path(filepath).resolve())
    sheet_selector = f'sheet "{sheet_name}"' if sheet_name else 'active sheet'
    script = f'''
    tell application "Microsoft Excel"
        open "{filepath}"
        set ws to {sheet_selector} of active workbook
        set data to value of used range of ws
        close active workbook saving no
        return data
    end tell
    '''
    result = subprocess.run(
        ['osascript', '-e', script],
        capture_output=True, text=True, timeout=120
    )
    if result.returncode != 0:
        raise RuntimeError(f"AppleScript error: {result.stderr}")
    return {sheet_name or 'Sheet1': result.stdout.strip()}


def read_excel_offline(filepath: str, sheet_name=None) -> dict:
    """Read Excel via openpyxl — offline fallback."""
    import openpyxl
    filepath = str(Path(filepath).resolve())
    wb = openpyxl.load_workbook(filepath, data_only=True)
    result = {}
    sheets = [wb[sheet_name]] if sheet_name else wb.worksheets
    for ws in sheets:
        result[ws.title] = [list(r) for r in ws.iter_rows(values_only=True)]
        logger.info(f"Sheet '{ws.title}': {len(result[ws.title])} rows")
    wb.close()
    return result


def main():
    if len(sys.argv) < 2:
        print("Usage: python mac_excel_reader.py <filepath> [sheet_name]")
        sys.exit(1)

    filepath = sys.argv[1]
    sheet_name = sys.argv[2] if len(sys.argv) > 2 else None

    for strategy_name, strategy in [
        ("xlwings", lambda: read_excel_xlwings(filepath, sheet_name)),
        ("AppleScript", lambda: read_excel_applescript(filepath, sheet_name)),
        ("openpyxl", lambda: read_excel_offline(filepath, sheet_name)),
    ]:
        try:
            data = strategy()
            logger.info(f"Strategy '{strategy_name}' succeeded")
            break
        except Exception as e:
            logger.warning(f"Strategy '{strategy_name}' failed: {e}")
    else:
        logger.error("All strategies failed")
        sys.exit(1)

    output = json.dumps(data, ensure_ascii=False, default=str, indent=2)
    print(output)
    out_path = Path(filepath).stem + "_data.json"
    Path(out_path).write_text(output, encoding='utf-8')
    logger.info(f"Saved to: {out_path}")


if __name__ == "__main__":
    main()
