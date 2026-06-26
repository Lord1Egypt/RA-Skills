#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SCRIPT="$ROOT_DIR/scripts/recovery-watchdog.sh"

pass() { printf '[PASS] %s\n' "$1"; }
fail() { printf '[FAIL] %s\n' "$1" >&2; exit 1; }

assert_contains() {
  local needle="$1" file="$2" msg="$3"
  grep -F "$needle" "$file" >/dev/null 2>&1 || fail "$msg"
}

assert_not_contains() {
  local needle="$1" file="$2" msg="$3"
  if grep -F "$needle" "$file" >/dev/null 2>&1; then
    fail "$msg"
  fi
}

make_mock_openclaw() {
  local mock_bin_dir="$1"
  cat > "$mock_bin_dir/openclaw" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

MOCK_DIR="${MOCK_DIR:?MOCK_DIR required}"
printf '%s\n' "$*" >> "$MOCK_DIR/commands.log"

if [[ "${1:-}" == "gateway" && "${2:-}" == "status" ]]; then
  count_file="$MOCK_DIR/status_count"
  count=0
  [[ -f "$count_file" ]] && count="$(cat "$count_file")"
  count=$((count + 1))
  printf '%s\n' "$count" > "$count_file"

  line="$(sed -n "${count}p" "$MOCK_DIR/status_plan.txt" 2>/dev/null || true)"
  if [[ -z "$line" ]]; then
    line="$(tail -n 1 "$MOCK_DIR/status_plan.txt" 2>/dev/null || true)"
  fi
  rc="${line%%|*}"
  out="${line#*|}"
  printf '%s\n' "$out"
  exit "${rc:-1}"
fi

if [[ "${1:-}" == "gateway" && "${2:-}" == "install" ]]; then
  install_count_file="$MOCK_DIR/install_count"
  install_count=0
  [[ -f "$install_count_file" ]] && install_count="$(cat "$install_count_file")"
  install_count=$((install_count + 1))
  printf '%s\n' "$install_count" > "$install_count_file"
  rc="$(cat "$MOCK_DIR/install_rc" 2>/dev/null || echo 0)"
  printf 'mock install rc=%s\n' "$rc"
  exit "$rc"
fi

echo "unexpected command: $*" >&2
exit 99
EOF
  chmod +x "$mock_bin_dir/openclaw"
}

run_case_healthy_skips_recovery() {
  local tdir mock_bin log_file cmd_file
  tdir="$(mktemp -d)"
  mock_bin="$tdir/mockbin"
  mkdir -p "$mock_bin"
  make_mock_openclaw "$mock_bin"

  export MOCK_DIR="$tdir"
  export PATH="$mock_bin:$PATH"
  export WATCHDOG_SKIP_SLEEP=1
  printf '0|Gateway is running and healthy\n' > "$tdir/status_plan.txt"
  printf '0\n' > "$tdir/install_rc"
  log_file="$tdir/watchdog.log"

  bash "$SCRIPT" \
    --log-file "$log_file" \
    --grace-seconds 1 \
    --status-retries 1 \
    --recovery-retries 1 \
    --status-interval-seconds 1 \
    --recovery-interval-seconds 1 \
    --max-runtime-seconds 60

  cmd_file="$tdir/commands.log"
  assert_contains "gateway status" "$cmd_file" "healthy case should check gateway status"
  assert_not_contains "gateway install" "$cmd_file" "healthy case should not run gateway install"
  assert_contains "result=healthy_no_recovery_needed" "$log_file" "healthy case should log no recovery result"
  pass "healthy status skips recovery"
}

run_case_unhealthy_runs_recovery() {
  local tdir mock_bin log_file cmd_file
  tdir="$(mktemp -d)"
  mock_bin="$tdir/mockbin"
  mkdir -p "$mock_bin"
  make_mock_openclaw "$mock_bin"

  export MOCK_DIR="$tdir"
  export PATH="$mock_bin:$PATH"
  export WATCHDOG_SKIP_SLEEP=1
  printf '1|Gateway not running\n1|Gateway not running\n0|Gateway is healthy and running\n' > "$tdir/status_plan.txt"
  printf '0\n' > "$tdir/install_rc"
  log_file="$tdir/watchdog.log"

  bash "$SCRIPT" \
    --log-file "$log_file" \
    --grace-seconds 1 \
    --status-retries 1 \
    --recovery-retries 2 \
    --status-interval-seconds 1 \
    --recovery-interval-seconds 1 \
    --max-runtime-seconds 60

  cmd_file="$tdir/commands.log"
  assert_contains "gateway install" "$cmd_file" "unhealthy case should run gateway install"
  assert_contains "status_rc=1" "$log_file" "unhealthy case should preserve non-zero status return codes"
  assert_contains "result=recovered" "$log_file" "unhealthy case should recover"
  pass "unhealthy status triggers bounded recovery"
}

run_case_uses_mock_binary_only() {
  local tdir mock_bin cmd_file
  tdir="$(mktemp -d)"
  mock_bin="$tdir/mockbin"
  mkdir -p "$mock_bin"
  make_mock_openclaw "$mock_bin"

  export MOCK_DIR="$tdir"
  export PATH="$mock_bin:$PATH"
  export WATCHDOG_SKIP_SLEEP=1
  printf '0|running\n' > "$tdir/status_plan.txt"
  printf '0\n' > "$tdir/install_rc"

  resolved_bin="$(command -v openclaw)"
  [[ "$resolved_bin" == "$mock_bin/openclaw" ]] || fail "tests must resolve openclaw to mock binary"

  bash "$SCRIPT" \
    --grace-seconds 1 \
    --status-retries 1 \
    --recovery-retries 1 \
    --status-interval-seconds 1 \
    --recovery-interval-seconds 1 \
    --max-runtime-seconds 60 >/dev/null

  cmd_file="$tdir/commands.log"
  assert_not_contains "update" "$cmd_file" "watchdog test must not call openclaw update"
  pass "tests run against mock openclaw binary only"
}

run_case_healthy_skips_recovery
run_case_unhealthy_runs_recovery
run_case_uses_mock_binary_only

run_case_retry_exhaustion_exits_nonzero() {
  local tdir mock_bin log_file cmd_file rc install_count
  tdir="$(mktemp -d)"
  mock_bin="$tdir/mockbin"
  mkdir -p "$mock_bin"
  make_mock_openclaw "$mock_bin"

  export MOCK_DIR="$tdir"
  export PATH="$mock_bin:$PATH"
  export WATCHDOG_SKIP_SLEEP=1
  printf '1|Gateway not running\n1|Gateway still not running\n1|Gateway still not running\n' > "$tdir/status_plan.txt"
  printf '0\n' > "$tdir/install_rc"
  log_file="$tdir/watchdog.log"

  set +e
  bash "$SCRIPT" \
    --log-file "$log_file" \
    --grace-seconds 1 \
    --status-retries 1 \
    --recovery-retries 2 \
    --status-interval-seconds 1 \
    --recovery-interval-seconds 1 \
    --max-runtime-seconds 60 >/dev/null 2>&1
  rc=$?
  set -e

  [[ "$rc" -eq 5 ]] || fail "retry exhaustion should exit 5, got $rc"
  cmd_file="$tdir/commands.log"
  assert_contains "gateway install" "$cmd_file" "retry exhaustion should attempt bounded installs"
  install_count="$(cat "$tdir/install_count")"
  [[ "$install_count" -eq 2 ]] || fail "retry exhaustion should run exactly 2 installs, got $install_count"
  assert_contains "result=failed_after_retries" "$log_file" "retry exhaustion should log failed_after_retries"
  pass "retry exhaustion exits non-zero after bounded recovery attempts"
}

run_case_deadline_exits_timeout() {
  local tdir mock_bin log_file rc start elapsed
  tdir="$(mktemp -d)"
  mock_bin="$tdir/mockbin"
  mkdir -p "$mock_bin"
  make_mock_openclaw "$mock_bin"

  export MOCK_DIR="$tdir"
  export PATH="$mock_bin:$PATH"
  unset WATCHDOG_SKIP_SLEEP || true
  printf '0|Gateway is running and healthy\n' > "$tdir/status_plan.txt"
  printf '0\n' > "$tdir/install_rc"
  log_file="$tdir/watchdog.log"

  start="$(date +%s)"
  set +e
  bash "$SCRIPT" \
    --log-file "$log_file" \
    --grace-seconds 2 \
    --status-retries 1 \
    --recovery-retries 1 \
    --status-interval-seconds 1 \
    --recovery-interval-seconds 1 \
    --max-runtime-seconds 1 >/dev/null 2>&1
  rc=$?
  set -e
  elapsed=$(( $(date +%s) - start ))

  [[ "$rc" -eq 4 ]] || fail "deadline timeout should exit 4, got $rc"
  [[ "$elapsed" -lt 4 ]] || fail "deadline should cap grace sleep, elapsed=${elapsed}s"
  assert_contains "result=timeout context=initial_grace" "$log_file" "deadline timeout should be logged"
  pass "global deadline caps grace sleep and exits timeout"
}

run_case_retry_exhaustion_exits_nonzero
run_case_deadline_exits_timeout
