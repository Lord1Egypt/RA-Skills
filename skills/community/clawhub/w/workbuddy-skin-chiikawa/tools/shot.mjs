#!/usr/bin/env node
// shot.mjs — 截取 WorkBuddy renderer 画面
// 用法: node tools/shot.mjs <out.png> [x y w h scale]
import { writeFileSync } from 'node:fs';

const PORT = process.env.WB_PORT || 9223;
const [out, x, y, w, h, scale] = process.argv.slice(2);
if (!out) { console.error('usage: shot.mjs out.png [x y w h scale]'); process.exit(1); }

const list = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
const page = list.find(t => t.type === 'page' && t.url.includes('renderer/index.html'));
if (!page) { console.error('renderer not found'); process.exit(1); }

const ws = new WebSocket(page.webSocketDebuggerUrl);
await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
let id = 0;
const pend = {};
ws.onmessage = ev => { const m = JSON.parse(ev.data); if (m.id && pend[m.id]) pend[m.id](m); };
const send = (method, params) => new Promise(r => { const i = ++id; pend[i] = r; ws.send(JSON.stringify({ id: i, method, params })); });

await send('Page.enable');
const params = { format: 'png' };
if (x !== undefined) params.clip = { x: +x, y: +y, width: +w, height: +h, scale: +(scale || 1) };
const shot = await send('Page.captureScreenshot', params);
if (!shot.result?.data) { console.error('capture failed:', JSON.stringify(shot).slice(0, 300)); process.exit(1); }
writeFileSync(out, Buffer.from(shot.result.data, 'base64'));
console.log('saved', out);
process.exit(0);
