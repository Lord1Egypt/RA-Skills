#!/usr/bin/env bash
#
# seo-reporter/audit.sh — SEO audit for a single URL
# Usage: ./audit.sh "https://example.com"
#

set -uo pipefail

# ── Colors ────────────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
BOLD='\033[1m'
RESET='\033[0m'

# ── Helpers ───────────────────────────────────────────────────────────────────
log()  { echo -e "${CYAN}[audit]${RESET} $*"; }
pass() { echo -e "${GREEN}✅ $*${RESET}"; }
warn() { echo -e "${YELLOW}⚠️  $*${RESET}"; }
fail() { echo -e "${RED}❌ $*${RESET}"; }

# Strip HTML tags (collapse whitespace)
strip_tags() {
  sed 's/<[^>]*>//g' | tr -s ' \t\n\r' ' ' | sed 's/^ //;s/ $//'
}

# Extract meta content attribute value
meta_content() {
  local name="$1"
  grep -i "name=['\"]${name}['\"]"   <<<"$HTML" | grep -o "content=['\"][^'\"]*['\"]" | sed 's/content=['\''"]//;s/['\''"]$//' | head -1 || true
}

# Extract property-based meta (og: etc)
meta_property() {
  local prop="$1"
  grep -i "property=['\"]${prop}['\"]" <<<"$HTML" | grep -o "content=['\"][^'\"]*['\"]" | sed 's/content=['\''"]//;s/['\''"]$//' | head -1 || true
}

# ── Args ───────────────────────────────────────────────────────────────────────
if [[ $# -lt 1 ]]; then
  echo "Usage: $0 \"https://example.com\""
  exit 1
fi

TARGET_URL="$1"

# Normalize URL (add https if missing)
if [[ ! "$TARGET_URL" =~ ^https?:// ]]; then
  TARGET_URL="https://${TARGET_URL}"
fi

DATE=$(date +%Y-%m-%d)
TMPDIR=$(mktemp -d)
HTML="${TMPDIR}/page.html"
HEADERS="${TMPDIR}/headers.txt"

log "Auditing: ${TARGET_URL}"

# ── Fetch ─────────────────────────────────────────────────────────────────────
HTTP_CODE=$(curl -s -o "$HTML" -D "$HEADERS" -L -A "seo-reporter/1.0" \
  -w "%{http_code}" --max-time 20 "$TARGET_URL" 2>/dev/null || echo "000")

if [[ "$HTTP_CODE" == "000" ]]; then
  echo "❌ Error: Could not reach ${TARGET_URL} — host unreachable or timeout."
  exit 1
fi

if [[ "$HTTP_CODE" == "4"* ]] || [[ "$HTTP_CODE" == "5"* ]]; then
  echo "❌ Error: Server returned HTTP ${HTTP_CODE}"
  exit 1
fi

log "Fetched (HTTP ${HTTP_CODE}), $(wc -c < "$HTML") bytes"

# ── Extract raw HTML content for analysis ────────────────────────────────────
# Downcase for grep safety
HTML_LOWER=$(tr '[:upper:]' '[:lower:]' < "$HTML")

# ── Arrays for findings ────────────────────────────────────────────────────────
declare -a TITLE_FINDINGS=() TITLE_STATUS=""
declare -a META_DESC_FINDINGS=() META_DESC_STATUS=""
declare -a H1_FINDINGS=() H1_STATUS=""
declare -a HEADING_STRUCT_FINDINGS=() HEADING_STRUCT_STATUS=""
declare -a CANONICAL_FINDINGS=() CANONICAL_STATUS=""
declare -a ROBOTS_FINDINGS=() ROBOTS_STATUS=""
declare -a SITEMAP_FINDINGS=() SITEMAP_STATUS=""
declare -a OG_FINDINGS=() OG_STATUS=""
declare -a VIEWPORT_FINDINGS=() VIEWPORT_STATUS=""
declare -a HTTPS_FINDINGS=() HTTPS_STATUS=""

# ── Derived URLs ──────────────────────────────────────────────────────────────
DOMAIN=$(echo "$TARGET_URL" | sed -E 's|https?://([^/]+).*|\1|')
PROTOCOL=$(echo "$TARGET_URL" | sed -E 's|(https?)://.*|\1|')
BASE_URL="${PROTOCOL}://${DOMAIN}"

ROBOTS_URL="${BASE_URL}/robots.txt"
SITEMAP_URL="${BASE_URL}/sitemap.xml"

# ── 1. Title Tag ───────────────────────────────────────────────────────────────
TITLE_RAW=$(grep -oi '<title>[^<]*</title>' "$HTML" | head -1 | strip_tags || true)
TITLE_LEN=${#TITLE_RAW}

if [[ -z "$TITLE_RAW" ]]; then
  TITLE_SCORE=0
  TITLE_STATUS="❌ Fail"
  TITLE_FINDINGS+=("Missing title tag — search engines have no page title.")
else
  TITLE_SCORE=10
  TITLE_STATUS="✅ Pass"
  if [[ $TITLE_LEN -lt 30 ]]; then
    TITLE_SCORE=7
    TITLE_STATUS="⚠️ Warning"
    TITLE_FINDINGS+=("Title is too short (${TITLE_LEN} chars). Aim for 50-60 characters.")
  elif [[ $TITLE_LEN -gt 60 ]]; then
    TITLE_SCORE=7
    TITLE_STATUS="⚠️ Warning"
    TITLE_FINDINGS+=("Title is too long (${TITLE_LEN} chars). It may be truncated in search results (optimal: 50-60 chars).")
  else
    TITLE_FINDINGS+=("Title length is optimal (${TITLE_LEN} chars).")
  fi
fi

# ── 2. Meta Description ───────────────────────────────────────────────────────
META_DESC=$(meta_content "description")
META_DESC_LEN=${#META_DESC}

if [[ -z "$META_DESC" ]]; then
  META_DESC_SCORE=0
  META_DESC_STATUS="❌ Fail"
  META_DESC_FINDINGS+=("Missing meta description — search engines will auto-generate snippet, losing control over search listings.")
else
  META_DESC_SCORE=10
  META_DESC_STATUS="✅ Pass"
  if [[ $META_DESC_LEN -lt 120 ]]; then
    META_DESC_SCORE=7
    META_DESC_STATUS="⚠️ Warning"
    META_DESC_FINDINGS+=("Meta description is too short (${META_DESC_LEN} chars). Aim for 150-160 characters.")
  elif [[ $META_DESC_LEN -gt 200 ]]; then
    META_DESC_SCORE=7
    META_DESC_STATUS="⚠️ Warning"
    META_DESC_FINDINGS+=("Meta description is too long (${META_DESC_LEN} chars). It may be truncated (optimal: 150-160 chars).")
  else
    META_DESC_FINDINGS+=("Meta description length is good (${META_DESC_LEN} chars).")
  fi
fi

# ── 3. H1 Heading ──────────────────────────────────────────────────────────────
H1_COUNT=$(grep -oi '<h1[^>]*>[^<]*</h1>' "$HTML" | wc -l || true)
H1_FIRST=$(grep -oi '<h1[^>]*>[^<]*</h1>' "$HTML" | head -1 | strip_tags || true)
H1_LEN=${#H1_FIRST}

if [[ "$H1_COUNT" -eq 0 ]]; then
  H1_SCORE=0
  H1_STATUS="❌ Fail"
  H1_FINDINGS+=("No H1 heading found — every page needs exactly one H1.")
elif [[ "$H1_COUNT" -gt 1 ]]; then
  H1_SCORE=5
  H1_STATUS="⚠️ Warning"
  H1_FINDINGS+=("${H1_COUNT} H1 tags found — only one H1 per page is recommended.")
else
  H1_SCORE=10
  H1_STATUS="✅ Pass"
  if [[ $H1_LEN -lt 10 ]]; then
    H1_SCORE=8
    H1_STATUS="⚠️ Warning"
    H1_FINDINGS+=("H1 exists but is very short (${H1_LEN} chars). Ensure it describes the page topic clearly.")
  else
    H1_FINDINGS+=("Exactly one H1 found: \"${H1_FIRST:0:60}...\"")
  fi
fi

# ── 4. Heading Structure (H1→H2→H3 hierarchy) ──────────────────────────────────
H2_COUNT=$(grep -oi '<h2[^>]*>[^<]*</h2>' "$HTML" | wc -l || true)
H3_COUNT=$(grep -oi '<h3[^>]*>[^<]*</h3>' "$HTML" | wc -l || true)
H4_COUNT=$(grep -oi '<h4[^>]*>[^<]*</h4>' "$HTML" | wc -l || true)
H5_COUNT=$(grep -oi '<h5[^>]*>[^<]*</h5>' "$HTML" | wc -l || true)
H6_COUNT=$(grep -oi '<h6[^>]*>[^<]*</h6>' "$HTML" | wc -l || true)

HEADING_STRUCT_SCORE=10
HEADING_STRUCT_STATUS="✅ Pass"
HEADING_STRUCT_FINDINGS=()

# Check for skip levels (e.g., H1 directly to H4)
if [[ "$H1_COUNT" -gt 0 ]] && [[ "$H2_COUNT" -eq 0 ]] && [[ "$H3_COUNT" -gt 0 ]]; then
  HEADING_STRUCT_SCORE=6
  HEADING_STRUCT_STATUS="⚠️ Warning"
  HEADING_STRUCT_FINDINGS+=("Heading hierarchy has a gap: H1 → H3 with no H2. Use H2 for major sections.")
fi

if [[ "$H2_COUNT" -gt 20 ]]; then
  HEADING_STRUCT_SCORE=$(( HEADING_STRUCT_SCORE < 8 ? HEADING_STRUCT_SCORE : 8 ))
  [[ "$HEADING_STRUCT_SCORE" -lt 10 ]] && HEADING_STRUCT_STATUS="⚠️ Warning"
  HEADING_STRUCT_FINDINGS+=("Page has ${H2_COUNT} H2 headings — verify each represents a distinct section.")
fi

HEADING_STRUCT_FINDINGS+=("Heading counts — H1:${H1_COUNT} H2:${H2_COUNT} H3:${H3_COUNT} H4:${H4_COUNT} H5:${H5_COUNT} H6:${H6_COUNT}.")

# ── 5. Canonical Tag ──────────────────────────────────────────────────────────
CANONICAL=$(grep -oi '<link[^>]*rel=["\x27]canonical["\x27][^>]*>' "$HTML" | grep -o "href=['\"][^'\"]*['\"]" | sed 's/href=['\''"]//;s/['\''"]$//' | head -1 || true)

if [[ -z "$CANONICAL" ]]; then
  CANONICAL_SCORE=0
  CANONICAL_STATUS="❌ Fail"
  CANONICAL_FINDINGS+=("No canonical tag found — search engines may index duplicate versions of this page.")
else
  CANONICAL_SCORE=10
  CANONICAL_STATUS="✅ Pass"
  CANONICAL_FINDINGS+=("Canonical set to: ${CANONICAL}")
  # Check if canonical matches target
  CANONICAL_NORM=$(echo "$CANONICAL" | sed -E 's|/+$||' | tr -d 'www.')
  TARGET_NORM=$(echo "$TARGET_URL" | sed -E 's|/+$||' | tr -d 'www.')
  if [[ "$CANONICAL_NORM" != "$TARGET_NORM" ]]; then
    CANONICAL_SCORE=6
    CANONICAL_STATUS="⚠️ Warning"
    CANONICAL_FINDINGS+=("Canonical (${CANONICAL}) differs from the URL being audited (${TARGET_URL}). Verify this is intentional (e.g., redirected domain).")
  fi
fi

# ── 6. Robots.txt ─────────────────────────────────────────────────────────────
ROBOTS_STATUS_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$ROBOTS_URL" 2>/dev/null || echo "000")
ROBOTS_CONTENT=$(curl -s --max-time 10 "$ROBOTS_URL" 2>/dev/null || echo "")

if [[ "$ROBOTS_STATUS_CODE" == "404" ]]; then
  ROBOTS_SCORE=3
  ROBOTS_STATUS="❌ Fail"
  ROBOTS_FINDINGS+=("No robots.txt found at ${ROBOTS_URL} — search engines have no crawl directiven.")
elif [[ "$ROBOTS_STATUS_CODE" != "200" ]]; then
  ROBOTS_SCORE=4
  ROBOTS_STATUS="⚠️ Warning"
  ROBOTS_FINDINGS+=("robots.txt returned HTTP ${ROBOTS_STATUS_CODE} — it may be inaccessible to crawlers.")
else
  ROBOTS_SCORE=10
  ROBOTS_STATUS="✅ Pass"
  ROBOTS_FINDINGS+=("robots.txt is accessible.")
  # Check if it blocks the target URL
  DOMAIN_ESCAPED=$(echo "$DOMAIN" | sed 's/\./\\./g')
  if echo "$ROBOTS_CONTENT" | grep -qi "disallow.*${DOMAIN_ESCAPED}"; then
    ROBOTS_SCORE=6
    ROBOTS_STATUS="⚠️ Warning"
    ROBOTS_FINDINGS+=("robots.txt may be blocking the domain or URL — verify Disallow directives are intentional.")
  fi
fi

# ── 7. Sitemap.xml ────────────────────────────────────────────────────────────
SITEMAP_STATUS_CODE=$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$SITEMAP_URL" 2>/dev/null || echo "000")
SITEMAP_CONTENT=$(curl -s --max-time 15 "$SITEMAP_URL" 2>/dev/null || echo "")

if [[ "$SITEMAP_STATUS_CODE" == "404" ]]; then
  # Try common alternatives
  SITEMAP_ALTS=(
    "${BASE_URL}/sitemap-index.xml"
    "${BASE_URL}/sitemap_index.xml"
    "${BASE_URL}/sitemap/index.xml"
  )
  FOUND_SITEMAP=""
  for ALT in "${SITEMAP_ALTS[@]}"; do
    if [[ $(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "$ALT" 2>/dev/null || echo "000") == "200" ]]; then
      FOUND_SITEMAP="$ALT"
      break
    fi
  done

  if [[ -n "$FOUND_SITEMAP" ]]; then
    SITEMAP_SCORE=8
    SITEMAP_STATUS="⚠️ Warning"
    SITEMAP_URL="$FOUND_SITEMAP"
    SITEMAP_FINDINGS+=("Default sitemap.xml not found, but alternate ${SITEMAP_URL} exists. Update robots.txt to reference the correct path.")
  else
    SITEMAP_SCORE=3
    SITEMAP_STATUS="❌ Fail"
    SITEMAP_FINDINGS+=("No sitemap.xml found at ${SITEMAP_URL} — a sitemap helps search engines discover and index pages efficiently.")
  fi
elif [[ "$SITEMAP_STATUS_CODE" != "200" ]]; then
  SITEMAP_SCORE=4
  SITEMAP_STATUS="⚠️ Warning"
  SITEMAP_FINDINGS+=("sitemap.xml returned HTTP ${SITEMAP_STATUS_CODE} — it may be inaccessible to crawlers.")
else
  SITEMAP_SCORE=10
  SITEMAP_STATUS="✅ Pass"
  SITEMAP_FINDINGS+=("sitemap.xml is accessible at ${SITEMAP_URL}.")

  # Check if audited URL is in sitemap
  if echo "$SITEMAP_CONTENT" | grep -qi "$TARGET_URL"; then
    SITEMAP_FINDINGS+=("Target URL is included in the sitemap.")
  else
    SITEMAP_SCORE=$(( SITEMAP_SCORE > 7 ? 7 : SITEMAP_SCORE ))
    SITEMAP_STATUS="⚠️ Warning"
    SITEMAP_FINDINGS+=("Target URL was not found in the sitemap — verify the page should be indexed.")
  fi
fi

# ── 8. Open Graph Tags ────────────────────────────────────────────────────────
OG_TITLE=$(meta_property "og:title")
OG_DESC=$(meta_property "og:description")
OG_IMAGE=$(meta_property "og:image")
OG_URL=$(meta_property "og:url")

OG_MISSING=()
[[ -z "$OG_TITLE" ]]  && OG_MISSING+=("og:title")
[[ -z "$OG_DESC" ]]   && OG_MISSING+=("og:description")
[[ -z "$OG_IMAGE" ]]  && OG_MISSING+=("og:image")

if [[ ${#OG_MISSING[@]} -eq 0 ]]; then
  OG_SCORE=10
  OG_STATUS="✅ Pass"
  OG_FINDINGS+=("All key Open Graph tags present (og:title, og:description, og:image).")
else
  OG_SCORE=$(( 10 - ${#OG_MISSING[@]} * 3 ))
  [[ $OG_SCORE -lt 0 ]] && OG_SCORE=0
  if [[ $OG_SCORE -ge 7 ]]; then
    OG_STATUS="⚠️ Warning"
  else
    OG_STATUS="❌ Fail"
  fi
  OG_FINDINGS+=("Missing Open Graph tags: ${OG_MISSING[*]} — social sharing will lack rich previews.")
fi

# ── 9. Mobile Viewport ─────────────────────────────────────────────────────────
VIEWPORT=$(meta_content "viewport")
if [[ -z "$VIEWPORT" ]]; then
  VIEWPORT_SCORE=3
  VIEWPORT_STATUS="❌ Fail"
  VIEWPORT_FINDINGS+=("No viewport meta tag — page may render poorly on mobile devices, impacting mobile rankings.")
else
  VIEWPORT_SCORE=10
  VIEWPORT_STATUS="✅ Pass"
  VIEWPORT_FINDINGS+=("Viewport meta tag present: ${VIEWPORT}")
fi

# ── 10. HTTPS ──────────────────────────────────────────────────────────────────
if [[ "$PROTOCOL" == "https" ]]; then
  HTTPS_SCORE=10
  HTTPS_STATUS="✅ Pass"
  HTTPS_FINDINGS+=("Page served over HTTPS.")
else
  HTTPS_SCORE=0
  HTTPS_STATUS="❌ Fail"
  HTTPS_FINDINGS+=("Page is NOT served over HTTPS — security and SEO impact. Migrate to HTTPS.")
fi

# ── Score totals ──────────────────────────────────────────────────────────────
TOTAL=$(( TITLE_SCORE + META_DESC_SCORE + H1_SCORE + HEADING_STRUCT_SCORE + \
          CANONICAL_SCORE + ROBOTS_SCORE + SITEMAP_SCORE + OG_SCORE + \
          VIEWPORT_SCORE + HTTPS_SCORE ))
MAX_SCORE=100
PERCENT=$(( TOTAL * 100 / MAX_SCORE ))

# Overall status
if [[ $PERCENT -ge 90 ]]; then
  OVERALL="🌟 Excellent"
elif [[ $PERCENT -ge 75 ]]; then
  OVERALL="✅ Good"
elif [[ $PERCENT -ge 50 ]]; then
  OVERALL="⚠️ Needs Work"
else
  OVERALL="❌ Poor"
fi

# ── Generate Markdown Report ──────────────────────────────────────────────────
cat <<REPORT
# 🔍 SEO Audit Report

**Date:** ${DATE}  
**URL:** ${TARGET_URL}  
**HTTP Status:** ${HTTP_CODE}

---

## Scores

| Factor | Score | Status |
|--------|-------|--------|
| Title Tag | ${TITLE_SCORE}/10 | ${TITLE_STATUS} |
| Meta Description | ${META_DESC_SCORE}/10 | ${META_DESC_STATUS} |
| H1 Heading | ${H1_SCORE}/10 | ${H1_STATUS} |
| Heading Structure | ${HEADING_STRUCT_SCORE}/10 | ${HEADING_STRUCT_STATUS} |
| Canonical Tag | ${CANONICAL_SCORE}/10 | ${CANONICAL_STATUS} |
| Robots.txt | ${ROBOTS_SCORE}/10 | ${ROBOTS_STATUS} |
| Sitemap.xml | ${SITEMAP_SCORE}/10 | ${SITEMAP_STATUS} |
| Open Graph Tags | ${OG_SCORE}/10 | ${OG_STATUS} |
| Mobile Viewport | ${VIEWPORT_SCORE}/10 | ${VIEWPORT_STATUS} |
| HTTPS | ${HTTPS_SCORE}/10 | ${HTTPS_STATUS} |

**Overall Score: ${TOTAL}/${MAX_SCORE} (${PERCENT}%) — ${OVERALL}**

---

## Title Tag

**Current:** ${TITLE_RAW:-"<missing>"}

$(for f in "${TITLE_FINDINGS[@]:-}"; do echo "- $f"; done)

---

## Meta Description

**Current:** ${META_DESC:-"<missing>"}

$(for f in "${META_DESC_FINDINGS[@]:-}"; do echo "- $f"; done)

---

## H1 & Heading Structure

**First H1:** ${H1_FIRST:-"<missing>"}

$(for f in "${H1_FINDINGS[@]:-}"; do echo "- $f"; done)
$(for f in "${HEADING_STRUCT_FINDINGS[@]:-}"; do echo "- $f"; done)

---

## Canonical Tag

**Canonical:** ${CANONICAL:-"<not set>"}

$(for f in "${CANONICAL_FINDINGS[@]:-}"; do echo "- $f"; done)

---

## Robots.txt

**URL checked:** ${ROBOTS_URL}  
**HTTP response:** ${ROBOTS_STATUS_CODE}

$(for f in "${ROBOTS_FINDINGS[@]:-}"; do echo "- $f"; done)

---

## Sitemap.xml

**URL checked:** ${SITEMAP_URL}  
**HTTP response:** ${SITEMAP_STATUS_CODE}

$(for f in "${SITEMAP_FINDINGS[@]:-}"; do echo "- $f"; done)

---

## Open Graph Tags

| Tag | Value |
|-----|-------|
| og:title | ${OG_TITLE:-"<missing>"} |
| og:description | ${OG_DESC:-"<missing>"} |
| og:image | ${OG_IMAGE:-"<missing>"} |
| og:url | ${OG_URL:-"<not set>"} |

$(for f in "${OG_FINDINGS[@]:-}"; do echo "- $f"; done)

---

## Mobile Viewport

**Current:** ${VIEWPORT:-"<missing>"}

$(for f in "${VIEWPORT_FINDINGS[@]:-}"; do echo "- $f"; done)

---

## HTTPS

**Protocol:** ${PROTOCOL}

$(for f in "${HTTPS_FINDINGS[@]:-}"; do echo "- $f"; done)

---

## Recommendations

1. **Title tag** — $(if [[ "$TITLE_SCORE" -lt 10 ]]; then
     if [[ -z "$TITLE_RAW" ]]; then echo "Add a descriptive title tag between 50-60 characters.";
     elif [[ $TITLE_LEN -lt 50 ]]; then echo "Expand the title to 50-60 characters with primary keyword near the start.";
     else echo "Trim the title to 50-60 characters so it doesn't get truncated in SERPs."; fi
   else echo "Title is well-optimized."; fi)

2. **Meta description** — $(if [[ "$META_DESC_SCORE" -lt 10 ]]; then
     if [[ -z "$META_DESC" ]]; then echo "Write a unique meta description of 150-160 characters that includes the primary keyword and a call-to-action.";
     else echo "Refine the meta description to 150-160 characters, front-loading the keyword and value proposition."; fi
   else echo "Meta description is well-written."; fi)

3. **H1 heading** — $(if [[ "$H1_COUNT" -eq 0 ]]; then echo "Add a single H1 that clearly describes the page topic, ideally with the primary keyword.";
                       elif [[ "$H1_COUNT" -gt 1 ]]; then echo "Consolidate to one H1 — move secondary headings to H2.";
                       else echo "H1 is correct."; fi)

4. **Canonical tag** — $(if [[ -z "$CANONICAL" ]]; then echo "Add a canonical tag pointing to this URL to prevent duplicate content issues.";
                        else echo "Verify canonical is self-referencing unless you intentionally canonicalize to a different URL."; fi)

5. **Robots.txt** — $(if [[ "$ROBOTS_SCORE" -lt 7 ]]; then echo "Create a robots.txt file at ${ROBOTS_URL} with appropriate Allow/Disallow directives.";
                      else echo "Keep robots.txt updated as the site evolves."; fi)

6. **Sitemap** — $(if [[ "$SITEMAP_SCORE" -lt 7 ]]; then echo "Generate and publish a sitemap.xml, then reference it in robots.txt with \`Sitemap: ${BASE_URL}/sitemap.xml\`.";
                   else echo "Sitemap is healthy — keep it updated with each new page."; fi)

7. **Open Graph** — $(if [[ ${#OG_MISSING[@]} -gt 0 ]]; then echo "Add missing OG tags (${OG_MISSING[*]}) to improve how links appear when shared on social media.";
                      else echo "Open Graph tags are complete — social sharing will render rich previews."; fi)

8. **Mobile viewport** — $(if [[ "$VIEWPORT_SCORE" -lt 10 ]]; then echo "Add \`<meta name='viewport' content='width=device-width, initial-scale=1'>\` to enable proper mobile rendering.";
                           else echo "Viewport is set correctly for mobile-friendliness."; fi)

9. **HTTPS** — $(if [[ "$HTTPS_SCORE" -lt 10 ]]; then echo "Migrate to HTTPS immediately — it's a confirmed Google ranking factor and required for modern browser features.";
                 else echo "HTTPS is enabled — keep certificates up to date and enforce HTTPS with a 301 redirect from HTTP."; fi)

---

*Report generated by seo-reporter skill on ${DATE}
REPORT

# Cleanup
rm -rf "$TMPDIR"
