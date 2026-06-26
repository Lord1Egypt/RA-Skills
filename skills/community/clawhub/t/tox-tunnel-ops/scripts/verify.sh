#!/usr/bin/env bash
# tox-tunnel-ops verification script
# Usage: bash verify.sh <local_port> [expected_service]
#
# Verifies that a tox-tcp-tunnel forwarded port is working.
# expected_service: ssh | http | postgres | mysql | redis | mongo | rdp | tcp (default: tcp)

set -uo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

LOCAL_PORT="${1:-}"
SERVICE="${2:-tcp}"

if [ -z "$LOCAL_PORT" ]; then
    echo "Usage: bash verify.sh <local_port> [ssh|http|postgres|mysql|redis|mongo|rdp|tcp]"
    exit 1
fi

info()  { echo -e "${GREEN}[OK]${NC}    $1"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $1"; }
fail()  { echo -e "${RED}[FAIL]${NC}  $1"; }

echo "===== Tunnel Verification: port $LOCAL_PORT ($SERVICE) ====="
echo ""

# --- Step 1: Port listening check ---
echo "--- Step 1: Port Check ---"
LISTENER=""
if command -v lsof &>/dev/null; then
    LISTENER=$(lsof -i :"$LOCAL_PORT" -sTCP:LISTEN 2>/dev/null | tail -1 || true)
elif command -v ss &>/dev/null; then
    LISTENER=$(ss -tlnp 2>/dev/null | grep ":$LOCAL_PORT " || true)
fi

if [ -n "$LISTENER" ]; then
    info "Port $LOCAL_PORT is listening"
else
    fail "Port $LOCAL_PORT is NOT listening"
    echo "     Is the toxtunnel client running with the correct config?"
    exit 1
fi

echo ""

# --- Step 2: TCP connectivity ---
echo "--- Step 2: TCP Connectivity ---"
TCP_OK=false
if command -v nc &>/dev/null; then
    if nc -z -w 5 127.0.0.1 "$LOCAL_PORT" 2>/dev/null; then
        info "TCP connection to 127.0.0.1:$LOCAL_PORT succeeded"
        TCP_OK=true
    else
        fail "TCP connection to 127.0.0.1:$LOCAL_PORT failed"
        echo "     Port is listening but tunnel may not be connected yet."
        echo "     Check if the Tox friend connection is established."
    fi
else
    # Fallback: bash /dev/tcp
    if (echo >/dev/tcp/127.0.0.1/"$LOCAL_PORT") 2>/dev/null; then
        info "TCP connection to 127.0.0.1:$LOCAL_PORT succeeded"
        TCP_OK=true
    else
        fail "TCP connection to 127.0.0.1:$LOCAL_PORT failed"
    fi
fi

if [ "$TCP_OK" = false ]; then
    exit 1
fi

echo ""

# --- Step 3: Service-specific verification ---
echo "--- Step 3: Service Verification ($SERVICE) ---"

case "$SERVICE" in
    ssh)
        if command -v nc &>/dev/null; then
            BANNER=$(echo "" | nc -w 3 127.0.0.1 "$LOCAL_PORT" 2>/dev/null | head -1 || true)
            if echo "$BANNER" | grep -qi "SSH"; then
                info "SSH banner received: $BANNER"
            else
                warn "No SSH banner — service may not be SSH, or connection was not forwarded"
            fi
        else
            warn "nc not available — cannot check SSH banner"
        fi
        echo ""
        echo "     Test: ssh -p $LOCAL_PORT user@127.0.0.1"
        ;;
    http)
        if command -v curl &>/dev/null; then
            HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" --connect-timeout 5 "http://127.0.0.1:$LOCAL_PORT/" 2>/dev/null || echo "000")
            if [ "$HTTP_CODE" != "000" ]; then
                info "HTTP response code: $HTTP_CODE"
            else
                fail "No HTTP response — web server may not be running on the remote side"
            fi
        else
            warn "curl not available — cannot test HTTP"
        fi
        echo ""
        echo "     Test: curl http://127.0.0.1:$LOCAL_PORT/"
        ;;
    postgres)
        if command -v psql &>/dev/null; then
            if psql -h 127.0.0.1 -p "$LOCAL_PORT" -c "SELECT 1" 2>/dev/null | grep -q "1"; then
                info "PostgreSQL responded to SELECT 1"
            else
                warn "PostgreSQL did not respond (may need credentials)"
            fi
        else
            warn "psql not available"
        fi
        echo ""
        echo "     Test: psql -h 127.0.0.1 -p $LOCAL_PORT -U <user> -d <dbname>"
        ;;
    mysql)
        if command -v mysql &>/dev/null; then
            if mysql -h 127.0.0.1 -P "$LOCAL_PORT" -e "SELECT 1" 2>/dev/null | grep -q "1"; then
                info "MySQL responded to SELECT 1"
            else
                warn "MySQL did not respond (may need credentials)"
            fi
        else
            warn "mysql client not available"
        fi
        echo ""
        echo "     Test: mysql -h 127.0.0.1 -P $LOCAL_PORT -u <user> -p"
        ;;
    redis)
        if command -v redis-cli &>/dev/null; then
            PONG=$(redis-cli -h 127.0.0.1 -p "$LOCAL_PORT" ping 2>/dev/null || true)
            if [ "$PONG" = "PONG" ]; then
                info "Redis responded: PONG"
            else
                warn "Redis did not respond with PONG"
            fi
        else
            warn "redis-cli not available"
        fi
        echo ""
        echo "     Test: redis-cli -h 127.0.0.1 -p $LOCAL_PORT ping"
        ;;
    mongo)
        if command -v mongosh &>/dev/null; then
            echo "     Test: mongosh --host 127.0.0.1 --port $LOCAL_PORT"
        elif command -v mongo &>/dev/null; then
            echo "     Test: mongo --host 127.0.0.1 --port $LOCAL_PORT"
        else
            warn "mongosh/mongo not available"
            echo "     Install mongosh and run: mongosh --host 127.0.0.1 --port $LOCAL_PORT"
        fi
        ;;
    rdp)
        info "RDP verification: TCP connection succeeded"
        echo "     RDP does not have a simple banner check."
        echo "     Test: open your RDP client and connect to 127.0.0.1:$LOCAL_PORT"
        if [[ "$(uname)" == "Darwin" ]]; then
            echo "     macOS: open 'rdp://full%20address=s:127.0.0.1:$LOCAL_PORT'"
        fi
        ;;
    tcp|*)
        info "Generic TCP connection works."
        echo "     Use your application to verify end-to-end connectivity."
        ;;
esac

echo ""
echo "===== Verification Complete ====="
