#!/bin/bash
# Test weather analysis for multiple cities

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
SCRIPT="$SCRIPT_DIR/weather_analysis.py"

# Function to test a city with retry
test_city() {
    local city="$1"
    local lang="${2:-en}"
    local retry=0
    local max_retries=2
    
    echo "Testing: $city (lang: $lang)"
    
    while [ $retry -lt $max_retries ]; do
        result=$(curl -s --max-time 15 "wttr.in/$city?format=j1" 2>&1)
        
        if [ $? -eq 0 ] && [ -n "$result" ]; then
            echo "$result" | python3 "$SCRIPT" "$city" --lang "$lang" 2>&1
            return 0
        fi
        
        retry=$((retry + 1))
        if [ $retry -lt $max_retries ]; then
            sleep 1
        fi
    done
    
    echo "Error: Failed to fetch data for $city after $max_retries attempts"
    return 1
}

# Test cities by country (English output)
echo "========================================="
echo "Testing China Cities (English)"
echo "========================================="
for city in Beijing Shanghai Guangzhou Shenzhen Chengdu; do
    test_city "$city" "en"
    echo ""
done

echo "========================================="
echo "Testing Japan Cities (English)"
echo "========================================="
for city in Tokyo Osaka Kyoto Yokohama; do
    test_city "$city" "en"
    echo ""
done

echo "========================================="
echo "Testing US Cities (English)"
echo "========================================="
for city in "New+York" "Los+Angeles" "San+Francisco" Seattle Miami; do
    test_city "$city" "en"
    echo ""
done

echo "========================================="
echo "Testing Canada Cities (English)"
echo "========================================="
for city in Toronto Vancouver Montreal Calgary; do
    test_city "$city" "en"
    echo ""
done

echo "========================================="
echo "Testing UK Cities (English)"
echo "========================================="
for city in London Manchester Edinburgh Birmingham; do
    test_city "$city" "en"
    echo ""
done

# Test Chinese output
echo "========================================="
echo "Testing Chinese Output"
echo "========================================="
for city in Beijing Shanghai Tokyo; do
    test_city "$city" "zh"
    echo ""
done

echo "========================================="
echo "All tests completed"
echo "========================================="
