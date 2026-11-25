// Screenshot every NN-*.html mockup in a folder at phone size, plus index.html at desktop size.
// Usage: node shot.mjs <folder>   (needs: npm i -D playwright && npx playwright install chromium)
import { chromium } from 'playwright';
import { readdirSync } from 'node:fs';
import path from 'node:path';

const dir = path.resolve(process.argv[2] || '.');
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 2 });
for (const f of readdirSync(dir).filter((n) => /^\d\d-.*\.html$/.test(n)).sort()) {
  await page.goto('file://' + path.join(dir, f));
  await page.screenshot({ path: path.join(dir, f.replace(/\.html$/, '.png')) });
}
await page.setViewportSize({ width: 1440, height: 1000 });
await page.goto('file://' + path.join(dir, 'index.html'));
await page.screenshot({ path: path.join(dir, 'index.png'), fullPage: true });
await browser.close();
