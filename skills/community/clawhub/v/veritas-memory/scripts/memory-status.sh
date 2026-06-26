#!/bin/bash
# Veritas Memory — Check memory system health
set -e

echo "🧠 Veritas Memory Status"
echo "========================"
echo ""

# STATE.md
if [ -f "STATE.md" ]; then
  SIZE=$(wc -c < STATE.md | awk '{print $1}')
  LINES=$(wc -l < STATE.md | awk '{print $1}')
  EVENTS=$(grep -c '^|' STATE.md 2>/dev/null || echo 0)
  echo "✓ STATE.md — $LINES lines, ${SIZE}B, ~$EVENTS events"
else
  echo "✗ STATE.md missing"
fi

# MEMORY.md
if [ -f "MEMORY.md" ]; then
  SIZE=$(wc -c < MEMORY.md | awk '{print $1}')
  LINES=$(wc -l < MEMORY.md | awk '{print $1}')
  echo "✓ MEMORY.md — $LINES lines, ${SIZE}B"
else
  echo "✗ MEMORY.md missing"
fi

# Daily logs
if [ -d "memory" ]; then
  COUNT=$(ls memory/*.md 2>/dev/null | wc -l)
  echo "✓ memory/ — $COUNT daily logs"
  echo ""
  echo "Recent:"
  ls -lt memory/*.md 2>/dev/null | head -5 | while read line; do
    echo "  $(echo $line | awk '{print $6, $7, $8, $NF}')"
  done
else
  echo "✗ memory/ directory missing"
fi

# Sub-directories
echo ""
for dir in knowledge decisions lessons checkpoints archive; do
  if [ -d "memory/$dir" ]; then
    COUNT=$(ls memory/$dir/ 2>/dev/null | wc -l)
    echo "✓ memory/$dir/ — $COUNT files"
  else
    echo "✗ memory/$dir/ missing"
  fi
done

# Session logs (approximate)
echo ""
if [ -d "sessions" ]; then
  COUNT=$(ls sessions/*.jsonl 2>/dev/null | wc -l)
  echo "✓ sessions/ — $COUNT session logs"
else
  echo "• sessions/ not in workspace"
fi

echo ""
echo "Health check complete."
