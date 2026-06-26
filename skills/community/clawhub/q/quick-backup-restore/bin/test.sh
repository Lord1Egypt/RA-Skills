#!/bin/bash
# =============================================================================
# bin/test.sh — Time Clawshine self-test (backup → restore → verify roundtrip)
# Creates a temporary repo, backs up test data, restores, and verifies integrity.
# Usage: bin/test.sh (does NOT require root — uses temp directories)
# =============================================================================

set -euo pipefail

TC_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# --- Parse flags ------------------------------------------------------------
for arg in "$@"; do
    case "$arg" in
        --help|-h)
            echo "Usage: bin/test.sh"
            echo ""
            echo "Runs the Time Clawshine self-test suite:"
            echo "  - Dependency checks"
            echo "  - Config validation"
            echo "  - Shell syntax checks on all scripts"
            echo "  - Backup → restore → verify roundtrip"
            echo ""
            echo "Does NOT require root — uses temp directories."
            echo "Exit code: 0 if all tests pass, 1 if any fail."
            exit 0
            ;;
    esac
done

# --- Colors (if supported) --------------------------------------------------
if [[ -t 1 ]]; then
    GREEN='\033[0;32m'; RED='\033[0;31m'; NC='\033[0m'
else
    GREEN=''; RED=''; NC=''
fi

PASS=0
FAIL=0
TESTS=0

_test() {
    local name="$1"
    TESTS=$(( TESTS + 1 ))
    echo -n "  [$TESTS] $name ... "
}

_ok() {
    PASS=$(( PASS + 1 ))
    echo -e "${GREEN}OK${NC}"
}

_fail() {
    FAIL=$(( FAIL + 1 ))
    echo -e "${RED}FAIL${NC}: $1"
}

echo "╔═════════════════════════════════════════════════════╗"
echo "║          Time Clawshine — Self Test                  ║"
echo "╚═════════════════════════════════════════════════════╝"
echo ""

# --- Check dependencies ----------------------------------------------------
_test "Dependencies available"
MISSING=()
for cmd in restic yq curl jq bash openssl; do
    command -v "$cmd" &>/dev/null || MISSING+=("$cmd")
done
if [[ ${#MISSING[@]} -gt 0 ]]; then
    _fail "missing: ${MISSING[*]}"
else
    _ok
fi

# --- Validate config.yaml syntax -------------------------------------------
_test "config.yaml is valid YAML"
if yq e '.' "$TC_ROOT/config.yaml" > /dev/null 2>&1; then
    _ok
else
    _fail "yq cannot parse config.yaml"
fi

# --- Validate config loads without error ------------------------------------
_test "Config loads and validates"
if CONFIG_OUTPUT=$(bash -c "export TC_SKIP_PASS_CHECK=true; source '$TC_ROOT/lib.sh'; tc_load_config" 2>&1); then
    _ok
else
    _fail "$CONFIG_OUTPUT"
fi

# --- Security / privacy defaults -------------------------------------------
_test "Privacy defaults block external egress"
if PRIVACY_OUTPUT=$(bash -c "export TC_SKIP_PASS_CHECK=true; source '$TC_ROOT/lib.sh'; tc_load_config; [[ \"\$PRIVACY_LOCAL_ONLY\" == \"true\" && \"\$UPDATE_CHECK\" == \"false\" && \"\$TG_ENABLED\" == \"false\" && \"\$HC_ENABLED\" == \"false\" ]]" 2>&1); then
    _ok
else
    _fail "$PRIVACY_OUTPUT"
fi

_test "local_only rejects enabled external integrations"
TMP_CONFIG=$(mktemp)
cp "$TC_ROOT/config.yaml" "$TMP_CONFIG"
yq e -i '.notifications.telegram.enabled = true | .notifications.telegram.bot_token = "test-bot-token" | .notifications.telegram.chat_id = "test-chat-id"' "$TMP_CONFIG"
if LOCAL_ONLY_OUTPUT=$(bash -c "export TC_CONFIG='$TMP_CONFIG' TC_SKIP_PASS_CHECK=true; source '$TC_ROOT/lib.sh'; tc_load_config" 2>&1); then
    _fail "config unexpectedly passed with local_only=true and Telegram enabled"
else
    if grep -q "privacy.local_only is true" <<< "$LOCAL_ONLY_OUTPUT"; then
        _ok
    else
        _fail "$LOCAL_ONLY_OUTPUT"
    fi
fi
rm -f "$TMP_CONFIG"

_test "Healthcheck URL validation requires HTTPS or loopback"
TMP_CONFIG=$(mktemp)
cp "$TC_ROOT/config.yaml" "$TMP_CONFIG"
yq e -i '.privacy.local_only = false | .notifications.healthcheck.enabled = true | .notifications.healthcheck.url = "http://example.com/ping/test"' "$TMP_CONFIG"
if HC_OUTPUT=$(bash -c "export TC_CONFIG='$TMP_CONFIG' TC_SKIP_PASS_CHECK=true; source '$TC_ROOT/lib.sh'; tc_load_config" 2>&1); then
    _fail "config unexpectedly accepted non-loopback HTTP healthcheck URL"
else
    if grep -q "must use https" <<< "$HC_OUTPUT"; then
        yq e -i '.notifications.healthcheck.url = "http://localhost:8080/ping/test"' "$TMP_CONFIG"
        if HC_LOCAL_OUTPUT=$(bash -c "export TC_CONFIG='$TMP_CONFIG' TC_SKIP_PASS_CHECK=true; source '$TC_ROOT/lib.sh'; tc_load_config" 2>&1); then
            _ok
        else
            _fail "$HC_LOCAL_OUTPUT"
        fi
    else
        _fail "$HC_OUTPUT"
    fi
fi
rm -f "$TMP_CONFIG"

_test "Telegram failures omit raw details by default"
TMP_CONFIG=$(mktemp)
MSG_FILE=$(mktemp)
cp "$TC_ROOT/config.yaml" "$TMP_CONFIG"
yq e -i '.privacy.local_only = false | .privacy.send_error_details = false | .privacy.include_hostname = false | .notifications.telegram.enabled = true | .notifications.telegram.bot_token = "test-bot-token" | .notifications.telegram.chat_id = "test-chat-id"' "$TMP_CONFIG"
if TG_OUTPUT=$(MSG_FILE="$MSG_FILE" bash -c "export TC_CONFIG='$TMP_CONFIG' TC_SKIP_PASS_CHECK=true; source '$TC_ROOT/lib.sh'; tc_load_config; tg_send() { printf '%s' \"\$1\" > \"\$MSG_FILE\"; }; tg_failure 'secret path /root/.ssh/id_rsa token=abc123'; cat \"\$MSG_FILE\"" 2>&1); then
    if grep -Eq 'secret|/root/\.ssh|token=abc123|Host:' <<< "$TG_OUTPUT"; then
        _fail "message leaked raw detail: $TG_OUTPUT"
    else
        _ok
    fi
else
    _fail "$TG_OUTPUT"
fi
rm -f "$TMP_CONFIG" "$MSG_FILE"

# --- Validate skill.json is valid JSON --------------------------------------
_test "skill.json is valid JSON"
if jq empty "$TC_ROOT/skill.json" 2>/dev/null; then
    _ok
else
    _fail "jq cannot parse skill.json"
fi

# --- Shell syntax checks on all scripts ------------------------------------
for script in lib.sh bin/backup.sh bin/setup.sh bin/restore.sh bin/status.sh bin/customize.sh bin/prune.sh bin/test.sh bin/uninstall.sh; do
    _test "Syntax check: $script"
    if [[ -f "$TC_ROOT/$script" ]]; then
        if bash -n "$TC_ROOT/$script" 2>/dev/null; then
            _ok
        else
            _fail "bash -n failed"
        fi
    else
        _fail "file not found"
    fi
done

# --- --help flag exits 0 on all scripts ------------------------------------
for script in bin/backup.sh bin/setup.sh bin/restore.sh bin/status.sh bin/customize.sh bin/prune.sh bin/test.sh bin/uninstall.sh; do
    _test "--help exits 0: $script"
    if bash "$TC_ROOT/$script" --help > /dev/null 2>&1; then
        _ok
    else
        _fail "--help returned non-zero"
    fi
done

_test "setup --dry-run exits 0 without root"
if bash "$TC_ROOT/bin/setup.sh" --dry-run > /dev/null 2>&1; then
    _ok
else
    _fail "setup --dry-run returned non-zero"
fi

_test "Cron converter maps hourly schedule to systemd"
if CRON_CAL=$(bash -c "source '$TC_ROOT/lib.sh'; tc_cron_to_systemd_calendar '5 * * * *'" 2>&1) \
    && [[ "$CRON_CAL" == "*-*-* *:05:00" ]]; then
    _ok
else
    _fail "$CRON_CAL"
fi

_test "Cron converter maps every 2 hours to systemd"
if CRON_CAL=$(bash -c "source '$TC_ROOT/lib.sh'; tc_cron_to_systemd_calendar '0 */2 * * *'" 2>&1) \
    && [[ "$CRON_CAL" == "*-*-* 00/2:00:00" ]]; then
    _ok
else
    _fail "$CRON_CAL"
fi

_test "Cron converter rejects weekly schedules for cron fallback"
if CRON_CAL=$(bash -c "source '$TC_ROOT/lib.sh'; tc_cron_to_systemd_calendar '0 0 * * 1'" 2>&1); then
    _fail "unexpected conversion: $CRON_CAL"
else
    _ok
fi

# --- Backup → Restore → Verify roundtrip -----------------------------------
_test "Roundtrip: backup → restore → verify"

TMPDIR=$(mktemp -d)
TEST_REPO="$TMPDIR/repo"
TEST_PASS="$TMPDIR/pass"
TEST_DATA="$TMPDIR/data"
TEST_RESTORE="$TMPDIR/restore"

mkdir -p "$TEST_DATA/subdir"
echo "Time Clawshine test file — $(date)" > "$TEST_DATA/testfile.txt"
echo "Nested content" > "$TEST_DATA/subdir/nested.txt"
dd if=/dev/urandom of="$TEST_DATA/subdir/binary.bin" bs=1024 count=4 2>/dev/null

# Generate password
openssl rand -base64 32 > "$TEST_PASS"
chmod 600 "$TEST_PASS"

# Init repo
if RESTIC_PASSWORD_FILE="$TEST_PASS" restic init -r "$TEST_REPO" > /dev/null 2>&1; then
    # Backup
    if RESTIC_PASSWORD_FILE="$TEST_PASS" restic backup -r "$TEST_REPO" "$TEST_DATA" > /dev/null 2>&1; then
        # Restore
        mkdir -p "$TEST_RESTORE"
        if RESTIC_PASSWORD_FILE="$TEST_PASS" restic restore latest -r "$TEST_REPO" --target "$TEST_RESTORE" > /dev/null 2>&1; then
            # Verify files match (use relative paths so hashes compare equal)
            ORIG_HASH=$(cd "$TEST_DATA" && find . -type f -exec sha256sum {} \; | sort | sha256sum)
            # Restored files are under $TEST_RESTORE/$TEST_DATA
            RESTORED_DATA="$TEST_RESTORE$TEST_DATA"
            if [[ -d "$RESTORED_DATA" ]]; then
                REST_HASH=$(cd "$RESTORED_DATA" && find . -type f -exec sha256sum {} \; | sort | sha256sum)
                if [[ "$ORIG_HASH" == "$REST_HASH" ]]; then
                    _ok
                else
                    _fail "hash mismatch after restore"
                fi
            else
                _fail "restored data directory not found at $RESTORED_DATA"
            fi
        else
            _fail "restic restore failed"
        fi
    else
        _fail "restic backup failed"
    fi

    # Check integrity
    _test "Roundtrip: restic check"
    if RESTIC_PASSWORD_FILE="$TEST_PASS" restic check -r "$TEST_REPO" > /dev/null 2>&1; then
        _ok
    else
        _fail "restic check failed"
    fi

    # Prune dry-run (should succeed without removing the single snapshot)
    _test "Roundtrip: prune --dry-run"
    if RESTIC_PASSWORD_FILE="$TEST_PASS" restic forget --keep-last 1 --prune --dry-run -r "$TEST_REPO" > /dev/null 2>&1; then
        _ok
    else
        _fail "restic forget --dry-run failed"
    fi

    # Verify password file permissions
    _test "Roundtrip: password file permissions"
    PASS_PERMS=$(stat -c '%a' "$TEST_PASS" 2>/dev/null || stat -f '%Lp' "$TEST_PASS" 2>/dev/null || echo "?")
    if [[ "$PASS_PERMS" == "600" ]]; then
        _ok
    else
        _fail "expected 600, got $PASS_PERMS"
    fi
else
    _fail "restic init failed"
fi

# Cleanup temp
rm -rf "$TMPDIR"

# --- Summary ----------------------------------------------------------------
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [[ $FAIL -eq 0 ]]; then
    echo -e "  ${GREEN}All $TESTS tests passed ✓${NC}"
    EXIT_CODE=0
else
    echo -e "  ${RED}$FAIL/$TESTS tests failed ✗${NC}"
    EXIT_CODE=1
fi
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
exit $EXIT_CODE
