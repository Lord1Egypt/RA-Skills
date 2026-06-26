#!/bin/bash
# Subdomain Takeover Checker — Detect dangling DNS records
# Generic version — no personal data

set -euo pipefail

# Known vulnerable CNAME patterns
VULN_PATTERNS=(
    "github.io:GitHub Pages"
    "github.com:GitHub"
    "herokudns.com:Heroku DNS"
    "herokuapp.com:Heroku"
    "herokussl.com:Heroku SSL"
    "amazonaws.com:AWS"
    "s3.amazonaws.com:AWS S3"
    "s3-website:AWS S3 Website"
    "cloudfront.net:CloudFront"
    "elasticbeanstalk.com:Elastic Beanstalk"
    "azurewebsites.net:Azure App Service"
    "cloudapp.azure.com:Azure Cloud App"
    "trafficmanager.net:Azure Traffic Manager"
    "cloudapp.net:Azure"
    "myshopify.com:Shopify"
    "fastly.net:Fastly"
    "pantheonsite.io:Pantheon"
    "surge.sh:Surge"
    "tumblr.com:Tumblr"
    "wordpress.com:WordPress"
    "zendesk.com:Zendesk"
    "netlify.app:Netlify"
    "vercel.app:Vercel"
    "firebaseapp.com:Firebase"
    "web.app:Firebase Hosting"
    "bitbucket.io:Bitbucket"
    "ghost.io:Ghost"
    "cargocollective.com:Cargo"
    "hatenablog.com:Hatena"
    "statuspage.io:Statuspage"
    "smugmug.com:SmugMug"
    "agilecrm.com:AgileCRM"
    "readthedocs.io:ReadTheDocs"
    "hatenadiary.com:Hatena Diary"
    "feedpress.me:Feedpress"
    "getresponse.com:GetResponse"
    "bitballoon.com:BitBalloon"
    "modulus.io:Modulus"
    "airee.ru:Airee"
    "anima.site:Anima"
    "canny.io:Canny"
    "read.heyday.ai:Heyday"
    "strikingly.com:Strikingly"
    "wishpond.com:Wishpond"
    "mayfirst.org:May First"
    "hatelabo.jp:Hatena Lab"
    "zone.id:Zone ID"
    "apigee.net:Apigee"
)

DOMAINS=()
PASSIVE=0
JSON_OUT=0
TIMEOUT=5
OUTPUT=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -l) while IFS= read -r line; do DOMAINS+=("$line"); done < "$2"; shift 2 ;;
        -d) DOMAINS+=("$2"); shift 2 ;;
        --passive) PASSIVE=1; shift ;;
        --json) JSON_OUT=1; shift ;;
        --timeout) TIMEOUT="$2"; shift 2 ;;
        --output) OUTPUT="$2"; shift 2 ;;
        *) shift ;;
    esac
done

if [ ${#DOMAINS[@]} -eq 0 ]; then
    echo "Usage: $0 -l subdomains.txt | -d sub.example.com"
    exit 1
fi

VULN_COUNT=0
SAFE_COUNT=0
RESULTS=""

check_subdomain() {
    local domain="$1"
    
    # Get CNAME
    local cname=$(dig +short +time=$TIMEOUT +tries=1 CNAME "$domain" 2>/dev/null | head -1)
    
    if [ -z "$cname" ]; then
        # Check if A record exists
        local a_record=$(dig +short +time=$TIMEOUT +tries=1 A "$domain" 2>/dev/null | head -1)
        if [ -n "$a_record" ]; then
            SAFE_COUNT=$((SAFE_COUNT + 1))
            return
        fi
        return
    fi
    
    # Check against vulnerable patterns
    for pattern_entry in "${VULN_PATTERNS[@]}"; do
        local pattern="${pattern_entry%%:*}"
        local service="${pattern_entry##*:}"
        if [[ "$cname" == *"$pattern"* ]]; then
            if [ "$PASSIVE" = "0" ]; then
                # Verify with HTTP check — NXDOMAIN or error page = vulnerable
                local http_code=$(curl -s -o /dev/null -w '%{http_code}' --max-time 5 "http://$domain" 2>/dev/null || echo "000")
                if [ "$http_code" = "404" ] || [ "$http_code" = "000" ]; then
                    VULN_COUNT=$((VULN_COUNT + 1))
                    RESULTS+="⚠️  $domain → $cname ($service — potentially claimable)\n"
                    return
                fi
            else
                VULN_COUNT=$((VULN_COUNT + 1))
                RESULTS+="⚠️  $domain → $cname ($service — check manually)\n"
                return
            fi
        fi
    done
    
    SAFE_COUNT=$((SAFE_COUNT + 1))
}

echo "=== Subdomain Takeover Scan ===" >&2
echo "Scanning ${#DOMAINS[@]} subdomains..." >&2
echo "" >&2

for domain in "${DOMAINS[@]}"; do
    domain=$(echo "$domain" | xargs)  # trim whitespace
    [ -z "$domain" ] && continue
    check_subdomain "$domain"
done

TOTAL=$((VULN_COUNT + SAFE_COUNT))

if [ "$JSON_OUT" = "1" ]; then
    echo "{\"vulnerable\":$VULN_COUNT,\"safe\":$SAFE_COUNT,\"total\":$TOTAL}"
else
    if [ -n "$RESULTS" ]; then
        echo "⚠️  POTENTIALLY VULNERABLE:"
        echo -e "$RESULTS"
    fi
    echo "Summary: $VULN_COUNT/$TOTAL potentially vulnerable"
fi

if [ -n "$OUTPUT" ]; then
    echo -e "$RESULTS" > "$OUTPUT"
    echo "Results written to $OUTPUT" >&2
fi

[ "$VULN_COUNT" -gt 0 ] && exit 1 || exit 0
