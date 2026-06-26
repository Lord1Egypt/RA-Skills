#!/bin/bash
# SEO Audit Bot - Quick Audit Script
# Usage: ./audit.sh <url>
# This script fetches key SEO signals for a given URL

URL=$1

if [ -z "$URL" ]; then
  echo "Usage: ./audit.sh <url>"
  exit 1
fi

echo "=== SEO AUDIT: $URL ==="
echo ""

# Fetch main page
echo "--- MAIN PAGE ---"
HTTP_CODE=$(curl -s -o /tmp/seo_page.html -w "%{http_code}" -L "$URL" 2>/dev/null)
echo "HTTP Status: $HTTP_CODE"

if [ "$HTTP_CODE" -ge 200 ] && [ "$HTTP_CODE" -lt 400 ]; then
  # Title
  TITLE=$(grep -oi '<title[^>]*>.*</title>' /tmp/seo_page.html | sed 's/<[^>]*>//g' | head -1)
  TITLE_LEN=${#TITLE}
  echo "Title: $TITLE"
  echo "Title Length: $TITLE_LEN chars"

  # Meta description
  META_DESC=$(grep -oi '<meta[^>]*name="description"[^>]*content="[^"]*"' /tmp/seo_page.html | sed 's/.*content="//;s/"//' | head -1)
  META_LEN=${#META_DESC}
  echo "Meta Description: ${META_DESC:-(none)}"
  echo "Meta Description Length: $META_LEN chars"

  # H1
  H1=$(grep -oi '<h1[^>]*>.*</h1>' /tmp/seo_page.html | sed 's/<[^>]*>//g' | head -1)
  echo "H1: ${H1:-(none)}"

  # H2 count
  H2_COUNT=$(grep -oi '<h2' /tmp/seo_page.html | wc -l)
  echo "H2 count: $H2_COUNT"

  # Images without alt
  IMG_TOTAL=$(grep -oi '<img' /tmp/seo_page.html | wc -l)
  IMG_NO_ALT=$(grep -oi '<img[^>]*>' /tmp/seo_page.html | grep -iv 'alt=' | wc -l)
  echo "Images: $IMG_TOTAL total, $IMG_NO_ALT without alt"

  # Word count (rough)
  WORD_COUNT=$(sed 's/<[^>]*>//g' /tmp/seo_page.html | wc -w)
  echo "Word count (approx): $WORD_COUNT"

  # Canonical
  CANONICAL=$(grep -oi '<link[^>]*rel="canonical"[^>]*href="[^"]*"' /tmp/seo_page.html | sed 's/.*href="//;s/"//' | head -1)
  echo "Canonical: ${CANONICAL:-(none)}"

  # Viewport
  VIEWPORT=$(grep -oi '<meta[^>]*name="viewport"' /tmp/seo_page.html | head -1)
  echo "Viewport: ${VIEWPORT:+✅ present}${VIEWPORT:-(none)}"

  # Open Graph
  OG_COUNT=$(grep -oi 'og:' /tmp/seo_page.html | wc -l)
  echo "Open Graph tags: $OG_COUNT"

  # Twitter Cards
  TWITTER_COUNT=$(grep -oi 'twitter:' /tmp/seo_page.html | wc -l)
  echo "Twitter Card tags: $TWITTER_COUNT"

  # JSON-LD
  JSONLD=$(grep -oi '<script[^>]*type="application/ld+json"' /tmp/seo_page.html | wc -l)
  echo "JSON-LD schemas: $JSONLD"
else
  echo "ERROR: Could not fetch page (HTTP $HTTP_CODE)"
fi

echo ""
echo "--- ROBOTS.TXT ---"
ROBOTS_CODE=$(curl -s -o /tmp/seo_robots.txt -w "%{http_code}" "$URL/robots.txt" 2>/dev/null)
if [ "$ROBOTS_CODE" = "200" ]; then
  echo "Status: ✅ Found"
  cat /tmp/seo_robots.txt | head -20
else
  echo "Status: ❌ Not found (HTTP $ROBOTS_CODE)"
fi

echo ""
echo "--- SITEMAP.XML ---"
SITEMAP_CODE=$(curl -s -o /tmp/seo_sitemap.xml -w "%{http_code}" "$URL/sitemap.xml" 2>/dev/null)
if [ "$SITEMAP_CODE" = "200" ]; then
  echo "Status: ✅ Found"
  SITEMAP_URLS=$(grep -oi '<loc>' /tmp/seo_sitemap.xml | wc -l)
  echo "URLs in sitemap: $SITEMAP_URLS"
else
  echo "Status: ❌ Not found (HTTP $SITEMAP_CODE)"
fi

echo ""
echo "=== AUDIT COMPLETE ==="
