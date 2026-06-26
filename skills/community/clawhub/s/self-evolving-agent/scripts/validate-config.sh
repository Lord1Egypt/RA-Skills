#!/usr/bin/env bash
# ============================================================
# validate-config.sh — Self-Evolving Agent 설정 검증기 v1.0
#
# 역할: config.yaml 유효성 검사. 오케스트레이터 실행 전 호출.
#
# 사용법:
#   bash validate-config.sh            # 상세 출력
#   bash validate-config.sh --quiet    # 조용한 모드 (exit code만)
#   bash validate-config.sh --fix      # 오류와 함께 수정 방법 안내
#
# 종료 코드:
#   0 — 설정 유효
#   1 — 하나 이상의 검증 실패
#
# 환경변수:
#   SEA_CONFIG — 검사할 config.yaml 경로 (기본: 자동 탐색)
#
# 검사 항목:
#   ✓ config.yaml 존재 여부
#   ✓ 유효한 YAML 형식
#   ✓ 필수 필드 존재 (analysis.days, analysis.max_sessions)
#   ✓ complaint_patterns에 ko 또는 en 패턴 최소 1개
#   ✓ delivery.platform 유효 값 (discord/slack/telegram/webhook)
#   ✓ Slack 플랫폼 → webhook_url 설정
#   ✓ Telegram 플랫폼 → bot_token + chat_id 설정
#   ✓ Discord 채널 ID가 구 하드코딩 값이 아닌지 확인
#   ✓ 숫자 범위 검사 (days: 1-90, max_sessions: 1-200)
# ============================================================

# SECURITY MANIFEST:
# Environment variables accessed: SEA_CONFIG, QUIET, FIX_MODE
# External endpoints called: None
# Local files read:
#   <SEA_CONFIG> / ~/openclaw/skills/self-evolving-agent/config.yaml
# Local files written: None
# Network: None

# !! set -euo pipefail 미사용 !!

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

# ── 플래그 파싱 ─────────────────────────────────────────────
QUIET=false
FIX_MODE=false
for arg in "$@"; do
  case "$arg" in
    --quiet|-q) QUIET=true ;;
    --fix)      FIX_MODE=true ;;
    --help|-h)
      echo "사용법: $0 [--quiet] [--fix]"
      echo "  --quiet  오류 없이 exit code만 반환"
      echo "  --fix    각 오류에 수정 방법 안내"
      exit 0
      ;;
  esac
done

# ── config.yaml 경로 탐색 ───────────────────────────────────
find_config() {
  if [ -n "${SEA_CONFIG:-}" ] && [ -f "$SEA_CONFIG" ]; then
    echo "$SEA_CONFIG"; return
  fi
  if [ -f "$SKILL_DIR/config.yaml" ]; then
    echo "$SKILL_DIR/config.yaml"; return
  fi
  echo "$HOME/openclaw/skills/self-evolving-agent/config.yaml"
}

CONFIG_FILE="$(find_config)"

# ── 출력 유틸 ───────────────────────────────────────────────
ERRORS=()
WARNINGS=()

err() {
  ERRORS+=("$1")
  [[ "$QUIET" == "true" ]] && return
  echo "  ❌ $1" >&2
  if [[ "$FIX_MODE" == "true" && -n "${2:-}" ]]; then
    echo "     → 수정: $2" >&2
  fi
}

warn() {
  WARNINGS+=("$1")
  [[ "$QUIET" == "true" ]] && return
  echo "  ⚠️  $1" >&2
}

ok() {
  [[ "$QUIET" == "true" ]] && return
  echo "  ✅ $1" >&2
}

# ── 검사 1: config.yaml 존재 여부 ───────────────────────────
check_file_exists() {
  if [ ! -f "$CONFIG_FILE" ]; then
    err "config.yaml 없음: $CONFIG_FILE" \
        "setup-wizard.sh 실행: bash $SCRIPT_DIR/setup-wizard.sh"
    return 1
  fi
  ok "config.yaml 존재: $CONFIG_FILE"
  return 0
}

# ── Python 검증 (PyYAML 또는 간단한 폴백 파서) ──────────────
# 출력 형식:
#   OK|메시지          — 검사 통과
#   ERR|메시지|수정방법 — 검사 실패
#   WARN|메시지        — 경고 (실패 아님)
run_python_checks() {
  local config_file="$1"
  python3 << PYEOF 2>/dev/null
import sys

config_file = r'$config_file'
errors = []    # (message, fix) tuples
warnings = []  # message strings

# ── YAML 파싱 ─────────────────────────────────────────────
def parse_simple_yaml(path):
    """PyYAML 없는 환경용 간단한 파서 (스칼라 + 섹션 구조)."""
    result = {}
    try:
        with open(path, encoding='utf-8') as f:
            lines = f.readlines()
    except Exception:
        return {}
    current_section = None
    current_sub = None
    current_subsub = None
    for raw in lines:
        line = raw.rstrip()
        stripped = line.lstrip()
        if not stripped or stripped.startswith('#'):
            continue
        indent = len(line) - len(stripped)
        if ':' not in stripped:
            continue
        key_part, _, val_part = stripped.partition(':')
        key = key_part.strip()
        val = val_part.strip().split('#')[0].strip().strip('"\'')
        if indent == 0:
            current_section = key
            current_sub = None
            current_subsub = None
            result.setdefault(key, {})
        elif indent == 2 and current_section:
            sec = result.setdefault(current_section, {})
            if val:
                sec[key] = val
                current_sub = None
            else:
                sec.setdefault(key, {})
                current_sub = key
                current_subsub = None
        elif indent == 4 and current_section and current_sub:
            sec = result.get(current_section, {})
            sub = sec.get(current_sub, {})
            if isinstance(sub, dict):
                if val:
                    sub[key] = val
                    current_subsub = None
                else:
                    sub.setdefault(key, {})
                    current_subsub = key
        elif indent == 6 and current_section and current_sub and current_subsub:
            sec = result.get(current_section, {})
            sub = sec.get(current_sub, {})
            if isinstance(sub, dict):
                subsub = sub.get(current_subsub, {})
                if isinstance(subsub, dict) and val:
                    subsub[key] = val
    return result

yaml_ok = False
cfg = {}
try:
    import yaml
    with open(config_file, encoding='utf-8') as f:
        cfg = yaml.safe_load(f)
    if cfg is None:
        errors.append(("config.yaml가 비어 있습니다",
                        "bash $SCRIPT_DIR/setup-wizard.sh 실행"))
        for msg, fix in errors:
            print(f"ERR|{msg}|{fix}")
        sys.exit(0)
    yaml_ok = True
except ImportError:
    try:
        cfg = parse_simple_yaml(config_file)
    except Exception as e:
        errors.append((f"YAML 파싱 실패: {e}", "config.yaml 문법을 확인하세요"))
        for msg, fix in errors:
            print(f"ERR|{msg}|{fix}")
        sys.exit(0)
except Exception as e:
    errors.append((f"YAML 파싱 실패: {e}", "config.yaml 문법을 확인하세요"))
    for msg, fix in errors:
        print(f"ERR|{msg}|{fix}")
    sys.exit(0)

if not isinstance(cfg, dict):
    errors.append(("YAML 최상위 구조가 올바르지 않습니다", "config.yaml 구조를 확인하세요"))
    for msg, fix in errors:
        print(f"ERR|{msg}|{fix}")
    sys.exit(0)

if yaml_ok:
    print("OK|유효한 YAML 형식")
else:
    print("OK|YAML 파싱 완료 (폴백 파서 사용 — PyYAML 설치 권장)")

# ── 검사 3: 필수 필드 ─────────────────────────────────────
analysis = cfg.get('analysis', {})
if not isinstance(analysis, dict):
    errors.append(("analysis 섹션 없음",
                   "config.yaml에 analysis: 섹션 추가 후 days, max_sessions 설정"))
else:
    days = analysis.get('days')
    if days is None:
        errors.append(("analysis.days 필드 없음",
                       "analysis:\\n  days: 7  # 1-90 범위"))
    else:
        try:
            days_int = int(days)
            if days_int < 1 or days_int > 90:
                errors.append((f"analysis.days={days_int} 범위 초과 (허용: 1-90)",
                                "days: 7  # 1-90 사이 값으로 수정"))
            else:
                print(f"OK|analysis.days={days_int}")
        except (ValueError, TypeError):
            errors.append((f"analysis.days='{days}' 숫자가 아님",
                           "days: 7  # 정수값 필요"))

    max_s = analysis.get('max_sessions')
    if max_s is None:
        errors.append(("analysis.max_sessions 필드 없음",
                       "analysis:\\n  max_sessions: 30  # 1-200 범위"))
    else:
        try:
            max_s_int = int(max_s)
            if max_s_int < 1 or max_s_int > 200:
                errors.append((f"analysis.max_sessions={max_s_int} 범위 초과 (허용: 1-200)",
                                "max_sessions: 30  # 1-200 사이 값으로 수정"))
            else:
                print(f"OK|analysis.max_sessions={max_s_int}")
        except (ValueError, TypeError):
            errors.append((f"analysis.max_sessions='{max_s}' 숫자가 아님",
                           "max_sessions: 30  # 정수값 필요"))

# ── 검사 4: complaint_patterns ────────────────────────────
patterns = analysis.get('complaint_patterns', {}) if isinstance(analysis, dict) else {}

if isinstance(patterns, dict):
    ko = patterns.get('ko', [])
    en = patterns.get('en', [])
    has_ko = isinstance(ko, list) and len(ko) > 0
    has_en = isinstance(en, list) and len(en) > 0
    if not has_ko and not has_en:
        errors.append(("complaint_patterns에 ko/en 패턴이 없습니다",
                       "config.yaml의 complaint_patterns.ko 또는 .en에 최소 1개 패턴 추가"))
    else:
        ko_count = len(ko) if has_ko else 0
        en_count = len(en) if has_en else 0
        print(f"OK|ko={ko_count}개, en={en_count}개 불만 패턴")
elif isinstance(patterns, list):
    if len(patterns) == 0:
        errors.append(("complaint_patterns 목록이 비어 있습니다",
                       "패턴을 추가하거나 setup-wizard.sh 재실행"))
    else:
        warnings.append("complaint_patterns가 구버전 형식 (flat list). ko/en 분리 구조 권장")
        print(f"OK|{len(patterns)}개 패턴 (구버전 형식)")
else:
    errors.append(("complaint_patterns 섹션 없거나 잘못된 형식",
                   "config.yaml의 complaint_patterns 섹션을 추가하세요"))

# ── 검사 5: delivery.platform ─────────────────────────────
delivery = cfg.get('delivery', {})
if not isinstance(delivery, dict):
    delivery = {}

platform = str(delivery.get('platform', '')).strip().lower()
valid_platforms = ['discord', 'slack', 'telegram', 'webhook']

if not platform:
    errors.append(("delivery.platform 미설정",
                   "delivery:\\n  platform: discord  # discord/slack/telegram/webhook 중 선택"))
elif platform not in valid_platforms:
    errors.append((f"delivery.platform='{platform}' 유효하지 않음",
                   f"platform: discord  # 허용 값: {', '.join(valid_platforms)}"))
else:
    print(f"OK|delivery.platform={platform}")

    # ── 검사 6: Slack → webhook_url ──────────────────────────
    if platform == 'slack':
        slack = delivery.get('slack', {})
        webhook_url = str(slack.get('webhook_url', '') if isinstance(slack, dict) else '').strip()
        if not webhook_url:
            errors.append(("delivery.slack.webhook_url 미설정",
                           'delivery:\\n  slack:\\n    webhook_url: "https://hooks.slack.com/services/..."'))
        elif not webhook_url.startswith('https://hooks.slack.com/'):
            errors.append((f"webhook_url='{webhook_url[:40]}...' Slack 형식 아님",
                           "https://hooks.slack.com/services/T.../B.../... 형식이어야 합니다"))
        else:
            print("OK|Slack webhook_url 설정됨")

    # ── 검사 7: Telegram → bot_token + chat_id ───────────────
    elif platform == 'telegram':
        tg = delivery.get('telegram', {})
        bot_token = str(tg.get('bot_token', '') if isinstance(tg, dict) else '').strip()
        chat_id   = str(tg.get('chat_id', '')   if isinstance(tg, dict) else '').strip()
        missing = []
        if not bot_token:
            missing.append("bot_token 미설정")
        if not chat_id:
            missing.append("chat_id 미설정")
        if missing:
            errors.append((f"Telegram 설정 불완전: {', '.join(missing)}",
                           'delivery:\\n  telegram:\\n    bot_token: "123456:ABC-DEF..."\\n    chat_id: "-1001234567890"'))
        else:
            print(f"OK|Telegram bot_token=...{bot_token[-5:]}, chat_id={chat_id}")

# ── 검사 8: Discord 구 하드코딩 채널 ID ──────────────────────
OLD_CHANNEL_ID = "1469905074661757049"

discord_sect = delivery.get('discord', {})
discord_ch = str(discord_sect.get('channel_id', '') if isinstance(discord_sect, dict) else '').strip()
cron_ch     = str(cfg.get('cron', {}).get('discord_channel', '') if isinstance(cfg.get('cron'), dict) else '').strip()

for field_name, ch_val in [("delivery.discord.channel_id", discord_ch),
                            ("cron.discord_channel", cron_ch)]:
    if ch_val == OLD_CHANNEL_ID:
        errors.append((f"{field_name}={OLD_CHANNEL_ID} 은 구 하드코딩 채널 ID입니다",
                       "올바른 Discord 채널 ID로 변경하세요 (Discord > 채널 오른쪽 클릭 > ID 복사)"))
    elif ch_val and ch_val.strip('"\''):
        print(f"OK|{field_name}={ch_val}")
    else:
        warnings.append(f"{field_name} 미설정 (Discord 사용 시 필수)")

# ── 결과 출력 ────────────────────────────────────────────────
for msg, fix in errors:
    print(f"ERR|{msg}|{fix}")
for w in warnings:
    print(f"WARN|{w}")
PYEOF
}

# ── 메인 검증 실행 ───────────────────────────────────────────
main() {
  [[ "$QUIET" == "false" ]] && echo "🔍 config.yaml 검증 중: $CONFIG_FILE" >&2

  # 파일 존재 확인
  if ! check_file_exists; then
    [[ "$QUIET" == "false" ]] && echo "" >&2
    [[ "$QUIET" == "false" ]] && echo "❌ 검증 실패 (1개 오류)" >&2
    [[ "$QUIET" == "false" ]] && echo "   실행하세요: bash $SCRIPT_DIR/setup-wizard.sh" >&2
    return 1
  fi

  # Python 검증 실행
  local py_output
  py_output="$(run_python_checks "$CONFIG_FILE" 2>/dev/null)"

  local error_count=0
  local warn_count=0
  local ok_count=0

  # OK|메시지 / ERR|메시지|수정 / WARN|메시지
  while IFS='|' read -r code msg fix; do
    [[ -z "$code" ]] && continue
    case "$code" in
      OK)
        ok "${msg:-OK}"
        ok_count=$(( ok_count + 1 ))
        ;;
      ERR)
        err "${msg:-알 수 없는 오류}" "${fix:-}"
        error_count=$(( error_count + 1 ))
        ;;
      WARN)
        warn "${msg:-경고}"
        warn_count=$(( warn_count + 1 ))
        ;;
    esac
  done <<< "$py_output"

  # Python 실행 실패
  if [ -z "$py_output" ]; then
    err "Python 실행 실패 — python3를 확인하세요" "python3 --version 으로 설치 확인"
    error_count=$(( error_count + 1 ))
  fi

  # 최종 결과
  if [[ "$QUIET" == "false" ]]; then
    echo "" >&2
    if [ "$error_count" -eq 0 ]; then
      echo "✅ config.yaml 유효 (검사 ${ok_count}개 통과, 경고 ${warn_count}개)" >&2
    else
      echo "❌ 검증 실패 ($error_count개 오류, $warn_count개 경고, $ok_count개 통과)" >&2
      echo "" >&2
      echo "   수정 후 재실행: bash $SCRIPT_DIR/validate-config.sh --fix" >&2
      echo "   또는 재설정:    bash $SCRIPT_DIR/setup-wizard.sh" >&2
    fi
  fi

  return $([ "$error_count" -eq 0 ] && echo 0 || echo 1)
}

main "$@"
