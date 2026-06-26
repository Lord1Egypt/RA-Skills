#!/usr/bin/env node
/**
 * Web Screenshot Tool
 * Usage: node screenshot.js <config.json>
 *
 * Captures screenshots of web pages, handling SPA login via form submission
 * or direct Pinia store calls. Uses $router.push() for SPA navigation to
 * preserve auth state across page transitions.
 */

const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');

const sleep = ms => new Promise(r => setTimeout(r, ms));

// Parse args
const configPath = process.argv[2];
if (!configPath) {
  console.error('Usage: node screenshot.js <config.json>');
  process.exit(1);
}

const config = JSON.parse(fs.readFileSync(path.resolve(configPath), 'utf-8'));

const {
  baseUrl,
  outputDir,
  resolution = [1920, 1080],
  login,
  pages,
  descriptions = {}
} = config;

const [vpWidth, vpHeight] = resolution;

// Ensure output dir exists
fs.mkdirSync(outputDir, { recursive: true });

(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/usr/bin/chromium-browser',
    headless: 'new',
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-gpu',
      `--window-size=${vpWidth},${vpHeight}`,
      '--disable-dev-shm-usage'
    ]
  });

  const page = await browser.newPage();
  await page.setViewport({ width: vpWidth, height: vpHeight });

  const screenshots = [];

  // ---- Helper: take screenshot ----
  async function capture(filepath) {
    await page.screenshot({ path: filepath, fullPage: false });
  }

  // ---- Helper: login page screenshot (before login) ----
  async function captureLoginPage(p) {
    console.log(`  Capturing login page: ${p.name}...`);
    await page.goto(baseUrl + p.path, { waitUntil: 'networkidle2', timeout: 20000 });
    await sleep(p.waitMs || 2000);
    const filepath = path.join(outputDir, `${p.name}.png`);
    await capture(filepath);
    screenshots.push({ filename: `${p.name}.png`, name: p.name, path: p.path });
    console.log(`    -> saved ${p.name}.png`);
  }

  // ---- Helper: form-based login ----
  async function formLogin() {
    const l = login;
    console.log('  Logging in via form...');

    // Navigate to login page if not already there
    if (!page.url().includes(l.url)) {
      await page.goto(baseUrl + l.url, { waitUntil: 'networkidle2', timeout: 20000 });
      await sleep(1000);
    }

    // Set input values using native setter (Vue-reactive compatible)
    await page.evaluate(({ uSel, pSel, username, password }) => {
      const setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
      const uInput = document.querySelector(uSel);
      const pInput = document.querySelector(pSel);
      if (uInput) { setter.call(uInput, username); uInput.dispatchEvent(new Event('input', { bubbles: true })); }
      if (pInput) { setter.call(pInput, password); pInput.dispatchEvent(new Event('input', { bubbles: true })); }
    }, {
      uSel: l.usernameSelector,
      pSel: l.passwordSelector,
      username: l.credentials.username,
      password: l.credentials.password
    });

    await sleep(300);

    // Click submit
    const btn = await page.$(l.submitSelector);
    if (btn) {
      await btn.click();
    }

    // Wait for SPA navigation
    try {
      await page.waitForFunction(
        () => window.location.pathname !== new URL(window.location.href).pathname || document.title !== '',
        { timeout: 10000 }
      );
    } catch (e) {
      // timeout is ok
    }
    await sleep(3000);
    console.log(`    -> URL after login: ${page.url()}`);
  }

  // ---- Helper: Pinia store login ----
  async function storeLogin() {
    const sl = login.storeLogin;
    console.log(`  Logging in via Pinia store: ${sl.storeName}.${sl.method}(${JSON.stringify(sl.args)})...`);

    // Navigate to login page first to initialize the Vue app
    await page.goto(baseUrl + (login.url || '/login'), { waitUntil: 'networkidle2', timeout: 20000 });
    await sleep(1000);

    await page.evaluate(({ storeName, method, args }) => {
      const app = document.querySelector('#app').__vue_app__;
      if (app) {
        const pinia = app.config.globalProperties.$pinia;
        if (pinia && pinia._s) {
          const store = pinia._s.get(storeName);
          if (store) {
            store[method](...args);
          } else {
            console.error(`Store "${storeName}" not found. Available:`, [...pinia._s.keys()]);
          }
        }
      }
    }, sl);

    await sleep(1000);
  }

  // ---- Helper: SPA navigation using $router.push ----
  async function spaNavigate(targetPath, waitMs) {
    await page.evaluate((p) => {
      const app = document.querySelector('#app').__vue_app__;
      if (app && app.config.globalProperties.$router) {
        app.config.globalProperties.$router.push(p);
      }
    }, targetPath);
    await sleep(waitMs);
  }

  // ---- Helper: fallback navigation via page.goto ----
  async function gotoNavigate(targetPath, waitMs) {
    await page.goto(baseUrl + targetPath, { waitUntil: 'networkidle2', timeout: 15000 });
    await sleep(waitMs);
  }

  // ===== Main flow =====
  let isLoggedIn = false;

  // Step 1: Capture any login pages first (before logging in)
  const loginPages = pages.filter(p => p.isLoginPage);
  for (const lp of loginPages) {
    await captureLoginPage(lp);
  }

  // Step 2: Login if configured
  if (login) {
    if (login.storeLogin) {
      await storeLogin();
      isLoggedIn = true;
    } else if (login.usernameSelector) {
      await formLogin();
      isLoggedIn = !page.url().includes('login');
    }
  }

  // Step 3: Capture remaining pages
  const otherPages = pages.filter(p => !p.isLoginPage);
  const useSpaNav = isLoggedIn;

  for (let i = 0; i < otherPages.length; i++) {
    const p = otherPages[i];
    const waitMs = p.waitMs || 2000;
    console.log(`  [${i + 1}/${otherPages.length}] ${p.name} -> ${p.path}...`);

    try {
      if (useSpaNav) {
        await spaNavigate(p.path, waitMs);
      } else {
        await gotoNavigate(p.path, waitMs);
      }
    } catch (e) {
      console.log(`    -> Navigation error: ${e.message}, trying fallback...`);
      await gotoNavigate(p.path, waitMs);
    }

    const filepath = path.join(outputDir, `${p.name}.png`);
    await capture(filepath);
    screenshots.push({ filename: `${p.name}.png`, name: p.name, path: p.path });
    console.log(`    -> saved ${p.name}.png (URL: ${page.url()})`);
  }

  await browser.close();

  // ===== Generate result.json =====
  const resultJson = {
    project: 'web-screenshot capture',
    captureDate: new Date().toISOString().split('T')[0],
    baseUrl,
    resolution: `${vpWidth}x${vpHeight}`,
    screenshots: screenshots.map(s => ({
      filename: s.filename,
      title: s.name.replace(/^\d+_/, '').replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase()),
      url: baseUrl + s.path,
      description: descriptions[s.name] || ''
    }))
  };

  const resultPath = path.join(outputDir, 'result.json');
  fs.writeFileSync(resultPath, JSON.stringify(resultJson, null, 2), 'utf-8');

  console.log(`\n=== Done! ${screenshots.length} screenshots saved to ${outputDir} ===`);
  console.log(`    result.json -> ${resultPath}`);
})();
