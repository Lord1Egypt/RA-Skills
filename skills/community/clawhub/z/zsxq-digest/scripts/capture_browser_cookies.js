#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function usage() {
  console.error('Usage: node capture_browser_cookies.js --ws-url <ws://...> [--url <https://...>]... [--cookie-name <name>] [--output <path>]');
}

function parseArgs(argv) {
  const args = {
    urls: [],
  };
  for (let i = 2; i < argv.length; i += 1) {
    const arg = argv[i];
    const next = argv[i + 1];
    if (arg === '--ws-url') {
      args.wsUrl = next; i += 1;
    } else if (arg === '--url') {
      args.urls.push(next); i += 1;
    } else if (arg === '--cookie-name') {
      args.cookieName = next; i += 1;
    } else if (arg === '--output') {
      args.output = next; i += 1;
    } else if (arg === '--help' || arg === '-h') {
      args.help = true;
    } else {
      throw new Error(`unknown argument: ${arg}`);
    }
  }
  return args;
}

async function cdpCall(wsUrl, method, params, state) {
  const id = ++state.id;
  return new Promise((resolve, reject) => {
    state.pending.set(id, { resolve, reject });
    state.ws.send(JSON.stringify({ id, method, params }));
  });
}

async function main() {
  const args = parseArgs(process.argv);
  if (args.help || !args.wsUrl) {
    usage();
    process.exit(args.help ? 0 : 2);
  }

  const ws = new WebSocket(args.wsUrl);
  const state = {
    ws,
    id: 0,
    pending: new Map(),
  };

  ws.onmessage = (event) => {
    const msg = JSON.parse(event.data);
    if (msg.id && state.pending.has(msg.id)) {
      const { resolve, reject } = state.pending.get(msg.id);
      state.pending.delete(msg.id);
      if (msg.error) reject(new Error(JSON.stringify(msg.error)));
      else resolve(msg.result);
    }
  };

  await new Promise((resolve, reject) => {
    ws.onopen = resolve;
    ws.onerror = reject;
  });

  try {
    await cdpCall(args.wsUrl, 'Network.enable', {}, state);
    const result = await cdpCall(args.wsUrl, 'Network.getCookies', {
      urls: args.urls.length ? args.urls : undefined,
    }, state);
    let cookies = Array.isArray(result.cookies) ? result.cookies : [];
    if (args.cookieName) {
      cookies = cookies.filter((cookie) => cookie && cookie.name === args.cookieName);
    }
    const payload = {
      status: 'ok',
      count: cookies.length,
      ws_url: args.wsUrl,
      urls: args.urls,
      cookies,
    };
    const text = JSON.stringify(payload, null, 2);
    if (args.output) {
      fs.mkdirSync(path.dirname(args.output), { recursive: true });
      fs.writeFileSync(args.output, text + '\n', 'utf8');
    }
    console.log(text);
  } finally {
    ws.close();
  }
}

main().catch((error) => {
  console.error(JSON.stringify({
    status: 'QUERY_FAILED',
    message: error.message,
    mode: 'browser-cdp-cookie-capture',
  }, null, 2));
  process.exit(2);
});
