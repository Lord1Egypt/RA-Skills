#!/bin/bash
# Tavily Search — thin wrapper around the REST API.
# Accepts the full API payload as raw JSON via --json.
#
# Usage: ./search.sh --json '{"query": "your search query", ...}'

set -e

# --- check API key -----------------------------------------------------
if [ -z "$TAVILY_API_KEY" ]; then
    echo "Error: TAVILY_API_KEY not set. Export it as an environment variable." >&2
    exit 1
fi

# --- parse arguments ----------------------------------------------------
JSON_INPUT=""

while [ $# -gt 0 ]; do
    case "$1" in
        --json)
            shift
            JSON_INPUT="$1"
            ;;
        *)
            # bare arg (no flag) — treat as JSON for back-compat
            if [ -z "$JSON_INPUT" ]; then
                JSON_INPUT="$1"
            fi
            ;;
    esac
    shift
done

if [ -z "$JSON_INPUT" ]; then
    echo "Usage: ./search.sh --json '<json>'"
    echo ""
    echo "The JSON body is sent directly to POST https://api.tavily.com/search"
    echo ""
    echo "Required fields:"
    echo "  query: string - Search query (keep under 400 chars)"
    echo ""
    echo "Optional fields:"
    echo "  max_results:               0-20 (default: 10)"
    echo "  search_depth:              \"basic\" (default), \"advanced\""
    echo "  time_range:                \"day\", \"week\", \"month\", \"year\""
    echo "  start_date / end_date:     \"YYYY-MM-DD\""
    echo "  include_domains:           [\"domain1.com\", ...]"
    echo "  exclude_domains:           [\"domain1.com\", ...]"
    echo "  country:                   country name (general topic only)"
    echo "  include_raw_content:       true/false"
    echo "  include_images:            true/false"
    echo "  include_image_descriptions: true/false"
    echo "  include_favicon:           true/false"
    echo ""
    echo "Example:"
    echo "  ./search.sh --json '{\"query\": \"latest AI trends\", \"time_range\": \"week\"}'"
    exit 1
fi

# --- call Tavily REST API -----------------------------------------------
printf '%s' "$JSON_INPUT" | curl -s --request POST \
    --url "https://api.tavily.com/search" \
    --header "Authorization: Bearer $TAVILY_API_KEY" \
    --header 'Content-Type: application/json' \
    --data @-
