// _lib.mjs: shared helpers for the sketchy scripts (Node 18+, no dependencies).
// Playwright resolution, argument parsing, short exact output.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { createRequire } from 'node:module';
import { fileURLToPath, pathToFileURL } from 'node:url';

export const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
export const SKILL_DIR = path.resolve(SCRIPT_DIR, '..');
export const ENGINE_DIR = path.join(SKILL_DIR, 'engine');
export const PW_VERSION = '1.63.0';
export const INSTALL_CMD = `npm i -D playwright@${PW_VERSION} && npx playwright install chromium`;
/** The install lines every script prints when playwright is missing (global in ~/.sketchy, or inside a project). */
export const INSTALL_LINES = [
  `macOS, Linux, Git Bash:  npm install --prefix ~/.sketchy playwright@${PW_VERSION} && npx --prefix ~/.sketchy playwright install chromium`,
  `Windows (cmd):           npm install --prefix "%USERPROFILE%\\.sketchy" playwright@${PW_VERSION} && npx --prefix "%USERPROFILE%\\.sketchy" playwright install chromium`,
  `Windows (PowerShell):    npm install --prefix "$env:USERPROFILE\\.sketchy" playwright@${PW_VERSION}; npx --prefix "$env:USERPROFILE\\.sketchy" playwright install chromium`,
  `inside a project:        ${INSTALL_CMD}`,
];

// a reader that closes the pipe early (| head) is not an error
for (const stream of [process.stdout, process.stderr]) stream.on('error', (e) => { if (e && e.code === 'EPIPE') process.exit(0); });

/* ---------- output ---------- */
const tty = Boolean(process.stdout.isTTY) && !process.env.NO_COLOR;
const paint = (code, s) => (tty ? `\x1b[${code}m${s}\x1b[0m` : s);
export const c = {
  red: (s) => paint(31, s), green: (s) => paint(32, s), yellow: (s) => paint(33, s),
  blue: (s) => paint(34, s), dim: (s) => paint(2, s), bold: (s) => paint(1, s),
};
const LABEL = { ok: c.green('ok   '), warn: c.yellow('warn '), error: c.red('error'), info: c.dim('info ') };
export const say = {
  ok: (m) => console.log(`${LABEL.ok} ${m}`),
  warn: (m) => console.log(`${LABEL.warn} ${m}`),
  error: (m) => console.log(`${LABEL.error} ${m}`),
  info: (m) => console.log(`${LABEL.info} ${m}`),
  fix: (m) => fixLines(m).forEach((l, i) => console.log(i === 0 ? `${c.dim('fix:')}  ${l}` : `      ${l}`)),
  line: (m = '') => console.log(m),
};

const fixLines = (fix) => (Array.isArray(fix) ? fix : [fix]);

/** Print an error with its fix and exit (default code 2 = bad usage or missing environment). */
export function die(message, fix, code = 2) {
  console.error(`${LABEL.error} ${message}`);
  if (fix) fixLines(fix).forEach((l, i) => console.error(i === 0 ? `${c.dim('fix:')}  ${l}` : `      ${l}`));
  process.exit(code);
}

export function fmtBytes(n) {
  if (n < 1024) return `${n} B`;
  if (n < 1024 * 1024) return `${(n / 1024).toFixed(1)} KB`;
  return `${(n / 1024 / 1024).toFixed(2)} MB`;
}

/** Path relative to the current folder when that is shorter, else absolute. */
export function rel(p) {
  const r = path.relative(process.cwd(), p);
  return r && !r.startsWith('..') && !path.isAbsolute(r) ? r : p;
}

/* ---------- arguments ---------- */
const camel = (s) => s.replace(/-([a-z])/g, (_, ch) => ch.toUpperCase());

export function printHelp(spec) {
  const out = [];
  out.push(`${spec.name}: ${spec.summary}`, '', `usage: node ${spec.file} ${spec.usage}`, '');
  if (spec.details) out.push(...spec.details, '');
  const opts = [...(spec.options || []), { name: 'help', short: 'h', type: 'boolean', help: 'show this help' }];
  out.push('options:');
  const left = opts.map((o) => `${o.short ? `-${o.short}, ` : '    '}--${o.name}${o.type && o.type !== 'boolean' ? ` <${o.arg || o.type}>` : ''}`);
  const w = Math.max(...left.map((l) => l.length));
  opts.forEach((o, i) => out.push(`  ${left[i].padEnd(w)}  ${o.help || ''}`));
  if (spec.examples && spec.examples.length) { out.push('', 'examples:'); spec.examples.forEach((e) => out.push(`  ${e}`)); }
  out.push('', 'exit codes: 0 ok, 1 problems found, 2 bad usage or missing environment');
  console.log(out.join('\n'));
}

export function parseArgs(argv, spec) {
  const opts = spec.options || [];
  const byLong = new Map(opts.map((o) => [o.name, o]));
  const byShort = new Map(opts.filter((o) => o.short).map((o) => [o.short, o]));
  const values = {};
  const positionals = [];
  for (const o of opts) if (o.default !== undefined) values[camel(o.name)] = o.default;
  const usageError = (msg) => die(msg, `node ${spec.file} --help`);
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--') { positionals.push(...argv.slice(i + 1)); break; }
    if (a === '-h' || a === '--help') { printHelp(spec); process.exit(0); }
    let o, val;
    if (a.startsWith('--')) {
      const eq = a.indexOf('=');
      const name = eq > 0 ? a.slice(2, eq) : a.slice(2);
      val = eq > 0 ? a.slice(eq + 1) : undefined;
      o = byLong.get(name);
      if (!o) usageError(`unknown option --${name}`);
    } else if (a.startsWith('-') && a.length > 1 && !/^-\d/.test(a)) {
      o = byShort.get(a.slice(1));
      if (!o) usageError(`unknown option ${a}`);
    } else { positionals.push(a); continue; }
    const key = camel(o.name);
    if (o.type === 'boolean') values[key] = val === undefined ? true : !/^(0|false|no)$/i.test(val);
    else {
      if (val === undefined) { val = argv[++i]; if (val === undefined) usageError(`--${o.name} needs a value`); }
      if (o.type === 'number') { const n = Number(val); if (!Number.isFinite(n)) usageError(`--${o.name} needs a number, got "${val}"`); values[key] = n; }
      else values[key] = val;
    }
  }
  const pmin = spec.positionals?.min ?? 0, pmax = spec.positionals?.max ?? 0;
  if (positionals.length < pmin) usageError(`missing ${spec.positionals.name || 'argument'}`);
  if (positionals.length > pmax) usageError(`unexpected argument "${positionals[pmax]}"`);
  return { values, positionals };
}

/** True when the module is the one node was started with. */
export function isMain(metaUrl) {
  try {
    const a = fs.realpathSync(path.resolve(process.argv[1] || ''));
    const b = fs.realpathSync(fileURLToPath(metaUrl));
    return process.platform === 'win32' ? a.toLowerCase() === b.toLowerCase() : a === b;
  } catch { return false; }
}

/* ---------- files and URLs ---------- */
export function fileUrl(file, query = '') {
  return pathToFileURL(path.resolve(file)).href + (query ? `?${query}` : '');
}

export function requireHtmlFile(arg, what = 'file') {
  if (!arg) die(`missing ${what}`, 'pass the path of an .html file');
  const abs = path.resolve(arg);
  if (!fs.existsSync(abs)) die(`${what} not found: ${arg}`, 'check the path (quote it when it contains spaces)');
  if (!fs.statSync(abs).isFile()) die(`not a file: ${arg}`, 'pass an .html file, not a folder');
  return abs;
}

export const baseName = (file) => path.basename(file, path.extname(file));

export function sketchyHome() {
  return process.env.SKETCHY_HOME ? path.resolve(process.env.SKETCHY_HOME) : path.join(os.homedir(), '.sketchy');
}

/* ---------- playwright ---------- */
/** Where playwright is looked up, in order. */
export function playwrightCandidates() {
  const list = [
    { name: 'current folder', base: process.cwd() },
    { name: 'repo root', base: path.resolve(SCRIPT_DIR, '..', '..', '..') },
    { name: process.env.SKETCHY_HOME ? '$SKETCHY_HOME' : '~/.sketchy', base: sketchyHome() },
  ];
  if (process.env.CLAUDE_PLUGIN_DATA) list.push({ name: '$CLAUDE_PLUGIN_DATA', base: path.resolve(process.env.CLAUDE_PLUGIN_DATA) });
  return list;
}

/** Resolve playwright: current folder, repo root, $SKETCHY_HOME or ~/.sketchy, then $CLAUDE_PLUGIN_DATA. */
export function loadPlaywright() {
  for (const cand of playwrightCandidates()) {
    try {
      const req = createRequire(path.join(cand.base, '_resolve.cjs'));
      const entry = req.resolve('playwright', { paths: [cand.base] });
      const pw = req(entry);
      let version = '';
      try { version = req(path.join(path.dirname(entry), 'package.json')).version; } catch { /* keep empty */ }
      loadedFrom = cand;
      return { pw, version, entry, source: cand.name, base: cand.base };
    } catch (e) {
      if (e && e.code !== 'MODULE_NOT_FOUND') return { error: e };
    }
  }
  return null;
}
let loadedFrom = null;

export function requirePlaywright() {
  const r = loadPlaywright();
  if (!r) die('playwright is not installed', INSTALL_LINES);
  if (r.error) die(`playwright failed to load: ${String(r.error.message).split('\n')[0]}`, INSTALL_LINES);
  if (r.version && r.version !== PW_VERSION) say.warn(`playwright ${r.version} found in ${r.source}, ${PW_VERSION} is the tested version (npm i -D playwright@${PW_VERSION})`);
  return r.pw;
}

/** The command that downloads Chromium, matching where playwright was found. */
export function chromiumInstallFix() {
  const isGlobal = loadedFrom && loadedFrom.name !== 'current folder' && loadedFrom.name !== 'repo root';
  return isGlobal ? [`npx --prefix "${loadedFrom.base}" playwright install chromium`] : ['npx playwright install chromium'];
}

export async function launchChromium(pw, extra = {}) {
  try {
    return await pw.chromium.launch({ headless: true, args: ['--font-render-hinting=none', '--force-color-profile=srgb'], ...extra });
  } catch (e) {
    const msg = String(e && e.message ? e.message : e);
    if (/Executable doesn't exist|playwright install/i.test(msg)) die('Chromium is not installed for Playwright', chromiumInstallFix());
    if (/missing dependencies|shared librar|libnss|libatk/i.test(msg)) die('Chromium cannot start: system libraries are missing', 'Linux: sudo npx playwright install-deps chromium');
    die(`Chromium failed to start: ${msg.split('\n')[0]}`, 'node doctor.mjs');
  }
}

/** New context and page. Reduced motion is on so the engine draws everything at once. */
export async function openPage(browser, { width = 1920, height = 1080, scale, mobile = false, media } = {}) {
  const context = await browser.newContext({
    viewport: { width, height },
    deviceScaleFactor: scale || (mobile ? 2 : 1),
    isMobile: mobile, hasTouch: mobile,
    reducedMotion: 'reduce', locale: 'en-US', colorScheme: 'light',
  });
  const page = await context.newPage();
  page.setDefaultTimeout(30000);
  if (media) await page.emulateMedia({ media });
  return { context, page };
}

export function prettyUrl(u) {
  if (/^file:/i.test(u)) { try { return rel(fileURLToPath(u.split('?')[0].split('#')[0])); } catch { return u; } }
  return u.length > 90 ? `${u.slice(0, 87)}...` : u;
}

/** Collect console errors, uncaught errors, failed requests and external requests. */
export function watchPage(page, state = { errors: new Map(), failed: new Map(), external: new Map() }) {
  const bump = (m, k) => m.set(k, (m.get(k) || 0) + 1);
  page.on('console', (msg) => {
    if (msg.type() !== 'error') return;
    const t = msg.text();
    if (/^Failed to load resource/i.test(t)) return; // reported by requestfailed with the URL
    bump(state.errors, t.split('\n')[0]);
  });
  page.on('pageerror', (e) => bump(state.errors, `uncaught: ${String(e && e.message ? e.message : e).split('\n')[0]}`));
  page.on('requestfailed', (req) => {
    const err = (req.failure() && req.failure().errorText) || 'failed';
    bump(state.failed, `${prettyUrl(req.url())} (${err})`);
  });
  page.on('response', (res) => { if (res.status() >= 400) bump(state.failed, `${prettyUrl(res.url())} (HTTP ${res.status()})`); });
  page.on('request', (req) => { const u = req.url(); if (!/^(file|data|blob|about):/i.test(u)) bump(state.external, u); });
  return state;
}

/** Wait for fonts, the deck runtime (if any), two frames, and finish running animations. */
export async function waitReady(page, ms = 15000) {
  const result = await page.evaluate(async (limit) => {
    const timeout = new Promise((r) => setTimeout(() => r('timeout'), limit));
    const work = (async () => {
      if (document.fonts && document.fonts.ready) await document.fonts.ready;
      if (window.SketchyDeck && window.SketchyDeck.ready) await window.SketchyDeck.ready;
      await new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)));
      for (const a of document.getAnimations()) {
        try { const t = a.effect.getComputedTiming(); if (Number.isFinite(t.endTime)) a.finish(); } catch { /* ignore */ }
      }
      return 'ok';
    })();
    return Promise.race([work, timeout]);
  }, ms);
  return result === 'ok';
}

export const isDeckPage = (page) => page.evaluate(() => Boolean(document.querySelector('main.sk-deck')));
export const slideCount = (page) => page.evaluate(() => document.querySelectorAll('main.sk-deck .sk-slide').length);
