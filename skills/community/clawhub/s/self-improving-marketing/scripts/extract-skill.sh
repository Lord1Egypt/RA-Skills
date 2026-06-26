#!/bin/bash
# Marketing Skill Extraction Helper
# Creates a new skill from a marketing learning entry
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

Create a new marketing skill from a learning entry.

Arguments:
  skill-name     Name of the skill (lowercase, hyphens for spaces)

Options:
  --dry-run      Show what would be created without creating files
  --output-dir   Relative output directory under current path (default: ./skills)
  -h, --help     Show this help message

Examples:
  $(basename "$0") enterprise-messaging-framework
  $(basename "$0") email-deliverability-checklist --dry-run
  $(basename "$0") utm-taxonomy-standard --output-dir ./skills/marketing

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
    log_error "Examples: 'enterprise-messaging-framework', 'email-deliverability-checklist', 'utm-taxonomy-standard'"
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
description: "[TODO: Describe the marketing pattern, campaign insight, or playbook this skill addresses]"
---

# $(echo "$SKILL_NAME" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2))}1')

[TODO: Brief introduction — what marketing problem this solves]

## Quick Reference

| Situation | Action |
|-----------|--------|
| [Campaign/channel trigger] | [Recommended action or playbook step] |

## Background

[TODO: Why this matters — what campaign failures or missed opportunities it prevents]

## Playbook

### Before (underperforming):
- Channel: [TODO]
- Key metric: X.X% (below Y.Y% benchmark)
- Messaging: [TODO: problematic approach]

### After (optimized):
- Key metric: X.X% (above benchmark)
- Messaging: [TODO: improved approach]
- Lift: +XX%

## Prevention

[TODO: Checklist item, review step, or automation to prevent recurrence]

## Benchmarks

| Metric | Poor | Average | Good |
|--------|------|---------|------|
| [Key metric] | <X% | X-Y% | >Y% |

## Source

- Learning ID: [TODO: Add original learning ID]
- Category: [TODO: messaging_miss | channel_underperformance | audience_drift | brand_inconsistency | attribution_gap | content_decay]
- Channel: [TODO: google_ads | linkedin | email | organic_search | social]
- Original File: .learnings/LEARNINGS.md
TEMPLATE
    echo "---"
    exit 0
fi

log_info "Creating marketing skill: $SKILL_NAME"

mkdir -p "$SKILL_PATH"

cat > "$SKILL_PATH/SKILL.md" << TEMPLATE
---
name: $SKILL_NAME
description: "[TODO: Describe the marketing pattern, campaign insight, or playbook this skill addresses]"
---

# $(echo "$SKILL_NAME" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2))}1')

[TODO: Brief introduction — what marketing problem this solves]

## Quick Reference

| Situation | Action |
|-----------|--------|
| [Campaign/channel trigger] | [Recommended action or playbook step] |

## Background

[TODO: Why this matters — what campaign failures or missed opportunities it prevents]

## Playbook

### Before (underperforming):
- Channel: [TODO]
- Key metric: X.X% (below Y.Y% benchmark)
- Messaging: [TODO: problematic approach]

### After (optimized):
- Key metric: X.X% (above benchmark)
- Messaging: [TODO: improved approach]
- Lift: +XX%

## Prevention

[TODO: Checklist item, review step, or automation to prevent recurrence]

## Benchmarks

| Metric | Poor | Average | Good |
|--------|------|---------|------|
| [Key metric] | <X% | X-Y% | >Y% |

## Source

- Learning ID: [TODO: Add original learning ID]
- Category: [TODO: messaging_miss | channel_underperformance | audience_drift | brand_inconsistency | attribution_gap | content_decay]
- Channel: [TODO: google_ads | linkedin | email | organic_search | social]
- Original File: .learnings/LEARNINGS.md
TEMPLATE

log_info "Created: $SKILL_PATH/SKILL.md"

echo ""
log_info "Skill scaffold created."
echo ""
echo "Next steps:"
echo "  1. Edit $SKILL_PATH/SKILL.md"
echo "  2. Fill in the TODO sections with metrics and examples from your learning"
echo "  3. Add benchmarks section with channel-specific thresholds"
echo "  4. Add references/ folder if you have detailed campaign data"
echo "  5. Update the original learning entry with:"
echo "     **Status**: promoted_to_skill"
echo "     **Skill-Path**: skills/$SKILL_NAME"
