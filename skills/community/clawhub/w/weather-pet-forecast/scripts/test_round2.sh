#!/bin/bash
# Test weather analysis with retry mechanism

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SCRIPT="$SCRIPT_DIR/weather_analysis.py"

test_city_with_retry() {
    local city="$1"
    local lang="${2:-en}"
    local max_retries=3
    local retry=0
    local result=""
    
    while [ $retry -lt $max_retries ]; do
        result=$(curl -s --max-time 20 --retry 2 --retry-delay 3 "wttr.in/$city?format=j1" 2>&1)
        
        if [ $? -eq 0 ] && [ -n "$result" ] && echo "$result" | python3 -c "import sys, json; json.load(sys.stdin)" 2>/dev/null; then
            echo "$result" | python3 "$SCRIPT" "$city" --lang "$lang"
            return 0
        fi
        
        retry=$((retry + 1))
        if [ $retry -lt $max_retries ]; then
            echo "   Retrying... ($retry/$max_retries)"
            sleep 2
        fi
    done
    
    echo "Error: Failed to fetch weather data for $city after $max_retries attempts"
    return 1
}

echo "========================================"
echo "Weather Analysis Round 2 Test"
echo "========================================"
echo ""

# Test cities that may have failed in round 1
test_cities=(
    "Beijing"
    "Osaka"
    "Kyoto"
    "New+York"
    "Los+Angeles"
    "Chicago"
    "Toronto"
    "Vancouver"
    "London"
    "Manchester"
    "Edinburgh"
)

for city in "${test_cities[@]}"; do
    echo "Testing: $city"
    echo "---"
    test_city_with_retry "$city" "en"
    echo ""
    sleep 3
done

echo "========================================"
echo "Round 2 Test Complete"
echo "========================================"
