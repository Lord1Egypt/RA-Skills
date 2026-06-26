#!/bin/bash
# AI Skill Extraction Helper
# Creates a new skill from an AI/LLM learning entry
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

Create a new AI/LLM skill from a learning entry.

Arguments:
  skill-name     Name of the skill (lowercase, hyphens for spaces)

Options:
  --dry-run      Show what would be created without creating files
  --output-dir   Relative output directory under current path (default: ./skills)
  -h, --help     Show this help message

Examples:
  $(basename "$0") code-gen-model-selection
  $(basename "$0") rag-chunk-sizing --dry-run
  $(basename "$0") lost-in-the-middle-fix --output-dir ./skills/ai

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
    log_error "Examples: 'code-gen-model-selection', 'rag-chunk-sizing', 'lost-in-the-middle-fix'"
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
description: "[TODO: Describe the model behavior, prompt pattern, or inference optimization this skill addresses]"
---

# $(echo "$SKILL_NAME" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2))}1')

[TODO: Brief introduction — what AI/model problem this solves]

## Quick Reference

| Situation | Action |
|-----------|--------|
| [Model/inference trigger] | [Config change, prompt fix, or model swap] |

## The Problem

[TODO: Describe the model behavior, quality issue, or pipeline failure]

## Solution

[TODO: Updated config, prompt pattern, model swap, or pipeline change]

## Model Compatibility Matrix

| Model | Provider | Version | Tested | Result |
|-------|----------|---------|--------|--------|
| [TODO] | [TODO] | [TODO] | [TODO] | [TODO] |

## Benchmark Results

| Metric | Before | After | Delta |
|--------|--------|-------|-------|
| Quality (eval score) | [TODO] | [TODO] | [TODO] |
| Latency (P50/P99) | [TODO] | [TODO] | [TODO] |
| Cost (per 1K requests) | [TODO] | [TODO] | [TODO] |

## Configuration

\`\`\`json
{
  "model": "[TODO: model name]",
  "temperature": 0.1,
  "top_p": 0.95,
  "max_tokens": 4096
}
\`\`\`

## Source

- Learning ID: [TODO: Add original learning ID]
- Category: [TODO: model_selection | prompt_optimization | inference_latency | fine_tune_regression | context_management | modality_gap | hallucination_rate | cost_efficiency]
- Area: [TODO: model_config | prompt_engineering | fine_tuning | rag_pipeline | inference | embeddings | multimodal | evaluation | guardrails]
- Original File: .learnings/LEARNINGS.md or .learnings/MODEL_ISSUES.md
TEMPLATE
    echo "---"
    exit 0
fi

log_info "Creating AI skill: $SKILL_NAME"

mkdir -p "$SKILL_PATH"

cat > "$SKILL_PATH/SKILL.md" << TEMPLATE
---
name: $SKILL_NAME
description: "[TODO: Describe the model behavior, prompt pattern, or inference optimization this skill addresses]"
---

# $(echo "$SKILL_NAME" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2))}1')

[TODO: Brief introduction — what AI/model problem this solves]

## Quick Reference

| Situation | Action |
|-----------|--------|
| [Model/inference trigger] | [Config change, prompt fix, or model swap] |

## The Problem

[TODO: Describe the model behavior, quality issue, or pipeline failure]

## Solution

[TODO: Updated config, prompt pattern, model swap, or pipeline change]

## Model Compatibility Matrix

| Model | Provider | Version | Tested | Result |
|-------|----------|---------|--------|--------|
| [TODO] | [TODO] | [TODO] | [TODO] | [TODO] |

## Benchmark Results

| Metric | Before | After | Delta |
|--------|--------|-------|-------|
| Quality (eval score) | [TODO] | [TODO] | [TODO] |
| Latency (P50/P99) | [TODO] | [TODO] | [TODO] |
| Cost (per 1K requests) | [TODO] | [TODO] | [TODO] |

## Configuration

\`\`\`json
{
  "model": "[TODO: model name]",
  "temperature": 0.1,
  "top_p": 0.95,
  "max_tokens": 4096
}
\`\`\`

## Source

- Learning ID: [TODO: Add original learning ID]
- Category: [TODO: model_selection | prompt_optimization | inference_latency | fine_tune_regression | context_management | modality_gap | hallucination_rate | cost_efficiency]
- Area: [TODO: model_config | prompt_engineering | fine_tuning | rag_pipeline | inference | embeddings | multimodal | evaluation | guardrails]
- Original File: .learnings/LEARNINGS.md or .learnings/MODEL_ISSUES.md
TEMPLATE

log_info "Created: $SKILL_PATH/SKILL.md"

echo ""
log_info "Skill scaffold created."
echo ""
echo "Next steps:"
echo "  1. Edit $SKILL_PATH/SKILL.md"
echo "  2. Fill in the TODO sections with model/config details from your learning"
echo "  3. Add model compatibility matrix (which models/providers were tested)"
echo "  4. Add benchmark results (before/after metrics)"
echo "  5. Add references/ folder if you have eval data or detailed docs"
echo "  6. Update the original learning entry with:"
echo "     **Status**: promoted_to_skill"
echo "     **Skill-Path**: skills/$SKILL_NAME"
