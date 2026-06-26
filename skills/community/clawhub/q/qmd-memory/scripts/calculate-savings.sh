#!/bin/bash
# QMD Memory Skill — Cost Savings Calculator
# As Above Technologies

echo "╔══════════════════════════════════════════════════════════════════╗"
echo "║            QMD COST SAVINGS CALCULATOR                           ║"
echo "╚══════════════════════════════════════════════════════════════════╝"
echo ""

# Estimate based on typical usage
read -p "How many times do you search memory per day? [50]: " SEARCHES_DAY
SEARCHES_DAY=${SEARCHES_DAY:-50}

read -p "Average cost per API memory call (\$) [0.03]: " COST_PER_CALL
COST_PER_CALL=${COST_PER_CALL:-0.03}

# Calculate
DAILY_COST=$(echo "$SEARCHES_DAY * $COST_PER_CALL" | bc)
MONTHLY_COST=$(echo "$DAILY_COST * 30" | bc)
ANNUAL_COST=$(echo "$MONTHLY_COST * 12" | bc)

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo ""
echo "📊 YOUR CURRENT API MEMORY COSTS (estimated):"
echo ""
printf "   Memory searches per day:     %d\n" $SEARCHES_DAY
printf "   Cost per API call:           \$%.3f\n" $COST_PER_CALL
printf "   Daily API cost:              \$%.2f\n" $DAILY_COST
printf "   Monthly API cost:            \$%.2f\n" $MONTHLY_COST
printf "   Annual API cost:             \$%.2f\n" $ANNUAL_COST
echo ""
echo "════════════════════════════════════════════════════════════════════"
echo ""
echo "🧠 WITH QMD LOCAL:"
echo ""
echo "   Monthly cost:                \$0.00"
echo "   Annual cost:                 \$0.00"
echo ""
echo "════════════════════════════════════════════════════════════════════"
echo ""
printf "💰 YOUR MONTHLY SAVINGS:         \$%.2f\n" $MONTHLY_COST
printf "💰 YOUR ANNUAL SAVINGS:          \$%.2f\n" $ANNUAL_COST
echo ""

# ROI calculation if skill had a price
SKILL_PRICE=20
if (( $(echo "$MONTHLY_COST > 0" | bc -l) )); then
    ROI=$(echo "$ANNUAL_COST / $SKILL_PRICE" | bc)
    printf "📈 ROI (if skill was \$%d):       %dx return\n" $SKILL_PRICE $ROI
fi

echo ""
echo "════════════════════════════════════════════════════════════════════"
echo ""
echo "The math is simple: Stop paying for memory. Start compounding knowledge."
echo ""
echo "Get the full QMD Memory Skill: clawhub install asabove/qmd-memory"
echo ""
