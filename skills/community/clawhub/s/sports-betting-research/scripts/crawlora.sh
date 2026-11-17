#!/usr/bin/env bash
# Crawlora REST helper — minimal, dependency-free (curl only).
# Calls https://api.crawlora.net/api/v1 with your Crawlora API key.
# Get a free key (2,000 credits/mo, no card) at https://crawlora.net?utm_source=github&utm_medium=referral&utm_campaign=crawlora-skills.
#
# Usage:
#   GET  :  crawlora.sh /path
#
# GET key=value args become the query string. Prints raw JSON to stdout — pipe into `jq`.
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
args=()
while [ $# -gt 0 ]; do
  case "$1" in
    -X|-d) echo "only GET are supported by the sports-betting-research skill" >&2; exit 2 ;;
    *) args+=("$1"); shift ;;
  esac
done

[ "${#args[@]}" -ge 1 ] || { echo "usage: crawlora.sh /<route> [k=v ...]" >&2; exit 2; }
path="${args[0]}"
rest=("${args[@]:1}")

# This skill's helper is limited to its documented Crawlora route set. Keep
# caller-account surfaces and unrelated API routes out of the helper even if
# someone supplies an undocumented path directly.
case "$method" in
  GET) ;;
  *)
    echo "only GET are supported by the sports-betting-research skill" >&2
    exit 2
    ;;
esac

# Reject path syntax that could smuggle a route through a shell glob check.
case "$path" in
  ""|*[?#%]*|*..*|*//* )
    echo "invalid path for the sports-betting-research skill" >&2
    exit 2
    ;;
esac

# Static routes use escaped case patterns. Parameterized routes use anchored
# extended regular expressions so every {param} is exactly one non-empty path
# segment; unlike a case '*', [^/]+ cannot consume another slash.
route_allowed=false
case "$path" in
  /draftkings/sportsbook/event) route_allowed=true ;;
  /draftkings/sportsbook/event-context) route_allowed=true ;;
  /draftkings/sportsbook/event-markets) route_allowed=true ;;
  /draftkings/sportsbook/featured-leagues) route_allowed=true ;;
  /draftkings/sportsbook/futures) route_allowed=true ;;
  /draftkings/sportsbook/league-events) route_allowed=true ;;
  /draftkings/sportsbook/leagues) route_allowed=true ;;
  /draftkings/sportsbook/live) route_allowed=true ;;
  /draftkings/sportsbook/odds) route_allowed=true ;;
  /draftkings/sportsbook/quick-links) route_allowed=true ;;
  /draftkings/sportsbook/team) route_allowed=true ;;
  /draftkings/sportsbook/teams) route_allowed=true ;;
  /espn/athlete) route_allowed=true ;;
  /espn/game-summary) route_allowed=true ;;
  /espn/news) route_allowed=true ;;
  /espn/rankings) route_allowed=true ;;
  /espn/scoreboard) route_allowed=true ;;
  /espn/standings) route_allowed=true ;;
  /espn/team) route_allowed=true ;;
  /espn/team-roster) route_allowed=true ;;
  /espn/teams) route_allowed=true ;;
  /flashscore/match-odds) route_allowed=true ;;
  /flashscore/odds-geos) route_allowed=true ;;
  /flashscore/team-outright-odds) route_allowed=true ;;
  /flashscore/tournament-outright-odds) route_allowed=true ;;
  /sofascore/categories) route_allowed=true ;;
  /sofascore/category-tournaments) route_allowed=true ;;
  /sofascore/draft) route_allowed=true ;;
  /sofascore/draft-picks) route_allowed=true ;;
  /sofascore/esports-game) route_allowed=true ;;
  /sofascore/event) route_allowed=true ;;
  /sofascore/event-at-bat-pitches) route_allowed=true ;;
  /sofascore/event-at-bats) route_allowed=true ;;
  /sofascore/event-average-positions) route_allowed=true ;;
  /sofascore/event-baseball-top-performers) route_allowed=true ;;
  /sofascore/event-best-players) route_allowed=true ;;
  /sofascore/event-comments) route_allowed=true ;;
  /sofascore/event-esports-games) route_allowed=true ;;
  /sofascore/event-graph) route_allowed=true ;;
  /sofascore/event-h2h) route_allowed=true ;;
  /sofascore/event-highlights) route_allowed=true ;;
  /sofascore/event-incidents) route_allowed=true ;;
  /sofascore/event-innings) route_allowed=true ;;
  /sofascore/event-lineups) route_allowed=true ;;
  /sofascore/event-managers) route_allowed=true ;;
  /sofascore/event-odds) route_allowed=true ;;
  /sofascore/event-player-heatmap) route_allowed=true ;;
  /sofascore/event-player-statistics) route_allowed=true ;;
  /sofascore/event-point-by-point) route_allowed=true ;;
  /sofascore/event-pregame-form) route_allowed=true ;;
  /sofascore/event-shotmap) route_allowed=true ;;
  /sofascore/event-statistics) route_allowed=true ;;
  /sofascore/event-team-heatmap) route_allowed=true ;;
  /sofascore/event-team-streaks) route_allowed=true ;;
  /sofascore/event-tennis-power) route_allowed=true ;;
  /sofascore/event-tv-channels) route_allowed=true ;;
  /sofascore/event-votes) route_allowed=true ;;
  /sofascore/live-events) route_allowed=true ;;
  /sofascore/manager) route_allowed=true ;;
  /sofascore/manager-events) route_allowed=true ;;
  /sofascore/mma-card) route_allowed=true ;;
  /sofascore/mma-schedule) route_allowed=true ;;
  /sofascore/odds-dropping) route_allowed=true ;;
  /sofascore/odds-winning) route_allowed=true ;;
  /sofascore/player) route_allowed=true ;;
  /sofascore/player-attributes) route_allowed=true ;;
  /sofascore/player-events) route_allowed=true ;;
  /sofascore/player-last-year-summary) route_allowed=true ;;
  /sofascore/player-national-team-statistics) route_allowed=true ;;
  /sofascore/player-penalty-history) route_allowed=true ;;
  /sofascore/player-ratings) route_allowed=true ;;
  /sofascore/player-season-heatmap) route_allowed=true ;;
  /sofascore/player-season-statistics) route_allowed=true ;;
  /sofascore/player-statistical-rankings) route_allowed=true ;;
  /sofascore/player-statistics-seasons) route_allowed=true ;;
  /sofascore/player-tournaments) route_allowed=true ;;
  /sofascore/player-transfers) route_allowed=true ;;
  /sofascore/ranking-types) route_allowed=true ;;
  /sofascore/rankings) route_allowed=true ;;
  /sofascore/referee) route_allowed=true ;;
  /sofascore/referee-events) route_allowed=true ;;
  /sofascore/referee-statistics) route_allowed=true ;;
  /sofascore/round-events) route_allowed=true ;;
  /sofascore/scheduled-events) route_allowed=true ;;
  /sofascore/scheduled-tournaments) route_allowed=true ;;
  /sofascore/search) route_allowed=true ;;
  /sofascore/search-typed) route_allowed=true ;;
  /sofascore/season-events) route_allowed=true ;;
  /sofascore/sports) route_allowed=true ;;
  /sofascore/stage) route_allowed=true ;;
  /sofascore/stage-categories) route_allowed=true ;;
  /sofascore/stage-driver-performance) route_allowed=true ;;
  /sofascore/stage-featured) route_allowed=true ;;
  /sofascore/stage-schedule) route_allowed=true ;;
  /sofascore/stage-seasons) route_allowed=true ;;
  /sofascore/stage-standings) route_allowed=true ;;
  /sofascore/stage-substages) route_allowed=true ;;
  /sofascore/standings) route_allowed=true ;;
  /sofascore/team) route_allowed=true ;;
  /sofascore/team-achievements) route_allowed=true ;;
  /sofascore/team-events) route_allowed=true ;;
  /sofascore/team-goal-distributions) route_allowed=true ;;
  /sofascore/team-near-events) route_allowed=true ;;
  /sofascore/team-of-the-week) route_allowed=true ;;
  /sofascore/team-of-the-week-periods) route_allowed=true ;;
  /sofascore/team-performance) route_allowed=true ;;
  /sofascore/team-player-statistics) route_allowed=true ;;
  /sofascore/team-player-statistics-seasons) route_allowed=true ;;
  /sofascore/team-players) route_allowed=true ;;
  /sofascore/team-rankings) route_allowed=true ;;
  /sofascore/team-season-statistics) route_allowed=true ;;
  /sofascore/team-statistics-seasons) route_allowed=true ;;
  /sofascore/team-top-players) route_allowed=true ;;
  /sofascore/team-tournaments) route_allowed=true ;;
  /sofascore/team-transfers) route_allowed=true ;;
  /sofascore/tennis-player-grand-slam-results) route_allowed=true ;;
  /sofascore/tournament-cuptree) route_allowed=true ;;
  /sofascore/tournament-info) route_allowed=true ;;
  /sofascore/tournament-player-of-the-season) route_allowed=true ;;
  /sofascore/tournament-player-statistics) route_allowed=true ;;
  /sofascore/tournament-rounds) route_allowed=true ;;
  /sofascore/tournament-seasons) route_allowed=true ;;
  /sofascore/tournament-statistics-info) route_allowed=true ;;
  /sofascore/tournament-team-of-the-season) route_allowed=true ;;
  /sofascore/tournament-teams) route_allowed=true ;;
  /sofascore/tournament-top-players) route_allowed=true ;;
  /sofascore/tournament-top-teams) route_allowed=true ;;
  /sofascore/tournament-venues) route_allowed=true ;;
  /sofascore/tournament-winners) route_allowed=true ;;
  /sofascore/tournaments-with-feature) route_allowed=true ;;
  /sofascore/trending-events) route_allowed=true ;;
  /sofascore/trending-players) route_allowed=true ;;
  /sofascore/venue) route_allowed=true ;;
  /sofascore/venue-events) route_allowed=true ;;
esac
if [ "$route_allowed" = false ]; then
  route_regexes=(

  )
  for route_regex in ${route_regexes[@]+"${route_regexes[@]}"}; do
    if [[ "$path" =~ $route_regex ]]; then
      route_allowed=true
      break
    fi
  done
fi
if [ "$route_allowed" = false ]; then
  echo "path is not in the sports-betting-research skill catalog" >&2
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

# GET-only skill: no request body or alternate method is accepted.
# -G + --data-urlencode URL-encodes each value (so spaces etc. are safe).
qs=()
for kv in ${rest[@]+"${rest[@]}"}; do
  [ -n "$kv" ] || continue
  case "$kv" in
    *@*) echo "@ is not allowed in query arguments" >&2; exit 2 ;;
  esac
  qs+=(--data-urlencode "$kv")
done
curl -q -fsS -G "${auth[@]}" ${qs[@]+"${qs[@]}"} "${base}${path}"