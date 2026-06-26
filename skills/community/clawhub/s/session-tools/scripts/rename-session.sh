#!/bin/bash
# Session Renamer - Claude Code 세션에 커스텀 타이틀 부여
#
# 사용법:
#   rename-session.sh <session_id> "<title>"          # 특정 세션에 이름 부여
#   rename-session.sh "<title>"                        # 현재 프로젝트의 최신 세션에 이름 부여
#   rename-session.sh --show <session_id>              # 현재 타이틀 확인
#   rename-session.sh --list                           # 현재 프로젝트의 이름 붙은 세션 목록
#
# 메커니즘:
#   Claude Code는 세션 JSONL에 {"type":"custom-title","customTitle":"...","sessionId":"..."} 레코드를
#   추가하여 커스텀 타이틀을 저장함.

set -e

CLAUDE_DIR="$HOME/.claude"
PROJECTS_DIR="$CLAUDE_DIR/projects"

# 현재 프로젝트 디렉토리 계산
CURRENT_DIR="$(pwd)"
PROJECT_FOLDER=$(echo "$CURRENT_DIR" | sed 's|/|-|g; s|\.|-|g')
SESSION_DIR="$PROJECTS_DIR/$PROJECT_FOLDER"

# ── 헬퍼 함수 ────────────────────────────────────────────

find_session_file() {
    local session_id="$1"
    local file="$SESSION_DIR/${session_id}.jsonl"
    if [ ! -f "$file" ]; then
        # 전체 프로젝트에서 검색
        file=$(find "$PROJECTS_DIR" -name "${session_id}.jsonl" 2>/dev/null | head -1)
    fi
    echo "$file"
}

get_current_title() {
    local session_file="$1"
    # JSONL에서 마지막 custom-title 레코드의 customTitle 값 추출
    grep '"type":"custom-title"' "$session_file" 2>/dev/null | tail -1 | \
        sed 's/.*"customTitle":"\([^"]*\)".*/\1/' || echo ""
}

set_title() {
    local session_file="$1"
    local session_id="$2"
    local title="$3"

    local current
    current=$(get_current_title "$session_file")
    if [ -n "$current" ]; then
        echo "현재 타이틀: $current"
        echo "새 타이틀:   $title"
    fi

    # custom-title 레코드 추가 (Claude Code 형식)
    printf '{"type":"custom-title","customTitle":"%s","sessionId":"%s"}\n' \
        "$(echo "$title" | sed 's/"/\\"/g')" \
        "$session_id" >> "$session_file"

    echo "타이틀 설정 완료: $title"
    echo "세션: $session_id"
}

show_title() {
    local session_id="$1"
    local session_file
    session_file=$(find_session_file "$session_id")

    if [ -z "$session_file" ] || [ ! -f "$session_file" ]; then
        echo "세션 파일을 찾을 수 없습니다: $session_id"
        exit 1
    fi

    local title
    title=$(get_current_title "$session_file")
    if [ -n "$title" ]; then
        echo "타이틀: $title"
    else
        echo "(타이틀 없음)"
    fi
}

list_sessions() {
    if [ ! -d "$SESSION_DIR" ]; then
        echo "프로젝트 세션 디렉토리를 찾을 수 없습니다: $SESSION_DIR"
        exit 1
    fi

    echo "=== 이름 붙은 세션 목록 ==="
    local found=0
    for f in "$SESSION_DIR"/*.jsonl; do
        [ -f "$f" ] || continue
        local title
        title=$(get_current_title "$f")
        if [ -n "$title" ]; then
            local id
            id=$(basename "$f" .jsonl)
            printf "%-36s  %s\n" "$id" "$title"
            found=$((found + 1))
        fi
    done

    if [ $found -eq 0 ]; then
        echo "(이름 붙은 세션 없음)"
    fi
}

# ── main ────────────────────────────────────────────────

case "$1" in
    --show)
        show_title "$2"
        ;;
    --list)
        list_sessions
        ;;
    *)
        # 인자 수에 따라 처리
        if [ $# -eq 2 ]; then
            # rename-session.sh <session_id> "<title>"
            SESSION_ID="$1"
            TITLE="$2"
            SESSION_FILE=$(find_session_file "$SESSION_ID")
            if [ -z "$SESSION_FILE" ] || [ ! -f "$SESSION_FILE" ]; then
                echo "세션 파일을 찾을 수 없습니다: $SESSION_ID"
                exit 1
            fi
            set_title "$SESSION_FILE" "$SESSION_ID" "$TITLE"

        elif [ $# -eq 1 ]; then
            # rename-session.sh "<title>" — 현재 프로젝트 최신 세션
            TITLE="$1"
            if [ ! -d "$SESSION_DIR" ]; then
                echo "프로젝트 세션 디렉토리를 찾을 수 없습니다: $SESSION_DIR"
                exit 1
            fi
            LATEST=$(ls -t "$SESSION_DIR"/*.jsonl 2>/dev/null | head -1)
            if [ -z "$LATEST" ]; then
                echo "세션 파일을 찾을 수 없습니다."
                exit 1
            fi
            SESSION_ID=$(basename "$LATEST" .jsonl)
            echo "최신 세션 선택: $SESSION_ID"
            set_title "$LATEST" "$SESSION_ID" "$TITLE"

        else
            echo "사용법:"
            echo "  $(basename "$0") <session_id> \"<title>\"    # 특정 세션에 이름 부여"
            echo "  $(basename "$0") \"<title>\"                  # 현재 프로젝트 최신 세션에 이름 부여"
            echo "  $(basename "$0") --show <session_id>         # 현재 타이틀 확인"
            echo "  $(basename "$0") --list                       # 이름 붙은 세션 목록"
            exit 1
        fi
        ;;
esac
