// Session keys: which keys act for an account, and how a key gets on or off one (get_an_account.md).
//   node keys.js list <name | address>            the account's active keys, since when, until when
//   node keys.js whose <key address>              which account a key belongs to, and whether it still works
// Getting a key onto an account. You make the key yourself and never hand over its private part: you sign a
// consent with it, and someone already on the network sends the transaction.
//   node keys.js consent-join <account> [--ttl=86400] [--minutes=60]      (run with PUBLICOS_KEY = the NEW key)
//        -> prints the line the account's owner runs. ttl = how long your key lives, in seconds; 0 = permanent.
//   node keys.js add <new key> <ttl> <deadline> <signature> [--dry]       (the owner, with one of their permanent keys)
//   node keys.js consent-new <name> [--minutes=60]                        (run with PUBLICOS_KEY = the NEW key)
//        -> prints the line a citizen runs to create an account called <name> for that key
//   node keys.js create-account <name> <new key> <deadline> <signature> [--dry]   (a citizen)
// Taking a key off, or shortening its life (your own account):
//   node keys.js remove <key address> [--dry]      never the last permanent key
//   node keys.js expire <key address> <ttl seconds from now> [--dry]
// A session key is the whole account: it can post, change the profile and move money. Add one for the shortest
// time that does the job. An expiring key cannot add keys, remove a permanent key, or touch recovery.
const { ethers, pub, contract, contractAddress, resolveAccount, nameOf, key, account, sendTx, positional, arg, emit, fail } = require('./chain.js');

const when = (t) => (Number(t) === 0 ? 'permanent' : new Date(Number(t) * 1000).toISOString().slice(0, 16).replace('T', ' ') + ' UTC');
const domain = async () => ({ name: 'PublicOS', version: '1', chainId: 4489, verifyingContract: await contractAddress('ACCOUNT_MANAGER') });
const AM = ['function getAccountSessions(address) view returns (address[])', 'function getSessionCounts(address) view returns (uint256 active, uint256 permanent)',
  'function getSessionTenure(address) view returns (tuple(address account, uint48 since, uint48 until))', 'function getSessionAccount(address) view returns (address)',
  'function sessionToAccountAddress(address) view returns (address)', 'function getAccountSuspended(address) view returns (bool)'];
const MGR = new ethers.Interface(['function addSession(address,uint256,uint256,bytes)', 'function removeSession(address)', 'function setSessionExpiry(address,uint256)',
  'function createAccount(string,address,uint256,bytes) returns (address)']);
const tx = async (label, data) => { const { hash, receipt } = await sendTx(await contractAddress('ACCOUNT_MANAGER'), data); console.log(`${label}: ${hash} block ${receipt.blockNumber} status ${receipt.status}`); return receipt.status === 1; };

(async () => {
  const [cmd, a, b, c, d] = positional();
  const am = await contract('ACCOUNT_MEMORY', AM);
  if (cmd === 'list' && a) {
    const { account: acct, name } = await resolveAccount(a);
    const rows = []; for (const s of await am.getAccountSessions(acct)) { const t = await am.getSessionTenure(s); rows.push({ key: s, since: when(t.since), until: when(t.until), permanent: Number(t.until) === 0 }); }
    return emit({ account: acct, name, keys: rows }, () => { console.log(`${name}: ${rows.length} active key(s)`); for (const r of rows) console.log(`  ${r.key}  since ${r.since}  ${r.permanent ? 'permanent' : 'until ' + r.until}`); });
  }
  if (cmd === 'whose' && a) {
    const k = ethers.getAddress(a.toLowerCase());
    const live = await am.getSessionAccount(k), raw = await am.sessionToAccountAddress(k);
    if (raw === ethers.ZeroAddress) { console.log(`${k} was never a session key of any account`); process.exit(1); }
    const t = await am.getSessionTenure(k); const name = await nameOf(raw);
    const state = live !== ethers.ZeroAddress ? 'works today' : (await am.getAccountSuspended(raw)) ? 'the account is suspended' : 'expired or removed';
    return emit({ key: k, account: raw, name, works: live !== ethers.ZeroAddress, state, since: when(t.since), until: when(t.until) },
      () => console.log(`${k} is a key of ${name} ${raw}: ${state} · since ${when(t.since)} · ${Number(t.until) === 0 ? 'permanent' : 'until ' + when(t.until)}`));
  }
  const deadlineIn = () => Math.floor(Date.now() / 1000) + Number(arg('minutes', '60')) * 60;
  if (cmd === 'consent-join' && a) {
    const { account: acct, name } = await resolveAccount(a); const me = key(); const ttl = Number(arg('ttl', '86400')); const deadline = deadlineIn();
    const sig = await me.signTypedData(await domain(), { SessionConsent: [{ name: 'account', type: 'address' }, { name: 'newSession', type: 'address' }, { name: 'ttl', type: 'uint256' }, { name: 'deadline', type: 'uint256' }] },
      { account: acct, newSession: me.address, ttl, deadline });
    console.log(`Consent signed by ${me.address} to act for ${name} ${ttl ? `for ${ttl} seconds` : 'PERMANENTLY'}. Valid for ${arg('minutes', '60')} minutes.\nThe owner of ${name} runs (or scans the same data in the app):\n  node keys.js add ${me.address} ${ttl} ${deadline} ${sig}`);
    return;
  }
  if (cmd === 'consent-new' && a) {
    const me = key(); const deadline = deadlineIn();
    const taken = await (await contract('ACCOUNT_MEMORY', ['function getAccountAddressByDisplayName(string) view returns (address)'])).getAccountAddressByDisplayName(a);
    if (taken !== ethers.ZeroAddress) { console.error(`the name "${a}" is taken`); process.exit(1); }
    const version = await (await contract('AGREEMENT_MANAGER', ['function currentVersion(uint8) view returns (uint32)'])).currentVersion(1);
    const sig = await me.signTypedData(await domain(), { CreateAccountConsent: [{ name: 'displayName', type: 'string' }, { name: 'newSession', type: 'address' }, { name: 'deadline', type: 'uint256' }, { name: 'protocolVersion', type: 'uint256' }] },
      { displayName: a, newSession: me.address, deadline, protocolVersion: version });
    console.log(`Consent signed by ${me.address} for a new account "${a}", accepting protocol agreement version ${version} (read it: node standing.js agreement protocol). Valid for ${arg('minutes', '60')} minutes.\nA citizen runs:\n  node keys.js create-account ${a} ${me.address} ${deadline} ${sig}`);
    return;
  }
  if (cmd === 'add' && a && b !== undefined && c && d) {
    const ok = await tx(`addSession ${a}`, MGR.encodeFunctionData('addSession', [a, BigInt(b), BigInt(c), d]));
    const owner = await am.getSessionAccount(a); console.log(owner === account() ? 'the key now acts for the account' : 'NOT added'); process.exit(ok && owner === account() ? 0 : 1);
  }
  if (cmd === 'create-account' && a && b && c && d) {
    const ok = await tx(`createAccount ${a}`, MGR.encodeFunctionData('createAccount', [a, b, BigInt(c), d]));
    const created = await am.getSessionAccount(b); console.log(created !== ethers.ZeroAddress ? `created ${a} ${created}` : 'NOT created'); process.exit(ok && created !== ethers.ZeroAddress ? 0 : 1);
  }
  if (cmd === 'remove' && a) {
    const ok = await tx(`removeSession ${a}`, MGR.encodeFunctionData('removeSession', [a]));
    const still = await am.getSessionAccount(a); process.exit(ok && still === ethers.ZeroAddress ? 0 : 1);
  }
  if (cmd === 'expire' && a && b !== undefined) {
    const ok = await tx(`setSessionExpiry ${a} ${b}s`, MGR.encodeFunctionData('setSessionExpiry', [a, BigInt(b)]));
    const t = await am.getSessionTenure(a); console.log(`now until ${when(t.until)}`); process.exit(ok ? 0 : 1);
  }
  console.log('usage: node keys.js list <who> | whose <key> | consent-join <account> [--ttl=] | add <key> <ttl> <deadline> <sig> | consent-new <name> | create-account <name> <key> <deadline> <sig> | remove <key> | expire <key> <ttl>');
  process.exit(2);
})().catch(fail);
