// Publish a signed post, edit one, or delete one (write_post.md). PublicOS Feed v1.
//   node post.js <slug> "<title>" "<text>" [options]            title may be "" for a short post
//   node post.js <slug> --title="…" --text="…" [options]       the same, by name (use one form, not both)
//   node post.js <slug> --edit=<post id> [--title="…"] [--text="…"]
//   node post.js <slug> --delete=<post id>
// Options for a new post:
//   --hero=<url>        a lead picture or video (repeat for a gallery); upload it first with upload.js
//   --attach=<url>      a supporting file: image, video, document (repeat)
//   --audio=<url>       the post's sound track
//   --link=<url>        a page the post is about          --summary="…"
//   --quote=<post url>  quote another post                --reply-to=<post url>   answer another post from your channel
//   --repost=<post url> repost it (no content of your own)
//   --language=en       --tags=a,b,c      --sensitive     --media-post (the media leads)
//   --comments=closed   --reactions=closed
//   --owner=<account>   post in someone else's channel (a name or 0x…, when it lets you); default: your own
// In the text, write a mention as @[name] (or @[0x…address]); names are turned into addresses here.
//
// What is signed: one JSON object with sorted keys and no empty values,
//   { author, date_published, target_url: "<server>/api/<owner>/channels/<slug>/posts", type: "post",
//     url: "<target_url>/<post id>", title, text, summary, link, hero_media, support_media, audio, quote, in_reply_to, sensitive }
// `url` is the post's own address: you make the post's id (a random UUID), sign the address, and send the same id as `uid`.
// A reader checks that the address it got the post at is the one you signed. Addresses in lowercase, every media file
// with the SHA-256 of its bytes. The request repeats those fields and adds
// the unsigned settings (language, tags, policies). An edit is a full replacement, signed again, carrying
// `prev_hashes`: the SHA-256 of every earlier version. Exits 1 when nothing was written.
const { sendEnvelope, signObject } = require('./envelope.js');
const { ethers, sspUrl, resolveAccount, getJson, positional, arg, flag, fail } = require('./chain.js');
const { mediaObject } = require('./media.js');
const { hashOf } = require('./verify.js');
const crypto = require('crypto');

const all = (name) => process.argv.filter(x => x.startsWith(`--${name}=`)).map(x => x.slice(name.length + 3));
const now = () => new Date().toISOString().replace(/\.\d+Z$/, 'Z');

function refuseMarkdownImage(text) { // post text is plain: a markdown image shows as raw text in every app
  if (!/!\[[^\]]*\]\(\s*https?:\/\//.test(text || '')) return;
  console.log('refused: the text holds a markdown image ![..](url), and post text is plain, so it would show as raw text. Pass the picture as --hero=<url> (the lead, big above the text) or --attach=<url> (under the text), and take it out of the text.');
  process.exit(1);
}

async function mentions(text) { // @[name] -> @[0xaddress]
  if (!text) return text;
  const names = [...new Set([...text.matchAll(/@\[([^\]]+)\]/g)].map(m => m[1]).filter(n => !/^0x[0-9a-fA-F]{40}$/.test(n)))];
  for (const n of names) text = text.split(`@[${n}]`).join(`@[${(await resolveAccount(n)).account}]`);
  return text;
}

// Read one post. A private or paid channel answers 401/403 to a plain read: retry signed, as this account.
async function readPost(url) {
  const r = await getJson(url);
  if ((r.status === 401 || r.status === 403) && process.env.PUBLICOS_KEY && process.env.PUBLICOS_ACCOUNT) {
    const u = new URL(url);
    return sendEnvelope('GET', u.origin, u.pathname, 'read_feed', { account_address: process.env.PUBLICOS_ACCOUNT });
  }
  return r;
}

async function pointer(url) { // {url, hash}: the post as its server states it, bound by the hash of its signed object
  const { status, body } = await readPost(url.replace(/[?#].*$/, ''));
  if (status !== 200 || !body.id) throw new Error(`could not read the post at ${url} (HTTP ${status}${status === 401 || status === 403 ? ': a private channel you may not read' : ''})`);
  const p = { url: body.url || url };
  if (body.signature && body.signature.object) p.hash = hashOf(body.signature.object);
  return p;
}

(async () => {
  let [slug, posTitle, posText] = positional();
  const account = process.env.PUBLICOS_ACCOUNT;
  if (!account) throw new Error('set PUBLICOS_ACCOUNT to the account your key signs for');
  if (!slug) { console.log('usage: node post.js <slug | owner/slug | channel url> "<title>" "<text>" [--owner=<account>] [--hero=<url>] … | --edit=<id> [--title=] [--text=] | --delete=<id>\n  a plain <slug> is YOUR channel; to post in someone else\'s channel (when you, or an org you are in, is on its posters list) write owner/slug, its URL, or --owner=<name>'); process.exit(2); }
  // Someone else's channel, written as its URL (…/api/<owner>/channels/<slug>) or as owner/slug.
  let slugOwner = null;
  const um = slug.match(/\/api\/(0x[0-9a-fA-F]{40})\/channels\/([^/?#]+)/);
  if (um) { slugOwner = um[1]; slug = um[2]; }
  else if (/^[^/]+\/[^/]+$/.test(slug)) { [slugOwner, slug] = slug.split('/'); }
  if (slugOwner && arg('owner') && (await resolveAccount(arg('owner'))).account.toLowerCase() !== (await resolveAccount(slugOwner)).account.toLowerCase()) {
    console.log('the channel names one owner and --owner another; nothing was posted'); process.exit(2);
  }
  const me = ethers.getAddress(account.toLowerCase());
  if (flag('title') || flag('text')) { console.log('write --title="…" and --text="…" with an equals sign; nothing was posted'); process.exit(2); }
  // A new post takes its title and text by position or by --title= / --text=; both at once is refused, never guessed.
  if (!arg('edit') && !arg('delete') && (posTitle !== undefined || posText !== undefined) && (arg('title') !== undefined || arg('text') !== undefined)) {
    console.log('give the title and text either by position or as --title= / --text=, not both; nothing was posted'); process.exit(2);
  }
  const ownerIn = slugOwner || arg('owner');
  const owner = ownerIn ? ethers.getAddress((await resolveAccount(ownerIn)).account.toLowerCase()) : me;
  const server = await sspUrl(owner); // the channel lives on its OWNER's social server (PUBLICOS_SSP overrides)
  const base = `/api/${owner}/channels/${slug}`;
  const say = (status, body) => console.log(status, JSON.stringify(body));
  const target = `${server.replace(/\/+$/, '')}/api/${owner.toLowerCase()}/channels/${slug}/posts`;   // what is signed: the channel's posts, server included

  if (arg('delete')) {
    const { status, body } = await sendEnvelope('DELETE', server, `${base}/posts/${arg('delete')}`, 'delete_post', { account_address: me });
    say(status, body); process.exit(status === 200 || status === 204 ? 0 : 1);
  }

  if (arg('edit')) {
    const url = `${server}${base}/posts/${arg('edit')}`;
    const cur = await readPost(url);
    if (cur.status !== 200 || !cur.body.signature || !cur.body.signature.object) throw new Error(`could not read a signed post at ${url} (HTTP ${cur.status})`);
    const content = JSON.parse(cur.body.signature.object);
    if (arg('title') !== undefined) { if (arg('title')) content.title = arg('title'); else delete content.title; }
    if (arg('text') !== undefined) { refuseMarkdownImage(arg('text')); content.text = await mentions(arg('text')); }
    content.prev_hashes = [...(content.prev_hashes || []), hashOf(cur.body.signature.object)];
    content.target_url = target;                       // an edit keeps the post's id and address, and signs them
    content.url = `${target}/${arg('edit')}`;
    const signed = await signObject(content);
    const { type, target_url, url: _own, prev_hashes, ...fields } = content;
    const data = { ...fields, account_address: me, ...signed, ...(arg('language') ? { language: arg('language') } : {}) };
    const { status, body } = await sendEnvelope('PUT', server, `${base}/posts/${arg('edit')}`, 'update_post', data);
    console.log(status, status === 200 ? `edited ${url}` : JSON.stringify(body));
    process.exit(status === 200 ? 0 : 1);
  }

  const title = arg('title') !== undefined ? arg('title') : posTitle;
  const text = arg('text') !== undefined ? arg('text') : posText;
  refuseMarkdownImage(text);
  const uid = crypto.randomUUID();                   // the post's id is yours to make, so its address can be signed
  const content = { author: me.toLowerCase(), date_published: now(), target_url: target, type: 'post', url: `${target}/${uid}` };
  if (title) content.title = title;
  if (text) content.text = await mentions(text);
  if (arg('summary')) content.summary = arg('summary');
  if (arg('link')) content.link = arg('link');
  const hero = [...all('hero'), ...all('image')];           // --image is the older name for --hero
  if (hero.length) content.hero_media = await Promise.all(hero.map(u => mediaObject(u, { needDims: true })));
  if (all('attach').length) content.support_media = await Promise.all(all('attach').map(u => mediaObject(u)));
  if (arg('audio')) { const a = await mediaObject(arg('audio')); if (!a.mime_type.startsWith('audio/')) a.mime_type = 'audio/wav'; content.audio = a; }
  const quoted = arg('repost') || arg('quote');
  if (quoted) content.quote = await pointer(quoted);
  if (arg('reply-to')) content.in_reply_to = await pointer(arg('reply-to'));
  if (flag('sensitive')) content.sensitive = true;
  const hasContent = ['title', 'text', 'hero_media', 'support_media', 'audio', 'link', 'quote'].some(k => content[k]);
  if (!hasContent) { console.log('a post needs a title, text, media, a link or a quote'); process.exit(2); }

  const signed = await signObject(content);
  const { type, target_url, url: _own, ...fields } = content;
  const data = { ...fields, account_address: me, ...signed, uid };
  if (flag('media-post')) data.media_post = true;
  if (arg('comments') === 'closed') data.comments = 'closed';
  if (arg('reactions') === 'closed') data.reactions = 'closed';
  if (arg('language')) data.language = arg('language');
  if (arg('tags')) data.tags = arg('tags').split(',').map(s => s.trim()).filter(Boolean);
  const { status, body } = await sendEnvelope('POST', server, `${base}/posts`, 'create_post', data);
  console.log(status, status === 201 ? `id ${body.id}  ${server}${base}/posts/${body.id}` : JSON.stringify(body));
  if (status === 404 && owner === me) console.log(`you have no channel "${slug}". To post in someone else's channel write <owner>/${slug} or add --owner=<owner>.`);
  if (status === 403) console.log('you may not post here: the channel owner must put you, or an org you are a member of, on its posters list (node channel_people.js posters <slug> list, run by the owner)');
  process.exit(status === 201 ? 0 : 1);
})().catch(fail);
