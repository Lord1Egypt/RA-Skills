#!/usr/bin/env python3
import argparse
import json
import os
import sqlite3
from pathlib import Path
from datetime import datetime, timezone


def resolve_skill_dir():
    cli = argparse.ArgumentParser(add_help=False)
    cli.add_argument('--skill-dir')
    args, _ = cli.parse_known_args()
    if args.skill_dir:
        return Path(args.skill_dir).expanduser().resolve()
    env_skill_dir = os.environ.get('SESSION_TOKEN_LEDGER_SKILL_DIR')
    if env_skill_dir:
        return Path(env_skill_dir).expanduser().resolve()
    return Path(__file__).resolve().parent.parent


SKILL_DIR = resolve_skill_dir()
WORKSPACE = SKILL_DIR.parent.parent
OPENCLAW_ROOT = WORKSPACE.parent
SESSIONS_DIR = OPENCLAW_ROOT / 'agents' / 'main' / 'sessions'
ASSETS_DIR = SKILL_DIR / 'assets'
REFERENCES_DIR = SKILL_DIR / 'references'
DB_PATH = ASSETS_DIR / 'session_tokens.db'
TMP_DB_PATH = ASSETS_DIR / 'session_tokens.tmp.db'
TOTAL_PATH = ASSETS_DIR / 'TOTAL_TOKENS.txt'
INDEX_PATH = ASSETS_DIR / 'index.json'
ANOMALIES_PATH = REFERENCES_DIR / 'ANOMALIES.md'
SQL_TEMPLATES_PATH = REFERENCES_DIR / 'queries.sql'

ASSETS_DIR.mkdir(parents=True, exist_ok=True)
REFERENCES_DIR.mkdir(parents=True, exist_ok=True)

BILLING_MODE = 'subscription'

PRICING = {
    'gpt-5.4': {
        'input_per_million': 0.0,
        'output_per_million': 0.0,
        'cache_read_per_million': 0.0,
        'cache_write_per_million': 0.0,
        'note': 'Subscription mode active; token cost is not directly billed per session.'
    }
}
DEFAULT_PRICING = {
    'input_per_million': 0.0,
    'output_per_million': 0.0,
    'cache_read_per_million': 0.0,
    'cache_write_per_million': 0.0,
    'note': 'Unknown model pricing or non-API billing mode.'
}


def iso_now():
    return datetime.now(timezone.utc).isoformat()


def parse_session_file(file_path: Path):
    input_tokens = output_tokens = cache_read = cache_write = 0
    start_at = ''
    end_at = ''
    model = provider = agent = channel = session_key = None
    usage_entries = bad_lines = total_lines = 0

    with file_path.open('r', encoding='utf-8') as f:
        for line in f:
            total_lines += 1
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                bad_lines += 1
                continue
            ts = obj.get('timestamp')
            if isinstance(ts, str):
                if not start_at:
                    start_at = ts
                end_at = ts
            if not session_key and isinstance(obj.get('sessionKey'), str):
                session_key = obj['sessionKey']
                parts = session_key.split(':')
                if len(parts) >= 2:
                    agent = parts[1]
                if len(parts) >= 4:
                    channel = parts[2]
            msg = obj.get('message') or {}
            if not model and isinstance(msg.get('model'), str):
                model = msg['model']
            if not provider and isinstance(msg.get('provider'), str):
                provider = msg['provider']
            usage = msg.get('usage') or {}
            if usage:
                usage_entries += 1
                input_tokens += int(usage.get('input', 0) or 0)
                output_tokens += int(usage.get('output', 0) or 0)
                cache_read += int(usage.get('cacheRead', 0) or 0)
                cache_write += int(usage.get('cacheWrite', 0) or 0)

    if not start_at:
        ts = datetime.fromtimestamp(file_path.stat().st_mtime, tz=timezone.utc).isoformat()
        start_at = ts
        end_at = ts

    session_id = file_path.name
    reset_source = None
    was_reset_file = 0
    if '.jsonl.reset.' in session_id:
        was_reset_file = 1
        reset_source = file_path.name.split('.jsonl.reset.', 1)[1]
        session_id = session_id.split('.jsonl.reset.')[0]
    elif session_id.endswith('.jsonl'):
        session_id = session_id[:-6]

    pricing = PRICING.get(model or '', DEFAULT_PRICING)
    cost_applicable = 1 if BILLING_MODE in ('api', 'hybrid') else 0
    estimated_cost_usd = 0.0
    if cost_applicable:
        estimated_cost_usd = (
            input_tokens * pricing['input_per_million'] / 1_000_000
            + output_tokens * pricing['output_per_million'] / 1_000_000
            + cache_read * pricing['cache_read_per_million'] / 1_000_000
            + cache_write * pricing['cache_write_per_million'] / 1_000_000
        )

    return {
        'session_id': session_id,
        'file_path': str(file_path),
        'start_at': start_at,
        'end_at': end_at,
        'date': start_at[:10],
        'input_tokens': input_tokens,
        'output_tokens': output_tokens,
        'total_tokens': input_tokens + output_tokens,
        'cache_read_tokens': cache_read,
        'cache_write_tokens': cache_write,
        'model': model,
        'provider': provider,
        'agent': agent,
        'channel': channel,
        'session_key': session_key,
        'usage_entries': usage_entries,
        'bad_lines': bad_lines,
        'total_lines': total_lines,
        'billing_mode': BILLING_MODE,
        'cost_applicable': cost_applicable,
        'estimated_cost_usd': round(estimated_cost_usd, 8),
        'pricing_note': pricing['note'],
        'was_reset_file': was_reset_file,
        'reset_source': reset_source,
    }


def list_transcripts():
    if not SESSIONS_DIR.exists():
        return []
    files = []
    for p in SESSIONS_DIR.iterdir():
        if p.name.endswith('.lock'):
            continue
        if not (p.name.endswith('.jsonl') or '.jsonl.reset.' in p.name):
            continue
        if p.name.endswith('.jsonl') and Path(str(p) + '.lock').exists():
            continue
        files.append(p)
    files.sort(key=lambda p: p.stat().st_mtime)
    return files


def load_sessions_registry():
    reg = SESSIONS_DIR / 'sessions.json'
    if not reg.exists():
        return {}
    try:
        return json.loads(reg.read_text(encoding='utf-8'))
    except Exception:
        return {}


def enrich_from_registry(record, registry):
    for _, entry in registry.items():
        if not isinstance(entry, dict):
            continue
        session_file = entry.get('sessionFile')
        if session_file == record['file_path'] or (record['session_id'] and entry.get('sessionId') == record['session_id']):
            if not record.get('channel'):
                record['channel'] = entry.get('lastChannel') or (entry.get('deliveryContext') or {}).get('channel')
            origin = entry.get('origin') or {}
            if not record.get('provider'):
                record['provider'] = origin.get('provider')
            break
    return record


def build_database(records):
    if TMP_DB_PATH.exists():
        TMP_DB_PATH.unlink()
    conn = sqlite3.connect(TMP_DB_PATH)
    cur = conn.cursor()
    cur.execute('PRAGMA journal_mode=DELETE;')
    cur.executescript('''
    CREATE TABLE sessions (
      session_id TEXT PRIMARY KEY,
      date TEXT NOT NULL,
      index_for_date INTEGER NOT NULL,
      session_key TEXT,
      transcript_file TEXT NOT NULL,
      ledger_file TEXT NOT NULL,
      model TEXT,
      provider TEXT,
      agent TEXT,
      channel TEXT,
      started_at TEXT NOT NULL,
      ended_at TEXT NOT NULL,
      input_tokens INTEGER NOT NULL,
      output_tokens INTEGER NOT NULL,
      total_tokens INTEGER NOT NULL,
      cache_read_tokens INTEGER NOT NULL,
      cache_write_tokens INTEGER NOT NULL,
      billing_mode TEXT NOT NULL,
      cost_applicable INTEGER NOT NULL DEFAULT 0,
      estimated_cost_usd REAL NOT NULL DEFAULT 0,
      pricing_note TEXT,
      usage_entries INTEGER NOT NULL DEFAULT 0,
      bad_lines INTEGER NOT NULL DEFAULT 0,
      total_lines INTEGER NOT NULL DEFAULT 0,
      was_reset_file INTEGER NOT NULL DEFAULT 0,
      reset_source TEXT,
      updated_at TEXT NOT NULL
    );
    CREATE TABLE daily_summary (
      date TEXT PRIMARY KEY,
      session_count INTEGER NOT NULL,
      input_tokens INTEGER NOT NULL,
      output_tokens INTEGER NOT NULL,
      total_tokens INTEGER NOT NULL,
      cache_read_tokens INTEGER NOT NULL,
      cache_write_tokens INTEGER NOT NULL,
      cost_applicable_sessions INTEGER NOT NULL DEFAULT 0,
      estimated_cost_usd REAL NOT NULL DEFAULT 0,
      updated_at TEXT NOT NULL
    );
    ''')

    by_date_counter = {}
    index = {'version': 5, 'generated_at': iso_now(), 'billing_mode': BILLING_MODE, 'sessions': {}}
    anomalies = []

    for record in records:
        n = by_date_counter.get(record['date'], 0) + 1
        by_date_counter[record['date']] = n
        ledger_file = f"{record['date']}_{n}.md"
        ledger_path = ASSETS_DIR / ledger_file
        ledger_body = f'''# Session Token Log\n\n- Date: {record['date']}\n- Session index for date: {n}\n- Session ID: {record['session_id']}\n- Session key: {record.get('session_key') or 'unknown'}\n- Transcript file: {record['file_path']}\n- Model: {record.get('model') or 'unknown'}\n- Provider: {record.get('provider') or 'unknown'}\n- Agent: {record.get('agent') or 'unknown'}\n- Channel: {record.get('channel') or 'unknown'}\n- Started at: {record['start_at']}\n- Last transcript timestamp: {record['end_at']}\n- Input tokens: {record['input_tokens']}\n- Output tokens: {record['output_tokens']}\n- Session total tokens: {record['total_tokens']}\n- Cached read tokens: {record['cache_read_tokens']}\n- Cached write tokens: {record['cache_write_tokens']}\n- Usage entries: {record['usage_entries']}\n- Bad JSON lines skipped: {record['bad_lines']}\n- Reset transcript file: {bool(record['was_reset_file'])}\n- Billing mode: {record['billing_mode']}\n- Cost applicable: {bool(record['cost_applicable'])}\n- Estimated cost (USD): {record['estimated_cost_usd']}\n- Pricing note: {record['pricing_note']}\n\nNotes:\n- Session total tokens = input + output.\n- Cached tokens are recorded separately and are not added into the session total.\n- In subscription mode, cost fields are retained for portability but are not directly billable.\n'''
        ledger_path.write_text(ledger_body, encoding='utf-8')
        now = iso_now()
        cur.execute(
            '''INSERT INTO sessions (
                session_id, date, index_for_date, session_key, transcript_file, ledger_file, model,
                provider, agent, channel, started_at, ended_at, input_tokens, output_tokens, total_tokens,
                cache_read_tokens, cache_write_tokens, billing_mode, cost_applicable, estimated_cost_usd, pricing_note,
                usage_entries, bad_lines, total_lines, was_reset_file, reset_source, updated_at
              ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
            (
                record['session_id'], record['date'], n, record.get('session_key'), record['file_path'], ledger_file,
                record.get('model'), record.get('provider'), record.get('agent'), record.get('channel'),
                record['start_at'], record['end_at'], record['input_tokens'], record['output_tokens'],
                record['total_tokens'], record['cache_read_tokens'], record['cache_write_tokens'],
                record['billing_mode'], record['cost_applicable'], record['estimated_cost_usd'], record['pricing_note'],
                record['usage_entries'], record['bad_lines'], record['total_lines'], record['was_reset_file'],
                record['reset_source'], now,
            ),
        )
        if record['bad_lines'] > 0:
            anomalies.append(f"- {record['session_id']}: skipped {record['bad_lines']} bad JSON line(s) in {record['file_path']}")
        if record['usage_entries'] == 0:
            anomalies.append(f"- {record['session_id']}: no usage entries found in {record['file_path']}")
        if record['total_tokens'] == 0:
            anomalies.append(f"- {record['session_id']}: total_tokens=0 in {record['file_path']}")
        index['sessions'][record['session_id']] = {**record, 'ledger_file': ledger_file, 'index_for_date': n}

    cur.execute('''
    INSERT INTO daily_summary (
      date, session_count, input_tokens, output_tokens, total_tokens,
      cache_read_tokens, cache_write_tokens, cost_applicable_sessions, estimated_cost_usd, updated_at
    )
    SELECT
      date, COUNT(*), SUM(input_tokens), SUM(output_tokens), SUM(total_tokens),
      SUM(cache_read_tokens), SUM(cache_write_tokens), SUM(cost_applicable), SUM(estimated_cost_usd), ?
    FROM sessions
    GROUP BY date
    ''', (iso_now(),))

    cur.executescript('''
    CREATE VIEW overall_summary AS
    SELECT COUNT(*) AS total_sessions,
           COALESCE(SUM(input_tokens), 0) AS total_input_tokens,
           COALESCE(SUM(output_tokens), 0) AS total_output_tokens,
           COALESCE(SUM(total_tokens), 0) AS total_tokens,
           COALESCE(SUM(cache_read_tokens), 0) AS total_cache_read_tokens,
           COALESCE(SUM(cache_write_tokens), 0) AS total_cache_write_tokens,
           MIN(billing_mode) AS billing_mode,
           COALESCE(SUM(cost_applicable), 0) AS cost_applicable_sessions,
           COALESCE(SUM(estimated_cost_usd), 0) AS estimated_cost_usd
    FROM sessions;

    CREATE VIEW model_summary AS
    SELECT COALESCE(model, 'unknown') AS model, COUNT(*) AS session_count,
           SUM(input_tokens) AS input_tokens, SUM(output_tokens) AS output_tokens,
           SUM(total_tokens) AS total_tokens, MIN(billing_mode) AS billing_mode,
           SUM(cost_applicable) AS cost_applicable_sessions,
           SUM(estimated_cost_usd) AS estimated_cost_usd
    FROM sessions GROUP BY COALESCE(model, 'unknown') ORDER BY total_tokens DESC;

    CREATE VIEW provider_summary AS
    SELECT COALESCE(provider, 'unknown') AS provider, COUNT(*) AS session_count,
           SUM(total_tokens) AS total_tokens, MIN(billing_mode) AS billing_mode,
           SUM(cost_applicable) AS cost_applicable_sessions,
           SUM(estimated_cost_usd) AS estimated_cost_usd
    FROM sessions GROUP BY COALESCE(provider, 'unknown') ORDER BY total_tokens DESC;

    CREATE VIEW channel_summary AS
    SELECT COALESCE(channel, 'unknown') AS channel, COUNT(*) AS session_count,
           SUM(total_tokens) AS total_tokens, MIN(billing_mode) AS billing_mode,
           SUM(cost_applicable) AS cost_applicable_sessions,
           SUM(estimated_cost_usd) AS estimated_cost_usd
    FROM sessions GROUP BY COALESCE(channel, 'unknown') ORDER BY total_tokens DESC;

    CREATE VIEW largest_sessions AS
    SELECT session_id, date, channel, model, billing_mode, input_tokens, output_tokens, total_tokens, estimated_cost_usd
    FROM sessions ORDER BY total_tokens DESC;

    CREATE VIEW cost_estimate AS
    SELECT session_id, date, model, provider, channel, billing_mode,
           cost_applicable, input_tokens, output_tokens,
           cache_read_tokens, cache_write_tokens, estimated_cost_usd, pricing_note
    FROM sessions
    WHERE cost_applicable = 1
    ORDER BY estimated_cost_usd DESC, total_tokens DESC;

    CREATE VIEW usage_efficiency AS
    SELECT session_id, date, channel, model, billing_mode,
           input_tokens, output_tokens, total_tokens,
           ROUND(CASE WHEN output_tokens = 0 THEN NULL ELSE CAST(input_tokens AS REAL) / output_tokens END, 2) AS input_output_ratio,
           usage_entries
    FROM sessions
    ORDER BY total_tokens DESC;

    CREATE VIEW bloated_sessions AS
    SELECT session_id, date, channel, model,
           input_tokens, output_tokens, total_tokens,
           ROUND(CASE WHEN output_tokens = 0 THEN NULL ELSE CAST(input_tokens AS REAL) / output_tokens END, 2) AS input_output_ratio,
           ROUND(CASE WHEN usage_entries = 0 THEN NULL ELSE CAST(total_tokens AS REAL) / usage_entries END, 2) AS tokens_per_usage_entry,
           usage_entries
    FROM sessions
    WHERE total_tokens >= 100000 OR input_tokens >= 100000 OR (output_tokens > 0 AND CAST(input_tokens AS REAL) / output_tokens >= 12)
    ORDER BY total_tokens DESC, input_output_ratio DESC;

    CREATE VIEW channel_efficiency AS
    SELECT COALESCE(channel, 'unknown') AS channel,
           COUNT(*) AS session_count,
           SUM(input_tokens) AS input_tokens,
           SUM(output_tokens) AS output_tokens,
           SUM(total_tokens) AS total_tokens,
           ROUND(CASE WHEN SUM(output_tokens) = 0 THEN NULL ELSE CAST(SUM(input_tokens) AS REAL) / SUM(output_tokens) END, 2) AS input_output_ratio,
           ROUND(CAST(SUM(total_tokens) AS REAL) / COUNT(*), 2) AS avg_tokens_per_session
    FROM sessions
    GROUP BY COALESCE(channel, 'unknown')
    ORDER BY total_tokens DESC;

    CREATE VIEW daily_efficiency AS
    SELECT date,
           COUNT(*) AS session_count,
           SUM(input_tokens) AS input_tokens,
           SUM(output_tokens) AS output_tokens,
           SUM(total_tokens) AS total_tokens,
           ROUND(CASE WHEN SUM(output_tokens) = 0 THEN NULL ELSE CAST(SUM(input_tokens) AS REAL) / SUM(output_tokens) END, 2) AS input_output_ratio,
           ROUND(CAST(SUM(total_tokens) AS REAL) / COUNT(*), 2) AS avg_tokens_per_session
    FROM sessions
    GROUP BY date
    ORDER BY date DESC;

    CREATE VIEW top_context_hogs AS
    SELECT session_id, date, channel, model,
           input_tokens,
           ROUND(CAST(input_tokens AS REAL) / total_tokens, 4) AS input_share_of_total,
           total_tokens,
           usage_entries
    FROM sessions
    ORDER BY input_tokens DESC, total_tokens DESC;
    ''')

    conn.commit()
    summary = cur.execute('SELECT total_sessions, total_input_tokens, total_output_tokens, total_tokens, total_cache_read_tokens, total_cache_write_tokens, billing_mode, cost_applicable_sessions, estimated_cost_usd FROM overall_summary').fetchone()
    conn.close()
    TMP_DB_PATH.replace(DB_PATH)

    TOTAL_PATH.write_text(
        f'''Session token ledger total\n\nCounted sessions: {summary[0]}\nTotal input tokens: {summary[1]}\nTotal output tokens: {summary[2]}\nTotal session tokens (input + output): {summary[3]}\nTotal cached read tokens recorded separately: {summary[4]}\nTotal cached write tokens recorded separately: {summary[5]}\nBilling mode: {summary[6]}\nCost-applicable sessions: {summary[7]}\nEstimated cost USD: {summary[8]}\nLast updated: {iso_now()}\nDatabase: {DB_PATH}\n''',
        encoding='utf-8'
    )
    INDEX_PATH.write_text(json.dumps(index, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    ANOMALIES_PATH.write_text('# Session Token Ledger Anomalies\n\n' + ('\n'.join(anomalies) if anomalies else '- None detected') + '\n', encoding='utf-8')
    if not SQL_TEMPLATES_PATH.exists():
        SQL_TEMPLATES_PATH.write_text('-- Query templates are shipped with this skill.\n', encoding='utf-8')


def main():
    records = [parse_session_file(p) for p in list_transcripts()]
    registry = load_sessions_registry()
    records = [enrich_from_registry(r, registry) for r in records]
    records.sort(key=lambda r: r['start_at'])
    build_database(records)
    print(DB_PATH)


if __name__ == '__main__':
    main()
