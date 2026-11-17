#!/usr/bin/env node
/* cdp-shot.js —— CDP 无头截图后端（零依赖，纯 node 标准库）
   背景: Chrome/Edge 132+ 逐步移除旧 headless CLI 开关（--screenshot/--dump-dom/--print-to-pdf），
   Chrome 152 上这些开关被静默忽略。本模块通过 --remote-debugging-port + DevTools 协议(WebSocket)
   实现与旧 --screenshot + --virtual-time-budget 等价的能力：
     Page.enable → setDeviceMetricsOverride(1920x1080) → navigate → loadEventFired
     → Emulation.setVirtualTimePolicy(pauseIfNetworkFetchesPending, budget) → virtualTimeBudgetExpired
     → Page.captureScreenshot → base64 落盘
   导出: async function cdpShot({ browser, url, out, width, height, budget, timeoutMs })
   被 shot.js 在旧 CLI 截图失败时作为回退调用；也可独立测试:
     node scripts/cdp-shot.js <浏览器> <页面路径或URL> <输出.png> [budget=20000] */
const net = require('net'), http = require('http'), crypto = require('crypto'),
      fs = require('fs'), path = require('path'), os = require('os'), { spawn } = require('child_process');

/* ---------- 极简 WebSocket 客户端（RFC6455 客户端侧，文本帧 + 分片 + ping/pong） ---------- */
class WS {
  constructor(sock) { this.sock = sock; this.buf = Buffer.alloc(0); this.msgs = []; this.waiters = []; this.started = false; }
  _start() {  // 握手完成（101 头摘除）后才开始按帧解析，避免把 HTTP 头误读为帧
    if (this.started) return; this.started = true;
    this.sock.on('data', d => { this.buf = Buffer.concat([this.buf, d]); this._parse(); });
  }
  _parse() {
    while (true) {
      if (this.buf.length < 2) return;
      const b0 = this.buf[0], b1 = this.buf[1];
      const fin = (b0 & 0x80) !== 0, op = b0 & 0x0f, masked = (b1 & 0x80) !== 0;
      let len = b1 & 0x7f, off = 2;
      if (len === 126) { if (this.buf.length < 4) return; len = this.buf.readUInt16BE(2); off = 4; }
      else if (len === 127) { if (this.buf.length < 10) return; const hi = this.buf.readUInt32BE(2), lo = this.buf.readUInt32BE(6); len = hi * 4294967296 + lo; off = 10; }
      let mask = null;
      if (masked) { if (this.buf.length < off + 4) return; mask = this.buf.slice(off, off + 4); off += 4; }
      if (this.buf.length < off + len) return;
      let payload = this.buf.slice(off, off + len);
      if (mask) { const out = Buffer.allocUnsafe(len); for (let i = 0; i < len; i++) out[i] = payload[i] ^ mask[i & 3]; payload = out; }
      this.buf = this.buf.slice(off + len);
      if (op === 0x8) { try { this.sock.end(); } catch (e) {} return; }              // close
      if (op === 0x9) { this._sendFrame(0x0A, payload); continue; }                   // ping → pong
      if (op === 0x1 || op === 0x2 || op === 0x0) {
        this._frag = this._frag ? Buffer.concat([this._frag, payload]) : payload;
        if (fin) { const msg = this._frag.toString('utf8'); this._frag = null;
          const w = this.waiters.shift(); if (w) w.resolve(msg); else this.msgs.push(msg); }
      }
    }
  }
  _sendFrame(op, payload) {
    const mask = crypto.randomBytes(4), masked = Buffer.allocUnsafe(payload.length);
    for (let i = 0; i < payload.length; i++) masked[i] = payload[i] ^ mask[i & 3];
    let hdr;
    if (payload.length <= 125) hdr = Buffer.from([0x80 | op, 0x80 | payload.length]);
    else if (payload.length <= 65535) { hdr = Buffer.alloc(4); hdr[0] = 0x80 | op; hdr[1] = 0x80 | 126; hdr.writeUInt16BE(payload.length, 2); }
    else { hdr = Buffer.alloc(10); hdr[0] = 0x80 | op; hdr[1] = 0x80 | 127; hdr.writeUInt32BE(0, 2); hdr.writeUInt32BE(payload.length, 6); }
    this.sock.write(Buffer.concat([hdr, mask, masked]));
  }
  send(str) { this._sendFrame(0x1, Buffer.from(str, 'utf8')); }
  next(timeoutMs) {
    if (this.dead) return Promise.reject(this.dead);
    if (this.msgs.length) return Promise.resolve(this.msgs.shift());
    return new Promise((resolve, reject) => {
      const t = setTimeout(() => { this.waiters = this.waiters.filter(w => w.resolve !== resolveFn); reject(new Error('WS 消息等待超时')); }, timeoutMs);
      const resolveFn = m => { clearTimeout(t); resolve(m); };
      this.waiters.push({ resolve: resolveFn, reject: e => { clearTimeout(t); reject(e); } });
    });
  }
  static async connect(port, path_) {
    const key = crypto.randomBytes(16).toString('base64');
    const sock = net.connect(port, '127.0.0.1');
    await new Promise((res, rej) => { sock.once('connect', res); sock.once('error', rej); });
    sock.write(`GET ${path_} HTTP/1.1\r\nHost: 127.0.0.1:${port}\r\nUpgrade: websocket\r\nConnection: Upgrade\r\nSec-WebSocket-Key: ${key}\r\nSec-WebSocket-Version: 13\r\n\r\n`);
    const ws = new WS(sock);
    // 摘掉 101 响应头：首帧数据前必有一段 \r\n\r\n 结尾的 HTTP 头（临时监听供轮询读取）
    const onData = d => { ws.buf = Buffer.concat([ws.buf, d]); };
    sock.on('data', onData);
    await new Promise((resolve, reject) => {
      const t = setTimeout(() => reject(new Error('WS 握手超时')), 10000);
      const iv = setInterval(() => {
        const i = ws.buf.indexOf('\r\n\r\n');
        if (i >= 0) { const head = ws.buf.slice(0, i).toString(); ws.buf = ws.buf.slice(i + 4);
          clearInterval(iv); clearTimeout(t); sock.removeListener('data', onData);
          if (/HTTP\/1\.1 101/.test(head)) { ws._start(); resolve(); } else reject(new Error('WS 握手被拒: ' + head.split('\r\n')[0])); }
      }, 30);
      sock.once('error', e => { clearInterval(iv); clearTimeout(t); reject(e); });
    });
    return ws;
  }
}

/* ---------- CDP 会话 ---------- */
class CDP {
  constructor(ws) { this.ws = ws; this.id = 0; this.pend = new Map(); this.handlers = []; this._pump(); }
  async _pump() {
    try { while (true) { const raw = await this.ws.next(300000);
      const msg = JSON.parse(raw);
      if (msg.id && this.pend.has(msg.id)) { const p = this.pend.get(msg.id); this.pend.delete(msg.id); msg.error ? p.rej(new Error(msg.error.message)) : p.res(msg.result); }
      else if (msg.method) this.handlers.forEach(h => h(msg));
    } } catch (e) { /* 连接关闭或超时 */ }
  }
  send(method, params, timeoutMs = 60000) {
    return new Promise((res, rej) => {
      const id = ++this.id; this.pend.set(id, { res, rej });
      this.ws.send(JSON.stringify({ id, method, params: params || {} }));
      setTimeout(() => { if (this.pend.has(id)) { this.pend.delete(id); rej(new Error(method + ' 超时')); } }, timeoutMs);
    });
  }
  waitEvent(method, timeoutMs = 90000) {
    return new Promise((resolve, reject) => {
      const t = setTimeout(() => { this.handlers = this.handlers.filter(h => h !== h0); reject(new Error('等待事件超时: ' + method)); }, timeoutMs);
      const h0 = msg => { if (msg.method === method) { clearTimeout(t); this.handlers = this.handlers.filter(x => x !== h0); resolve(msg.params); } };
      this.handlers.push(h0);
    });
  }
}

function freePort() { return new Promise(res => { const s = net.createServer(); s.listen(0, '127.0.0.1', () => { const p = s.address().port; s.close(() => res(p)); }); }); }
function httpJSON(port, p) { return new Promise((res, rej) => { http.get({ host: '127.0.0.1', port, path: p, timeout: 3000 }, r => { let b = ''; r.on('data', d => b += d); r.on('end', () => { try { res(JSON.parse(b)); } catch (e) { rej(e); } }); }).on('error', rej).on('timeout', function () { this.destroy(new Error('http 超时')); }); }); }

async function cdpShot({ browser, url, out, width = 1920, height = 1080, budget = 20000, timeoutMs = 120000, readyJs = null, settleMs = 3500 }) {
  const port = await freePort();
  const profile = path.join(os.tmpdir(), 'cdp-profile-' + process.pid + '-' + Date.now());
  const cp = spawn(browser, ['--headless=new', '--remote-debugging-port=' + port, '--user-data-dir=' + profile,
    '--no-first-run', '--no-default-browser-check', '--disable-gpu', '--hide-scrollbars', 'about:blank'],
    { stdio: 'ignore' });
  const kill = () => { try { cp.kill(); } catch (e) {} };
  const DBG = process.env.SHOT_DEBUG ? m => console.error('[cdp] ' + m) : () => {};
  const main = (async () => {
    // 等 DevTools HTTP 就绪并找到 page target
    let wsUrl = null;
    for (let i = 0; i < 60; i++) {
      await new Promise(r => setTimeout(r, 500));
      try { const list = await httpJSON(port, '/json/list');
        const page = list.find(t => t.type === 'page');
        if (page) { wsUrl = page.webSocketDebuggerUrl; break; } } catch (e) {}
    }
    if (!wsUrl) throw new Error('DevTools 服务未就绪（浏览器可能被策略禁止调试）');
    DBG('devtools 就绪 ' + wsUrl.slice(0, 60));
    const ws = await WS.connect(port, new URL(wsUrl).pathname + (new URL(wsUrl).search || ''));
    wsSock = ws.sock;
    DBG('ws 已连接');
    const cdp = new CDP(ws);
    await cdp.send('Page.enable');
    await cdp.send('Emulation.setDeviceMetricsOverride', { width, height, deviceScaleFactor: 1, mobile: false });
    const loadP = cdp.waitEvent('Page.loadEventFired', 60000);
    await cdp.send('Page.navigate', { url: encodeURI(url) });
    DBG('navigate 已发出');
    await loadP;
    DBG('load 完成');
    // 定格等待：页面侧已注入 0s transition，动画 cue 一次性到位；等字体+启动完成
    // readyJs 为真值表达式，轮询直到为 true（默认 20s 上限）；否则退化为固定 settleMs 等待
    if (readyJs) {
      let ok = false;
      for (let i = 0; i < 80 && !ok; i++) {
        await new Promise(r => setTimeout(r, 250));
        try { const r = await cdp.send('Runtime.evaluate', { expression: readyJs, returnByValue: true });
          ok = !!(r && r.result && r.result.value === true); } catch (e) {}
      }
      DBG('readyJs=' + ok);
    } else {
      await new Promise(r => setTimeout(r, settleMs || 3500));
    }
    const shot = await cdp.send('Page.captureScreenshot', { format: 'png' });
    fs.writeFileSync(out, Buffer.from(shot.data, 'base64'));
    DBG('截图已落盘 ' + out);
    try { await cdp.send('Browser.close', {}, 5000); } catch (e) {}
  })();
  try { await Promise.race([main, new Promise((_, rej) => setTimeout(() => rej(new Error('CDP 全流程超时 ' + timeoutMs + 'ms')), timeoutMs))]); }
  finally { kill(); }
}

module.exports = cdpShot;
/* 独立自测: node cdp-shot.js <浏览器> <页面> <输出.png> [budget] */
if (require.main === module) {
  const [, , b, u, o, bd] = process.argv;
  if (!b || !u || !o) { console.error('用法: node cdp-shot.js <浏览器> <页面路径或URL> <输出.png> [budget]'); process.exit(1); }
  const url = /^https?:|^file:/.test(u) ? u : 'file:///' + path.resolve(u).replace(/\\/g, '/');
  cdpShot({ browser: b, url, out: o, budget: bd ? +bd : 20000 }).then(
    () => { console.log('saved(CDP): ' + o); process.exit(0); },
    e => { console.error('✗ CDP 截图失败: ' + e.message); process.exit(1); });
}
