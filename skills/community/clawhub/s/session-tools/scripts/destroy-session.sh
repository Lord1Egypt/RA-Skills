#!/bin/bash
# Session Destroyer - 현재 Claude Code 세션 삭제 스크립트

set -e

CLAUDE_DIR="$HOME/.claude"
BAK_DIR="$CLAUDE_DIR/.bak"
PROJECTS_DIR="$CLAUDE_DIR/projects"

# 백업 폴더 생성
mkdir -p "$BAK_DIR"

# 현재 작업 디렉토리에서 프로젝트 폴더명 추출
# Claude Code는 /를 -로, .을 -로 변환
CURRENT_DIR="$(pwd)"
PROJECT_FOLDER=$(echo "$CURRENT_DIR" | sed 's|/|-|g; s|\.|-|g')

# 프로젝트 세션 디렉토리 찾기
SESSION_DIR="$PROJECTS_DIR/$PROJECT_FOLDER"

if [ ! -d "$SESSION_DIR" ]; then
    echo "세션 디렉토리를 찾을 수 없습니다: $SESSION_DIR"
    exit 1
fi

# 가장 최근 수정된 세션 파일 찾기
LATEST_SESSION=$(ls -t "$SESSION_DIR"/*.jsonl 2>/dev/null | head -1)

if [ -z "$LATEST_SESSION" ]; then
    echo "세션 파일을 찾을 수 없습니다."
    exit 1
fi

SESSION_ID=$(basename "$LATEST_SESSION" .jsonl)
BAK_FILENAME="${PROJECT_FOLDER}_${SESSION_ID}.jsonl"

echo "세션 삭제 중..."
echo "  원본: $LATEST_SESSION"
echo "  백업: $BAK_DIR/$BAK_FILENAME"

# 세션 파일을 백업 폴더로 이동
mv "$LATEST_SESSION" "$BAK_DIR/$BAK_FILENAME"

echo "세션이 백업 폴더로 이동되었습니다."

# VSCode/Cursor 환경 감지 및 Extension Host 재시작
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
if [ -n "$VSCODE_IPC_HOOK" ] || [ -n "$VSCODE_IPC_HOOK_CLI" ] || [ "$TERM_PROGRAM" = "vscode" ]; then
    echo "VSCode/Cursor 환경 감지됨. Extension Host를 재시작합니다..."
    bash "$SCRIPT_DIR/restart-extension-host.sh"
fi

echo "완료!"
