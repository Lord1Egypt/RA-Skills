#!/usr/bin/env node
/** 爪爪桥接 v15 — Node.js 版（Windows 兼容）*/
const WebSocket = require('ws');
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');
const os = require('os');

const API = process.env.ZZ_API || 'https://ai0000.cn/zz/';
const ID_FILE = path.join(os.homedir(), '.zz', 'id');

// 读取或获取编号
let MY_ID;
try {
  MY_ID = fs.readFileSync(ID_FILE, 'utf8').trim();
  console.log(`[加载] 编号: ${MY_ID}`);
} catch {
  // 没有本地编号，向服务器注册
  try {
    const resp = execSync(`curl -s "${API}register"`, { encoding: 'utf8' });
    MY_ID = JSON.parse(resp).id;
    fs.mkdirSync(path.dirname(ID_FILE), { recursive: true });
    fs.writeFileSync(ID_FILE, MY_ID);
    console.log(`[注册成功] 编号: ${MY_ID}`);
  } catch (e) {
    console.error(`[错误] 获取编号失败: ${e.message}`);
    process.exit(1);
  }
}

const BRIDGE_ID = 'D' + MY_ID;
const SESSION_ID = 'zz-' + MY_ID;
const WS_URL = API.replace('https://', 'wss://').replace('http://', 'ws://') + `?role=bridge&uid=${MY_ID}`;

let lastProcessedId = '';

function callOpenClaw(message) {
  try {
    const stdout = execSync(
      `openclaw agent -m "${message.replace(/"/g, '\\"')}" --session-id ${SESSION_ID} --json --timeout 120`,
      { encoding: 'utf8', timeout: 130000 }
    );
    const jsonStart = stdout.indexOf('{');
    if (jsonStart < 0) return null;
    const data = JSON.parse(stdout.slice(jsonStart));
    const payloads = data?.result?.payloads;
    if (payloads && payloads.length > 0) return payloads[0].text;
    return null;
  } catch (e) {
    if (e.killed) console.log('[CLI 超时]');
    else console.log(`[CLI 错误] ${e.message?.slice(0, 100)}`);
    return null;
  }
}

function handleMessage(data) {
  const msgId = data.msg_id || '';
  const to = data.to || '';
  const content = data.content || '';

  if (!content) return null;
  if (msgId && msgId === lastProcessedId) return null;
  if (to && to !== MY_ID && to !== BRIDGE_ID) return null;

  lastProcessedId = msgId;
  const sender = data.from || '';
  console.log(`[收] #${sender}: ${content.slice(0, 80)}`);

  const reply = callOpenClaw(content);
  if (!reply) {
    console.log('[跳过] CLI 无回复');
    return null;
  }

  console.log(`[回] → #${sender}: ${reply.slice(0, 80)}`);
  return {
    msg_id: `reply-${msgId}`,
    from: BRIDGE_ID,
    to: sender,
    content: reply,
    ts: Date.now()
  };
}

function connect() {
  const ws = new WebSocket(WS_URL);
  ws.on('open', () => console.log(`[已连接] ${WS_URL}`));
  ws.on('close', () => { console.log('[断开] 5秒后重连...'); setTimeout(connect, 5000); });
  ws.on('error', (e) => console.log(`[错误] ${e.message}`));
  ws.on('message', (raw) => {
    try {
      const data = JSON.parse(raw);
      const reply = handleMessage(data);
      if (reply) ws.send(JSON.stringify(reply));
    } catch {}
  });
}

console.log(`
  ┌────────────────────────────────────────┐
  │  🦞 爪爪桥接 v15 (Node.js)            │
  │  编号: ${MY_ID.padEnd(10)} (bridge: ${BRIDGE_ID})  │
  │  引擎: WebSocket + openclaw agent      │
  └────────────────────────────────────────┘
`);

connect();
