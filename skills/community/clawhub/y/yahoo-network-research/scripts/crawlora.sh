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
    -X|-d) echo "only GET are supported by the yahoo-network-research skill" >&2; exit 2 ;;
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
    echo "only GET are supported by the yahoo-network-research skill" >&2
    exit 2
    ;;
esac

# Reject path syntax that could smuggle a route through a shell glob check.
case "$path" in
  ""|*[?#%]*|*..*|*//* )
    echo "invalid path for the yahoo-network-research skill" >&2
    exit 2
    ;;
esac

# Static routes use escaped case patterns. Parameterized routes use anchored
# extended regular expressions so every {param} is exactly one non-empty path
# segment; unlike a case '*', [^/]+ cannot consume another slash.
route_allowed=false
case "$path" in
  /yahoo-autos/article) route_allowed=true ;;
  /yahoo-autos/category) route_allowed=true ;;
  /yahoo-autos/home) route_allowed=true ;;
  /yahoo-entertainment/article) route_allowed=true ;;
  /yahoo-entertainment/category) route_allowed=true ;;
  /yahoo-entertainment/home) route_allowed=true ;;
  /yahoo-health/article) route_allowed=true ;;
  /yahoo-health/category) route_allowed=true ;;
  /yahoo-health/home) route_allowed=true ;;
  /yahoo-life/article) route_allowed=true ;;
  /yahoo-life/home) route_allowed=true ;;
  /yahoo-news/article) route_allowed=true ;;
  /yahoo-news/category) route_allowed=true ;;
  /yahoo-news/comments) route_allowed=true ;;
  /yahoo-news/comments/replies) route_allowed=true ;;
  /yahoo-news/home) route_allowed=true ;;
  /yahoo-news/related) route_allowed=true ;;
  /yahoo-news/suggest) route_allowed=true ;;
  /yahoo-shopping/article) route_allowed=true ;;
  /yahoo-shopping/author) route_allowed=true ;;
  /yahoo-shopping/categories) route_allowed=true ;;
  /yahoo-shopping/category) route_allowed=true ;;
  /yahoo-shopping/experts) route_allowed=true ;;
  /yahoo-shopping/home) route_allowed=true ;;
  /yahoo-shopping/shopping-list) route_allowed=true ;;
  /yahoo-shopping/shopping-lists) route_allowed=true ;;
  /yahoo-shopping/sitemap) route_allowed=true ;;
  /yahoo-shopping/sitemaps) route_allowed=true ;;
  /yahoo-shopping/store) route_allowed=true ;;
  /yahoo-shopping/stores) route_allowed=true ;;
  /yahoo-shopping/suggest) route_allowed=true ;;
  /yahoo-sports/college-rankings) route_allowed=true ;;
  /yahoo-sports/draft) route_allowed=true ;;
  /yahoo-sports/dropdown-catalog) route_allowed=true ;;
  /yahoo-sports/game) route_allowed=true ;;
  /yahoo-sports/golf-leaderboard) route_allowed=true ;;
  /yahoo-sports/golf-player) route_allowed=true ;;
  /yahoo-sports/golf-player-news) route_allowed=true ;;
  /yahoo-sports/golf-players) route_allowed=true ;;
  /yahoo-sports/golf-schedule) route_allowed=true ;;
  /yahoo-sports/home) route_allowed=true ;;
  /yahoo-sports/injury-report) route_allowed=true ;;
  /yahoo-sports/league-schedule) route_allowed=true ;;
  /yahoo-sports/leagues) route_allowed=true ;;
  /yahoo-sports/mma-fight-card) route_allowed=true ;;
  /yahoo-sports/mma-schedule) route_allowed=true ;;
  /yahoo-sports/more-news) route_allowed=true ;;
  /yahoo-sports/motorsports-race) route_allowed=true ;;
  /yahoo-sports/motorsports-schedule) route_allowed=true ;;
  /yahoo-sports/navigation) route_allowed=true ;;
  /yahoo-sports/network-catalog) route_allowed=true ;;
  /yahoo-sports/news) route_allowed=true ;;
  /yahoo-sports/newsletter-archive) route_allowed=true ;;
  /yahoo-sports/newsletters) route_allowed=true ;;
  /yahoo-sports/odds-featured) route_allowed=true ;;
  /yahoo-sports/odds-game) route_allowed=true ;;
  /yahoo-sports/odds-games) route_allowed=true ;;
  /yahoo-sports/odds-trending) route_allowed=true ;;
  /yahoo-sports/olympics-medals) route_allowed=true ;;
  /yahoo-sports/player) route_allowed=true ;;
  /yahoo-sports/player-search) route_allowed=true ;;
  /yahoo-sports/playoff-bracket) route_allowed=true ;;
  /yahoo-sports/playoff-bracket-catalog) route_allowed=true ;;
  /yahoo-sports/rss-catalog) route_allowed=true ;;
  /yahoo-sports/rss-feed) route_allowed=true ;;
  /yahoo-sports/schedule-catalog) route_allowed=true ;;
  /yahoo-sports/scoreboard) route_allowed=true ;;
  /yahoo-sports/section-stream) route_allowed=true ;;
  /yahoo-sports/soccer-scoreboard) route_allowed=true ;;
  /yahoo-sports/sportsbook-catalog) route_allowed=true ;;
  /yahoo-sports/standings) route_allowed=true ;;
  /yahoo-sports/stats) route_allowed=true ;;
  /yahoo-sports/stats-catalog) route_allowed=true ;;
  /yahoo-sports/stats-discovery) route_allowed=true ;;
  /yahoo-sports/team) route_allowed=true ;;
  /yahoo-sports/team-roster) route_allowed=true ;;
  /yahoo-sports/team-schedule) route_allowed=true ;;
  /yahoo-sports/tennis-rankings) route_allowed=true ;;
  /yahoo-sports/tennis-schedule) route_allowed=true ;;
  /yahoo-sports/tennis-scoreboard) route_allowed=true ;;
  /yahoo-sports/topic-news) route_allowed=true ;;
  /yahoo-sports/video-headlines) route_allowed=true ;;
  /yahoo-sports/video-list-catalog) route_allowed=true ;;
  /yahoo-sports/watch-schedule) route_allowed=true ;;
  /yahoo-tech/article) route_allowed=true ;;
  /yahoo-tech/category) route_allowed=true ;;
  /yahoo-tech/home) route_allowed=true ;;
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
  echo "path is not in the yahoo-network-research skill catalog" >&2
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