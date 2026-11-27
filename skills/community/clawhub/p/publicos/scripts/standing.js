// Is this account in good standing, and what is coming at it (etiquette.md, subscriptions_and_domain.md). No key needed
// for the reads.
//   node standing.js <name | address>              can it transact, is it suspended or about to be, penalties (with
//                                                  reasons and deadlines), blocks on services, frozen money, a key reset
//                                                  announced against it, its record as a flagger, the agreements it accepted
//   node standing.js agreement protocol|operator|citizen [--account=<who>]   the text in force, and what an account accepted
//   node standing.js why <key address> [<contract name>]     would the network admit a transaction from this key, and if not, why
//   node standing.js pay-penalty <who> <amount in OX> [--dry]  pay a penalty (yours or anyone's) from your MainSafe
//   add --json for the full data. Exits 1 when something needs attention.
// Words: a PENALTY is a debt the court put on an account, with a reason and a pay-before date. A SUSPENSION stops
// every session key of the account; it is announced 10 days before it lands. FROZEN money cannot be sent or received.
const { ethers, pub, contract, contractAddress, resolveAccount, account, sendTx, whyRejected, positional, arg, emit, fail } = require('./chain.js');

const soft = async (fn, dflt = null) => { try { return await fn(); } catch { return dflt; } };
const day = (t) => (Number(t) ? new Date(Number(t) * 1000).toISOString().slice(0, 16).replace('T', ' ') + ' UTC' : null);
const KINDS = { protocol: 1, operator: 2, citizen: 3 };
const PSTATUS = ['open', 'paid', 'cancelled', 'promoted (closed as unpaid)'];

(async () => {
  const [cmd, a, b] = positional();
  if (cmd === 'agreement' && KINDS[a]) {
    const mgr = await contract('AGREEMENT_MANAGER', ['function currentVersion(uint8) view returns (uint32)']);
    const mem = await contract('AGREEMENT_MEMORY', ['function getVersion(uint8,uint32) view returns (tuple(string text, bytes32 textHash, uint64 publishedAt, uint64 validFrom))', 'function agreedOf(uint8,address) view returns (tuple(uint32 version, uint64 at))']);
    const v = Number(await mgr.currentVersion(KINDS[a]));
    if (!v) { console.log(`no ${a} agreement is published`); return; }
    const t = await mem.getVersion(KINDS[a], v);
    const who = arg('account') || process.env.PUBLICOS_ACCOUNT; let accepted = null;
    if (who) { const { account: acct, name } = await resolveAccount(who); const x = await mem.agreedOf(KINDS[a], acct); accepted = { account: name, version: Number(x.version), at: day(x.at) }; }
    return emit({ kind: a, version: v, in_force_since: day(t.validFrom), text: t.text, accepted }, () => {
      console.log(`${a} agreement, version ${v}, in force since ${day(t.validFrom)}` + (accepted ? `\n${accepted.account} ${accepted.version ? `accepted version ${accepted.version} on ${accepted.at}` : 'has not accepted it'}` : '') + `\n\n${t.text}`);
    });
  }
  if (cmd === 'why' && a) {
    const to = await contractAddress(b || 'RECORD_MANAGER');
    const r = await whyRejected(ethers.getAddress(a.toLowerCase()), to);
    console.log(r.code === 0 ? 'the network would admit a transaction from this key' : `refused (${r.label}): ${r.reason}. ${r.remedy || ''}`); process.exit(r.code === 0 ? 0 : 1);
  }
  if (cmd === 'pay-penalty' && a && b) {
    const { account: target, name } = await resolveAccount(a); account();
    const pm = await contract('PENALTIES_MANAGER', ['function owed(address) view returns (uint256)', 'function payPenalties(address,uint256)']);
    const ox = await contract('PUBLICOS_TOKEN', ['function decimals() view returns (uint8)']); const d = await ox.decimals();
    const before = await pm.owed(target);
    if (before === 0n) { console.log(`${name} owes nothing`); process.exit(3); }
    const { hash, receipt } = await sendTx(await pm.getAddress(), pm.interface.encodeFunctionData('payPenalties', [target, ethers.parseUnits(b, d)]));
    const after = await pm.owed(target);
    console.log(`${hash} block ${receipt.blockNumber} status ${receipt.status} · ${name} owed ${ethers.formatUnits(before, d)}, now ${ethers.formatUnits(after, d)} OX`); process.exit(after < before ? 0 : 1);
  }
  if (!cmd) { console.log('usage: node standing.js <who> | agreement protocol|operator|citizen [--account=<who>] | why <key> [<contract>] | pay-penalty <who> <OX>'); process.exit(2); }

  const { account: acct, name } = await resolveAccount(cmd);
  const am = await contract('ACCOUNT_MEMORY', ['function getIsOrgAccount(address) view returns (bool)', 'function getAccountSuspended(address) view returns (bool)',
    'function getPendingReset(address) view returns (tuple(address newSoleSession, uint64 announcedAt, uint64 landsAt, bool extended))']);
  const ox = await contract('PUBLICOS_TOKEN', ['function decimals() view returns (uint8)', 'function frozen(address) view returns (bool)']); const d = await ox.decimals();
  const isOrg = await am.getIsOrgAccount(acct);
  const o = { account: acct, name, kind: isOrg ? 'org' : 'individual', problems: [] };
  const dm = await contract('DOMAIN_MEMORY', ['function isDomainCompliant(address) view returns (bool)', 'function domainPaidUntil(address) view returns (uint256)']);
  o.domain_paid = await dm.isDomainCompliant(acct); const until = await dm.domainPaidUntil(acct);
  o.domain_paid_until = until >= 32503680000n ? 'never expires' : day(until);
  if (!o.domain_paid) o.problems.push('the domain has lapsed: every transaction but paying the domain is refused');
  else if (until < 32503680000n && Number(until) - Date.now() / 1000 < 14 * 86400) o.problems.push(`the domain lapses on ${o.domain_paid_until}`);
  o.suspended = await soft(() => am.getAccountSuspended(acct), false);
  if (o.suspended) o.problems.push('the account is SUSPENDED: none of its keys can act');
  const sn = await soft(() => contract('SUSPENSION_NOTICE', ['function appliesAt(address) view returns (uint256)']));
  const applies = sn ? await soft(() => sn.appliesAt(acct), 0n) : 0n;
  if (applies && applies > 0n) { o.suspension_lands = day(applies); o.problems.push(`a suspension was announced and lands on ${o.suspension_lands}`); }
  const pmgr = await soft(() => contract('PENALTIES_MANAGER', ['function owed(address) view returns (uint256)', 'function servicesBlocked(address) view returns (bool)']));
  const pmem = await soft(() => contract('PENALTIES_MEMORY', ['function count(address) view returns (uint256)', 'function penalty(address,uint256) view returns (tuple(uint256 amount, uint256 paid, uint256 issuedAt, uint256 payBefore, uint8 status))',
    'function evidence(address,uint256) view returns (string)', 'function blacklisted(address) view returns (bool)']));
  if (pmgr && pmem) {
    o.penalties_owed = ethers.formatUnits(await soft(() => pmgr.owed(acct), 0n), d);
    o.services_blocked = await soft(() => pmgr.servicesBlocked(acct), false);
    o.blacklisted = await soft(() => pmem.blacklisted(acct), false);
    o.penalties = [];
    const n = Number(await soft(() => pmem.count(acct), 0n));
    for (let i = 0; i < n; i++) { const p = await pmem.penalty(acct, i); o.penalties.push({ id: i, amount: ethers.formatUnits(p.amount, d), paid: ethers.formatUnits(p.paid, d), status: PSTATUS[Number(p.status)], pay_before: day(p.payBefore), reason: await soft(() => pmem.evidence(acct, i), '') }); }
    if (Number(o.penalties_owed) > 0) o.problems.push(`owes ${o.penalties_owed} OX in penalties`);
    if (o.services_blocked) o.problems.push('cannot subscribe to providers until its penalties are settled');
    if (o.blacklisted) o.problems.push('blacklisted by the court');
  }
  const safe = await (await contract('SAFE_MANAGER', ['function getMainSafeAddress(address) view returns (address)'])).getMainSafeAddress(acct);
  o.money_frozen = await soft(() => ox.frozen(safe), false);
  if (o.money_frozen) o.problems.push('its OX is FROZEN: it cannot send or receive');
  const reset = await soft(() => am.getPendingReset(acct));
  if (reset && Number(reset.landsAt)) { o.key_reset = { new_key: reset.newSoleSession, lands: day(reset.landsAt) }; o.problems.push(`a KEY RESET was announced: on ${o.key_reset.lands} every key is replaced by ${reset.newSoleSession}. If this was not asked for, the account's own permanent key can object.`); }
  if (!isOrg) {
    const fl = await soft(() => contract('FLAG_REGISTRY_MEMORY', ['function standingOf(address) view returns (tuple(uint256 filed, uint256 overturned, uint64 suspendedUntil))']));
    const st = fl ? await soft(() => fl.standingOf(acct)) : null;
    if (st) { o.flags_filed = Number(st.filed); o.flags_overturned = Number(st.overturned); if (Number(st.suspendedUntil) > Date.now() / 1000) { o.problems.push(`may not file flags until ${day(st.suspendedUntil)}`); } }
    const mem = await soft(() => contract('AGREEMENT_MEMORY', ['function agreedOf(uint8,address) view returns (tuple(uint32 version, uint64 at))']));
    if (mem) { o.agreements = {}; for (const [k, id] of Object.entries(KINDS)) { const x = await soft(() => mem.agreedOf(id, acct)); if (x && Number(x.version)) o.agreements[k] = { version: Number(x.version), at: day(x.at) }; } }
  }
  o.block = await pub.getBlockNumber();
  emit(o, () => {
    console.log(`${name}   ${acct}   ${o.kind}`);
    console.log(o.problems.length ? 'NEEDS ATTENTION:\n' + o.problems.map(p => '  ! ' + p).join('\n') : 'in good standing: nothing owed, nothing pending');
    console.log(`domain paid until ${o.domain_paid_until}`);
    for (const p of o.penalties || []) console.log(`penalty #${p.id}: ${p.amount} OX (${p.paid} paid), ${p.status}, pay before ${p.pay_before}${p.reason ? ' · ' + p.reason.slice(0, 160) : ''}`);
    if (o.agreements) console.log('accepted: ' + (Object.entries(o.agreements).map(([k, v]) => `${k} v${v.version} (${v.at})`).join(' · ') || 'no agreement on record'));
    if (o.flags_filed !== undefined) console.log(`flags filed: ${o.flags_filed}, overturned: ${o.flags_overturned}`);
  });
  process.exit(o.problems.length ? 1 : 0);
})().catch(fail);
