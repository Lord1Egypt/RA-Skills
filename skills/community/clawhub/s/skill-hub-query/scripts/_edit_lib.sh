#!/usr/bin/env bash
# skill-hub-query: edit-capability library
# Implements GET-then-PATCH-then-verify three-stage flow for editing a skill's
# card metadata (display name, summary, tags, visibility, etc.) on a compatible Hub.
# Sourced by edit.sh; not executed directly.
# shellcheck disable=SC2155,SC2034
#
# NOTE: This file targets the optional /edit and /detail endpoints. Not every
# compatible Hub implements them. If your Hub does not implement them, set
# SKILL_HUB_DISABLE_EDIT=1 to make edit.sh refuse to run with an informative
# message instead of producing confusing 404/405 errors.

set -euo pipefail
umask 077

# Dependencies: _lib.sh must be sourced first (provides HUB_URL, HUB_API_PREFIX,
# HUB_LEGACY_API_PREFIX, CACHE_DIR, SKILL_DIR, load_token, etc.)

# Lazy endpoint resolution: compute templates on each call so SKILL_HUB_URL set
# after sourcing the lib is still honored, and so an unset URL produces a clear
# error at the first network call.
#
# Callers MUST run `require_hub_url || return $?` before calling these helpers,
# because `exit` inside a $(...) command substitution only kills the subshell.
EDIT_PREFIX="${SKILL_HUB_EDIT_PREFIX:-${HUB_LEGACY_API_PREFIX}}"
_edit_endpoint_tmpl() {
  echo "$(load_endpoint)${EDIT_PREFIX}/edit"
}
_detail_endpoint_tmpl() {
  echo "$(load_endpoint)${EDIT_PREFIX}/detail"
}

EDIT_BACKUP_DIR="${CACHE_DIR}/edit-backups"
mkdir -p "$EDIT_BACKUP_DIR"

# Keep last N backups per slug
EDIT_BACKUP_RETENTION="${SKILL_HUB_BACKUP_RETENTION:-20}"

# Editable card fields (must match your Hub's PUT /edit/<slug> contract)
EDIT_SCALAR_FIELDS=(displayName summary videoAttachmentUrl businessCategory visibility)
EDIT_ARRAY_FIELDS=(applicablePosition businessDomain business scene platform tags)
EDIT_NULLABLE_FIELDS=(videoAttachmentUrl summary displayName)

# ---------- Helpers ----------

# Build an auth header argument list for curl (or empty if no token)
_auth_curl_args() {
  local token=""
  if token="$(load_token 2>/dev/null)"; then
    local hdr scheme
    hdr="$(load_auth_header)"
    scheme="$(load_auth_scheme)"
    echo "-H"
    echo "${hdr}: ${scheme}${token}"
  fi
}

# Fetch a skill's authoritative snapshot via PUT /edit/<slug> with empty body
# (this convention returns the current 11+ fields; preferred over /detail because
# it's the same source-of-truth the PUT writes to)
fetch_skill_snapshot() {
  local slug="$1"
  local -a auth_args
  mapfile -t auth_args < <(_auth_curl_args)
  local resp
  resp=$(curl -sS --max-time 30 -X PUT "$(_edit_endpoint_tmpl)/${slug}" \
    -H "Content-Type: application/json" \
    "${auth_args[@]}" \
    -d '{}' 2>&1) || {
      echo "[error] Failed to fetch snapshot for ${slug}: network error" >&2
      return 1
    }

  local code
  code=$(echo "$resp" | jq -r '.code // 0' 2>/dev/null)
  if [[ "$code" != "200" ]]; then
    local msg
    msg=$(echo "$resp" | jq -r '.message // "unknown error"' 2>/dev/null)
    echo "[error] Failed to fetch snapshot for ${slug} (code=${code}): ${msg}" >&2
    echo "       If your Hub does not implement /edit, set SKILL_HUB_DISABLE_EDIT=1" >&2
    return 1
  fi

  echo "$resp" | jq '.data'
}

# Independent verification channel via GET /detail/<slug>
fetch_skill_via_detail() {
  local slug="$1"
  local -a auth_args
  mapfile -t auth_args < <(_auth_curl_args)
  local resp
  resp=$(curl -sS --max-time 30 "${auth_args[@]}" "$(_detail_endpoint_tmpl)/${slug}" 2>&1) || return 1

  local code
  code=$(echo "$resp" | jq -r '.code // 0' 2>/dev/null)
  if [[ "$code" != "200" ]]; then
    return 1
  fi

  echo "$resp" | jq '.data.skill // empty'
}

# Persist a snapshot backup, return file path
# Filename: <slug>_<YYYYMMDD_HHMMSS>_<random6>.json
backup_snapshot() {
  local slug="$1"
  local snapshot_json="$2"
  local ts rand
  ts=$(date +%Y%m%d_%H%M%S)
  rand=$(head -c 4 /dev/urandom 2>/dev/null | od -An -tx1 | tr -d ' \n' | head -c 6)
  [[ -z "$rand" ]] && rand="$$"
  local file="${EDIT_BACKUP_DIR}/${slug}_${ts}_${rand}.json"
  echo "$snapshot_json" > "$file"
  chmod 600 "$file"

  # retention: keep latest N backups per slug
  local backups
  # shellcheck disable=SC2012
  backups=$(ls -1t "${EDIT_BACKUP_DIR}/${slug}_"*.json 2>/dev/null || true)
  if [[ -n "$backups" ]]; then
    local to_delete
    to_delete=$(echo "$backups" | tail -n +"$((EDIT_BACKUP_RETENTION + 1))")
    if [[ -n "$to_delete" ]]; then
      echo "$to_delete" | xargs -r rm -f
    fi
  fi

  echo "$file"
}

# Resolve current user email for owner pre-check.
# Order (no internal-network specific path):
#   1. SKILL_HUB_OWNER_EMAIL env var (explicit override)
#   2. git config user.email
#   3. (skipped) fall back to platform 403
get_current_user_email() {
  if [[ -n "${SKILL_HUB_OWNER_EMAIL:-}" ]]; then
    echo "$SKILL_HUB_OWNER_EMAIL"
    return 0
  fi
  local email
  email="$(git config --global user.email 2>/dev/null || true)"
  if [[ -z "$email" ]]; then
    email="$(git config user.email 2>/dev/null || true)"
  fi
  if [[ -n "$email" ]]; then
    echo "$email"
    return 0
  fi
  return 1
}

# Pre-validate owner; on mismatch, refuse early. Server enforces 403 as a backstop.
verify_owner() {
  local snapshot_json="$1"
  local owner
  owner=$(echo "$snapshot_json" | jq -r '.ownerEmail // empty')
  local current_user
  current_user=$(get_current_user_email) || {
    echo "[warn] Cannot determine current user email (no SKILL_HUB_OWNER_EMAIL, no git config user.email)." >&2
    echo "       Skipping client-side owner check; the Hub server will enforce permissions." >&2
    return 0
  }

  if [[ "$owner" != "$current_user" ]]; then
    echo "[error] Owner pre-check failed:" >&2
    echo "        skill ownerEmail = $owner" >&2
    echo "        your identity    = $current_user" >&2
    echo "        Only the owner can edit a skill's card metadata." >&2
    echo "        (Override identity with: export SKILL_HUB_OWNER_EMAIL=\"<email>\")" >&2
    return 1
  fi
  return 0
}

# Print a diff table for changed fields
# Args: snapshot_json + patch_json
# Returns: 0 if there are diffs, 1 if all fields already match
print_diff() {
  local before="$1"
  local patch="$2"

  echo ""
  echo "========== Field-change diff =========="

  local has_diff=0
  local keys
  keys=$(echo "$patch" | jq -r 'keys[]')
  while IFS= read -r key; do
    local old new
    old=$(jq -r --arg k "$key" '
      if (.[$k] | type) == "array" then (.[$k] | @json)
      elif .[$k] == null then ""
      else (.[$k] | tostring) end' <<< "$before")
    new=$(jq -r --arg k "$key" '
      if (.[$k] | type) == "array" then (.[$k] | @json)
      elif .[$k] == null then ""
      else (.[$k] | tostring) end' <<< "$patch")

    if [[ "$old" != "$new" ]]; then
      has_diff=1
      echo ""
      echo "  ${key}:"
      echo "    old: ${old:-(empty)}"
      echo "    new: ${new:-(empty)}"
    fi
  done <<< "$keys"

  if [[ "$has_diff" -eq 0 ]]; then
    echo "  All requested field values already match current state. No PUT needed."
    return 1
  fi
  echo ""
  echo "======================================"
  return 0
}

# Execute the PUT
apply_patch() {
  local slug="$1"
  local patch_json="$2"
  local -a auth_args
  mapfile -t auth_args < <(_auth_curl_args)

  local resp
  resp=$(curl -sS --max-time 30 -X PUT "$(_edit_endpoint_tmpl)/${slug}" \
    -H "Content-Type: application/json" \
    "${auth_args[@]}" \
    -d "$patch_json" 2>&1) || {
      echo "[error] PUT call failed: network error" >&2
      return 1
    }

  local code msg
  code=$(echo "$resp" | jq -r '.code // 0' 2>/dev/null)
  msg=$(echo "$resp" | jq -r '.message // "unknown error"' 2>/dev/null)

  if [[ "$code" != "200" ]]; then
    echo "[error] PUT failed (code=${code}): ${msg}" >&2
    return 1
  fi

  echo "$resp" | jq '.data'
}

# Verify post-change with dual-channel reads + retry to absorb propagation delay
# Args: slug + patch_json
# Returns: 0 = all consistent, 1 = real mismatch, 2 = visibility silently downgraded
verify_post_change() {
  local slug="$1"
  local patch_json="$2"

  # Retry: 1s -> 2s -> 3s, stop early if all fields match
  local attempt=0
  local max_attempts=3
  local after_snapshot after_detail
  local -a sleep_intervals=(1 2 3)

  while [[ "$attempt" -lt "$max_attempts" ]]; do
    sleep "${sleep_intervals[$attempt]}"
    attempt=$((attempt + 1))

    if ! after_snapshot=$(fetch_skill_snapshot "$slug" 2>/dev/null); then
      echo "  [warn] attempt $attempt: failed to fetch PUT-channel snapshot" >&2
      continue
    fi

    if ! after_detail=$(fetch_skill_via_detail "$slug" 2>/dev/null); then
      after_detail="{}"
    fi

    # Quick check: are all fields already consistent? if yes, stop early
    local quick_ok=1
    local _keys
    _keys=$(echo "$patch_json" | jq -r 'keys[]')
    while IFS= read -r _k; do
      local _req _act
      _req=$(echo "$patch_json" | jq -c --arg k "$_k" '.[$k]')
      _act=$(echo "$after_snapshot" | jq -c --arg k "$_k" '.[$k] // null')
      if [[ "$_req" != "$_act" ]]; then
        quick_ok=0
        break
      fi
    done <<< "$_keys"

    if [[ "$quick_ok" -eq 1 ]]; then
      break
    fi

    if [[ "$attempt" -lt "$max_attempts" ]]; then
      echo "  attempt $attempt: some fields not yet consistent, retrying in ${sleep_intervals[$attempt]}s..." >&2
    fi
  done

  if [[ -z "${after_snapshot:-}" ]]; then
    echo "[warn] verify: snapshot unfetchable after $max_attempts attempts" >&2
    return 1
  fi

  local all_consistent=1
  local visibility_silently_downgraded=0

  echo ""
  echo "========== Post-write verification (dual-channel) =========="
  local keys
  keys=$(echo "$patch_json" | jq -r 'keys[]')
  while IFS= read -r key; do
    local requested actual_put actual_detail
    requested=$(echo "$patch_json" | jq -c --arg k "$key" '.[$k]')
    actual_put=$(echo "$after_snapshot" | jq -c --arg k "$key" '.[$k] // null')
    actual_detail=$(echo "$after_detail" | jq -c --arg k "$key" '.[$k] // null')

    if [[ "$requested" == "$actual_put" ]]; then
      echo "  OK  ${key}: PUT-channel matches"
    else
      all_consistent=0
      if [[ "$key" == "visibility" ]]; then
        visibility_silently_downgraded=1
        echo "  !!  ${key}: silently rewritten by platform"
        echo "      requested:        ${requested}"
        echo "      actual (PUT):     ${actual_put}"
        echo "      actual (detail):  ${actual_detail}"
        echo "      Reason: your Hub may enforce visibility policy for certain users/orgs."
      else
        echo "  XX  ${key}: mismatch"
        echo "      requested:        ${requested}"
        echo "      actual (PUT):     ${actual_put}"
        echo "      actual (detail):  ${actual_detail}"
      fi
    fi
  done <<< "$keys"
  echo "==========================================="
  echo ""

  if [[ "$all_consistent" -eq 1 ]]; then
    return 0
  fi

  # Edge case: visibility silently rewritten but every other field is fine
  if [[ "$visibility_silently_downgraded" -eq 1 ]]; then
    local non_vis_keys
    non_vis_keys=$(echo "$patch_json" | jq -r 'keys[] | select(. != "visibility")')
    local other_ok=1
    if [[ -n "$non_vis_keys" ]]; then
      while IFS= read -r key; do
        local req act
        req=$(echo "$patch_json" | jq -c --arg k "$key" '.[$k]')
        act=$(echo "$after_snapshot" | jq -c --arg k "$key" '.[$k] // null')
        [[ "$req" != "$act" ]] && other_ok=0
      done <<< "$non_vis_keys"
    fi
    if [[ "$other_ok" -eq 1 ]]; then
      echo "  info: other fields all took effect; visibility was silently rewritten. Partial success (edge case)."
      return 2
    fi
  fi

  return 1
}

# Roll back from a backup file (used on PUT failure or verification failure)
# Note: server typically does not accept null, so null-valued fields are restored
# as [] (arrays) or "" (strings) — semantic equivalent of "empty"
rollback_from_backup() {
  local slug="$1"
  local backup_file="$2"
  local -a auth_args
  mapfile -t auth_args < <(_auth_curl_args)

  echo ""
  echo "[info] Rolling back ${slug} from backup..."
  echo "       backup: $backup_file"

  if [[ ! -f "$backup_file" ]]; then
    echo "[error] Backup file does not exist; cannot roll back" >&2
    return 1
  fi

  local rollback_payload
  rollback_payload=$(jq '{
    displayName:           (.displayName           // ""),
    summary:               (.summary               // ""),
    videoAttachmentUrl:    (.videoAttachmentUrl    // ""),
    businessCategory:      (.businessCategory      // ""),
    visibility:            (.visibility            // ""),
    applicablePosition:    (.applicablePosition    // []),
    businessDomain:        (.businessDomain        // []),
    business:              (.business              // []),
    scene:                 (.scene                 // []),
    platform:              (.platform              // []),
    tags:                  (.tags                  // [])
  }' "$backup_file")

  local resp
  resp=$(curl -sS --max-time 30 -X PUT "$(_edit_endpoint_tmpl)/${slug}" \
    -H "Content-Type: application/json" \
    "${auth_args[@]}" \
    -d "$rollback_payload" 2>&1)

  local code
  code=$(echo "$resp" | jq -r '.code // 0' 2>/dev/null)
  if [[ "$code" == "200" ]]; then
    echo "[ok] Rollback succeeded (null fields restored as [] / \"\" since the Hub does not accept null)"
    return 0
  else
    echo "[error] Rollback failed (code=${code}); inspect manually at $(_edit_endpoint_tmpl)/${slug}" >&2
    echo "        Backup is preserved at: $backup_file" >&2
    return 1
  fi
}
