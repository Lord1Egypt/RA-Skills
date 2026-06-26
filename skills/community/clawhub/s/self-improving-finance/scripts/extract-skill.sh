#!/bin/bash
# Finance Skill Extraction Helper
# Creates a new skill from a finance learning entry
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

Create a new finance skill from a learning entry.

Arguments:
  skill-name     Name of the skill (lowercase, hyphens for spaces)

Options:
  --dry-run      Show what would be created without creating files
  --output-dir   Relative output directory under current path (default: ./skills)
  -h, --help     Show this help message

Examples:
  $(basename "$0") month-end-reconciliation-checklist
  $(basename "$0") fx-translation-rates --dry-run
  $(basename "$0") je-approval-workflow --output-dir ./skills/finance

The skill will be created in: \$SKILLS_DIR/<skill-name>/
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
    log_error "Examples: 'month-end-reconciliation', 'fx-translation-rates', 'je-approval-workflow'"
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
    log_error "Use a different name or remove the existing skill first."
    exit 1
fi

if [ "$DRY_RUN" = true ]; then
    log_info "Dry run - would create:"
    echo "  $SKILL_PATH/"
    echo "  $SKILL_PATH/SKILL.md"
    echo ""
    echo "Template content would be:"
    echo "---"
    cat << TEMPLATE
name: $SKILL_NAME
description: "[TODO: Describe the finance procedure, control, or reconciliation pattern this skill addresses]"
---

# $(echo "$SKILL_NAME" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2))}1')

[TODO: Brief introduction — what finance problem this solves]

## Quick Reference

| Situation | Action |
|-----------|--------|
| [Reconciliation/control/close trigger] | [Procedure or remediation to apply] |

## The Problem

[TODO: Describe the incorrect treatment or process gap (anonymized)]

## Solution

[TODO: Describe the correct treatment with standard reference (ASC, IFRS, SOX)]

## Prevention

[TODO: Close checklist item, control step, or system configuration to prevent recurrence]

## Source

- Learning ID: [TODO: Add original learning ID]
- Category: [TODO: reconciliation_error | control_weakness | forecast_variance | regulatory_gap | valuation_error | cash_flow_anomaly]
- Area: [TODO: accounting | treasury | tax | audit | budgeting | reporting | accounts_payable | accounts_receivable]
- Original File: .learnings/LEARNINGS.md

IMPORTANT: All examples must be anonymized. No real account numbers, bank details,
client names, or specific financial figures.
TEMPLATE
    echo "---"
    exit 0
fi

log_info "Creating finance skill: $SKILL_NAME"

mkdir -p "$SKILL_PATH"

cat > "$SKILL_PATH/SKILL.md" << TEMPLATE
---
name: $SKILL_NAME
description: "[TODO: Describe the finance procedure, control, or reconciliation pattern this skill addresses]"
---

# $(echo "$SKILL_NAME" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2))}1')

[TODO: Brief introduction — what finance problem this solves]

## Quick Reference

| Situation | Action |
|-----------|--------|
| [Reconciliation/control/close trigger] | [Procedure or remediation to apply] |

## The Problem

[TODO: Describe the incorrect treatment or process gap (anonymized)]

## Solution

[TODO: Describe the correct treatment with standard reference (ASC, IFRS, SOX)]

## Prevention

[TODO: Close checklist item, control step, or system configuration to prevent recurrence]

## Source

- Learning ID: [TODO: Add original learning ID]
- Category: [TODO: reconciliation_error | control_weakness | forecast_variance | regulatory_gap | valuation_error | cash_flow_anomaly]
- Area: [TODO: accounting | treasury | tax | audit | budgeting | reporting | accounts_payable | accounts_receivable]
- Original File: .learnings/LEARNINGS.md

IMPORTANT: All examples must be anonymized. No real account numbers, bank details,
client names, or specific financial figures.
TEMPLATE

log_info "Created: $SKILL_PATH/SKILL.md"

echo ""
log_info "Skill scaffold created."
echo ""
echo "Next steps:"
echo "  1. Edit $SKILL_PATH/SKILL.md"
echo "  2. Fill in the TODO sections with anonymized finance examples from your learning"
echo "  3. Add prevention section (close checklist item, control step, system config)"
echo "  4. Reference applicable standards (ASC, IFRS, SOX section)"
echo "  5. Add references/ folder if you have detailed documentation"
echo "  6. Update the original learning entry with:"
echo "     **Status**: promoted_to_skill"
echo "     **Skill-Path**: skills/$SKILL_NAME"
