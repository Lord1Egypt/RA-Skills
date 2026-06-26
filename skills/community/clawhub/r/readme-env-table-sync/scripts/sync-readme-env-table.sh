#!/usr/bin/env bash
set -euo pipefail

ENV_FILE="${ENV_FILE:-.env.example}"
README_FILE="${README_FILE:-README.md}"
SYNC_MODE="${SYNC_MODE:-report}"
TABLE_START_MARKER="${TABLE_START_MARKER:-<!-- ENV_TABLE_START -->}"
TABLE_END_MARKER="${TABLE_END_MARKER:-<!-- ENV_TABLE_END -->}"

if [[ "$SYNC_MODE" != "report" && "$SYNC_MODE" != "apply" ]]; then
  echo "ERROR: SYNC_MODE must be 'report' or 'apply' (got: $SYNC_MODE)" >&2
  exit 1
fi

if [[ ! -f "$ENV_FILE" ]]; then
  echo "ERROR: ENV_FILE not found: $ENV_FILE" >&2
  exit 1
fi

if [[ ! -f "$README_FILE" ]]; then
  echo "ERROR: README_FILE not found: $README_FILE" >&2
  exit 1
fi

python3 - "$ENV_FILE" "$README_FILE" "$SYNC_MODE" "$TABLE_START_MARKER" "$TABLE_END_MARKER" <<'PY'
import sys
import re
from pathlib import Path


def parse_env_lines(env_text: str):
    items = []
    for raw in env_text.splitlines():
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('export '):
            line = line[len('export '):].strip()
        if '=' not in line:
            continue
        key, value = line.split('=', 1)
        key = key.strip()
        if not key:
            continue
        if not re.match(r'^[A-Za-z_][A-Za-z0-9_]*$', key):
            continue
        value = value.strip()
        if value == '':
            value_repr = '(empty)'
        else:
            value_repr = value
        items.append((key, value_repr))

    # stable + dedup, first key wins
    dedup = {}
    for key, value in items:
        if key not in dedup:
            dedup[key] = value
    return sorted(dedup.items(), key=lambda kv: kv[0].lower())


def build_table(pairs):
    lines = [
        '| ENV key | Default in template |',
        '|---|---|',
    ]
    for key, value in pairs:
        safe = value.replace('|', '\\|')
        lines.append(f'| `{key}` | `{safe}` |')
    if len(lines) == 2:
        lines.append('| _(none)_ | _(none)_ |')
    return '\n'.join(lines)


def replace_block(readme_text: str, start: str, end: str, new_block: str):
    start_idx = readme_text.find(start)
    if start_idx == -1:
        raise ValueError(f'missing start marker: {start}')
    end_idx = readme_text.find(end)
    if end_idx == -1:
        raise ValueError(f'missing end marker: {end}')
    if end_idx < start_idx:
        raise ValueError('end marker appears before start marker')

    body_start = start_idx + len(start)
    existing = readme_text[body_start:end_idx]

    normalized_new = '\n\n' + new_block + '\n\n'
    updated = readme_text[:body_start] + normalized_new + readme_text[end_idx:]
    return existing, normalized_new, updated


env_file = Path(sys.argv[1])
readme_file = Path(sys.argv[2])
mode = sys.argv[3]
start_marker = sys.argv[4]
end_marker = sys.argv[5]

env_text = env_file.read_text(encoding='utf-8')
readme_text = readme_file.read_text(encoding='utf-8')

pairs = parse_env_lines(env_text)
table = build_table(pairs)

try:
    existing, normalized_new, updated = replace_block(readme_text, start_marker, end_marker, table)
except ValueError as exc:
    print(f'ERROR: {exc}', file=sys.stderr)
    sys.exit(1)

if existing == normalized_new:
    print(f'OK: README env table already in sync ({len(pairs)} keys).')
    sys.exit(0)

if mode == 'report':
    print(f'DRIFT: README env table out of sync ({len(pairs)} keys).', file=sys.stderr)
    print('Run with SYNC_MODE=apply to update.', file=sys.stderr)
    sys.exit(1)

readme_file.write_text(updated, encoding='utf-8')
print(f'UPDATED: Synced README env table ({len(pairs)} keys).')
sys.exit(0)
PY
