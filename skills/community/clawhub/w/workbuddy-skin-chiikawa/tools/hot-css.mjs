import { readFileSync } from 'node:fs';

const ROOT = new URL('..', import.meta.url).pathname;
const list = await (await fetch('http://127.0.0.1:9223/json/list')).json();
const page = list.find(t => t.type === 'page' && t.url.includes('renderer/index.html'));
if (!page) { console.error('no renderer'); process.exit(1); }
const css = readFileSync(ROOT + 'src/theme.css', 'utf8');
const bg = readFileSync(ROOT + 'assets/bg.jpg').toString('base64');
const themed = css.replace(/\/\*__BG__\*\/"";\/\*__END__\*\//, () => JSON.stringify(`data:image/jpeg;base64,${bg}`));
const expr = `(() => { const el = document.getElementById('wbs-style'); if (!el) return 'no style el'; el.textContent = ${JSON.stringify(themed)}; return 'hot updated'; })()`;
const ws = new WebSocket(page.webSocketDebuggerUrl);
await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
ws.onmessage = ev => { const m = JSON.parse(ev.data); if (m.id === 1) { console.log('✓', m.result?.result?.value ?? JSON.stringify(m.result)); ws.close(); process.exit(0); } };
ws.send(JSON.stringify({ id: 1, method: 'Runtime.evaluate', params: { expression: expr, returnByValue: true } }));
setTimeout(() => { console.error('timeout'); process.exit(1); }, 15000);
