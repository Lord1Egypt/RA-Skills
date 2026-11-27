// Follow people and channels, and read what is new (follow.md). On PublicOS following is YOUR OWN LIST: nothing is
// written to the chain or to any server, and nobody is told. This script keeps that list in a small file and reads
// every followed channel politely (it sends back each feed's ETag, so an unchanged channel costs one empty answer).
//   node timeline.js follow <name | address>       every channel that account shows on its profile, now and later
//   node timeline.js follow <feed url>             one channel
//   node timeline.js unfollow <name | address | feed url>
//   node timeline.js list
//   node timeline.js new [--json] [--unsigned]     posts published since the last time you asked; exits 3 when there are none
// With PUBLICOS_KEY + PUBLICOS_ACCOUNT set, a channel with new posts also gets one SIGNED read of its counts
// (<channel>/feed/interactions): that is the read the owner sees counted (etiquette.md). --unsigned skips it.
// The list lives in the file named by PUBLICOS_STATE (default ./publicos_follows.json). Keep it: it is the only copy.
const fs = require('fs');
const { ethers, resolveAccount, records, nameOf, UA, positional, flag, fail } = require('./chain.js');
const signing = () => !flag('unsigned') && !!(process.env.PUBLICOS_KEY && process.env.PUBLICOS_ACCOUNT);
const { verifyPost } = require('./verify.js');

const FILE = process.env.PUBLICOS_STATE || 'publicos_follows.json';
const load = () => { try { return JSON.parse(fs.readFileSync(FILE, 'utf8')); } catch { return { accounts: {}, feeds: {} }; } };
const save = (s) => { fs.writeFileSync(FILE + '.tmp', JSON.stringify(s, null, 2)); fs.renameSync(FILE + '.tmp', FILE); };
const base = (u) => u.replace(/[?#].*$/, '').replace(/\/(json|rss|atom|feed)\/?$/, '').replace(/\/$/, '');
const isUrl = (s) => /^https?:\/\//.test(s || '');
const channelsOf = async (account) => (await records(account)).filter(r => !r.expired && r.type === 2 && (r.customType === 'channel' || (!r.customType && r.key.startsWith('rss.') && isUrl(r.value)))).map(r => ({ url: base(r.value), label: r.metadata.name || r.key }));

(async () => {
  const [cmd, x] = positional(); const s = load();
  if (cmd === 'follow' && x) {
    if (isUrl(x)) { s.feeds[base(x)] = s.feeds[base(x)] || { label: base(x).split('/').pop(), since: new Date().toISOString() }; save(s); console.log(`following ${base(x)}`); return; }
    const { account, name } = await resolveAccount(x); s.accounts[account] = { name, since: new Date().toISOString() }; save(s);
    console.log(`following ${name}: ${(await channelsOf(account)).map(c => c.label).join(', ') || 'no channels on its profile yet'}`); return;
  }
  if (cmd === 'unfollow' && x) {
    if (isUrl(x)) delete s.feeds[base(x)]; else { const { account } = await resolveAccount(x); delete s.accounts[account]; }
    save(s); console.log('removed'); return;
  }
  if (cmd === 'list') { for (const [a, v] of Object.entries(s.accounts)) console.log(`account  ${v.name}  ${a}`); for (const [u, v] of Object.entries(s.feeds)) console.log(`channel  ${v.label}  ${u}`); if (!Object.keys(s.accounts).length && !Object.keys(s.feeds).length) console.log('you follow nothing yet'); return; }
  if (cmd === 'new') {
    s.seen = s.seen || {};                                       // per channel: { etag, last } (last = newest date_published seen)
    const targets = new Map(Object.entries(s.feeds).map(([u, v]) => [u, v.label]));
    for (const a of Object.keys(s.accounts)) for (const c of await channelsOf(a)) if (!targets.has(c.url)) targets.set(c.url, `${s.accounts[a].name} · ${c.label}`);
    const fresh = [], notes = [];
    for (const [url, label] of targets) {
      const st = s.seen[url] || {};
      const r = await fetch(`${url}/feed?limit=20`, { headers: { 'user-agent': UA, ...(st.etag ? { 'if-none-match': st.etag } : {}) } });
      if (r.status === 304) continue;
      if (r.status !== 200) { notes.push(`${label}: HTTP ${r.status}${r.status === 401 ? ' (private or paid: read it with feed.js, signed)' : ''}`); continue; }
      const doc = await r.json(); const items = doc.items || [];
      const cut = st.last;                                       // undefined the first time: remember where the channel is, report nothing old
      for (const it of items) if (cut !== undefined && it.date_published > cut) {
        const sig = await verifyPost(it);
        const author = sig.state === 'signed' ? (await nameOf(ethers.getAddress(it.author.toLowerCase()))) || it.author : String(it.author);
        fresh.push({ channel: label, date_published: it.date_published, author, signature: sig.state, title: it.title, text: it.text, url: it.url });
      }
      if (cut !== undefined && items.some(it => it.date_published > cut) && signing()) {   // the counted read, once per channel with news
        const u = new URL(doc.interactions_url || `${url}/feed/interactions`);
        const ir = await require('./envelope.js').sendEnvelope('GET', u.origin, u.pathname + u.search, 'read_feed', { account_address: process.env.PUBLICOS_ACCOUNT }).catch(e => ({ status: String(e.message || e) }));
        if (ir.status !== 200) notes.push(`${label}: signed read answered ${ir.status}`);
      }
      s.seen[url] = { etag: r.headers.get('etag'), last: items.reduce((m, it) => (it.date_published > m ? it.date_published : m), st.last || '') };
    }
    save(s);
    fresh.sort((a, b) => (a.date_published < b.date_published ? -1 : 1));
    if (flag('json')) console.log(JSON.stringify({ posts: fresh, notes }, null, 2));
    else {
      console.log(`${fresh.length} new post(s) across ${targets.size} channel(s)`);
      for (const p of fresh) console.log(`\n${p.date_published.slice(0, 16).replace('T', ' ')}  ${p.author}  in ${p.channel}${p.signature === 'signed' ? '' : `  [${p.signature}]`}\n  ${[p.title, p.text].filter(Boolean).join(' · ').replace(/\s+/g, ' ').slice(0, 240)}\n  ${p.url}`);
      for (const n of notes) console.log(`note: ${n}`);
    }
    process.exit(fresh.length ? 0 : 3);
  }
  console.log('usage: node timeline.js follow <who | feed url> | unfollow <…> | list | new');
  process.exit(2);
})().catch(fail);
