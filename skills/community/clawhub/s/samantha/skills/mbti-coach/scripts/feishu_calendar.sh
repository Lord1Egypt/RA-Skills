#!/usr/bin/env bash
# 飞书日历 API 工具脚本
# 用法：
#   feishu_calendar.sh list [days]          列出未来 N 天的事件（默认7天）
#   feishu_calendar.sh create TITLE START END [DESC]  创建事件
#   feishu_calendar.sh token                获取并打印 access token（调试用）

set -e

# ── 读取凭证 ──────────────────────────────────────────────────────────────────

FEISHU_BASE="https://open.feishu.cn/open-apis"

_load_credentials() {
  # 1. 环境变量
  if [[ -n "$FEISHU_APP_ID" && -n "$FEISHU_APP_SECRET" ]]; then
    return 0
  fi
  # 2. openclaw 配置文件
  local cfg="$HOME/.openclaw/openclaw.json"
  if [[ -f "$cfg" ]]; then
    FEISHU_APP_ID=$(python3 -c "import json,sys; d=json.load(open('$cfg')); print(d.get('feishu_app_id',''))" 2>/dev/null || true)
    FEISHU_APP_SECRET=$(python3 -c "import json,sys; d=json.load(open('$cfg')); print(d.get('feishu_app_secret',''))" 2>/dev/null || true)
    if [[ -n "$FEISHU_APP_ID" && -n "$FEISHU_APP_SECRET" ]]; then
      return 0
    fi
  fi
  # 3. skill 目录下的 .env
  local skill_dir
  skill_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
  local env_file="$skill_dir/.env"
  if [[ -f "$env_file" ]]; then
    # shellcheck disable=SC1090
    source "$env_file"
  fi
  if [[ -z "$FEISHU_APP_ID" || -z "$FEISHU_APP_SECRET" ]]; then
    echo "错误：未找到飞书凭证。请设置环境变量 FEISHU_APP_ID 和 FEISHU_APP_SECRET" >&2
    exit 1
  fi
}

_get_token() {
  _load_credentials
  local resp
  resp=$(curl -s -X POST "$FEISHU_BASE/auth/v3/tenant_access_token/internal" \
    -H "Content-Type: application/json" \
    -d "{\"app_id\":\"$FEISHU_APP_ID\",\"app_secret\":\"$FEISHU_APP_SECRET\"}")
  local code
  code=$(echo "$resp" | python3 -c "import json,sys; print(json.load(sys.stdin).get('code',1))")
  if [[ "$code" != "0" ]]; then
    echo "飞书认证失败: $resp" >&2
    exit 1
  fi
  echo "$resp" | python3 -c "import json,sys; print(json.load(sys.stdin)['tenant_access_token'])"
}

_get_calendar_id() {
  local token="$1"
  # 优先使用环境变量
  if [[ -n "$FEISHU_CALENDAR_ID" ]]; then
    echo "$FEISHU_CALENDAR_ID"
    return
  fi
  local resp
  resp=$(curl -s "$FEISHU_BASE/calendar/v4/calendars" \
    -H "Authorization: Bearer $token")
  # 找 primary 日历
  echo "$resp" | python3 -c "
import json, sys
d = json.load(sys.stdin)
cals = d.get('data', {}).get('calendar_list', [])
for c in cals:
    if c.get('type') == 'primary':
        print(c['calendar_id'])
        sys.exit(0)
if cals:
    print(cals[0]['calendar_id'])
" 2>/dev/null
}

# ── 命令：list ────────────────────────────────────────────────────────────────

cmd_list() {
  local days="${1:-7}"
  local token
  token=$(_get_token)
  local cal_id
  cal_id=$(_get_calendar_id "$token")

  if [[ -z "$cal_id" ]]; then
    echo "错误：未找到可用日历" >&2
    exit 1
  fi

  local now
  now=$(date +%s)
  local end_ts
  end_ts=$((now + days * 86400))

  local resp
  resp=$(curl -s "$FEISHU_BASE/calendar/v4/calendars/$cal_id/events?start_time=$now&end_time=$end_ts&page_size=50" \
    -H "Authorization: Bearer $token")

  echo "$resp" | python3 -c "
import json, sys
from datetime import datetime
d = json.load(sys.stdin)
events = d.get('data', {}).get('items', [])
print(f'本周共 {len(events)} 个事件：')
print()
for e in events:
    ts = e.get('start_time', {}).get('timestamp', '')
    if ts:
        dt = datetime.fromtimestamp(int(ts)).strftime('%m/%d %H:%M')
    else:
        dt = '全天'
    title = e.get('summary', '(无标题)')
    desc = e.get('description', '')[:50]
    print(f'  [{dt}] {title}')
    if desc:
        print(f'         {desc}')
"
}

# ── 命令：create ──────────────────────────────────────────────────────────────

cmd_create() {
  local title="$1"
  local start_str="$2"   # 格式：2026-03-16 09:00
  local end_str="$3"     # 格式：2026-03-16 09:30
  local desc="${4:-}"

  if [[ -z "$title" || -z "$start_str" || -z "$end_str" ]]; then
    echo "用法：feishu_calendar.sh create TITLE START END [DESC]" >&2
    echo "示例：feishu_calendar.sh create '战略思考' '2026-03-16 09:00' '2026-03-16 09:20' '无手机深度思考'" >&2
    exit 1
  fi

  local start_ts end_ts
  start_ts=$(python3 -c "from datetime import datetime; print(int(datetime.strptime('$start_str', '%Y-%m-%d %H:%M').timestamp()))")
  end_ts=$(python3 -c "from datetime import datetime; print(int(datetime.strptime('$end_str', '%Y-%m-%d %H:%M').timestamp()))")

  local token
  token=$(_get_token)
  local cal_id
  cal_id=$(_get_calendar_id "$token")

  local payload
  payload=$(python3 -c "
import json
print(json.dumps({
    'summary': '$title',
    'description': '''$desc''',
    'start_time': {'timestamp': '$start_ts', 'timezone': 'Asia/Shanghai'},
    'end_time':   {'timestamp': '$end_ts',   'timezone': 'Asia/Shanghai'}
}))
")

  local resp
  resp=$(curl -s -X POST "$FEISHU_BASE/calendar/v4/calendars/$cal_id/events" \
    -H "Authorization: Bearer $token" \
    -H "Content-Type: application/json" \
    -d "$payload")

  local code
  code=$(echo "$resp" | python3 -c "import json,sys; print(json.load(sys.stdin).get('code',1))")
  if [[ "$code" == "0" ]]; then
    echo "✓ 已创建：$title ($start_str)"
  else
    echo "✗ 创建失败：$title — $resp" >&2
    exit 1
  fi
}

# ── 命令：token（调试用）──────────────────────────────────────────────────────

cmd_token() {
  _get_token
}

# ── 入口 ──────────────────────────────────────────────────────────────────────

case "${1:-}" in
  list)   cmd_list "${2:-7}" ;;
  create) cmd_create "$2" "$3" "$4" "${5:-}" ;;
  token)  cmd_token ;;
  *)
    echo "用法：feishu_calendar.sh <list|create|token> [参数]"
    exit 1
    ;;
esac
