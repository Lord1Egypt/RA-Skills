#!/usr/bin/env python3
"""Import Anthropic (Claude) daily usage CSV into token-ledger SQLite.

The CSV is expected to have columns like:
usage_date_utc,model_version,...,usage_input_tokens_no_cache,usage_input_tokens_cache_write_5m,usage_input_tokens_cache_read,usage_output_tokens,...

Usage:
  python3 import_claude_usage_csv.py /path/to/file.csv

Writes into table: provider_daily_usage
"""

import csv
import json
import sys
import sqlite3
from pathlib import Path
from datetime import datetime, timezone

DB = Path.home() / '.openclaw/ledger.db'

def ensure_table(db: sqlite3.Connection):
    db.execute('''
    CREATE TABLE IF NOT EXISTS provider_daily_usage (
      provider       TEXT NOT NULL,
      usage_date_utc  TEXT NOT NULL,
      model_version  TEXT NOT NULL,
      usage_type     TEXT,
      context_window TEXT,
      input_no_cache INTEGER DEFAULT 0,
      cache_write_5m INTEGER DEFAULT 0,
      cache_write_1h INTEGER DEFAULT 0,
      cache_read     INTEGER DEFAULT 0,
      output_tokens  INTEGER DEFAULT 0,
      web_search_count INTEGER DEFAULT 0,
      inference_geo  TEXT,
      speed          TEXT,
      source_file    TEXT,
      imported_at    TEXT NOT NULL,
      raw_row        TEXT,
      PRIMARY KEY (provider, usage_date_utc, model_version, usage_type, context_window, inference_geo, speed)
    );
    ''')
    db.execute('CREATE INDEX IF NOT EXISTS idx_pdu_day ON provider_daily_usage(usage_date_utc);')
    db.commit()


def main():
    if len(sys.argv) < 2:
        print('Usage: python3 import_claude_usage_csv.py /path/to/file.csv', file=sys.stderr)
        sys.exit(2)

    src = Path(sys.argv[1]).expanduser().resolve()
    if not src.exists():
        raise SystemExit(f'File not found: {src}')

    db = sqlite3.connect(str(DB))
    ensure_table(db)

    imported_at = datetime.now(timezone.utc).isoformat()

    with src.open('r', newline='', encoding='utf-8') as f:
        r = csv.DictReader(f)
        rows = []
        for row in r:
            rows.append((
                'anthropic',
                row.get('usage_date_utc'),
                row.get('model_version'),
                row.get('usage_type'),
                row.get('context_window'),
                int(row.get('usage_input_tokens_no_cache') or 0),
                int(row.get('usage_input_tokens_cache_write_5m') or 0),
                int(row.get('usage_input_tokens_cache_write_1h') or 0),
                int(row.get('usage_input_tokens_cache_read') or 0),
                int(row.get('usage_output_tokens') or 0),
                int(row.get('web_search_count') or 0),
                row.get('inference_geo'),
                row.get('speed') or '',
                str(src),
                imported_at,
                json.dumps(row, ensure_ascii=False),
            ))

    db.executemany('''
      INSERT OR REPLACE INTO provider_daily_usage
      (provider, usage_date_utc, model_version, usage_type, context_window,
       input_no_cache, cache_write_5m, cache_write_1h, cache_read, output_tokens,
       web_search_count, inference_geo, speed, source_file, imported_at, raw_row)
      VALUES (?,?,?,?,?, ?,?,?,?,?, ?,?,?, ?,?,?)
    ''', rows)
    db.commit()

    print(f'Imported {len(rows)} rows into provider_daily_usage from {src.name}')

if __name__ == '__main__':
    main()
