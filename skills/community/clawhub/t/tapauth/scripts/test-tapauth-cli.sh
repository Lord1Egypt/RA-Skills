#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TAPAUTH_SCRIPT="${SCRIPT_DIR}/tapauth.sh"
TMPDIR="$(mktemp -d)"
trap 'rm -rf "$TMPDIR"' EXIT

FAKE_BIN="${TMPDIR}/bin"
STATE_DIR="${TMPDIR}/state"
TAPAUTH_HOME="${TMPDIR}/tapauth-home"
mkdir -p "$FAKE_BIN" "$STATE_DIR" "$TAPAUTH_HOME"

cat > "${FAKE_BIN}/sleep" <<'EOF'
#!/usr/bin/env bash
exit 0
EOF
chmod +x "${FAKE_BIN}/sleep"

cat > "${FAKE_BIN}/curl" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail

state_dir="${TAPAUTH_TEST_STATE:?}"
method="GET"
url=""
for arg in "$@"; do
  case "$arg" in
    -X) method="NEXT" ;;
    POST)
      if [ "$method" = "NEXT" ]; then
        method="POST"
      fi
      ;;
    http://tapauth.test/*) url="$arg" ;;
  esac
done

if [ "$method" = "POST" ]; then
  echo "POST ${url}" >> "${state_dir}/calls"
  cat <<RESP
TAPAUTH_GRANT_ID=grant-123
TAPAUTH_GRANT_SECRET=secret-abc
TAPAUTH_APPROVE_URL=http://tapauth.test/approve/grant-123
RESP
  printf '\n201'
  exit 0
fi

echo "GET ${url}" >> "${state_dir}/calls"
count_file="${state_dir}/get-count"
count=0
[ -f "$count_file" ] && count="$(cat "$count_file")"
count=$((count + 1))
echo "$count" > "$count_file"

if [ "$count" -eq 1 ]; then
  cat <<RESP
TAPAUTH_STATUS=pending
TAPAUTH_APPROVE_URL=http://tapauth.test/approve/grant-123
RESP
  printf '\n202'
  exit 0
fi

cat <<RESP
TAPAUTH_TOKEN_B64=dGVzdC10b2tlbg==
TAPAUTH_EXPIRES=1893456000
RESP
printf '\n200'
EOF
chmod +x "${FAKE_BIN}/curl"

run_tapauth() {
  PATH="${FAKE_BIN}:$PATH" \
    TAPAUTH_TEST_STATE="$STATE_DIR" \
    TAPAUTH_BASE_URL="http://tapauth.test" \
    TAPAUTH_HOME="$TAPAUTH_HOME" \
    "$TAPAUTH_SCRIPT" "$@"
}

if run_tapauth --token google calendar.readonly >"${TMPDIR}/missing.out" 2>"${TMPDIR}/missing.err"; then
  echo "expected --token without a grant to fail" >&2
  exit 1
fi
grep -q "run without --token first" "${TMPDIR}/missing.err"
if [ -f "${STATE_DIR}/calls" ]; then
  echo "--token without a cached grant should not create or poll grants" >&2
  exit 1
fi

run_tapauth google calendar.readonly >"${TMPDIR}/url.out" 2>"${TMPDIR}/url.err"
grep -q "Approve access: http://tapauth.test/approve/grant-123" "${TMPDIR}/url.out"
grep -q "TAPAUTH_GRANT_ID=grant-123" "${TAPAUTH_HOME}/google-calendar.readonly.env"
grep -q "TAPAUTH_GRANT_SECRET=secret-abc" "${TAPAUTH_HOME}/google-calendar.readonly.env"
if grep -q "GET " "${STATE_DIR}/calls"; then
  echo "URL mode should not poll grants" >&2
  exit 1
fi

token="$(run_tapauth --token google calendar.readonly 2>"${TMPDIR}/token.err")"
[ "$token" = "test-token" ]
grep -q "Waiting for approval" "${TMPDIR}/token.err"
grep -q "TAPAUTH_EXPIRES=1893456000" "${TAPAUTH_HOME}/google-calendar.readonly.env"

echo "tapauth CLI lifecycle smoke test passed"
