// Read a profile: every record of an account, decoded and sorted into what people see (read_profiles.md). No key needed.
//   node profile.js <name | address> [--kind=identity|social|cards|tabs|channels|hidden_tabs|marks|settings|other] [--key=<record key>] [--full] [--json]   (values over 150 chars are cut unless --full)
// A profile IS its records. Each stored value is a JSON string holding the real value and its metadata; this
// script parses it for you and groups the records the way PublicOS clients do:
//   identity  profile.avatar · profile.banner · profile.bio · profile.color · the page background · NFT pointers
//   social    the fixed list of networks (com.twitter, com.github, url, email …): handle in value, URL in metadata.link
//   cards     card.<id>: content, image, NFT, app, tip and pinned-post cards
//   tabs      record type 2 whose JSON says "subtype":"tab": a web tab on the profile
//   channels  record type 2 whose JSON says "subtype":"channel": a feed, value = its URL
//   hidden_tabs  record type 2 with neither: the apps show it nowhere (fix: rewrite it with the subtype)
//   marks     automated_account · skill (the URL of a SKILL.md this account publishes for agents)
//   settings  record type 1: app settings the owner stored on chain
//   other     anything else (clients do not show these to people)
const { resolveAccount, records, positional, arg, flag, emit, fail } = require('./chain.js');

const IDENTITY = new Set(['profile.avatar', 'profile.banner', 'profile.bio', 'profile.color', 'profile.status',
  '_osux_profile_background_url_', 'profile.avatar.nft', 'profile.banner.nft']);
// The fixed list of networks PublicOS clients show as social links. A profile record under any other key is not shown.
const SOCIAL = new Set(['com.twitter', 'com.instagram', 'com.github', 'app.bsky', 'com.linkedin', 'org.telegram',
  'com.reddit', 'com.youtube', 'xyz.farcaster', 'url', 'email']);
const isHttp = (v) => typeof v === 'string' && /^https?:\/\//i.test(v);

function kindOf(r) {
  if (r.key === 'automated_account' || r.key === 'skill') return 'marks';   // skill: where agents find this account's SKILL.md
  if (IDENTITY.has(r.key)) return 'identity';
  if (r.key.startsWith('card.')) return 'cards';
  // Tabs and channels are judged the way the apps judge them: by the "subtype" INSIDE the stored JSON, not by the
  // contract's customType column. A type-2 record without "tab" or "channel" there is shown nowhere in the apps.
  if (r.type === 2) {
    const sub = r.record && typeof r.record === 'object' ? r.record.subtype : undefined;
    if (sub === 'channel') return 'channels';
    if (sub === 'tab') return 'tabs';
    return 'hidden_tabs';
  }
  if (r.type === 1) return 'settings';
  if (r.type === 0 && SOCIAL.has(r.key)) return 'social';
  return 'other';
}

function cardKind(r) {
  const m = r.metadata || {};
  if (m.cardKind) return m.cardKind;
  let v = r.value; if (typeof v === 'string') { try { v = JSON.parse(v); } catch {} }
  if (v && typeof v === 'object' && v.app) return 'app';
  if (m.tip) return 'tip';
  if (m.isImageRecord || m.image) return 'image';
  return 'text';
}

(async () => {
  const [who] = positional();
  if (!who) { console.log('usage: node profile.js <name | address> [--kind=…] [--key=…] [--json]'); process.exit(2); }
  const { account, name } = await resolveAccount(who);
  let recs = (await records(account)).map(r => ({ ...r, kind: kindOf(r) }));
  recs.forEach(r => { if (r.kind === 'cards') r.card_kind = cardKind(r); delete r.record; });
  const wantKind = arg('kind'), wantKey = arg('key');
  if (wantKey) recs = recs.filter(r => r.key === wantKey);
  if (wantKind) recs = recs.filter(r => r.kind === wantKind);
  const order = ['identity', 'marks', 'social', 'cards', 'tabs', 'channels', 'hidden_tabs', 'settings', 'other'];
  const groups = Object.fromEntries(order.map(k => [k, recs.filter(r => r.kind === k)]).filter(([, v]) => v.length));

  emit({ account, name, count: recs.length, groups }, () => {
    console.log(`${name}   ${account}   ${recs.length} record(s)`);
    const show = (v) => { const t = (typeof v === 'string' ? v : JSON.stringify(v)); const one = t.replace(/\s+/g, ' ');
      return flag('full') || one.length <= 150 ? t : `${one.slice(0, 150)} … (${t.length} chars, CUT: add --full to see it whole)`; };
    for (const [k, list] of Object.entries(groups)) {
      console.log(`\n${k}${k === 'hidden_tabs' ? '   (type-2 records the apps do NOT show: the stored JSON has no "subtype":"tab" or "channel"; rewrite them with it)' : ''}`);
      for (const r of list) {
        const m = r.metadata || {}; const bits = [];
        if (k === 'cards') bits.push(`[${r.card_kind}]`);
        if (m.name) bits.push(`"${m.name}"`);
        if (r.value !== '' && r.value != null) bits.push(show(r.value));
        if (m.image) bits.push(`image ${m.image}`);
        if (k === 'tabs' && m.url && m.url !== r.value) bits.push(`url ${m.url}`);
        if (m.link) bits.push(`→ ${m.link}`);
        if (m.tip) bits.push(`tip → ${m.tip.to} (chain ${m.tip.chainId})`);
        if (r.expired) bits.push('(EXPIRED)');
        console.log(`  ${r.key.padEnd(30)} ${bits.join('  ')}`);
      }
    }
  });
})().catch(fail);
