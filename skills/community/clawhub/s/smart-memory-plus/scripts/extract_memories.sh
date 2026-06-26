#!/usr/bin/env bash
# extract_memories.sh — Extract memories from conversation.
#
# Usage:
#   extract_memories.sh                    — Output extraction guide only
#   extract_memories.sh --auto <text>      — Auto-extract from provided text
#   extract_memories.sh --from-stdin       — Read conversation text from stdin

set -euo pipefail

WORKSPACE="${OPENCLAW_WORKSPACE:-$HOME/.openclaw/workspace}"
TODAY=$(date -u '+%Y-%m-%d')
DAILY_FILE="$WORKSPACE/memory/${TODAY}.md"

# Ensure memory directory exists
mkdir -p "$WORKSPACE/memory"

# Create daily file if it doesn't exist
if [ ! -f "$DAILY_FILE" ]; then
    cat > "$DAILY_FILE" << EOF
# ${TODAY}

EOF
fi

case "${1:-guide}" in
    --auto)
        shift
        TEXT="$*"
        if [ -z "$TEXT" ]; then
            echo "Error: no text provided"
            exit 1
        fi
        # Use Python for safe extraction (no shell injection)
        python3 - "$WORKSPACE" "$DAILY_FILE" "$TEXT" << 'PYEOF'
import sys, re, os
from datetime import datetime, timezone

workspace = sys.argv[1]
daily_file = sys.argv[2]
text = sys.argv[3]

# Type detection keywords (subset for quick extraction)
TYPE_MAP = {
    "PREF": ["prefer", "like", "dislike", "favorite", "习惯", "喜欢", "讨厌", "偏好"],
    "PROJ": ["project", "deploy", "website", "项目", "网站", "部署", "github.com"],
    "TECH": ["config", "database", "api", "server", "配置", "数据库", "端口", "prompt"],
    "LESSON": ["lesson", "learned", "mistake", "error", "教训", "错误", "记住", "don't"],
    "PEOPLE": ["person", "name", "team", "用户", "人", "名字", "老板"],
}

SENSITIVE = re.compile(
    r"(?:password|passwd|pwd)\s*[:=]\s*\S+|"
    r"(?:api[_-]?key|token|secret|bearer)\s*[:=]\s*\S+|"
    r"clh_[A-Za-z0-9]{30,}|sk-[A-Za-z0-9]{20,}|ghp_[A-Za-z0-9]{30,}|"
    r"-----BEGIN (?:RSA |EC )?PRIVATE KEY-----",
    re.IGNORECASE,
)

# Split by newlines first; if only 1 line, also split by sentence boundaries
raw_lines = text.split("\n")
if len(raw_lines) == 1 and len(text) > 80:
    # Split single long line into sentences for better extraction
    sentences = re.split(r'(?<=[.!?。！？])\s+', text)
    lines = [s.strip() for s in sentences if s.strip()]
else:
    lines = [l.strip() for l in raw_lines]

extracted = []
current_type = None

for line in lines:
    line = line.strip()
    if not line or line.startswith("#") or line.startswith("```"):
        continue
    # Skip sensitive content
    if SENSITIVE.search(line):
        continue
    # Detect type
    lower = line.lower()
    for t, keywords in TYPE_MAP.items():
        if any(kw in lower for kw in keywords):
            current_type = t
            break
    # Extract meaningful statements (not questions, not short)
    if len(line) > 15 and not line.endswith("?"):
        tag = f"[{current_type}]" if current_type else "[TECH]"
        extracted.append(f"{tag} {line.lstrip('- *')}")

if extracted:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    with open(daily_file, "a", encoding="utf-8") as f:
        f.write(f"\n## Auto-extracted ({ts})\n")
        for item in extracted[:10]:  # Cap at 10
            f.write(f"- {item}\n")
    print(f"Extracted {min(len(extracted), 10)} memories → {daily_file}")
else:
    print("Nothing to extract.")
PYEOF
        ;;

    --from-stdin)
        TEXT=$(cat)
        exec "$0" --auto "$TEXT"
        ;;

    guide|*)
        echo "=== Memory Extraction Guide ==="
        echo "Today: $TODAY"
        echo "Daily file: $DAILY_FILE"
        echo ""
        echo "--- Usage ---"
        echo "  --auto <text>    Auto-extract from provided text"
        echo "  --from-stdin     Read conversation from stdin"
        echo "  (no args)        Show this guide"
        echo ""
        echo "--- Extraction Instructions ---"
        echo "1. Review the conversation for durable facts"
        echo "2. Classify each by type: [PREF] [PROJ] [TECH] [LESSON] [PEOPLE]"
        echo "3. Append to $DAILY_FILE with type tags"
        echo "4. Promote high-importance items to MEMORY.md"
        echo ""
        echo "--- Template ---"
        echo ""
        cat << 'TMPL'
## [TYPE] Category Name
- Description of the memory item
- Another item if applicable

Where [TYPE] is one of:
  [PREF]   — User preference, habit, style
  [PROJ]   — Project context, active work
  [TECH]   — Technical detail, config, system fact
  [LESSON] — Lesson learned, error correction
  [PEOPLE] — Person, relationship, social context
TMPL
        ;;
esac
