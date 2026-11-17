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
    echo "only GET and POST are supported by the restaurant-food-delivery-research skill" >&2
    exit 2
    ;;
esac

# Reject path syntax that could smuggle a route through a shell glob check.
case "$path" in
  ""|*[?#%]*|*..*|*//* )
    echo "invalid path for the restaurant-food-delivery-research skill" >&2
    exit 2
    ;;
esac

# Static routes use escaped case patterns. Parameterized routes use anchored
# extended regular expressions so every {param} is exactly one non-empty path
# segment; unlike a case '*', [^/]+ cannot consume another slash.
route_allowed=false
case "$path" in
  /7now/catalog) route_allowed=true ;;
  /7now/categories) route_allowed=true ;;
  /7now/category) route_allowed=true ;;
  /7now/combo) route_allowed=true ;;
  /7now/combos) route_allowed=true ;;
  /7now/deals) route_allowed=true ;;
  /7now/offers) route_allowed=true ;;
  /7now/popular) route_allowed=true ;;
  /7now/product) route_allowed=true ;;
  /7now/promotion) route_allowed=true ;;
  /7now/search) route_allowed=true ;;
  /7now/stores) route_allowed=true ;;
  /7now/suggest) route_allowed=true ;;
  /arbys/categories) route_allowed=true ;;
  /arbys/directory) route_allowed=true ;;
  /arbys/location) route_allowed=true ;;
  /arbys/locations) route_allowed=true ;;
  /arbys/menu) route_allowed=true ;;
  /burgerking/availability) route_allowed=true ;;
  /burgerking/locations) route_allowed=true ;;
  /burgerking/menu) route_allowed=true ;;
  /burgerking/product) route_allowed=true ;;
  /chick-fil-a/content) route_allowed=true ;;
  /chick-fil-a/content-taxonomy) route_allowed=true ;;
  /chick-fil-a/faq) route_allowed=true ;;
  /chick-fil-a/location) route_allowed=true ;;
  /chick-fil-a/locations) route_allowed=true ;;
  /chick-fil-a/menu) route_allowed=true ;;
  /chick-fil-a/menu-item) route_allowed=true ;;
  /chick-fil-a/menu-taxonomy) route_allowed=true ;;
  /chipotle/ingredients) route_allowed=true ;;
  /chipotle/meals) route_allowed=true ;;
  /chipotle/menu) route_allowed=true ;;
  /chipotle/menu/metadata) route_allowed=true ;;
  /chipotle/restaurant) route_allowed=true ;;
  /chipotle/restaurant/meals) route_allowed=true ;;
  /chipotle/restaurant/menu) route_allowed=true ;;
  /chipotle/restaurants) route_allowed=true ;;
  /culvers/calendar) route_allowed=true ;;
  /culvers/categories) route_allowed=true ;;
  /culvers/directory) route_allowed=true ;;
  /culvers/flavor) route_allowed=true ;;
  /culvers/item) route_allowed=true ;;
  /culvers/menu) route_allowed=true ;;
  /culvers/store) route_allowed=true ;;
  /deliveroo/fulfillment-times) route_allowed=true ;;
  /deliveroo/restaurant) route_allowed=true ;;
  /deliveroo/restaurant/menu) route_allowed=true ;;
  /deliveroo/search) route_allowed=true ;;
  /deliveroo/search/filters) route_allowed=true ;;
  /dominos/coupons) route_allowed=true ;;
  /dominos/customization) route_allowed=true ;;
  /dominos/menu) route_allowed=true ;;
  /dominos/nutrition) route_allowed=true ;;
  /dominos/store) route_allowed=true ;;
  /dominos/store-locator) route_allowed=true ;;
  /doordash/explore) route_allowed=true ;;
  /doordash/feed) route_allowed=true ;;
  /doordash/search) route_allowed=true ;;
  /doordash/search/autocomplete) route_allowed=true ;;
  /doordash/search/filters) route_allowed=true ;;
  /doordash/search/items) route_allowed=true ;;
  /dunkin/directory) route_allowed=true ;;
  /dunkin/menu) route_allowed=true ;;
  /dunkin/nearby) route_allowed=true ;;
  /dunkin/store) route_allowed=true ;;
  /fiveguys/directory) route_allowed=true ;;
  /fiveguys/faq) route_allowed=true ;;
  /fiveguys/faq-categories) route_allowed=true ;;
  /fiveguys/menu) route_allowed=true ;;
  /fiveguys/nearby) route_allowed=true ;;
  /fiveguys/nutrition) route_allowed=true ;;
  /fiveguys/ordering-locations) route_allowed=true ;;
  /fiveguys/ordering-menu) route_allowed=true ;;
  /fiveguys/search) route_allowed=true ;;
  /fiveguys/store) route_allowed=true ;;
  /foodpanda/restaurant) route_allowed=true ;;
  /foodpanda/restaurant/menu) route_allowed=true ;;
  /foodpanda/restaurant/reviews) route_allowed=true ;;
  /foodpanda/search) route_allowed=true ;;
  /foodpanda/search/cuisines) route_allowed=true ;;
  /grubhub/availability) route_allowed=true ;;
  /grubhub/offers) route_allowed=true ;;
  /grubhub/restaurant) route_allowed=true ;;
  /grubhub/restaurant/menu) route_allowed=true ;;
  /grubhub/restaurant/reviews) route_allowed=true ;;
  /grubhub/search) route_allowed=true ;;
  /grubhub/timepicker) route_allowed=true ;;
  /instacart/departments) route_allowed=true ;;
  /instacart/item) route_allowed=true ;;
  /instacart/search) route_allowed=true ;;
  /instacart/search-nearby) route_allowed=true ;;
  /instacart/stores) route_allowed=true ;;
  /instacart/trending) route_allowed=true ;;
  /jimmy-johns/menu) route_allowed=true ;;
  /jimmy-johns/modifiers) route_allowed=true ;;
  /jimmy-johns/nearby) route_allowed=true ;;
  /jimmy-johns/sitemap) route_allowed=true ;;
  /jimmy-johns/store) route_allowed=true ;;
  /justeat/restaurant) route_allowed=true ;;
  /justeat/restaurant/menu) route_allowed=true ;;
  /justeat/search) route_allowed=true ;;
  /justeat/search/filters) route_allowed=true ;;
  /kfc/delivery-estimate) route_allowed=true ;;
  /kfc/menu) route_allowed=true ;;
  /kfc/nearby) route_allowed=true ;;
  /kfc/promotion) route_allowed=true ;;
  /kfc/promotions) route_allowed=true ;;
  /kfc/store) route_allowed=true ;;
  /kfc/stores) route_allowed=true ;;
  /kroger/categories) route_allowed=true ;;
  /kroger/category) route_allowed=true ;;
  /kroger/coupons) route_allowed=true ;;
  /kroger/product) route_allowed=true ;;
  /kroger/product/reviews) route_allowed=true ;;
  /kroger/products) route_allowed=true ;;
  /kroger/related-tags) route_allowed=true ;;
  /kroger/search) route_allowed=true ;;
  /kroger/store) route_allowed=true ;;
  /kroger/suggest) route_allowed=true ;;
  /mcdonalds/categories) route_allowed=true ;;
  /mcdonalds/item) route_allowed=true ;;
  /mcdonalds/item-list) route_allowed=true ;;
  /mcdonalds/menu) route_allowed=true ;;
  /mcdonalds/restaurant-menu) route_allowed=true ;;
  /mcdonalds/restaurants) route_allowed=true ;;
  /opentable/restaurant) route_allowed=true ;;
  /opentable/restaurant/menus) route_allowed=true ;;
  /opentable/restaurant/reviews) route_allowed=true ;;
  /opentable/search) route_allowed=true ;;
  /pandamart/search) route_allowed=true ;;
  /pandamart/store) route_allowed=true ;;
  /pandamart/store/categories) route_allowed=true ;;
  /pandamart/store/product) route_allowed=true ;;
  /pandamart/store/products) route_allowed=true ;;
  /pandamart/store/search) route_allowed=true ;;
  /panera/at-work-locations) route_allowed=true ;;
  /panera/cafe) route_allowed=true ;;
  /panera/catering-delivery-info) route_allowed=true ;;
  /panera/catering-menu) route_allowed=true ;;
  /panera/geocode) route_allowed=true ;;
  /panera/item-detail) route_allowed=true ;;
  /panera/item-options) route_allowed=true ;;
  /panera/locations) route_allowed=true ;;
  /panera/menu) route_allowed=true ;;
  /panera/quantity-rules) route_allowed=true ;;
  /panera/retired-products) route_allowed=true ;;
  /panera/time-slots) route_allowed=true ;;
  /panera/upsell-suggestions) route_allowed=true ;;
  /papajohns/allergens) route_allowed=true ;;
  /papajohns/colombia/menu) route_allowed=true ;;
  /papajohns/deals) route_allowed=true ;;
  /papajohns/directory) route_allowed=true ;;
  /papajohns/elsalvador/menu) route_allowed=true ;;
  /papajohns/india/deal) route_allowed=true ;;
  /papajohns/india/menu) route_allowed=true ;;
  /papajohns/india/menu/item) route_allowed=true ;;
  /papajohns/india/stores) route_allowed=true ;;
  /papajohns/intl/deals) route_allowed=true ;;
  /papajohns/intl/ingredients) route_allowed=true ;;
  /papajohns/intl/menu) route_allowed=true ;;
  /papajohns/intl/offer) route_allowed=true ;;
  /papajohns/intl/product) route_allowed=true ;;
  /papajohns/intl/stores) route_allowed=true ;;
  /papajohns/menu) route_allowed=true ;;
  /papajohns/menu/item) route_allowed=true ;;
  /papajohns/nearby) route_allowed=true ;;
  /papajohns/nutrition) route_allowed=true ;;
  /papajohns/peru/menu) route_allowed=true ;;
  /papajohns/poland/menu) route_allowed=true ;;
  /papajohns/russia/menu) route_allowed=true ;;
  /papajohns/store) route_allowed=true ;;
  /pizzahut/bundle-choices) route_allowed=true ;;
  /pizzahut/delivery-estimate) route_allowed=true ;;
  /pizzahut/menu) route_allowed=true ;;
  /pizzahut/modifiers) route_allowed=true ;;
  /pizzahut/store) route_allowed=true ;;
  /pizzahut/stores) route_allowed=true ;;
  /popeyes/faq) route_allowed=true ;;
  /popeyes/location) route_allowed=true ;;
  /popeyes/locations) route_allowed=true ;;
  /popeyes/menu) route_allowed=true ;;
  /popeyes/offers) route_allowed=true ;;
  /popeyes/promotions) route_allowed=true ;;
  /popeyes/quests) route_allowed=true ;;
  /popeyes/rewards) route_allowed=true ;;
  /raisingcanes/directory) route_allowed=true ;;
  /raisingcanes/menu) route_allowed=true ;;
  /raisingcanes/nearby) route_allowed=true ;;
  /raisingcanes/promotion) route_allowed=true ;;
  /raisingcanes/promotions) route_allowed=true ;;
  /raisingcanes/store) route_allowed=true ;;
  /shakeshack/locations) route_allowed=true ;;
  /shakeshack/menu) route_allowed=true ;;
  /shakeshack/nearby) route_allowed=true ;;
  /shakeshack/store) route_allowed=true ;;
  /sonic/availability) route_allowed=true ;;
  /sonic/categories) route_allowed=true ;;
  /sonic/deals) route_allowed=true ;;
  /sonic/directory) route_allowed=true ;;
  /sonic/item) route_allowed=true ;;
  /sonic/location-suggest) route_allowed=true ;;
  /sonic/locations) route_allowed=true ;;
  /sonic/menu) route_allowed=true ;;
  /sonic/nearby) route_allowed=true ;;
  /sonic/nutrition-documents) route_allowed=true ;;
  /sonic/sitemap) route_allowed=true ;;
  /sonic/store) route_allowed=true ;;
  /starbucks/menu) route_allowed=true ;;
  /starbucks/nearest-store) route_allowed=true ;;
  /starbucks/stores) route_allowed=true ;;
  /subway/available-times) route_allowed=true ;;
  /subway/combos) route_allowed=true ;;
  /subway/menu) route_allowed=true ;;
  /subway/nearby) route_allowed=true ;;
  /subway/sitemap) route_allowed=true ;;
  /subway/store) route_allowed=true ;;
  /swiggy/collections) route_allowed=true ;;
  /swiggy/restaurant) route_allowed=true ;;
  /swiggy/restaurant/menu) route_allowed=true ;;
  /swiggy/search) route_allowed=true ;;
  /taco-bell/app-menu) route_allowed=true ;;
  /taco-bell/categories) route_allowed=true ;;
  /taco-bell/menu) route_allowed=true ;;
  /taco-bell/nutrition) route_allowed=true ;;
  /taco-bell/product) route_allowed=true ;;
  /taco-bell/store) route_allowed=true ;;
  /taco-bell/store-menu) route_allowed=true ;;
  /taco-bell/stores) route_allowed=true ;;
  /ubereats/feed) route_allowed=true ;;
  /ubereats/search) route_allowed=true ;;
  /wendys/categories) route_allowed=true ;;
  /wendys/directory) route_allowed=true ;;
  /wendys/item) route_allowed=true ;;
  /wendys/menu) route_allowed=true ;;
  /wendys/nearby) route_allowed=true ;;
  /wendys/nutrition) route_allowed=true ;;
  /wendys/restaurant) route_allowed=true ;;
  /wendys/store) route_allowed=true ;;
  /wendys/store-menu) route_allowed=true ;;
  /wendys/time-slots) route_allowed=true ;;
  /whataburger/sitemap) route_allowed=true ;;
  /whataburger/store) route_allowed=true ;;
  /wingstop/delivery-store) route_allowed=true ;;
  /wingstop/directory) route_allowed=true ;;
  /wingstop/flavors) route_allowed=true ;;
  /wingstop/menu) route_allowed=true ;;
  /wingstop/nearby) route_allowed=true ;;
  /wingstop/store) route_allowed=true ;;
  /wolt/cities) route_allowed=true ;;
  /wolt/collections) route_allowed=true ;;
  /wolt/restaurant) route_allowed=true ;;
  /wolt/restaurant/availability) route_allowed=true ;;
  /wolt/restaurant/menu) route_allowed=true ;;
  /wolt/restaurant/menu/search) route_allowed=true ;;
  /wolt/search) route_allowed=true ;;
  /wolt/search/filters) route_allowed=true ;;
  /yelp/geocode) route_allowed=true ;;
  /yelp/search) route_allowed=true ;;
  /zaxbys/menu) route_allowed=true ;;
  /zaxbys/nearby) route_allowed=true ;;
  /zaxbys/store) route_allowed=true ;;
  /zomato/cities) route_allowed=true ;;
  /zomato/collection) route_allowed=true ;;
  /zomato/collections) route_allowed=true ;;
  /zomato/restaurant) route_allowed=true ;;
  /zomato/restaurant/menu) route_allowed=true ;;
  /zomato/search) route_allowed=true ;;
esac
if [ "$route_allowed" = false ]; then
  route_regexes=(
  '^/doordash/store/[^/]+$'
  '^/doordash/store/[^/]+/fulfillment$'
  '^/doordash/store/[^/]+/info$'
  '^/doordash/store/[^/]+/item/[^/]+$'
  '^/doordash/store/[^/]+/menu$'
  '^/doordash/store/[^/]+/reviews$'
  '^/starbucks/product/[^/]+/[^/]+$'
  '^/starbucks/product/[^/]+/[^/]+/nutrition$'
  '^/ubereats/store/[^/]+$'
  '^/ubereats/store/[^/]+/menu$'
  '^/ubereats/store/[^/]+/reviews$'
  '^/yelp/business/[^/]+$'
  '^/yelp/business/[^/]+/menu$'
  '^/yelp/business/[^/]+/photos$'
  '^/yelp/business/[^/]+/reviews$'
  '^/yelp/business/[^/]+/reviews/highlights$'
  '^/yelp/business/[^/]+/reviews/search$'
  )
  for route_regex in ${route_regexes[@]+"${route_regexes[@]}"}; do
    if [[ "$path" =~ $route_regex ]]; then
      route_allowed=true
      break
    fi
  done
fi
if [ "$route_allowed" = false ]; then
  echo "path is not in the restaurant-food-delivery-research skill catalog" >&2
  exit 2
fi

# Enforce the documented HTTP method for each route, not just the global method set.
route_method_allowed=false
route_method_regexes=(
  '^GET:/7now/catalog$'
  '^GET:/7now/categories$'
  '^GET:/7now/category$'
  '^GET:/7now/combo$'
  '^GET:/7now/combos$'
  '^GET:/7now/deals$'
  '^GET:/7now/offers$'
  '^GET:/7now/popular$'
  '^GET:/7now/product$'
  '^GET:/7now/promotion$'
  '^GET:/7now/search$'
  '^GET:/7now/stores$'
  '^GET:/7now/suggest$'
  '^GET:/arbys/categories$'
  '^GET:/arbys/directory$'
  '^GET:/arbys/location$'
  '^GET:/arbys/locations$'
  '^GET:/arbys/menu$'
  '^GET:/burgerking/availability$'
  '^GET:/burgerking/locations$'
  '^GET:/burgerking/menu$'
  '^GET:/burgerking/product$'
  '^GET:/chick-fil-a/content$'
  '^GET:/chick-fil-a/content-taxonomy$'
  '^GET:/chick-fil-a/faq$'
  '^GET:/chick-fil-a/location$'
  '^GET:/chick-fil-a/locations$'
  '^GET:/chick-fil-a/menu$'
  '^GET:/chick-fil-a/menu-item$'
  '^GET:/chick-fil-a/menu-taxonomy$'
  '^GET:/chipotle/ingredients$'
  '^GET:/chipotle/meals$'
  '^GET:/chipotle/menu$'
  '^GET:/chipotle/menu/metadata$'
  '^GET:/chipotle/restaurant$'
  '^GET:/chipotle/restaurant/meals$'
  '^GET:/chipotle/restaurant/menu$'
  '^GET:/chipotle/restaurants$'
  '^GET:/culvers/calendar$'
  '^GET:/culvers/categories$'
  '^GET:/culvers/directory$'
  '^GET:/culvers/flavor$'
  '^GET:/culvers/item$'
  '^GET:/culvers/menu$'
  '^GET:/culvers/store$'
  '^GET:/deliveroo/fulfillment-times$'
  '^GET:/deliveroo/restaurant$'
  '^GET:/deliveroo/restaurant/menu$'
  '^GET:/deliveroo/search$'
  '^GET:/deliveroo/search/filters$'
  '^GET:/dominos/coupons$'
  '^GET:/dominos/customization$'
  '^GET:/dominos/menu$'
  '^GET:/dominos/nutrition$'
  '^GET:/dominos/store$'
  '^GET:/dominos/store-locator$'
  '^GET:/doordash/explore$'
  '^GET:/doordash/feed$'
  '^GET:/doordash/search$'
  '^GET:/doordash/search/autocomplete$'
  '^GET:/doordash/search/filters$'
  '^GET:/doordash/search/items$'
  '^GET:/doordash/store/[^/]+$'
  '^GET:/doordash/store/[^/]+/fulfillment$'
  '^GET:/doordash/store/[^/]+/info$'
  '^GET:/doordash/store/[^/]+/item/[^/]+$'
  '^GET:/doordash/store/[^/]+/menu$'
  '^GET:/doordash/store/[^/]+/reviews$'
  '^GET:/dunkin/directory$'
  '^GET:/dunkin/menu$'
  '^GET:/dunkin/nearby$'
  '^GET:/dunkin/store$'
  '^GET:/fiveguys/directory$'
  '^GET:/fiveguys/faq$'
  '^GET:/fiveguys/faq-categories$'
  '^GET:/fiveguys/menu$'
  '^GET:/fiveguys/nearby$'
  '^GET:/fiveguys/nutrition$'
  '^GET:/fiveguys/ordering-locations$'
  '^GET:/fiveguys/ordering-menu$'
  '^GET:/fiveguys/search$'
  '^GET:/fiveguys/store$'
  '^GET:/foodpanda/restaurant$'
  '^GET:/foodpanda/restaurant/menu$'
  '^GET:/foodpanda/restaurant/reviews$'
  '^GET:/foodpanda/search$'
  '^GET:/foodpanda/search/cuisines$'
  '^GET:/grubhub/availability$'
  '^GET:/grubhub/offers$'
  '^GET:/grubhub/restaurant$'
  '^GET:/grubhub/restaurant/menu$'
  '^GET:/grubhub/restaurant/reviews$'
  '^GET:/grubhub/search$'
  '^GET:/grubhub/timepicker$'
  '^GET:/instacart/departments$'
  '^GET:/instacart/item$'
  '^GET:/instacart/search$'
  '^GET:/instacart/search-nearby$'
  '^GET:/instacart/stores$'
  '^GET:/instacart/trending$'
  '^GET:/jimmy-johns/menu$'
  '^GET:/jimmy-johns/modifiers$'
  '^GET:/jimmy-johns/nearby$'
  '^GET:/jimmy-johns/sitemap$'
  '^GET:/jimmy-johns/store$'
  '^GET:/justeat/restaurant$'
  '^GET:/justeat/restaurant/menu$'
  '^GET:/justeat/search$'
  '^GET:/justeat/search/filters$'
  '^GET:/kfc/delivery-estimate$'
  '^GET:/kfc/menu$'
  '^GET:/kfc/nearby$'
  '^GET:/kfc/promotion$'
  '^GET:/kfc/promotions$'
  '^GET:/kfc/store$'
  '^GET:/kfc/stores$'
  '^GET:/kroger/categories$'
  '^GET:/kroger/category$'
  '^GET:/kroger/coupons$'
  '^GET:/kroger/product$'
  '^GET:/kroger/product/reviews$'
  '^GET:/kroger/products$'
  '^GET:/kroger/related-tags$'
  '^GET:/kroger/search$'
  '^GET:/kroger/store$'
  '^GET:/kroger/suggest$'
  '^GET:/mcdonalds/categories$'
  '^GET:/mcdonalds/item$'
  '^GET:/mcdonalds/item-list$'
  '^GET:/mcdonalds/menu$'
  '^GET:/mcdonalds/restaurant-menu$'
  '^GET:/mcdonalds/restaurants$'
  '^GET:/opentable/restaurant$'
  '^GET:/opentable/restaurant/menus$'
  '^GET:/opentable/restaurant/reviews$'
  '^GET:/opentable/search$'
  '^GET:/pandamart/search$'
  '^GET:/pandamart/store$'
  '^GET:/pandamart/store/categories$'
  '^GET:/pandamart/store/product$'
  '^GET:/pandamart/store/products$'
  '^GET:/pandamart/store/search$'
  '^GET:/panera/at-work-locations$'
  '^GET:/panera/cafe$'
  '^GET:/panera/catering-delivery-info$'
  '^GET:/panera/catering-menu$'
  '^GET:/panera/geocode$'
  '^GET:/panera/item-detail$'
  '^GET:/panera/item-options$'
  '^GET:/panera/locations$'
  '^GET:/panera/menu$'
  '^GET:/panera/quantity-rules$'
  '^GET:/panera/retired-products$'
  '^GET:/panera/time-slots$'
  '^GET:/panera/upsell-suggestions$'
  '^GET:/papajohns/allergens$'
  '^GET:/papajohns/colombia/menu$'
  '^GET:/papajohns/deals$'
  '^GET:/papajohns/directory$'
  '^GET:/papajohns/elsalvador/menu$'
  '^GET:/papajohns/india/deal$'
  '^GET:/papajohns/india/menu$'
  '^GET:/papajohns/india/menu/item$'
  '^GET:/papajohns/india/stores$'
  '^GET:/papajohns/intl/deals$'
  '^GET:/papajohns/intl/ingredients$'
  '^GET:/papajohns/intl/menu$'
  '^GET:/papajohns/intl/offer$'
  '^GET:/papajohns/intl/product$'
  '^GET:/papajohns/intl/stores$'
  '^GET:/papajohns/menu$'
  '^GET:/papajohns/menu/item$'
  '^GET:/papajohns/nearby$'
  '^GET:/papajohns/nutrition$'
  '^GET:/papajohns/peru/menu$'
  '^GET:/papajohns/poland/menu$'
  '^GET:/papajohns/russia/menu$'
  '^GET:/papajohns/store$'
  '^GET:/pizzahut/bundle-choices$'
  '^GET:/pizzahut/delivery-estimate$'
  '^GET:/pizzahut/menu$'
  '^GET:/pizzahut/modifiers$'
  '^GET:/pizzahut/store$'
  '^GET:/pizzahut/stores$'
  '^GET:/popeyes/faq$'
  '^GET:/popeyes/location$'
  '^GET:/popeyes/locations$'
  '^GET:/popeyes/menu$'
  '^GET:/popeyes/offers$'
  '^GET:/popeyes/promotions$'
  '^GET:/popeyes/quests$'
  '^GET:/popeyes/rewards$'
  '^GET:/raisingcanes/directory$'
  '^GET:/raisingcanes/menu$'
  '^GET:/raisingcanes/nearby$'
  '^GET:/raisingcanes/promotion$'
  '^GET:/raisingcanes/promotions$'
  '^GET:/raisingcanes/store$'
  '^GET:/shakeshack/locations$'
  '^GET:/shakeshack/menu$'
  '^GET:/shakeshack/nearby$'
  '^GET:/shakeshack/store$'
  '^GET:/sonic/availability$'
  '^GET:/sonic/categories$'
  '^GET:/sonic/deals$'
  '^GET:/sonic/directory$'
  '^GET:/sonic/item$'
  '^GET:/sonic/location-suggest$'
  '^GET:/sonic/locations$'
  '^GET:/sonic/menu$'
  '^GET:/sonic/nearby$'
  '^GET:/sonic/nutrition-documents$'
  '^GET:/sonic/sitemap$'
  '^GET:/sonic/store$'
  '^GET:/starbucks/menu$'
  '^GET:/starbucks/nearest-store$'
  '^GET:/starbucks/product/[^/]+/[^/]+$'
  '^GET:/starbucks/stores$'
  '^GET:/subway/available-times$'
  '^GET:/subway/combos$'
  '^GET:/subway/menu$'
  '^GET:/subway/nearby$'
  '^GET:/subway/sitemap$'
  '^GET:/subway/store$'
  '^GET:/swiggy/collections$'
  '^GET:/swiggy/restaurant$'
  '^GET:/swiggy/restaurant/menu$'
  '^GET:/swiggy/search$'
  '^GET:/taco-bell/app-menu$'
  '^GET:/taco-bell/categories$'
  '^GET:/taco-bell/menu$'
  '^GET:/taco-bell/nutrition$'
  '^GET:/taco-bell/product$'
  '^GET:/taco-bell/store$'
  '^GET:/taco-bell/store-menu$'
  '^GET:/taco-bell/stores$'
  '^GET:/ubereats/feed$'
  '^GET:/ubereats/search$'
  '^GET:/ubereats/store/[^/]+$'
  '^GET:/ubereats/store/[^/]+/menu$'
  '^GET:/ubereats/store/[^/]+/reviews$'
  '^GET:/wendys/categories$'
  '^GET:/wendys/directory$'
  '^GET:/wendys/item$'
  '^GET:/wendys/menu$'
  '^GET:/wendys/nearby$'
  '^GET:/wendys/nutrition$'
  '^GET:/wendys/restaurant$'
  '^GET:/wendys/store$'
  '^GET:/wendys/store-menu$'
  '^GET:/wendys/time-slots$'
  '^GET:/whataburger/sitemap$'
  '^GET:/whataburger/store$'
  '^GET:/wingstop/delivery-store$'
  '^GET:/wingstop/directory$'
  '^GET:/wingstop/flavors$'
  '^GET:/wingstop/menu$'
  '^GET:/wingstop/nearby$'
  '^GET:/wingstop/store$'
  '^GET:/wolt/cities$'
  '^GET:/wolt/collections$'
  '^GET:/wolt/restaurant$'
  '^GET:/wolt/restaurant/availability$'
  '^GET:/wolt/restaurant/menu$'
  '^GET:/wolt/restaurant/menu/search$'
  '^GET:/wolt/search$'
  '^GET:/wolt/search/filters$'
  '^GET:/yelp/business/[^/]+$'
  '^GET:/yelp/business/[^/]+/menu$'
  '^GET:/yelp/business/[^/]+/photos$'
  '^GET:/yelp/business/[^/]+/reviews$'
  '^GET:/yelp/business/[^/]+/reviews/highlights$'
  '^GET:/yelp/business/[^/]+/reviews/search$'
  '^GET:/yelp/geocode$'
  '^GET:/yelp/search$'
  '^GET:/zaxbys/menu$'
  '^GET:/zaxbys/nearby$'
  '^GET:/zaxbys/store$'
  '^GET:/zomato/cities$'
  '^GET:/zomato/collection$'
  '^GET:/zomato/collections$'
  '^GET:/zomato/restaurant$'
  '^GET:/zomato/restaurant/menu$'
  '^GET:/zomato/search$'
  '^POST:/starbucks/product/[^/]+/[^/]+/nutrition$'
)
for route_method_regex in ${route_method_regexes[@]+"${route_method_regexes[@]}"}; do
  if [[ "$method:$path" =~ $route_method_regex ]]; then
    route_method_allowed=true
    break
  fi
done
if [ "$route_method_allowed" = false ]; then
  echo "method is not allowed for this restaurant-food-delivery-research route" >&2
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
