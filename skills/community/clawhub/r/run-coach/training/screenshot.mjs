// screenshot.mjs — Render an HTML file to a full-page HD PNG using Playwright
//
// Uses chrome-headless-shell (not full Chrome) to avoid SIGTRAP crash
// when running as a non-root user inside Docker containers.
//
// Usage: node screenshot.mjs <input.html> <output.png>

import { chromium } from '/app/node_modules/playwright-core/index.mjs';
import { readdirSync, existsSync } from 'fs';
import { join } from 'path';

const [,, htmlFile, outFile] = process.argv;
if (!htmlFile || !outFile) {
  console.log('Usage: node screenshot.mjs <input.html> <output.png>');
  process.exit(1);
}

// Auto-detect chrome-headless-shell binary path using native fs only
function findHeadlessShell() {
  const base = '/home/node/.cache/ms-playwright';
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

const browser = await chromium.launch({
  headless: true,
  executablePath,
  args: ['--no-sandbox', '--disable-setuid-sandbox']
});

const context = await browser.newContext({
  viewport: { width: 1200, height: 800 },
  deviceScaleFactor: 2  // 2400px output width — sharp text, within Telegram's 10000px total limit
});

const page = await context.newPage();
await page.goto('file://' + htmlFile, { waitUntil: 'networkidle' });
await page.screenshot({ path: outFile, type: 'png', fullPage: true });
await browser.close();

console.log('done: ' + outFile);
