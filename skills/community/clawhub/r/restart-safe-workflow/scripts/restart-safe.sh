#!/usr/bin/env bash
set -euo pipefail

# OpenClaw Restart Safe Flow
# Sprint 3.5: 任务级续跑（pendingActions + resume executor + reconcile）

STATE_DIR="${STATE_DIR:-./state/restart}"
GATEWAY_RESTART_CMD="${GATEWAY_RESTART_CMD:-openclaw gateway restart}"
HEALTH_TIMEOUT_SEC="${HEALTH_TIMEOUT_SEC:-30}"
RECONCILE_MAX_RETRIES="${RECONCILE_MAX_RETRIES:-3}"
RECONCILE_BACKOFF_SEC="${RECONCILE_BACKOFF_SEC:-5}"
ACTION_ALLOWLIST_FILE="${ACTION_ALLOWLIST_FILE:-}"
NOTIFY_CHANNEL="${NOTIFY_CHANNEL:-}"
NOTIFY_TARGET="${NOTIFY_TARGET:-}"
NOTIFY_ACCOUNT="${NOTIFY_ACCOUNT:-}"
NOTIFY_MODE="${NOTIFY_MODE:-compact}"
REPORT_VERBOSE="${REPORT_VERBOSE:-false}"

mkdir -p "$STATE_DIR"

log() { printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S%z')" "$*"; }
die() { log "ERROR: $*"; exit 1; }
require_cmd() { command -v "$1" >/dev/null 2>&1 || die "缺少命令: $1"; }

state_file() { echo "$STATE_DIR/$1.json"; }
runner_log_file() { echo "$STATE_DIR/$1.runner.log"; }

is_notify_required() {
  [ -n "$NOTIFY_CHANNEL" ] && [ -n "$NOTIFY_TARGET" ]
}

state_init() {
  local task_id="$1" title="$2" next_action="$3" criteria="$4"
  local file; file="$(state_file "$task_id")"
  python3 - "$file" "$task_id" "$title" "$next_action" "$criteria" <<'PY'
import json, os, sys
from datetime import datetime, timezone
file, task_id, title, next_action, criteria = sys.argv[1:]
now = datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds')
if os.path.exists(file):
    with open(file, 'r', encoding='utf-8') as f: obj = json.load(f)
else:
    obj = {
      "taskId": task_id,
      "phase": "init",
      "attempt": 0,
      "startedAt": now,
      "updatedAt": now,
      "title": title,
      "nextAction": next_action,
      "successCriteria": criteria,
      "doctorOk": False,
      "checkpointed": False,
      "restartIssued": False,
      "restartCompleted": False,
      "healthOk": False,
      "resumeEventSent": False,
      "notifyPreSent": False,
      "notifyPreMessageId": "",
      "notifyPostSent": False,
      "notifyPostMessageId": "",
      "notifyAlertSent": False,
      "notifyAlertMessageId": "",
      "resumeStatus": "idle",
      "resumeCursor": 0,
      "resumeError": "",
      "resumeLastAt": "",
      "resumeRetryCount": 0,
      "pendingActions": [],
      "resumeCompletedActions": [],
      "lastError": "",
      "runnerPid": "",
      "runnerLog": "",
      "timeline": []
    }
obj.setdefault("taskId", task_id)
obj["title"] = title
obj["nextAction"] = next_action
obj["successCriteria"] = criteria
obj["updatedAt"] = now
obj.setdefault("timeline", [])
obj.setdefault("pendingActions", [])
obj.setdefault("resumeCompletedActions", [])
obj.setdefault("escalationRequired", False)
obj.setdefault("escalationReason", "")
obj.setdefault("taskPlanVersion", "v1")
obj.setdefault("actionStates", {})
obj.setdefault("idempotencyLedger", {})
with open(file, 'w', encoding='utf-8') as f:
    json.dump(obj, f, ensure_ascii=False, indent=2)
PY
}

state_update() {
  local task_id="$1" phase="$2" note="$3" extra_json="${4:-}"
  [ -n "$extra_json" ] || extra_json='{}'
  local file; file="$(state_file "$task_id")"

  python3 - "$file" "$phase" "$note" "$extra_json" <<'PY'
import json, os, sys
from datetime import datetime, timezone
file, phase, note, extra_raw = sys.argv[1:]
now = datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds')
if os.path.exists(file):
    with open(file, 'r', encoding='utf-8') as f: obj = json.load(f)
else:
    obj = {"timeline": []}
try:
    extra = json.loads(extra_raw)
except Exception:
    extra = {}
obj["phase"] = phase
obj["updatedAt"] = now
obj.setdefault("timeline", []).append({"at": now, "phase": phase, "note": note})
for k, v in extra.items():
    obj[k] = v
with open(file, 'w', encoding='utf-8') as f:
    json.dump(obj, f, ensure_ascii=False, indent=2)
PY

  log "状态已写入: ${file} (phase=${phase})"
}

state_bump_attempt() {
  local task_id="$1"; local file; file="$(state_file "$task_id")"
  python3 - "$file" <<'PY'
import json, os, sys
from datetime import datetime, timezone
file = sys.argv[1]
now = datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds')
if os.path.exists(file):
    with open(file, 'r', encoding='utf-8') as f: obj = json.load(f)
else:
    obj = {"timeline": []}
obj["attempt"] = int(obj.get("attempt", 0)) + 1
obj["updatedAt"] = now
with open(file, 'w', encoding='utf-8') as f:
    json.dump(obj, f, ensure_ascii=False, indent=2)
PY
}

state_get() {
  local task_id="$1" key="$2"; local file; file="$(state_file "$task_id")"
  python3 - "$file" "$key" <<'PY'
import json, sys
f, k = sys.argv[1:]
with open(f, 'r', encoding='utf-8') as fh: obj = json.load(fh)
cur = obj
for p in k.split('.'):
    if isinstance(cur, dict) and p in cur:
        cur = cur[p]
    else:
        print('')
        raise SystemExit(0)
if isinstance(cur, bool):
    print('true' if cur else 'false')
elif cur is None:
    print('')
else:
    print(cur)
PY
}

emit_event() {
  local text="$1"
  if openclaw system event --mode now --text "$text" >/dev/null 2>&1; then
    log "事件已发送: $text"; return 0
  fi
  log "WARN: 事件发送失败（忽略，不阻断流程）: $text"; return 1
}

extract_message_id() {
  printf '%s' "$1" | sed -n 's/.*"messageId"[[:space:]]*:[[:space:]]*"\([^"]\+\)".*/\1/p' | head -n 1
}

emit_visible() {
  local task_id="$1" kind="$2" msg="$3"
  if ! is_notify_required; then
    log "可见通知未配置（NOTIFY_CHANNEL/NOTIFY_TARGET），跳过"
    return 1
  fi

  local sent_key msgid_key
  case "$kind" in
    pre) sent_key="notifyPreSent"; msgid_key="notifyPreMessageId" ;;
    post) sent_key="notifyPostSent"; msgid_key="notifyPostMessageId" ;;
    alert) sent_key="notifyAlertSent"; msgid_key="notifyAlertMessageId" ;;
    *) die "未知通知类型: $kind" ;;
  esac

  if [ "$(state_get "$task_id" "$sent_key" || true)" = "true" ]; then
    log "可见通知已存在（kind=$kind），跳过重复发送"
    return 0
  fi

  local cmd=(openclaw message send --json --channel "$NOTIFY_CHANNEL" --target "$NOTIFY_TARGET" --message "$msg")
  [ -n "$NOTIFY_ACCOUNT" ] && cmd+=(--account "$NOTIFY_ACCOUNT")

  local out
  if out="$("${cmd[@]}" 2>&1)"; then
    local message_id
    message_id="$(extract_message_id "$out")"
    state_update "$task_id" "$(state_get "$task_id" phase)" "visible-notify:${kind}" "{\"${sent_key}\":true,\"${msgid_key}\":\"${message_id}\",\"lastError\":\"\"}"
    log "可见通知已发送: $NOTIFY_CHANNEL -> $NOTIFY_TARGET (kind=$kind, messageId=${message_id:-unknown})"
    return 0
  fi

  log "WARN: 可见通知发送失败（kind=$kind）: $out"
  return 1
}

wait_for_health() {
  local start_ts now_ts
  start_ts="$(date +%s)"
  while true; do
    now_ts="$(date +%s)"
    [ $((now_ts - start_ts)) -lt "$HEALTH_TIMEOUT_SEC" ] || return 1
    if openclaw gateway status >/dev/null 2>&1 && openclaw health >/dev/null 2>&1; then
      log "网关健康检查通过"; return 0
    fi
    sleep 2
  done
}

set_resume_status() {
  local task_id="$1" status="$2" err="${3:-}"
  local extra
  extra="{\"resumeStatus\":\"$status\",\"resumeError\":\"$err\",\"resumeLastAt\":\"$(date -Iseconds)\"}"
  state_update "$task_id" "$(state_get "$task_id" phase)" "resume-status:${status}" "$extra"
}

actions_to_readable() {
  local file="$1" key="$2"
  python3 - "$file" "$key" <<'PY'
import json,sys
f,key=sys.argv[1:]
obj=json.load(open(f,'r',encoding='utf-8'))
arr=obj.get(key,[])
lines=[]
for i,a in enumerate(arr,1):
    t=a.get('type','notify')
    aid=a.get('actionId',f'a{i}')
    if t=='notify':
        d=a.get('text','')
    elif t=='command':
        d=a.get('command','')
    elif t=='script':
        d=a.get('path','')
    else:
        d=str(a)
    lines.append(f"{i}. [{aid}] {t}: {d}")
print('\n'.join(lines))
PY
}

action_state_stats() {
  local file="$1"
  python3 - "$file" <<'PY'
import json,sys
obj=json.load(open(sys.argv[1],'r',encoding='utf-8'))
states=obj.get('actionStates',{}) or {}
stats={'pending':0,'running':0,'success':0,'failed':0,'skipped':0,'unknown':0}
for _,v in states.items():
    s=v.get('status','unknown')
    if s in stats:
        stats[s]+=1
    else:
        stats['unknown']+=1
print(json.dumps(stats, ensure_ascii=False))
PY
}

action_state_details() {
  local file="$1"
  python3 - "$file" <<'PY'
import json,sys
obj=json.load(open(sys.argv[1],'r',encoding='utf-8'))
states=obj.get('actionStates',{}) or {}
rows=[]
for aid,v in states.items():
    rows.append({
      'actionId': aid,
      'status': v.get('status','unknown'),
      'attempts': v.get('attempts',0),
      'lastError': v.get('lastError','')
    })
rows=sorted(rows, key=lambda x: x['actionId'])
print(json.dumps(rows, ensure_ascii=False))
PY
}

emit_resume_summary() {
  local task_id="$1" stage="$2"
  local file; file="$(state_file "$task_id")"
  [ -f "$file" ] || return 0
  if ! is_notify_required; then
    return 0
  fi
  if [ "$NOTIFY_MODE" = "compact" ]; then
    return 0
  fi

  local pending done cursor stats
  pending="$(actions_to_readable "$file" pendingActions)"
  done="$(actions_to_readable "$file" resumeCompletedActions)"
  cursor="$(state_get "$task_id" resumeCursor)"
  [ -n "$cursor" ] || cursor="0"
  stats="$(action_state_stats "$file")"

  local msg
  case "$stage" in
    pre)
      msg="【重启前任务清单】任务 ${task_id}\n正在处理：重启事务执行链路\n重启后预计处理：\n${pending:-（无）}" ;;
    post-plan)
      msg="【重启后待处理任务】任务 ${task_id}\n待处理清单：\n${pending:-（无）}\n当前游标：${cursor}\n动作统计：${stats}" ;;
    post-result)
      msg="【重启后任务执行结果】任务 ${task_id}\n已完成：\n${done:-（无）}\n剩余待处理：\n${pending:-（无）}\n动作统计：${stats}" ;;
    *) return 0 ;;
  esac

  local cmd=(openclaw message send --json --channel "$NOTIFY_CHANNEL" --target "$NOTIFY_TARGET" --message "$msg")
  [ -n "$NOTIFY_ACCOUNT" ] && cmd+=(--account "$NOTIFY_ACCOUNT")
  local out
  out="$("${cmd[@]}" 2>&1)" || { log "WARN: 任务清单通知失败(stage=$stage): $out"; return 1; }
  log "任务清单通知已发送(stage=$stage)"
  return 0
}

parse_next_actions_json() {
  local next_action="$1"
  python3 - "$next_action" <<'PY'
import json, sys

s = sys.argv[1].strip()
actions = []

if not s:
    print('[]')
    raise SystemExit(0)

def add_notify(text):
    actions.append({"type":"notify","text":text})

def add_query_time(tz="Asia/Shanghai"):
    actions.append({"type":"query_time","timezone":tz,"format":"human"})

# 兼容原有前缀 + 支持分号串联表达式
parts = [p.strip() for p in s.split(';') if p.strip()]
if not parts:
    parts = [s]

for part in parts:
    if part.startswith('json:'):
        raw = part[5:].strip()
        obj = json.loads(raw)
        if isinstance(obj, dict):
            obj = [obj]
        if not isinstance(obj, list):
            raise ValueError('json: must be list/dict')
        actions.extend(obj)
    elif part == 'notify-time':
        add_query_time('Asia/Shanghai')
        add_notify('当前时间：${current_time_human}')
    elif part.startswith('notify-time:'):
        tz = part.split(':', 1)[1].strip() or 'Asia/Shanghai'
        add_query_time(tz)
        add_notify('当前时间：${current_time_human}')
    elif part.startswith('notify:'):
        add_notify(part[7:].strip() or '(empty notify)')
    elif part.startswith('cmd:'):
        actions.append({"type":"command","command":part[4:].strip()})
    elif part.startswith('script:'):
        actions.append({"type":"script","path":part[7:].strip()})
    else:
        # 默认当作用户可见续跑说明
        add_notify(f"【任务续跑】{part}")

for i, a in enumerate(actions):
    if not isinstance(a, dict):
        raise ValueError('action must be object')
    a.setdefault('actionId', f'a{i+1}')
    a.setdefault('type', 'notify')

print(json.dumps(actions, ensure_ascii=False))
PY
}

compile_next_plan() {
  local task_id="$1" next_action="$2"
  local actions_json
  actions_json="$(parse_next_actions_json "$next_action")" || return 1
  python3 - "$task_id" "$actions_json" <<'PY'
import json,sys

task_id=sys.argv[1]
actions=json.loads(sys.argv[2])
plan={"taskPlanVersion":"v1","taskId":task_id,"actions":actions}
print(json.dumps(plan, ensure_ascii=False, indent=2))
PY
}

plan_only() {
  local task_id="$1" next_action="$2"
  compile_next_plan "$task_id" "$next_action"
}

validate_tasks_file() {
  local tasks_file="$1"
  [ -f "$tasks_file" ] || die "任务计划文件不存在: $tasks_file"
  python3 - "$tasks_file" <<'PY'
import json,sys
p=sys.argv[1]
obj=json.load(open(p,'r',encoding='utf-8'))
errs=[]
if obj.get('taskPlanVersion')!='v1':
    errs.append('taskPlanVersion 必须为 v1')
if not obj.get('taskId'):
    errs.append('taskId 不能为空')
actions=obj.get('actions')
if not isinstance(actions,list) or not actions:
    errs.append('actions 必须为非空数组')
allowed={'notify','query_time','command','script','tool_call'}
if isinstance(actions,list):
    for i,a in enumerate(actions,1):
        if not isinstance(a,dict):
            errs.append(f'actions[{i}] 必须为对象'); continue
        if not a.get('actionId'):
            errs.append(f'actions[{i}] 缺少 actionId')
        t=a.get('type')
        if t not in allowed:
            errs.append(f'actions[{i}] 非法 type: {t}')

if errs:
    print('VALIDATE: FAIL')
    for e in errs:
        print('-',e)
    raise SystemExit(1)

print('VALIDATE: OK')
print(json.dumps({'taskId':obj['taskId'],'actions':len(actions)}, ensure_ascii=False))
PY
}

actions_json_from_tasks_file() {
  local tasks_file="$1"
  python3 - "$tasks_file" <<'PY'
import json,sys
obj=json.load(open(sys.argv[1],'r',encoding='utf-8'))
print(json.dumps(obj.get('actions',[]), ensure_ascii=False))
PY
}

normalize_actions_for_state() {
  local actions_json="$1"
  python3 - "$actions_json" <<'PY'
import json,sys
arr=json.loads(sys.argv[1])
for i,a in enumerate(arr,1):
    if not isinstance(a,dict):
        a={"type":"notify","text":str(a)}
        arr[i-1]=a
    a.setdefault('actionId', f'a{i}')
    a.setdefault('type', 'notify')
    a.setdefault('deps', [])
    a.setdefault('retryPolicy', {"maxRetries":0,"backoffSec":5,"strategy":"linear"})
    a.setdefault('timeoutSec', 120)
    a.setdefault('onFailure', 'stop')
    a.setdefault('idempotencyKey', f"{a.get('type','notify')}:{a.get('actionId',f'a{i}')}")
print(json.dumps(arr, ensure_ascii=False))
PY
}

action_state_init_json() {
  local actions_json="$1"
  python3 - "$actions_json" <<'PY'
import json,sys
arr=json.loads(sys.argv[1])
states={}
for a in arr:
    aid=str(a.get('actionId',''))
    if not aid:
        continue
    states[aid]={"status":"pending","attempts":0,"lastError":"","startedAt":"","finishedAt":""}
print(json.dumps(states, ensure_ascii=False))
PY
}

idempotency_seen() {
  local task_id="$1" idem_key="$2"
  [ -n "$idem_key" ] || return 1
  local v
  v="$(state_get "$task_id" "idempotencyLedger.${idem_key}" || true)"
  [ "$v" = "true" ]
}

idempotency_mark_done() {
  local task_id="$1" idem_key="$2"
  [ -n "$idem_key" ] || return 0
  local file; file="$(state_file "$task_id")"
  python3 - "$file" "$idem_key" <<'PY'
import json,sys
from datetime import datetime, timezone
f,key=sys.argv[1:]
obj=json.load(open(f,'r',encoding='utf-8'))
ledger=obj.setdefault('idempotencyLedger',{})
ledger[key]=True
obj['updatedAt']=datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds')
json.dump(obj,open(f,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('ok')
PY
  state_update "$task_id" "resume-running" "idempotency-mark:${idem_key}" '{}'
}

action_state_mark() {
  local task_id="$1" action_id="$2" status="$3" err="${4:-}" attempts="${5:-}"
  local file; file="$(state_file "$task_id")"
  python3 - "$file" "$action_id" "$status" "$err" "$attempts" <<'PY'
import json,sys
from datetime import datetime, timezone
f,aid,status,err,attempts = sys.argv[1:]
obj=json.load(open(f,'r',encoding='utf-8'))
st=obj.setdefault('actionStates',{}).setdefault(aid,{"status":"pending","attempts":0,"lastError":"","startedAt":"","finishedAt":""})
now=datetime.now(timezone.utc).astimezone().isoformat(timespec='seconds')
st['status']=status
if attempts:
    try: st['attempts']=int(attempts)
    except: pass
if err is not None:
    st['lastError']=err
if status=='running':
    st['startedAt']=now
if status in ('success','failed','skipped'):
    st['finishedAt']=now
obj['updatedAt']=now
json.dump(obj,open(f,'w',encoding='utf-8'),ensure_ascii=False,indent=2)
print('ok')
PY
}

action_deps_met() {
  local task_id="$1" action_json="$2"
  python3 - "$(state_file "$task_id")" "$action_json" <<'PY'
import json,sys
state=json.load(open(sys.argv[1],'r',encoding='utf-8'))
a=json.loads(sys.argv[2])
deps=a.get('deps') or a.get('params',{}).get('deps') or []
states=state.get('actionStates',{})
for d in deps:
    if states.get(str(d),{}).get('status')!='success':
        print('false')
        raise SystemExit(0)
print('true')
PY
}

queue_resume_actions() {
  local task_id="$1" next_action="$2"
  local actions_json action_states_json
  if ! actions_json="$(parse_next_actions_json "$next_action" 2>/tmp/restart-parse.err)"; then
    local err; err="$(cat /tmp/restart-parse.err 2>/dev/null | tr '\n' ' ' | sed 's/"/\\"/g')"
    state_update "$task_id" "resume-failed" "parse-next-action-failed" "{\"resumeStatus\":\"failed\",\"resumeError\":\"$err\",\"lastError\":\"parse nextAction failed\"}"
    return 1
  fi

  actions_json="$(normalize_actions_for_state "$actions_json")"
  action_states_json="$(action_state_init_json "$actions_json")"

  state_update "$task_id" "resume-queued" "resume-actions-queued" "{\"taskPlanVersion\":\"v1\",\"pendingActions\":$actions_json,\"resumeCompletedActions\":[],\"resumeCursor\":0,\"resumeStatus\":\"idle\",\"resumeError\":\"\",\"resumeRetryCount\":0,\"actionStates\":$action_states_json}"
  return 0
}

is_allowed_command() {
  local cmd="$1"

  # Optional external allowlist (plain text, one prefix per line, supports comments)
  if [ -n "$ACTION_ALLOWLIST_FILE" ] && [ -f "$ACTION_ALLOWLIST_FILE" ]; then
    while IFS= read -r line; do
      line="${line%%#*}"
      line="$(echo "$line" | xargs)"
      [ -n "$line" ] || continue
      if [[ "$cmd" == "$line"* ]]; then
        return 0
      fi
    done < "$ACTION_ALLOWLIST_FILE"
    return 1
  fi

  case "$cmd" in
    "openclaw gateway status"*|"openclaw health"*|"openclaw status"*|"date"*|"echo "*)
      return 0 ;;
    *)
      return 1 ;;
  esac
}

is_allowed_script() {
  local p="$1"
  case "$p" in
    skills/restart-safe-workflow/scripts/*|/home/ubuntu/.openclaw/workspace/skills/restart-safe-workflow/scripts/*)
      if [[ "$p" == *".."* ]]; then
        return 1
      fi
      return 0 ;;
    *) return 1 ;;
  esac
}

execute_action() {
  local task_id="$1" action_json="$2"

  local action_type action_id action_text action_cmd action_path action_tz
  action_type="$(python3 - "$action_json" <<'PY'
import json,sys
obj=json.loads(sys.argv[1]); print(obj.get('type','notify'))
PY
)"
  action_id="$(python3 - "$action_json" <<'PY'
import json,sys
obj=json.loads(sys.argv[1]); print(obj.get('actionId',''))
PY
)"

  case "$action_type" in
    notify)
      action_text="$(python3 - "$action_json" <<'PY'
import json,sys
obj=json.loads(sys.argv[1]); print(obj.get('text', obj.get('params',{}).get('text','')))
PY
)"
      if ! is_notify_required; then
        log "续跑 notify 动作缺少通知配置"
        return 1
      fi
      if [[ "$action_text" == *"\${current_time_human}"* ]]; then
        local current
        current="$(state_get "$task_id" currentTimeHuman || true)"
        action_text="${action_text//\$\{current_time_human\}/$current}"
      fi
      # 续跑动作的通知使用 post 通道，不写入 notifyPostSent，避免污染主流程判据
      local out cmd
      cmd=(openclaw message send --json --channel "$NOTIFY_CHANNEL" --target "$NOTIFY_TARGET" --message "$action_text")
      [ -n "$NOTIFY_ACCOUNT" ] && cmd+=(--account "$NOTIFY_ACCOUNT")
      out="$("${cmd[@]}" 2>&1)" || { log "续跑 notify 失败(actionId=$action_id): $out"; return 1; }
      log "续跑 notify 成功(actionId=$action_id)"
      ;;
    query_time)
      action_tz="$(python3 - "$action_json" <<'PY'
import json,sys
obj=json.loads(sys.argv[1])
print(obj.get('timezone') or obj.get('params',{}).get('timezone') or 'Asia/Shanghai')
PY
)"
      local iso human
      iso="$(TZ="$action_tz" date -Iseconds)"
      human="$(TZ="$action_tz" date '+%Y-%m-%d %H:%M:%S (%Z)')"
      state_update "$task_id" "resume-running" "resume-action-time:${action_id}" "{\"currentTimeIso\":\"$iso\",\"currentTimeHuman\":\"$human\",\"currentTimeTz\":\"$action_tz\"}"
      log "续跑 query_time 成功(actionId=$action_id): $human"
      ;;
    command)
      action_cmd="$(python3 - "$action_json" <<'PY'
import json,sys
obj=json.loads(sys.argv[1]); print(obj.get('command', obj.get('params',{}).get('command','')))
PY
)"
      if ! is_allowed_command "$action_cmd"; then
        log "续跑 command 不在白名单(actionId=$action_id): $action_cmd"
        return 1
      fi
      bash -lc "$action_cmd" >/tmp/restart-action-${task_id}-${action_id}.out 2>&1 || {
        log "续跑 command 执行失败(actionId=$action_id): $action_cmd"
        return 1
      }
      log "续跑 command 成功(actionId=$action_id): $action_cmd"
      ;;
    script)
      action_path="$(python3 - "$action_json" <<'PY'
import json,sys
obj=json.loads(sys.argv[1]); print(obj.get('path', obj.get('params',{}).get('path','')))
PY
)"
      if ! is_allowed_script "$action_path"; then
        log "续跑 script 不在白名单(actionId=$action_id): $action_path"
        return 1
      fi
      bash -lc "$action_path" >/tmp/restart-script-${task_id}-${action_id}.out 2>&1 || {
        log "续跑 script 执行失败(actionId=$action_id): $action_path"
        return 1
      }
      log "续跑 script 成功(actionId=$action_id): $action_path"
      ;;
    *)
      log "未知续跑动作类型(actionId=$action_id): $action_type"
      return 1 ;;
  esac

  return 0
}

run_resume_actions() {
  local task_id="$1"
  local file; file="$(state_file "$task_id")"
  [ -f "$file" ] || die "状态文件不存在: $file"

  set_resume_status "$task_id" running ""
  state_update "$task_id" "resume-running" "resume-actions-running" '{}'

  while true; do
    file="$(state_file "$task_id")"
    local actions_count
    actions_count="$(python3 - "$file" <<'PY'
import json,sys
obj=json.load(open(sys.argv[1],'r',encoding='utf-8'))
print(len(obj.get('pendingActions',[])))
PY
)"

    if [ "$actions_count" -eq 0 ]; then
      set_resume_status "$task_id" success ""
      state_update "$task_id" "resume-done" "resume-actions-complete" '{}'
      return 0
    fi

    local action_json action_id on_failure idem_key max_retries backoff deps_ok
    action_json="$(python3 - "$file" <<'PY'
import json,sys
obj=json.load(open(sys.argv[1],'r',encoding='utf-8'))
arr=obj.get('pendingActions',[])
print(json.dumps(arr[0], ensure_ascii=False) if arr else '')
PY
)"
    [ -n "$action_json" ] || {
      set_resume_status "$task_id" success ""
      state_update "$task_id" "resume-done" "resume-actions-empty" '{}'
      return 0
    }

    action_id="$(python3 - "$action_json" <<'PY'
import json,sys
a=json.loads(sys.argv[1]); print(a.get('actionId',''))
PY
)"
    on_failure="$(python3 - "$action_json" <<'PY'
import json,sys
a=json.loads(sys.argv[1]); print(a.get('onFailure','stop'))
PY
)"
    idem_key="$(python3 - "$action_json" <<'PY'
import json,sys
a=json.loads(sys.argv[1]); print(a.get('idempotencyKey',''))
PY
)"
    max_retries="$(python3 - "$action_json" <<'PY'
import json,sys
a=json.loads(sys.argv[1]); rp=a.get('retryPolicy',{}) or {}; print(rp.get('maxRetries',0))
PY
)"
    backoff="$(python3 - "$action_json" <<'PY'
import json,sys
a=json.loads(sys.argv[1]); rp=a.get('retryPolicy',{}) or {}; print(rp.get('backoffSec',5))
PY
)"

    deps_ok="$(action_deps_met "$task_id" "$action_json")"
    if [ "$deps_ok" != "true" ]; then
      action_state_mark "$task_id" "$action_id" "failed" "deps not satisfied" "0" >/dev/null
      if [ "$on_failure" = "continue" ] || [ "$on_failure" = "escalate" ]; then
        if [ "$on_failure" = "escalate" ]; then
          state_update "$task_id" "resume-running" "resume-action-escalate:${action_id}" '{"escalationRequired":true,"escalationReason":"action_deps_not_satisfied"}'
        fi
        local completed_json pending_json completed_count
        completed_json="$(python3 - "$file" "$action_id" <<'PY'
import json,sys
f,aid=sys.argv[1:]
obj=json.load(open(f,'r',encoding='utf-8'))
pending=obj.get('pendingActions',[])
done=obj.get('resumeCompletedActions',[])
for a in pending:
    if str(a.get('actionId',''))==aid:
        done.append(a); break
print(json.dumps(done, ensure_ascii=False))
PY
)"
        pending_json="$(python3 - "$file" "$action_id" <<'PY'
import json,sys
f,aid=sys.argv[1:]
obj=json.load(open(f,'r',encoding='utf-8'))
pending=[a for a in obj.get('pendingActions',[]) if str(a.get('actionId',''))!=aid]
print(json.dumps(pending, ensure_ascii=False))
PY
)"
        completed_count="$(python3 - "$completed_json" <<'PY'
import json,sys
print(len(json.loads(sys.argv[1])))
PY
)"
        state_update "$task_id" "resume-running" "resume-action-skip:${action_id}" "{\"resumeCursor\":$completed_count,\"resumeCompletedActions\":$completed_json,\"pendingActions\":$pending_json}"
        continue
      fi
      state_update "$task_id" "resume-failed" "resume-action-fail:${action_id}" "{\"resumeStatus\":\"failed\",\"resumeError\":\"deps not satisfied: ${action_id}\",\"lastError\":\"resume deps failed\"}"
      return 1
    fi

    if idempotency_seen "$task_id" "$idem_key"; then
      action_state_mark "$task_id" "$action_id" "skipped" "idempotency hit" "0" >/dev/null
      local completed_json pending_json completed_count
      completed_json="$(python3 - "$file" "$action_id" <<'PY'
import json,sys
f,aid=sys.argv[1:]
obj=json.load(open(f,'r',encoding='utf-8'))
pending=obj.get('pendingActions',[])
done=obj.get('resumeCompletedActions',[])
for a in pending:
    if str(a.get('actionId',''))==aid:
        done.append(a); break
print(json.dumps(done, ensure_ascii=False))
PY
)"
      pending_json="$(python3 - "$file" "$action_id" <<'PY'
import json,sys
f,aid=sys.argv[1:]
obj=json.load(open(f,'r',encoding='utf-8'))
pending=[a for a in obj.get('pendingActions',[]) if str(a.get('actionId',''))!=aid]
print(json.dumps(pending, ensure_ascii=False))
PY
)"
      completed_count="$(python3 - "$completed_json" <<'PY'
import json,sys
print(len(json.loads(sys.argv[1])))
PY
)"
      state_update "$task_id" "resume-running" "resume-action-skip-idempotent:${action_id}" "{\"resumeCursor\":$completed_count,\"resumeCompletedActions\":$completed_json,\"pendingActions\":$pending_json}"
      continue
    fi

    local attempt=1 success="false" last_err=""
    while [ "$attempt" -le $((max_retries + 1)) ]; do
      action_state_mark "$task_id" "$action_id" "running" "" "$attempt" >/dev/null
      state_update "$task_id" "resume-running" "resume-action-start:${action_id}:try-${attempt}" '{}'
      if execute_action "$task_id" "$action_json"; then
        success="true"
        action_state_mark "$task_id" "$action_id" "success" "" "$attempt" >/dev/null
        idempotency_mark_done "$task_id" "$idem_key"
        break
      fi
      last_err="action failed: ${action_id}, try=${attempt}"
      if [ "$attempt" -le "$max_retries" ]; then
        sleep $((backoff * attempt))
      fi
      attempt=$((attempt+1))
    done

    if [ "$success" = "true" ]; then
      local completed_json pending_json completed_count
      completed_json="$(python3 - "$file" "$action_id" <<'PY'
import json,sys
f,aid=sys.argv[1:]
obj=json.load(open(f,'r',encoding='utf-8'))
pending=obj.get('pendingActions',[])
done=obj.get('resumeCompletedActions',[])
for a in pending:
    if str(a.get('actionId',''))==aid:
        done.append(a); break
print(json.dumps(done, ensure_ascii=False))
PY
)"
      pending_json="$(python3 - "$file" "$action_id" <<'PY'
import json,sys
f,aid=sys.argv[1:]
obj=json.load(open(f,'r',encoding='utf-8'))
pending=[a for a in obj.get('pendingActions',[]) if str(a.get('actionId',''))!=aid]
print(json.dumps(pending, ensure_ascii=False))
PY
)"
      completed_count="$(python3 - "$completed_json" <<'PY'
import json,sys
print(len(json.loads(sys.argv[1])))
PY
)"
      state_update "$task_id" "resume-running" "resume-action-ok:${action_id}" "{\"resumeCursor\":$completed_count,\"resumeCompletedActions\":$completed_json,\"pendingActions\":$pending_json}"
      continue
    fi

    action_state_mark "$task_id" "$action_id" "failed" "$last_err" "$max_retries" >/dev/null
    if [ "$on_failure" = "continue" ] || [ "$on_failure" = "escalate" ]; then
      if [ "$on_failure" = "escalate" ]; then
        state_update "$task_id" "resume-running" "resume-action-escalate:${action_id}" '{"escalationRequired":true,"escalationReason":"action_failed"}'
      fi
      local completed_json pending_json completed_count
      completed_json="$(python3 - "$file" "$action_id" <<'PY'
import json,sys
f,aid=sys.argv[1:]
obj=json.load(open(f,'r',encoding='utf-8'))
pending=obj.get('pendingActions',[])
done=obj.get('resumeCompletedActions',[])
for a in pending:
    if str(a.get('actionId',''))==aid:
        done.append(a); break
print(json.dumps(done, ensure_ascii=False))
PY
)"
      pending_json="$(python3 - "$file" "$action_id" <<'PY'
import json,sys
f,aid=sys.argv[1:]
obj=json.load(open(f,'r',encoding='utf-8'))
pending=[a for a in obj.get('pendingActions',[]) if str(a.get('actionId',''))!=aid]
print(json.dumps(pending, ensure_ascii=False))
PY
)"
      completed_count="$(python3 - "$completed_json" <<'PY'
import json,sys
print(len(json.loads(sys.argv[1])))
PY
)"
      state_update "$task_id" "resume-running" "resume-action-fail-continue:${action_id}" "{\"resumeCursor\":$completed_count,\"resumeCompletedActions\":$completed_json,\"pendingActions\":$pending_json}"
      continue
    fi

    local retry
    retry="$(state_get "$task_id" resumeRetryCount)"
    [ -n "$retry" ] || retry="0"
    retry=$((retry+1))
    state_update "$task_id" "resume-failed" "resume-action-fail:${action_id}" "{\"resumeStatus\":\"failed\",\"resumeError\":\"$last_err\",\"resumeRetryCount\":$retry,\"lastError\":\"resume action failed\"}"
    return 1
  done
}


build_compact_post_message() {
  local task_id="$1"
  local file; file="$(state_file "$task_id")"
  python3 - "$file" <<'PY'
import json,sys
from datetime import datetime
obj=json.load(open(sys.argv[1],'r',encoding='utf-8'))

states=obj.get('actionStates',{}) or {}
completed=obj.get('resumeCompletedActions',[]) or []
pending_actions=obj.get('pendingActions',[]) or []

# action 元信息：优先从 completed/pending 提取 type 与简述
meta={}
for a in completed + pending_actions:
    if not isinstance(a,dict):
        continue
    aid=str(a.get('actionId',''))
    if not aid:
        continue
    t=a.get('type','unknown')
    brief=''
    if t=='notify':
        brief=(a.get('text') or a.get('params',{}).get('text',''))[:20]
    elif t=='command':
        brief=(a.get('command') or a.get('params',{}).get('command',''))[:20]
    elif t=='script':
        brief=(a.get('path') or a.get('params',{}).get('path',''))[:20]
    elif t=='query_time':
        brief=(a.get('timezone') or a.get('params',{}).get('timezone','Asia/Shanghai'))
    meta[aid]={'type':t,'brief':brief}

rows=[]
ok=fail=running=pending=skipped=0
for idx,(aid,v) in enumerate(sorted(states.items()), start=1):
    st=v.get('status','unknown')
    if st=='success': ok+=1
    elif st=='failed': fail+=1
    elif st=='running': running+=1
    elif st=='pending': pending+=1
    elif st=='skipped': skipped+=1

    m=meta.get(aid,{})
    t=m.get('type','unknown')
    err=(v.get('lastError') or '').strip()
    attempts=v.get('attempts',0)

    icon={'success':'✅','failed':'❌','skipped':'⏭️','running':'⏳','pending':'🕒'}.get(st,'•')
    item=f"{idx}. `{aid}` · {t} · {icon} {st}"
    if st=='failed' and attempts:
        item += f"（重试{attempts}次"
        if err:
            item += f"，{err[:24]}"
        item += "）"
    rows.append(item)

total=len(states)
remaining=len(pending_actions)

# 清理结果细化
cleaned_total=len(completed)
cleaned_success=sum(1 for aid,v in states.items() if v.get('status')=='success')
cleaned_failed=sum(1 for aid,v in states.items() if v.get('status')=='failed')
cleaned_skipped=sum(1 for aid,v in states.items() if v.get('status')=='skipped')
alerts=cleaned_failed

# 时间优先用已记录值，其次当前时间
time_human=obj.get('currentTimeHuman')
if not time_human:
    time_human=datetime.now().strftime('%Y-%m-%d %H:%M:%S (Asia/Shanghai)')

# 任务清单展示上限
max_items=8
shown=rows[:max_items]
more=max(0,len(rows)-max_items)
list_text='\n'.join(shown) if shown else '无'
if more>0:
    list_text += f'\n{max_items+1}. 其余 **{more}** 项已省略'

msg=(
    "### ✅ 重启成功后通知\n\n"
    "**Gateway 状态**：已恢复\n"
    f"**当前时间**：{time_human}\n"
    f"**任务队列**：总 {total}｜完成 {ok}｜失败 {fail}｜跳过 {skipped}｜执行中 {running}｜待处理 {pending}\n"
    f"**任务清理结果**：已清理 {cleaned_total}（成功 {cleaned_success} / 失败 {cleaned_failed} / 跳过 {cleaned_skipped}）｜保留 {remaining}｜告警 {alerts}\n\n"
    "#### 任务清单（摘要）\n"
    f"{list_text}"
)
print(msg)
PY
}

mark_done_if_complete() {
  local task_id="$1"
  local ok_health ok_resume ok_pre ok_post ok_resume_actions
  ok_health="$(state_get "$task_id" healthOk)"
  ok_resume="$(state_get "$task_id" resumeEventSent)"
  ok_pre="$(state_get "$task_id" notifyPreSent)"
  ok_post="$(state_get "$task_id" notifyPostSent)"
  ok_resume_actions="$(state_get "$task_id" resumeStatus)"

  if ! is_notify_required; then
    ok_pre="true"; ok_post="true"
  fi

  if [ "$ok_health" = "true" ] && [ "$ok_resume" = "true" ] && [ "$ok_pre" = "true" ] && [ "$ok_post" = "true" ] && [ "$ok_resume_actions" = "success" ]; then
    state_update "$task_id" "done" "workflow-complete" '{"lastError":""}'
    return 0
  fi

  state_update "$task_id" "notify-failed" "completion-gate-blocked" "{\"lastError\":\"completion gate blocked: health/resume/notify/resumeActions not satisfied\"}"
  return 1
}

finalize_after_restart() {
  local task_id="$1"

  local restart_completed
  restart_completed="$(state_get "$task_id" restartCompleted)"
  if [ "$restart_completed" != "true" ]; then
    state_update "$task_id" "notify-failed" "finalize-without-restart-complete" '{"lastError":"finalize blocked: restartCompleted!=true"}'
    return 1
  fi

  log "[F1] 重启后健康检查"
  if ! wait_for_health; then
    state_update "$task_id" "health-failed" "health-timeout" '{"healthOk":false,"lastError":"gateway health check timeout"}'
    emit_event "restart-alert:${task_id}:重启后${HEALTH_TIMEOUT_SEC}s内未通过健康检查，请立即排障"
    emit_visible "$task_id" alert "【重启告警】任务 ${task_id} 在 ${HEALTH_TIMEOUT_SEC}s 内健康检查未通过，请执行 openclaw logs / openclaw gateway status 排障。" || true
    return 1
  fi
  state_update "$task_id" "health-ok" "health-check-passed" '{"healthOk":true,"lastError":""}'

  log "[F2] 触发恢复事件"
  if openclaw system event --mode now --text "resume:${task_id}"; then
    state_update "$task_id" "resumed" "resume-event-sent" '{"resumeEventSent":true,"lastError":""}'
  else
    state_update "$task_id" "resumed" "resume-event-failed" '{"resumeEventSent":false,"lastError":"resume event failed"}'
    return 1
  fi

  emit_event "restart-result:${task_id}:重启恢复成功，已触发resume事件"
  if is_notify_required && [ "$NOTIFY_MODE" != "compact" ]; then
    if ! emit_visible "$task_id" post "【重启完成】任务 ${task_id} 已恢复成功，resume 事件已触发。"; then
      state_update "$task_id" "notify-failed" "post-notify-failed" '{"lastError":"post visible notify failed"}'
      return 1
    fi
    state_update "$task_id" "post-notified" "post-notify-finished" '{}'
  fi

  emit_resume_summary "$task_id" post-plan || true

  log "[F3] 执行任务续跑动作"
  if ! run_resume_actions "$task_id"; then
    return 1
  fi

  if is_notify_required && [ "$NOTIFY_MODE" = "compact" ]; then
    local compact_msg
    compact_msg="$(build_compact_post_message "$task_id")"
    if ! emit_visible "$task_id" post "$compact_msg"; then
      state_update "$task_id" "notify-failed" "post-notify-failed:compact" '{"lastError":"post compact notify failed"}'
      return 1
    fi
    state_update "$task_id" "post-notified" "post-notify-finished:compact" '{}'
  fi

  emit_resume_summary "$task_id" post-result || true

  mark_done_if_complete "$task_id"
}

continue_flow() {
  local task_id="$1"
  local file; file="$(state_file "$task_id")"
  [ -f "$file" ] || die "状态文件不存在: $file"

  local phase; phase="$(state_get "$task_id" phase)"
  if [ "$phase" = "done" ]; then
    log "任务已完成，跳过 continue: $task_id"; return 0
  fi

  state_update "$task_id" "restarting" "restart-command-issued" '{"restartIssued":true,"lastError":""}'

  log "[C1] 执行重启: $GATEWAY_RESTART_CMD"
  if ! bash -lc "$GATEWAY_RESTART_CMD"; then
    state_update "$task_id" "restart-failed" "restart-command-failed" '{"restartIssued":true,"restartCompleted":false,"lastError":"restart command failed"}'
    emit_event "restart-alert:${task_id}:重启命令执行失败"
    emit_visible "$task_id" alert "【重启告警】任务 ${task_id} 重启命令执行失败，请排障。" || true
    return 1
  fi

  state_update "$task_id" "restarting" "restart-command-complete" '{"restartCompleted":true,"lastError":""}'
  finalize_after_restart "$task_id"
}

reconcile_one() {
  local task_id="$1"
  local file; file="$(state_file "$task_id")"
  [ -f "$file" ] || return 0

  local phase restart_completed retry
  phase="$(state_get "$task_id" phase)"
  restart_completed="$(state_get "$task_id" restartCompleted)"
  retry="$(state_get "$task_id" resumeRetryCount)"
  [ -n "$retry" ] || retry="0"
  if [ "$retry" != "" ]; then
    retry="$(printf '%s' "$retry" | sed 's/[^0-9].*$//')"
  fi
  [ -n "$retry" ] || retry="0"

  case "$phase" in
    done)
      log "reconcile: $task_id 已完成，跳过"; return 0 ;;
    resumed|post-notified|notify-failed|health-ok|resume-failed|resume-running|resume-queued|resume-done)
      if [ "$retry" -ge "$RECONCILE_MAX_RETRIES" ]; then
        state_update "$task_id" "$phase" "reconcile-escalated" '{"escalationRequired":true,"escalationReason":"retry_exceeded","lastError":"reconcile retry exceeded"}'
        log "reconcile: $task_id 超过重试上限，升级人工处理"
        if is_notify_required; then
          local msg="【重启补偿告警】任务 ${task_id} 已超过补偿重试上限(${RECONCILE_MAX_RETRIES})，请人工介入。"
          local cmd=(openclaw message send --json --channel "$NOTIFY_CHANNEL" --target "$NOTIFY_TARGET" --message "$msg")
          [ -n "$NOTIFY_ACCOUNT" ] && cmd+=(--account "$NOTIFY_ACCOUNT")
          "${cmd[@]}" >/dev/null 2>&1 || true
        fi
        return 1
      fi

      if [ "$retry" -gt 0 ]; then
        local backoff=$((RECONCILE_BACKOFF_SEC * retry))
        log "reconcile: $task_id 退避 ${backoff}s 后重试"
        sleep "$backoff"
      fi

      state_update "$task_id" "$phase" "reconcile-retry" "{\"resumeRetryCount\":$((retry+1))}"

      if [ "$restart_completed" = "true" ]; then
        log "reconcile: 修复后置流程 $task_id (phase=$phase, with restart)"
        finalize_after_restart "$task_id" || true
      else
        log "reconcile: 修复续跑流程 $task_id (phase=$phase, no restart)"
        run_resume_actions "$task_id" || true
      fi
      ;;
    *)
      log "reconcile: $task_id 当前 phase=$phase，不在补偿范围" ;;
  esac
}

reconcile_flow() {
  local only_task_id="${1:-}"
  if [ -n "$only_task_id" ]; then
    reconcile_one "$only_task_id"
    return 0
  fi

  shopt -s nullglob
  local f id
  for f in "$STATE_DIR"/*.json; do
    id="$(basename "$f" .json)"
    reconcile_one "$id"
  done
}

resume_run_only() {
  local task_id="$1"
  local file; file="$(state_file "$task_id")"
  [ -f "$file" ] || die "状态文件不存在: $file"
  run_resume_actions "$task_id"
}

spawn_detached_continue() {
  local task_id="$1"
  local log_file script_abs cwd pid
  log_file="$(runner_log_file "$task_id")"
  script_abs="$(cd "$(dirname "$0")" && pwd)/$(basename "$0")"
  cwd="$(pwd)"

  STATE_DIR="$STATE_DIR" \
  GATEWAY_RESTART_CMD="$GATEWAY_RESTART_CMD" \
  HEALTH_TIMEOUT_SEC="$HEALTH_TIMEOUT_SEC" \
  NOTIFY_CHANNEL="$NOTIFY_CHANNEL" \
  NOTIFY_TARGET="$NOTIFY_TARGET" \
  NOTIFY_ACCOUNT="$NOTIFY_ACCOUNT" \
  nohup bash -lc "cd '$cwd' && '$script_abs' continue --task-id '$task_id'" >"$log_file" 2>&1 < /dev/null &

  pid="$!"
  state_update "$task_id" "restarting" "detached-runner-started" "{\"runnerPid\":\"$pid\",\"runnerLog\":\"$log_file\",\"restartIssued\":true}"
  log "已启动 detached runner: pid=$pid log=$log_file"
}

usage() {
  cat <<'EOF'
OpenClaw restart-safe workflow

Subcommands:
  run         预检 + 落盘 + （默认 detached）重启后续流程
  plan        仅编译 --next 到 TaskPlan(v1)
  validate    校验任务计划 JSON 文件
  continue    detached runner 执行重启 + finalize
  resume-run  仅执行 pendingActions（不重启）
  reconcile   对未闭环任务执行补偿（可指定 --task-id）
  report      输出任务摘要（支持 --verbose 查看动作明细）
  diagnose    输出任务诊断建议
  resume      仅触发恢复事件（手工补偿）
  status      查看任务状态文件

run options:
  --task-id <id>        任务ID（默认 task-YYYYmmdd-HHMMSS）
  --title <text>        任务标题
  --next <text>         重启后下一步（支持 notify:/notify-time[:TZ]/cmd:/script:/json:，可用 ; 串联）
  --criteria <text>     验收标准
  --no-restart          只做预检与落盘，不执行重启
  --inline              不使用 detached runner，内联执行（调试用）
  --notify-channel <c>  可见通知渠道（如 feishu）
  --notify-target <t>   可见通知目标（user:ou_xxx / chat:oc_xxx）
  --notify-account <a>  可见通知账号ID（可选）
  --tasks-file <file>   任务计划文件（validate 必填，run 可选先校验）
  --verbose             report 输出动作级明细

Env:
  RECONCILE_MAX_RETRIES  补偿最大重试次数（默认3）
  RECONCILE_BACKOFF_SEC  补偿退避秒数（默认5）
  ACTION_ALLOWLIST_FILE  命令白名单文件（每行一个前缀）
  NOTIFY_MODE            通知模式：compact(默认2条) | verbose(多条过程通知)

State phases:
  init -> prechecked -> checkpointed -> resume-queued -> restarting -> health-ok -> resumed -> post-notified -> resume-running -> resume-done -> done
  failures: doctor-failed / restart-failed / health-failed / notify-failed / resume-failed
EOF
}

run_flow() {
  local task_id="$1" title="$2" next_action="$3" criteria="$4" do_restart="$5" inline_mode="$6" tasks_file="${7:-}"

  state_init "$task_id" "$title" "$next_action" "$criteria"
  state_bump_attempt "$task_id"
  state_update "$task_id" "init" "run-start" '{}'

  log "[1/4] 预检配置: openclaw doctor --non-interactive"
  if openclaw doctor --non-interactive; then
    state_update "$task_id" "prechecked" "doctor-ok" '{"doctorOk":true,"checkpointed":false,"restartIssued":false,"restartCompleted":false,"healthOk":false,"resumeEventSent":false,"lastError":""}'
  else
    state_update "$task_id" "doctor-failed" "doctor-failed" '{"doctorOk":false,"checkpointed":false,"restartIssued":false,"restartCompleted":false,"healthOk":false,"resumeEventSent":false,"lastError":"doctor check failed"}'
    die "doctor 失败，已阻断重启"
  fi

  log "[2/4] 写入恢复点"
  state_update "$task_id" "checkpointed" "checkpoint-written" '{"checkpointed":true,"lastError":""}'

  log "[3/4] 解析并入队续跑动作"
  if [ -n "$tasks_file" ]; then
    local file_actions action_states_json
    file_actions="$(actions_json_from_tasks_file "$tasks_file")"
    file_actions="$(normalize_actions_for_state "$file_actions")"
    action_states_json="$(action_state_init_json "$file_actions")"
    state_update "$task_id" "resume-queued" "resume-actions-queued:tasks-file" "{\"taskPlanVersion\":\"v1\",\"pendingActions\":$file_actions,\"resumeCompletedActions\":[],\"resumeCursor\":0,\"resumeStatus\":\"idle\",\"resumeError\":\"\",\"resumeRetryCount\":0,\"actionStates\":$action_states_json}"
  else
    if ! queue_resume_actions "$task_id" "$next_action"; then
      return 1
    fi
  fi

  if [ "$do_restart" = "false" ]; then
    log "已按要求跳过重启（--no-restart）"
    return 0
  fi

  log "[4/4] 发送重启前通知并启动重启链路"
  emit_event "restart-notice:${task_id}:即将执行gateway重启，短时可能无回包"
  if is_notify_required; then
    if ! emit_visible "$task_id" pre "【重启通知】任务 ${task_id} 即将重启 OpenClaw Gateway，约 10~30 秒内可能短时无回包。"; then
      state_update "$task_id" "notify-failed" "pre-notify-failed" '{"lastError":"pre visible notify failed"}'
      return 1
    fi
    emit_resume_summary "$task_id" pre || true
  fi

  if [ "$inline_mode" = "true" ]; then
    log "内联执行 continue（--inline）"
    continue_flow "$task_id"
  else
    log "启动 detached continue runner"
    spawn_detached_continue "$task_id"
  fi
}

resume_only() {
  local task_id="$1"
  local file; file="$(state_file "$task_id")"
  [ -f "$file" ] || die "状态文件不存在: $file"
  if openclaw system event --mode now --text "resume:${task_id}"; then
    state_update "$task_id" "resumed" "manual-resume-event-sent" '{"resumeEventSent":true,"lastError":""}'
    log "已发送恢复事件: resume:${task_id}"; return 0
  fi
  state_update "$task_id" "resumed" "manual-resume-event-failed" '{"resumeEventSent":false,"lastError":"manual resume event failed"}'
  die "恢复事件发送失败: resume:${task_id}"
}


report_only() {
  local task_id="$1"; local file; file="$(state_file "$task_id")"
  [ -f "$file" ] || die "状态文件不存在: $file"
  python3 - "$file" "$REPORT_VERBOSE" <<'PY'
import json,sys
obj=json.load(open(sys.argv[1],'r',encoding='utf-8'))
verbose=(sys.argv[2].lower()=='true')
actions=obj.get('actionStates',{}) or {}
stats={'pending':0,'running':0,'success':0,'failed':0,'skipped':0,'unknown':0}
for _,v in actions.items():
    s=v.get('status','unknown')
    stats[s if s in stats else 'unknown']+=1
summary={
 "taskId":obj.get("taskId"),
 "phase":obj.get("phase"),
 "attempt":obj.get("attempt"),
 "healthOk":obj.get("healthOk"),
 "resumeEventSent":obj.get("resumeEventSent"),
 "resumeStatus":obj.get("resumeStatus"),
 "resumeCursor":obj.get("resumeCursor"),
 "pendingCount":len(obj.get("pendingActions",[])),
 "completedCount":len(obj.get("resumeCompletedActions",[])),
 "notifyPreSent":obj.get("notifyPreSent"),
 "notifyPostSent":obj.get("notifyPostSent"),
 "escalationRequired":obj.get("escalationRequired",False),
 "escalationReason":obj.get("escalationReason",""),
 "actionStats":stats
}
if verbose:
    details=[]
    for aid,v in sorted(actions.items()):
        details.append({
          "actionId":aid,
          "status":v.get('status','unknown'),
          "attempts":v.get('attempts',0),
          "lastError":v.get('lastError','')
        })
    summary["actionDetails"]=details
print(json.dumps(summary,ensure_ascii=False,indent=2))
PY
}

diagnose_only() {
  local task_id="$1"; local file; file="$(state_file "$task_id")"
  [ -f "$file" ] || die "状态文件不存在: $file"
  python3 - "$file" <<'PY'
import json,sys
obj=json.load(open(sys.argv[1],'r',encoding='utf-8'))
phase=obj.get('phase','')
issues=[]
suggestions=[]
if not obj.get('doctorOk'):
    issues.append('doctor 未通过')
    suggestions.append('执行 openclaw doctor --non-interactive 并修复告警后重试')
if obj.get('restartIssued') and not obj.get('restartCompleted'):
    issues.append('重启命令未完成')
    suggestions.append('检查 openclaw gateway status 与 systemd 日志')
if obj.get('restartCompleted') and not obj.get('healthOk'):
    issues.append('重启后健康检查未通过')
    suggestions.append('执行 openclaw logs / openclaw health 排障')
if obj.get('healthOk') and not obj.get('resumeEventSent'):
    issues.append('resume 事件未发送')
    suggestions.append('执行 restart-safe.sh resume --task-id <id> 手动补发')
if obj.get('resumeStatus')!='success':
    issues.append('任务续跑未成功')
if obj.get('notifyPreSent') is False:
    issues.append('重启前可见通知未送达')
if obj.get('notifyPostSent') is False:
    issues.append('重启后可见通知未送达')
if phase!='done':
    issues.append(f'当前phase={phase} 未完成')

actions=obj.get('actionStates',{}) or {}
for aid,v in sorted(actions.items()):
    st=v.get('status','unknown')
    if st in ('failed','running','pending'):
        issues.append(f'action[{aid}] 状态={st} attempts={v.get("attempts",0)} err={v.get("lastError","")}')

if obj.get('escalationRequired'):
    issues.append(f"升级告警已触发: {obj.get('escalationReason','unknown')}")

if not issues:
    print('DIAGNOSE: OK (无阻塞问题)')
else:
    print('DIAGNOSE: NEED_ACTION')
    for i,x in enumerate(issues,1):
        print(f'{i}. {x}')
    uniq=[]
    for s in suggestions:
        if s not in uniq:
            uniq.append(s)
    if uniq:
        print('--- 建议动作 ---')
        for i,s in enumerate(uniq,1):
            print(f'{i}. {s}')
PY
}

status_only() {
  local task_id="$1"; local file; file="$(state_file "$task_id")"
  [ -f "$file" ] || die "状态文件不存在: $file"
  cat "$file"
}

main() {
  require_cmd openclaw
  require_cmd python3

  local cmd="${1:-}"; shift || true
  case "$cmd" in
    run|plan|validate|continue|resume-run|reconcile|report|diagnose|resume|status) ;;
    -h|--help|help|"") usage; exit 0 ;;
    *) die "未知子命令: $cmd" ;;
  esac

  local task_id="task-$(date +%Y%m%d-%H%M%S)"
  local task_id_set="false"
  local title="OpenClaw重启事务"
  local next_action="resume-workflow"
  local criteria="workflow completed and reported"
  local do_restart="true"
  local inline_mode="false"
  local tasks_file=""

  while [ "$#" -gt 0 ]; do
    case "$1" in
      --task-id) task_id="${2:-}"; task_id_set="true"; shift 2 ;;
      --title) title="${2:-}"; shift 2 ;;
      --next) next_action="${2:-}"; shift 2 ;;
      --criteria) criteria="${2:-}"; shift 2 ;;
      --no-restart) do_restart="false"; shift ;;
      --inline) inline_mode="true"; shift ;;
      --notify-channel) NOTIFY_CHANNEL="${2:-}"; shift 2 ;;
      --notify-target) NOTIFY_TARGET="${2:-}"; shift 2 ;;
      --notify-account) NOTIFY_ACCOUNT="${2:-}"; shift 2 ;;
      --tasks-file) tasks_file="${2:-}"; shift 2 ;;
      --verbose) REPORT_VERBOSE="true"; shift ;;
      -h|--help) usage; exit 0 ;;
      *) die "未知参数: $1" ;;
    esac
  done

  [ -n "$task_id" ] || die "--task-id 不能为空"

  case "$cmd" in
    run)
      if [ -n "$tasks_file" ]; then
        validate_tasks_file "$tasks_file"
      fi
      run_flow "$task_id" "$title" "$next_action" "$criteria" "$do_restart" "$inline_mode" "$tasks_file" ;;
    plan) plan_only "$task_id" "$next_action" ;;
    validate)
      [ -n "$tasks_file" ] || die "validate 需要 --tasks-file <plan.json>"
      validate_tasks_file "$tasks_file" ;;
    continue) continue_flow "$task_id" ;;
    resume-run) resume_run_only "$task_id" ;;
    reconcile)
      if [ "$task_id_set" = "true" ]; then
        reconcile_flow "$task_id"
      else
        reconcile_flow
      fi ;;
    report) report_only "$task_id" ;;
    diagnose) diagnose_only "$task_id" ;;
    resume) resume_only "$task_id" ;;
    status) status_only "$task_id" ;;
  esac
}

main "$@"
