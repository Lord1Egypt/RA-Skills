#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function usage() {
  console.error('Usage: node prepare_zsxq_qr_bootstrap.js --ws-url <ws://...> [--output <path>]');
}

function parseArgs(argv) {
  const args = {};
  for (let i = 2; i < argv.length; i += 1) {
    const arg = argv[i];
    const next = argv[i + 1];
    if (arg === '--ws-url') {
      args.wsUrl = next; i += 1;
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

async function cdpCall(state, method, params = {}) {
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
  const state = { ws, id: 0, pending: new Map() };
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

  const expression = `(() => {
    const icon = document.querySelector('.protocol .icon');
    const existingIframe = document.querySelector('.qrcode-container iframe');
    if (existingIframe) {
      return {
        status: 'QR_READY',
        title: document.title,
        url: location.href,
        icon_class: icon?.className || '',
        button_text: '',
        iframe_url: existingIframe.src,
        page_text: (document.body?.innerText || '').replace(/\\s+/g, ' ').trim().slice(0, 500)
      };
    }
    const btn = document.querySelector('.get-qr-btn');
    if (!icon) return { status: 'QUERY_FAILED', message: 'protocol icon not found', url: location.href, title: document.title };
    if (!btn) return { status: 'QUERY_FAILED', message: 'get-qr button not found', url: location.href, title: document.title };
    const clickIfNeeded = () => {
      if (!(icon.className || '').includes('checked')) icon.click();
      btn.click();
    };
    clickIfNeeded();
    const iframe = document.querySelector('.qrcode-container iframe');
    return {
      status: iframe ? 'QR_READY' : 'AUTH_CAPTURE_UNVERIFIED',
      title: document.title,
      url: location.href,
      icon_class: icon.className || '',
      button_text: (btn.innerText || '').trim(),
      iframe_url: iframe ? iframe.src : '',
      page_text: (document.body?.innerText || '').replace(/\\s+/g, ' ').trim().slice(0, 500)
    };
  })()`;

  try {
    const evalResult = await cdpCall(state, 'Runtime.evaluate', {
      expression,
      returnByValue: true,
      awaitPromise: true,
    });
    const payload = evalResult.result?.value || {};
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
    mode: 'zsxq-qr-bootstrap-prepare',
  }, null, 2));
  process.exit(2);
});
