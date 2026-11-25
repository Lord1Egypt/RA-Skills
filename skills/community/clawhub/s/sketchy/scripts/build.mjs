#!/usr/bin/env node
// build.mjs: inline every local stylesheet, script, font and image into one self-contained HTML file.
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { parseArgs, say, die, fmtBytes, rel, baseName, isMain, c } from './_lib.mjs';

const MB = 1024 * 1024;
const SIZE_WARN = 8 * MB;

const MIME = {
  '.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf', '.otf': 'font/otf', '.eot': 'application/vnd.ms-fontobject',
  '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.gif': 'image/gif', '.webp': 'image/webp',
  '.avif': 'image/avif', '.svg': 'image/svg+xml', '.ico': 'image/x-icon', '.bmp': 'image/bmp',
  '.mp3': 'audio/mpeg', '.wav': 'audio/wav', '.ogg': 'audio/ogg', '.m4a': 'audio/mp4',
  '.mp4': 'video/mp4', '.webm': 'video/webm', '.json': 'application/json', '.css': 'text/css', '.js': 'text/javascript',
};
const FONT_EXT = new Set(['.woff2', '.woff', '.ttf', '.otf', '.eot']);

const spec = {
  name: 'sketchy build', file: 'build.mjs', usage: '<in.html> [-o out.html]',
  summary: 'inline every local CSS, JS, font and image into one self-contained HTML file.',
  details: [
    'Inlines <link rel=stylesheet>, @import, <script src>, CSS url() (fonts, images as base64),',
    '<img src> and icons. Paths resolve relative to the file that mentions them.',
    'https:// URLs stay as they are and print a warning (the result then needs a network).',
    'Safe to run again on its own output: nothing local is left, so the file stays the same.',
  ],
  options: [
    { name: 'out', short: 'o', type: 'string', arg: 'file', help: 'output file (default: out/<name>.html next to the input)' },
  ],
  positionals: { min: 1, max: 1, name: '<in.html>' },
  examples: ['node build.mjs deck.html', 'node build.mjs deck.html -o dist/deck.html'],
};

/* ---------- small helpers ---------- */
const lineAt = (text, index) => { let n = 1; for (let i = 0; i < index && i < text.length; i++) if (text.charCodeAt(i) === 10) n++; return n; };
const isRemote = (u) => /^(?:https?:|ftp:|wss?:)?\/\//i.test(u) || /^(?:https?|ftp|wss?):/i.test(u);
const isSkipped = (u) => !u || u.startsWith('#') || /^(?:data|blob|about|javascript|mailto|tel):/i.test(u);

function parseAttrs(str) {
  const attrs = [];
  const re = /([^\s"'<>\/=]+)(?:\s*=\s*(?:"([^"]*)"|'([^']*)'|([^\s"'=<>`]+)))?/g;
  let m;
  while ((m = re.exec(str))) attrs.push([m[1], m[2] ?? m[3] ?? m[4] ?? null]);
  return attrs;
}
const getAttr = (attrs, name) => { const a = attrs.find(([n]) => n.toLowerCase() === name); return a ? a[1] : undefined; };
const hasAttr = (attrs, name) => attrs.some(([n]) => n.toLowerCase() === name);
const dropAttrs = (attrs, names) => attrs.filter(([n]) => !names.includes(n.toLowerCase()));
const serAttrs = (attrs) => attrs.map(([n, v]) => (v === null ? n : `${n}="${String(v).replace(/"/g, '&quot;')}"`)).join(' ');
const withAttrs = (tag, attrs) => `<${tag}${attrs.length ? ' ' + serAttrs(attrs) : ''}>`;

/** Split "a/b.png?x=1#y" into { file: "a/b.png", suffix: "?x=1#y" }. */
function splitRef(ref) {
  const i = ref.search(/[?#]/);
  return i < 0 ? { file: ref, suffix: '' } : { file: ref.slice(0, i), suffix: ref.slice(i) };
}

export function buildHtml(inputAbs) {
  const htmlDir = path.dirname(inputAbs);
  const stats = { css: 0, js: 0, fonts: 0, images: 0, media: 0, bytesByFile: new Map() };
  const warnings = new Map(); // text -> fix
  const errors = new Map();
  const warn = (msg, fix) => { if (!warnings.has(msg)) warnings.set(msg, fix); };
  const fail = (msg, fix) => { if (!errors.has(msg)) errors.set(msg, fix); };

  function resolveLocal(ref, baseDir, whereLabel) {
    const { file } = splitRef(ref);
    let p;
    if (/^file:/i.test(file)) { try { p = fileURLToPath(file); } catch { fail(`${whereLabel}: bad file URL ${ref}`, 'use a relative path'); return null; } }
    else {
      let decoded = file;
      try { decoded = decodeURI(file); } catch { /* keep raw */ }
      p = decoded.startsWith('/') && !path.isAbsolute(decoded.slice(1)) ? path.join(htmlDir, decoded) : path.resolve(baseDir, decoded);
    }
    if (!fs.existsSync(p) || !fs.statSync(p).isFile()) {
      fail(`${whereLabel}: file not found: ${ref}`, `put the file at ${rel(p)} or correct the path`);
      return null;
    }
    return p;
  }

  function dataUri(p, whereLabel) {
    const ext = path.extname(p).toLowerCase();
    const mime = MIME[ext];
    if (!mime) { warn(`${whereLabel}: unknown file type ${ext || '(none)'} for ${path.basename(p)}, using application/octet-stream`, 'rename it with a standard extension'); }
    const buf = fs.readFileSync(p);
    stats.bytesByFile.set(p, buf.length);
    if (FONT_EXT.has(ext)) stats.fonts++;
    else if (/^image\//.test(mime || '')) stats.images++;
    else stats.media++;
    return `data:${mime || 'application/octet-stream'};base64,${buf.toString('base64')}`;
  }

  /* ----- CSS: @import and url() ----- */
  const CSS_RE = /\/\*[\s\S]*?\*\/|@import\s+(?:url\(\s*(?:"([^"]*)"|'([^']*)'|([^)\s]*))\s*\)|"([^"]*)"|'([^']*)')\s*([^;]*);|url\(\s*(?:"([^"]*)"|'([^']*)'|([^)\s]*))\s*\)/gi;

  function inlineCss(css, cssFile, labelFile, stack) {
    const dir = path.dirname(cssFile);
    css = css.replace(/^﻿/, '').replace(/^\s*@charset\s+[^;]+;/i, '');
    css = css.replace(CSS_RE, (m, i1, i2, i3, i4, i5, media, u1, u2, u3, offset, whole) => {
      if (m.startsWith('/*')) return m;
      const where = `${labelFile}:${lineAt(whole, offset)}`;
      if (/^@import/i.test(m)) {
        const ref = (i1 ?? i2 ?? i3 ?? i4 ?? i5 ?? '').trim();
        if (isSkipped(ref)) return m;
        if (isRemote(ref)) { warn(`${where}: remote @import ${ref} stays a network request`, 'download that stylesheet next to the page and import the local copy'); return m; }
        if (/layer\(|supports\(/i.test(media || '')) { warn(`${where}: @import with layer() or supports() cannot be inlined`, 'use a plain <link> or @import'); return m; }
        const p = resolveLocal(ref, dir, where);
        if (!p) return m;
        if (stack.includes(p)) { fail(`${where}: @import loop at ${ref}`, 'remove the circular import'); return m; }
        stats.css++;
        const body = inlineCss(fs.readFileSync(p, 'utf8'), p, rel(p), [...stack, p]);
        const mq = (media || '').trim();
        return mq ? `@media ${mq} {\n${body}\n}` : body;
      }
      const ref = (u1 ?? u2 ?? u3 ?? '').trim();
      if (isSkipped(ref)) return m;
      if (isRemote(ref)) { warn(`${where}: remote url(${ref.length > 60 ? ref.slice(0, 57) + '...' : ref}) stays a network request`, 'download the file next to the stylesheet and reference the local copy'); return m; }
      const p = resolveLocal(ref, dir, where);
      if (!p) return m;
      return `url(${dataUri(p, where)})`;
    });
    css = css.replace(/\/\*#\s*sourceMappingURL=[^*]*\*\//g, '');
    return css;
  }

  /* ----- HTML ----- */
  const ATTR = `((?:"[^"]*"|'[^']*'|[^'">])*)`;
  const TAG_RE = new RegExp(
    `<!--[\\s\\S]*?-->|<script\\b${ATTR}>([\\s\\S]*?)<\\/script\\s*>|<style\\b${ATTR}>([\\s\\S]*?)<\\/style\\s*>|<([a-zA-Z][\\w:-]*)\\b${ATTR}>`, 'gi');
  const ASSET_ATTRS = { img: ['src'], source: ['src'], video: ['src', 'poster'], audio: ['src'], image: ['href', 'xlink:href'], input: ['src'] };

  const src = fs.readFileSync(inputAbs, 'utf8').replace(/^﻿/, '');
  const inputLabel = rel(inputAbs);

  const out = src.replace(TAG_RE, (m, sAttr, sBody, stAttr, stBody, tag, tAttr, offset, whole) => {
    if (m.startsWith('<!--')) return m;
    const where = `${inputLabel}:${lineAt(whole, offset)}`;

    /* <script src> */
    if (sAttr !== undefined) {
      const attrs = parseAttrs(sAttr);
      const ref = getAttr(attrs, 'src');
      if (ref === undefined || ref === null) return m;
      if (isSkipped(ref)) return m;
      if (isRemote(ref)) { warn(`${where}: remote script ${ref.length > 70 ? ref.slice(0, 67) + '...' : ref} stays a network request`, 'download it next to the page and use the local copy'); return m; }
      const p = resolveLocal(ref, htmlDir, where);
      if (!p) return m;
      stats.js++;
      if (hasAttr(attrs, 'defer') && getAttr(attrs, 'type') !== 'module') warn(`${where}: defer on ${ref} is dropped when inlined`, 'put the script tag at the end of <body>');
      let js = fs.readFileSync(p, 'utf8').replace(/^﻿/, '').replace(/\/\/[#@]\s*sourceMappingURL=.*$/gm, '');
      stats.bytesByFile.set(p, js.length);
      js = js.replace(/<\/(script)/gi, '<\\/$1');
      if (js.includes('<!--')) js = js.replace(/<!--/g, '<\\!--');
      const keep = dropAttrs(attrs, ['src', 'defer', 'async', 'integrity', 'crossorigin', 'referrerpolicy', 'nomodule']);
      return `${withAttrs('script', keep)}\n/* sketchy build: ${path.relative(htmlDir, p).split(path.sep).join('/')} */\n${js}\n</script>`;
    }

    /* <style> blocks: resolve their @import and url() relative to the page */
    if (stAttr !== undefined) {
      if (!/url\(|@import/i.test(stBody)) return m;
      const attrs = parseAttrs(stAttr);
      const body = inlineCss(stBody, inputAbs, inputLabel, [inputAbs]).replace(/<\/(style)/gi, '<\\/$1');
      return `${withAttrs('style', attrs)}${body}</style>`;
    }

    /* every other tag */
    const t = tag.toLowerCase();
    const attrs = parseAttrs(tAttr);

    if (t === 'link') {
      const relv = (getAttr(attrs, 'rel') || '').toLowerCase();
      const href = getAttr(attrs, 'href');
      if (!href || isSkipped(href)) return m;
      const kinds = relv.split(/\s+/);
      if (kinds.includes('stylesheet')) {
        if (isRemote(href)) { warn(`${where}: remote stylesheet ${href.length > 70 ? href.slice(0, 67) + '...' : href} stays a network request`, 'download it next to the page and link the local copy'); return m; }
        const p = resolveLocal(href, htmlDir, where);
        if (!p) return m;
        stats.css++;
        const css = inlineCss(fs.readFileSync(p, 'utf8'), p, rel(p), [p]).replace(/<\/(style)/gi, '<\\/$1');
        stats.bytesByFile.set(p, css.length);
        const keep = dropAttrs(attrs, ['rel', 'href', 'integrity', 'crossorigin', 'referrerpolicy', 'type', 'as', 'hreflang', 'blocking']);
        return `${withAttrs('style', keep)}\n/* sketchy build: ${path.relative(htmlDir, p).split(path.sep).join('/')} */\n${css}\n</style>`;
      }
      if (kinds.some((k) => ['preload', 'prefetch', 'modulepreload'].includes(k)) && !isRemote(href)) return ''; // the file is inlined now
      if (kinds.some((k) => k === 'icon' || k === 'apple-touch-icon' || k === 'shortcut')) {
        if (isRemote(href)) return m;
        const p = resolveLocal(href, htmlDir, where);
        if (!p) return m;
        return withAttrs('link', attrs.map(([n, v]) => (n.toLowerCase() === 'href' ? [n, dataUri(p, where)] : [n, v])));
      }
      return m;
    }

    let changed = false;
    let next = attrs;
    const assetNames = ASSET_ATTRS[t];
    if (assetNames && !(t === 'input' && (getAttr(attrs, 'type') || '').toLowerCase() !== 'image')) {
      next = next.map(([n, v]) => {
        if (!assetNames.includes(n.toLowerCase()) || v === null || isSkipped(v)) return [n, v];
        if (isRemote(v)) { warn(`${where}: remote ${t} ${v.length > 70 ? v.slice(0, 67) + '...' : v} stays a network request`, 'download it next to the page'); return [n, v]; }
        const p = resolveLocal(v, htmlDir, where);
        if (!p) return [n, v];
        changed = true;
        return [n, dataUri(p, where)];
      });
    }
    const styleVal = getAttr(next, 'style');
    if (styleVal && /url\(/i.test(styleVal)) {
      const nv = inlineCss(styleVal, inputAbs, inputLabel, [inputAbs]);
      if (nv !== styleVal) { next = next.map(([n, v]) => (n.toLowerCase() === 'style' ? [n, nv] : [n, v])); changed = true; }
    }
    return changed ? `<${tag}${next.length ? ' ' + serAttrs(next) : ''}${/\/\s*>$/.test(m) ? ' /' : ''}>` : m;
  });

  return { html: out, stats, warnings, errors };
}

function main() {
  const { values, positionals } = parseArgs(process.argv.slice(2), spec);
  const inputAbs = path.resolve(positionals[0]);
  if (!fs.existsSync(inputAbs) || !fs.statSync(inputAbs).isFile()) die(`input not found: ${positionals[0]}`, 'pass the path of an .html file');

  let outAbs;
  if (values.out) outAbs = path.resolve(values.out);
  else if (path.basename(path.dirname(inputAbs)) === 'out') outAbs = inputAbs; // already in out/: rebuild in place, stay idempotent
  else outAbs = path.join(path.dirname(inputAbs), 'out', `${baseName(inputAbs)}.html`);

  const { html, stats, warnings, errors } = buildHtml(inputAbs);

  for (const [msg, fix] of warnings) { say.warn(msg); if (fix) say.fix(fix); }
  if (errors.size) {
    for (const [msg, fix] of errors) { say.error(msg); if (fix) say.fix(fix); }
    console.error(`${errors.size} file${errors.size === 1 ? '' : 's'} missing, nothing written`);
    process.exit(1);
  }

  fs.mkdirSync(path.dirname(outAbs), { recursive: true });
  fs.writeFileSync(outAbs, html);
  const size = Buffer.byteLength(html);
  const parts = [];
  if (stats.css) parts.push(`${stats.css} css`);
  if (stats.js) parts.push(`${stats.js} js`);
  if (stats.fonts) parts.push(`${stats.fonts} font${stats.fonts === 1 ? '' : 's'}`);
  if (stats.images) parts.push(`${stats.images} image${stats.images === 1 ? '' : 's'}`);
  if (stats.media) parts.push(`${stats.media} media`);
  say.ok(`built ${rel(outAbs)}  ${fmtBytes(size)}  ${parts.length ? '(inlined ' + parts.join(', ') + ')' : c.dim('(nothing local left to inline)')}`);
  if (size > SIZE_WARN) {
    const big = [...stats.bytesByFile.entries()].sort((a, b) => b[1] - a[1])[0];
    say.warn(`${fmtBytes(size)} is over ${SIZE_WARN / MB} MB; mail and chat tools may refuse it${big ? ` (largest: ${path.basename(big[0])}, ${fmtBytes(big[1])})` : ''}`);
    say.fix('shrink images (max 1600 px wide, JPEG or WebP) and drop unused font files');
  }
}

if (isMain(import.meta.url)) main();
