#!/usr/bin/env node
/**
 * smoke_views.js — Multi-view regression smoke test
 *
 * Usage:
 *   NODE_PATH=<managed-node_modules> <managed-node.exe> smoke_views.js
 *
 * Iterates every view, triggers its loader, captures DOM metrics,
 * scans for forbidden strings, and screenshots each view.
 * Outputs JSON summary and saves PNGs to shots/.
 *
 * Customize: set BASE_URL, VIEWS[], FORBIDDEN[], and SPECIFIC_ASSERTS.
 */

const { chromium } = require('playwright');
const fs = require('fs');

// ---- CONFIG (edit per project) ----
const BASE_URL = process.env.BASE_URL || 'http://localhost:3000';
const SHOT_DIR = process.env.SHOT_DIR || './shots';
const WAIT_MS = 1600; // ms to wait after switching view for DOM to settle

// List all view IDs that switchView(name) accepts — replace with your app's views
const VIEWS = ['dashboard', 'profile', 'settings', 'reports', 'admin'];

// Known bug-signature strings that must NOT appear anywhere
const FORBIDDEN = ['NaN%', 'undefined%', '+NaN', '-NaN'];

// Specific metric assertions — format: { view, metricLabel, expectedValue }
// The script finds the metric-card whose label includes metricLabel,
// reads its .metric-value text, and asserts equality.
const SPECIFIC_ASSERTS = [];
// Example:
// { view: 'dashboard', label: '最大回撤', value: '-12.50%' },
// { view: 'dashboard', label: '胜率', value: '7.10%' },

// ------------------------------------

(async () => {
  fs.mkdirSync(SHOT_DIR, { recursive: true });

  const browser = await chromium.launch();
  const page = await browser.newPage({ setDefaultTimeout: 15000 });

  const consoleErrors = [];
  const pageErrors = [];
  page.on('console', m => { if (m.type() === 'error') consoleErrors.push(m.text()); });
  page.on('pageerror', e => pageErrors.push('PAGEERROR: ' + e.message));

  await page.goto(BASE_URL, { waitUntil: 'networkidle' });
  await page.waitForTimeout(2500);

  const results = [];
  for (const v of VIEWS) {
    await page.evaluate((vid) => {
      if (typeof switchView === 'function') switchView(vid);
    }, v);
    await page.waitForTimeout(WAIT_MS);

    const info = await page.evaluate((vid) => {
      const view = document.getElementById('view-' + vid);
      const metricVals = Array.from(view ? view.querySelectorAll('.metric-value') : [])
        .map(e => (e.textContent || '').trim()).filter(Boolean).slice(0, 8);
      const cards = Array.from(view ? view.querySelectorAll('.metric-card') : []).slice(0, 8)
        .map(c => {
          const label = (c.querySelector('.metric-label') || {}).textContent || '';
          const val = (c.querySelector('.metric-value') || {}).textContent || '';
          return (label + ':' + val).trim();
        });
      return { visible: view ? (view.classList.contains('active') || getComputedStyle(view).display !== 'none') : false, metricCount: metricVals.length, metrics: metricVals, cards };
    }, v);

    const fullText = await page.evaluate((vid) => {
      const view = document.getElementById('view-' + vid);
      return view ? view.innerText.replace(/\s+/g, ' ') : '';
    }, v);

    const hits = FORBIDDEN.filter(f => fullText.includes(f));
    await page.screenshot({ path: `${SHOT_DIR}/smoke_${v}.png` });
    results.push({ view: v, ...info, forbiddenHits: hits });
  }

  // Specific assertions
  const assertResults = [];
  for (const a of SPECIFIC_ASSERTS) {
    await page.evaluate((vid) => { if (typeof switchView === 'function') switchView(vid); }, a.view);
    await page.waitForTimeout(WAIT_MS);
    const actual = await page.evaluate((label) => {
      const cards = Array.from(document.querySelectorAll('.metric-card'));
      const found = cards.find(c => (c.querySelector('.metric-label')||{}).textContent && c.querySelector('.metric-label').textContent.includes(label));
      return found ? (found.querySelector('.metric-value').textContent||'').trim() : 'CARD_NOT_FOUND';
    }, a.label);
    assertResults.push({ view: a.view, label: a.label, expected: a.value, actual, pass: actual === a.value });
  }

  await browser.close();

  const forbiddenGlobal = results.filter(r => r.forbiddenHits.length).map(r => ({ view: r.view, hits: r.forbiddenHits }));
  const summary = {
    ts: new Date().toISOString(),
    base: BASE_URL,
    viewsTested: VIEWS.length,
    consoleErrors, pageErrors,
    forbiddenGlobal,
    asserts: assertResults,
    pass: consoleErrors.length === 0 && pageErrors.length === 0 && forbiddenGlobal.length === 0 && assertResults.every(a => a.pass),
    perView: results.map(r => ({ view: r.view, visible: r.visible, metricCount: r.metricCount, forbiddenHits: r.forbiddenHits, sample: r.metrics.slice(0, 4) }))
  };

  console.log(JSON.stringify(summary, null, 2));
  fs.writeFileSync('smoke_result.json', JSON.stringify(summary, null, 2));
})().catch(e => { console.error('FATAL', e); process.exit(1); });
