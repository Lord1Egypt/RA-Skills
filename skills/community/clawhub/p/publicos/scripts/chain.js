// Chain helpers the other scripts share (act_basics.md §1): resolve contracts from the registry,
// find the account's BSP, simulate, ask the node why a transaction would be refused, send.
// Node 18+, ethers v6. PUBLICOS_KEY = your session key, PUBLICOS_ACCOUNT = the account it signs for.
const { ethers } = require('ethers');

const CHAIN_ID = 4489;
const RPC = process.env.PUBLICOS_RPC || 'https://rpc.publicos.dev';
const REGISTRY = process.env.PUBLICOS_REGISTRY || '0xF69a649A5541d2d0108E00f697647fF1dD4Bd4bD'; // the ModuleRegistry (endpoints.md)
const UA = process.env.PUBLICOS_UA || 'PublicOS-Agent/1.0 (+https://publicos.dev/agents)';

function providerFor(url) {
  const req = new ethers.FetchRequest(url); req.setHeader('User-Agent', UA);
  // Past its rate limit the edge answers 503 with an HTML body: wait (0.5 s, 1 s, 2 s, 4 s) and ask again (etiquette.md).
  req.retryFunc = async (_req, resp, attempt) => {
    if ((resp.statusCode === 503 || resp.statusCode === 429) && attempt < 4) { await new Promise(r => setTimeout(r, 500 * 2 ** attempt)); return true; }
    return false;
  };
  return new ethers.JsonRpcProvider(req, CHAIN_ID, { staticNetwork: true });
}
const pub = providerFor(RPC);
const registry = new ethers.Contract(REGISTRY, ['function getModuleAddress(bytes32) view returns (address)'], pub);
const _mods = {};
/** Address of a module by its registry name, e.g. 'RECORD_MANAGER'. */
async function contractAddress(name) {
  if (!_mods[name]) {
    const a = await registry.getModuleAddress(ethers.id(name));
    if (a === ethers.ZeroAddress) throw new Error(`module ${name} not in the registry`);
    _mods[name] = a;
  }
  return _mods[name];
}

function key(provider = pub) {
  const pk = process.env.PUBLICOS_KEY;
  if (!pk) throw new Error('set PUBLICOS_KEY to your session key');
  return new ethers.Wallet(pk, provider);
}
function account() {
  // the account you act for: --account=0x… on the command line, or the PUBLICOS_ACCOUNT environment variable
  const fromFlag = (process.argv.find(x => x.startsWith('--account=')) || '').slice('--account='.length);
  const a = fromFlag || process.env.PUBLICOS_ACCOUNT;
  if (!a) throw new Error('say which account you act for: --account=0x… or the PUBLICOS_ACCOUNT environment variable');
  if (!/^0x[0-9a-fA-F]{40}$/.test(a)) throw new Error(`the account must be given as its address (0x…), not "${a}". Find it with: node lookup.js ${a}`);
  return ethers.getAddress(a.toLowerCase());
}

/** The RPC of the BSP this account subscribes to (its own chain provider); the public RPC when it has none. */
async function bspRpc(acct) {
  const subs = new ethers.Contract(await contractAddress('SUBS_MEMORY'), ['function slugOf(uint8,address) view returns (string)'], pub);
  const slug = await subs.slugOf(0, acct);
  if (!slug) return RPC;
  const reg = new ethers.Contract(await contractAddress('BSP_REGISTRY_MEMORY'),
    ['function getBSPBySlug(string) view returns (tuple(bool exists, string slug, string title, string apiUrl, string region, address owner))'], pub);
  const bsp = await reg.getBSPBySlug(slug);
  return bsp.exists && bsp.apiUrl ? bsp.apiUrl : RPC;
}

/** The social server (SSP) an account subscribes to, from the chain: SUBS_MEMORY.slugOf(1, account), then the
 *  SSP registry. `PUBLICOS_SSP` overrides it. Throws when the account has no SSP: there is nowhere to read or write. */
async function sspUrl(acct) {
  if (process.env.PUBLICOS_SSP) return process.env.PUBLICOS_SSP.replace(/\/$/, '');
  const subs = new ethers.Contract(await contractAddress('SUBS_MEMORY'), ['function slugOf(uint8,address) view returns (string)'], pub);
  const slug = await subs.slugOf(1, ethers.getAddress(acct));
  if (!slug) throw new Error(`${acct} has no social server (SSP) subscription`);
  const reg = new ethers.Contract(await contractAddress('SOCIAL_SERVER_REGISTRY_MEMORY'),
    ['function getSocialServerBySlug(string) view returns (tuple(bool exists, string slug, string title, string apiUrl, string region, address owner))'], pub);
  const ssp = await reg.getSocialServerBySlug(slug);
  if (!ssp.exists || !ssp.apiUrl) throw new Error(`social server "${slug}" is not in the registry`);
  return ssp.apiUrl.replace(/\/$/, '');
}

/** Ask the node, before sending, whether it would refuse a transaction from this key to this contract. */
async function whyRejected(from, to) {
  const r = await pub.send('publicos_whyTxRejected', [{ from, to }]);
  return r; // {code, label, reason, remedy}; code 0 = fine
}

// The contracts' custom errors, so a refusal reads as words instead of "unknown custom error".
// The ones an account meets in normal use carry a plain explanation.
const CUSTOM_ERRORS = new ethers.Interface([
  'error Gov_AlreadyVoted(uint256 id, address voter)', 'error Gov_BadCooldown()', 'error Gov_BadDuration()', 'error Gov_BadMaxOpen()',
  'error Gov_BadQuorum()', 'error Gov_BadReason()', 'error Gov_NotClosable(uint256 id)', 'error Gov_NotOpen(uint256 id)',
  'error Gov_ProposerHasOpenVote(address proposer, address org)', 'error Gov_ProposerInCooldown(address proposer, address org, uint256 until)',
  'error Gov_TooManyOpenVotes(address org, uint256 maxOpen)', 'error Gov_UnknownProposal(uint256 id)', 'error Gov_ZeroWeight(address voter, address org)',
  'error VW_AlreadyMember(address account, address org)', 'error VW_DelegateeNotMember(address delegatee, address org)',
  'error VW_NotMember(address account, address org)', 'error VW_TooManyTagDelegations(address delegator, address org)',
  'error AdminCapReached()', 'error AlreadyAdmin()', 'error AlreadyResolved()', 'error AlreadyVoted()', 'error ElectorateTooSmall()',
  'error EmptyInitialSet()', 'error InvalidAddress()', 'error InvalidAdmin()', 'error InvalidProposal()', 'error NoSuchPlan()', 'error NotAdmin()',
  'error NotAuthorized()', 'error NotCitizen()', 'error PayoutUnreachable()', 'error PlanClosed()', 'error TokenNotAccepted()',
  'error TooManyActiveProposals()', 'error VotingClosed()', 'error VotingOpen()', 'error ZeroAddress()',
]);
const PLAIN = {
  Gov_ProposerHasOpenVote: 'you already have a proposal in this org that is still waiting for votes; an org takes one waiting proposal per member. Wait until it passes or fails, or ask another member to propose this',
  Gov_TooManyOpenVotes: (a) => `this org already has ${a.maxOpen} proposals open, its limit; wait for one to end`,
  Gov_AlreadyVoted: (a) => `you already voted on proposal ${a.id}`,
  Gov_NotOpen: (a) => `proposal ${a.id} is not open any more`,
  Gov_UnknownProposal: (a) => `there is no proposal ${a.id}`,
  Gov_ZeroWeight: 'you had no vote weight when this proposal started (you joined after it opened)',
  Gov_ProposerInCooldown: (a) => `you withdrew a proposal here and must wait until ${new Date(Number(a.until) * 1000).toISOString().slice(0, 16)} UTC to propose again`,
  VW_AlreadyMember: 'that account is already a member',
  VW_NotMember: 'that account is not a member of this org',
};
/** Turn a revert into words: the reason string, or a known custom error by name (and in plain words when it has one). */
function explainRevert(e) {
  const data = e && (e.data || (e.info && e.info.error && e.info.error.data) || (e.error && e.error.data));
  if (typeof data === 'string' && data.length >= 10) {
    try {
      const d = CUSTOM_ERRORS.parseError(data);
      if (d && (d.name === 'Error' || d.name === 'Panic')) return null;   // a plain reason string: ethers already prints it
      if (d) { const p = PLAIN[d.name]; const args = Object.fromEntries(d.fragment.inputs.map((x, i) => [x.name, d.args[i]]));
        return `refused (${d.name}): ${p ? (typeof p === 'function' ? p(args) : p) : 'see the contract for this error'}`; }
    } catch {}
  }
  return null;
}
async function simulate(tx) {
  try { await pub.call(tx); } catch (e) { const w = explainRevert(e); if (w) throw new Error(w); throw e; }
  try { return await pub.estimateGas(tx); } catch (e) { const w = explainRevert(e); if (w) throw new Error(w); throw e; }
}
/** The gas to send with: the node's estimate plus 30 %, never under 300k, never over 30M. */
const gasFor = (est) => { let g = est * 13n / 10n; if (g < 300_000n) g = 300_000n; if (g > 30_000_000n) g = 30_000_000n; return g; };

// ---- records, written to the records standard (publicos.dev Library "Records") --------------------
/** The key of a channel tab: channel.<slug>; a slug over 23 is cut to 14 + 8 hex of its SHA-256 (a key is at most 31). */
function channelTabKey(slug) {
  const k = `channel.${slug}`;
  if (k.length <= 31) return k;
  return `channel.${slug.slice(0, 14)}-${require('crypto').createHash('sha256').update(slug).digest('hex').slice(0, 8)}`;
}
/** A channel tab record (router, type 2, subtype "channel"): {key, value, type, customType}, the value being the record JSON. */
function channelTabRecord(server, owner, slug, label) {
  const key = channelTabKey(slug);
  const url = `${server}/api/${ethers.getAddress(owner.toLowerCase())}/channels/${slug}/json`;
  return { key, url, type: 2, customType: 'channel',
    value: JSON.stringify({ key, value: url, type: 2, metadata: { name: label || slug, order: 0 }, noTitle: false, subtype: 'channel' }) };
}
/** The record JSON for any plain value (records standard § 1): a bare value is invisible to the apps. */
function recordEnvelope(key, value, type = 0, subtype = '') {
  try { const o = JSON.parse(value); if (o && typeof o === 'object' && !Array.isArray(o) && o.key === key && typeof o.value === 'string') return value; } catch {}
  const r = { key, value: String(value), type, metadata: {}, noTitle: false };
  if (subtype) r.subtype = subtype;
  return JSON.stringify(r);
}

/** Simulate, check the admission rules, then send a legacy zero-gas transaction through the account's BSP. */
async function sendTx(to, data, { value = 0n, gasLimit } = {}) {
  const acct = account();
  if (process.argv.includes('--dry') || process.env.PUBLICOS_DRY) {
    // A dry run sends nothing: the call is simulated as one of the account's session keys, and the node is asked
    // whether it would admit the transaction. It needs no key (the first active session key stands in).
    let from = process.env.PUBLICOS_KEY ? key().address : null;
    if (!from) {
      const am = new ethers.Contract(await contractAddress('ACCOUNT_MEMORY'), ['function getAccountSessions(address) view returns (address[])'], pub);
      from = (await am.getAccountSessions(acct))[0];
      if (!from) throw new Error(`${acct} has no active session key to simulate as`);
    }
    const est = await simulate({ from, to, data, value });              // a revert here carries the reason
    const why = await whyRejected(from, to);
    if (why && why.code !== 0) throw new Error(`refused: ${why.label}: ${why.reason}. ${why.remedy || ''}`);
    console.log(`dry run: the chain would accept this from ${from} (about ${est} gas; nothing was sent)`);
    process.exit(0);
  }
  const signer = key();
  const est = await simulate({ from: signer.address, to, data, value }); // a revert here carries the reason
  const why = await whyRejected(signer.address, to);
  if (why && why.code !== 0) throw new Error(`refused: ${why.label}: ${why.reason}. ${why.remedy || ''}`);
  const rpc = await bspRpc(acct);
  const w = key(providerFor(rpc));
  const tx = await w.sendTransaction({ to, data, value, type: 0, gasPrice: 0n, gasLimit: gasLimit || gasFor(est), chainId: CHAIN_ID });
  let receipt;
  try { receipt = await tx.wait(); } catch (e) {
    const r = e.receipt;
    if (r && r.gasUsed * 100n >= r.gasLimit * 98n) throw new Error(`the transaction ${tx.hash} ran out of gas (${r.gasUsed} of ${r.gasLimit}) and changed nothing; try again, or tell the operator`);
    throw new Error(`the transaction ${tx.hash} reverted on chain and changed nothing (it passed the simulation, so something changed in between; check and retry once)`);
  }
  return { hash: tx.hash, receipt, rpc };
}

// ---- read helpers (no key needed) -------------------------------------------------------------------

/** A contract by its registry name, e.g. contract('ACCOUNT_MEMORY', ['function getDisplayName(address) view returns (string)']). */
async function contract(name, abi) { return new ethers.Contract(await contractAddress(name), abi, pub); }

const ACCOUNT_ABI = [
  'function getAccountAddressByDisplayName(string) view returns (address)',
  'function getDisplayName(address) view returns (string)',
  'function getIsOrgAccount(address) view returns (bool)',
  'function getSessionAccount(address) view returns (address)',
];

/** The current name of an account ('' when the address is not an account). */
async function nameOf(address) {
  try { return await (await contract('ACCOUNT_MEMORY', ACCOUNT_ABI)).getDisplayName(address); } catch { return ''; }
}

/** Turn what a person typed into an account: a name, an account address, or a session key's address.
 *  Returns { account, name, via } where via is 'name' | 'account' | 'session'. Throws when nothing matches. */
async function resolveAccount(input) {
  if (!input) throw new Error('give a name or an address');
  const am = await contract('ACCOUNT_MEMORY', ACCOUNT_ABI);
  if (!/^0x[0-9a-fA-F]{40}$/.test(input)) {
    const a = await am.getAccountAddressByDisplayName(input);
    if (a === ethers.ZeroAddress) throw new Error(`no account is named "${input}" (names are exact, case-insensitive)`);
    return { account: a, name: await nameOf(a), via: 'name' };
  }
  const a = ethers.getAddress(input.toLowerCase());
  const name = await nameOf(a);
  if (name) return { account: a, name, via: 'account' };
  let owner = ethers.ZeroAddress;
  try { owner = await am.getSessionAccount(a); } catch {}
  if (owner !== ethers.ZeroAddress) return { account: owner, name: await nameOf(owner), via: 'session' };
  throw new Error(`${a} is not an account and not a session key of one`);
}

/** Every record of an account, decoded. Each row: { key, value, type, customType, expiration, expired, record }
 *  where `record` is the parsed JSON the chain stores (its inner `value` and `metadata` are what people see)
 *  and `value` is that inner value (or the raw string when the stored value is not JSON). */
async function records(account) {
  const bp = new ethers.Contract(account, [
    'function getRecordCount() view returns (uint256)',
    'function getAllRecords(uint256,uint256) view returns (string[], string[], uint256[], uint8[], string[], bool[])',
  ], pub);
  const total = Number(await bp.getRecordCount());
  const out = [];
  for (let off = 0; off < total; off += 50) {
    const [keys, values, exps, types, customs, expired] = await bp.getAllRecords(off, 50);
    keys.forEach((k, i) => {
      let record = null; try { record = JSON.parse(values[i]); } catch {}
      const wrapped = !!(record && typeof record === 'object' && 'value' in record);
      const inner = wrapped ? record.value : values[i];
      // bare: stored as a plain value, not the {key,value,type} JSON the apps read. The apps skip such a record.
      out.push({ key: k, value: inner, type: Number(types[i]), customType: customs[i], expiration: Number(exps[i]), expired: expired[i],
        metadata: (record && record.metadata) || {}, record, bare: !wrapped });
    });
  }
  return out;
}

/** eth_getLogs over a block range, walked in windows the RPC accepts (10,000 blocks). */
async function logs(address, topics, fromBlock = 0, toBlock) {
  const head = toBlock ?? await pub.getBlockNumber();
  const windows = [];
  for (let from = fromBlock; from <= head; from += 10000) windows.push([from, Math.min(from + 9999, head)]);
  const parts = new Array(windows.length); let next = 0;
  const worker = async () => { while (next < windows.length) { const i = next++; const [f, t] = windows[i];
    parts[i] = await pub.send('eth_getLogs', [{ address, topics, fromBlock: ethers.toQuantity(f), toBlock: ethers.toQuantity(t) }]); } };
  await Promise.all(Array.from({ length: 6 }, worker));            // six windows at a time: polite, and about 6x faster
  return { logs: parts.flat(), head };
}

/** A plain GET of JSON with our User-Agent. Returns { status, body, headers }. */
async function getJson(url, headers = {}) {
  const r = await fetch(url, { headers: { 'user-agent': UA, accept: 'application/json', ...headers } });
  const text = await r.text(); let body = text; try { body = JSON.parse(text); } catch {}
  return { status: r.status, body, headers: r.headers };
}

// ---- command-line helpers the scripts share --------------------------------------------------------
const argv = process.argv.slice(2);
const positional = () => argv.filter(x => !x.startsWith('--'));
const arg = (name, dflt) => { const a = argv.find(x => x.startsWith(`--${name}=`)); return a ? a.slice(name.length + 3) : dflt; };
const flag = (name) => argv.includes(`--${name}`);
/** Print an object as JSON (with --json) or hand it to a plain-text printer. */
function emit(obj, text) {
  if (flag('json')) console.log(JSON.stringify(obj, (_, v) => (typeof v === 'bigint' ? v.toString() : v), 2));
  else text(obj);
}
const fail = (e) => { if (process.env.PUBLICOS_DEBUG) console.error(e); console.error("ERR", e.shortMessage || e.message || String(e)); process.exit(1); };

module.exports = { ethers, CHAIN_ID, RPC, UA, pub, providerFor, contractAddress, key, account, bspRpc, sspUrl, whyRejected, sendTx,
  contract, nameOf, resolveAccount, records, logs, getJson, positional, arg, flag, emit, fail, channelTabKey, channelTabRecord, recordEnvelope };
