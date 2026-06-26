#!/bin/bash
# skill-cost - wrapper script for OpenClaw agent
# Usage: bash ~/.openclaw/workspace/skills/skill-cost/skill-cost.sh <command> [args]
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
VENV_ACTIVATE="$SKILL_DIR/.venv/bin/activate"
if [ -f "$VENV_ACTIVATE" ] && [ ! -L "$VENV_ACTIVATE" ]; then
  source "$VENV_ACTIVATE"
fi

case "$1" in
  report)
    shift
    python3 "$SKILL_DIR/src/cost_report.py" "$@"
    ;;
  ranking)
    shift
    python3 "$SKILL_DIR/src/cost_report.py" --top 10 "$@"
    ;;
  detail)
    shift
    python3 "$SKILL_DIR/src/cost_query.py" detail "$@"
    ;;
  compare)
    shift
    python3 "$SKILL_DIR/src/cost_query.py" compare "$@"
    ;;
  *)
    echo "skill-cost — Per-skill token usage and cost tracker"
    echo ""
    echo "Commands:"
    echo "  bash $0 report                        Full per-skill cost report"
    echo "  bash $0 report --days 7               Last 7 days"
    echo "  bash $0 report --since 2026-03-01     Since a specific date"
    echo "  bash $0 report --format json           JSON output"
    echo "  bash $0 ranking                        Top 10 skills by cost"
    echo "  bash $0 ranking --top 5               Top N skills"
    echo "  bash $0 detail <skill-name>           Detailed breakdown for a skill"
    echo "  bash $0 compare <skill1> <skill2>     Compare two skills"
    echo ""
    echo "Global options:"
    echo "  --days N         Filter to last N days"
    echo "  --since DATE     Filter since YYYY-MM-DD"
    echo "  --agent NAME     Filter by agent name"
    echo "  --format FORMAT  Output format: text (default), json"
    ;;
esac
