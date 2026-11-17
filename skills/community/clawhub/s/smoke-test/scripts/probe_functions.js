#!/usr/bin/env node
/**
 * probe_functions.js — Global function availability probe
 *
 * Usage:
 *   NODE_PATH=<managed-node_modules> <managed-node.exe> probe_functions.js
 *
 * Scans index.html for all inline onclick="fnName(...)" references,
 * then verifies typeof window[fnName] === 'function' in the live browser.
 *
 * Output: JSON { total, ok, missing[], okList[] }
 *
 * Customize: set BASE_URL and EXCLUDE (known non-function onclick targets).
 */

const { chromium } = require('playwright');

// ---- CONFIG (edit per project) ----
const BASE_URL = process.env.BASE_URL || 'http://localhost:3000';
const EXCLUDE = ['showToast', 'closeModal', 'handleKey']; // non-function onclick targets
// ------------------------------------

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ setDefaultTimeout: 15000 });

  const consoleErrors = [];
  page.on('console', m => { if (m.type() === 'error') consoleErrors.push(m.text()); });

  await page.goto(BASE_URL, { waitUntil: 'networkidle' });
  await page.waitForTimeout(2000);

  // Extract all onclick references from index.html
  const fns = await page.evaluate(() => {
    const set = new Set();
    document.querySelectorAll('[onclick]').forEach(el => {
      const raw = el.getAttribute('onclick') || '';
      const matches = raw.match(/(\w+)\s*\(/g);
      if (matches) matches.forEach(m => set.add(m.replace('(', '')));
    });
    return Array.from(set);
  });

  // Probe each function in the browser
  const result = await page.evaluate(({ fns, exclude }) => {
    const missing = [];
    const ok = [];
    for (const fn of fns) {
      if (exclude.includes(fn)) continue;
      if (typeof window[fn] === 'function') ok.push(fn);
      else missing.push(fn);
    }
    return { total: fns.length, ok: ok.length, missing, okList: ok };
  }, { fns, exclude: EXCLUDE });

  await browser.close();

  result.consoleErrors = consoleErrors;
  result.pass = result.missing.length === 0 && consoleErrors.length === 0;

  console.log(JSON.stringify(result, null, 2));
})().catch(e => { console.error('FATAL', e); process.exit(1); });
