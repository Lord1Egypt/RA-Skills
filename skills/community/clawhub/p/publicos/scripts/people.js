// Find people (find_people.md). There is no directory and no search box: you find accounts by exact name, through the
// vouch graph, through org members, and by replaying account creations. No key needed.
//   node people.js counts                      how many individuals, orgs and citizens; the vouch threshold
//   node people.js vouchers <name | address>   who vouched for this account
//   node people.js vouchees <name | address>   who this account vouched for
//   node people.js members <org>               the members of an org
//   node people.js created [--from=<block>] [--to=<block>]   every account and org created in that range, with who created it
//   add --json for the full data
// Reading is public, but people are not a dataset: do not build contact lists from this, and do not message
// someone because you found them here (etiquette.md).
const { ethers, pub, contract, contractAddress, resolveAccount, nameOf, logs, positional, arg, emit, fail } = require('./chain.js');

const named = async (list) => { const out = []; for (const a of list) out.push({ account: a, name: await nameOf(a) }); return out; };
const printList = (title, rows) => { console.log(title); if (!rows.length) console.log('  none'); for (const r of rows) console.log(`  ${(r.name || '?').padEnd(24)} ${r.account}`); };

(async () => {
  const [cmd, who] = positional();
  if (cmd === 'counts') {
    const am = await contract('ACCOUNT_MEMORY', ['function individualCount() view returns (uint256)', 'function orgCount() view returns (uint256)']);
    const cm = await contract('CITIZENSHIP_MANAGER', ['function citizenCount() view returns (uint256)']);
    const vm = await contract('VOUCH_MANAGER', ['function computeCurrentThreshold() view returns (uint256)']);
    const o = { individuals: Number(await am.individualCount()), orgs: Number(await am.orgCount()), citizens: Number(await cm.citizenCount()),
      vouches_needed_to_be_eligible: Number(await vm.computeCurrentThreshold()), block: await pub.getBlockNumber() };
    return emit(o, () => console.log(`${o.individuals} individuals (${o.citizens} citizens, ${o.individuals - o.citizens} private) · ${o.orgs} orgs · ${o.vouches_needed_to_be_eligible} vouches make someone eligible for citizenship · block ${o.block}`));
  }
  if ((cmd === 'vouchers' || cmd === 'vouchees') && who) {
    const { account, name } = await resolveAccount(who);
    const vm = await contract('VOUCH_MANAGER', ['function getVouchersOf(address) view returns (address[])', 'function getVoucheesOf(address) view returns (address[])']);
    const rows = await named(cmd === 'vouchers' ? await vm.getVouchersOf(account) : await vm.getVoucheesOf(account));
    return emit({ account, name, [cmd]: rows }, () => printList(cmd === 'vouchers' ? `who vouched for ${name}` : `who ${name} vouched for`, rows));
  }
  if (cmd === 'members' && who) {
    const { account, name } = await resolveAccount(who);
    const os = await contract('ORG_STORAGE', ['function getMemberCount(address) view returns (uint256)', 'function getMembers(address,uint256,uint256) view returns (address[])']);
    const total = Number(await os.getMemberCount(account)); const all = [];
    for (let off = 0; off < total; off += 50) all.push(...await os.getMembers(account, off, 50));
    const rows = await named(all);
    return emit({ org: account, name, members: rows }, () => printList(`${name}: ${total} member(s)`, rows));
  }
  if (cmd === 'created') {
    const mgr = await contractAddress('ACCOUNT_MANAGER');
    const iface = new ethers.Interface([
      'event AccountCreated(address indexed account, string displayName, address indexed firstSession, address indexed minter)',
      'event OrgCreated(address indexed org, string displayName, address[] initialMembers, uint256 initialThreshold)']);
    const topics = [[iface.getEvent('AccountCreated').topicHash, iface.getEvent('OrgCreated').topicHash]];
    const from = Number(arg('from', '0')); const to = arg('to') ? Number(arg('to')) : undefined;
    const { logs: raw, head } = await logs(mgr, topics, from, to);
    const rows = [];
    for (const l of raw) {
      const ev = iface.parseLog(l); const block = Number(l.blockNumber);
      if (ev.name === 'AccountCreated') rows.push({ block, kind: 'individual', account: ev.args.account, name_at_creation: ev.args.displayName, name_now: await nameOf(ev.args.account), created_by: ev.args.minter, created_by_name: await nameOf(ev.args.minter) });
      else rows.push({ block, kind: 'org', account: ev.args.org, name_at_creation: ev.args.displayName, name_now: await nameOf(ev.args.org), first_members: ev.args.initialMembers.length });
    }
    return emit({ from, to: head, created: rows, next_from: head + 1 }, () => {
      console.log(`created in blocks ${from} → ${head}: ${rows.length}`);
      for (const r of rows) console.log(`  ${String(r.block).padStart(8)}  ${r.kind.padEnd(10)} ${(r.name_now || r.name_at_creation).padEnd(22)} ${r.account}` + (r.created_by ? `  by ${r.created_by_name || r.created_by}` : `  ${r.first_members} first member(s)`));
      console.log(`next time: --from=${head + 1}`);
      if (from === 0) console.log('(an account made when the network itself started has no creation event, so this list can be one or two shorter than `counts`)');
    });
  }
  console.log('usage: node people.js counts | vouchers <who> | vouchees <who> | members <org> | created [--from=<block>] [--to=<block>]');
  process.exit(2);
})().catch(fail);
