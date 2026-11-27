// Check a post's signature the way PublicOS clients do (read_feeds.md, "Is this post really theirs?").
// A post item carries `signature` = { object, value, signer }: `object` is the signed content as text, `value` the
// EIP-191 signature over its UTF-8 bytes. Three checks, in this order:
//   1. recover the signing key from `value` over `object`
//   2. every content field of the post equals the same field in `object`, compared as VALUES (a date is the same
//      instant however either side writes it; an absent field equals an empty one)
//   3. on chain, that key is a session key of the post's `author`
// Returns { state: 'signed' | 'unsigned' | 'bad', reason }. An unsigned post is valid, but its `author` is only
// what the server says: never treat it as an account.
const { ethers, contract } = require('./chain.js');

const _accountByKey = {};
async function sessionAccount(key) {
  if (!(key in _accountByKey)) {
    const am = await contract('ACCOUNT_MEMORY', ['function getSessionAccount(address) view returns (address)']);
    const a = String(await am.getSessionAccount(key)).toLowerCase();
    _accountByKey[key] = /^0x0{40}$/.test(a) ? null : a;
  }
  return _accountByKey[key];
}

const POST_RE = /^https?:\/\/[^/]+\/api\/(0x[0-9a-fA-F]{40})\/channels\/([^/]+)\/posts\/[^/?#]+/;

/** The first signed content field that differs from the post as served, or null. */
function mismatch(it, so) {
  const gone = (v) => v === null || v === undefined || v === '';
  const txt = (a, b) => (gone(a) && gone(b)) || (!gone(a) && !gone(b) && typeof b === 'string' && a === b);
  const num = (a, b) => (a == null && b == null) || (typeof a === 'number' && typeof b === 'number' && a === b);
  const empty = (b) => b == null || (typeof b === 'object' && !Object.keys(b).length);
  const media = (m, b) => {
    if (!m && empty(b)) return true;
    if (!m !== empty(b) || typeof b !== 'object') return false;
    return txt(m.url, b.url) && txt(m.mime_type, b.mime_type) && txt(m.sha256, b.sha256) && num(m.size_in_bytes, b.size_in_bytes) &&
      num(m.width, b.width) && num(m.height, b.height) && txt(m.thumbnail_url, b.thumbnail_url) &&
      num(m.duration_in_seconds, b.duration_in_seconds) && txt(m.title, b.title) && txt(m.alt, b.alt) && (m.loop === true) === (b.loop === true);
  };
  const list = (a, b) => {
    a = a || [];
    const bGone = b == null || (Array.isArray(b) && !b.length);
    if (!a.length && bGone) return true;
    if (!a.length !== bGone || !Array.isArray(b) || a.length !== b.length) return false;
    return a.every((m, i) => media(m, b[i]));
  };
  const ptr = (p, b) => { if (!p && empty(b)) return true; if (!p !== empty(b) || typeof b !== 'object') return false; return txt(p.url, b.url) && txt(p.hash, b.hash); };
  // An instant as "ms|extra fraction digits": Date.parse is only trusted to the millisecond.
  const inst = (s) => {
    const m = typeof s === 'string' && /^(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d)(?:\.(\d+))?(Z|[+-]\d\d:\d\d)$/.exec(s.trim());
    if (!m) return null;
    const t = Date.parse(m[1] + m[3]); if (isNaN(t)) return null;
    return t + '|' + (m[2] || '').replace(/0+$/, '');
  };
  if (so.type !== 'post') return 'type';
  if (!txt(it.title, so.title)) return 'title';
  if (!txt(it.text, so.text)) return 'text';
  if (!txt(it.summary, so.summary)) return 'summary';
  if (!txt(it.link, so.link)) return 'link';
  if (!list(it.hero_media, so.hero_media)) return 'hero_media';
  if (!list(it.support_media, so.support_media)) return 'support_media';
  if (!media(it.audio, so.audio)) return 'audio';
  if (it.sensitive == null ? so.sensitive != null : !(typeof so.sensitive === 'boolean' && so.sensitive === it.sensitive)) return 'sensitive';
  const d = inst(so.date_published); if (!d || d !== inst(it.date_published)) return 'date_published';
  if (typeof so.author !== 'string' || !so.author || so.author.toLowerCase() !== String(it.author || '').toLowerCase()) return 'author';
  if (!ptr(it.quote, so.quote)) return 'quote';
  if (!ptr(it.in_reply_to, so.in_reply_to)) return 'in_reply_to';
  if (typeof so.target_url !== 'string' || !so.target_url) return 'target_url';
  const ref = POST_RE.exec(String(it.url || ''));
  if (ref) { // the channel in the post's own permalink, so a server cannot move a signed post to another channel
    const path = so.target_url.replace(/^https?:\/\/[^/]+/i, '').split(/[?#]/)[0];
    if (path.toLowerCase() !== `/api/${ref[1]}/channels/${ref[2]}/posts`.toLowerCase()) return 'target_url';
  }
  // Since 2026-11 the author signs where the post lives, server included. A target written with a server's name must
  // name the server the post is on, and `url`, the post's own address, must be the address the post is served with
  // (case, a trailing slash and a query do not count). An object with a bare path and no `url` is a post from before.
  const key = (u) => String(u).split('#')[0].split('?')[0].trim().replace(/\/+$/, '').toLowerCase();
  const host = (u) => { const m = /^https?:\/\/([^/]+)/i.exec(String(u)); return m ? m[1].toLowerCase() : ''; };
  if (it.url && host(so.target_url) && host(it.url) && host(so.target_url) !== host(it.url)) return 'target_url';
  if (so.url != null && so.url !== '') {
    if (typeof so.url !== 'string') return 'url';
    if (it.url && key(so.url) !== key(it.url)) return 'url';
  }
  return null;
}

async function verifyPost(it) {
  const s = it.signature || {};
  const bad = (reason) => ({ state: 'bad', reason });
  if (!s.object && !s.value) return { state: 'unsigned', reason: 'This post is not signed.' };
  if (!s.object || !s.value) return bad('incomplete signature data');
  let key, blob;
  try { key = ethers.verifyMessage(s.object, s.value).toLowerCase(); } catch { return bad('the signature could not be recovered'); }
  try { blob = JSON.parse(s.object); } catch { return bad('the signed object is not valid JSON'); }
  if (!blob || typeof blob !== 'object' || Array.isArray(blob)) return bad('the signed object is not a JSON object');
  const field = mismatch(it, blob);
  if (field) return bad(`"${field}" does not match what was signed`);
  const author = String(it.author || '').toLowerCase();
  const acct = await sessionAccount(key);
  if (!acct) return bad('the signing key belongs to no account on chain');
  if (acct !== author) return bad(`the signing key belongs to ${acct}, not to the author`);
  return { state: 'signed', reason: 'signature verified', signer: key };
}

/** SHA-256 (hex, no 0x) over the UTF-8 bytes of a signed object: every hash in the format. */
const hashOf = (signedObjectText) => require('node:crypto').createHash('sha256').update(Buffer.from(signedObjectText, 'utf8')).digest('hex');

module.exports = { verifyPost, mismatch, hashOf, POST_RE };
