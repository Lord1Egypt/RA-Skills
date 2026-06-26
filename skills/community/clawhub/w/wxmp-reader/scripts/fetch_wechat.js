#!/usr/bin/env node
/**
 * fetch_wechat.js — Read WeChat Official Account (公众号) articles
 *
 * Bypasses WeChat's anti-bot detection by emulating a real mobile browser.
 * Requires: playwright-core (npm) + a Chrome/Chromium binary on the system.
 *
 * Usage:
 *   node fetch_wechat.js <url> [options]
 *
 * Options:
 *   --json              Output as JSON (title, author, date, content)
 *   --max-chars=N       Truncate content to N characters (default: 0 = no limit)
 *   --chrome-path=PATH  Override Chrome binary path (auto-detected by default)
 *
 * Exit codes:
 *   0  Success
 *   1  Error (missing args, page blocked, Chrome not found, etc.)
 */

// ─── Resolve playwright-core ──────────────────────────────────
let chromium;
try {
  ({ chromium } = require('playwright-core'));
} catch {
  // When running inside OpenClaw, playwright-core lives in OpenClaw's node_modules.
  // Search common locations (nvm, global node_modules, /usr).
  const { execSync } = require('child_process');
  const searchDirs = [
    process.env.NVM_DIR || `${process.env.HOME}/.nvm`,
    '/usr/lib/node_modules',
    '/usr/local/lib/node_modules',
    '/usr',
  ].join(' ');
  const searchResult = execSync(
    `find ${searchDirs} -name 'playwright-core' -path '*/node_modules/*' -type d 2>/dev/null | head -1`,
    { encoding: 'utf-8' }
  ).trim();
  if (!searchResult) {
    console.error('Error: playwright-core not found. Install with: npm install -g playwright-core');
    process.exit(1);
  }
  ({ chromium } = require(searchResult));
}

// ─── Resolve Chrome binary ────────────────────────────────────
function findChrome() {
  const candidates = [
    '/usr/bin/google-chrome-stable',
    '/usr/bin/google-chrome',
    '/usr/bin/chromium-browser',
    '/usr/bin/chromium',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  ];
  const fs = require('fs');
  for (const p of candidates) {
    if (fs.existsSync(p)) return p;
  }
  // Last resort: try `which`
  try {
    const { execSync } = require('child_process');
    return execSync('which google-chrome-stable || which google-chrome || which chromium', {
      encoding: 'utf-8',
    }).trim().split('\n')[0];
  } catch {
    return null;
  }
}

// ─── Parse arguments ──────────────────────────────────────────
const args = process.argv.slice(2);
const url = args.find(a => a.startsWith('http'));
const jsonMode = args.includes('--json');
const maxCharsArg = args.find(a => a.startsWith('--max-chars='));
const maxChars = maxCharsArg ? parseInt(maxCharsArg.split('=')[1]) : 0;
const chromeArg = args.find(a => a.startsWith('--chrome-path='));
const chromePath = chromeArg ? chromeArg.split('=').slice(1).join('=') : findChrome();

if (!url) {
  console.error('Usage: node fetch_wechat.js <wechat-article-url> [--json] [--max-chars=N] [--chrome-path=PATH]');
  process.exit(1);
}

if (!chromePath) {
  console.error('Error: Chrome/Chromium not found. Install it or specify --chrome-path=');
  process.exit(1);
}

// ─── Main ─────────────────────────────────────────────────────
(async () => {
  const browser = await chromium.launch({
    headless: true,
    executablePath: chromePath,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-blink-features=AutomationControlled',
    ],
  });

  const context = await browser.newContext({
    // Mobile UA — WeChat's anti-bot is much more lenient on mobile
    userAgent:
      'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    viewport: { width: 390, height: 844 },
    locale: 'zh-CN',
    timezoneId: 'Asia/Shanghai',
  });

  // Remove the navigator.webdriver fingerprint (primary bot detection signal)
  await context.addInitScript(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
  });

  const page = await context.newPage();

  try {
    await page.goto(url, { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(1500);
  } catch (e) {
    console.error('Page load failed:', e.message);
    await browser.close();
    process.exit(1);
  }

  // ─── Extract article content ───────────────────────────────
  const result = await page.evaluate(() => {
    const titleEl = document.querySelector('#activity-name, .rich_media_title');
    const authorEl = document.querySelector('#js_name, .account_nickname_inner');
    const dateEl = document.querySelector('#publish_time, .rich_media_meta_text');
    const contentEl = document.querySelector('#js_content, .rich_media_content');

    return {
      title: titleEl ? titleEl.innerText.trim() : document.title || '',
      author: authorEl ? authorEl.innerText.trim() : '',
      date: dateEl ? dateEl.innerText.trim() : '',
      content: contentEl ? contentEl.innerText.trim() : '',
    };
  });

  await browser.close();

  // ─── Validate ──────────────────────────────────────────────
  if (!result.content || result.content.length < 50) {
    console.error('Warning: Content appears empty or too short.');
    console.error('Possible causes: article deleted, paywalled, followers-only, or CAPTCHA triggered.');
    console.error('Tip: retrying often works if it was a transient CAPTCHA.');
    process.exit(1);
  }

  // ─── Truncate if requested ─────────────────────────────────
  let content = result.content;
  if (maxChars > 0 && content.length > maxChars) {
    content =
      content.substring(0, maxChars) +
      `\n\n[Truncated: showing ${maxChars} of ${result.content.length} chars]`;
  }

  // ─── Output ────────────────────────────────────────────────
  if (jsonMode) {
    console.log(JSON.stringify({ ...result, content }, null, 2));
  } else {
    console.log(`Title: ${result.title}`);
    if (result.author) console.log(`Author: ${result.author}`);
    if (result.date) console.log(`Date: ${result.date}`);
    console.log('─'.repeat(60));
    console.log(content);
  }
})();
