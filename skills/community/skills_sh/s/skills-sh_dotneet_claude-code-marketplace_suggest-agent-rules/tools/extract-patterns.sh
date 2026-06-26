#!/bin/bash
# extract-patterns.sh - 複数セッションからルール提案に有用なパターンを抽出
#
# Usage: ./extract-patterns.sh [OPTIONS]
#   -p, --project <path>   特定プロジェクトのセッションを分析
#   -n, --limit <num>      分析するセッション数（デフォルト: 5）
#   -j, --json             JSON形式で出力
#
# 出力内容:
#   - 繰り返し発生したエラーパターン
#   - よく使用されるツールとファイル
#   - ユーザーの明示的な好み・指示
#   - 手戻りパターン（エラー→修正の繰り返し）

set -euo pipefail

LIMIT=5
PROJECT=""
JSON_OUTPUT=false
CLAUDE_DIR="$HOME/.claude/projects"

while [[ $# -gt 0 ]]; do
    case $1 in
        -p|--project)
            PROJECT="$2"
            shift 2
            ;;
        -n|--limit)
            LIMIT="$2"
            shift 2
            ;;
        -j|--json)
            JSON_OUTPUT=true
            shift
            ;;
        *)
            echo "Unknown option: $1" >&2
            exit 1
            ;;
    esac
done

# セッションファイルを収集
collect_sessions() {
    local search_dir="$CLAUDE_DIR"

    if [[ -n "$PROJECT" ]]; then
        local encoded_project="${PROJECT//\//-}"
        search_dir="$CLAUDE_DIR/*${encoded_project}*"
    fi

    # shellcheck disable=SC2086 # Intentional glob expansion for search_dir
    find $search_dir -maxdepth 2 -name "*.jsonl" -type f 2>/dev/null | \
        grep -v '/subagents/' | \
        head -n "$LIMIT"
}

SESSIONS=$(collect_sessions)

if [[ -z "$SESSIONS" ]]; then
    echo "No sessions found" >&2
    exit 1
fi

# 一時ファイル
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT

# 全セッションからツール使用を集計
echo "Analyzing $(echo "$SESSIONS" | wc -l | tr -d ' ') sessions..."

TOOL_COUNTS="$TMP_DIR/tool_counts.txt"
FILE_READS="$TMP_DIR/file_reads.txt"
FILE_EDITS="$TMP_DIR/file_edits.txt"
USER_PREFS="$TMP_DIR/user_prefs.txt"
ERRORS="$TMP_DIR/errors.txt"

touch "$TOOL_COUNTS" "$FILE_READS" "$FILE_EDITS" "$USER_PREFS" "$ERRORS"

for session in $SESSIONS; do
    # ツール使用を集計
    grep -o '"name":"[^"]*"' "$session" 2>/dev/null | \
        sed 's/"name":"//g; s/"//g' >> "$TOOL_COUNTS" || true

    # 読み取りファイル
    grep '"name":"Read"' "$session" 2>/dev/null | \
        grep -o '"file_path":"[^"]*"' | \
        sed 's/"file_path":"//g; s/"//g' >> "$FILE_READS" || true

    # 編集ファイル
    grep -E '"name":"(Edit|Write)"' "$session" 2>/dev/null | \
        grep -o '"file_path":"[^"]*"' | \
        sed 's/"file_path":"//g; s/"//g' >> "$FILE_EDITS" || true

    # ユーザーの好み（特定キーワードを含む）
    grep '"type":"user"' "$session" 2>/dev/null | while read -r line; do
        content=$(echo "$line" | jq -r '.message.content // ""' 2>/dev/null)
        if echo "$content" | grep -q -i -E '(必ず|常に|always|never|しない|prefer|好み|rule|ルール|規約|convention|don.t|do not)'; then
            echo "$content" | head -2
        fi
    done >> "$USER_PREFS" || true

    # エラー
    grep -i '"type":"tool_result"' "$session" 2>/dev/null | \
        grep -i -E '(error|failed|exception|denied)' | \
        jq -r '.content // ""' 2>/dev/null | \
        head -3 >> "$ERRORS" || true
done

# 結果を出力
if [[ "$JSON_OUTPUT" == "true" ]]; then
    cat << EOF
{
  "sessions_analyzed": $(echo "$SESSIONS" | wc -l | tr -d ' '),
  "top_tools": [
$(sort "$TOOL_COUNTS" | uniq -c | sort -rn | head -10 | awk '{printf "    {\"count\": %d, \"tool\": \"%s\"},\n", $1, $2}' | sed '$ s/,$//')
  ],
  "frequently_read_files": [
$(sort "$FILE_READS" | uniq -c | sort -rn | head -10 | awk '{printf "    {\"count\": %d, \"file\": \"%s\"},\n", $1, $2}' | sed '$ s/,$//')
  ],
  "frequently_edited_files": [
$(sort "$FILE_EDITS" | uniq -c | sort -rn | head -10 | awk '{printf "    {\"count\": %d, \"file\": \"%s\"},\n", $1, $2}' | sed '$ s/,$//')
  ],
  "user_preferences_sample": [
$(head -10 "$USER_PREFS" | while read -r line; do printf '    "%s",\n' "$(echo "$line" | sed 's/"/\\"/g' | head -c 200)"; done | sed '$ s/,$//')
  ],
  "common_errors_sample": [
$(head -5 "$ERRORS" | while read -r line; do printf '    "%s",\n' "$(echo "$line" | sed 's/"/\\"/g' | head -c 200)"; done | sed '$ s/,$//')
  ]
}
EOF
else
    echo ""
    echo "=== Analysis Results ($(echo "$SESSIONS" | wc -l | tr -d ' ') sessions) ==="

    echo ""
    echo "--- Top 10 Tools Used ---"
    sort "$TOOL_COUNTS" | uniq -c | sort -rn | head -10

    echo ""
    echo "--- Frequently Read Files ---"
    sort "$FILE_READS" | uniq -c | sort -rn | head -10

    echo ""
    echo "--- Frequently Edited Files ---"
    sort "$FILE_EDITS" | uniq -c | sort -rn | head -10

    echo ""
    echo "--- User Preferences Found ---"
    head -10 "$USER_PREFS" | while read -r line; do
        if [[ -n "$line" ]]; then
            echo "  • $(echo "$line" | head -c 100)"
        fi
    done

    echo ""
    echo "--- Common Errors ---"
    head -5 "$ERRORS" | while read -r line; do
        if [[ -n "$line" ]]; then
            echo "  • $(echo "$line" | head -c 150)"
        fi
    done
fi
