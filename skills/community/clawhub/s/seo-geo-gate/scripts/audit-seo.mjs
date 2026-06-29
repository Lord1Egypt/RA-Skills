#!/usr/bin/env node
// audit-seo.mjs — portable, zero-dependency on-disk SEO/quality auditor.
//
// Runs the reference site build-time "hard gate" checks against ANY built static
// site (a directory of .html files + their local CSS/JS/images). Framework
// agnostic: point it at Astro `dist/`, Next `out/`, Hugo `public/`, a Jekyll
// `_site/`, or a plain folder of HTML.
//
//   node audit-seo.mjs [--dir dist] [--strict] [--max-page-kb 500]
//                      [--max-img-kb 500] [--json]
//
// Severity model:
//   ERROR — genuinely hurts ranking / breaks crawlers / fails Core Web Vitals.
//           Exits 1 (CI gate).
//   WARN  — best-practice miss; review. With --strict, warns become errors.
//
// No npm install. Pure Node >=18 (uses fs, path, no external HTML parser —
// regex extraction is intentionally conservative and good enough for audit
// signals; it does not execute or fully parse the DOM).

import { readFileSync, statSync, readdirSync } from 'node:fs';
import { join, extname, relative, resolve } from 'node:path';

// ---- args -----------------------------------------------------------------
const args = process.argv.slice(2);
const opt = (name, def) => {
  const i = args.indexOf(`--${name}`);
  return i >= 0 && args[i + 1] && !args[i + 1].startsWith('--') ? args[i + 1] : def;
};
const flag = (name) => args.includes(`--${name}`);

const DIR = resolve(opt('dir', 'dist'));
const STRICT = flag('strict');
const JSON_OUT = flag('json');
const MAX_PAGE = Number(opt('max-page-kb', '500')) * 1024;
const MAX_IMG = Number(opt('max-img-kb', '500')) * 1024;

const IMG_EXT = new Set(['.webp', '.avif', '.jpg', '.jpeg', '.png', '.gif', '.svg']);
const SCRIPT_TYPE_ALLOW = new Set(['application/ld+json', 'application/json', 'importmap']);

// ---- findings -------------------------------------------------------------
const findings = []; // {file, sev:'error'|'warn', rule, msg}
const add = (file, sev, rule, msg) => findings.push({ file, sev, rule, msg });

// ---- fs walk --------------------------------------------------------------
function* walk(dir) {
  let entries;
  try { entries = readdirSync(dir, { withFileTypes: true }); }
  catch { return; }
  for (const e of entries) {
    const p = join(dir, e.name);
    if (e.isDirectory()) yield* walk(p);
    else yield p;
  }
}

// ---- tiny HTML helpers (regex; conservative) ------------------------------
const tagOpenRe = (tag) => new RegExp(`<${tag}\\b[^>]*>`, 'gi');
const countTag = (html, tag) => (html.match(tagOpenRe(tag)) || []).length;
const hasTag = (html, tag) => tagOpenRe(tag).test(html);

function attr(tagStr, name) {
  const m = tagStr.match(new RegExp(`\\b${name}\\s*=\\s*("([^"]*)"|'([^']*)'|([^\\s>]+))`, 'i'));
  if (!m) return null;
  return m[2] ?? m[3] ?? m[4] ?? '';
}
const hasAttr = (tagStr, name) =>
  new RegExp(`\\b${name}(\\s*=|[\\s>])`, 'i').test(tagStr);

function allTags(html, tag) {
  return html.match(tagOpenRe(tag)) || [];
}

// strip <head>..</head>? no — we scan whole doc; fine for these checks.

// ---- per-page checks ------------------------------------------------------
function auditHtml(file, html) {
  const rel = relative(DIR, file);
  // Error pages (404/50x) are intentionally noindex: they don't need a
  // canonical, description, OG tags, or structured data. Skip those checks
  // for them but still enforce h1/viewport/semantic/perf hygiene.
  const isErrorPage = /(^|\/)(404|50\d)\.html$/i.test(rel);

  // 1) exactly one <h1>
  const h1 = countTag(html, 'h1');
  if (h1 !== 1) add(rel, 'error', 'h1', `expected exactly 1 <h1>, got ${h1}`);

  // 2) viewport meta
  const metas = allTags(html, 'meta');
  const vp = metas.find((m) => /name\s*=\s*["']?viewport/i.test(m));
  if (!vp) add(rel, 'error', 'viewport', 'missing <meta name="viewport">');
  else {
    const c = attr(vp, 'content') || '';
    if (!/width=device-width/i.test(c) || !/initial-scale=1/i.test(c))
      add(rel, 'error', 'viewport', `viewport content invalid: "${c}"`);
  }

  // 3) semantic landmarks
  for (const t of ['main', 'nav', 'footer'])
    if (!hasTag(html, t)) add(rel, 'error', 'semantic', `missing <${t}>`);

  // 4) <title>
  const titleM = html.match(/<title[^>]*>([\s\S]*?)<\/title>/i);
  const title = titleM ? titleM[1].replace(/\s+/g, ' ').trim() : '';
  if (!title) add(rel, 'error', 'title', 'missing or empty <title>');
  else if (title.length < 10 || title.length > 60)
    add(rel, 'warn', 'title', `title length ${title.length} (aim 10–60 chars)`);

  // 5) meta description
  const desc = metas.find((m) => /name\s*=\s*["']?description/i.test(m));
  if (!desc) { if (!isErrorPage) add(rel, 'error', 'description', 'missing <meta name="description">'); }
  else {
    const c = (attr(desc, 'content') || '').trim();
    if (c.length < 50 || c.length > 160)
      add(rel, 'warn', 'description', `description length ${c.length} (aim 50–160 chars)`);
  }

  // 6) canonical
  const links = allTags(html, 'link');
  const canon = links.find((l) => /rel\s*=\s*["']?canonical/i.test(l));
  if (!canon) { if (!isErrorPage) add(rel, 'error', 'canonical', 'missing <link rel="canonical">'); }
  else {
    const href = attr(canon, 'href') || '';
    if (!/^https?:\/\//i.test(href))
      add(rel, 'error', 'canonical', `canonical href must be absolute: "${href}"`);
  }

  // 7) Open Graph minimum
  if (!isErrorPage) {
    const ogTitle = metas.some((m) => /property\s*=\s*["']?og:title/i.test(m));
    const ogImage = metas.some((m) => /property\s*=\s*["']?og:image/i.test(m));
    if (!ogTitle) add(rel, 'warn', 'opengraph', 'missing og:title');
    if (!ogImage) add(rel, 'warn', 'opengraph', 'missing og:image');
  }

  // 8) images: width/height/alt + loading strategy
  for (const img of allTags(html, 'img')) {
    const src = attr(img, 'src') || '(no src)';
    if (!hasAttr(img, 'width') || !hasAttr(img, 'height'))
      add(rel, 'error', 'img-dims', `<img> missing width/height — CLS risk (${src})`);
    if (attr(img, 'alt') === null)
      add(rel, 'error', 'img-alt', `<img> missing alt (${src})`);
    const loading = (attr(img, 'loading') || '').toLowerCase();
    const fetchpri = (attr(img, 'fetchpriority') || '').toLowerCase();
    const isHero = loading === 'eager' || fetchpri === 'high';
    if (isHero) {
      if (fetchpri !== 'high')
        add(rel, 'warn', 'img-hero', `hero/eager <img> should set fetchpriority="high" (${src})`);
    } else if (loading !== 'lazy') {
      add(rel, 'warn', 'img-lazy', `non-hero <img> should be loading="lazy" (${src})`);
    }
  }

  // 9) inline executable scripts + inline event handlers (CSP / perf)
  const scriptRe = /<script\b([^>]*)>([\s\S]*?)<\/script>/gi;
  let sm;
  while ((sm = scriptRe.exec(html))) {
    const attrs = sm[1], body = sm[2];
    if (hasAttr(attrs, 'src')) continue;        // external — ok
    if (!body.trim()) continue;                  // empty — ok
    const type = (attr(attrs, 'type') || '').toLowerCase();
    if (SCRIPT_TYPE_ALLOW.has(type)) continue;   // data block (JSON-LD etc.) — ok
    add(rel, 'warn', 'inline-script', `inline executable <script type="${type || '(default)'}"> (blocks strict CSP)`);
  }
  // inline on*= handlers
  for (const m of html.matchAll(/<([a-zA-Z][\w-]*)\b([^>]*)>/g)) {
    if (/\son[a-z]+\s*=/i.test(m[2]))
      add(rel, 'warn', 'inline-handler', `<${m[1]}> has inline event handler (blocks strict CSP)`);
  }

  // 10) structured data presence
  if (!isErrorPage && !/<script[^>]*type\s*=\s*["']application\/ld\+json/i.test(html))
    add(rel, 'warn', 'jsonld', 'no JSON-LD structured data on page');

  // 11) external resource references (informational for general SEO)
  const extRefs = new Set();
  const grab = (tag, a) => {
    for (const t of allTags(html, tag)) {
      const v = attr(t, a);
      if (v && /^https?:\/\//i.test(v)) extRefs.add(v.split('?')[0]);
    }
  };
  grab('script', 'src'); grab('img', 'src'); grab('source', 'src');
  for (const l of links) {
    const r = (attr(l, 'rel') || '').toLowerCase();
    if (/(stylesheet|preload|prefetch)/.test(r)) {
      const v = attr(l, 'href');
      if (v && /^https?:\/\//i.test(v)) extRefs.add(v.split('?')[0]);
    }
  }
  if (extRefs.size)
    add(rel, 'warn', 'external-res', `${extRefs.size} external resource ref(s) (self-host for CSP + speed): ${[...extRefs].slice(0, 3).join(', ')}${extRefs.size > 3 ? ' …' : ''}`);

  // 12) page weight: HTML + local CSS + local JS
  let total = Buffer.byteLength(html, 'utf8');
  const addLocal = (url) => {
    if (!url || !url.startsWith('/')) return;
    try { total += statSync(join(DIR, url.split('?')[0])).size; } catch {}
  };
  for (const l of links)
    if (/rel\s*=\s*["']?stylesheet/i.test(l)) addLocal(attr(l, 'href'));
  for (const s of allTags(html, 'script')) addLocal(attr(s, 'src'));
  if (total > MAX_PAGE)
    add(rel, 'error', 'page-weight', `HTML+CSS+JS = ${(total / 1024).toFixed(0)} KB > ${(MAX_PAGE / 1024).toFixed(0)} KB budget`);
}

// ---- standalone CSS baseline (font-size floor) ----------------------------
function auditCss(file, css) {
  const rel = relative(DIR, file);
  for (const m of css.matchAll(/font-size\s*:\s*([^;}]+)/gi)) {
    const raw = m[1].replace(/!important/i, '').trim();
    if (/^(var\(|calc\(|inherit|initial|unset|0\b)/.test(raw)) continue;
    const um = raw.match(/^([\d.]+)(px|pt|rem|em)?$/);
    if (!um) continue;
    const n = parseFloat(um[1]); const unit = um[2] || 'px';
    const px = unit === 'px' ? n : unit === 'pt' ? n * 1.3333 : n * 16; // rem/em ≈16px base
    if (px < 10) add(rel, 'warn', 'baseline-font', `font-size ${raw} (≈${px.toFixed(0)}px) < 10px floor`);
  }
}

// ---- image file sizes -----------------------------------------------------
function auditImageFile(file) {
  const rel = relative(DIR, file);
  const bytes = statSync(file).size;
  if (bytes > MAX_IMG)
    add(rel, 'warn', 'img-size', `${(bytes / 1024).toFixed(0)} KB > ${(MAX_IMG / 1024).toFixed(0)} KB — recompress / use WebP/AVIF`);
}

// ---- run ------------------------------------------------------------------
let nHtml = 0, nCss = 0, nImg = 0;
let dirOk = true;
try { statSync(DIR); } catch { dirOk = false; }
if (!dirOk) {
  console.error(`✗ directory not found: ${DIR}\n  pass --dir <build output> (e.g. dist, out, public, _site)`);
  process.exit(2);
}

for (const file of walk(DIR)) {
  const ext = extname(file).toLowerCase();
  if (ext === '.html') { nHtml++; auditHtml(file, readFileSync(file, 'utf8')); }
  else if (ext === '.css') { nCss++; auditCss(file, readFileSync(file, 'utf8')); }
  else if (IMG_EXT.has(ext)) { nImg++; auditImageFile(file); }
}

// ---- report ---------------------------------------------------------------
const errors = findings.filter((f) => f.sev === 'error');
const warns = findings.filter((f) => f.sev === 'warn');

if (JSON_OUT) {
  console.log(JSON.stringify({ dir: DIR, scanned: { html: nHtml, css: nCss, img: nImg }, errors, warns }, null, 2));
} else {
  const byFile = {};
  for (const f of findings) (byFile[f.file] ||= []).push(f);
  const icon = (s) => (s === 'error' ? '✗' : '⚠');
  for (const [file, fs] of Object.entries(byFile)) {
    console.log(`\n${file}`);
    for (const f of fs.sort((a, b) => (a.sev === b.sev ? 0 : a.sev === 'error' ? -1 : 1)))
      console.log(`  ${icon(f.sev)} [${f.rule}] ${f.msg}`);
  }
  // Rough heuristic score: errors dominate; warns nudge. Repeated soft
  // advisories (e.g. long titles across many pages) shouldn't crater it.
  const score = Math.max(0, Math.round(100 - errors.length * 8 - warns.length * 0.5));
  console.log(`\n${'─'.repeat(56)}`);
  console.log(`scanned: ${nHtml} html · ${nCss} css · ${nImg} images`);
  console.log(`errors: ${errors.length}   warnings: ${warns.length}   heuristic score: ${score}/100`);
  if (nHtml === 0) console.log('note: 0 HTML files found — is --dir pointing at the build output?');
}

const failed = errors.length > 0 || (STRICT && warns.length > 0);
process.exit(failed ? 1 : 0);
