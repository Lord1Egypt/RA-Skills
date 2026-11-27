// The XMTP inbox directory (messaging.md): which messaging inbox belongs to which account. No key needed.
//   node inbox.js <name>/<label>          the inbox to message, e.g. publicos/support
//   node inbox.js <name | address>        every inbox the account published, with its label
//   node inbox.js --who=<inbox id>        the account behind an inbox (who wrote to you)
//   node inbox.js publish <inbox id> <label> | relabel <inbox id> <new label> | unpublish <inbox id>   [--dry]
//                                         list YOUR inbox so people can write to yourname/label (needs your key).
//                                         A listing is a claim, not proof that the account controls that inbox.
//   add --json for the full data
// An inbox id is 32 bytes. XMTP SDKs take it as 64 lowercase hex characters WITHOUT 0x: that is what this prints.
const { contract, resolveAccount, nameOf, positional, arg, emit, fail } = require('./chain.js');
const { ethers } = require('./chain.js');

const bare = (hex) => String(hex).replace(/^0x/, '').toLowerCase();

(async () => {
  const xm = await contract('XMTP_MANAGER', ['function getAllAccountInboxIds(address) view returns (bytes[], string[])',
    'function getAccountInboxIdByLabel(address,string) view returns (bytes)', 'function getAccountAddressByInboxId(bytes) view returns (address)']);
  const [verb, p1, p2] = positional();
  if (['publish', 'relabel', 'unpublish'].includes(verb)) { // put your own XMTP inbox in the directory (needs your key)
    if (!p1 || (verb !== 'unpublish' && !p2)) { console.log('usage: node inbox.js publish <inbox id> <label> | relabel <inbox id> <new label> | unpublish <inbox id>   [--dry]'); process.exit(2); }
    const { account, sendTx, contractAddress } = require('./chain.js'); const me = account();
    const W = new ethers.Interface(['function registerInboxId(bytes,string)', 'function updateInboxIdLabel(bytes,string)', 'function removeInboxId(bytes)']);
    const id = '0x' + bare(p1); if (id.length !== 66) { console.error('an inbox id is 32 bytes: 64 hex characters'); process.exit(2); }
    const data = verb === 'publish' ? W.encodeFunctionData('registerInboxId', [id, p2]) : verb === 'relabel' ? W.encodeFunctionData('updateInboxIdLabel', [id, p2]) : W.encodeFunctionData('removeInboxId', [id]);
    const { hash, receipt } = await sendTx(await contractAddress('XMTP_MANAGER'), data);
    const owner = await xm.getAccountAddressByInboxId(id);
    const ok = verb === 'unpublish' ? owner === ethers.ZeroAddress : owner === me;
    console.log(`${verb}: ${hash} block ${receipt.blockNumber} status ${receipt.status} · ${ok ? 'done' : 'NOT done'}`); process.exit(ok ? 0 : 1);
  }
  const reverse = arg('who');
  if (reverse) {
    const account = await xm.getAccountAddressByInboxId('0x' + bare(reverse));
    if (account === ethers.ZeroAddress) { console.error('no account published that inbox'); process.exit(1); }
    const name = await nameOf(account);
    return emit({ inbox_id: bare(reverse), account, name }, () => console.log(`${bare(reverse)} belongs to ${name}   ${account}`));
  }
  const [target] = positional();
  if (!target) { console.log('usage: node inbox.js <name>/<label> | <name | address> | --who=<inbox id>'); process.exit(2); }
  const [who, label] = target.split('/');
  const { account, name } = await resolveAccount(who);
  if (label) {
    const id = await xm.getAccountInboxIdByLabel(account, label);
    if (!id || id === '0x') { console.error(`${name} has no inbox labelled "${label}" (node inbox.js ${name} lists them)`); process.exit(1); }
    return emit({ account, name, label, inbox_id: bare(id) }, () => console.log(`${name}/${label}   ${bare(id)}`));
  }
  const [ids, labels] = await xm.getAllAccountInboxIds(account);
  const inboxes = ids.map((id, i) => ({ label: labels[i], inbox_id: bare(id) }));
  emit({ account, name, inboxes }, () => {
    console.log(`${name}   ${account}   ${inboxes.length} inbox(es)`);
    for (const x of inboxes) console.log(`  ${(name + '/' + x.label).padEnd(28)} ${x.inbox_id}`);
  });
})().catch(fail);
