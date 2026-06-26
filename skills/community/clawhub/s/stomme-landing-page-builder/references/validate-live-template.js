#!/usr/bin/env node
/**
 * validate-live.js — Automated post-deploy validation for stomme.ai
 * Uses Playwright to test in real browser contexts.
 *
 * Usage: node scripts/validate-live.js [url]
 * Default: https://stomme.ai
 * Exit 0 = pass, Exit 1 = failures
 */

const { chromium } = require('playwright');

const SITE = process.argv[2] || 'https://stomme.ai';
const PAGES = ['/', '/pricing.html'];
const VIEWPORTS = [
  { name: 'desktop', width: 1440, height: 900 },
  { name: 'mobile-safari', width: 375, height: 812, isMobile: true, hasTouch: true },
];

let pass = 0, fail = 0;

function ok(test, detail = '') {
  pass++;
  console.log(`  ✅ ${test}${detail ? ` — ${detail}` : ''}`);
}

function bad(test, detail = '') {
  fail++;
  console.error(`  ❌ ${test}${detail ? ` — ${detail}` : ''}`);
}

function luminance(r, g, b) {
  const [rs, gs, bs] = [r, g, b].map(c => {
    c = c / 255;
    return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
}

function contrastRatio(rgb1, rgb2) {
  const l1 = luminance(...rgb1);
  const l2 = luminance(...rgb2);
  return (Math.max(l1, l2) + 0.05) / (Math.min(l1, l2) + 0.05);
}

function parseRgb(str) {
  if (!str) return null;
  const m = str.match(/rgba?\((\d+),\s*(\d+),\s*(\d+)/);
  return m ? [parseInt(m[1]), parseInt(m[2]), parseInt(m[3])] : null;
}

async function run() {
  const browser = await chromium.launch({ headless: true });

  for (const vp of VIEWPORTS) {
    console.log(`\n── ${vp.name} (${vp.width}x${vp.height}) ──`);
    const context = await browser.newContext({
      viewport: { width: vp.width, height: vp.height },
      isMobile: vp.isMobile || false,
      hasTouch: vp.hasTouch || false,
    });

    for (const path of PAGES) {
      const url = SITE + path;
      console.log(`\n  Page: ${url}`);
      const page = await context.newPage();

      // Clear storage for clean state
      await page.goto(url, { waitUntil: 'networkidle' });
      await page.evaluate(() => localStorage.clear());
      await page.reload({ waitUntil: 'networkidle' });

      // ── 1. CSS custom properties resolve ──────────────────────────
      const vars = await page.evaluate(() => {
        const root = getComputedStyle(document.documentElement);
        return ['--color-accent', '--color-text', '--color-bg', '--color-white',
          '--color-text-secondary', '--color-border', '--font-heading', '--font-body'
        ].map(v => ({ name: v, val: root.getPropertyValue(v).trim() }));
      });
      for (const { name, val } of vars) {
        if (val && val !== '') ok(`CSS var ${name}`, val.substring(0, 30));
        else bad(`CSS var ${name}`, 'EMPTY or undefined');
      }

      // ── 2. Interactive element contrast ───────────────────────────
      const elements = await page.evaluate(() => {
        const sels = [
          { sel: '.nav-cta', label: 'Nav CTA button' },
          { sel: '.nav-links a', label: 'Nav link' },
          { sel: '.btn-primary', label: 'Primary button (body)' },
        ];
        return sels.map(({ sel, label }) => {
          const el = document.querySelector(sel);
          if (!el) return { label, error: 'not found' };
          const s = getComputedStyle(el);
          return { label, color: s.color, bg: s.backgroundColor, fontSize: parseFloat(s.fontSize) };
        });
      });
      for (const el of elements) {
        if (el.error) { bad(`${el.label} contrast`, el.error); continue; }
        const fg = parseRgb(el.color);
        const bg = parseRgb(el.bg);
        if (!fg || !bg) { bad(`${el.label} contrast`, `unparseable: ${el.color} / ${el.bg}`); continue; }
        const ratio = contrastRatio(fg, bg);
        const threshold = el.fontSize >= 18.66 ? 3.0 : 4.5;
        if (ratio >= threshold) ok(`${el.label} contrast`, `${ratio.toFixed(2)}:1 (need ${threshold}:1)`);
        else bad(`${el.label} contrast`, `${ratio.toFixed(2)}:1 — FAILS WCAG AA (need ${threshold}:1)`);
      }

      // ── 3. Theme toggle — 3 full cycles ───────────────────────────
      if (path === '/') {
        const toggleResults = await page.evaluate(async () => {
          const toggle = document.querySelector('.theme-toggle');
          if (!toggle) return { error: 'no toggle' };
          const results = [];
          for (let i = 0; i < 6; i++) {
            toggle.click();
            await new Promise(r => setTimeout(r, 150));
            results.push({
              click: i + 1,
              theme: document.documentElement.getAttribute('data-theme'),
              bg: getComputedStyle(document.body).backgroundColor,
              stored: localStorage.getItem('stomme-theme'),
            });
          }
          return { results };
        });

        if (toggleResults.error) {
          bad('Theme toggle', toggleResults.error);
        } else {
          const cycles = toggleResults.results;
          let toggleOk = true;

          // Verify alternating themes
          for (let i = 1; i < cycles.length; i++) {
            if (cycles[i].theme === cycles[i - 1].theme) {
              bad('Theme toggle cycle', `Click ${i + 1} did not change theme (stuck on ${cycles[i].theme})`);
              toggleOk = false;
              break;
            }
          }
          // Verify localStorage matches attribute
          for (const c of cycles) {
            if (c.theme !== c.stored) {
              bad('Theme toggle storage', `data-theme=${c.theme} but localStorage=${c.stored}`);
              toggleOk = false;
              break;
            }
          }
          if (toggleOk) ok('Theme toggle — 3 full cycles', 'alternates correctly, localStorage synced');
        }
      }

      // ── 4. Language switcher — all 3 locales ──────────────────────
      if (path === '/') {
        const langResults = await page.evaluate(async () => {
          const results = [];
          for (const lang of ['sv', 'de', 'en']) {
            const btn = document.querySelector(`.lang-btn[data-lang="${lang}"]`);
            if (!btn) { results.push({ lang, error: 'button missing' }); continue; }
            btn.click();
            await new Promise(r => setTimeout(r, 300));
            const hero = document.querySelector('[data-copy="heroTitle"]');
            results.push({
              lang,
              heroText: hero?.textContent?.substring(0, 50) || 'EMPTY',
              stored: localStorage.getItem('stomme-lang'),
              htmlLang: document.documentElement.lang,
            });
          }
          return results;
        });

        for (const r of langResults) {
          if (r.error) { bad(`Lang ${r.lang}`, r.error); continue; }
          if (r.heroText === 'EMPTY') bad(`Lang ${r.lang} hero text`, 'empty after switch');
          else if (r.stored === r.lang) ok(`Lang ${r.lang}`, `"${r.heroText}"`);
          else bad(`Lang ${r.lang} storage`, `expected ${r.lang}, got ${r.stored}`);
        }
      }

      // ── 5. Cache-bust version params on assets ────────────────────
      const assets = await page.evaluate(() => {
        return [...document.querySelectorAll('script[src], link[rel="stylesheet"][href]')].map(el => ({
          tag: el.tagName,
          src: el.src || el.href,
          hasVersion: /\?v=/.test(el.src || el.href),
        }));
      });
      const unversioned = assets.filter(a => !a.hasVersion && !a.src.includes('cdn'));
      if (unversioned.length === 0) ok('Cache-bust hashes', `all ${assets.length} assets versioned`);
      else bad('Cache-bust hashes', `${unversioned.length} unversioned: ${unversioned.map(a => a.src.split('/').pop()).join(', ')}`);

      // ── 6. No broken internal links ───────────────────────────────
      const brokenLinks = await page.evaluate(() => {
        return [...document.querySelectorAll('a[href]')]
          .filter(a => {
            const h = a.getAttribute('href');
            return !h || h === '#' || h === 'undefined' || h === 'null';
          })
          .map(a => ({ text: a.textContent.trim().substring(0, 30), href: a.getAttribute('href') }));
      });
      if (brokenLinks.length === 0) ok('Internal links', 'no broken hrefs');
      else bad('Internal links', `${brokenLinks.length} broken: ${brokenLinks.map(l => l.text).join(', ')}`);

      // ── 7. Meta tags ──────────────────────────────────────────────
      const meta = await page.evaluate(() => ({
        title: document.title,
        desc: document.querySelector('meta[name="description"]')?.content,
        ogTitle: document.querySelector('meta[property="og:title"]')?.content,
      }));
      if (meta.title) ok('Page title', meta.title.substring(0, 40));
      else bad('Page title', 'missing');
      if (meta.desc) ok('Meta description', 'present');
      else bad('Meta description', 'missing');

      await page.close();
    }
    await context.close();
  }

  await browser.close();

  // ── Summary ─────────────────────────────────────────────────────────────
  console.log('\n════════════════════════════════════════');
  console.log(`  PASS: ${pass}  FAIL: ${fail}`);
  console.log('════════════════════════════════════════');

  if (fail > 0) {
    console.error('\n⛔ Validation FAILED — deploy should be investigated');
    process.exit(1);
  } else {
    console.log('\n✅ All checks passed');
    process.exit(0);
  }
}

run().catch(err => {
  console.error('Validation script crashed:', err);
  process.exit(1);
});
