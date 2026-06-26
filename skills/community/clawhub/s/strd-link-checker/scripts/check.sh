#!/bin/bash
# check.sh — Full link audit for a directory of HTML files
# Checks all internal + external links, reports broken/redirected/slow/affiliate

set -e

DIR="${1:-${SITE_DIR:-./site}}"
TIMEOUT="${LINK_CHECK_TIMEOUT:-10}"
AFFILIATE_DOMAINS="${AFFILIATE_DOMAINS:-amazon.com,hostname/s/aspx,godaddy.com,bluehost.com,digitalocean.com,heroku.com,shopify.com,awin1.com,ref=}"

echo "# 🔗 Link Checker Report"
echo "Directory: $DIR"
echo "Generated: $(date '+%Y-%m-%d %H:%M:%S UTC')"
echo ""

# Count files
HTML_FILES=$(find "$DIR" -name "*.html" 2>/dev/null | wc -l | tr -d ' ')
echo "HTML files found: $HTML_FILES"
echo ""

if [ "$HTML_FILES" -eq 0 ]; then
    echo "No HTML files found in $DIR"
    exit 0
fi

# Temp files
TMP_BROKEN=$(mktemp)
TMP_REDIRECT=$(mktemp)
TMP_SLOW=$(mktemp)
TMP_AFFILIATE=$(mktemp)
TMP_ALL=$(mktemp)

trap "rm -f $TMP_BROKEN $TMP_REDIRECT $TMP_SLOW $TMP_AFFILIATE $TMP_ALL" EXIT

# Extract all links from HTML files
find "$DIR" -name "*.html" -exec grep -nH -oE 'href="[^"]*"' {} \; 2>/dev/null | \
    sed 's/href="/\t/' | sed 's/"$//' | sed 's/"$//' > "$TMP_ALL"

TOTAL_LINKS=$(wc -l < "$TMP_ALL" | tr -d ' ')
echo "Total links found: $TOTAL_LINKS"
echo ""

# Check each link
check_link() {
    local file="$1"
    local line="$2"
    local url="$3"
    
    # Skip javascript and anchors
    [[ "$url" =~ ^javascript: ]] && return
    [[ "$url" =~ ^# ]] && return
    # Skip mailto:
    [[ "$url" =~ ^mailto: ]] && return
    # Skip empty
    [ -z "$url" ] && return
    
    # Get status
    local status_code=""
    local redirect_url=""
    local response_time=""
    
    # Measure response time
    local start_time=$(date +%s.%N)
    local curl_output
    curl_output=$(curl -s -o /dev/null -w "%{http_code}|%{redirect_url}|%{time_total}" \
        --max-time "$TIMEOUT" -L -I "$url" 2>/dev/null)
    local end_time=$(date +%s.%N)
    
    if [ -z "$curl_output" ]; then
        status_code="000"
        response_time="timeout"
    else
        status_code=$(echo "$curl_output" | cut -d'|' -f1)
        redirect_url=$(echo "$curl_output" | cut -d'|' -f2)
        response_time=$(echo "$curl_output" | cut -d'|' -f3)
    fi
    
    # Categorize
    if [[ "$status_code" =~ ^4|^5|^000 ]]; then
        echo -e "BROKEN\t$file\t$line\t$url\t$status_code" >> "$TMP_BROKEN"
    elif [[ "$status_code" =~ ^3 ]] && [ -n "$redirect_url" ]; then
        echo -e "REDIRECT\t$file\t$line\t$url\t$redirect_url" >> "$TMP_REDIRECT"
    fi
    
    # Slow check
    if [[ "$response_time" != "timeout" ]] && [ -n "$response_time" ]; then
        if (( $(echo "$response_time > 5" | bc -l 2>/dev/null) )); then
            echo -e "SLOW\t$file\t$line\t$url\t$response_time" >> "$TMP_SLOW"
        fi
    fi
    
    # Affiliate check
    for aff_domain in $(echo "$AFFILIATE_DOMAINS" | tr ',' ' '); do
        if [[ "$url" == *"$aff_domain"* ]]; then
            echo -e "AFFILIATE\t$file\t$line\t$url" >> "$TMP_AFFILIATE"
            break
        fi
    done
}

export -f check_link
export TIMEOUT
export TMP_BROKEN TMP_REDIRECT TMP_SLOW TMP_AFFILIATE

# Process links (limit concurrency to avoid overwhelming targets)
total=$(wc -l < "$TMP_ALL" | tr -d ' ')
count=0

while IFS=$'\t' read -r file line url; do
    count=$((count + 1))
    if [ $((count % 20)) -eq 0 ]; then
        echo -ne "  Checking links: $count/$total\r"
    fi
    check_link "$file" "$line" "$url" &
    # Limit to 10 concurrent curls
    if [ $count -eq 10 ]; then
        wait
        count=0
    fi
done < "$TMP_ALL"
wait
echo -ne "  Checking links: $total/$total... done.\n"

# Report
BROKEN_COUNT=$(wc -l < "$TMP_BROKEN" 2>/dev/null || echo 0)
REDIRECT_COUNT=$(wc -l < "$TMP_REDIRECT" 2>/dev/null || echo 0)
SLOW_COUNT=$(wc -l < "$TMP_SLOW" 2>/dev/null || echo 0)
AFFILIATE_COUNT=$(wc -l < "$TMP_AFFILIATE" 2>/dev/null || echo 0)

echo ""
echo "## Summary"
echo "- Total links checked: $TOTAL_LINKS"
echo "- Broken (4xx/5xx): \`$BROKEN_COUNT\` $([ "$BROKEN_COUNT" -gt 0 ] && echo '🔴' || echo '✅')"
echo "- Redirected: \`$REDIRECT_COUNT\` $([ "$REDIRECT_COUNT" -gt 0 ] && echo '🟡' || echo '✅')"
echo "- Slow (>5s): \`$SLOW_COUNT\` $([ "$SLOW_COUNT" -gt 0 ] && echo '🟠' || echo '✅')"
echo "- Affiliate links found: \`$AFFILIATE_COUNT\` ✅"
echo ""

# Broken links
if [ "$BROKEN_COUNT" -gt 0 ]; then
    echo "## 🔴 Broken Links"
    while IFS=$'\t' read -r type file line url status; do
        echo "- \`$file\` line $line: [$url]($url) — HTTP $status"
    done < "$TMP_BROKEN"
    echo ""
fi

# Redirects
if [ "$REDIRECT_COUNT" -gt 0 ]; then
    echo "## 🟡 Redirects"
    while IFS=$'\t' read -r type file line url destination; do
        echo "- \`$file\` line $line: [$url]($url) → $destination"
    done < "$TMP_REDIRECT"
    echo ""
fi

# Slow links
if [ "$SLOW_COUNT" -gt 0 ]; then
    echo "## 🟠 Slow Links (>5s)"
    while IFS=$'\t' read -r type file line url response_time; do
        echo "- \`$file\` line $line: [$url]($url) — ${response_time}s"
    done < "$TMP_SLOW"
    echo ""
fi

# Affiliate links
if [ "$AFFILIATE_COUNT" -gt 0 ]; then
    echo "## ✅ Affiliate Links"
    while IFS=$'\t' read -r type file line url; do
        echo "- \`$file\` line $line: [$url]($url)"
    done < "$TMP_AFFILIATE"
    echo ""
fi

# Clean summary if all good
if [ "$BROKEN_COUNT" -eq 0 ] && [ "$REDIRECT_COUNT" -eq 0 ] && [ "$SLOW_COUNT" -eq 0 ]; then
    echo "🎉 All links checked — no critical issues found."
    echo ""
fi
