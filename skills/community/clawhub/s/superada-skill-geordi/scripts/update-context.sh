#!/bin/bash
# update-context.sh — Update project context after Geordi builds
# Usage: update-context.sh <project-path> "Summary of changes"
# Usage: update-context.sh <project-path> --init  (create from template)

set -euo pipefail

PROJECT_PATH="${1:?Usage: update-context.sh <project-path> \"changes summary\"}"
PROJECT_PATH="${PROJECT_PATH/#\~/$HOME}"
ACTION="${2:?Usage: update-context.sh <project-path> \"changes summary\" OR --init}"

PROJECT_NAME=$(basename "$PROJECT_PATH")
MEMORY_DIR="$HOME/clawd/memory"
DATE=$(date '+%Y-%m-%d')
TIMESTAMP=$(date '+%Y-%m-%d %H:%M UTC')

# --- Find existing context file ---
CONTEXT_FILE=""
if [ -f "$PROJECT_PATH/CONTEXT.md" ]; then
  CONTEXT_FILE="$PROJECT_PATH/CONTEXT.md"
elif [ "$PROJECT_NAME" = "entity" ] && [ -f "$MEMORY_DIR/entity-project-context.md" ]; then
  CONTEXT_FILE="$MEMORY_DIR/entity-project-context.md"
elif [ -f "$MEMORY_DIR/${PROJECT_NAME}-context.md" ]; then
  CONTEXT_FILE="$MEMORY_DIR/${PROJECT_NAME}-context.md"
elif [ -f "$MEMORY_DIR/${PROJECT_NAME}-project-context.md" ]; then
  CONTEXT_FILE="$MEMORY_DIR/${PROJECT_NAME}-project-context.md"
elif [ -f "$MEMORY_DIR/projects/${PROJECT_NAME}/context.md" ]; then
  CONTEXT_FILE="$MEMORY_DIR/projects/${PROJECT_NAME}/context.md"
fi

# --- Init mode: create context file from template ---
if [ "$ACTION" = "--init" ]; then
  if [ -n "$CONTEXT_FILE" ]; then
    echo "⚠️  Context file already exists: $CONTEXT_FILE" >&2
    echo "  Use update-context.sh $PROJECT_PATH \"changes\" to update it." >&2
    exit 0
  fi

  CONTEXT_FILE="$PROJECT_PATH/CONTEXT.md"
  
  # Auto-detect tech stack
  TECH_STACK=""
  [ -f "$PROJECT_PATH/package.json" ] && TECH_STACK="Node.js"
  [ -f "$PROJECT_PATH/tsconfig.json" ] && TECH_STACK="$TECH_STACK, TypeScript"
  [ -f "$PROJECT_PATH/vite.config.ts" ] && TECH_STACK="$TECH_STACK, Vite"
  [ -d "$PROJECT_PATH/packages" ] && TECH_STACK="$TECH_STACK, Monorepo"

  cat > "$CONTEXT_FILE" << EOF
# ${PROJECT_NAME} - Project Context

## Overview
TODO: Add project description

## Tech Stack
${TECH_STACK:-TODO: Add tech stack}

## Key Files
TODO: Add key files and their purposes

## Architecture
TODO: Add architecture notes

## Known Issues
None documented yet.

## Recent Updates

### $DATE
- Context file created

*Last updated: $TIMESTAMP*
EOF

  echo "✅ Created context file: $CONTEXT_FILE" >&2
  echo "  Edit it to add project details." >&2
  exit 0
fi

# --- Update mode: append changes to Recent Updates ---
if [ -z "$CONTEXT_FILE" ]; then
  echo "❌ No context file found. Run: update-context.sh $PROJECT_PATH --init" >&2
  exit 1
fi

CHANGES="$ACTION"

# Check if today's date section already exists
if grep -q "### $DATE" "$CONTEXT_FILE" 2>/dev/null; then
  # Append to existing date section (before the next ### or *Last updated*)
  # Use python for reliable multi-line editing
  python3 -c "
import sys
content = open('$CONTEXT_FILE').read()
marker = '### $DATE'
idx = content.index(marker) + len(marker)
# Find end of line after marker
nl = content.index('\n', idx)
# Insert after the date header line
changes = '\n- $CHANGES'
content = content[:nl] + changes + content[nl:]
# Update last updated timestamp
import re
content = re.sub(r'\*Last updated:.*?\*', '*Last updated: $TIMESTAMP*', content)
open('$CONTEXT_FILE', 'w').write(content)
" 2>/dev/null
else
  # Add new date section before *Last updated*
  if grep -q '\*Last updated:' "$CONTEXT_FILE" 2>/dev/null; then
    python3 -c "
import re
content = open('$CONTEXT_FILE').read()
update_line = re.search(r'\*Last updated:.*?\*', content)
if update_line:
    insert_pos = update_line.start()
    new_section = '### $DATE\n- $CHANGES\n\n'
    content = content[:insert_pos] + new_section + '*Last updated: $TIMESTAMP*\n'
    open('$CONTEXT_FILE', 'w').write(content)
" 2>/dev/null
  else
    # No Last updated line, just append
    echo "" >> "$CONTEXT_FILE"
    echo "### $DATE" >> "$CONTEXT_FILE"
    echo "- $CHANGES" >> "$CONTEXT_FILE"
    echo "" >> "$CONTEXT_FILE"
    echo "*Last updated: $TIMESTAMP*" >> "$CONTEXT_FILE"
  fi
fi

echo "✅ Updated context: $CONTEXT_FILE" >&2
echo "  Added: $CHANGES" >&2
