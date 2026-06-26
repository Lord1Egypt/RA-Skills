#!/bin/bash
# Synology Backup — Shared library
# Source this in all scripts: source "$(dirname "$0")/lib.sh"

# ---------------------------------------------------------------------------
# Config loading + validation (no eval, all vars quoted, explicit patterns)
# ---------------------------------------------------------------------------

load_config() {
    local config="$1"
    if [[ ! -f "$config" ]]; then
        echo "Error: Config not found at $config" >&2
        exit 1
    fi
    if ! jq empty "$config" 2>/dev/null; then
        echo "Error: Config is not valid JSON: $config" >&2
        exit 1
    fi

    # Export CONFIG so validate_config can use it for backupPaths iteration
    CONFIG="$config"

    HOST="$(jq -r '.host' "$config")"
    SHARE="$(jq -r '.share' "$config")"
    MOUNT="$(jq -r '.mountPoint // "/mnt/synology"' "$config")"
    CREDS="$(jq -r '.credentialsFile' "$config" | sed "s|^~|$HOME|")"
    SMB_VER="$(jq -r '.smbVersion // "3.0"' "$config")"
    RETENTION="$(jq -r '.retention // 7' "$config")"
    PRE_RESTORE_RETENTION="$(jq -r '.preRestoreRetention // 3' "$config")"
    INCLUDE_SUBAGENT="$(jq -r '.includeSubAgentWorkspaces // true' "$config")"
    TRANSPORT="$(jq -r '.transport // "smb"' "$config")"
    SSH_USER="$(jq -r '.sshUser // ""' "$config")"
    SSH_HOST="$(jq -r '.sshHost // .host' "$config")"
    SSH_PORT="$(jq -r '.sshPort // "22"' "$config")"
    SSH_DEST="$(jq -r '.sshDest // ""' "$config")"
    TELEGRAM_TARGET="$(jq -r '.telegramTarget // ""' "$config")"
    NOTIFY_ON_SUCCESS="$(jq -r '.notifyOnSuccess // false' "$config")"
    if [[ "$NOTIFY_ON_SUCCESS" != "true" && "$NOTIFY_ON_SUCCESS" != "false" ]]; then
        NOTIFY_ON_SUCCESS="false"
    fi
    STATE_FILE="$(jq -r '.stateFile // ""' "$config" | sed "s|^~|$HOME|")"
    # Default state file alongside config
    [[ -z "$STATE_FILE" ]] && STATE_FILE="$(dirname "$config")/.synology-backup-state.json"

    validate_config
}

validate_config() {
    # Host: safe hostnames/IPs only
    if [[ -z "$HOST" || "$HOST" == "null" ]]; then
        echo "Error: host is required in config" >&2; exit 1
    fi
    if ! [[ "$HOST" =~ ^[a-zA-Z0-9._-]+$ ]]; then
        echo "Error: host contains invalid characters" >&2; exit 1
    fi

    # Share path: alphanumeric, slashes, hyphens, underscores, dots
    if [[ -z "$SHARE" || "$SHARE" == "null" ]]; then
        echo "Error: share is required in config" >&2; exit 1
    fi
    if ! [[ "$SHARE" =~ ^[a-zA-Z0-9/_.-]+$ ]]; then
        echo "Error: share contains invalid characters" >&2; exit 1
    fi
    if [[ "$SHARE" == *".."* ]]; then
        echo "Error: share must not contain path traversal (..)" >&2; exit 1
    fi

    # Mount point: absolute path
    if [[ -z "$MOUNT" || "$MOUNT" == "null" ]]; then
        echo "Error: mountPoint is required" >&2; exit 1
    fi
    if ! [[ "$MOUNT" =~ ^/[a-zA-Z0-9/_.-]+$ ]]; then
        echo "Error: mountPoint must be an absolute path with safe characters" >&2; exit 1
    fi
    if [[ "$MOUNT" == *".."* ]]; then
        echo "Error: mountPoint must not contain path traversal (..)" >&2; exit 1
    fi

    # SMB version: digits and dots only
    if ! [[ "$SMB_VER" =~ ^[0-9.]+$ ]]; then
        echo "Error: smbVersion contains invalid characters" >&2; exit 1
    fi

    # Retention: positive integers
    if ! [[ "$RETENTION" =~ ^[0-9]+$ ]]; then
        echo "Error: retention must be a non-negative integer" >&2; exit 1
    fi
    if ! [[ "$PRE_RESTORE_RETENTION" =~ ^[0-9]+$ ]]; then
        echo "Error: preRestoreRetention must be a non-negative integer" >&2; exit 1
    fi

    # Boolean
    if [[ "$INCLUDE_SUBAGENT" != "true" && "$INCLUDE_SUBAGENT" != "false" ]]; then
        echo "Error: includeSubAgentWorkspaces must be true or false" >&2; exit 1
    fi

    # Transport: explicit allowlist
    if [[ "$TRANSPORT" != "smb" && "$TRANSPORT" != "ssh" ]]; then
        echo "Error: transport must be 'smb' or 'ssh'" >&2; exit 1
    fi

    # Credentials file (required for SMB)
    if [[ "$TRANSPORT" == "smb" ]]; then
        if [[ -z "$CREDS" || "$CREDS" == "null" || ! -f "$CREDS" ]]; then
            echo "Error: credentialsFile not found: $CREDS" >&2; exit 1
        fi
    fi

    # SSH validation
    if [[ "$TRANSPORT" == "ssh" ]]; then
        if [[ -z "$SSH_USER" || "$SSH_USER" == "null" ]]; then
            echo "Error: sshUser is required for ssh transport" >&2; exit 1
        fi
        if ! [[ "$SSH_USER" =~ ^[a-zA-Z0-9_-]+$ ]]; then
            echo "Error: sshUser contains invalid characters" >&2; exit 1
        fi
        # Validate SSH_HOST independently (may differ from HOST)
        if [[ -z "$SSH_HOST" || "$SSH_HOST" == "null" ]]; then
            echo "Error: sshHost is required for ssh transport" >&2; exit 1
        fi
        if ! [[ "$SSH_HOST" =~ ^[a-zA-Z0-9._-]+$ ]]; then
            echo "Error: sshHost contains invalid characters" >&2; exit 1
        fi
        if [[ -z "$SSH_DEST" || "$SSH_DEST" == "null" ]]; then
            echo "Error: sshDest (remote backup path) is required for ssh transport" >&2; exit 1
        fi
        # sshDest: alphanumeric, slashes, hyphens, underscores, dots — no traversal or metacharacters
        if ! [[ "$SSH_DEST" =~ ^[a-zA-Z0-9/_.-]+$ ]]; then
            echo "Error: sshDest contains invalid characters" >&2; exit 1
        fi
        if [[ "$SSH_DEST" == *".."* ]]; then
            echo "Error: sshDest must not contain path traversal (..)" >&2; exit 1
        fi
        if ! [[ "$SSH_PORT" =~ ^[0-9]+$ ]]; then
            echo "Error: sshPort must be a number" >&2; exit 1
        fi
    fi

    # Validate all backup paths
    while IFS= read -r path_raw; do
        validate_path "$path_raw"
    done < <(jq -r '.backupPaths[]' "$CONFIG")
}

validate_path() {
    local p="$1"
    if [[ -z "$p" ]]; then return; fi
    # Reject command substitution, semicolons, pipes, backticks, path traversal
    if [[ "$p" == *'$('* || "$p" == *'`'* || "$p" == *';'* || \
          "$p" == *'|'* || "$p" == *'&'* || "$p" == *".."* ]]; then
        echo "Error: backupPath contains unsafe characters: $p" >&2
        exit 1
    fi
    # Must start with ~ or /
    if ! [[ "$p" =~ ^[~/] ]]; then
        echo "Error: backupPath must be absolute or home-relative (~): $p" >&2
        exit 1
    fi
}

# ---------------------------------------------------------------------------
# Build rsync exclude args from config (backupExclude list)
# ---------------------------------------------------------------------------

build_exclude_args() {
    local -a args=()
    # Built-in sensible defaults
    args+=(--exclude='.git/' --exclude='node_modules/' --exclude='__pycache__/'
           --exclude='*.pyc' --exclude='.DS_Store' --exclude='Thumbs.db'
           --exclude='*.tmp' --exclude='*.swp')
    # User-configured excludes
    local count
    count="$(jq -r '.backupExclude | length // 0' "$CONFIG" 2>/dev/null || echo 0)"
    if [[ "$count" -gt 0 ]]; then
        while IFS= read -r pattern; do
            [[ -z "$pattern" ]] && continue
            # Validate: no shell metacharacters beyond glob wildcards
            if [[ "$pattern" == *'$('* || "$pattern" == *'`'* || \
                  "$pattern" == *';'* || "$pattern" == *'|'* || "$pattern" == *'&'* ]]; then
                echo "Warning: skipping unsafe exclude pattern: $pattern" >&2
                continue
            fi
            args+=(--exclude="$pattern")
        done < <(jq -r '.backupExclude[]' "$CONFIG")
    fi
    printf '%s\n' "${args[@]}"
}

# ---------------------------------------------------------------------------
# Mount helpers
# ---------------------------------------------------------------------------

ensure_mounted() {
    if mountpoint -q "$MOUNT" 2>/dev/null; then
        return 0
    fi
    mkdir -p -- "$MOUNT"
    if [[ "$TRANSPORT" == "smb" ]]; then
        mount -t cifs "//${HOST}/${SHARE}" "$MOUNT" \
            -o "credentials=${CREDS},vers=${SMB_VER}"
        echo "Mounted //${HOST}/${SHARE} → $MOUNT"
    fi
    # SSH transport: no local mount needed — rsync connects directly
}

# Mount with retry + health check.
# Retries up to 3 times with 10s sleep between attempts.
# After successful mount, verifies the NAS is responsive with a write test.
ensure_mounted_with_retry() {
    local max_attempts=3
    local attempt

    for (( attempt=1; attempt<=max_attempts; attempt++ )); do
        echo "Mount attempt $attempt/$max_attempts..."

        # Try to mount
        if ensure_mounted; then
            # For SSH transport, no mount health check needed
            if [[ "$TRANSPORT" == "ssh" ]]; then
                echo "SSH transport — no mount needed"
                return 0
            fi

            # Health check: verify the NAS is actually responsive
            if touch "$MOUNT/.ping" 2>/dev/null && rm -f "$MOUNT/.ping" 2>/dev/null; then
                echo "Mount health check passed"
                return 0
            else
                echo "⚠️  Mount exists but NAS not responsive (write test failed)" >&2
                # Try to unmount and re-mount on next attempt
                umount "$MOUNT" 2>/dev/null || true
            fi
        else
            echo "⚠️  Mount failed on attempt $attempt" >&2
        fi

        if [[ "$attempt" -lt "$max_attempts" ]]; then
            echo "Retrying in 10s..."
            sleep 10
        fi
    done

    echo "Error: Failed to mount after $max_attempts attempts" >&2
    return 1
}

# Remote path helper for SSH transport
remote_path() {
    local subpath="$1"
    echo "${SSH_USER}@${SSH_HOST}:${SSH_DEST}/${subpath}"
}

# Rsync with SSH transport support
# Dereferences symlinks (--copy-links) to avoid I/O errors on SMB/NAS
rsync_to_dest() {
    local src="$1"
    local dest_subpath="$2"
    local -a exclude_args
    mapfile -t exclude_args < <(build_exclude_args)

    if [[ "$TRANSPORT" == "ssh" ]]; then
        rsync -a --copy-links --delete -e "ssh -p ${SSH_PORT} -o BatchMode=yes -o StrictHostKeyChecking=yes" \
            "${exclude_args[@]}" -- \
            "$src" "$(remote_path "$dest_subpath")"
    else
        rsync -a --copy-links --delete \
            "${exclude_args[@]}" -- \
            "$src" "$dest_subpath"
    fi
}

# ---------------------------------------------------------------------------
# State file — tracks last successful backup timestamp
# ---------------------------------------------------------------------------

write_success_state() {
    local snapshot="$1"
    local size="$2"
    local manifest_checksum="$3"
    cat > "$STATE_FILE" << STATE
{
  "lastSuccess": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "lastSnapshot": "$snapshot",
  "lastSize": "$size",
  "manifestChecksum": "$manifest_checksum"
}
STATE
}

read_last_success() {
    if [[ -f "$STATE_FILE" ]]; then
        jq -r '.lastSuccess // "never"' "$STATE_FILE" 2>/dev/null || echo "never"
    else
        echo "never"
    fi
}

# ---------------------------------------------------------------------------
# Legacy notification shim
# ---------------------------------------------------------------------------

send_telegram() {
    local msg="$1"
    echo "[synology-backup notify shim] $msg" >&2
    return 0
}
