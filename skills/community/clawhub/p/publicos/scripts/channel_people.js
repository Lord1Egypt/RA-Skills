// Decide who is in your channel: answer follow requests, and keep its lists (follow.md, "If you own a channel").
//   node channel_people.js requests <slug> [--status=pending|approved|ignored]    who asked to follow
//   node channel_people.js approve <slug> <request id> [--expires=<RFC 3339 date>]
//   node channel_people.js ignore <slug> <request id>
//   node channel_people.js readers <slug> list | add <who> [--expires=…] | remove <who>      may read a private channel
//   node channel_people.js posters <slug> list | add <who> | remove <who>                    may post (posting = approved)
//   node channel_people.js commenters <slug> list | add <who> | remove <who>                 may comment and react, when the channel uses that list
//   node channel_people.js bans <slug> list | add <who> [--reason="…"] | remove <who>        banned from the channel
// <who> is a name or an account address. A follow request shows up in your notifications (notifications.js); `requests` lists them.
// Approving a request puts the account on the reader list; taking someone out again is `readers … remove`.
const { sendEnvelope } = require('./envelope.js');
const { ethers, sspUrl, resolveAccount, nameOf, positional, arg, flag, fail } = require('./chain.js');

const LISTS = { readers: ['whitelist', 'whitelist'], posters: ['posters', 'poster'], commenters: ['interaction-list', 'interaction_list'], bans: ['bans', 'ban'] };

(async () => {
  const [cmd, slug, x, y] = positional();
  const account = process.env.PUBLICOS_ACCOUNT;
  if (!account) throw new Error('set PUBLICOS_ACCOUNT to the account your key signs for');
  if (!cmd || !slug) { console.log('usage: node channel_people.js requests <slug> | approve <slug> <id> | ignore <slug> <id> | readers|posters|commenters|bans <slug> list|add <who>|remove <who>'); process.exit(2); }
  const me = ethers.getAddress(account.toLowerCase());
  const server = await sspUrl(me);
  const base = `/api/${me}/channels/${slug}`;
  const data = { account_address: me };
  const done = (r, good = [200, 201]) => { console.log(r.status, JSON.stringify(r.body)); process.exit(good.includes(r.status) ? 0 : 1); };

  if (cmd === 'requests') {
    const r = await sendEnvelope('GET', server, `${base}/followers?status=${arg('status', 'pending')}`, 'list_followers', data);
    if (r.status !== 200) return done(r);
    const rows = r.body.follow_requests || [];
    for (const q of rows) q.name = await nameOf(ethers.getAddress(q.requester_address.toLowerCase()));
    if (flag('json')) return console.log(JSON.stringify(rows, null, 2));
    console.log(`${rows.length} request(s), ${arg('status', 'pending')}`);
    for (const q of rows) console.log(`  ${(q.name || '?').padEnd(22)} ${q.requester_address}  ${q.status}  ${(q.created_at || '').slice(0, 10)}  id ${q.uid}`);
    return;
  }
  if (cmd === 'approve' && x) return done(await sendEnvelope('PUT', server, `${base}/followers/${x}`, 'approve_follower', { ...data, ...(arg('expires') ? { expires_at: arg('expires') } : {}) }));
  if (cmd === 'ignore' && x) return done(await sendEnvelope('PUT', server, `${base}/followers/${x}/ignore`, 'ignore_follower', data));

  if (LISTS[cmd]) {
    const [route, act] = LISTS[cmd];
    if (x === 'list' || !x) {
      const r = await sendEnvelope('GET', server, `${base}/${route}`, `list_${act === 'ban' ? 'bans' : act === 'poster' ? 'posters' : act}`, data);
      if (r.status !== 200) return done(r);
      const rows = Array.isArray(r.body) ? r.body : (r.body.items || []);
      for (const q of rows) q.name = await nameOf(ethers.getAddress(q.address.toLowerCase()));
      if (flag('json')) return console.log(JSON.stringify(rows, null, 2));
      console.log(`${cmd} of ${slug}: ${rows.length}`);
      for (const q of rows) console.log(`  ${(q.name || '?').padEnd(22)} ${q.address}${q.expires_at ? `  until ${q.expires_at.slice(0, 10)}` : ''}${q.reason ? `  (${q.reason})` : ''}`);
      return;
    }
    if ((x === 'add' || x === 'remove') && y) {
      const { account: target } = await resolveAccount(y);
      if (x === 'add') return done(await sendEnvelope('POST', server, `${base}/${route}`, `add_${act}`,
        { ...data, address: target, ...(arg('expires') ? { expires_at: arg('expires') } : {}), ...(arg('reason') ? { reason: arg('reason') } : {}) }));
      return done(await sendEnvelope('DELETE', server, `${base}/${route}/${target}`, `remove_${act}`, data));
    }
  }
  console.log('unknown command; run without arguments for the usage'); process.exit(2);
})().catch(fail);
