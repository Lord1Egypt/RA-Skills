#!/bin/bash
# Business Skill Extraction Helper
# Creates a new skill scaffold from a business learning or issue
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

Create a new business skill scaffold from a learning or business issue entry.

Arguments:
  skill-name     Name of the skill (lowercase, hyphens for spaces)

Options:
  --dry-run      Show what would be created without creating files
  --output-dir   Relative output directory under current path (default: ./skills)
  -h, --help     Show this help message

Examples:
  $(basename "$0") approval-escalation-cadence
  $(basename "$0") kpi-definition-registry-ops --dry-run
  $(basename "$0") vendor-handoff-checklist --output-dir ./skills/business
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
    case $1 in
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
    log_error "Output directory must be a relative path under the current directory."
    exit 1
fi

if [[ "$SKILLS_DIR" =~ (^|/)\.\.(/|$) ]]; then
    log_error "Output directory cannot include '..' path segments."
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
    echo "---"
    cat << TEMPLATE
name: $SKILL_NAME
description: "[TODO: Describe the business administration skill and trigger conditions.]"
---

# $(echo "$SKILL_NAME" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2))}1')

[TODO: Brief introduction]

## Quick Reference
| Situation | Recommended Action |
|-----------|-------------------|
| [Business trigger] | [What to do] |

## Recommended Action
[TODO: Step-by-step process guidance]

## Reminder-Only Safety
This skill is documentation/reminder only.
Do NOT execute approvals, spending, vendor commitments, payroll, or legal actions.

## Source
- Entry ID: [TODO: LRN-YYYYMMDD-XXX or BUS-YYYYMMDD-XXX]
TEMPLATE
    echo "---"
    exit 0
fi

mkdir -p "$SKILL_PATH"

cat > "$SKILL_PATH/SKILL.md" << TEMPLATE
---
name: $SKILL_NAME
description: "[TODO: Describe the business administration skill and trigger conditions.]"
---

# $(echo "$SKILL_NAME" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2))}1')

[TODO: Brief introduction]

## Quick Reference

| Situation | Recommended Action |
|-----------|-------------------|
| [Business trigger] | [What to do] |

## Recommended Action

[TODO: Step-by-step process guidance]

## Reminder-Only Safety

This skill is documentation/reminder only.
Do NOT execute approvals, spending, vendor commitments, payroll, or legal actions.

## Source

- Entry ID: [TODO: LRN-YYYYMMDD-XXX or BUS-YYYYMMDD-XXX]
- Original File: .learnings/LEARNINGS.md or .learnings/BUSINESS_ISSUES.md
TEMPLATE

log_info "Created: $SKILL_PATH/SKILL.md"
log_warn "TODO placeholders included. Customize before use."
