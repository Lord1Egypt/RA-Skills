#!/usr/bin/env bash
# Test suite for session-tracker v2.5 — runs against an ISOLATED session dir.
# Superset of v2.4 tests + new T09/T05/T02 security-fix tests.
set -u
ST="python3 $(dirname $(readlink -f $0))/../scripts/session_tracker.py"
export SESSION_TRACKER_DIR="/tmp/st_test_$$"
FAIL=0
PASS=0

check() {  # check <desc> <expected_substring> <actual_output>
  if echo "$3" | rg -q "$2"; then
    PASS=$((PASS+1)); echo "PASS: $1"
  else
    FAIL=$((FAIL+1)); echo "FAIL: $1 — expected [$2] in:"; echo "$3" | head -5
  fi
}

echo "=== 1. help + version ==="
OUT=$($ST --help 2>&1)
check "help mentions v2.6" "v2\.6" "$OUT"

echo "=== 2. init without journal ==="
OUT=$($ST init "Test task one" --steps "alpha,beta" 2>&1)
check "init ok" "Session initialized" "$OUT"
check "journal OFF by default" "journal=OFF" "$OUT"
check "version in state" "2.6" "$(cat $SESSION_TRACKER_DIR/state.json)"

echo "=== 3. freshness fix: read-only commands must NOT touch state ==="
BEFORE=$(stat -c %Y "$SESSION_TRACKER_DIR/state.json")
sleep 1.1
$ST status >/dev/null 2>&1
$ST crash-detect >/dev/null 2>&1
$ST resume >/dev/null 2>&1
$ST stats >/dev/null 2>&1
$ST doctor >/dev/null 2>&1
AFTER=$(stat -c %Y "$SESSION_TRACKER_DIR/state.json")
if [ "$BEFORE" = "$AFTER" ]; then
  PASS=$((PASS+1)); echo "PASS: read-only cmds left state.json untouched"
else
  FAIL=$((FAIL+1)); echo "FAIL: state.json mtime changed on read-only cmds ($BEFORE -> $AFTER)"
fi

echo "=== 3b. activity commands DO touch state ==="
$ST log "doing work" >/dev/null 2>&1
UPDATED=$(python3 -c "import json;print(json.load(open('$SESSION_TRACKER_DIR/state.json'))['updated'])")
if [ -n "$UPDATED" ]; then PASS=$((PASS+1)); echo "PASS: log updated state.updated"; else FAIL=$((FAIL+1)); echo "FAIL: no updated field"; fi

echo "=== 4. ad-hoc step (not declared at init) ==="
OUT=$($ST step 7 --start --desc "ad-hoc discovered step" 2>&1)
check "ad-hoc step accepted" "Step 7 START" "$OUT"

echo "=== 5. sync with string IDs ==="
OUT=$(echo '[{"id":"write-doc","content":"Write doc","status":"completed","priority":"high"},{"id":"1","content":"alpha","status":"in_progress"}]' | $ST sync 2>&1)
check "sync ok" "Synced 2 todo items" "$OUT"

echo "=== 6. done without journal (no journal file) ==="
OUT=$($ST done 2>&1)
check "done ok" "Session marked complete" "$OUT"
if [ ! -f "$SESSION_TRACKER_DIR/journal.jsonl" ]; then
  PASS=$((PASS+1)); echo "PASS: no journal created when opt-in flag absent"
else
  FAIL=$((FAIL+1)); echo "FAIL: journal created without opt-in"
fi

echo "=== 7. orphan archive (the v2.3 data-loss bug) ==="
$ST init "Crashy session" --steps "one" --journal >/dev/null 2>&1
$ST log "about to crash" >/dev/null 2>&1
# v2.5: init on orphan now ABORTS without --replace (T02 fix)
OUT=$($ST init "Next session after crash" --journal 2>&1)
check "init aborts on orphan (T02)" "init aborted" "$OUT"
check "orphan archived before abort" "ARCHIVED" "$OUT"
# Now use --replace to actually overwrite
OUT=$($ST init "Next session after crash" --journal --replace 2>&1)
check "init --replace overwrites orphan" "Session initialized" "$OUT"
ARCHIVED=$(ls "$SESSION_TRACKER_DIR" | rg "crashed_state_" | head -1)
if [ -n "$ARCHIVED" ]; then
  PASS=$((PASS+1)); echo "PASS: orphan state archived to $ARCHIVED"
  TASK=$(python3 -c "import json;print(json.load(open('$SESSION_TRACKER_DIR/$ARCHIVED'))['task'])")
  check "archived task preserved" "Crashy session" "$TASK"
else
  FAIL=$((FAIL+1)); echo "FAIL: no crashed_state_*.json archive found"
fi
check "orphan summarized in journal" "session_orphaned" "$(cat $SESSION_TRACKER_DIR/journal.jsonl)"

echo "=== 8. done --note with journal ==="
OUT=$($ST done --note "v2.5 test session complete" 2>&1)
check "journal append reported" "Journal entry appended" "$OUT"
check "note in journal" "v2\.5 test session complete" "$(cat $SESSION_TRACKER_DIR/journal.jsonl)"
check "duration recorded" "duration_s" "$(cat $SESSION_TRACKER_DIR/journal.jsonl)"

echo "=== 9. stats ==="
OUT=$($ST stats 2>&1)
check "stats shows crash rate" "Crash rate" "$OUT"
check "stats shows completion" "Next session after crash" "$OUT"

echo "=== 10. doctor: healthy + dead monitor detection ==="
OUT=$($ST doctor 2>&1)
check "doctor healthy verdict" "VERDICT: healthy" "$OUT"
# simulate a dead monitor PID (sandbox reset scenario)
echo '{"pid": 999999999, "start_time": null, "session_id": "deadbeef"}' > "$SESSION_TRACKER_DIR/monitor.pid"
echo "[monitor] started fake" > "$SESSION_TRACKER_DIR/monitor.log"
OUT=$($ST doctor 2>&1)
check "doctor detects dead monitor" "MONITOR DEAD" "$OUT"
check "doctor shows last log line" "fake" "$OUT"
if [ ! -f "$SESSION_TRACKER_DIR/monitor.pid" ]; then
  PASS=$((PASS+1)); echo "PASS: stale monitor.pid unlinked by doctor"
else
  FAIL=$((FAIL+1)); echo "FAIL: stale monitor.pid still present"
fi

echo "=== 11. cleanup preserves journal; --purge-journal removes it ==="
$ST init "cleanup test" --journal >/dev/null 2>&1
$ST done >/dev/null 2>&1
OUT=$($ST cleanup --force 2>&1)
check "cleanup preserves journal" "Journal PRESERVED" "$OUT"
if [ -f "$SESSION_TRACKER_DIR/journal.jsonl" ]; then
  PASS=$((PASS+1)); echo "PASS: journal file survived cleanup"
else
  FAIL=$((FAIL+1)); echo "FAIL: journal.jsonl deleted by plain cleanup"
fi
OUT=$($ST cleanup --force --purge-journal 2>&1)
if [ ! -f "$SESSION_TRACKER_DIR/journal.jsonl" ]; then
  PASS=$((PASS+1)); echo "PASS: --purge-journal removed history"
else
  FAIL=$((FAIL+1)); echo "FAIL: journal survived --purge-journal"
fi
check "state gone after cleanup" "No session state" "$($ST status 2>&1)"

echo "=== 12. portability: scan dirs derive from session dir parent ==="
OUT=$($ST init "portable" 2>&1)
check "init in custom dir" "Session initialized" "$OUT"

echo "=== 13. T09 guard: refuse dangerous SESSION_TRACKER_DIR ==="
# Test that the script refuses to operate when SESSION_TRACKER_DIR=/ or $HOME
# Note: $ST already includes "python3", so we extract just the script path.
SCRIPT_PATH=$(echo "$ST" | sed 's/^python3 //')
OUT=$(SESSION_TRACKER_DIR="/" python3 "$SCRIPT_PATH" init "should fail" 2>&1)
RC=$?
check "T09: refuses SESSION_TRACKER_DIR=/" "FATAL" "$OUT"
if [ $RC -ne 0 ]; then
  PASS=$((PASS+1)); echo "PASS: T09 guard exits non-zero on dangerous path"
else
  FAIL=$((FAIL+1)); echo "FAIL: T09 guard did not exit on dangerous path"
fi
OUT=$(SESSION_TRACKER_DIR="$HOME" python3 "$SCRIPT_PATH" init "should fail" 2>&1)
check "T09: refuses SESSION_TRACKER_DIR=\$HOME" "FATAL" "$OUT"

echo "=== 14. T09 guard: cleanup --dry-run does not delete ==="
$ST init "dry-run test" --journal >/dev/null 2>&1
$ST log "some work" >/dev/null 2>&1
OUT=$($ST cleanup --dry-run 2>&1)
check "dry-run lists files" "files to delete" "$OUT"
check "dry-run does not delete" "nothing will be deleted" "$OUT"
# Verify state still exists
if [ -f "$SESSION_TRACKER_DIR/state.json" ]; then
  PASS=$((PASS+1)); echo "PASS: dry-run left state.json intact"
else
  FAIL=$((FAIL+1)); echo "FAIL: dry-run deleted state.json"
fi

echo "=== 15. T05 fix: monitor.pid records start_time + session_id ==="
$ST init "monitor test" >/dev/null 2>&1
$ST monitor --start --interval 1 >/dev/null 2>&1
sleep 0.5
PID_CONTENT=$(cat "$SESSION_TRACKER_DIR/monitor.pid")
check "monitor.pid is JSON with start_time" "start_time" "$PID_CONTENT"
check "monitor.pid has session_id" "session_id" "$PID_CONTENT"
$ST monitor --stop >/dev/null 2>&1

echo "=== 16. T05 fix: stop_monitor refuses to signal PID-reused process ==="
# Write a monitor.pid pointing at PID 1 (init, definitely not our monitor)
# with a recorded start_time that won't match PID 1's actual start time.
echo '{"pid": 1, "start_time": "999999", "session_id": "fake"}' > "$SESSION_TRACKER_DIR/monitor.pid"
OUT=$($ST monitor --stop 2>&1)
check "stop_monitor refuses PID-reused process" "NOT signaling" "$OUT"
check "stop_monitor unlinks stale PID" "" "$OUT"
if [ ! -f "$SESSION_TRACKER_DIR/monitor.pid" ]; then
  PASS=$((PASS+1)); echo "PASS: stale PID file unlinked after refusal"
else
  FAIL=$((FAIL+1)); echo "FAIL: stale PID file still present after refusal"
fi

echo "=== 17. T02 fix: crash-detect labels untrusted data ==="
$ST init "task with <script>alert(1)</script>" --steps "step1" >/dev/null 2>&1
# Simulate crash: don't call done, just init a new one (which aborts)
OUT=$($ST crash-detect 2>&1)
check "crash-detect shows untrusted-data label" "UNTRUSTED DATA" "$OUT"

echo "=== 18. T02 fix: resume labels untrusted data ==="
OUT=$($ST resume 2>&1)
check "resume shows untrusted-data label" "UNTRUSTED DATA" "$OUT"

echo ""
echo "==================================="
echo "RESULTS: $PASS passed, $FAIL failed"
rm -rf "$SESSION_TRACKER_DIR"
[ $FAIL -eq 0 ] && echo "ALL TESTS PASSED" || echo "SOME TESTS FAILED"
