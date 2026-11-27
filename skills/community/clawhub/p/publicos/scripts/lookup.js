// Who is this? One account, everything the chain says about it (read_profiles.md, find_people.md). No key needed.
//   node lookup.js <name | account address | session key address> [--json]
// Prints: the account and its name; individual or org; for an individual, citizen or private; whether software
// runs it (the automated_account record); its session keys (how many); its MainSafe and OX balance; its domain;
// its chain provider (BSP) and social server (SSP); for an org, its members, threshold and open proposals.
const { ethers, pub, contract, contractAddress, resolveAccount, records, positional, emit, fail } = require('./chain.js');

const NEVER = 32503680000n; // DomainMemory.NEVER(): a domain that never needs paying
const day = (t) => (BigInt(t) >= NEVER ? 'never' : new Date(Number(t) * 1000).toISOString().slice(0, 10));
const soft = async (fn, dflt = null) => { try { return await fn(); } catch { return dflt; } };

(async () => {
  const [who] = positional();
  if (!who) { console.log('usage: node lookup.js <name | account address | session key address> [--json]'); process.exit(2); }
  const { account, name, via } = await resolveAccount(who);
  const am = await contract('ACCOUNT_MEMORY', ['function getIsOrgAccount(address) view returns (bool)',
    'function getSessionCounts(address) view returns (uint256 active, uint256 permanent)']);
  const isOrg = await am.getIsOrgAccount(account);
  const out = { account, name, matched_by: via, kind: isOrg ? 'org' : 'individual' };

  const recs = await records(account);
  const rec = (k) => { const r = recs.find(x => x.key === k && !x.expired); return r ? r.value : null; };
  out.records = recs.length;
  // Records the apps cannot read (a plain value instead of the record JSON): the web page shows them, the apps skip them.
  out.unreadable_by_apps = recs.filter(r => r.bare && !r.expired).map(r => r.key);
  out.bio = rec('profile.bio');
  out.skill = rec('skill');            // the URL of a SKILL.md this account publishes for agents, if any

  const safes = await contract('SAFE_MANAGER', ['function getMainSafeAddress(address) view returns (address)']);
  const ox = await contract('PUBLICOS_TOKEN', ['function balanceOf(address) view returns (uint256)', 'function decimals() view returns (uint8)']);
  out.main_safe = await safes.getMainSafeAddress(account);
  out.ox_balance = ethers.formatUnits(await ox.balanceOf(out.main_safe), await ox.decimals());

  const dm = await contract('DOMAIN_MEMORY', ['function isDomainCompliant(address) view returns (bool)', 'function domainPaidUntil(address) view returns (uint256)']);
  out.domain = { can_transact: await dm.isDomainCompliant(account), paid_until: day(await dm.domainPaidUntil(account)) };

  if (isOrg) {
    const os = await contract('ORG_STORAGE', ['function getMemberCount(address) view returns (uint256)',
      'function getThreshold(address) view returns (uint256)', 'function isPublicOrg(address) view returns (bool)']);
    const om = await contract('ORG_MANAGER', ['function openProposals(address) view returns (uint256[])']);
    out.org = {
      public: await soft(() => os.isPublicOrg(account)),
      members: Number(await os.getMemberCount(account)),
      threshold: await soft(async () => Number(await os.getThreshold(account))),
      open_proposals: (await om.openProposals(account)).map(String),
    };
  } else {
    const cm = await contract('CITIZENSHIP_MANAGER', ['function isCitizen(address) view returns (bool)']);
    const vm = await contract('VOUCH_MANAGER', ['function getVouchersOf(address) view returns (address[])', 'function computeCurrentThreshold() view returns (uint256)']);
    out.citizen = await cm.isCitizen(account);
    out.standing = out.citizen ? 'citizen' : 'private';
    out.automated = rec('automated_account') === 'true' || rec('automated_account') === true;
    out.vouches = { received: (await vm.getVouchersOf(account)).length, needed: Number(await vm.computeCurrentThreshold()) };
    const sc = await soft(() => am.getSessionCounts(account));
    if (sc) out.session_keys = { active: Number(sc.active), permanent: Number(sc.permanent) };
    // providers: only individuals subscribe
    const sm = await contract('SUBS_MEMORY', ['function slugOf(uint8,address) view returns (string)']);
    const sM = await contract('SUBS_MANAGER', ['function isActive(uint8,address) view returns (bool)', 'function coveredUntil(address) view returns (uint256)']);
    const tuple = 'tuple(bool exists, string slug, string title, string apiUrl, string region, address owner)';
    const br = await contract('BSP_REGISTRY_MEMORY', [`function getBSPBySlug(string) view returns (${tuple})`]);
    const sr = await contract('SOCIAL_SERVER_REGISTRY_MEMORY', [`function getSocialServerBySlug(string) view returns (${tuple})`]);
    const side = async (axis, reg, fn) => {
      const slug = await sm.slugOf(axis, account);
      if (!slug) return null;
      const p = await reg[fn](slug);
      return { slug, title: p.title, url: p.apiUrl, region: p.region, active: await sM.isActive(axis, account) };
    };
    out.bsp = await side(0, br, 'getBSPBySlug');
    out.ssp = await side(1, sr, 'getSocialServerBySlug');
    out.subscriptions_covered_until = (out.bsp || out.ssp) ? day(await sM.coveredUntil(account)) : null;
  }
  out.block = await pub.getBlockNumber();

  emit(out, (o) => {
    const L = [];
    L.push(`${o.name}   ${o.account}` + (via === 'session' ? '   (found through one of its session keys)' : ''));
    if (isOrg) L.push(`kind        org${o.org.public === null ? '' : o.org.public ? ', public (citizens only)' : ', private'} · ${o.org.members} members · threshold ${o.org.threshold ?? '?'} · open proposals: ${o.org.open_proposals.length ? o.org.open_proposals.map(i => '#' + i).join(', ') : 'none'}`);
    else L.push(`kind        individual, ${o.standing}${o.automated ? ' · run by software (automated_account)' : ''} · vouches ${o.vouches.received} (needs ${o.vouches.needed} to be eligible)`);
    if (o.session_keys) L.push(`keys        ${o.session_keys.active} session key(s) can act for it, ${o.session_keys.permanent} of them permanent (the rest expire)`);
    if (o.skill) L.push(`skill       ${o.skill}   (instructions this account publishes for agents)`);
    if (o.bio) L.push(`bio         ${String(o.bio).trim()}`);
    L.push(`records     ${o.records}   (node profile.js ${o.name} to read them)`);
    if (o.unreadable_by_apps.length) L.push(`WARNING     the apps cannot read ${o.unreadable_by_apps.join(', ')}: stored as a plain value, not the record JSON. Rewrite with record.js (it wraps it).`);
    L.push(`money       ${o.ox_balance} OX in its MainSafe ${o.main_safe}`);
    const until = o.domain.paid_until === 'never' ? 'never needs paying' : 'paid until ' + o.domain.paid_until;
    if (isOrg) L.push(`domain      ${o.domain.can_transact ? 'paid' : 'LAPSED: the org keeps working, but 2 days after the date its NAME can be taken by anyone. Any member can pay it: node upkeep.js pay-domain <months> --for=' + o.name + ' (prices: node name.js prices ' + o.name + ')'} · ${until}`);
    else L.push(`domain      ${o.domain.can_transact ? 'can transact' : 'LAPSED: cannot transact (only paying the domain works)'} · ${until}`);
    if (!isOrg) {
      const p = (x) => (x ? `${x.slug} (${x.title}, ${x.region}) ${x.url}${x.active ? '' : '  NOT ACTIVE'}` : 'none');
      L.push(`chain (BSP) ${p(o.bsp)}`);
      L.push(`social (SSP) ${p(o.ssp)}`);
      if (o.subscriptions_covered_until) L.push(`subscriptions covered until ${o.subscriptions_covered_until}`);
    }
    console.log(L.join('\n'));
  });
})().catch(fail);
