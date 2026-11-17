#!/usr/bin/env bash
# Idempotent setup for the tklr-reminders skill. Safe to re-run.
#
#   bash install.sh
#
# --home exists but is not for you: the wrapper passes the workspace it already
# resolved. Naming one here puts the data where neither `tklr` in a terminal nor
# the scheduled dispatcher will look, and both report success anyway. An earlier
# agent copied this usage line, invented a path for it, and produced exactly
# that -- so the flag is not shown. `setup` now refuses it.
#
# Does four things, skipping whatever is already done:
#   1. installs tklr via uv (Hermes ships its own uv)
#   2. creates the tklr workspace (config.toml + tklr.db)
#   3. installs the dispatcher into ~/.hermes/scripts/
#   4. reports whether [alerts] channel letters have been defined yet
#
# It deliberately does NOT invent [alerts] letters, and does NOT create the
# cron job.
#
# HOST-SPECIFIC. Steps 1 and 3 assume a Hermes layout: uv shipped at
# $HERMES_HOME/bin/uv and off PATH, and a scheduler that will only run scripts
# living in ~/.hermes/scripts/. The Python side of the skill keeps all of this
# in scripts/host.py (see its header for what a port has to change); a shell
# script cannot import it, so these two steps are the shell half of the same
# seam. Step 3 is the one that disappears entirely on a host whose scheduler
# will run a script where it already lives.
#
# Not inventing letters matters: a letter defined as a placeholder no-op like
# 'true' would make the dispatcher treat every alert as successfully
# delivered and delete it, so reminders would silently reach nobody. Letters
# must be real delivery commands, which needs the user's channels — see
# templates/alerts-config-example.toml.

set -uo pipefail

# Mirrors tklr's own resolution: TKLR_HOME, then XDG_CONFIG_HOME/tklr, then
# ~/.config/tklr. Skipping the XDG step would build the workspace somewhere
# tklr never looks on any machine that sets it.
TKLR_HOME="${TKLR_HOME:-${XDG_CONFIG_HOME:-$HOME/.config}/tklr}"
TKLR_PYTHON="${TKLR_PYTHON:-}"
while [[ $# -gt 0 ]]; do
    case "$1" in
        --home) TKLR_HOME="$2"; shift 2 ;;
        --python) TKLR_PYTHON="$2"; shift 2 ;;
        *) echo "unknown argument: $1" >&2; exit 2 ;;
    esac
done

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# $HERMES_HOME, not $HOME/.hermes: host.py and the dispatcher both resolve the
# host directory that way, and this script writes the files THEY read. Hardcoding
# the default here put the dispatcher and the recorded paths somewhere the
# scheduler does not look, on any machine that sets it -- with every step
# reporting success. The `uv` lookup below already honoured it, so the script
# disagreed with itself as well as with the Python.
HERMES_HOME="${HERMES_HOME:-$HOME/.hermes}"
HERMES_SCRIPTS="$HERMES_HOME/scripts"
LOG_DIR="$HERMES_HOME/logs"
export PATH="$HOME/.local/bin:$PATH"

step() { printf '\n=== %s\n' "$1"; }
ok()   { printf '  ok: %s\n' "$1"; }
warn() { printf '  !! %s\n' "$1"; }

# Hermes installs itself with uv and ships its own copy, so on a Hermes machine
# uv always exists — at $HERMES_HOME/bin/uv, which is NOT on PATH. Prefer that
# one; fall back to a uv on PATH so the skill still works outside Hermes.
#
# We deliberately do NOT hunt for a system interpreter. `uv tool install
# --python '>=3.12'` reuses any suitable Python it can find and downloads one
# only if none exists, which is both simpler and more correct than guessing.
# (Never pass a bare `python3`: inside the Hermes agent that is the agent's own
# venv, which may be older than 3.12 — pip then reports "Could not find a
# version that satisfies the requirement tklr-dgraham", which reads like a
# missing package rather than a version mismatch.)
find_uv() {
    local c
    for c in "${UV:-}" "${HERMES_HOME:-$HOME/.hermes}/bin/uv" uv; do
        [[ -z "$c" ]] && continue
        c="$(command -v "$c" 2>/dev/null || { [[ -x "$c" ]] && echo "$c"; })"
        if [[ -n "$c" ]] && "$c" tool --help >/dev/null 2>&1; then echo "$c"; return 0; fi
    done
    return 1
}

# ---------------------------------------------------------------- 1. tklr
step "tklr installation"

# The floor lives in tklr_mutate.py, which is what actually depends on it, and
# is read from there rather than repeated: two copies of a version number drift
# the first time one is bumped, and the copy that stops matching is the one
# that silently stops gating.
TKLR_MIN="$(sed -n 's/^TESTED_AGAINST = "\([0-9.]*\)".*/\1/p' \
            "$SKILL_DIR/scripts/tklr_mutate.py" 2>/dev/null | head -1)"

# Reads the number out of "tklr version 1.0.43 (up to date)". grep -o, not sed:
# a BRE `.*` is greedy with no way to say otherwise, so the sed form matched the
# LAST digit run and reported 1.0.43 as "43" -- which compares older than every
# floor and would have refused every install.
tklr_version() { tklr --version 2>&1 | head -1 | grep -oE '[0-9]+(\.[0-9]+)+' | head -1; }

# True when $1 is older than $2. sort -V is the only version comparison
# available without leaving POSIX-ish shell, and it is right for these.
older_than() { [[ "$1" != "$2" ]] && [[ "$(printf '%s\n%s\n' "$1" "$2" | sort -V | head -1)" == "$1" ]]; }

check_tklr_version() {
    local have="$1"
    [[ -z "$TKLR_MIN" || -z "$have" ]] && return 0
    if older_than "$have" "$TKLR_MIN"; then
        warn "tklr $have is older than $TKLR_MIN, which this skill requires."
        warn ""
        warn "It reads tklr's Alerts table directly and depends on behaviour"
        warn "that differs in older releases, so it would fail in ways that"
        warn "look like bugs in the skill rather than a version mismatch."
        warn ""
        warn "Upgrade, then re-run this script:"
        warn "  uv tool upgrade tklr-dgraham    # or: pipx upgrade tklr-dgraham"
        return 1
    fi
    return 0
}

if command -v tklr >/dev/null 2>&1; then
    # Whose tklr this is matters when there is more than one on the machine:
    # this names the exact binary rather than leaving it to be guessed.
    ok "already installed — $(tklr --version 2>&1 | head -1) at $(command -v tklr)"
    ok "using the existing installation; nothing new will be installed"
    check_tklr_version "$(tklr_version)" || exit 1
else
    UV="$(find_uv)" || true
    if [[ -z "$UV" ]]; then
        warn "uv not found, so tklr cannot be installed."
        warn ""
        warn "uv is normally already present on a Hermes machine at"
        warn "  ${HERMES_HOME:-$HOME/.hermes}/bin/uv"
        warn "If it is there, point this script at it:"
        warn "  UV=${HERMES_HOME:-$HOME/.hermes}/bin/uv bash install.sh"
        warn ""
        warn "Otherwise install uv by whichever method its docs recommend for"
        warn "this machine — it brings its own Python and needs none to"
        warn "bootstrap, so it works where no Python is installed at all:"
        warn "  https://docs.astral.sh/uv/getting-started/installation/"
        warn "then re-run this script."
        exit 1
    fi
    ok "using uv at $UV ($("$UV" --version 2>&1 | head -1))"

    # '>=3.12' lets uv reuse any suitable interpreter already on the machine
    # and download one only if none qualifies. --python overrides it.
    PYSPEC="${TKLR_PYTHON:->=3.12}"
    echo "  installing tklr-dgraham (python $PYSPEC) ..."
    # --quiet: uv otherwise lists all 28 resolved packages. That output is
    # noise to a human and actively harmful to an agent, which has to read it
    # before deciding what to do next -- see run_installer() in the wrapper.
    if ! "$UV" tool install --quiet --python "$PYSPEC" tklr-dgraham; then
        warn "uv could not install tklr."
        warn "If pip reported 'Could not find a version that satisfies the"
        warn "requirement tklr-dgraham', that is a Python version mismatch, NOT a"
        warn "missing package — every release requires >= 3.12."
        exit 1
    fi

    hash -r 2>/dev/null || true
    if ! command -v tklr >/dev/null 2>&1; then
        # uv puts shims in ~/.local/bin; if that is not on PATH it is invisible.
        warn "installed, but 'tklr' is not on PATH — run: $UV tool update-shell"
        exit 1
    fi
    ok "installed — $(tklr --version 2>&1 | head -1) at $(command -v tklr)"
    # A fresh install of the current release should never trip this. It is here
    # because "the newest release is older than the floor" is worth failing on
    # loudly rather than discovering later inside a parse error.
    check_tklr_version "$(tklr_version)" || exit 1

    # Recorded because only this branch installed tklr. reset.sh used to infer
    # ownership from "uv reports it", which is not the same question: a user who
    # ran `uv tool install tklr-dgraham` before adding this skill has a uv-owned
    # tklr the skill did not install, and the reset would have removed their
    # copy. Written only here, never on the reuse branch, and cleared by reset.
    mkdir -p "$HERMES_SCRIPTS"
    printf 'tklr-dgraham\n' > "$HERMES_SCRIPTS/tklr-installed-by-skill" 2>/dev/null || true
fi

# ------------------------------------------------------------ 2. workspace
# The wrapper passes the workspace it already resolved, so this always matches
# for a real setup. It differs only when a person passed --home by hand, and
# that workspace is one `setup` will refuse to use, `tklr` will not read and the
# dispatcher will not poll -- everything here would still report success. Said
# out loud rather than left to the header, because a header is not read at the
# moment the flag is typed.
DEFAULT_TKLR_HOME="${XDG_CONFIG_HOME:-$HOME/.config}/tklr"
if [[ "$TKLR_HOME" != "$DEFAULT_TKLR_HOME" ]]; then
    warn "--home $TKLR_HOME is not the workspace tklr resolves ($DEFAULT_TKLR_HOME)."
    # No backticks in this string: bash runs them as a command substitution
    # inside double quotes, and the first draft of this warning executed tklr
    # and pasted its usage text into the middle of the sentence.
    warn "  Nothing will poll it, and running tklr by hand will not see it."
    warn "  Set TKLR_HOME or XDG_CONFIG_HOME for everything instead."
fi

step "workspace at $TKLR_HOME"
mkdir -p "$TKLR_HOME"
if [[ ! -f "$TKLR_HOME/tklr.db" ]]; then
    # Any read command bootstraps config.toml and tklr.db.
    tklr --home "$TKLR_HOME" alerts >/dev/null 2>&1 || true
fi
[[ -f "$TKLR_HOME/config.toml" ]] && ok "config.toml present" || warn "config.toml missing"
[[ -f "$TKLR_HOME/tklr.db" ]]     && ok "tklr.db present"     || warn "tklr.db missing"

# ------------------------------------------------------------ 3. dispatcher
step "dispatcher in $HERMES_SCRIPTS"
mkdir -p "$HERMES_SCRIPTS" "$LOG_DIR"
if install -m 0755 "$SKILL_DIR/scripts/tklr_alert_poller.py" \
        "$HERMES_SCRIPTS/tklr_alert_poller.py"; then
    ok "installed tklr_alert_poller.py"
else
    warn "could not copy the dispatcher"
    exit 1
fi

if python3 -c "import ast,sys; ast.parse(open(sys.argv[1]).read())" \
        "$HERMES_SCRIPTS/tklr_alert_poller.py" 2>/dev/null; then
    ok "poller parses cleanly"
else
    warn "poller failed to parse"
fi

# The wrapper stays in the skill directory, but a scheduled run has no way to
# learn where that is: the blueprint prompt is copied verbatim, so the
# ${HERMES_SKILL_DIR} token SKILL.md relies on is never substituted there. The
# skill directory has already moved once (a symlink under the host's skills dir
# to a git checkout named by skills.external_dirs) and every hardcoded path
# broke, silently, until an agent hit the missing file and improvised. Recording
# it beside the dispatcher gives anything running unattended one stable place to
# read, and this script is the only thing that already knows the answer.
if printf '%s\n' "$SKILL_DIR/scripts/tklr_agent_wrapper.py" \
        > "$HERMES_SCRIPTS/tklr-wrapper-path" 2>/dev/null; then
    ok "recorded wrapper path for scheduled runs"
else
    warn "could not record the wrapper path; the daily health check will fail"
fi

# --------------------------------------------- 4. are channel letters set up?
step "alert channels in $TKLR_HOME/config.toml"
LETTERS=$(python3 - "$TKLR_HOME/config.toml" <<'PY'
import sys, tomllib
from pathlib import Path
p = Path(sys.argv[1])
try:
    alerts = tomllib.loads(p.read_text(encoding="utf-8")).get("alerts") or {}
except Exception:
    alerts = {}
print(" ".join(sorted(k for k in alerts if k != "n")))
PY
)
if [[ -n "$LETTERS" ]]; then
    ok "letters defined: $LETTERS"
else
    warn "no channel letters defined yet — reminders using @a cannot be created"
fi

# ----------------------------------------------------------------- summary
step "next steps"
# Deliberately NOT a procedure. This block used to spell out the whole setup as
# numbered steps, and on 2026-08-07 an agent ran install.sh first, read them,
# and followed steps 2/3/5 verbatim -- copying the letter `a` and the sample
# message text character for character -- instead of the one command that does
# all of it. A complete ordered recipe will always beat a single instruction
# elsewhere, so the recipe is gone. `setup` runs this script itself; nothing
# below needs doing by hand.
cat <<EOF
  FOR THE AGENT — do NOT continue by hand from here. This script only installs
  tklr and the workspace; it configures no channel and schedules no delivery.

  Run this one command. It is idempotent, it calls this script for you, and it
  does everything that is left — alert channel, dispatcher, cron job, and a
  test alert that proves delivery works:

    python3 $SKILL_DIR/scripts/tklr_agent_wrapper.py setup --platform <the platform this conversation is on>

  Then wait for the test alert to arrive and ask the user whether it did.
  Report what it can now do with:

    python3 $SKILL_DIR/scripts/tklr_agent_wrapper.py --home $TKLR_HOME welcome

  and send that output verbatim. Never show the user a wrapper command.
EOF
echo
echo "tklr home: $TKLR_HOME"
echo "log:       $LOG_DIR/tklr-alerts.log"
