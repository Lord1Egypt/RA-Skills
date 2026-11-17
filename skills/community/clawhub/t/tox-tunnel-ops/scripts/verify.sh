#!/usr/bin/env bash
# tox-tunnel-ops verification script
#
# Usage: bash scripts/verify.sh <local_port> [expected_service] [config_or_data_dir]
#
#   local_port         the client-side forwarded port to test
#   expected_service   ssh | http | postgres | mysql | redis | mongo | rdp | tcp
#                      (default: tcp).  An unrecognised value is an error, not a pass.
#   config_or_data_dir optional client.yaml (or data_dir) so the script can ask the
#                      running daemon (`toxtunnel inspect`) whether the tunnel is
#                      actually up, instead of guessing from a local TCP accept.
#
# Exit codes — check these, do not read the prose:
#   0  end-to-end delivery through the tunnel was PROVEN by a service-level probe
#   1  a check FAILED — the tunnel is not working
#   2  local checks passed but end-to-end delivery was NOT PROVEN (no probe tool
#      installed, or the protocol has no cheap probe).  This is NOT success.
#
# Why the distinction matters: the toxtunnel client binds and accepts on the local
# forward port *before* any Tox tunnel exists.  A successful TCP connect to
# 127.0.0.1:<port> therefore proves only that the local listener is up — it says
# nothing about TUNNEL_OPEN succeeding or the remote target being reachable.  Only
# a reply from the real remote service proves the end-to-end path.

set -uo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

LOCAL_PORT="${1:-}"
SERVICE="${2:-tcp}"
DAEMON_REF="${3:-}"

FAILURES=0
E2E_PROVEN=false

usage() {
    echo "Usage: bash scripts/verify.sh <local_port> [ssh|http|postgres|mysql|redis|mongo|rdp|tcp] [client.yaml|data_dir]"
}

info()  { echo -e "${GREEN}[OK]${NC}    $1"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $1"; }
fail()  { echo -e "${RED}[FAIL]${NC}  $1"; FAILURES=$((FAILURES + 1)); }
# Local checks passed, but nothing proved the far end answered.
unproven() { echo -e "${YELLOW}[UNPROVEN]${NC} $1"; }

if [ -z "$LOCAL_PORT" ]; then
    usage
    exit 1
fi

case "$SERVICE" in
    ssh|http|postgres|mysql|redis|mongo|rdp|tcp) ;;
    *)
        echo -e "${RED}[FAIL]${NC}  Unknown service type '$SERVICE'."
        echo "        A typo here would otherwise be silently verified as a generic TCP pass."
        usage
        exit 1
        ;;
esac

# Portable timeout wrapper: coreutils `timeout` where available, else run bare
# (every probe below also passes its own client-side timeout flag where it has one).
if command -v timeout &>/dev/null; then
    tmo() { timeout "$@"; }
elif command -v gtimeout &>/dev/null; then
    tmo() { gtimeout "$@"; }
else
    tmo() { shift; "$@"; }
fi

echo "===== Tunnel Verification: port $LOCAL_PORT ($SERVICE) ====="
echo ""

# --- Step 1: Port listening check ---
echo "--- Step 1: Local Listener ---"
LISTENER=""
BIND_ADDRS=""
if command -v lsof &>/dev/null; then
    LISTENER=$(lsof -nP -i "TCP:$LOCAL_PORT" -sTCP:LISTEN 2>/dev/null | tail -n +2 || true)
    BIND_ADDRS=$(printf '%s\n' "$LISTENER" | awk '{print $9}' || true)
elif command -v ss &>/dev/null; then
    LISTENER=$(ss -tlnp 2>/dev/null | grep -E "[:.]$LOCAL_PORT[[:space:]]" || true)
    BIND_ADDRS=$(printf '%s\n' "$LISTENER" | awk '{print $4}' || true)
elif command -v netstat &>/dev/null; then
    LISTENER=$(netstat -an 2>/dev/null | grep -E "[:.]$LOCAL_PORT[[:space:]].*LISTEN" || true)
    BIND_ADDRS=$(printf '%s\n' "$LISTENER" | awk '{print $4}' || true)
fi

if [ -n "$LISTENER" ]; then
    info "Port $LOCAL_PORT is listening"
    # A forward binds whatever local_address says (v0.4.13+). With the key absent
    # — and on every v0.4.12-and-older daemon — the client calls
    # TcpListener(io, port), which binds asio::ip::tcp::v4(): 0.0.0.0, every IPv4
    # interface. This check reports what the socket actually shows either way.
    if printf '%s\n' "$BIND_ADDRS" | grep -qE '(^|[^0-9.])(0\.0\.0\.0|\*|\[?::\]?):?'"$LOCAL_PORT"'$|^\*:'"$LOCAL_PORT"'$'; then
        warn "Listener is bound to a WILDCARD address (0.0.0.0 / *), not loopback."
        echo "       On v0.4.13+ set \`local_address: 127.0.0.1\` on this forward; on older"
        echo "       daemons no such key exists, so firewall the port. Any host that can reach this"

        echo "       machine on port $LOCAL_PORT gets the forwarded service, with no auth."
        echo "       Mitigate with a host firewall rule, e.g.:"
        echo "         Linux (nftables): nft add rule inet filter input tcp dport $LOCAL_PORT iif != lo drop"
        echo "         Linux (ufw):      ufw deny in to any port $LOCAL_PORT"
        echo "         macOS (pf):       block in proto tcp to any port $LOCAL_PORT"
        echo "       ...or use a loopback-only SOCKS5 listener (client.socks5) instead of a forward."
    fi
    printf '%s\n' "$LISTENER" | sed 's/^/       /'
else
    fail "Port $LOCAL_PORT is NOT listening"
    echo "       Is the toxtunnel client running with the correct config?"
    echo "       Check: toxtunnel config check -c <client.yaml> --strict"
    exit 1
fi

echo ""

# --- Step 2: Daemon-reported tunnel state (optional but authoritative) ---
echo "--- Step 2: Daemon State ---"
if [ -n "$DAEMON_REF" ] && command -v toxtunnel &>/dev/null; then
    if [ -d "$DAEMON_REF" ]; then
        INSPECT_ARGS=(-d "$DAEMON_REF")
    else
        INSPECT_ARGS=(-c "$DAEMON_REF")
    fi
    STATUS_JSON=$(tmo 10 toxtunnel inspect status "${INSPECT_ARGS[@]}" --json 2>/dev/null || true)
    if [ -n "$STATUS_JSON" ]; then
        # Field-scoped extraction; avoids matching a different numeric field.
        FRIENDS=$(printf '%s' "$STATUS_JSON" \
            | tr ',{}' '\n\n\n' \
            | grep '"friends_online"' \
            | head -1 | grep -oE '[0-9]+$' || true)
        if [ -n "$FRIENDS" ] && [ "$FRIENDS" -gt 0 ] 2>/dev/null; then
            info "Daemon reports friends_online=$FRIENDS (Tox link is up)"
        elif [ -n "$FRIENDS" ]; then
            fail "Daemon reports friends_online=0 — no Tox peer is connected."
            echo "       The local port will still accept connections; nothing will flow."
            echo "       Nothing downstream of this can succeed. Diagnose the Tox link first:"
            echo "         bash scripts/diagnose.sh <client.yaml>"
        else
            warn "Could not read friends_online from 'inspect status --json' output"
        fi
    else
        warn "'toxtunnel inspect status' returned nothing (daemon down, wrong data_dir, or inspect disabled)"
    fi
elif [ -n "$DAEMON_REF" ]; then
    warn "toxtunnel binary not on PATH — skipping daemon state check"
else
    warn "No config/data_dir argument given — skipping daemon state check"
    echo "       Re-run as: bash scripts/verify.sh $LOCAL_PORT $SERVICE <client.yaml>"
    echo "       so the tunnel state can be read from the daemon rather than inferred."
fi

echo ""

# --- Step 3: TCP connectivity (LOCAL ONLY — proves nothing about the tunnel) ---
echo "--- Step 3: Local TCP Accept ---"
TCP_OK=false
if command -v nc &>/dev/null; then
    if nc -z -w 5 127.0.0.1 "$LOCAL_PORT" 2>/dev/null; then
        TCP_OK=true
    fi
else
    if (echo >"/dev/tcp/127.0.0.1/$LOCAL_PORT") 2>/dev/null; then
        TCP_OK=true
    fi
fi

if [ "$TCP_OK" = true ]; then
    info "TCP connect to 127.0.0.1:$LOCAL_PORT succeeded"
    echo "       NOTE: this only proves the local toxtunnel listener accepted a socket."
    echo "       The client accepts before TUNNEL_OPEN is attempted, so this says nothing"
    echo "       about the Tox link or the remote target. Step 4 is the real test."
else
    fail "TCP connect to 127.0.0.1:$LOCAL_PORT failed even though the port is listening"
    echo "       Something is refusing or dropping loopback connections (firewall? proxy?)."
    exit 1
fi

echo ""

# --- Step 4: Service-specific end-to-end verification ---
echo "--- Step 4: End-to-End Service Probe ($SERVICE) ---"

case "$SERVICE" in
    ssh)
        if command -v nc &>/dev/null; then
            BANNER=$(tmo 10 nc -w 6 127.0.0.1 "$LOCAL_PORT" </dev/null 2>/dev/null | head -1 || true)
            if printf '%s' "$BANNER" | grep -q "^SSH-"; then
                info "SSH banner received from the far end: $BANNER"
                echo "       This came from the remote sshd, so the tunnel is working end to end."
                E2E_PROVEN=true
            elif [ -n "$BANNER" ]; then
                fail "Got a reply, but it is not an SSH banner: $BANNER"
                echo "       The forward may point at the wrong remote_port."
            else
                fail "No SSH banner — the connection was accepted locally but nothing came back."
                echo "       Typical causes: Tox friend not online, rules.yaml denied the TUNNEL_OPEN,"
                echo "       or sshd is not listening on the configured remote_host:remote_port."
                echo "       Check the server log for TUNNEL_ERROR / 'denied'."
            fi
        else
            unproven "nc not available — cannot read the SSH banner, end-to-end NOT verified"
        fi
        echo ""
        echo "       Manual test: ssh -p $LOCAL_PORT user@127.0.0.1"
        ;;
    http)
        if command -v curl &>/dev/null; then
            # --noproxy: a system HTTP proxy (Clash/mihomo TUN, corporate proxy) would
            # otherwise intercept the loopback request and answer 502 for it.
            #
            # Do NOT infer failure from the body of -w "%{http_code}": on a connection
            # failure curl still prints "000" AND the `|| echo` fallback appends its own,
            # yielding "000000", which compares unequal to "000" and reads as success.
            # Branch on curl's exit status instead.
            HTTP_CODE=$(curl --noproxy '*' -s -o /dev/null -w '%{http_code}' \
                             --connect-timeout 5 --max-time 20 \
                             "http://127.0.0.1:$LOCAL_PORT/" 2>/dev/null)
            CURL_RC=$?
            if [ "$CURL_RC" -eq 0 ] && [ -n "$HTTP_CODE" ] && [ "$HTTP_CODE" != "000" ]; then
                info "HTTP response code from the far end: $HTTP_CODE"
                echo "       A real HTTP status came back, so the tunnel is working end to end."
                echo "       (A 4xx/5xx is still end-to-end success — the remote server answered.)"
                E2E_PROVEN=true
            else
                fail "No HTTP response (curl exit $CURL_RC, code '${HTTP_CODE:-none}')"
                echo "       The local port accepted the socket but no HTTP reply came back."
                echo "       Check: Tox friend online? rules.yaml allows remote_host:remote_port?"
                echo "       Is the web server actually running on the remote side?"
            fi
        else
            unproven "curl not available — end-to-end NOT verified"
        fi
        echo ""
        echo "       Manual test: curl --noproxy '*' http://127.0.0.1:$LOCAL_PORT/"
        ;;
    postgres)
        if command -v psql &>/dev/null; then
            # PGCONNECT_TIMEOUT bounds the libpq connect; tmo bounds the whole thing.
            PG_OUT=$(PGCONNECT_TIMEOUT=10 tmo 25 psql -h 127.0.0.1 -p "$LOCAL_PORT" \
                        -w -c "SELECT 1" 2>&1 || true)
            if printf '%s' "$PG_OUT" | grep -q "^ *1$"; then
                info "PostgreSQL answered SELECT 1 — end-to-end verified"
                E2E_PROVEN=true
            elif printf '%s' "$PG_OUT" | grep -qiE "authentication|password|role .* does not exist|database .* does not exist|no pg_hba"; then
                info "PostgreSQL answered with an auth/database error — the server is reachable"
                echo "       (${PG_OUT%%$'\n'*})"
                echo "       A protocol-level reply proves the tunnel end to end; only the"
                echo "       credentials are missing."
                E2E_PROVEN=true
            else
                fail "No PostgreSQL protocol reply through the tunnel"
                echo "       ${PG_OUT%%$'\n'*}"
            fi
        else
            unproven "psql not available — end-to-end NOT verified"
        fi
        echo ""
        echo "       Manual test: psql -h 127.0.0.1 -p $LOCAL_PORT -U <user> -d <dbname>"
        ;;
    mysql)
        if command -v mysql &>/dev/null; then
            MY_OUT=$(tmo 25 mysql -h 127.0.0.1 -P "$LOCAL_PORT" --protocol=TCP \
                        --connect-timeout=10 -e "SELECT 1" 2>&1 || true)
            if printf '%s' "$MY_OUT" | grep -q "^1$"; then
                info "MySQL answered SELECT 1 — end-to-end verified"
                E2E_PROVEN=true
            elif printf '%s' "$MY_OUT" | grep -qiE "access denied|using password|unknown database"; then
                info "MySQL answered with an auth error — the server is reachable"
                echo "       (${MY_OUT%%$'\n'*})"
                echo "       A protocol-level reply proves the tunnel end to end."
                E2E_PROVEN=true
            else
                fail "No MySQL protocol reply through the tunnel"
                echo "       ${MY_OUT%%$'\n'*}"
            fi
        else
            unproven "mysql client not available — end-to-end NOT verified"
        fi
        echo ""
        echo "       Manual test: mysql -h 127.0.0.1 -P $LOCAL_PORT -u <user> -p"
        ;;
    redis)
        if command -v redis-cli &>/dev/null; then
            PONG=$(tmo 20 redis-cli -h 127.0.0.1 -p "$LOCAL_PORT" -t 10 ping 2>&1 || true)
            if [ "$PONG" = "PONG" ]; then
                info "Redis answered PONG — end-to-end verified"
                E2E_PROVEN=true
            elif printf '%s' "$PONG" | grep -qiE "NOAUTH|WRONGPASS|DENIED"; then
                info "Redis answered with an auth error ($PONG) — the server is reachable"
                echo "       A protocol-level reply proves the tunnel end to end."
                E2E_PROVEN=true
            else
                fail "Redis did not answer PING through the tunnel (got: ${PONG:-nothing})"
            fi
        else
            unproven "redis-cli not available — end-to-end NOT verified"
        fi
        echo ""
        echo "       Manual test: redis-cli -h 127.0.0.1 -p $LOCAL_PORT ping"
        ;;
    mongo)
        MONGO_BIN=""
        command -v mongosh &>/dev/null && MONGO_BIN=mongosh
        [ -z "$MONGO_BIN" ] && command -v mongo &>/dev/null && MONGO_BIN=mongo
        if [ -n "$MONGO_BIN" ]; then
            MG_OUT=$(tmo 30 "$MONGO_BIN" --host 127.0.0.1 --port "$LOCAL_PORT" --quiet \
                        --eval 'db.runCommand({ping:1}).ok' 2>&1 || true)
            if printf '%s' "$MG_OUT" | grep -q '^1$'; then
                info "MongoDB answered ping — end-to-end verified"
                E2E_PROVEN=true
            elif printf '%s' "$MG_OUT" | grep -qiE "requires authentication|Authentication failed|not authorized"; then
                info "MongoDB answered with an auth error — the server is reachable"
                echo "       A protocol-level reply proves the tunnel end to end."
                E2E_PROVEN=true
            else
                fail "No MongoDB protocol reply through the tunnel"
                echo "       ${MG_OUT%%$'\n'*}"
            fi
        else
            unproven "mongosh/mongo not available — end-to-end NOT verified"
        fi
        echo ""
        echo "       Manual test: mongosh --host 127.0.0.1 --port $LOCAL_PORT"
        ;;
    rdp)
        # RDP's X.224 Connection Request is cheap to send and the server replies with
        # a Connection Confirm, so this IS a real end-to-end probe when python3 exists.
        if command -v python3 &>/dev/null; then
            if tmo 20 python3 - "$LOCAL_PORT" <<'PYEOF'
import socket, sys
# X.224 Connection Request (RDP negotiation), 19 bytes.
req = bytes([0x03,0x00,0x00,0x13,0x0e,0xe0,0x00,0x00,0x00,0x00,0x00,
             0x01,0x00,0x08,0x00,0x00,0x00,0x00,0x00])
try:
    s = socket.create_connection(("127.0.0.1", int(sys.argv[1])), timeout=10)
    s.settimeout(10)
    s.sendall(req)
    data = s.recv(64)
    s.close()
except Exception:
    sys.exit(1)
# TPKT version 3, and a plausible X.224 Connection Confirm.
sys.exit(0 if len(data) >= 4 and data[0] == 0x03 else 1)
PYEOF
            then
                info "RDP server replied to an X.224 Connection Request — end-to-end verified"
                E2E_PROVEN=true
            else
                fail "No RDP protocol reply through the tunnel"
                echo "       The local port accepted the socket but the remote RDP host did not answer."
                echo "       Check the Tox link, rules.yaml, and that RDP is enabled on the target."
            fi
        else
            unproven "python3 not available — cannot send an RDP probe, end-to-end NOT verified"
            echo "       A local TCP accept does NOT show the remote desktop is reachable."
        fi
        echo ""
        echo "       Manual test: open your RDP client and connect to 127.0.0.1:$LOCAL_PORT"
        if [ "$(uname)" = "Darwin" ]; then
            echo "       macOS: open 'rdp://full%20address=s:127.0.0.1:$LOCAL_PORT'"
        fi
        ;;
    tcp)
        unproven "Generic TCP: there is no protocol-agnostic way to prove the far end answered."
        echo "       Everything above is local to this machine. Use the real application,"
        echo "       or re-run with a specific service type, to confirm the tunnel end to end."
        echo "       Also useful: toxtunnel inspect tunnels -c <client.yaml> — a tunnel that"
        echo "       appears there with advancing BYTES_IN/BYTES_OUT is genuinely carrying data."
        ;;
esac

echo ""
echo "===== Verification Summary ====="
if [ "$FAILURES" -gt 0 ]; then
    echo -e "${RED}FAILED${NC} — $FAILURES check(s) failed. The tunnel is not working."
    exit 1
elif [ "$E2E_PROVEN" = true ]; then
    echo -e "${GREEN}VERIFIED${NC} — the remote service answered through the tunnel."
    exit 0
else
    echo -e "${YELLOW}NOT PROVEN${NC} — local checks passed, but nothing confirmed the far end"
    echo "responded. Do NOT report this as a working tunnel. Exit code 2."
    exit 2
fi
