#!/bin/bash
# Weather Query Script - Amap Weather API
# Usage: weather.sh <city_name_or_code> [output_format]

API_KEY="${AMAP_API_KEY:-}"
CITY="$1"
OUTPUT_FORMAT="${2:-json}"

# Check if API key is set
if [ -z "$API_KEY" ]; then
    echo "Error: AMAP_API_KEY environment variable is not set."
    echo "Please set it first: export AMAP_API_KEY='your_api_key_here'"
    exit 1
fi

# Check if city is provided
if [ -z "$CITY" ]; then
    echo "Usage: weather.sh <city_name_or_code> [json|pretty]"
    echo "Examples:"
    echo "  weather.sh BEIJING"
    echo "  weather.sh 110000"
    echo "  weather.sh SHANGHAI pretty"
    exit 1
fi

# Build API URL
API_URL="https://restapi.amap.com/v3/weather/weatherInfo?city=${CITY}&key=${API_KEY}&output=json"

# Make API request
echo "Querying weather for: $CITY"
echo "----------------------------------------"

RESPONSE=$(curl -s "${API_URL}")

# Check if jq is available for pretty printing
if [ "$OUTPUT_FORMAT" = "pretty" ] && command -v jq &> /dev/null; then
    echo "$RESPONSE" | jq '.'
elif [ "$OUTPUT_FORMAT" = "human" ]; then
    # Human-readable output
    echo "$RESPONSE" | jq -r '
        if .status == "1" then
            .lives[0] | "📍 \(.province)\(.city)\n🌤️ Weather: \(.weather)\n🌡️ Temperature: \(.temperature)°C\n💨 Wind: \(.winddirection) \(.windpower)\n💧 Humidity: \(.humidity)%\n📅 Updated: \(.reporttime)"
        else
            "❌ Error: \(.info)"
        end
    ' 2>/dev/null || echo "$RESPONSE"
else
    echo "$RESPONSE"
fi
