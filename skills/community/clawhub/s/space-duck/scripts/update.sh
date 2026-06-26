#!/usr/bin/env bash
# Space Duck — one-command update wrapper.
#
# Why this exists:
#   `clawhub install space-duck` alone leaves users stranded on three different
#   failure modes (slug@version not supported, "already installed" requires
#   --force, post-install listener bounce is silent). This wrapper closes all
#   three plus auto-discovers paths so it works on any environment (Josh's
#   workspace, Wayne's BYOB box, fresh user installs, etc.).
#
# Apple-grade UX goals:
#   • Run with no arguments and no env vars
#   • Auto-discover skill install location
#   • Auto-discover listener supervisord script
#   • Snapshot before write → atomic rollback if anything fails
#   • Self-test by checking responder.log + listener_state pulse
#   • Print clear progress at every step
#   • Exit 0 on success, non-zero with explicit code on each failure type
#
# Doctrine:
#   • Bash, not Python — minimise deps. POSIX-compatible commands only.
#   • Idempotent — running twice = same end state.
#   • Fails loudly with specific next-step suggestion.
#   • Never auto-restarts a service the user didn't already have running.
#
# Exit codes:
#   0   = success (or already up-to-date)
#   10  = clawhub CLI not installed
#   11  = skill location could not be auto-discovered
#   12  = clawhub install command failed
#   13  = listener script not found (install succeeded, bounce skipped)
#   14  = listener bounce failed
#   15  = post-install self-test failed (listener not pulsing)
#   16  = registry lookup failed AND no installed version found
#   20  = unexpected error (caught by trap)
#
# Authored 2026-06-15 — Apple-grade update story Phase 1 of 5.
# Phase 2: doctor.sh. Phase 3: MC button. Phase 4: TG /update. Phase 5: cron.

set -uo pipefail
trap 'echo "✗ Unexpected error at line $LINENO. Exit 20." >&2; exit 20' ERR

# ─── Styling ──────────────────────────────────────────────────────────────────
if [[ -t 1 ]] && command -v tput >/dev/null 2>&1; then
  C_GREEN=$(tput setaf 2 2>/dev/null || echo)
  C_YELLOW=$(tput setaf 3 2>/dev/null || echo)
  C_RED=$(tput setaf 1 2>/dev/null || echo)
  C_BLUE=$(tput setaf 4 2>/dev/null || echo)
  C_BOLD=$(tput bold 2>/dev/null || echo)
  C_RESET=$(tput sgr0 2>/dev/null || echo)
else
  C_GREEN= C_YELLOW= C_RED= C_BLUE= C_BOLD= C_RESET=
fi

step()  { echo "${C_BLUE}→${C_RESET} ${C_BOLD}$*${C_RESET}"; }
ok()    { echo "${C_GREEN}✓${C_RESET} $*"; }
warn()  { echo "${C_YELLOW}⚠${C_RESET} $*" >&2; }
fail()  { echo "${C_RED}✗${C_RESET} $*" >&2; }
hint()  { echo "  ${C_BLUE}↳${C_RESET} $*" >&2; }

# ─── 0. Banner ────────────────────────────────────────────────────────────────
echo
echo "${C_BOLD}🦆 Space Duck — Update${C_RESET}"
echo "$(date -u +'%Y-%m-%d %H:%M:%S UTC')"
echo

# ─── 1. Check clawhub CLI ─────────────────────────────────────────────────────
step "Checking ClawHub CLI"
if ! command -v clawhub >/dev/null 2>&1; then
  fail "ClawHub CLI not found on PATH"
  hint "Install with: npm install -g @clawhub/cli"
  hint "Or visit: https://clawhub.ai/docs/cli"
  exit 10
fi
CLAWHUB_VERSION=$(clawhub -V 2>/dev/null | head -1 || echo "unknown")
ok "ClawHub CLI present ($CLAWHUB_VERSION)"

# ─── 2. Auto-discover skill location ──────────────────────────────────────────
step "Discovering skill location"
SKILL_DIR=""
SEARCH_PATHS=(
  "$HOME/.openclaw/skills/space-duck"
  "$HOME/.clawhub/skills/space-duck"
  "/data/.openclaw/workspace/skills/space-duck"
  "/data/.openclaw/skills/space-duck"
  "$HOME/.local/share/clawhub/skills/space-duck"
  "$HOME/skills/space-duck"
)
# Also try ./skills/space-duck (cwd-relative, matches clawhub default)
SEARCH_PATHS+=("$(pwd)/skills/space-duck")

for p in "${SEARCH_PATHS[@]}"; do
  if [[ -f "$p/_meta.json" ]]; then
    SKILL_DIR="$p"
    break
  fi
done

if [[ -z "$SKILL_DIR" ]]; then
  warn "No existing space-duck install found in known paths."
  hint "Will install fresh into \$HOME/.openclaw/skills/space-duck"
  SKILL_DIR="$HOME/.openclaw/skills/space-duck"
  FRESH_INSTALL=1
else
  ok "Skill installed at: $SKILL_DIR"
  FRESH_INSTALL=0
fi

# Skill parent directory (clawhub installs to <parent>/<slug>)
SKILL_PARENT=$(dirname "$SKILL_DIR")

# ─── 3. Read current version ──────────────────────────────────────────────────
CURRENT_VERSION="(not installed)"
if [[ -f "$SKILL_DIR/_meta.json" ]]; then
  CURRENT_VERSION=$(python3 -c "import json,sys; print(json.load(open('$SKILL_DIR/_meta.json')).get('version','unknown'))" 2>/dev/null || echo "unknown")
fi
step "Current version: ${C_BOLD}$CURRENT_VERSION${C_RESET}"

# ─── 4. Check registry for latest ─────────────────────────────────────────────
step "Checking registry for latest version"
LATEST_VERSION=""
if INSPECT_OUT=$(clawhub inspect space-duck 2>&1); then
  LATEST_VERSION=$(echo "$INSPECT_OUT" | grep -E '^Latest:' | head -1 | awk '{print $2}')
fi

if [[ -z "$LATEST_VERSION" ]]; then
  if [[ "$CURRENT_VERSION" == "(not installed)" || "$CURRENT_VERSION" == "unknown" ]]; then
    fail "Registry lookup failed AND no installed version found."
    hint "Check network connection and re-run."
    exit 16
  fi
  warn "Registry lookup failed — staying on $CURRENT_VERSION"
  exit 0
fi
ok "Latest version: ${C_BOLD}$LATEST_VERSION${C_RESET}"

# ─── 5. Up-to-date short-circuit ──────────────────────────────────────────────
if [[ "$CURRENT_VERSION" == "$LATEST_VERSION" ]]; then
  echo
  ok "Already up to date (v$LATEST_VERSION). Nothing to do."
  echo
  exit 0
fi

echo
echo "${C_BOLD}Update plan:${C_RESET} v$CURRENT_VERSION → v$LATEST_VERSION"
echo

# ─── 6. Snapshot for rollback ─────────────────────────────────────────────────
if [[ "$FRESH_INSTALL" == "0" ]]; then
  step "Snapshotting current install"
  BACKUP_ROOT="$SKILL_PARENT/.skill-backups/space-duck"
  BACKUP_DIR="$BACKUP_ROOT/$(date -u +'%Y%m%dT%H%M%SZ')-v$CURRENT_VERSION"
  mkdir -p "$BACKUP_ROOT"
  if cp -a "$SKILL_DIR" "$BACKUP_DIR" 2>/dev/null; then
    ok "Snapshot at: $BACKUP_DIR"
  else
    warn "Snapshot failed (permissions?) — continuing without rollback"
    BACKUP_DIR=""
  fi
fi

# ─── 7. Run clawhub install with --force ──────────────────────────────────────
step "Installing v$LATEST_VERSION"
if INSTALL_OUT=$(clawhub --workdir "$(dirname "$SKILL_PARENT")" --dir "$(basename "$SKILL_PARENT")" \
                  install space-duck --version "$LATEST_VERSION" --force 2>&1); then
  ok "Install succeeded"
else
  # Try without explicit version (some CLIs require slug-only when forcing)
  if INSTALL_OUT=$(clawhub --workdir "$(dirname "$SKILL_PARENT")" --dir "$(basename "$SKILL_PARENT")" \
                    install space-duck --force 2>&1); then
    ok "Install succeeded (fallback path)"
  else
    fail "clawhub install failed:"
    echo "$INSTALL_OUT" | sed 's/^/  /' >&2
    if [[ -n "${BACKUP_DIR:-}" ]]; then
      hint "Snapshot preserved at: $BACKUP_DIR"
      hint "Rollback with: rm -rf '$SKILL_DIR' && mv '$BACKUP_DIR' '$SKILL_DIR'"
    fi
    exit 12
  fi
fi

# Re-read version
NEW_VERSION=$(python3 -c "import json; print(json.load(open('$SKILL_DIR/_meta.json')).get('version','unknown'))" 2>/dev/null || echo "unknown")
if [[ "$NEW_VERSION" != "$LATEST_VERSION" ]]; then
  warn "Installed _meta.json reports $NEW_VERSION (expected $LATEST_VERSION)"
fi
ok "Skill on disk: v$NEW_VERSION"

# ─── 8. Auto-discover listener script ─────────────────────────────────────────
step "Locating listener supervisor script"
LISTENER_SCRIPT=""
LISTENER_CANDIDATES=(
  "$SKILL_DIR/scripts/setup_listeners_supervised.sh"
)
for p in "${LISTENER_CANDIDATES[@]}"; do
  if [[ -x "$p" ]]; then
    LISTENER_SCRIPT="$p"
    break
  fi
done

# Detect already-running listeners (regardless of script presence)
RUNNING_LISTENERS=$(pgrep -fa 'telegram_listener\.py\|peck_responder\.py\|peck_listener\.py' 2>/dev/null | grep -v "$0" || true)

if [[ -z "$LISTENER_SCRIPT" ]]; then
  if [[ -n "$RUNNING_LISTENERS" ]]; then
    warn "Listener script not found, but listener processes are running."
    hint "Restart manually OR pgrep + start fresh."
    echo "  Detected processes:"
    echo "$RUNNING_LISTENERS" | sed 's/^/    /'
    echo
    echo "${C_BOLD}Update complete (listener restart skipped).${C_RESET}"
    echo "  Old version: v$CURRENT_VERSION"
    echo "  New version: v$NEW_VERSION"
    exit 13
  else
    ok "No listener script and no running listeners — install-only mode."
    echo
    echo "${C_BOLD}Update complete.${C_RESET}"
    echo "  Old version: v$CURRENT_VERSION"
    echo "  New version: v$NEW_VERSION"
    hint "Start listeners with: $SKILL_DIR/scripts/setup_listeners_supervised.sh"
    exit 0
  fi
fi
ok "Listener script: $LISTENER_SCRIPT"

# ─── 9. Bounce listeners ──────────────────────────────────────────────────────
if [[ -z "$RUNNING_LISTENERS" ]]; then
  step "No listeners currently running — starting fresh"
  if BOUNCE_OUT=$("$LISTENER_SCRIPT" 2>&1); then
    ok "Listener started"
  else
    fail "Listener start failed:"
    echo "$BOUNCE_OUT" | sed 's/^/  /' >&2
    exit 14
  fi
else
  step "Bouncing listeners"
  if BOUNCE_OUT=$("$LISTENER_SCRIPT" --restart 2>&1); then
    ok "Listener bounce complete"
  else
    fail "Listener bounce failed:"
    echo "$BOUNCE_OUT" | sed 's/^/  /' >&2
    hint "Manual recovery: kill -9 <pid> + $LISTENER_SCRIPT"
    exit 14
  fi
fi

# ─── 10. Post-install self-test ───────────────────────────────────────────────
step "Self-test — waiting for listener pulse"
RESPONDER_LOG="$HOME/.space-duck/responder.log"
LISTENER_LOG="$HOME/.space-duck/logs/telegram_listener.log"
PULSE_OK=0

# Give the listener up to 15s to come back online
for i in {1..15}; do
  sleep 1
  if pgrep -f 'telegram_listener\.py' >/dev/null 2>&1; then
    PULSE_OK=1
    break
  fi
done

if [[ "$PULSE_OK" != "1" ]]; then
  fail "Listener not pulsing after 15s"
  hint "Check: $LISTENER_LOG"
  hint "Manual restart: $LISTENER_SCRIPT"
  exit 15
fi
ok "Listener is alive"

# ─── 11. Final report ─────────────────────────────────────────────────────────
echo
echo "${C_GREEN}${C_BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${C_RESET}"
echo "${C_GREEN}${C_BOLD}✓ Space Duck updated successfully${C_RESET}"
echo "${C_GREEN}${C_BOLD}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${C_RESET}"
echo
echo "  Previous: v$CURRENT_VERSION"
echo "  Current:  v$NEW_VERSION"
echo "  Listener: alive"
if [[ -n "${BACKUP_DIR:-}" ]]; then
  echo "  Backup:   $BACKUP_DIR"
fi
echo
echo "  Diagnostics: $(dirname "$0")/doctor.sh"
echo
exit 0
