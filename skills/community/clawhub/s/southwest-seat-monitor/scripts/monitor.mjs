#!/usr/bin/env node
// Southwest seat monitor — reference implementation for the southwest-seat-monitor skill.
// READ-ONLY. Never submits a seat change.
//
// Alerts route to the AGENT session (configurable). The agent relays to the human as needed.
//
// Prereqs:
//   - patchright installed (`npm i patchright`)
//   - a real Chrome (`google-chrome-stable`) running with a PERSISTENT, already-logged-in profile,
//     exposing a CDP port (default 9222). See ../../seat-monitor/SKILL.md for the method.
//
// Usage:
//   node monitor.mjs --once     # single check, print result, exit
//   node monitor.mjs            # loop with randomized intervals, waking hours only
//
// Config via env (all optional):
//   SW_STATE, SW_CDP, SW_WINDOW_COLUMNS, SW_DAILY_CAP, SW_WAKE_START, SW_WAKE_END,
//   SW_MIN_MIN, SW_MAX_MIN, SW_TIGHT_MIN_MIN, SW_TIGHT_MIN_MAX, SW_FLIGHT_DEP,
//   SW_TARGET_LABEL, SW_TARGET_AIRPORT, SW_AGENT_SESSION
import fs from 'node:fs';
import path from 'node:path';
import { execFile } from 'node:child_process';

const STATE = process.env.SW_STATE || path.join(process.env.HOME || '.', '.sw-seat-monitor');
const OUT = path.join(STATE, 'out');
const LOG = path.join(STATE, 'monitor.log');
const SEEN = path.join(STATE, 'alerted-seats.json');
const HEALTH = path.join(STATE, 'health.json');
const CDP = process.env.SW_CDP || 'http://127.0.0.1:9222';
fs.mkdirSync(OUT, { recursive: true });

// ---- config ----
const TARGET_LABEL = process.env.SW_TARGET_LABEL || 'FLIGHT 2 of 2';  // segment button pattern
const TARGET_AIRPORT = process.env.SW_TARGET_AIRPORT || process.env.SW_TARGET_DEST || '';
const WINDOW_COLUMNS = (process.env.SW_WINDOW_COLUMNS || 'A,F').split(',');
const DAILY_CAP = +(process.env.SW_DAILY_CAP || 60);
const WAKE_START = +(process.env.SW_WAKE_START || 7), WAKE_END = +(process.env.SW_WAKE_END || 23);
const MIN_MIN = +(process.env.SW_MIN_MIN || 8), MAX_MIN = +(process.env.SW_MAX_MIN || 18);
const TIGHT_MIN_MIN = +(process.env.SW_TIGHT_MIN_MIN || 3), TIGHT_MIN_MAX = +(process.env.SW_TIGHT_MIN_MAX || 5);
const FLIGHT_DEP = process.env.SW_FLIGHT_DEP || '';   // ISO e.g. 2026-10-22T15:20:00-04:00
const TZ = process.env.SW_TZ || 'America/Los_Angeles';
const AGENT_SESSION = process.env.SW_AGENT_SESSION || '';

const sleep = ms => new Promise(r => setTimeout(r, ms));
const log = m => { const l = `[${new Date().toISOString()}] ${m}`; console.log(l); try { fs.appendFileSync(LOG, l + '\n'); } catch {} };
const nowLocal = () => new Date(new Date().toLocaleString('en-US', { timeZone: TZ }));
const inWake = () => { const h = nowLocal().getHours(); return h >= WAKE_START && h < WAKE_END; };
const hoursToFlight = () => FLIGHT_DEP ? (new Date(FLIGHT_DEP) - Date.now()) / 3600000 : Infinity;
const dayKey = () => nowLocal().toISOString().slice(0, 10);
const rd = f => { try { return JSON.parse(fs.readFileSync(f, 'utf8')); } catch { return {}; } };
const loadSeen = () => rd(SEEN);
const saveSeen = o => fs.writeFileSync(SEEN, JSON.stringify(o, null, 2));
const bump = () => { const f = path.join(STATE, 'counter.json'); const c = rd(f); c[dayKey()] = (c[dayKey()] || 0) + 1; fs.writeFileSync(f, JSON.stringify(c, null, 2)); return c[dayKey()]; };
const underCap = () => (rd(path.join(STATE, 'counter.json'))[dayKey()] || 0) < DAILY_CAP;
const pause = (a, b) => sleep(a + Math.random() * (b - a));
const readHealth = () => rd(HEALTH);
const writeHealth = h => fs.writeFileSync(HEALTH, JSON.stringify(h, null, 2));

// Alerts go to the agent session; the agent decides whether to ping the human.
function alertAgent(msg) {
  if (!AGENT_SESSION) { log('ALERT (no SW_AGENT_SESSION set): ' + msg.replace(/\n/g, ' | ')); return Promise.resolve(); }
  return new Promise(res => {
    execFile('openclaw', ['message', 'send', '--to', AGENT_SESSION, '--text', msg], e => {
      if (e) log('agent alert failed: ' + e.message); else log('agent alert sent');
      res();
    });
  });
}

async function signedOut(page) {
  const txt = await page.evaluate(() => (document.body.innerText || '').slice(0, 4000)).catch(() => '');
  return /sign in|log in|username|password/i.test(txt) && !/upcoming trip|my account|rapid rewards/i.test(txt);
}

async function checkOnce(page) {
  await page.goto('https://www.southwest.com/loyalty/myaccount/', { waitUntil: 'domcontentloaded', timeout: 45000 }).catch(() => {});
  await pause(4000, 6500);
  if (await signedOut(page)) { log('SESSION HEALTH: signed out'); return { ok: false, reason: 'signed-out' }; }

  let dh = null;
  for (let i = 0; i < 10 && !dh; i++) {
    dh = await page.$$eval('a', as => { const a = as.find(x => (x.innerText || '').trim() === 'Details'); return a ? a.getAttribute('href') : null; }).catch(() => null);
    if (!dh) await sleep(1500);
  }
  if (!dh) return { ok: false, reason: 'no-details' };
  await page.goto('https://www.southwest.com' + dh, { waitUntil: 'domcontentloaded', timeout: 45000 }).catch(() => {});

  let href = null;
  for (let i = 0; i < 14 && !href; i++) {
    href = await page.$$eval('a', as => { const a = as.find(x => /Upgrade or modify seats/i.test((x.innerText || '').trim())); return a ? a.getAttribute('href') : null; }).catch(() => null);
    if (!href) href = await page.$$eval('a', as => { const a = as.find(x => /select-seats/.test(x.getAttribute('href') || '')); return a ? a.getAttribute('href') : null; }).catch(() => null);
    if (!href) await sleep(1500);
  }
  if (!href) return { ok: false, reason: 'no-seat-link' };
  await page.goto('https://www.southwest.com' + href, { waitUntil: 'domcontentloaded', timeout: 45000 }).catch(() => {});

  let rendered = false;
  for (let i = 0; i < 16 && !rendered; i++) {
    rendered = await page.evaluate(() => document.querySelectorAll('button[aria-label*="Seat "]').length > 0).catch(() => false);
    if (!rendered) await sleep(1500);
  }
  await pause(1200, 2500);

  const sre = new RegExp(TARGET_LABEL.replace(/\s+/g, '\\s*'), 'i').source;
  const sw = await page.evaluate(({ sre, ap }) => {
    const re = new RegExp(sre, 'i');
    for (const e of document.querySelectorAll('button')) {
      const t = (e.innerText || '').replace(/\s+/g, ' ').trim();
      if (re.test(t) && (!ap || new RegExp(ap, 'i').test(t))) { e.click(); return t.slice(0, 60); }
    }
    return null;
  }, { sre, ap: TARGET_AIRPORT }).catch(() => null);
  log('segment switch: ' + (sw || 'NOT FOUND'));
  await pause(7000, 10000);

  const seats = await page.evaluate(() => {
    const out = [];
    for (const e of document.querySelectorAll('button')) {
      const lab = (e.getAttribute('aria-label') || '').replace(/\s+/g, ' ').trim();
      const m = lab.match(/Seat\s+([0-9]{1,2}[A-F])/i);
      if (!m) continue;
      const dis = e.disabled || e.getAttribute('aria-disabled') === 'true' || /disabled/i.test((e.className || '').toString());
      out.push({ seat: m[1].toUpperCase(), window: /window/i.test(lab), dis, lab: lab.slice(0, 160) });
    }
    return out;
  }).catch(() => []);

  if (!seats.length) return { ok: false, reason: 'no-seats' };

  const windows = seats.filter(s => WINDOW_COLUMNS.includes(s.seat.slice(-1)) || s.window);
  const openWindows = windows.filter(s => !s.dis);
  const openAny = seats.filter(s => !s.dis);
  log(`seats=${seats.length} windows=${windows.length} openWindows=${openWindows.length} openAny=${openAny.length}`);
  fs.writeFileSync(path.join(OUT, 'latest-seats.json'), JSON.stringify(seats, null, 2));
  return { ok: true, sw, seats, windows, openWindows, openAny };
}

// ---- main ----
const ONCE = process.argv.slice(2).includes('--once');
const { chromium } = await import('patchright');

const browser = await chromium.connectOverCDP(CDP);
const ctx = browser.contexts()[0];
let page = ctx.pages().find(p => /select-seats/.test(p.url())) || ctx.pages().find(p => /southwest\.com/i.test(p.url()));
if (!page) page = await ctx.newPage();

function recordOutcome(ok) {
  const h = readHealth();
  h.consecutiveFails = ok ? 0 : (h.consecutiveFails || 0) + 1;
  h.lastRun = new Date().toISOString();
  h.lastOk = ok;
  writeHealth(h);
  return h;
}

if (ONCE) {
  const r = await checkOnce(page);
  recordOutcome(r.ok);
  log('once-result: ' + JSON.stringify({ ok: r.ok, reason: r.reason, sw: r.sw, openWindows: (r.openWindows || []).map(s => s.seat) }));
  await browser.close().catch(() => {});
  process.exit(0);
}

log('=== southwest seat monitor start (agent-alerting) ===');
let hs = readHealth();
if ((hs.consecutiveFails || 0) >= 3 && !hs.alertedFails) {
  await alertAgent(`⚠️ Southwest seat monitor: session looks broken (${hs.consecutiveFails} consecutive failures). Likely needs a re-login.`);
  hs.alertedFails = true; writeHealth(hs);
}

for (;;) {
  if (!underCap()) { log('daily cap — sleep 1h'); await sleep(3600e3); continue; }
  if (!inWake()) { log('outside waking hours — sleep 30m'); await sleep(1800e3); continue; }
  const n = bump(); const h = hoursToFlight(); const tight = h > 0 && h <= 24;
  const label = FLIGHT_DEP ? `MCO→LAS` : 'target segment';
  try {
    const r = await checkOnce(page);
    const s = recordOutcome(r.ok);
    if (!r.ok && ['signed-out', 'no-details', 'no-seat-link'].includes(r.reason) && s.consecutiveFails >= 3 && !s.alertedFails) {
      await alertAgent(`⚠️ Southwest monitor needs attention: ${r.reason} (${s.consecutiveFails}x). Session may need re-login.`);
      s.alertedFails = true; writeHealth(s);
    }
    if (r.ok && s.alertedFails) { s.alertedFails = false; writeHealth(s); }
    if (r.ok) {
      const seen = loadSeen(); const fresh = [];
      for (const x of r.openWindows) { if (!seen[x.seat]) { fresh.push(x.seat); seen[x.seat] = new Date().toISOString(); } }
      saveSeen(seen);
      if (fresh.length) await alertAgent(`🪟 WINDOW SEAT OPEN on ${label}: ${fresh.join(', ')}. Seat map: https://www.southwest.com/air/seat/select-seats — relay to the user.`);
      else log('no new windows');
    }
    log(`poll #${n} done (${tight ? 'tight' : 'normal'}) hToFlight=${h === Infinity ? 'n/a' : h.toFixed(1)}`);
  } catch (e) { log('check error: ' + (e && e.message)); recordOutcome(false); }
  const lo = tight ? TIGHT_MIN_MIN : MIN_MIN, hi = tight ? TIGHT_MIN_MAX : MAX_MIN;
  const w = lo + Math.random() * (hi - lo); log(`next in ${w.toFixed(1)} min`); await sleep(w * 60e3);
}
