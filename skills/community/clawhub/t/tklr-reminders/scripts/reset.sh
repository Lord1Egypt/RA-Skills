#!/usr/bin/env bash
# reset.sh — return this machine to the state of someone who has just obtained
# the tklr-reminders skill and not yet set it up, so setup can be tested from
# scratch.
#
#   bash reset.sh              interactive, requires typing NUKE
#   bash reset.sh --dry-run    show exactly what would happen
#   bash reset.sh --yes        skip the prompt (for scripted testing)
#
# THIS DESTROYS ALL YOUR REMINDERS. ~/.config/tklr holds every event, task,
# and note you have entered — there is no undo. Take a copy first if you care:
#     cp -a ~/.config/tklr ~/tklr-backup-$(date +%F)
#
# What it removes:
#   1. the every-minute cron job          (hermes cron remove)
#   2. any pending blueprint suggestion   (~/.hermes/cron/suggestions.json)
#   3. the installed dispatcher           (~/.hermes/scripts/tklr_alert_poller.py)
#   4. the dispatcher log + rotations     (~/.hermes/logs/tklr-alerts.log*)
#   5. the skill's usage registration     (entry in ~/.hermes/skills/.usage.json)
#   6. the cached skill prompt index      (~/.hermes/.skills_prompt_snapshot.json)
#   7. the ENTIRE tklr workspace          (~/.config/tklr — config AND database)
#   8. tklr itself, only if uv owns it AND this skill installed it
#
# HOST-SPECIFIC, all of it: every path above is Hermes layout and the cron
# calls are Hermes' scheduler. This is a test-harness script rather than part
# of the delivery path, so it is the last thing a port needs and the easiest to
# reduce to whatever the new host's equivalents are. scripts/host.py names the
# same seams for the Python side.
#
# What it NEVER touches:
#   * the skill source directory itself — SKILL.md, scripts/, templates/,
#     references/. That is the thing under test: a new person starts with these
#     files present and nothing configured, so deleting them would leave nothing
#     to test. It is also version-controlled work that this script has no
#     business removing. There is deliberately no flag to override this; nothing
#     below ever writes to or deletes anything under SKILL_DIR.

set -uo pipefail

DRY_RUN=0
ASSUME_YES=0
while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run) DRY_RUN=1; shift ;;
        --yes|-y)  ASSUME_YES=1; shift ;;
        -h|--help) sed -n '2,30p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'; exit 0 ;;
        *) echo "unknown argument: $1" >&2; exit 2 ;;
    esac
done

# Every path below is absolute, derived from $HOME or from this script's own
# location, so the working directory you run from does not matter.
SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# TKLR_HOME from the environment DOES matter — it redirects the rm -rf. Note
# where it came from and sanity-check it before trusting it.
if [[ -n "${TKLR_HOME:-}" ]]; then
    TKLR_HOME_SOURCE="inherited from the TKLR_HOME environment variable"
else
    TKLR_HOME_SOURCE="default"
fi
TKLR_HOME="${TKLR_HOME:-$HOME/.config/tklr}"

# Refuse to recursively delete anything that is not plainly a tklr workspace.
guard_tklr_home() {
    local p real
    p="$TKLR_HOME"
    if [[ -z "${p// }" ]]; then
        echo "REFUSING: TKLR_HOME is empty." >&2; exit 3
    fi
    real="$(cd "$p" 2>/dev/null && pwd -P || echo "$p")"
    case "$real" in
        / | /home | /root | /usr | /etc | /var | /tmp)
            echo "REFUSING: TKLR_HOME resolves to $real — that is not a workspace." >&2; exit 3 ;;
    esac
    if [[ "$real" == "$(cd "$HOME" && pwd -P)" ]]; then
        echo "REFUSING: TKLR_HOME resolves to your home directory ($real)." >&2; exit 3
    fi
    # If it exists, it must look like a tklr workspace before we rm -rf it.
    if [[ -d "$real" && ! -e "$real/tklr.db" && ! -e "$real/config.toml" ]]; then
        echo "REFUSING: $real exists but has neither tklr.db nor config.toml," >&2
        echo "          so it does not look like a tklr workspace." >&2
        echo "          Unset TKLR_HOME, or point it at the right directory." >&2
        exit 3
    fi
}
guard_tklr_home
# Assigned with a default rather than unconditionally: this overwrote a set
# $HERMES_HOME, so on any machine that moves the host directory the reset
# cleaned a path that did not exist and left the real dispatcher, log and
# recorded paths in place -- while reporting that everything had been removed.
# A reset that lies is worse than no reset, since its only purpose is to make a
# from-scratch test mean something.
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
DISPATCHER="$HERMES_HOME/scripts/tklr_alert_poller.py"
LOG_GLOB="$HERMES_HOME/logs/tklr-alerts.log"
USAGE_JSON="$HERMES_HOME/skills/.usage.json"
SNAPSHOT="$HERMES_HOME/.skills_prompt_snapshot.json"
SUGGESTIONS="$HERMES_HOME/cron/suggestions.json"
export PATH="$HOME/.local/bin:$PATH"

step() { printf '\n=== %s\n' "$1"; }
act()  { if [[ $DRY_RUN -eq 1 ]]; then printf '  would: %s\n' "$1"; else printf '  %s\n' "$1"; fi; }
skip() { printf '  (already absent) %s\n' "$1"; }

# ------------------------------------------------------------------ survey
echo "This will remove, if present:"
FOUND=0

CRON_IDS=$(timeout 60 hermes cron list 2>/dev/null \
    | awk '/^ *[0-9a-f]{12} \[/{id=$1} /Name: *tklr-alert-poller/{print id}')
if [[ -n "$CRON_IDS" ]]; then
    echo "  - cron job(s): $(echo "$CRON_IDS" | tr '\n' ' ')"; FOUND=1
fi
[[ -f "$DISPATCHER" ]] && { echo "  - dispatcher:  $DISPATCHER"; FOUND=1; }
compgen -G "${LOG_GLOB}*" >/dev/null 2>&1 && { echo "  - log file(s): ${LOG_GLOB}*"; FOUND=1; }
if [[ -d "$TKLR_HOME" ]]; then
    RECS=$(sqlite3 "$TKLR_HOME/tklr.db" "select count(*) from Records;" 2>/dev/null || echo "?")
    echo "  - tklr workspace: $TKLR_HOME  ($(du -sh "$TKLR_HOME" 2>/dev/null | cut -f1), $RECS reminders — DESTROYS YOUR DATA)"
    [[ "$TKLR_HOME_SOURCE" != "default" ]] && \
        echo "      ^ NOTE: this path is $TKLR_HOME_SOURCE, not the default"
    FOUND=1
fi
# Which uv? Hermes ships its own at $HERMES_HOME/bin/uv, not on PATH.
UV_BIN=""
for c in "${UV:-}" "$HERMES_HOME/bin/uv" uv; do
    [[ -z "$c" ]] && continue
    c="$(command -v "$c" 2>/dev/null || { [[ -x "$c" ]] && echo "$c"; })"
    [[ -n "$c" ]] && { UV_BIN="$c"; break; }
done
# Two separate questions, and only both together justify removing tklr:
# can uv remove it, and did THIS SKILL put it there. uv ownership alone answers
# the first and was being read as an answer to the second -- so a user who ran
# `uv tool install tklr-dgraham` themselves before adding the skill would have
# had their own tklr uninstalled by a reset. install.sh records the marker only
# on the branch that actually performs the install.
INSTALL_MARKER="$HERMES_HOME/scripts/tklr-installed-by-skill"
UV_OWNS=""
if [[ -n "$UV_BIN" ]] && "$UV_BIN" tool list 2>/dev/null | grep -q "tklr-dgraham"; then
    UV_OWNS=1
fi
SKILL_INSTALLED=""
[[ -f "$INSTALL_MARKER" ]] && SKILL_INSTALLED=1

if command -v tklr >/dev/null 2>&1; then
    if [[ -n "$UV_OWNS" && -n "$SKILL_INSTALLED" ]]; then
        echo "  - tklr package: $(tklr --version 2>&1 | head -1) (uv tool uninstall)"; FOUND=1
    elif [[ -n "$UV_OWNS" ]]; then
        echo
        echo "NOT touching tklr at $(command -v tklr)"
        echo "  uv owns it, but there is no record of this skill installing it,"
        echo "  so it was already on this machine. Remove it yourself if you"
        echo "  want it gone: $UV_BIN tool uninstall tklr-dgraham"
    else
        echo
        echo "NOT touching tklr at $(command -v tklr)"
        echo "  uv does not report owning it, so this skill did not install it."
        echo "  (This skill installs tklr only with uv.)"
    fi
fi
[[ -f "$USAGE_JSON" ]] && grep -q "tklr-reminders" "$USAGE_JSON" 2>/dev/null && \
    { echo "  - usage registration in $USAGE_JSON"; FOUND=1; }
[[ -f "$SUGGESTIONS" ]] && grep -q "tklr" "$SUGGESTIONS" 2>/dev/null && \
    { echo "  - blueprint suggestion in $SUGGESTIONS"; FOUND=1; }
[[ -f "$SNAPSHOT" ]] && { echo "  - cached skill index $SNAPSHOT (rebuilt automatically)"; FOUND=1; }
echo
echo "Keeping the skill source at $SKILL_DIR"
echo "  (that is what a new person starts with — this script never removes it)"

if [[ $FOUND -eq 0 ]]; then
    echo "  nothing — already pristine."
    exit 0
fi

# ------------------------------------------------------------------ consent
if [[ $DRY_RUN -eq 0 && $ASSUME_YES -eq 0 ]]; then
    echo
    echo "There is no undo. Reminders in $TKLR_HOME will be gone."
    printf 'Type NUKE to proceed: '
    read -r reply
    if [[ "$reply" != "NUKE" ]]; then
        echo "Aborted — nothing was changed."
        exit 1
    fi
fi

# ------------------------------------------------------------------- 1. cron
step "cron job"
if [[ -n "$CRON_IDS" ]]; then
    while read -r id; do
        [[ -z "$id" ]] && continue
        act "hermes cron remove $id"
        if [[ $DRY_RUN -eq 0 ]]; then
            timeout 60 hermes cron remove "$id" >/dev/null 2>&1
            # Do NOT trust the exit code: `hermes cron remove` returns 0 even
            # for an id that does not exist. Confirm by re-querying instead.
            if timeout 60 hermes cron list 2>/dev/null | grep -q "$id"; then
                echo "    STILL THERE — remove it by hand: hermes cron remove $id"
            else
                echo "    removed (confirmed gone from 'hermes cron list')"
            fi
        fi
    done <<< "$CRON_IDS"
else
    skip "no tklr-alert-poller job"
fi

# ------------------------------------------------- 2. blueprint suggestion
step "blueprint suggestion"
if [[ -f "$SUGGESTIONS" ]] && grep -q "tklr" "$SUGGESTIONS" 2>/dev/null; then
    act "drop tklr entries from $SUGGESTIONS"
    if [[ $DRY_RUN -eq 0 ]]; then
        python3 - "$SUGGESTIONS" <<'PY'
import json, sys
from pathlib import Path
p = Path(sys.argv[1])
try:
    data = json.loads(p.read_text(encoding="utf-8"))
except Exception as e:
    print(f"    could not parse: {e}"); sys.exit(0)

def keeps(entry):
    return "tklr" not in json.dumps(entry).lower()

if isinstance(data, list):
    kept = [e for e in data if keeps(e)]
    dropped = len(data) - len(kept)
elif isinstance(data, dict) and isinstance(data.get("suggestions"), list):
    orig = data["suggestions"]
    data["suggestions"] = [e for e in orig if keeps(e)]
    dropped = len(orig) - len(data["suggestions"])
    kept = data
else:
    kept = {k: v for k, v in data.items() if keeps({k: v})} if isinstance(data, dict) else data
    dropped = "?"
p.write_text(json.dumps(kept if not isinstance(kept, list) else kept, indent=2), encoding="utf-8")
print(f"    dropped {dropped} entr(y/ies)")
PY
    fi
else
    skip "no tklr suggestion"
fi

# ------------------------------------------------------------- 3. dispatcher
step "installed dispatcher"
if [[ -f "$DISPATCHER" ]]; then
    act "rm $DISPATCHER"
    [[ $DRY_RUN -eq 0 ]] && rm -f "$DISPATCHER"
else
    skip "$DISPATCHER"
fi

# Both are written by install.sh beside the dispatcher, and both are read by
# things that run unattended. Leaving either behind makes the NEXT setup look
# like it worked when it did not: a stale pin means an install that never
# recorded its workspace still finds one, and a stale wrapper path means a
# scheduled health check still resolves the script. A reset that leaves working
# scaffolding behind cannot be used to test a from-scratch install, which is
# the only thing it is for.
step "recorded paths beside the dispatcher"
for recorded in "$HERMES_HOME/scripts/tklr-workspace-path" \
                "$HERMES_HOME/scripts/tklr-wrapper-path" \
                "$INSTALL_MARKER"; do
    if [[ -f "$recorded" ]]; then
        act "rm $recorded"
        [[ $DRY_RUN -eq 0 ]] && rm -f "$recorded"
    else
        skip "$recorded"
    fi
done

# -------------------------------------------------------------------- 4. log
step "dispatcher log"
if compgen -G "${LOG_GLOB}*" >/dev/null 2>&1; then
    act "rm ${LOG_GLOB}*"
    [[ $DRY_RUN -eq 0 ]] && rm -f "${LOG_GLOB}"*
    # the lock file lives beside the log
    [[ $DRY_RUN -eq 0 ]] && rm -f "$HERMES_HOME/logs/.tklr-alerts.lock"
else
    skip "${LOG_GLOB}*"
fi

# ---------------------------------------------------- 5. usage registration
step "skill usage registration"
if [[ -f "$USAGE_JSON" ]] && grep -q "tklr-reminders" "$USAGE_JSON" 2>/dev/null; then
    act "remove tklr-reminders from $USAGE_JSON"
    if [[ $DRY_RUN -eq 0 ]]; then
        python3 - "$USAGE_JSON" <<'PY'
import json, sys
from pathlib import Path
p = Path(sys.argv[1])
try:
    data = json.loads(p.read_text(encoding="utf-8"))
except Exception as e:
    print(f"    could not parse: {e}"); sys.exit(0)
removed = 0
if isinstance(data, dict):
    for key in [k for k in data if "tklr-reminders" in str(k)]:
        data.pop(key); removed += 1
    for key, val in list(data.items()):
        if isinstance(val, dict):
            for sub in [k for k in val if "tklr-reminders" in str(k)]:
                val.pop(sub); removed += 1
p.write_text(json.dumps(data, indent=2), encoding="utf-8")
print(f"    removed {removed} entr(y/ies)")
PY
    fi
else
    skip "no tklr-reminders usage entry"
fi

# --------------------------------------------------------- 6. prompt cache
step "cached skill index"
if [[ -f "$SNAPSHOT" ]]; then
    act "rm $SNAPSHOT  (Hermes rebuilds it on next use)"
    [[ $DRY_RUN -eq 0 ]] && rm -f "$SNAPSHOT"
else
    skip "$SNAPSHOT"
fi

# ------------------------------------------------------- 7. tklr workspace
step "tklr workspace (YOUR REMINDERS)"
if [[ -d "$TKLR_HOME" ]]; then
    act "rm -rf $TKLR_HOME"
    [[ $DRY_RUN -eq 0 ]] && rm -rf "$TKLR_HOME"
else
    skip "$TKLR_HOME"
fi

# --------------------------------------------------------- 8. tklr package
step "tklr package"
if command -v tklr >/dev/null 2>&1; then
    # We only remove what this skill installed. That needs BOTH uv ownership
    # (so uv can remove it) and the marker install.sh writes on the branch that
    # actually installs (so we know it was us). uv ownership alone answers a
    # different question and would take a user's own tklr with it.
    if [[ -n "$UV_OWNS" && -n "$SKILL_INSTALLED" ]]; then
        act "$UV_BIN tool uninstall tklr-dgraham"
        if [[ $DRY_RUN -eq 0 ]]; then
            "$UV_BIN" tool uninstall tklr-dgraham >/dev/null 2>&1
            hash -r 2>/dev/null || true
            # Do not trust the exit code; confirm it actually left PATH.
            if command -v tklr >/dev/null 2>&1; then
                echo "    STILL ON PATH: $(command -v tklr)"
            else
                echo "    uninstalled (confirmed gone from PATH)"
            fi
        fi
    elif [[ -n "$UV_OWNS" ]]; then
        # uv could remove it, but nothing says this skill put it there. Naming
        # the exact command matters more than usual here: the reason we stop is
        # that it may be the user's own tklr, so the decision is theirs.
        echo "  LEAVING ALONE: tklr at $(command -v tklr)"
        echo "    uv owns it, but there is no record of this skill installing"
        echo "    it, so it was already on this machine."
        echo "    Remove it yourself if you want to:"
        echo "      $UV_BIN tool uninstall tklr-dgraham"
    else
        echo "  LEAVING ALONE: tklr at $(command -v tklr)"
        echo "    uv does not report owning it, so this skill did not install it."
        echo "    Remove it yourself if you want to, e.g.:"
        echo "      pipx uninstall tklr-dgraham"
    fi
else
    skip "tklr not on PATH"
fi

# The skill source directory is deliberately absent from this script's removal
# steps. It is what a fresh install starts from and it is version-controlled;
# nothing here should ever delete it.

# ------------------------------------------------------------------ verify
step "result"
if [[ $DRY_RUN -eq 1 ]]; then
    echo "  dry run — nothing was changed."
    exit 0
fi

REMAIN=0
check() { if eval "$1"; then echo "  STILL PRESENT: $2"; REMAIN=1; else echo "  gone: $2"; fi; }
check '[[ -d "$TKLR_HOME" ]]'   "$TKLR_HOME"
check '[[ -f "$DISPATCHER" ]]'  "$DISPATCHER"
check 'compgen -G "${LOG_GLOB}*" >/dev/null 2>&1' "${LOG_GLOB}*"
check 'command -v tklr >/dev/null 2>&1' "tklr on PATH"
if timeout 60 hermes cron list 2>/dev/null | grep -q "tklr-alert-poller"; then
    echo "  STILL PRESENT: cron job tklr-alert-poller"; REMAIN=1
else
    echo "  gone: cron job"
fi

echo
if [[ $REMAIN -eq 0 ]]; then
    echo "Pristine. To exercise setup from scratch:"
    echo "  1. /reload-skills   (so the agent re-reads the skill)"
    echo "  2. ask it: \"set up my calendar and reminders\""
else
    echo "Some items remain — see above."
fi

# Pre-existing clutter from earlier attempts is NOT touched; listed so you can
# decide for yourself.
LEFTOVERS=()
for f in "$HOME/tklr-poller.log" "$HOME/.tklr-poller.log" "$HOME/.calcurse-alerts.log" "$HOME/old-tklr-reminders"; do
    [[ -e "$f" ]] && LEFTOVERS+=("$f")
done
if [[ ${#LEFTOVERS[@]} -gt 0 ]]; then
    echo
    echo "Unrelated leftovers left alone (delete by hand if you want):"
    for f in "${LEFTOVERS[@]}"; do echo "  $f"; done
fi
