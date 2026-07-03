#!/bin/bash
# Create a PRD (Product Requirements Document) for a feature
# Usage: ./create-prd.sh "Feature description"

set -e

DESCRIPTION="$1"
if [ -z "$DESCRIPTION" ]; then
  echo "Usage: ./create-prd.sh \"Feature description\""
  exit 1
fi

# Generate filename from description
SLUG=$(echo "$DESCRIPTION" | tr '[:upper:]' '[:lower:]' | tr ' ' '-' | tr -cd 'a-z0-9-' | cut -c1-50)
DATE=$(date +%Y-%m-%d)
FILENAME="prd-${SLUG}.md"

mkdir -p tasks

cat > "tasks/$FILENAME" << EOF
# PRD: $DESCRIPTION

**Date:** $DATE
**Author:** Ada (via Ralph skill)
**Status:** Draft

## Overview

$DESCRIPTION

## Goals

- [ ] Goal 1
- [ ] Goal 2
- [ ] Goal 3

## User Stories

### Story 1: [Title]
**Priority:** 1
**Description:** 
**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2

### Story 2: [Title]
**Priority:** 2
**Description:**
**Acceptance Criteria:**
- [ ] Criterion 1
- [ ] Criterion 2

## Technical Notes

- 

## Out of Scope

- 

## Open Questions

- 
EOF

echo "✅ Created: tasks/$FILENAME"
echo ""
echo "Next steps:"
echo "1. Edit tasks/$FILENAME with detailed requirements"
echo "2. Convert to prd.json: ~/agent-workspace/skills/ralph/scripts/convert-prd.sh tasks/$FILENAME"
