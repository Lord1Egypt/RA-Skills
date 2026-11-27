// Citizenship (concepts.md, find_people.md): where an account stands, vouching, and claiming.
//   node citizenship.js status <name | address>     citizen or private; vouches against the threshold; a citizen's vouch budget
//   node citizenship.js vouch <who> --yes [--dry]   (citizens only) vouch that <who> is a real, unique person you can name
//   node citizenship.js claim --yes [--dry]         (an eligible private, with a permanent key) accept the citizen agreement and become a citizen
// A citizen is an individual that other citizens vouched for. A vouch is a lasting promise by a person: the voucher
// must always be able to say who that person is. It cannot be taken back, and it is not an agent's to give: run
// `vouch` only on the explicit instruction of the citizen who owns the key, for someone THEY know. Citizenship is
// one per living person; an account run by software stays private.
const { ethers, contract, contractAddress, resolveAccount, nameOf, account, sendTx, positional, flag, emit, fail } = require('./chain.js');

const soft = async (fn, dflt = null) => { try { return await fn(); } catch { return dflt; } };

(async () => {
  const [cmd, who] = positional();
  const cm = await contract('CITIZENSHIP_MANAGER', ['function isCitizen(address) view returns (bool)', 'function wasEverCitizen(address) view returns (bool)', 'function grantingPaused() view returns (bool)', 'function agreeTermsAndClaimCitizenship(uint32)']);
  const vm = await contract('VOUCH_MANAGER', ['function getVouchCount(address) view returns (uint256)', 'function computeCurrentThreshold() view returns (uint256)', 'function getBudget(address) view returns (uint256)',
    'function hasVouched(address,address) view returns (bool)', 'function getVouchersOf(address) view returns (address[])', 'function vouch(address)']);
  if (cmd === 'status' && who) {
    const { account: a, name } = await resolveAccount(who);
    const citizen = await cm.isCitizen(a); const count = Number(await vm.getVouchCount(a)); const need = Number(await vm.computeCurrentThreshold());
    const o = { account: a, name, citizen, vouches: count, threshold: need, eligible_to_claim: !citizen && count >= need, was_ever_citizen: await soft(() => cm.wasEverCitizen(a)),
      vouch_budget: citizen ? Number(await soft(() => vm.getBudget(a), 0n)) : undefined, vouching_paused: await soft(() => cm.grantingPaused(), false) };
    return emit(o, () => console.log(`${name}: ${citizen ? 'citizen' : 'private'} · ${count} vouch(es), ${need} make an account eligible` +
      (o.eligible_to_claim ? ' · ELIGIBLE: it can claim citizenship itself (node citizenship.js claim)' : '') + (citizen ? ` · can still vouch for ${o.vouch_budget} account(s)` : '') + (o.vouching_paused ? ' · vouching is paused network-wide' : '')));
  }
  if (cmd === 'vouch' && who) {
    const me = account(); const { account: target, name } = await resolveAccount(who);
    if (!flag('yes')) { console.log(`A vouch is permanent and personal: it says the owner of this key knows who ${name} is and can always say so. Only on their explicit instruction. Add --yes to go ahead.`); process.exit(2); }
    const { hash, receipt } = await sendTx(await contractAddress('VOUCH_MANAGER'), vm.interface.encodeFunctionData('vouch', [target]));
    const done = await vm.hasVouched(me, target);
    console.log(`${hash} block ${receipt.blockNumber} status ${receipt.status} · ${done ? `vouched for ${name}: ${await vm.getVouchCount(target)} of ${await vm.computeCurrentThreshold()}` : 'NOT recorded'}`); process.exit(done ? 0 : 1);
  }
  if (cmd === 'claim') {
    const me = account();
    const version = await (await contract('AGREEMENT_MANAGER', ['function currentVersion(uint8) view returns (uint32)'])).currentVersion(3);
    if (!flag('yes')) { console.log(`Claiming citizenship accepts the citizen agreement, version ${version} (read it first: node standing.js agreement citizen). It says this account is one living person. Add --yes to go ahead.`); process.exit(2); }
    const { hash, receipt } = await sendTx(await contractAddress('CITIZENSHIP_MANAGER'), cm.interface.encodeFunctionData('agreeTermsAndClaimCitizenship', [version]));
    const now = await cm.isCitizen(me);
    console.log(`${hash} block ${receipt.blockNumber} status ${receipt.status} · ${now ? `${await nameOf(me)} is a citizen` : 'NOT a citizen'}`); process.exit(now ? 0 : 1);
  }
  console.log('usage: node citizenship.js status <who> | vouch <who> --yes | claim --yes');
  process.exit(2);
})().catch(fail);
