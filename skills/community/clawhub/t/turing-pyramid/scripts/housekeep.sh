#!/bin/bash
# housekeep.sh — Runtime artifact cleanup for Turing Pyramid
# Safe to run any time. Idempotent.
#
# Cleans:
#   - audit.log: rotate when > MAX_AUDIT_LINES (keep tail)
#   - backups/: remove files older than MAX_BACKUP_AGE_DAYS
#   - pending_actions.json: compact old COMPLETED/FAILED/DEFERRED entries
#   - *.lock: stale lock files older than 1 hour
#   - *.tmp: orphaned temp files

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
ASSETS_DIR="$SKILL_DIR/assets"

# Configurable limits
MAX_AUDIT_LINES="${TP_MAX_AUDIT_LINES:-500}"
MAX_BACKUP_AGE_DAYS="${TP_MAX_BACKUP_AGE_DAYS:-7}"
MAX_PENDING_RESOLVED="${TP_MAX_PENDING_RESOLVED:-50}"  # keep N most recent resolved

cleaned=0
log() { echo "[housekeep] $*"; }

# ─── 1. audit.log rotation (extract → digest → trim) ─────────
AUDIT_LOG="$ASSETS_DIR/audit.log"
DIGEST_FILE="$ASSETS_DIR/decisions.log"
if [[ -f "$AUDIT_LOG" ]]; then
    lines=$(wc -l < "$AUDIT_LOG")
    if [[ "$lines" -gt "$MAX_AUDIT_LINES" ]]; then
        keep=$((MAX_AUDIT_LINES / 2))
        to_purge=$((lines - keep))
        
        # Extract significant entries before purging:
        # - Has a real reason (not "no reason given", not test)
        # - Has a conclusion
        # - High impact (>=2.0)
        head -n "$to_purge" "$AUDIT_LOG" | jq -c 'select(
            (.conclusion != null and .conclusion != "") or
            (.impact >= 2.0) or
            (.reason != null and .reason != "(no reason given)" and (.reason | test("test|ceiling|floor|manual"; "i") | not))
        )' >> "$DIGEST_FILE" 2>/dev/null
        
        # Now trim
        tmp=$(mktemp)
        tail -n "$keep" "$AUDIT_LOG" > "$tmp" && mv "$tmp" "$AUDIT_LOG"
        log "audit.log: rotated $lines → $keep lines (significant entries → decisions.log)"
        ((cleaned++))
    fi
fi

# ─── 2. backups/ pruning ──────────────────────────────────────
BACKUPS_DIR="$ASSETS_DIR/backups"
if [[ -d "$BACKUPS_DIR" ]]; then
    old_count=$(find "$BACKUPS_DIR" -maxdepth 1 -type f -mtime +"$MAX_BACKUP_AGE_DAYS" 2>/dev/null | wc -l)
    if [[ "$old_count" -gt 0 ]]; then
        find "$BACKUPS_DIR" -maxdepth 1 -type f -mtime +"$MAX_BACKUP_AGE_DAYS" -delete
        log "backups/: removed $old_count files older than ${MAX_BACKUP_AGE_DAYS}d"
        ((cleaned++))
    fi
fi

# ─── 3. pending_actions.json compaction ───────────────────────
PENDING_FILE="$ASSETS_DIR/pending_actions.json"
if [[ -f "$PENDING_FILE" ]]; then
    total_resolved=$(jq '[.actions[] | select(.status == "COMPLETED" or .status == "FAILED" or .status == "DEFERRED")] | length' "$PENDING_FILE" 2>/dev/null)
    if [[ -n "$total_resolved" && "$total_resolved" -gt "$MAX_PENDING_RESOLVED" ]]; then
        # Extract decisions from entries about to be purged → decisions.log
        jq -c '[
            .actions[]
            | select(.status != "PENDING")
            | select(.evidence != null or .resolution != null)
        ] | sort_by(.resolved_at // .proposed_at) | reverse | .['\'"$MAX_PENDING_RESOLVED"\'':][] |
        {type: "action", timestamp: (.resolved_at // .proposed_at),
         need, action: .action_name, status, evidence, resolution, defer_reason}' \
         "$PENDING_FILE" >> "$DIGEST_FILE" 2>/dev/null
        
        # Keep: all PENDING + N most recent resolved (by resolved_at)
        tmp=$(mktemp)
        jq --argjson keep "$MAX_PENDING_RESOLVED" '
          .actions = (
            [.actions[] | select(.status == "PENDING")] +
            ([.actions[] | select(.status != "PENDING")] | sort_by(.resolved_at // .proposed_at) | reverse | .[:$keep])
          ) |
          .pending_count = ([.actions[] | select(.status=="PENDING")] | length) |
          .completed_count = ([.actions[] | select(.status=="COMPLETED")] | length) |
          .deferred_count = ([.actions[] | select(.status=="DEFERRED")] | length)
        ' "$PENDING_FILE" > "$tmp" && mv "$tmp" "$PENDING_FILE"
        log "pending_actions: compacted (kept $MAX_PENDING_RESOLVED resolved, was $total_resolved; decisions → decisions.log)"
        ((cleaned++))
    fi
fi

# ─── 4. stale lock files ──────────────────────────────────────
stale_locks=$(find "$ASSETS_DIR" -maxdepth 1 -name "*.lock" -size 0 -mmin +60 2>/dev/null)
if [[ -n "$stale_locks" ]]; then
    echo "$stale_locks" | xargs rm -f
    log "locks: removed stale empty lock files"
    ((cleaned++))
fi

# ─── 5. orphaned .tmp files ───────────────────────────────────
old_tmps=$(find "$ASSETS_DIR" -maxdepth 1 -name "*.tmp.*" -mmin +30 2>/dev/null | wc -l)
if [[ "$old_tmps" -gt 0 ]]; then
    find "$ASSETS_DIR" -maxdepth 1 -name "*.tmp.*" -mmin +30 -delete
    log "tmp: removed $old_tmps orphaned temp files"
    ((cleaned++))
fi

if [[ "$cleaned" -eq 0 ]]; then
    echo "[housekeep] clean — nothing to do"
else
    echo "[housekeep] done ($cleaned tasks)"
fi
