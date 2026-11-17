#!/usr/bin/env node
// pause.mjs — 还原：注入本就来去无痕，重载 renderer 即回到官方外观
const PORT = 9223;
async function main() {
  const list = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
  const page = list.find(t => t.type === 'page' && t.url.includes('renderer/index.html'));
  if (!page) { console.log('· 调试端口无 renderer（皮肤本就不在）'); return; }
  const ws = new WebSocket(page.webSocketDebuggerUrl);
  await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
  ws.send(JSON.stringify({ id: 1, method: 'Page.reload', params: { ignoreCache: true } }));
  await new Promise(r => setTimeout(r, 1000));
  ws.close();
  console.log('✓ 已重载界面，恢复官方外观');
}
main().catch(e => { console.error('✗', e.message); process.exit(1); });
