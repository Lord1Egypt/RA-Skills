#!/usr/bin/env node
// shoot.mjs: screenshot every slide (or the page), write a contact sheet, report console errors.
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';
import {
  parseArgs, say, die, rel, baseName, requireHtmlFile, requirePlaywright, launchChromium,
  openPage, watchPage, waitReady, isDeckPage, slideCount, fileUrl, isMain, fmtBytes,
} from './_lib.mjs';

const spec = {
  name: 'sketchy shoot', file: 'shoot.mjs', usage: '<file.html> [--out dir] [--sizes 1920x1080,390x844] [--slides]',
  summary: 'screenshot every slide (or the whole page), write contact-sheet.png, report console errors.',
  details: [
    'Decks (main.sk-deck): every slide via ?slide=N&static at the first size, plus the other sizes for slide 1.',
    'Pages: one full-page shot per size. Reduced motion is on, so the engine draws everything at once.',
    'Look at contact-sheet.png first, then open single slides that look wrong.',
    'Exit 1 when the page logs a console error, throws, or a request fails.',
  ],
  options: [
    { name: 'out', type: 'string', arg: 'dir', help: 'output folder (default: shots/<name>/ next to the file)' },
    { name: 'sizes', type: 'string', arg: 'WxH,WxH', default: '1920x1080,390x844', help: 'viewport sizes; the first is the main one (default 1920x1080,390x844)' },
    { name: 'slides', type: 'boolean', help: 'decks: shoot every slide at every size, not just slide 1 at the extra sizes' },
  ],
  positionals: { min: 1, max: 1, name: '<file.html>' },
  examples: ['node shoot.mjs out/deck.html', 'node shoot.mjs deck.html --out review --sizes 1920x1080', 'node shoot.mjs page.html --sizes 1280x800,390x844'],
};

const { values, positionals } = parseArgs(process.argv.slice(2), spec);

function parseSizes(s) {
  const sizes = String(s).split(',').map((x) => x.trim()).filter(Boolean).map((x) => {
    const m = /^(\d{2,5})x(\d{2,5})$/i.exec(x);
    if (!m) die(`bad size "${x}"`, 'use WxH, for example --sizes 1920x1080,390x844');
    return { w: +m[1], h: +m[2], key: `${m[1]}x${m[2]}` };
  });
  if (!sizes.length) die('no sizes given', 'use --sizes 1920x1080,390x844');
  return sizes;
}

const pad = (n) => String(n).padStart(2, '0');

async function main() {
  const file = requireHtmlFile(positionals[0], 'html file');
  const sizes = parseSizes(values.sizes);
  const outDir = path.resolve(values.out || path.join(path.dirname(file), 'shots', baseName(file)));
  fs.mkdirSync(outDir, { recursive: true });
  for (const f of fs.readdirSync(outDir)) if (/^(slide-\d+.*|page-.*|contact-sheet.*)\.png$/.test(f)) fs.unlinkSync(path.join(outDir, f)); // stale shots from a longer deck

  const pw = requirePlaywright();
  const browser = await launchChromium(pw);
  const state = { errors: new Map(), failed: new Map(), external: new Map() };
  const shots = []; // { file, label, kind: 'main'|'small'|'page', w, h }
  let isDeck = false, count = 0;

  try {
    // probe: deck or page, and how many slides
    {
      const { context, page } = await openPage(browser, { width: sizes[0].w, height: sizes[0].h });
      watchPage(page, state);
      await page.goto(fileUrl(file, 'static'), { waitUntil: 'load' });
      if (!(await waitReady(page))) say.warn('page was not ready after 15 s; shooting anyway');
      isDeck = await isDeckPage(page);
      count = isDeck ? await slideCount(page) : 0;
      await context.close();
    }

    if (isDeck && count === 0) die('deck has no slides', 'add <section class="sk-slide"> elements inside main.sk-deck', 1);

    for (let si = 0; si < sizes.length; si++) {
      const size = sizes[si];
      const mobile = size.w <= 600;
      const { context, page } = await openPage(browser, { width: size.w, height: size.h, mobile });
      watchPage(page, state);
      if (isDeck) {
        const last = si === 0 || values.slides ? count : 1;
        for (let n = 1; n <= last; n++) {
          await page.goto(fileUrl(file, `slide=${n}&static`), { waitUntil: 'load' });
          if (!(await waitReady(page))) say.warn(`slide ${n} was not ready after 15 s`);
          const name = si === 0 ? `slide-${pad(n)}.png` : `slide-${pad(n)}-${size.key}.png`;
          await page.screenshot({ path: path.join(outDir, name) });
          shots.push({ file: name, label: si === 0 ? `slide ${n}` : `slide ${n} @ ${size.key}`, kind: si === 0 ? 'main' : 'small', w: size.w, h: size.h });
        }
      } else {
        await page.goto(fileUrl(file, 'static'), { waitUntil: 'load' });
        if (!(await waitReady(page))) say.warn(`page was not ready after 15 s at ${size.key}`);
        const name = `page-${size.key}.png`;
        await page.screenshot({ path: path.join(outDir, name), fullPage: true });
        shots.push({ file: name, label: `page @ ${size.key}`, kind: 'page', w: size.w, h: size.h });
      }
      await context.close();
    }

    const sheets = await contactSheets(browser, outDir, shots);
    const totalBytes = shots.reduce((s, x) => s + fs.statSync(path.join(outDir, x.file)).size, 0);
    say.ok(isDeck
      ? `${count} slide${count === 1 ? '' : 's'} at ${sizes[0].key}${sizes.length > 1 ? ` + ${sizes.slice(1).map((s) => s.key).join(', ')}${values.slides ? ' (all slides)' : ' (slide 1)'}` : ''}, ${shots.length} shots, ${fmtBytes(totalBytes)}`
      : `page shot at ${sizes.map((s) => s.key).join(', ')}`);
    say.ok(`folder  ${rel(outDir)}`);
    for (const s of sheets) say.ok(`sheet   ${rel(path.join(outDir, s))}`);
  } finally {
    await browser.close();
  }

  // report
  let bad = 0;
  for (const [msg] of state.errors) { say.error(`console: ${msg}`); bad++; }
  for (const [msg] of state.failed) { say.error(`request failed: ${msg}`); bad++; }
  if (state.failed.size) say.fix('check the path, or run build.mjs so everything is inlined');
  for (const [url] of state.external) say.warn(`external request: ${url}`);
  if (state.external.size) say.fix('run build.mjs and use local files only; the final file must work offline');
  if (bad) { say.line(`${bad} problem${bad === 1 ? '' : 's'} on the page`); process.exit(1); }
  say.ok('no console errors, no failed requests');
}

/** Compose contact sheets from the shots with an HTML grid rendered by Playwright. */
async function contactSheets(browser, outDir, shots) {
  const PER_SHEET = 20;
  const main = shots.filter((s) => s.kind !== 'small');
  const small = shots.filter((s) => s.kind === 'small');
  const names = [];
  const groups = [];
  const rest = [...main];
  while (rest.length) groups.push({ main: rest.splice(0, PER_SHEET), small: [] });
  if (!groups.length) groups.push({ main: [], small: [] });
  groups[groups.length - 1].small = small;

  const tmp = path.join(outDir, '.contact-sheet.tmp.html');
  for (let gi = 0; gi < groups.length; gi++) {
    const g = groups[gi];
    const cols = g.main.length <= 4 ? Math.max(g.main.length, 1) : g.main.length <= 9 ? 3 : 4;
    const cell = (s, cls) => `<figure class="${cls}"><img src="${pathToFileURL(path.join(outDir, s.file)).href}" alt=""><figcaption>${s.label}</figcaption></figure>`;
    const html = `<!doctype html><html><head><meta charset="utf-8"><style>
      body{margin:0;padding:24px;width:1752px;background:#ececea;font:14px/1.2 system-ui,Segoe UI,sans-serif;color:#333}
      h1{font:600 15px system-ui;margin:0 0 14px;color:#555}
      .grid{display:grid;grid-template-columns:repeat(${cols},1fr);gap:18px}
      .row{display:flex;flex-wrap:wrap;gap:18px;margin-top:22px;align-items:flex-start}
      figure{margin:0}
      figure img{display:block;width:100%;height:auto;background:#fff;box-shadow:0 1px 4px rgba(0,0,0,.25);outline:1px solid rgba(0,0,0,.12)}
      figcaption{margin-top:6px;color:#555}
      .p img{max-height:520px;width:auto;max-width:100%;object-fit:contain;object-position:top}
      .m img{height:340px;width:auto}
    </style></head><body>
      <h1>${path.basename(outDir)}${groups.length > 1 ? ` (sheet ${gi + 1} of ${groups.length})` : ''}</h1>
      <div class="grid">${g.main.map((s) => cell(s, s.kind === 'page' ? 'p' : 's')).join('')}</div>
      ${g.small.length ? `<div class="row">${g.small.map((s) => cell(s, 'm')).join('')}</div>` : ''}
    </body></html>`;
    fs.writeFileSync(tmp, html);
    const { context, page } = await openPage(browser, { width: 1800, height: 900 });
    try {
      await page.goto(pathToFileURL(tmp).href, { waitUntil: 'load' });
      await page.evaluate(() => Promise.all([...document.images].map((i) => i.decode().catch(() => {}))));
      const name = gi === 0 ? 'contact-sheet.png' : `contact-sheet-${gi + 1}.png`;
      await page.screenshot({ path: path.join(outDir, name), fullPage: true });
      names.push(name);
    } finally { await context.close(); }
  }
  try { fs.unlinkSync(tmp); } catch { /* leave it; harmless */ }
  return names;
}

if (isMain(import.meta.url)) main().catch((e) => die(`shoot failed: ${String(e && e.message ? e.message : e).split('\n')[0]}`, 'node doctor.mjs', 1));
