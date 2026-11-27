// The app directory (apps.md): apps registered on chain, each with an owner and pointers (its URL, icon, description…).
// No key needed.
//   node apps.js show <slug>                  one app: title, owner, every pointer
//   node apps.js by-owner <name | address>    the apps an account or org owns
//   node apps.js search "<title>"             by title: the WHOLE title, case-insensitive ("Manual" matches, "Man" does not)
//   node apps.js list                         every app (replays the registrations: slow, about a minute on a long chain)
// Owning an app entry (needs your key; --dry to try it without sending):
//   node apps.js register <slug> "<title>"    then:  set <slug> <pointer> <value> · unset <slug> <pointer> · title <slug> "<title>" · remove <slug> --yes
//   Registering an app advertises it nowhere: it only makes the name resolvable.
//   add --json for the full data
const { ethers, contract, contractAddress, resolveAccount, nameOf, logs, positional, emit, fail } = require('./chain.js');

const ABI = ['function getAppBySlug(string) view returns (tuple(bool exists, string slug, string title, address owner))',
  'function getAllAppPointers(string) view returns (string[], string[])', 'function getAppsByOwner(address) view returns (string[])',
  'function searchByTitle(string) view returns (string[])', 'function getTotalAppCount() view returns (uint256)'];

async function app(reg, slug) {
  const a = await reg.getAppBySlug(slug);
  if (!a.exists) return null;
  const [types, values] = await reg.getAllAppPointers(slug);
  return { slug: a.slug, title: a.title, owner: a.owner, owner_name: await nameOf(a.owner), pointers: Object.fromEntries(types.map((t, i) => [t, values[i]])) };
}
const line = (a) => `  ${a.slug.padEnd(18)} "${a.title}"  by ${a.owner_name || a.owner}  ${a.pointers.url || '(no url)'}`;

(async () => {
  const [cmd, x] = positional();
  const reg = await contract('APP_REGISTRY_MANAGER', ABI);
  if (['register', 'set', 'unset', 'title', 'remove'].includes(cmd)) { // own an app entry (needs your key; any individual may register)
    const [, slug, p1, p2] = positional();
    const { sendTx, contractAddress, flag } = require('./chain.js');
    const W = new ethers.Interface(['function registerApp(string,string)', 'function removeApp(string)', 'function updateAppTitle(string,string)', 'function setAppPointer(string,string,string)', 'function removeAppPointer(string,string)']);
    let data;
    if (cmd === 'register' && slug && p1) data = W.encodeFunctionData('registerApp', [slug, p1]);
    else if (cmd === 'title' && slug && p1) data = W.encodeFunctionData('updateAppTitle', [slug, p1]);
    else if (cmd === 'set' && slug && p1 && p2) data = W.encodeFunctionData('setAppPointer', [slug, p1, p2]);
    else if (cmd === 'unset' && slug && p1) data = W.encodeFunctionData('removeAppPointer', [slug, p1]);
    else if (cmd === 'remove' && slug) { if (!flag('yes')) { console.log(`removing "${slug}" frees the name for anyone and breaks every profile card that points at it. Add --yes to go ahead.`); process.exit(2); } data = W.encodeFunctionData('removeApp', [slug]); }
    else { console.log('usage: node apps.js register <slug> "<title>" | set <slug> <pointer> <value> | unset <slug> <pointer> | title <slug> "<title>" | remove <slug> --yes   [--dry]\npointers: url, icon, description, category_one, category_two, card_origin, playstore_link, appstore_link'); process.exit(2); }
    const { hash, receipt } = await sendTx(await contractAddress('APP_REGISTRY_MANAGER'), data);
    const now = await app(reg, slug);
    console.log(`${cmd} ${slug}: ${hash} block ${receipt.blockNumber} status ${receipt.status}`); if (now) { console.log(`  "${now.title}" owner ${now.owner_name || now.owner}`); for (const [k, v] of Object.entries(now.pointers)) console.log(`  ${k.padEnd(16)} ${v}`); }
    process.exit(receipt.status === 1 && (cmd === 'remove' ? !now : !!now) ? 0 : 1);
  }
  if (cmd === 'show' && x) {
    const a = await app(reg, x.toLowerCase());
    if (!a) { console.error(`no app is registered under "${x}"`); process.exit(1); }
    if (a.pointers.skill) console.error(`this app publishes a skill for agents: ${a.pointers.skill}`);
    return emit(a, () => { console.log(`${a.slug}   "${a.title}"   owner ${a.owner_name || '?'} ${a.owner}`); for (const [k, v] of Object.entries(a.pointers)) console.log(`  ${k.padEnd(16)} ${v}`); });
  }
  if (cmd === 'by-owner' && x) {
    const { account, name } = await resolveAccount(x);
    const list = []; for (const s of await reg.getAppsByOwner(account)) list.push(await app(reg, s));
    return emit({ owner: account, name, apps: list }, () => { console.log(`apps owned by ${name}: ${list.length}`); list.forEach(a => console.log(line(a))); });
  }
  if (cmd === 'search' && x) {
    const list = []; for (const s of await reg.searchByTitle(x)) list.push(await app(reg, s));
    return emit({ title: x, apps: list }, () => { console.log(`apps titled "${x}": ${list.length}`); list.forEach(a => console.log(line(a))); });
  }
  if (cmd === 'list') {
    const total = Number(await reg.getTotalAppCount());
    const iface = new ethers.Interface(['event AppRegistered(string indexed slug, address indexed owner, string title)']);
    const { logs: raw, head } = await logs(await contractAddress('APP_REGISTRY_MEMORY'), [iface.getEvent('AppRegistered').topicHash]);
    const owners = [...new Set(raw.map(l => ethers.getAddress('0x' + l.topics[2].slice(26))))];
    const seen = new Set(), list = [];
    for (const o of owners) for (const s of await reg.getAppsByOwner(o)) if (!seen.has(s)) { seen.add(s); list.push(await app(reg, s)); }
    return emit({ total, apps: list, block: head }, () => {
      console.log(`${total} app(s) registered`); list.forEach(a => console.log(line(a)));
      if (list.length !== total) console.log(`  (found ${list.length} of ${total}: an app whose ownership moved to an account that never registered one is not reachable this way)`);
    });
  }
  console.log('usage: node apps.js show <slug> | by-owner <who> | search "<title>" | list');
  process.exit(2);
})().catch(fail);
