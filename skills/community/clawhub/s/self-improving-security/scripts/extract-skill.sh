#!/bin/bash
# Security Skill Extraction Helper
# Creates a new security skill from a learning or incident entry
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

Create a new security skill from a learning or incident entry.

Arguments:
  skill-name     Name of the skill (lowercase, hyphens for spaces)

Options:
  --dry-run      Show what would be created without creating files
  --output-dir   Relative output directory under current path (default: ./skills)
  -h, --help     Show this help message

Examples:
  $(basename "$0") s3-bucket-hardening
  $(basename "$0") jwt-validation-patterns --dry-run
  $(basename "$0") secret-rotation-playbook --output-dir ./skills/security

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
    log_error "Examples: 's3-bucket-hardening', 'jwt-validation', 'secret-rotation'"
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
description: "[TODO: Describe the security skill and when to use it. Include threat/trigger conditions.]"
---

# $(echo "$SKILL_NAME" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2))}1')

[TODO: Brief introduction explaining the security problem this skill addresses]

## Quick Reference

| Threat/Trigger | Remediation |
|----------------|-------------|
| [Security trigger] | [What to do] |

## Background

[TODO: Why this matters — what vulnerability, risk, or compliance gap it addresses]

## Remediation

[TODO: Step-by-step remediation with commands/configuration]

## Verification

[TODO: How to verify the remediation was effective]

## CRITICAL REMINDER

NEVER include actual secrets, credentials, tokens, or PII in this skill.
All sensitive values must use REDACTED_* placeholders.

## Related Standards

- CWE: [TODO]
- Compliance: [TODO: SOC2 / GDPR / HIPAA / PCI-DSS reference]

## Source

This skill was extracted from a security finding.
- Entry ID: [TODO: LRN-YYYYMMDD-XXX or SEC-YYYYMMDD-XXX]
- Original File: .learnings/LEARNINGS.md or .learnings/SECURITY_INCIDENTS.md
TEMPLATE
    echo "---"
    exit 0
fi

log_info "Creating security skill: $SKILL_NAME"

mkdir -p "$SKILL_PATH"

cat > "$SKILL_PATH/SKILL.md" << TEMPLATE
---
name: $SKILL_NAME
description: "[TODO: Describe the security skill and when to use it. Include threat/trigger conditions.]"
---

# $(echo "$SKILL_NAME" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2))}1')

[TODO: Brief introduction explaining the security problem this skill addresses]

## Quick Reference

| Threat/Trigger | Remediation |
|----------------|-------------|
| [Security trigger] | [What to do] |

## Background

[TODO: Why this matters — what vulnerability, risk, or compliance gap it addresses]

## Remediation

[TODO: Step-by-step remediation with commands/configuration]

## Verification

[TODO: How to verify the remediation was effective]

## CRITICAL REMINDER

NEVER include actual secrets, credentials, tokens, or PII in this skill.
All sensitive values must use REDACTED_* placeholders.

## Related Standards

- CWE: [TODO]
- Compliance: [TODO: SOC2 / GDPR / HIPAA / PCI-DSS reference]

## Source

This skill was extracted from a security finding.
- Entry ID: [TODO: LRN-YYYYMMDD-XXX or SEC-YYYYMMDD-XXX]
- Original File: .learnings/LEARNINGS.md or .learnings/SECURITY_INCIDENTS.md
TEMPLATE

log_info "Created: $SKILL_PATH/SKILL.md"

echo ""
log_info "Security skill scaffold created."
echo ""
echo "Next steps:"
echo "  1. Edit $SKILL_PATH/SKILL.md"
echo "  2. Fill in TODO sections with content from your finding"
echo "  3. Verify NO secrets, credentials, or PII are included"
echo "  4. Add references/ folder for compliance mappings"
echo "  5. Add scripts/ folder for scanners or hardening scripts"
echo "  6. Update the original entry with:"
echo "     **Status**: promoted_to_skill"
echo "     **Skill-Path**: skills/$SKILL_NAME"
