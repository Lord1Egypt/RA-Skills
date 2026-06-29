#!/usr/bin/env bash
# skill-hub-query: edit a skill's card metadata on a compatible Hub
# Implements GET-then-diff-then-backup-then-PUT-then-verify (5-stage safety flow).
#
# Usage:
#   edit.sh <slug> --show                          # show current values, do not change
#   edit.sh <slug> --summary "new text"            # change one field
#   edit.sh <slug> --summary "..." --dry-run        # run diff + backup, do not PUT
#   edit.sh <slug> --summary "..." --tags "a,b,c"   # multiple fields
#   edit.sh <slug> --visibility public --yes        # user-authorized skip of interactive confirm
#
# Editable fields:
#   --display-name TEXT      display name
#   --summary TEXT           summary text
#   --video-url URL          video attachment URL (pass empty string to clear)
#   --category TEXT          business category
#   --visibility public|private  visibility (HIGH-RISK: triggers extra confirmation)
#   --position a,b,c         applicable position(s) (comma-separated; full overwrite)
#   --business-domain a,b
#   --business a,b
#   --scene a,b
#   --platform a,b
#   --tags a,b,c
#
# Safety guarantees:
#   1. Always GET the authoritative current value first
#   2. Owner pre-check (server-side 403 is the ultimate safety net)
#   3. Show diff before any write; stdin blocks for y/N unless --yes (user-authorized)
#   4. visibility changes trigger extra prompt (some Hubs silently downgrade on policy)
#   5. After PUT, verify via dual-channel cross-read with retry; auto-rollback on mismatch
#   6. Edge case: when only visibility is silently rewritten and all other fields took
#      effect, treat as partial success (don't roll back the legitimate changes)
#
# Hub compatibility:
#   This script requires your Hub to implement:
#     PUT  <endpoint>/edit/<slug>     (body = JSON patch; empty body returns current state)
#     GET  <endpoint>/detail/<slug>   (used as the cross-check channel)
#
#   If your Hub does NOT implement these, set:  export SKILL_HUB_DISABLE_EDIT=1
#   to disable edit.sh with an informative refusal instead of confusing errors.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=_lib.sh
source "${SCRIPT_DIR}/_lib.sh"

# Built-in provider override: skillhub.cn has no public edit API.
if is_skillhub_cn; then
  cat >&2 <<EOF
[error] Editing card metadata is not supported on skillhub.cn.

Why: card metadata on skillhub.cn is a one-way mirror synced from the upstream
source (e.g. clawhub or GitHub). The public API only exposes write operations
for publish / unlist / relist / delete / claim -- none of which edit card
fields such as summary, tags, visibility, etc. To change card information,
update the upstream source and re-publish.

Supported skillhub.cn operations:
  bash $SCRIPT_DIR/query.sh keyword <kw>
  bash $SCRIPT_DIR/query.sh today
  bash $SCRIPT_DIR/query.sh slug <exact-slug>
  bash $SCRIPT_DIR/query.sh versions <exact-slug>
  bash $SCRIPT_DIR/install.sh <exact-slug>
EOF
  exit 1
fi

# Optional kill-switch for Hubs without /edit
if [[ "${SKILL_HUB_DISABLE_EDIT:-0}" == "1" ]]; then
  cat >&2 <<EOF
[disabled] edit.sh is disabled because SKILL_HUB_DISABLE_EDIT=1.

edit.sh requires the optional Hub endpoints:
  PUT  <endpoint>/edit/<slug>      (body = JSON patch; empty body returns current state)
  GET  <endpoint>/detail/<slug>    (cross-check channel)

If your Hub does not implement these (clawhub.ai default does not), keep this disabled.
If your Hub does implement them, unset SKILL_HUB_DISABLE_EDIT and (optionally)
configure SKILL_HUB_EDIT_PREFIX to mount edit/detail under a different path.
EOF
  exit 1
fi

# shellcheck source=_edit_lib.sh
source "${SCRIPT_DIR}/_edit_lib.sh"

# ---------- Argument parsing ----------
SLUG=""
SHOW_ONLY=0
DRY_RUN=0
YES=0

declare -A PATCH_SCALAR
declare -A PATCH_ARRAY

usage() {
  cat <<'EOF'
skill-hub-query/scripts/edit.sh -- edit a Hub skill's card metadata.

Usage:
  edit.sh <slug> --show                          # show current state
  edit.sh <slug> --summary "new text"            # change one field (interactive confirm)
  edit.sh <slug> --summary "..." --dry-run        # run diff + backup, no PUT
  edit.sh <slug> --summary "..." --tags "a,b,c"   # multiple fields
  edit.sh <slug> --visibility public --yes        # user-authorized; skip prompt (agent must NOT add --yes on its own)

Editable fields:
  --display-name TEXT             display name
  --summary TEXT                  summary text
  --video-url URL                 video attachment URL (pass empty string to clear)
  --category TEXT                 business category
  --visibility public|private     visibility (HIGH-RISK: extra confirmation)
  --position a,b,c                applicable position(s) (comma-separated; full overwrite)
  --business-domain a,b
  --business a,b
  --scene a,b
  --platform a,b
  --tags a,b,c

Control flags:
  --show          show current values, do not modify
  --dry-run       run GET / diff / backup, do not PUT
  --yes           user-authorized; skip interactive confirm (agent must NOT add on its own)
  -h, --help

Exit codes:
  0   success (including the visibility partial-success edge case)
  1   failure (bad args / 404 / 403 / verification failed and rolled back)

Hub compatibility:
  Requires your Hub to implement PUT /edit/<slug> and GET /detail/<slug>.
  If unsupported, set: export SKILL_HUB_DISABLE_EDIT=1
EOF
  exit "${1:-0}"
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --show)            SHOW_ONLY=1; shift;;
    --dry-run)         DRY_RUN=1; shift;;
    --yes)             YES=1; shift;;
    -h|--help)         usage 0;;

    --display-name)    PATCH_SCALAR[displayName]="$2"; shift 2;;
    --summary)         PATCH_SCALAR[summary]="$2"; shift 2;;
    --video-url)       PATCH_SCALAR[videoAttachmentUrl]="$2"; shift 2;;
    --category)        PATCH_SCALAR[businessCategory]="$2"; shift 2;;
    --visibility)
      case "$2" in
        public|private) PATCH_SCALAR[visibility]="$2";;
        *) echo "[error] --visibility must be 'public' or 'private' (got: $2)" >&2; exit 1;;
      esac
      shift 2;;

    --position)         PATCH_ARRAY[applicablePosition]="$2"; shift 2;;
    --business-domain)  PATCH_ARRAY[businessDomain]="$2"; shift 2;;
    --business)         PATCH_ARRAY[business]="$2"; shift 2;;
    --scene)            PATCH_ARRAY[scene]="$2"; shift 2;;
    --platform)         PATCH_ARRAY[platform]="$2"; shift 2;;
    --tags)             PATCH_ARRAY[tags]="$2"; shift 2;;

    --*) echo "[error] Unknown flag: $1 (use --help)" >&2; exit 1;;
    *)
      if [[ -z "$SLUG" ]]; then SLUG="$1"
      else echo "[error] Too many positional args: $1" >&2; exit 1
      fi
      shift;;
  esac
done

if [[ -z "$SLUG" ]]; then
  echo "[error] Missing <slug>" >&2
  usage 1
fi

# Fail-fast if Hub URL is not configured (before any user-facing step output).
require_hub_url || exit $?

# ---------- Step 1: GET current snapshot ----------
echo ""
echo "[edit] target slug: $SLUG"
echo "[edit] Hub URL    : $(load_endpoint)"
echo ""
echo "[1/5] fetching current state (GET)..."
SNAPSHOT=$(fetch_skill_snapshot "$SLUG") || exit 1

OWNER=$(echo "$SNAPSHOT" | jq -r '.ownerEmail // empty')
echo "      ok; current owner: $OWNER"

# --show mode
if [[ "$SHOW_ONLY" -eq 1 ]]; then
  echo ""
  echo "========== Current skill card =========="
  echo "$SNAPSHOT" | jq '{
    slug, displayName, summary, ownerEmail, visibility, businessCategory,
    grade, source, builtIn, isRecommended,
    applicablePosition, businessDomain, business, scene, platform, tags,
    videoAttachmentUrl
  }'
  echo "========================================"
  exit 0
fi

if [[ ${#PATCH_SCALAR[@]} -eq 0 && ${#PATCH_ARRAY[@]} -eq 0 ]]; then
  echo ""
  echo "[error] No fields specified to change (use --help for the list, or --show to read-only inspect)" >&2
  exit 1
fi

# ---------- Step 2: owner pre-check ----------
echo ""
echo "[2/5] owner pre-check..."
verify_owner "$SNAPSHOT" || exit 1
echo "      ok"

# ---------- Step 3: build patch + show diff ----------
echo ""
echo "[3/5] building patch and computing diff..."

PATCH_JSON='{}'
for key in "${!PATCH_SCALAR[@]}"; do
  val="${PATCH_SCALAR[$key]}"
  PATCH_JSON=$(echo "$PATCH_JSON" | jq --arg k "$key" --arg v "$val" '. + {($k): $v}')
done

for key in "${!PATCH_ARRAY[@]}"; do
  csv="${PATCH_ARRAY[$key]}"
  if [[ -z "$csv" ]]; then
    PATCH_JSON=$(echo "$PATCH_JSON" | jq --arg k "$key" '. + {($k): []}')
  else
    arr=$(echo "$csv" | jq -R 'split(",") | map(gsub("^\\s+|\\s+$"; ""))')
    PATCH_JSON=$(echo "$PATCH_JSON" | jq --arg k "$key" --argjson v "$arr" '. + {($k): $v}')
  fi
done

if ! print_diff "$SNAPSHOT" "$PATCH_JSON"; then
  echo "[ok] All requested values already match current state; nothing to do."
  exit 0
fi

# ---------- Step 4: backup + user confirm ----------
echo ""
echo "[4/5] writing backup and confirming..."
BACKUP_FILE=$(backup_snapshot "$SLUG" "$SNAPSHOT")
echo "      backup: $BACKUP_FILE"

if [[ "$DRY_RUN" -eq 1 ]]; then
  echo ""
  echo "[dry-run] diff and backup written; no PUT sent."
  exit 0
fi

# Extra confirmation for visibility changes
if [[ -n "${PATCH_SCALAR[visibility]:-}" ]]; then
  cur_vis=$(echo "$SNAPSHOT" | jq -r '.visibility // "null"')
  new_vis="${PATCH_SCALAR[visibility]}"
  if [[ "$cur_vis" != "$new_vis" ]]; then
    echo ""
    echo "[high-risk] visibility change requested"
    echo "            $cur_vis  ->  $new_vis"
    if [[ "$new_vis" == "public" ]]; then
      echo "            note: some Hubs enforce visibility policy and may silently rewrite to private."
      echo "                  This script will honestly report the actual stored value during verification."
    fi
  fi
fi

if [[ "$YES" -ne 1 ]]; then
  echo ""
  read -r -p "Submit this patch? [y/N] " ans
  if [[ "${ans,,}" != "y" && "${ans,,}" != "yes" ]]; then
    echo "[cancel] no PUT sent."
    exit 0
  fi
fi

# ---------- Step 5: PUT + dual-channel verify + rollback ----------
echo ""
echo "[5/5] applying patch and verifying..."
if ! apply_patch "$SLUG" "$PATCH_JSON" >/dev/null; then
  echo "[error] PUT failed; no server-side change occurred, no rollback needed" >&2
  exit 1
fi
echo "      PUT ok (HTTP layer)"

set +e
verify_post_change "$SLUG" "$PATCH_JSON"
verify_rc=$?
set -e

case "$verify_rc" in
  0)
    echo ""
    echo "[ok] all fields verified consistent with the request"
    exit 0;;
  2)
    echo ""
    echo "[partial-ok] visibility silently rewritten by Hub; all other fields took effect"
    exit 0;;
  *)
    echo ""
    echo "[error] verification failed: stored values differ from the request (not a visibility soft-downgrade)" >&2
    rollback_from_backup "$SLUG" "$BACKUP_FILE"
    exit 1;;
esac
