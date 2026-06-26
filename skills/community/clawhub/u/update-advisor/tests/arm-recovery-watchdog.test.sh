#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ARM_SCRIPT="$ROOT_DIR/scripts/arm-recovery-watchdog.sh"

pass() { printf '[PASS] %s\n' "$1"; }
fail() { printf '[FAIL] %s\n' "$1" >&2; exit 1; }

assert_contains() {
  local needle="$1" file="$2" msg="$3"
  grep -F -- "$needle" "$file" >/dev/null 2>&1 || fail "$msg"
}

assert_not_contains() {
  local needle="$1" file="$2" msg="$3"
  if grep -F -- "$needle" "$file" >/dev/null 2>&1; then
    fail "$msg"
  fi
}

real_path() {
  python3 -c 'import os,sys; print(os.path.realpath(sys.argv[1]))' "$1"
}

state_value() {
  local state_file="$1" key="$2"
  awk -F= -v k="$key" '$1==k{print substr($0, index($0,"=")+1); exit}' "$state_file"
}

make_mock_tools() {
  local mock_bin_dir="$1"
  cat > "$mock_bin_dir/launchctl" <<'EOF_LAUNCHCTL'
#!/usr/bin/env bash
set -euo pipefail
MOCK_DIR="${MOCK_DIR:?MOCK_DIR required}"
printf 'launchctl %s\n' "$*" >> "$MOCK_DIR/commands.log"
case "${1:-}" in
  bootstrap)
    [[ "${LAUNCHCTL_FAIL_BOOTSTRAP:-0}" == "1" ]] && exit 42
    exit 0
    ;;
  print)
    [[ "${LAUNCHCTL_FAIL_PRINT:-0}" == "1" ]] && exit 43
    exit 0
    ;;
  bootout)
    exit 0
    ;;
  *)
    echo "unexpected launchctl command: $*" >&2
    exit 99
    ;;
esac
EOF_LAUNCHCTL
  chmod +x "$mock_bin_dir/launchctl"

  cat > "$mock_bin_dir/systemd-run" <<'EOF_SYSTEMD_RUN'
#!/usr/bin/env bash
set -euo pipefail
MOCK_DIR="${MOCK_DIR:?MOCK_DIR required}"
printf 'systemd-run %s\n' "$*" >> "$MOCK_DIR/commands.log"
[[ "${SYSTEMD_RUN_FAIL:-0}" == "1" ]] && exit 45
exit 0
EOF_SYSTEMD_RUN
  chmod +x "$mock_bin_dir/systemd-run"

  cat > "$mock_bin_dir/systemctl" <<'EOF_SYSTEMCTL'
#!/usr/bin/env bash
set -euo pipefail
MOCK_DIR="${MOCK_DIR:?MOCK_DIR required}"
printf 'systemctl %s\n' "$*" >> "$MOCK_DIR/commands.log"
if [[ "${1:-}" == "--user" && "${2:-}" == "show" && "${SYSTEMCTL_FAIL_SHOW:-0}" == "1" ]]; then
  exit 46
fi
exit 0
EOF_SYSTEMCTL
  chmod +x "$mock_bin_dir/systemctl"

  cat > "$mock_bin_dir/openclaw" <<'EOF_OPENCLAW'
#!/usr/bin/env bash
set -euo pipefail
printf 'openclaw %s\n' "$*" >> "${MOCK_DIR:?MOCK_DIR required}/openclaw-commands.log"
if [[ "${1:-}" == "gateway" && "${2:-}" == "status" ]]; then
  echo "mock gateway healthy"
  exit 0
fi
echo "unexpected openclaw command: $*" >&2
exit 99
EOF_OPENCLAW
  chmod +x "$mock_bin_dir/openclaw"

  cat > "$mock_bin_dir/plutil" <<'EOF_PLUTIL'
#!/usr/bin/env bash
set -euo pipefail
MOCK_DIR="${MOCK_DIR:?MOCK_DIR required}"
printf 'plutil %s\n' "$*" >> "$MOCK_DIR/commands.log"
[[ "${PLUTIL_FAIL:-0}" == "1" ]] && exit 44
exit 0
EOF_PLUTIL
  chmod +x "$mock_bin_dir/plutil"
}

run_case_launchd_arm_and_cleanup_success() {
  local tdir mock_bin state_file out_file cleanup_out label plist commands openclaw_bin resolved_openclaw_bin recorded_openclaw_bin
  tdir="$(mktemp -d)"
  mock_bin="$tdir/mockbin"
  mkdir -p "$mock_bin" "$tdir/state"
  make_mock_tools "$mock_bin"

  export MOCK_DIR="$tdir"
  state_file="$tdir/state/watchdog.state"
  out_file="$tdir/arm.out"
  cleanup_out="$tdir/cleanup.out"
  openclaw_bin="$mock_bin/openclaw"
  resolved_openclaw_bin="$(real_path "$openclaw_bin")"

  WATCHDOG_BACKEND="launchd" \
  LAUNCHCTL_BIN="$mock_bin/launchctl" \
  PLUTIL_BIN="$mock_bin/plutil" \
  STATE_DIR="$tdir/state" \
  LABEL_PREFIX="test.openclaw.watchdog" \
  LAUNCHCTL_DOMAIN="gui/test" \
  WATCHDOG_SCRIPT="$ROOT_DIR/scripts/recovery-watchdog.sh" \
  OPENCLAW_BIN="$openclaw_bin" \
  bash "$ARM_SCRIPT" arm --state-file "$state_file" > "$out_file"

  [[ -s "$state_file" ]] || fail "launchd arm should write a non-empty state file"
  [[ "$(state_value "$state_file" backend)" == "launchd" ]] || fail "state should record launchd backend"
  label="$(state_value "$state_file" label)"
  plist="$(state_value "$state_file" plist)"
  [[ "$label" == test.openclaw.watchdog.* ]] || fail "label should be unique with configured prefix"
  [[ -f "$plist" ]] || fail "launchd arm should render plist"
  assert_not_contains "__LABEL__" "$plist" "rendered plist should not retain label placeholder"
  assert_not_contains "__SKILL_DIR__" "$plist" "rendered plist should not retain skill dir placeholder"
  assert_contains "<key>EnvironmentVariables</key>" "$plist" "rendered plist should include launchd environment"
  assert_contains "<key>OPENCLAW_BIN</key>" "$plist" "rendered plist should include OPENCLAW_BIN key"
  assert_contains "<string>$resolved_openclaw_bin</string>" "$plist" "rendered plist should carry resolved absolute mock OpenClaw path"
  assert_contains "<key>PATH</key>" "$plist" "rendered plist should include PATH key"
  recorded_openclaw_bin="$(state_value "$state_file" openclaw_bin)"
  [[ "$recorded_openclaw_bin" == "$resolved_openclaw_bin" ]] || fail "state file should record resolved openclaw_bin"

  commands="$tdir/commands.log"
  assert_contains "plutil -lint $plist" "$commands" "launchd arm should validate plist"
  assert_contains "launchctl bootstrap gui/test $plist" "$commands" "launchd arm should bootstrap launchd job"
  assert_contains "launchctl print gui/test/$label" "$commands" "launchd arm should verify launchd job"
  [[ ! -e "$tdir/openclaw-commands.log" ]] || fail "arming should resolve but not invoke openclaw"

  WATCHDOG_BACKEND="launchd" \
  LAUNCHCTL_BIN="$mock_bin/launchctl" \
  PLUTIL_BIN="$mock_bin/plutil" \
  STATE_DIR="$tdir/state" \
  bash "$ARM_SCRIPT" cleanup --state-file "$state_file" > "$cleanup_out"

  assert_contains "launchctl bootout gui/test/$label" "$commands" "launchd cleanup should bootout launchd job"
  [[ ! -e "$state_file" ]] || fail "cleanup should remove state file"
  [[ ! -e "$plist" ]] || fail "cleanup should remove rendered plist"
  pass "launchd arm verifies job, records OPENCLAW_BIN, and cleanup removes state/plist"
}

run_case_systemd_arm_and_cleanup_success() {
  local tdir mock_bin state_file out_file cleanup_out unit commands openclaw_bin resolved_openclaw_bin recorded_openclaw_bin
  tdir="$(mktemp -d)"
  mock_bin="$tdir/mockbin"
  mkdir -p "$mock_bin" "$tdir/state"
  make_mock_tools "$mock_bin"

  export MOCK_DIR="$tdir"
  state_file="$tdir/state/watchdog.state"
  out_file="$tdir/arm.out"
  cleanup_out="$tdir/cleanup.out"
  openclaw_bin="$mock_bin/openclaw"
  resolved_openclaw_bin="$(real_path "$openclaw_bin")"

  OS_NAME="Linux" \
  WATCHDOG_BACKEND="auto" \
  SYSTEMD_RUN_BIN="$mock_bin/systemd-run" \
  SYSTEMCTL_BIN="$mock_bin/systemctl" \
  STATE_DIR="$tdir/state" \
  SYSTEMD_UNIT_PREFIX="test-openclaw-watchdog" \
  WATCHDOG_SCRIPT="$ROOT_DIR/scripts/recovery-watchdog.sh" \
  OPENCLAW_BIN="$openclaw_bin" \
  bash "$ARM_SCRIPT" arm --state-file "$state_file" > "$out_file"

  [[ -s "$state_file" ]] || fail "systemd arm should write a non-empty state file"
  [[ "$(state_value "$state_file" backend)" == "systemd" ]] || fail "state should record systemd backend"
  unit="$(state_value "$state_file" unit)"
  [[ "$unit" == test-openclaw-watchdog-*.service ]] || fail "systemd unit should use configured prefix"
  recorded_openclaw_bin="$(state_value "$state_file" openclaw_bin)"
  [[ "$recorded_openclaw_bin" == "$resolved_openclaw_bin" ]] || fail "state file should record resolved openclaw_bin"

  commands="$tdir/commands.log"
  assert_contains "systemd-run --user --unit $unit" "$commands" "systemd arm should call systemd-run --user with unique unit"
  assert_contains "--setenv OPENCLAW_BIN=$resolved_openclaw_bin" "$commands" "systemd arm should pass OPENCLAW_BIN into unit environment"
  assert_contains "--setenv PATH=$(dirname "$resolved_openclaw_bin")" "$commands" "systemd arm should pass PATH into unit environment"
  assert_contains "systemctl --user show $unit" "$commands" "systemd arm should verify unit with systemctl show"
  [[ ! -e "$tdir/openclaw-commands.log" ]] || fail "systemd arming should resolve but not invoke openclaw"

  OS_NAME="Linux" \
  WATCHDOG_BACKEND="systemd" \
  SYSTEMCTL_BIN="$mock_bin/systemctl" \
  STATE_DIR="$tdir/state" \
  bash "$ARM_SCRIPT" cleanup --state-file "$state_file" > "$cleanup_out"

  assert_contains "systemctl --user stop $unit" "$commands" "systemd cleanup should stop unit"
  assert_contains "systemctl --user reset-failed $unit" "$commands" "systemd cleanup should reset failed unit"
  [[ ! -e "$state_file" ]] || fail "systemd cleanup should remove state file"
  pass "systemd arm verifies user unit, records OPENCLAW_BIN, and cleanup removes state"
}

run_case_launchd_print_failure_blocks_update_path() {
  local tdir mock_bin state_file out_file rc commands
  tdir="$(mktemp -d)"
  mock_bin="$tdir/mockbin"
  mkdir -p "$mock_bin" "$tdir/state"
  make_mock_tools "$mock_bin"

  export MOCK_DIR="$tdir"
  export LAUNCHCTL_FAIL_PRINT=1
  state_file="$tdir/state/watchdog.state"
  out_file="$tdir/arm-fail.out"

  set +e
  WATCHDOG_BACKEND="launchd" \
  LAUNCHCTL_BIN="$mock_bin/launchctl" \
  PLUTIL_BIN="$mock_bin/plutil" \
  STATE_DIR="$tdir/state" \
  LABEL_PREFIX="test.openclaw.watchdog" \
  LAUNCHCTL_DOMAIN="gui/test" \
  WATCHDOG_SCRIPT="$ROOT_DIR/scripts/recovery-watchdog.sh" \
  OPENCLAW_BIN="$mock_bin/openclaw" \
  bash "$ARM_SCRIPT" arm --state-file "$state_file" > "$out_file" 2>&1
  rc=$?
  set -e
  unset LAUNCHCTL_FAIL_PRINT

  [[ "$rc" -ne 0 ]] || fail "launchd arm should fail when launchctl print verification fails"
  [[ ! -e "$state_file" ]] || fail "failed launchd arming should not leave state file"
  commands="$tdir/commands.log"
  assert_contains "launchctl bootout" "$commands" "failed launchd verification should attempt bootout cleanup"
  pass "launchd verification failure blocks update path"
}

run_case_systemd_verify_failure_blocks_update_path() {
  local tdir mock_bin state_file rc commands
  tdir="$(mktemp -d)"
  mock_bin="$tdir/mockbin"
  mkdir -p "$mock_bin" "$tdir/state"
  make_mock_tools "$mock_bin"

  export MOCK_DIR="$tdir"
  export SYSTEMCTL_FAIL_SHOW=1
  state_file="$tdir/state/watchdog.state"

  set +e
  OS_NAME="Linux" \
  WATCHDOG_BACKEND="systemd" \
  SYSTEMD_RUN_BIN="$mock_bin/systemd-run" \
  SYSTEMCTL_BIN="$mock_bin/systemctl" \
  STATE_DIR="$tdir/state" \
  WATCHDOG_SCRIPT="$ROOT_DIR/scripts/recovery-watchdog.sh" \
  OPENCLAW_BIN="$mock_bin/openclaw" \
  bash "$ARM_SCRIPT" arm --state-file "$state_file" >/dev/null 2>&1
  rc=$?
  set -e
  unset SYSTEMCTL_FAIL_SHOW

  [[ "$rc" -ne 0 ]] || fail "systemd arm should fail when systemctl show verification fails"
  [[ ! -e "$state_file" ]] || fail "failed systemd arming should not leave state file"
  commands="$tdir/commands.log"
  assert_contains "systemctl --user stop" "$commands" "failed systemd verification should attempt stop cleanup"
  assert_contains "systemctl --user reset-failed" "$commands" "failed systemd verification should reset failed unit"
  pass "systemd verification failure blocks update path"
}

run_case_plutil_failure_blocks_before_bootstrap() {
  local tdir mock_bin state_file rc commands
  tdir="$(mktemp -d)"
  mock_bin="$tdir/mockbin"
  mkdir -p "$mock_bin" "$tdir/state"
  make_mock_tools "$mock_bin"

  export MOCK_DIR="$tdir"
  export PLUTIL_FAIL=1
  state_file="$tdir/state/watchdog.state"

  set +e
  WATCHDOG_BACKEND="launchd" \
  LAUNCHCTL_BIN="$mock_bin/launchctl" \
  PLUTIL_BIN="$mock_bin/plutil" \
  STATE_DIR="$tdir/state" \
  LABEL_PREFIX="test.openclaw.watchdog" \
  LAUNCHCTL_DOMAIN="gui/test" \
  WATCHDOG_SCRIPT="$ROOT_DIR/scripts/recovery-watchdog.sh" \
  OPENCLAW_BIN="$mock_bin/openclaw" \
  bash "$ARM_SCRIPT" arm --state-file "$state_file" >/dev/null 2>&1
  rc=$?
  set -e
  unset PLUTIL_FAIL

  [[ "$rc" -ne 0 ]] || fail "launchd arm should fail when plist validation fails"
  [[ ! -e "$state_file" ]] || fail "plutil failure should not leave state file"
  commands="$tdir/commands.log"
  assert_not_contains "launchctl bootstrap" "$commands" "plutil failure must block launchctl bootstrap"
  pass "plist validation failure blocks launchd bootstrap"
}

run_case_missing_openclaw_blocks_arm() {
  local tdir mock_bin state_file rc
  tdir="$(mktemp -d)"
  mock_bin="$tdir/mockbin"
  mkdir -p "$mock_bin" "$tdir/state"
  make_mock_tools "$mock_bin"

  export MOCK_DIR="$tdir"
  state_file="$tdir/state/watchdog.state"

  set +e
  WATCHDOG_BACKEND="systemd" \
  SYSTEMD_RUN_BIN="$mock_bin/systemd-run" \
  SYSTEMCTL_BIN="$mock_bin/systemctl" \
  STATE_DIR="$tdir/state" \
  WATCHDOG_SCRIPT="$ROOT_DIR/scripts/recovery-watchdog.sh" \
  OPENCLAW_BIN="$tdir/missing-openclaw" \
  bash "$ARM_SCRIPT" arm --state-file "$state_file" >/dev/null 2>&1
  rc=$?
  set -e

  [[ "$rc" -ne 0 ]] || fail "arm should fail when OPENCLAW_BIN is missing/not executable"
  [[ ! -e "$state_file" ]] || fail "missing OPENCLAW_BIN should not leave state file"
  pass "missing OPENCLAW_BIN blocks watchdog arming"
}

run_case_launchd_arm_and_cleanup_success
run_case_systemd_arm_and_cleanup_success
run_case_launchd_print_failure_blocks_update_path
run_case_systemd_verify_failure_blocks_update_path
run_case_plutil_failure_blocks_before_bootstrap
run_case_missing_openclaw_blocks_arm
