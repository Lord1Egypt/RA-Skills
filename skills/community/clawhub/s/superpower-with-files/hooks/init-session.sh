#!/bin/bash
# Initialize planning files for a new session in the branded SPF directory
# Usage: ./init-session.sh [project-name] [target-dir]

set -e

PROJECT_NAME="${1:-project}"
if [ -n "$2" ]; then
    # If a target directory is provided, we assume it's a parent folder (like ~/projects)
    # and create a subfolder for the project.
    TARGET_DIR="$2/$PROJECT_NAME"
else
    # Default to the branded SPF folder in the current directory
    TARGET_DIR=".superpower-with-files"
fi
DATE=$(date +%Y-%m-%d)

echo "Initializing SPF planning files for: $PROJECT_NAME in $TARGET_DIR/"

mkdir -p "$TARGET_DIR"

# Create task_plan.md if it doesn't exist
if [ ! -f "$TARGET_DIR/task_plan.md" ]; then
    cat > "$TARGET_DIR/task_plan.md" << 'EOF'
# Task Plan: [Brief Description]

## Goal
[One sentence describing the end state]

## Current Phase
Phase 1

## Phases

### Phase 1: Requirements & Discovery
- [ ] Understand user intent
- [ ] Identify constraints
- [ ] Document in findings.md
- **Status:** in_progress

### Phase 2: Planning & Structure
- [ ] Define approach
- [ ] Create project structure
- **Status:** pending

### Phase 3: Implementation
- [ ] Execute the plan
- [ ] Write to files before executing
- **Status:** pending

### Phase 4: Testing & Verification
- [ ] Verify requirements met
- [ ] Document test results
- **Status:** pending

### Phase 5: Delivery
- [ ] Review outputs
- [ ] Deliver to user
- **Status:** pending

## Decisions Made
| Decision | Rationale |
|----------|-----------|

## Errors Encountered
| Error | Resolution |
|-------|------------|

---
*Last Updated: YYYY-MM-DD HH:MM UTC*
EOF
    # Update timestamp
    sed -i "s/YYYY-MM-DD HH:MM/$(date -u +'%Y-%m-%d %H:%M')/" "$TARGET_DIR/task_plan.md"
    echo "Created $TARGET_DIR/task_plan.md"
else
    echo "task_plan.md already exists, skipping"
fi

# Create findings.md if it doesn't exist
if [ ! -f "$TARGET_DIR/findings.md" ]; then
    cat > "$TARGET_DIR/findings.md" << 'EOF'
# Findings & Decisions

## Requirements
-

## Research Findings
-

## Technical Decisions
| Decision | Rationale |
|----------|-----------|

## Issues Encountered
| Issue | Resolution |
|-------|------------|

## Resources
-

---
*Last Updated: YYYY-MM-DD HH:MM UTC*
EOF
    sed -i "s/YYYY-MM-DD HH:MM/$(date -u +'%Y-%m-%d %H:%M')/" "$TARGET_DIR/findings.md"
    echo "Created $TARGET_DIR/findings.md"
else
    echo "findings.md already exists, skipping"
fi

# Create progress.md if it doesn't exist
if [ ! -f "$TARGET_DIR/progress.md" ]; then
    cat > "$TARGET_DIR/progress.md" << EOF
# Progress Log

## Session: $DATE

### Current Status
- **Phase:** 1 - Requirements & Discovery
- **Started:** $DATE

### Actions Taken
-

### Test Results
| Test | Expected | Actual | Status |
|------|----------|--------|--------|

### Errors
| Error | Resolution |
|-------|------------|

---
*Last Updated: $DATE $(date -u +'%H:%M') UTC*
EOF
    echo "Created $TARGET_DIR/progress.md"
else
    echo "progress.md already exists, skipping"
fi

echo ""
echo "SPF Planning files initialized!"
echo "Location: $TARGET_DIR/"
echo "Files: task_plan.md, findings.md, progress.md"
