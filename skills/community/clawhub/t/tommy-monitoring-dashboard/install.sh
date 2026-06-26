#!/bin/bash

# Live Monitoring Dashboard Installation Script
# Zero-Token Real-time OpenClaw Monitoring

set -e

echo "🚀 Installing Live Monitoring Dashboard (Zero Token Edition)..."

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_DIR="$SKILL_DIR/config"
DATA_DIR="$SKILL_DIR/data"
SCRIPTS_DIR="$SKILL_DIR/scripts"

# Create necessary directories
echo "📁 Creating directory structure..."
mkdir -p "$CONFIG_DIR"
mkdir -p "$DATA_DIR/performance"
mkdir -p "$SCRIPTS_DIR"

# Make scripts executable
echo "🔧 Setting up executable permissions..."
chmod +x "$SCRIPTS_DIR/zero-token-dashboard.sh"
chmod +x "$SCRIPTS_DIR/performance-tracker.sh"

# Initialize performance configuration
PERF_CONFIG="$CONFIG_DIR/performance-config.json"
if [[ ! -f "$PERF_CONFIG" ]]; then
    echo "⚙️ Creating performance configuration..."
    cat > "$PERF_CONFIG" << EOF
{
    "cpu_warning": 70,
    "cpu_critical": 85,
    "mem_warning": 75,
    "mem_critical": 90,
    "disk_warning": 80,
    "disk_critical": 95,
    "retention_days": 7
}
EOF
fi

# Initialize live state file
LIVE_STATE="$CONFIG_DIR/live-state.json"
if [[ ! -f "$LIVE_STATE" ]]; then
    echo "📊 Creating live state file..."
    cat > "$LIVE_STATE" << EOF
{
    "activity_message_id": "",
    "health_message_id": "",
    "channel_id": "",
    "last_update": 0,
    "initialized": false
}
EOF
fi

# Check system requirements
echo "🔍 Checking system requirements..."

# Check for jq
if ! command -v jq &> /dev/null; then
    echo "⚠️  Warning: jq not found. Install with: brew install jq"
    echo "   Performance configuration parsing may fail without jq"
fi

# Check for bc  
if ! command -v bc &> /dev/null; then
    echo "⚠️  Warning: bc not found. Install with: brew install bc"
    echo "   Mathematical calculations may fail without bc"
fi

# Check for basic utilities
REQUIRED_COMMANDS=("ps" "top" "uptime" "df" "openclaw")
MISSING_COMMANDS=()

for cmd in "${REQUIRED_COMMANDS[@]}"; do
    if ! command -v "$cmd" &> /dev/null; then
        MISSING_COMMANDS+=("$cmd")
    fi
done

if [[ ${#MISSING_COMMANDS[@]} -gt 0 ]]; then
    echo "❌ Missing required commands: ${MISSING_COMMANDS[*]}"
    echo "   Please install missing dependencies before running the dashboard"
    exit 1
fi

# Test OpenClaw message command
echo "🧪 Testing OpenClaw integration..."
if ! openclaw message --help &> /dev/null; then
    echo "⚠️  Warning: OpenClaw message command not available"
    echo "   Discord integration may not function properly"
fi

# Create a test cron job for the dashboard (user can modify as needed)
echo "⏰ Setting up monitoring cron job..."

CRON_COMMAND="cd $SKILL_DIR && ./scripts/zero-token-dashboard.sh"
CRON_SCHEDULE="every 1m"

echo ""
echo "📝 Manual setup required:"
echo "   1. Create Discord channel for monitoring (e.g., #tommy-monitoring)"
echo "   2. Update message IDs in zero-token-dashboard.sh after initial posts"
echo "   3. Create cron job with command:"
echo "      Schedule: $CRON_SCHEDULE"
echo "      Command: $CRON_COMMAND"
echo "   4. Configure performance alert thresholds in:"
echo "      $PERF_CONFIG"

echo ""
echo "🚀 Installation complete!"
echo ""
echo "📖 Usage:"
echo "   ./scripts/zero-token-dashboard.sh    # Manual dashboard update"
echo "   ./scripts/performance-tracker.sh track    # Log current metrics"
echo "   ./scripts/performance-tracker.sh trends   # View performance trends"
echo "   ./scripts/performance-tracker.sh alerts   # View recent alerts"
echo ""
echo "📊 Features enabled:"
echo "   ✅ Zero-token Discord dashboard"
echo "   ✅ Real-time system monitoring"
echo "   ✅ Performance trend analysis"
echo "   ✅ Smart threshold alerting"
echo "   ✅ Historical data tracking"
echo "   ✅ Automatic cleanup (7-day retention)"
echo ""
echo "🎯 Ready for production monitoring!"