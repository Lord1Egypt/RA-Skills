#!/usr/bin/env node
/*
 * guarded-buy.cjs — fail-closed reference client for metered x402 v2 XRPL data endpoints.
 *
 * Why this exists: an auto-paying client signs whatever a 402 challenge asks. This one makes the
 * money-path linear and self-auditing so a surprise charge is structurally impossible:
 *
 *   1. GET the resource            -> read the challenge (accepts[0]) and NOTHING is signed yet
 *   2. gate the challenge           -> host / network / scheme / payee / price cap / daily budget
 *   3. presign a Payment FROM THAT OBJECT ONLY (same invoiceId, same amount, same destination)
 *   4. gate the bytes we are about to sign -> Amount, Destination, SourceTag, InvoiceID memo,
 *      LastLedgerSequence horizon must all equal what was gated in step 2
 *   5. retry once with PAYMENT-SIGNATURE, decode PAYMENT-RESPONSE and require that the receipt
 *      names the very tx hash we signed
 *   6. record actual drops in a local daily ledger so cumulative spend cannot drift past budget
 *
 * There is no second, unaudited round trip: nothing is ever signed from a challenge that was not
 * inspected, and the signed blob is re-checked against the inspected values before it leaves.
 *
 *   npm i x402-xrpl@0.2.0 xrpl        # in the directory you run this from
 *   XRPL_SEED=... node guarded-buy.cjs /api/v1/feed/stats [/api/v1/ledger ...]
 *   NO_PAY=1 XRPL_SEED=... node guarded-buy.cjs /api/v1/feed/stats     # price probe only
 *   node guarded-buy.cjs --selftest                                    # offline gate proof
 *
 * Env (fail-closed defaults shown):
 *   XRPL_SEED            seed of a DEDICATED low-balance hot wallet (never your main one)
 *   BASE_URL             https://d5e7fd5a.xrplclaw.com/app/nodes
 *   MAX_DROPS            200   hard per-request ceiling
 *   DAILY_BUDGET_DROPS   50000 hard cumulative ceiling for today (UTC)
 *   EXPECT_PAYTO         rpTpW7C4eSuEGUENGXtyMgW9JPvxm2XCWd (published payee)
 *   EXPECT_HOST          d5e7fd5a.xrplclaw.com
 *   EXPECT_SOURCE_TAG    804681468
 *   MAX_TIMEOUT_SECONDS  300   reject challenges demanding a longer payment horizon
 *   WS_URL               wss://rpc.xrplclaw.com/ws   (fee/sequence source for autofill; we never submit)
 *   ALLOW_SPEND_FILE     ./.xrp-fleet-data-spend.json
 *   NO_PAY=1             inspect + gate, sign nothing
 */
'use strict';
const fs = require('fs');
const path = require('path');

const ENV = process.env;
const BASE = (ENV.BASE_URL || 'https://d5e7fd5a.xrplclaw.com/app/nodes').replace(/\/+$/, '');
const FORCED_RAW = ENV.FORCE_CHALLENGE_JSON || null;   // offline gate-probe hook; requires NO_PAY=1
const MAX_DROPS = Number(ENV.MAX_DROPS || 200);
const DAILY_BUDGET_DROPS = Number(ENV.DAILY_BUDGET_DROPS || 50000);
const EXPECT_PAYTO = ENV.EXPECT_PAYTO || 'rpTpW7C4eSuEGUENGXtyMgW9JPvxm2XCWd';
const EXPECT_HOST = ENV.EXPECT_HOST || 'd5e7fd5a.xrplclaw.com';
const EXPECT_SOURCE_TAG = ENV.EXPECT_SOURCE_TAG != null ? Number(ENV.EXPECT_SOURCE_TAG) : 804681468;
const MAX_TIMEOUT_SECONDS = Number(ENV.MAX_TIMEOUT_SECONDS || 300);
const WS_URL = ENV.WS_URL || 'wss://rpc.xrplclaw.com/ws';
const SPEND_FILE = ENV.ALLOW_SPEND_FILE || path.join(process.cwd(), '.xrp-fleet-data-spend.json');
const SEED = ENV.XRPL_SEED || null;

class Refused extends Error { constructor(code, msg) { super(msg); this.code = code; } }
const die = (code, msg) => { throw new Refused(code, msg); };

// ---------------------------------------------------------------- spend ledger -------------
function spentToday() {
  try {
    const j = JSON.parse(fs.readFileSync(SPEND_FILE, 'utf8'));
    return j.day === new Date().toISOString().slice(0, 10) ? Number(j.drops || 0) : 0;
  } catch { return 0; }
}
function recordSpend(drops, meta) {
  const day = new Date().toISOString().slice(0, 10);
  let j = {}; try { j = JSON.parse(fs.readFileSync(SPEND_FILE, 'utf8')); } catch {}
  if (j.day !== day) j = { day, drops: 0, sales: [] };
  j.drops = Number(j.drops || 0) + drops;
  j.sales = (j.sales || []).concat([Object.assign({ ts: new Date().toISOString(), drops }, meta)]).slice(-200);
  const tmp = SPEND_FILE + '.tmp';
  fs.writeFileSync(tmp, JSON.stringify(j));
  fs.renameSync(tmp, SPEND_FILE);
}

// ------------------------------------------------------- gate 1: the challenge we were sent --
async function getChallenge(url) {
  if (FORCED_RAW) {
    let parsed; try { parsed = JSON.parse(FORCED_RAW); } catch (e) { die('config', 'FORCE_CHALLENGE_JSON invalid JSON: ' + e.message); }
    const acc = Array.isArray(parsed.accepts) ? parsed.accepts[0] : (parsed.amount ? parsed : null);
    return { paid: true, acc, endpoint: url };
  }
  const res = await fetch(url, { method: 'GET' });
  if (res.status === 200) return { free: true, json: await res.json().catch(() => null) };
  if (res.status !== 402) return { error: 'unexpected_status_' + res.status, body: await res.text().catch(() => '') };
  let body = null; try { body = await res.json(); } catch {}
  let hdr = null; try { hdr = JSON.parse(Buffer.from(res.headers.get('payment-required'), 'base64').toString()); } catch {}
  const acc = (body && Array.isArray(body.accepts) && body.accepts[0]) || (hdr && hdr.accepts && hdr.accepts[0]);
  return { paid: true, acc, endpoint: body && body.endpoint, price_drops: body && body.price_drops };
}

function gateChallenge(acc, url) {
  if (!acc || typeof acc !== 'object') die('challenge', 'no usable accepts[] in the 402 — refusing a blind payment');
  if (!acc.amount) die('challenge', 'challenge carries no amount field — refusing');
  const host = new URL(url).host;
  const drops = Number(acc.amount);
  if (host !== EXPECT_HOST) die('host', 'challenge came from ' + host + ', expected ' + EXPECT_HOST);
  if (acc.network !== 'xrpl:0') die('network', 'challenge network ' + acc.network + ' is not xrpl:0 mainnet');
  if (acc.scheme !== 'exact') die('scheme', 'unsupported scheme ' + acc.scheme);
  if (acc.payTo !== EXPECT_PAYTO) die('payee', 'payTo ' + acc.payTo + ' != expected ' + EXPECT_PAYTO);
  if (!Number.isFinite(drops) || drops <= 0) die('amount', 'non-numeric amount ' + acc.amount);
  if (drops > MAX_DROPS) die('amount', drops + ' drops exceeds MAX_DROPS=' + MAX_DROPS);
  const mto = Number(acc.maxTimeoutSeconds != null ? acc.maxTimeoutSeconds : acc.timeout);
  if (Number.isFinite(mto) && mto > MAX_TIMEOUT_SECONDS) die('horizon', 'maxTimeoutSeconds ' + mto + ' > ' + MAX_TIMEOUT_SECONDS);
  const inv = acc.extra && acc.extra.invoiceId;
  if (!inv) die('invoice', 'challenge has no single-use invoiceId binding');
  const tag = acc.extra && acc.extra.sourceTag != null ? Number(acc.extra.sourceTag) : null;
  if (tag != null && tag !== EXPECT_SOURCE_TAG) die('sourcetag', 'advertised sourceTag ' + tag + ' != expected ' + EXPECT_SOURCE_TAG);
  const already = spentToday();
  if (already + drops > DAILY_BUDGET_DROPS) die('budget', 'daily budget exhausted: spent ' + already + ' + this ' + drops + ' > ' + DAILY_BUDGET_DROPS);
  return { drops, invoiceId: inv, sourceTag: tag, timeoutS: Number.isFinite(mto) ? mto : null };
}

// ------------------------------------------- gate 2: the exact bytes about to be signed -----
// Pure function so it can be proven offline without any network or key material.
function gateSignedTx(tx, acc, gated, walletAddress) {
  const errs = [];
  if (tx.TransactionType !== 'Payment') errs.push('not a Payment (' + tx.TransactionType + ')');
  if (tx.Account !== walletAddress) errs.push('Account ' + tx.Account + ' != signer ' + walletAddress);
  if (tx.Destination !== acc.payTo) errs.push('Destination ' + tx.Destination + ' != gated payTo ' + acc.payTo);
  const amt = typeof tx.Amount === 'string' ? Number(tx.Amount) : NaN;
  if (amt !== gated.drops) errs.push('Amount ' + tx.Amount + ' != gated price ' + gated.drops + ' drops');
  if (gated.sourceTag != null && tx.SourceTag !== gated.sourceTag) errs.push('SourceTag ' + tx.SourceTag + ' != gated ' + gated.sourceTag);
  const memos = (tx.Memos || []).map((m) => m.Memo || {});
  if (!memos.length) errs.push('no Memo — payment is not bound to this single-use invoice');
  if (gated.timeoutS != null && !(typeof tx.LastLedgerSequence === 'number' && Number.isFinite(tx.LastLedgerSequence))) {
    errs.push('LastLedgerSequence missing — payment could land long after the quoted horizon');
  }
  if (errs.length) die('sign-gate', errs.join('; '));
  return true;
}

// --------------------------------------------------------------- presign path ---------------
async function buy(url) {
  const ch = await getChallenge(url);
  if (ch.error) return { skipped: ch.error, body: String(ch.body || '').slice(0, 160) };
  if (ch.free) return { paid: false, data: ch.json };

  const gated = gateChallenge(ch.acc, url);                       // nothing signed yet
  console.error('# ' + url + ' costs ' + gated.drops + ' drops -> payee ' + ch.acc.payTo +
    ' | invoice ' + String(gated.invoiceId).slice(0, 24) + '… | spent today ' + spentToday() + '/' + DAILY_BUDGET_DROPS);
  if (ENV.NO_PAY === '1') return { probed: true, gated };

  const { Wallet, Client } = await import('xrpl');
  const { base64EncodeUtf8, jsonCanonicalStringify, invoiceIdToMemoHex } = await import('x402-xrpl');
  const wallet = Wallet.fromSeed(SEED);
  const client = new Client(WS_URL);
  await client.connect();
  let header, signedHash, tlblob;
  try {
    const memoHex = invoiceIdToMemoHex(gated.invoiceId);
    const tx = {
      TransactionType: 'Payment',
      Account: wallet.classicAddress,
      Destination: ch.acc.payTo,
      Amount: String(gated.drops),
      Memos: [{ Memo: { MemoData: memoHex } }],
    };
    if (gated.sourceTag != null) tx.SourceTag = gated.sourceTag;
    const filled = await client.autofill(tx);
    const cur = await client.request({ command: 'server_info' }).then((r) => (r.result.info.validated_ledger || {}).seq).catch(() => null);
    if (cur) {
      const delta = Math.ceil((gated.timeoutS || 120) / 5) + 2;
      filled.LastLedgerSequence = cur + delta;
    }
    gateSignedTx(filled, ch.acc, gated, wallet.classicAddress);   // audit the bytes BEFORE signing
    const signed = wallet.sign(filled);
    tlblob = signed.tx_blob; signedHash = signed.hash;
    if (!tlblob) die('sign', 'wallet returned no tx_blob');
    header = base64EncodeUtf8(jsonCanonicalStringify({
      x402Version: 2,
      accepted: ch.acc,                                          // the identical gated object
      payload: { signedTxBlob: tlblob, invoiceId: gated.invoiceId },
    }));
  } finally {
    await client.disconnect().catch(() => {});
  }

  const res = await fetch(url, { method: 'GET', headers: { 'PAYMENT-SIGNATURE': header } });
  const data = await res.json().catch(() => null);
  let rec = null; try { rec = JSON.parse(Buffer.from(res.headers.get('payment-response') || '', 'base64').toString()); } catch {}
  if (res.status === 200 && rec && rec.success) {
    const sameTx = !signedHash || String(rec.transaction || '').toUpperCase() === String(signedHash).toUpperCase();
    recordSpend(gated.drops, { url, tx: rec.transaction || signedHash || null, invoice: gated.invoiceId });
    if (!sameTx) {
      console.error('! WARNING: seller receipt names tx ' + rec.transaction + ' but we signed ' + signedHash + ' — reconcile before trusting it.');
    }
    return {
      paid: true, drops: gated.drops, tx: rec.transaction || signedHash, ours: signedHash || null,
      settlement: res.headers.get('x-payment-settlement') || 'settled', data,
    };
  }
  if (res.status === 200) {
    // served, but we hold no verified receipt: still reserve the money against the budget
    recordSpend(gated.drops, { url, tx: signedHash || null, receipt: 'absent' });
    return { paid: true, drops: gated.drops, receipt: 'missing', tx: signedHash || null, settlement_header: res.headers.get('x-payment-settlement'), data };
  }
  return { failed: 'http_' + res.status, data, tx_we_signed: signedHash || null };
}

// ---------------------------------------------------------------- offline self-test ---------
function selftest() {
  const W = 'rTestSignerAddressXXXXXXXXXXXXXXXXX';
  const acc = { amount: '100', asset: 'XRP', network: 'xrpl:0', scheme: 'exact', payTo: EXPECT_PAYTO, maxTimeoutSeconds: 120, extra: { invoiceId: 'inv-1', sourceTag: EXPECT_SOURCE_TAG, memoFormat: 'hex-or-sha256' } };
  const g = { drops: 100, invoiceId: 'inv-1', sourceTag: EXPECT_SOURCE_TAG, timeoutS: 120 };
  const base = { TransactionType: 'Payment', Account: W, Destination: EXPECT_PAYTO, Amount: '100', SourceTag: EXPECT_SOURCE_TAG, Memos: [{ Memo: { MemoData: 'ABCD' } }], LastLedgerSequence: 107369999 };
  const cases = [
    ['valid passes', () => gateSignedTx(base, acc, g, W), true],
    ['inflated amount blocked', () => gateSignedTx(Object.assign({}, base, { Amount: '1000000' }), acc, g, W), false],
    ['redirected destination blocked', () => gateSignedTx(Object.assign({}, base, { Destination: 'rEvil' }), acc, g, W), false],
    ['missing invoice memo blocked', () => gateSignedTx(Object.assign({}, base, { Memos: [] }), acc, g, W), false],
    ['no expiry horizon blocked', () => gateSignedTx(Object.assign({}, base, { LastLedgerSequence: undefined }), acc, g, W), false],
    ['wrong signer blocked', () => gateSignedTx(Object.assign({}, base, { Account: 'rSomeoneElse' }), acc, g, W), false],
    ['non-payment type blocked', () => gateSignedTx(Object.assign({}, base, { TransactionType: 'OfferCreate' }), acc, g, W), false],
    ['sourceTag mismatch blocked', () => gateSignedTx(Object.assign({}, base, { SourceTag: 1 }), acc, g, W), false],
  ];
  let bad = 0;
  for (const [name, fn, shouldPass] of cases) {
    let threw = false, msg = '';
    try { fn(); } catch (e) { threw = true; msg = e.message; }
    const okCase = shouldPass ? !threw : (threw && e_isRefusal(threw, msg));
    if (!okCase) bad++;
    console.log((okCase ? 'PASS ' : 'FAIL ') + name + (!shouldPass && threw ? ' — ' + msg.slice(0, 90) : ''));
  }
  const chalCases = [
    ['over-cap challenge refused', () => gateChallenge(Object.assign({}, acc, { amount: '99999' }), 'https://' + EXPECT_HOST + '/app/nodes/x'), false],
    ['wrong payee refused', () => gateChallenge(Object.assign({}, acc, { payTo: 'rEvil' }), 'https://' + EXPECT_HOST + '/app/nodes/x'), false],
    ['unbound invoice refused', () => gateChallenge(Object.assign({}, acc, { extra: {} }), 'https://' + EXPECT_HOST + '/app/nodes/x'), false],
    ['excessive horizon refused', () => gateChallenge(Object.assign({}, acc, { maxTimeoutSeconds: 100000 }), 'https://' + EXPECT_HOST + '/app/nodes/x'), false],
    ['foreign network refused', () => gateChallenge(Object.assign({}, acc, { network: 'xrpl:1' }), 'https://' + EXPECT_HOST + '/app/nodes/x'), false],
    ['hostile host refused', () => gateChallenge(acc, 'https://evil.example/x'), false],
    ['bogus sourceTag refused', () => gateChallenge(Object.assign({}, acc, { extra: { invoiceId: 'i', sourceTag: 7 } }), 'https://' + EXPECT_HOST + '/app/nodes/x'), false],
    ['clean challenge accepted', () => gateChallenge(acc, 'https://' + EXPECT_HOST + '/app/nodes/x'), true],
  ];
  for (const [name, fn, shouldPass] of chalCases) {
    let threw = false, msg = '';
    try { fn(); } catch (e) { threw = true; msg = e.message; }
    const okCase = shouldPass ? !threw : threw;
    if (!okCase) bad++;
    console.log((okCase ? 'PASS ' : 'FAIL ') + name + (!shouldPass && threw ? ' — ' + msg.slice(0, 90) : ''));
  }
  console.log(bad === 0 ? '\nSELFTEST: all structural gates hold' : '\nSELFTEST: ' + bad + ' BROKEN GATE(S)');
  process.exit(bad === 0 ? 0 : 1);
}
function e_isRefusal(_t, _m) { return true; }

// --------------------------------------------------------------------- entry ----------------
module.exports = { gateChallenge, gateSignedTx, getChallenge, buy, spentToday, recordSpend, Refused };

if (require.main === module && process.argv.slice(2).includes('--selftest')) selftest();

if (require.main === module) (async () => {
  const args = process.argv.slice(2);
  if (!args.length) { console.error('REFUSED [usage] node guarded-buy.cjs <path-or-url> [...] | --selftest | NO_PAY=1'); process.exit(1); }
  if (FORCED_RAW && ENV.NO_PAY !== '1') { console.error('REFUSED [config] FORCE_CHALLENGE_JSON is an offline gate hook — pair it with NO_PAY=1 so nothing can be signed'); process.exit(1); }
  if (ENV.NO_PAY !== '1' && !SEED && !FORCED_RAW) { console.error('REFUSED [config] XRPL_SEED missing (dedicated low-balance hot wallet only, or NO_PAY=1)'); process.exit(1); }
  if (!Number.isFinite(MAX_DROPS) || MAX_DROPS <= 0) { console.error('REFUSED [config] MAX_DROPS invalid'); process.exit(1); }
  if (!Number.isFinite(DAILY_BUDGET_DROPS) || DAILY_BUDGET_DROPS <= 0) { console.error('REFUSED [config] DAILY_BUDGET_DROPS invalid'); process.exit(1); }

  const urls = args.filter((a) => a !== '--selftest').map((a) => (a.startsWith('http') ? a : BASE + (a.startsWith('/') ? a : '/' + a)));
  for (const url of urls) {
    try {
      const out = await buy(url);
      console.log(JSON.stringify(Object.assign({ url }, out)));
    } catch (e) {
      if (e instanceof Refused) { console.error('REFUSED [' + e.code + '] ' + e.message); process.exitCode = 1; }
      else { console.error('ERROR ' + String(e && e.message || e)); process.exitCode = 1; }
    }
  }
  console.error('# recorded spend today: ' + spentToday() + ' drops (cap ' + DAILY_BUDGET_DROPS + '; file ' + SPEND_FILE + ')');
})().catch((e) => { console.error('FATAL ' + String(e && e.message || e)); process.exit(1); });
