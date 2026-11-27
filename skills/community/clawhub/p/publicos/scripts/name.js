// Names (subscriptions_and_domain.md): is a name free, what would it cost you, and renaming your account.
//   node name.js check <new name> [--months=12] [--account=<who>]   free or taken, and the price for that account
//   node name.js prices <name or account> [--months=1,6,12]       a price list for any name, held or not (nothing spent)
//   node name.js rename <new name> <months> [--dry]                 rename your account and pay <months> of the new name
// A name is unique, case-insensitive, letters and digits with - or _ inside. Shorter names cost more a month; a
// citizen's name of five or more characters costs nothing, and a citizen gets one free rename a year. The price
// depends on who asks, so `check` prices it for --account (default: PUBLICOS_ACCOUNT).
const { ethers, contract, contractAddress, resolveAccount, nameOf, account, sendTx, positional, arg, emit, fail } = require('./chain.js');

const STATUS = ['available', 'held by an account whose domain lapsed: renaming to it takes it over', 'taken', 'not available yet (cooling down, or reserved)', 'already yours'];
const DM = ['function quoteForName(address,string,uint256) view returns (uint256 cost, bool isFree)', 'function nameClaimStatus(address,string) view returns (uint8)',
  'function renameQuota(address) view returns (bool annualOpen, uint256 nextAnnualAt, uint256 bonusTickets)', 'function changeName(string,uint256)'];

(async () => {
  const [cmd, newName, months] = positional();
  const dm = await contract('DOMAIN_MANAGER', DM);
  const ox = await contract('PUBLICOS_TOKEN', ['function decimals() view returns (uint8)']); const d = await ox.decimals();
  if (cmd === 'check' && newName) {
    const who = arg('account') || process.env.PUBLICOS_ACCOUNT;
    if (!who) { // whether the name is free does not depend on who asks; its price does
      const st = Number(await dm.nameClaimStatus(ethers.ZeroAddress, newName));
      const free = st === 0 || st === 1;
      emit({ name: newName, status: STATUS[st] || String(st), can_take: free }, () => console.log(`"${newName}": ${STATUS[st] || st}\nthe price depends on the account that would hold it: add --account=<its name or address>`));
      process.exit(free ? 0 : 1);
    }
    const { account: a, name } = await resolveAccount(who);
    const m = Number(arg('months', '12'));
    const status = Number(await dm.nameClaimStatus(a, newName));
    const q = await dm.quoteForName(a, newName, m);
    const quota = await dm.renameQuota(a).catch(() => null);
    const o = { name: newName, status: STATUS[status] || String(status), can_take: status <= 1, for_account: name, months: m, cost_ox: ethers.formatUnits(q.cost, d), free: q.isFree,
      free_rename_open: quota ? quota.annualOpen : null, bonus_renames: quota ? Number(quota.bonusTickets) : null };
    emit(o, () => console.log(`"${newName}": ${o.status}\nfor ${name}: ${o.free ? 'this name is free to hold' : `${o.cost_ox} OX pays ${m} month(s) of holding this name (its domain fee)`}` +
      (quota ? `\nrenames: the yearly rename is ${quota.annualOpen ? 'available' : 'used'}${Number(quota.bonusTickets) ? `, plus ${quota.bonusTickets} bonus rename(s)` : ''}` : '') +
      `\nto see whether the network would accept it, without changing anything: node scripts/name.js rename ${newName} ${m} --dry --account=${a}`));
    process.exit(o.can_take ? 0 : 1);
  }
  if (cmd === 'prices' && newName) {
    // A price list for a name, any name, held or not: nothing is owned or spent to ask. For an existing account
    // it is that account's renewal price (quoteDomain); for a free name, what a private account or an org would pay
    // (quoteForName with no account). A "month" is the domain's 30-day period. Read-only.
    const mem = await contract('DOMAIN_MEMORY', ['function domainPaidUntil(address) view returns (uint256)', 'function maxDomainMonths() view returns (uint256)',
      'function discountBpsPerMonth() view returns (uint256)', 'function maxDiscountBps() view returns (uint256)']);
    const q = await contract('DOMAIN_MANAGER', ['function quoteDomain(address,uint256) view returns (uint256)', ...DM]);
    let holder = null; try { holder = await resolveAccount(newName); } catch {}
    const maxM = Number(await mem.maxDomainMonths()), step = Number(await mem.discountBpsPerMonth()), cap = Number(await mem.maxDiscountBps());
    const want = (arg('months') ? arg('months').split(',') : ['1', '3', '6', '12', '24', '36', '60']).map(Number).filter(m => m >= 1 && m <= maxM);
    let paid = null;
    if (holder) { paid = await mem.domainPaidUntil(holder.account); if (paid >= 32503680000n) { console.log(`${holder.name}: a citizen's name, it never needs paying`); process.exit(0); } }
    const rows = [];
    for (const m of want) {
      const cost = holder ? await q.quoteDomain(holder.account, m) : (await q.quoteForName(ethers.ZeroAddress, newName, m)).cost;
      rows.push({ months: m, cost_ox: ethers.formatUnits(cost, d), per_month_ox: (Number(ethers.formatUnits(cost, d)) / m).toFixed(4), discount_pct: Math.min((m - 1) * step, cap) / 100 });
    }
    const o = { name: holder ? holder.name : newName, held: !!holder, paid_until: paid ? new Date(Number(paid) * 1000).toISOString().slice(0, 10) : null, max_months: maxM, rows };
    emit(o, () => {
      console.log(holder ? `${holder.name}: renewal prices for this account (domain paid until ${o.paid_until})` : `"${newName}": prices for a private account or an org holding it (a citizen pays nothing for 5+ characters)`);
      console.log('  months   total OX   per month   discount');
      for (const r of rows) console.log(`  ${String(r.months).padStart(6)}   ${r.cost_ox.padStart(8)}   ${r.per_month_ox.padStart(9)}   ${r.discount_pct}%`);
      console.log(`a month is 30 days; prepay up to ${maxM}; the discount grows ${step / 100}% per extra month, up to ${cap / 100}%.`);
      if (holder) console.log(`to pay: your own name  node scripts/upkeep.js pay-domain <months>   ·   another's (your org's)  … pay-domain <months> --for=${holder.name}   (add --dry first)`);
    });
    process.exit(0);
  }
  if (cmd === 'rename' && newName && months) {
    const me = account();
    const before = await nameOf(me);
    const { hash, receipt } = await sendTx(await contractAddress('DOMAIN_MANAGER'), dm.interface.encodeFunctionData('changeName', [newName, BigInt(months)]));
    const after = await nameOf(me);
    console.log(`${hash} block ${receipt.blockNumber} status ${receipt.status} · name ${before} → ${after}`);
    process.exit(after.toLowerCase() === newName.toLowerCase() && after !== before ? 0 : 1); // a change of letter case only is not a rename
  }
  console.log('usage: node name.js check <new name> [--months=12] [--account=<who>] | prices <name or account> [--months=1,6,12] | rename <new name> <months> [--dry]');
  process.exit(2);
})().catch(fail);
