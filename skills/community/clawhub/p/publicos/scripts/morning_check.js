// The morning check: can this account still act today? Four chain reads, no key needed
// (subscriptions_and_domain.md, "Your morning check"). Node 18+, ethers v6.
//   node morning_check.js <account>
// Exit code 0 when everything is fine, 1 when something needs attention (so a cron can alert).
const { ethers } = require('ethers');

const RPC = process.env.PUBLICOS_RPC || 'https://rpc.publicos.dev';
const REGISTRY = process.env.PUBLICOS_REGISTRY || '0xF69a649A5541d2d0108E00f697647fF1dD4Bd4bD'; // the ModuleRegistry (endpoints.md)
const UA = process.env.PUBLICOS_UA || 'PublicOS-Agent/1.0 (+https://publicos.dev/agents)';
const NEVER = 32503680000n; // DomainMemory.NEVER(): a domain that is free for good

(async () => {
  const account = process.argv[2];
  if (!account) { console.log('usage: node morning_check.js <account address>'); process.exit(2); }
  const req = new ethers.FetchRequest(RPC); req.setHeader('User-Agent', UA);
  const provider = new ethers.JsonRpcProvider(req, undefined, { staticNetwork: true });
  const registry = new ethers.Contract(REGISTRY, ['function getModuleAddress(bytes32) view returns (address)'], provider);
  const domain = new ethers.Contract(await registry.getModuleAddress(ethers.id('DOMAIN_MEMORY')),
    ['function isDomainCompliant(address) view returns (bool)', 'function domainPaidUntil(address) view returns (uint256)'], provider);
  const subs = new ethers.Contract(await registry.getModuleAddress(ethers.id('SUBS_MANAGER')),
    ['function isActive(uint8,address) view returns (bool)', 'function coveredUntil(address) view returns (uint256)'], provider);

  const [compliant, paidUntil, bsp, ssp, covered] = await Promise.all([
    domain.isDomainCompliant(account), domain.domainPaidUntil(account),
    subs.isActive(0, account), subs.isActive(1, account), subs.coveredUntil(account),
  ]);
  const day = (t) => (t >= NEVER ? 'never expires' : new Date(Number(t) * 1000).toISOString().slice(0, 10));
  const daysLeft = (t) => (t >= NEVER ? Infinity : Math.floor((Number(t) - Date.now() / 1000) / 86400));

  const lines = [
    `domain     ${compliant ? 'OK ' : 'LAPSED'}  paid until ${day(paidUntil)}`,
    `BSP        ${bsp ? 'active' : 'INACTIVE'}`,
    `SSP        ${ssp ? 'active' : 'INACTIVE'}`,
    `deposit    covers fees until ${day(covered)}${daysLeft(covered) < 14 ? '  (top up soon)' : ''}`,
  ];
  console.log(lines.join('\n'));
  const attention = !compliant || !bsp || !ssp || daysLeft(covered) < 14 || daysLeft(paidUntil) < 14;
  process.exit(attention ? 1 : 0);
})().catch(e => { console.error('ERR', e.shortMessage || e.message); process.exit(1); });
