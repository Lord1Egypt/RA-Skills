#!/usr/bin/env bash
# skill-hub-query: install / update a skill from the configured Hub
# Usage:
#   bash install.sh <slug> [version] [--yes]
#   bash install.sh some-skill              # install latest (prompts if already installed)
#   bash install.sh some-skill 2.4.0        # install specific version
#   bash install.sh some-skill --yes        # user-authorized; skip overwrite prompt
#
# Note: --yes is a user-authorization flag. An LLM/agent caller MUST NOT add it
# on its own; only add it when the human user has explicitly approved.
set -euo pipefail
SELF_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
# shellcheck source=./_lib.sh
source "${SELF_DIR}/_lib.sh"

setup_legacy_notice

SLUG=""; VERSION=""; YES=0
for arg in "$@"; do
  case "$arg" in
    --yes|-y) YES=1 ;;
    -*)
      echo "[error] Unknown flag: $arg" >&2
      echo "        Usage: bash install.sh <slug> [version] [--yes]" >&2
      exit 1
      ;;
    *)
      if [[ -z "$SLUG" ]]; then
        SLUG="$arg"
      elif [[ -z "$VERSION" ]]; then
        VERSION="$arg"
      else
        echo "[error] Too many positional arguments: $arg" >&2
        exit 1
      fi
      ;;
  esac
done

if [[ -z "$SLUG" ]]; then
  echo "Usage: bash install.sh <slug> [version] [--yes]" >&2
  exit 1
fi

# Security: validate the slug before it is used in any URL or filesystem path.
validate_slug "$SLUG" || exit 1

# Resolve version (use cache, fall back to API)
# Note: skillhub.cn has no cache and no version-list API call here; the download
# endpoint always serves the latest. If a specific version is requested for
# skillhub.cn we honor it on the URL but the public download endpoint ignores it.
if is_skillhub_cn; then
  if [[ -z "$VERSION" ]]; then
    # Try to resolve latest from skillhub.cn detail (informational only)
    detail_json="$(shcn_detail "$SLUG" 2>/dev/null || echo "")"
    if [[ -n "$detail_json" ]]; then
      VERSION="$(echo "$detail_json" | jq -r '.latestVersion.version // "latest"' 2>/dev/null || echo "latest")"
    fi
    [[ -z "$VERSION" ]] && VERSION="latest"
  fi
elif [[ -z "$VERSION" ]]; then
  if [[ -f "$CACHE_FILE" ]]; then
    VERSION="$(jq -r --arg s "$SLUG" '.[$s].latestVersion.version // empty' "$CACHE_FILE" 2>/dev/null || echo "")"
  fi
  if [[ -z "$VERSION" ]]; then
    resp="$(api_get "${HUB_API_PREFIX}/versions/${SLUG}?limit=1")"
    VERSION="$(echo "$resp" | jq -r '.data.items[0].version // empty' 2>/dev/null || echo "")"
  fi
  if [[ -z "$VERSION" ]]; then
    echo "[error] Cannot resolve latest version for ${SLUG}. Check the slug, or run sync.sh first." >&2
    exit 1
  fi
fi

SKILLS_ROOT="$(resolve_skills_dir)"
INSTALL_DIR="${SKILLS_ROOT}/${SLUG}"
echo "[install] preparing: $SLUG @ $VERSION"
echo "[install] target:    $INSTALL_DIR"

# Already-installed -> require confirmation (or --yes)
if [[ -d "$INSTALL_DIR" ]]; then
  installed_ver="$(jq -r --arg s "$SLUG" '.[$s] // "unknown"' "$VERSIONS_FILE" 2>/dev/null || echo "unknown")"
  echo "[install] currently installed: $installed_ver -> will overwrite with $VERSION"

  # If the install dir is inside a git repo, warn about uncommitted changes
  if (cd "$INSTALL_DIR" 2>/dev/null && git rev-parse --git-dir >/dev/null 2>&1); then
    dirty_count="$(cd "$INSTALL_DIR" && git status --porcelain . 2>/dev/null | wc -l 2>/dev/null || echo "0")"
    if [[ "$dirty_count" -gt 0 ]]; then
      echo "[warn] detected $dirty_count uncommitted change(s); overwrite will discard them!" >&2
      echo "       Suggest: cd $INSTALL_DIR && git stash" >&2
    fi
  fi

  if [[ "$YES" != "1" ]]; then
    if [[ ! -t 0 ]]; then
      echo "[error] $SLUG exists and --yes not given; refusing silent overwrite in non-interactive mode." >&2
      echo "        To proceed: bash install.sh $SLUG $VERSION --yes" >&2
      exit 1
    fi
    read -r -p "Confirm overwrite? [y/N] " answer
    if [[ "$answer" != "y" && "$answer" != "Y" ]]; then
      echo "Cancelled."
      exit 0
    fi
  fi
fi

# Download ZIP
tmp_zip="$(mktemp 2>/dev/null || mktemp -t skill-hub-query-zip)"
mv "$tmp_zip" "${tmp_zip}.zip"
tmp_zip="${tmp_zip}.zip"
echo "[install] downloading..."
if is_skillhub_cn; then
  shcn_download "$SLUG" "$tmp_zip" || exit $?
else
  api_download "$SLUG" "$VERSION" "$tmp_zip"
fi

zip_size="$(stat -c %s "$tmp_zip" 2>/dev/null || stat -f %z "$tmp_zip")"
echo "[install] zip size: $zip_size bytes"

# Path-traversal defense: reject entries with .. or absolute paths
#
# Note: awk's `END { exit bad?1:0 }` intentionally returns non-zero on bad
# entries; under set -e + command substitution the whole script would die, so
# wrap in set +e/set -e to isolate.
echo "[install] verifying zip paths..."
set +e
bad_entries="$(unzip -Z1 "$tmp_zip" 2>/dev/null | awk '
  /^\// { print "absolute: " $0; bad=1 }
  /(^|\/)\.\.(\/|$)/ { print "traversal: " $0; bad=1 }
  END { exit bad?1:0 }
')"
awk_status=$?
set -e

if [[ "$awk_status" -ne 0 ]]; then
  echo "[error] zip contains unsafe paths; refusing to extract:" >&2
  echo "$bad_entries" >&2
  rm -f "$tmp_zip"
  exit 6
fi

# Extract to a staging dir; replace whole dir atomically once validated.
# (Naive `unzip -o` would leave ghost files from the old version behind.)
echo "[install] extracting and validating..."
staging="$(mktemp -d 2>/dev/null || mktemp -d -t skill-hub-query-stage)"
trap 'rm -rf "$staging" 2>/dev/null; rm -f "$tmp_zip" 2>/dev/null; rm -f "${_LEGACY_NOTICE_MARKER:-}" 2>/dev/null' EXIT

unzip -o -q "$tmp_zip" -d "$staging"
rm -f "$tmp_zip"

# Some zips wrap content in <slug>/; sink to subdir when needed
src_dir="$staging"
if [[ ! -f "$staging/SKILL.md" ]]; then
  shopt -s nullglob dotglob
  entries=("$staging"/*)
  shopt -u nullglob dotglob
  if [[ "${#entries[@]}" == "1" && -d "${entries[0]}" && -f "${entries[0]}/SKILL.md" ]]; then
    src_dir="${entries[0]}"
  fi
fi

if [[ ! -f "$src_dir/SKILL.md" ]]; then
  echo "[error] Extracted content is missing SKILL.md; aborting without touching the existing install." >&2
  exit 7
fi

# Move into place: backup old -> move new in -> remove backup. Roll back on failure.
echo "[install] installing to $INSTALL_DIR"
backup_dir=""
if [[ -d "$INSTALL_DIR" ]]; then
  backup_dir="${INSTALL_DIR}.bak.$$"
  mv "$INSTALL_DIR" "$backup_dir"
fi
if ! mv "$src_dir" "$INSTALL_DIR"; then
  echo "[error] install failed; rolling back..." >&2
  rm -rf "$INSTALL_DIR" 2>/dev/null || true
  [[ -n "$backup_dir" ]] && mv "$backup_dir" "$INSTALL_DIR"
  exit 8
fi
[[ -n "$backup_dir" ]] && rm -rf "$backup_dir"

# Update versions ledger (atomic write)
mkdir -p "$(dirname "$VERSIONS_FILE")"
if [[ ! -f "$VERSIONS_FILE" ]]; then
  echo '{}' > "$VERSIONS_FILE"
fi
jq --arg s "$SLUG" --arg v "$VERSION" '.[$s] = $v' "$VERSIONS_FILE" \
  > "${VERSIONS_FILE}.tmp"
mv "${VERSIONS_FILE}.tmp" "$VERSIONS_FILE"

# Report
echo "[ok] installed"
echo ""
echo "  Key files:"
if [[ -f "$INSTALL_DIR/SKILL.md" ]]; then
  echo "  - SKILL.md ($(wc -l < "$INSTALL_DIR/SKILL.md") lines)"
fi
if [[ -d "$INSTALL_DIR/scripts" ]]; then
  echo "  - scripts/ ($(find "$INSTALL_DIR/scripts" -type f | wc -l) files)"
fi
if [[ -d "$INSTALL_DIR/references" ]]; then
  echo "  - references/ ($(find "$INSTALL_DIR/references" -type f | wc -l) files)"
fi
echo ""
echo "  The skill will be loaded on the next agent session start."
