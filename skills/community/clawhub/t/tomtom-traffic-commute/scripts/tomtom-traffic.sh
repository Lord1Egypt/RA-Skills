#!/usr/bin/env bash
# TomTom Traffic helper
# Get commute times via TomTom Routing API
#
# Usage:
#   ./scripts/tomtom-traffic.sh <origin-lat,origin-lon> <dest-lat,dest-lon> [departure-time]
#
# Examples:
#   ./scripts/tomtom-traffic.sh "51.5081,-0.0753" "50.8213,-0.1325"
#   ./scripts/tomtom-traffic.sh "50.8213,-0.1325" "51.5081,-0.0753" "2026-06-09T06:45:00+01:00"
#
# Environment: TOMTOM_API_KEY (required)

if [ -z "$TOMTOM_API_KEY" ]; then
  echo '{"error": "TOMTOM_API_KEY not set. Get a free key at https://developer.tomtom.com/"}'
  exit 1
fi

API_KEY="$TOMTOM_API_KEY"
ORIGIN="$1"
DEST="$2"
DEPARTURE="${3:-now}"

if [ -z "$ORIGIN" ] || [ -z "$DEST" ]; then
  echo "Usage: $0 <origin-lat,origin-lon> <dest-lat,dest-lon> [departure-time]"
  echo ""
  echo "Example:"
  echo "  TOMTOM_API_KEY=yourkey $0 '51.5081,-0.0753' '50.8213,-0.1325'"
  echo "  TOMTOM_API_KEY=yourkey $0 '51.5081,-0.0753' '50.8213,-0.1325' '2026-06-09T06:45:00+01:00'"
  exit 1
fi

if [ "$DEPARTURE" = "now" ]; then
  DEPART_PARAM=""
else
  DEPART_PARAM="&departAt=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$DEPARTURE', safe=''))")"
fi

URL="https://api.tomtom.com/routing/1/calculateRoute/${ORIGIN}:${DEST}/json?key=${API_KEY}&traffic=true&routeType=fastest${DEPART_PARAM}"

RESPONSE=$(curl -s "$URL")

python3 -c "
import sys, json
try:
    data = json.loads(sys.stdin.read())
    route = data['routes'][0]['summary']
    dist_km = route['lengthInMeters'] / 1000
    travel_min = route['travelTimeInSeconds'] / 60
    delay_min = route['trafficDelayInSeconds'] / 60
    traffic_km = route['trafficLengthInMeters'] / 1000
    depart = route.get('departureTime', 'now')
    arrive = route.get('arrivalTime', 'N/A')

    print(json.dumps({
        'distance_km': round(dist_km, 1),
        'travel_time_min': round(travel_min),
        'traffic_delay_min': round(delay_min),
        'traffic_affected_km': round(traffic_km, 1),
        'departure_time': depart,
        'arrival_time': arrive,
        'summary': f'{round(dist_km, 1)} km, {round(travel_min)} min (delay: {round(delay_min)} min)'
    }, indent=2))
except Exception as e:
    print(json.dumps({'error': str(e), 'hint': 'Check your API key and coordinates'}))
" <<< "$RESPONSE"
