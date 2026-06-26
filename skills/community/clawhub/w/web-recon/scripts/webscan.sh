#!/bin/bash
#===============================================================================
# webscan.sh - Unified Web Security Scanner v1.1.0
#
# Usage:
#   webscan.sh <domain> [options] [step]
#
# Options:
#   --quick       Light scan (recon, fingerprint, secrets, headers, report)
#   --full        Full scan - all steps (default)
#   --json        Output JSON report alongside markdown
#   --screenshot  Capture homepage screenshot
#   --resume      Skip steps that already have output files
#
# Steps (run individually or all):
#   all         - Run all steps (default)
#   recon       - Passive recon + port scan
#   fingerprint - Technology fingerprinting
#   subdomains  - Subdomain enumeration
#   dirs        - Directory/file discovery
#   secrets     - Secrets scanning
#   vulns       - Vulnerability scanning + header scoring
#   wpscan      - WordPress specific (if detected)
#   nuclei      - Template-based vuln scan
#   ssl         - SSL/TLS analysis
#   screenshot  - Homepage screenshot
#   report      - Generate summary report
#
# Environment:
#   SHODAN_API_KEY  - Shodan API key for infrastructure intel
#   OUTDIR          - Override output directory
#
# Output: ~/.openclaw/workspace/recon/<domain>/
#===============================================================================

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

#-------------------------------------------------------------------------------
# Configuration
#-------------------------------------------------------------------------------
SECLISTS="/usr/share/seclists"
VERSION="1.1.0"

# Security header definitions: name|severity(critical/high/medium/low)|description
SECURITY_HEADERS=(
    "Strict-Transport-Security|critical|Forces HTTPS connections"
    "Content-Security-Policy|critical|Prevents XSS and injection attacks"
    "X-Frame-Options|high|Prevents clickjacking"
    "X-Content-Type-Options|medium|Prevents MIME sniffing"
    "Referrer-Policy|medium|Controls referrer information"
    "Permissions-Policy|medium|Restricts browser features"
    "X-XSS-Protection|low|Legacy XSS filter (deprecated but still useful)"
    "Cross-Origin-Opener-Policy|low|Isolates browsing context"
    "Cross-Origin-Resource-Policy|low|Controls cross-origin resource loading"
    "Cross-Origin-Embedder-Policy|low|Controls cross-origin embedding"
)

get_wordlist() {
    local type="$1"
    case "$type" in
        dirs)
            for f in "$SECLISTS/Discovery/Web-Content/raft-medium-directories.txt" \
                     "$SECLISTS/Discovery/Web-Content/big.txt" \
                     "$SECLISTS/Discovery/Web-Content/common.txt" \
                     "/usr/share/dirb/wordlists/common.txt"; do
                [[ -s "$f" ]] && echo "$f" && return
            done ;;
        files)
            for f in "$SECLISTS/Discovery/Web-Content/raft-medium-files.txt" \
                     "$SECLISTS/Discovery/Web-Content/common.txt" \
                     "/usr/share/dirb/wordlists/common.txt"; do
                [[ -s "$f" ]] && echo "$f" && return
            done ;;
        subdomains)
            for f in "$SECLISTS/Discovery/DNS/subdomains-top1million-20000.txt" \
                     "$SECLISTS/Discovery/DNS/subdomains-top1million-5000.txt"; do
                [[ -s "$f" ]] && echo "$f" && return
            done ;;
        quick)
            for f in "$SECLISTS/Discovery/Web-Content/quickhits.txt" \
                     "$SECLISTS/Discovery/Web-Content/common.txt"; do
                [[ -s "$f" ]] && echo "$f" && return
            done ;;
    esac
}

#-------------------------------------------------------------------------------
# Parse arguments
#-------------------------------------------------------------------------------
DOMAIN=""
STEP="all"
MODE="full"
JSON_OUTPUT=false
SCREENSHOT=false
RESUME=false

while [[ $# -gt 0 ]]; do
    case "$1" in
        --quick)    MODE="quick"; shift ;;
        --full)     MODE="full"; shift ;;
        --json)     JSON_OUTPUT=true; shift ;;
        --screenshot) SCREENSHOT=true; shift ;;
        --resume)   RESUME=true; shift ;;
        -h|--help)
            sed -n '2,/^#====/p' "$0" | grep "^#" | sed 's/^# \?//'
            exit 0 ;;
        -*)         echo "Unknown option: $1"; exit 1 ;;
        *)
            if [[ -z "$DOMAIN" ]]; then
                DOMAIN="$1"
            else
                STEP="$1"
            fi
            shift ;;
    esac
done

if [[ -z "$DOMAIN" ]]; then
    echo "Usage: webscan.sh <domain> [--quick|--full] [--json] [--screenshot] [--resume] [step]"
    exit 1
fi

# Strip protocol
DOMAIN="${DOMAIN#https://}"
DOMAIN="${DOMAIN#http://}"
DOMAIN="${DOMAIN%%/*}"

OUTDIR="${OUTDIR:-$HOME/.openclaw/workspace/recon/$DOMAIN}"
mkdir -p "$OUTDIR"

URL="https://$DOMAIN"
TIMESTAMP=$(date -Iseconds)
IP=""

log() { echo "[$(date +%H:%M:%S)] $*"; }

run_step() {
    if [[ "$STEP" != "all" && "$STEP" != "$1" ]]; then
        return 1
    fi
    if [[ "$MODE" == "quick" ]]; then
        case "$1" in
            recon|fingerprint|secrets|vulns|report) return 0 ;;
            screenshot) $SCREENSHOT && return 0 || return 1 ;;
            *) return 1 ;;
        esac
    fi
    return 0
}

# Resume check: skip if output exists and --resume
has_output() {
    $RESUME && [[ -s "$OUTDIR/$1" ]]
}

#-------------------------------------------------------------------------------
# JSON accumulator
#-------------------------------------------------------------------------------
declare -A JSON_DATA
json_set() { JSON_DATA["$1"]="$2"; }

#-------------------------------------------------------------------------------
# Step: RECON - Passive recon + port scan
#-------------------------------------------------------------------------------
step_recon() {
    has_output "dns.txt" && { log "📡 RECON: Skipped (resume)"; return; }
    log "📡 RECON: Passive reconnaissance..."

    # DNS
    {
        echo "=== DNS Records ==="
        echo "A:    $(dig +short $DOMAIN A 2>/dev/null | tr '\n' ' ')"
        echo "AAAA: $(dig +short $DOMAIN AAAA 2>/dev/null | tr '\n' ' ')"
        echo "MX:   $(dig +short $DOMAIN MX 2>/dev/null | tr '\n' ' ')"
        echo "NS:   $(dig +short $DOMAIN NS 2>/dev/null | tr '\n' ' ')"
        echo "TXT:  $(dig +short $DOMAIN TXT 2>/dev/null | head -3 | tr '\n' ' ')"
    } > "$OUTDIR/dns.txt"

    # IP
    IP=$(dig +short $DOMAIN A 2>/dev/null | head -1)

    # IP Geolocation
    if [[ -n "$IP" ]]; then
        curl -s "http://ip-api.com/json/$IP" > "$OUTDIR/geo.json" 2>/dev/null
    fi

    # Port scan (top 1000 ports)
    if command -v nmap &>/dev/null && [[ -n "$IP" ]]; then
        log "   🔌 Port scanning $IP..."
        timeout 120 nmap -sT -T4 --top-ports 1000 -oN "$OUTDIR/ports.txt" -oG "$OUTDIR/ports-grep.txt" "$IP" 2>/dev/null || true
    fi

    # Shodan lookup
    if [[ -n "${SHODAN_API_KEY:-}" && -n "$IP" ]]; then
        log "   🌍 Shodan lookup..."
        curl -s "https://api.shodan.io/shodan/host/$IP?key=$SHODAN_API_KEY" > "$OUTDIR/shodan.json" 2>/dev/null || true
    elif command -v shodan &>/dev/null && [[ -n "$IP" ]]; then
        timeout 30 shodan host "$IP" > "$OUTDIR/shodan.txt" 2>/dev/null || true
    fi

    # Wayback URLs
    if command -v waybackurls &>/dev/null; then
        echo "$DOMAIN" | timeout 60 waybackurls 2>/dev/null | head -500 > "$OUTDIR/wayback.txt" || true
    fi

    log "   ✓ DNS, geo, ports, wayback saved"
}

#-------------------------------------------------------------------------------
# Step: FINGERPRINT - Technology identification
#-------------------------------------------------------------------------------
step_fingerprint() {
    has_output "headers.txt" && { log "🔧 FINGERPRINT: Skipped (resume)"; return; }
    log "🔧 FINGERPRINT: Technology stack..."

    curl -sI -L --connect-timeout 10 --max-time 30 "$URL" > "$OUTDIR/headers.txt" 2>/dev/null || true

    if command -v whatweb &>/dev/null; then
        timeout 60 whatweb -q -a 3 "$URL" > "$OUTDIR/whatweb.txt" 2>/dev/null || true
    fi

    if command -v wafw00f &>/dev/null; then
        timeout 30 wafw00f "$URL" > "$OUTDIR/waf.txt" 2>&1 || true
    fi

    # CMS detection
    WP_CHECK=$(curl -sL --max-time 10 "$URL" 2>/dev/null | grep -c "wp-content\|wp-includes" || echo "0")
    if [[ "$WP_CHECK" -gt 0 ]]; then
        echo "wordpress" > "$OUTDIR/cms.txt"
    else
        echo "unknown" > "$OUTDIR/cms.txt"
    fi

    log "   ✓ Headers, whatweb, WAF, CMS saved"
}

#-------------------------------------------------------------------------------
# Step: SUBDOMAINS
#-------------------------------------------------------------------------------
step_subdomains() {
    has_output "subdomains.txt" && { log "🔎 SUBDOMAINS: Skipped (resume)"; return; }
    log "🔎 SUBDOMAINS: Enumerating..."

    if command -v subfinder &>/dev/null; then
        timeout 120 subfinder -d "$DOMAIN" -silent > "$OUTDIR/subdomains-subfinder.txt" 2>/dev/null || true
    fi

    if command -v amass &>/dev/null; then
        timeout 180 amass enum -passive -d "$DOMAIN" -o "$OUTDIR/subdomains-amass.txt" 2>/dev/null || true
    fi

    cat "$OUTDIR"/subdomains-*.txt 2>/dev/null | sort -u > "$OUTDIR/subdomains.txt" || true

    if command -v httpx &>/dev/null && [[ -s "$OUTDIR/subdomains.txt" ]]; then
        cat "$OUTDIR/subdomains.txt" | timeout 120 httpx -silent -status-code > "$OUTDIR/subdomains-live.txt" 2>/dev/null || true
    fi

    COUNT=$(wc -l < "$OUTDIR/subdomains.txt" 2>/dev/null || echo 0)
    log "   ✓ Found $COUNT subdomains"
}

#-------------------------------------------------------------------------------
# Step: DIRS
#-------------------------------------------------------------------------------
step_dirs() {
    has_output "dirs.txt" && { log "📂 DIRS: Skipped (resume)"; return; }
    log "📂 DIRS: Directory bruteforce..."

    WORDLIST=$(get_wordlist dirs)
    [[ -n "$WORDLIST" ]] && log "   Using: $(basename $WORDLIST) ($(wc -l < $WORDLIST) entries)"

    if command -v gobuster &>/dev/null && [[ -n "$WORDLIST" ]]; then
        timeout 300 gobuster dir -u "$URL" -w "$WORDLIST" -q -t 20 \
            --no-error -o "$OUTDIR/dirs-gobuster.txt" 2>/dev/null || true
    fi

    QUICKLIST=$(get_wordlist quick)
    if command -v ffuf &>/dev/null && [[ -n "$QUICKLIST" ]]; then
        timeout 120 ffuf -u "$URL/FUZZ" -w "$QUICKLIST" -mc 200,301,302,403 \
            -s -o "$OUTDIR/dirs-ffuf.json" -of json 2>/dev/null || true
    fi

    {
        cat "$OUTDIR/dirs-gobuster.txt" 2>/dev/null
        jq -r '.results[]?.url' "$OUTDIR/dirs-ffuf.json" 2>/dev/null
    } | sort -u > "$OUTDIR/dirs.txt" 2>/dev/null || true

    COUNT=$(wc -l < "$OUTDIR/dirs.txt" 2>/dev/null || echo 0)
    log "   ✓ Found $COUNT directories/files"
}

#-------------------------------------------------------------------------------
# Step: SECRETS
#-------------------------------------------------------------------------------
step_secrets() {
    has_output "sensitive-files.txt" && { log "🔐 SECRETS: Skipped (resume)"; return; }
    log "🔐 SECRETS: Scanning for exposed secrets..."

    if [[ -x "$SCRIPT_DIR/titus-web.sh" ]]; then
        "$SCRIPT_DIR/titus-web.sh" "$URL" > "$OUTDIR/titus.txt" 2>&1 || true
    fi

    {
        echo "=== Sensitive File Check ==="
        for path in .env .env.local .env.production .env.staging \
                    .git/config .git/HEAD .gitignore \
                    wp-config.php.bak config.php.bak web.config \
                    .htaccess .htpasswd .DS_Store \
                    robots.txt sitemap.xml crossdomain.xml \
                    api/swagger.json swagger.json openapi.json \
                    .well-known/security.txt security.txt \
                    phpinfo.php info.php test.php \
                    backup.sql database.sql dump.sql \
                    server-status server-info; do
            CODE=$(curl -sI -o /dev/null -w "%{http_code}" --max-time 5 "$URL/$path" 2>/dev/null)
            if [[ "$CODE" == "200" ]]; then
                echo "FOUND ($CODE): $URL/$path"
            fi
        done
    } > "$OUTDIR/sensitive-files.txt"

    log "   ✓ Secrets scan complete"
}

#-------------------------------------------------------------------------------
# Step: VULNS - Security checks + header scoring
#-------------------------------------------------------------------------------
step_vulns() {
    has_output "header-score.txt" && { log "⚠️  VULNS: Skipped (resume)"; return; }
    log "⚠️  VULNS: Security analysis..."

    # Fetch headers once
    HEADERS=$(curl -sI --max-time 10 "$URL" 2>/dev/null)

    # Score security headers
    {
        echo "=== Security Header Score ==="
        echo ""
        TOTAL=0
        PRESENT=0
        SCORE=0
        MAX_SCORE=0

        for hdr_def in "${SECURITY_HEADERS[@]}"; do
            IFS='|' read -r HDR_NAME SEVERITY DESC <<< "$hdr_def"
            TOTAL=$((TOTAL + 1))

            case "$SEVERITY" in
                critical) POINTS=30 ;;
                high)     POINTS=20 ;;
                medium)   POINTS=10 ;;
                low)      POINTS=5 ;;
            esac
            MAX_SCORE=$((MAX_SCORE + POINTS))

            if echo "$HEADERS" | grep -qi "^$HDR_NAME"; then
                VALUE=$(echo "$HEADERS" | grep -i "^$HDR_NAME" | head -1 | sed 's/^[^:]*: //')
                echo "✅ $HDR_NAME [$SEVERITY] +$POINTS"
                echo "   Value: $VALUE"
                echo "   $DESC"
                PRESENT=$((PRESENT + 1))
                SCORE=$((SCORE + POINTS))
            else
                echo "❌ $HDR_NAME [$SEVERITY] -$POINTS"
                echo "   MISSING — $DESC"
            fi
            echo ""
        done

        PERCENT=$((SCORE * 100 / MAX_SCORE))
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "Score: $SCORE/$MAX_SCORE ($PERCENT%)"
        echo "Headers present: $PRESENT/$TOTAL"
        echo ""
        if [[ $PERCENT -ge 80 ]]; then
            echo "Rating: 🟢 GOOD"
        elif [[ $PERCENT -ge 50 ]]; then
            echo "Rating: 🟡 FAIR"
        elif [[ $PERCENT -ge 25 ]]; then
            echo "Rating: 🟠 POOR"
        else
            echo "Rating: 🔴 CRITICAL"
        fi
    } > "$OUTDIR/header-score.txt"

    json_set "header_score" "$SCORE"
    json_set "header_max" "$MAX_SCORE"
    json_set "header_percent" "$PERCENT"

    # CORS check
    {
        echo "=== CORS Configuration ==="
        CORS_HEADERS=$(curl -sI -H "Origin: https://evil.com" --max-time 10 "$URL" 2>/dev/null)
        ACAO=$(echo "$CORS_HEADERS" | grep -i "access-control-allow-origin" | head -1)
        if [[ -n "$ACAO" ]]; then
            echo "$ACAO"
            if echo "$ACAO" | grep -q "\*"; then
                echo "⚠️  WARNING: Wildcard CORS — any origin allowed"
            elif echo "$ACAO" | grep -qi "evil.com"; then
                echo "🔴 CRITICAL: Origin reflection — CORS misconfiguration"
            else
                echo "✅ Restricted CORS policy"
            fi
        else
            echo "No CORS headers (OK for same-origin only)"
        fi
    } > "$OUTDIR/cors.txt"

    # SSL quick check
    if command -v testssl &>/dev/null; then
        timeout 120 testssl --quiet --sneaky "$DOMAIN" > "$OUTDIR/ssl.txt" 2>&1 || true
    fi

    # Nikto
    if command -v nikto &>/dev/null; then
        timeout 300 nikto -h "$URL" -maxtime 300 -nointeractive \
            -o "$OUTDIR/nikto.txt" 2>/dev/null || true
    fi

    log "   ✓ Security analysis complete"
}

#-------------------------------------------------------------------------------
# Step: WPSCAN
#-------------------------------------------------------------------------------
step_wpscan() {
    CMS=$(cat "$OUTDIR/cms.txt" 2>/dev/null)
    if [[ "$CMS" != "wordpress" ]]; then
        log "📝 WPSCAN: Skipped (not WordPress)"
        return
    fi
    has_output "wpscan.txt" && { log "📝 WPSCAN: Skipped (resume)"; return; }
    log "📝 WPSCAN: WordPress scan..."

    if command -v wpscan &>/dev/null; then
        timeout 300 wpscan --url "$URL" --no-banner --random-user-agent \
            --enumerate ap,at,cb,dbe > "$OUTDIR/wpscan.txt" 2>&1 || true
    fi

    log "   ✓ WordPress scan complete"
}

#-------------------------------------------------------------------------------
# Step: NUCLEI
#-------------------------------------------------------------------------------
step_nuclei() {
    has_output "nuclei.txt" && { log "🧬 NUCLEI: Skipped (resume)"; return; }
    log "🧬 NUCLEI: Template scan..."

    if command -v nuclei &>/dev/null; then
        nuclei -update-templates -silent 2>/dev/null || true
        timeout 600 nuclei -u "$URL" -severity low,medium,high,critical \
            -silent -o "$OUTDIR/nuclei.txt" 2>/dev/null || true
    fi

    COUNT=$(wc -l < "$OUTDIR/nuclei.txt" 2>/dev/null || echo 0)
    log "   ✓ Found $COUNT potential issues"
}

#-------------------------------------------------------------------------------
# Step: SSL
#-------------------------------------------------------------------------------
step_ssl() {
    has_output "ssl.txt" && { log "🔒 SSL: Skipped (resume)"; return; }
    log "🔒 SSL: TLS analysis..."

    if command -v testssl &>/dev/null && [[ ! -s "$OUTDIR/ssl.txt" ]]; then
        timeout 180 testssl --quiet "$DOMAIN" > "$OUTDIR/ssl.txt" 2>&1 || true
    fi

    log "   ✓ SSL analysis complete"
}

#-------------------------------------------------------------------------------
# Step: SCREENSHOT
#-------------------------------------------------------------------------------
step_screenshot() {
    has_output "screenshot.png" && { log "📸 SCREENSHOT: Skipped (resume)"; return; }
    log "📸 SCREENSHOT: Capturing homepage..."

    if command -v cutycapt &>/dev/null; then
        timeout 30 cutycapt --url="$URL" --out="$OUTDIR/screenshot.png" \
            --min-width=1280 --delay=3000 2>/dev/null || true
    elif command -v chromium &>/dev/null; then
        timeout 30 chromium --headless --disable-gpu --screenshot="$OUTDIR/screenshot.png" \
            --window-size=1280,1024 --no-sandbox "$URL" 2>/dev/null || true
    elif command -v google-chrome &>/dev/null; then
        timeout 30 google-chrome --headless --disable-gpu --screenshot="$OUTDIR/screenshot.png" \
            --window-size=1280,1024 --no-sandbox "$URL" 2>/dev/null || true
    else
        log "   ⚠ No screenshot tool found (install cutycapt or chromium)"
        return
    fi

    [[ -s "$OUTDIR/screenshot.png" ]] && log "   ✓ Screenshot saved" || log "   ⚠ Screenshot failed"
}

#-------------------------------------------------------------------------------
# Step: REPORT
#-------------------------------------------------------------------------------
step_report() {
    log "📄 REPORT: Generating summary..."

    [[ -z "$IP" ]] && IP=$(dig +short $DOMAIN A 2>/dev/null | head -1)
    COUNTRY=$(jq -r '.country // "Unknown"' "$OUTDIR/geo.json" 2>/dev/null || echo "Unknown")
    CITY=$(jq -r '.city // "Unknown"' "$OUTDIR/geo.json" 2>/dev/null || echo "Unknown")
    ISP=$(jq -r '.isp // "Unknown"' "$OUTDIR/geo.json" 2>/dev/null || echo "Unknown")
    WAF=$(grep -oP "behind \K[^\s]+" "$OUTDIR/waf.txt" 2>/dev/null | head -1 || echo "None detected")
    CMS=$(cat "$OUTDIR/cms.txt" 2>/dev/null || echo "Unknown")
    SUBDOMAIN_COUNT=$(wc -l < "$OUTDIR/subdomains.txt" 2>/dev/null || echo 0)
    DIR_COUNT=$(wc -l < "$OUTDIR/dirs.txt" 2>/dev/null || echo 0)
    NUCLEI_COUNT=$(wc -l < "$OUTDIR/nuclei.txt" 2>/dev/null || echo 0)
    OPEN_PORTS=$(grep "open" "$OUTDIR/ports.txt" 2>/dev/null | wc -l || echo 0)
    HEADER_SCORE=$(grep "^Score:" "$OUTDIR/header-score.txt" 2>/dev/null | head -1 || echo "Not scored")
    HEADER_RATING=$(grep "^Rating:" "$OUTDIR/header-score.txt" 2>/dev/null | head -1 || echo "N/A")

    REPORT="$OUTDIR/results.md"
    cat > "$REPORT" << EOF
# Security Scan Results: $DOMAIN
Generated: $TIMESTAMP
Scanner: webscan.sh v$VERSION
Mode: $MODE

---

## Executive Summary

**Target:** $URL
**IP:** $IP
**Location:** $CITY, $COUNTRY
**ISP:** $ISP
**WAF:** $WAF
**CMS:** $CMS

## Security Header Score

$HEADER_SCORE
$HEADER_RATING

## Statistics

| Metric | Count |
|--------|-------|
| Open Ports | $OPEN_PORTS |
| Subdomains | $SUBDOMAIN_COUNT |
| Directories/Files | $DIR_COUNT |
| Nuclei Findings | $NUCLEI_COUNT |

## Key Findings

### Open Ports
\`\`\`
$(grep "open" "$OUTDIR/ports.txt" 2>/dev/null | head -20 || echo "No port scan data")
\`\`\`

### Sensitive Files Found
\`\`\`
$(grep "FOUND" "$OUTDIR/sensitive-files.txt" 2>/dev/null || echo "None")
\`\`\`

### CORS Configuration
\`\`\`
$(cat "$OUTDIR/cors.txt" 2>/dev/null || echo "Not checked")
\`\`\`

### Secrets Scan
\`\`\`
$(grep -E "findings|secrets|No findings" "$OUTDIR/titus.txt" 2>/dev/null | tail -5 || echo "Not run")
\`\`\`

### Nuclei Findings
\`\`\`
$(cat "$OUTDIR/nuclei.txt" 2>/dev/null | head -20 || echo "None")
\`\`\`

$(if [[ "$CMS" == "wordpress" ]]; then
echo "### WordPress Analysis"
echo '```'
grep -E "out of date|XML-RPC|Version:" "$OUTDIR/wpscan.txt" 2>/dev/null | head -20 || echo "Not run"
echo '```'
fi)

---

## Files Generated

$(ls -la "$OUTDIR"/*.txt "$OUTDIR"/*.json "$OUTDIR"/*.png 2>/dev/null | awk '{print "- " $NF " (" $5 " bytes)"}')

---
*Generated by webscan.sh v$VERSION*
EOF

    # JSON report
    if $JSON_OUTPUT; then
        cat > "$OUTDIR/results.json" << EOJSON
{
  "domain": "$DOMAIN",
  "url": "$URL",
  "ip": "$IP",
  "location": {"city": "$CITY", "country": "$COUNTRY"},
  "isp": "$ISP",
  "waf": "$WAF",
  "cms": "$CMS",
  "scanner": "webscan.sh",
  "version": "$VERSION",
  "mode": "$MODE",
  "timestamp": "$TIMESTAMP",
  "stats": {
    "open_ports": $OPEN_PORTS,
    "subdomains": $SUBDOMAIN_COUNT,
    "directories": $DIR_COUNT,
    "nuclei_findings": $NUCLEI_COUNT
  },
  "header_score": {
    "score": "${JSON_DATA[header_score]:-0}",
    "max": "${JSON_DATA[header_max]:-0}",
    "percent": "${JSON_DATA[header_percent]:-0}"
  },
  "sensitive_files": [$(grep "FOUND" "$OUTDIR/sensitive-files.txt" 2>/dev/null | sed 's/FOUND ([0-9]*): //' | while read -r line; do echo "\"$line\","; done | sed '$ s/,$//')],
  "open_ports_list": [$(grep "open" "$OUTDIR/ports.txt" 2>/dev/null | awk '{print "\""$1" "$3"\","}' | sed '$ s/,$//')],
  "nuclei_findings_list": [$(head -20 "$OUTDIR/nuclei.txt" 2>/dev/null | while read -r line; do echo "\"$(echo "$line" | sed 's/"/\\"/g')\","; done | sed '$ s/,$//')],
  "files": [$(ls "$OUTDIR"/*.txt "$OUTDIR"/*.json "$OUTDIR"/*.png 2>/dev/null | while read -r f; do echo "\"$(basename $f)\","; done | sed '$ s/,$//')]
}
EOJSON
        log "   ✓ JSON report: $OUTDIR/results.json"
    fi

    log "   ✓ Report: $OUTDIR/results.md"
}

#-------------------------------------------------------------------------------
# Main
#-------------------------------------------------------------------------------
log "🔍 WEBSCAN v$VERSION: $DOMAIN"
log "   Mode: $MODE | JSON: $JSON_OUTPUT | Resume: $RESUME"
log "   Output: $OUTDIR"
echo ""

run_step recon       && step_recon
run_step fingerprint && step_fingerprint
run_step subdomains  && step_subdomains
run_step dirs        && step_dirs
run_step secrets     && step_secrets
run_step vulns       && step_vulns
run_step wpscan      && step_wpscan
run_step nuclei      && step_nuclei
run_step ssl         && step_ssl
(run_step screenshot || $SCREENSHOT) && step_screenshot
run_step report      && step_report

echo ""
log "✅ Scan complete: $OUTDIR"
log "📊 Report: $OUTDIR/results.md"
$JSON_OUTPUT && log "📊 JSON:   $OUTDIR/results.json"
