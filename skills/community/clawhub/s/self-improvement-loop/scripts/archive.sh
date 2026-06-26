#!/bin/bash
# archive.sh — Self-improvement Hot/Cold ETL
# v4.6.3 — silent 模式：dry-run 预览后自动执行
# v4.6.3 新增：recurrence_count 由归档时统计历史 JSONL 计算，不依赖 AI
# v4.6.3 新增：--write-notified 用 Python 重写，支持 entry_id fallback + pending JSON 生成
# 设计原则：「脚本做机械，AI 做语义」
# Modes:
#   --dry-run   — 只输出预览，不写入文件
#   (no args)   — Silent 执行：预览 + 自动归档，无交互
#   --write-notified — 由 self-improvement-check 调用，写回 notified 状态

WORKSPACE="${HOME}/.openclaw/workspace"
LEARNINGS_DIR="$WORKSPACE/.learnings"
ARCHIVE_DIR="$LEARNINGS_DIR/archive"
TIMESTAMP=$(date '+%Y-%m-%dT%H:%M:%S+08:00')
TODAY_MONTH=$(date '+%Y-%m')
DRY_RUN=false

# ── Parse args ──────────────────────────────────────────────
if [ "$1" = "--dry-run" ]; then
    DRY_RUN=true
fi
if [ "$1" = "--write-notified" ]; then
    JSON_FILE="$2"
    [ -z "$JSON_FILE" ] && echo "Error: --write-notified requires JSON file" && exit 1
    [ ! -f "$JSON_FILE" ] && echo "Error: JSON file not found: $JSON_FILE" && exit 1
    WRITE_NOTIFIED_PY="$WORKSPACE/skills/self-improvement-loop/scripts/write_notified.py"
    # v4.6.3: pass entry_id field to write_notified.py via a temp JSON with entry_id populated
    # Read the distill-check JSON and inject entry_id from first_entry_id, then call write_notified.py
    PENDING_DIR="$LEARNINGS_DIR/.pending_notifications"
    # v4.7.1: Fix - python3 JSON_FILE would execute JSON as script
    # Use "python3 -" to read JSON_FILE as data, heredoc as stdin
    python3 - "$JSON_FILE" "$LEARNINGS_DIR" "$WRITE_NOTIFIED_PY" <<'PYEOF'
import json, sys, subprocess, os

json_file = sys.argv[1]
learnings_dir = sys.argv[2]
write_notified_py = sys.argv[3]

with open(json_file) as f:
    data = json.load(f)

patterns = data.get("patterns", [])
category_fallback = data.get("category_fallback", [])

for entry in patterns + category_fallback:
    name = entry.get("name", "")
    count = entry.get("count", 1)
    raw_md = entry.get("raw_md", "")
    # v4.6.3: entry_id = first_entry_id (精确匹配 MD 标题), pattern_name = name (兼容旧版)
    entry_id = entry.get("first_entry_id", "") or name
    pattern_name = name
    triggered = entry.get("notification_trigger", 0)
    nc = entry.get("notification_count", 1)

    if not triggered:
        continue

    # Escape raw_md for JSON string
    raw_md_esc = json.dumps(raw_md)[1:-1]  # strip outer quotes from json.dumps
    safe_name = "".join(c if c.isalnum() or c in "._-" else "_" for c in pattern_name)
    ts = str(int(subprocess.check_output(["date", "+%s"]).strip()))
    pending_dir = os.path.join(learnings_dir, ".pending_notifications")
    os.makedirs(pending_dir, exist_ok=True)
    out_path = os.path.join(pending_dir, f"{ts}_{safe_name}.json")

    notify_json = {
        "entry_id": entry_id,
        "pattern_name": pattern_name,
        "count": count,
        "notification_count": nc,  # v4.6.8: include nc for write_notified.py old mode
        "raw_md": raw_md,
        "action_taken": "pending",
        "notified_at": subprocess.check_output(["date", "+%Y-%m-%dT%H:%M:%S+08:00"]).strip().decode()
    }
    with open(out_path, "w") as out:
        json.dump(notify_json, out, ensure_ascii=False)

    # Update MD file via write_notified.py
    result = subprocess.run(
        ["python3", write_notified_py, "--status", "active", "--notified", "1", "--nc", str(nc + 1), entry_id, learnings_dir],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print(f"WARNING: write_notified failed for {entry_id}: {result.stderr}", file=sys.stderr)

PYEOF
    exit $?
fi

# ── Ensure archive dir exists ────────────────────────────────
mkdir -p "$ARCHIVE_DIR"

# ── Count how many times a Pattern-Key has appeared in archived JSONL files ──
# Called during archive to compute Recurrence-Count automatically
count_archived_occurrences() {
    local pk="$1"
    # Empty PK = each entry is unique
    [ -z "$pk" ] && echo "1" && return
    # Count occurrences of this PK in all existing archive JSONL files
    local count=0
    for jsonl_file in "$ARCHIVE_DIR"/*.jsonl; do
        [ -f "$jsonl_file" ] || continue
        local result
        result=$(grep -c "pattern_key.*$pk" "$jsonl_file" 2>/dev/null)
        [ -z "$result" ] && result=0
        count=$(( count + result ))
    done
    echo "$(( count + 1 ))"  # +1 because this entry will also be archived
}

# Escape string for JSON output (handles newlines, quotes, backslashes)
json_escape() {
    python3 -c "import sys,json; s=sys.stdin.read(); print(json.dumps(s)[1:-1])"
}

# ── Source file → source tag mapping ─────────────────────────
source_tag() {
    case "$1" in
        *LEARNINGS*)       echo "LEARNINGS" ;;
        *ERRORS*)          echo "ERRORS" ;;
        *FEATURE*)         echo "FEATURE" ;;
        *)                 echo "UNKNOWN" ;;
    esac
}

# ── Normalize status for outcome field ──────────────────────
normalize_outcome() {
    case "$1" in
        promoted)  echo "promoted" ;;
        resolved)  echo "resolved" ;;
        *)         echo "resolved" ;;
    esac
}

# ── Emit JSONL entry (centralized to avoid duplication) ─────
emit_entry() {
    local entry_lines="$1"
    local entry_id="$2"
    local entry_cat="$3"
    local current_status_val="$4"

    local outcome logged_at resolved_at pattern_key entry_id_short title_text
    local summary details suggested_action tags_str tag_json recurrence_count

    outcome=$(normalize_outcome "$current_status_val")
    logged_at=$(extract_meta "$entry_lines" "Logged")
    resolved_at="$TIMESTAMP"
    pattern_key=$(extract_meta "$entry_lines" "Pattern-Key")
    entry_id_short=$(echo "$entry_id" | sed 's/^## \[//;s/\].*//')
    title_text=$(echo "$entry_id" | sed -n 's/^## \[[^]]*] //p')
    summary=$(extract_field "$entry_lines" "What Happened")
    details=$(extract_field "$entry_lines" "Root Cause")
    suggested_action=$(extract_field "$entry_lines" "How To Avoid Next Time")
    tags_str=$(extract_meta "$entry_lines" "Tags")
    recurrence_count=$(count_archived_occurrences "$pattern_key")

    # Escape JSON strings
    summary=$(json_escape <<< "$summary")
    details=$(json_escape <<< "$details")
    suggested_action=$(json_escape <<< "$suggested_action")
    tags_str=$(json_escape <<< "$tags_str")
    title_text=$(json_escape <<< "$title_text")
    pattern_key=$(json_escape <<< "$pattern_key")

    if [ -n "$tags_str" ]; then
        tag_json=$(echo "$tags_str" | sed "s/, */\",\"/g; s/^/\"/; s/$/\"/")
        tag_json="[$tag_json]"
    else
        tag_json="[]"
    fi

    echo "{\"archived_at\":\"$TIMESTAMP\",\"source_file\":\"$src_tag\",\"outcome\":\"$outcome\",\"entry_id\":\"$entry_id_short\",\"pattern_key\":\"$pattern_key\",\"category\":\"$entry_cat\",\"logged_at\":\"$logged_at\",\"resolved_at\":\"$resolved_at\",\"title\":\"$title_text\",\"summary\":\"$summary\",\"details\":\"$details\",\"suggested_action\":\"$suggested_action\",\"tags\":$tag_json,\"recurrence_count\":$recurrence_count}"
}

# ── Extract field value from MD entry ──────────────────────
extract_field() {
    local entry="$1"
    local field="$2"
    local val
    val=$(echo "$entry" | awk -v f="### $field" 'index($0,f)==1{getline; print}')
    [ -z "$val" ] && val=$(echo "$entry" | awk -v f="$field" 'index($0,f)==1{ sub(/.*:[[:space:]]*/,""); print }')
    echo "$val" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//'
}

extract_meta() {
    local entry="$1"
    local key="$2"
    local val
    val=$(echo "$entry" | grep "^[[:space:]]*- $key:" | sed 's/.*:[[:space:]]*//')
    [ -z "$val" ] && val=$(echo "$entry" | grep "^[[:space:]]*\*\*$key" | sed 's/.*\*://')
    echo "$val" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//'
}

# ── Process a single MD file, emit JSONL lines ───────────────
process_file() {
    local file="$1"
    [ ! -f "$file" ] && return

    local src_tag
    src_tag=$(source_tag "$file")

    local in_entry=false
    local entry_id="" entry_cat="" entry_lines="" current_status=""
    local title="" summary="" details="" suggested_action="" tags_str=""

    while IFS= read -r line; do
        case "$line" in
            "## ["*)
                # Emit previous entry if it's resolved/promoted
                if $in_entry && [ -n "$entry_id" ]; then
                    case "$current_status" in
                        resolved|promoted)
                            # Emit via centralized function
                            emit_entry "$entry_lines" "$entry_id" "$entry_cat"
                            ;;
                    esac
                fi
                # Start new entry
                in_entry=true
                entry_id="$line"
                entry_cat=$(echo "$line" | sed -n 's/^## \[[^ ]*] //p' | tr -d '[:space:]')
                [ -z "$entry_cat" ] && entry_cat="uncategorized"
                entry_lines="$line"$'\n'
                current_status=""
                title=""
                ;;
            *)
                if $in_entry; then
                    entry_lines="$entry_lines$line"$'\n'
                    if echo "$line" | grep -qi "^[[:space:]]*\*\*Status"; then
                        current_status=$(echo "$line" | sed 's/\*\*/./g; s/.*://' | sed 's/^[[:space:]]*//; s/[[:space:]].*//' | tr -d '[:space:]' | tr "[:upper:]" "[:lower:]")
                    fi
                fi
                ;;
        esac
    done < "$file"

    # Flush last entry
    if $in_entry && [ -n "$entry_id" ]; then
        case "$current_status" in
            resolved|promoted)
                emit_entry "$entry_lines" "$entry_id" "$entry_cat" "$current_status"
                ;;
        esac
    fi
}

# ── Collect all archive candidates ────────────────────────────
PREVIEW_FILE="/tmp/archive-preview-$(date '+%Y%m%d').txt"
LOG_FILE="/tmp/archive-log-$(date '+%Y%m%d').txt"
> "$PREVIEW_FILE"
> "$LOG_FILE"

total_candidates=0
for file in "$LEARNINGS_DIR/LEARNINGS.md" "$LEARNINGS_DIR/ERRORS.md" "$LEARNINGS_DIR/FEATURE_REQUESTS.md"; do
    [ ! -f "$file" ] && continue
    count=$(grep -c "^## \[" "$file" 2>/dev/null || echo 0)
    resolved_count=$( { grep -ciE "resolved|promoted" "$file" || true; } | tail -1 )
    if [ "$resolved_count" -gt 0 ] 2>/dev/null; then
        echo "Archived $file ($resolved_count / $count entries will be archived)" >> "$LOG_FILE"
        process_file "$file" >> "$PREVIEW_FILE"
        echo "" >> "$LOG_FILE"
        total_candidates=$(( total_candidates + resolved_count ))
    fi
done

# ── Dry-run: show preview and exit ──────────────────────────
if [ "$DRY_RUN" = true ]; then
    echo "=== Archive Dry-Run — $(date '+%Y-%m-%d %H:%M:%S') ==="
else
    echo "=== Archive — $(date '+%Y-%m-%d %H:%M:%S') ==="
fi
echo "Archive dir: $ARCHIVE_DIR"
echo "Target file: $ARCHIVE_DIR/$TODAY_MONTH.jsonl"
echo ""
if [ "$total_candidates" -eq 0 ]; then
    echo "No resolved/promoted entries found. Nothing to archive."
    echo ""
    cat "$LOG_FILE"
    echo ""
    echo "[DRY-RUN complete — no files modified]"
    exit 0
fi

echo "Total entries to archive: $total_candidates"
echo ""
echo "--- PREVIEW (first 20 entries) ---"
head -20 "$LOG_FILE"
if [ "$(wc -l < "$LOG_FILE")" -gt 20 ]; then
    echo "... (truncated, $total_candidates entries total)"
fi
echo ""

if [ "$DRY_RUN" = true ]; then
    echo "[DRY-RUN — no files modified]"
    exit 0
fi

# ── Execute: write JSONL ─────────────────────────────────────
ARCHIVE_FILE="$ARCHIVE_DIR/$TODAY_MONTH.jsonl"
touch "$ARCHIVE_FILE"
grep -E '^\{' "$PREVIEW_FILE" >> "$ARCHIVE_FILE"
echo "Appended to $ARCHIVE_FILE"

# ── Execute: remove archived entries from MD files ───────────
remove_archived_entries() {
    local file="$1"
    [ ! -f "$file" ] && return

    local tmpfile
    tmpfile=$(mktemp)
    local in_entry=false
    local current_status=""
    local entry_lines=""
    local entry_id=""

    while IFS= read -r line; do
        case "$line" in
            "## ["*)
                # Process previous entry
                if $in_entry && [ -n "$entry_id" ]; then
                    case "$current_status" in
                        resolved|promoted)
                            # Skip: do not write resolved/promoted entries
                            ;;
                        *)
                            # Keep: write accumulated lines
                            printf '%s\n' "$entry_lines" >> "$tmpfile"
                            ;;
                    esac
                fi
                in_entry=true
                entry_id="$line"
                entry_lines="$line"$'\n'
                current_status=""
                ;;
            *)
                if $in_entry; then
                    entry_lines="$entry_lines$line"$'\n'
                    if echo "$line" | grep -qi "^[[:space:]]*\*\*Status"; then
                        current_status=$(echo "$line" | sed 's/\*\*/./g; s/.*://' | sed 's/^[[:space:]]*//; s/[[:space:]].*//' | tr -d '[:space:]' | tr "[:upper:]" "[:lower:]")
                    fi
                fi
                ;;
        esac
    done < "$file"

    # Flush last entry
    if $in_entry && [ -n "$entry_id" ]; then
        case "$current_status" in
            resolved|promoted) ;;  # skip
            *) printf '%s\n' "$entry_lines" >> "$tmpfile" ;;
        esac
    fi

    mv "$tmpfile" "$file"
}

for file in "$LEARNINGS_DIR/LEARNINGS.md" "$LEARNINGS_DIR/ERRORS.md" "$LEARNINGS_DIR/FEATURE_REQUESTS.md"; do
    [ ! -f "$file" ] && continue
    if grep -qi "Status.*resolved\\|Status.*promoted" "$file" 2>/dev/null; then
        remove_archived_entries "$file"
        echo "Cleaned: $file"
    fi
done

# ── Clean up orphaned pending notification files (>7 days) ──
PENDING_DIR="$LEARNINGS_DIR/.pending_notifications"
if [ -d "$PENDING_DIR" ]; then
    stale_count=$(find "$PENDING_DIR" -name "*.json" -mtime +7 -print 2>/dev/null | wc -l)
    if [ "$stale_count" -gt 0 ]; then
        find "$PENDING_DIR" -name "*.json" -mtime +7 -delete 2>/dev/null
        echo "Removed $stale_count orphaned pending JSON files (>7 days)."
    fi
fi

echo ""
echo "=== Archive Complete ==="
echo "Archived $total_candidates entries to $ARCHIVE_DIR/$TODAY_MONTH.jsonl"
echo "MD files cleaned."
