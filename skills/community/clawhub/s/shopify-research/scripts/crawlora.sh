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
    -X|-d) echo "only GET are supported by the shopify-research skill" >&2; exit 2 ;;
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
    echo "only GET are supported by the shopify-research skill" >&2
    exit 2
    ;;
esac

# Reject path syntax that could smuggle a route through a shell glob check.
case "$path" in
  ""|*[?#%]*|*..*|*//* )
    echo "invalid path for the shopify-research skill" >&2
    exit 2
    ;;
esac

# Static routes use escaped case patterns. Parameterized routes use anchored
# extended regular expressions so every {param} is exactly one non-empty path
# segment; unlike a case '*', [^/]+ cannot consume another slash.
route_allowed=false
case "$path" in
  /allbirds/collections) route_allowed=true ;;
  /allbirds/pages) route_allowed=true ;;
  /allbirds/products) route_allowed=true ;;
  /allbirds/search/suggest) route_allowed=true ;;
  /allbirds/sitemap/urls) route_allowed=true ;;
  /allbirds/sitemaps) route_allowed=true ;;
  /allbirds/store) route_allowed=true ;;
  /brooklinen/collections) route_allowed=true ;;
  /brooklinen/pages) route_allowed=true ;;
  /brooklinen/products) route_allowed=true ;;
  /brooklinen/search/suggest) route_allowed=true ;;
  /brooklinen/sitemap/urls) route_allowed=true ;;
  /brooklinen/sitemaps) route_allowed=true ;;
  /brooklinen/store) route_allowed=true ;;
  /colehaan/collections) route_allowed=true ;;
  /colehaan/pages) route_allowed=true ;;
  /colehaan/products) route_allowed=true ;;
  /colehaan/search/suggest) route_allowed=true ;;
  /colehaan/sitemap/urls) route_allowed=true ;;
  /colehaan/sitemaps) route_allowed=true ;;
  /colehaan/store) route_allowed=true ;;
  /everlane/collections) route_allowed=true ;;
  /everlane/pages) route_allowed=true ;;
  /everlane/products) route_allowed=true ;;
  /everlane/search/suggest) route_allowed=true ;;
  /everlane/sitemap/urls) route_allowed=true ;;
  /everlane/sitemaps) route_allowed=true ;;
  /everlane/store) route_allowed=true ;;
  /fashionnova/collections) route_allowed=true ;;
  /fashionnova/pages) route_allowed=true ;;
  /fashionnova/products) route_allowed=true ;;
  /fashionnova/search/suggest) route_allowed=true ;;
  /fashionnova/sitemap/urls) route_allowed=true ;;
  /fashionnova/sitemaps) route_allowed=true ;;
  /fashionnova/store) route_allowed=true ;;
  /gymshark/collections) route_allowed=true ;;
  /gymshark/pages) route_allowed=true ;;
  /gymshark/products) route_allowed=true ;;
  /gymshark/sitemap/urls) route_allowed=true ;;
  /gymshark/sitemaps) route_allowed=true ;;
  /gymshark/store) route_allowed=true ;;
  /jcrew/categories) route_allowed=true ;;
  /jcrew/category) route_allowed=true ;;
  /jcrew/product) route_allowed=true ;;
  /jcrew/product/reviews) route_allowed=true ;;
  /jcrew/search) route_allowed=true ;;
  /jcrew/size-chart) route_allowed=true ;;
  /jcrew/stores) route_allowed=true ;;
  /jcrew/suggest) route_allowed=true ;;
  /kyliecosmetics/collections) route_allowed=true ;;
  /kyliecosmetics/pages) route_allowed=true ;;
  /kyliecosmetics/products) route_allowed=true ;;
  /kyliecosmetics/search/suggest) route_allowed=true ;;
  /kyliecosmetics/sitemap/urls) route_allowed=true ;;
  /kyliecosmetics/sitemaps) route_allowed=true ;;
  /kyliecosmetics/store) route_allowed=true ;;
  /ohpolly/collections) route_allowed=true ;;
  /ohpolly/pages) route_allowed=true ;;
  /ohpolly/products) route_allowed=true ;;
  /ohpolly/search/suggest) route_allowed=true ;;
  /ohpolly/sitemap/urls) route_allowed=true ;;
  /ohpolly/sitemaps) route_allowed=true ;;
  /ohpolly/store) route_allowed=true ;;
  /quince/categories) route_allowed=true ;;
  /quince/navigation) route_allowed=true ;;
  /quince/product) route_allowed=true ;;
  /quince/product/faq) route_allowed=true ;;
  /quince/product/reviews) route_allowed=true ;;
  /quince/search) route_allowed=true ;;
  /quince/sitemap/urls) route_allowed=true ;;
  /quince/sitemaps) route_allowed=true ;;
  /quince/suggest) route_allowed=true ;;
  /rothys/collections) route_allowed=true ;;
  /rothys/pages) route_allowed=true ;;
  /rothys/products) route_allowed=true ;;
  /rothys/search/suggest) route_allowed=true ;;
  /rothys/sitemap/urls) route_allowed=true ;;
  /rothys/sitemaps) route_allowed=true ;;
  /rothys/store) route_allowed=true ;;
  /shopify/collections) route_allowed=true ;;
  /shopify/pages) route_allowed=true ;;
  /shopify/products) route_allowed=true ;;
  /shopify/search/suggest) route_allowed=true ;;
  /shopify/sitemap/urls) route_allowed=true ;;
  /shopify/sitemaps) route_allowed=true ;;
  /shopify/store) route_allowed=true ;;
  /skims/collections) route_allowed=true ;;
  /skims/pages) route_allowed=true ;;
  /skims/products) route_allowed=true ;;
  /skims/search/suggest) route_allowed=true ;;
  /skims/sitemap/urls) route_allowed=true ;;
  /skims/sitemaps) route_allowed=true ;;
  /skims/store) route_allowed=true ;;
  /stevemadden/collections) route_allowed=true ;;
  /stevemadden/pages) route_allowed=true ;;
  /stevemadden/products) route_allowed=true ;;
  /stevemadden/search/suggest) route_allowed=true ;;
  /stevemadden/sitemap/urls) route_allowed=true ;;
  /stevemadden/sitemaps) route_allowed=true ;;
  /stevemadden/store) route_allowed=true ;;
  /thebodyshop/collections) route_allowed=true ;;
  /thebodyshop/pages) route_allowed=true ;;
  /thebodyshop/products) route_allowed=true ;;
  /thebodyshop/search/suggest) route_allowed=true ;;
  /thebodyshop/sitemap/urls) route_allowed=true ;;
  /thebodyshop/sitemaps) route_allowed=true ;;
  /thebodyshop/store) route_allowed=true ;;
esac
if [ "$route_allowed" = false ]; then
  route_regexes=(
  '^/allbirds/collections/[^/]+/products$'
  '^/allbirds/pages/[^/]+$'
  '^/allbirds/products/[^/]+$'
  '^/allbirds/products/[^/]+/recommendations$'
  '^/brooklinen/collections/[^/]+/products$'
  '^/brooklinen/pages/[^/]+$'
  '^/brooklinen/products/[^/]+$'
  '^/brooklinen/products/[^/]+/recommendations$'
  '^/colehaan/collections/[^/]+/products$'
  '^/colehaan/pages/[^/]+$'
  '^/colehaan/products/[^/]+$'
  '^/colehaan/products/[^/]+/recommendations$'
  '^/everlane/collections/[^/]+/products$'
  '^/everlane/pages/[^/]+$'
  '^/everlane/products/[^/]+$'
  '^/everlane/products/[^/]+/recommendations$'
  '^/fashionnova/collections/[^/]+/products$'
  '^/fashionnova/pages/[^/]+$'
  '^/fashionnova/products/[^/]+$'
  '^/fashionnova/products/[^/]+/recommendations$'
  '^/gymshark/collections/[^/]+/products$'
  '^/gymshark/pages/[^/]+$'
  '^/gymshark/products/[^/]+$'
  '^/gymshark/products/[^/]+/recommendations$'
  '^/kyliecosmetics/collections/[^/]+/products$'
  '^/kyliecosmetics/pages/[^/]+$'
  '^/kyliecosmetics/products/[^/]+$'
  '^/kyliecosmetics/products/[^/]+/recommendations$'
  '^/ohpolly/collections/[^/]+/products$'
  '^/ohpolly/pages/[^/]+$'
  '^/ohpolly/products/[^/]+$'
  '^/ohpolly/products/[^/]+/recommendations$'
  '^/rothys/collections/[^/]+/products$'
  '^/rothys/pages/[^/]+$'
  '^/rothys/products/[^/]+$'
  '^/rothys/products/[^/]+/recommendations$'
  '^/shopify/collections/[^/]+/products$'
  '^/shopify/pages/[^/]+$'
  '^/shopify/products/[^/]+$'
  '^/shopify/products/[^/]+/recommendations$'
  '^/skims/collections/[^/]+/products$'
  '^/skims/pages/[^/]+$'
  '^/skims/products/[^/]+$'
  '^/skims/products/[^/]+/recommendations$'
  '^/stevemadden/collections/[^/]+/products$'
  '^/stevemadden/pages/[^/]+$'
  '^/stevemadden/products/[^/]+$'
  '^/stevemadden/products/[^/]+/recommendations$'
  '^/thebodyshop/collections/[^/]+/products$'
  '^/thebodyshop/pages/[^/]+$'
  '^/thebodyshop/products/[^/]+$'
  '^/thebodyshop/products/[^/]+/recommendations$'
  )
  for route_regex in ${route_regexes[@]+"${route_regexes[@]}"}; do
    if [[ "$path" =~ $route_regex ]]; then
      route_allowed=true
      break
    fi
  done
fi
if [ "$route_allowed" = false ]; then
  echo "path is not in the shopify-research skill catalog" >&2
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