#!/usr/bin/env bash
# ============================================================
# register-cron.sh — Self-Evolving Agent 크론 등록 v2.0
#
# 변경 이력:
#   v2.0 (2026-02-17) — 개선
#     - config.yaml에서 스케줄/채널/모델 읽기
#     - set -euo pipefail 제거 (크론 에러 노출 방지)
#     - Python 서브프로세스 실패 시 명확한 에러 메시지
#     - 기존 크론 업데이트 옵션 추가 (--update 플래그)
#   v1.0 (2026-02-16) — 초기 버전
#
# 사용법:
#   bash register-cron.sh           # 최초 등록
#   bash register-cron.sh --update  # 기존 크론 설정 업데이트
#   bash register-cron.sh --remove  # 크론 제거
# ============================================================

# SECURITY MANIFEST:
# Environment variables accessed: SEA_CONFIG, SEA_CRON_SCHEDULE, SEA_MODEL,
#   SEA_DISCORD_CHANNEL (required), SEA_CRON_AGENT_ID, CRON_FILE
# External endpoints called: None
# Local files read:
#   ~/.openclaw/cron/jobs.json  (OpenClaw cron registry)
#   <SKILL_DIR>/scripts/lib/config-loader.sh (sourced)
#   <SEA_CONFIG> / ~/openclaw/skills/self-evolving-agent/config.yaml (via config-loader)
# Local files written:
#   ~/.openclaw/cron/jobs.json              (cron job added/updated/removed)
#   ~/.openclaw/cron/jobs.json.bak.self-evolving  (backup before modification)
# Network: None

# !! set -euo pipefail 사용 금지 (크론 에러 노출 방지) !!

# ── 설정 로드 ────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

if [ -f "$SCRIPT_DIR/lib/config-loader.sh" ]; then
  source "$SCRIPT_DIR/lib/config-loader.sh"
  sea_load_config 2>/dev/null || true
fi

CRON_FILE="${CRON_FILE:-$HOME/.openclaw/cron/jobs.json}"
CRON_BACKUP="${CRON_FILE}.bak.self-evolving"
CRON_NAME="🧠 Self-Evolving Agent 주간 분석"

# config에서 읽기 (없으면 기본값)
CRON_SCHEDULE="${SEA_CRON_SCHEDULE:-0 22 * * 0}"
CRON_MODEL="${SEA_MODEL:-anthropic/claude-sonnet-4-5}"
CRON_DISCORD="${SEA_DISCORD_CHANNEL:?ERROR: Set SEA_DISCORD_CHANNEL in config.yaml}"
CRON_AGENT="${SEA_CRON_AGENT_ID:-opus}"

# ── 플래그 파싱 ─────────────────────────────────────────────
MODE="register"
for arg in "$@"; do
  case "$arg" in
    --update) MODE="update" ;;
    --remove) MODE="remove" ;;
    --help|-h)
      echo "사용법: $0 [--update | --remove | --help]"
      echo "  (기본)    최초 크론 등록"
      echo "  --update  기존 크론 설정 업데이트"
      echo "  --remove  크론 제거"
      exit 0
      ;;
  esac
done

# ── 헬퍼 함수 ───────────────────────────────────────────────

# cron 파일 유효성 확인
validate_cron_file() {
  if [ ! -f "$CRON_FILE" ]; then
    echo "❌ 크론 파일 없음: $CRON_FILE"
    return 1
  fi
  if ! python3 -c "import json; json.load(open('$CRON_FILE'))" 2>/dev/null; then
    echo "❌ 크론 파일 JSON 파싱 실패: $CRON_FILE"
    return 1
  fi
  return 0
}

# 기존 크론 존재 여부 확인
check_existing() {
  python3 -c "
import json
try:
    with open('$CRON_FILE') as f:
        d = json.load(f)
    jobs = d.get('jobs', [])
    match = [j for j in jobs if '$CRON_NAME' in j.get('name', '')]
    print(match[0]['id'] if match else 'not_found')
except Exception as e:
    print('error:' + str(e))
" 2>/dev/null || echo "error"
}

# UUID 생성 (Python)
gen_uuid() {
  python3 -c "import uuid; print(str(uuid.uuid4()))" 2>/dev/null || date '+%s'
}

# 크론 페이로드 메시지 생성
build_cron_message() {
  cat << 'MSGEOF'
bash ~/openclaw/skills/self-evolving-agent/scripts/v4/orchestrator.sh 2>/dev/null || echo '분석 실패: 로그 확인 필요'

위 스크립트 실행 결과를 그대로 출력하세요.
⛔ message 도구 호출 절대 금지. 텍스트 출력만.
MSGEOF
}

# ── 크론 등록 ───────────────────────────────────────────────
do_register() {
  echo "=== Self-Evolving Agent 크론 등록 ==="

  local existing_id
  existing_id="$(check_existing)"

  if [ "$existing_id" != "not_found" ] && [ "$existing_id" != "error" ] && ! echo "$existing_id" | grep -q "^error:"; then
    echo "⚠️  이미 등록됨 (ID: $existing_id)"
    echo "   업데이트하려면: bash $0 --update"
    echo "   제거하려면:    bash $0 --remove"
    return 0
  fi

  validate_cron_file || return 1

  # 백업
  cp "$CRON_FILE" "$CRON_BACKUP" 2>/dev/null && echo "✅ 백업: $CRON_BACKUP" || echo "⚠️ 백업 실패 (계속 진행)"

  local new_id
  new_id="$(gen_uuid)"
  local now_ms
  now_ms="$(python3 -c "import time; print(int(time.time() * 1000))" 2>/dev/null || echo 0)"
  local cron_message
  cron_message="$(build_cron_message)"

  python3 << PYEOF
import json, sys

cron_message = '''$cron_message'''

try:
    with open('$CRON_FILE', encoding='utf-8') as f:
        data = json.load(f)
except Exception as e:
    print(f'❌ 파일 읽기 실패: {e}')
    sys.exit(1)

new_job = {
    "id": "$new_id",
    "agentId": "$CRON_AGENT",
    "name": "$CRON_NAME",
    "enabled": True,
    "createdAtMs": $now_ms,
    "updatedAtMs": $now_ms,
    "schedule": {
        "kind": "cron",
        "expr": "$CRON_SCHEDULE",
        "tz": "Asia/Seoul"
    },
    "sessionTarget": "isolated",
    "wakeMode": "now",
    "payload": {
        "kind": "agentTurn",
        "model": "$CRON_MODEL",
        "message": cron_message,
        "thinking": "off"
    },
    "delivery": {
        "mode": "announce",
        "channel": "discord",
        "to": "channel:$CRON_DISCORD"
    },
    "state": {
        "consecutiveErrors": 0
    }
}

data.setdefault('jobs', []).append(new_job)

try:
    with open('$CRON_FILE', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
except Exception as e:
    print(f'❌ 파일 쓰기 실패: {e}')
    sys.exit(1)

print(f"✅ 크론 등록 완료!")
print(f"   이름: {new_job['name']}")
print(f"   ID: {new_job['id']}")
print(f"   스케줄: {new_job['schedule']['expr']} (Asia/Seoul)")
print(f"   모델: {new_job['payload']['model']}")
print(f"   채널: channel:{new_job['delivery']['to'].split(':')[-1]}")
PYEOF
}

# ── 크론 업데이트 ────────────────────────────────────────────
do_update() {
  echo "=== Self-Evolving Agent 크론 업데이트 ==="

  local existing_id
  existing_id="$(check_existing)"

  if [ "$existing_id" = "not_found" ]; then
    echo "⚠️ 등록된 크론 없음. 등록 먼저 실행: bash $0"
    return 1
  fi

  validate_cron_file || return 1
  cp "$CRON_FILE" "$CRON_BACKUP" 2>/dev/null || true

  local now_ms
  now_ms="$(python3 -c "import time; print(int(time.time() * 1000))" 2>/dev/null || echo 0)"
  local cron_message
  cron_message="$(build_cron_message)"

  python3 << PYEOF
import json, sys

cron_message = '''$cron_message'''
target_id = '$existing_id'

with open('$CRON_FILE', encoding='utf-8') as f:
    data = json.load(f)

updated = False
for job in data.get('jobs', []):
    if job.get('id') == target_id or '$CRON_NAME' in job.get('name', ''):
        job['schedule']['expr'] = '$CRON_SCHEDULE'
        job['payload']['model'] = '$CRON_MODEL'
        job['payload']['message'] = cron_message
        job['delivery']['to'] = 'channel:$CRON_DISCORD'
        job['updatedAtMs'] = $now_ms
        updated = True
        print(f"✅ 업데이트: {job['name']} (ID: {job['id']})")
        break

if not updated:
    print('⚠️ 대상 크론 찾지 못함')
    sys.exit(0)

with open('$CRON_FILE', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"   스케줄: $CRON_SCHEDULE")
print(f"   모델: $CRON_MODEL")
PYEOF
}

# ── 크론 제거 ────────────────────────────────────────────────
do_remove() {
  echo "=== Self-Evolving Agent 크론 제거 ==="

  validate_cron_file || return 1
  cp "$CRON_FILE" "$CRON_BACKUP" 2>/dev/null || true

  python3 << PYEOF
import json, sys

with open('$CRON_FILE', encoding='utf-8') as f:
    data = json.load(f)

before_count = len(data.get('jobs', []))
data['jobs'] = [j for j in data.get('jobs', []) if '$CRON_NAME' not in j.get('name', '')]
after_count = len(data.get('jobs', []))
removed = before_count - after_count

with open('$CRON_FILE', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

if removed > 0:
    print(f"✅ 크론 제거 완료 ({removed}개)")
else:
    print("⚠️ 제거할 크론 없음")
PYEOF
}

# ── 메인 ────────────────────────────────────────────────────
main() {
  echo "설정: 스케줄=$CRON_SCHEDULE | 모델=$CRON_MODEL | 채널=$CRON_DISCORD"
  echo ""

  case "$MODE" in
    register) do_register ;;
    update)   do_update ;;
    remove)   do_remove ;;
  esac
}

main "$@"
