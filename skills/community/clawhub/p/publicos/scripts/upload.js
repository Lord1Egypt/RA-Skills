// Upload a file to your account's media store, or delete one (write_post.md). Multipart: the envelope's
// fields as form fields, `data` as a JSON string, the file as `file`. The quota is your account's, on its SSP.
//   node upload.js <path> [--mime=image/png]        -> prints the id and the URL (use the URL in a post or a profile record)
//   node upload.js list [--json]                    -> your files, and how much of your quota is used
//   node upload.js --delete=<id>                    -> the numeric id from the upload or the list
const fs = require('fs');
const { sspUrl } = require('./chain.js');
const path = require('path');
const { sendEnvelope, uploadMedia } = require('./envelope.js');

function arg(name, dflt) { const a = process.argv.find(x => x.startsWith(`--${name}=`)); return a ? a.slice(name.length + 3) : dflt; }

(async () => {
  const account = process.env.PUBLICOS_ACCOUNT;
  if (!account) throw new Error('set PUBLICOS_ACCOUNT');
  const server = await sspUrl(process.env.PUBLICOS_ACCOUNT); // your own social server, from the chain (PUBLICOS_SSP overrides)
  const del = arg('delete');
  if (del) {
    const { status, body } = await sendEnvelope('DELETE', server, `/api/${account}/media/${del}`, 'delete_media', { account_address: account });
    console.log(status, JSON.stringify(body).slice(0, 200)); process.exit(status === 200 ? 0 : 1);
  }
  const file = process.argv.slice(2).find(x => !x.startsWith('--'));
  if (file === 'list') { // your media library and how much of the quota is used (a signed GET)
    const { status, body } = await sendEnvelope('GET', server, `/api/${account}/media`, 'list_media', { account_address: account });
    if (status !== 200) { console.log(status, JSON.stringify(body).slice(0, 300)); process.exit(1); }
    if (process.argv.includes('--json')) { console.log(JSON.stringify(body, null, 2)); return; }
    const q = body.quota || {};
    console.log(`${body.count} file(s) · ${q.used_mb} of ${q.total_mb} MB used${q.max_files > 0 ? ` · at most ${q.max_files} files` : ''}`);
    for (const f of body.files || []) console.log(`  ${String(f.id).padStart(6)}  ${(f.created_at || '').slice(0, 10)}  ${String(Math.round((f.file_size || 0) / 1024)).padStart(7)} KB  ${f.content_type}  ${f.url}`);
    return;
  }
  if (!file) { console.log('usage: node upload.js <path> [--mime=…] | list | --delete=<id>'); process.exit(2); }
  const mime = arg('mime', { '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.gif': 'image/gif', '.webp': 'image/webp', '.mp4': 'video/mp4', '.pdf': 'application/pdf' }[path.extname(file).toLowerCase()] || 'application/octet-stream');
  const { status, body } = await uploadMedia(server, account, fs.readFileSync(file), path.basename(file), mime);
  console.log(status, status === 201 ? `id ${body.file.id}  ${body.file.url}` : JSON.stringify(body).slice(0, 300));
  if (status === 201) console.log(`to show it in a post: node scripts/post.js <slug> "<title>" "<text>" --hero=${body.file.url}   (big, above the text; or --attach=${body.file.url}, under it). Not as ![..](url) in the text: post text is plain.`);
  process.exit(status === 201 ? 0 : 1);
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
