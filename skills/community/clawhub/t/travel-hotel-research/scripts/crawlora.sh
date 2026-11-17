#!/usr/bin/env bash
# Crawlora REST helper — minimal, dependency-free (curl only).
# Calls https://api.crawlora.net/api/v1 with your Crawlora API key.
# Get a free key (2,000 credits/mo, no card) at https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills.
#
# Usage:
#   GET  :  crawlora.sh /amazon/search k=laptop s=relevanceblender
#   GET  :  crawlora.sh /youtube/transcript/dQw4w9WgXcQ
#   POST :  crawlora.sh -X POST /google/search '{"keyword":"web scraping api","language":"en","country":"us"}'
#   POST :  crawlora.sh -X POST /google/trends/explore/interest-over-time '{"keywords":["bitcoin"]}'
#
# GET key=value args become the query string. POST takes one JSON body argument
# (or pass it with -d '<json>'). Prints raw JSON to stdout — pipe into `jq`.
set -euo pipefail

: "${CRAWLORA_API_KEY:?Set CRAWLORA_API_KEY first — get a free key at https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills}"
# The key is written to a curl config file below. Restrict it to the key
# alphabet so a newline, quote, or config directive cannot alter that file.
case "$CRAWLORA_API_KEY" in
  *[!A-Za-z0-9._-]*) echo "invalid CRAWLORA_API_KEY format" >&2; exit 2 ;;
esac
# Fixed, non-overridable: an env-configurable base URL would let anything that
# can set CRAWLORA_API_BASE redirect this key to an attacker-controlled host.
base="https://api.crawlora.net/api/v1"

method="GET"
body=""
args=()
while [ $# -gt 0 ]; do
  case "$1" in
    -X)
      [ $# -ge 2 ] || { echo "-X requires an HTTP method" >&2; exit 2; }
      method="$2"; shift 2 ;;
    -d)
      [ $# -ge 2 ] || { echo "-d requires a request body" >&2; exit 2; }
      body="$2"; shift 2 ;;
    *)  args+=("$1"); shift ;;
  esac
done

[ "${#args[@]}" -ge 1 ] || { echo "usage: crawlora.sh [-X METHOD] /path [k=v ... | json-body]" >&2; exit 2; }
path="${args[0]}"
rest=("${args[@]:1}")

# This skill's helper is limited to its documented Crawlora route set. Keep
# caller-account surfaces and unrelated API routes out of the helper even if
# someone supplies an undocumented path directly.
case "$method" in
  GET|POST) ;;
  *)
    echo "only GET and POST are supported by the travel-hotel-research skill" >&2
    exit 2
    ;;
esac

# Reject path syntax that could smuggle a route through a shell glob check.
case "$path" in
  ""|*[?#%]*|*..*|*//* )
    echo "invalid path for the travel-hotel-research skill" >&2
    exit 2
    ;;
esac

# Static routes use escaped case patterns. Parameterized routes use anchored
# extended regular expressions so every {param} is exactly one non-empty path
# segment; unlike a case '*', [^/]+ cannot consume another slash.
route_allowed=false
case "$path" in
  /accor/amenities) route_allowed=true ;;
  /accor/brands) route_allowed=true ;;
  /accor/catalog/hotels) route_allowed=true ;;
  /accor/destination/hotels) route_allowed=true ;;
  /accor/property) route_allowed=true ;;
  /accor/search) route_allowed=true ;;
  /accor/search/details) route_allowed=true ;;
  /accor/search/suggest) route_allowed=true ;;
  /agoda/activities/search) route_allowed=true ;;
  /agoda/flights/itinerary-amenities) route_allowed=true ;;
  /agoda/flights/search) route_allowed=true ;;
  /agoda/flights/search-locations) route_allowed=true ;;
  /agoda/homes/search) route_allowed=true ;;
  /agoda/hotels/search) route_allowed=true ;;
  /airbnb/search) route_allowed=true ;;
  /booking-attractions/detail) route_allowed=true ;;
  /booking-attractions/reviews) route_allowed=true ;;
  /booking-attractions/search) route_allowed=true ;;
  /booking-flights/autocomplete) route_allowed=true ;;
  /booking-flights/search) route_allowed=true ;;
  /booking/hotel-detail) route_allowed=true ;;
  /booking/reviews) route_allowed=true ;;
  /booking/search) route_allowed=true ;;
  /expedia/activities/search) route_allowed=true ;;
  /expedia/flights/search) route_allowed=true ;;
  /expedia/locations/search) route_allowed=true ;;
  /expedia/properties/detail) route_allowed=true ;;
  /expedia/properties/filters) route_allowed=true ;;
  /expedia/properties/reviews) route_allowed=true ;;
  /expedia/properties/search) route_allowed=true ;;
  /hotels/autocomplete) route_allowed=true ;;
  /hotels/offers) route_allowed=true ;;
  /hotels/property) route_allowed=true ;;
  /hotels/rates) route_allowed=true ;;
  /hotels/reviews) route_allowed=true ;;
  /hotels/reviews/archive) route_allowed=true ;;
  /hotels/search) route_allowed=true ;;
  /ticketmaster/attraction) route_allowed=true ;;
  /ticketmaster/attraction-events) route_allowed=true ;;
  /ticketmaster/attraction-related) route_allowed=true ;;
  /ticketmaster/attraction-reviews) route_allowed=true ;;
  /ticketmaster/discover-categories) route_allowed=true ;;
  /ticketmaster/discover-category-events) route_allowed=true ;;
  /ticketmaster/discover-cities) route_allowed=true ;;
  /ticketmaster/discover-city-events) route_allowed=true ;;
  /ticketmaster/event) route_allowed=true ;;
  /ticketmaster/search-events) route_allowed=true ;;
  /ticketmaster/suggest) route_allowed=true ;;
  /ticketmaster/trending-attractions) route_allowed=true ;;
  /ticketmaster/venue) route_allowed=true ;;
  /ticketmaster/venue-enhanced-details) route_allowed=true ;;
  /ticketmaster/venue-events) route_allowed=true ;;
  /ticketweb/event) route_allowed=true ;;
  /ticketweb/search) route_allowed=true ;;
  /ticketweb/venue) route_allowed=true ;;
  /tripadvisor/autocomplete) route_allowed=true ;;
  /tripadvisor/enums) route_allowed=true ;;
  /tripadvisor/hotels) route_allowed=true ;;
  /tripadvisor/place) route_allowed=true ;;
  /tripadvisor/reviews) route_allowed=true ;;
  /tripadvisor/search) route_allowed=true ;;
  /tripcom/hotels/search) route_allowed=true ;;
esac
if [ "$route_allowed" = false ]; then
  route_regexes=(
  '^/agoda/activities/[^/]+$'
  '^/agoda/hotels/[^/]+$'
  '^/airbnb/host/[^/]+$'
  '^/airbnb/host/[^/]+/listings$'
  '^/airbnb/host/[^/]+/reviews$'
  '^/airbnb/room/[^/]+$'
  '^/airbnb/room/[^/]+/calendar$'
  '^/airbnb/room/[^/]+/reviews$'
  '^/tripcom/hotels/[^/]+$'
  )
  for route_regex in ${route_regexes[@]+"${route_regexes[@]}"}; do
    if [[ "$path" =~ $route_regex ]]; then
      route_allowed=true
      break
    fi
  done
fi
if [ "$route_allowed" = false ]; then
  echo "path is not in the travel-hotel-research skill catalog" >&2
  exit 2
fi

# Enforce the documented HTTP method for each route, not just the global method set.
route_method_allowed=false
route_method_regexes=(
  '^GET:/accor/amenities$'
  '^GET:/accor/brands$'
  '^GET:/accor/catalog/hotels$'
  '^GET:/accor/destination/hotels$'
  '^GET:/accor/property$'
  '^GET:/accor/search$'
  '^GET:/accor/search/details$'
  '^GET:/accor/search/suggest$'
  '^GET:/agoda/activities/[^/]+$'
  '^GET:/agoda/activities/search$'
  '^GET:/agoda/flights/search$'
  '^GET:/agoda/flights/search-locations$'
  '^GET:/agoda/homes/search$'
  '^GET:/agoda/hotels/[^/]+$'
  '^GET:/agoda/hotels/search$'
  '^GET:/airbnb/host/[^/]+$'
  '^GET:/airbnb/host/[^/]+/listings$'
  '^GET:/airbnb/host/[^/]+/reviews$'
  '^GET:/airbnb/room/[^/]+$'
  '^GET:/airbnb/room/[^/]+/calendar$'
  '^GET:/airbnb/room/[^/]+/reviews$'
  '^GET:/airbnb/search$'
  '^GET:/booking-attractions/detail$'
  '^GET:/booking-attractions/reviews$'
  '^GET:/booking-attractions/search$'
  '^GET:/booking-flights/autocomplete$'
  '^GET:/booking-flights/search$'
  '^GET:/booking/hotel-detail$'
  '^GET:/booking/reviews$'
  '^GET:/booking/search$'
  '^GET:/hotels/autocomplete$'
  '^GET:/ticketmaster/attraction$'
  '^GET:/ticketmaster/attraction-events$'
  '^GET:/ticketmaster/attraction-related$'
  '^GET:/ticketmaster/attraction-reviews$'
  '^GET:/ticketmaster/discover-categories$'
  '^GET:/ticketmaster/discover-category-events$'
  '^GET:/ticketmaster/discover-cities$'
  '^GET:/ticketmaster/discover-city-events$'
  '^GET:/ticketmaster/event$'
  '^GET:/ticketmaster/search-events$'
  '^GET:/ticketmaster/suggest$'
  '^GET:/ticketmaster/trending-attractions$'
  '^GET:/ticketmaster/venue$'
  '^GET:/ticketmaster/venue-enhanced-details$'
  '^GET:/ticketmaster/venue-events$'
  '^GET:/ticketweb/event$'
  '^GET:/ticketweb/search$'
  '^GET:/ticketweb/venue$'
  '^GET:/tripadvisor/autocomplete$'
  '^GET:/tripadvisor/enums$'
  '^GET:/tripadvisor/hotels$'
  '^GET:/tripadvisor/place$'
  '^GET:/tripadvisor/reviews$'
  '^GET:/tripadvisor/search$'
  '^GET:/tripcom/hotels/[^/]+$'
  '^GET:/tripcom/hotels/search$'
  '^POST:/agoda/flights/itinerary-amenities$'
  '^POST:/expedia/activities/search$'
  '^POST:/expedia/flights/search$'
  '^POST:/expedia/locations/search$'
  '^POST:/expedia/properties/detail$'
  '^POST:/expedia/properties/filters$'
  '^POST:/expedia/properties/reviews$'
  '^POST:/expedia/properties/search$'
  '^POST:/hotels/offers$'
  '^POST:/hotels/property$'
  '^POST:/hotels/rates$'
  '^POST:/hotels/reviews$'
  '^POST:/hotels/reviews/archive$'
  '^POST:/hotels/search$'
)
for route_method_regex in ${route_method_regexes[@]+"${route_method_regexes[@]}"}; do
  if [[ "$method:$path" =~ $route_method_regex ]]; then
    route_method_allowed=true
    break
  fi
done
if [ "$route_method_allowed" = false ]; then
  echo "method is not allowed for this travel-hotel-research route" >&2
  exit 2
fi



# Keep the API key out of the curl process command line. A private temporary
# config supplies the header and is removed automatically on exit.
umask 077
curl_config="$(mktemp "${TMPDIR:-/tmp}/crawlora-curl.XXXXXX")"
chmod 600 "$curl_config"
trap 'rm -f "$curl_config"' EXIT
printf 'header = "x-api-key: %s"\n' "$CRAWLORA_API_KEY" >"$curl_config"
auth=(--config "$curl_config")

if [ "$method" = "GET" ]; then
  # -G + --data-urlencode URL-encodes each value (so spaces etc. are safe).
  qs=()
  for kv in ${rest[@]+"${rest[@]}"}; do
    [ -n "$kv" ] || continue
    # curl treats both @file and name@file forms as local-file input for
    # --data-urlencode. Reject @ outright so query arguments cannot disclose
    # local files to the Crawlora API.
    case "$kv" in
      *@*) echo "@ is not allowed in query arguments" >&2; exit 2 ;;
    esac
    qs+=(--data-urlencode "$kv")
  done
  # -q must be the first curl option: ignore any user ~/.curlrc so inherited
  # config cannot redirect the request, add uploads, or alter credential use.
  curl -q -fsS -G "${auth[@]}" ${qs[@]+"${qs[@]}"} "${base}${path}"
else
  [ -n "$body" ] || body="${rest[0]:-}"
  [ -n "$body" ] || body='{}'
  # Stream the body on stdin so curl never interprets a user value as its
  # @file shorthand (and cannot read local files supplied in a request body).
  printf '%s' "$body" | curl -q -fsS -X "$method" "${auth[@]}" \
    -H "Content-Type: application/json" --data-binary @- "${base}${path}"
fi
