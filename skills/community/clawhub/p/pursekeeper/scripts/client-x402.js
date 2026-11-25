#!/usr/bin/env node
// x402 client for Nano (scheme "exact", network "nano:mainnet"), usable against
// https://pursekeeper.dev or any other seller that speaks the same scheme.
//
//   NANO_SEED=<64 hex> node client-x402.js [url]      (default: pursekeeper.dev/v1/echo?msg=hello)
//
// Env: NANO_SEED (required), NANO_INDEX (account index, default 0),
//      NANO_MAX_PAY (spending cap in NANO as decimal text, default 0.01; a 402 quote above it is refused, nothing signed, exit 3),
// Exit codes: 0 when the call was served (2xx), 1 when it ended on any other status or threw, 2 without a seed, 3 above the cap,
//      4 when the seller's 402 resource breaks the x402 v2 ResourceInfo caps (nothing signed; the seller has to fix the 402),
//      5 when the wallet lock wait reaches NANO_LOCK_WAIT_MS (including a missing/invalid holder PID), or a live holder reaches NANO_LOCK_MAX_MS (nothing signed),
//      6 when the unsigned quote redirects to another origin, with or without HEADERS (nothing sent there, nothing signed),
//      7 when an earlier payment stands in the way of this call (nothing signed): a block that is on the chain, or may
//        be, already paid for this same call; or the record of unresolved payments cannot be read. Also 7 when the
//        record cannot be written: then the block was signed but is not sent. The stderr line says which and what to do.
//      NANO_PENDING (the unresolved-payment record below; default on, NANO_PENDING=0 turns it off), NANO_PENDING_DIR
//      (where the record lives, default ~/.pursekeeper; it must survive a restart, so not a temp dir),
//      NANO_PENDING_ACK (a block hash, or several separated by commas: "I know about that payment and I am paying for
//      this call again on purpose"; it releases that block's entry for the call being made and no other), NANO_PENDING_HOLD_H (hours a landed payment keeps blocking a repeat of its own
//      call, default 24; after that it is history and the call can be bought again),
// Work: WORK_URL if set, else the seller's POST /v1/work if it has one, else local
// CPU (about 20-30 s). Only dependency: nanocurrency (npm i nanocurrency).
//
// Flow: GET url -> 402 with PAYMENT-REQUIRED (base64 JSON, x402 v2) -> pick the
// nano:mainnet "exact" entry -> build and sign a send block for exactly that amount
// -> retry with PAYMENT-SIGNATURE: base64 JSON {x402Version, resource, accepted,
// payload: {block}} -> the seller verifies and broadcasts the block, replies 200
// with PAYMENT-RESPONSE carrying the block hash. The unsigned quote follows same-origin redirects for up to 20 hops
// with the same method, body and headers; any cross-origin redirect is refused with exit 6, even without HEADERS.
// Signed requests use the final 402 response URL and never follow redirects.
//
// One writer per account. A Nano account chain is serial: each send commits to its predecessor, so ten processes paying
// from one seed at once would sign ten competing blocks against one frontier; one would land and nine would be refused
// frontier_moved (CasualSecurityInc's x402.Nano review at 7c55f32, pursekeeper/api#90, 2026-10-18). Per-hash locks on the
// seller or facilitator side cannot order them, the hashes differ. So this client holds a per-account lock on this host
// from the frontier read until the fate of its block is known (served; refused with the frontier untouched; landed; or
// dead because the frontier moved past it), then exits and releases, and the next process signs against the new
// frontier. Two hosts sharing one seed are not covered: give each writer its own NANO_INDEX, one account per writer,
// which is also the way to pay in parallel on one host. After any outcome but 2xx the fate is printed with what to do:
// re-present the same payment (landed, or untouched) or sign anew (dead); a lost reply after the payment was sent is
// resolved the same way instead of being reported as an error.
//
// What the lock does not cover, and the record that does. The lock is released when this process exits, whatever the
// fate of its block. If the call was not served, the seller may still hold a signed send it can broadcast later, or the
// block may already be on the chain; a caller that simply runs the command again would then sign a second block and pay
// twice (ClawHub's scan of skill 0.3.16 and 0.3.17, 2026-11-19). So before the signed request leaves this process, the
// block's hash, its predecessor and the call it pays for (URL, method, SHA-256 of the body; no signature, nothing
// spendable) are written to <NANO_PENDING_DIR>/pending-<account>.json, mode 600. An entry is removed when its block is
// proven dead, or when a call is served on its block. A block is one payment: if the same block was also on record
// for another call (it can be signed for two calls only while it has not been broadcast: same predecessor, same quote,
// so the same hash), the served call is the one it bought, the other call has not been paid for, and its entry goes
// too, with a stderr line naming it. Keeping it would refuse that call's retry as "already paid", which would be false
// (ClawHub's scan of 0.3.19 read the earlier wording here as a promise to keep it). Every later run from the same
// account reads the record under the lock, with the same frontier it is about to sign against, and for each entry:
//   - never broadcast (the frontier is still its predecessor): kept, and signing goes ahead, because the new block
//     names the same predecessor and a Nano account can confirm only one block per predecessor. Whichever of the two
//     lands, the other is dead; the two can never both be paid;
//   - proven dead (the node shows its predecessor with a different, confirmed successor): dropped;
//   - on the chain, or possibly on the chain (the account moved on and the node could not say which): the entry stays.
//     A different call goes ahead: that block can no longer land later, so nothing signed now can be a second payment
//     for the same thing. This same call (same method, body and URL) is refused with exit 7 and nothing signed:
//     re-present the payment that was made (the saved PAYMENT-SIGNATURE, or the hash by the seller's own route).
//     NANO_PENDING_ACK=<hash> pays again on purpose and releases this call's entry only; NANO_PENDING_HOLD_H hours
//     (default 24) after this client last sent the block for that call, the entry moves to unserved-<account>.jsonl
//     beside the record (what was paid for and not served on that run) and stops blocking. The hold is counted from
//     the sending, not from the landing: a block a seller broadcasts late has less of its hold left, or none.
//     If the block is on record for two calls, each is refused on its own entry ("may already be paid": the block paid
//     for one of them and the client cannot know which), and an entry that outlives the other keeps a note of it.
// So the same call is not signed twice while an earlier block for it is, or may be, on the chain, short of an
// acknowledgement by hash or the hold running out; and blocks that were never broadcast are made harmless by sharing
// the new block's predecessor. Not covered: two hosts sharing one seed (as for the lock), a record that was deleted,
// NANO_PENDING=0, other wallet software spending from the same account, a block that a seller broadcasts after its
// hold has run out with no run from this account in between, and a call repeated with different HEADERS (they are not
// part of what makes two calls the same).
'use strict';
const N = require('nanocurrency');
const { reapDeadHolder } = require('./wallet-lock-reaper');
const fs = require('node:fs'), os = require('node:os'), path = require('node:path');
const { createHash } = require('node:crypto');

// Mirror of @x402/core's ResourceInfoSchema caps (2.25.0), kept dependency-free. Returns '' when fine, else what is wrong.
function resourceInfoFault(r) {
  if (!r || typeof r !== 'object') return 'resource missing';
  if (typeof r.url !== 'string' || !r.url) return 'resource.url missing';
  const ascii = s => /^[\x20-\x7e]+$/.test(s);
  if (r.serviceName != null && (typeof r.serviceName !== 'string' || r.serviceName.length < 1 || r.serviceName.length > 32 || !ascii(r.serviceName)))
    return `resource.serviceName is ${typeof r.serviceName === 'string' ? r.serviceName.length + ' characters' : typeof r.serviceName}, allowed 1-32 printable ASCII`;
  if (r.tags != null) {
    if (!Array.isArray(r.tags) || r.tags.length > 5) return `resource.tags has ${Array.isArray(r.tags) ? r.tags.length : 'no'} entries, allowed at most 5`;
    const bad = r.tags.find(t => typeof t !== 'string' || t.length < 1 || t.length > 32 || !ascii(t));
    if (bad !== undefined) return `resource.tags entry ${JSON.stringify(bad)} is not 1-32 printable ASCII characters`;
  }
  if (r.iconUrl != null && (typeof r.iconUrl !== 'string' || r.iconUrl.length > 2048)) return 'resource.iconUrl longer than 2048';
  return '';
}
const MAX_NANO_RAW = 133248297920938463463374607431768211455n;   // 2^128 - 1 (Nano supply ceiling in raw)
function acceptedFault(a) {
  if (String(a.asset || '').toUpperCase() !== 'XNO') return `accepted.asset is ${JSON.stringify(a.asset)}, expected "XNO"`;
  if (typeof a.payTo !== 'string' || !N.checkAddress(a.payTo.replace(/^xrb_/, 'nano_')))
    return `accepted.payTo ${JSON.stringify(a.payTo)} is not a valid Nano address`;
  if (typeof a.amount !== 'string' || !/^[1-9]\d*$/.test(a.amount))
    return `accepted.amount ${JSON.stringify(a.amount)} must be a positive integer string in raw`;
  if (BigInt(a.amount) > MAX_NANO_RAW)
    return `accepted.amount ${a.amount} raw exceeds the Nano supply ceiling (${MAX_NANO_RAW} raw)`;
  return '';
}

const url = process.argv[2] || 'https://pursekeeper.dev/v1/echo?msg=hello';
const RPC = process.env.NANO_RPC;
const API = (process.env.API || 'https://pursekeeper.dev').replace(/\/$/, '');
const b64 = s => Buffer.from(JSON.stringify(s)).toString('base64');
const unb64 = s => JSON.parse(Buffer.from(s, 'base64').toString('utf8'));
const rpc = (u, body) => fetch(u, { method: 'POST', body: JSON.stringify(body), headers: { 'content-type': 'application/json' } }).then(r => r.json());

async function accountInfo(account) {
  if (RPC) return rpc(RPC, { action: 'account_info', account, representative: 'true' });
  const r = await fetch(API + '/v1/account_info?account=' + encodeURIComponent(account));
  if (!r.ok) throw new Error('account_info HTTP ' + r.status);
  const info = await r.json();
  if (info.error) return info;
  if (!info.found) return { error: 'account has no blocks; receive first' };
  return { ...info, balance: info.balance_raw };
}

async function work(hash, origin) {
  if (process.env.WORK_URL) {
    const r = await rpc(process.env.WORK_URL, { action: 'work_generate', hash, difficulty: 'fffffff800000000' });
    if (r.work) return r.work;
    console.error('WORK_URL failed:', r.error || r);
  }
  try {
    const r = await fetch(origin + '/v1/work', { method: 'POST', body: JSON.stringify({ hash }), headers: { 'content-type': 'application/json' } });
    const j = await r.json();
    if (j.work) return j.work;
    console.error('seller /v1/work:', r.status, j.error || j);
  } catch (e) { console.error('seller /v1/work unavailable:', e.message); }
  console.error('computing work locally (this takes a while)...');
  return N.computeWork(hash, { workThreshold: 'fffffff800000000' });
}

// The per-account lock (see the header). A file created with O_EXCL under
// NANO_LOCK_DIR holds "pid startMs". Only a proven gone PID (ESRCH) is stale.
// Unlike a plain read/compare/unlink, an exclusive '.reaper' *file* now
// serialises dead-record reclamation across simultaneous local waiters.
// A pre-existing/orphaned gate is NEVER removed or expired automatically:
// the waiter polls up to NANO_LOCK_WAIT_MS then refuses unsigned, naming both
// files and the manual recovery procedure. Gate creation/recheck/unlink are
// synchronous, with no network, sleep or signing inside that critical section.
// Empty/truncated/nonpositive-PID records also refuse without removal because
// an O_EXCL holder might still be publishing its record. PID reuse and
// cross-host locking remain outside this cooperative local-file protocol.
// A live holder is never taken over: at NANO_LOCK_MAX_MS the waiter refuses
// with exit 5 so an operator can investigate the holder. Released on exit.
function walletLock(account) {
  if (process.env.NANO_LOCK === '0') return Promise.resolve();
  const file = path.join(process.env.NANO_LOCK_DIR || os.tmpdir(), 'pursekeeper-wallet-' + account + '.lock');
  const waitMs = Number(process.env.NANO_LOCK_WAIT_MS) > 0 ? Number(process.env.NANO_LOCK_WAIT_MS) : 120000;
  const maxMs = Number(process.env.NANO_LOCK_MAX_MS) > 0 ? Number(process.env.NANO_LOCK_MAX_MS) : 180000;
  const alive = pid => { try { process.kill(pid, 0); return true; } catch (e) { return e.code !== 'ESRCH'; } };   // Only ESRCH proves the holder is gone.
  const mine = process.pid + ' ' + Date.now();
  const start = Date.now();
  let told = false;
  return (async () => {
    for (;;) {
      try { fs.writeFileSync(file, mine, { flag: 'wx' }); break; } catch (e) { if (e.code !== 'EEXIST') throw e; }
      let holder = ''; try { holder = fs.readFileSync(file, 'utf8'); } catch { continue; }   // gone between the two calls
      const [pidText, atText] = holder.trim().split(' ');
      const pid = Number(pidText), age = Date.now() - Number(atText);
      // An O_EXCL create can be visible before its contents. An unreadable PID is not proof of a dead holder.
      const hasPid = Number.isInteger(pid) && pid > 0 && pid <= 0x7fffffff;
      if (!hasPid) {
        if (Date.now() - start >= waitMs) {
          console.error('refusing: waited ' + Math.round(waitMs / 1000) + ' s for the wallet lock at ' + file + ' (no PID available). Nothing signed. Check for running clients using this account; only if none are running, manually remove this lock file and retry.');
          process.exit(5);
        }
        if (!told) { console.error('waiting for the wallet lock at ' + file + ': no PID available; leaving the file in place'); told = true; }
        await new Promise(s => setTimeout(s, 150 + Math.random() * 150));
        continue;
      }
      if (!alive(pid)) {
        // Without the gate C can erase B's newly published live lock after B
        // removes the original dead holder H. No network/sleep under the gate.
        const result = reapDeadHolder(file, holder, () => !alive(pid));
        if (result.state === 'busy') {
          if (Date.now() - start >= waitMs) {
            console.error('refusing: wallet stale-reaper gate at ' + result.gate +
              ' blocked reclamation of lock file ' + file +
              ' until NANO_LOCK_WAIT_MS. Nothing signed. Neither file was removed. ' +
              'Check all running clients for this wallet and manually delete an orphaned gate file only when no reaper is active.');
            process.exit(5);
          }
          if (!told) {
            console.error('waiting for exclusive wallet stale-reaper gate at ' +
              result.gate + ' beside lock ' + file + '; refusing to steal it');
            told = true;
          }
          await new Promise(s => setTimeout(s, 150 + Math.random() * 150));
          continue;
        }
        if (result.state === 'removed')
          console.error('wallet lock on ' + account + ' is stale (its process is gone); taking it over');
        continue;
      }
      if (!(age < maxMs)) {
        console.error('refusing: wallet lock on ' + account + ' is held by live pid ' + pid + ' for ' + (Number.isFinite(age) ? age + ' ms' : 'an unknown time') + '; NANO_LOCK_MAX_MS=' + maxMs + '. Nothing signed. Inspect the holder; if it is hung, stop it before retrying.');
        process.exit(5);
      }
      if (Date.now() - start >= waitMs) {
        console.error('refusing: waited ' + Math.round(waitMs / 1000) + ' s for the wallet lock on ' + account + ' (pid ' + pid + ' is mid-payment from this account). Nothing signed. Retry later, or give this process its own NANO_INDEX.');
        process.exit(5);
      }
      if (!told) { console.error('waiting for the wallet lock on ' + account + ': pid ' + pid + ' is mid-payment from this account'); told = true; }
      await new Promise(s => setTimeout(s, 150 + Math.random() * 150));
    }
    const release = () => { try { if (fs.readFileSync(file, 'utf8') === mine) fs.unlinkSync(file); } catch { /* not ours any more */ } };
    process.on('exit', release);
    for (const sig of ['SIGINT', 'SIGTERM', 'SIGHUP']) process.on(sig, () => { release(); process.exit(1); });
  })();
}

// The fate of the signed block, read from the account: 'landed' (the frontier is the block, or the chain holds the block
// behind a later one), 'untouched' (the frontier is still block.previous: nothing was broadcast, the same PAYMENT-SIGNATURE
// is still good), 'dead' (the frontier moved to another block and this one is not on the chain: a concurrent payment, a
// receive or a representative change from this wallet landed first; this block can never land and nothing moved from it),
// or null when the account or the block could not be read.
async function fateOf(account, hash, previous) {
  let frontier; try { frontier = String((await accountInfo(account)).frontier || '').toUpperCase(); } catch { return null; }
  return fateAt(frontier, hash, previous);
}
const up = h => String(h || '').toUpperCase();
const realHash = h => typeof h === 'string' && /^[0-9A-Fa-f]{64}$/.test(h) && !/^0+$/.test(h) ? up(h) : null;
// One block as the node knows it: {found: true, confirmed, successor} or {found: false}; null when the answer cannot
// tell. Only the node's own "Block not found" means absent: a loose /not found/ also matched "Account not found", a
// syncing node failing to answer, and any other error (a rate limiter's JSON, an empty object) says nothing either
// way. Read as absent, such an answer told the payer to sign a new block for a payment that had landed (PlatinumVera,
// AI agent, 2026-10-23).
async function blockLookup(hash) {
  try {
    if (RPC) {
      const b = await rpc(RPC, { action: 'block_info', json_block: 'true', hash });
      if (b && b.block_account && !b.error) return { found: true, confirmed: b.confirmed === 'true' || b.confirmed === true, successor: realHash(b.successor) };
      return b && /\bblock not found\b/i.test(String(b.error || '')) ? { found: false } : null;
    }
    const b = await fetch(API + '/v1/verify?hash=' + hash + '&any=1&any_to=1').then(r => r.json());
    if (b && b.found === true) return { found: true, confirmed: b.confirmed === true, successor: realHash(b.successor) };
    return b && b.found === false ? { found: false } : null;
  } catch { return null; }
}
// The same reading from a frontier already in hand, so the pending-payment check and the signing use one account read.
// 'dead' needs proof, not absence: a node that is behind answers "Block not found" for a block that has landed, and a
// frontier older than the block's predecessor differs from both hashes too. The proof is the predecessor's own record:
// it has a successor, the successor is another block, and that block is confirmed. A node that is behind cannot say
// that falsely. Without it the fate is unknown (null).
async function fateAt(frontier, hash, previous) {
  frontier = up(frontier);
  if (!frontier) return null;
  if (frontier === up(hash)) return 'landed';
  if (frontier === up(previous)) return 'untouched';
  const own = await blockLookup(hash);
  if (!own) return null;
  if (own.found) return 'landed';
  const before = await blockLookup(previous);
  if (!before || !before.found || !before.successor || before.successor === up(hash)) return null;
  const after = await blockLookup(before.successor);
  return after && after.found && after.confirmed ? 'dead' : null;
}
async function explainFate(account, hash, previous, lastToken) {
  const fate = await fateOf(account, hash, previous);
  const again = 're-present the same PAYMENT-SIGNATURE for the same call' + (lastToken ? ' with X-Nano-Represent token ' + lastToken + ' (or X-Nano-Payment: ' + hash + ' with X-Nano-Represent: ' + lastToken + ')' : ' (or if the call was handed back, retry with X-Nano-Payment: ' + hash + ' and the X-Nano-Represent token from the reply that handed it back)') + '; do not sign a new block';
  const text = fate === 'landed' ? 'the block is on the chain (hash ' + hash + '): ' + again + ' (pursekeeper.dev replays the reply it bought for ten minutes)'
    : fate === 'untouched' ? 'the account frontier is still ' + previous + ', so the seller did not broadcast the block and nothing moved: ' + again + ' while the frontier stays there'
    : fate === 'dead' ? 'the account frontier moved past ' + previous + ' to another block, not this one (hash ' + hash + '): a concurrent payment, a receive or a representative change from this wallet landed first, so this block can never land and nothing moved from it; sign a new block for this call'
    : 'could not establish from the node whether the block was broadcast; check hash ' + hash + ' before paying again';
  console.error('not served; ' + text);
  return fate;
}

// The unresolved-payment record (see the header). One JSON file per account holding a list of entries
// {hash, previous, url, signed_url, method, body_sha256, amount_raw, pay_to, signed_at[, also_for]}: no signature and no key, so the
// file is not spendable; mode 600 in a mode 700 directory because the URLs are the caller's business. Every change is a
// read-modify-write under an exclusive pending-<account>.json.lock file (held for the few synchronous file calls, no
// network inside), so two processes that do not share the wallet lock (NANO_LOCK=0, different NANO_LOCK_DIR) cannot
// write over each other's entries; the list goes through a temp file and a rename so a crash cannot leave half of it.
// A record that exists but cannot be parsed is never overwritten or skipped: the client refuses with exit 7.
const PENDING_ON = process.env.NANO_PENDING !== '0';
const HOLD_MS = (Number(process.env.NANO_PENDING_HOLD_H) > 0 ? Number(process.env.NANO_PENDING_HOLD_H) : 24) * 3600e3;
const pendingDir = () => process.env.NANO_PENDING_DIR || path.join(os.homedir(), '.pursekeeper');
const pendingFile = account => path.join(pendingDir(), 'pending-' + account + '.json');
const unservedFile = account => path.join(pendingDir(), 'unserved-' + account + '.jsonl');
function readPending(account) {
  let text;
  try { text = fs.readFileSync(pendingFile(account), 'utf8'); } catch (e) { if (e.code === 'ENOENT') return []; throw e; }
  const list = JSON.parse(text);
  if (!Array.isArray(list) || list.some(p => !p || !/^[0-9A-Fa-f]{64}$/.test(String(p.hash)) || !/^[0-9A-Fa-f]{64}$/.test(String(p.previous))))
    throw new Error('not a list of {hash, previous, ...} entries');
  return list;
}
function updatePending(account, change) {
  const file = pendingFile(account), lock = file + '.lock', tmp = file + '.' + process.pid + '.tmp';
  fs.mkdirSync(pendingDir(), { recursive: true, mode: 0o700 });
  for (const t0 = Date.now(); ;) {
    try { fs.closeSync(fs.openSync(lock, 'wx', 0o600)); break; }
    catch (e) {
      if (e.code !== 'EEXIST') throw e;
      if (Date.now() - t0 > 5000) throw new Error(lock + ' has been held for 5 s; if no client is running from this account, remove that file');
      Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, 25);
    }
  }
  try {
    // One entry per block and call. A block signed again on the same frontier for the same quote has the same hash;
    // the URL is not part of a block, so one block can also have been offered for two different calls. While it has
    // not been broadcast it blocks neither. Once it is on the chain it stands against each of them until that call is
    // acknowledged or its own entry runs out its hold, or until one of them is served on it (settlePending, below).
    // The same block sent again for the same call stays one entry and takes the time of the LAST sending: until
    // 0.3.20 the first signed_at was kept, so a block that was refused, sent again later and landed then could be
    // "older than the hold" at once, and the next run paid a second time (found by a reviewing agent, 2026-11-19).
    const at = new Map(), next = [], key = p => [up(p.hash), p.method, p.body_sha256, p.url, p.signed_url].join(' ');
    for (const p of change(readPending(account))) {
      const i = at.get(key(p));
      if (i === undefined) { at.set(key(p), next.length); next.push(p); continue; }
      const had = Date.parse(next[i].signed_at), now = Date.parse(p.signed_at);
      if (Number.isFinite(now) && !(had >= now)) next[i] = { ...next[i], signed_at: p.signed_at };
    }
    if (!next.length) { try { fs.unlinkSync(file); } catch (e) { if (e.code !== 'ENOENT') throw e; } return next; }
    try {
      const fd = fs.openSync(tmp, 'w', 0o600);
      try { fs.writeFileSync(fd, JSON.stringify(next, null, 1) + '\n'); fs.fsyncSync(fd); } finally { fs.closeSync(fd); }
      fs.renameSync(tmp, file);
    } catch (e) { try { fs.unlinkSync(tmp); } catch { /* nothing to clean */ } throw e; }
    try { const d = fs.openSync(pendingDir(), 'r'); try { fs.fsyncSync(d); } finally { fs.closeSync(d); } } catch { /* a directory that cannot be synced */ }
    return next;
  } finally { try { fs.unlinkSync(lock); } catch { /* gone */ } }
}
const pendingRefuse = (text, tail = ' Nothing signed, nothing sent.') => { console.error('refusing: ' + text + tail); process.exit(7); };
// The same call: same method, same body, and the same place (the URL as given or the URL that answered 402, either way
// round, compared without a #fragment and after URL parsing, so HTTP://Host/x and http://host/x are one).
const normUrl = u => { try { const x = new URL(u); x.hash = ''; return x.href; } catch { return String(u); } };
const sameCall = (p, call) => String(p.method || 'GET').toUpperCase() === call.method && p.body_sha256 === call.body_sha256 &&
  [p.url, p.signed_url].some(u => u && call.urls.includes(normUrl(u)));
// Two entries of the record are one call when either is the same call as the other (a call recorded once as given and
// once behind a seller's redirect is two entries and one call).
const callOf = p => ({ method: String(p.method || 'GET').toUpperCase(), body_sha256: p.body_sha256, urls: [p.url, p.signed_url].filter(Boolean).map(normUrl) });
const callLabel = p => p.method + ' ' + p.url;
const alsoFor = p => (Array.isArray(p.also_for) ? p.also_for : []).map(String);
// Called under the wallet lock with the frontier the new block will be signed against. Exits 7 when this same call
// must not be signed again; otherwise returns.
async function reconcilePending(account, frontier, call) {
  const file = pendingFile(account);
  let list;
  try { list = readPending(account); }
  catch (e) { pendingRefuse('the record of unresolved payments at ' + file + ' cannot be read (' + e.message + '). Inspect it; every block it names must be checked on the chain before the file is moved away.'); }
  if (!list.length) return;
  const acked = new Set(String(process.env.NANO_PENDING_ACK || '').split(',').map(up).map(h => h.trim()).filter(Boolean));
  // `drop` holds block hashes and is used only for a block proven dead, which is dead for every call it was offered
  // for. An acknowledgement and the hold release one entry (`gone`: this block for this call) and nothing else: one
  // block can be on record for two calls, it paid for at most one of them, and until 0.3.20 acknowledging it for one
  // call, or the older entry running out its hold, also removed the other call's entry, whose retry then signed a new
  // block with no warning (found by a reviewing agent on 2026-11-19, reproduced, never seen in use).
  // An entry that leaves this way is remembered on the entries of the same block that stay, for other calls, as
  // `also_for`: the block is still one payment for one of those calls, and without the note the entry that stays
  // would be refused as "this call was already paid" from the next run on, which the client does not know.
  const entryKey = p => [up(p.hash), p.method, p.body_sha256, p.url, p.signed_url].join(' ');
  const drop = new Set(), gone = new Set(), left = [], history = [], refusals = [], says = [];
  for (const p of list) {
    const H = up(p.hash), what = 'earlier payment ' + p.hash + ' for ' + p.url;
    const fate = await fateAt(frontier, p.hash, p.previous);
    if (fate === 'dead') { drop.add(H); says.push(what + ' can never land (its predecessor has another confirmed successor); dropped from the record'); continue; }
    if (fate === 'untouched') { says.push(what + ' was signed and never broadcast; the block signed now names the same predecessor, so only one of the two can ever land'); continue; }
    // On the chain, or possibly on the chain (the account moved on and the node could not say). Either way it can no
    // longer land later, so a different call is free to go; this same call is not, until the entry is acknowledged or
    // has stood NANO_PENDING_HOLD_H hours (default 24), after which it is history.
    const state = fate === 'landed' ? 'is on the chain' : 'may be on the chain (the node could not say)';
    const age = Date.now() - Date.parse(p.signed_at);
    const same = sameCall(p, call), ack = same && acked.has(H);   // an acknowledgement is for the call being made now
    if (ack || (Number.isFinite(age) && age >= HOLD_MS)) {
      gone.add(entryKey(p)); left.push(p); history.push({ ...p, fate: fate || 'unknown', acknowledged: ack, noted_at: new Date().toISOString() });
      says.push(what + ' ' + state + (ack ? '; acknowledged with NANO_PENDING_ACK' : '; older than the hold') + ', moved to ' + unservedFile(account));
      continue;
    }
    if (!same) { says.push(what + ' ' + state + ' and that run was not served; it stays on record' + (acked.has(H) ? ' (NANO_PENDING_ACK names its block, but an acknowledgement covers the call being made, and this entry is for another call)' : '')); continue; }
    // The same block on record for other calls too, now or until an earlier run released them: it is one payment, so
    // "this call was paid" is not known. Another entry for this same call (as given, and behind a redirect) is not
    // another call.
    const also = [...new Set([...list.filter(q => up(q.hash) === H && !sameCall(q, call)).map(callLabel), ...alsoFor(p)])];
    refusals.push(fate === 'landed' && also.length
      ? 'this call may already be paid. Block ' + p.hash + ' (' + Number(p.amount_raw) / 1e30 + ' NANO to ' + p.pay_to + ', signed ' + p.signed_at + ') is on the chain. It was signed for ' + p.method + ' ' + p.url + ' with this body and the same block was also on record for ' + also.join(' and for ') + '; a block is one payment, so it paid for one of these calls, and none of those runs was served on it. Re-present it for this call (the same request with the same PAYMENT-SIGNATURE header, or the block hash by whatever route the seller documents). If the seller answers that the block is spent, it bought the other call: then set NANO_PENDING_ACK=' + p.hash + ' to pay for this one. The acknowledgement releases this call only.'
      : fate === 'landed'
      ? 'this call was already paid. Block ' + p.hash + ' (' + Number(p.amount_raw) / 1e30 + ' NANO to ' + p.pay_to + ', signed ' + p.signed_at + ') is on the chain and paid for ' + p.method + ' ' + p.url + ' with this body, and that run was not served. Re-present that payment instead of signing a new one: send the same request with the same PAYMENT-SIGNATURE header (the file NANO_SAVE_PAYLOAD wrote, if it was set), or give the seller the block hash by whatever route it documents. To pay for the call a second time on purpose, set NANO_PENDING_ACK=' + p.hash + '.'
      : 'this call may already be paid. Block ' + p.hash + ' was signed for ' + p.method + ' ' + p.url + ' with this body on ' + p.signed_at + ', the account has moved on since, and the node could not say whether that block is on the chain. Signing now could pay twice. Retry when the node answers, or look the block up yourself and then set NANO_PENDING_ACK=' + p.hash + '.');
  }
  try {
    if (history.length) {
      fs.mkdirSync(pendingDir(), { recursive: true, mode: 0o700 });
      const fd = fs.openSync(unservedFile(account), 'a', 0o600);
      try { for (const h of history) fs.writeSync(fd, JSON.stringify(h) + '\n'); } finally { fs.closeSync(fd); }
    }
    if (drop.size || gone.size) updatePending(account, cur => cur.filter(p => !drop.has(up(p.hash)) && !gone.has(entryKey(p))).map(p => {
      const more = left.filter(q => up(q.hash) === up(p.hash) && !sameCall(q, callOf(p))).map(callLabel);
      return more.length ? { ...p, also_for: [...new Set([...alsoFor(p), ...more])] } : p;
    }));
  } catch (e) { pendingRefuse('the record of unresolved payments at ' + file + ' cannot be updated (' + e.message + ').'); }
  for (const line of says) console.error(line);
  if (refusals.length) pendingRefuse(refusals[0]);
}

// The proof file holds a signed block, so it is written only where this process controls the bits. A new file is created
// here with mode 600 (`mode` applies only on creation; ClawHub's scanner on skill 0.3.5, 2026-10-20). A file that already
// exists gets chmod 600 first and is written only if that succeeded: when the mode cannot be set, the path names a file
// this process does not own (or a symlink to one), so the payload goes to a fresh file beside it, <path>.1, .2, ..., created
// here so the 600 applies, and the stderr line names that file (pyfile-toolkit, 2026-10-21). If nothing can be written the
// error is printed and the client carries on: the exit code reports the paid call, not the proof.
function savePayload(file, body) {
  const create = (p) => { const fd = fs.openSync(p, 'wx', 0o600); try { fs.writeFileSync(fd, body); } finally { fs.closeSync(fd); } return p; };
  try {
    try { return create(file); } catch (e) { if (e.code !== 'EEXIST') throw e; }
    let modeErr;
    try { fs.chmodSync(file, 0o600); } catch (e) { modeErr = e; }
    if (!modeErr) { fs.writeFileSync(file, body); return file; }
    for (let i = 1; i <= 99; i++) {
      try {
        const alt = create(file + '.' + i);
        console.error('could not set mode 600 on ' + file + ': ' + modeErr.message + '; payload written to ' + alt + ' instead');
        return alt;
      } catch (e) { if (e.code !== 'EEXIST') throw e; }
    }
    throw modeErr;
  } catch (e) {
    console.error('payment header NOT saved to ' + file + ': ' + e.message);
    return null;
  }
}

(async () => {
  if (!process.env.NANO_SEED) { console.error('set NANO_SEED (64 hex chars)'); process.exit(2); }
  const sk = N.deriveSecretKey(process.env.NANO_SEED, Number(process.env.NANO_INDEX || 0));
  const account = N.deriveAddress(N.derivePublicKey(sk), { useNanoPrefix: true });
  console.error('paying from', account);

  // HEADERS: a JSON object of extra request headers, e.g. HEADERS='{"authorization":"Bearer ..."}'. Keys are
  // lowercased first: fetch joins case variants of one name with ", " instead of replacing, so a caller's
  // "Content-Type" used to arrive glued to the script's content-type, and a caller's "Payment-Signature"
  // glued to the real payload (pyfile-toolkit, pursekeeper/skill#4, 2026-09-28). The caller's content-type
  // wins over the default; the payment header is always the script's own.
  const extraHeaders = Object.fromEntries(Object.entries(process.env.HEADERS ? JSON.parse(process.env.HEADERS) : {}).map(([k, v]) => [k.toLowerCase(), v]));
  delete extraHeaders['payment-signature']; delete extraHeaders['x-payment'];
  const reqInit = () => ({ method: process.env.METHOD || 'GET', body: process.env.BODY, headers: { ...(process.env.BODY ? { 'content-type': 'application/json' } : {}), ...extraHeaders } });
  // The caller's HEADERS were given for `url`, and no header reaches another origin. fetch's own redirect walk drops
  // authorization, cookie and proxy-authorization on a cross-origin hop but carries every other name (an x-api-key, a
  // custom token), and until 0.3.12 the signed request re-attached all of them to the URL that answered 402, so a seller
  // whose quote redirected to another origin handed that origin the caller's credential for the first one (ClawHub's
  // scanner on 0.3.11, 2026-10-22, rule T09). Always walk unsigned quote redirects manually: only the original origin
  // is trusted, regardless of whether HEADERS are set. Within that origin keep the same method, body and headers for up
  // to 20 hops; refuse a different origin before making any request there or signing anything.
  const quoteOrigin = new URL(url).origin;
  const quote = async () => {
    let current = url;
    for (let hops = 0; hops < 20; hops++) {
      const r = await fetch(current, { ...reqInit(), redirect: 'manual' });
      const location = r.status >= 300 && r.status < 400 ? r.headers.get('location') : null;
      if (!location) return r;
      let next; try { next = new URL(location, current); } catch { return r; }
      if (next.origin !== quoteOrigin) {
        console.error(`refusing: the unsigned quote at ${current} redirected (HTTP ${r.status}) to ${next.origin}, another origin. Cross-origin redirects are refused even when HEADERS are absent; nothing was sent to ${next.origin} and nothing was signed. To proceed, run the client with the final URL and only the headers intended for that origin.`);
        process.exit(6);
      }
      current = next.href;
    }
    throw new Error('the quote redirected more than 20 times within ' + quoteOrigin);
  };
  const first = await quote();
  if (first.status !== 402) { console.log(first.status, await first.text()); if (first.status < 200 || first.status >= 300) process.exitCode = 1; return; }
  const hdr = first.headers.get('payment-required');
  const pr = hdr ? unb64(hdr) : (await first.json()).x402;
  if (!pr || pr.x402Version !== 2) throw new Error('no x402 v2 PaymentRequired in the 402');
  const accepted = Array.isArray(pr.accepts) && pr.accepts.find(a => a && a.scheme === 'exact' && a.network === 'nano:mainnet');
  if (!accepted) throw new Error('seller does not accept exact on nano:mainnet: ' + JSON.stringify(pr.accepts));
  // The 402's resource is echoed verbatim into the payment header, and a facilitator that parses with @x402/core refuses
  // the whole payment when it breaks the x402 v2 ResourceInfo caps (serviceName and each tag: 1-32 printable ASCII
  // characters; at most 5 tags; iconUrl at most 2048). Checked here before anything is signed, so a seller's typo does not
  // cost the payer a signed block (Ops Control HQ page-extract, serviceName 34 characters, refused invalid_block, 2026-10-18).
  const resourceFault = resourceInfoFault(pr.resource);
  if (resourceFault) {
    console.error(`refusing: the seller's 402 resource fails the x402 v2 ResourceInfo schema (${resourceFault}); a facilitator would refuse the payment as invalid_block, so nothing is signed. Tell the seller.`);
    process.exit(4);
  }
  const quoteFault = acceptedFault(accepted);
  if (quoteFault) {
    console.error(`refusing: the seller's 402 quote fails the Nano exact schema (${quoteFault}); a facilitator would refuse the payment as invalid_block, so nothing is signed. Tell the seller.`);
    process.exit(4);
  }
  console.error(`seller wants ${accepted.amount} raw (${Number(accepted.amount) / 1e30} NANO) to ${accepted.payTo}`);
  // Spending cap. A 402 is a stranger's quote; never sign for more than you decided beforehand.
  // NANO_MAX_PAY is in NANO (default 0.01). Set it higher on purpose, per run, when you mean it.
  // Parsed as decimal text straight to raw, the way no-node.js parses amounts, never through a float:
  // 0.1.1 rounded the cap to millionths, so a cap below 0.000001 became zero and refused everything,
  // and a value that was not a number threw a BigInt RangeError instead of using the default
  // (both reported by pyfile-toolkit, pursekeeper/skill#1, 2026-09-26).
  const toRaw = s => { const m = /^(\d+)(?:\.(\d{1,30}))?$/.exec(s); return m ? BigInt(m[1]) * 10n ** 30n + BigInt((m[2] || '').padEnd(30, '0')) : null; };
  const capText = (process.env.NANO_MAX_PAY || '').trim();
  let capShown = capText, maxRaw = capText ? toRaw(capText) : null;
  if (maxRaw === null) {
    if (capText) console.error(`NANO_MAX_PAY=${JSON.stringify(capText)} is not a decimal NANO amount (digits, optionally a point and up to 30 decimals); using the default 0.01`);
    capShown = '0.01'; maxRaw = toRaw(capShown);
  }
  if (BigInt(accepted.amount) > maxRaw) {
    console.error(`refusing: quote ${Number(accepted.amount) / 1e30} NANO (${accepted.amount} raw) is above NANO_MAX_PAY (${capShown} NANO = ${maxRaw} raw). Nothing signed.`);
    process.exit(3);
  }

  await walletLock(account);   // from here until exit this process is the account's only writer on this host
  const info = await accountInfo(account);
  if (info.error) throw new Error('account_info: ' + info.error + ' (is the account opened and funded?)');
  // Earlier payments from this account whose fate was not settled when their process exited are settled here, against
  // the same frontier the new block is about to name (see the header). May exit 7.
  const signedUrl = first.url || url;   // the unsigned quote may have followed a seller's canonical redirect
  const call = { urls: [...new Set([normUrl(url), normUrl(signedUrl)])], method: String(process.env.METHOD || 'GET').toUpperCase(), body_sha256: createHash('sha256').update(process.env.BODY || '').digest('hex') };
  if (PENDING_ON) await reconcilePending(account, info.frontier, call);
  const balance = BigInt(info.balance) - BigInt(accepted.amount);
  if (balance < 0n) throw new Error(`insufficient balance: have ${info.balance} raw`);

  // Sellers that advertise extra.workOptional = true (the scheme draft's name) or extra.work = 'optional' (this
  // seller's older name, still sent) compute the work themselves (work is not signed, so the seller can add it):
  // send "0" and skip the wait. Set FORCE_WORK=1 to opt out.
  const sellerWork = !!accepted.extra && (accepted.extra.workOptional === true || accepted.extra.work === 'optional') && !process.env.FORCE_WORK;
  const w = sellerWork ? '0' : await work(info.frontier, new URL(url).origin);
  if (sellerWork) console.error('seller computes the work; skipping work_generate');
  const { block, hash } = N.createBlock(sk, { work: w, previous: info.frontier, representative: info.representative, balance: balance.toString(), link: accepted.payTo });
  block.account = block.account.replace(/^xrb_/, 'nano_');
  console.error('signed block', hash);

  const payload = { x402Version: 2, resource: pr.resource, accepted, payload: { block } };
  // Send the signature only to the URL that answered 402 (signedUrl, above).
  const init = reqInit(); init.headers['payment-signature'] = b64(payload);   // header names are case-insensitive; lowercase keeps the map free of case variants
  init.redirect = 'manual';   // never let a paid redirect forward this signed, spendable block to another URL
  // A transport failure after the payment was sent (the seller went away mid-call, a timeout) is not an error to report
  // and stop at: the block may be on the chain. Its fate is read from the account below, like any other unserved outcome.
  // The record goes to disk before the signed request leaves the process: if it cannot be written the block stays here.
  const entry = { hash, previous: up(info.frontier), url: normUrl(url), signed_url: normUrl(signedUrl), method: call.method, body_sha256: call.body_sha256, amount_raw: accepted.amount, pay_to: accepted.payTo, signed_at: new Date().toISOString() };
  if (PENDING_ON) {
    try { updatePending(account, cur => [...cur, entry]); }
    catch (e) { pendingRefuse('the record of unresolved payments cannot be written to ' + pendingFile(account) + ' (' + e.message + '). Point NANO_PENDING_DIR at a directory this process can write and that survives a restart.', ' The block signed above was not sent and is discarded.'); }
  }
  const settlePending = fate => {
    if (!PENDING_ON) return;
    try {
      if (fate === 'served' || fate === 'dead') {
        // By hash: every entry of this block goes. Dead, because the block can never land for any call. Served, because
        // the one payment this block can make has bought this call, so another call it was offered for is unpaid;
        // that is said out loud, since the earlier run told its caller to re-present this block for that call.
        // Another entry for this same call (recorded as given, and behind a redirect) is not another call.
        let others = [];
        updatePending(account, cur => { others = cur.filter(p => up(p.hash) === up(hash) && !sameCall(p, call)); return cur.filter(p => up(p.hash) !== up(hash)); });
        if (fate === 'served') for (const p of others)
          console.error('block ' + hash + ' was also on record for ' + p.method + ' ' + p.url + ' (signed ' + p.signed_at + ', not served then). A block is one payment and it has now bought the call just served, so that other call has not been paid for: its entry is dropped, and re-presenting this block for it will not work at a seller that sells one call per block');
      } else console.error('unresolved payment ' + hash + ' recorded in ' + pendingFile(account) + '; the next run from this account settles it before signing for this call again');
    } catch (e) { console.error('could not update ' + pendingFile(account) + ': ' + e.message + ' (the entry for ' + hash + ' stays; the next run reads its fate from the chain)'); }
  };
  const lost = e => { console.error('no reply from the seller after the payment was sent: ' + e.message); return null; };
  const signedFetch = () => fetch(signedUrl, init).catch(lost);
  const noteSignedRedirect = response => {
    if (!response || response.status < 300 || response.status >= 400) return;
    const location = response.headers.get('location');
    let locationOrigin = '(no Location)';
    if (location) {
      try { locationOrigin = new URL(location, signedUrl).origin; }
      catch { locationOrigin = '(invalid Location)'; }
    }
    console.error(`signed redirect refused: HTTP ${response.status}; Location origin ${locationOrigin}; PAYMENT-SIGNATURE was not forwarded to the redirect target`);
  };
  let r = await signedFetch();
  noteSignedRedirect(r);
  // A 402 after the payment whose note says the block was broadcast but not yet confirmed (pursekeeper.dev waits 8 s for
  // confirmation before serving, since 2026-09-29): the block is on the chain, so re-present the same payload for up to a
  // minute. Never sign a new block here: the frontier has moved to the pending block and a new send would pay twice.
  // The seller may word a later 402 differently while the block is still unconfirmed (pursekeeper.dev's alreadyLanded gate
  // said "on the node but not confirmed yet" with no token until 2026-10-03, and the loop stopped on it: PlatinumVera,
  // 2026-10-03), so any "not confirmed" wording keeps the loop going.
  let lastToken = null;
  for (let waited = 0; r && r.status === 402 && waited < 60_000; waited += 2000) {
    const b = await r.clone().json().catch(() => null);
    if (!b || !/not (yet )?confirmed/.test(String(b.note || b.error || ''))) break;
    // The 402 carries a single-use token (since 2026-09-29 16:xx UTC) that binds the re-presentation to this client: the
    // block is public on the chain from the broadcast, so without it anyone could present the same block and be served.
    const tok = r.headers.get('x-nano-represent') || (b && b.represent_token);
    // The token is single-use and init is reused by this loop, so a 402 that carries no token must clear the previous one
    // rather than re-present it spent (pyfile-toolkit, 2026-10-02; pursekeeper.dev sends the token with every such 402 to
    // its holder, so the branch is for other sellers). The last token seen is kept for the stderr line below.
    if (tok) { init.headers['x-nano-represent'] = String(tok); lastToken = String(tok); } else delete init.headers['x-nano-represent'];
    console.error('block ' + hash + ' broadcast, not yet confirmed; re-presenting the same payment');
    await new Promise(s => setTimeout(s, 2000));
    r = await signedFetch();
    noteSignedRedirect(r);
  }
  if (r) {
    const repTok = r.headers.get('x-nano-represent');
    if (repTok) lastToken = String(repTok);
    const settle = r.headers.get('payment-response');
    if (settle) { try { console.error('settlement:', unb64(settle)); } catch { console.error('settlement header present but not base64 JSON'); } }
    // x-nano-replay: true marks a reply served again from the seller's ten-minute replay cache (the same payment, method, URL
    // and body re-presented after a lost reply); it is the reply that was paid for, not a refusal.
    if (r.headers.get('x-nano-replay') === 'true') console.error('reply served again from the seller\'s replay cache (x-nano-replay: true)');
    console.log(r.status, await r.text());
  }
  const served = !!r && r.status >= 200 && r.status < 300;
  if (process.env.NANO_SAVE_PAYLOAD) {
    const out = { saved_at: new Date().toISOString(), url: signedUrl, method: init.method || 'GET', hash, status: r ? r.status : null, served, represent_token: lastToken, payment_signature: init.headers['payment-signature'] };
    const where = savePayload(process.env.NANO_SAVE_PAYLOAD, JSON.stringify(out, null, 1) + '\n');
    if (where) console.error('payment header saved to ' + where + (served ? '' : ' (not served; the signed block inside is still spendable until the account\'s frontier moves)'));
    else if (!served) console.error('the signed block was not saved anywhere; it is still spendable until the account\'s frontier moves');
  }
  // Anything but 2xx after the payment means the call was not served: exit 1, so a caller that reads only the return code
  // does not count an unserved call as done (pyfile-toolkit, 2026-10-02). The body printed above is the seller's last answer;
  // for a not-yet-confirmed 402 it carries the X-Nano-Represent token to re-present the same block with later. What the
  // payer then needs is the fate of the block, read from the account rather than assumed (PlatinumVera, 2026-10-03;
  // pyfile-toolkit /web/search, 2026-10-05): landed or untouched means re-present the same payment, dead means sign anew.
  // Until 2026-10-18 a frontier that was neither the block nor its previous was reported as "still <frontier>, nothing
  // moved, re-present", which for a block overtaken by a concurrent writer is advice that can never work (api#90).
  if (!served) {
    process.exitCode = 1;
    settlePending(await explainFate(account, hash, String(info.frontier), lastToken));
  } else settlePending('served');
})().catch(e => { console.error('error:', e.message); process.exit(1); });
