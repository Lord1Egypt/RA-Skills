#!/bin/bash
# analyze-session.sh - セッションファイルを解析してルール提案に有用な情報を抽出
#
# Usage: ./analyze-session.sh <session-file> [OPTIONS]
#   -s, --summary          概要のみ表示（デフォルト）
#   -u, --user-messages    ユーザーメッセージを抽出
#   -t, --tools            ツール使用状況を分析
#   -e, --errors           エラーと修正パターンを抽出
#   -p, --preferences      ユーザーの好み・指示パターンを抽出
#   -j, --json             JSON形式で出力
#   -a, --all              全ての分析を実行
#
# Examples:
#   ./analyze-session.sh ~/.claude/projects/-Users-xxx/session.jsonl --summary
#   ./analyze-session.sh ~/.claude/projects/-Users-xxx/session.jsonl --all --json

set -euo pipefail

if [[ $# -lt 1 ]]; then
    echo "Usage: $0 <session-file> [OPTIONS]" >&2
    exit 1
fi

SESSION_FILE="$1"
shift

if [[ ! -f "$SESSION_FILE" ]]; then
    echo "Error: Session file not found: $SESSION_FILE" >&2
    exit 1
fi

# オプション解析
MODE="summary"
JSON_OUTPUT=false
ALL_MODE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -s|--summary) MODE="summary"; shift ;;
        -u|--user-messages) MODE="user"; shift ;;
        -t|--tools) MODE="tools"; shift ;;
        -e|--errors) MODE="errors"; shift ;;
        -p|--preferences) MODE="preferences"; shift ;;
        -j|--json) JSON_OUTPUT=true; shift ;;
        -a|--all) ALL_MODE=true; shift ;;
        *) echo "Unknown option: $1" >&2; exit 1 ;;
    esac
done

# ファイルタイプを検出
detect_file_type() {
    # ファイル内にuserまたはassistantタイプのメッセージがあるか確認
    if grep -q -m 1 -E '"type":"(user|assistant)"' "$SESSION_FILE" 2>/dev/null; then
        echo "claude"
    elif head -1 "$SESSION_FILE" | jq -e '.type == "session_meta"' > /dev/null 2>&1; then
        echo "codex"
    else
        echo "unknown"
    fi
}

FILE_TYPE=$(detect_file_type)

# Claude Codeセッションの解析
analyze_claude_summary() {
    local total_lines
    total_lines=$(wc -l < "$SESSION_FILE" | tr -d ' ')

    local user_count
    user_count=$(grep -c '"type":"user"' "$SESSION_FILE" 2>/dev/null || echo "0")

    local assistant_count
    assistant_count=$(grep -c '"type":"assistant"' "$SESSION_FILE" 2>/dev/null || echo "0")

    local tool_uses
    tool_uses=$(grep -o '"type":"tool_use"' "$SESSION_FILE" 2>/dev/null | wc -l | tr -d ' ')

    # 最初と最後のタイムスタンプ
    local first_ts
    first_ts=$(head -10 "$SESSION_FILE" | grep '"timestamp"' | head -1 | jq -r '.timestamp // empty' 2>/dev/null || echo "N/A")

    local last_ts
    last_ts=$(tail -10 "$SESSION_FILE" | grep '"timestamp"' | tail -1 | jq -r '.timestamp // empty' 2>/dev/null || echo "N/A")

    # プロジェクト情報
    local cwd
    cwd=$(head -10 "$SESSION_FILE" | grep '"cwd"' | head -1 | jq -r '.cwd // empty' 2>/dev/null || echo "N/A")

    local branch
    branch=$(head -10 "$SESSION_FILE" | grep '"gitBranch"' | head -1 | jq -r '.gitBranch // empty' 2>/dev/null || echo "N/A")

    if [[ "$JSON_OUTPUT" == "true" ]]; then
        cat << EOF
{
  "file_type": "claude",
  "total_records": $total_lines,
  "user_messages": $user_count,
  "assistant_messages": $assistant_count,
  "tool_uses": $tool_uses,
  "first_timestamp": "$first_ts",
  "last_timestamp": "$last_ts",
  "project": "$cwd",
  "branch": "$branch"
}
EOF
    else
        echo "=== Session Summary (Claude Code) ==="
        echo "File: $SESSION_FILE"
        echo "Project: $cwd"
        echo "Branch: $branch"
        echo "Start: $first_ts"
        echo "End: $last_ts"
        echo ""
        echo "Records: $total_lines"
        echo "User messages: $user_count"
        echo "Assistant messages: $assistant_count"
        echo "Tool uses: $tool_uses"
    fi
}

# ユーザーメッセージを抽出
extract_user_messages() {
    echo "=== User Messages ==="
    grep '"type":"user"' "$SESSION_FILE" | while read -r line; do
        local ts
        ts=$(echo "$line" | jq -r '.timestamp // "N/A"' 2>/dev/null)
        local content
        content=$(echo "$line" | jq -r '.message.content // ""' 2>/dev/null)

        # contentが文字列の場合
        if [[ -n "$content" ]] && [[ "$content" != "null" ]]; then
            echo ""
            echo "[$ts]"
            echo "$content" | head -5
            if [[ $(echo "$content" | wc -l) -gt 5 ]]; then
                echo "... (truncated)"
            fi
        fi
    done
}

# ツール使用状況を分析
analyze_tools() {
    echo "=== Tool Usage Analysis ==="

    # ツール名ごとの使用回数
    echo ""
    echo "Tool usage count:"
    grep -o '"name":"[^"]*"' "$SESSION_FILE" 2>/dev/null | \
        grep -v '"name":"message"' | \
        sed 's/"name":"//g; s/"//g' | \
        sort | uniq -c | sort -rn | head -20

    # 最も読まれたファイル
    echo ""
    echo "Most accessed files (Read tool):"
    grep '"name":"Read"' "$SESSION_FILE" 2>/dev/null | \
        jq -r '.input.file_path // empty' 2>/dev/null | \
        sort | uniq -c | sort -rn | head -10

    # 最も編集されたファイル
    echo ""
    echo "Most edited files (Edit/Write tool):"
    grep -E '"name":"(Edit|Write)"' "$SESSION_FILE" 2>/dev/null | \
        jq -r '.input.file_path // empty' 2>/dev/null | \
        sort | uniq -c | sort -rn | head -10
}

# エラーパターンを抽出
extract_errors() {
    echo "=== Error Patterns ==="

    # tool_resultでエラーを含むもの
    echo ""
    echo "Tool errors found:"
    grep -i '"type":"tool_result"' "$SESSION_FILE" 2>/dev/null | \
        grep -i -E '(error|failed|exception|denied|not found|permission)' | \
        jq -r '.content // .text // ""' 2>/dev/null | head -20
}

# ユーザーの好みパターンを抽出
extract_preferences() {
    echo "=== User Preferences & Instructions ==="

    # 特定のキーワードを含むユーザーメッセージ
    echo ""
    echo "Explicit preferences/instructions found:"
    grep '"type":"user"' "$SESSION_FILE" | while read -r line; do
        local content
        content=$(echo "$line" | jq -r '.message.content // ""' 2>/dev/null | tr '[:upper:]' '[:lower:]')

        # 好みや指示を示すパターンをチェック
        if echo "$content" | grep -q -E '(必ず|常に|always|never|しない|prefer|好み|rule|ルール|規約|convention|don.t|do not|やめて|止めて)'; then
            local ts
            ts=$(echo "$line" | jq -r '.timestamp // "N/A"' 2>/dev/null)
            local orig_content
            orig_content=$(echo "$line" | jq -r '.message.content // ""' 2>/dev/null)
            echo ""
            echo "[$ts]"
            echo "$orig_content" | head -3
        fi
    done | head -50
}

# 実行
if [[ "$FILE_TYPE" == "claude" ]]; then
    if [[ "$ALL_MODE" == "true" ]]; then
        analyze_claude_summary
        echo ""
        extract_user_messages
        echo ""
        analyze_tools
        echo ""
        extract_errors
        echo ""
        extract_preferences
    else
        case "$MODE" in
            summary) analyze_claude_summary ;;
            user) extract_user_messages ;;
            tools) analyze_tools ;;
            errors) extract_errors ;;
            preferences) extract_preferences ;;
        esac
    fi
elif [[ "$FILE_TYPE" == "codex" ]]; then
    echo "Codex session analysis - Summary only"
    meta=$(head -1 "$SESSION_FILE")
    echo "$meta" | jq '{
        id: .payload.id,
        cwd: .payload.cwd,
        cli_version: .payload.cli_version,
        branch: .payload.git.branch
    }' 2>/dev/null || echo "Failed to parse Codex session"
else
    echo "Unknown session file format" >&2
    exit 1
fi
