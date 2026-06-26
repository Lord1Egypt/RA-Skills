#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

function parseArgs(argv) {
  const args = { url: '', outputHtml: '', outputShot: '', outputText: '', waitMs: 5000, selector: '' };
  for (let i = 2; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--url') args.url = argv[++i];
    else if (a === '--output-html') args.outputHtml = argv[++i];
    else if (a === '--output-shot') args.outputShot = argv[++i];
    else if (a === '--output-text') args.outputText = argv[++i];
    else if (a === '--wait-ms') args.waitMs = Number(argv[++i] || 5000);
    else if (a === '--selector') args.selector = argv[++i];
    else throw new Error(`Unknown arg: ${a}`);
  }
  if (!args.url) throw new Error('Missing --url');
  if (!args.outputHtml) throw new Error('Missing --output-html');
  return args;
}

async function main() {
  const args = parseArgs(process.argv);
  let chromiumPath = null;
  for (const p of ['/usr/bin/google-chrome-stable', '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser']) {
    if (fs.existsSync(p)) { chromiumPath = p; break; }
  }
  if (!chromiumPath) {
    console.error('No Chromium-based browser found. Install Chrome/Chromium first.');
    process.exit(2);
  }

  let playwright;
  try {
    playwright = require('playwright-core');
  } catch (e) {
    console.error('Missing dependency: playwright-core');
    console.error('Install with: npm install playwright-core');
    process.exit(2);
  }

  const browser = await playwright.chromium.launch({
    executablePath: chromiumPath,
    headless: true,
    args: ['--no-sandbox', '--disable-dev-shm-usage']
  });
  const page = await browser.newPage({ viewport: { width: 1440, height: 2200 } });
  await page.goto(args.url, { waitUntil: 'domcontentloaded', timeout: 120000 });
  if (args.selector) {
    try {
      await page.waitForSelector(args.selector, { timeout: 15000 });
    } catch (_) {}
  }
  await page.waitForTimeout(args.waitMs);
  const html = await page.content();
  fs.writeFileSync(path.resolve(args.outputHtml), html, 'utf8');
  if (args.outputText) {
    const text = await page.evaluate((selector) => {
      const selectors = selector ? [selector] : ['#js_content', '.rich_media_content', 'article', 'main', 'body'];
      for (const sel of selectors) {
        const el = document.querySelector(sel);
        if (el && el.innerText && el.innerText.trim()) return el.innerText.trim();
      }
      return document.body ? document.body.innerText.trim() : '';
    }, args.selector || '');
    fs.writeFileSync(path.resolve(args.outputText), text, 'utf8');
  }
  if (args.outputShot) {
    await page.screenshot({ path: path.resolve(args.outputShot), fullPage: true });
  }
  await browser.close();
}

main().catch(err => {
  console.error(err && err.stack ? err.stack : String(err));
  process.exit(1);
});
