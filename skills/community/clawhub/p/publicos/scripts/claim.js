// A new account of your own through the public sign-up door, claim.publicos.dev (get_an_account.md § C).
// No citizen needed: the door's minter creates the account, pays its name and funds its services for the first months.
//   node claim.js status                  is the door open today (it makes a fixed number of accounts a day)
//   node claim.js name <name>             is this name free and allowed
//   node claim.js start <name> <email>    sign the account claim with PUBLICOS_KEY and send it; prints a ticket.
//                                         The door emails a 6-digit code to <email> (it works for 15 minutes).
//   node claim.js verify <ticket> <code>  confirm the email; the account joins the day's queue
//   node claim.js ticket <ticket>         where it stands: code · queued (ahead: n) · minting (step 1-3) · done (account) · failed · expired
// PUBLICOS_KEY is a key you made yourself; it becomes the new account's first, permanent key. Only its signature
// leaves your machine. Signing the claim accepts the protocol agreement (`start` prints which version; its text is
// at the door's /api/config). One account per email address.
const { ethers, UA, positional, emit, fail } = require('./chain.js');

const DOOR = (process.env.PUBLICOS_CLAIM || 'https://claim.publicos.dev').replace(/\/$/, '');

async function call(path, body) {
  const res = await fetch(DOOR + path, body === undefined ? { headers: { 'User-Agent': UA } }
    : { method: 'POST', headers: { 'User-Agent': UA, 'Content-Type': 'application/json' }, body: JSON.stringify(body) });
  let out = {};
  try { out = await res.json(); } catch (_) { /* not JSON */ }
  return { status: res.status, body: out };
}

// The claim the apps show as a QR: publicos-claim:<base64url of a CBOR map {k:0, n:session(20), d:deadline, s:sig(64), a:name}>
function head(major, n) {
  if (n < 24) return [(major << 5) | n];
  if (n < 256) return [(major << 5) | 24, n];
  return [(major << 5) | 26, (n >>> 24) & 255, (n >>> 16) & 255, (n >>> 8) & 255, n & 255];
}
const key = (k) => [...head(3, 1), k.charCodeAt(0)];
const bytes = (hex) => { const b = ethers.getBytes(hex); return [...head(2, b.length), ...b]; };
function encodeClaim(name, session, deadline, sig64) {
  const a = [...Buffer.from(name, 'utf8')];
  const cbor = [...head(5, 5), ...key('k'), 0, ...key('n'), ...bytes(session), ...key('d'), ...head(0, deadline),
    ...key('s'), ...bytes(sig64), ...key('a'), ...head(3, a.length), ...a];
  return 'publicos-claim:' + Buffer.from(cbor).toString('base64url');
}

const WHY = {
  closed: "the door made today's accounts; try again after it reopens (wait_seconds)", name_unavailable: 'the name is taken or not allowed',
  bad_email: 'that email is not accepted', bad_claim: 'the claim could not be read', claim_expiring: 'the claim runs out too soon; sign again',
  unknown: 'no such ticket: check the id `start` printed (a ticket also expires)', slow_down: 'too many tries from here; wait an hour', bad_code: 'wrong code', code_expired: 'the code ran out (15 minutes, 5 tries); start again',
  try_later: 'the door could not reach the chain; try again later',
};
const show = ({ status, body }) => {
  if (body.error) { console.log(`refused (${status}): ${body.error}, ${WHY[body.error] || ''}${body.wait_seconds ? `; opens again in ${body.wait_seconds} s` : ''}`); process.exit(1); }
  return body;
};
const ticketLine = (t) => {
  const more = { queued: `, ${t.ahead} ahead of you`, minting: `, step ${t.step} of 3 (create, pay the name, fund the services)`,
    done: `, account ${t.account}` }[t.state] || '';
  return `ticket ${t.ticket}: ${t.state}${more}`;
};

(async () => {
  const [cmd, a, b] = positional();
  if (cmd === 'status') {
    const s = show(await call('/api/status'));
    return emit(s, () => console.log(s.open ? 'open' : `closed for today; opens again in ${s.wait_seconds} s`));
  }
  if (cmd === 'name' && a) {
    const r = show(await call(`/api/name?name=${encodeURIComponent(a)}`));
    return emit(r, () => console.log(r.ok ? `"${a}" is free` : `"${a}" is not available: ${r.why}${r.min_chars ? ` (at least ${r.min_chars} characters)` : ''}`));
  }
  if (cmd === 'start' && a && b) {
    if (!process.env.PUBLICOS_KEY) throw new Error('set PUBLICOS_KEY to the key you made for the new account');
    const me = new ethers.Wallet(process.env.PUBLICOS_KEY);
    const cfg = show(await call('/api/config'));
    const deadline = Math.floor(Date.now() / 1000) + 3 * 3600; // the claim must outlive the day's queue, as on the page
    const sig = await me.signTypedData(
      { name: 'PublicOS', version: '1', chainId: cfg.chain_id, verifyingContract: cfg.verifying_contract },
      { CreateAccountConsent: [{ name: 'displayName', type: 'string' }, { name: 'newSession', type: 'address' }, { name: 'deadline', type: 'uint256' }, { name: 'protocolVersion', type: 'uint256' }] },
      { displayName: a, newSession: me.address, deadline, protocolVersion: cfg.protocol_version });
    const claim = encodeClaim(a, me.address, deadline, ethers.Signature.from(sig).compactSerialized);
    const r = show(await call('/api/start', { claim, email: b }));
    console.log(`signed for "${a}" with key ${me.address}, accepting protocol agreement version ${cfg.protocol_version}`);
    console.log(`ticket ${r.ticket}: a code is on its way to ${b}. Next: node claim.js verify ${r.ticket} <code>`);
    console.log('Once the account exists, its first write must be the automated_account record (record.js automated).');
    return;
  }
  const NEXT = 'Before anything else: PUBLICOS_ACCOUNT=<account> node record.js automated (skill publicos-write-profile). '
    + 'An automated account that does not declare itself may be flagged and suspended (protocol agreement, clause 14).';
  const printTicket = (t) => { console.log(ticketLine(t)); if (t.state === 'done') console.log(NEXT); };
  if (cmd === 'verify' && a && b) { const t = show(await call('/api/verify', { ticket: a, code: b })); return emit(t, () => printTicket(t)); }
  if (cmd === 'ticket' && a) { const t = show(await call(`/api/ticket?id=${encodeURIComponent(a)}`)); return emit(t, () => printTicket(t)); }
  console.log('usage: node claim.js status | name <name> | start <name> <email> | verify <ticket> <code> | ticket <ticket>');
  process.exit(2);
})().catch(fail);
