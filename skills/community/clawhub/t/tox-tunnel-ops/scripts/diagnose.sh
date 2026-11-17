#!/usr/bin/env bash
# tox-tunnel-ops diagnostic script
# Usage: bash scripts/diagnose.sh [config_file]
#
# Runs a layered diagnostic checklist for tox-tcp-tunnel issues.
#
# Exit codes:
#   0  no issues found
#   1  at least one WARN or FAIL was reported
#
# Design note: config validation is delegated to the product's own validator,
# `toxtunnel config check --strict` (v0.4.11+). Ad-hoc grep/awk parsing of YAML
# gets quoting, lists and comments wrong, so this script only parses YAML with a
# real parser (PyYAML) and says so plainly when one is not available. It never
# claims a config is valid on the strength of a heuristic.

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
note()  { echo -e "${CYAN}[NOTE]${NC}  $1"; }          # informational, not an issue
skip()  { echo -e "${YELLOW}[SKIP]${NC}  $1"; }        # could not check — not a pass
section() { echo -e "\n${CYAN}--- $1 ---${NC}"; }

# Portable timeout wrapper, same shape as verify.sh: coreutils `timeout` where
# available, GNU `gtimeout` on a macOS box with coreutils installed, else run
# bare. Calling `timeout` directly turns every probe below into a false warning
# on a stock macOS, which has neither.
if command -v timeout &>/dev/null; then
    tmo() { timeout "$@"; }
elif command -v gtimeout &>/dev/null; then
    tmo() { gtimeout "$@"; }
else
    tmo() { shift; "$@"; }
fi

# Values discovered by the structured parse (Layer 2), consumed by later layers.
MODE=""
DATA_DIR=""
RULES_FILE=""          # as written in the config
RULES_FILE_RESOLVED=""  # what the daemon would actually open, given its CWD
LOG_FILE=""
FWD_PORTS=""
SERVER_IDS=""
HAVE_PYYAML=false

echo "===== tox-tunnel-ops Diagnostic ====="

# =========================================================================
# Layer 1: Process & Binary
# =========================================================================
section "Layer 1: Process & Binary"

TOXTUNNEL_BIN=""
if command -v toxtunnel &>/dev/null; then
    TOXTUNNEL_BIN=$(command -v toxtunnel)
    TT_VERSION=$(toxtunnel --version 2>/dev/null | head -1 || true)
    info "toxtunnel found at: $TOXTUNNEL_BIN (version ${TT_VERSION:-unknown})"
else
    fail "toxtunnel not found in PATH"
    echo "       Install a release package, or add the binary's directory to PATH."
fi

# pgrep -x matches the process NAME only. Never use `pgrep -f toxtunnel` here:
# -f matches the whole command line, so it also matches this very script, the
# shell that launched it, and any SSH/CI wrapper that mentions toxtunnel.
if command -v pgrep &>/dev/null; then
    TT_PIDS=$(pgrep -x toxtunnel 2>/dev/null || true)
else
    TT_PIDS=""
fi
if [ -n "$TT_PIDS" ]; then
    info "toxtunnel process(es) running: $(echo "$TT_PIDS" | tr '\n' ' ')"
    for p in $TT_PIDS; do
        ps -o pid=,args= -p "$p" 2>/dev/null | sed 's/^/       /'
    done
else
    warn "No toxtunnel process found running (pgrep -x toxtunnel)"
fi

# =========================================================================
# Layer 2: Configuration Validation
# =========================================================================
section "Layer 2: Configuration Validation"

if [ -z "$CONFIG_FILE" ]; then
    warn "No config file specified — most checks below cannot run"
    echo "       Usage: bash scripts/diagnose.sh /path/to/config.yaml"
elif [ ! -f "$CONFIG_FILE" ]; then
    fail "Config file not found: $CONFIG_FILE"
    CONFIG_FILE=""
else
    info "Config file exists: $CONFIG_FILE"

    # ---- 2a. The product's own validator, first and authoritative ----------
    if [ -n "$TOXTUNNEL_BIN" ]; then
        CHECK_OUT=$(toxtunnel config check -c "$CONFIG_FILE" --strict 2>&1)
        CHECK_RC=$?
        if [ "$CHECK_RC" -eq 0 ]; then
            info "toxtunnel config check --strict: PASSED"
            [ -n "$CHECK_OUT" ] && printf '%s\n' "$CHECK_OUT" | sed 's/^/       /'
        elif [ "$(printf '%s\n' "$CHECK_OUT" | grep -c .)" -eq 1 ] &&
             printf '%s' "$CHECK_OUT" | grep -q "Server ID must be 76 characters"; then
            # Known false positive (v0.4.12): `config check` does NOT resolve
            # known-servers aliases, while the daemon does. A registered alias in
            # client.server_id therefore always fails this check even though the
            # daemon starts fine. Verified against the v0.4.12 binary.
            # note(), not warn(): warn() increments ISSUES and would make the
            # whole script exit 1 on a config that is actually fine. This is a
            # known config-check limitation on daemons before v0.4.13, and the
            # alias is verified properly against known_servers.yaml below.
            note "toxtunnel config check --strict rejected the server_id length"
            printf '%s\n' "$CHECK_OUT" | sed 's/^/       /'
            echo "       This is a KNOWN LIMITATION of config check BEFORE v0.4.13,"
            echo "       not necessarily a real error: those builds do not resolve"
            echo "       known-servers aliases, so any alias-form client.server_id"
            echo "       fails. v0.4.13+ resolves them and this will not fire. The alias check"
            echo "       below is the one that matters. If it passes, the daemon will"
            echo "       resolve the alias and start normally."
        else
            fail "toxtunnel config check --strict FAILED (exit $CHECK_RC)"
            printf '%s\n' "$CHECK_OUT" | sed 's/^/       /'
            echo "       Fix these before looking at anything else — the daemon"
            echo "       applies the same validation at startup."
        fi
        echo "       (Scope: on v0.4.13 and older, config check validates the main config"
        echo "        only and does NOT open server.rules_file; v0.5.0+ loads and parses"
        echo "        it. Layer 3 covers the semantics no version checks.)"
    else
        skip "toxtunnel binary unavailable — cannot run the authoritative validator"
        echo "       Install toxtunnel and re-run; the checks below are a weaker substitute."
    fi

    # ---- 2b. Structured read of the things config check does not cover -----
    if command -v python3 &>/dev/null && python3 -c "import yaml" 2>/dev/null; then
        HAVE_PYYAML=true
    fi

    if [ "$HAVE_PYYAML" = false ]; then
        skip "PyYAML not available — cannot read the config structurally"
        echo "       Install it (pip3 install pyyaml) for data_dir / forwards / rules checks."
        echo "       No conclusion about this config's contents is being drawn."
    else
        PARSE_OUT=$(python3 - "$CONFIG_FILE" <<'PYEOF'
import os, sys, yaml

cfg_path = sys.argv[1]
out = []


def emit(level, msg):
    out.append(f"{level}\t{msg}")


def setv(key, value):
    out.append(f"SET\t{key}\t{value}")


try:
    with open(cfg_path) as f:
        cfg = yaml.safe_load(f)
except Exception as e:
    emit("FAIL", f"Cannot parse config YAML: {e}")
    print("\n".join(out))
    sys.exit(0)

if not isinstance(cfg, dict):
    emit("FAIL", "Config root is not a YAML mapping")
    print("\n".join(out))
    sys.exit(0)

mode = cfg.get("mode")
if mode in ("server", "client"):
    emit("OK", f"Mode: {mode}")
    setv("MODE", mode)
else:
    emit("FAIL", f"'mode:' must be 'server' or 'client' (found: {mode!r})")

# ---- data_dir -------------------------------------------------------------
data_dir = cfg.get("data_dir")
if isinstance(data_dir, str) and data_dir:
    expanded = os.path.expanduser(data_dir)
    setv("DATA_DIR", expanded)
    if os.path.isdir(expanded):
        emit("OK", f"data_dir exists: {expanded}")
        if os.access(expanded, os.W_OK):
            emit("OK", "data_dir is writable")
        else:
            emit("FAIL", f"data_dir is NOT writable: {expanded}")
        save = os.path.join(expanded, "tox_save.dat")
        if os.path.isdir(save):
            emit("FAIL", f"{save} is a DIRECTORY, not a file — the v0.4.8 Linux "
                         "packaging bug. Stop the daemon and rmdir it; the daemon "
                         "self-heals an empty one on next start.")
        elif os.path.isfile(save):
            emit("OK", "tox_save.dat found (Tox identity exists)")
        else:
            emit("NOTE", "tox_save.dat not present — the first run will mint a new "
                         "identity (and therefore a new public key)")
    else:
        emit("NOTE", f"data_dir does not exist yet: {expanded} (created on first run)")
else:
    emit("NOTE", "No data_dir set — the platform default is used "
                 "(~/.config/toxtunnel or the OS equivalent)")

# ---- logging --------------------------------------------------------------
logging = cfg.get("logging") or {}
if isinstance(logging, dict):
    lf = logging.get("file")
    if isinstance(lf, str) and lf:
        setv("LOG_FILE", os.path.expanduser(lf))

# ---- client ---------------------------------------------------------------
if mode == "client":
    client = cfg.get("client") or {}
    if not isinstance(client, dict):
        emit("FAIL", "'client:' is not a mapping")
        client = {}

    # server_id may be a scalar OR a YAML list (failover). fallback_server_ids
    # is a separate, equally valid way to name fallbacks alongside a scalar.
    sid = client.get("server_id")
    ids = []
    if isinstance(sid, str) and sid:
        ids.append(sid)
    elif isinstance(sid, list):
        ids.extend([str(x) for x in sid if x])
    fallbacks = client.get("fallback_server_ids")
    if isinstance(fallbacks, list):
        ids.extend([str(x) for x in fallbacks if x])
    elif isinstance(fallbacks, str) and fallbacks:
        ids.append(fallbacks)

    if not ids:
        emit("FAIL", "No client.server_id — paste the server's 76-char Tox ID, or an "
                     "alias registered with `toxtunnel servers add`")
    else:
        if isinstance(sid, list) or fallbacks:
            emit("OK", f"Multi-server failover configured ({len(ids)} server ID(s); "
                       "entry 0 is the preferred primary)")
        setv("SERVER_IDS", ",".join(ids))
        for one in ids:
            if one.startswith("<") and one.endswith(">"):
                emit("FAIL", f"server_id is still the placeholder {one!r} — the daemon "
                             "exits at startup before it even creates an identity")
            elif len(one) == 76 and all(c in "0123456789abcdefABCDEF" for c in one):
                emit("OK", f"server_id {one[:12]}... is a literal 76-char Tox ID")
            else:
                emit("ALIAS", one)   # resolved against known_servers.yaml by the shell

    forwards = client.get("forwards")
    socks5 = client.get("socks5") or {}
    pipe = client.get("pipe")
    has_socks = isinstance(socks5, dict) and socks5.get("enabled") is True
    if isinstance(forwards, list) and forwards:
        ports = []
        wide_binds = []  # (port, local_address|None) for the bind advisory
        for i, fw in enumerate(forwards):
            if not isinstance(fw, dict):
                emit("FAIL", f"client.forwards[{i}] is not a mapping")
                continue
            lp, rh, rp = fw.get("local_port"), fw.get("remote_host"), fw.get("remote_port")
            missing = [k for k, v in (("local_port", lp), ("remote_host", rh),
                                      ("remote_port", rp)) if v in (None, "")]
            if missing:
                emit("FAIL", f"client.forwards[{i}] is missing {', '.join(missing)}")
                continue
            ports.append(str(lp))
            la = fw.get("local_address")
            wide_binds.append((lp, la))
            _lbl = (f"[{la}]:{lp}" if la and ":" in str(la) else
                    (f"{la}:{lp}" if la else str(lp)))
            emit("OK", f"forward: local {_lbl} -> {rh}:{rp}")
            # `local_address` is the real key from v0.4.13. These are the
            # plausible-looking spellings that are NOT it, on any version.
            for stray in ("local_host", "bind", "listen", "bind_address"):
                if stray in fw:
                    emit("FAIL", f"client.forwards[{i}] has '{stray}', which ToxTunnel "
                                 "does not implement. It is silently ignored and the "
                                 "port binds the version default instead (0.0.0.0 "
                                 "before v0.5.0, 127.0.0.1 from v0.5.0).")
        if ports:
            setv("FWD_PORTS", ",".join(ports))
            # Only the forwards that actually bind wide are worth warning about.
            # A forward with an explicit loopback local_address is fine, and
            # flagging it would train the operator to ignore this line.
            def _is_loopback(addr):
                # IPv4 loopback is the whole 127/8 block, not just 127.0.0.1;
                # IPv6 loopback is ::1, which may be written with padding.
                a = str(addr).strip().strip("[]").lower()
                return a.startswith("127.") or a in ("::1", "0:0:0:0:0:0:0:1")

            def _label(addr, port):
                a = str(addr)
                return (f"[{a}]:{port}" if ":" in a else f"{a}:{port}")

            # A specific non-loopback address (192.168.1.10) binds ONE interface,
            # not all of them. Both are exposure worth flagging, but calling a
            # single-interface bind "every interface" is simply wrong.
            # Keep the three provenances apart: an absent key means the
            # version default (wildcard before v0.5.0, loopback after), an
            # explicit IPv4 wildcard is a deliberate choice, and ::
            # is the IPv6 wildcard — calling that one "every IPv4 interface" is
            # simply the wrong family.
            implicit = [str(p) for p, a in wide_binds if not a]
            # Only numeric literals are valid local_address values -- validation
            # uses asio::ip::make_address. `*` and `[::]` are how listeners are
            # DISPLAYED (ss/lsof), never what a config can contain.
            explicit_v4 = [str(p) for p, a in wide_binds
                           if a and str(a).strip() == "0.0.0.0"]
            explicit_v6 = [str(p) for p, a in wide_binds
                           if a and str(a).strip() == "::"]
            if explicit_v6:
                emit("WARN", f"{len(explicit_v6)} forward(s) bind the IPv6 wildcard (::): "
                             + ", ".join(explicit_v6) + ". Reachable on every IPv6 interface.")
            if explicit_v4:
                emit("NOTE", f"{len(explicit_v4)} forward(s) set local_address explicitly to the "
                             "IPv4 wildcard: " + ", ".join(explicit_v4) + ". Deliberate, so this "
                             "is not flagged as a mistake — but it is still open to the network.")
            wildcard = implicit
            # Anything left that is not a valid numeric literal is a config
            # error, not a bind to report: `*` and `[::]` are ss/lsof display
            # forms and make_address rejects them.
            invalid = [f"{a}" for p, a in wide_binds
                       if a and str(a).strip() in ("*", "[::]")]
            if invalid:
                emit("FAIL", "local_address must be a numeric IP literal; "
                             + ", ".join(sorted(set(invalid)))
                             + " is listener-display syntax and the daemon will reject it.")
            specific = [f"{a}:{p}" for p, a in wide_binds
                        if a and not _is_loopback(a)
                        and str(a).strip() not in ("0.0.0.0", "::", "*", "[::]")]
            if specific:
                emit("WARN", f"{len(specific)} forward(s) bind a specific non-loopback "
                             "interface: " + ", ".join(specific) + ". Reachable by any host "
                             "on that network — intended only if the forward is meant to "
                             "serve other machines.")
            wide = wildcard
            if wide:
                emit("WARN", f"{len(wide)} static forward(s) have no local_address: "
                             + ", ".join(wide) + ". What they bind depends on the daemon "
                             "version: every IPv4 interface before v0.5.0 (any host that "
                             "can reach this machine gets the forwarded service "
                             "unauthenticated), loopback only from v0.5.0 (other machines "
                             "silently lose access). Set the key explicitly — "
                             "`local_address: 127.0.0.1` or `0.0.0.0` (v0.4.13+); on "
                             "v0.4.12 and older there is no such key and the bind is "
                             "always wide, so use a host firewall rule or a "
                             "loopback-only SOCKS5 listener instead.")
    elif has_socks:
        emit("OK", "No static forwards; SOCKS5 listener is enabled instead")
    elif pipe:
        emit("OK", "No static forwards; pipe mode is configured instead")
    else:
        emit("WARN", "Client has no forwards, no socks5, and no pipe — it will connect "
                     "to the server and then do nothing")

    if has_socks and pipe:
        emit("FAIL", "client.socks5 and client.pipe cannot both be enabled "
                     "(the validator rejects this)")
    if has_socks:
        listen = str(socks5.get("listen", ""))
        host = listen.rsplit(":", 1)[0].strip("[]") if ":" in listen else listen
        if host and host not in ("127.0.0.1", "::1", "localhost"):
            emit("FAIL", f"client.socks5.listen '{listen}' is not loopback — the "
                         "validator rejects it, and SOCKS5 has no authentication")
        else:
            emit("OK", f"SOCKS5 listener on loopback: {listen}")

# ---- server ---------------------------------------------------------------
if mode == "server":
    server = cfg.get("server") or {}
    if not isinstance(server, dict):
        emit("FAIL", "'server:' is not a mapping")
        server = {}
    rf = server.get("rules_file")
    if isinstance(rf, str) and rf:
        expanded = os.path.expanduser(rf)
        setv("RULES_FILE_RAW", expanded)
        if not os.path.isabs(expanded):
            # config.cpp expands ~ only; the path is handed to RulesEngine::from_file
            # as-is, so it resolves against the DAEMON's working directory — NOT the
            # directory holding the config. Verified on v0.4.12: the same config
            # loads from one cwd and dies with "Rules file not found" from another.
            emit("FAIL", f"server.rules_file '{rf}' is RELATIVE. ToxTunnel resolves it "
                         "against the daemon's working directory, not the config's "
                         "directory, so a service unit with a different "
                         "WorkingDirectory will fail to start with 'Rules file not "
                         "found'. Use an absolute path.")
        setv("RULES_FILE_ABS", os.path.abspath(expanded))
    else:
        emit("WARN", "No server.rules_file — the server is default-deny and will refuse "
                     "every friend request and every tunnel open")

print("\n".join(out))
PYEOF
        )
        while IFS= read -r line; do
            [ -z "$line" ] && continue
            lvl=${line%%$'\t'*}
            rest=${line#*$'\t'}
            case "$lvl" in
                OK)    info "$rest" ;;
                WARN)  warn "$rest" ;;
                FAIL)  fail "$rest" ;;
                NOTE)  note "$rest" ;;
                ALIAS) SERVER_ALIASES="${SERVER_ALIASES:-}${SERVER_ALIASES:+ }$rest" ;;
                SET)
                    key=${rest%%$'\t'*}
                    val=${rest#*$'\t'}
                    case "$key" in
                        MODE)           MODE="$val" ;;
                        DATA_DIR)       DATA_DIR="$val" ;;
                        LOG_FILE)       LOG_FILE="$val" ;;
                        FWD_PORTS)      FWD_PORTS="$val" ;;
                        SERVER_IDS)     SERVER_IDS="$val" ;;
                        RULES_FILE_RAW) RULES_FILE="$val" ;;
                        RULES_FILE_ABS) RULES_FILE_RESOLVED="$val" ;;
                    esac
                    ;;
                *) echo "       $line" ;;
            esac
        done <<< "$PARSE_OUT"

        # ---- alias resolution (YAML-parsed; never interpolated into a regex) ----
        for alias in ${SERVER_ALIASES:-}; do
            if [ -z "$DATA_DIR" ]; then
                warn "server_id '$alias' looks like an alias, but no data_dir is set so "
                echo "       known_servers.yaml cannot be located. Verify with:"
                echo "         toxtunnel servers list -c $CONFIG_FILE"
                continue
            fi
            KS="$DATA_DIR/known_servers.yaml"
            if [ ! -f "$KS" ]; then
                fail "server_id '$alias' is not a 76-char Tox ID and $KS does not exist"
                echo "       Register it: toxtunnel servers add $alias <76-char-tox-id> -c $CONFIG_FILE"
                continue
            fi
            if python3 - "$KS" "$alias" <<'PYEOF'
import sys, yaml
try:
    with open(sys.argv[1]) as f:
        data = yaml.safe_load(f) or {}
except Exception:
    sys.exit(2)
entries = data.get("servers", data) if isinstance(data, dict) else data
if isinstance(entries, dict):
    entries = list(entries.values())
if not isinstance(entries, list):
    sys.exit(2)
want = sys.argv[2]
for e in entries:
    if isinstance(e, dict) and (e.get("alias") == want or e.get("tox_id") == want):
        sys.exit(0)
sys.exit(1)
PYEOF
            then
                info "server_id '$alias' resolves to an entry in $KS"
            else
                fail "server_id '$alias' has no matching alias in $KS"
                echo "       Needs a 76-char Tox ID or a registered alias."
                echo "       List them: toxtunnel servers list -c $CONFIG_FILE"
            fi
        done
    fi
fi

# =========================================================================
# Layer 3: Rules File
#
# config check --strict does NOT open rules_file on v0.4.13 and older (v0.5.0+
# parses it for existence/syntax), so most of this layer is additional
# coverage, not a repeat — and the semantic checks are extra on every version.
# =========================================================================
section "Layer 3: Rules File"

if [ "$MODE" != "server" ]; then
    note "Not a server config — no rules file to analyse"
elif [ -z "$RULES_FILE" ]; then
    note "No rules_file configured (already reported above)"
else
    # Deliberately NOT rebased against the config's directory: the daemon resolves
    # a relative rules_file against its own working directory.
    if [ -f "$RULES_FILE_RESOLVED" ]; then
        info "rules_file readable from this shell's cwd: $RULES_FILE_RESOLVED"
        case "$RULES_FILE" in
            /*) ;;
            *)  warn "...but the path in the config is relative. This shell's cwd is "
                echo "       $(pwd); the daemon's may differ. Make it absolute."
                ;;
        esac
    else
        fail "rules_file not found at $RULES_FILE_RESOLVED"
        echo "       The server refuses to start: 'Failed to load rules file: Rules file"
        echo "       not found'. Use an absolute path."
    fi

    if [ "$HAVE_PYYAML" = false ]; then
        skip "PyYAML not available — rules file not analysed"
    elif [ -f "$RULES_FILE_RESOLVED" ]; then
        RISK_OUT=$(python3 - "$RULES_FILE_RESOLVED" <<'PYEOF'
import re, sys, yaml

out = []


def emit(level, msg):
    out.append(f"{level}\t{msg}")


try:
    with open(sys.argv[1]) as f:
        data = yaml.safe_load(f)
except Exception as e:
    emit("FAIL", f"Cannot parse rules file: {e}")
    print("\n".join(out))
    sys.exit(0)

if not data:
    emit("WARN", "Rules file is empty — the server denies everything")
    print("\n".join(out))
    sys.exit(0)

rules = data if isinstance(data, list) else (data.get("rules") or [])
if not rules:
    emit("WARN", "No 'rules:' entries — the server denies everything")
    print("\n".join(out))
    sys.exit(0)

# Keys the rules parser actually reads inside an allow/deny target entry.
# Anything else is silently ignored, and an entry with no `ports` key means
# ALL PORTS — so a `port: 22` typo widens the allow instead of narrowing it.
TARGET_KEYS = {"host", "ports"}
seen_friends = {}

for i, rule in enumerate(rules, start=1):
    if not isinstance(rule, dict):
        emit("FAIL", f"Rule #{i} is not a mapping")
        continue

    fk = rule.get("friend") or rule.get("friend_pk") or ""
    if "friend_public_key" in rule:
        emit("FAIL", f"Rule #{i} uses 'friend_public_key', which the parser does not "
                     "recognise. Use 'friend' (or the alias 'friend_pk').")
    if not isinstance(fk, str) or len(fk) != 64:
        emit("FAIL", f"Rule #{i}: friend key is {len(fk) if isinstance(fk, str) else '?'} "
                     "chars, expected exactly 64 hex (the first 64 of the 76-char Tox ID)")
    elif not re.fullmatch(r"[0-9A-Fa-f]{64}", fk):
        emit("FAIL", f"Rule #{i}: friend key contains non-hex characters")
    else:
        key = fk.upper()
        if key in seen_friends:
            first = seen_friends[key]
            emit("FAIL", f"Rule #{i} DUPLICATES the friend key already used by rule #{first}. "
                         "Lookup is a linear first-match, so rule "
                         f"#{i} is dead config and its allow/deny entries NEVER apply. "
                         f"Merge them into rule #{first}.")
        else:
            seen_friends[key] = i

    for section_name in ("allow", "deny"):
        entries = rule.get(section_name)
        if entries is None:
            continue
        if not isinstance(entries, list):
            emit("FAIL", f"Rule #{i}: '{section_name}' must be a list")
            continue
        for j, entry in enumerate(entries, start=1):
            if not isinstance(entry, dict):
                emit("FAIL", f"Rule #{i} {section_name}[{j}] is not a mapping")
                continue
            unknown = sorted(set(entry) - TARGET_KEYS)
            host = entry.get("host", "")
            ports = entry.get("ports")
            if unknown:
                emit("FAIL", f"Rule #{i} {section_name}[{j}] has unrecognised key(s) "
                             f"{unknown}. The parser IGNORES them. If you meant 'ports', "
                             "note that a missing 'ports' key means ALL PORTS — this "
                             "entry is broader than it looks.")
            if "host" not in entry:
                emit("FAIL", f"Rule #{i} {section_name}[{j}] has no 'host'")
            if "ports" not in entry:
                if section_name == "allow":
                    emit("FAIL", f"Rule #{i} allow[{j}] omits 'ports', which the engine "
                                 f"reads as ALL PORTS on '{host}'. Write an explicit list, "
                                 "or 'ports: []' if all ports really are intended.")
                else:
                    emit("NOTE", f"Rule #{i} deny[{j}] omits 'ports', so it denies ALL PORTS "
                                 f"on '{host}' (deny takes precedence over every allow)")
            elif ports == []:
                lvl = "WARN" if section_name == "allow" else "NOTE"
                emit(lvl, f"Rule #{i} {section_name}[{j}]: 'ports: []' means ALL PORTS "
                          f"on '{host}'")
            elif not isinstance(ports, list):
                emit("FAIL", f"Rule #{i} {section_name}[{j}]: 'ports' must be a list")
            else:
                bad = [p for p in ports if not isinstance(p, int) or not 1 <= p <= 65535]
                if bad:
                    emit("FAIL", f"Rule #{i} {section_name}[{j}]: invalid port(s) {bad}")

            if section_name == "allow" and isinstance(host, str):
                if host == "*":
                    emit("FAIL", f"Rule #{i} allow[{j}] allows ALL HOSTS")
                elif host.count("*") > 1:
                    emit("FAIL", f"Rule #{i} allow[{j}] host '{host}' has more than one "
                                 "'*'. The matcher handles ONE prefix and ONE suffix "
                                 "only, so this pattern never matches anything.")

# rate_limit_defaults sanity: both byte keys must be non-zero to engage.
defaults = data.get("rate_limit_defaults") if isinstance(data, dict) else None
blocks = [("rate_limit_defaults", defaults)]
for i, rule in enumerate(rules, start=1):
    if isinstance(rule, dict) and isinstance(rule.get("rate_limit"), dict):
        blocks.append((f"rule #{i} rate_limit", rule["rate_limit"]))
for name, blk in blocks:
    if not isinstance(blk, dict):
        continue
    bps, burst = blk.get("bytes_per_sec"), blk.get("bytes_burst")
    if bool(bps) != bool(burst):
        emit("WARN", f"{name}: bytes_per_sec={bps!r} / bytes_burst={burst!r} — BOTH must "
                     "be non-zero for the byte budget to engage. As written it does "
                     "nothing.")
    mode_v = blk.get("mode")
    if mode_v is not None and mode_v not in ("off", "report", "enforce"):
        emit("FAIL", f"{name}: mode '{mode_v}' is not one of off | report | enforce")

if not out:
    emit("OK", "Rules file structure looks sound")

print("\n".join(out))
PYEOF
        )
        RISK_RC=$?
        if [ "$RISK_RC" -ne 0 ]; then
            fail "Rules analysis crashed (python exit $RISK_RC) — treat the rules as unverified"
        fi
        while IFS= read -r line; do
            [ -z "$line" ] && continue
            lvl=${line%%$'\t'*}
            rest=${line#*$'\t'}
            case "$lvl" in
                OK)   info "$rest" ;;
                WARN) warn "$rest" ;;
                FAIL) fail "$rest" ;;
                NOTE) note "$rest" ;;
                *)    echo "       $line" ;;
            esac
        done <<< "$RISK_OUT"
        note "Allow-only rules are normal: the engine is default-deny, so a friend with"
        echo "       no matching allow is already refused. Missing 'deny:' is not a risk."
    fi
fi

# =========================================================================
# Layer 4: Network & Tox Connection
# =========================================================================
section "Layer 4: Network & Tox Connection"

# ICMP to a public resolver tells you almost nothing about Tox reachability:
# Tox bootstraps over UDP (and falls back to TCP relays), and plenty of networks
# drop ICMP while passing both. Report it as a hint, never as a verdict.
PING_OK=false
if command -v ping &>/dev/null; then
    if [ "$(uname)" = "Darwin" ]; then
        ping -c 1 -W 2000 1.1.1.1 &>/dev/null && PING_OK=true
    else
        ping -c 1 -W 2 1.1.1.1 &>/dev/null && PING_OK=true
    fi
    if [ "$PING_OK" = true ]; then
        note "ICMP to 1.1.1.1 works (a hint only — Tox needs UDP/TCP to DHT nodes, not ICMP)"
    else
        note "ICMP to 1.1.1.1 failed. This is NOT proof the network is down: many"
        echo "       networks drop ICMP while passing Tox fine. The signals that matter"
        echo "       are 'Connected to Tox DHT' in the log and friends_online from"
        echo "       'toxtunnel inspect status'."
    fi
fi

if [ -n "$TOXTUNNEL_BIN" ] && [ -n "$DATA_DIR" ] && [ -S "$DATA_DIR/toxtunnel.sock" ]; then
    STATUS=$(tmo 10 toxtunnel inspect status -d "$DATA_DIR" --json 2>/dev/null || true)
    if [ -n "$STATUS" ]; then
        FRIENDS=$(printf '%s' "$STATUS" | tr ',{}' '\n\n\n' | grep '"friends_online"' \
                  | head -1 | grep -oE '[0-9]+$' || true)
        if [ -n "$FRIENDS" ] && [ "$FRIENDS" -gt 0 ] 2>/dev/null; then
            info "Daemon reports friends_online=$FRIENDS"
        elif [ -n "$FRIENDS" ]; then
            fail "Daemon reports friends_online=0 — no Tox peer is connected"
            echo "       Nothing can be forwarded until this is non-zero."
        fi
        # v0.5.0+ reports DHT connectivity directly; older daemons omit the field.
        DHT=$(printf '%s' "$STATUS" | tr ',{}' '\n\n\n' | grep '"dht_connected"' \
              | head -1 | grep -oE '(true|false)$' || true)
        if [ "$DHT" = true ]; then
            info "Daemon reports dht_connected=true"
        elif [ "$DHT" = false ]; then
            fail "Daemon reports dht_connected=false — not currently connected to the Tox DHT"
            echo "       Look for 'Bootstrap contacted 0 of N node(s)' in its log. Fix outbound"
            echo "       UDP/TCP to the bootstrap nodes, pin tox.bootstrap_nodes by IP, or on a"
            echo "       proxy-only host set tox.proxy (v0.5.0+)."
        fi
        printf '%s\n' "$STATUS" | sed 's/^/       /' | head -5
    else
        warn "'toxtunnel inspect status' returned nothing (inspect disabled, or stale socket)"
    fi
elif [ -n "$DATA_DIR" ]; then
    note "No inspect socket at $DATA_DIR/toxtunnel.sock — daemon down, different data_dir,"
    echo "       or inspect.enabled: false"
fi

# =========================================================================
# Layer 5: Local Forward Ports
# =========================================================================
section "Layer 5: Local Forward Ports"

if [ -z "$FWD_PORTS" ]; then
    note "No client forwards to check (server mode, pipe mode, SOCKS5, or unparsed config)"
else
    IFS=',' read -r -a PORT_ARR <<< "$FWD_PORTS"
    for PORT in "${PORT_ARR[@]}"; do
        [ -z "$PORT" ] && continue
        LISTENER=""
        if command -v lsof &>/dev/null; then
            LISTENER=$(lsof -nP -i "TCP:$PORT" -sTCP:LISTEN 2>/dev/null | tail -n +2 || true)
        elif command -v ss &>/dev/null; then
            LISTENER=$(ss -tlnp 2>/dev/null | grep -E "[:.]$PORT[[:space:]]" || true)
        fi
        if [ -z "$LISTENER" ]; then
            warn "Port $PORT is not listening — client not running, or it failed to bind"
            echo "       Look for 'TcpListener: failed to bind' or 'cannot listen on"
            echo "       configured forward port(s)' in the log."
            continue
        fi
        if printf '%s\n' "$LISTENER" | grep -qi toxtunnel; then
            info "Port $PORT is listening (toxtunnel)"
        else
            fail "Port $PORT is held by another process — toxtunnel cannot bind it:"
            printf '%s\n' "$LISTENER" | sed 's/^/       /'
            continue
        fi
        # A successful connect here proves only that the local listener accepted.
        # It does NOT prove TUNNEL_OPEN succeeded or the target was reached.
        if command -v nc &>/dev/null; then
            if nc -z -w 3 127.0.0.1 "$PORT" 2>/dev/null; then
                note "Port $PORT accepts local TCP connections (local listener only —"
                echo "       this says nothing about the tunnel; use scripts/verify.sh"
                echo "       with the right service type to prove the far end answers)"
            else
                fail "Port $PORT is listening but refuses connections"
            fi
        fi
    done
fi

# =========================================================================
# Layer 6: Log Analysis
# =========================================================================
section "Layer 6: Log Analysis"

if [ -z "$LOG_FILE" ]; then
    note "No logging.file configured — cannot analyse a log"
    echo "       Add:  logging: { level: debug, file: /tmp/toxtunnel.log }"
    echo "       Or read the service journal: journalctl -u toxtunnel -n 200"
elif [ ! -f "$LOG_FILE" ]; then
    warn "Configured log file does not exist: $LOG_FILE"
else
    info "Log file: $LOG_FILE"

    if grep -q "Connected to Tox DHT" "$LOG_FILE" 2>/dev/null; then
        info "DHT connection: established at least once"
    else
        warn "No 'Connected to Tox DHT' line in the log"
    fi

    SELF_STATUS=$(grep "Self connection status:" "$LOG_FILE" 2>/dev/null | tail -1 || true)
    if [ -n "$SELF_STATUS" ]; then
        note "Latest self connection status: ${SELF_STATUS##*Self connection status: }"
        echo "       (This is the DHT link, NOT the per-friend path. It routinely says"
        echo "        TCP while the friend path is direct UDP.)"
    fi

    if grep -qE "Server friend [0-9]+ is now online|Friend [0-9]+ \(pk=[0-9A-Fa-f]+\) connected" \
            "$LOG_FILE" 2>/dev/null; then
        info "Friend connection: established at least once"
        LAST_FRIEND=$(grep -E "Server friend [0-9]+ (is now online|went offline)|Friend [0-9]+ \(pk=[0-9A-Fa-f]+\) (connected|disconnected)" \
                      "$LOG_FILE" 2>/dev/null | tail -1 || true)
        echo "       latest: $LAST_FRIEND"
    else
        warn "Friend connection never established (per this log)"
        if grep -q "Refused friend request" "$LOG_FILE" 2>/dev/null; then
            fail "Server refused a friend request — the client's public key is not in rules.yaml:"
            grep "Refused friend request" "$LOG_FILE" 2>/dev/null | tail -2 | sed 's/^/       /'
        fi
        if grep -q "Still trying to reach server" "$LOG_FILE" 2>/dev/null; then
            echo "       Client is still retrying — allow 1-3 min on a relay path."
        fi
    fi

    # Transport for the CONFIGURED server, not merely the last line in the file.
    if [ -n "$DATA_DIR" ] && [ -f "$DATA_DIR/known_servers.yaml" ] && [ "$HAVE_PYYAML" = true ]; then
        TRANSPORT_OUT=$(python3 - "$DATA_DIR/known_servers.yaml" "${SERVER_IDS:-}" <<'PYEOF'
import sys, yaml
try:
    with open(sys.argv[1]) as f:
        data = yaml.safe_load(f) or {}
except Exception:
    sys.exit(0)
entries = data.get("servers", data) if isinstance(data, dict) else data
if isinstance(entries, dict):
    entries = list(entries.values())
if not isinstance(entries, list):
    sys.exit(0)
wanted = [w for w in sys.argv[2].split(",") if w]
for e in entries:
    if not isinstance(e, dict):
        continue
    tox_id = str(e.get("tox_id", ""))
    alias = str(e.get("alias", ""))
    if wanted and not any(w == alias or w.upper() == tox_id.upper() for w in wanted):
        continue
    label = alias or (tox_id[:12] + "...")
    print(f"{label}\t{e.get('last_connection_type', 'unknown')}")
PYEOF
        )
        if [ -n "$TRANSPORT_OUT" ]; then
            while IFS=$'\t' read -r label transport; do
                case "$transport" in
                    udp) info "Transport to '$label': udp (direct — full speed)" ;;
                    tcp) warn "Transport to '$label': tcp (Tox relay) — bulk throughput is"
                         echo "       ~3-10 KB/s. Fine for SSH keystrokes and DB queries, unusable"
                         echo "       for file copies or RDP. Get onto direct UDP if you need speed." ;;
                    *)   note "Transport to '$label': $transport" ;;
                esac
            done <<< "$TRANSPORT_OUT"
        else
            note "No known_servers.yaml entry matches the configured server_id yet"
        fi
    fi

    # "Send lossless packet failed ... error 7" is toxcore back-pressure (SENDQ
    # full), not a fault. Count with grep -c on a single command, never
    # `pipeline || echo 0` — grep -c already prints 0 and then exits 1, so the
    # fallback appends a second line and the arithmetic test blows up.
    ERROR_LINES=$(grep -i "error" "$LOG_FILE" 2>/dev/null | grep -v "Send lossless packet failed" || true)
    if [ -n "$ERROR_LINES" ]; then
        ERRORS=$(printf '%s\n' "$ERROR_LINES" | wc -l | tr -d ' ')
        warn "Found $ERRORS error line(s) in the log. Last 5:"
        printf '%s\n' "$ERROR_LINES" | tail -5 | sed 's/^/       /'
    else
        info "No error lines in the log (toxcore SENDQ back-pressure excluded)"
    fi

    if grep -q "Invalid public key" "$LOG_FILE" 2>/dev/null; then
        fail "'Invalid public key' in log — rules.yaml friend keys must be 64 hex chars"
    fi
    if grep -q "Rules file not found" "$LOG_FILE" 2>/dev/null; then
        fail "'Rules file not found' in log — the rules_file path is wrong (use an absolute path)"
    fi
    if grep -q "already in use by toxtunnel pid" "$LOG_FILE" 2>/dev/null; then
        fail "Another daemon owns this data_dir — give this one its own, or stop the other:"
        grep "already in use by toxtunnel pid" "$LOG_FILE" 2>/dev/null | tail -2 | sed 's/^/       /'
    fi
    if grep -qiE "failed to bind|cannot listen on configured forward port|Reload: not forwarding" \
            "$LOG_FILE" 2>/dev/null; then
        fail "A local port could not be bound (usually already in use):"
        grep -iE "failed to bind|cannot listen on configured forward port|Reload: not forwarding" \
            "$LOG_FILE" 2>/dev/null | tail -3 | sed 's/^/       /'
    fi
    if grep -q "tox_thread wedge" "$LOG_FILE" 2>/dev/null; then
        fail "Watchdog fired (tox_thread wedge) — the daemon aborted and was restarted:"
        grep "tox_thread wedge" "$LOG_FILE" 2>/dev/null | tail -2 | sed 's/^/       /'
    fi
fi

# =========================================================================
# Summary
# =========================================================================
echo ""
echo "===== Diagnostic Complete ====="
if [ "$ISSUES" -gt 0 ]; then
    echo -e "${YELLOW}Found $ISSUES issue(s). Review the items above.${NC}"
    echo "Anything reported [SKIP] was NOT checked — it is not a pass."
    exit 1
else
    echo -e "${GREEN}All checks passed.${NC}"
    echo "Note: passing here does not prove data flows. Run scripts/verify.sh with the"
    echo "right service type to confirm the far end actually answers."
    exit 0
fi
