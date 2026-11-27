// Orgs (org_votes.md): an org has no key, it acts only when its members vote. See the orgs an account is in, read a
// proposal in plain words, vote, propose, run a passed vote, delegate, leave, create one.
//   node org.js mine [<name | address>]            the orgs an account belongs to (default: PUBLICOS_ACCOUNT)
//   node org.js show <org>                         members, how votes work there, its money, what is open
//   node org.js proposal <id>                      one proposal: what it would do, who asked, the tally, the deadline
//   node org.js vote <id> for|against|abstain [--dry]
//   node org.js run <id> [--dry]                   run a vote that passed, in an org that waits for the voting period
//   node org.js propose <org> pay <who> <amount in OX> [--dry]       pay OX from the org's MainSafe
//   node org.js propose <org> add-member <who> | remove-member <who> [--dry]
//   node org.js propose <org> publish-channel <owner>/<slug> ["<label>"]   show a member's channel on the org's profile
//   node org.js propose <org> set-record <key> '<value>' [--type=0] [--custom=] | delete-record <key> [--dry]
//   node org.js delegate <org> <who> [--dry]       hand your vote to another member (yourself = take it back)
//   node org.js leave <org> [--dry]
//   node org.js create "<name>" --members=<who>,<who> [--threshold=1] [--public] [--dry]
// Voting for a person is their decision: show them the proposal and cast exactly what they choose.
// In an org that runs proposals at once, the vote that passes a proposal also runs it.
const { ethers, pub, contract, contractAddress, resolveAccount, nameOf, account, sendTx, positional, arg, flag, emit, fail, sspUrl, channelTabRecord, recordEnvelope } = require('./chain.js');

const ACTIONS = 'SET_RECORD,DELETE_RECORD,ADD_MEMBER,REMOVE_MEMBER,SET_THRESHOLD,EXECUTE_SAFE_TX,REGISTER_INBOX_ID,REMOVE_INBOX_ID,UPDATE_INBOX_ID_LABEL,REGISTER_ADDITIONAL_WALLET,REMOVE_WALLET,ADD_SAFE_MODULE,REMOVE_SAFE_MODULE,ADD_SAFE_OWNER,REMOVE_SAFE_OWNER,CHANGE_SAFE_THRESHOLD,REGISTER_APP,REMOVE_APP,UPDATE_APP_DISPLAY_NAME,SET_APP_POINTER,REMOVE_APP_POINTER,REGISTER_BSP,REMOVE_BSP,UPDATE_BSP_TITLE,SET_BSP_POINTER,REMOVE_BSP_POINTER,REGISTER_SOCIAL_SERVER,REMOVE_SOCIAL_SERVER,UPDATE_SOCIAL_SERVER_TITLE,SET_SOCIAL_SERVER_POINTER,REMOVE_SOCIAL_SERVER_POINTER,REQUEST_PARENT,CANCEL_PARENT_REQUEST,ACCEPT_CHILD,RELEASE_CHILD,EXECUTE_ON_DESCENDANT_SAFE,EXECUTE_ON_DESCENDANT,REMOVE_ALL_VOUCHES,SUSPEND_ACCOUNT,UNSUSPEND_ACCOUNT,DAO_RECOVERY_FULL_RESET,SET_GRANTING_PAUSED,SET_ACCOUNT_CREATION_PAUSED,CREATE_ORG_SUBDOMAIN,RENAME_ORG_SUBDOMAIN,DELETE_ORG_SUBDOMAIN,EXECUTE_ON_OWN_SUB_SAFE,SET_MULTIPLE_RECORDS,PAY_DOMAIN,CHANGE_NAME,SET_QUORUM_BPS,SET_VOTE_DURATION,SET_MAX_OPEN_VOTES,SET_WAIT_FULL_PERIOD,PAY_PENALTIES,SET_CHILD_LOCK,SET_PROPOSER_CAP'.split(',');
const STATUS = ['none', 'open', 'executed', 'failed', 'cancelled'];
const PARAMS = 'tuple(address targetAddress, uint256 valueParam, string keyParam, string valueStringParam, uint8 recordTypeValueParam, string customTypeParam, bytes dataParam, uint8 operationParam)';
const VIEW = `tuple(uint256 id, address org, uint8 status, bool waitFullPeriod, uint256 snapshotBlock, uint256 expirationTimestamp, address initiator, uint8 actionType, bytes32 tag, uint256 snapshotTotal, uint256 quorumBps, uint256 requiredQuorum, uint256 forVotes, uint256 againstVotes, uint256 abstainVotes, bool passed, bool executable, bool closable, ${PARAMS} params)`;
const OM = new ethers.Interface([`function startVote(address,uint8,${PARAMS},bytes32) returns (uint256)`, 'function castVote(uint256,uint8)', 'function execute(uint256)',
  'function delegate(address,bytes32,address)', 'function leaveOrg(address)']);
const ZERO32 = ethers.ZeroHash;
const empty = (o = {}) => ({ targetAddress: ethers.ZeroAddress, valueParam: 0n, keyParam: '', valueStringParam: '', recordTypeValueParam: 0, customTypeParam: '', dataParam: '0x', operationParam: 0, ...o });
const send = async (label, to, data) => { const { hash, receipt } = await sendTx(to, data); console.log(`${label}: ${hash} block ${receipt.blockNumber} status ${receipt.status}`); return receipt; };

async function engine() { return contract('VOTING_MECHANISM', [`function getProposal(uint256) view returns (${VIEW})`, 'function hasVoted(uint256,address) view returns (bool)', 'function openProposals(address) view returns (uint256[])',
  'function orgQuorumBps(address) view returns (uint256)', 'function orgVoteDuration(address) view returns (uint256)', 'function orgMaxOpen(address) view returns (uint256)', 'function orgWaitFullPeriod(address) view returns (bool)', 'function orgProposerCap(address) view returns (bool)']); }
async function storage() { return contract('ORG_STORAGE', ['function getOrgsForAccount(address) view returns (address[])', 'function getMemberCount(address) view returns (uint256)',
  'function getMembers(address,uint256,uint256) view returns (address[])', 'function getThreshold(address) view returns (uint256)', 'function isPublicOrg(address) view returns (bool)', 'function isMember(address,address) view returns (bool)']); }

async function plainWords(p, d) { // what a proposal would do, for a person
  const a = ACTIONS[Number(p.actionType)] || `action ${p.actionType}`; const x = p.params; const who = async (addr) => (await nameOf(addr)) || addr;
  if (a === 'SET_RECORD') {
    let r = null; try { r = JSON.parse(x.valueStringParam); } catch {}
    if (r && r.subtype === 'channel' && Number(r.type) === 2) return `show a channel on the org's profile: tab "${(r.metadata || {}).name || x.keyParam}" -> ${r.value}`;
    if (r && typeof r === 'object' && 'value' in r) return `write the record "${x.keyParam}" on the org's profile: ${r.value}`;
    return `write the record "${x.keyParam}" on the org's profile as a BARE value, which the apps will not show: ${x.valueStringParam}`;
  }
  if (a === 'DELETE_RECORD') return `delete the record "${x.keyParam}" from the org's profile`;
  if (a === 'ADD_MEMBER') return `add ${await who(x.targetAddress)} as a member`;
  if (a === 'REMOVE_MEMBER') return `remove ${await who(x.targetAddress)} from the members`;
  if (a === 'SET_THRESHOLD') return `set the org's threshold to ${x.valueParam}`;
  if (a === 'SET_QUORUM_BPS') return `set the quorum to ${Number(x.valueParam) / 100}% of the members' voting weight`;
  if (a === 'SET_VOTE_DURATION') return `make a vote last ${Number(x.valueParam) / 3600} h`;
  if (a === 'SET_MAX_OPEN_VOTES') return `allow up to ${x.valueParam} open votes at once`;
  if (a === 'SET_WAIT_FULL_PERIOD') return Number(x.valueParam) ? 'make a passed vote wait for the end of its period' : 'make a vote run the moment it passes';
  if (a === 'SET_PROPOSER_CAP') return Number(x.valueParam) ? 'allow each member only one proposal waiting for votes' : 'let members have several proposals waiting at once';
  if (a === 'EXECUTE_SAFE_TX') {
    const token = await contractAddress('PUBLICOS_TOKEN');
    if (x.targetAddress === token && x.dataParam.startsWith('0xa9059cbb')) {
      const [toSafe, amount] = ethers.AbiCoder.defaultAbiCoder().decode(['address', 'uint256'], '0x' + x.dataParam.slice(10));
      const sm = await contract('SAFE_MANAGER', ['function getSafeOwnerAccount(address) view returns (address)']);
      let owner = ethers.ZeroAddress; try { owner = await sm.getSafeOwnerAccount(toSafe); } catch {}
      return `pay ${ethers.formatUnits(amount, d)} OX from the org's MainSafe to ${owner !== ethers.ZeroAddress ? await who(owner) : toSafe + ' (NOT a MainSafe of any account)'}`;
    }
    return `make the org's MainSafe call ${x.targetAddress} (value ${x.valueParam}, data ${x.dataParam.slice(0, 74)}…): read this one carefully`;
  }
  if (a === 'REGISTER_INBOX_ID') return `publish a messaging inbox for the org, labelled "${x.keyParam}"`;
  return `${a.toLowerCase().replace(/_/g, ' ')}${x.targetAddress !== ethers.ZeroAddress ? ' · target ' + await who(x.targetAddress) : ''}${x.keyParam ? ' · ' + x.keyParam : ''}${x.valueStringParam ? ' · ' + x.valueStringParam.slice(0, 120) : ''}${x.valueParam ? ' · ' + x.valueParam : ''}`;
}
async function proposalView(id) {
  const g = await engine(); let p;
  try { p = await g.getProposal(id); } catch { throw new Error(`there is no proposal ${id} (open ones: node org.js show <org>)`); }
  if (Number(p.status) === 0) throw new Error(`there is no proposal ${id}`);
  const ox = await contract('PUBLICOS_TOKEN', ['function decimals() view returns (uint8)']);
  const me = process.env.PUBLICOS_ACCOUNT;
  return { id: String(p.id), org: p.org, org_name: await nameOf(p.org), status: STATUS[Number(p.status)], action: ACTIONS[Number(p.actionType)] || String(p.actionType),
    does: await plainWords(p, await ox.decimals()), asked_by: (await nameOf(p.initiator)) || p.initiator, closes: new Date(Number(p.expirationTimestamp) * 1000).toISOString().slice(0, 16).replace('T', ' ') + ' UTC',
    votes: { for: String(p.forVotes), against: String(p.againstVotes), abstain: String(p.abstainVotes), needed: String(p.requiredQuorum), of: String(p.snapshotTotal) },
    passed: p.passed, can_run_now: p.executable, waits_for_the_period: p.waitFullPeriod, you_voted: me ? await g.hasVoted(id, me) : undefined };
}
const printProposal = (v) => console.log(`#${v.id} in ${v.org_name} · ${v.status}${v.passed ? ' · PASSED' : ''}\n  would: ${v.does}\n  asked by ${v.asked_by} · closes ${v.closes}\n  votes: ${v.votes.for} for · ${v.votes.against} against · ${v.votes.abstain} abstain · needs ${v.votes.needed} of ${v.votes.of}` +
  (v.you_voted !== undefined ? `\n  you ${v.you_voted ? 'already voted' : 'have not voted'}` : '') + (v.can_run_now ? `\n  it can be run now: node org.js run ${v.id}` : ''));

(async () => {
  let [cmd, a, b, c, d] = positional();
  // Forms agents try first (the ten, 2026-11-16): `proposals <org>` = show; `proposal <org> <id>` and
  // `vote <org> <id> for` name the org first. Proposal ids are global, so the org is simply dropped.
  if (cmd === 'proposals') cmd = 'show';
  if ((cmd === 'proposal' || cmd === 'vote') && a && b && !/^#?\d+$/.test(a) && /^#?\d+$/.test(b)) [a, b, c] = [b, c, d];
  if ((cmd === 'proposal' || cmd === 'vote' || cmd === 'run') && a) a = String(a).replace(/^#/, '');
  const os = await storage();
  if (cmd === 'mine') {
    const { account: acct, name } = await resolveAccount(a || process.env.PUBLICOS_ACCOUNT);
    const g = await engine(); const rows = [];
    for (const o of await os.getOrgsForAccount(acct)) rows.push({ org: o, name: await nameOf(o), public: await os.isPublicOrg(o), members: Number(await os.getMemberCount(o)), open_proposals: (await g.openProposals(o)).map(String) });
    return emit({ account: acct, name, orgs: rows }, () => { console.log(`${name} is a member of ${rows.length} org(s)`); for (const r of rows) console.log(`  ${(r.name || '?').padEnd(22)} ${r.org}  ${r.public ? 'public' : 'private'} · ${r.members} members · open proposals: ${r.open_proposals.join(', ') || 'none'}`); });
  }
  if (cmd === 'show' && a) {
    const { account: org, name } = await resolveAccount(a); const g = await engine();
    const total = Number(await os.getMemberCount(org)); const members = []; for (let off = 0; off < total; off += 50) for (const m of await os.getMembers(org, off, 50)) members.push({ account: m, name: await nameOf(m) });
    const safe = await (await contract('SAFE_MANAGER', ['function getMainSafeAddress(address) view returns (address)'])).getMainSafeAddress(org);
    const ox = await contract('PUBLICOS_TOKEN', ['function balanceOf(address) view returns (uint256)', 'function decimals() view returns (uint8)']);
    const o = { org, name, public: await os.isPublicOrg(org), threshold: Number(await os.getThreshold(org)), quorum_percent: Number(await g.orgQuorumBps(org)) / 100, vote_lasts_hours: Number(await g.orgVoteDuration(org)) / 3600,
      max_open_votes: Number(await g.orgMaxOpen(org)), waits_for_the_period: await g.orgWaitFullPeriod(org), one_proposal_per_member: await g.orgProposerCap(org), main_safe: safe, ox: ethers.formatUnits(await ox.balanceOf(safe), await ox.decimals()),
      open_proposals: (await g.openProposals(org)).map(String), members };
    return emit(o, () => { console.log(`${name}   ${org}   ${o.public ? 'public org (citizens only)' : 'private org'}`);
      console.log(`votes: quorum ${o.quorum_percent}% · a vote lasts ${o.vote_lasts_hours} h · ${o.waits_for_the_period ? 'a passed vote waits for the period, then anyone runs it' : 'a vote runs the moment it passes'} · up to ${o.max_open_votes} open at once · ${o.one_proposal_per_member ? 'one waiting proposal per member' : 'members may have several proposals waiting'}`);
      console.log(`  change them by vote: org.js propose <org> set quorum|vote-hours|max-open|wait|one-per-member <value>`);
      console.log(`money: ${o.ox} OX in ${safe}`); console.log(`open proposals: ${o.open_proposals.map(i => '#' + i).join(', ') || 'none'}`);
      console.log(`${total} member(s): ${members.map(m => m.name || m.account).join(', ')}`); });
  }
  if (cmd === 'proposal' && a) { const v = await proposalView(a); return emit(v, () => printProposal(v)); }

  const mgr = await contractAddress('ORG_MANAGER');
  if (cmd === 'vote' && a && b) {
    const support = { against: 0, for: 1, abstain: 2 }[b]; if (support === undefined) { console.log('vote for, against or abstain'); process.exit(2); }
    printProposal(await proposalView(a));
    await send(`castVote ${a} ${b}`, mgr, OM.encodeFunctionData('castVote', [BigInt(a), support]));
    const g = await engine(); const voted = await g.hasVoted(a, account()); const after = await g.getProposal(a);
    console.log(voted ? `your vote counted · the proposal is now ${STATUS[Number(after.status)]}` : 'the vote did NOT count'); process.exit(voted ? 0 : 1);
  }
  if (cmd === 'run' && a) { printProposal(await proposalView(a)); await send(`execute ${a}`, mgr, OM.encodeFunctionData('execute', [BigInt(a)])); const p = await (await engine()).getProposal(a); console.log(`now ${STATUS[Number(p.status)]}`); process.exit(Number(p.status) === 2 ? 0 : 1); }
  const PROPOSE_USAGE = 'propose <org> pay <who> <OX> | add-member <who> | remove-member <who> | publish-channel <owner>/<slug> ["<label>"] | set-record <key> <value> | delete-record <key>\n' +
    '  | set quorum <percent> | set vote-hours <h> | set max-open <1-5> | set wait on|off | set one-per-member on|off   (the org\'s voting settings; current ones: org.js show <org>)\n' +
    'rules: an org has at most its limit of open proposals (org.js show <org> says it, 2 by default), and each member may have only ONE proposal still waiting for votes; propose the next one after yours passes, or ask another member';
  if (cmd === 'propose' && !b) { console.log(PROPOSE_USAGE); process.exit(2); }
  if (cmd === 'propose' && a && b) {
    if (b === 'add') b = 'add-member'; if (b === 'remove') b = 'remove-member';
    const { account: org, name } = await resolveAccount(a); let type, params, words;
    if (b === 'pay' && c && d) {
      const { account: payee, name: pn } = await resolveAccount(c);
      const sm = await contract('SAFE_MANAGER', ['function getMainSafeAddress(address) view returns (address)']); const ox = await contract('PUBLICOS_TOKEN', ['function decimals() view returns (uint8)']);
      const amount = ethers.parseUnits(d, await ox.decimals());
      type = 5; params = empty({ targetAddress: await contractAddress('PUBLICOS_TOKEN'), dataParam: new ethers.Interface(['function transfer(address,uint256)']).encodeFunctionData('transfer', [await sm.getMainSafeAddress(payee), amount]) });
      words = `pay ${d} OX from ${name}'s MainSafe to ${pn}`;
    } else if ((b === 'add-member' || b === 'remove-member') && c) { const { account: m, name: mn } = await resolveAccount(c); type = b === 'add-member' ? 2 : 3; params = empty({ targetAddress: m }); words = `${b.replace('-', ' ')} ${mn}`; }
    else if (b === 'set-record' && c && d) { const rt = Number(arg('type', '0')); type = 0; params = empty({ keyParam: c, valueStringParam: recordEnvelope(c, d, rt, arg('custom', '')), recordTypeValueParam: rt, customTypeParam: arg('custom', '') }); words = `write the record ${c}`; }
    else if (b === 'publish-channel' && c) {
      // Show a member's channel on the org's profile: a channel tab record (records standard), voted like any record.
      const m = c.match(/\/api\/(0x[0-9a-fA-F]{40})\/channels\/([^/?#]+)/) || c.match(/^([^/]+)\/([a-z0-9-]+)$/);
      if (!m) { console.log('publish-channel takes <owner>/<slug> or the channel URL'); process.exit(2); }
      const { account: owner, name: on } = await resolveAccount(m[1]);
      const t = channelTabRecord(await sspUrl(owner), owner, m[2], d || m[2]);
      type = 0; params = empty({ keyParam: t.key, valueStringParam: t.value, recordTypeValueParam: t.type, customTypeParam: t.customType });
      words = `show ${on}'s channel "${m[2]}" on the org's profile (record ${t.key} -> ${t.url})`;
    }
    else if (b === 'delete-record' && c) { type = 1; params = empty({ keyParam: c }); words = `delete the record ${c}`; }
    else if (b === 'set' && c && d !== undefined) {
      // The org's voting settings, changed by a vote like anything else (the contract re-checks the same bounds).
      const onoff = (v) => { if (!/^(on|off)$/.test(v)) { console.log(`${c} takes on or off`); process.exit(2); } return v === 'on' ? 1n : 0n; };
      const num = (v, lo, hi, what) => { const n = Number(v); if (!Number.isFinite(n) || n < lo || n > hi) { console.log(`${c} takes ${what}`); process.exit(2); } return n; };
      if (c === 'quorum') { const p = num(d, 0, 100, 'a percent, 0 to 100 (the votes for plus the abstentions a proposal needs, as a share of the members\' total voting weight; 0 = no minimum turnout)'); type = 50; params = empty({ valueParam: BigInt(Math.round(p * 100)) }); words = `set the quorum to ${p}% of the members' voting weight`; }
      else if (c === 'vote-hours') { const h = num(d, 1, 720, 'hours, 1 to 720 (30 days)'); type = 51; params = empty({ valueParam: BigInt(Math.round(h * 3600)) }); words = `make a vote last ${h} h`; }
      else if (c === 'max-open') { const n = num(d, 1, 5, 'a whole number, 1 to 5'); if (!Number.isInteger(n)) { console.log('max-open takes a whole number, 1 to 5'); process.exit(2); } type = 52; params = empty({ valueParam: BigInt(n) }); words = `allow up to ${n} open votes at once`; }
      else if (c === 'wait') { const v = onoff(d); type = 53; params = empty({ valueParam: v }); words = v ? 'make a passed vote wait for the end of its period' : 'make a vote run the moment it passes'; }
      else if (c === 'one-per-member') { const v = onoff(d); type = 56; params = empty({ valueParam: v }); words = v ? 'allow each member only one proposal waiting for votes' : 'let members have several proposals waiting at once'; }
      else { console.log('settings: quorum <percent> | vote-hours <h> | max-open <1-5> | wait on|off | one-per-member on|off   (see the current ones: org.js show <org>)'); process.exit(2); }
    }
    else { console.log(PROPOSE_USAGE); process.exit(2); }
    const before = (await (await engine()).openProposals(org)).map(String);
    console.log(`proposing in ${name}: ${words}`);
    await send('startVote', mgr, OM.encodeFunctionData('startVote', [org, type, params, ZERO32]));
    const after = (await (await engine()).openProposals(org)).map(String); const made = after.filter(x => !before.includes(x));
    console.log(made.length ? `proposal ${made.join(', ')} is open` : 'no new open proposal (in an org of one, or one that runs at once, it may already have run: check the org)'); return;
  }
  if (cmd === 'delegate' && a && b) { const { account: org } = await resolveAccount(a); const { account: to } = await resolveAccount(b); await send('delegate', mgr, OM.encodeFunctionData('delegate', [org, ZERO32, to])); return; }
  if (cmd === 'leave' && a) { const { account: org } = await resolveAccount(a); await send('leaveOrg', mgr, OM.encodeFunctionData('leaveOrg', [org])); const still = await os.isMember(org, account()); process.exit(still ? 1 : 0); }
  if (cmd === 'create' && a) {
    const members = []; for (const m of (arg('members') || '').split(',').filter(Boolean)) members.push((await resolveAccount(m.trim())).account);
    if (!members.length) { console.log('name the first members: --members=<who>,<who> (include yourself)'); process.exit(2); }
    const AMI = new ethers.Interface(['function createOrg(string,address[],uint256,bool) returns (address)']);
    await send(`createOrg ${a}`, await contractAddress('ACCOUNT_MANAGER'), AMI.encodeFunctionData('createOrg', [a, members, BigInt(arg('threshold', '1')), flag('public')]));
    const made = await (await contract('ACCOUNT_MEMORY', ['function getAccountAddressByDisplayName(string) view returns (address)'])).getAccountAddressByDisplayName(a);
    console.log(made !== ethers.ZeroAddress ? `created ${a} ${made}` : 'NOT created'); process.exit(made !== ethers.ZeroAddress ? 0 : 1);
  }
  console.log('usage: node org.js mine [who] | show <org> | proposal <id> | vote <id> for|against|abstain | run <id> | propose <org> … | delegate <org> <who> | leave <org> | create "<name>" --members=…');
  process.exit(2);
})().catch(fail);
