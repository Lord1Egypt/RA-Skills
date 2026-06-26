#!/usr/bin/env bash
# /spidershield pin <subcommand> [args]
# Skill pinning — detect rug pull attacks by tracking content hashes.
# Wraps: spidershield agent-pin add|verify|list|remove|add-all

set -euo pipefail

# Helper: resolve CLI command (prefer spidershield open-source package)
_run() {
  if command -v spidershield &>/dev/null; then
    spidershield "$@"
  elif python3 -c "import spidershield" 2>/dev/null; then
    python3 -m spidershield "$@"
  else
    echo "" >&2
    echo "spidershield not installed. To use this command:" >&2
    echo "" >&2
    echo "  pip install spidershield" >&2
    echo "" >&2
    echo "Or use /spidershield check <skill-name> (works without installation)." >&2
    exit 1
  fi
}

SUBCMD="${1:-}"
if [[ $# -gt 0 ]]; then shift; fi

case "$SUBCMD" in
  add)
    TARGET="${1:-}"
    if [[ -z "$TARGET" ]]; then
      echo "Usage: /spidershield pin add <path-to-skill>" >&2
      echo "Example: /spidershield pin add ~/.openclaw/skills/web-search-pro/" >&2
      exit 1
    fi
    echo ""
    echo "SpiderShield — Pin Skill"
    echo ""
    _run agent-pin add "$TARGET"
    ;;
  add-all)
    echo ""
    echo "SpiderShield — Pin All Installed Skills"
    echo ""
    _run agent-pin add-all
    ;;
  verify)
    echo ""
    echo "SpiderShield — Verify Pinned Skills"
    echo ""
    TARGET="${1:-}"
    if [[ -n "$TARGET" ]]; then
      if [[ -e "$TARGET" ]]; then
        _run agent-pin verify "$TARGET"
      elif [[ -d "$HOME/.openclaw/skills/$TARGET" ]]; then
        _run agent-pin verify "$HOME/.openclaw/skills/$TARGET"
      else
        echo "Error: '$TARGET' not found as path or installed skill name." >&2
        echo "Usage: /spidershield pin verify [<path-to-skill>]" >&2
        exit 1
      fi
    else
      _run agent-pin verify
    fi
    ;;
  list)
    echo ""
    echo "SpiderShield — Pinned Skills"
    echo ""
    _run agent-pin list
    ;;
  remove)
    NAME="${1:-}"
    if [[ -z "$NAME" ]]; then
      echo "Usage: /spidershield pin remove <skill-name>" >&2
      exit 1
    fi
    _run agent-pin remove "$NAME"
    ;;
  *)
    echo "SpiderShield Pin — Rug Pull Detection" >&2
    echo "" >&2
    echo "Usage:" >&2
    echo "  /spidershield pin add <path>        Pin a skill (record hash)" >&2
    echo "  /spidershield pin add-all           Pin all installed skills" >&2
    echo "  /spidershield pin verify [path]     Verify pinned skills" >&2
    echo "  /spidershield pin list              List all pinned skills" >&2
    echo "  /spidershield pin remove <name>     Remove a pin" >&2
    exit 1
    ;;
esac
