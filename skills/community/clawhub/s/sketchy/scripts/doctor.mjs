#!/usr/bin/env node
// doctor.mjs: check that the machine can run the sketchy scripts, and print the exact fix for each failure.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { pathToFileURL } from 'node:url';
import {
  parseArgs, say, c, rel, isMain, ENGINE_DIR, SKILL_DIR, PW_VERSION, INSTALL_LINES,
  loadPlaywright, playwrightCandidates, chromiumInstallFix, sketchyHome,
} from './_lib.mjs';

const spec = {
  name: 'sketchy doctor', file: 'doctor.mjs', usage: '',
  summary: 'check Node, Playwright and Chromium, FFmpeg, the skill fonts and write access; print the fix for each failure.',
  details: [
    'Core (must work): Node 18+, playwright, a Chromium that launches, the engine files and fonts, write access to this folder.',
    'Video (optional): FFmpeg on PATH, needed only by render-video.mjs. Missing FFmpeg is a warning, not a failure.',
    'Info only: your own themes and templates in ~/.sketchy and ./.sketchy.',
    'Exit 0 when the core works, 1 when it does not.',
  ],
  options: [],
  positionals: { min: 0, max: 0 },
  examples: ['node doctor.mjs'],
};

const results = { core: [], video: [] };
function report(group, level, msg, fix) {
  results[group].push(level);
  say[level](msg);
  if (fix && level !== 'ok') say.fix(fix);
}
const perOs = (win, mac, linux) => [`Windows: ${win}`, `macOS:   ${mac}`, `Linux:   ${linux}`];

function checkNode() {
  const v = process.versions.node;
  const major = Number(v.split('.')[0]);
  if (major >= 18) report('core', 'ok', `node ${v}`);
  else report('core', 'error', `node ${v} is too old, 18 or newer is needed`, perOs('winget install OpenJS.NodeJS.LTS', 'brew install node', 'nvm install --lts   (or your distro package for Node 18+)'));
}

function checkPlaywright() {
  const r = loadPlaywright();
  if (!r) {
    report('core', 'error', `playwright is not installed (looked in: ${playwrightCandidates().map((x) => x.name).join(', ')})`, INSTALL_LINES);
    return null;
  }
  if (r.error) { report('core', 'error', `playwright failed to load: ${String(r.error.message).split('\n')[0]}`, INSTALL_LINES); return null; }
  if (r.version === PW_VERSION) report('core', 'ok', `playwright ${r.version} (${r.source})`);
  else report('core', 'warn', `playwright ${r.version || '?'} found in ${r.source}, ${PW_VERSION} is the tested version`, `npm i -D playwright@${PW_VERSION}`);
  return r.pw;
}

async function checkChromium(pw) {
  if (!pw) { report('core', 'error', 'chromium not checked (playwright missing)'); return null; }
  try {
    const browser = await pw.chromium.launch({ headless: true });
    const page = await browser.newPage();
    await page.goto('about:blank');
    const ua = await page.evaluate(() => navigator.userAgent);
    report('core', 'ok', `chromium ${(/Chrome\/([\d.]+)/.exec(ua) || [])[1] || ''} launches`);
    return browser;
  } catch (e) {
    const msg = String(e && e.message ? e.message : e);
    if (/Executable doesn't exist|playwright install/i.test(msg)) report('core', 'error', 'chromium is not downloaded for playwright', chromiumInstallFix());
    else if (/missing dependencies|shared librar|libnss|libatk/i.test(msg)) report('core', 'error', 'chromium cannot start: system libraries are missing', ['Linux: sudo npx playwright install-deps chromium']);
    else report('core', 'error', `chromium failed to start: ${msg.split('\n')[0]}`, ['re-download it: npx playwright install chromium', 'on Linux also: sudo npx playwright install-deps chromium']);
    return null;
  }
}

async function checkEngine(browser) {
  const need = ['sketchy.css', 'sketchy.js'];
  const missing = need.filter((f) => !fs.existsSync(path.join(ENGINE_DIR, f)));
  if (missing.length) report('core', 'error', `engine files missing: ${missing.join(', ')}`, [`restore them from the repo: git checkout -- ${rel(ENGINE_DIR)}`, 'or reinstall the skill']);
  else report('core', 'ok', `engine files in ${rel(ENGINE_DIR)}`);
  const optional = ['sketchy-deck.js', 'sketches.js', 'sketchy-charts.js', 'sketchy-sound.js'].filter((f) => !fs.existsSync(path.join(ENGINE_DIR, f)));
  if (optional.length) say.info(`optional engine modules missing: ${optional.join(', ')}`);

  const fontsDir = path.join(ENGINE_DIR, 'fonts');
  const files = fs.existsSync(fontsDir) ? fs.readdirSync(fontsDir).filter((f) => f.endsWith('.woff2')) : [];
  const caveat = files.filter((f) => f.startsWith('Caveat')).length;
  const courier = files.filter((f) => f.startsWith('CourierPrime')).length;
  if (!caveat || !courier) {
    report('core', 'error', `skill fonts missing (Caveat ${caveat} files, Courier Prime ${courier} files in ${rel(fontsDir)})`, [`restore them: git checkout -- ${rel(fontsDir)}`, 'the fonts are SIL OFL 1.1; the originals are on Google Fonts (Caveat, Courier Prime)']);
    return;
  }
  report('core', 'ok', `fonts ${files.length} files (Caveat ${caveat}, Courier Prime ${courier})`);
  if (!browser || missing.length) return;
  // do the files decode, and does sketchy.css find them?
  const tmp = path.join(os.tmpdir(), `sketchy-doctor-${process.pid}.html`);
  try {
    fs.writeFileSync(tmp, `<!doctype html><meta charset="utf-8"><link rel="stylesheet" href="${pathToFileURL(path.join(ENGINE_DIR, 'sketchy.css')).href}"><p style="font-family:Caveat">Hello</p><p style="font-family:'Courier Prime';font-weight:700">Hello</p>`);
    const page = await browser.newPage();
    await page.goto(pathToFileURL(tmp).href);
    const status = await page.evaluate(async () => {
      await Promise.all([document.fonts.load('20px Caveat', 'Hello'), document.fonts.load('700 20px "Courier Prime"', 'Hello')]);
      return { caveat: document.fonts.check('20px Caveat', 'Hello'), courier: document.fonts.check('700 20px "Courier Prime"', 'Hello'), faces: Array.from(document.fonts).filter((f) => f.status === 'loaded').length };
    });
    if (status.caveat && status.courier && status.faces >= 2) report('core', 'ok', 'fonts decode and load in Chromium (Caveat, Courier Prime)');
    else report('core', 'error', `fonts do not load in Chromium (Caveat ${status.caveat}, Courier Prime ${status.courier})`, [`restore the files: git checkout -- ${rel(fontsDir)}`]);
    await page.close();
  } catch (e) {
    report('core', 'warn', `font load test failed: ${String(e.message).split('\n')[0]}`);
  } finally { try { fs.unlinkSync(tmp); } catch { /* ignore */ } }
}

function checkFfmpeg() {
  const run = (args) => spawnSync('ffmpeg', args, { encoding: 'utf8', windowsHide: true });
  const v = run(['-version']);
  if (v.error || v.status !== 0) {
    report('video', 'warn', 'ffmpeg not found on PATH (only render-video.mjs needs it)', perOs('winget install Gyan.FFmpeg   (then open a new terminal)', 'brew install ffmpeg', 'sudo apt install ffmpeg   (or your distro package)'));
    return;
  }
  const ver = (/ffmpeg version (\S+)/.exec(v.stdout) || [])[1] || '?';
  const enc = run(['-hide_banner', '-encoders']).stdout || '';
  const missing = ['libx264', 'aac'].filter((n) => !new RegExp(`\\b${n}\\b`).test(enc));
  if (missing.length) report('video', 'warn', `ffmpeg ${ver} has no ${missing.join(' or ')} encoder (needed for MP4 with sound)`, perOs('winget install Gyan.FFmpeg', 'brew install ffmpeg', 'sudo apt install ffmpeg'));
  else report('video', 'ok', `ffmpeg ${ver} (libx264, aac)`);
}

function checkWrite() {
  const probe = path.join(process.cwd(), `.sketchy-doctor-${process.pid}.tmp`);
  try { fs.writeFileSync(probe, 'ok'); fs.unlinkSync(probe); report('core', 'ok', `write access in ${process.cwd()}`); }
  catch (e) { report('core', 'error', `cannot write in ${process.cwd()} (${e.code || e.message})`, ['cd to a folder you can write to; the scripts create out/ and shots/ next to your HTML']); }
}

function checkUserFolders() {
  const countIn = (dir, ext) => (fs.existsSync(dir) ? fs.readdirSync(dir).filter((f) => f.endsWith(ext)).length : null);
  const describe = (label, base) => {
    if (!fs.existsSync(base)) { say.info(`${label} not present (optional: your own themes and templates go there)`); return; }
    const t = countIn(path.join(base, 'themes'), '.css'), h = countIn(path.join(base, 'templates'), '.html');
    say.info(`${label}: themes ${t === null ? 'no folder' : t}, templates ${h === null ? 'no folder' : h}`);
  };
  describe(process.env.SKETCHY_HOME ? '$SKETCHY_HOME' : '~/.sketchy', sketchyHome());
  describe('./.sketchy', path.join(process.cwd(), '.sketchy'));
}

async function main() {
  parseArgs(process.argv.slice(2), spec);
  say.line(c.bold(`sketchy doctor (${process.platform}, skill at ${SKILL_DIR})`));
  checkNode();
  const pw = checkPlaywright();
  const browser = await checkChromium(pw);
  try { await checkEngine(browser); } finally { if (browser) await browser.close(); }
  checkWrite();
  checkFfmpeg();
  checkUserFolders();

  const coreBad = results.core.filter((l) => l === 'error').length;
  const videoOk = results.video.length > 0 && results.video.every((l) => l === 'ok');
  say.line(coreBad === 0
    ? `core: ready. video: ${videoOk ? 'ready' : 'unavailable until ffmpeg works'}.`
    : `core: NOT ready (${coreBad} failure${coreBad === 1 ? '' : 's'}). Fix the lines marked error, then run doctor again.`);
  process.exit(coreBad === 0 ? 0 : 1);
}

if (isMain(import.meta.url)) main().catch((e) => { console.error(`error  doctor failed: ${String(e && e.message ? e.message : e).split('\n')[0]}`); process.exit(1); });
