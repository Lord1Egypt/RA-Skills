#!/usr/bin/env bash
# update-ox.sh — "is the pinned ox install usable?" readiness gate for
# every invocation of this skill.
#
# Reads ~/.openclaw/memory/sageox-ox-install.json to confirm the install
# state exists, then verifies that `ox` on PATH resolves to the pinned
# install at $HOME/.local/bin/ox. A bare `command -v ox` is insufficient:
# if an older system ox (e.g. /usr/local/bin/ox) appears before
# $HOME/.local/bin on PATH, `command -v` would silently resolve to it
# and defeat the pinned-release contract. The curl install path has no
# per-run update — users re-run install-ox-curl.sh to bump the pinned
# release.
#
# Usage: update-ox.sh
#
# Stdout: nothing on success
# Stderr: one-line "needs install", "not at pinned path", or "PATH
#         order wrong" signal
# Exit:
#   0 — pinned ox is ready, agent should proceed to the next prerequisite
#   2 — ox is not usable (no state file, binary missing at pinned path,
#       or PATH resolves to a different ox); agent must read
#       references/INSTALL.md and run the install flow before continuing

set -euo pipefail

STATE_FILE="$HOME/.openclaw/memory/sageox-ox-install.json"
EXPECTED_OX="$HOME/.local/bin/ox"

if [ ! -f "$STATE_FILE" ]; then
  echo "ox install state not configured — run install flow from references/INSTALL.md" >&2
  exit 2
fi

# The pinned install must actually exist at the expected path. Anything
# else (deleted, wrong permissions, never installed by this skill) means
# the state file is stale and the install flow needs to be re-run.
if [ ! -x "$EXPECTED_OX" ]; then
  echo "error: ox is not installed at $EXPECTED_OX" >&2
  echo "fix: re-run the install flow from references/INSTALL.md" >&2
  exit 2
fi

# `command -v` must resolve to the pinned install — not some other ox
# earlier on PATH. If an older system install shadows the pinned one,
# running the skill against it would defeat the whole point of the
# pinned-release contract, so fail with a PATH-order hint.
resolved_ox="$(command -v ox 2>/dev/null || true)"
if [ "$resolved_ox" != "$EXPECTED_OX" ]; then
  echo "error: 'ox' resolves to '${resolved_ox:-<not on PATH>}', not $EXPECTED_OX" >&2
  echo "fix: prepend \$HOME/.local/bin to PATH in ~/.openclaw/.env so the pinned install wins" >&2
  exit 2
fi

# Verify the binary itself still reports the pinned version. The path
# check above proves PATH order is right; this check proves the bytes
# behind the path haven't been replaced or corrupted since install.
# `jq` is required by the skill (see SKILL.md § 2), so it's guaranteed
# present by the time this script runs.
expected_ref="$(jq -r '.ox_install_ref // empty' "$STATE_FILE" 2>/dev/null || true)"
if [ -z "$expected_ref" ]; then
  echo "error: $STATE_FILE is missing ox_install_ref" >&2
  echo "fix: re-run the install flow from references/INSTALL.md" >&2
  exit 2
fi
expected_version="${expected_ref#v}"

if ! version_output="$("$EXPECTED_OX" version 2>&1)"; then
  echo "error: $EXPECTED_OX failed to run" >&2
  echo "$version_output" >&2
  echo "fix: re-run the install flow from references/INSTALL.md" >&2
  exit 2
fi

first_line="$(printf '%s\n' "$version_output" | head -n1)"
if [ "$first_line" != "ox $expected_version" ]; then
  echo "error: $EXPECTED_OX reports '$first_line', expected 'ox $expected_version'" >&2
  echo "fix: re-run the install flow from references/INSTALL.md" >&2
  exit 2
fi

exit 0
