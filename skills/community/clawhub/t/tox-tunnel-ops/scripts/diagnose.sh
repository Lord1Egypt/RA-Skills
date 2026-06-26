#!/usr/bin/env bash
# tox-tunnel-ops diagnostic script
# Usage: bash diagnose.sh [config_file]
#
# Runs a layered diagnostic checklist for tox-tcp-tunnel issues.
# Exits with 0 if all checks pass, 1 if any issue is found.

set -uo pipefail

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

CONFIG_FILE="${1:-}"
ISSUES=0

info()  { echo -e "${GREEN}[OK]${NC}    $1"; }
warn()  { echo -e "${YELLOW}[WARN]${NC}  $1"; ISSUES=$((ISSUES + 1)); }
fail()  { echo -e "${RED}[FAIL]${NC}  $1"; ISSUES=$((ISSUES + 1)); }
section() { echo -e "\n${CYAN}--- $1 ---${NC}"; }

echo "===== tox-tunnel-ops Diagnostic ====="

# =========================================================================
# Layer 1: Process & Binary
# =========================================================================
section "Layer 1: Process & Binary"

if command -v toxtunnel &>/dev/null; then
    TOXTUNNEL_PATH=$(command -v toxtunnel)
    info "toxtunnel found at: $TOXTUNNEL_PATH"
else
    fail "toxtunnel not found in PATH"
    echo "     Install: build from source or check your PATH"
fi

PROCS=$(ps aux 2>/dev/null | grep -v grep | grep toxtunnel || true)
if [ -n "$PROCS" ]; then
    info "toxtunnel process(es) running:"
    echo "$PROCS" | while IFS= read -r line; do
        echo "       $line"
    done
else
    warn "No toxtunnel process found running"
fi

# =========================================================================
# Layer 2: Configuration Static Check
# =========================================================================
section "Layer 2: Configuration Static Check"

if [ -n "$CONFIG_FILE" ]; then
    if [ -f "$CONFIG_FILE" ]; then
        info "Config file exists: $CONFIG_FILE"

        # YAML syntax validation (secure: pass path as argument, not inline)
        if command -v python3 &>/dev/null; then
            if python3 -c "import yaml, sys; yaml.safe_load(open(sys.argv[1]))" "$CONFIG_FILE" 2>/dev/null; then
                info "Config YAML syntax is valid"
            elif python3 -c "
import sys, json
# Fallback: basic YAML structure check without PyYAML
with open(sys.argv[1]) as f:
    content = f.read()
# Check for tabs (YAML requires spaces)
if '\t' in content:
    sys.exit(1)
# Check basic key: value structure
lines = [l for l in content.split('\n') if l.strip() and not l.strip().startswith('#')]
if not any(':' in l for l in lines):
    sys.exit(1)
sys.exit(0)
" "$CONFIG_FILE" 2>/dev/null; then
                info "Config YAML syntax looks valid (basic check — install PyYAML for full validation)"
            else
                fail "Config YAML syntax is INVALID — check indentation (use spaces, not tabs)"
            fi
        else
            warn "python3 not available — cannot validate YAML syntax"
        fi

        # Extract mode
        MODE=$(grep -E "^mode:" "$CONFIG_FILE" 2>/dev/null | awk '{print $2}' || true)
        if [ -n "$MODE" ]; then
            info "Mode: $MODE"
        else
            fail "No 'mode:' field found in config"
        fi

        # Check data_dir
        DATA_DIR=$(grep -E "^data_dir:" "$CONFIG_FILE" 2>/dev/null | awk '{print $2}' | tr -d '"' | tr -d "'" || true)
        if [ -n "$DATA_DIR" ]; then
            # Expand ~ if present
            DATA_DIR="${DATA_DIR/#\~/$HOME}"
            if [ -d "$DATA_DIR" ]; then
                info "data_dir exists: $DATA_DIR"
                if [ -w "$DATA_DIR" ]; then
                    info "data_dir is writable"
                else
                    fail "data_dir is NOT writable: $DATA_DIR"
                fi
                if [ -f "$DATA_DIR/tox_save.dat" ]; then
                    info "tox_save.dat found (Tox identity exists)"
                else
                    warn "tox_save.dat not found — first run will create a new identity"
                fi
            else
                warn "data_dir does not exist: $DATA_DIR (will be created on first run)"
            fi
        fi

        # Client-specific checks
        if [ "$MODE" = "client" ]; then
            SERVER_ID=$(grep -E "server_id:" "$CONFIG_FILE" 2>/dev/null | awk '{print $2}' | tr -d '"' | tr -d "'" || true)
            if [ -n "$SERVER_ID" ] && [ "$SERVER_ID" != "<PASTE_SERVER_TOX_ID_HERE>" ]; then
                ID_LEN=${#SERVER_ID}
                if [ "$ID_LEN" -eq 76 ]; then
                    info "server_id is 76 chars (literal Tox ID)"
                else
                    # v0.2.0+: a non-76-char server_id is treated as an alias
                    # that resolves via <data_dir>/known_servers.yaml at startup.
                    KS="${DATA_DIR:-}/known_servers.yaml"
                    if [ -n "${DATA_DIR:-}" ] && [ -f "$KS" ] && \
                       grep -qE "^[[:space:]]*alias:[[:space:]]*\"?${SERVER_ID}\"?[[:space:]]*$" "$KS"; then
                        info "server_id is alias '$SERVER_ID' — resolves via $KS"
                    else
                        fail "server_id '$SERVER_ID' is $ID_LEN chars and has no matching alias in ${KS:-known_servers.yaml} (need 76-char Tox ID or registered alias)"
                    fi
                fi
            else
                fail "server_id is not set — paste the server's Tox ID or an alias from 'toxtunnel servers list'"
            fi

            # Check forwards
            FWD_COUNT=$(grep -c "local_port:" "$CONFIG_FILE" 2>/dev/null || echo "0")
            if [ "$FWD_COUNT" -gt 0 ]; then
                info "Found $FWD_COUNT port forward(s)"
            else
                warn "No port forwards configured in client config"
            fi
        fi

        # Server-specific: check rules_file
        if [ "$MODE" = "server" ]; then
            RULES_FILE=$(grep -E "rules_file:" "$CONFIG_FILE" 2>/dev/null | awk '{print $2}' | tr -d '"' | tr -d "'" || true)
            if [ -n "$RULES_FILE" ]; then
                # Resolve relative path against config dir
                CONFIG_DIR=$(dirname "$CONFIG_FILE")
                if [[ "$RULES_FILE" != /* ]]; then
                    RULES_FILE="$CONFIG_DIR/$RULES_FILE"
                fi
                if [ -f "$RULES_FILE" ]; then
                    info "rules_file exists: $RULES_FILE"

                    # Validate rules YAML
                    if command -v python3 &>/dev/null; then
                        if python3 -c "import yaml, sys; yaml.safe_load(open(sys.argv[1]))" "$RULES_FILE" 2>/dev/null; then
                            info "rules.yaml syntax is valid"
                        elif ! grep -q "	" "$RULES_FILE" 2>/dev/null; then
                            info "rules.yaml syntax looks valid (install PyYAML for full validation)"
                        else
                            fail "rules.yaml syntax is INVALID"
                        fi
                    fi
                else
                    fail "rules_file not found: $RULES_FILE"
                fi
            else
                warn "No rules_file configured — server is default-deny and will refuse all incoming friend requests/tunnels"
            fi
        fi
    else
        fail "Config file not found: $CONFIG_FILE"
    fi
else
    warn "No config file specified — pass config path as argument"
    echo "     Usage: bash diagnose.sh /path/to/config.yaml"
fi

# =========================================================================
# Layer 3: Rules Risk Analysis
# =========================================================================
section "Layer 3: Rules Risk Analysis"

if [ -n "${RULES_FILE:-}" ] && [ -f "${RULES_FILE:-}" ] && command -v python3 &>/dev/null; then
    # Check if PyYAML is available
    if ! python3 -c "import yaml" 2>/dev/null; then
        warn "PyYAML not installed — cannot analyze rules risk (pip3 install pyyaml)"
    else
    RISK_OUTPUT=$(python3 - "$RULES_FILE" 2>/dev/null <<'PYEOF'
import yaml, sys, re

try:
    data = yaml.safe_load(open(sys.argv[1]))
except Exception as e:
    print(f"FAIL: Cannot parse rules file: {e}")
    sys.exit(0)

if not data:
    print("WARN: Rules file is empty — default deny all")
    sys.exit(0)

rules = data if isinstance(data, list) else data.get("rules", [])
if not rules:
    print("WARN: No rules defined — default deny all")
    sys.exit(0)

risks = []
for i, rule in enumerate(rules):
    fk = rule.get("friend") or rule.get("friend_pk", "")

    # Check friend key format
    if len(fk) != 64:
        risks.append(f"HIGH: Rule #{i+1}: friend key is {len(fk)} chars (expected 64 hex)")
    elif not re.match(r'^[0-9A-Fa-f]{64}$', fk):
        risks.append(f"HIGH: Rule #{i+1}: friend key contains non-hex characters")

    # Check overly broad allows
    for allow in rule.get("allow", []):
        host = allow.get("host", "")
        ports = allow.get("ports", [])
        if host == "*" and not ports:
            risks.append(f"HIGH: Rule #{i+1}: allows ALL hosts + ALL ports (wide open)")
        elif host == "*":
            risks.append(f"MEDIUM: Rule #{i+1}: allows ALL hosts on ports {ports}")
        elif not ports:
            risks.append(f"MEDIUM: Rule #{i+1}: allows ALL ports on host '{host}'")

    # Check for rules with allow but no deny
    if rule.get("allow") and not rule.get("deny"):
        pass  # Normal — deny-takes-precedence model handles this

for r in risks:
    print(r)

if not risks:
    print("OK: No risk issues found in rules")
PYEOF
    ) || true

    if [ -n "$RISK_OUTPUT" ]; then
        while IFS= read -r line; do
            if echo "$line" | grep -q "^HIGH"; then
                fail "$line"
            elif echo "$line" | grep -q "^MEDIUM"; then
                warn "$line"
            elif echo "$line" | grep -q "^WARN"; then
                warn "$line"
            elif echo "$line" | grep -q "^OK"; then
                info "$line"
            elif echo "$line" | grep -q "^FAIL"; then
                fail "$line"
            else
                echo "       $line"
            fi
        done <<< "$RISK_OUTPUT"
    fi
    fi  # end PyYAML available check
else
    if [ -z "${RULES_FILE:-}" ]; then
        info "No rules file to analyze (skipped)"
    elif [ ! -f "${RULES_FILE:-}" ]; then
        warn "Rules file not found — cannot analyze"
    else
        warn "python3 not available — cannot perform rules risk analysis"
    fi
fi

# =========================================================================
# Layer 4: Network & Tox Connection
# =========================================================================
section "Layer 4: Network & Tox Connection"

# Check internet connectivity
PING_OK=false
if [[ "$(uname)" == "Darwin" ]]; then
    ping -c 1 -W 2000 1.1.1.1 &>/dev/null && PING_OK=true
else
    ping -c 1 -W 2 1.1.1.1 &>/dev/null && PING_OK=true
fi
if [ "$PING_OK" = true ]; then
    info "Internet connectivity: OK"
else
    BOOTSTRAP_MODE=$(grep -E "bootstrap_mode:" "${CONFIG_FILE:-/dev/null}" 2>/dev/null | awk '{print $2}' || true)
    if [ "$BOOTSTRAP_MODE" = "lan" ]; then
        info "Internet not reachable (OK — using LAN bootstrap mode)"
    else
        warn "Internet connectivity: FAILED — auto bootstrap mode requires internet"
        echo "     If both machines are on the same LAN, use bootstrap_mode: lan"
    fi
fi

# Check Tox port
TOX_PORT=$(grep -E "tcp_port:" "${CONFIG_FILE:-/dev/null}" 2>/dev/null | awk '{print $2}' || echo "33445")
if command -v lsof &>/dev/null; then
    TOX_PORT_CHECK=$(lsof -i :"$TOX_PORT" 2>/dev/null || true)
    if [ -n "$TOX_PORT_CHECK" ]; then
        info "Tox port $TOX_PORT is in use (expected if toxtunnel is running)"
    fi
fi

# =========================================================================
# Layer 5: Port & Tunnel Connectivity
# =========================================================================
section "Layer 5: Port & Tunnel Connectivity"

if [ -n "${CONFIG_FILE:-}" ] && [ -f "${CONFIG_FILE:-}" ]; then
    PORTS=$(grep -E "local_port:" "$CONFIG_FILE" 2>/dev/null | sed 's/.*local_port:\s*//' | tr -d '"' | tr -d "'" | tr -d ' ' || true)
    for PORT in $PORTS; do
        if command -v lsof &>/dev/null; then
            PORT_USER=$(lsof -i :"$PORT" -sTCP:LISTEN 2>/dev/null | tail -1 || true)
            if [ -n "$PORT_USER" ]; then
                PROC_NAME=$(echo "$PORT_USER" | awk '{print $1}')
                if echo "$PROC_NAME" | grep -qi toxtunnel; then
                    info "Port $PORT is listening (toxtunnel)"
                else
                    fail "Port $PORT is occupied by: $PROC_NAME — toxtunnel cannot bind"
                fi
            else
                warn "Port $PORT is not listening — client may not be running or not connected yet"
            fi
        fi

        # Smoke test: try TCP connect
        if command -v nc &>/dev/null; then
            if nc -z -w 3 127.0.0.1 "$PORT" 2>/dev/null; then
                info "Port $PORT: TCP connect OK"
            else
                warn "Port $PORT: TCP connect failed"
            fi
        fi
    done

    if [ -z "$PORTS" ]; then
        info "No local_port entries found (server mode or pipe mode)"
    fi
fi

# =========================================================================
# Layer 6: Log Keywords
# =========================================================================
section "Layer 6: Log Analysis"

if [ -n "${CONFIG_FILE:-}" ] && [ -f "${CONFIG_FILE:-}" ]; then
    LOG_FILE=$(grep -A3 "logging:" "$CONFIG_FILE" 2>/dev/null | grep "file:" 2>/dev/null | awk '{print $2}' | tr -d '"' | tr -d "'" || true)
    if [ -n "$LOG_FILE" ] && [ -f "$LOG_FILE" ]; then
        info "Log file found: $LOG_FILE"

        if grep -q "Connected to DHT" "$LOG_FILE" 2>/dev/null; then
            info "DHT connection: established"
        else
            warn "DHT connection: not found in logs"
        fi

        if grep -q "Self connection status: Online" "$LOG_FILE" 2>/dev/null; then
            info "Self connection: Online"
        fi

        if grep -q "Friend connection status: Connected" "$LOG_FILE" 2>/dev/null; then
            info "Friend connection: established"
        else
            warn "Friend connection: not established (or not in logs)"
        fi

        ERRORS=$(grep -ci "error" "$LOG_FILE" 2>/dev/null || echo "0")
        if [ "$ERRORS" -gt 0 ]; then
            warn "Found $ERRORS error(s) in log. Last 5:"
            grep -i "error" "$LOG_FILE" 2>/dev/null | tail -5 | while IFS= read -r line; do
                echo "       $line"
            done
        else
            info "No errors in log"
        fi

        # Check for specific known issues
        if grep -q "Invalid public key" "$LOG_FILE" 2>/dev/null; then
            fail "Log contains 'Invalid public key' — check rules.yaml friend keys (must be 64 hex chars)"
        fi
        if grep -q "Rules file not found" "$LOG_FILE" 2>/dev/null; then
            fail "Log contains 'Rules file not found' — check rules_file path in server config"
        fi
        if grep -q "Failed to bind" "$LOG_FILE" 2>/dev/null; then
            fail "Log contains 'Failed to bind' — port already in use"
        fi
    else
        warn "No log file configured or file not found — run with -l debug for verbose output"
        echo "     Tip: add to config: logging: { level: debug, file: /tmp/toxtunnel.log }"
    fi
fi

# =========================================================================
# Summary
# =========================================================================
echo ""
echo "===== Diagnostic Complete ====="
if [ "$ISSUES" -gt 0 ]; then
    echo -e "${YELLOW}Found $ISSUES issue(s). Review the items above.${NC}"
    exit 1
else
    echo -e "${GREEN}All checks passed.${NC}"
    exit 0
fi
