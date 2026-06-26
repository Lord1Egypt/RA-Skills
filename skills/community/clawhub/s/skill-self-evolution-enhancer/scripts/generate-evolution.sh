#!/bin/bash
# Skill Self-Evolution Scaffold Generator
# Creates .learnings/ and template files in a target skill for domain-specific self-improvement.
# Usage: ./generate-evolution.sh <target-skill-path> [--dry-run]
#
# Part of skill-self-evolution-enhancer. The agent should then:
# 1. Read the target skill's SKILL.md
# 2. Perform deep capability & scenario analysis
# 3. Fill DOMAIN-CONFIG-DRAFT.md with extracted domain
# 4. Parameterize and finalize .learnings/ files and EVOLUTION.md
# 5. Add Review→Apply→Report and OpenClaw feedback rules

set -e

# Resolve script directory (skill-self-evolution-enhancer/scripts/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ASSETS_DIR="$(cd "$SCRIPT_DIR/../assets" && pwd)"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

usage() {
    cat << EOF
Usage: $(basename "$0") <target-skill-path> [options]

Create self-evolution scaffolding in a target skill. Output structure matches self-improving-agent:
  target-skill/.learnings/LEARNINGS.md, ERRORS.md, FEATURE_REQUESTS.md

Arguments:
  target-skill-path   Path to the skill directory (e.g., ./skills/my-skill, ~/skills/rewrite-master)

Options:
  --dry-run          Show what would be created without creating files
  -h, --help         Show this help message

Examples:
  $(basename "$0") ./skills/rewrite-master
  $(basename "$0") ~/.cursor/skills/pc-optimizer --dry-run

Output:
  - target-skill/.learnings/LEARNINGS.md, ERRORS.md, FEATURE_REQUESTS.md (with placeholders)
  - target-skill/DOMAIN-CONFIG-DRAFT.md (for agent to fill)
  - target-skill/EVOLUTION.md (with placeholders)
EOF
}

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1" >&2; }

# Parse arguments
TARGET_PATH=""
DRY_RUN=false

while [[ $# -gt 0 ]]; do
    case $1 in
        --dry-run)
            DRY_RUN=true
            shift
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
            if [ -z "$TARGET_PATH" ]; then
                TARGET_PATH="$1"
            else
                log_error "Unexpected argument: $1"
                usage
                exit 1
            fi
            shift
            ;;
    esac
done

if [ -z "$TARGET_PATH" ]; then
    log_error "Target skill path is required"
    usage
    exit 1
fi

# Resolve to absolute path
TARGET_PATH="$(cd "$TARGET_PATH" 2>/dev/null && pwd)" || {
    log_error "Target path does not exist or is not accessible: $TARGET_PATH"
    exit 1
}

# Validate target has SKILL.md
if [ ! -f "$TARGET_PATH/SKILL.md" ]; then
    log_error "Target skill must have SKILL.md: $TARGET_PATH/SKILL.md"
    exit 1
fi

# Validate assets exist
for f in DOMAIN-CONFIG-TEMPLATE.md LEARNINGS-TEMPLATE.md ERRORS-TEMPLATE.md FEATURE_REQUESTS-TEMPLATE.md EVOLUTION-RULES-TEMPLATE.md; do
    if [ ! -f "$ASSETS_DIR/$f" ]; then
        log_error "Missing asset: $ASSETS_DIR/$f"
        exit 1
    fi
done

# Same structure as self-improving-agent: .learnings/ directly
LEARNINGS_DIR="$TARGET_PATH/.learnings"

if [ "$DRY_RUN" = true ]; then
    log_info "Dry run - would create:"
    echo "  $LEARNINGS_DIR/"
    echo "  $LEARNINGS_DIR/LEARNINGS.md (from LEARNINGS-TEMPLATE.md, placeholders)"
    echo "  $LEARNINGS_DIR/ERRORS.md (from ERRORS-TEMPLATE.md, placeholders)"
    echo "  $LEARNINGS_DIR/FEATURE_REQUESTS.md (from FEATURE_REQUESTS-TEMPLATE.md, placeholders)"
    echo "  $TARGET_PATH/DOMAIN-CONFIG-DRAFT.md (from DOMAIN-CONFIG-TEMPLATE.md)"
    echo "  $TARGET_PATH/EVOLUTION.md (from EVOLUTION-RULES-TEMPLATE.md, placeholders)"
    echo ""
    log_info "Agent should: 1) Read SKILL.md 2) Deep analysis 3) Fill DOMAIN-CONFIG-DRAFT.md 4) Replace placeholders"
    exit 0
fi

# Create .learnings/
log_info "Creating $LEARNINGS_DIR/"
mkdir -p "$LEARNINGS_DIR"

# Copy templates with generic placeholders (agent fills domain-specific values later)
log_info "Creating LEARNINGS.md, ERRORS.md, FEATURE_REQUESTS.md"
cp "$ASSETS_DIR/LEARNINGS-TEMPLATE.md" "$LEARNINGS_DIR/LEARNINGS.md"
cp "$ASSETS_DIR/ERRORS-TEMPLATE.md" "$LEARNINGS_DIR/ERRORS.md"
cp "$ASSETS_DIR/FEATURE_REQUESTS-TEMPLATE.md" "$LEARNINGS_DIR/FEATURE_REQUESTS.md"

# Create DOMAIN-CONFIG-DRAFT.md for agent to fill
SKILL_NAME=$(basename "$TARGET_PATH")
sed "s/\[skill-name\]/$SKILL_NAME/g" "$ASSETS_DIR/DOMAIN-CONFIG-TEMPLATE.md" > "$TARGET_PATH/DOMAIN-CONFIG-DRAFT.md"
log_info "Created DOMAIN-CONFIG-DRAFT.md (agent should fill this)"

# Create EVOLUTION.md with placeholders
cp "$ASSETS_DIR/EVOLUTION-RULES-TEMPLATE.md" "$TARGET_PATH/EVOLUTION.md"
log_info "Created EVOLUTION.md (agent should replace placeholders)"

echo ""
log_info "Scaffold created successfully!"
echo ""
echo "Next steps:"
echo "  1. Read $TARGET_PATH/SKILL.md and perform deep capability & scenario analysis"
echo "  2. Fill $TARGET_PATH/DOMAIN-CONFIG-DRAFT.md with extracted domain config"
echo "  3. Replace placeholders in .learnings/*.md and EVOLUTION.md using the domain config"
echo "  4. Ensure language of generated files matches target skill's user language"
echo "  5. Add Review→Apply→Report and OpenClaw feedback rules (see references/openclaw-feedback.md)"
