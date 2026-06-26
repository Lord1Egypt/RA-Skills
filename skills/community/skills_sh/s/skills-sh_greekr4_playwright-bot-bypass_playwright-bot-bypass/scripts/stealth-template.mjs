#!/usr/bin/env node
/**
 * Stealth Browser Template v2.2
 * Reusable factory for bot-detection-resistant browser automation.
 *
 * Design principle: with `channel: 'chrome'` + headed mode (both mandated here)
 * real Chrome already supplies a genuine User-Agent, WebGL/GPU renderer, canvas
 * fingerprint, PluginArray, and self-consistent permission/hardware values.
 * rebrowser-playwright additionally hides the CDP `Runtime.enable` headless tell.
 * So this template adds ONLY two things on top of that real environment:
 *   1. strips Playwright's main-world artifacts (`window.__pwInitScripts` etc.),
 *      the deterministic signature detectors key on for `isPlaywright`;
 *   2. enables rebrowser's Runtime-fix (env var, set below before import).
 * It touches NOTHING on `navigator` — hand-rolled fakes (PluginArray, canvas
 * noise, hardcoded hardwareConcurrency, a permissions override, a webdriver
 * delete, a languages getter) were removed across v2.1/v2.2 because each created
 * a detectable inconsistency (verified against bot-detector.rebrowser.net,
 * deviceandbrowserinfo.com, browserscan.net — all green after the cleanup).
 *
 * MEASURED 2026-06-10 (macOS, headed Chrome): passes bot.sannysoft.com,
 * bot-detector.rebrowser.net (0 red), deviceandbrowserinfo ("human"),
 * browserscan ("Normal"). Does NOT defeat IP-reputation / behavioral / login
 * walls, and `window.__playwright_builtins__` (a separate, non-configurable
 * Playwright global) cannot be stripped — see SKILL.md "Detection Coverage".
 *
 * Usage:
 *   import { createStealthBrowser, humanDelay, humanType, simulateMouseMovement } from './stealth-template.mjs';
 *   const { browser, context, page } = await createStealthBrowser();
 *
 * Authorized-use only: respect each site's Terms of Service, robots.txt, and
 * applicable law. Intended for QA, accessibility testing, and research.
 */

import { pathToFileURL } from 'node:url';

// rebrowser's Runtime.enable fix must be configured BEFORE the library is
// imported. Default it to 'addBinding' (keeps main-world access while hiding
// the CDP leak) unless the caller already set it. Then import dynamically.
process.env.REBROWSER_PATCHES_RUNTIME_FIX_MODE ??= 'addBinding';
const { chromium } = await import('rebrowser-playwright');

// Init script (runs at document_start in the page) that removes Playwright's
// main-world signature objects. Defined as a string-free function so Playwright
// serializes it for injection. Verified to flip isPlaywright true->false.
function stripPlaywrightArtifacts() {
  const hide = (k) => {
    try { delete window[k]; } catch { /* non-configurable */ }
    if (Object.prototype.hasOwnProperty.call(window, k)) {
      try { Object.defineProperty(window, k, { get: () => undefined, configurable: true }); } catch { /* sealed */ }
    }
  };
  for (const k of Object.getOwnPropertyNames(window)) {
    if (/^__pw|pwInitScripts|playwright/i.test(k)) hide(k);
  }
  // window.chrome presence for the rare headless fallback (no-op in real Chrome).
  if (!window.chrome) window.chrome = {};
}

/**
 * Create a stealth browser instance.
 * @param {Object} options
 * @param {boolean} options.headless - Run headed (default: false, required for stealth)
 * @param {Object} options.viewport - Viewport size (default: { width: 1280, height: 800 })
 * @param {string} options.userAgent - Custom user agent (optional; defaults to real Chrome UA)
 * @param {string} options.locale - Browser locale (default: 'ko-KR'); sets navigator.languages + Accept-Language natively & consistently
 * @param {string} options.storageState - Path to saved session state for cookie persistence (optional)
 * @param {Object} options.proxy - Proxy config { server, username?, password? } (optional)
 * @param {boolean} options.noSandbox - Add --no-sandbox (opt-in: needed for Linux root/CI, but is itself a bot signal — off by default)
 * @returns {Promise<{browser, context, page}>}
 */
export async function createStealthBrowser(options = {}) {
  const {
    headless = false,
    viewport = { width: 1280, height: 800 },
    userAgent = null,
    locale = 'ko-KR',
    storageState = null,
    proxy = null,
    noSandbox = false
  } = options;

  const launchOptions = {
    headless,
    channel: 'chrome',
    args: ['--disable-blink-features=AutomationControlled']
  };
  // --no-sandbox is a security risk AND an automation signal; opt in only when
  // the environment requires it (e.g. running as root in Linux CI).
  if (noSandbox) launchOptions.args.push('--no-sandbox');
  if (proxy) launchOptions.proxy = proxy;

  const browser = await chromium.launch(launchOptions);

  // `locale` sets BOTH navigator.languages and the Accept-Language header
  // natively and consistently (main thread + workers) — which is why we no
  // longer override navigator.languages in JS (that created an own-property /
  // worker-mismatch tell).
  const contextOptions = { viewport, locale };
  if (userAgent) contextOptions.userAgent = userAgent;
  if (storageState) contextOptions.storageState = storageState;

  const context = await browser.newContext(contextOptions);

  // Strip Playwright's main-world artifacts on every navigation. This is the
  // ONLY init script — it touches nothing on navigator.
  await context.addInitScript(stripPlaywrightArtifacts);

  const page = await context.newPage();

  return { browser, context, page };
}

/**
 * Save session state for cookie persistence.
 * @param {BrowserContext} context
 * @param {string} path - File path to save state
 */
export async function saveSession(context, path) {
  await context.storageState({ path });
}

/**
 * Add a human-like random delay between actions.
 * @param {number} min - Minimum delay in ms
 * @param {number} max - Maximum delay in ms
 */
export function humanDelay(min = 100, max = 500) {
  return new Promise(resolve => {
    const delay = Math.random() * (max - min) + min;
    setTimeout(resolve, delay);
  });
}

/**
 * Type text with human-like speed.
 * @param {Page} page - Playwright page
 * @param {string} selector - Element selector
 * @param {string} text - Text to type
 */
export async function humanType(page, selector, text) {
  await page.click(selector);
  for (const char of text) {
    await page.keyboard.type(char);
    await humanDelay(50, 150);
  }
}

/**
 * Simulate natural mouse movement on the page.
 * Helps avoid Cloudflare Turnstile behavioral detection.
 * @param {Page} page
 * @param {number} moves - Number of movements (default: random 5-10)
 */
export async function simulateMouseMovement(page, moves) {
  const count = moves ?? 5 + Math.floor(Math.random() * 5);
  for (let i = 0; i < count; i++) {
    await page.mouse.move(
      100 + Math.random() * 600,
      100 + Math.random() * 400,
      { steps: 10 }
    );
    await humanDelay(50, 200);
  }
}

// CLI: run this file directly to open a stealth browser at bot.sannysoft.com.
// pathToFileURL handles spaces / non-ASCII / Windows paths correctly.
if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  console.log('Testing stealth browser...');
  const { browser, page } = await createStealthBrowser();

  process.on('SIGINT', async () => {
    await browser.close();
    process.exit(0);
  });

  await page.goto('https://bot.sannysoft.com');
  console.log('Browser opened. Check results in the browser window.');
  console.log('Press Ctrl+C to close.');
}
