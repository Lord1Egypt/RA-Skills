// An account's money (send_ox.md, subscriptions_and_domain.md): what it holds, what moved, what it can collect.
//   node money.js balance <name | address>            OX in the MainSafe, the service balance, what it can claim, what it owes
//   node money.js history <name | address> [--days=7 | --from=<block>] [--to=<block>]    payments in and out, with names
//   node money.js claim [--dry]                        collect what the account can claim into its MainSafe (needs your key)
//   add --json for the full data
// Money never sits in an account or a key: it is in the account's MainSafe. "Claim" pays out, in one call, a citizen's
// share of the fees, a provider's earnings, grants and the welcome bonus, minus any penalty owed. To pay someone,
// use send_ox.js.
const { ethers, pub, contract, contractAddress, resolveAccount, nameOf, logs, account, sendTx, positional, arg, emit, fail } = require('./chain.js');

const soft = async (fn, dflt = null) => { try { return await fn(); } catch { return dflt; } };

async function balance(who) {
  const { account: a, name } = await resolveAccount(who);
  const ox = await contract('PUBLICOS_TOKEN', ['function balanceOf(address) view returns (uint256)', 'function decimals() view returns (uint8)', 'function frozen(address) view returns (bool)']);
  const d = await ox.decimals(); const f = (v) => ethers.formatUnits(v, d);
  const safe = await (await contract('SAFE_MANAGER', ['function getMainSafeAddress(address) view returns (address)'])).getMainSafeAddress(a);
  const o = { account: a, name, main_safe: safe, ox: f(await ox.balanceOf(safe)), frozen: await soft(() => ox.frozen(safe), false) };
  const isOrg = await (await contract('ACCOUNT_MEMORY', ['function getIsOrgAccount(address) view returns (bool)'])).getIsOrgAccount(a);
  if (!isOrg) {
    const sm = await contract('SUBS_MEMORY', ['function getAccount(address) view returns (tuple(uint128 balance, uint64 checkpoint, uint64 lastSeen))', 'function fee(uint8) view returns (uint256)', 'function slugOf(uint8,address) view returns (string)']);
    const sM = await contract('SUBS_MANAGER', ['function coveredUntil(address) view returns (uint256)', 'function previewSettle(address) view returns (uint256 toBsp, uint256 toSsp, bool minted)']);
    const acct = await soft(() => sm.getAccount(a));
    if (acct) {
      const [bsp, ssp] = [await sm.slugOf(0, a), await sm.slugOf(1, a)];
      const owed = await soft(() => sM.previewSettle(a));
      const covered = await soft(() => sM.coveredUntil(a));
      o.services = { balance: f(acct.balance), bsp: bsp || null, ssp: ssp || null,
        fee_per_month: f((bsp ? await sm.fee(0) : 0n) + (ssp ? await sm.fee(1) : 0n)),
        owed_to_providers_now: owed ? f(owed.toBsp + owed.toSsp) : null, paid_by_the_network: owed ? owed.minted : null,
        covered_until: covered ? new Date(Number(covered) * 1000).toISOString().slice(0, 10) : null };
    }
    const acc = await soft(async () => (await contract('ACCUMULATOR', ['function previewClaim(address) view returns (uint256 total, uint256 directPart, uint256 stipendPart, uint256 garnished)'])).previewClaim(a));
    if (acc) o.claimable = { total: f(acc.total), earnings_and_grants: f(acc.directPart), share_of_fees: f(acc.stipendPart), kept_for_penalties: f(acc.garnished) };
  }
  o.penalties_owed = await soft(async () => f(await (await contract('PENALTIES_MANAGER', ['function owed(address) view returns (uint256)'])).owed(a)), null);
  emit(o, () => {
    console.log(`${name}   ${a}`);
    console.log(`MainSafe     ${o.ox} OX   ${safe}${o.frozen ? '   FROZEN: cannot send or receive' : ''}`);
    if (o.services) console.log(`services     ${o.services.balance} OX on deposit · ${o.services.fee_per_month} OX a month (${[o.services.bsp && 'chain: ' + o.services.bsp, o.services.ssp && 'social: ' + o.services.ssp].filter(Boolean).join(', ') || 'no providers'})` +
      (o.services.paid_by_the_network ? ' · paid by the network (citizen)' : o.services.covered_until ? ` · covered until ${o.services.covered_until}` : ''));
    if (o.claimable) console.log(`can claim    ${o.claimable.total} OX` + (Number(o.claimable.total) > 0 ? `  (earnings and grants ${o.claimable.earnings_and_grants}, share of fees ${o.claimable.share_of_fees}${Number(o.claimable.kept_for_penalties) > 0 ? `, ${o.claimable.kept_for_penalties} kept back for penalties` : ''})   node money.js claim` : ''));
    if (o.penalties_owed !== null) console.log(`owes         ${o.penalties_owed} OX in penalties${Number(o.penalties_owed) > 0 ? '   (node standing.js for the list)' : ''}`);
  });
}

async function history(who) {
  const { account: a, name } = await resolveAccount(who);
  const sm = await contract('SAFE_MANAGER', ['function getMainSafeAddress(address) view returns (address)', 'function getSafeOwnerAccount(address) view returns (address)']);
  const safe = await sm.getMainSafeAddress(a);
  const token = await contractAddress('PUBLICOS_TOKEN');
  const ox = await contract('PUBLICOS_TOKEN', ['function decimals() view returns (uint8)']); const d = await ox.decimals();
  const head = await pub.getBlockNumber();
  const from = arg('from') !== undefined ? Number(arg('from')) : arg('days') !== undefined ? Math.max(0, head - Math.round(Number(arg('days')) * 43200)) : 0; // a block every 2 s; default: everything
  const to = arg('to') ? Number(arg('to')) : head;
  const T = ethers.id('Transfer(address,address,uint256)'), me = ethers.zeroPadValue(safe, 32);
  const out = (await logs(token, [T, me], from, to)).logs, inn = (await logs(token, [T, null, me], from, to)).logs;
  const who2 = {};
  const label = async (addr) => {
    if (addr in who2) return who2[addr];
    if (addr === ethers.ZeroAddress) return (who2[addr] = 'the network (minted or burned)');
    let owner = ethers.ZeroAddress; try { owner = await sm.getSafeOwnerAccount(addr); } catch {}
    return (who2[addr] = owner !== ethers.ZeroAddress ? (await nameOf(owner)) || owner : (await nameOf(addr)) || `${addr} (a contract or outside address)`);
  };
  const rows = []; const stamps = {};
  const when = async (b) => (stamps[b] = stamps[b] || new Date((await pub.getBlock(b)).timestamp * 1000).toISOString().slice(0, 16).replace('T', ' ') + ' UTC');
  for (const l of [...out.map(x => [x, 'out']), ...inn.map(x => [x, 'in'])]) {
    const [log, dir] = l; const other = ethers.getAddress('0x' + log.topics[dir === 'out' ? 2 : 1].slice(26));
    rows.push({ block: Number(log.blockNumber), date: await when(Number(log.blockNumber)), direction: dir, amount: ethers.formatUnits(BigInt(log.data), d), counterparty: await label(other), counterparty_address: other, tx: log.transactionHash });
  }
  rows.sort((x, y) => x.block - y.block);
  emit({ account: a, name, main_safe: safe, from, to, payments: rows, next_from: to + 1 }, () => {
    console.log(`${name}: ${rows.length} OX movement(s) ${from === 0 ? 'in its whole history' : `since block ${from} (older ones were not looked at)`}, up to block ${to}`);
    for (const r of rows) console.log(`  ${r.date}  block ${String(r.block).padStart(8)}  ${r.direction === 'in' ? 'IN  +' : 'OUT -'}${r.amount.padStart(12)} OX  ${r.direction === 'in' ? 'from' : 'to  '} ${r.counterparty}`);
    console.log(`next time: --from=${to + 1}`);
  });
}

(async () => {
  const [cmd, who] = positional();
  if (cmd === 'balance' && who) return balance(who);
  if (cmd === 'history' && who) return history(who);
  if (cmd === 'claim') {
    const me = account();
    const acc = await contract('ACCUMULATOR', ['function previewClaim(address) view returns (uint256 total, uint256 directPart, uint256 stipendPart, uint256 garnished)', 'function claim()']);
    const ox = await contract('PUBLICOS_TOKEN', ['function decimals() view returns (uint8)']); const d = await ox.decimals();
    const p = await acc.previewClaim(me);
    if (p.total === 0n) { console.log('nothing to claim'); process.exit(3); }
    console.log(`claiming ${ethers.formatUnits(p.total, d)} OX into the MainSafe`);
    const { hash, receipt } = await sendTx(await acc.getAddress(), acc.interface.encodeFunctionData('claim'));
    const after = await acc.previewClaim(me);
    console.log(`${hash} block ${receipt.blockNumber} status ${receipt.status} · left to claim ${ethers.formatUnits(after.total, d)} OX`);
    process.exit(receipt.status === 1 && after.total < p.total ? 0 : 1);
  }
  console.log('usage: node money.js balance <who> | history <who> [--days=7 | --from=<block>] | claim [--dry]');
  process.exit(2);
})().catch(fail);
