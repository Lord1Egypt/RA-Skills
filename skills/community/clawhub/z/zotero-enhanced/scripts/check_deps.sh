#!/bin/bash
set -e

# Zotero Enhanced dependency checker
# Validates required commands and environment variables

# --- Argument handling ---
case "$1" in
    --help|-h)
        cat <<EOF
Usage: $0
Check that all dependencies for Zotero Enhanced are installed.

Environment variables checked (not required to be set):
  ZOTERO_USER_ID, ZOTERO_API_KEY, WEBDAV_URL, WEBDAV_USER, WEBDAV_PASS

Version: zotero-enhanced check_deps.sh v1.3.8
EOF
        exit 0
        ;;
    --version)
        echo "zotero-enhanced check_deps.sh v1.3.8"
        exit 0
        ;;
esac

echo "🔍 Checking Zotero Enhanced dependencies..."

# --- Check commands ---
ERRORS=0
for cmd in curl jq pdftotext zip unzip; do
    if command -v "$cmd" >/dev/null 2>&1; then
        echo "  ✅ $cmd"
    else
        echo "  ❌ $cmd (missing)"
        ERRORS=$((ERRORS + 1))
    fi
done

# Platform-specific md5 check
if command -v md5sum >/dev/null 2>&1 || command -v md5 >/dev/null 2>&1; then
    echo "  ✅ md5 utility (md5sum or md5)"
else
    echo "  ❌ md5 utility (neither md5sum nor md5 found)"
    ERRORS=$((ERRORS + 1))
fi

# Platform-specific stat check
if stat -c %Y /dev/null >/dev/null 2>&1 || stat -f %m /dev/null >/dev/null 2>&1; then
    echo "  ✅ stat utility (Linux or macOS style)"
else
    echo "  ❌ stat utility (unsupported options)"
    ERRORS=$((ERRORS + 1))
fi

# --- Check environment variables ---
echo ""
echo "📋 Checking environment variables..."

if [ -n "$ZOTERO_USER_ID" ]; then
    echo "  ✅ ZOTERO_USER_ID is set"
else
    echo "  ⚠️  ZOTERO_USER_ID is not set (required for all operations)"
fi

if [ -n "$ZOTERO_API_KEY" ]; then
    echo "  ✅ ZOTERO_API_KEY is set"
else
    echo "  ⚠️  ZOTERO_API_KEY is not set (required for all operations)"
fi

if [ -n "$WEBDAV_URL" ] && [ -n "$WEBDAV_USER" ] && [ -n "$WEBDAV_PASS" ]; then
    echo "  ✅ WebDAV variables are set (will use WebDAV storage)"
elif [ -n "$WEBDAV_URL" ] || [ -n "$WEBDAV_USER" ] || [ -n "$WEBDAV_PASS" ]; then
    echo "  ⚠️  Partial WebDAV variables set (missing: $( [ -z "$WEBDAV_URL" ] && echo "WEBDAV_URL " ; [ -z "$WEBDAV_USER" ] && echo "WEBDAV_USER " ; [ -z "$WEBDAV_PASS" ] && echo "WEBDAV_PASS" )) - will fall back to Zotero cloud storage"
else
    echo "  ℹ️  No WebDAV variables set (will use Zotero cloud storage)"
fi

# --- Summary ---
echo ""
if [ $ERRORS -eq 0 ]; then
    echo "✅ All dependencies satisfied."
    echo "   You can now use the Zotero Enhanced scripts."
    echo ""
    echo "Quick test:"
    echo "  ZOTERO_USER_ID=\"\$ZOTERO_USER_ID\" ZOTERO_API_KEY=\"\$ZOTERO_API_KEY\" \\"
    echo "  bash scripts/search.sh \"test\""
    exit 0
else
    echo "❌ Missing $ERRORS dependency(ies). Please install missing packages."
    echo ""
    echo "Install missing packages:"
    echo "  Debian/Ubuntu: sudo apt-get install curl jq poppler-utils zip"
    echo "  macOS: brew install curl jq poppler zip"
    exit 1
fi