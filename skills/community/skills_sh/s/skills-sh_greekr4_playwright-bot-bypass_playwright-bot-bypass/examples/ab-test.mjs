#!/usr/bin/env node
/**
 * A/B Test: Detected vs Stealth
 * Compare bot detection between standard playwright and stealth mode
 *
 * Usage: node ab-test.mjs
 * Requires: npm install rebrowser-playwright playwright
 */

import os from 'node:os';
import path from 'node:path';
import { createStealthBrowser } from '../scripts/stealth-template.mjs';

let chromiumStandard;
try {
  const pw = await import('playwright');
  chromiumStandard = pw.chromium;
} catch {
  console.error('Standard "playwright" package not installed.');
  console.error('Run: npm install playwright && npx playwright install chromium');
  console.error('\nSkipping A side — running stealth-only test.\n');
}

console.log('='.repeat(45));
console.log('      A/B TEST: Detected vs Stealth        ');
console.log('='.repeat(45) + '\n');

let browserA, browserB;

try {
  // A: Standard Playwright (will be detected)
  let resultA = { webdriver: 'skipped', renderer: 'skipped' };
  if (chromiumStandard) {
    console.log('[A] Starting standard Playwright...');
    browserA = await chromiumStandard.launch({
      headless: false,
      channel: 'chrome',
      args: ['--window-position=0,0']
    });
    const contextA = await browserA.newContext({ viewport: { width: 640, height: 700 } });
    const pageA = await contextA.newPage();

    await pageA.goto('https://bot.sannysoft.com', { waitUntil: 'networkidle' });
    await pageA.waitForSelector('table tr td', { timeout: 10000 });

    resultA = await pageA.evaluate(() => {
      const get = (name) => {
        for (const row of document.querySelectorAll('table tr')) {
          if (row.textContent.includes(name)) {
            const cells = row.querySelectorAll('td');
            return cells.length >= 2 ? cells[1].textContent.trim() : 'N/A';
          }
        }
        return 'N/A';
      };
      return { webdriver: get('WebDriver'), renderer: get('WebGL Renderer') };
    });

    await pageA.screenshot({ path: path.join(os.tmpdir(), 'ab-test-detected.png') });
  }

  // B: Stealth mode (will bypass detection)
  console.log('[B] Starting stealth Rebrowser...');
  const { browser, page: pageB } = await createStealthBrowser({
    viewport: { width: 640, height: 700 }
  });
  browserB = browser;

  await pageB.goto('https://bot.sannysoft.com', { waitUntil: 'networkidle' });
  await pageB.waitForSelector('table tr td', { timeout: 10000 });

  const resultB = await pageB.evaluate(() => {
    const get = (name) => {
      for (const row of document.querySelectorAll('table tr')) {
        if (row.textContent.includes(name)) {
          const cells = row.querySelectorAll('td');
          return cells.length >= 2 ? cells[1].textContent.trim() : 'N/A';
        }
      }
      return 'N/A';
    };
    return { webdriver: get('WebDriver'), renderer: get('WebGL Renderer') };
  });

  await pageB.screenshot({ path: path.join(os.tmpdir(), 'ab-test-stealth.png') });

  // Results
  console.log('\n' + '='.repeat(45));
  console.log('               RESULTS                     ');
  console.log('='.repeat(45));
  console.log(`[A] Standard:  WebDriver=${resultA.webdriver}`);
  console.log(`               Renderer=${resultA.renderer}`);
  console.log(`[B] Stealth:   WebDriver=${resultB.webdriver}`);
  console.log(`               Renderer=${resultB.renderer}`);
  console.log('='.repeat(45));
  console.log(`\nScreenshots: ${path.join(os.tmpdir(), 'ab-test-detected.png')}, ${path.join(os.tmpdir(), 'ab-test-stealth.png')}\n`);

} catch (err) {
  console.error('Error:', err.message);
} finally {
  await browserA?.close().catch(() => {});
  await browserB?.close().catch(() => {});
}

console.log('Done!');
