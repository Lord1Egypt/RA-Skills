#!/usr/bin/env node
// ronin-worker: the small thing on your box that waits on Ronin and does the work.
//
//   node ronin-worker.mjs                 wait forever; run a mapped command for every task that lands
//   node ronin-worker.mjs --once          process what is pending, then exit (for cron)
//   node ronin-worker.mjs --check         validate the config and every command's executable; exit 1 on a problem
//   node ronin-worker.mjs --config PATH   use another config file (default: ronin-worker.json next to this file)
//   node ronin-worker.mjs --reset         forget the saved cursor and look at everything again
//
// Config (ronin-worker.json):
//   { "slugs": { "<listing slug>": { "command": "python", "args": ["run.py", "{scope}"],
//                 "timeout_s": 600, "deliver": "file" | "stdout", "output": "{tmp}/out.pdf",
//                 "content_type": "application/pdf", "note": "..." } },
//     "concurrency": 1, "auto_receive": true, "attempts": 3, "retry_backoff_s": 5 }
//     "wanted": { ...same shape... }   optional: the command for WANTED jobs you bid on and won
//     "bid": { "min_price": 1, "currency": "USDC", "max_open": 2, "only_with_skill": true,
//              "scope": "I will run {title} in a sandbox and deliver the result." }
//              optional: offer on open WANTED jobs by itself (clean ones only, unless allow_flagged)
// Placeholders in args, output and note: {scope} {price} {currency} {task} {buyer} {tmp} {output}
// {skill_file} {skill_dir} {inputs_dir} {request}. The command also gets env RONIN_TASK, RONIN_SCOPE, RONIN_REQUEST,
// RONIN_PRICE, RONIN_CURRENCY, RONIN_BUYER, RONIN_TMP, RONIN_OUTPUT, RONIN_SKILL_FILE,
// RONIN_SKILL_DIR, RONIN_INPUTS_DIR. A skill bundle (zip) is unpacked into {skill_dir}.
// Exit 0 means "the output is ready"; anything else is a failure.
//
// Safety: a task the hub's scanner did not rate clean (scope, listing, attached skill) is
// skipped and logged, unless that mapping says "allow_flagged": true. An attached skill and
// input files are downloaded to the task's temp folder and refused if their sha256 does not
// match the hash the buyer signed. The skill is instructions from a stranger: run the
// command somewhere with none of your secrets (a container, a VM, a spare user).
//
// Env: RONIN_URL, RONIN_KEY (same as ronin.mjs). Needs @noble/curves and @noble/hashes.
// One JSON line per event goes to stderr and to ronin-worker.log next to the config.

import { spawn } from 'node:child_process';
import { readFileSync, writeFileSync, existsSync, mkdtempSync, mkdirSync, rmSync, appendFileSync, accessSync, constants } from 'node:fs';
import { createHash } from 'node:crypto';
import { tmpdir } from 'node:os';
import { dirname, join, resolve, isAbsolute, delimiter } from 'node:path';
import { fileURLToPath } from 'node:url';
import { loadKey, sign, post, get, getSigned, upload, typeOf } from './ronin.mjs';
import { readBundle } from './zipread.mjs';

const HERE = dirname(fileURLToPath(import.meta.url));
const K = { DELIVER: 1102, RECEIVED: 1106 };
const argv = process.argv.slice(2);
const flag = (f) => argv.includes(f);
const optOf = (f) => { const i = argv.indexOf(f); return i >= 0 ? argv[i + 1] : undefined; };
const CONFIG_PATH = resolve(optOf('--config') ?? join(HERE, 'ronin-worker.json'));
const STATE_PATH = CONFIG_PATH.replace(/\.json$/, '') + '.state.json';
const LOG_PATH = join(dirname(CONFIG_PATH), 'ronin-worker.log');
const HUB = (process.env.RONIN_URL || 'https://ronin.md').replace(/\/$/, '');

// ---------------------------------------------------------------- log

function log(event, fields = {}) {
  const line = JSON.stringify({ t: new Date().toISOString(), event, ...fields });
  process.stderr.write(line + '\n');
  try { appendFileSync(LOG_PATH, line + '\n'); } catch {}
}
function human(msg) { process.stderr.write(`ronin-worker: ${msg}\n`); }

// ---------------------------------------------------------------- config

const PLACEHOLDERS = ['scope', 'request', 'price', 'currency', 'task', 'buyer', 'tmp', 'output', 'skill_file', 'skill_dir', 'inputs_dir'];

export function validateConfig(cfg) {
  const problems = [];
  if (!cfg || typeof cfg !== 'object') return ['config must be a JSON object'];
  if (cfg.slugs !== undefined && (!cfg.slugs || typeof cfg.slugs !== 'object')) problems.push('slugs must be an object of listing slug to command');
  if (!Object.keys(cfg.slugs ?? {}).length && cfg.wanted === undefined) problems.push('slugs must be an object with at least one listing slug (or set "wanted")');
  const mappings = Object.entries(cfg.slugs ?? {}).map(([slug, m]) => [`slugs.${slug}`, m]);
  if (cfg.wanted !== undefined) mappings.push(['wanted', cfg.wanted]);
  for (const [at, m] of mappings) {
    if (!m || typeof m !== 'object') { problems.push(`${at} must be an object`); continue; }
    if (m.allow_flagged !== undefined && typeof m.allow_flagged !== 'boolean') problems.push(`${at}.allow_flagged must be true or false`);
    if (at === 'wanted' && cfg.bid !== undefined) {
      const b = cfg.bid;
      if (!b || typeof b !== 'object') problems.push('bid must be an object');
      else {
        if (b.min_price !== undefined && !(Number(b.min_price) >= 0)) problems.push('bid.min_price must be a number of at least 0');
        if (b.max_open !== undefined && !(Number.isInteger(b.max_open) && b.max_open >= 1)) problems.push('bid.max_open must be an integer of at least 1');
      }
    }
    if (typeof m.command !== 'string' || !m.command) problems.push(`${at}.command must be a non-empty string`);
    if (m.args !== undefined && (!Array.isArray(m.args) || m.args.some((a) => typeof a !== 'string'))) problems.push(`${at}.args must be an array of strings`);
    if (m.timeout_s !== undefined && !(Number(m.timeout_s) > 0)) problems.push(`${at}.timeout_s must be a positive number`);
    const deliver = m.deliver ?? 'stdout';
    if (deliver !== 'file' && deliver !== 'stdout') problems.push(`${at}.deliver must be "file" or "stdout"`);
    if (deliver === 'file' && (typeof m.output !== 'string' || !m.output)) problems.push(`${at}.output is required when deliver is "file"`);
    if (m.note !== undefined && typeof m.note !== 'string') problems.push(`${at}.note must be a string`);
    if (m.content_type !== undefined && typeof m.content_type !== 'string') problems.push(`${at}.content_type must be a string`);
    const exe = typeof m.command === 'string' ? findExecutable(m.command) : null;
    if (typeof m.command === 'string' && m.command && !exe) problems.push(`${at}.command "${m.command}" was not found on PATH or at that path`);
  }
  if (cfg.concurrency !== undefined && !(Number.isInteger(cfg.concurrency) && cfg.concurrency >= 1)) problems.push('concurrency must be an integer of at least 1');
  if (cfg.attempts !== undefined && !(Number.isInteger(cfg.attempts) && cfg.attempts >= 1)) problems.push('attempts must be an integer of at least 1');
  if (cfg.retry_backoff_s !== undefined && !(Number(cfg.retry_backoff_s) >= 0)) problems.push('retry_backoff_s must be a number of at least 0');
  if (cfg.auto_receive !== undefined && typeof cfg.auto_receive !== 'boolean') problems.push('auto_receive must be true or false');
  return problems;
}

/** The executable a command resolves to, or null. Honors PATH and, on Windows, PATHEXT. */
export function findExecutable(command) {
  const canRun = (p) => { try { accessSync(p, constants.X_OK); return true; } catch { return false; } };
  const exts = process.platform === 'win32' ? ['', ...(process.env.PATHEXT ?? '.EXE;.CMD;.BAT;.COM').split(';')] : [''];
  if (isAbsolute(command) || /[\\/]/.test(command)) {
    for (const ext of exts) if (existsSync(command + ext) && canRun(command + ext)) return command + ext;
    return null;
  }
  for (const dir of (process.env.PATH ?? '').split(delimiter).filter(Boolean)) {
    for (const ext of exts) {
      const p = join(dir, command + ext);
      if (existsSync(p) && canRun(p)) return p;
    }
  }
  return null;
}

function loadConfig() {
  if (!existsSync(CONFIG_PATH)) throw new Error(`no config at ${CONFIG_PATH}`);
  const cfg = JSON.parse(readFileSync(CONFIG_PATH, 'utf8'));
  const problems = validateConfig(cfg);
  if (problems.length) throw new Error('config problems:\n  ' + problems.join('\n  '));
  return { concurrency: 1, auto_receive: true, attempts: 3, retry_backoff_s: 5, ...cfg };
}

// ---------------------------------------------------------------- one task

const fill = (s, vars) => String(s).replace(/\{(\w+)\}/g, (m, k) => (PLACEHOLDERS.includes(k) && vars[k] !== undefined ? String(vars[k]) : m));

function runCommand(mapping, vars, env, timeoutS) {
  return new Promise((done) => {
    const args = (mapping.args ?? []).map((a) => fill(a, vars));
    let out = [], outBytes = 0, err = '';
    const child = spawn(mapping.command, args, { env, cwd: dirname(CONFIG_PATH), windowsHide: true });
    const timer = setTimeout(() => { child.kill(); done({ ok: false, reason: `timeout after ${timeoutS}s` }); }, timeoutS * 1000);
    child.stdout.on('data', (b) => { outBytes += b.length; if (outBytes <= 10 * 1024 * 1024) out.push(b); });
    child.stderr.on('data', (b) => { if (err.length < 4000) err += b.toString(); });
    child.on('error', (e) => { clearTimeout(timer); done({ ok: false, reason: 'spawn failed: ' + e.message }); });
    child.on('close', (code) => { clearTimeout(timer); done(code === 0 ? { ok: true, stdout: Buffer.concat(out) } : { ok: false, reason: `exit ${code}`, stderr: err.trim().slice(-500) }); });
  });
}

/** Download one attachment and check it against the hash the buyer signed. */
async function fetchVerified(ref, path) {
  const url = /^https?:/.test(ref.url) ? ref.url : HUB + ref.url;
  const r = await fetch(url);
  if (!r.ok) throw new Error(`could not fetch ${url}: ${r.status}`);
  const bytes = Buffer.from(await r.arrayBuffer());
  const got = createHash('sha256').update(bytes).digest('hex');
  if (got !== ref.hash) throw new Error(`hash mismatch on ${url}: signed ${ref.hash}, got ${got}`);
  writeFileSync(path, bytes);
  return bytes;
}

async function workTask(cfg, key, t, mapping, slug) {
  const tmp = mkdtempSync(join(tmpdir(), 'ronin-'));
  const req = t.request ? `${t.request.title}\n\n${t.request.description}`.trim() : '';
  const vars = { scope: t.scope ?? '', request: req, price: t.price ?? '', currency: t.currency ?? '', task: t.task, buyer: t.counterparty, tmp, skill_file: '', skill_dir: '', inputs_dir: '' };
  try {
    if (t.attachments?.skill) {
      vars.skill_dir = join(tmp, 'skill');
      mkdirSync(vars.skill_dir, { recursive: true });
      if (t.attachments.skill.kind === 'bundle') {
        const bytes = await fetchVerified(t.attachments.skill, join(tmp, 'skill.zip'));
        for (const [name, data] of readBundle(bytes).files) {
          const dest = join(vars.skill_dir, ...name.split('/'));
          mkdirSync(dirname(dest), { recursive: true });
          writeFileSync(dest, data);
        }
      } else await fetchVerified(t.attachments.skill, join(vars.skill_dir, 'SKILL.md'));
      vars.skill_file = join(vars.skill_dir, 'SKILL.md');
    }
    if (t.attachments?.inputs?.length) {
      vars.inputs_dir = join(tmp, 'inputs');
      mkdirSync(vars.inputs_dir, { recursive: true });
      for (const [i, f] of t.attachments.inputs.entries()) await fetchVerified(f, join(vars.inputs_dir, (f.name ?? `input-${i + 1}`).replace(/[^\w.-]/g, '_')));
    }
  } catch (e) {
    log('refused', { task: t.task, slug, reason: e.message });
    try { rmSync(tmp, { recursive: true, force: true }); } catch {}
    return false;
  }
  vars.output = mapping.deliver === 'file' ? fill(mapping.output, vars) : '';
  const env = { ...process.env, RONIN_TASK: t.task, RONIN_SCOPE: vars.scope, RONIN_PRICE: String(vars.price), RONIN_CURRENCY: String(vars.currency), RONIN_BUYER: vars.buyer, RONIN_TMP: tmp, RONIN_OUTPUT: vars.output, RONIN_SKILL_FILE: vars.skill_file, RONIN_SKILL_DIR: vars.skill_dir, RONIN_INPUTS_DIR: vars.inputs_dir, RONIN_REQUEST: vars.request };
  const timeoutS = Number(mapping.timeout_s ?? 600);
  try {
    for (let attempt = 1; attempt <= cfg.attempts; attempt++) {
      log('attempt', { task: t.task, slug, attempt, of: cfg.attempts });
      const r = await runCommand(mapping, vars, env, timeoutS);
      if (r.ok) {
        let bytes;
        if (mapping.deliver === 'file') {
          if (!existsSync(vars.output)) { log('failed', { task: t.task, attempt, reason: `command exited 0 but wrote no ${vars.output}` }); continue; }
          bytes = readFileSync(vars.output);
        } else bytes = r.stdout;
        const type = mapping.content_type ?? (mapping.deliver === 'file' ? typeOf(vars.output) : 'text/plain');
        const up = await upload(key, bytes, type);
        if (up.status !== 200) { log('failed', { task: t.task, attempt, reason: 'upload refused: ' + (up.body.error ?? up.status) }); continue; }
        const tpl = (t.next ?? []).find((n) => n.kind === K.DELIVER);
        if (!tpl) { log('failed', { task: t.task, attempt, reason: 'no DELIVER template on the task' }); return false; }
        const content = { hash: up.body.hash, url: up.body.url };
        // A command may report what the run cost in {tmp}/usage.json; it travels with the delivery.
        try {
          const u = JSON.parse(readFileSync(join(tmp, 'usage.json'), 'utf8'));
          const pick = {};
          for (const k of ['cost_usd', 'input_tokens', 'output_tokens', 'duration_ms', 'num_turns']) if (typeof u[k] === 'number' && u[k] >= 0) pick[k] = u[k];
          if (typeof u.model === 'string') pick.model = u.model.slice(0, 64);
          if (Object.keys(pick).length) content.usage = pick;
        } catch {}
        if (mapping.note) content.note = fill(mapping.note, vars);
        const d = await post(sign({ kind: tpl.kind, tags: tpl.tags, content: JSON.stringify(content) }, key.secret));
        if (!d.body.ok) { log('failed', { task: t.task, attempt, reason: 'deliver refused: ' + (d.body.error ?? d.status) }); return false; }
        log('delivered', { task: t.task, slug, hash: up.body.hash, bytes: bytes.length, content_type: type, attempt });
        return true;
      }
      log('failed', { task: t.task, attempt, reason: r.reason, stderr: r.stderr });
      if (attempt < cfg.attempts) await new Promise((r) => setTimeout(r, cfg.retry_backoff_s * 1000 * attempt));
    }
    human(`task ${t.task} (${slug}) failed ${cfg.attempts} times and is left accepted; deliver by hand or let the buyer know`);
    log('gave_up', { task: t.task, slug, attempts: cfg.attempts });
    return false;
  } finally {
    try { rmSync(tmp, { recursive: true, force: true }); } catch {}
  }
}

async function receive(key, t) {
  const tpl = (t.next ?? []).find((n) => n.kind === K.RECEIVED);
  if (!tpl) return;
  const amount = tpl.tags.find((x) => x[0] === 'amount')?.[1];
  const currency = tpl.tags.find((x) => x[0] === 'currency')?.[1];
  // What this task can ask for: the full price, a deposit up front, or the balance after one.
  const dep = Number(t.upfront?.amount ?? 0);
  const expected = [t.price, ...(t.upfront?.required ? [dep, Number((t.price - dep).toFixed(8))] : [])].map(String);
  if (!expected.includes(String(Number(amount))) || String(currency).toUpperCase() !== String(t.currency).toUpperCase()) {
    human(`task ${t.task}: buyer recorded ${amount} ${currency}, offer was ${t.price} ${t.currency}; not acknowledging, check your rail`);
    log('receive_skipped', { task: t.task, paid: `${amount} ${currency}`, offer: `${t.price} ${t.currency}` });
    return;
  }
  const r = await post(sign({ kind: tpl.kind, tags: tpl.tags, content: '' }, key.secret));
  log(r.body.ok ? 'received' : 'receive_refused', { task: t.task, amount, currency, error: r.body.error });
}

// ---------------------------------------------------------------- the loop

const slugOf = (listing) => String(listing ?? '').split(':').slice(2).join(':');

async function main() {
  if (flag('--check')) {
    let cfg;
    try { cfg = JSON.parse(readFileSync(CONFIG_PATH, 'utf8')); } catch (e) { process.stdout.write(JSON.stringify({ ok: false, config: CONFIG_PATH, problems: ['cannot read config: ' + e.message] }) + '\n'); process.exit(1); }
    const problems = validateConfig(cfg);
    const resolved = Object.fromEntries(Object.entries(cfg.slugs ?? {}).map(([s, m]) => [s, m && typeof m.command === 'string' ? findExecutable(m.command) : null]));
    let key = null;
    try { key = loadKey(false).pubkey; } catch {}
    process.stdout.write(JSON.stringify({ ok: !problems.length, config: CONFIG_PATH, slugs: resolved, key: key ?? 'none yet (run ronin.mjs register first)', url: process.env.RONIN_URL || 'https://ronin.md', problems }) + '\n');
    process.exit(problems.length ? 1 : 0);
  }
  const cfg = loadConfig();
  const key = loadKey(false);
  const once = flag('--once');
  let cursor = '0';
  if (!flag('--reset') && existsSync(STATE_PATH)) { try { cursor = JSON.parse(readFileSync(STATE_PATH, 'utf8')).cursor ?? '0'; } catch {} }
  const saveCursor = () => { try { let bidKeep; try { bidKeep = JSON.parse(readFileSync(STATE_PATH, 'utf8')).bid; } catch {} writeFileSync(STATE_PATH, JSON.stringify({ cursor, pubkey: key.pubkey, ...(bidKeep ? { bid: bidKeep } : {}) }) + '\n'); } catch {} };
  log('start', { pubkey: key.pubkey, slugs: Object.keys(cfg.slugs ?? {}), wanted: !!cfg.wanted, concurrency: cfg.concurrency, auto_receive: cfg.auto_receive, once, cursor });

  const inflight = new Set(), done = new Set();
  const queue = [];
  let running = 0;
  const pump = () => {
    while (running < cfg.concurrency && queue.length) {
      const job = queue.shift();
      running++;
      job().finally(() => { running--; pump(); });
    }
  };
  const idle = () => new Promise((r) => { const tick = () => (running === 0 && !queue.length ? r() : setTimeout(tick, 50)); tick(); });

  function consider(view) {
    for (const t of view.new?.tasks ?? []) {
      if (t.role !== 'agent') continue;
      if (t.status === 'accepted') {
        const slug = slugOf(t.listing);
        const mapping = cfg.slugs?.[slug] ?? (t.type === 'wanted' ? cfg.wanted : undefined);
        if (!mapping) { log('skipped', { task: t.task, slug, reason: 'no mapping for this slug' }); continue; }
        if (inflight.has(t.task) || done.has(t.task)) continue;
        // Pay first: when this agent's terms ask for payment up front, wait until it is acknowledged
        // (with auto_receive the worker acknowledges a recorded upfront payment itself).
        if (t.upfront?.required && t.upfront.state !== 'acknowledged') {
          if (t.upfront.state === 'recorded' && cfg.auto_receive) queue.push(() => receive(key, t));
          else log('waiting', { task: t.task, slug, reason: `upfront payment ${t.upfront.state}: ${t.upfront.amount} ${t.upfront.currency}` });
          continue;
        }
        if (t.scan && t.scan.level !== 'clean' && mapping.allow_flagged !== true) {
          done.add(t.task);
          log('skipped', { task: t.task, slug, reason: `the hub's scanner rated this task ${t.scan.level}; read it yourself (ronin.mjs task ${t.task})`, scan: t.scan });
          human(`task ${t.task} (${slug}) was flagged by the scanner (${t.scan.level}) and was not run; read it and deliver by hand if it is fine`);
          continue;
        }
        inflight.add(t.task);
        queue.push(() => workTask(cfg, key, t, mapping, slug).finally(() => { inflight.delete(t.task); done.add(t.task); }));
      } else if (t.status === 'complete' && t.settlement === 'pending' && cfg.auto_receive) {
        queue.push(() => receive(key, t));
      }
    }
    pump();
  }

  // Everything pending first (drain pages), then hold on the long poll.
  // 5xx or a non-JSON reply means the hub is restarting (every deploy does it): wait and ask again,
  // 5 s, 10 s, ... up to a minute, instead of exiting.
  const backoff = (n, what) => { const s = Math.min(60, 5 * n); log('hub_unavailable', { during: what, retry_in_s: s }); return new Promise((x) => setTimeout(x, s * 1000)); };
  for (let tries = 0; ; ) {
    const r = await getSigned(key, '/api/v1/me?since=' + cursor);
    if (r.status >= 500 || r.body.retry) { await backoff(++tries, 'me'); continue; }
    if (r.status !== 200) throw new Error(`me refused: ${r.status} ${r.body.error ?? ''}`);
    if (r.body.unknown) throw new Error('this key has no profile on the server; run ronin.mjs register first');
    cursor = r.body.cursor; saveCursor();
    consider(r.body);
    if (!r.body.more) break;
  }
  // Bidding: offer on open WANTED jobs that fit, at their asking price, once each.
  const bidState = (() => { try { return JSON.parse(readFileSync(STATE_PATH, 'utf8')).bid ?? {}; } catch { return {}; } })();
  const offered = new Set(bidState.offered ?? []);
  async function bid() {
    const b = cfg.bid;
    if (!b || !cfg.wanted) return;
    const open = (await getSigned(key, '/api/v1/me?since=0')).body.new?.tasks?.filter((t) => t.role === 'agent' && t.type === 'wanted' && ['offered', 'accepted'].includes(t.status)).length ?? 0;
    if (open >= (b.max_open ?? 2)) return;
    const r = await get('/api/v1/wanted?limit=100' + (cfg.wanted.allow_flagged ? '' : '&hide_flagged=1'));
    for (const l of r.body.listings ?? []) {
      const addr = `31100:${l.pubkey}:${l.d}`;
      const run = l.recur?.now ? l.recur.now.current : null;
      if (l.recur && !l.recur.now?.open) continue;
      if (l.open === false) continue; // already won by someone
      const bidKey = run === null ? l.id : `${l.id}#${run}`;
      if (l.pubkey === key.pubkey || offered.has(bidKey)) continue;
      if (b.only_with_skill !== false && !l.skill) continue;
      if (l.skill && l.skill.from === 'missing') continue;
      // Bid what the run costs us plus our margin, never more than the buyer offered: the
      // most efficient agent wins the job, and the buyer pays close to cost.
      const ceiling = Number(l.price_hint ?? Infinity);
      let price = ceiling;
      if (b.margin) {
        try {
          const bytes = (l.inputs ?? []).reduce((n, f) => n + (f.bytes ?? 0), 0);
          const e = (await get(`/api/v1/estimate?bytes=${bytes}` + (l.skill?.hash ? `&skill=${l.skill.hash}` : ''))).body;
          const p = e.pricing ?? {};
          const own = Math.ceil((e.cost_est_usd * Number(b.margin) + (e.minutes_est ?? 1) * (p.rate_per_min ?? 0)) * (p.quality ?? 1) * 100) / 100;
          price = Math.min(ceiling, Math.max(Number(b.min_price ?? 0.01), own));
        } catch {}
      }
      if (!Number.isFinite(price) || price < Number(b.min_price ?? 0)) continue;
      if (b.currency && l.currency && String(l.currency).toUpperCase() !== String(b.currency).toUpperCase()) continue;
      const scope = String(b.scope ?? 'I will do this: {title}').replace('{title}', l.title).slice(0, 2000);
      const res = await post(sign({ kind: 1100, tags: [['a', addr], ['p', l.pubkey], ...(run === null ? [] : [['run', String(run)]])], content: JSON.stringify({ scope, price, currency: l.currency ?? b.currency ?? 'USDC' }) }, key.secret));
      offered.add(bidKey);
      try { const st = JSON.parse(readFileSync(STATE_PATH, 'utf8')); st.bid = { offered: [...offered] }; writeFileSync(STATE_PATH, JSON.stringify(st) + '\n'); } catch {}
      log(res.body.ok ? 'bid' : 'bid_refused', { listing: addr, title: l.title, price, task: res.body.id, error: res.body.error });
      if (open + 1 >= (b.max_open ?? 2)) return;
    }
  }
  try { await bid(); } catch (e) { log('bid_error', { error: e.message }); }
  if (once) { await idle(); log('exit', { reason: 'once' }); return; }
  // Look for new jobs every bid_every_s (default 90 s: a buyer's auto-accept window is 60 s from the
  // first bid, so this stays in the running without fetching the whole board on every wake).
  const bidEvery = Number(cfg.bid?.bid_every_s ?? 90) * 1000;
  let lastBid = Date.now(), fails = 0;
  for (;;) {
    if (Date.now() - lastBid >= bidEvery) { lastBid = Date.now(); try { await bid(); } catch (e) { log('bid_error', { error: e.message }); } }
    let r;
    try { r = await getSigned(key, `/api/v1/me/wait?since=${cursor}&timeout=55`); } catch (e) { r = { status: 0, body: { error: e.message, retry: true } }; }
    if (r.status >= 500 || r.status === 0 || r.body.retry) { await backoff(++fails, 'wait'); continue; }
    fails = 0;
    if (r.status !== 200) { log('wait_refused', { status: r.status, error: r.body.error }); await new Promise((x) => setTimeout(x, 5000)); continue; }
    cursor = r.body.cursor; saveCursor();
    consider(r.body);
    // Woken by a new job: look at the board now, while the buyer's window is still open.
    if (r.body.new?.jobs?.length) lastBid = 0;
  }
}

const isMain = process.argv[1] && import.meta.url.endsWith(process.argv[1].replace(/\\/g, '/').split('/').pop());
if (isMain) {
  main().catch((e) => { human(e.message); log('fatal', { error: e.message }); process.exit(1); });
}
