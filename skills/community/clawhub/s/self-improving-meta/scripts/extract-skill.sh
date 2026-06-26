#!/bin/bash
# Meta Skill Extraction Helper
# Creates a new skill from a meta learning entry
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

Create a new meta skill from an infrastructure learning entry.

Meta-skills are special: they modify the infrastructure that all other skills
depend on. Extra care in testing is required — always verify in a fresh session.

Arguments:
  skill-name     Name of the skill (lowercase, hyphens for spaces)

Options:
  --dry-run      Show what would be created without creating files
  --output-dir   Relative output directory under current path (default: ./skills)
  -h, --help     Show this help message

Examples:
  $(basename "$0") prompt-file-compression
  $(basename "$0") hook-error-handling --dry-run
  $(basename "$0") rule-deduplication --output-dir ./skills/meta

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
    log_error "Examples: 'prompt-file-compression', 'hook-error-handling', 'rule-deduplication'"
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
description: "[TODO: Describe the agent infrastructure pattern, prompt file fix, or hook improvement this skill addresses]"
---

# $(echo "$SKILL_NAME" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2))}1')

[TODO: Brief introduction — what infrastructure problem this solves]

**WARNING**: This is a meta-skill. It modifies infrastructure that other skills depend on.
Test thoroughly in a fresh session before publishing.

## Quick Reference

| Situation | Action |
|-----------|--------|
| [Infrastructure trigger] | [Fix or improvement] |

## The Problem

### Current State

[TODO: Description of the problematic prompt file content, hook behavior, or rule conflict]

### Impact

[TODO: How this manifests in agent behavior — misinterpretation, ignored rules, context waste]

## Solution

### Fix

[TODO: Corrected instruction, compressed prompt, resolved conflict, or fixed hook]

### Step-by-Step

1. [TODO: Identify the infrastructure problem]
2. [TODO: Locate all affected files]
3. [TODO: Apply the fix]
4. [TODO: Test in a fresh session]
5. [TODO: Document the change]

## Testing

- [ ] Agent correctly interprets the modified instruction
- [ ] No other rules or skills are broken
- [ ] Context token usage is reduced (if applicable)
- [ ] Hook fires correctly (if applicable)

## Propagation

| Change Type | Scope |
|-------------|-------|
| [File changed] | [Who/what is affected] |

## Source

- Learning ID: [TODO: Add original learning ID]
- Category: [TODO: prompt_drift | rule_conflict | skill_gap | hook_failure | context_bloat | instruction_ambiguity]
- Area: [TODO: agent_config | skill_authoring | hook_scripts | prompt_files | rule_files | memory_management | extension_api]
- Original File: .learnings/LEARNINGS.md or .learnings/META_ISSUES.md
TEMPLATE
    echo "---"
    exit 0
fi

log_info "Creating meta skill: $SKILL_NAME"

mkdir -p "$SKILL_PATH"

cat > "$SKILL_PATH/SKILL.md" << TEMPLATE
---
name: $SKILL_NAME
description: "[TODO: Describe the agent infrastructure pattern, prompt file fix, or hook improvement this skill addresses]"
---

# $(echo "$SKILL_NAME" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2))}1')

[TODO: Brief introduction — what infrastructure problem this solves]

**WARNING**: This is a meta-skill. It modifies infrastructure that other skills depend on.
Test thoroughly in a fresh session before publishing.

## Quick Reference

| Situation | Action |
|-----------|--------|
| [Infrastructure trigger] | [Fix or improvement] |

## The Problem

### Current State

[TODO: Description of the problematic prompt file content, hook behavior, or rule conflict]

### Impact

[TODO: How this manifests in agent behavior — misinterpretation, ignored rules, context waste]

## Solution

### Fix

[TODO: Corrected instruction, compressed prompt, resolved conflict, or fixed hook]

### Step-by-Step

1. [TODO: Identify the infrastructure problem]
2. [TODO: Locate all affected files]
3. [TODO: Apply the fix]
4. [TODO: Test in a fresh session]
5. [TODO: Document the change]

## Testing

- [ ] Agent correctly interprets the modified instruction
- [ ] No other rules or skills are broken
- [ ] Context token usage is reduced (if applicable)
- [ ] Hook fires correctly (if applicable)

## Propagation

| Change Type | Scope |
|-------------|-------|
| [File changed] | [Who/what is affected] |

## Source

- Learning ID: [TODO: Add original learning ID]
- Category: [TODO: prompt_drift | rule_conflict | skill_gap | hook_failure | context_bloat | instruction_ambiguity]
- Area: [TODO: agent_config | skill_authoring | hook_scripts | prompt_files | rule_files | memory_management | extension_api]
- Original File: .learnings/LEARNINGS.md or .learnings/META_ISSUES.md
TEMPLATE

log_info "Created: $SKILL_PATH/SKILL.md"

log_warn "Meta-skills modify shared infrastructure. Test in a fresh session before publishing."

echo ""
log_info "Skill scaffold created."
echo ""
echo "Next steps:"
echo "  1. Edit $SKILL_PATH/SKILL.md"
echo "  2. Fill in the TODO sections with the infrastructure fix from your learning"
echo "  3. Add testing checklist (fresh session verification is mandatory for meta-skills)"
echo "  4. Add propagation table showing which files/agents are affected"
echo "  5. Update the original learning entry with:"
echo "     **Status**: promoted_to_skill"
echo "     **Skill-Path**: skills/$SKILL_NAME"
