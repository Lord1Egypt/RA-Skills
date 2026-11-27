// The shape of the network (map.md, endpoints.md): is it up, who runs the servers, what things cost, where each
// system contract is. No key needed.
//   node network.js status        chain id, the latest block and its age, how many accounts, the fees
//   node network.js providers     every registered chain provider (BSP) and social server (SSP): slug, name, URL, region, owner
//   node network.js modules       the address of every system contract this guide uses, resolved from the registry
//   node network.js server [<slug or url>]   one social server: is it up, its size limits, its house rules and privacy notice
//   add --json for the full data
const { ethers, pub, RPC, contract, contractAddress, nameOf, getJson, positional, emit, fail } = require('./chain.js');

const MODULES = ['ACCOUNT_MEMORY', 'ACCOUNT_MANAGER', 'RECORD_MANAGER', 'CITIZENSHIP_MANAGER', 'VOUCH_MANAGER', 'ORG_MANAGER', 'ORG_STORAGE',
  'VOTING_MECHANISM', 'PUBLICOS_ROOT_ORG', 'DOMAIN_MANAGER', 'DOMAIN_MEMORY', 'SUBS_MANAGER', 'SUBS_MEMORY', 'BSP_REGISTRY_MEMORY',
  'SOCIAL_SERVER_REGISTRY_MEMORY', 'SAFE_MANAGER', 'SAFE_AUTH', 'PUBLICOS_TOKEN', 'XMTP_MANAGER', 'APP_REGISTRY_MANAGER', 'APP_REGISTRY_MEMORY', 'AGREEMENT_MANAGER'];
const TUPLE = 'tuple(bool exists, string slug, string title, string apiUrl, string region, address owner)';

async function providers() {
  const br = await contract('BSP_REGISTRY_MEMORY', [`function getBSPBySlug(string) view returns (${TUPLE})`, 'function getTotalBSPCount() view returns (uint256)', 'function getBSPSlugs(uint256,uint256) view returns (string[])']);
  const sr = await contract('SOCIAL_SERVER_REGISTRY_MEMORY', [`function getSocialServerBySlug(string) view returns (${TUPLE})`, 'function getTotalSocialServerCount() view returns (uint256)', 'function getSocialServerSlugs(uint256,uint256) view returns (string[])']);
  const row = async (p) => ({ slug: p.slug, title: p.title, url: p.apiUrl, region: p.region, owner: p.owner, owner_name: await nameOf(p.owner) });
  const bsps = [], ssps = [];
  for (const s of await br.getBSPSlugs(0, Number(await br.getTotalBSPCount()))) bsps.push(await row(await br.getBSPBySlug(s)));
  for (const s of await sr.getSocialServerSlugs(0, Number(await sr.getTotalSocialServerCount()))) ssps.push(await row(await sr.getSocialServerBySlug(s)));
  return { bsps, ssps };
}

(async () => {
  const [cmd, x] = positional();
  if (cmd === 'status') {
    const block = await pub.getBlock('latest');
    const am = await contract('ACCOUNT_MEMORY', ['function individualCount() view returns (uint256)', 'function orgCount() view returns (uint256)']);
    const cm = await contract('CITIZENSHIP_MANAGER', ['function citizenCount() view returns (uint256)']);
    const vm = await contract('VOUCH_MANAGER', ['function computeCurrentThreshold() view returns (uint256)']);
    const sm = await contract('SUBS_MEMORY', ['function fee(uint8) view returns (uint256)']);
    const ox = await contract('PUBLICOS_TOKEN', ['function decimals() view returns (uint8)']);
    const d = await ox.decimals();
    const o = { rpc: RPC, chain_id: Number((await pub.getNetwork()).chainId), block: block.number, block_age_seconds: Math.floor(Date.now() / 1000) - block.timestamp,
      individuals: Number(await am.individualCount()), orgs: Number(await am.orgCount()), citizens: Number(await cm.citizenCount()), vouches_to_be_eligible: Number(await vm.computeCurrentThreshold()),
      fee_per_month_ox: { bsp: ethers.formatUnits(await sm.fee(0), d), ssp: ethers.formatUnits(await sm.fee(1), d) } };
    return emit(o, () => console.log(`chain ${o.chain_id} at ${o.rpc}\nblock ${o.block}, ${o.block_age_seconds} s old${o.block_age_seconds > 120 ? '  (STALE: the chain may be stalled)' : ''}\n${o.individuals} individuals (${o.citizens} citizens) · ${o.orgs} orgs · ${o.vouches_to_be_eligible} vouches make someone eligible for citizenship\nfees per month: chain provider ${o.fee_per_month_ox.bsp} OX · social server ${o.fee_per_month_ox.ssp} OX (a citizen's are covered by the network)`));
  }
  if (cmd === 'providers') {
    const p = await providers();
    for (const s of p.ssps) { try { s.healthy = (await getJson(s.url.replace(/\/$/, '') + '/health')).status === 200; } catch { s.healthy = false; } }
    const sm = await contract('SUBS_MEMORY', ['function fee(uint8) view returns (uint256)']);
    const d = await (await contract('PUBLICOS_TOKEN', ['function decimals() view returns (uint8)'])).decimals();
    p.fee_per_month_ox = { bsp: ethers.formatUnits(await sm.fee(0), d), ssp: ethers.formatUnits(await sm.fee(1), d) };
    return emit(p, () => {
      console.log(`every chain provider costs ${p.fee_per_month_ox.bsp} OX a month and every social server ${p.fee_per_month_ox.ssp} OX a month (one fee per kind, the same for all; a citizen's are covered by the network)`);
      console.log('chain providers (BSP): where an account sends its transactions');
      for (const b of p.bsps) console.log(`  ${b.slug.padEnd(14)} ${b.title.padEnd(20)} ${b.region.padEnd(4)} ${b.url}   run by ${b.owner_name || b.owner}`);
      console.log('social servers (SSP): where posts, channels and media live');
      for (const s of p.ssps) console.log(`  ${s.slug.padEnd(14)} ${s.title.padEnd(20)} ${s.region.padEnd(4)} ${s.url}   run by ${s.owner_name || s.owner}${s.healthy ? '' : '   NOT ANSWERING'}`);
    });
  }
  if (cmd === 'modules') {
    const rows = []; for (const m of MODULES) rows.push({ name: m, address: await contractAddress(m) });
    return emit({ modules: rows }, () => rows.forEach(r => console.log(`  ${r.name.padEnd(32)} ${r.address}`)));
  }
  if (cmd === 'server') { // one social server's own facts: is it up, its size limits, its house rules and privacy notice
    let url = x;
    if (!url) url = (await providers()).ssps[0].url;
    else if (!/^https?:\/\//.test(url)) { const p = (await providers()).ssps.find(s => s.slug === url); if (!p) throw new Error(`no social server is registered as "${url}"`); url = p.url; }
    url = url.replace(/\/$/, '');
    const [health, limits, rules] = await Promise.all([getJson(url + '/health'), getJson(url + '/api/limits'), getJson(url + '/privacy_and_agreements')]);
    const o = { url, healthy: health.status === 200, limits: limits.status === 200 ? limits.body : null,
      rules: rules.status === 200 ? { version: rules.body.version, effective_from: rules.body.effective_from, languages: Object.keys(rules.body.rules || {}), rules: rules.body.rules, privacy: rules.body.privacy } : null };
    return emit(o, () => {
      console.log(`${url}   ${o.healthy ? 'answering' : 'NOT ANSWERING'}`);
      if (o.limits) console.log('limits  ' + Object.entries(o.limits).map(([k, v]) => `${k.replace(/^max_/, '')} ${v}`).join(' · '));
      if (o.rules) console.log(`house rules and privacy notice: version ${o.rules.version}, in force since ${o.rules.effective_from}, languages ${o.rules.languages.join(', ')}   (--json prints the text; read it before you post there)`);
      else console.log('this server publishes no house rules');
    });
  }
  console.log('usage: node network.js status | providers | modules | server [<slug or url>]');
  process.exit(2);
})().catch(fail);
