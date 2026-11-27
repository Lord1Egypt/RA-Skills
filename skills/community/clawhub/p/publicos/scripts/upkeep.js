// Keep an account running (subscriptions_and_domain.md): pay the domain, join or top up a provider, leave, withdraw.
//   node upkeep.js pay-domain <months> [--for=<account>]   --for pays another account's domain (an org's) from your MainSafe
//   node upkeep.js subscribe <bsp|ssp> <slug> <topUp in OX>     (topUp 0 is allowed; same slug again = top up only)
//   node upkeep.js leave <bsp|ssp>
//   node upkeep.js withdraw <amount in OX>
// Every amount is in OX and converted with the token's decimals (18): never pass raw wei by hand.
// The managers take the OX from your MainSafe themselves, so no SAFE_AUTH step. Simulates first, then
// proves the result by reading the state back (a mined transaction alone proves nothing).
const { ethers, pub, contractAddress, account, sendTx, resolveAccount } = require('./chain.js');

const AXIS = { bsp: 0, ssp: 1 };

(async () => {
  const [verb, a1, a2, a3] = process.argv.slice(2);
  const me = account();
  const OX = new ethers.Contract(await contractAddress('PUBLICOS_TOKEN'), ['function decimals() view returns (uint8)'], pub);
  const dec = await OX.decimals();
  const subs = new ethers.Contract(await contractAddress('SUBS_MANAGER'), [
    'function subscribe(uint8,string,uint256)', 'function leave(uint8)', 'function withdraw(uint256)',
    'function isActive(uint8,address) view returns (bool)', 'function coveredUntil(address) view returns (uint256)',
    'function canJoin(uint8,string,address) view returns (bool)'], pub);
  const subsMem = new ethers.Contract(await contractAddress('SUBS_MEMORY'), ['function slugOf(uint8,address) view returns (string)'], pub);
  const when = t => (t >= 32503680000n ? 'never' : new Date(Number(t) * 1000).toISOString().slice(0, 10));

  if (verb === 'pay-domain') {
    const months = BigInt(a1 || 0);
    if (months < 1n) throw new Error('months must be 1 or more');
    const dm = new ethers.Contract(await contractAddress('DOMAIN_MANAGER'),
      ['function payDomain(uint256)', 'function topUpDomain(address,uint256)', 'function quoteDomain(address,uint256) view returns (uint256)'], pub);
    const mem = new ethers.Contract(await contractAddress('DOMAIN_MEMORY'), ['function domainPaidUntil(address) view returns (uint256)'], pub);
    // --for=<name or 0x…>: pay another account's domain (an org's, say) from YOUR MainSafe. A gift: no vote, no refund.
    const forArg = (process.argv.find(x => x.startsWith('--for=')) || '').slice(6);
    const who = forArg ? (await resolveAccount(forArg)).account : me;
    const before = await mem.domainPaidUntil(who);
    if (before === 32503680000n) { console.log('domain is NEVER (never pays): nothing to do'); process.exit(0); }
    console.log(`${forArg ? forArg + "'s " : ''}domain paid until ${when(before)}; ${months} month(s) cost ${ethers.formatUnits(await dm.quoteDomain(who, months), dec)} OX${forArg ? ', paid from your MainSafe' : ''}`);
    const call = forArg ? dm.interface.encodeFunctionData('topUpDomain', [who, months]) : dm.interface.encodeFunctionData('payDomain', [months]);
    const { hash } = await sendTx(await dm.getAddress(), call);
    const after = await mem.domainPaidUntil(who);
    console.log(`${hash}: paid until ${when(after)}`);
    process.exit(after > before ? 0 : 1);
  }

  if (verb === 'subscribe') {
    const axis = AXIS[a1]; if (axis === undefined || !a2) throw new Error('usage: subscribe <bsp|ssp> <slug> <topUp OX>');
    const topUp = ethers.parseUnits(a3 || '0', dec);
    const current = await subsMem.slugOf(axis, me);
    if (current !== a2 && !(await subs.canJoin(axis, a2, me))) throw new Error(`"${a2}" does not admit this account (invite-only, full, or banned)`);
    const before = await subs.coveredUntil(me);
    const { hash } = await sendTx(await subs.getAddress(), subs.interface.encodeFunctionData('subscribe', [axis, a2, topUp]));
    const [active, slug, after] = await Promise.all([subs.isActive(axis, me), subsMem.slugOf(axis, me), subs.coveredUntil(me)]);
    console.log(`${hash}: ${a1} ${slug} active=${active}, covered until ${when(before)} -> ${when(after)}`);
    process.exit(slug === a2 ? 0 : 1);
  }

  if (verb === 'leave') {
    const axis = AXIS[a1]; if (axis === undefined) throw new Error('usage: leave <bsp|ssp>');
    const { hash } = await sendTx(await subs.getAddress(), subs.interface.encodeFunctionData('leave', [axis]));
    const slug = await subsMem.slugOf(axis, me);
    console.log(`${hash}: ${a1} slug now "${slug}"`);
    process.exit(slug === '' ? 0 : 1);
  }

  if (verb === 'withdraw') {
    const amount = ethers.parseUnits(a1 || '0', dec);
    const token = new ethers.Contract(await OX.getAddress(), ['function balanceOf(address) view returns (uint256)'], pub);
    const safe = await new ethers.Contract(await contractAddress('SAFE_MANAGER'), ['function getMainSafeAddress(address) view returns (address)'], pub).getMainSafeAddress(me);
    const before = await token.balanceOf(safe);
    const { hash } = await sendTx(await subs.getAddress(), subs.interface.encodeFunctionData('withdraw', [amount]));
    const after = await token.balanceOf(safe);
    console.log(`${hash}: MainSafe +${ethers.formatUnits(after - before, dec)} OX`);
    process.exit(after > before ? 0 : 1);
  }

  console.log('usage: node upkeep.js pay-domain <months> [--for=<account>] | subscribe <bsp|ssp> <slug> <topUp OX> | leave <bsp|ssp> | withdraw <OX>');
  process.exit(2);
})().catch(e => { console.error('ERR', e.shortMessage || e.message); process.exit(1); });
