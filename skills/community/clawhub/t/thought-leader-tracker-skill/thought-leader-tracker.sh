#!/bin/bash

# Thought Leader Tracker
# Daily collection of podcasts, interviews, and videos from thought leaders

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$SCRIPT_DIR/config.json"
OUTPUT_DIR="$SCRIPT_DIR/daily-logs"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print banner
print_banner() {
    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║         Thought Leader Tracker                         ║"
    echo "║         Daily Content Collection System                ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

# Print usage
print_usage() {
    echo "Usage: $0 [command] [options]"
    echo ""
    echo "Commands:"
    echo "  collect [7|30]    Collect content (default: 7 days)"
    echo "  add-person        Add a new thought leader to config"
    echo "  list              List all tracked thought leaders"
    echo "  help              Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 collect        # Collect content from last 7 days"
    echo "  $0 collect 30     # Collect content from last 30 days"
    echo "  $0 list           # Show all tracked people"
    echo ""
}

# List thought leaders
list_leaders() {
    echo -e "${GREEN}Tracked Thought Leaders:${NC}"
    echo ""
    
    if command -v jq &> /dev/null; then
        jq -r '.thoughtLeaders[] | "  • \(.name)\n    Keywords: \(.keywords | join(", "))\n    Platforms: \(.platforms | join(", "))\n"' "$CONFIG_FILE"
    else
        echo "  (Install jq for better formatting)"
        cat "$CONFIG_FILE"
    fi
}

# Add a new thought leader
add_leader() {
    echo -e "${YELLOW}Add New Thought Leader${NC}"
    echo ""
    
    read -p "Name: " name
    read -p "Keywords (comma-separated): " keywords_input
    read -p "Platforms (youtube/apple-podcasts/spotify, comma-separated): " platforms_input
    
    # Convert to arrays
    keywords=$(echo "$keywords_input" | sed 's/,/","/g')
    platforms=$(echo "$platforms_input" | sed 's/,/","/g')
    
    # Create JSON entry
    new_entry=$(cat <<EOF
  {
    "name": "$name",
    "keywords": ["$keywords"],
    "platforms": ["$platforms"]
  }
EOF
)
    
    # Add to config (simple append - in production use proper JSON manipulation)
    echo ""
    echo -e "${GREEN}Entry created:${NC}"
    echo "$new_entry"
    echo ""
    echo -e "${YELLOW}Note: Manual JSON editing recommended for production use${NC}"
    echo "Config file: $CONFIG_FILE"
}

# Run collector
run_collector() {
    local days=${1:-7}
    
    echo -e "${GREEN}Starting content collection...${NC}"
    echo "Time range: Last $days days"
    echo ""
    
    # Ensure output directory exists
    mkdir -p "$OUTPUT_DIR"
    
    # Run Node.js collector
    if command -v node &> /dev/null; then
        node "$SCRIPT_DIR/scripts/collector.js" "$days"
    else
        echo -e "${RED}Error: Node.js is required but not installed${NC}"
        exit 1
    fi
}

# Main
print_banner

case "${1:-help}" in
    collect)
        run_collector "$2"
        ;;
    list)
        list_leaders
        ;;
    add-person|add)
        add_leader
        ;;
    help|--help|-h)
        print_usage
        ;;
    *)
        echo -e "${RED}Unknown command: $1${NC}"
        print_usage
        exit 1
        ;;
esac
