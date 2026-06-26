#!/bin/bash
# =============================================================================
# bin/customize.sh — Time Clawshine local path customization
#
# Analyzes your system locally (no API calls, no data leaves the machine) to suggest:
#   - Extra paths worth backing up (whitelist)
#   - Additional exclusion patterns (blacklist)
#
# Always shows suggestions and asks for confirmation before changing anything.
# Updates config.yaml only after explicit user approval.
#
# Usage: sudo bin/customize.sh
# =============================================================================

set -euo pipefail

TC_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# --- Early --help (before sourcing lib.sh so it works without config) -------
for arg in "$@"; do
    case "$arg" in
        --help|-h)
            echo "Usage: sudo bin/customize.sh"
            echo ""
            echo "Analyzes your system locally (no API calls, 100% offline) and suggests:"
            echo "  - Extra paths worth backing up (e.g. ~/.config, custom scripts)"
            echo "  - Junk patterns to exclude (e.g. node_modules, *.log)"
            echo "  - Credential stores like ~/.ssh and ~/.gnupg are not auto-suggested"
            echo ""
            echo "Shows suggestions and asks for confirmation before modifying config.yaml."
            exit 0
            ;;
    esac
done

source "$TC_ROOT/lib.sh"

tc_check_deps
tc_load_config

# Must run as root
[[ $EUID -eq 0 ]] || { echo "ERROR: Run as root (sudo bin/customize.sh)"; exit 1; }

echo "╔════════════════════════════════════════════════════════════════════╗"
echo "║      Time Clawshine — Customize Backup Paths                ║"
echo "╚════════════════════════════════════════════════════════════════════╝"
echo ""
echo "This command will:"
echo "  1. Analyze your system paths locally"
echo "  2. Detect extra paths that may be worth backing up"
echo "  3. Scan for common junk patterns to exclude"
echo "  4. Show you the suggestions"
echo "  5. Ask for your confirmation before changing anything"
echo ""
echo "  100% local — no data leaves this machine."
echo ""
read -rp "Continue? [y/N]: " CONFIRM
[[ "$CONFIRM" =~ ^[Yy]$ ]] || { echo "Aborted."; exit 0; }

# --- Helper: check if a path is already covered by BACKUP_PATHS --------------
_is_covered() {
    local candidate="$1"
    for bp in "${BACKUP_PATHS[@]}"; do
        # Direct match or candidate is under an already-backed-up path
        [[ "$candidate" == "$bp" ]] && return 0
        [[ "$candidate" == "$bp"/* ]] && return 0
        # Already-backed-up path is under candidate (candidate is a parent)
        [[ "$bp" == "$candidate"/* ]] && return 0
    done
    return 1
}

# --- Whitelist: detect important paths not already covered --------------------
echo ""
echo "==> Scanning for extra paths worth backing up..."

WHITELIST_SUGGESTIONS=()

# Hardcoded well-known important directories
    CANDIDATE_IMPORTANT=(
    "$HOME/bin"
    "$HOME/.config"
    "$HOME/.local/share"
    "$HOME/.bashrc"
    "$HOME/.profile"
    "$HOME/.zshrc"
)

for candidate in "${CANDIDATE_IMPORTANT[@]}"; do
    [[ -e "$candidate" ]] || continue
    _is_covered "$candidate" && continue
    WHITELIST_SUGGESTIONS+=("$candidate")
done

# Also scan $HOME depth-1 for directories that might be important
while IFS= read -r dir; do
    [[ -d "$dir" ]] || continue
    # Skip known unimportant dirs
    dirname=$(basename "$dir")
    case "$dirname" in
        .cache|.git|.local|.config|.ssh|.gnupg|.npm|.cargo|.venv|__pycache__|node_modules|.tmp|tmp|.Trash*)
            continue ;;
    esac
    _is_covered "$dir" && continue
    # Only suggest if it contains files (not empty)
    if [[ -n "$(find "$dir" -maxdepth 1 -type f 2>/dev/null | head -1)" ]]; then
        WHITELIST_SUGGESTIONS+=("$dir")
    fi
done < <(find "$HOME" -maxdepth 1 -mindepth 1 -type d 2>/dev/null | sort)

# --- Blacklist: detect common junk patterns -----------------------------------
echo "==> Scanning for common exclusion patterns..."

BLACKLIST_SUGGESTIONS=()

# Hardcoded common junk patterns
JUNK_PATTERNS=(
    "node_modules"
    "*.log"
    "*.cache"
    ".venv"
    "*.mp4"
    "*.mkv"
    "*.iso"
    "*.zip"
    "*.tar.gz"
    "cache"
    "tmp"
    ".npm"
    ".cargo/registry"
)

# Current excludes without --exclude= prefix
CURRENT_EXCLUDES=()
for ex in "${EXCLUDES[@]}"; do
    CURRENT_EXCLUDES+=("${ex#--exclude=}")
done

for pattern in "${JUNK_PATTERNS[@]}"; do
    # Skip if already in current excludes
    already=false
    for ex in "${CURRENT_EXCLUDES[@]}"; do
        [[ "$ex" == "$pattern" ]] && { already=true; break; }
    done
    [[ "$already" == "true" ]] && continue

    # Only suggest if at least one match exists in backup paths
    found=false
    for bp in "${BACKUP_PATHS[@]}"; do
        [[ -d "$bp" ]] || continue
        if [[ -n "$(find "$bp" -maxdepth 3 -name "$pattern" 2>/dev/null | head -1)" ]]; then
            found=true
            break
        fi
    done
    [[ "$found" == "true" ]] && BLACKLIST_SUGGESTIONS+=("$pattern")
done

# --- Show suggestions --------------------------------------------------------
echo ""
echo "┌─────────────────────────────────────────────────────────┐"
echo "│              Local Analysis Suggestions                 │"
echo "├─────────────────────────────────────────────────────────┤"
echo "│  Credential stores like ~/.ssh and ~/.gnupg are not      │"
echo "│  auto-suggested. Add them manually only with strong      │"
echo "│  controls for repo access and password-file backup.      │"
echo "│                                                         │"

if [[ ${#WHITELIST_SUGGESTIONS[@]} -eq 0 ]]; then
    echo "│  Extra paths (whitelist): none suggested                │"
else
    echo "│  Extra paths to ADD to backup:                          │"
    for path in "${WHITELIST_SUGGESTIONS[@]}"; do
        printf "│    + %-51s │\n" "$path"
    done
fi

echo "│                                                         │"

if [[ ${#BLACKLIST_SUGGESTIONS[@]} -eq 0 ]]; then
    echo "│  Exclusions (blacklist): none suggested                 │"
else
    echo "│  Patterns to EXCLUDE from backup:                       │"
    for pat in "${BLACKLIST_SUGGESTIONS[@]}"; do
        printf "│    - %-51s │\n" "$pat"
    done
fi

echo "└─────────────────────────────────────────────────────────┘"

# --- Bail early if nothing to do ---------------------------------------------
if [[ ${#WHITELIST_SUGGESTIONS[@]} -eq 0 && ${#BLACKLIST_SUGGESTIONS[@]} -eq 0 ]]; then
    echo ""
    echo "No extra suggestions. Your current config.yaml is already optimal."
    echo "You can always edit backup.extra_paths and backup.extra_excludes manually."
    exit 0
fi

# --- Confirmation gate -------------------------------------------------------
echo ""
echo "⚠️  Review the suggestions above carefully before accepting."
echo "   Your current config.yaml will be updated."
echo "   A backup of the original will be saved as config.yaml.bak"
echo ""
read -rp "Apply these suggestions to config.yaml? [y/N]: " APPLY
[[ "$APPLY" =~ ^[Yy]$ ]] || { echo "Aborted. config.yaml unchanged."; exit 0; }

# --- Apply to config.yaml ----------------------------------------------------
echo ""
echo "==> Saving config.yaml.bak..."
cp "$CONFIG_FILE" "${CONFIG_FILE}.bak"

echo "==> Updating config.yaml..."

# Sanitize function — only allow safe characters (whitelist approach)
_sanitize_entry() {
    local entry="$1"
    if [[ ! "$entry" =~ ^[a-zA-Z0-9/_.*@:~-]+$ ]]; then
        echo "    ⚠ Skipped unsafe entry (invalid chars): $entry" >&2
        return 1
    fi
    return 0
}

# Add whitelist entries to extra_paths
for path in "${WHITELIST_SUGGESTIONS[@]}"; do
    _sanitize_entry "$path" || continue
    # Skip if already in standard paths or extra_paths
    if ! grep -qF "$path" "$CONFIG_FILE"; then
        yq e -i ".backup.extra_paths += [\"$path\"]" "$CONFIG_FILE"
        echo "    + Added path: $path"
    else
        echo "    ~ Already present: $path"
    fi
done

# Add blacklist entries to extra_excludes
for pat in "${BLACKLIST_SUGGESTIONS[@]}"; do
    _sanitize_entry "$pat" || continue
    if ! grep -qF "$pat" "$CONFIG_FILE"; then
        yq e -i ".backup.extra_excludes += [\"$pat\"]" "$CONFIG_FILE"
        echo "    - Added exclude: $pat"
    else
        echo "    ~ Already present: $pat"
    fi
done

# --- Re-register cron with updated config ------------------------------------
echo ""
echo "==> Re-running setup to apply updated config..."
bash "$TC_ROOT/bin/setup.sh" --skip-backup

echo ""
echo "╔══════════════════════════════════════════════════════╗"
echo "║              Customization complete ✓                ║"
echo "╠══════════════════════════════════════════════════════╣"
echo "║  config.yaml updated                                 ║"
echo "║  Original saved as config.yaml.bak                  ║"
echo "║  Run 'sudo bin/backup.sh' to test the new config     ║"
echo "╚══════════════════════════════════════════════════════╝"
