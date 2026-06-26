#!/bin/bash
# =============================================================================
# lib.sh — shared functions for Time Clawshine
# Sourced by all bin/ scripts via: source "$TC_ROOT/lib.sh"
# =============================================================================

# --- Resolve config path -----------------------------------------------------
# lib.sh lives at project root — no ".." needed
TC_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="${TC_CONFIG:-$TC_ROOT/config.yaml}"

[[ -f "$CONFIG_FILE" ]] || { echo "[time-clawshine] ERROR: config.yaml not found at $CONFIG_FILE"; exit 1; }

# --- YAML parser (requires yq v4) -------------------------------------------
_cfg() {
    # Usage: _cfg '.repository.path'
    yq e "$1" "$CONFIG_FILE"
}

_cfg_list() {
    # Usage: _cfg_list '.backup.paths[]'  → one item per line
    yq e "$1" "$CONFIG_FILE"
}

# --- Load config into variables ----------------------------------------------
tc_load_config() {
    REPO=$(_cfg '.repository.path')
    PASS_FILE=$(_cfg '.repository.password_file')
    KEEP_LAST=$(_cfg '.retention.keep_last')
    LOG_FILE=$(_cfg '.logging.file')
    # shellcheck disable=SC2034  # Used by scripts sourcing lib.sh (e.g. backup.sh)
    VERBOSE=$(_cfg '.logging.verbose')
    CRON_EXPR=$(_cfg '.schedule.cron')

    TG_ENABLED=$(_cfg '.notifications.telegram.enabled')
    TG_TOKEN=$(_cfg '.notifications.telegram.bot_token')
    TG_CHAT_ID=$(_cfg '.notifications.telegram.chat_id')
    TG_DAILY_DIGEST=$(_cfg '.notifications.telegram.daily_digest')

    HC_ENABLED=$(_cfg '.notifications.healthcheck.enabled')
    HC_URL=$(_cfg '.notifications.healthcheck.url')
    HC_PING_START=$(_cfg '.notifications.healthcheck.ping_start')

    PRIVACY_LOCAL_ONLY=$(_cfg '.privacy.local_only')
    PRIVACY_SEND_ERROR_DETAILS=$(_cfg '.privacy.send_error_details')
    PRIVACY_INCLUDE_HOSTNAME=$(_cfg '.privacy.include_hostname')

    CHECK_EVERY=$(_cfg '.integrity.check_every')
    MIN_DISK_MB=$(_cfg '.safety.min_disk_mb')
    UPDATE_CHECK=$(_cfg '.updates.check')

    # Defaults for optional fields
    [[ -z "$CHECK_EVERY"    || "$CHECK_EVERY"    == "null" ]] && CHECK_EVERY=0
    [[ -z "$MIN_DISK_MB"    || "$MIN_DISK_MB"    == "null" ]] && MIN_DISK_MB=0
    [[ -z "$TG_DAILY_DIGEST" || "$TG_DAILY_DIGEST" == "null" ]] && TG_DAILY_DIGEST=false
    [[ -z "$UPDATE_CHECK"   || "$UPDATE_CHECK"   == "null" ]] && UPDATE_CHECK=true
    [[ -z "$HC_ENABLED"     || "$HC_ENABLED"     == "null" ]] && HC_ENABLED=false
    [[ -z "$HC_URL"         || "$HC_URL"         == "null" ]] && HC_URL=""
    [[ -z "$HC_PING_START"  || "$HC_PING_START"  == "null" ]] && HC_PING_START=true
    [[ -z "$PRIVACY_LOCAL_ONLY"         || "$PRIVACY_LOCAL_ONLY"         == "null" ]] && PRIVACY_LOCAL_ONLY=true
    [[ -z "$PRIVACY_SEND_ERROR_DETAILS" || "$PRIVACY_SEND_ERROR_DETAILS" == "null" ]] && PRIVACY_SEND_ERROR_DETAILS=false
    [[ -z "$PRIVACY_INCLUDE_HOSTNAME"   || "$PRIVACY_INCLUDE_HOSTNAME"   == "null" ]] && PRIVACY_INCLUDE_HOSTNAME=false

    # Validate critical config values
    _require_cfg() {
        local name="$1" val="$2"
        if [[ -z "$val" || "$val" == "null" ]]; then
            echo "[time-clawshine] ERROR: config.yaml missing required field: $name"
            exit 1
        fi
    }
    _require_cfg 'repository.path'          "$REPO"
    _require_cfg 'repository.password_file' "$PASS_FILE"
    _require_cfg 'retention.keep_last'      "$KEEP_LAST"
    _require_cfg 'logging.file'             "$LOG_FILE"

    # Validate password file exists (skip during setup — file is created later)
    if [[ ! -f "$PASS_FILE" ]] && [[ "${TC_SKIP_PASS_CHECK:-}" != "true" ]]; then
        echo "[time-clawshine] ERROR: Password file not found: $PASS_FILE"
        echo "Without it, no backup or restore is possible."
        exit 1
    fi

    # Build backup paths array (standard + extra)
    mapfile -t _BASE_PATHS  < <(_cfg_list '.backup.paths[]')
    mapfile -t _EXTRA_PATHS < <(_cfg_list '.backup.extra_paths[]' 2>/dev/null || true)
    BACKUP_PATHS=("${_BASE_PATHS[@]}")
    for p in "${_EXTRA_PATHS[@]}"; do
        [[ -n "$p" && "$p" != "null" ]] && BACKUP_PATHS+=("$p")
    done

    # Build exclude flags array (standard + extra)
    mapfile -t _BASE_EX  < <(_cfg_list '.backup.exclude[]')
    mapfile -t _EXTRA_EX < <(_cfg_list '.backup.extra_excludes[]' 2>/dev/null || true)
    EXCLUDES=()
    for ex in "${_BASE_EX[@]}" "${_EXTRA_EX[@]}"; do
        [[ -n "$ex" && "$ex" != "null" ]] && EXCLUDES+=("--exclude=$ex")
    done

    # Validate config types
    tc_validate_config
}

# --- Config schema validation ------------------------------------------------
tc_validate_config() {
    local errors=()

    _validate_bool() {
        local name="$1" val="$2"
        case "$val" in
            true|false) ;;
            *) errors+=("$name must be true or false (got: '$val')") ;;
        esac
    }

    _is_loopback_http_url() {
        local url="$1"
        [[ "$url" =~ ^http://(localhost|127\.0\.0\.1|127\.[0-9]+\.[0-9]+\.[0-9]+|\[::1\])(:[0-9]+)?(/|$) ]]
    }

    _validate_external_url() {
        local name="$1" url="$2"
        if [[ "$url" =~ ^https:// ]]; then
            return 0
        fi
        if _is_loopback_http_url "$url"; then
            return 0
        fi
        errors+=("$name must use https:// unless it points to loopback localhost")
    }

    # retention.keep_last must be a positive integer
    if ! [[ "$KEEP_LAST" =~ ^[0-9]+$ ]] || [[ "$KEEP_LAST" -le 0 ]]; then
        errors+=("retention.keep_last must be a positive integer (got: '$KEEP_LAST')")
    fi

    # safety.min_disk_mb must be a non-negative integer
    if ! [[ "$MIN_DISK_MB" =~ ^[0-9]+$ ]]; then
        errors+=("safety.min_disk_mb must be a non-negative integer (got: '$MIN_DISK_MB')")
    fi

    # integrity.check_every must be a non-negative integer
    if ! [[ "$CHECK_EVERY" =~ ^[0-9]+$ ]]; then
        errors+=("integrity.check_every must be a non-negative integer (got: '$CHECK_EVERY')")
    fi

    # schedule.cron must look like a cron expression (5 fields)
    if [[ -n "$CRON_EXPR" && "$CRON_EXPR" != "null" ]]; then
        local field_count
        field_count=$(echo "$CRON_EXPR" | awk '{print NF}')
        if [[ "$field_count" -ne 5 ]]; then
            errors+=("schedule.cron must have 5 fields (got $field_count: '$CRON_EXPR')")
        fi
    fi

    # backup.paths must have at least one entry
    if [[ ${#BACKUP_PATHS[@]} -eq 0 ]]; then
        errors+=("backup.paths must have at least one path")
    fi

    _validate_bool 'notifications.telegram.enabled' "$TG_ENABLED"
    _validate_bool 'notifications.telegram.daily_digest' "$TG_DAILY_DIGEST"
    _validate_bool 'notifications.healthcheck.enabled' "$HC_ENABLED"
    _validate_bool 'notifications.healthcheck.ping_start' "$HC_PING_START"
    _validate_bool 'privacy.local_only' "$PRIVACY_LOCAL_ONLY"
    _validate_bool 'privacy.send_error_details' "$PRIVACY_SEND_ERROR_DETAILS"
    _validate_bool 'privacy.include_hostname' "$PRIVACY_INCLUDE_HOSTNAME"
    _validate_bool 'updates.check' "$UPDATE_CHECK"

    # telegram: if enabled, token and chat_id must be set
    if [[ "$TG_ENABLED" == "true" ]]; then
        [[ -z "$TG_TOKEN" || "$TG_TOKEN" == "null" ]] && \
            errors+=("notifications.telegram.bot_token is required when enabled: true")
        [[ -z "$TG_CHAT_ID" || "$TG_CHAT_ID" == "null" ]] && \
            errors+=("notifications.telegram.chat_id is required when enabled: true")
    fi

    # healthcheck: if enabled, url must be set
    if [[ "$HC_ENABLED" == "true" ]]; then
        [[ -z "$HC_URL" || "$HC_URL" == "null" ]] && \
            errors+=("notifications.healthcheck.url is required when enabled: true")
        [[ -n "$HC_URL" && "$HC_URL" != "null" ]] && \
            _validate_external_url 'notifications.healthcheck.url' "$HC_URL"
    fi

    # local_only is a hard privacy gate. External integrations require users to
    # set it false explicitly so setup cannot enable egress by accident.
    if [[ "$PRIVACY_LOCAL_ONLY" == "true" ]]; then
        [[ "$TG_ENABLED" == "true" ]] && \
            errors+=("privacy.local_only is true; set it to false before enabling Telegram")
        [[ "$HC_ENABLED" == "true" ]] && \
            errors+=("privacy.local_only is true; set it to false before enabling healthcheck")
        [[ "$UPDATE_CHECK" == "true" ]] && \
            errors+=("privacy.local_only is true; set it to false before enabling update checks")
    fi

    if [[ ${#errors[@]} -gt 0 ]]; then
        echo "[time-clawshine] CONFIG VALIDATION ERRORS:"
        for e in "${errors[@]}"; do echo "  ✗ $e"; done
        exit 1
    fi
}

# --- Logging -----------------------------------------------------------------
timestamp() { date '+%Y-%m-%d %H:%M:%S'; }

log() {
    local level="${1:-INFO}"
    local msg="${2:-}"
    echo "[$(timestamp)] [$level] $msg" | tee -a "$LOG_FILE"
}

log_info()  { log "INFO " "$1"; }
log_warn()  { log "WARN " "$1"; }
log_error() { log "ERROR" "$1"; }

# --- Telegram ----------------------------------------------------------------
tg_send() {
    local msg="$1"
    [[ "$PRIVACY_LOCAL_ONLY" == "true" ]] && return 0
    [[ "$TG_ENABLED" != "true" ]]     && return 0
    [[ -z "$TG_TOKEN" ]]              && return 0
    [[ "$TG_TOKEN" == "null" ]]       && return 0
    [[ -z "$TG_CHAT_ID" ]]            && return 0
    [[ "$TG_CHAT_ID" == "null" ]]     && return 0

    curl -s -X POST \
        "https://api.telegram.org/bot${TG_TOKEN}/sendMessage" \
        -H "Content-Type: application/json" \
        -d "$(jq -n \
            --arg chat_id "$TG_CHAT_ID" \
            --arg text "$msg" \
            '{chat_id: $chat_id, text: $text, parse_mode: "Markdown"}')" \
        > /dev/null 2>&1 || true
}

_external_hostname_line() {
    [[ "$PRIVACY_INCLUDE_HOSTNAME" == "true" ]] || return 0
    local hostname; hostname=$(hostname 2>/dev/null || echo "unknown")
    printf 'Host: %s\n' "$hostname"
}

_redact_external_text() {
    local input="$1"
    head -c 600 <<< "$input" \
        | sed -E \
            -e 's#[[:alnum:]_.-]+:[[:alnum:]_/@%+=.,:-]+#/[redacted-secret]#g' \
            -e 's#/[[:alnum:]_./@%+:-]+#/[redacted-path]#g' \
            -e 's#([Tt]oken|[Pp]assword|[Ss]ecret|[Kk]ey)=([^[:space:]]+)#\1=[redacted]#g'
}

tg_failure() {
    local error_msg="$1"
    local host_line details_line=""
    host_line=$(_external_hostname_line)

    if [[ "$PRIVACY_SEND_ERROR_DETAILS" == "true" ]]; then
        local safe_msg
        safe_msg=$(_redact_external_text "$error_msg")
        [[ ${#error_msg} -gt 600 ]] && safe_msg+=$'\n[...truncated]'
        details_line=$'\nDetails (redacted):\n```\n'"$safe_msg"$'\n```'
    fi

    tg_send "🔴 *Time Clawshine — Backup FALHOU*
${host_line}Time: $(timestamp)
Status: backup action failed. Check local logs with status.sh.${details_line}"
}

# --- Healthcheck (healthchecks.io / hc-style endpoints) ---------------------
# Pings <url>[/state] with a short timeout. Non-blocking — failures are logged
# but never abort the backup.
# Usage: hc_send                 → success ping (URL as-is)
#        hc_send /start          → mark backup started
#        hc_send /fail [msg]     → mark backup failed (optional body)
hc_send() {
    [[ "$PRIVACY_LOCAL_ONLY" == "true" ]] && return 0
    [[ "$HC_ENABLED" != "true" ]]   && return 0
    [[ -z "$HC_URL" ]]              && return 0
    [[ "$HC_URL" == "null" ]]       && return 0

    local state="${1:-}"
    local body="${2:-}"
    local url="${HC_URL%/}${state}"
    [[ "$PRIVACY_SEND_ERROR_DETAILS" != "true" ]] && body=""

    if [[ -n "$body" ]]; then
        curl -fsS -m 10 --retry 2 --data-raw "$body" "$url" >/dev/null 2>&1 \
            || log_warn "Healthcheck ping failed for state '${state:-success}'"
    else
        curl -fsS -m 10 --retry 2 "$url" >/dev/null 2>&1 \
            || log_warn "Healthcheck ping failed for state '${state:-success}'"
    fi
}

# --- Scheduler helpers -------------------------------------------------------
_tc_pad2() {
    printf '%02d' "$((10#$1))"
}

_tc_cron_time_field_to_systemd() {
    local value="$1"
    local max="$2"
    local max_step="$3"

    if [[ "$value" == "*" ]]; then
        printf '*'
        return 0
    fi

    if [[ "$value" =~ ^\*/([0-9]+)$ ]]; then
        local step="${BASH_REMATCH[1]}"
        local step_num=$((10#$step))
        if [[ "$step_num" -lt 1 || "$step_num" -gt "$max_step" ]]; then
            return 1
        fi
        printf '00/%s' "$step_num"
        return 0
    fi

    local IFS=',' part part_num
    local -a parts out=()
    read -r -a parts <<< "$value"
    for part in "${parts[@]}"; do
        if ! [[ "$part" =~ ^[0-9]+$ ]]; then
            return 1
        fi
        part_num=$((10#$part))
        if [[ "$part_num" -lt 0 || "$part_num" -gt "$max" ]]; then
            return 1
        fi
        out+=("$(_tc_pad2 "$part_num")")
    done

    [[ ${#out[@]} -gt 0 ]] || return 1
    (IFS=','; printf '%s' "${out[*]}")
}

tc_cron_to_systemd_calendar() {
    local expr="$1"
    local minute hour day month weekday extra
    read -r minute hour day month weekday extra <<< "$expr"

    [[ -n "${minute:-}" && -n "${hour:-}" && -n "${day:-}" && -n "${month:-}" && -n "${weekday:-}" ]] || return 1
    [[ -z "${extra:-}" ]] || return 1

    # systemd calendar day/month/week semantics do not map 1:1 to every cron
    # expression. Convert only daily/hourly/minutely schedules that preserve
    # the user's requested cadence exactly; setup falls back to cron otherwise.
    [[ "$day" == "*" && "$month" == "*" && "$weekday" == "*" ]] || return 1

    local systemd_minute systemd_hour
    systemd_minute=$(_tc_cron_time_field_to_systemd "$minute" 59 59) || return 1
    systemd_hour=$(_tc_cron_time_field_to_systemd "$hour" 23 23) || return 1

    printf '*-*-* %s:%s:00\n' "$systemd_hour" "$systemd_minute"
}

# --- Restic wrapper ----------------------------------------------------------
restic_cmd() {
    RESTIC_PASSWORD_FILE="$PASS_FILE" restic -r "$REPO" "$@"
}

# --- Validation --------------------------------------------------------------
# Filter BACKUP_PATHS to only paths that currently exist. A missing path is a
# warning (logged + skipped), not a fatal error — typical on fresh OpenClaw
# installs where some optional dirs (e.g. ~/.openclaw/cron) only appear once
# the user creates cron jobs. We still fail loudly if EVERY configured path is
# missing, since that means there is genuinely nothing to back up.
tc_validate_paths() {
    local existing=()
    local missing=()
    for path in "${BACKUP_PATHS[@]}"; do
        if [[ -e "$path" ]]; then
            existing+=("$path")
        else
            missing+=("$path")
        fi
    done

    if [[ ${#missing[@]} -gt 0 ]]; then
        log_warn "Skipping ${#missing[@]} configured path(s) that do not exist: ${missing[*]}"
    fi

    if [[ ${#existing[@]} -eq 0 ]]; then
        log_error "No backup paths exist — nothing to back up (configured: ${BACKUP_PATHS[*]})"
        tg_failure "No backup paths exist. Check backup.paths in config.yaml."
        return 1
    fi

    BACKUP_PATHS=("${existing[@]}")
    return 0
}

tc_check_deps() {
    local missing=()
    for cmd in restic yq curl jq openssl; do
        command -v "$cmd" &>/dev/null || missing+=("$cmd")
    done
    if [[ ${#missing[@]} -gt 0 ]]; then
        echo "[time-clawshine] ERROR: Missing dependencies: ${missing[*]}"
        echo "Run: sudo bin/setup.sh"
        exit 1
    fi
}

# --- Version -----------------------------------------------------------------
tc_current_version() {
    local skill_json="$TC_ROOT/skill.json"
    if [[ -f "$skill_json" ]] && command -v jq &>/dev/null; then
        jq -r '.version' "$skill_json" 2>/dev/null || echo "unknown"
    else
        echo "unknown"
    fi
}

# --- Update check ------------------------------------------------------------
# Quick (max 5s) ClawHub probe used by backup.sh's daily check and by
# status.sh. Sets:
#   TC_UPDATE_STATE   = "uptodate" | "newer" | "error"
#   TC_UPDATE_VERSION = remote version when known (empty on error)
#   TC_UPDATE_ERROR   = short reason string when state == error
# Always returns 0 — failures surface via TC_UPDATE_STATE so callers can
# render a descriptive message instead of just "could not reach ClawHub".
tc_check_update() {
    local current="${1:-$(tc_current_version)}"
    local url="https://clawhub.com/api/v1/skills/quick-backup-restore"
    TC_UPDATE_STATE="error"
    TC_UPDATE_VERSION=""
    TC_UPDATE_ERROR=""

    if [[ "${PRIVACY_LOCAL_ONLY:-true}" == "true" || "${UPDATE_CHECK:-false}" != "true" ]]; then
        TC_UPDATE_STATE="disabled"
        TC_UPDATE_ERROR="disabled by privacy/update configuration"
        return 0
    fi

    local body http_code curl_err
    body=$(curl -fsS --max-time 5 -w '\n%{http_code}' "$url" 2>&1)
    curl_err=$?
    if [[ $curl_err -ne 0 ]]; then
        # Strip the trailing \n%{http_code} line; it isn't present on hard failures.
        TC_UPDATE_ERROR="network error (curl exit $curl_err): ${body//$'\n'/ }"
        return 0
    fi

    http_code="${body##*$'\n'}"
    local json="${body%$'\n'*}"
    if [[ "$http_code" != "200" ]]; then
        TC_UPDATE_ERROR="HTTP $http_code from ClawHub"
        return 0
    fi

    TC_UPDATE_VERSION=$(jq -r '.version // empty' <<< "$json" 2>/dev/null || true)
    if [[ -z "$TC_UPDATE_VERSION" ]]; then
        # shellcheck disable=SC2034  # Read by callers after tc_check_update returns.
        TC_UPDATE_ERROR="ClawHub response had no .version field"
        return 0
    fi

    if [[ "$TC_UPDATE_VERSION" == "$current" ]]; then
        TC_UPDATE_STATE="uptodate"
    else
        # shellcheck disable=SC2034  # Read by callers after tc_check_update returns.
        TC_UPDATE_STATE="newer"
    fi
    return 0
}

# --- Telegram digest ---------------------------------------------------------
tg_digest() {
    local snapshot_count="$1"
    local repo_size="$2"
    local disk_free="$3"
    local host_line
    host_line=$(_external_hostname_line)
    tg_send "📊 *Time Clawshine — Resumo diário*
${host_line}Time: $(timestamp)

Snapshots: $snapshot_count
Repository: $repo_size
Disk free: $disk_free"
}

# --- Disk space check --------------------------------------------------------
tc_check_disk() {
    local min_mb="$1"
    [[ "$min_mb" -le 0 ]] 2>/dev/null && return 0
    local repo_dir; repo_dir=$(dirname "$REPO")
    local avail_kb; avail_kb=$(df --output=avail "$repo_dir" 2>/dev/null | tail -1 | tr -d ' ')
    if [[ -z "$avail_kb" || "$avail_kb" == "Avail" ]]; then
        log_warn "Could not determine free disk space — skipping disk guard"
        return 0
    fi
    local avail_mb=$(( avail_kb / 1024 ))
    if [[ $avail_mb -lt $min_mb ]]; then
        log_error "Disk space too low: ${avail_mb}MB free < ${min_mb}MB minimum"
        tg_failure "Disco quase cheio: ${avail_mb}MB livre, mínimo configurado: ${min_mb}MB. Backup abortado."
        return 1
    fi
    return 0
}
