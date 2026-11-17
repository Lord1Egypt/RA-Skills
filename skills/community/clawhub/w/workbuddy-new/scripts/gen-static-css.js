#!/usr/bin/env node
/*
 * gen-static-css.js
 * Produce a SELF-CONTAINED css for asar injection (no runtime host-class,
 * no CSS vars). Reads the runtime skin css (scoped under
 * html.dream-host-workbuddy / :root.dream-host-workbuddy) and:
 *   - strips the scope prefixes -> global (:root kept for var block)
 *   - inlines hero/texture PNGs as base64 data URIs (replacing var(--dream-hero...))
 *   NOTE: no marker here - asar-patch.js owns the marker block
 * Usage: node gen-static-css.js --theme-dir <dir> --out <file>
 */
const fs = require('fs');
const path = require('path');

function parseArgs(argv) {
  const a = { themeDir: null, out: null };
  for (let i = 0; i < argv.length; i++) {
    if (argv[i] === '--theme-dir') a.themeDir = argv[++i];
    else if (argv[i] === '--out') a.out = argv[++i];
  }
  return a;
}
function dataUri(p) {
  const b = fs.readFileSync(p);
  const ext = path.extname(p).slice(1).toLowerCase();
  const mime = ext === 'jpg' || ext === 'jpeg' ? 'image/jpeg'
             : ext === 'webp' ? 'image/webp' : 'image/png';
  return `url("data:${mime};base64,${b.toString('base64')}")`;
}

const a = parseArgs(process.argv.slice(2));
if (!a.themeDir || !a.out) { console.error('need --theme-dir and --out'); process.exit(1); }

const pkg = JSON.parse(fs.readFileSync(path.join(a.themeDir, 'theme.json'), 'utf8'));
const cssRel = pkg.targets.workbuddy.css;
let css = fs.readFileSync(path.join(a.themeDir, cssRel), 'utf8');

const imgs = pkg.images || {};
let hero = null, texture = null;
if (imgs.hero) { const p = path.resolve(a.themeDir, imgs.hero); if (fs.existsSync(p)) hero = dataUri(p); }
if (imgs.texture) { const p = path.resolve(a.themeDir, imgs.texture); if (fs.existsSync(p)) texture = dataUri(p); }

// 1) strip scope prefixes -> global
css = css.replace(/html\.dream-host-workbuddy/g, '');
css = css.replace(/:root\.dream-host-workbuddy/g, ':root');
// 2) inline hero/texture (with or without fallback)
if (hero) css = css.replace(/var\(--dream-hero[^)]*\)/g, hero);
if (texture) css = css.replace(/var\(--dream-texture[^)]*\)/g, texture);

// NOTE: do NOT wrap in a marker here. asar-patch.js owns the marker block
// (it wraps the inject css); pre-baking the marker would trip its
// double-inject guard. Output is the raw self-contained static css only.
fs.writeFileSync(a.out, css, 'utf8');
console.log('Wrote static css:', a.out, css.length, 'bytes; hero inlined:', !!hero);
