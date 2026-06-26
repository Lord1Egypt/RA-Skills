#!/bin/bash
set -euo pipefail

# SECURITY MANIFEST:
#   Environment variables accessed directly: none
#   Runtime/provider environment variables may be accessed by the installed SkillProbe CLI
#   External endpoints called: whatever configured LLM provider the installed runtime is already using
#   Local files read: SKILL.md of target skill being evaluated
#   Local files written: evaluation reports in outputs/ directory

# SkillProbe evaluation helper script
# This script runs the full evaluation pipeline on a target skill directory.

if [ $# -lt 1 ]; then
    echo "Usage: evaluate.sh <skill-path> [--model MODEL] [--tasks COUNT] [--repeats N] [--llm-judge] [--judge-model MODEL] [--db PATH]"
    echo ""
    echo "Example: evaluate.sh ./skills/my-skill --model your-model --tasks 30 --repeats 2 --llm-judge --db outputs/evaluations.db"
    exit 1
fi

SKILL_PATH="$1"
shift

MODEL=""
TASKS=30
REPEATS=2
ENABLE_LLM_JUDGE=0
JUDGE_MODEL=""
DB_PATH="outputs/evaluations.db"

while [[ $# -gt 0 ]]; do
    case $1 in
        --model)
            MODEL=$(printf '%s' "$2" | tr -cd '[:alnum:]._-/')
            shift 2
            ;;
        --tasks)
            TASKS=$(printf '%s' "$2" | tr -cd '[:digit:]')
            shift 2
            ;;
        --repeats)
            REPEATS=$(printf '%s' "$2" | tr -cd '[:digit:]')
            shift 2
            ;;
        --llm-judge)
            ENABLE_LLM_JUDGE=1
            shift
            ;;
        --judge-model)
            JUDGE_MODEL=$(printf '%s' "$2" | tr -cd '[:alnum:]._-/')
            shift 2
            ;;
        --db)
            DB_PATH=$(printf '%s' "$2" | tr -cd '[:alnum:]._/-')
            shift 2
            ;;
        *)
            echo "Unknown option: $1"
            exit 1
            ;;
    esac
done

if [ ! -d "$SKILL_PATH" ]; then
    echo "Error: $SKILL_PATH is not a directory"
    exit 1
fi

echo "SkillProbe: Evaluating skill at $SKILL_PATH"
echo "  Model: ${MODEL:-<runtime-configured>}"
echo "  Tasks: $TASKS"
echo "  Repeats: $REPEATS"
echo "  LLM Judge: $([ "$ENABLE_LLM_JUDGE" -eq 1 ] && echo enabled || echo disabled)"
echo "  Judge model: ${JUDGE_MODEL:-<same as eval model>}"
echo "  SQLite DB: $DB_PATH"
echo ""

SCRIPT_DIR=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
PACKAGE_ROOT=$(cd "$SCRIPT_DIR/../.." && pwd)
HAS_RUNTIME=0

if [ -f "$PACKAGE_ROOT/apps/cli/main.py" ]; then
    HAS_RUNTIME=1
fi

if command -v skillprobe >/dev/null 2>&1; then
    HAS_RUNTIME=1
fi

if [ "$HAS_RUNTIME" -eq 0 ]; then
    cat <<EOF
SkillProbe helper runtime was not found next to this ClawHub package.

This package is still useful in OpenClaw as a prompt-driven evaluation workflow:
- ask the agent to profile a target skill
- generate baseline vs with-skill tasks
- compare the outputs using the report format in SKILL.md

If you want the local CLI evaluator, install the full SkillProbe project first:
  1. Clone or open the full skillprobe source tree
  2. Run: pip install -e /path/to/skillprobe
  3. Re-run either:
     - skillprobe evaluate <skill-path> --model $MODEL --tasks $TASKS --repeats $REPEATS --db $DB_PATH
     - bash clawhub/scripts/evaluate.sh <skill-path> --model $MODEL --tasks $TASKS --repeats $REPEATS --db $DB_PATH
EOF
    exit 1
fi

if [ -f "$PACKAGE_ROOT/apps/cli/main.py" ]; then
    CMD=(python -m apps.cli.main evaluate "$SKILL_PATH" --tasks "$TASKS" --repeats "$REPEATS" --db "$DB_PATH")
    if [ -n "$MODEL" ]; then
        CMD+=(--model "$MODEL")
    fi
    if [ "$ENABLE_LLM_JUDGE" -eq 1 ]; then
        CMD+=(--llm-judge)
    fi
    if [ -n "$JUDGE_MODEL" ]; then
        CMD+=(--judge-model "$JUDGE_MODEL")
    fi
    (
        cd "$PACKAGE_ROOT"
        "${CMD[@]}"
    )
    exit 0
fi

if command -v skillprobe >/dev/null 2>&1; then
    CMD=(skillprobe evaluate "$SKILL_PATH" --tasks "$TASKS" --repeats "$REPEATS" --db "$DB_PATH")
    if [ -n "$MODEL" ]; then
        CMD+=(--model "$MODEL")
    fi
    if [ "$ENABLE_LLM_JUDGE" -eq 1 ]; then
        CMD+=(--llm-judge)
    fi
    if [ -n "$JUDGE_MODEL" ]; then
        CMD+=(--judge-model "$JUDGE_MODEL")
    fi
    "${CMD[@]}"
    exit 0
fi
