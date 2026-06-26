#!/bin/bash
#
# Fetch supermarket specials using curl
# Usage: ./fetch_sales.sh [woolworths|coles|both]

STORE="${1:-both}"
USER_AGENT="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

fetch_woolworths() {
    echo "=== Woolworths Specials ==="
    echo "Date: $(date +%Y-%m-%d)"
    echo "URL: https://www.woolworths.com.au/shop/catalogue"
    echo ""
    
    # Try to fetch the page
    HTML=$(curl -s -L "https://www.woolworths.com.au/shop/catalogue" \
        -H "User-Agent: $USER_AGENT" \
        -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
        -H "Accept-Language: en-US,en;q=0.5" \
        --max-time 30 2>/dev/null)
    
    if [ -z "$HTML" ]; then
        echo "Error: Could not fetch Woolworths page"
        echo "Note: This site requires JavaScript. Try visiting manually:"
        echo "https://www.woolworths.com.au/shop/catalogue"
        return 1
    fi
    
    # Check if we got meaningful content
    TITLE=$(echo "$HTML" | grep -o '<title>[^<]*</title>' | sed 's/<[^\u003e]*>//g')
    echo "Page title: $TITLE"
    echo "Content length: ${#HTML} characters"
    echo ""
    
    # Try to extract prices
    echo "Sample prices found:"
    echo "$HTML" | grep -oE '\$[0-9]+\.?[0-9]*' | head -10
    
    echo ""
    echo "Note: Full extraction may require JavaScript rendering."
    echo "Consider using browser automation for complete results."
}

fetch_coles() {
    echo "=== Coles Specials ==="
    echo "Date: $(date +%Y-%m-%d)"
    echo "URL: https://www.coles.com.au/on-special"
    echo ""
    
    # Try to fetch the page
    HTML=$(curl -s -L "https://www.coles.com.au/on-special" \
        -H "User-Agent: $USER_AGENT" \
        -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
        -H "Accept-Language: en-US,en;q=0.5" \
        --max-time 30 2>/dev/null)
    
    if [ -z "$HTML" ]; then
        echo "Error: Could not fetch Coles page"
        echo "Note: This site requires JavaScript. Try visiting manually:"
        echo "https://www.coles.com.au/on-special"
        return 1
    fi
    
    # Check if we got meaningful content
    TITLE=$(echo "$HTML" | grep -o '<title>[^<]*</title>' | sed 's/<[^\u003e]*>//g')
    echo "Page title: $TITLE"
    echo "Content length: ${#HTML} characters"
    echo ""
    
    # Try to extract prices
    echo "Sample prices found:"
    echo "$HTML" | grep -oE '\$[0-9]+\.?[0-9]*' | head -10
    
    echo ""
    echo "Note: Full extraction may require JavaScript rendering."
    echo "Consider using browser automation for complete results."
}

# Main execution
case "$STORE" in
    woolworths)
        fetch_woolworths
        ;;
    coles)
        fetch_coles
        ;;
    both)
        fetch_woolworths
        echo ""
        echo "========================================"
        echo ""
        fetch_coles
        ;;
    *)
        echo "Usage: $0 [woolworths|coles|both]"
        exit 1
        ;;
esac
