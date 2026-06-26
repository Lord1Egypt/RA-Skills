#!/usr/bin/env bash
# web-screenshot - Capture web page screenshots or PDFs using Playwright
# Usage:
#   screenshot.sh <url> [output_path] [--fullpage] [--pdf]
#   screenshot.sh https://example.com /tmp/ss.png        # screenshot
#   screenshot.sh https://example.com /tmp/ss.png --fullpage  # full page
#   screenshot.sh https://example.com /tmp/ss.pdf --pdf  # PDF export

set -e

URL="$1"
OUTPUT="$2"
MODE="${3:-screenshot}"

if [ -z "$URL" ]; then
  echo "Usage: screenshot.sh <url> [output_path] [--fullpage|--pdf]"
  exit 1
fi

# Default output path
if [ -z "$OUTPUT" ]; then
  TIMESTAMP=$(date +%Y%m%d_%H%M%S)
  if [ "$MODE" = "--pdf" ]; then
    OUTPUT="/tmp/openclaw/screenshot_${TIMESTAMP}.pdf"
  else
    OUTPUT="/tmp/openclaw/screenshot_${TIMESTAMP}.png"
  fi
fi

mkdir -p "$(dirname "$OUTPUT")"

PLAYWRIGHT_SCRIPT=$(mktemp /tmp/pw_ss_XXXXXX.js)

if [ "$MODE" = "--pdf" ]; then
  cat > "$PLAYWRIGHT_SCRIPT" << 'JSEOF'
const { chromium } = require('playwright');
const url = process.argv[2];
const output = process.argv[3];
(async () => {
  const browser = await chromium.launch({ headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.emulateMedia({ media: 'screen' });
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 20000 });
  await page.waitForTimeout(3000);
  await page.pdf({ path: output, format: 'A4', printBackground: true, margin: { top: '1cm', bottom: '1cm' } });
  await browser.close();
  console.log('PDF saved:', output);
})().catch(e => { console.error('ERROR:', e.message); process.exit(1); });
JSEOF
else
  FULLPAGE_FLAG="false"
  if [ "$MODE" = "--fullpage" ]; then FULLPAGE_FLAG="true"; fi
  cat > "$PLAYWRIGHT_SCRIPT" << JSEOF
const { chromium } = require('playwright');
const url = process.argv[2];
const output = process.argv[3];
const fullPage = process.argv[4] === 'true';
(async () => {
  const browser = await chromium.launch({ headless: true, args: ['--no-sandbox', '--disable-setuid-sandbox'] });
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 20000 });
  await page.waitForTimeout(3000);
  await page.screenshot({ path: output, fullPage: fullPage });
  await browser.close();
  const size = require('fs').statSync(output).size;
  console.log('OK ' + (size/1024).toFixed(0) + 'KB saved:', output);
})().catch(e => { console.error('ERROR:', e.message); process.exit(1); });
JSEOF
fi

NODE_PATH=/root/.npm/_npx/e41f203b7505f1fb/node_modules \
  node "$PLAYWRIGHT_SCRIPT" "$URL" "$OUTPUT" "$FULLPAGE_FLAG" 2>/dev/null

rm -f "$PLAYWRIGHT_SCRIPT"
