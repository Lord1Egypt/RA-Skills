// Run a channel of your own: create it, change its settings, show it on your profile, export it, delete it
// (write_post.md, "A channel of your own"). A channel lives on YOUR social server, owned by your account; an org cannot own one,
// but it can show one on its profile (node org.js propose <org> publish-channel <owner>/<slug>).
//   node channel.js create <slug> "<name>" [settings]
//   node channel.js set <slug> [settings]                 change only what you name
//   node channel.js publish <slug> ["<label>"]            put it on your profile (a chain record: followers find it there)
//   node channel.js unpublish <slug>                      take it off your profile (the channel stays)
//   node channel.js export <slug> > backup.json           every post, as stored
//   node channel.js delete <slug> --yes                   deletes the channel AND everything in it, for good
// Settings (all optional):
//   --description="…"  --icon=<image url>  --language=en  --tags=a,b,c  --name="…" (set only)
//   --read=anyone|signed|account|standing|citizen     the lowest tier that may read
//   --private | --public        private: only accounts on the channel's reader list read it (people ask to follow, you approve)
//   --posting=owner|open|approved   who may post          --post-tier=<tier>   --rate-limit=<posts per day, 0 = none>
//   --comment=<tier>  --react=<tier>                      who may comment / react
//   --quotes=open|closed  --reposts=open|closed  --replies=open|closed
//   --max-posts=<n>  --max-days=<n>                       how much history readers are served (0 = no limit)
//   --sensitive=true|false      --secret=true|false       secret: left out of the public channel listing
// The tiers, lowest first: anyone, signed (any valid signature), account, standing (an account in good standing),
// citizen. Once a channel has been private its read tier stays at least "signed".
// Read a channel's settings (yours or anyone's) with: node feed.js channel <who> <slug>
const { sendEnvelope } = require('./envelope.js');
const { ethers, pub, sspUrl, contractAddress, sendTx, positional, arg, flag, fail, channelTabRecord } = require('./chain.js');

function settings() {
  const d = {};
  const str = (flagName, field) => { if (arg(flagName) !== undefined) d[field] = arg(flagName); };
  const num = (flagName, field) => { if (arg(flagName) !== undefined) d[field] = Number(arg(flagName)); };
  const bool = (flagName, field) => { if (arg(flagName) !== undefined) d[field] = arg(flagName) === 'true'; };
  str('description', 'description'); str('icon', 'icon_url'); str('language', 'language');
  str('read', 'read_identity'); str('posting', 'posting_policy'); str('layout', 'layout'); str('post-tier', 'posting_identity');
  str('comment', 'comment_identity'); str('react', 'reaction_identity');
  str('quotes', 'quote_policy'); str('reposts', 'repost_policy'); str('replies', 'reply_policy');
  num('rate-limit', 'post_rate_limit'); num('max-posts', 'max_posts'); num('max-days', 'max_days');
  bool('sensitive', 'sensitive'); bool('secret', 'secret');
  if (arg('tags') !== undefined) d.tags = arg('tags').split(',').map(s => s.trim()).filter(Boolean);
  if (flag('private')) d.read_use_channel_list = true;
  if (flag('public')) { d.read_use_channel_list = false; d.read_use_friends = false; }
  return d;
}
const summary = (c) => `${c.slug}  "${c.name}"  read:${c.read_identity}${c.is_private ? ' PRIVATE' : ''}  posting:${c.posting_policy}  layout:${c.layout || 'feed'}  comment:${c.comment_identity}  react:${c.reaction_identity}${c.secret ? '  secret' : ''}`;

(async () => {
  const [cmd, slug, label] = positional();
  const account = process.env.PUBLICOS_ACCOUNT;
  if (!account) throw new Error('set PUBLICOS_ACCOUNT to the account your key signs for');
  if (!cmd || !slug) { console.log('usage: node channel.js create <slug> "<name>" [settings] | set <slug> [settings] | publish <slug> ["<label>"] | unpublish <slug> | export <slug> | delete <slug> --yes'); process.exit(2); }
  const me = ethers.getAddress(account.toLowerCase());
  const server = await sspUrl(me);                 // your own social server, from the chain
  const root = `/api/${me}/channels`;
  const feedUrl = `${server}${root}/${slug}/feed`;

  if (cmd === 'create') {
    if (!label) { console.log('give the channel a name: node channel.js create <slug> "<name>"'); process.exit(2); }
    const { status, body } = await sendEnvelope('POST', server, root, 'create_channel', { account_address: me, slug, name: label, ...settings() });
    console.log(status, status === 201 ? `created ${summary(body.channel)}\n  feed ${feedUrl}\n  not on your profile yet: node channel.js publish ${slug}` : JSON.stringify(body));
    process.exit(status === 201 ? 0 : 1);
  }
  if (cmd === 'set') {
    const d = settings(); if (arg('name') !== undefined) d.name = arg('name');
    if (!Object.keys(d).length) { console.log('name at least one setting to change'); process.exit(2); }
    const { status, body } = await sendEnvelope('PUT', server, `${root}/${slug}`, 'update_channel', { account_address: me, ...d });
    console.log(status, status === 200 ? `now ${summary(body.channel)}` : JSON.stringify(body));
    process.exit(status === 200 ? 0 : 1);
  }
  if (cmd === 'export') {
    const { status, body } = await sendEnvelope('GET', server, `${root}/${slug}/export`, 'export_channel', { account_address: me });
    if (status !== 200) { console.error(status, JSON.stringify(body)); process.exit(1); }
    console.log(typeof body === 'string' ? body : JSON.stringify(body, null, 2)); return;
  }
  if (cmd === 'delete') {
    if (!flag('yes')) { console.log(`this deletes "${slug}" and every post, comment and reaction in it, for good. Export it first if in doubt. Add --yes to go ahead.`); process.exit(2); }
    const { status, body } = await sendEnvelope('DELETE', server, `${root}/${slug}`, 'delete_channel', { account_address: me });
    console.log(status, JSON.stringify(body)); process.exit(status === 200 ? 0 : 1);
  }
  if (cmd === 'publish' || cmd === 'unpublish') {
    // The profile record that makes a channel visible: a channel tab (router, type 2, subtype "channel", key channel.<slug>),
    // whose value is the channel's JSON URL; never expires (records standard).
    const t = channelTabRecord(server, me, slug, label);
    let key = t.key;
    const iface = new ethers.Interface(['function setRecord(address,string,string,uint256,uint8,string)', 'function deleteRecord(address,string)']);
    const RM = await contractAddress('RECORD_MANAGER');
    if (cmd === 'unpublish') { // a channel published before 2026-11-16 sits under rss.<slug>
      const bp = new ethers.Contract(me, ['function getRecord(string) view returns (string,uint256,uint8,string,bool,bool)'], pub);
      if (!(await bp.getRecord(key))[4] && (await bp.getRecord(`rss.${slug}`))[4]) key = `rss.${slug}`;
    }
    console.log(`${cmd} ${key}${cmd === 'publish' ? ` -> ${t.url}` : ''}`);
    const data = cmd === 'publish'
      ? iface.encodeFunctionData('setRecord', [me, key, t.value, 0, t.type, t.customType])
      : iface.encodeFunctionData('deleteRecord', [me, key]);
    const { hash, receipt } = await sendTx(RM, data);
    console.log(`${cmd} ${key}: ${hash} block ${receipt.blockNumber} status ${receipt.status}`);
    process.exit(receipt.status === 1 ? 0 : 1);
  }
  console.log('unknown command'); process.exit(2);
})().catch(fail);
