#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

function usage() {
  console.error('Usage: node probe_wechat_qr_state.js --ws-url <ws://...> [--output <path>]');
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
    const visible = (el) => {
      if (!el) return false;
      const style = window.getComputedStyle(el);
      return style.display !== 'none' && style.visibility !== 'hidden' && style.opacity !== '0';
    };
    const text = (el) => (el?.innerText || el?.textContent || '').replace(/\\s+/g, ' ').trim();
    const qrImg = document.querySelector('.js_qrcode_img, .web_qrcode_img, .qrcode');
    const afterScan = document.querySelector('.js_wx_after_scan');
    const defaultTip = document.querySelector('.js_wx_default_tip');
    const timeoutPanel = document.querySelector('.js_wx_timeout, .js_timeout, .js_qrcode_timeout');
    const refreshBtn = document.querySelector('.js_refresh_qrcode');
    const qrImageUrl = qrImg ? qrImg.src : '';
    const qrSrcExpired = /expired/i.test(qrImageUrl);
    let status = 'AUTH_CAPTURE_UNVERIFIED';
    if (visible(afterScan)) status = 'AUTH_WAITING_CONFIRMATION';
    else if (qrSrcExpired || visible(timeoutPanel) || (visible(refreshBtn) && (!visible(qrImg) || qrSrcExpired))) status = 'QR_EXPIRED';
    else if (visible(qrImg) || visible(defaultTip)) status = 'QR_READY';
    return {
      title: document.title,
      url: location.href,
      status,
      qr_image_url: qrImageUrl,
      qr_src_expired: qrSrcExpired,
      qr_visible: visible(qrImg),
      after_scan_visible: visible(afterScan),
      timeout_visible: visible(timeoutPanel),
      refresh_visible: visible(refreshBtn),
      page_text: text(document.body).slice(0, 500),
      hints: {
        default_tip: text(defaultTip).slice(0, 200),
        after_scan: text(afterScan).slice(0, 200),
        timeout: text(timeoutPanel).slice(0, 200)
      }
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
    mode: 'wechat-qr-probe',
  }, null, 2));
  process.exit(2);
});
