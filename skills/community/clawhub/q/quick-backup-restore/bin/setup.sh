#!/bin/bash
# =============================================================================
# bin/setup.sh — Time Clawshine initial setup
# Run once as root: sudo bin/setup.sh
# =============================================================================

set -euo pipefail

TC_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
source "$TC_ROOT/lib.sh"

# Flags
SKIP_BACKUP=false
NO_SYSTEM=false
ASSUME_YES=false
DRY_RUN=false
for arg in "$@"; do
    case "$arg" in
        --skip-backup)       SKIP_BACKUP=true ;;
        --no-system-install) NO_SYSTEM=true ;;
        --assume-yes|-y)     ASSUME_YES=true ;;
        --dry-run)           DRY_RUN=true ;;
        --help|-h)
            echo "Usage: sudo bin/setup.sh [options]"
            echo ""
            echo "Options:"
            echo "  --skip-backup          Skip initial validation backup after setup"
            echo "  --no-system-install    Repo-only setup: no apt-get, no cron/systemd, no /usr/local/bin"
            echo "  --assume-yes, -y       Skip confirmation prompts (for CI/automated use)"
            echo "  --dry-run              Preview dependencies, files, and scheduler without changes"
            echo "  --help, -h             Show this help"
            exit 0
            ;;
    esac
done

if [[ "$DRY_RUN" == "true" ]]; then
    echo "╔══════════════════════════════════════╗"
    echo "║    Time Clawshine — Setup Preview    ║"
    echo "╚══════════════════════════════════════╝"
    echo ""
    echo "No changes will be made."
    echo ""

    echo "Dependencies:"
    for cmd in restic yq curl jq openssl; do
        if command -v "$cmd" &>/dev/null; then
            echo "  - $cmd: present"
        else
            echo "  - $cmd: would need installation"
        fi
    done

    echo ""
    CONFIG_PREVIEW_LOADED=false
    if command -v yq &>/dev/null; then
        export TC_SKIP_PASS_CHECK=true
        if tc_load_config; then
            CONFIG_PREVIEW_LOADED=true
            echo "Repository and data:"
            echo "  - Repository path       : $REPO"
            echo "  - Password file         : $PASS_FILE"
            echo "  - Log file              : $LOG_FILE"
            echo "  - Retention             : keep last $KEEP_LAST snapshots"
            echo "  - Backup paths          : ${BACKUP_PATHS[*]}"
            echo "  - Privacy local_only    : $PRIVACY_LOCAL_ONLY"
            echo "  - Telegram enabled      : $TG_ENABLED"
            echo "  - Healthcheck enabled   : $HC_ENABLED"
            echo "  - Update check          : $UPDATE_CHECK"
        else
            echo "Config could not be loaded; fix validation errors above before setup."
            exit 1
        fi
    else
        echo "Config preview skipped because yq is not installed yet."
    fi

    echo ""
    if [[ "$NO_SYSTEM" == "true" ]]; then
        echo "System changes: none (--no-system-install)"
    else
        echo "System changes that would be applied with root:"
        echo "  - Install missing apt packages as needed: restic, curl, jq"
        echo "  - Install yq from GitHub with SHA256 verification if absent"
        echo "  - Install /usr/local/bin/time-clawshine"
        echo "  - Create /usr/local/bin/quick-backup-restore symlink"
        if [[ -d /run/systemd/system ]] && command -v systemctl &>/dev/null; then
            if [[ "$CONFIG_PREVIEW_LOADED" == "true" ]]; then
                if SYSTEMD_PREVIEW=$(tc_cron_to_systemd_calendar "$CRON_EXPR"); then
                    echo "  - Register /etc/systemd/system/time-clawshine.{service,timer} (OnCalendar=$SYSTEMD_PREVIEW)"
                else
                    echo "  - Register /etc/cron.d/time-clawshine (preserves schedule.cron exactly)"
                fi
            else
                echo "  - Register systemd timer or cron after config can be loaded"
            fi
        else
            echo "  - Register /etc/cron.d/time-clawshine"
        fi
        echo "  - Configure /etc/logrotate.d/time-clawshine"
        echo "  - Restrict config.yaml permissions to 600"
    fi
    echo ""
    echo "Run without --dry-run when you are ready to apply."
    exit 0
fi

# Must run as root
[[ $EUID -eq 0 ]] || { echo "ERROR: Run as root (sudo bin/setup.sh)"; exit 1; }

echo "╔══════════════════════════════════════╗"
echo "║    Time Clawshine — Setup            ║"
echo "╚══════════════════════════════════════╝"
echo ""

# --- Ensure all scripts are executable (git may strip +x on some platforms) --
chmod +x "$TC_ROOT/bin/"*.sh "$TC_ROOT/lib.sh" 2>/dev/null || true

# --- Detect and migrate v2.x artifacts --------------------------------------
_migrate_v2() {
    local v2_artifacts=()
    [[ -f "/etc/cron.d/quick-backup-restore" ]]        && v2_artifacts+=("/etc/cron.d/quick-backup-restore")
    [[ -f "/etc/logrotate.d/quick-backup-restore" ]]    && v2_artifacts+=("/etc/logrotate.d/quick-backup-restore")
    [[ -f "/var/lock/quick-backup-restore.lock" ]]      && v2_artifacts+=("/var/lock/quick-backup-restore.lock")
    for f in /var/tmp/quick-backup-restore-*; do
        [[ -e "$f" ]] && v2_artifacts+=("$f")
    done

    [[ ${#v2_artifacts[@]} -eq 0 ]] && return 0

    echo ""
    echo "==> Detected v2.x installation artifacts:"
    for a in "${v2_artifacts[@]}"; do echo "    - $a"; done
    echo ""
    echo "    These will be cleaned up. Your repository, password, and snapshots are preserved."

    if [[ "$ASSUME_YES" != "true" ]]; then
        read -rp "    Proceed with migration? [Y/n]: " CONFIRM_MIG
        [[ "$CONFIRM_MIG" =~ ^[Nn]$ ]] && { echo "    Skipping migration."; return 0; }
    fi

    for a in "${v2_artifacts[@]}"; do
        rm -f "$a" && echo "    Removed: $a"
    done

    # Rename v2 marker files to v3 equivalents
    for old_marker in /var/tmp/quick-backup-restore-check-counter \
                      /var/tmp/quick-backup-restore-digest-date \
                      /var/tmp/quick-backup-restore-update-date; do
        if [[ -f "$old_marker" ]]; then
            new_marker="${old_marker//quick-backup-restore/time-clawshine}"
            mv "$old_marker" "$new_marker" 2>/dev/null && echo "    Renamed: $old_marker → $new_marker"
        fi
    done

    echo "    ✓ v2 migration complete"
    echo ""
}

_migrate_v2

# --- Install dependencies ---------------------------------------------------
if [[ "$NO_SYSTEM" == "true" ]]; then
    echo "==> --no-system-install: skipping dependency installation"
    tc_check_deps || { echo "ERROR: Dependencies missing. Install manually or run without --no-system-install"; exit 1; }
else
    echo "==> Checking dependencies..."

    # Build list of missing packages. yq comes from GitHub (not apt) — track
    # apt deps separately so we only invoke apt-get update when actually needed.
    MISSING_PKGS=()
    NEED_APT_UPDATE=false
    for pkg in restic curl jq; do
        if ! command -v "$pkg" &>/dev/null; then
            MISSING_PKGS+=("$pkg")
            NEED_APT_UPDATE=true
        fi
    done
    if ! command -v yq &>/dev/null; then
        MISSING_PKGS+=("yq (from GitHub)")
    fi

    if [[ ${#MISSING_PKGS[@]} -gt 0 ]]; then
        echo "==> The following dependencies will be installed:"
        for p in "${MISSING_PKGS[@]}"; do echo "    - $p"; done
        if [[ "$ASSUME_YES" != "true" ]]; then
            read -rp "Proceed? [y/N]: " CONFIRM_DEPS
            [[ "$CONFIRM_DEPS" =~ ^[Yy]$ ]] || { echo "Aborted."; exit 0; }
        fi
    else
        echo "    All dependencies already installed — OK"
    fi

    install_pkg() {
        local pkg="$1"
        if ! command -v "$pkg" &>/dev/null; then
            echo "    Installing $pkg..."
            apt-get install -qq -y "$pkg"
        else
            echo "    $pkg already installed — OK"
        fi
    }

    # Only refresh the apt index when at least one apt-managed dep is missing.
    # When all bins are present, apt-get update just produces noise (and can
    # spam unrelated repo warnings) without changing the install outcome.
    if [[ "$NEED_APT_UPDATE" == "true" ]]; then
        apt-get update -qq
    else
        echo "    Skipping apt-get update (all apt-managed deps already present)"
    fi

    install_pkg restic
    install_pkg curl
    install_pkg jq

    # yq — install from GitHub if not present (apt version often outdated)
    if ! command -v yq &>/dev/null; then
        echo "    Installing yq..."
        YQ_VERSION="v4.44.1"
        YQ_BIN="/usr/local/bin/yq"
        case "$(uname -m)" in
            x86_64)  YQ_BINARY="yq_linux_amd64" ;;
            aarch64) YQ_BINARY="yq_linux_arm64" ;;
            armv7l)  YQ_BINARY="yq_linux_arm" ;;
            *)       echo "    ERROR: Unsupported architecture: $(uname -m)"; exit 1 ;;
        esac
        YQ_URL="https://github.com/mikefarah/yq/releases/download/${YQ_VERSION}/${YQ_BINARY}"
        YQ_BSD_URL="https://github.com/mikefarah/yq/releases/download/${YQ_VERSION}/checksums-bsd"

        # 1. Download checksum FIRST (fail early if unavailable)
        EXPECTED_SHA=$(curl -fsSL "$YQ_BSD_URL" | grep "^SHA256 (${YQ_BINARY})" | awk -F'= ' '{print $2}')
        if [[ -z "$EXPECTED_SHA" ]]; then
            echo "    ERROR: Could not fetch yq checksum — refusing unverified binary install"
            exit 1
        fi

        # 2. Download binary to a temporary path so an unverified file never
        # replaces an existing yq installation.
        YQ_TMP=$(mktemp)
        curl -fsSL "$YQ_URL" -o "$YQ_TMP"

        # 3. Verify checksum
        ACTUAL_SHA=$(sha256sum "$YQ_TMP" | awk '{print $1}')
        if [[ "$EXPECTED_SHA" != "$ACTUAL_SHA" ]]; then
            rm -f "$YQ_TMP"
            echo "    ERROR: yq checksum mismatch! Expected $EXPECTED_SHA, got $ACTUAL_SHA"
            echo "    Temporary binary removed. Possible supply chain compromise — investigate before retrying."
            exit 1
        fi
        install -m 755 "$YQ_TMP" "$YQ_BIN"
        rm -f "$YQ_TMP"
        chmod +x "$YQ_BIN"
        echo "    yq $YQ_VERSION installed (checksum verified) — OK"
    else
        echo "    yq already installed — OK"
    fi
fi

# --- Load config (after deps are ready) ------------------------------------
export TC_SKIP_PASS_CHECK=true  # password file may not exist yet during setup
tc_load_config

# --- Create repository directory -------------------------------------------
echo ""
echo "==> Creating repository directory: $REPO"
mkdir -p "$REPO"
chmod 700 "$REPO"

# --- Generate password (skip if already exists) ----------------------------
echo ""
if [[ -f "$PASS_FILE" ]]; then
    echo "==> Password file already exists: $PASS_FILE — skipping generation"
else
    echo "==> Generating restic encryption password..."
    mkdir -p "$(dirname "$PASS_FILE")"
    # Safety: refuse to overwrite if file appeared between check and write
    if [[ -f "$PASS_FILE" ]]; then
        echo "    WARN: Password file appeared unexpectedly at $PASS_FILE — not overwriting"
    else
        # Generate 48 random bytes from openssl's CSPRNG and base64-encode them
        # so the password is printable ASCII (restic stores the encryption key
        # as a plain string in this file). 'set -C' (noclobber) refuses to
        # overwrite if the path was created racing the [[ -f ]] check above.
        # The redirect target on the right of '>' is $PASS_FILE — a path on
        # local disk; this line does no remote IO.
        ( set -C; openssl rand -base64 48 > "$PASS_FILE" ) 2>/dev/null \
            || { echo "ERROR: Could not write password to $PASS_FILE"; exit 1; }
        chmod 600 "$PASS_FILE"
    fi
    echo ""
    echo "    ┌──────────────────────────────────────────────────────────┐"
    echo "    │  Password saved to: $PASS_FILE"
    echo "    │                                                          │"
    echo "    │  *** BACK THIS UP — without it, no restore is possible, │"
    echo "    │  even if the repo is intact ***                         │"
    echo "    └──────────────────────────────────────────────────────────┘"
    echo ""
    echo "    To view the password later: sudo cat $PASS_FILE"
fi

# --- Initialize restic repo ------------------------------------------------
echo ""
echo "==> Initializing restic repository..."
if restic_cmd snapshots &>/dev/null; then
    echo "    Repository already initialized — OK"
else
    restic_cmd init
    echo "    Repository initialized — OK"
fi

# --- Install backup script to bin ------------------------------------------
if [[ "$NO_SYSTEM" == "true" ]]; then
    echo ""
    echo "==> --no-system-install: skipping binary install, cron, and config permissions"
    CRON_FILE="N/A (--no-system-install)"
else
    echo ""
    echo "==> Installing backup script to /usr/local/bin/time-clawshine..."
    cp "$TC_ROOT/bin/backup.sh" /usr/local/bin/time-clawshine
    # Inject TC_ROOT so the installed script knows where to find config
    sed -i "s|^TC_ROOT=.*|TC_ROOT=\"$TC_ROOT\"|" /usr/local/bin/time-clawshine
    chmod 755 /usr/local/bin/time-clawshine
    # Backward-compat symlink (v2 name)
    ln -sf /usr/local/bin/time-clawshine /usr/local/bin/quick-backup-restore

    # --- Register scheduler (systemd preferred, cron fallback) ------------------
    # Detect systemd as PID 1. 'systemctl is-system-running' returns non-zero
    # for 'degraded' state (any unrelated unit failed), which used to send us
    # down the cron fallback path on otherwise-healthy hosts and could end up
    # leaving BOTH cron and a pre-existing timer firing. /run/systemd/system
    # is the canonical "systemd is the init system" check.
    HAVE_SYSTEMD=false
    if [[ -d /run/systemd/system ]] && command -v systemctl &>/dev/null; then
        HAVE_SYSTEMD=true
    fi

    USE_SYSTEMD_TIMER=false
    SYSTEMD_CALENDAR=""
    if [[ "$HAVE_SYSTEMD" == "true" ]]; then
        if SYSTEMD_CALENDAR=$(tc_cron_to_systemd_calendar "$CRON_EXPR"); then
            USE_SYSTEMD_TIMER=true
        else
            echo ""
            echo "    WARN: schedule.cron is not supported by the systemd converter."
            echo "          Using cron.d instead so the requested schedule is preserved."
        fi
    fi

    echo ""
    if [[ "$USE_SYSTEMD_TIMER" == "true" ]]; then
        echo "==> Registering systemd timer: [$CRON_EXPR -> $SYSTEMD_CALENDAR]"

        UNIT_DIR="/etc/systemd/system"

        cat > "$UNIT_DIR/time-clawshine.service" <<EOF
[Unit]
Description=Time Clawshine — encrypted incremental backup
After=network.target

[Service]
Type=oneshot
Environment=TC_CONFIG=$CONFIG_FILE
ExecStart=/usr/local/bin/time-clawshine
# StandardOutput=journal (NOT append:LOG_FILE) — log() already writes to
# LOG_FILE via tee(1). Capturing stdout to the same file too would duplicate
# every line. Errors/unexpected stderr still land in the journal:
#   journalctl -u time-clawshine.service
StandardOutput=journal
StandardError=journal
EOF

        cat > "$UNIT_DIR/time-clawshine.timer" <<EOF
[Unit]
Description=Time Clawshine — scheduled backup timer

[Timer]
OnCalendar=$SYSTEMD_CALENDAR
Persistent=true
RandomizedDelaySec=30

[Install]
WantedBy=timers.target
EOF

        systemctl daemon-reload
        systemctl enable --now time-clawshine.timer
        # Short form keeps the summary box within its 36-char field. The full
        # unit name is implicit and discoverable via `systemctl status`.
        CRON_FILE="systemd timer @ $SYSTEMD_CALENDAR"
        echo "    Systemd timer enabled: $SYSTEMD_CALENDAR"

        # Remove cron if it exists (migrating to systemd)
        for legacy_cron in "/etc/cron.d/quick-backup-restore" "/etc/cron.d/time-clawshine"; do
            [[ -f "$legacy_cron" ]] && rm -f "$legacy_cron" && echo "    Removed legacy cron: $legacy_cron"
        done
    else
        echo "==> Registering cron job: [$CRON_EXPR]"

        # Before installing cron, tear down any pre-existing systemd timer
        # left over from a previous install where systemd WAS available — we
        # never want both cron AND timer firing the backup back-to-back.
        if command -v systemctl &>/dev/null; then
            systemctl disable --now time-clawshine.timer 2>/dev/null || true
            for unit in /etc/systemd/system/time-clawshine.timer \
                        /etc/systemd/system/time-clawshine.service; do
                if [[ -f "$unit" ]]; then
                    rm -f "$unit"
                    echo "    Removed pre-existing systemd unit: $unit"
                fi
            done
            systemctl daemon-reload 2>/dev/null || true
        fi

        CRON_FILE="/etc/cron.d/time-clawshine"
        cat > "$CRON_FILE" <<EOF
# Time Clawshine — scheduled backup
# Generated by setup.sh on $(date)
# Edit schedule in config.yaml, then re-run setup.sh
$CRON_EXPR root TC_CONFIG=$CONFIG_FILE /usr/local/bin/time-clawshine >/dev/null 2>> $LOG_FILE
EOF
        chmod 644 "$CRON_FILE"
        echo "    Cron registered at: $CRON_FILE"
    fi

    # --- Configure logrotate ---------------------------------------------------
    echo ""
    echo "==> Configuring logrotate for $LOG_FILE..."
    LOGROTATE_FILE="/etc/logrotate.d/time-clawshine"
    cat > "$LOGROTATE_FILE" <<EOF
$LOG_FILE {
    weekly
    rotate 4
    compress
    missingok
    notifempty
    create 640 root root
}
EOF
    chmod 644 "$LOGROTATE_FILE"
    echo "    Logrotate configured at: $LOGROTATE_FILE"

    # --- Restrict config.yaml permissions (may contain Telegram token) ----------
    chmod 600 "$CONFIG_FILE"
    echo "    config.yaml permissions set to 600"
fi

# --- Run initial backup to validate ----------------------------------------
# Capture the result instead of exiting immediately on failure: the core
# install (deps, repo, scheduler, logrotate) may all have completed fine even
# if this first backup didn't run cleanly. We still want the user to see the
# summary box so they know exactly what IS in place before deciding what to
# fix or retry.
VALIDATION_RESULT="skipped (--skip-backup)"
VALIDATION_EXIT=0
if [[ "$SKIP_BACKUP" != "true" ]]; then
    echo ""
    echo "==> Running initial backup to validate setup..."
    if TC_CONFIG="$CONFIG_FILE" "$TC_ROOT/bin/backup.sh"; then
        VALIDATION_RESULT="success"
    else
        VALIDATION_EXIT=$?
        VALIDATION_RESULT="FAILED (exit $VALIDATION_EXIT)"
    fi
fi

# --- Summary ---------------------------------------------------------------
if [[ "$VALIDATION_EXIT" -eq 0 ]]; then
    SETUP_HEADER="Setup complete [OK]"
else
    SETUP_HEADER="Setup partial -- see validation"
fi

# ASCII-only padding so printf '%-Ns' pads BYTES that equal visual columns.
# Box-drawing characters in the borders (╔ ═ ╗ etc.) are multi-byte but
# echoed as fixed-width literals, so the borders themselves stay aligned.
# Field values must stay ASCII; truncate long values to keep the right
# border vertical.
_field_fit() {
    local val="$1" max=36
    if [[ ${#val} -gt $max ]]; then
        # Truncate with ASCII ellipsis so printf '%-Ns' byte-padding stays
        # consistent with visual columns. Reserve 3 cols for "...".
        printf '%s...' "${val:0:max-3}"
    else
        printf '%s' "$val"
    fi
}

echo ""
echo "╔══════════════════════════════════════════════════════╗"
printf "║  %-50s  ║\n" "$SETUP_HEADER"
echo "╠══════════════════════════════════════════════════════╣"
printf "║  Repository   : %-36s ║\n" "$(_field_fit "$REPO")"
printf "║  Password     : %-36s ║\n" "$(_field_fit "$PASS_FILE")"
printf "║  Scheduler    : %-36s ║\n" "$(_field_fit "$CRON_FILE")"
printf "║  Log          : %-36s ║\n" "$(_field_fit "$LOG_FILE")"
printf "║  Retention    : %-36s ║\n" "$KEEP_LAST snapshots"
printf "║  Validation   : %-36s ║\n" "$(_field_fit "$VALIDATION_RESULT")"
echo "╚══════════════════════════════════════════════════════╝"
echo ""

if [[ "$VALIDATION_EXIT" -ne 0 ]]; then
    echo "  ⚠ Core install OK, but the first backup did not finish cleanly."
    echo "    Logs       : tail $LOG_FILE"
    echo "    Retry now  : sudo /usr/local/bin/time-clawshine"
    echo "    Common fix : create any missing backup.paths listed in the log."
    exit "$VALIDATION_EXIT"
fi

echo "  Restore helper: sudo bin/restore.sh"
echo "  View snapshots: restic -r $REPO --password-file $PASS_FILE snapshots"
