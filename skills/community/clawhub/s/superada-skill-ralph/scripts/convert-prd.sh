#!/bin/bash
# Convert a PRD markdown file to prd.json for Ralph
# Usage: ./convert-prd.sh <prd.md> [output_dir]

set -e

PRD_FILE="$1"
OUTPUT_DIR="${2:-scripts/ralph}"

if [ -z "$PRD_FILE" ] || [ ! -f "$PRD_FILE" ]; then
  echo "Usage: ./convert-prd.sh <prd.md> [output_dir]"
  echo "Example: ./convert-prd.sh tasks/prd-feature.md scripts/ralph"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

# Extract feature name from filename
FEATURE_NAME=$(basename "$PRD_FILE" .md | sed 's/^prd-//')
BRANCH_NAME="ralph/$FEATURE_NAME"

echo "📄 Converting PRD to prd.json..."
echo "   Source: $PRD_FILE"
echo "   Output: $OUTPUT_DIR/prd.json"
echo "   Branch: $BRANCH_NAME"
echo ""

# Use Codex/Claude to convert (or simple parsing)
# For now, create a template that can be filled in

# Count stories in the PRD (look for ### Story patterns)
STORY_COUNT=$(grep -c "^### Story" "$PRD_FILE" 2>/dev/null || echo "0")

if [ "$STORY_COUNT" -eq 0 ]; then
  echo "⚠️  No stories found (looking for '### Story' headings)"
  echo "   Creating template prd.json - edit manually or use AI to parse"
  
  cat > "$OUTPUT_DIR/prd.json" << EOF
{
  "branchName": "$BRANCH_NAME",
  "feature": "$FEATURE_NAME",
  "userStories": [
    {
      "id": "1",
      "title": "First task",
      "description": "Implement the first part",
      "acceptanceCriteria": [
        "Tests pass",
        "Code is clean"
      ],
      "priority": 1,
      "passes": false
    }
  ]
}
EOF
else
  echo "📝 Found $STORY_COUNT stories"
  
  # Extract stories using awk
  python3 << PYTHON
import re
import json
import sys

with open("$PRD_FILE", 'r') as f:
    content = f.read()

# Find all story sections
story_pattern = r'### Story \d+: (.+?)\n.*?(?:\*\*Priority:\*\*|Priority:)\s*(\d+).*?(?:\*\*Description:\*\*|Description:)\s*(.+?)(?:\*\*Acceptance Criteria:\*\*|Acceptance Criteria:)(.*?)(?=### Story|\Z)'
stories = []
matches = re.findall(story_pattern, content, re.DOTALL | re.IGNORECASE)

for i, match in enumerate(matches, 1):
    title, priority, desc, criteria_text = match
    
    # Parse criteria
    criteria = re.findall(r'- \[.\] (.+)', criteria_text)
    if not criteria:
        criteria = re.findall(r'- (.+)', criteria_text)
    
    stories.append({
        "id": str(i),
        "title": title.strip(),
        "description": desc.strip(),
        "acceptanceCriteria": [c.strip() for c in criteria if c.strip()],
        "priority": int(priority) if priority else i,
        "passes": False
    })

# If no stories found via regex, create placeholder
if not stories:
    stories = [{
        "id": "1",
        "title": "Review and split PRD manually",
        "description": "The PRD needs to be broken into smaller stories",
        "acceptanceCriteria": ["PRD is split into atomic tasks"],
        "priority": 1,
        "passes": False
    }]

prd_json = {
    "branchName": "$BRANCH_NAME",
    "feature": "$FEATURE_NAME", 
    "userStories": stories
}

with open("$OUTPUT_DIR/prd.json", 'w') as f:
    json.dump(prd_json, f, indent=2)

print(f"✅ Created prd.json with {len(stories)} stories")
PYTHON
fi

# Initialize progress file
if [ ! -f "$OUTPUT_DIR/progress.txt" ]; then
  cat > "$OUTPUT_DIR/progress.txt" << EOF
# Ralph Progress Log
Feature: $FEATURE_NAME
Started: $(date)
---
EOF
fi

echo ""
echo "✅ Conversion complete!"
echo ""
echo "Next: Run the Ralph loop:"
echo "   ~/agent-workspace/skills/ralph/scripts/run-ralph.sh $(pwd) 10"
