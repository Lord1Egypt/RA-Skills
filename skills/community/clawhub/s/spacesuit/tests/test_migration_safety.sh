#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT
WS="$TMP/workspace with spaces"
bash "$ROOT/scripts/install.sh" --workspace "$WS" >/dev/null
[[ -d "$WS/var/pid" && -d "$WS/tmp" ]]
printf '0.3.0\n' > "$WS/.spacesuit-version"
printf '\nCUSTOM OUTSIDE MARKERS\n' >> "$WS/AGENTS.md"
cp "$WS/AGENTS.md" "$TMP/original"
bash "$ROOT/scripts/install.sh" --workspace "$WS" >/dev/null
cmp "$WS/AGENTS.md" "$TMP/original"
[[ "$(cat "$WS/.spacesuit-version")" == 0.3.0 ]]
printf 'Personal unmarked instructions\n' > "$WS/SOUL.md"
bash "$ROOT/scripts/upgrade.sh" --workspace "$WS" >/dev/null
[[ "$(cat "$WS/SOUL.md")" == 'Personal unmarked instructions' ]]
[[ "$(cat "$WS/.spacesuit-version")" == 0.3.0 ]]
bash "$ROOT/scripts/upgrade.sh" --workspace "$WS" --adopt-unmarked --dry-run >/dev/null
[[ ! -d "$WS/.spacesuit-backups" ]]
bash "$ROOT/scripts/upgrade.sh" --workspace "$WS" --adopt-unmarked >/dev/null
[[ "$(cat "$WS/.spacesuit-version")" == "$(cat "$ROOT/VERSION")" ]]
grep -q 'CUSTOM OUTSIDE MARKERS' "$WS/AGENTS.md"
BACKUPS=("$WS"/.spacesuit-backups/upgrade.*)
[[ "${#BACKUPS[@]}" -eq 1 ]]
BACKUP="${BACKUPS[0]}"
[[ "$(cat "$BACKUP/SOUL.md")" == 'Personal unmarked instructions' ]]
cp "$BACKUP/SOUL.md" "$WS/SOUL.md"
cp "$BACKUP/.spacesuit-version" "$WS/.spacesuit-version"
cmp "$BACKUP/SOUL.md" "$WS/SOUL.md"
[[ "$(cat "$WS/.spacesuit-version")" == 0.3.0 ]]
printf '\n<!-- SPACESUIT:BEGIN AGENTS -->\n' >> "$WS/AGENTS.md"
cp "$WS/SOUL.md" "$TMP/before-reject"
if bash "$ROOT/scripts/upgrade.sh" --workspace "$WS" --adopt-unmarked >/dev/null 2>&1; then exit 1; fi
cmp "$WS/SOUL.md" "$TMP/before-reject"
# A registry-shaped source can omit extensionless version/build files.
PKG="$TMP/package"; mkdir "$PKG"
cp -R "$ROOT/scripts" "$ROOT/base" "$ROOT/templates" "$PKG/"
cp "$ROOT/version.txt" "$PKG/"
bash "$PKG/scripts/install.sh" --workspace "$TMP/registry workspace" >/dev/null
[[ "$(cat "$TMP/registry workspace/.spacesuit-version")" == "$(cat "$ROOT/version.txt")" ]]
echo 'Migration preservation, dry run, marker rejection, backup restoration and version fallback pass.'
