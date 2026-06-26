#!/usr/bin/env bash
set -euo pipefail

# 一键验收：OpenClaw 重启安全流程（Sprint4）
# 覆盖：状态机、真实重启、任务续跑、补偿重试、report/diagnose

WITH_RESTART="false"
TASK_PREFIX="accept-$(date +%Y%m%d-%H%M%S)"
STATE_DIR="${STATE_DIR:-./state/restart}"
REPORT_FILE=""
NOTIFY_CHANNEL="${NOTIFY_CHANNEL:-}"
NOTIFY_TARGET="${NOTIFY_TARGET:-}"
NOTIFY_ACCOUNT="${NOTIFY_ACCOUNT:-}"
NOTIFY_MODE="${NOTIFY_MODE:-compact}"
INTERNAL_RUN="false"
DETACH_ON_RESTART="true"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SAFE_SCRIPT="${SCRIPT_DIR}/restart-safe.sh"
ALLOWLIST_FILE="${SCRIPT_DIR}/../config-action-allowlist.txt"

while [ "$#" -gt 0 ]; do
  case "$1" in
    --with-restart) WITH_RESTART="true"; shift ;;
    --task-prefix) TASK_PREFIX="${2:-}"; shift 2 ;;
    --report-file) REPORT_FILE="${2:-}"; shift 2 ;;
    --notify-channel) NOTIFY_CHANNEL="${2:-}"; shift 2 ;;
    --notify-target) NOTIFY_TARGET="${2:-}"; shift 2 ;;
    --notify-account) NOTIFY_ACCOUNT="${2:-}"; shift 2 ;;
    --notify-mode) NOTIFY_MODE="${2:-compact}"; shift 2 ;;
    --internal-run) INTERNAL_RUN="true"; shift ;;
    --no-detach) DETACH_ON_RESTART="false"; shift ;;
    -h|--help)
      cat <<'EOF'
用法：
  skills/restart-safe-workflow/scripts/restart-acceptance.sh [--with-restart]
      [--task-prefix <prefix>] [--report-file <path>]
      [--notify-channel <c> --notify-target <t> [--notify-account <a>]]
      [--notify-mode compact|verbose]
      [--internal-run] [--no-detach]
EOF
      exit 0 ;;
    *) echo "未知参数: $1" >&2; exit 2 ;;
  esac
done

[ -n "$REPORT_FILE" ] || REPORT_FILE="./state/restart/acceptance-${TASK_PREFIX}.log"
mkdir -p "$(dirname "$REPORT_FILE")" "$STATE_DIR"
: > "$REPORT_FILE"

# 自守护模式：当启用真实重启时，默认先自我detached，避免调用会话在重启中断
if [ "$WITH_RESTART" = "true" ] && [ "$DETACH_ON_RESTART" = "true" ] && [ "$INTERNAL_RUN" != "true" ]; then
  SELF_LOG="${STATE_DIR}/acceptance-${TASK_PREFIX}.runner.log"
  nohup bash -lc "cd '$(pwd)' && '$0' --with-restart --task-prefix '$TASK_PREFIX' --report-file '$REPORT_FILE' --internal-run --notify-mode '$NOTIFY_MODE' ${NOTIFY_CHANNEL:+--notify-channel '$NOTIFY_CHANNEL'} ${NOTIFY_TARGET:+--notify-target '$NOTIFY_TARGET'} ${NOTIFY_ACCOUNT:+--notify-account '$NOTIFY_ACCOUNT'}" >"$SELF_LOG" 2>&1 < /dev/null &
  echo "[DETACHED] acceptance runner started: pid=$! log=$SELF_LOG report=$REPORT_FILE"
  exit 0
fi

PASS_CNT=0
FAIL_CNT=0
log() { echo "[$(date '+%Y-%m-%d %H:%M:%S%z')] $*" | tee -a "$REPORT_FILE"; }
pass() { PASS_CNT=$((PASS_CNT+1)); log "PASS | $*"; }
fail() { FAIL_CNT=$((FAIL_CNT+1)); log "FAIL | $*"; }
require_cmd(){ command -v "$1" >/dev/null 2>&1 || { log "缺少命令: $1"; exit 2; }; }

json_get() {
  local file="$1" key="$2"
  python3 - "$file" "$key" <<'PY'
import json,sys
f,k=sys.argv[1:]
with open(f,'r',encoding='utf-8') as fh: obj=json.load(fh)
cur=obj
for p in k.split('.'):
    if isinstance(cur,dict) and p in cur: cur=cur[p]
    else: print(''); raise SystemExit(0)
if isinstance(cur,bool): print('true' if cur else 'false')
elif cur is None: print('')
else: print(cur)
PY
}

require_cmd openclaw
require_cmd python3
require_cmd bash
[ -x "$SAFE_SCRIPT" ] || { log "未找到可执行脚本: $SAFE_SCRIPT"; exit 2; }

TASK_MAIN="${TASK_PREFIX}-main"
TASK_GATE="${TASK_PREFIX}-gate"
TASK_RESTART="${TASK_PREFIX}-restart"
TASK_RETRY="${TASK_PREFIX}-retry"
STATE_MAIN="${STATE_DIR}/${TASK_MAIN}.json"
STATE_GATE="${STATE_DIR}/${TASK_GATE}.json"
STATE_RESTART="${STATE_DIR}/${TASK_RESTART}.json"
STATE_RETRY="${STATE_DIR}/${TASK_RETRY}.json"
RUNNER_LOG="${STATE_DIR}/${TASK_RESTART}.runner.log"

NOTIFY_ARGS=()
if [ -n "$NOTIFY_CHANNEL" ] && [ -n "$NOTIFY_TARGET" ]; then
  NOTIFY_ARGS+=(--notify-channel "$NOTIFY_CHANNEL" --notify-target "$NOTIFY_TARGET")
  [ -n "$NOTIFY_ACCOUNT" ] && NOTIFY_ARGS+=(--notify-account "$NOTIFY_ACCOUNT")
  log "notify configured: channel=$NOTIFY_CHANNEL target=$NOTIFY_TARGET account=${NOTIFY_ACCOUNT:-<default>}"
else
  log "notify not configured: skip visible-ack assertion"
fi

log "=== OpenClaw 重启流程一键验收开始 ==="
log "task_prefix=${TASK_PREFIX}"
log "with_restart=${WITH_RESTART}"
log "notify_mode=${NOTIFY_MODE}"
log "report=${REPORT_FILE}"

# TC0: Phase1 计划编译/校验
if "$SAFE_SCRIPT" plan --task-id "${TASK_PREFIX}-plan" --next "notify:验收;notify-time" >/tmp/restart-accept-plan.out 2>&1; then
  if grep -q '"taskPlanVersion": "v1"' /tmp/restart-accept-plan.out; then
    pass "TC0 plan 输出 TaskPlan(v1)"
  else
    fail "TC0 plan 输出缺少 taskPlanVersion"
  fi
else
  fail "TC0 plan 执行失败"
fi

if "$SAFE_SCRIPT" validate --tasks-file "${SCRIPT_DIR}/../examples/plan-valid.json" >/tmp/restart-accept-validate-ok.out 2>&1; then
  pass "TC0.1 validate(valid) 通过"
else
  fail "TC0.1 validate(valid) 失败"
fi

if "$SAFE_SCRIPT" validate --tasks-file "${SCRIPT_DIR}/../examples/plan-invalid.json" >/tmp/restart-accept-validate-bad.out 2>&1; then
  fail "TC0.2 validate(invalid) 应失败但成功"
else
  pass "TC0.2 validate(invalid) 正确失败"
fi

if openclaw doctor --non-interactive >/tmp/restart-accept-doctor.out 2>&1; then
  pass "TC1 doctor --non-interactive 可执行"
else
  fail "TC1 doctor --non-interactive 失败（请先修复配置）"
fi

TMPDIR_SHIM="$(mktemp -d)"
REAL_OPENCLAW="$(command -v openclaw)"
mkdir -p "$TMPDIR_SHIM/bin"
cat > "$TMPDIR_SHIM/bin/openclaw" <<EOF
#!/usr/bin/env bash
if [ "\${1:-}" = "doctor" ] && [ "\${2:-}" = "--non-interactive" ]; then
  echo "shim: force doctor failure" >&2
  exit 99
fi
exec "$REAL_OPENCLAW" "\$@"
EOF
chmod +x "$TMPDIR_SHIM/bin/openclaw"

rm -f "$STATE_GATE"
if PATH="$TMPDIR_SHIM/bin:$PATH" "$SAFE_SCRIPT" run --task-id "$TASK_GATE" --no-restart >/tmp/restart-accept-gate.out 2>&1; then
  fail "TC2 doctor失败阻断未生效（流程不应成功）"
else
  if [ -f "$STATE_GATE" ] && [ "$(json_get "$STATE_GATE" phase)" = "doctor-failed" ] && [ "$(json_get "$STATE_GATE" doctorOk)" = "false" ]; then
    pass "TC2 doctor失败可阻断重启，且写入失败态 phase=doctor-failed"
  else
    fail "TC2 doctor失败后状态不符合预期"
  fi
fi
rm -rf "$TMPDIR_SHIM"

rm -f "$STATE_MAIN"
if ACTION_ALLOWLIST_FILE="$ALLOWLIST_FILE" "$SAFE_SCRIPT" run --task-id "$TASK_MAIN" --next "cmd:echo sprint4-resume-ok" --criteria "看到续跑证据" --no-restart >/tmp/restart-accept-main.out 2>&1; then
  if [ -f "$STATE_MAIN" ] && [ "$(json_get "$STATE_MAIN" phase)" = "resume-queued" ]; then
    pass "TC3 no-restart 可落盘且 phase=resume-queued"
  else
    fail "TC3 状态文件缺失或 phase 非 resume-queued"
  fi
else
  fail "TC3 run --no-restart 执行失败"
fi

if ACTION_ALLOWLIST_FILE="$ALLOWLIST_FILE" "$SAFE_SCRIPT" resume-run --task-id "$TASK_MAIN" >/tmp/restart-accept-resumerun.out 2>&1; then
  if [ "$(json_get "$STATE_MAIN" resumeStatus)" = "success" ] && [ "$(json_get "$STATE_MAIN" phase)" = "resume-done" ]; then
    pass "TC4 resume-run 成功且 resumeStatus=success"
  else
    fail "TC4 resume-run 后状态异常"
  fi
else
  fail "TC4 resume-run 执行失败"
fi

if ACTION_ALLOWLIST_FILE="$ALLOWLIST_FILE" "$SAFE_SCRIPT" report --task-id "$TASK_MAIN" >/tmp/restart-accept-report.out 2>&1; then
  grep -q '"pendingCount"' /tmp/restart-accept-report.out && pass "TC5 report 输出摘要成功" || fail "TC5 report 输出缺少关键字段"
else
  fail "TC5 report 执行失败"
fi

if ACTION_ALLOWLIST_FILE="$ALLOWLIST_FILE" "$SAFE_SCRIPT" report --task-id "$TASK_MAIN" --verbose >/tmp/restart-accept-report-verbose.out 2>&1; then
  if grep -q '"actionDetails"' /tmp/restart-accept-report-verbose.out && grep -q '"actionStats"' /tmp/restart-accept-report-verbose.out; then
    pass "TC5.1 report --verbose 输出动作级明细"
  else
    fail "TC5.1 report --verbose 缺少 actionDetails/actionStats"
  fi
else
  fail "TC5.1 report --verbose 执行失败"
fi

if ACTION_ALLOWLIST_FILE="$ALLOWLIST_FILE" "$SAFE_SCRIPT" diagnose --task-id "$TASK_MAIN" >/tmp/restart-accept-diagnose.out 2>&1; then
  grep -q 'DIAGNOSE:' /tmp/restart-accept-diagnose.out && pass "TC6 diagnose 输出成功" || fail "TC6 diagnose 输出异常"
else
  fail "TC6 diagnose 执行失败"
fi

if [ "$WITH_RESTART" = "true" ]; then
  rm -f "$STATE_RESTART" "$RUNNER_LOG"
  if NOTIFY_MODE="$NOTIFY_MODE" ACTION_ALLOWLIST_FILE="$ALLOWLIST_FILE" "$SAFE_SCRIPT" run --task-id "$TASK_RESTART" --next "notify:重启后自动续跑动作" --criteria "真实重启+续跑完成" "${NOTIFY_ARGS[@]}" >/tmp/restart-accept-real.out 2>&1; then
    pass "TC7 run 启动成功（detached）"
  else
    fail "TC7 run 启动失败"
  fi

  ok="false"
  for _ in $(seq 1 120); do
    if [ -f "$STATE_RESTART" ]; then
      ph="$(json_get "$STATE_RESTART" phase)"
      if [ "$ph" = "done" ]; then ok="true"; break; fi
      if [ "$ph" = "restart-failed" ] || [ "$ph" = "health-failed" ] || [ "$ph" = "notify-failed" ] || [ "$ph" = "resume-failed" ]; then break; fi
    fi
    sleep 2
  done

  if [ "$ok" = "true" ]; then
    if [ "$(json_get "$STATE_RESTART" healthOk)" = "true" ] && [ "$(json_get "$STATE_RESTART" resumeEventSent)" = "true" ] && [ "$(json_get "$STATE_RESTART" resumeStatus)" = "success" ]; then
      if [ -n "$NOTIFY_CHANNEL" ] && [ -n "$NOTIFY_TARGET" ]; then
        if [ "$(json_get "$STATE_RESTART" notifyPreSent)" = "true" ] && [ "$(json_get "$STATE_RESTART" notifyPostSent)" = "true" ]; then
          if [ "$NOTIFY_MODE" = "compact" ]; then
            vis_count="$(python3 - <<'PY' "$STATE_RESTART"
import json,sys
obj=json.load(open(sys.argv[1],'r',encoding='utf-8'))
notes=[t.get('note','') for t in obj.get('timeline',[])]
print(sum(1 for n in notes if n.startswith('visible-notify:')))
PY
)"
            if [ "$vis_count" = "2" ]; then
              pass "TC8 真实重启 + 通知(2条制) + 续跑全通过"
            else
              fail "TC8 通知条数不符合compact预期(实际=${vis_count}, 预期=2)"
            fi
          else
            pass "TC8 真实重启 + 通知 + 续跑全通过"
          fi
        else
          fail "TC8 真实重启通过，但通知字段不完整"
        fi
      else
        pass "TC8 真实重启+续跑通过（无通知断言）"
      fi
    else
      fail "TC8 真实重启链路未满足 health/resume/resumeStatus"
    fi
  else
    fail "TC8 真实重启未收敛到 done"
    [ -f "$RUNNER_LOG" ] && tail -n 120 "$RUNNER_LOG" | tee -a "$REPORT_FILE" >/dev/null || true
  fi

  # TC9: 注入失败并验证重试升级
  rm -f "$STATE_RETRY"
  if ACTION_ALLOWLIST_FILE="$ALLOWLIST_FILE" "$SAFE_SCRIPT" run --task-id "$TASK_RETRY" --next "cmd:forbidden_command_should_fail" --no-restart >/tmp/restart-accept-retry-run.out 2>&1; then
    if ACTION_ALLOWLIST_FILE="$ALLOWLIST_FILE" "$SAFE_SCRIPT" resume-run --task-id "$TASK_RETRY" >/tmp/restart-accept-retry-resume.out 2>&1; then
      fail "TC9 预期续跑失败但实际成功"
    else
      [ "$(json_get "$STATE_RETRY" phase)" = "resume-failed" ] && pass "TC9 续跑失败注入成功" || fail "TC9 续跑失败后phase异常"
    fi
  else
    fail "TC9 前置run失败"
  fi

  if RECONCILE_MAX_RETRIES=1 ACTION_ALLOWLIST_FILE="$ALLOWLIST_FILE" "$SAFE_SCRIPT" reconcile --task-id "$TASK_RETRY" >/tmp/restart-accept-retry-reconcile.out 2>&1; then
    if [ "$(json_get "$STATE_RETRY" escalationRequired)" = "true" ] || [ "$(json_get "$STATE_RETRY" phase)" = "resume-failed" ] || [ "$(json_get "$STATE_RETRY" phase)" = "notify-failed" ]; then
      pass "TC10 reconcile 重试策略生效"
    else
      fail "TC10 reconcile 重试策略未生效"
    fi
  else
    # reconcile 可能返回非0，但状态落盘可视为策略触发
    if [ "$(json_get "$STATE_RETRY" escalationRequired)" = "true" ]; then
      pass "TC10 reconcile 升级策略触发（返回非0）"
    else
      fail "TC10 reconcile 执行失败且无升级状态"
    fi
  fi
else
  log "SKIP | TC7~TC10 真实重启/补偿链路（使用 --with-restart 开启）"
fi

log "=== 验收结束：PASS=${PASS_CNT}, FAIL=${FAIL_CNT} ==="
if [ "$FAIL_CNT" -gt 0 ]; then log "结果：FAIL"; exit 1; fi
log "结果：PASS"; exit 0
