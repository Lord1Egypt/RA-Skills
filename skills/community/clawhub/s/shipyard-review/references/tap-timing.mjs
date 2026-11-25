// Tap timing at phone size: how long until a tapped tab looks active, and until its content shows.
// Usage: node tap-timing.mjs <base url> <start path> "Label A,Label B,..." [--nav "nav a"] [--cpu 4]
// Needs Playwright (npm i -D playwright && npx playwright install chromium). Signed-in screens: pass
// --storage <file> made with Playwright's storageState after signing in by hand.
import { chromium } from 'playwright';

const [base, start = '/', labelsArg = ''] = process.argv.slice(2).filter((a, i, all) => !a.startsWith('--') && !all[i - 1]?.startsWith('--'));
const opt = (name, dflt) => { const i = process.argv.indexOf(`--${name}`); return i > -1 ? process.argv[i + 1] : dflt; };
if (!base || !labelsArg) { console.log('Usage: node tap-timing.mjs <base url> <start path> "Tab A,Tab B" [--nav "nav a"] [--cpu 4] [--storage file]'); process.exit(1); }
const NAV = opt('nav', 'nav a');

const browser = await chromium.launch();
const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, deviceScaleFactor: 3, isMobile: true, hasTouch: true, storageState: opt('storage') });
const page = await ctx.newPage();
await (await ctx.newCDPSession(page)).send('Emulation.setCPUThrottlingRate', { rate: Number(opt('cpu', 4)) });
let requests = 0;
page.on('request', () => requests++);
await page.goto(new URL(start, base).href, { waitUntil: 'networkidle' });

const rows = [];
for (const label of labelsArg.split(',').map((s) => s.trim())) {
  const link = page.locator(NAV, { hasText: label }).first();
  const href = await link.getAttribute('href');
  const box = await link.boundingBox();
  const x = box.x + box.width / 2, y = box.y + box.height / 2;
  const under = await page.evaluate(([px, py]) => { const e = document.elementFromPoint(px, py); return e?.closest('a')?.getAttribute('href') ?? `${e?.tagName}.${e?.className}`; }, [x, y]);
  const before = await link.evaluate((a) => getComputedStyle(a).color);
  requests = 0;
  await page.evaluate(() => { window.__t0 = performance.now(); });
  const tap = page.touchscreen.tap(x, y);
  // "Looks active": colour changed, or aria-current / data-active set.
  const highlight = await page.waitForFunction(([h, c]) => {
    const a = [...document.querySelectorAll('a')].find((el) => el.getAttribute('href') === h && el.offsetParent);
    return a && (getComputedStyle(a).color !== c || a.getAttribute('aria-current') === 'page' || a.hasAttribute('data-active')) ? performance.now() - window.__t0 : false;
  }, [href, before], { polling: 'raf', timeout: 20000 }).then((h) => h.jsonValue()).catch(() => null);
  await tap;
  const content = await page.waitForFunction((h) => (location.pathname === new URL(h, location.href).pathname && !document.querySelector('.skeleton,[aria-busy="true"]') ? performance.now() - window.__t0 : false), href, { polling: 'raf', timeout: 20000 }).then((h) => h.jsonValue()).catch(() => null);
  rows.push({ tap: label, underTap: under === href ? 'ok' : under, highlightMs: highlight && Math.round(highlight), contentMs: content && Math.round(content), requests });
  await page.waitForTimeout(800);
}
console.table(rows);
const slow = rows.filter((r) => r.highlightMs === null || r.highlightMs > 100 || r.contentMs === null || r.contentMs > 1000);
if (slow.length) console.log(`Over budget: ${slow.map((r) => r.tap).join(', ')} (highlight 100 ms, content 1 s; 300 ms on a second visit).`);
await browser.close();
