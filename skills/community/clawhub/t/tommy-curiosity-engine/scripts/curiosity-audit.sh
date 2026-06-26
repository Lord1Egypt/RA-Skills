#!/bin/bash
# curiosity-audit.sh — Health check for the Curiosity Engine
# Usage: ./curiosity-audit.sh [curiosity_dir]
# Checks file freshness, queue size, follow-through rate, and engagement ratios.

CURIOSITY_DIR="${1:-workspace/curiosity}"

if [ ! -d "$CURIOSITY_DIR" ]; then
  echo "❌ Curiosity directory not found: $CURIOSITY_DIR"
  exit 1
fi

echo "🔍 Curiosity Engine Health Check"
echo "================================"
echo ""

# File freshness
echo "📁 File Freshness:"
for f in CURIOSITY.md questions.md hits.md competence.md; do
  filepath="$CURIOSITY_DIR/$f"
  if [ -f "$filepath" ]; then
    days_old=$(( ($(date +%s) - $(stat -f %m "$filepath" 2>/dev/null || stat -c %Y "$filepath" 2>/dev/null)) / 86400 ))
    if [ "$days_old" -gt 7 ]; then
      echo "  ⚠️  $f — ${days_old} days old (stale)"
    elif [ "$days_old" -gt 3 ]; then
      echo "  🟡 $f — ${days_old} days old"
    else
      echo "  ✅ $f — ${days_old} days old"
    fi
  else
    echo "  ⬜ $f — not created yet"
  fi
done
echo ""

# Question queue size
if [ -f "$CURIOSITY_DIR/questions.md" ]; then
  active=$(grep -c '^\### \[Q-' "$CURIOSITY_DIR/questions.md" 2>/dev/null || echo 0)
  resolved=$(grep -c '✓' "$CURIOSITY_DIR/questions.md" 2>/dev/null || echo 0)
  total=$((active + resolved))
  echo "❓ Question Queue:"
  echo "  Active: $active (max 30)"
  echo "  Resolved: $resolved"
  if [ "$active" -gt 30 ]; then
    echo "  ⚠️  Over cap! Archive low-interest questions."
  fi
  if [ "$total" -gt 0 ]; then
    rate=$(( resolved * 100 / total ))
    echo "  Follow-through rate: ${rate}% (target: >40%)"
    if [ "$rate" -lt 30 ]; then
      echo "  ⚠️  Low follow-through. Focus on depth, not breadth."
    fi
  fi
else
  echo "❓ Question Queue: not created yet"
fi
echo ""

# Hit log health
if [ -f "$CURIOSITY_DIR/hits.md" ]; then
  extrinsic=$(grep -c '|.*|.*|.*|' "$CURIOSITY_DIR/hits.md" 2>/dev/null || echo 0)
  # Rough count — subtract header rows
  extrinsic=$((extrinsic > 2 ? extrinsic - 2 : 0))
  echo "🎯 Engagement Log:"
  echo "  Entries (approx): $extrinsic"
  if [ "$extrinsic" -eq 0 ]; then
    echo "  ⬜ No hits logged yet. Start exploring!"
  fi
else
  echo "🎯 Engagement Log: not created yet"
fi
echo ""

# Reflection count
if [ -d "$CURIOSITY_DIR/reflections" ]; then
  reflection_count=$(ls "$CURIOSITY_DIR/reflections/"*.md 2>/dev/null | wc -l | tr -d ' ')
  echo "📝 Reflections: $reflection_count"
else
  echo "📝 Reflections: directory not created yet"
fi
echo ""

# Mulling items check
if [ -f "$CURIOSITY_DIR/CURIOSITY.md" ]; then
  mulling=$(grep -c '^\### \[M' "$CURIOSITY_DIR/CURIOSITY.md" 2>/dev/null || echo 0)
  echo "🧠 Mulling items: $mulling (max 3)"
  if [ "$mulling" -gt 3 ]; then
    echo "  ⚠️  Over cap! Prune to top 3."
  fi
else
  echo "🧠 CURIOSITY.md: not created yet"
fi

echo ""
echo "================================"
echo "Done. Run periodically during maintenance heartbeats."
