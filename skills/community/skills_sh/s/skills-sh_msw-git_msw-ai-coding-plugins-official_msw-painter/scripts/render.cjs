#!/usr/bin/env node
'use strict';

/**
 * msw-painter render helper — converts SVG/Canvas/HTML code to PNG.
 *
 * Usage:
 *   node render.cjs --type <svg|canvas|html> --in <path> --out <path.png> --width <px> --height <px>
 *
 * Code can also be passed via stdin instead of --in (use `--in -` or omit --in).
 * Transparent background by default. width/height default to 128×128 when omitted.
 *
 * Exit code: 0 = success, 1 = failure (message on stderr).
 *
 * Security posture (W012 mitigations):
 *   - All network requests from the page are blocked at the puppeteer level
 *     (request interception). Sprite rendering needs no external resources.
 *   - A strict Content-Security-Policy meta tag is injected so that even if
 *     interception is bypassed, the page cannot reach external origins.
 *   - SVG / HTML input is sanitized to remove <script>, <foreignObject>,
 *     event handlers (on*), and any non-data: href / xlink:href / src.
 *   - Chromium is launched without --no-sandbox unless explicitly opted in
 *     via PAINTER_DISABLE_SANDBOX=1 (e.g. CI containers that require it).
 *
 * Dependency: puppeteer (one-time `npm ci` required; see SKILL.md).
 */

const fs = require('fs');
const path = require('path');

function parseArgs(argv) {
  const args = { type: null, in: null, out: null, width: 128, height: 128 };
  for (let i = 2; i < argv.length; i++) {
    const k = argv[i];
    const v = argv[i + 1];
    if (k === '--type') { args.type = v; i++; }
    else if (k === '--in') { args.in = v; i++; }
    else if (k === '--out') { args.out = v; i++; }
    else if (k === '--width') { args.width = parseInt(v, 10); i++; }
    else if (k === '--height') { args.height = parseInt(v, 10); i++; }
    else if (k === '-h' || k === '--help') { args.help = true; }
  }
  return args;
}

function usage() {
  console.error('Usage: node render.cjs --type <svg|canvas|html> [--in <path>|-] --out <path.png> [--width N] [--height N]');
}

function readInput(inPath) {
  if (!inPath || inPath === '-') {
    return fs.readFileSync(0, 'utf8');
  }
  return fs.readFileSync(inPath, 'utf8');
}

// --- Input sanitization (W012) -------------------------------------------------
//
// Sprite rendering legitimately needs only static markup and inline scripts that
// draw to a canvas. It NEVER needs to load remote resources or attach DOM event
// handlers. We strip the classes of constructs that could exfiltrate data or
// pull in attacker-controlled code, even though the network is also blocked.
//
// This is intentionally conservative: SVG <script> is allowed inside a normal
// SVG, but is unnecessary for the chunky/maple styles documented in SKILL.md,
// so we remove it. The canvas type intentionally keeps its own controlled
// <script> wrapper (built below in buildHtml), which is injected by us, not by
// the user.

function sanitizeMarkup(src) {
  if (typeof src !== 'string') return '';
  let s = src;

  // Remove <script>…</script> blocks (any case, any attributes).
  s = s.replace(/<script\b[\s\S]*?<\/script\s*>/gi, '');
  // Remove self-closing or unterminated <script ...> tags too.
  s = s.replace(/<script\b[^>]*\/?>/gi, '');

  // Remove <foreignObject> — can host arbitrary HTML inside SVG.
  s = s.replace(/<foreignObject\b[\s\S]*?<\/foreignObject\s*>/gi, '');
  s = s.replace(/<foreignObject\b[^>]*\/?>/gi, '');

  // Remove <iframe>, <object>, <embed>, <link>, <meta http-equiv refresh>.
  s = s.replace(/<(iframe|object|embed|link)\b[\s\S]*?<\/\1\s*>/gi, '');
  s = s.replace(/<(iframe|object|embed|link|meta)\b[^>]*\/?>/gi, '');

  // Strip inline event handlers: on*="..." or on*='...'.
  s = s.replace(/\son[a-z]+\s*=\s*"(?:[^"\\]|\\.)*"/gi, '');
  s = s.replace(/\son[a-z]+\s*=\s*'(?:[^'\\]|\\.)*'/gi, '');
  s = s.replace(/\son[a-z]+\s*=\s*[^\s>]+/gi, '');

  // Block non-data: URLs in href / xlink:href / src.
  // We allow only: data: URIs, fragment refs (#foo), and empty values.
  const urlAttr = /(\s(?:xlink:href|href|src)\s*=\s*)("([^"]*)"|'([^']*)')/gi;
  s = s.replace(urlAttr, (full, prefix, _quoted, dq, sq) => {
    const val = (dq !== undefined ? dq : sq) || '';
    const safe = val === '' || val.startsWith('data:') || val.startsWith('#');
    return safe ? full : `${prefix}""`;
  });

  // Block javascript:/vbscript:/etc. anywhere they might survive above passes.
  s = s.replace(/\b(?:javascript|vbscript|data:text\/html)\s*:/gi, 'about:blank#blocked-');

  return s;
}

// --- HTML scaffolding ----------------------------------------------------------

function buildHtml(type, code, width, height) {
  // Strict CSP: no network at all, only inline styles/scripts that we ourselves
  // inject below. `default-src 'none'` denies everything; we then re-allow only
  // the inline pieces that the canvas wrapper genuinely needs.
  const csp = [
    "default-src 'none'",
    "img-src data:",
    "style-src 'unsafe-inline'",
    "script-src 'unsafe-inline'",
    "base-uri 'none'",
    "form-action 'none'",
    "frame-ancestors 'none'",
  ].join('; ');

  const head = `<!doctype html>
<html><head>
  <meta charset="utf-8">
  <meta http-equiv="Content-Security-Policy" content="${csp}">
  <style>
    html, body { margin: 0; padding: 0; background: transparent; }
    body { width: ${width}px; height: ${height}px; image-rendering: pixelated; image-rendering: crisp-edges; }
    svg, canvas, img { display: block; image-rendering: pixelated; image-rendering: crisp-edges; }
  </style>
</head><body>`;
  const closer = `</body></html>`;

  if (type === 'svg') {
    return head + sanitizeMarkup(code) + closer;
  }

  if (type === 'canvas') {
    // The user code runs inside our wrapper; the wrapper itself is trusted, but
    // we still want the user's code to be unable to reach the network. The CSP
    // and request interception cover that.
    return head
      + `<canvas id="__c" width="${width}" height="${height}"></canvas>`
      + `<script>
          (function(){
            var c = document.getElementById('__c');
            var ctx = c.getContext('2d');
            ctx.imageSmoothingEnabled = false;
            try {
              ${code}
              window.__painterDone = true;
            } catch (e) {
              window.__painterError = String(e && e.stack || e);
            }
          })();
        </script>`
      + closer;
  }

  if (type === 'html') {
    // Full-document HTML mode: still sanitize, but we don't wrap in our head.
    // We DO inject a CSP meta as the first child of <head> if one exists,
    // otherwise we fall back to the wrapped form.
    const sanitized = sanitizeMarkup(code);
    if (/<head\b[^>]*>/i.test(sanitized)) {
      return sanitized.replace(
        /<head\b[^>]*>/i,
        (m) => `${m}<meta http-equiv="Content-Security-Policy" content="${csp}">`
      );
    }
    return head + sanitized + closer;
  }

  throw new Error(`unknown type: ${type}`);
}

// --- Puppeteer driver ----------------------------------------------------------

async function render(args) {
  const puppeteer = require('puppeteer');

  const code = readInput(args.in);
  const html = buildHtml(args.type, code, args.width, args.height);

  // Sandbox: keep Chromium's sandbox ON by default. Some constrained
  // environments (CI containers, WSL without user namespaces) cannot start
  // a sandboxed Chromium; allow opt-out via env var only.
  const disableSandbox = process.env.PAINTER_DISABLE_SANDBOX === '1';
  const launchArgs = ['--disable-dev-shm-usage'];
  if (disableSandbox) {
    launchArgs.push('--no-sandbox', '--disable-setuid-sandbox');
  }

  const browser = await puppeteer.launch({
    headless: 'new',
    args: launchArgs,
  });

  try {
    const page = await browser.newPage();

    // Block ALL network requests. Sprite rendering does not need network.
    // Even with CSP in place, request interception is the belt-and-suspenders
    // guarantee that no external origin is ever contacted.
    await page.setRequestInterception(true);
    page.on('request', (req) => {
      const url = req.url();
      // Allow the synthetic data: URL we navigate to, and nothing else.
      if (url.startsWith('data:') || url === 'about:blank') {
        req.continue();
      } else {
        req.abort();
      }
    });

    await page.setViewport({ width: args.width, height: args.height, deviceScaleFactor: 1 });

    // Navigate to a data: URL instead of using setContent + networkidle. With
    // network fully blocked, networkidle would have nothing to wait on anyway,
    // and data: URLs make the origin opaque so even relative URL tricks fail.
    const dataUrl = 'data:text/html;charset=utf-8,' + encodeURIComponent(html);
    await page.goto(dataUrl, { waitUntil: 'load' });

    if (args.type === 'canvas') {
      await page.waitForFunction(
        () => window.__painterDone === true || typeof window.__painterError === 'string',
        { timeout: 10000 }
      );
      const err = await page.evaluate(() => window.__painterError);
      if (err) throw new Error('canvas code threw:\n' + err);
    }

    const outDir = path.dirname(path.resolve(args.out));
    if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

    const clip = { x: 0, y: 0, width: args.width, height: args.height };
    await page.screenshot({ path: args.out, type: 'png', omitBackground: true, clip });
  } finally {
    await browser.close();
  }
}

(async () => {
  const args = parseArgs(process.argv);
  if (args.help) { usage(); process.exit(0); }
  if (!args.type || !args.out) {
    usage();
    process.exit(1);
  }
  if (!['svg', 'canvas', 'html'].includes(args.type)) {
    console.error(`--type must be svg|canvas|html (got: ${args.type})`);
    process.exit(1);
  }
  if (!Number.isFinite(args.width) || !Number.isFinite(args.height) || args.width <= 0 || args.height <= 0) {
    console.error(`--width / --height must be positive integers`);
    process.exit(1);
  }

  try {
    await render(args);
    process.stdout.write(path.resolve(args.out) + '\n');
  } catch (e) {
    console.error('render failed:', e && e.stack || e);
    process.exit(1);
  }
})();
