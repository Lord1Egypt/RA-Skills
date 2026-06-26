#!/usr/bin/env node
/**
 * Stealth Google Search Example
 * Demonstrates bot-detection-free Google search with human-like typing
 *
 * Usage: node stealth-google-search.mjs "search query"
 * Requires: npm install rebrowser-playwright
 */

import os from 'node:os';
import path from 'node:path';
import { createStealthBrowser, humanType, humanDelay, simulateMouseMovement } from '../scripts/stealth-template.mjs';

const searchQuery = process.argv[2] || 'Playwright automation';

async function stealthGoogleSearch(query) {
  console.log(`Searching Google for: "${query}"\n`);

  const { browser, page } = await createStealthBrowser();

  try {
    await page.goto('https://www.google.com', { waitUntil: 'domcontentloaded' });
    await page.waitForSelector('textarea[name="q"]', { timeout: 10000 });

    // Simulate natural mouse movement before typing
    await simulateMouseMovement(page);

    // Human-like typing instead of instant fill
    await humanType(page, 'textarea[name="q"]', query);
    await humanDelay(300, 800);
    await page.press('textarea[name="q"]', 'Enter');

    await page.waitForSelector('div.g, #captcha, #sorry', { timeout: 10000 }).catch(() => {});

    const url = page.url();
    if (url.includes('sorry')) {
      console.log('CAPTCHA detected! Bot detection triggered.');
    } else {
      console.log('Search successful! No CAPTCHA.');

      const results = await page.evaluate(() => {
        const items = document.querySelectorAll('div.g');
        return Array.from(items).slice(0, 5).map(item => {
          const title = item.querySelector('h3')?.textContent || '';
          const link = item.querySelector('a')?.href || '';
          return { title, link };
        });
      });

      console.log('\nTop Results:');
      results.forEach((r, i) => {
        console.log(`${i + 1}. ${r.title}`);
        console.log(`   ${r.link}\n`);
      });
    }

    const outOk = path.join(os.tmpdir(), 'google-search-result.png');
    await page.screenshot({ path: outOk });
    console.log(`Screenshot saved: ${outOk}\n`);
  } catch (err) {
    console.error('Error:', err.message);
    await page.screenshot({ path: path.join(os.tmpdir(), 'google-search-error.png') }).catch(() => {});
  } finally {
    await browser.close();
  }
}

stealthGoogleSearch(searchQuery).catch(console.error);
