#!/usr/bin/env bash
# GeekNews OSS Brief — 매일 08:00 KST 실행용 cron 스크립트
#
# crontab 등록 예시 (UTC 서버):
#   0 23 * * * /path/to/geeknews-oss-brief/scripts/run_geeknews_brief.sh >> /var/log/geeknews-brief.log 2>&1
#
# crontab 등록 예시 (KST 서버):
#   0 8 * * * /path/to/geeknews-oss-brief/scripts/run_geeknews_brief.sh >> /var/log/geeknews-brief.log 2>&1

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
OUTPUT_FILE="/tmp/geeknews_brief_$(date +%Y%m%d).md"
LOG_PREFIX="[$(date '+%Y-%m-%d %H:%M:%S')]"

echo "${LOG_PREFIX} === GeekNews OSS Brief 시작 ==="

# 1. 환경변수 체크
if [[ -z "${TELEGRAM_BOT_TOKEN:-}" ]] || [[ -z "${TELEGRAM_CHAT_ID:-}" ]]; then
    echo "${LOG_PREFIX} ❌ TELEGRAM_BOT_TOKEN 또는 TELEGRAM_CHAT_ID가 설정되지 않음"
    exit 1
fi

# 2. GeekNews 수집 + 큐레이션 + 메시지 생성
#    이 부분은 실제 구현에 맞게 교체한다.
#    옵션 A: Claude API 호출 (권장)
#    옵션 B: Python 스크립트로 직접 구현
#
#    아래는 Claude API를 curl로 호출하는 예시:

if [[ -n "${ANTHROPIC_API_KEY:-}" ]]; then
    echo "${LOG_PREFIX} Claude API로 큐레이션 실행..."
    
    PROMPT="오늘 GeekNews(https://news.hada.io)의 메인페이지를 확인하고, geeknews-oss-brief 스킬의 선정 기준에 따라 HOT 이슈 5개를 선정해서 텔레그램 메시지 포맷으로 작성해줘. 오픈소스와 GitHub star 급상승 프로젝트를 우선순위 높게."
    
    RESPONSE=$(curl -s https://api.anthropic.com/v1/messages \
        -H "content-type: application/json" \
        -H "x-api-key: ${ANTHROPIC_API_KEY}" \
        -H "anthropic-version: 2023-06-01" \
        -d "{
            \"model\": \"claude-sonnet-4-20250514\",
            \"max_tokens\": 2000,
            \"tools\": [{\"type\": \"web_search_20250305\", \"name\": \"web_search\"}],
            \"messages\": [{\"role\": \"user\", \"content\": \"${PROMPT}\"}]
        }")
    
    # 응답에서 텍스트 추출
    echo "$RESPONSE" | python3 -c "
import sys, json
data = json.load(sys.stdin)
texts = [b['text'] for b in data.get('content', []) if b.get('type') == 'text']
print('\n'.join(texts))
" > "$OUTPUT_FILE"
    
else
    echo "${LOG_PREFIX} ⚠️  ANTHROPIC_API_KEY 없음 — 수동 실행 필요"
    echo "ANTHROPIC_API_KEY를 설정하거나, 직접 큐레이션 스크립트를 구현하세요." > "$OUTPUT_FILE"
    exit 1
fi

# 3. 텔레그램 전송
echo "${LOG_PREFIX} 텔레그램 전송 중..."
python3 "${SCRIPT_DIR}/send_telegram.py" --message-file "$OUTPUT_FILE"

# 4. 정리
echo "${LOG_PREFIX} === 완료 ==="
echo "${LOG_PREFIX} 메시지 파일: ${OUTPUT_FILE}"
