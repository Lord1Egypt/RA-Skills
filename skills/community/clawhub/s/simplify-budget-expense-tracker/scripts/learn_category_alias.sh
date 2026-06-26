#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "Usage: learn_category_alias.sh \"<raw expense message>\" \"<category>\"" >&2
  exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RAW_MESSAGE="$1"
CATEGORY_NAME="$2"
DATA_DIR="${SCRIPT_DIR}/../data"
LEARNED_ALIAS_FILE="${DATA_DIR}/learned_category_aliases.json"

mkdir -p "$DATA_DIR"

PARSED="$(bash "${SCRIPT_DIR}/log.sh" --preview --category "$CATEGORY_NAME" "$RAW_MESSAGE")"
DESCRIPTION="$(printf '%s' "$PARSED" | jq -r '.description')"
CATEGORY="$(printf '%s' "$PARSED" | jq -r '.category')"

python3 - "$LEARNED_ALIAS_FILE" "$CATEGORY" "$DESCRIPTION" <<'PY'
import json
import os
import re
import sys

path, category, description = sys.argv[1], sys.argv[2], sys.argv[3]

def normalize_phrase(text):
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = " ".join(text.split())
    return text

def singularize_word(word):
    if len(word) <= 3:
        return word
    if word.endswith("ies") and len(word) > 4:
        return word[:-3] + "y"
    if word.endswith("oes") and len(word) > 4:
        return word[:-2]
    if word.endswith("ses") and len(word) > 4:
        return word[:-2]
    if word.endswith("s") and not word.endswith("ss"):
        return word[:-1]
    return word

normalized = normalize_phrase(description)
if not normalized:
    print("SKIP: empty description")
    raise SystemExit(0)

tokens = normalized.split()
if len(tokens) > 4:
    print("SKIP: description too broad")
    raise SystemExit(0)

blocked = {
    "expense", "today", "yesterday", "thing", "stuff", "payment", "purchase",
    "bought", "spent", "paid"
}
meaningful = [tok for tok in tokens if tok not in blocked]
if not meaningful:
    print("SKIP: description not specific enough")
    raise SystemExit(0)

aliases = set()
aliases.add(" ".join(meaningful))
aliases.add(" ".join(singularize_word(tok) for tok in meaningful))
aliases = {alias.strip() for alias in aliases if alias.strip()}

if not aliases:
    print("SKIP: no safe aliases")
    raise SystemExit(0)

data = {}
if os.path.exists(path):
    try:
      with open(path, "r", encoding="utf-8") as f:
          loaded = json.load(f)
          if isinstance(loaded, dict):
              data = loaded
    except Exception:
      data = {}

bucket = data.setdefault(category, [])
existing = {normalize_phrase(item) for item in bucket if isinstance(item, str)}
new_items = []
for alias in sorted(aliases):
    if normalize_phrase(alias) not in existing:
        bucket.append(alias)
        new_items.append(alias)

with open(path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=True, sort_keys=True)
    f.write("\n")

if new_items:
    print("LEARNED: " + ", ".join(new_items))
else:
    print("LEARNED: no-op")
PY
