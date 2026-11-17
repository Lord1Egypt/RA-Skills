#!/usr/bin/env node
// inference-proxy.js: a localhost OpenAI-compatible proxy that pays one Nano 402 door per call from
// the agent's own wallet, inside a cumulative cap the operator set before starting it.
//
//   NANO_SEED=<64 hex> NANO_CAP=0.1 UPSTREAM=https://nano-gpt.com/api/x402 node inference-proxy.js
//   then point the runtime at http://127.0.0.1:3402/v1 with PROXY_KEY as its API key (checked, then dropped here).
//
// What it does: every request to /v1/* is forwarded to UPSTREAM/v1/* unchanged. When the door answers
// 402, the proxy reads the quote, decides under a lock whether it may pay (door host bound at setup,
// amount within the per-call limit, cumulative spend within the cap, quote not expired, optional payTo
// allow-list), and only then signs a send block. Two 402 dialects are paid:
//   "nano"  (NanoGPT accountless): per-payment deposit account; the proxy broadcasts the send itself and
//           then POSTs the same body to the quote's completeUrl, which must be on the UPSTREAM host.
//   "exact" (x402 v2, nano:mainnet; @x402nano/exact, feeless402, pursekeeper.dev and most of the
//           sellers list): the signed block travels in PAYMENT-SIGNATURE and the seller broadcasts it.
// Anything else, and any check that fails, ends in a refusal to the runtime with nothing signed.
//
// Env: NANO_SEED (required), NANO_INDEX (default 0),
//      PROXY_KEY (required, 16+ characters; every /v1/* request must carry it as "Authorization: Bearer <key>"
//                 or "x-api-key: <key>", else 401 with nothing forwarded or signed; the proxy binds loopback,
//                 but loopback is shared with every process and every browser tab on the machine),
//      UPSTREAM (required; the one door this instance may pay, e.g. https://nano-gpt.com/api/x402),
//      NANO_CAP (required; cumulative cap in XNO as decimal text, over the life of the state file),
//      NANO_MAX_PER_CALL (default 0.001 XNO; a quote above it is refused),
//      NANO_ALLOW_PAYTO (optional comma-separated accounts; when set, a quote's payTo must be on it;
//                        NanoGPT issues a fresh account per payment, so leave it unset for that door),
//      STATE_FILE (default ~/.pursekeeper/inference-proxy-<port>.json; spent, received, every payment),
//      PORT (default 3402; the proxy binds 127.0.0.1 only),
//      NANO_RPC (optional node RPC; else the free endpoints at API, default https://pursekeeper.dev),
//      WORK_URL (optional RPC-style work_generate endpoint; else API /v1/work, else local CPU, slow),
//      RECEIVE (default 1: pocket refunds and other receivables before a paid call; 0 to skip).
// Every request must name a loopback Host (127.0.0.1, localhost, [::1]) and carry no Origin header, so a web page
// the operator's browser opens cannot reach the wallet by a no-preflight POST or by DNS rebinding (403).
// Endpoints: ANY /v1/* forwarded and paid; GET /_nano/state (same key) for the cap, spend and payment list
// (hashes only; the seed never leaves this process; the state file is mode 600). A signed send that did not
// land stays counted until a block is confirmed at its height; the proxy publishes a change block there itself. Streaming: stream:true is forwarded; the door's SSE is piped as it
// arrives (x-payer-stream: passthrough); a JSON answer to a stream request is wrapped as one SSE
// chunk plus [DONE] carrying the whole message, tool_calls included (x-payer-stream: buffered). Only dependency: nanocurrency (npm i nanocurrency).
//
// The allow-door mode, the single decision function that runs before any signing, and the
// x-payer-stream header are taken from llmrt's Python payer (xno_payer_proxy.py, 2026-10-08), with credit.
'use strict';
const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const os = require('node:os');
const N = require('nanocurrency');
const { createHash, timingSafeEqual } = require('node:crypto');

const RAW = 10n ** 30n;
const ZERO = '0'.repeat(64);
const toRaw = s => { const m = /^(\d+)(?:\.(\d{1,30}))?$/.exec(String(s ?? '').trim()); return m ? BigInt(m[1]) * RAW + BigInt((m[2] || '').padEnd(30, '0')) : null; };
const fmt = r => { r = BigInt(r); const w = r / RAW, f = (r % RAW).toString().padStart(30, '0').replace(/0+$/, ''); return w + (f ? '.' + f : ''); };
const b64 = s => Buffer.from(JSON.stringify(s)).toString('base64');
const unb64 = s => JSON.parse(Buffer.from(s, 'base64').toString('utf8'));
const sleep = ms => new Promise(s => setTimeout(s, ms));
const log = (...a) => console.error(new Date().toISOString(), ...a);

// ---- configuration, all read once; a missing control is a refusal to start, not a default ----
const cfg = (() => {
  const die = m => { console.error('inference-proxy: ' + m); process.exit(2); };
  if (!/^[0-9a-fA-F]{64}$/.test(process.env.NANO_SEED || '')) die('set NANO_SEED (64 hex characters)');
  const proxyKey = (process.env.PROXY_KEY || '').trim();
  if (proxyKey.length < 16) die('set PROXY_KEY (16+ characters, e.g. $(openssl rand -hex 16)); the runtime presents it as "Authorization: Bearer <key>" or "x-api-key: <key>", and nothing without it is forwarded or paid');
  const upstream = (process.env.UPSTREAM || '').replace(/\/+$/, '');
  let u; try { u = new URL(upstream); } catch { die('set UPSTREAM to the door this proxy may pay, e.g. https://nano-gpt.com/api/x402'); }
  if (u.protocol !== 'https:' && u.hostname !== '127.0.0.1' && u.hostname !== 'localhost') die('UPSTREAM must be https (or loopback for tests)');
  const cap = toRaw(process.env.NANO_CAP);
  if (cap === null || cap <= 0n) die('set NANO_CAP, the cumulative spending cap in XNO as decimal text (e.g. 0.1)');
  const perCall = toRaw(process.env.NANO_MAX_PER_CALL ?? '0.001');
  if (perCall === null || perCall <= 0n) die('NANO_MAX_PER_CALL must be a decimal XNO amount');
  const allow = (process.env.NANO_ALLOW_PAYTO || '').split(',').map(s => s.trim()).filter(Boolean);
  for (const a of allow) if (!N.checkAddress(a)) die('NANO_ALLOW_PAYTO: not a Nano address: ' + a);
  const port = Number(process.env.PORT || 3402);
  const keyHash = createHash('sha256').update(proxyKey).digest();
  const sk = N.deriveSecretKey(process.env.NANO_SEED, Number(process.env.NANO_INDEX || 0));
  const pub = N.derivePublicKey(sk);
  const account = N.deriveAddress(pub, { useNanoPrefix: true });
  return {
    keyHash,
    upstream, host: u.host, protocol: u.protocol, cap, perCall, allow, port, sk, pub, account,
    state: process.env.STATE_FILE || path.join(os.homedir(), '.pursekeeper', `inference-proxy-${port}.json`),
    rpc: process.env.NANO_RPC || null,
    api: (process.env.API || 'https://pursekeeper.dev').replace(/\/$/, ''),
    workUrl: process.env.WORK_URL || null,
    receive: (process.env.RECEIVE ?? '1') !== '0',
  };
})();

// ---- state: persisted before anything is signed, so a crash overcounts rather than undercounts ----
const state = (() => {
  let s = { account: cfg.account, upstream: cfg.upstream, spent_raw: '0', received_raw: '0', calls: 0, paid: 0, refused: 0, payments: [], receipts: [] };
  try { s = { ...s, ...JSON.parse(fs.readFileSync(cfg.state, 'utf8')) }; } catch (e) { if (e.code !== 'ENOENT') { console.error('state file unreadable: ' + e.message); process.exit(2); } }
  if (s.account !== cfg.account) { console.error(`state file ${cfg.state} belongs to ${s.account}, not ${cfg.account}; use another STATE_FILE`); process.exit(2); }
  return s;
})();
function persist() {
  fs.mkdirSync(path.dirname(cfg.state), { recursive: true, mode: 0o700 });
  const tmp = cfg.state + '.tmp';
  fs.writeFileSync(tmp, JSON.stringify(state, null, 1), { mode: 0o600 });
  fs.renameSync(tmp, cfg.state);
}
const spent = () => BigInt(state.spent_raw);
// Every payment entry carries `counted`: whether its amount is inside spent_raw right now. Count and uncount only through this.
function count(p, counted) {
  if (!!p.counted === counted) return;
  const a = BigInt(p.amount_raw);
  state.spent_raw = (counted ? spent() + a : spent() - a).toString();
  p.counted = counted;
}

// ---- chain access: a node's RPC when given, else the free endpoints on pursekeeper.dev ----
const post = (u, body) => fetch(u, { method: 'POST', body: JSON.stringify(body), headers: { 'content-type': 'application/json' } }).then(r => r.json());
async function accountInfo() {
  if (cfg.rpc) {
    const r = await post(cfg.rpc, { action: 'account_info', account: cfg.account, representative: 'true', include_confirmed: 'true' });
    if (r.error) return /not found/i.test(r.error) ? { found: false } : { error: r.error };
    return { found: true, frontier: r.frontier, balance: r.balance, representative: r.representative, height: Number(r.block_count), confirmed_height: Number(r.confirmation_height), confirmed_frontier: r.confirmed_frontier || null };
  }
  const r = await fetch(cfg.api + '/v1/account_info?account=' + cfg.account);
  if (!r.ok) throw new Error('account_info HTTP ' + r.status);
  const i = await r.json();
  if (i.error) return { error: i.error };
  return i.found ? { found: true, frontier: i.frontier, balance: i.balance_raw, representative: i.representative, height: Number(i.block_count), confirmed_height: Number(i.confirmation_height), confirmed_frontier: i.confirmed_frontier || null } : { found: false };
}
async function receivable() {
  if (cfg.rpc) {
    const r = await post(cfg.rpc, { action: 'receivable', account: cfg.account, count: '10', source: 'true', threshold: '1' });
    const b = r.blocks && typeof r.blocks === 'object' ? r.blocks : {};
    return Object.entries(b).map(([hash, v]) => ({ hash, amount_raw: String(v.amount), from: v.source }));
  }
  const r = await fetch(cfg.api + '/v1/receivable?account=' + cfg.account).then(x => x.json());
  return Array.isArray(r.blocks) ? r.blocks : [];
}
async function work(hash) {
  if (cfg.workUrl) {
    const r = await post(cfg.workUrl, { action: 'work_generate', hash, difficulty: 'fffffff800000000' }).catch(e => ({ error: e.message }));
    if (r.work) return r.work;
    log('WORK_URL failed:', r.error || r);
  }
  if (cfg.rpc) {
    const r = await post(cfg.rpc, { action: 'work_generate', hash, difficulty: 'fffffff800000000' }).catch(e => ({ error: e.message }));
    if (r.work) return r.work;
  }
  for (let i = 0; i < 6; i++) {
    const r = await post(cfg.api + '/v1/work', { hash }).catch(e => ({ error: e.message }));
    if (r.work) return r.work;
    if (!/limit/i.test(String(r.error))) break;
    await sleep(10000);
  }
  log('computing work on the CPU (this takes a while)');
  return N.computeWork(hash, { workThreshold: 'fffffff800000000' });
}
async function broadcast(block, subtype) {
  if (cfg.rpc) {
    const r = await post(cfg.rpc, { action: 'process', json_block: 'true', subtype, block });
    if (!r.hash) throw new Error('process: ' + JSON.stringify(r).slice(0, 200));
    return r.hash;
  }
  const r = await post(cfg.api + '/v1/process', { block, subtype });
  if (!r.ok) throw new Error('process: ' + JSON.stringify(r).slice(0, 200));
  return r.hash;
}
// Did a block this process handed to the network land? true, false, or a thrown "cannot tell".
async function landed(hash) {
  const i = await accountInfo();
  if (i.found && String(i.frontier).toUpperCase() === hash.toUpperCase()) return true;
  if (cfg.rpc) {
    const r = await post(cfg.rpc, { action: 'block_info', json_block: 'true', hash });
    if (r.contents) return true;
    if (/not found/i.test(String(r.error))) return false;
    throw new Error('cannot tell whether ' + hash + ' landed: ' + JSON.stringify(r).slice(0, 120));
  }
  const v = await fetch(cfg.api + '/v1/verify?hash=' + hash + '&any=1').then(r => r.json()).catch(e => { throw new Error('cannot tell whether ' + hash + ' landed: ' + e.message); });
  if (v.found === true) return true;
  if (v.found === false) return false;
  throw new Error('cannot tell whether ' + hash + ' landed: ' + JSON.stringify(v).slice(0, 120));
}

// ---- the chain-side wallet, used only inside the lock ----
let chain = Promise.resolve();
const withLock = fn => { const p = chain.then(fn, fn); chain = p.then(() => {}, () => {}); return p; };

class Refuse extends Error { constructor(code, detail) { super(code); this.code = code; this.detail = detail || {}; } }

function signSend(info, amountRaw, toAccount, w) {
  const balance = BigInt(info.balance) - amountRaw;
  if (balance < 0n) throw new Refuse('insufficient_balance', { balance_raw: String(info.balance), amount_raw: String(amountRaw) });
  const { block, hash } = N.createBlock(cfg.sk, { work: w, previous: info.frontier, representative: info.representative, balance: balance.toString(), link: toAccount });
  block.account = block.account.replace(/^xrb_/, 'nano_');
  return { block, hash };
}

// Pocket what is receivable (NanoGPT refunds over-quotes on-chain). Bounded, best effort, counted as received.
async function pocket() {
  if (!cfg.receive) return;
  let pend; try { pend = await receivable(); } catch (e) { log('receivable read failed: ' + e.message); return; }
  for (const b of pend.slice(0, 3)) {
    try {
      const i = await accountInfo();
      if (i.error) return;
      const previous = i.found ? i.frontier : ZERO;
      const balance = (i.found ? BigInt(i.balance) : 0n) + BigInt(b.amount_raw);
      const rep = i.representative || 'nano_3arg3asgtigae3xckabaaewkx3bzsh7nwz7jkmjos79ihyaxwphhm6qgjps4';
      const w = await work(previous === ZERO ? cfg.pub : previous);
      const block = { type: 'state', account: cfg.account, previous, representative: rep, balance: balance.toString(), link: b.hash, work: w };
      block.signature = N.signBlock({ hash: N.hashBlock(block), secretKey: cfg.sk });
      const h = await broadcast(block, previous === ZERO ? 'open' : 'receive');
      state.received_raw = (BigInt(state.received_raw) + BigInt(b.amount_raw)).toString();
      state.receipts.push({ t: new Date().toISOString(), hash: h, from: b.from, amount_raw: String(b.amount_raw), source: b.hash });
      persist();
      log('pocketed ' + fmt(b.amount_raw) + ' XNO from ' + b.from + ' -> ' + h);
    } catch (e) { log('receive failed: ' + e.message); return; }
  }
}

// A signed send that has not landed can still land for as long as the account's frontier is the block's `previous`:
// a seller that refused the call still holds a valid signed block, and a node that took a broadcast whose reply was lost
// may put it on the chain later. So such a send stays counted until it either lands or a different block is confirmed at
// its height. The proxy forces the second outcome itself: it publishes a change block at that height (same balance,
// same representative, nothing moves; the work computed for the send is good for it, since work is over `previous`).
// Until 0.3.1 the refused send was uncounted at once, which left one per-call amount per frontier that a seller could
// broadcast later outside the cap.
const PENDING = new Set(['signed', 'unknown', 'not_broadcast', 'not_broadcast_refused']);
const pending = () => state.payments.filter(p => PENDING.has(p.status) && !p.final && p.height != null);   // entries written before 0.3.1 carry no height and are left as they are
async function invalidate(p, info) {
  const w = p.work && p.work !== '0' ? p.work : await work(info.frontier);
  const block = { type: 'state', account: cfg.account, previous: info.frontier, representative: info.representative, balance: String(info.balance), link: ZERO, work: w };
  block.signature = N.signBlock({ hash: N.hashBlock(block), secretKey: cfg.sk });
  p.invalidated_by = await broadcast(block, 'change');
  log(`send ${p.hash} (${p.status}) can no longer land: change block ${p.invalidated_by} published at the same height; the spend stays counted until a block is confirmed there`);
}
// One look at one pending entry against a fresh account read. Returns true when the entry is settled for good.
async function settleOne(p, info) {
  const on = await landed(p.hash);                                     // throws when the chain cannot be read: the entry is left as it is
  if (on) { p.status = p.kind === 'nano' ? 'broadcast' : 'broadcast_not_served'; p.final = true; count(p, true); return true; }
  if (info.confirmed_height >= p.height) { p.final = true; count(p, false); return true; }   // a different block is confirmed at this height
  if (String(info.frontier).toUpperCase() === String(p.previous).toUpperCase()) await invalidate(p, info);
  return false;
}
// Settle what can be settled: at every paid call before the decision, at start-up, and right after a refusal.
async function settlePending(entries) {
  const list = entries || pending();
  if (!list.length) return;
  for (const p of list) {
    for (let pass = 0; pass < 3; pass++) {
      let info; try { info = await accountInfo(); } catch (e) { log('settle ' + p.hash + ': ' + e.message); break; }
      if (!info.found || info.error) break;
      const hadInvalidator = !!p.invalidated_by;
      let done; try { done = await settleOne(p, info); } catch (e) { log('settle ' + p.hash + ': ' + e.message); break; }
      persist();
      if (done || (hadInvalidator && pass > 0)) break;             // a change block was just published: look again once it has had a moment to confirm
      await sleep(pass === 0 ? 300 : 700);
    }
  }
}

// ---- the 402 quote, in either dialect ----
function parseQuote(status, headers, bodyText) {
  if (status !== 402) return null;
  const pr = headers.get('payment-required');
  if (pr) {
    let v; try { v = unb64(pr); } catch { throw new Refuse('malformed_quote', { field: 'payment-required' }); }
    if (v.x402Version !== 2 || !Array.isArray(v.accepts)) throw new Refuse('malformed_quote', { field: 'x402Version' });
    const a = v.accepts.find(x => x.scheme === 'exact' && x.network === 'nano:mainnet');
    if (!a) throw new Refuse('no_nano_option', { accepts: v.accepts.map(x => `${x.scheme}/${x.network}`) });
    return { kind: 'exact', payTo: a.payTo, amount: a.amount, pr: v, accepted: a, sellerWork: a.extra && a.extra.work === 'optional' };
  }
  let j; try { j = JSON.parse(bodyText); } catch { throw new Refuse('malformed_quote', { field: 'body' }); }
  const list = j && j.payment && Array.isArray(j.payment.accepted) ? j.payment.accepted : null;
  if (list) {
    const a = list.find(x => x.scheme === 'nano' && /^nano[-:]mainnet$/.test(String(x.network)));
    if (!a) throw new Refuse('no_nano_option', { accepts: list.map(x => `${x.scheme}/${x.network}`) });
    return { kind: 'nano', payTo: a.payTo, amount: a.amount, paymentId: a.paymentId || j.payment.paymentId, completeUrl: a.completeUrl || j.payment.completeUrl, statusUrl: a.statusUrl || j.payment.statusUrl, expiresAt: a.expiresAt || j.payment.expiresAt };
  }
  if (j && j.x402 && j.x402.x402Version === 2) return parseQuote(402, new Map([['payment-required', b64(j.x402)]]), '');
  throw new Refuse('malformed_quote', { field: 'unknown dialect' });
}

// The one decision, made under the lock before anything is signed. Every path out is a Refuse or a quote cleared to pay.
function decide(q) {
  if (!N.checkAddress(String(q.payTo || ''))) throw new Refuse('malformed_quote', { field: 'payTo' });
  if (!/^\d+$/.test(String(q.amount || ''))) throw new Refuse('malformed_quote', { field: 'amount' });
  const amount = BigInt(q.amount);
  if (amount <= 0n) throw new Refuse('malformed_quote', { field: 'amount', value: q.amount });
  if (q.kind === 'nano') {
    for (const [k, u] of [['completeUrl', q.completeUrl], ['statusUrl', q.statusUrl]]) {
      let p; try { p = new URL(String(u)); } catch { throw new Refuse('malformed_quote', { field: k }); }
      if (p.host !== cfg.host) throw new Refuse('host_mismatch', { field: k, host: p.host, upstream: cfg.host });
      // Same host is not enough: a quote naming http:// on an https door would carry the chat (and the signed block)
      // in clear. The URL's protocol must be the door's (ClawHub's scanner on 0.3.5, 2026-10-20).
      if (p.protocol !== cfg.protocol) throw new Refuse('protocol_mismatch', { field: k, protocol: p.protocol, upstream: cfg.protocol });
    }
    if (!q.paymentId) throw new Refuse('malformed_quote', { field: 'paymentId' });
    // One payment id is paid at most once by this state file. A repeated id is a replay whatever the door says, and an
    // in-flight entry counts too, so two parallel requests cannot both pay it (Ops Control HQ, Review A case A11, 2026-10-10).
    const prior = state.payments.find(p => p.paymentId && p.paymentId === q.paymentId && p.status !== 'not_broadcast');
    if (prior) throw new Refuse('paymentid_replayed', { paymentId: q.paymentId, hash: prior.hash, status: prior.status });
    // expiresAt is required, not optional: until 0.2.1 a quote without one skipped the check and was paid (pyfile-toolkit, 2026-10-10).
    if (q.expiresAt === undefined || q.expiresAt === null || q.expiresAt === '') throw new Refuse('malformed_quote', { field: 'expiresAt' });
    const t = Date.parse(String(q.expiresAt));
    if (!Number.isFinite(t) || t < Date.now() + 5000) throw new Refuse('quote_expired', { expiresAt: q.expiresAt });
  }
  if (q.kind === 'exact') {
    // The resource the quote names (x402 v2: top-level `resource`, a string or {url}; v1 shape: accepts[].resource) must be on
    // the door's host when present. A quote for a resource elsewhere is not this door's quote and is refused before signing
    // (Ops Control HQ, Review A cases A06/A07, 2026-10-10).
    for (const [k, v] of [['resource', q.pr && q.pr.resource], ['accepts.resource', q.accepted && q.accepted.resource]]) {
      if (v === undefined || v === null) continue;
      const u = typeof v === 'object' ? v.url : v;
      let p; try { p = new URL(String(u)); } catch { throw new Refuse('malformed_quote', { field: k }); }
      if (p.host !== cfg.host) throw new Refuse('resource_mismatch', { field: k, host: p.host, upstream: cfg.host });
      if (p.protocol !== cfg.protocol) throw new Refuse('protocol_mismatch', { field: k, protocol: p.protocol, upstream: cfg.protocol });
    }
  }
  if (cfg.allow.length && !cfg.allow.includes(q.payTo)) throw new Refuse('payto_not_allowed', { payTo: q.payTo });
  if (amount > cfg.perCall) throw new Refuse('over_per_call_limit', { amount: fmt(amount), limit: fmt(cfg.perCall) });
  if (spent() + amount > cfg.cap) throw new Refuse('cap_exceeded', { amount: fmt(amount), spent: fmt(spent()), cap: fmt(cfg.cap) });
  return amount;
}

// ---- HTTP plumbing ----
// Runtime credential headers are dropped before the door sees them: the runtime is told to use "any API key"
// and the proxy is the one paying. Until 0.2.3 only authorization and proxy-authorization were dropped, so a
// runtime that sends its key as x-api-key forwarded it verbatim (pyfile-toolkit, api#89, 2026-10-10).
const CREDENTIAL = ['authorization', 'proxy-authorization', 'x-api-key', 'api-key', 'x-auth-token', 'x-goog-api-key', 'cookie'];
const HOP = new Set(['host', 'connection', 'keep-alive', 'transfer-encoding', 'content-length', ...CREDENTIAL, 'payment-signature', 'x-payment', 'x-nano-represent', 'x-x402', 'x-x402-payment-id']);
function doorHeaders(req, extra) {
  const h = {};
  for (const [k, v] of Object.entries(req.headers)) if (!HOP.has(k)) h[k] = Array.isArray(v) ? v.join(', ') : v;
  if (!h['content-type'] && req.method !== 'GET') h['content-type'] = 'application/json';
  return { ...h, ...extra };
}
const PASS = ['content-type', 'x-x402-payment-id', 'x-x402-amount-paid', 'x-x402-actual-cost-usd', 'x-x402-quoted-cost-usd', 'x-x402-reconciliation-amount', 'x-x402-reconciliation-refunded', 'payment-response', 'x-nano-replay', 'x-request-id'];
function refuse(res, status, code, detail, extra) {
  state.refused++;
  state.refusals = (state.refusals || []).slice(-19).concat([{ t: new Date().toISOString(), code, detail, path: res.req && res.req.url }]);
  persist();
  log('refused ' + code + ' ' + JSON.stringify(detail || {}).slice(0, 300));
  res.writeHead(status, { 'content-type': 'application/json', 'x-payer-refused': code });
  res.end(JSON.stringify({ error: { message: `inference-proxy refused: ${code} ${JSON.stringify(detail || {})}`, type: 'nano_payer_refused', code }, payer: { code, detail, ...extra } }));
}
// The whole message becomes the one delta: content, tool_calls (each with its index, as the chunk schema has it),
// refusal and whatever else the door put there. Until 0.2.2 only content was carried, so a tool-call answer
// arrived as finish_reason tool_calls with no call in it (pyfile-toolkit, api#89, 2026-10-10).
function asDelta(m) {
  const { role, content, tool_calls, ...rest } = m || {};
  const d = { role: role || 'assistant', content: content == null ? '' : content, ...rest };
  if (Array.isArray(tool_calls)) d.tool_calls = tool_calls.map((t, i) => ({ index: i, ...t }));
  return d;
}
// A door answer in the 300s is never relayed or followed: the runtime would see a status with no Location (that header is
// not passed through), and the proxy itself follows nothing after the host check. Named instead, with the Location's origin.
function isRedirect(r) { return r.status >= 300 && r.status <= 399; }
function redirectDetail(r) {
  let origin = null; try { origin = new URL(r.headers.get('location') || '', cfg.upstream).origin; } catch { origin = null; }
  return { status: r.status, location_origin: origin };
}
async function relay(res, r, wantStream, extra) {
  const h = { ...extra };
  for (const k of PASS) if (r.headers.get(k)) h[k] = r.headers.get(k);
  const ct = r.headers.get('content-type') || '';
  if (wantStream && !/text\/event-stream/.test(ct) && r.ok) {
    // The door answered a stream request with a plain completion: hand it over as one chunk so the runtime's SSE reader works.
    const text = await r.text();
    let j; try { j = JSON.parse(text); } catch { j = null; }
    h['content-type'] = 'text/event-stream'; h['x-payer-stream'] = 'buffered'; h['cache-control'] = 'no-cache';
    res.writeHead(r.status, h);
    if (j && Array.isArray(j.choices)) {
      const chunk = { id: j.id, object: 'chat.completion.chunk', created: j.created, model: j.model, usage: j.usage,
        choices: j.choices.map(c => ({ index: c.index, delta: asDelta(c.message), finish_reason: c.finish_reason || 'stop' })) };
      res.write('data: ' + JSON.stringify(chunk) + '\n\n');
    } else res.write('data: ' + text.replace(/\n/g, ' ') + '\n\n');
    res.end('data: [DONE]\n\n');
    return;
  }
  if (wantStream) h['x-payer-stream'] = 'passthrough';
  res.writeHead(r.status, h);
  if (!r.body) return res.end();
  for await (const chunk of r.body) res.write(chunk);
  res.end();
}

// Loopback is shared with every process and every browser tab on the machine. Before anything is read, counted
// or signed: the Host must be a loopback name (a page that rebinds its DNS to 127.0.0.1 arrives with its own
// host name), no Origin header (a browser sets one on every cross-site request, including the no-preflight
// POSTs a page may send to 127.0.0.1), and /v1/* must carry PROXY_KEY (a page cannot set Authorization or
// x-api-key without a preflight, which the proxy never answers).
const LOOPBACK = new Set(['127.0.0.1', 'localhost', '[::1]', '::1']);
function gate(req) {
  const host = String(req.headers.host || '').trim().toLowerCase().replace(/:\d+$/, '');
  if (!LOOPBACK.has(host)) return { status: 403, code: 'host_not_loopback', detail: { host: req.headers.host || null } };
  if (req.headers.origin !== undefined) return { status: 403, code: 'browser_origin', detail: { origin: String(req.headers.origin).slice(0, 200) } };
  return null;
}
const keyMatches = v => { if (typeof v !== 'string' || !v) return false; return timingSafeEqual(createHash('sha256').update(v.trim()).digest(), cfg.keyHash); };
function keyPresented(req) {
  const a = req.headers.authorization, m = typeof a === 'string' ? /^Bearer\s+(.+)$/i.exec(a.trim()) : null;
  return keyMatches(m && m[1]) || keyMatches(req.headers['x-api-key']);
}

async function handle(req, res) {
  const g = gate(req);
  if (g) return refuse(res, g.status, g.code, g.detail);
  // The state readout is key-gated like /v1/*: it lists recent payment hashes, pay-to accounts and payment ids, and
  // on a shared loopback any process could read them without the key (ClawHub's scanner on 0.3.6, 2026-10-20).
  const keyRefusal = () => refuse(res, 401, 'proxy_key', { presented: ['authorization', 'x-api-key'].filter(h => req.headers[h] !== undefined), hint: 'send PROXY_KEY as "Authorization: Bearer <key>" or "x-api-key: <key>"' });
  if (req.method === 'GET' && req.url === '/_nano/state') {
    if (!keyPresented(req)) return keyRefusal();
    res.writeHead(200, { 'content-type': 'application/json' });
    return res.end(JSON.stringify({ account: cfg.account, upstream: cfg.upstream, cap: fmt(cfg.cap), per_call_limit: fmt(cfg.perCall), spent: fmt(spent()), remaining: fmt(cfg.cap - spent()), received: fmt(state.received_raw),
      calls: state.calls, paid: state.paid, refused: state.refused, allow_payto: cfg.allow, refusals: (state.refusals || []).slice(-10), payments: state.payments.slice(-50).map(p => ({ ...p, payload: undefined })), receipts: state.receipts.slice(-20) }, null, 1));
  }
  if (!req.url.startsWith('/v1/')) { res.writeHead(404, { 'content-type': 'application/json' }); return res.end('{"error":"only /v1/* is forwarded"}'); }
  if (!keyPresented(req)) return keyRefusal();
  state.calls++;
  const chunks = []; let size = 0;
  for await (const c of req) { size += c.length; if (size > 4 << 20) { res.writeHead(413); return res.end(); } chunks.push(c); }
  const body = chunks.length ? Buffer.concat(chunks) : undefined;
  let wantStream = false; try { wantStream = !!(body && JSON.parse(body.toString()).stream); } catch { /* not JSON; forwarded as is */ }
  const url = cfg.upstream + req.url;
  const send = extra => fetch(url, { method: req.method, headers: doorHeaders(req, extra), body, redirect: 'manual' });

  let first;
  try { first = await send({}); } catch (e) { return refuse(res, 502, 'door_unreachable', { error: e.message }); }
  if (isRedirect(first)) return refuse(res, 502, 'door_redirect', redirectDetail(first));
  if (first.status !== 402) return relay(res, first, wantStream, {});
  let quote;
  try { quote = parseQuote(first.status, first.headers, await first.text()); } catch (e) { return e instanceof Refuse ? refuse(res, 402, e.code, e.detail) : refuse(res, 502, 'quote_unreadable', { error: e.message }); }

  // Everything that moves money happens inside the lock: decide, sign, broadcast (nano) or hand over (exact).
  let paid;
  try {
    paid = await withLock(async () => {
      await settlePending();
      const amount = decide(quote);                                 // first: nothing below runs for a refused quote
      await pocket();
      const info = await accountInfo();
      if (info.error) throw new Refuse('account_unreadable', { error: info.error });
      if (!info.found) throw new Refuse('account_not_opened', { account: cfg.account });
      const entry = { t: new Date().toISOString(), kind: quote.kind, amount_raw: amount.toString(), payTo: quote.payTo, paymentId: quote.paymentId || null, hash: null, status: 'deciding', counted: false, final: false, path: req.url };
      state.payments.push(entry);
      if (quote.kind === 'nano') {
        const w = await work(info.frontier);
        const { block, hash } = signSend(info, amount, quote.payTo, w);
        entry.hash = hash; entry.previous = info.frontier; entry.height = info.height + 1; entry.work = w; entry.status = 'signed'; count(entry, true); persist();   // counted before the network sees it
        try { await broadcast(block, 'send'); entry.status = 'broadcast'; entry.final = true; }
        catch (e) {
          let on; try { on = await landed(hash); } catch { on = null; }
          if (on === false) {
            // The node did not take it, but the signed block exists: retire it at this height. Uncounted only once a block is confirmed there.
            entry.status = 'not_broadcast'; persist();
            await settlePending([entry]);
            throw new Refuse('broadcast_failed', { error: e.message, hash, counted: !!entry.counted, invalidated_by: entry.invalidated_by || null });
          }
          if (on) entry.final = true;
          entry.status = on ? 'broadcast' : 'unknown';              // unknown stays counted until a later read settles it
        }
        state.paid++; persist();
        return { entry, amount };
      }
      // exact: sign, then present; the seller broadcasts. Counted at signing; a refusal is settled against the chain below.
      const w = quote.sellerWork ? '0' : await work(info.frontier);
      const { block, hash } = signSend(info, amount, quote.payTo, w);
      entry.hash = hash; entry.previous = info.frontier; entry.height = info.height + 1; entry.work = w; entry.status = 'signed'; count(entry, true); persist();
      const payload = { x402Version: 2, resource: quote.pr.resource, accepted: quote.accepted, payload: { block } };
      const extra = { 'payment-signature': b64(payload) };
      let r = await send(extra);
      for (let waited = 0; r.status === 402 && waited < 60000; waited += 2000) {
        const b = await r.clone().json().catch(() => null);
        if (!b || !/not (yet )?confirmed/.test(String(b.note || b.error || ''))) break;
        const tok = r.headers.get('x-nano-represent') || b.represent_token;
        if (tok) extra['x-nano-represent'] = String(tok); else delete extra['x-nano-represent'];
        await sleep(2000); r = await send(extra);
      }
      if (r.ok) { entry.status = 'served'; entry.final = true; state.paid++; persist(); return { entry, amount, response: r }; }
      // Not served. Was the block broadcast? Landed: counted, reported with the hash and the seller's token. Not landed: the
      // seller still holds a valid signed block, so it is retired with a change block at the same height and uncounted once a
      // block is confirmed there. The payload is not kept: a refused call is a new quote and a new send, never a re-presentation.
      let on; try { on = await landed(hash); } catch { on = null; }
      entry.status = on === true ? 'broadcast_not_served' : on === false ? 'not_broadcast_refused' : 'unknown';
      if (on === true) { entry.final = true; entry.represent_token = extra['x-nano-represent'] || null; }
      persist();
      if (on === false) await settlePending([entry]);
      throw new Refuse('not_served_after_payment', { status: r.status, hash, broadcast: on, counted: !!entry.counted, invalidated_by: entry.invalidated_by || null, body: (await r.text().catch(() => '')).slice(0, 300) });
    });
  } catch (e) {
    if (e instanceof Refuse) return refuse(res, e.code === 'not_served_after_payment' ? 502 : 402, e.code, e.detail);
    log('payment error: ' + (e.stack || e.message));
    return refuse(res, 502, 'payment_error', { error: e.message });
  }

  if (quote.kind === 'exact') return relay(res, paid.response, wantStream, { 'x-payer-paid': fmt(paid.amount), 'x-payer-hash': paid.entry.hash });
  // nano: the money moved; complete the call outside the lock so the next request can pay in parallel.
  // The door sees the send a few seconds after the broadcast (NanoGPT: status "paid", readyToComplete true; a complete
  // posted before that answers 402 with the money already spent, seen 2026-10-10), so poll the status URL first, then
  // complete, and re-poll on a 402 from the complete step. Bounded: about 90 s in all, then the runtime is told the hash
  // and payment id so the same body can be completed by hand within the quote's life.
  const completeInit = () => ({ method: req.method, headers: doorHeaders(req, { 'x-x402': 'nano', 'x-x402-payment-id': quote.paymentId }), body, redirect: 'manual' });
  // Status answers: a JSON with status/readyToComplete when the door tracks it; anything else (404, HTML, timeout, or a
  // redirect, which is never followed: the status URL passed the host check, a Location would not) counts as "cannot tell"
  // and the complete step is simply tried (ClawHub's scanner on 0.3.10, 2026-10-22).
  const paidAtDoor = async () => { try { const x = await fetch(quote.statusUrl, { redirect: 'manual' }); if (!x.ok) return null; const s = await x.json(); return !!(s.readyToComplete === true || s.status === 'paid' || s.status === 'completed'); } catch { return null; } };
  let r = null, lastErr = null;
  const deadline = Date.now() + 90000;
  for (let attempt = 0; attempt < 30 && Date.now() < deadline; attempt++) {
    if (attempt > 0) await sleep(Math.min(5000, 1000 * attempt));
    if ((await paidAtDoor()) === false) continue;           // door says not yet: wait, do not spend the complete
    try { r = await fetch(quote.completeUrl, completeInit()); } catch (e) { lastErr = e; r = null; continue; }
    if (r.status !== 402) break;
    await r.text().catch(() => {});                          // 402 from complete: the door has not seen the send yet
    r = null;
  }
  if (!r) { paid.entry.status = 'paid_not_served'; persist(); return refuse(res, 502, 'complete_unreachable', { error: lastErr ? lastErr.message : 'door did not see the payment within 90 s', hash: paid.entry.hash, paymentId: quote.paymentId, completeUrl: quote.completeUrl }); }
  if (isRedirect(r)) { paid.entry.status = 'paid_not_served'; persist(); return refuse(res, 502, 'door_redirect', { ...redirectDetail(r), hash: paid.entry.hash, paymentId: quote.paymentId, completeUrl: quote.completeUrl }); }
  paid.entry.status = r.ok ? 'served' : 'paid_not_served';
  if (r.headers.get('x-x402-reconciliation-amount')) paid.entry.reconciliation = r.headers.get('x-x402-reconciliation-amount');
  persist();
  return relay(res, r, wantStream, { 'x-payer-paid': fmt(paid.amount), 'x-payer-hash': paid.entry.hash, 'x-payer-payment-id': quote.paymentId });
}

const server = http.createServer((req, res) => handle(req, res).catch(e => { log('handler error: ' + (e.stack || e.message)); if (!res.headersSent) refuse(res, 500, 'internal', { error: e.message }); else res.end(); }));
server.listen(cfg.port, '127.0.0.1', () => {
  persist();
  if (pending().length) withLock(() => settlePending()).catch(e => log('settle at start: ' + e.message));
  log(`inference-proxy on http://127.0.0.1:${server.address().port}/v1 -> ${cfg.upstream}; paying from ${cfg.account}; cap ${fmt(cfg.cap)} XNO (spent ${fmt(spent())}), per call ${fmt(cfg.perCall)}; PROXY_KEY set; state ${cfg.state}`);
});
