#!/usr/bin/env bash
# Raon OS — Startup Companion CLI
# @yeomyeonggeori/raon-os
#
# Usage: raon.sh <module> <command> [options]
#   Modules: biz-plan, gov-funding, investor-match
#
# Environment:
#   RAON_API_URL  — K-Startup AI API base URL (optional)
#   RAON_API_KEY  — API key (optional)
#   Falls back to local LLM + RAG when API is not configured.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"
MODULE="${1:-help}"
COMMAND="${2:-}"
shift 2 2>/dev/null || true

# --- .env 자동 로드 (환경변수 미설정 키만 적용) ---
if [ -f "${HOME}/.openclaw/.env" ]; then
  while IFS='=' read -r _k _v; do
    # 주석·빈줄 건너뜀, 이미 설정된 변수는 덮어쓰지 않음
    [[ -z "${_k}" || "${_k}" == \#* ]] && continue
    _k="${_k// /}"
    if [ -z "${!_k:-}" ]; then
      export "${_k}=${_v}"
    fi
  done < "${HOME}/.openclaw/.env"
fi

# --- Config ---
API_URL="${RAON_API_URL:-}"
API_KEY="${RAON_API_KEY:-}"

# --- Colors ---
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info()  { echo -e "${BLUE}[raon]${NC} $*"; }
ok()    { echo -e "${GREEN}[raon]${NC} $*"; }
warn()  { echo -e "${YELLOW}[raon]${NC} $*"; }
err()   { echo -e "${RED}[raon]${NC} $*" >&2; }

# --- Helpers ---
check_file() {
  local file="$1"
  if [[ ! -f "$file" ]]; then
    err "파일을 찾을 수 없습니다: $file"
    exit 1
  fi
}

extract_text_from_pdf() {
  local file="$1"
  if command -v pdftotext &>/dev/null; then
    pdftotext "$file" -
  elif command -v python3 &>/dev/null; then
    python3 -c "
import sys
try:
    import PyPDF2
    reader = PyPDF2.PdfReader('$file')
    for page in reader.pages:
        print(page.extract_text() or '')
except ImportError:
    try:
        import pdfplumber
        with pdfplumber.open('$file') as pdf:
            for page in pdf.pages:
                print(page.extract_text() or '')
    except ImportError:
        print('ERROR: pdftotext, PyPDF2, or pdfplumber required', file=sys.stderr)
        sys.exit(1)
"
  else
    err "PDF 파싱 도구가 필요합니다: pdftotext, PyPDF2, or pdfplumber"
    exit 1
  fi
}

call_api() {
  local endpoint="$1"
  local data="$2"

  if [[ -n "$API_URL" && -n "$API_KEY" ]]; then
    curl -s -X POST "${API_URL}${endpoint}" \
      -H "Authorization: Bearer ${API_KEY}" \
      -H "Content-Type: application/json" \
      -d "$data"
  else
    echo "__LOCAL_MODE__"
  fi
}

# --- biz-plan module ---
bizplan_evaluate() {
  python3 "$SCRIPT_DIR/evaluate.py" evaluate "$@"
}

bizplan_improve() {
  python3 "$SCRIPT_DIR/evaluate.py" improve "$@"
}

bizplan_interactive() {
  python3 "$SCRIPT_DIR/evaluate.py" interactive "$@"
}

# --- gov-funding module ---
govfunding_match() {
  python3 "$SCRIPT_DIR/evaluate.py" match "$@"
}

govfunding_info() {
  local program=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --program) program="$2"; shift 2 ;;
      *) shift ;;
    esac
  done

  if [[ -z "$program" ]]; then
    err "--program 옵션을 입력하세요."
    exit 1
  fi

  info "$program 정보 조회 중..."

  local ref_file="$BASE_DIR/references/gov-programs.md"
  if [[ -f "$ref_file" ]]; then
    grep -A 20 -i "$program" "$ref_file" || echo "프로그램을 찾을 수 없습니다: $program"
  else
    err "references/gov-programs.md 파일이 필요합니다."
  fi
}

govfunding_draft() {
  local program="" file=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --program) program="$2"; shift 2 ;;
      --file) file="$2"; shift 2 ;;
      *) shift ;;
    esac
  done

  if [[ -z "$program" || -z "$file" ]]; then
    err "--program 과 --file 옵션이 필요합니다."
    exit 1
  fi

  check_file "$file"
  info "$program 지원서 초안 생성 중..."

  python3 "$SCRIPT_DIR/evaluate.py" draft --file "$file" --program "$program"
}

govfunding_checklist() {
  local program="" file=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --program) program="$2"; shift 2 ;;
      --file) file="$2"; shift 2 ;;
      *) shift ;;
    esac
  done

  if [[ -z "$program" || -z "$file" ]]; then
    err "--program 과 --file 옵션이 필요합니다."
    exit 1
  fi

  check_file "$file"
  info "$program 지원 준비 체크리스트 생성 중..."

  python3 "$SCRIPT_DIR/evaluate.py" checklist --file "$file" --program "$program"
}

# --- investor-match module ---
investor_match() {
  local CMD="${1:-profile}"
  
  if [[ "$CMD" == --* ]]; then
    # Direct flags -> implicit profile
    python3 "$SCRIPT_DIR/evaluate.py" investor "$@"
  elif [[ "$CMD" == "profile" ]]; then
    shift
    python3 "$SCRIPT_DIR/evaluate.py" investor "$@"
  else
    warn "Unknown command: investor-match $CMD"
    show_help
  fi
}

# --- Help ---
show_help() {
  cat <<EOF
🌅 Raon OS — Startup Companion
   @yeomyeonggeori/raon-os

Usage: raon.sh <module> <command> [options]

Modules:
  biz-plan       사업계획서 평가 및 개선
    evaluate     --file <pdf> | --text <text> | stdin    TIPS 기준 평가
    improve      --file <pdf> | --text <text> | stdin    개선안 생성
    interactive  --file <pdf> | --text <text>            대화형 평가 세션

  gov-funding    정부 지원사업 매칭
    match        --file <pdf> | --text <text> | stdin    최적 프로그램 매칭
    info         --program <name>                        프로그램 정보 조회
    draft        --program <name> --file <pdf>           지원서 초안
    checklist    --program <name> --file <pdf>           지원 준비 체크리스트

  investor-match 투자자 매칭 (Factsheet AI)
    profile      --file <pdf>                            투자 매력도 분석 및 프로필

  valuation      밸류에이션 산출
    estimate     [--stage seed] [--industry ai] [--revenue N]  밸류에이션 추정
                 [--mrr N] [--tips] [--gov-rnd N] [--json]
                 [--team 1.0] [--market 1.0] [--product 1.0]

  eval-pipeline  LLM 평가 정확도 추적
    add          --file <name> --result pass/fail [--score N]  실제 결과 등록
    run          --file <pdf> [--model name]                   평가 실행+저장
    compare      --file <name>                                 비교
    report                                                     전체 리포트

  idea           YC RFS 기반 창업 아이디어
    list         YC RFS 전체 목록 출력
    detail <N>   카테고리 상세 (1-9)
    suggest      배경/관심사 기반 아이디어 추천

  serve          HTTP API 서버 실행
    [port]       포트 번호 (기본: 8400)
  install        launchd 서비스 등록 (부팅 시 자동 시작)
  uninstall      launchd 서비스 제거
  install-model  로컬 LLM 모델 다운로드 (Ollama, 선택사항)

Options:
  --file <path>  PDF 또는 텍스트 파일
  --text <text>  직접 텍스트 입력
  --model <name> 로컬 Ollama 모델 지정 (기본: qwen3:8b)
  --json         JSON 형식 출력
  (stdin)        파이프 입력: echo "..." | raon.sh biz-plan evaluate

Environment (우선순위 순):
  OPENROUTER_API_KEY   OpenRouter (GPT-4, Claude, Gemini 등)
  GEMINI_API_KEY       Google Gemini + 임베딩
  ANTHROPIC_API_KEY    Claude
  OPENAI_API_KEY       OpenAI + 임베딩

  ✅ 위 키 중 하나만 있으면 Ollama 없이 바로 사용 가능
  ⚙️  키 없을 경우 → 로컬 Ollama 자동 사용 (raon.sh install-model 로 설치)
  가입: https://k-startup.ai
EOF
}

# --- Onboarding (first run) ---
RAON_INIT_FILE="${HOME}/.raon-os-init"
if [ ! -f "$RAON_INIT_FILE" ]; then
  echo ""
  echo -e "${GREEN}🌅 라온 OS에 오신 걸 환영합니다!${NC}"
  echo ""
  echo "  한국 스타트업 파운더를 위한 AI 비서입니다."
  echo "  사업계획서 평가, 정부 지원사업 매칭, 투자자 연결을 도와드려요."
  echo ""
  # 이미 API 키가 있으면 → 바로 사용 가능 메시지
  if [ -n "$OPENROUTER_API_KEY" ] || [ -n "$GEMINI_API_KEY" ] || [ -n "$ANTHROPIC_API_KEY" ] || [ -n "$OPENAI_API_KEY" ]; then
    echo -e "  ${GREEN}✅ API 키 감지됨 — 바로 사용 가능합니다!${NC}"
  else
    echo -e "  ${YELLOW}⚙️  API 키 미설정 — 두 가지 방법 중 선택:${NC}"
    echo ""
    echo -e "  ${BLUE}방법 1 (권장)${NC} — Cloud API 키 설정:"
    echo "    echo 'GEMINI_API_KEY=your-key' >> ~/.openclaw/.env"
    echo "    (키 발급: https://aistudio.google.com/app/apikey)"
    echo ""
    echo -e "  ${BLUE}방법 2${NC} — 로컬 Ollama 사용:"
    echo -e "    ${YELLOW}raon.sh install-model${NC}  (자동 설치)"
  fi
  echo ""
  echo -e "  시작하기: ${BLUE}raon.sh biz-plan evaluate --file 사업계획서.pdf${NC}"
  echo -e "  도움말:   ${BLUE}raon.sh help${NC}"
  echo ""
  touch "$RAON_INIT_FILE"
fi

# --- Router ---
case "$MODULE" in
  biz-plan)
    case "$COMMAND" in
      evaluate)    bizplan_evaluate "$@" ;;
      improve)     bizplan_improve "$@" ;;
      interactive) bizplan_interactive "$@" ;;
      *)           err "Unknown command: biz-plan $COMMAND"; show_help ;;
    esac
    ;;
  gov-funding)
    case "$COMMAND" in
      match)     govfunding_match "$@" ;;
      info)      govfunding_info "$@" ;;
      draft)     govfunding_draft "$@" ;;
      checklist) govfunding_checklist "$@" ;;
      *)         err "Unknown command: gov-funding $COMMAND"; show_help ;;
    esac
    ;;
  investor-match)
    investor_match "$@"
    ;;
  valuation)
    python3 "$SCRIPT_DIR/valuation.py" "${COMMAND:-estimate}" "$@"
    ;;
  eval-pipeline)
    python3 "$SCRIPT_DIR/eval_pipeline.py" "$COMMAND" "$@"
    ;;
  serve)
    PORT="${COMMAND:-8400}"
    info "Starting Raon OS API Server on port $PORT..."
    python3 "$SCRIPT_DIR/server.py" --port "$PORT" "$@"
    ;;
  install)
    # 서버 자동시작(launchd 등록)이 필요하면 scripts/install-service.sh 실행
    # launchctl 관련 코드는 보안상 install-service.sh로 분리되어 있습니다.
    bash "$SCRIPT_DIR/install-service.sh" install
    ;;
  uninstall)
    # launchctl 관련 코드는 install-service.sh로 분리되어 있습니다.
    bash "$SCRIPT_DIR/install-service.sh" uninstall
    ;;
  install-model)
    MODEL="${COMMAND:-qwen3:8b}"
    echo ""
    echo -e "${BLUE}🤖 로컬 LLM 모델 설치: $MODEL${NC}"
    echo "   (Cloud API 키가 있으면 이 단계는 불필요합니다)"
    echo ""
    # Ollama 설치 확인
    if ! command -v ollama &>/dev/null; then
      echo -e "${YELLOW}Ollama 미설치 — 자동 설치 시도...${NC}"
      if command -v brew &>/dev/null; then
        brew install ollama && echo -e "${GREEN}✅ Ollama 설치 완료${NC}"
      else
        echo -e "${YELLOW}Homebrew 미설치. 아래 명령어로 수동 설치하세요:${NC}"
        echo "  curl -fsSL https://ollama.ai/install.sh | sh"
        exit 1
      fi
    else
      echo -e "${GREEN}✅ Ollama 감지됨: $(ollama --version 2>/dev/null)${NC}"
    fi
    echo ""
    echo -e "${BLUE}📥 모델 다운로드 중: $MODEL${NC}"
    echo "   (qwen3:8b 기준 약 4.7GB, 인터넷 속도에 따라 수 분 소요)"
    echo ""
    if ollama pull "$MODEL"; then
      echo ""
      echo -e "${GREEN}🎉 설치 완료! 이제 라온 OS를 사용할 수 있습니다.${NC}"
      echo -e "   시작: ${BLUE}raon.sh biz-plan evaluate --file 사업계획서.pdf${NC}"
    else
      echo -e "${YELLOW}⚠️  모델 다운로드 실패. 직접 실행: ollama pull $MODEL${NC}"
      exit 1
    fi
    ;;
  profile)
    python3 "$SCRIPT_DIR/gamification.py" profile "$@"
    ;;
  history)
    LOG_FILE="$BASE_DIR/history.jsonl"
    if [ -f "$LOG_FILE" ]; then
      echo -e "${BLUE}=== Raon OS History ===${NC}"
      # simple parse with grep/sed if jq missing, but assuming jq is likely or just cat
      tail -n 10 "$LOG_FILE"
    else
      echo "No history yet."
    fi
    ;;
  idea)
    python3 "$SCRIPT_DIR/idea.py" "${COMMAND:-list}" "$@"
    ;;
  help|--help|-h|"")
    show_help
    ;;
  *)
    err "Unknown module: $MODULE"
    show_help
    exit 1
    ;;
esac
