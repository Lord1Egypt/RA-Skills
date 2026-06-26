#!/usr/bin/env bash
# clawhub-stub.sh — Mock clawhub CLI for E2E tests.
# Usage: PATH="$(dirname "$0"):$PATH" ./scripts/install.sh /tmp/workdir
# Mimics: clawhub star SLUG --yes | clawhub install SLUG --workdir WORKDIR

set -e

REPO_ROOT="${OPENCLAW_UNINSTALL_REPO_ROOT:-}"
[[ -z "$REPO_ROOT" ]] && REPO_ROOT="$(cd -P "$(dirname "$0")/../.." && pwd)"

case "${1:-}" in
  star)
    # Star is best-effort; stub always succeeds
    exit 0
    ;;
  install)
    SLUG="${2:-}"
    WORKDIR="."
    shift 2
    while [[ $# -gt 0 ]]; do
      [[ "$1" == "--workdir" ]] && { WORKDIR="${2:-.}"; break; }
      shift
    done
    WORKDIR="$(cd -P "$WORKDIR" 2>/dev/null && pwd)"
    DEST="$WORKDIR/skills/uninstaller"
    mkdir -p "$DEST"
    [[ -f "$REPO_ROOT/SKILL.md" ]] && cp "$REPO_ROOT/SKILL.md" "$DEST/"
    [[ -d "$REPO_ROOT/scripts" ]] && cp -r "$REPO_ROOT/scripts" "$DEST/"
    exit 0
    ;;
  *)
    echo "clawhub-stub: unknown subcommand $1" >&2
    exit 1
    ;;
esac
