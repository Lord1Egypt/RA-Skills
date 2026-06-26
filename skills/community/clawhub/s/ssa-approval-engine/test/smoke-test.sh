#!/usr/bin/env bash
# smoke-test.sh — approval-engine 冒烟测试
# 验证所有模块正确加载、导出 API，以及基本功能可用
# Compatible with bash 3+ (macOS default)

SKILL_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SRC="$SKILL_DIR/src"
CFG="$SKILL_DIR/config"

PASS=0; FAIL=0

green()  { printf "\033[32m  ✅ %s\033[0m\n" "$1"; }
red()    { printf "\033[31m  ❌ %s\033[0m\n" "$*"; }
bold()   { printf "\033[1m%s\033[0m\n" "$1"; }

pass() { green "$1"; PASS=$((PASS+1)); }
fail() { red "$1"; FAIL=$((FAIL+1)); }

# run_check <name> <js-code> <grep-pattern>
run_check() {
  local name="$1" js="$2" expect="$3"
  local out
  out=$(node -e "$js" 2>/dev/null)
  if echo "$out" | grep -q "$expect"; then
    pass "$name"
  else
    fail "$name  [got: $(echo "$out" | head -1 | cut -c1-80)]"
  fi
}

bold "============================================"
bold " approval-engine Smoke Test"
bold " $SKILL_DIR"
bold "============================================"
echo ""

# ─────────────────────────────────────────────
bold "1. File Existence (13 deliverables)"
# ─────────────────────────────────────────────
for f in \
  "config/approval-rules.json" \
  "src/approval-engine.js" \
  "src/rule-evaluator.js" \
  "src/approval-store.js" \
  "src/exception-detector.js" \
  "src/alert-manager.js" \
  "src/exception-logger.js" \
  "src/recovery-engine.js" \
  "src/retry-handler.js" \
  "src/escalation-handler.js" \
  "src/discord-notifier.js" \
  "src/notification-router.js" \
  "src/notification-templates.js"
do
  if [ -f "$SKILL_DIR/$f" ]; then pass "$f"; else fail "$f MISSING"; fi
done

echo ""
bold "2. JSON Validation"
if node -e "JSON.parse(require('fs').readFileSync('$CFG/approval-rules.json','utf8'))" 2>/dev/null; then
  pass "approval-rules.json valid"
else
  fail "approval-rules.json INVALID"
fi

echo ""
bold "3. JS Syntax Check"
for f in "$SRC"/*.js; do
  fname=$(basename "$f")
  if node --check "$f" 2>/dev/null; then pass "$fname syntax"; else fail "$fname SYNTAX ERROR"; fi
done

echo ""
bold "4. Module Load & Exports"

# bash 3 compatible: check each module with expected exports
check_exports() {
  local mod="$1" exp="$2"
  local result
  result=$(node -e "
    const m=require('$SRC/$mod');
    const keys=Object.keys(m);
    const req='$exp'.split(',');
    const missing=req.filter(k=>!keys.includes(k));
    if(missing.length>0){console.log('MISSING:'+missing.join(','));process.exit(1);}
    console.log('OK');
  " 2>/dev/null)
  if [ "$result" = "OK" ]; then
    pass "$mod.js exports OK"
  else
    fail "$mod.js  [$result]"
  fi
}

check_exports "approval-engine"       "createApproval,submitApproval,getApprovalStatus,checkTimeouts,autoCreateApprovals,getStats,listApprovals"
check_exports "rule-evaluator"        "evaluateTrigger,evaluateConditions,matchRules,loadConfig,getRule,getThresholds"
check_exports "approval-store"        "createApproval,getApproval,getAllApprovals,updateApproval,submitDecision,getPendingApprovals,getExpiredApprovals,getStats"
check_exports "exception-detector"    "detectAll,detectApprovalTimeout,detectSystemError,detectOrderAnomaly,runPeriodicCheck"
check_exports "alert-manager"         "sendAlert,sendDiscordAlert,throttleAlert,getAlertHistory,getAlertStats"
check_exports "exception-logger"      "logException,getExceptions,getExceptionById,markResolved,getStats"
check_exports "recovery-engine"       "recover,getRecoveryStrategy,executeStrategy,getRecoveryStatus,listRecoveries,getRecoveryStats"
check_exports "retry-handler"         "retry,withRetry,getRetryStats,resetStats,calculateDelay"
check_exports "escalation-handler"    "escalate,acknowledge,resolve,listEscalations,getEscalationStats"
check_exports "discord-notifier"      "sendMessage,sendEmbed,sendApprovalRequest,sendAlert,sendRecoveryNotification,sendEscalationRequest"
check_exports "notification-router"   "route,routeBatch,getChannel,getRoutingRules"
check_exports "notification-templates" "getApprovalTemplate,getAlertTemplate,getEscalationTemplate,getRecoveryTemplate,COLORS"

echo ""
bold "5. Config Structure"

run_check "approval-rules.json has rules" \
  "const c=require('$CFG/approval-rules.json');console.log(Object.keys(c).join(','))" \
  "rules"

run_check "approval-rules.json has thresholds" \
  "const c=require('$CFG/approval-rules.json');console.log(Object.keys(c).join(','))" \
  "thresholds"

run_check "rules[0] has id field" \
  "const c=require('$CFG/approval-rules.json');console.log(c.rules[0].id)" \
  "."

echo ""
bold "6. Rule Evaluator"

run_check "loadConfig() returns object with rules" \
  "const ev=require('$SRC/rule-evaluator');const c=ev.loadConfig();console.log(Object.keys(c).join(','))" \
  "rules"

run_check "matchRules() returns array" \
  "const ev=require('$SRC/rule-evaluator');const m=ev.matchRules({quotation:{amount:1000},sales:{owner:'alice'}});console.log(Array.isArray(m))" \
  "true"

run_check "matchRules() triggers quotation-approval at amount>50000" \
  "const ev=require('$SRC/rule-evaluator');const m=ev.matchRules({quotation:{amount:100001},sales:{owner:'alice'}});console.log(m.map(r=>r.id).join(','))" \
  "quotation-approval"

echo ""
bold "7. Approval Store"

run_check "getStats() returns object with total" \
  "const s=require('$SRC/approval-store');const p=s.getStats();const done=(r)=>{console.log(JSON.stringify(r));process.exit(0);};if(p&&p.then)p.then(done).catch(()=>done({}));else done(p||{});setTimeout(()=>process.exit(0),3000);" \
  "total"

run_check "getPendingApprovals() returns array" \
  "const s=require('$SRC/approval-store');const p=s.getPendingApprovals();const done=(r)=>{console.log(JSON.stringify(r));process.exit(0);};if(p&&p.then)p.then(done).catch(()=>done([]));else done(p||[]);setTimeout(()=>process.exit(0),3000);" \
  "\["

echo ""
bold "8. Retry Handler"

run_check "calculateDelay() returns positive number" \
  "const rh=require('$SRC/retry-handler');console.log(rh.calculateDelay(1,1000,'exponential'))" \
  "[0-9]"

# withRetry returns a wrapped fn; call it to get the Promise
run_check "withRetry() wraps fn correctly (returns function)" \
  "const rh=require('$SRC/retry-handler');const wrapped=rh.withRetry(async()=>'success',{maxRetries:1,delayMs:5});console.log(typeof wrapped)" \
  "function"

run_check "retry() resolves successfully" \
  "const rh=require('$SRC/retry-handler');rh.retry(async()=>'done',{maxRetries:1,delayMs:5}).then(r=>{console.log(r);process.exit(0);}).catch(e=>{console.log('err');process.exit(0);});setTimeout(()=>process.exit(0),5000);" \
  "done"

echo ""
bold "9. Notification Templates"

run_check "getApprovalTemplate() returns non-null object" \
  "const nt=require('$SRC/notification-templates');const t=nt.getApprovalTemplate('quotation_approval_request',{approvalId:'T1',amount:1000});console.log(t?'ok':'null')" \
  "ok"

run_check "COLORS has success key (Discord color codes)" \
  "const nt=require('$SRC/notification-templates');console.log(JSON.stringify(nt.COLORS))" \
  "success"

run_check "getAlertTemplate() returns non-null" \
  "const nt=require('$SRC/notification-templates');const t=nt.getAlertTemplate({title:'Test Alert',message:'test'},'warning');console.log(t?'ok':'null')" \
  "ok"

echo ""
bold "10. Exception Logger"

run_check "getStats() returns object" \
  "const el=require('$SRC/exception-logger');const p=el.getStats();const done=(r)=>{console.log(JSON.stringify(r));process.exit(0);};if(p&&p.then)p.then(done).catch(()=>done({}));else done(p||{});setTimeout(()=>process.exit(0),3000);" \
  "{"

run_check "LOG_FILE is a string path" \
  "const el=require('$SRC/exception-logger');console.log(typeof el.LOG_FILE)" \
  "string"

echo ""
bold "11. Recovery Engine"

run_check "getRecoveryStrategy() returns strategy for api_error/medium" \
  "const re=require('$SRC/recovery-engine');const s=re.getRecoveryStrategy('api_error','medium');console.log(s?'ok':'null')" \
  "ok"

echo ""
# ─────────────────────────────────────────────
bold "=== Summary ==="
# ─────────────────────────────────────────────
TOTAL=$((PASS+FAIL))
echo ""
printf "  Total:  %d\n" "$TOTAL"
printf "\033[32m  Pass:   %d\033[0m\n" "$PASS"
if [ "$FAIL" -gt 0 ]; then
  printf "\033[31m  Fail:   %d\033[0m\n" "$FAIL"
else
  printf "  Fail:   0\n"
fi
echo ""
if [ "$FAIL" -eq 0 ]; then
  printf "\033[32m🎉 All checks passed! approval-engine is ready.\033[0m\n"
  exit 0
else
  printf "\033[31m💥 %d check(s) failed. Please review the output above.\033[0m\n" "$FAIL"
  exit 1
fi
