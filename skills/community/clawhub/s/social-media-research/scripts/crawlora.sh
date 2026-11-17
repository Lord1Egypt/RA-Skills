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
    -X|-d) echo "only GET are supported by the social-media-research skill" >&2; exit 2 ;;
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
    echo "only GET are supported by the social-media-research skill" >&2
    exit 2
    ;;
esac

# Reject path syntax that could smuggle a route through a shell glob check.
case "$path" in
  ""|*[?#%]*|*..*|*//* )
    echo "invalid path for the social-media-research skill" >&2
    exit 2
    ;;
esac

# Static routes use escaped case patterns. Parameterized routes use anchored
# extended regular expressions so every {param} is exactly one non-empty path
# segment; unlike a case '*', [^/]+ cannot consume another slash.
route_allowed=false
case "$path" in
  /bilibili/anime-home) route_allowed=true ;;
  /bilibili/autocomplete) route_allowed=true ;;
  /bilibili/guochuang-home) route_allowed=true ;;
  /bilibili/must-watch) route_allowed=true ;;
  /bilibili/popular) route_allowed=true ;;
  /bilibili/ranking) route_allowed=true ;;
  /bilibili/vertical-home) route_allowed=true ;;
  /bilibili/weekly) route_allowed=true ;;
  /bluesky/author-feed) route_allowed=true ;;
  /bluesky/followers) route_allowed=true ;;
  /bluesky/follows) route_allowed=true ;;
  /bluesky/post-likes) route_allowed=true ;;
  /bluesky/post-quotes) route_allowed=true ;;
  /bluesky/post-reposted-by) route_allowed=true ;;
  /bluesky/post-thread) route_allowed=true ;;
  /bluesky/posts) route_allowed=true ;;
  /bluesky/profile) route_allowed=true ;;
  /bluesky/search-actors) route_allowed=true ;;
  /bluesky/trending-topics) route_allowed=true ;;
  /facebook/marketplace/search) route_allowed=true ;;
  /linkedin/product/categories) route_allowed=true ;;
  /linkedin/products/search) route_allowed=true ;;
  /patreon/creator) route_allowed=true ;;
  /patreon/creator/tiers) route_allowed=true ;;
  /patreon/explore) route_allowed=true ;;
  /patreon/rss) route_allowed=true ;;
  /pinterest/categories) route_allowed=true ;;
  /pinterest/search) route_allowed=true ;;
  /reddit/leads) route_allowed=true ;;
  /reddit/search) route_allowed=true ;;
  /reddit/subreddits/posts) route_allowed=true ;;
  /reddit/trends) route_allowed=true ;;
  /threads/search) route_allowed=true ;;
  /threads/search/topics) route_allowed=true ;;
  /tiktok/category) route_allowed=true ;;
  /tiktok/comments) route_allowed=true ;;
  /tiktok/creative-center/filters) route_allowed=true ;;
  /tiktok/creative-center/hashtags) route_allowed=true ;;
  /tiktok/creative-center/top-content) route_allowed=true ;;
  /tiktok/creative-center/videos) route_allowed=true ;;
  /tiktok/hashtags) route_allowed=true ;;
  /tiktok/mobile/feed) route_allowed=true ;;
  /tiktok/mobile/hashtag) route_allowed=true ;;
  /tiktok/mobile/hashtag/posts) route_allowed=true ;;
  /tiktok/mobile/hashtags) route_allowed=true ;;
  /tiktok/mobile/live/effects) route_allowed=true ;;
  /tiktok/mobile/live/gifts) route_allowed=true ;;
  /tiktok/mobile/live/search) route_allowed=true ;;
  /tiktok/mobile/music/beats) route_allowed=true ;;
  /tiktok/mobile/music/collections) route_allowed=true ;;
  /tiktok/mobile/music/pick) route_allowed=true ;;
  /tiktok/mobile/music/posts) route_allowed=true ;;
  /tiktok/mobile/music/related) route_allowed=true ;;
  /tiktok/mobile/music/trending) route_allowed=true ;;
  /tiktok/mobile/search) route_allowed=true ;;
  /tiktok/mobile/search/music) route_allowed=true ;;
  /tiktok/mobile/search/user) route_allowed=true ;;
  /tiktok/mobile/trending/categories) route_allowed=true ;;
  /tiktok/mobile/trending/effects) route_allowed=true ;;
  /tiktok/popular-trend/country-industry-meta) route_allowed=true ;;
  /tiktok/posts) route_allowed=true ;;
  /tiktok/search) route_allowed=true ;;
  /tiktok/search/hashtag) route_allowed=true ;;
  /tiktok/search/user) route_allowed=true ;;
  /tiktok/top-ads/analysis) route_allowed=true ;;
  /tiktok/top-ads/detail) route_allowed=true ;;
  /tiktok/top-ads/filters) route_allowed=true ;;
  /tiktok/top-ads/list) route_allowed=true ;;
  /tiktok/top-ads/location-info) route_allowed=true ;;
  /tiktok/top-ads/locations) route_allowed=true ;;
  /tiktok/top-ads/recommend) route_allowed=true ;;
  /tiktok/top-ads/safety) route_allowed=true ;;
  /tiktok/top-ads/spotlight) route_allowed=true ;;
  /tiktok/top-ads/suggestions) route_allowed=true ;;
  /tiktok/trending) route_allowed=true ;;
esac
if [ "$route_allowed" = false ]; then
  route_regexes=(
  '^/facebook/[^/]+$'
  '^/instagram/post/[^/]+/[^/]+$'
  '^/instagram/profile/[^/]+$'
  '^/instagram/reels/[^/]+$'
  '^/linkedin/company/[^/]+$'
  '^/linkedin/product/[^/]+$'
  '^/linkedin/showcase/[^/]+$'
  '^/pinterest/board/[^/]+/[^/]+$'
  '^/pinterest/ideas/[^/]+$'
  '^/pinterest/pin/[^/]+$'
  '^/pinterest/user/[^/]+$'
  '^/pinterest/user/[^/]+/boards$'
  '^/pinterest/user/[^/]+/pins$'
  '^/reddit/comments/[^/]+$'
  '^/reddit/domain/[^/]+/posts$'
  '^/reddit/post/[^/]+$'
  '^/reddit/subreddit/[^/]+/about$'
  '^/reddit/subreddit/[^/]+/comments$'
  '^/reddit/subreddit/[^/]+/posts$'
  '^/reddit/user/[^/]+/comments$'
  '^/reddit/user/[^/]+/posts$'
  '^/threads/post/[^/]+/[^/]+$'
  '^/threads/post/[^/]+/[^/]+/replies$'
  '^/threads/profile/[^/]+$'
  '^/threads/profile/[^/]+/media$'
  '^/threads/profile/[^/]+/posts$'
  '^/threads/profile/[^/]+/replies$'
  '^/threads/profile/[^/]+/reposts$'
  '^/threads/profile/[^/]+/topics$'
  '^/tiktok/explore/[^/]+$'
  '^/tiktok/hashtag/[^/]+$'
  '^/tiktok/post/[^/]+$'
  '^/tiktok/profile/[^/]+$'
  '^/x/post/[^/]+$'
  '^/x/profile/[^/]+$'
  '^/x/profile/[^/]+/posts$'
  )
  for route_regex in ${route_regexes[@]+"${route_regexes[@]}"}; do
    if [[ "$path" =~ $route_regex ]]; then
      route_allowed=true
      break
    fi
  done
fi
if [ "$route_allowed" = false ]; then
  echo "path is not in the social-media-research skill catalog" >&2
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