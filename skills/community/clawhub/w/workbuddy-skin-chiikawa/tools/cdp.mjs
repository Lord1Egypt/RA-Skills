#!/usr/bin/env node
// cdp.mjs — 极简 CDP 客户端：对 WorkBuddy renderer 执行 JS
// 用法: node tools/cdp.mjs '<js expression>'  或  node tools/cdp.mjs -f script.js
import { readFileSync } from 'node:fs';

const PORT = process.env.WB_PORT || 9223;

async function main() {
  let expr;
  if (process.argv[2] === '-f') expr = readFileSync(process.argv[3], 'utf8');
  else expr = process.argv[2];
  if (!expr) { console.error('usage: cdp.mjs <expr> | -f file'); process.exit(1); }

  const list = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
  const page = list.find(t => t.type === 'page' && t.url.includes('renderer/index.html'));
  if (!page) { console.error('renderer not found'); process.exit(1); }

  const ws = new WebSocket(page.webSocketDebuggerUrl);
  await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });

  const result = await new Promise((resolve, reject) => {
    ws.onmessage = (ev) => {
      const msg = JSON.parse(ev.data);
      if (msg.id === 1) resolve(msg);
    };
    ws.send(JSON.stringify({
      id: 1, method: 'Runtime.evaluate',
      params: { expression: expr, returnByValue: true, awaitPromise: true },
    }));
    setTimeout(() => reject(new Error('timeout')), 15000);
  });
  ws.close();

  const r = result.result;
  if (r?.exceptionDetails) {
    console.error('JS ERROR:', JSON.stringify(r.exceptionDetails.exception?.description || r.exceptionDetails.text));
    process.exit(1);
  }
  const val = r?.result?.value;
  console.log(typeof val === 'string' ? val : JSON.stringify(val, null, 2));
}
main().catch(e => { console.error(e.message); process.exit(1); });
