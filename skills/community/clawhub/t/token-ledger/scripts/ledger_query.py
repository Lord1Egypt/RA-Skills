#!/usr/bin/env python3
"""token-ledger query (safe presets)

Usage:
  python3 ledger_query.py today
  python3 ledger_query.py history --days 30
  python3 ledger_query.py top-sessions --days 7 --limit 20

All queries read from ~/.openclaw/ledger.db.
"""

import argparse, sqlite3
from pathlib import Path

DB=Path.home()/'.openclaw/ledger.db'

def q_today(db):
  return db.execute('''
    SELECT provider, model,
      COUNT(*) calls,
      SUM(input_tokens) input,
      SUM(output_tokens) output,
      SUM(cache_read_tokens) cache_read,
      SUM(cache_write_tokens) cache_write,
      SUM(input_tokens + cache_read_tokens + cache_write_tokens) prompt_context,
      SUM(input_tokens + cache_read_tokens + cache_write_tokens + output_tokens) billed_total,
      ROUND(SUM(cost_total), 6) cost
    FROM calls
    WHERE ts >= date('now')
    GROUP BY provider, model
    ORDER BY cost DESC
  ''').fetchall()

def q_history(db, days):
  return db.execute('''
    SELECT substr(ts,1,10) day,
      ROUND(SUM(cost_total), 6) cost,
      SUM(input_tokens + cache_read_tokens + cache_write_tokens + output_tokens) billed_total
    FROM calls
    WHERE ts >= date('now', ?)
    GROUP BY day
    ORDER BY day
  ''', (f'-{days} days',)).fetchall()

def q_top_sessions(db, days, limit):
  return db.execute('''
    SELECT session_key,
      COUNT(*) calls,
      ROUND(SUM(cost_total), 6) cost,
      SUM(input_tokens + cache_read_tokens + cache_write_tokens + output_tokens) billed_total
    FROM calls
    WHERE ts >= date('now', ?)
    GROUP BY session_key
    ORDER BY cost DESC
    LIMIT ?
  ''', (f'-{days} days', limit)).fetchall()


def main():
  ap=argparse.ArgumentParser()
  ap.add_argument('cmd', choices=['today','history','top-sessions'])
  ap.add_argument('--days', type=int, default=30)
  ap.add_argument('--limit', type=int, default=20)
  args=ap.parse_args()

  db=sqlite3.connect(str(DB))
  if args.cmd=='today':
    rows=q_today(db)
    print('provider\tmodel\tcalls\tinput\toutput\tcache_read\tcache_write\tprompt_context\tbilled_total\tcost')
    for r in rows:
      print('\t'.join(map(str,r)))
  elif args.cmd=='history':
    rows=q_history(db,args.days)
    print('day\tcost\tbilled_total')
    for r in rows:
      print('\t'.join(map(str,r)))
  else:
    rows=q_top_sessions(db,args.days,args.limit)
    print('session_key\tcalls\tcost\tbilled_total')
    for r in rows:
      print('\t'.join(map(str,r)))

if __name__=='__main__':
  main()
