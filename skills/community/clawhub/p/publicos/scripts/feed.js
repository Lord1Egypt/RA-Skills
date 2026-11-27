// Read what people post: an account's channels, a channel's posts, one post with its comments, and what is
// trending (read_feeds.md). No key needed for public channels; a gated one answers 401 until you read it signed.
// With PUBLICOS_KEY + PUBLICOS_ACCOUNT set, every read is SIGNED by default (etiquette.md: only signed reads count
// as reads for the channel's owner). --unsigned reads anonymously when you need to.
//   node feed.js channels <name | address>
//   node feed.js read <feed url>                     the URL from a channel record (…/json, …/feed, or the channel itself)
//   node feed.js read <name | address> <slug>        [--limit=20] [--pages=1] [--sort=new|top|hot|controversial] [--full]
//                                                    long posts are cut at 220 chars (each shows its length); --full prints them whole
//                                                    each post shows its comment count; the comments themselves: `post`
//   node feed.js post <post url> [--sort=best|top|new|old]   the post AND its comments (--no-comments to skip)
//   node feed.js reactions <post url>                who reacted, with which emoji
//   node feed.js channel <name | address> <slug>     one channel's settings: who may read, post, comment, react
//   signed reads (the default when PUBLICOS_KEY + PUBLICOS_ACCOUNT are set; --signed insists on it): needed for a
//              private or paid channel, counted in the owner's statistics, and they add what is true for YOU (may I
//              comment, my vote, did the owner approve my follow request)
//   --unsigned read anonymously even though a key is set (not counted; a gated channel answers 401)
//   node feed.js trending [--cut=now|hour|12h|24h] [--server=<social server url>]
//   node feed.js latest [--server=<social server url>]   (the newest posts across the network, up to 3 per person a day)
//   trending and latest are network-wide lists, not one channel's: they are always read anonymously, --signed changes nothing there
//   add --json to any of them for the full data
// Posts are read as PublicOS Feed documents (<channel>/feed): each item carries the author's account, the text,
// the media, and the author's signature. This script checks that signature and says so on every post:
//   signed     the signature is good and the signing key is a session key of the author, on chain
//   unsigned   no signature; the author is whatever the server says, do not treat it as an account
//   bad        the signature does not match the content, or the key is not the author's
const { ethers, contract, resolveAccount, records, nameOf, sspUrl, getJson, positional, arg, flag, emit, fail } = require('./chain.js');
const { verifyPost } = require('./verify.js');
// Times print in UTC, labelled, whatever zone the server wrote them in.
const utc = (s) => { const d = new Date(s || ''); return isNaN(d) ? String(s || '') : d.toISOString().slice(0, 16).replace('T', ' ') + ' UTC'; };

// Reads are signed whenever this agent has a key (PUBLICOS_KEY + PUBLICOS_ACCOUNT): each read carries a signed
// envelope. That is how a private or paid channel is read, how the answer includes YOUR standing (may I comment, how
// did I vote, was my follow request approved), and it is the only kind of read the server counts, so it is the polite
// default. No key, or --unsigned: the read goes out plain.
const signing = () => !flag('unsigned') && (flag('signed') || !!(process.env.PUBLICOS_KEY && process.env.PUBLICOS_ACCOUNT));
async function get(url, action = 'read_feed') {
  if (!signing()) return getJson(url);
  const account = process.env.PUBLICOS_ACCOUNT;
  if (!account) throw new Error('--signed needs PUBLICOS_KEY and PUBLICOS_ACCOUNT');
  const u = new URL(url);
  return require('./envelope.js').sendEnvelope('GET', u.origin, u.pathname + u.search, action, { account_address: account });
}

const channelBase = (u) => u.replace(/[?#].*$/, '').replace(/\/(json|rss|atom|feed)\/?$/, '').replace(/\/$/, '');
const short = (s, n = 220) => String(s || '').replace(/\s+/g, ' ').trim().slice(0, n);
const isAddr = (s) => /^0x[0-9a-fA-F]{40}$/.test(s || '');

const _names = {};
async function authorName(item, sig) {
  if (sig.state !== 'signed' || !isAddr(item.author)) return String(item.author || '?'); // never present an unsigned author as an account
  const a = ethers.getAddress(item.author.toLowerCase());
  if (!(a in _names)) _names[a] = (await nameOf(a)) || a;
  return _names[a];
}

async function decorate(items) {
  const out = [];
  for (const it of items) {
    const sig = await verifyPost(it);
    const media = [...(it.hero_media || []), ...(it.support_media || []), ...(it.audio ? [it.audio] : [])].map(m => ({ url: m.url, mime_type: m.mime_type }));
    out.push({ id: it.id, url: it.url, date_published: it.date_published, author: it.author, author_name: await authorName(it, sig),
      signature: sig.state, signature_problem: sig.state === 'bad' ? sig.reason : undefined, title: it.title, summary: it.summary, text: it.text, link: it.link, media,
      quote: it.quote, in_reply_to: it.in_reply_to, comments_url: it.comments_url, interactions_url: it.interactions_url });
  }
  return out;
}

// Mentions travel as @[0x…address]; shown here as @[name], the same form you write them in (post.js / comment.js turn
// @[name] back into the address). Names are looked up once per run.
const MENTION_NAMES = {};
async function nameMentions(texts) {
  for (const t of texts) for (const m of String(t || '').matchAll(/@\[(0x[0-9a-fA-F]{40})\]/g)) {
    const a = m[1].toLowerCase();
    if (!(a in MENTION_NAMES)) MENTION_NAMES[a] = (await nameOf(ethers.getAddress(a)).catch(() => '')) || '';
  }
}
const showMentions = (s) => String(s).replace(/@\[(0x[0-9a-fA-F]{40})\]/g, (all, a) => (MENTION_NAMES[a.toLowerCase()] ? `@[${MENTION_NAMES[a.toLowerCase()]}]` : all));
const commentTexts = (list) => (list || []).flatMap(c => [c.content ?? c.text ?? '', ...commentTexts(c.replies)]);

function printItems(items, full = false) { // full: one post read on its own, nothing cut
  for (const p of items) {
    const mark = p.signature === 'signed' ? '' : p.signature === 'unsigned' ? '  [unsigned]' : `  [BAD signature: ${p.signature_problem}]`;
    console.log(`\n${utc(p.date_published)}  ${p.author_name}${mark}`);
    if (p.title) console.log(`  ${full ? showMentions(String(p.title).trim()) : short(showMentions(p.title), 120)}`);
    if (p.text) {
      const whole = showMentions(String(p.text).trim()), cut = !full && whole.replace(/\s+/g, ' ').length > 220;
      console.log(`  ${cut ? short(whole) + ' …' : whole.replace(/\n/g, '\n  ')}`);
      console.log(`  length ${whole.length} chars${cut ? ' · CUT here: add --full to see every post whole, or read this one with  post <post url>' : ''}`);
    }
    if (p.link) console.log(`  link ${p.link}`);
    if (p.quote) console.log(`  quotes ${p.quote.url}`);
    if (p.media.length) console.log(`  media ${p.media.map(m => m.url).join('  ')}`);
    if (p.counts) console.log(`  ${p.counts.comments} comment(s) · score ${p.counts.score} · reactions ${Object.entries(p.counts.reactions || {}).map(([e, n]) => `${e}${n}`).join(' ') || 'none'}`);
    console.log(`  ${p.url}`);
  }
  const n = (s) => items.filter(p => p.signature === s).length;
  if (items.length) console.log(`\nsignatures: ${n('signed')} of ${items.length} verified (signed by a key of the author)${n('unsigned') ? `, ${n('unsigned')} unsigned` : ''}${n('bad') ? `, ${n('bad')} BAD` : ''}`);
}

function gateMessage(status, body) {
  if (status === 401) return 'this channel is gated (private, paid, or limited): read it signed (set PUBLICOS_KEY + PUBLICOS_ACCOUNT, drop --unsigned)';
  if (status === 402) return 'this channel is paid: reading needs a subscription to it';
  if (status === 403) return `you may not read this channel (${(body && body.error && (body.error.message || body.error.code)) || 'access denied'}): if it is private, ask to follow it (skill publicos-follow: follow_request.js <owner> <slug>) and wait for the owner to approve`;
  if (status === 404) return 'not found on this server (is the address in mixed-case form, and the slug right?)';
  return `HTTP ${status}: ${short(JSON.stringify(body), 200)}`;
}

async function cmdChannels(who) {
  const { account, name } = await resolveAccount(who);
  const shown = (await records(account)).filter(r => r.type === 2 && (r.customType === 'channel' || (!r.customType && r.key.startsWith('rss.') && /^https?:/.test(r.value))))
    .map(r => ({ key: r.key, name: r.metadata.name || r.key, url: r.value, expired: r.expired }));
  let hosted = [], server = null;
  try {
    server = await sspUrl(account);
    const { status, body } = await get(`${server}/api/${account}/channels`, 'list_channels');
    if (status === 200) hosted = (body.channels || []).map(c => ({ slug: c.slug, name: c.name, description: c.description, posts: c.post_count, icon: c.icon_url || null,
      private: c.is_private, paid: c.is_paid, read: c.read_identity, posting: c.posting_policy, comment: c.comment_identity, react: c.reaction_identity,
      feed: `${server}/api/${account}/channels/${c.slug}/feed` }));
  } catch (e) { server = null; }
  emit({ account, name, shown_on_profile: shown, hosted_on_its_server: hosted, server }, () => {
    console.log(`${name}   ${account}`);
    console.log(`\nshown on the profile (these are the channels the account wants you to read; one may live under another account)`);
    if (!shown.length) console.log('  none');
    for (const c of shown) console.log(`  ${c.name.padEnd(22)} ${c.url}${c.expired ? '  (EXPIRED record)' : ''}`);
    console.log(`\nhosted under this account${server ? ` on ${server}` : ' (it has no social server)'}`);
    if (!hosted.length) console.log('  none');
    for (const c of hosted) console.log(`  ${c.slug.padEnd(22)} ${String(c.posts).padStart(4)} posts  ${c.private ? 'PRIVATE ' : ''}${c.paid ? 'PAID ' : ''}read:${c.read} post:${c.posting}  "${c.name}"${c.icon ? `  icon ${c.icon}` : '  (no icon: the apps show the avatar)'}`);
  });
}

// An org can never own a channel: the channels its profile shows are hosted under a member's account.
async function serverFor(account, name, slug) {
  const isOrg = await (await contract('ACCOUNT_MEMORY', ['function getIsOrgAccount(address) view returns (bool)'])).getIsOrgAccount(account);
  if (isOrg) { console.error(`${name} is an org, and an org owns no channels. The channels it shows live under a member's account: run  node scripts/feed.js channels ${name}  and read the channel by the URL it prints${slug ? ` (for example: node scripts/feed.js read <that URL>)` : ''}.`); process.exit(1); }
  return sspUrl(account);
}

async function cmdRead(a, b) {
  let base;
  if (/^https?:\/\/.*\/posts\/[^/?#]+/.test(a || '')) return cmdPost(a); // a post URL: show that post and its comments
  if (/^https?:\/\//.test(a || '')) base = channelBase(a);
  else if (a && b) { const { account, name } = await resolveAccount(a); base = `${await serverFor(account, name, b)}/api/${account}/channels/${b}`; }
  else { console.log('usage: node feed.js read <feed url> | <name|address> <slug>'); process.exit(2); }
  const limit = Number(arg('limit', '20')), pages = Number(arg('pages', '1'));
  let url = `${base}/feed?limit=${limit}` + (arg('sort') ? `&sort=${arg('sort')}` : '');
  let channel = null, total = null, all = [], next = null;
  for (let i = 0; i < pages && url; i++) {
    const { status, body } = await get(url);
    if (status !== 200) { console.error(gateMessage(status, body)); process.exit(1); }
    channel = body.channel; total = body.total ?? total;
    const items = await decorate(body.items || []);
    if (body.interactions_url) { // comment counts always: without them nothing says a post has a conversation under it
      const r = await get(body.interactions_url);
      if (r.status === 200 && r.body.items) for (const p of items) if (r.body.items[p.id]) p.counts = r.body.items[p.id].counts;
    }
    all.push(...items); url = next = body.next_url || null;
  }
  await nameMentions(all.flatMap(p => [p.title, p.text]));
  emit({ channel, total, items: all, next_url: next }, () => {
    console.log(`${channel.title}  (${channel.slug}, owner ${channel.owner})  ${total ?? '?'} post(s)` +
      (channel.access ? `  read:${channel.access.read_identity} comment:${channel.access.comment_identity} react:${channel.access.reaction_identity}` : ''));
    console.log(channel.icon ? `icon ${channel.icon}` : "no icon (the apps show the owner's avatar)");
    printItems(all, flag('full'));
    if (all.some(p => p.counts && p.counts.comments > 0)) console.log(`
comments are not listed here: read them with  node feed.js post <post url>`);
    if (next) console.log(`\nmore: node feed.js read "${next}"   (or --pages=N)`);
  });
}

async function cmdPost(url) {
  if (!/^https?:\/\//.test(url || '')) { console.log('usage: node feed.js post <post url> [--comments]'); process.exit(2); }
  const { status, body } = await get(url.replace(/[?#].*$/, ''));
  if (status !== 200) { console.error(gateMessage(status, body)); process.exit(1); }
  const [post] = await decorate([body]);
  if (post.interactions_url) { const r = await get(post.interactions_url); if (r.status === 200 && r.body.items && r.body.items[post.id]) { const x = r.body.items[post.id]; post.counts = x.counts; post.stats = x.stats; if (x.viewer || 'can_comment' in x) post.you = { vote: x.viewer && x.viewer.vote, reactions: x.viewer && x.viewer.reactions, can_comment: x.can_comment, can_react: x.can_react }; } }
  let comments = null;
  if (!flag('no-comments') && post.comments_url) { // comments by default (--comments still accepted)
    const r = await get(post.comments_url + (arg('sort') ? `?sort=${arg('sort')}` : ''));
    comments = r.status === 200 ? r.body : { error: gateMessage(r.status, r.body) };
    for (const c of (comments.comments || [])) await nameComment(c);
  }
  await nameMentions([post.title, post.text, ...commentTexts(comments && comments.comments)]);
  emit({ post, comments }, () => {
    printItems([post], true);
    if (post.you) console.log(`  you: ${post.you.can_comment ? 'may comment' : 'may NOT comment'} · ${post.you.can_react ? 'may react' : 'may NOT react'} · your vote ${post.you.vote || 0} · your reactions ${(post.you.reactions || []).join(' ') || 'none'}`);
    if (comments) {
      if (comments.error) return console.log(`\ncomments: ${comments.error}`);
      console.log(`\n${comments.count ?? (comments.comments || []).length} comment(s)`);
      // Each comment: who, when, the whole text, then its id, its score and reactions, and your own vote/reactions on it.
      // Replies sit indented under the comment they answer.
      const walk = (list, depth) => { for (const c of list || []) {
        const pad = '  '.repeat(depth + 1);
        console.log(`${pad}${utc(c.created_at)}  ${c.author_name || c.account_address || '?'}${depth ? ' (reply)' : ''}: ${showMentions(String(c.content ?? c.text ?? '').trim()).replace(/\n/g, '\n' + '  '.repeat(depth + 2))}`);
        const reacts = Array.isArray(c.reactions) ? c.reactions.map(r => `${r.emoji}${r.count > 1 ? r.count : ''}`).join(' ') : '';
        const mine = [c.user_vote ? `you voted ${c.user_vote > 0 ? 'up' : 'down'}` : '', (c.user_reaction_emojis || []).length ? `you reacted ${c.user_reaction_emojis.join(' ')}` : ''].filter(Boolean).join(', ');
        console.log(`${pad}  id ${c.uid || c.id} · score ${c.score ?? 0} (+${c.upvotes ?? 0}/-${c.downvotes ?? 0})${reacts ? ' · ' + reacts : ''}${mine ? ' · ' + mine : ''}`);
        walk(c.replies, depth + 1);
      } };
      walk(comments.comments, 0);
      if ((comments.comments || []).length) {
        console.log(`\nto answer a comment, REPLY to it (it threads under it):  pos comment ${post.url || url} "<text>" --reply-to=<id>`);
        console.log(`to vote or react on a comment:  pos comment ${post.url || url} --vote=up|down --on-comment=<id>   ·   --react=<emoji> --on-comment=<id>`);
      }
    }
  });
}
async function nameComment(c) {
  const a = c.account_address || c.author;
  if (isAddr(a)) c.author_name = (await nameOf(ethers.getAddress(a.toLowerCase()))) || a;
  for (const r of (c.replies || [])) await nameComment(r);
}

async function cmdTrending() { return cmdNetList('trending'); }

async function cmdNetList(kind) {
  let server = arg('server') || process.env.PUBLICOS_SSP;
  if (!server && process.env.PUBLICOS_ACCOUNT) { try { server = await sspUrl(process.env.PUBLICOS_ACCOUNT); } catch {} }
  if (!server) { // any registered social server answers: take the first in the registry
    const reg = await contract('SOCIAL_SERVER_REGISTRY_MEMORY', ['function getSocialServerSlugs(uint256,uint256) view returns (string[])',
      'function getSocialServerBySlug(string) view returns (tuple(bool exists, string slug, string title, string apiUrl, string region, address owner))']);
    server = (await reg.getSocialServerBySlug((await reg.getSocialServerSlugs(0, 1))[0])).apiUrl;
  }
  server = server.replace(/\/$/, '');
  if (kind === 'latest') {
    const { status, body } = await getJson(`${server}/api/stats/latest/feed`);
    if (status !== 200) { console.error(gateMessage(status, body)); process.exit(1); }
    const items = await decorate(body.items || []);
    await nameMentions(items.flatMap(p => [p.title, p.text]));
    return emit({ server, items }, () => {
      console.log(`latest posts on the whole network, newest first (asked ${server})`);
      if (!items.length) console.log('  nothing in the last 7 days');
      printItems(items);
    });
  }
  const cut = arg('cut', '24h');
  const { status, body } = await getJson(`${server}/api/stats/trending/feed?cut=${cut}`);
  if (status !== 200) { console.error(gateMessage(status, body)); process.exit(1); }
  const items = await decorate(body.items || []);
  await nameMentions(items.flatMap(p => [p.title, p.text]));
  emit({ server, cut, items, trending: body.trending }, () => {
    console.log(`trending on the network, window "${cut}" (asked ${server})`);
    if (!items.length) console.log('  nothing yet: a post is listed only after enough different people read it');
    printItems(items);
  });
}

async function cmdReactions(url) {
  if (!/^https?:\/\//.test(url || '')) { console.log('usage: node feed.js reactions <post url>'); process.exit(2); }
  const { status, body } = await get(url.replace(/[?#].*$/, '') + '/reactions');
  if (status !== 200) { console.error(gateMessage(status, body)); process.exit(1); }
  const who = []; for (const r of body.user_reactions || []) who.push({ emoji: r.emoji, account: r.account_address, name: (await nameOf(ethers.getAddress(r.account_address.toLowerCase()))) || r.account_address });
  emit({ totals: body.reactions, who }, () => {
    console.log((body.reactions || []).map(r => `${r.emoji} ${r.count}`).join('   ') || 'no reactions');
    for (const w of who) console.log(`  ${w.emoji}  ${w.name}`);
  });
}

async function cmdChannel(who, slug) {
  if (!who || !slug) { console.log('usage: node feed.js channel <name | address> <slug> [--signed]'); process.exit(2); }
  const { account, name } = await resolveAccount(who);
  const server = await serverFor(account, name, slug);
  const { status, body } = await get(`${server}/api/${account}/channels/${slug}`, 'list_channels');
  if (status !== 200) { console.error(gateMessage(status, body)); process.exit(1); }
  const c = body.channel;
  emit(body, () => {
    console.log(`${c.name}  (${slug}, owner ${name})  ${c.post_count} post(s)${c.is_private ? '  PRIVATE' : ''}${c.is_paid ? '  PAID' : ''}${c.sensitive ? '  sensitive' : ''}`);
    if (c.description) console.log(`  ${short(c.description)}`);
    console.log(`  who reads: ${c.read_identity}${c.read_use_channel_list ? ' + the reader list of the channel' : ''}${c.read_use_friends ? ' + the friends list of the owner' : ''}`);
    console.log(`  who posts: ${c.posting_policy} (tier ${c.posting_identity})${c.post_rate_limit ? `, at most ${c.post_rate_limit} a day` : ''}`);
    console.log(`  who comments: ${c.comment_identity} · who reacts: ${c.reaction_identity}`);
    console.log(`  quotes ${c.quote_policy || 'open'} · reposts ${c.repost_policy || 'open'} · replies ${c.reply_policy || 'open'}`);
    if (c.max_posts || c.max_days) console.log(`  history shown to readers: ${c.max_posts ? `the newest ${c.max_posts} posts` : ''}${c.max_posts && c.max_days ? ', ' : ''}${c.max_days ? `the last ${c.max_days} days` : ''}`);
    if ('follow_status' in c || c.subscription) console.log(`  you: follow request ${c.follow_status || 'never asked'}${c.subscription ? ` · subscription ${c.subscription.active ? 'active' : 'not active'}` : ''}`);
    else if (!signing() && (c.is_private || c.is_paid)) console.log('  (read signed to see where your own follow request or subscription stands)');
    console.log(`  feed ${server}/api/${account}/channels/${slug}/feed`);
  });
}

(async () => {
  const [cmd, a, b] = positional();
  if (cmd === 'reactions') return cmdReactions(a);
  if (cmd === 'channel') return cmdChannel(a, b);
  if (cmd === 'channels' && a) return cmdChannels(a);
  if (cmd === 'read') return cmdRead(a, b);
  if (cmd === 'post') return cmdPost(a);
  if (cmd === 'trending') return cmdTrending();
  if (cmd === 'latest') return cmdNetList('latest');
  console.log('usage: node feed.js channels <who> | channel <who> <slug> | read <feed url> | read <who> <slug> | post <post url> [--comments] | reactions <post url> | trending [--cut=24h] | latest   (signed by default when a key is set, --unsigned to read anonymously, --json for data)');
  process.exit(2);
})().catch(fail);
