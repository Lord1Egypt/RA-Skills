#!/usr/bin/env bash
# update-skill.sh — check for + apply skill updates from GitHub.
#
# VERSION.json is the single source of truth. No need to read SKILL.md
# or API endpoints — just compare version strings.
#
# Usage:  bash update-skill.sh
# Stdout: JSON — success or failure always returns exit 0 (non-fatal)
#
# Output examples:
#   {"updated":false,"current_version":"1.1.0","extension_recommended":"2.3.0","extension_install_url":"https://...","error":null}
#   {"updated":true,"old_version":"1.0.0","new_version":"1.1.0","changelog":"v1.1.0: ...","extension_recommended":"2.3.0","extension_install_url":"https://..."}
#   {"updated":false,"error":"cannot fetch remote version — network issue"}
set -u

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

LOCAL_VERSION_FILE="$HOME/.monsterget/version.json"
REPO="monsterget-com/skills"
BRANCH="main"
REMOTE_URL="https://raw.githubusercontent.com/$REPO/$BRANCH/tiktok-collector/VERSION.json"

# ---- helpers ----

json_val() {
  # Extract a (non-nested) string value from a JSON key.
  # Usage:  json_val "skill" < file.json   or   echo "$json" | json_val "skill"
  sed -n 's/.*"'"$1"'"[[:space:]]*:[[:space:]]*"\([^"]*\)".*/\1/p' | head -1
}

# ---- read local version ----

LOCAL_SKILL="0"
LOCAL_EXT="unknown"
LOCAL_API="0"
if [ -f "$LOCAL_VERSION_FILE" ]; then
  LOCAL_SKILL="$(json_val "skill_version" < "$LOCAL_VERSION_FILE")"
  [ -z "$LOCAL_SKILL" ] && LOCAL_SKILL="0"
  LOCAL_EXT="$(json_val "extension_version" < "$LOCAL_VERSION_FILE")"
  [ -z "$LOCAL_EXT" ] && LOCAL_EXT="unknown"
  LOCAL_API="$(json_val "scrapers_api" < "$LOCAL_VERSION_FILE")"
  [ -z "$LOCAL_API" ] && LOCAL_API="0"
elif [ -f "$SKILL_DIR/VERSION.json" ]; then
  # Bootstrap: no ~/.monsterget/version.json yet, fall back to skill dir
  LOCAL_SKILL="$(json_val "skill" < "$SKILL_DIR/VERSION.json")"
  [ -z "$LOCAL_SKILL" ] && LOCAL_SKILL="0"
  LOCAL_API="$(json_val "scrapers_api" < "$SKILL_DIR/VERSION.json")"
  [ -z "$LOCAL_API" ] && LOCAL_API="0"
fi

# ---- fetch remote version ----

REMOTE_JSON="$(curl -sL --max-time 15 "$REMOTE_URL" 2>/dev/null)" || REMOTE_JSON=""
if [ -z "$REMOTE_JSON" ]; then
  printf '{"updated":false,"current_version":"%s","scrapers_api":"%s","extension_recommended":"%s","extension_install_url":"","error":"cannot fetch remote version — network issue"}\n' \
    "$LOCAL_SKILL" "$LOCAL_API" "$LOCAL_EXT"
  exit 0
fi

REMOTE_SKILL="$(printf '%s' "$REMOTE_JSON" | json_val "skill")"
[ -z "$REMOTE_SKILL" ] && REMOTE_SKILL="0"
REMOTE_EXT="$(printf '%s' "$REMOTE_JSON" | json_val "extension_recommended")"
[ -z "$REMOTE_EXT" ] && REMOTE_EXT="unknown"
REMOTE_INSTALL_URL="$(printf '%s' "$REMOTE_JSON" | json_val "extension_install_url")"
[ -z "$REMOTE_INSTALL_URL" ] && REMOTE_INSTALL_URL="https://monsterget.com/install"
REMOTE_CHANGELOG="$(printf '%s' "$REMOTE_JSON" | json_val "changelog")"
REMOTE_VER="$(printf '%s' "$REMOTE_JSON" | json_val "version")"
REMOTE_API="$(printf '%s' "$REMOTE_JSON" | json_val "scrapers_api")"
[ -z "$REMOTE_API" ] && REMOTE_API="0"

# ---- compare ----

if [ "$LOCAL_SKILL" = "$REMOTE_SKILL" ]; then
  # Skill is current — output extension/scrapers info for the AI to action on
  printf '{"updated":false,"current_version":"%s","scrapers_api":"%s","extension_recommended":"%s","extension_install_url":"%s","error":null}\n' \
    "$REMOTE_VER" "$REMOTE_API" "$REMOTE_EXT" "$REMOTE_INSTALL_URL"
  exit 0
fi

# ---- update: download and replace ----

TMP_DIR="$(mktemp -d 2>/dev/null || echo "$HOME/.monsterget/_update_tmp")"
[ -d "$TMP_DIR" ] || mkdir -p "$TMP_DIR"
trap 'rm -rf "$TMP_DIR"' EXIT

UPDATED=false
if curl -sL --max-time 120 \
  "https://codeload.github.com/$REPO/tar.gz/refs/heads/$BRANCH" \
  -o "$TMP_DIR/repo.tar.gz" &&
  tar -xzf "$TMP_DIR/repo.tar.gz" -C "$TMP_DIR" 2>/dev/null; then

  SRC="$TMP_DIR/skills-$BRANCH/tiktok-collector"
  if [ -f "$SRC/VERSION.json" ]; then
    # Verify the staged files look valid before overwriting
    STAGED_SKILL="$(json_val "skill" < "$SRC/VERSION.json")"
    if [ -n "$STAGED_SKILL" ]; then
      # Remove old scripts, copy entire tree (SKILL.md + scripts + VERSION.json + AGENTS.md + INSTALL.md)
      rm -rf "$SKILL_DIR/scripts"
      cp -r "$SRC/." "$SKILL_DIR/"
      chmod +x "$SKILL_DIR/scripts/"*.sh 2>/dev/null || true
      UPDATED=true
    fi
  fi
fi

# ---- persist local version record ----

mkdir -p "$HOME/.monsterget"
cat > "$LOCAL_VERSION_FILE" <<EOF
{
  "skill_version": "$REMOTE_SKILL",
  "extension_version": "$LOCAL_EXT",
  "scrapers_api": "$LOCAL_API"
}
EOF

# ---- output ----

if [ "$UPDATED" = true ]; then
  printf '{"updated":true,"old_version":"%s","new_version":"%s","changelog":"%s","scrapers_api":"%s","extension_recommended":"%s","extension_install_url":"%s"}\n' \
    "$LOCAL_SKILL" "$REMOTE_SKILL" "$REMOTE_CHANGELOG" "$REMOTE_API" "$REMOTE_EXT" "$REMOTE_INSTALL_URL"
else
  printf '{"updated":false,"current_version":"%s","scrapers_api":"%s","extension_recommended":"%s","extension_install_url":"%s","error":"download failed — skill not updated; network may be unavailable"}\n' \
    "$LOCAL_SKILL" "$LOCAL_API" "$LOCAL_EXT" "$REMOTE_INSTALL_URL"
  # Ensure the local version file still reflects actual disk state (the old skill is still there)
  cat > "$LOCAL_VERSION_FILE" <<EOF
{
  "skill_version": "$LOCAL_SKILL",
  "extension_version": "$LOCAL_EXT",
  "scrapers_api": "$LOCAL_API"
}
EOF
fi
exit 0