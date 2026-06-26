// One-time login session capture.
// Pops up a real Chrome window. User logs in manually.
// On successful navigation away from /login, saves storageState.json + a structure summary.
//
// The structure summary (post-login-summary.json) dumps visible nav / heading / button text
// from the page right after login — useful when you (or Claude) are designing the stage flow
// and need to know what selectors are available without poking the live UI repeatedly.
const { chromium } = require('playwright');
const path = require('path');

const BASE = process.env.SCREENCAST_BASE || 'http://localhost:3000';
const LOGIN_PATH = process.env.SCREENCAST_LOGIN_PATH || '/login';
const VIEWPORT = {
  width: parseInt(process.env.SCREENCAST_VIEWPORT_W || '1440', 10),
  height: parseInt(process.env.SCREENCAST_VIEWPORT_H || '900', 10),
};

(async () => {
  const browser = await chromium.launch({
    headless: false,
    args: ['--disable-blink-features=AutomationControlled'],
  });
  const context = await browser.newContext({
    viewport: VIEWPORT,
    ignoreHTTPSErrors: true,
  });
  const page = await context.newPage();

  console.log(`[login] Opening ${BASE}${LOGIN_PATH}. Please log in in the browser window.`);
  await page.goto(`${BASE}${LOGIN_PATH}`, { timeout: 30000 });

  console.log('[login] Waiting for successful login (URL leaves login page)...');
  try {
    await page.waitForURL((url) => !url.toString().includes(LOGIN_PATH), { timeout: 600000 });
  } catch (e) {
    console.error('[login] Timed out waiting for login. Closing.');
    await browser.close();
    process.exit(2);
  }

  await page.waitForTimeout(2500); // let SPA settle
  console.log('[login] Logged in. Current URL:', page.url());
  console.log('[login] Title:', await page.title());

  // Post-login screenshot for structure exploration.
  await page.screenshot({ path: path.join(__dirname, 'post-login.png'), fullPage: false });

  // Dump visible structure to help author the stage flow.
  const summary = await page.evaluate(() => {
    const ts = (el) => (el.innerText || '').trim().replace(/\s+/g, ' ').slice(0, 100);
    const navItems = [...document.querySelectorAll('nav a, [role="navigation"] a, aside a, [class*="sidebar"] a, [class*="menu"] a')]
      .slice(0, 30)
      .map((el) => ({ text: ts(el), href: el.getAttribute('href') }));
    const headings = [...document.querySelectorAll('h1,h2,h3')]
      .slice(0, 20)
      .map((el) => ({ tag: el.tagName, text: ts(el) }));
    const buttons = [...document.querySelectorAll('button')]
      .slice(0, 30)
      .map((el) => ({ text: ts(el), title: el.title }))
      .filter((b) => b.text);
    return { url: location.href, navItems, headings, buttons };
  });
  require('fs').writeFileSync(path.join(__dirname, 'post-login-summary.json'), JSON.stringify(summary, null, 2));

  await context.storageState({ path: path.join(__dirname, 'storageState.json') });
  console.log('[login] Storage state saved.');

  await browser.close();
  console.log('[login] DONE');
})();
