#!/bin/bash
# Wrapper for a11y-audit.sh with RAM guardrails
# Sets memory limits for low-RAM environments (e.g., <2GB)

set -e

# Get available memory in MB from /proc/meminfo (MemAvailable)
# Get available memory in MB from /proc/meminfo (MemAvailable), free -m, or cgroup limits
if [ -r /proc/meminfo ]; then
    # MemAvailable in kB
    AVAILABLE_MEM=$(awk '/^MemAvailable:/ {print int($2/1024)}' /proc/meminfo)
else
    # Fallback to free -m (6th column is available memory in MB)
    AVAILABLE_MEM=$(free -m | awk '/^Mem: / {print $6}')
fi
# Prefer container/cgroup memory limit over host /proc/meminfo (v1 then v2)
# Note: We check v1 first. If v1 yields a valid limit (not unlimited and not too large), we use it.
# If v1 is readable but yields an invalid limit (unlimited or too large), we ignore it and check v2.
# If v1 is not readable, we check v2.
# We only use v2 if we haven't already gotten a valid limit from v1.
if [ -r /sys/fs/cgroup/memory/memory.limit_in_bytes ]; then
    CG_LIMIT_BYTES=$(cat /sys/fs/cgroup/memory/memory.limit_in_bytes 2>/dev/null)
    if [ -n "$CG_LIMIT_BYTES" ]; then
        # Check for unlimited sentinel (9223372036854775807) or unreasonably large values (>100 TB)
        if [ "$CG_LIMIT_BYTES" -ne 9223372036854775807 ] && [ "$CG_LIMIT_BYTES" -le 109951162777600 ]; then
            CG_LIMIT_MB=$(echo "$CG_LIMIT_BYTES" | awk '{print int($1/(1024*1024))}')
            if [ -n "$CG_LIMIT_MB" ] && [ "$CG_LIMIT_MB" -gt 0 ]; then
                AVAILABLE_MEM=$CG_LIMIT_MB
            fi
        fi
    fi
fi
# If we still don't have a valid memory amount from v1 (or v1 was not readable), try v2.
if [ -z "${CG_LIMIT_MB:-}" ] || [ "${CG_LIMIT_MB:-0}" -le 0 ]; then
    if [ -r /sys/fs/cgroup/memory.max ]; then
        CG_LIMIT_BYTES=$(cat /sys/fs/cgroup/memory.max 2>/dev/null)
        if [ -n "$CG_LIMIT_BYTES" ]; then
            CG_LIMIT_MB=$(echo "$CG_LIMIT_BYTES" | awk '{if ($1+0 > 0) print int($1/(1024*1024)); else print 0}')
            if [ -n "$CG_LIMIT_MB" ] && [ "$CG_LIMIT_MB" -gt 0 ]; then
                AVAILABLE_MEM=$CG_LIMIT_MB
            fi
        fi
    fi
fi
# If we still don't have a valid memory amount, error out
if [ -z "$AVAILABLE_MEM" ] || [ "$AVAILABLE_MEM" -le 0 ]; then
    echo "ERROR: Could not determine available memory"
    exit 1
fi
# Configurable limits via environment variables (with sensible defaults)
# ULIMIT_PERCENT: percentage of available memory to use for ulimit -v (virtual memory ceiling)
# ULIMIT_MIN_MB: minimum virtual memory limit in MB
# NODE_PERCENT: percentage of available memory for Node's old space (--max-old-space-size)
# NODE_MIN_MB: minimum Node old space in MB
ULIMIT_PERCENT=${ULIMIT_PERCENT:-90}
ULIMIT_MIN_MB=${ULIMIT_MIN_MB:-1536}
NODE_PERCENT=${NODE_PERCENT:-30}
NODE_MIN_MB=${NODE_MIN_MB:-256}

# Compute ulimit virtual memory limit (in MB)
LIMIT_MEM=$(( AVAILABLE_MEM * ULIMIT_PERCENT / 100 ))
# Cap to available budget; minimum applies only when budget supports it
if [ "$LIMIT_MEM" -gt "$AVAILABLE_MEM" ]; then
    LIMIT_MEM=$AVAILABLE_MEM
fi
if [ "$LIMIT_MEM" -lt "$ULIMIT_MIN_MB" ] && [ "$AVAILABLE_MEM" -ge "$ULIMIT_MIN_MB" ]; then
    LIMIT_MEM=$ULIMIT_MIN_MB
fi
# Convert to bytes for ulimit (ulimit takes KB)
LIMIT_KB=$(( LIMIT_MEM * 1024 ))

# Set memory limits for the process (affects children)
ulimit -v "$LIMIT_KB" || { echo "ERROR: Failed to set virtual memory limit to ${LIMIT_KB} KB" >&2; exit 1; }

# Node memory limit (in MB)
NODE_MEM_MB=$(( AVAILABLE_MEM * NODE_PERCENT / 100 ))
# Cap to available budget; minimum applies only when budget supports it
if [ "$NODE_MEM_MB" -gt "$AVAILABLE_MEM" ]; then
    NODE_MEM_MB=$AVAILABLE_MEM
fi
if [ "$NODE_MEM_MB" -lt "$NODE_MIN_MB" ] && [ "$AVAILABLE_MEM" -ge "$NODE_MIN_MB" ]; then
    NODE_MEM_MB=$NODE_MIN_MB
fi
NODE_OPTIONS="${NODE_OPTIONS} --max-old-space-size=${NODE_MEM_MB}"
export NODE_OPTIONS

# Run the audit script with the guardrails
export PATH="$(dirname "$0"):$PATH"
cd "$(dirname "$0")/.."
bash scripts/a11y-audit.sh "$@"
