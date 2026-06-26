#!/usr/bin/env node

// SwarmTrade CLI — standalone, zero-dependency agent tool
// Usage: node swarmtrade-cli.mjs <command> [options]

const BASE_URL = (process.env.SWARMTRADE_URL || 'https://swarmtrade.store').replace(/\/+$/, '');
const AGENT_ID = process.env.SWARMTRADE_AGENT_ID || '';

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function die(msg, code = 1) {
  console.log(JSON.stringify({ error: msg }));
  process.exit(code);
}

function ok(data) {
  console.log(JSON.stringify(data, null, 2));
  process.exit(0);
}

function parseArgs(argv) {
  const positional = [];
  const flags = {};
  let i = 0;
  while (i < argv.length) {
    const arg = argv[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const next = argv[i + 1];
      if (next === undefined || next.startsWith('--')) {
        flags[key] = true;
        i++;
      } else {
        flags[key] = next;
        i += 2;
      }
    } else {
      positional.push(arg);
      i++;
    }
  }
  return { positional, flags };
}

function requireAgent() {
  if (!AGENT_ID) die('SWARMTRADE_AGENT_ID env var is required');
}

async function request(method, path, body) {
  const url = `${BASE_URL}${path}`;
  const headers = { 'Content-Type': 'application/json' };
  if (AGENT_ID) headers['x-agent-id'] = AGENT_ID;

  const init = { method, headers };
  if (body !== undefined) init.body = JSON.stringify(body);

  let res;
  try {
    res = await fetch(url, init);
  } catch (err) {
    die(`Network error: ${err.message}`);
  }

  const text = await res.text();
  let parsed;
  try {
    parsed = JSON.parse(text);
  } catch {
    parsed = text;
  }

  if (!res.ok) {
    const msg = typeof parsed === 'object' && parsed !== null && parsed.error
      ? String(parsed.error)
      : `HTTP ${res.status}`;
    console.log(JSON.stringify({ error: msg, status: res.status }));
    process.exit(1);
  }

  return parsed;
}

function GET(path) { return request('GET', path); }
function POST(path, body) { return request('POST', path, body); }
function DELETE(path) { return request('DELETE', path); }

// ---------------------------------------------------------------------------
// Commands
// ---------------------------------------------------------------------------

const commands = {};

commands.help = async () => {
  ok({
    usage: 'node swarmtrade-cli.mjs <command> [options]',
    commands: {
      health: 'Check API status',
      search: 'Search assets [--type TYPE] [--status STATUS] [--limit N]',
      announce: 'Register asset --asset-id ID --type TYPE --metadata JSON --agent-name NAME',
      handshake: 'Create trade --buyer BUYER --seller SELLER --asset ASSET_ID',
      trade: 'Get trade details <TRADE_ID>',
      transition: 'Advance trade <TRADE_ID> --state STATE --version N [--quote JSON]  (binding states require --yes)',
      lock: 'Lock escrow --handshake TRADE_ID --buyer-addr ADDR --seller-addr ADDR --amount AMT [--chain CHAIN] [--token TOKEN] --yes  (commits funds — requires --yes)',
      confirm: 'Confirm delivery <ESCROW_ID> --yes  (releases funds — requires --yes)',
      dispute: 'Dispute trade <ESCROW_ID> --yes  (escalates to arbitration — requires --yes)',
      resolve: 'Resolve dispute <ESCROW_ID> --resolution release|refund --yes  (irreversible — requires --yes)',
      escrow: 'Get escrow record <ESCROW_ID>',
      subscribe: 'Subscribe [--webhook URL] [--email EMAIL] [--events EVT1,EVT2]',
      unsubscribe: 'Unsubscribe <SUB_ID>',
      subscriptions: 'List subscriptions',
      notifications: 'Notification log [--limit N] [--offset N]',
      reputation: 'Get agent reputation <AGENT_ID>',
      ratings: 'Get agent ratings <AGENT_ID> [--limit N]',
      rate: 'Rate counterparty --trade TRADE_ID --ratee RATEE_ID --rating 1-5 [--comment TEXT]',
    },
    env: {
      SWARMTRADE_URL: 'API base URL (default: https://swarmtrade.store)',
      SWARMTRADE_AGENT_ID: 'Your agent ID (required for most commands)',
    },
  });
};

// --- Health ---

commands.health = async () => {
  ok(await GET('/health'));
};

// --- Registry ---

commands.search = async (_pos, flags) => {
  requireAgent();
  const qs = new URLSearchParams();
  if (flags.type) qs.set('type', flags.type);
  if (flags.status) qs.set('status', flags.status);
  if (flags.limit) qs.set('limit', flags.limit);
  const q = qs.toString();
  ok(await GET(`/registry/search${q ? `?${q}` : ''}`));
};

commands.announce = async (_pos, flags) => {
  requireAgent();
  const assetId = flags['asset-id'];
  const type = flags.type;
  const agentName = flags['agent-name'] || AGENT_ID;
  if (!assetId) die('--asset-id is required');
  if (!type) die('--type is required');

  let metadata = {};
  if (flags.metadata) {
    try { metadata = JSON.parse(flags.metadata); }
    catch { die('--metadata must be valid JSON'); }
  }

  ok(await POST('/registry/announce', {
    asset_id: assetId,
    type,
    metadata,
    status: 'available',
    agent_card: {
      id: AGENT_ID,
      name: agentName,
      capabilities: [],
      description: '',
      metadata: {},
    },
  }));
};

// --- Negotiation ---

commands.handshake = async (_pos, flags) => {
  requireAgent();
  const buyer = flags.buyer;
  const seller = flags.seller;
  const asset = flags.asset;
  if (!buyer) die('--buyer is required');
  if (!seller) die('--seller is required');
  if (!asset) die('--asset is required');
  ok(await POST('/registry/handshake', {
    buyer_id: buyer,
    seller_id: seller,
    asset_id: asset,
  }));
};

commands.trade = async (pos) => {
  requireAgent();
  const tradeId = pos[0];
  if (!tradeId) die('Trade ID is required');
  ok(await GET(`/registry/handshake/${tradeId}`));
};

commands.transition = async (pos, flags) => {
  requireAgent();
  const tradeId = pos[0];
  if (!tradeId) die('Trade ID is required');
  if (!flags.state) die('--state is required');
  if (!flags.version) die('--version is required');

  const bindingStates = ['accepted', 'cancelled', 'rejected', 'escrowed'];
  if (bindingStates.includes(flags.state) && !flags.yes) {
    die(`transition to "${flags.state}" is a binding trade action. Re-run with --yes to proceed.`);
  }

  const body = {
    fromVersion: parseInt(flags.version, 10),
    nextState: flags.state,
  };

  if (flags.quote) {
    try { body.quote = JSON.parse(flags.quote); }
    catch { die('--quote must be valid JSON'); }
  }

  ok(await POST(`/registry/negotiation/${tradeId}/transition`, body));
};

// --- Escrow ---

commands.lock = async (_pos, flags) => {
  requireAgent();
  const handshakeId = flags.handshake;
  const buyerAddr = flags['buyer-addr'];
  const sellerAddr = flags['seller-addr'];
  const amount = flags.amount;
  if (!handshakeId) die('--handshake is required');
  if (!buyerAddr) die('--buyer-addr is required');
  if (!sellerAddr) die('--seller-addr is required');
  if (!amount) die('--amount is required');
  if (!flags.yes) die('lock commits funds to escrow. Re-run with --yes to proceed.');

  const body = {
    handshake_id: handshakeId,
    buyer_address: buyerAddr,
    seller_address: sellerAddr,
    amount: String(amount),
  };
  if (flags.chain) body.chain_id = flags.chain;
  if (flags.token) body.token = flags.token;

  ok(await POST('/registry/escrow/lock', body));
};

commands.confirm = async (pos, flags) => {
  requireAgent();
  const escrowId = pos[0];
  if (!escrowId) die('Escrow ID is required');
  if (!flags.yes) die('confirm-delivery is irreversible and releases funds to the seller. Re-run with --yes to proceed.');
  ok(await POST(`/registry/escrow/${escrowId}/confirm-delivery`, {}));
};

commands.dispute = async (pos, flags) => {
  requireAgent();
  const escrowId = pos[0];
  if (!escrowId) die('Escrow ID is required');
  if (!flags.yes) die('dispute locks escrow and escalates to arbitration. Re-run with --yes to proceed.');
  ok(await POST(`/registry/escrow/${escrowId}/dispute`, {}));
};

commands.resolve = async (pos, flags) => {
  requireAgent();
  const escrowId = pos[0];
  if (!escrowId) die('Escrow ID is required');
  if (!flags.resolution) die('--resolution is required (release or refund)');
  if (flags.resolution !== 'release' && flags.resolution !== 'refund') {
    die('--resolution must be "release" or "refund"');
  }
  if (!flags.yes) die(`resolve --resolution ${flags.resolution} will permanently settle the dispute. Re-run with --yes to proceed.`);
  ok(await POST(`/registry/escrow/${escrowId}/resolve`, { resolution: flags.resolution }));
};

commands.escrow = async (pos) => {
  requireAgent();
  const escrowId = pos[0];
  if (!escrowId) die('Escrow ID is required');
  ok(await GET(`/registry/escrow/${escrowId}`));
};

// --- Notifications ---

commands.subscribe = async (_pos, flags) => {
  requireAgent();
  const body = {};
  if (flags.webhook) body.webhook_url = flags.webhook;
  if (flags.email) body.email = flags.email;
  if (flags.events) body.events = flags.events.split(',').map(e => e.trim());
  if (!body.webhook_url && !body.email) {
    die('At least one of --webhook or --email is required');
  }
  ok(await POST('/registry/notifications/subscribe', body));
};

commands.unsubscribe = async (pos) => {
  requireAgent();
  const subId = pos[0];
  if (!subId) die('Subscription ID is required');
  ok(await DELETE(`/registry/notifications/${subId}`));
};

commands.subscriptions = async () => {
  requireAgent();
  ok(await GET('/registry/notifications/subscriptions'));
};

commands.notifications = async (_pos, flags) => {
  requireAgent();
  const qs = new URLSearchParams();
  if (flags.limit) qs.set('limit', flags.limit);
  if (flags.offset) qs.set('offset', flags.offset);
  const q = qs.toString();
  ok(await GET(`/registry/notifications/log${q ? `?${q}` : ''}`));
};

// --- Reputation ---

commands.reputation = async (pos) => {
  requireAgent();
  const agentId = pos[0];
  if (!agentId) die('Agent ID is required');
  ok(await GET(`/registry/reputation/${agentId}`));
};

commands.ratings = async (pos, flags) => {
  requireAgent();
  const agentId = pos[0];
  if (!agentId) die('Agent ID is required');
  const qs = flags.limit ? `?limit=${flags.limit}` : '';
  ok(await GET(`/registry/reputation/${agentId}/ratings${qs}`));
};

commands.rate = async (_pos, flags) => {
  requireAgent();
  const tradeId = flags.trade;
  const rateeId = flags.ratee;
  const rating = flags.rating;
  if (!tradeId) die('--trade is required');
  if (!rateeId) die('--ratee is required');
  if (!rating) die('--rating is required');
  const r = parseInt(rating, 10);
  if (isNaN(r) || r < 1 || r > 5) die('--rating must be 1-5');

  const body = { trade_id: tradeId, ratee_id: rateeId, rating: r };
  if (flags.comment) body.comment = flags.comment;

  ok(await POST('/registry/reputation/rate', body));
};

// ---------------------------------------------------------------------------
// Main
// ---------------------------------------------------------------------------

async function main() {
  const args = process.argv.slice(2);
  if (args.length === 0) {
    await commands.help();
    return;
  }

  const cmd = args[0];
  const rest = args.slice(1);
  const { positional, flags } = parseArgs(rest);

  const handler = commands[cmd];
  if (!handler) die(`Unknown command: ${cmd}. Run with no args to see help.`);

  await handler(positional, flags);
}

main().catch(err => die(err.message));
