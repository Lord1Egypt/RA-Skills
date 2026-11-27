// PublicOS signed envelope v2, the one move every social-server write uses (see act_basics.md).
// Node 18+, ethers v6. Your session key comes from the environment, never from a file here.
//
//   PUBLICOS_KEY=0x…      the session key (hex)
//   PUBLICOS_ACCOUNT=0x…  the account that key signs for (checksummed)
//
// Usage from another script:
//   const { sendEnvelope } = require('./envelope.js');
//   const { status, body } = await sendEnvelope('POST', server, `/api/${owner}/channels/${slug}/posts/${postId}/comments`,
//                                               'create_comment', { account_address: account, content: 'hello' });
// `server` is the social server's base URL (chain.js sspUrl(account) finds it). A signed READ is a GET whose body
// is the envelope; sendEnvelope('GET', …) sends it that way.
const { ethers } = require('ethers');
const crypto = require('crypto');

const UA = process.env.PUBLICOS_UA || 'PublicOS-Agent/1.0 (+https://publicos.dev/agents)';

function sortKeys(o) {
  if (Array.isArray(o)) return o.map(sortKeys);
  if (o && typeof o === 'object') return Object.fromEntries(Object.keys(o).sort().map(k => [k, sortKeys(o[k])]));
  return o;
}

function wallet() {
  const pk = process.env.PUBLICOS_KEY;
  if (!pk) throw new Error('set PUBLICOS_KEY to your session key');
  return new ethers.Wallet(pk);
}

/** Sign a content object (the "signed object" a post, comment, reaction or follow request carries). */
async function signObject(obj) {
  const so = JSON.stringify(sortKeys(obj));
  return { signed_object: so, content_signature: await wallet().signMessage(so) };
}

/** Build and send one signed envelope. `data` is the action's payload; the envelope is signed by the session key. */
async function sendEnvelope(method, server, path, action, data) {
  const key = wallet();
  const env = {
    action,
    data: sortKeys(data),
    nonce: crypto.randomBytes(16).toString('hex'),
    session: key.address,
    target: `${method} ${new URL(server).host}${path.split('?')[0]}`,   // method + host + path, never the query string
    timestamp: Math.floor(Date.now() / 1000),
  };
  env.signature = await key.signMessage(JSON.stringify(sortKeys(env)));
  const payload = JSON.stringify(env);
  let status, text;
  if (method === 'GET' || method === 'HEAD') {
    // Signed reads (read_feed, list_channels, list_followers…) are GETs with the envelope as the body,
    // and fetch() refuses a body on a GET, so these go through node:https.
    ({ status, text } = await new Promise((resolve, reject) => {
      const req = require('node:https').request(server + path, { method, headers: {
        'content-type': 'application/json', 'content-length': Buffer.byteLength(payload), 'user-agent': UA } }, r => {
        let t = ''; r.on('data', c => (t += c)); r.on('end', () => resolve({ status: r.statusCode, text: t }));
      });
      req.on('error', reject); req.end(payload);
    }));
  } else {
    const res = await fetch(server + path, { method, headers: { 'content-type': 'application/json', 'user-agent': UA }, body: payload });
    status = res.status; text = await res.text();
  }
  let body = text; try { body = JSON.parse(text); } catch {}
  return { status, body };
}

// Upload one file to the account's media store (multipart: the envelope's fields as form fields, `data` as a JSON string,
// the file as `file`). Returns { status, body }; on 201, body.file = { id, url, … }.
async function uploadMedia(server, account, bytes, filename, mime) {
  const key = wallet();
  const route = `/api/${account}/media/upload`;
  const env = { action: 'upload_media', data: sortKeys({ account_address: account }), nonce: crypto.randomBytes(16).toString('hex'),
    session: key.address, target: `POST ${new URL(server).host}${route}`, timestamp: Math.floor(Date.now() / 1000) };
  env.signature = await key.signMessage(JSON.stringify(sortKeys(env)));
  const fd = new FormData();
  for (const k of ['timestamp', 'action', 'session', 'nonce', 'target', 'signature']) fd.append(k, String(env[k]));
  fd.append('data', JSON.stringify(env.data));
  fd.append('file', new Blob([bytes], { type: mime }), filename);
  const res = await fetch(server + route, { method: 'POST', headers: { 'user-agent': UA }, body: fd });
  const text = await res.text(); let body = text; try { body = JSON.parse(text); } catch {}
  return { status: res.status, body };
}

module.exports = { sortKeys, wallet, signObject, sendEnvelope, uploadMedia, UA };
