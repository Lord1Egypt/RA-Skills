#!/bin/bash
# list-sessions.sh - Claude CodeとCodexのセッション一覧を取得
#
# Usage: ./list-sessions.sh [OPTIONS]
#   -p, --project <path>   特定のプロジェクトのセッションのみ表示
#   -n, --limit <num>      表示するセッション数（デフォルト: 10）
#   -a, --all              全エージェントのセッションを表示（デフォルト: Claude Codeのみ）
#   -j, --json             JSON形式で出力
#
# 出力例:
#   2026-01-17 09:30:00 | claude | /Users/xxx/project | 7fdbec67-xxx.jsonl
#   2026-01-16 15:00:00 | codex  | /Users/xxx/project | rollout-xxx.jsonl

set -euo pipefail

LIMIT=10
PROJECT=""
ALL_AGENTS=false
JSON_OUTPUT=false

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
        -a|--all)
            ALL_AGENTS=true
            shift
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

CLAUDE_DIR="$HOME/.claude/projects"
CODEX_DIR="$HOME/.codex/sessions"

# Claude Codeセッションを取得
get_claude_sessions() {
    if [[ ! -d "$CLAUDE_DIR" ]]; then
        return
    fi

    find "$CLAUDE_DIR" -maxdepth 2 -name "*.jsonl" -type f 2>/dev/null | while read -r file; do
        # サブエージェントファイルを除外
        if [[ "$file" == *"/subagents/"* ]]; then
            continue
        fi

        local filename
        filename=$(basename "$file")
        local dir
        dir=$(dirname "$file")
        local project_encoded
        project_encoded=$(basename "$dir")

        # プロジェクトパスをデコード（-- は /. に、- は / に変換）
        local project_path
        project_path="${project_encoded//--//.}"
        project_path="${project_path//-//}"

        # プロジェクトフィルタリング
        if [[ -n "$PROJECT" ]] && [[ "$project_path" != *"$PROJECT"* ]]; then
            continue
        fi

        # タイムスタンプを取得（最初のuserメッセージから）
        local timestamp
        timestamp=$(head -10 "$file" 2>/dev/null | grep '"type":"user"' | head -1 | jq -r '.timestamp // empty' 2>/dev/null || echo "")

        if [[ -z "$timestamp" ]]; then
            timestamp=$(stat -f "%Sm" -t "%Y-%m-%dT%H:%M:%S" "$file" 2>/dev/null || stat -c "%y" "$file" 2>/dev/null | cut -d. -f1)
        fi

        echo "${timestamp}|claude|${project_path}|${filename}|${file}"
    done
}

# Codexセッションを取得
get_codex_sessions() {
    if [[ ! -d "$CODEX_DIR" ]] || [[ "$ALL_AGENTS" != "true" ]]; then
        return
    fi

    find "$CODEX_DIR" -name "rollout-*.jsonl" -type f 2>/dev/null | while read -r file; do
        local filename
        filename=$(basename "$file")

        # session_metaからcwdを取得
        local cwd
        cwd=$(head -1 "$file" 2>/dev/null | jq -r '.payload.cwd // empty' 2>/dev/null || echo "unknown")

        local timestamp
        timestamp=$(head -1 "$file" 2>/dev/null | jq -r '.payload.timestamp // .timestamp // empty' 2>/dev/null || echo "")

        if [[ -n "$PROJECT" ]] && [[ "$cwd" != *"$PROJECT"* ]]; then
            continue
        fi

        echo "${timestamp}|codex|${cwd}|${filename}|${file}"
    done
}

# 結果を収集してソート
results=$( (get_claude_sessions; get_codex_sessions) | sort -r | head -n "$LIMIT")

if [[ "$JSON_OUTPUT" == "true" ]]; then
    echo "["
    first=true
    while IFS='|' read -r timestamp agent project filename filepath; do
        if [[ -z "$timestamp" ]]; then continue; fi
        if [[ "$first" == "true" ]]; then
            first=false
        else
            echo ","
        fi
        echo "  {"
        echo "    \"timestamp\": \"$timestamp\","
        echo "    \"agent\": \"$agent\","
        echo "    \"project\": \"$project\","
        echo "    \"filename\": \"$filename\","
        echo "    \"filepath\": \"$filepath\""
        echo -n "  }"
    done <<< "$results"
    echo ""
    echo "]"
else
    printf "%-20s | %-6s | %-40s | %s\n" "TIMESTAMP" "AGENT" "PROJECT" "FILENAME"
    echo "-------------------------------------------------------------------------------------"
    while IFS='|' read -r timestamp agent project filename filepath; do
        if [[ -z "$timestamp" ]]; then continue; fi
        # タイムスタンプを短縮形式に変換
        short_ts=$(echo "$timestamp" | sed 's/T/ /' | cut -c1-19)
        # プロジェクトパスを短縮
        short_project="${project/$HOME/~}"
        if [[ ${#short_project} -gt 40 ]]; then
            short_project="...${short_project: -37}"
        fi
        printf "%-20s | %-6s | %-40s | %s\n" "$short_ts" "$agent" "$short_project" "$filename"
    done <<< "$results"
fi
