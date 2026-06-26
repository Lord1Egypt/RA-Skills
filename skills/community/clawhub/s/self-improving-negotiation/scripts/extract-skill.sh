#!/bin/bash
# Negotiation Skill Extraction Helper
# Creates a new skill scaffold from a negotiation learning or issue entry.
# Usage: ./extract-skill.sh <skill-name> [--dry-run]

set -e

SKILLS_DIR="./skills"
SKILL_NAME=""
DRY_RUN=false

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

usage() {
    cat << EOF
Usage: $(basename "$0") <skill-name> [options]

Create a negotiation skill scaffold from learnings.

Arguments:
  skill-name     Name of the skill (lowercase, hyphens)

Options:
  --dry-run      Show generated scaffold without writing files
  --output-dir   Relative output directory (default: ./skills)
  -h, --help     Show this help message

Examples:
  $(basename "$0") value-anchor-reset
  $(basename "$0") concession-guardrail --dry-run
  $(basename "$0") batna-preflight --output-dir ./skills/negotiation
EOF
}

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1" >&2; }

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
    log_error "Invalid skill name format (lowercase letters, numbers, hyphens)"
    exit 1
fi

if [[ "$SKILLS_DIR" = /* ]]; then
    log_error "Output directory must be relative"
    exit 1
fi

if [[ "$SKILLS_DIR" =~ (^|/)\.\.(/|$) ]]; then
    log_error "Output directory cannot include '..'"
    exit 1
fi

SKILLS_DIR="${SKILLS_DIR#./}"
SKILLS_DIR="./$SKILLS_DIR"
SKILL_PATH="$SKILLS_DIR/$SKILL_NAME"

if [ "$DRY_RUN" = true ]; then
    log_info "Dry run. Would create:"
    echo "  $SKILL_PATH/SKILL.md"
    echo ""
    cat << TEMPLATE
---
name: $SKILL_NAME
description: "[TODO: Describe the negotiation pattern and trigger conditions]"
---

# $(echo "$SKILL_NAME" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) \$i=toupper(substr(\$i,1,1)) tolower(substr(\$i,2))}1')

[TODO: Explain what this negotiation skill solves]

## Quick Reference

| Situation | Action |
|-----------|--------|
| [Trigger] | [Response] |

## Guardrails

- [TODO: Concession thresholds]
- [TODO: Approval requirements]
- [TODO: BATNA and escalation requirements]

## Source

- Entry ID: [TODO]
- Category: [TODO]
- Original File: .learnings/LEARNINGS.md or .learnings/NEGOTIATION_ISSUES.md
TEMPLATE
    exit 0
fi

if [ -d "$SKILL_PATH" ]; then
    log_error "Skill already exists: $SKILL_PATH"
    exit 1
fi

mkdir -p "$SKILL_PATH"

cat > "$SKILL_PATH/SKILL.md" << TEMPLATE
---
name: $SKILL_NAME
description: "[TODO: Describe the negotiation pattern and trigger conditions]"
---

# $(echo "$SKILL_NAME" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) \$i=toupper(substr(\$i,1,1)) tolower(substr(\$i,2))}1')

[TODO: Explain what this negotiation skill solves]

## Quick Reference

| Situation | Action |
|-----------|--------|
| [Trigger] | [Response] |

## Guardrails

- [TODO: Concession thresholds]
- [TODO: Approval requirements]
- [TODO: BATNA and escalation requirements]

## Safety

Reminder-only pattern documentation.
No auto-acceptance of terms, no pricing commitment, no legal/financial approvals, no finalization of agreements.

## Source

- Entry ID: [TODO]
- Category: [TODO]
- Original File: .learnings/LEARNINGS.md or .learnings/NEGOTIATION_ISSUES.md
TEMPLATE

log_info "Created: $SKILL_PATH/SKILL.md"
log_info "Next: fill TODOs, validate safety guardrails, and update source entry status."

