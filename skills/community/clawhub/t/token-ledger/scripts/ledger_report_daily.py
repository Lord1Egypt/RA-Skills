#!/usr/bin/env python3
"""Deterministic daily finance report from ledger.db (no LLM needed)."""

import sqlite3
from pathlib import Path
from datetime import datetime

DB=Path.home()/'.openclaw/ledger.db'

def main():
  db=sqlite3.connect(str(DB))
  day=datetime.now().strftime('%Y-%m-%d')

  rows=db.execute('''
    SELECT provider, model,
      SUM(input_tokens) input,
      SUM(output_tokens) output,
      SUM(cache_read_tokens) cache_read,
      SUM(cache_write_tokens) cache_write,
      SUM(input_tokens + cache_read_tokens + cache_write_tokens) prompt_context,
      SUM(input_tokens + cache_read_tokens + cache_write_tokens + output_tokens) billed_total,
      SUM(cost_total) cost,
      MAX(cost_source) source
    FROM calls
    WHERE ts >= date('now')
    GROUP BY provider, model
    ORDER BY cost DESC
  ''').fetchall()

  total=db.execute('SELECT SUM(cost_total) FROM calls WHERE ts >= date(\'now\')').fetchone()[0] or 0

  print(f"🪙 Daily Ledger Report — {day}")
  print()
  for p, m, inp, out, cr, cw, pc, bt, cost, src in rows:
    print(f"{p}/{m}")
    print(f"- prompt_context: {pc:,} (in={inp:,} + cr={cr:,} + cw={cw:,})")
    print(f"- billed_total:   {bt:,} (prompt_context + out={out:,})")
    print(f"- cost: ${cost:.4f} ({src})")
    print()

  print(f"TOTAL: ${total:.4f}")

if __name__=='__main__':
  main()
