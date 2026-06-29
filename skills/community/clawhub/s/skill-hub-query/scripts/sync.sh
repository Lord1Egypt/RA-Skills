#!/usr/bin/env bash
# skill-hub-query: cache sync (full / incremental)
# Usage:
#   bash sync.sh           # auto (first run -> full, otherwise incremental)
#   bash sync.sh --full    # force full refresh (also prunes removed slugs)
#   bash sync.sh --incr    # force incremental (cache must already exist)
#
# Incremental only unions new data — it does not prune deleted skills.
# Use --full to clean up removed/withdrawn slugs.
set -euo pipefail
SELF_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# shellcheck source=./_lib.sh
source "${SELF_DIR}/_lib.sh"

setup_legacy_notice

# ---------- skillhub.cn provider branch ----------
# skillhub.cn is queried LIVE (no local cache). Its catalog is huge (~71k
# skills) with no bulk-export endpoint, so a "sync everything" model is not
# meaningful. This is informational, not an error -- exit 0.
# Generic-contract behavior is unaffected when SKILL_HUB_PROVIDER is unset.
if is_skillhub_cn; then
  cat >&2 <<EOF
[info] skillhub.cn is queried live; no local cache needed (no-op sync).

To search and install on skillhub.cn use:

  SKILL_HUB_PROVIDER=skillhub_cn bash $SELF_DIR/query.sh keyword <kw>
  SKILL_HUB_PROVIDER=skillhub_cn bash $SELF_DIR/query.sh today
  SKILL_HUB_PROVIDER=skillhub_cn bash $SELF_DIR/query.sh slug <exact-slug>
  SKILL_HUB_PROVIDER=skillhub_cn bash $SELF_DIR/install.sh <exact-slug>
EOF
  exit 0
fi

# Track temp files so EXIT trap can clean them up on any failure path.
# Note: setup_legacy_notice already registered an EXIT trap for the legacy notice
# marker; we replace it with a composed trap that also handles our temp files.
_SYNC_TMP_FILES=()
_sync_cleanup() {
  local f
  for f in "${_SYNC_TMP_FILES[@]:-}"; do
    [[ -n "$f" ]] && rm -f "$f" "${f}.tmp" 2>/dev/null
  done
  rm -f "${_LEGACY_NOTICE_MARKER:-}" 2>/dev/null
}
trap _sync_cleanup EXIT

MODE="${1:-auto}"
PAGE_SIZE=100

# Atomic write helper: write stdin to <target>.tmp, then mv
atomic_write() {
  local target="$1"
  local tmp="${target}.tmp"
  cat > "$tmp"
  mv "$tmp" "$target"
}

# ---------- Full sync ----------
full_sync() {
  echo "[sync] Full sync starting (typically 5-15s)..." >&2

  local tmp_all
  tmp_all="$(mktemp)"
  _SYNC_TMP_FILES+=("$tmp_all")
  echo '{}' > "$tmp_all"

  local first total pages
  first="$(api_get "${HUB_API_PREFIX}/search?page=1&size=${PAGE_SIZE}&orderBy=updatedAt&order=desc")"
  if [[ -z "$first" ]] || ! echo "$first" | jq empty 2>/dev/null; then
    echo "[error] First-page response is empty or non-JSON. Aborting sync." >&2
    echo "        Run 'bash $SELF_DIR/doctor.sh' to verify Hub URL / token / connectivity." >&2
    rm -f "$tmp_all"
    exit 3
  fi
  total="$(echo "$first" | jq -r '.data.total // 0')"
  pages=$(( (total + PAGE_SIZE - 1) / PAGE_SIZE ))

  echo "[sync] Hub has $total skill(s) total ($pages page(s))" >&2

  echo "$first" | jq '[.data.records[] | {(.slug): .}] | add // {}' > "$tmp_all"

  local p resp
  for ((p=2; p<=pages; p++)); do
    echo "[sync]   page $p / $pages..." >&2
    resp="$(api_get "${HUB_API_PREFIX}/search?page=${p}&size=${PAGE_SIZE}&orderBy=updatedAt&order=desc")"
    jq -s '.[0] * (.[1].data.records | map({(.slug): .}) | add // {})' \
      "$tmp_all" <(echo "$resp") > "${tmp_all}.tmp"
    mv "${tmp_all}.tmp" "$tmp_all"
    # 100ms inter-page delay (rate-limit-friendly)
    sleep 0.1
  done

  # Diff against previous cache to report removed slugs
  if [[ -f "$CACHE_FILE" ]]; then
    local removed
    removed="$(jq -s '(.[0] | keys) - (.[1] | keys) | length' \
      "$CACHE_FILE" "$tmp_all" 2>/dev/null || echo "0")"
    if [[ -n "$removed" && "$removed" != "0" ]]; then
      echo "[sync] Pruned $removed removed/withdrawn skill(s)" >&2
    fi
  fi

  mv "$tmp_all" "$CACHE_FILE"

  # lastFullSync: local wall-clock for human display
  # lastIncrementalSync: server-side max updatedAt (NOT wall-clock) — avoids
  # client/server clock skew dropping data on the next incremental sync
  local now max_updated
  now="$(date +%s%3N)"
  max_updated="$(jq '[.[].updatedAt // 0] | max // 0' "$CACHE_FILE" 2>/dev/null || echo "0")"
  jq -n --argjson now "$now" --argjson cursor "$max_updated" --argjson total "$total" \
    '{lastFullSync: $now, lastIncrementalSync: $cursor, totalCount: $total, version: 1}' \
    > "$CACHE_META"

  echo "[sync] Full sync complete; $total skill(s) in cache" >&2
}

# ---------- Incremental sync ----------
incr_sync() {
  local last_sync
  last_sync="$(jq -r '.lastIncrementalSync // 0' "$CACHE_META" 2>/dev/null || echo "0")"
  if [[ "$last_sync" == "0" ]]; then
    echo "[sync] No last-sync cursor; switching to full sync" >&2
    full_sync
    return
  fi

  local last_dt
  last_dt="$(date -d "@$((last_sync/1000))" '+%H:%M:%S' 2>/dev/null || echo "$last_sync")"
  echo "[sync] Incremental sync (cursor: ${last_dt})..." >&2

  local resp new_records new_count
  resp="$(api_get "${HUB_API_PREFIX}/search?page=1&size=${PAGE_SIZE}&orderBy=updatedAt&order=desc")"

  new_records="$(echo "$resp" | jq --argjson ls "$last_sync" \
    '[.data.records[] | select(.updatedAt > $ls)]')"
  new_count="$(echo "$new_records" | jq 'length')"

  # If page 1 was entirely new data, escalate to full to avoid missing pages 2+
  # (jq select cannot exceed PAGE_SIZE; equality check is the precise condition)
  if [[ "$new_count" -eq "$PAGE_SIZE" ]]; then
    echo "[sync]   page 1 is entirely new (=${PAGE_SIZE}); upgrading to full sync" >&2
    full_sync
    return
  fi

  if [[ "$new_count" == "0" ]]; then
    echo "[sync]   no changes" >&2
    # No new data -> don't advance cursor (don't use wall-clock here either)
    return
  fi

  local merged
  merged="$(echo "$new_records" | jq 'map({(.slug): .}) | add // {}')"
  jq -s '.[0] * .[1]' "$CACHE_FILE" <(echo "$merged") | atomic_write "$CACHE_FILE"

  # Advance cursor: take max(server max updatedAt in this batch, old cursor)
  local batch_max new_cursor
  batch_max="$(echo "$new_records" | jq '[.[].updatedAt // 0] | max // 0')"
  new_cursor=$(( batch_max > last_sync ? batch_max : last_sync ))
  jq --argjson cursor "$new_cursor" '.lastIncrementalSync = $cursor' "$CACHE_META" \
    | atomic_write "$CACHE_META"

  echo "[sync]   $new_count new/updated record(s)" >&2
  echo "[sync]   note: incremental does NOT prune removed skills; run --full to clean" >&2
}

# ---------- Main ----------
case "$MODE" in
  --full)
    full_sync
    ;;
  --incr)
    if [[ ! -f "$CACHE_FILE" ]]; then
      echo "[error] Cache not found; drop --incr or run: bash sync.sh --full" >&2
      exit 1
    fi
    incr_sync
    ;;
  auto)
    if [[ ! -f "$CACHE_FILE" || ! -f "$CACHE_META" ]]; then
      full_sync
    else
      if ! jq empty "$CACHE_FILE" 2>/dev/null; then
        echo "[sync]   cache file corrupted; rebuilding via full sync" >&2
        full_sync
      else
        incr_sync
      fi
    fi
    ;;
  *)
    echo "[error] Unknown argument: $MODE" >&2
    echo "        Usage: bash sync.sh [--full | --incr]  (no arg = auto)" >&2
    exit 1
    ;;
esac
