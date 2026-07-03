#!/bin/bash
# generate-readme.sh — Generate a README.md for a skill folder
# Usage: generate-readme.sh <skill-dir> <skill-name> <description>
set -euo pipefail

SKILL_DIR="$1"
SKILL_NAME="$2"
DESCRIPTION="${3:-A skill for OpenClaw/Clawdbot agents.}"

# Try to extract description from SKILL.md if it exists
if [[ -f "$SKILL_DIR/SKILL.md" ]]; then
  SKILL_DESC=$(grep -A1 "^description:" "$SKILL_DIR/SKILL.md" 2>/dev/null | head -1 | sed 's/^description: *//' || echo "")
  if [[ -n "$SKILL_DESC" && "$DESCRIPTION" == "A skill for OpenClaw/Clawdbot agents." ]]; then
    DESCRIPTION="$SKILL_DESC"
  fi
fi

# Detect main script files
SCRIPTS=""
if [[ -d "$SKILL_DIR/scripts" ]]; then
  SCRIPTS=$(find "$SKILL_DIR/scripts" -type f -executable -o -name "*.sh" -o -name "*.mjs" -o -name "*.js" -o -name "*.py" 2>/dev/null | sort)
fi

# Detect if there's a SKILL.md (agent instructions)
HAS_SKILL_MD="no"
[[ -f "$SKILL_DIR/SKILL.md" ]] && HAS_SKILL_MD="yes"

# Build README
cat > "$SKILL_DIR/README.md" << READMEEOF
# ${SKILL_NAME}

${DESCRIPTION}

## Structure

\`\`\`
${SKILL_NAME}/
READMEEOF

# Add file tree
find "$SKILL_DIR" -type f | sed "s|$SKILL_DIR/||" | sort | while read -r f; do
  echo "├── $f" >> "$SKILL_DIR/README.md"
done

cat >> "$SKILL_DIR/README.md" << 'READMEEOF'
```

READMEEOF

# Add scripts section if scripts exist
if [[ -n "$SCRIPTS" ]]; then
  echo "## Scripts" >> "$SKILL_DIR/README.md"
  echo "" >> "$SKILL_DIR/README.md"
  while IFS= read -r script; do
    script_name=$(basename "$script")
    echo "- \`$script_name\` — $(head -2 "$script" | grep -oP '(?<=#\s).*' | head -1 || echo "Script")" >> "$SKILL_DIR/README.md"
  done <<< "$SCRIPTS"
  echo "" >> "$SKILL_DIR/README.md"
fi

# Add agent instructions note
if [[ "$HAS_SKILL_MD" == "yes" ]]; then
  cat >> "$SKILL_DIR/README.md" << 'READMEEOF'
## Agent Instructions

This skill includes a `SKILL.md` file with instructions for AI agents on how to use it. If you're running [OpenClaw](https://github.com/openclaw/openclaw), drop this folder into your skills directory and it will be auto-detected.

READMEEOF
fi

# Add requirements
cat >> "$SKILL_DIR/README.md" << 'READMEEOF'
## Requirements

- [OpenClaw](https://github.com/openclaw/openclaw) or compatible AI agent framework
- Node.js 18+ (for JavaScript-based scripts)

## License

MIT
READMEEOF

echo "✅ Generated README.md for $SKILL_NAME"
