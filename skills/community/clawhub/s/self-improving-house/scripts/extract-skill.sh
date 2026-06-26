#!/bin/bash
# Domotics Skill Extraction Helper
# Creates a new skill scaffold from a domotics learning/issue.
# Usage: ./extract-skill.sh <skill-name> [--dry-run]

set -e

SKILLS_DIR="./skills"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

usage() {
    cat << EOF
Usage: $(basename "$0") <skill-name> [options]

Create a new domotics skill scaffold from a recurring learning or issue.

Arguments:
  skill-name     Lowercase name with hyphens

Options:
  --dry-run      Print scaffold without creating files
  --output-dir   Relative output directory (default: ./skills)
  -h, --help     Show help

Examples:
  $(basename "$0") night-occupancy-lock-guard
  $(basename "$0") zigbee-mesh-recovery --dry-run
  $(basename "$0") hvac-overshoot-control --output-dir ./skills/domotics
EOF
}

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1" >&2
}

SKILL_NAME=""
DRY_RUN=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --output-dir)
            if [ -z "${2:-}" ] || [[ "${2:-}" == -* ]]; then
                log_error "--output-dir requires a relative path argument"
                usage
                exit 1
            fi
            SKILLS_DIR="$2"
            shift 2
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        -*)
            log_error "Unknown option: $1"
            usage
            exit 1
            ;;
        *)
            if [ -z "$SKILL_NAME" ]; then
                SKILL_NAME="$1"
            else
                log_error "Unexpected argument: $1"
                usage
                exit 1
            fi
            shift
            ;;
    esac
done

if [ -z "$SKILL_NAME" ]; then
    log_error "Skill name is required"
    usage
    exit 1
fi

if ! [[ "$SKILL_NAME" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
    log_error "Invalid skill name format. Use lowercase letters, numbers, and hyphens only."
    exit 1
fi

if [[ "$SKILLS_DIR" = /* ]]; then
    log_error "Output directory must be relative."
    exit 1
fi

if [[ "$SKILLS_DIR" =~ (^|/)\.\.(/|$) ]]; then
    log_error "Output directory cannot include '..'."
    exit 1
fi

SKILLS_DIR="${SKILLS_DIR#./}"
SKILLS_DIR="./$SKILLS_DIR"
SKILL_PATH="$SKILLS_DIR/$SKILL_NAME"

if [ -d "$SKILL_PATH" ] && [ "$DRY_RUN" = false ]; then
    log_error "Skill already exists: $SKILL_PATH"
    exit 1
fi

if [ "$DRY_RUN" = true ]; then
    log_info "Dry run - would create:"
    echo "  $SKILL_PATH/"
    echo "  $SKILL_PATH/SKILL.md"
    echo ""
    cat << TEMPLATE
---
name: $SKILL_NAME
description: "[TODO: Describe domotics pattern and trigger conditions]"
---

# $(echo "$SKILL_NAME" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2))}1')

[TODO: Problem statement and context]

## Quick Reference

| Situation | Action |
|-----------|--------|
| [TODO] | [TODO] |

## Safety Boundary

- Documentation/reminder only
- No direct actuator actions
- Human confirmation for locks/alarms/gas-water/heaters

## Diagnostic Steps

1. [TODO]
2. [TODO]
3. [TODO]

## Remediation

[TODO: Repeatable procedure]

## Source

- Entry ID: [TODO: LRN-... or DOM-...]
- Category: [TODO: automation_conflict | sensor_drift | device_unreachable | integration_break | energy_optimization | safety_rule_gap | occupancy_mismatch | latency_jitter]
- Original File: .learnings/LEARNINGS.md or .learnings/DOMOTICS_ISSUES.md
TEMPLATE
    exit 0
fi

mkdir -p "$SKILL_PATH"

cat > "$SKILL_PATH/SKILL.md" << TEMPLATE
---
name: $SKILL_NAME
description: "[TODO: Describe domotics pattern and trigger conditions]"
---

# $(echo "$SKILL_NAME" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2))}1')

[TODO: Problem statement and context]

## Quick Reference

| Situation | Action |
|-----------|--------|
| [TODO] | [TODO] |

## Safety Boundary

- Documentation/reminder only
- No direct actuator actions
- Human confirmation for locks/alarms/gas-water/heaters

## Diagnostic Steps

1. [TODO]
2. [TODO]
3. [TODO]

## Remediation

[TODO: Repeatable procedure]

## Source

- Entry ID: [TODO: LRN-... or DOM-...]
- Category: [TODO: automation_conflict | sensor_drift | device_unreachable | integration_break | energy_optimization | safety_rule_gap | occupancy_mismatch | latency_jitter]
- Original File: .learnings/LEARNINGS.md or .learnings/DOMOTICS_ISSUES.md
TEMPLATE

log_info "Created: $SKILL_PATH/SKILL.md"
log_warn "Review TODO placeholders before using the extracted skill."
