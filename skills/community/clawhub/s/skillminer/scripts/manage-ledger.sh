#!/usr/bin/env bash
# manage-ledger.sh — deterministic ledger transitions for skillminer
#
# v0.1.0 — schema 0.4
#
# Usage:
#   manage-ledger.sh accept    <id>
#   manage-ledger.sh reject    <id> "<reason>"
#   manage-ledger.sh defer     <id> "<reason>"
#   manage-ledger.sh promote   <id>                 # observations[] → candidates[] (pending)
#   manage-ledger.sh silence   <id> "<reason>"      # permanent veto (no 30-day expiry)
#   manage-ledger.sh unsilence <id>                 # lift a silence
#   manage-ledger.sh show      [<id>]               # dump ledger summary or one entry
#
# Env:
#   CLAWD_DIR     (optional, defaults to ~/clawd in wrapper scripts) — base workspace (memory + drafted skills output)
#
# Deps: bash, jq, git. Deterministic, no LLM, no network.
# Atomic via tmpfile + rename. Safe for single-human use (no locking for
# concurrent writers — skillminer does not have concurrent writers).
#
# Mutation effects:
#   accept      — candidate stays in candidates[] with status=accepted; morning-write picks it up
#   reject      — candidate moved to rejected[]; 30-day cooldown applies
#   defer       — candidate moved to deferred[]; 30-day cooldown applies
#   promote     — observation copied to candidates[] as status=pending; observation stays in
#                 observations[] until the next scan replaces the array. Idempotent.
#   silence     — target (candidates[]/observations[]/standalone) added to silenced[]; NO expiry.
#                 If the id is currently in candidates[] or observations[], it is also removed.
#   unsilence   — remove id from silenced[]. Does NOT resurrect the candidate/observation.

set -euo pipefail

source "$(dirname "${BASH_SOURCE[0]}")/lib/slug-validate.sh"
source "$(dirname "${BASH_SOURCE[0]}")/lib/atomic-write.sh"

# Only mutating commands need the lock; 'show' is read-only
case "${1:-}" in
  accept|reject|defer|promote|silence|unsilence)
    if ! acquire_skillminer_lock; then
      exit 3
    fi
    ;;
esac

die()   { printf 'error: %s\n' "$*" >&2; exit 1; }
usage() {
  cat >&2 <<'USAGE'
Usage:
  manage-ledger.sh accept    <id>
  manage-ledger.sh reject    <id> "<reason>"
  manage-ledger.sh defer     <id> "<reason>"
  manage-ledger.sh promote   <id>
  manage-ledger.sh silence   <id> "<reason>"
  manage-ledger.sh unsilence <id>
  manage-ledger.sh show      [<id>]
USAGE
  exit 2
}

command -v jq >/dev/null || die "jq is required"

iso_now()   { date -u +"%Y-%m-%dT%H:%M:%SZ"; }
today_utc() { date -u +"%Y-%m-%d"; }

# resolve paths ------------------------------------------------------------

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
FORGE_DIR="$SKILL_DIR"
CLAWD_DIR="${CLAWD_DIR:-$HOME/clawd}"
STATE="$FORGE_DIR/state/state.json"

[[ -f "$STATE" ]] || die "state.json not found at $STATE"
jq -e . "$STATE" >/dev/null 2>&1 || die "state.json is not valid JSON: $STATE"

# schema guard — accept 0.2 (legacy), 0.3, and 0.4
SCHEMA_VERSION=$(jq -r '.schema_version // ""' "$STATE")
case "$SCHEMA_VERSION" in
  0.5) ;;
  0.2|0.3|0.4) die "legacy schema_version '$SCHEMA_VERSION' — run 'scripts/migrate-state.sh' to upgrade" ;;
  *) die "unsupported schema_version '$SCHEMA_VERSION'" ;;
esac

# atomic-write helper ------------------------------------------------------

# write_state <jq-filter> [<--arg key val> ...]
# Reads $STATE, applies the jq filter (with any --arg pairs), writes back
# atomically. Aborts if jq fails or the result is not valid JSON.
write_state() {
  local filter="$1"; shift
  local tmp
  tmp=$(mktemp "${STATE}.XXXXXX")
  # shellcheck disable=SC2064
  trap "rm -f '$tmp'" EXIT
  if ! jq --indent 2 "$@" "$filter" "$STATE" > "$tmp"; then
    die "jq filter failed; state unchanged"
  fi
  jq -e . "$tmp" >/dev/null || die "post-write JSON invalid; state unchanged"
  mv "$tmp" "$STATE"
  trap - EXIT
}

# commands -----------------------------------------------------------------

cmd="${1:-}"; [[ -n "$cmd" ]] || usage; shift

case "$cmd" in

  accept)
    id="${1:-}"; [[ -n "$id" ]] || usage
    validate_slug "$id" "candidate id" || exit 4
    NOW=$(iso_now)

    if ! jq -e --arg id "$id" '
      .candidates[] | select(.id == $id and .status == "pending")
    ' "$STATE" >/dev/null; then
      die "no pending candidate with id '$id' (not found or wrong status)"
    fi

    write_state '
      .candidates |= map(
        if .id == $id and .status == "pending"
          then .status = "accepted" | .updatedAt = $now
          else .
        end
      )
      | .last_update = $now
    ' --arg id "$id" --arg now "$NOW"

    echo "ok: accepted '$id'"
    ;;

  reject)
    id="${1:-}"; reason="${2:-}"
    [[ -n "$id" && -n "$reason" ]] || usage
    validate_slug "$id" "candidate id" || exit 4
    NOW=$(iso_now); TODAY=$(today_utc)

    jq -e --arg id "$id" '.candidates[] | select(.id == $id)' "$STATE" >/dev/null \
      || die "no candidate with id '$id' in candidates[]"

    write_state '
      .candidates |= map(
        if .id == $id then
          .status = "rejected"
          | .written = false
          | .rejectedReason = $reason
          | .rejectedAt = $today
          | .updatedAt = $now
        else . end
      )
      | .last_update = $now
    ' --arg id "$id" --arg reason "$reason" --arg today "$TODAY" --arg now "$NOW"

    # Move _pending/<slug> to _rejected/<slug>-<timestamp>/ graveyard
    pending="$CLAWD_DIR/skills/_pending/$id"
    if [ -d "$pending" ]; then
      graveyard="$CLAWD_DIR/skills/_rejected"
      mkdir -p "$graveyard"
      mv "$pending" "$graveyard/$id-$(date -u +%Y%m%dT%H%M%SZ)"
    fi

    echo "rejected: $id"
    ;;

  defer)
    id="${1:-}"; reason="${2:-}"
    [[ -n "$id" && -n "$reason" ]] || usage
    validate_slug "$id" "candidate id" || exit 4
    NOW=$(iso_now); TODAY=$(today_utc)

    jq -e --arg id "$id" '.candidates[] | select(.id == $id)' "$STATE" >/dev/null \
      || die "no candidate with id '$id' in candidates[]"

    if jq -e --arg id "$id" '.deferred[] | select(.id == $id)' "$STATE" >/dev/null; then
      die "id '$id' already in deferred[] — refusing to double-defer"
    fi

    write_state '
      (.candidates[] | select(.id == $id)) as $c
      | .deferred += [{
          id: $c.id,
          deferredAt: $today,
          reason: $reason,
          intentSummary: ($c.intentSummary // ""),
          triggerPhrases: ($c.triggerPhrases // [])
        }]
      | .candidates |= map(select(.id != $id))
      | .last_update = $now
    ' --arg id "$id" --arg reason "$reason" --arg today "$TODAY" --arg now "$NOW"

    echo "ok: deferred '$id'"
    ;;

  promote)
    id="${1:-}"; [[ -n "$id" ]] || usage
    validate_slug "$id" "candidate id" || exit 4
    NOW=$(iso_now); TODAY=$(today_utc)

    # Require observations-capable schema for promote.
    [[ "$SCHEMA_VERSION" == "0.3" || "$SCHEMA_VERSION" == "0.4" || "$SCHEMA_VERSION" == "0.5" ]] || die "promote requires schema 0.3 or 0.4 (found $SCHEMA_VERSION)"

    jq -e --arg id "$id" '(.observations // [])[] | select(.id == $id)' "$STATE" >/dev/null \
      || die "no observation with id '$id' in observations[]"

    # Idempotent: if already in candidates[], refuse.
    if jq -e --arg id "$id" '.candidates[] | select(.id == $id)' "$STATE" >/dev/null; then
      die "id '$id' already in candidates[] — refusing to duplicate"
    fi

    # Cooldown + silence guard: don't let promote bypass a prior decision.
    if jq -e --arg id "$id" '.rejected[] | select(.id == $id)' "$STATE" >/dev/null; then
      die "id '$id' is in rejected[] — cooldown applies. Wait for expiry or hand-edit."
    fi
    if jq -e --arg id "$id" '.deferred[] | select(.id == $id)' "$STATE" >/dev/null 2>&1; then
      die "Pattern '$id' is in deferred[] — cooldown applies. Wait for expiry or use reject to permanently block."
    fi
    if jq -e --arg id "$id" '(.silenced // [])[] | select(.id == $id)' "$STATE" >/dev/null; then
      die "id '$id' is silenced — run 'unsilence' first if you want to revisit"
    fi

    write_state '
      ((.observations // [])[] | select(.id == $id)) as $o
      | .candidates += [{
          id:              $o.id,
          type:            "skill_candidate",
          intentSummary:   ($o.intentSummary // ""),
          firstSeen:       ($o.firstSeen // $o.lastSeen // $today),
          lastSeen:        ($o.lastSeen // $today),
          daysSeen:        ($o.daysSeen // []),
          occurrences:     ($o.occurrences // 0),
          confidence:      "low",
          status:          "pending",
          written:         false,
          triggerPhrases:  ($o.triggerPhrases // []),
          proposedSteps:   ($o.proposedSteps // []),
          coverageRisk:    ($o.coverageRisk // false),
          coverageOverlaps:($o.coverageOverlaps // []),
          sourceCitations: ($o.sourceCitations // []),
          rejectedReason:  null,
          rejectedAt:      null,
          deferredReason:  null,
          deferredAt:      null,
          resurfacedFrom:  "observation",
          resurfacedFromDate: $today,
          promotedFromObservation: true,
          createdAt:       $now,
          updatedAt:       $now
        }]
      | .last_update = $now
    ' --arg id "$id" --arg today "$TODAY" --arg now "$NOW"

    echo "ok: promoted '$id' from observations[] to candidates[] (status=pending, confidence=low)"
    echo "note: proposedSteps may be empty — run accept only after hand-editing steps if needed,"
    echo "      or wait for the next scan to see if it crosses the ≥3 occ / ≥2 days threshold."
    ;;

  silence)
    id="${1:-}"; reason="${2:-}"
    [[ -n "$id" && -n "$reason" ]] || usage
    validate_slug "$id" "candidate id" || exit 4
    NOW=$(iso_now); TODAY=$(today_utc)

    [[ "$SCHEMA_VERSION" == "0.3" || "$SCHEMA_VERSION" == "0.4" || "$SCHEMA_VERSION" == "0.5" ]] || die "silence requires schema 0.3 or 0.4 (found $SCHEMA_VERSION)"

    # Require target to exist somewhere in the ledger. Silencing an unknown id
    # would produce a silenced[] entry with empty intentSummary/triggerPhrases,
    # violating the semantic-match contract those fields enforce.
    if ! jq -e --arg id "$id" '
      [ (.candidates[]? | select(.id == $id))
      , ((.observations // [])[]? | select(.id == $id))
      , (.rejected[]? | select(.id == $id))
      , (.deferred[]? | select(.id == $id))
      ] | length > 0
    ' "$STATE" >/dev/null; then
      echo "error: silence target '$id' not found in candidates/observations/rejected/deferred — use 'show' to list" >&2
      exit 2
    fi

    if jq -e --arg id "$id" '(.silenced // [])[] | select(.id == $id)' "$STATE" >/dev/null; then
      die "id '$id' already silenced — use unsilence first if you want to change reason"
    fi

    # Pull intentSummary + triggerPhrases from wherever the id lives.
    # Search order: candidates[], observations[], rejected[], deferred[].
    write_state '
      ( [ .candidates[]? | select(.id == $id) ]
      + [ (.observations // [])[]? | select(.id == $id) ]
      + [ .rejected[]? | select(.id == $id) ]
      + [ .deferred[]? | select(.id == $id) ]
      | first // {id: $id, intentSummary: "", triggerPhrases: []}
      ) as $src
      | .silenced = ((.silenced // []) + [{
          id: $src.id,
          silencedAt: $today,
          reason: $reason,
          intentSummary: ($src.intentSummary // ""),
          triggerPhrases: ($src.triggerPhrases // [])
        }])
      | .candidates   |= map(select(.id != $id))
      | .observations = ((.observations // []) | map(select(.id != $id)))
      | .last_update  = $now
    ' --arg id "$id" --arg reason "$reason" --arg today "$TODAY" --arg now "$NOW"

    echo "ok: silenced '$id' (permanent — no 30-day expiry)"
    ;;

  unsilence)
    id="${1:-}"; [[ -n "$id" ]] || usage
    validate_slug "$id" "candidate id" || exit 4
    NOW=$(iso_now)

    [[ "$SCHEMA_VERSION" == "0.3" || "$SCHEMA_VERSION" == "0.4" || "$SCHEMA_VERSION" == "0.5" ]] || die "unsilence requires schema 0.3 or 0.4 (found $SCHEMA_VERSION)"

    jq -e --arg id "$id" '(.silenced // [])[] | select(.id == $id)' "$STATE" >/dev/null \
      || die "id '$id' not in silenced[]"

    write_state '
      .silenced   = ((.silenced // []) | map(select(.id != $id)))
      | .last_update = $now
    ' --arg id "$id" --arg now "$NOW"

    echo "ok: unsilenced '$id'"
    echo "note: this does NOT resurrect the candidate/observation. Wait for the next scan"
    echo "      or hand-edit if you want to re-add it to candidates[]."
    ;;

  show)
    id="${1:-}"
    if [[ -z "$id" ]]; then
      jq '{
        schema_version,
        last_scan, last_write, last_update,
        counts: {
          candidates:   (.candidates | length),
          observations: ((.observations // []) | length),
          rejected:     (.rejected | length),
          deferred:     (.deferred | length),
          silenced:     ((.silenced // []) | length)
        },
        candidates:   [.candidates[] | {id, status, confidence, occurrences, lastSeen}],
        observations: [(.observations // [])[] | {id, occurrences, daysSeen, reason}],
        silenced:     [(.silenced // [])[]     | {id, silencedAt, reason}]
      }' "$STATE"
    else
      validate_slug "$id" "candidate id" || exit 4
      jq --arg id "$id" '{
        candidate:   ([.candidates[]?           | select(.id == $id)] | first),
        observation: ([(.observations // [])[]? | select(.id == $id)] | first),
        rejected:    ([.rejected[]?             | select(.id == $id)] | first),
        deferred:    ([.deferred[]?             | select(.id == $id)] | first),
        silenced:    ([(.silenced // [])[]?     | select(.id == $id)] | first)
      }' "$STATE"
    fi
    ;;

  *)
    usage
    ;;
esac
