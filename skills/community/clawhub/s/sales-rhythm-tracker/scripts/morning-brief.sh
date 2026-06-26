#!/bin/bash
# Sales Rhythm Tracker — Morning Brief Generator
# Reads pipeline.md and outputs a prioritized action plan
# Called by OpenClaw agent when user asks for morning brief

SALES_DIR="${HOME}/.openclaw/workspace/sales"
PIPELINE="$SALES_DIR/pipeline.md"
TODAY=$(date +"%Y-%m-%d")
DAY_OF_WEEK=$(date +"%A")

if [ ! -f "$PIPELINE" ]; then
  echo "❌ Pipeline not initialized. Run: init-pipeline.sh first"
  exit 1
fi

# Determine sprint week (cycles reset on 1st of each month)
DAY_OF_MONTH=$(date +"%d")
if [ "$DAY_OF_MONTH" -le 7 ]; then
  SPRINT_WEEK=1
  SPRINT_PHASE="SEED (播种) — Maximize outreach volume today. Target 4+ new contacts."
elif [ "$DAY_OF_MONTH" -le 14 ]; then
  SPRINT_WEEK=2
  SPRINT_PHASE="FLIP (翻牌) — Qualify ruthlessly. Identify your top 30%. Cut the rest."
elif [ "$DAY_OF_MONTH" -le 21 ]; then
  SPRINT_WEEK=3
  SPRINT_PHASE="HARVEST (采果) — Push every qualified lead to YES or NO. No gray zones."
else
  SPRINT_WEEK=4
  SPRINT_PHASE="RESET (机动) — Onboard wins, collect payment, seed next cycle."
fi

echo "============================================"
echo "📊 SALES MORNING BRIEF — $TODAY ($DAY_OF_WEEK)"
echo "Sprint: Week $SPRINT_WEEK | Phase: $SPRINT_PHASE"
echo "============================================"
echo ""
echo "📌 DAILY TARGET (8-Visit Structure):"
echo "   • 4 × New customer outreach (seed)"
echo "   • 2 × Follow-up contacts (nurture)"
echo "   • 2 × Closing push (harvest)"
echo ""
echo "---"
echo "📋 PIPELINE DATA:"
echo ""
cat "$PIPELINE"
echo ""
echo "---"
echo ""
echo "💡 AGENT INSTRUCTIONS:"
echo "Based on the pipeline above, please:"
echo "1. Identify all leads with Last Contact > 7 days → flag 🔴 Red"
echo "2. Identify leads in 'closing' or 'negotiation' stage → top priority"
echo "3. For each priority lead, check their Type (Tiger/Peacock/Koala/Owl)"
echo "   and suggest the right approach script"
echo "4. List top 3-5 actions for today, ordered by urgency score"
echo "5. Identify which leads to SEED today (new outreach)"
echo "6. End with: total active leads, deals at risk, and one this-week close target"
echo ""
echo "Format output as the morning brief structure defined in SKILL.md"
