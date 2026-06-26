#!/bin/bash
# Create daily work log file

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
TEMPLATE_FILE="$SCRIPT_DIR/daily_log_template.md"
LOG_DIR="$SCRIPT_DIR/daily_logs"

# Create logs directory if it doesn't exist
mkdir -p "$LOG_DIR"

# Get today's date
TODAY=$(date +%Y-%m-%d)
LOG_FILE="$LOG_DIR/$TODAY.md"

# Check if log file already exists
if [[ -f "$LOG_FILE" ]]; then
    echo "📁 Daily log for $TODAY already exists: $LOG_FILE"
    echo "Opening in editor..."
    ${EDITOR:-nano} "$LOG_FILE"
    exit 0
fi

# Create log file from template
echo "📝 Creating daily log for $TODAY..."
cp "$TEMPLATE_FILE" "$LOG_FILE"

# Replace template variables
sed -i '' "s/{{DATE}}/$TODAY/g" "$LOG_FILE"
sed -i '' "s/{{MORNING_START}}/9:00/g" "$LOG_FILE"
sed -i '' "s/{{MORNING_END}}/12:00/g" "$LOG_FILE"
sed -i '' "s/{{AFTERNOON_START}}/13:00/g" "$LOG_FILE"
sed -i '' "s/{{AFTERNOON_END}}/17:00/g" "$LOG_FILE"

echo "✅ Created daily log: $LOG_FILE"
echo ""
echo "Next steps:"
echo "1. Edit the log file: ${EDITOR:-nano} '$LOG_FILE'"
echo "2. Use './jira_log.sh log' to log work to Jira"
echo "3. Check off items as you complete them"
echo ""
echo "Opening log file..."
${EDITOR:-nano} "$LOG_FILE"