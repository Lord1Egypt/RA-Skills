#!/bin/bash
#
# weekly_unsubscribe_sync.sh
# 
# Automated weekly sync of unsubscribes from web form to Renatus.
# Designed to run via cron (e.g., every Sunday at 2 AM).
#
# Requirements:
# - Chrome/Brave running with --remote-debugging-port=9222
# - Logged into backoffice.myrenatus.com
# - Python 3 + Playwright installed
#

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_DIR="$SCRIPT_DIR/../logs"
DATA_DIR="$SCRIPT_DIR/../data"
DATE_STR=$(date +%Y%m%d_%H%M%S)
LOG_FILE="$LOG_DIR/unsubscribe_sync_$DATE_STR.log"
EMAILS_FILE="$DATA_DIR/unsubscribes_$DATE_STR.txt"
REPORT_FILE="$DATA_DIR/unsubscribe_report_$DATE_STR.json"

# Chrome CDP endpoint
CDP_URL="${CDP_URL:-http://127.0.0.1:9222}"

# Ensure directories exist
mkdir -p "$LOG_DIR" "$DATA_DIR"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

log "=== Weekly Unsubscribe Sync Started ==="
log "Date: $DATE_STR"
log "CDP URL: $CDP_URL"

# Check if Chrome is accessible
if ! curl -s "$CDP_URL/json/version" >/dev/null 2>&1; then
    log "ERROR: Cannot connect to Chrome at $CDP_URL"
    log "Make sure Chrome is running with: --remote-debugging-port=9222"
    exit 1
fi

log "Chrome CDP endpoint is accessible"

# Step 1: Extract unsubscribes from browser localStorage
log "Step 1: Extracting unsubscribes from browser..."

python3 << 'PYEOF' >"$EMAILS_FILE" 2>&1
import json
import sys
from playwright.sync_api import sync_playwright

CDP_URL = "$CDP_URL"

try:
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP_URL, timeout=30000)
        
        # Try to get unsubscribes from first context
        emails = []
        for context in browser.contexts:
            page = context.new_page()
            try:
                page.goto("https://YOUR_DOMAIN/unsubscribe.html", wait_until="domcontentloaded", timeout=10000)
                page.wait_for_timeout(1000)
                
                # Extract from localStorage
                result = page.evaluate("""
                    () => {
                        try {
                            return JSON.parse(localStorage.getItem('unsubscribed') || '[]');
                        } catch {
                            return [];
                        }
                    }
                """)
                
                if isinstance(result, list):
                    emails = result
                    break
            except Exception as e:
                print(f"Error in context: {e}", file=sys.stderr)
            finally:
                try:
                    page.close()
                except:
                    pass
        
        # Also check all contexts for unsubscribed_leads key (edge function storage)
        for context in browser.contexts:
            for page in context.pages:
                try:
                    result = page.evaluate("""
                        () => {
                            const items = [];
                            for (let i = 0; i < localStorage.length; i++) {
                                const key = localStorage.key(i);
                                if (key && key.includes('unsubscribe')) {
                                    items.push({key: key, value: localStorage.getItem(key)});
                                }
                            }
                            return items;
                        }
                    """)
                    print(f"Found keys: {result}", file=sys.stderr)
                except:
                    pass
        
        # Write emails one per line
        for email in emails:
            print(email)
        
        browser.close()
        
except Exception as e:
    print(f"Failed to extract: {e}", file=sys.stderr)
    sys.exit(1)
PYEOF

EMAIL_COUNT=$(wc -l < "$EMAILS_FILE" | tr -d ' ')
log "Found $EMAIL_COUNT unsubscribed email(s)"

if [ "$EMAIL_COUNT" -eq 0 ]; then
    log "No unsubscribes to process. Exiting."
    exit 0
fi

# Step 2: Check Renatus authentication
log "Step 2: Verifying Renatus authentication..."

python3 << 'PYEOF'
import sys
from playwright.sync_api import sync_playwright

CDP_URL = "$CDP_URL"

try:
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP_URL, timeout=30000)
        
        for context in browser.contexts:
            page = context.new_page()
            try:
                page.goto("https://backoffice.myrenatus.com/Home/index", wait_until="domcontentloaded", timeout=15000)
                page.wait_for_timeout(2000)
                
                auth = page.evaluate("""
                    () => {
                        const auth = localStorage.getItem('auth');
                        const xsrf = localStorage.getItem('__RequestVerificationToken');
                        return { hasAuth: !!auth, hasXsrf: !!xsrf };
                    }
                """)
                
                if auth.get('hasAuth') and auth.get('hasXsrf'):
                    print("Auth OK")
                    sys.exit(0)
            except:
                pass
            finally:
                try:
                    page.close()
                except:
                    pass
        
        print("No authenticated session found")
        sys.exit(1)
        
except Exception as e:
    print(f"Error: {e}")
    sys.exit(1)
PYEOF

if [ $? -ne 0 ]; then
    log "ERROR: No authenticated Renatus session found"
    log "Make sure you're logged into backoffice.myrenatus.com"
    exit 1
fi

log "Renatus authentication verified"

# Step 3: Process unsubscribes
log "Step 3: Processing unsubscribes in Renatus..."

python3 "$SCRIPT_DIR/process_unsubscribes.py" \
    --file "$EMAILS_FILE" \
    --execute \
    --cdp-url "$CDP_URL" \
    2>&1 | tee -a "$LOG_FILE"

SYNC_STATUS=${PIPESTATUS[0]}

# Step 4: Clear processed unsubscribes from localStorage
if [ $SYNC_STATUS -eq 0 ]; then
    log "Step 4: Clearing processed unsubscribes from browser..."
    
    python3 << 'PYEOF'
import sys
from playwright.sync_api import sync_playwright

CDP_URL = "$CDP_URL"
EMAILS_FILE = "$EMAILS_FILE"

try:
    # Read processed emails
    with open(EMAILS_FILE) as f:
        processed = set(line.strip() for line in f if line.strip())
    
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(CDP_URL, timeout=30000)
        
        for context in browser.contexts:
            for page in context.pages:
                try:
                    page.evaluate("""
                        (processed) => {
                            try {
                                const current = JSON.parse(localStorage.getItem('unsubscribed') || '[]');
                                const remaining = current.filter(e => !processed.includes(e));
                                localStorage.setItem('unsubscribed', JSON.stringify(remaining));
                                return { before: current.length, after: remaining.length };
                            } catch {
                                return { error: true };
                            }
                        }
                    """, list(processed))
                except:
                    pass
        
        browser.close()
        print("Cleared processed unsubscribes")
        
except Exception as e:
    print(f"Warning: Could not clear localStorage: {e}")
    sys.exit(0)  # Non-fatal
PYEOF
fi

# Step 5: Generate report
log "Step 5: Generating report..."

REPORT=$(cat << REPORTEOF
{
    "sync_date": "$DATE_STR",
    "emails_processed": $EMAIL_COUNT,
    "status": "$([ $SYNC_STATUS -eq 0 ] && echo 'success' || echo 'failed')",
    "log_file": "$LOG_FILE",
    "emails_file": "$EMAILS_FILE"
}
REPORTEOF
)

echo "$REPORT" > "$REPORT_FILE"

log "=== Sync Complete ==="
log "Report: $REPORT_FILE"
log "Log: $LOG_FILE"

# Optional: Send notification (uncomment if you want email/Slack alerts)
# if [ $SYNC_STATUS -ne 0 ]; then
#     echo "Unsubscribe sync failed. Check $LOG_FILE" | mail -s "Unsubscribe Sync Failed" admin@example.com
# fi

exit $SYNC_STATUS
