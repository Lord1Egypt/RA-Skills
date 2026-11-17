// screenshot.mjs — Render an HTML file to a full-page HD PNG using Playwright
//
// Uses chrome-headless-shell (not full Chrome) to avoid SIGTRAP crash
// when running as a non-root user inside Docker containers.
//
// Usage: node screenshot.mjs <input.html> <output.png>

import { chromium } from 'playwright-core';
import { readdirSync, existsSync } from 'fs';
import { join, resolve } from 'path';
import { pathToFileURL } from 'url';

const [,, htmlFile, outFile] = process.argv;
if (!htmlFile || !outFile) {
  console.log('Usage: node screenshot.mjs <input.html> <output.png>');
  process.exit(1);
}

// Auto-detect chrome-headless-shell binary path using native fs (no child_process)
function findHeadlessShell() {
  // Standard Playwright cache locations; override with PLAYWRIGHT_BROWSERS_PATH
  const base = process.env.PLAYWRIGHT_BROWSERS_PATH
    || join(process.env.HOME || '', '.cache', 'ms-playwright');
  if (!existsSync(base)) return null;
  for (const dir of readdirSync(base)) {
    const candidate = join(base, dir, 'chrome-headless-shell-linux64', 'chrome-headless-shell');
    if (existsSync(candidate)) return candidate;
  }
  return null;
}

const executablePath = findHeadlessShell();
if (!executablePath) {
  console.error('chrome-headless-shell not found. Run setup.sh first.');
  process.exit(1);
}

// --no-sandbox is required for chrome-headless-shell as a non-root user inside
// Docker. The page it renders is made inert instead: JavaScript is disabled,
// every non-file:// request is blocked, and text-to-image.sh HTML-escapes all
// plan content before it reaches the page.
const browser = await chromium.launch({
  headless: true,
  executablePath,
  args: ['--no-sandbox', '--disable-setuid-sandbox']
});

const context = await browser.newContext({
  viewport: { width: 1200, height: 800 },
  deviceScaleFactor: 2,  // 2400px output width — sharp text, within Telegram's 10000px total limit
  javaScriptEnabled: false,
  offline: true
});

const page = await context.newPage();
// Local-only rendering: the plan page never loads anything over the network.
await page.route('**/*', route =>
  route.request().url().startsWith('file://') ? route.continue() : route.abort()
);
await page.goto(pathToFileURL(resolve(htmlFile)).href, { waitUntil: 'load' });
await page.screenshot({ path: outFile, type: 'png', fullPage: true });
await browser.close();

console.log('done: ' + outFile);
