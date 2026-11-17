#!/usr/bin/env node
// CDP Proxy - 通过 HTTP API 操控用户日常 Chrome
// webclaw3 增强版：新增 Aria 树接口 + 请求日志
// Node.js 22+（使用原生 WebSocket）

import http from 'node:http';
import { URL } from 'node:url';
import fs from 'node:fs';
import { appendFile } from 'node:fs/promises';
import path from 'node:path';
import os from 'node:os';
import net from 'node:net';

const PORT = parseInt(process.env.CDP_PROXY_PORT || '3456');
let ws = null;
let cmdId = 0;
const pending = new Map(); // id -> {resolve, timer}
const sessions = new Map(); // targetId -> sessionId
const ariaRefs = new Map(); // targetId -> Map(refId -> { backendDOMNodeId, role, name })

// --- 请求日志（NDJSON append，与 relay.mjs 格式一致）---
const NO_LOG_PATHS = new Set(['/health', '/targets', '/logs']);
const PATH_TO_OP = {
  '/eval': 'cdp.eval',
  '/click': 'cdp.click',
  '/clickAt': 'cdp.clickAt',
  '/scroll': 'cdp.scroll',
  '/screenshot': 'cdp.screenshot',
  '/aria-tree': 'cdp.ariaTree',
  '/click-aria': 'cdp.clickAria',
  '/type-aria': 'cdp.typeAria',
  '/new': 'cdp.new',
  '/close': 'cdp.close',
  '/navigate': 'cdp.navigate',
  '/back': 'cdp.back',
  '/info': 'cdp.info',
  '/setFiles': 'cdp.setFiles',
};

const LOG_RESULT_MAX = 500;
function truncateForLog(value) {
  const s = typeof value === 'string' ? value : JSON.stringify(value);
  if (!s || s.length <= LOG_RESULT_MAX) return s;
  return s.slice(0, LOG_RESULT_MAX) + `...(truncated, original ${s.length} chars)`;
}

async function logOperation(logFile, method, pathname, params, resultOrError, durationMs) {
  if (!logFile) return;
  const op = PATH_TO_OP[pathname] || `cdp.${pathname.slice(1)}`;
  const entry = {
    op,
    params,
    timestamp: new Date().toISOString(),
    channel: 'cdp_http',
    duration_ms: durationMs,
  };
  if (resultOrError instanceof Error) {
    entry.error = resultOrError.message;
  } else {
    entry.result = truncateForLog(resultOrError);
  }
  try {
    await appendFile(logFile, JSON.stringify(entry) + '\n', 'utf-8');
  } catch { /* 日志写入失败不影响主流程 */ }
}

// --- Aria 树 ---
const SKIP_ROLES = new Set([
  'generic', 'none', 'InlineTextBox', 'LineBreak',
  'RootWebArea', 'ignored',
]);
const TEXT_ROLES = new Set(['StaticText']);

async function getAriaTree(sessionId, targetId) {
  await sendCDP('Accessibility.enable', {}, sessionId);
  const resp = await sendCDP('Accessibility.getFullAXTree', {}, sessionId);
  const nodes = resp.result?.nodes || [];

  const nodeMap = new Map();
  for (const n of nodes) nodeMap.set(n.nodeId, n);

  const refMap = new Map();
  let refCounter = 0;
  const lines = [];

  function getVal(axValue) {
    if (!axValue) return '';
    return axValue.value ?? '';
  }

  function collectText(node) {
    const parts = [];
    const name = getVal(node.name);
    if (name) parts.push(name);
    if (node.childIds) {
      for (const cid of node.childIds) {
        const child = nodeMap.get(cid);
        if (child && (TEXT_ROLES.has(getVal(child.role)) || child.ignored)) {
          const t = getVal(child.name);
          if (t && !parts.includes(t)) parts.push(t);
        }
      }
    }
    return parts.join(' ').trim();
  }

  function walk(nodeId, depth) {
    const node = nodeMap.get(nodeId);
    if (!node) return;

    const role = getVal(node.role);
    const ignored = node.ignored;

    if (ignored || SKIP_ROLES.has(role) || TEXT_ROLES.has(role)) {
      if (node.childIds) {
        for (const cid of node.childIds) walk(cid, depth);
      }
      return;
    }

    const text = collectText(node);
    if (!text && !node.childIds?.length) return;

    const refId = `e${++refCounter}`;
    if (node.backendDOMNodeId) {
      refMap.set(refId, {
        backendDOMNodeId: node.backendDOMNodeId,
        role,
        name: getVal(node.name),
      });
    }

    const indent = '  '.repeat(depth);
    const childCount = node.childIds?.filter(cid => {
      const c = nodeMap.get(cid);
      return c && !c.ignored && !SKIP_ROLES.has(getVal(c.role)) && !TEXT_ROLES.has(getVal(c.role));
    }).length || 0;

    let line = `${indent}[ref=${refId}] ${role}`;
    if (text) line += `: ${text}`;
    if (childCount > 0 && ['list', 'table', 'tablist', 'menu', 'tree', 'group', 'radiogroup'].includes(role)) {
      line += ` (${childCount} items)`;
    }
    lines.push(line);

    if (node.childIds) {
      for (const cid of node.childIds) walk(cid, depth + 1);
    }
  }

  const roots = nodes.filter(n => !nodes.some(p => p.childIds?.includes(n.nodeId)));
  if (roots.length > 0) {
    for (const root of roots) walk(root.nodeId, 0);
  }

  ariaRefs.set(targetId, refMap);
  return lines.join('\n');
}

function findAriaNode(targetId, role, name) {
  const refMap = ariaRefs.get(targetId);
  if (!refMap) return null;
  for (const [refId, info] of refMap) {
    if (info.role === role && info.name && info.name.includes(name)) {
      return { refId, ...info };
    }
  }
  // 模糊匹配：只匹配 role
  if (name === undefined || name === '') {
    for (const [refId, info] of refMap) {
      if (info.role === role) return { refId, ...info };
    }
  }
  return null;
}

async function resolveNodeToObjectId(sessionId, backendDOMNodeId) {
  await sendCDP('DOM.enable', {}, sessionId);
  const resp = await sendCDP('DOM.resolveNode', { backendNodeId: backendDOMNodeId }, sessionId);
  if (resp.result?.object?.objectId) return resp.result.object.objectId;
  throw new Error('无法解析 DOM 节点: backendDOMNodeId=' + backendDOMNodeId);
}

// --- WebSocket 兼容层 ---
let WS;
if (typeof globalThis.WebSocket !== 'undefined') {
  // Node 22+ 原生 WebSocket（浏览器兼容 API）
  WS = globalThis.WebSocket;
} else {
  // 回退到 ws 模块
  try {
    WS = (await import('ws')).default;
  } catch {
    console.error('[CDP Proxy] 错误：Node.js 版本 < 22 且未安装 ws 模块');
    console.error('  解决方案：升级到 Node.js 22+ 或执行 npm install -g ws');
    process.exit(1);
  }
}

// --- 自动发现 Chrome 调试端口 ---
async function discoverChromePort() {
  // 1. 尝试读 DevToolsActivePort 文件
  const possiblePaths = [];
  const platform = os.platform();

  if (platform === 'darwin') {
    const home = os.homedir();
    possiblePaths.push(
      path.join(home, 'Library/Application Support/Google/Chrome/DevToolsActivePort'),
      path.join(home, 'Library/Application Support/Google/Chrome Canary/DevToolsActivePort'),
      path.join(home, 'Library/Application Support/Chromium/DevToolsActivePort'),
    );
  } else if (platform === 'linux') {
    const home = os.homedir();
    possiblePaths.push(
      path.join(home, '.config/google-chrome/DevToolsActivePort'),
      path.join(home, '.config/chromium/DevToolsActivePort'),
    );
  } else if (platform === 'win32') {
    const localAppData = process.env.LOCALAPPDATA || '';
    possiblePaths.push(
      path.join(localAppData, 'Google/Chrome/User Data/DevToolsActivePort'),
      path.join(localAppData, 'Chromium/User Data/DevToolsActivePort'),
    );
  }

  for (const p of possiblePaths) {
    try {
      const content = fs.readFileSync(p, 'utf-8').trim();
      const lines = content.split('\n');
      const port = parseInt(lines[0]);
      if (port > 0 && port < 65536) {
        const ok = await checkPort(port);
        if (ok) {
          // 第二行是带 UUID 的 WebSocket 路径（如 /devtools/browser/xxx-xxx）
          // 非显式 --remote-debugging-port 启动时，Chrome 可能只接受此路径
          const wsPath = lines[1] || null;
          console.log(`[CDP Proxy] 从 DevToolsActivePort 发现端口: ${port}${wsPath ? ' (带 wsPath)' : ''}`);
          return { port, wsPath };
        }
      }
    } catch { /* 文件不存在，继续 */ }
  }

  // 2. 扫描常用端口
  const commonPorts = [9222, 9229, 9333];
  for (const port of commonPorts) {
    const ok = await checkPort(port);
    if (ok) {
      console.log(`[CDP Proxy] 扫描发现 Chrome 调试端口: ${port}`);
      return { port, wsPath: null };
    }
  }

  return null;
}

// 用 TCP 探测端口是否监听——避免 WebSocket 连接触发 Chrome 安全弹窗
// （WebSocket 探测会被 Chrome 视为调试连接，弹出授权对话框）
function checkPort(port) {
  return new Promise((resolve) => {
    const socket = net.createConnection(port, '127.0.0.1');
    const timer = setTimeout(() => { socket.destroy(); resolve(false); }, 2000);
    socket.once('connect', () => { clearTimeout(timer); socket.destroy(); resolve(true); });
    socket.once('error', () => { clearTimeout(timer); resolve(false); });
  });
}

function getWebSocketUrl(port, wsPath) {
  if (wsPath) return `ws://127.0.0.1:${port}${wsPath}`;
  return `ws://127.0.0.1:${port}/devtools/browser`;
}

// --- WebSocket 连接管理 ---
let chromePort = null;
let chromeWsPath = null;

let connectingPromise = null;
async function connect() {
  if (ws && (ws.readyState === WS.OPEN || ws.readyState === 1)) return;
  if (connectingPromise) return connectingPromise;  // 复用进行中的连接

  if (!chromePort) {
    const discovered = await discoverChromePort();
    if (!discovered) {
      throw new Error(
        'Chrome 未开启远程调试端口。请用以下方式启动 Chrome：\n' +
        '  macOS: /Applications/Google\\ Chrome.app/Contents/MacOS/Google\\ Chrome --remote-debugging-port=9222\n' +
        '  Linux: google-chrome --remote-debugging-port=9222\n' +
        '  或在 chrome://flags 中搜索 "remote debugging" 并启用'
      );
    }
    chromePort = discovered.port;
    chromeWsPath = discovered.wsPath;
  }

  const wsUrl = getWebSocketUrl(chromePort, chromeWsPath);
  if (!wsUrl) throw new Error('无法获取 Chrome WebSocket URL');

  return connectingPromise = new Promise((resolve, reject) => {
    ws = new WS(wsUrl);

    const onOpen = () => {
      cleanup();
      connectingPromise = null;
      console.log(`[CDP Proxy] 已连接 Chrome (端口 ${chromePort})`);
      resolve();
    };
    const onError = (e) => {
      cleanup();
      connectingPromise = null;
      const msg = e.message || e.error?.message || '连接失败';
      console.error('[CDP Proxy] 连接错误:', msg);
      reject(new Error(msg));
    };
    const onClose = () => {
      console.log('[CDP Proxy] 连接断开');
      ws = null;
      chromePort = null; // 重置端口缓存，下次连接重新发现
      chromeWsPath = null;
      sessions.clear();
    };
    const onMessage = (evt) => {
      const data = typeof evt === 'string' ? evt : (evt.data || evt);
      const msg = JSON.parse(typeof data === 'string' ? data : data.toString());

      if (msg.method === 'Target.attachedToTarget') {
        const { sessionId, targetInfo } = msg.params;
        sessions.set(targetInfo.targetId, sessionId);
      }
      if (msg.id && pending.has(msg.id)) {
        const { resolve, timer } = pending.get(msg.id);
        clearTimeout(timer);
        pending.delete(msg.id);
        resolve(msg);
      }
    };

    function cleanup() {
      ws.removeEventListener?.('open', onOpen);
      ws.removeEventListener?.('error', onError);
    }

    // 兼容 Node 原生 WebSocket 和 ws 模块的事件 API
    if (ws.on) {
      ws.on('open', onOpen);
      ws.on('error', onError);
      ws.on('close', onClose);
      ws.on('message', onMessage);
    } else {
      ws.addEventListener('open', onOpen);
      ws.addEventListener('error', onError);
      ws.addEventListener('close', onClose);
      ws.addEventListener('message', onMessage);
    }
  });
}

function sendCDP(method, params = {}, sessionId = null) {
  return new Promise((resolve, reject) => {
    if (!ws || (ws.readyState !== WS.OPEN && ws.readyState !== 1)) {
      return reject(new Error('WebSocket 未连接'));
    }
    const id = ++cmdId;
    const msg = { id, method, params };
    if (sessionId) msg.sessionId = sessionId;
    const timer = setTimeout(() => {
      pending.delete(id);
      reject(new Error('CDP 命令超时: ' + method));
    }, 30000);
    pending.set(id, { resolve, timer });
    ws.send(JSON.stringify(msg));
  });
}

async function ensureSession(targetId) {
  if (sessions.has(targetId)) return sessions.get(targetId);
  const resp = await sendCDP('Target.attachToTarget', { targetId, flatten: true });
  if (resp.result?.sessionId) {
    sessions.set(targetId, resp.result.sessionId);
    return resp.result.sessionId;
  }
  throw new Error('attach 失败: ' + JSON.stringify(resp.error));
}

// --- 等待页面加载 ---
async function waitForLoad(sessionId, timeoutMs = 15000) {
  // 启用 Page 域
  await sendCDP('Page.enable', {}, sessionId);

  return new Promise((resolve) => {
    let resolved = false;
    const done = (result) => {
      if (resolved) return;
      resolved = true;
      clearTimeout(timer);
      clearInterval(checkInterval);
      resolve(result);
    };

    const timer = setTimeout(() => done('timeout'), timeoutMs);
    const checkInterval = setInterval(async () => {
      try {
        const resp = await sendCDP('Runtime.evaluate', {
          expression: 'document.readyState',
          returnByValue: true,
        }, sessionId);
        if (resp.result?.result?.value === 'complete') {
          done('complete');
        }
      } catch { /* 忽略 */ }
    }, 500);
  });
}

// --- 读取 POST body ---
async function readBody(req) {
  let body = '';
  for await (const chunk of req) body += chunk;
  return body;
}

// --- HTTP API ---
const server = http.createServer(async (req, res) => {
  const parsed = new URL(req.url, `http://localhost:${PORT}`);
  const pathname = parsed.pathname;
  const q = Object.fromEntries(parsed.searchParams);
  const logFile = q.logFile || null;
  if (q.logFile) delete q.logFile;
  const startTime = Date.now();

  res.setHeader('Content-Type', 'application/json; charset=utf-8');

  try {
    // /health 不需要连接 Chrome
    if (pathname === '/health') {
      const connected = ws && (ws.readyState === WS.OPEN || ws.readyState === 1);
      res.end(JSON.stringify({ status: 'ok', connected, sessions: sessions.size, chromePort }));
      return;
    }

    await connect();

    // GET /targets - 列出所有页面
    if (pathname === '/targets') {
      const resp = await sendCDP('Target.getTargets');
      const pages = resp.result.targetInfos.filter(t => t.type === 'page');
      res.end(JSON.stringify(pages, null, 2));
    }

    // GET /new?url=xxx - 创建新后台 tab
    else if (pathname === '/new') {
      const targetUrl = q.url || 'about:blank';
      const resp = await sendCDP('Target.createTarget', { url: targetUrl, background: true });
      const targetId = resp.result.targetId;

      // 等待页面加载
      if (targetUrl !== 'about:blank') {
        try {
          const sid = await ensureSession(targetId);
          await waitForLoad(sid);
        } catch { /* 非致命，继续 */ }
      }

      res.end(JSON.stringify({ targetId }));
    }

    // GET /close?target=xxx - 关闭 tab
    else if (pathname === '/close') {
      const resp = await sendCDP('Target.closeTarget', { targetId: q.target });
      sessions.delete(q.target);
      res.end(JSON.stringify(resp.result));
    }

    // GET /navigate?target=xxx&url=yyy - 导航（自动等待加载）
    else if (pathname === '/navigate') {
      const sid = await ensureSession(q.target);
      const resp = await sendCDP('Page.navigate', { url: q.url }, sid);

      // 等待页面加载完成
      await waitForLoad(sid);

      res.end(JSON.stringify(resp.result));
    }

    // GET /back?target=xxx - 后退
    else if (pathname === '/back') {
      const sid = await ensureSession(q.target);
      await sendCDP('Runtime.evaluate', { expression: 'history.back()' }, sid);
      await waitForLoad(sid);
      res.end(JSON.stringify({ ok: true }));
    }

    // POST /eval?target=xxx - 执行 JS
    else if (pathname === '/eval') {
      const sid = await ensureSession(q.target);
      const body = await readBody(req);
      const expr = body || q.expr || 'document.title';
      const resp = await sendCDP('Runtime.evaluate', {
        expression: expr,
        returnByValue: true,
        awaitPromise: true,
      }, sid);
      if (resp.result?.result?.value !== undefined) {
        res.end(JSON.stringify({ value: resp.result.result.value }));
      } else if (resp.result?.exceptionDetails) {
        res.statusCode = 400;
        res.end(JSON.stringify({ error: resp.result.exceptionDetails.text }));
      } else {
        res.end(JSON.stringify(resp.result));
      }
    }

    // POST /click?target=xxx - 点击（body 为 CSS 选择器）
    // POST /click?target=xxx — JS 层面点击（简单快速，覆盖大多数场景）
    else if (pathname === '/click') {
      const sid = await ensureSession(q.target);
      const selector = await readBody(req);
      if (!selector) {
        res.statusCode = 400;
        res.end(JSON.stringify({ error: 'POST body 需要 CSS 选择器' }));
        return;
      }
      const selectorJson = JSON.stringify(selector);
      const js = `(() => {
        const el = document.querySelector(${selectorJson});
        if (!el) return { error: '未找到元素: ' + ${selectorJson} };
        el.scrollIntoView({ block: 'center' });
        el.click();
        return { clicked: true, tag: el.tagName, text: (el.textContent || '').slice(0, 100) };
      })()`;
      const resp = await sendCDP('Runtime.evaluate', {
        expression: js,
        returnByValue: true,
        awaitPromise: true,
      }, sid);
      if (resp.result?.result?.value) {
        const val = resp.result.result.value;
        if (val.error) {
          res.statusCode = 400;
          res.end(JSON.stringify(val));
        } else {
          res.end(JSON.stringify(val));
        }
      } else {
        res.end(JSON.stringify(resp.result));
      }
    }

    // POST /clickAt?target=xxx — CDP 浏览器级真实鼠标点击（算用户手势，能触发文件对话框、绕过反自动化检测）
    else if (pathname === '/clickAt') {
      const sid = await ensureSession(q.target);
      const selector = await readBody(req);
      if (!selector) {
        res.statusCode = 400;
        res.end(JSON.stringify({ error: 'POST body 需要 CSS 选择器' }));
        return;
      }
      const selectorJson = JSON.stringify(selector);
      const js = `(() => {
        const el = document.querySelector(${selectorJson});
        if (!el) return { error: '未找到元素: ' + ${selectorJson} };
        el.scrollIntoView({ block: 'center' });
        const rect = el.getBoundingClientRect();
        return { x: rect.x + rect.width / 2, y: rect.y + rect.height / 2, tag: el.tagName, text: (el.textContent || '').slice(0, 100) };
      })()`;
      const coordResp = await sendCDP('Runtime.evaluate', {
        expression: js,
        returnByValue: true,
        awaitPromise: true,
      }, sid);
      const coord = coordResp.result?.result?.value;
      if (!coord || coord.error) {
        res.statusCode = 400;
        res.end(JSON.stringify(coord || coordResp.result));
        return;
      }
      await sendCDP('Input.dispatchMouseEvent', {
        type: 'mousePressed', x: coord.x, y: coord.y, button: 'left', clickCount: 1
      }, sid);
      await sendCDP('Input.dispatchMouseEvent', {
        type: 'mouseReleased', x: coord.x, y: coord.y, button: 'left', clickCount: 1
      }, sid);
      res.end(JSON.stringify({ clicked: true, x: coord.x, y: coord.y, tag: coord.tag, text: coord.text }));
    }

    // POST /setFiles?target=xxx — 给 file input 设置本地文件（绕过文件对话框）
    // body: JSON { "selector": "input[type=file]", "files": ["/path/to/file1.png", "/path/to/file2.png"] }
    else if (pathname === '/setFiles') {
      const sid = await ensureSession(q.target);
      const body = JSON.parse(await readBody(req));
      if (!body.selector || !body.files) {
        res.statusCode = 400;
        res.end(JSON.stringify({ error: '需要 selector 和 files 字段' }));
        return;
      }
      // 获取 DOM 节点
      await sendCDP('DOM.enable', {}, sid);
      const doc = await sendCDP('DOM.getDocument', {}, sid);
      const node = await sendCDP('DOM.querySelector', {
        nodeId: doc.result.root.nodeId,
        selector: body.selector
      }, sid);
      if (!node.result?.nodeId) {
        res.statusCode = 400;
        res.end(JSON.stringify({ error: '未找到元素: ' + body.selector }));
        return;
      }
      // 设置文件
      await sendCDP('DOM.setFileInputFiles', {
        nodeId: node.result.nodeId,
        files: body.files
      }, sid);
      res.end(JSON.stringify({ success: true, files: body.files.length }));
    }

    // GET /scroll?target=xxx&y=3000 - 滚动
    else if (pathname === '/scroll') {
      const sid = await ensureSession(q.target);
      const y = parseInt(q.y || '3000');
      const direction = q.direction || 'down'; // down | up | top | bottom
      let js;
      if (direction === 'top') {
        js = 'window.scrollTo(0, 0); "scrolled to top"';
      } else if (direction === 'bottom') {
        js = 'window.scrollTo(0, document.body.scrollHeight); "scrolled to bottom"';
      } else if (direction === 'up') {
        js = `window.scrollBy(0, -${Math.abs(y)}); "scrolled up ${Math.abs(y)}px"`;
      } else {
        js = `window.scrollBy(0, ${Math.abs(y)}); "scrolled down ${Math.abs(y)}px"`;
      }
      const resp = await sendCDP('Runtime.evaluate', {
        expression: js,
        returnByValue: true,
      }, sid);
      // 等待懒加载触发
      await new Promise(r => setTimeout(r, 800));
      res.end(JSON.stringify({ value: resp.result?.result?.value }));
    }

    // GET /screenshot?target=xxx&file=/tmp/x.png - 截图
    else if (pathname === '/screenshot') {
      const sid = await ensureSession(q.target);
      const format = q.format || 'png';
      const resp = await sendCDP('Page.captureScreenshot', {
        format,
        quality: format === 'jpeg' ? 80 : undefined,
      }, sid);
      if (q.file) {
        fs.writeFileSync(q.file, Buffer.from(resp.result.data, 'base64'));
        res.end(JSON.stringify({ saved: q.file }));
      } else {
        res.setHeader('Content-Type', 'image/' + format);
        res.end(Buffer.from(resp.result.data, 'base64'));
      }
    }

    // GET /info?target=xxx - 获取页面信息
    else if (pathname === '/info') {
      const sid = await ensureSession(q.target);
      const resp = await sendCDP('Runtime.evaluate', {
        expression: 'JSON.stringify({title: document.title, url: location.href, ready: document.readyState})',
        returnByValue: true,
      }, sid);
      res.end(resp.result?.result?.value || '{}');
    }

    // GET /aria-tree?target=xxx - 获取压缩的 Accessibility Tree
    else if (pathname === '/aria-tree') {
      const sid = await ensureSession(q.target);
      const tree = await getAriaTree(sid, q.target);
      const refCount = ariaRefs.get(q.target)?.size || 0;
      const result = { tree, refs: refCount };
      res.setHeader('Content-Type', 'text/plain; charset=utf-8');
      res.end(tree);
      return;
    }

    // POST /click-aria?target=xxx - 按 Aria 语义点击（body: {"role":"button","name":"下一页"}）
    else if (pathname === '/click-aria') {
      const sid = await ensureSession(q.target);
      const body = JSON.parse(await readBody(req));
      if (!body.role) {
        res.statusCode = 400;
        res.end(JSON.stringify({ error: '需要 role 字段' }));
        return;
      }

      // 如果没有缓存的 aria tree，先获取一次
      if (!ariaRefs.has(q.target)) {
        await getAriaTree(sid, q.target);
      }

      const node = findAriaNode(q.target, body.role, body.name || '');
      if (!node) {
        res.statusCode = 400;
        const result = { error: `未找到 Aria 节点: role=${body.role}, name=${body.name || '(any)'}` };
        res.end(JSON.stringify(result));
        return;
      }

      const objectId = await resolveNodeToObjectId(sid, node.backendDOMNodeId);
      const clickResp = await sendCDP('Runtime.callFunctionOn', {
        objectId,
        functionDeclaration: `function() {
          this.scrollIntoView({ block: 'center' });
          this.click();
          return { tag: this.tagName, text: (this.textContent || '').slice(0, 100) };
        }`,
        returnByValue: true,
        awaitPromise: true,
      }, sid);

      const val = clickResp.result?.result?.value || {};
      const result = { clicked: true, ref: node.refId, role: node.role, name: node.name, ...val };
      res.end(JSON.stringify(result));
    }

    // POST /type-aria?target=xxx - 按 Aria 语义输入文本（body: {"role":"textbox","name":"搜索","text":"hello"}）
    else if (pathname === '/type-aria') {
      const sid = await ensureSession(q.target);
      const body = JSON.parse(await readBody(req));
      if (!body.role || body.text === undefined) {
        res.statusCode = 400;
        res.end(JSON.stringify({ error: '需要 role 和 text 字段' }));
        return;
      }

      if (!ariaRefs.has(q.target)) {
        await getAriaTree(sid, q.target);
      }

      const node = findAriaNode(q.target, body.role, body.name || '');
      if (!node) {
        res.statusCode = 400;
        const result = { error: `未找到 Aria 节点: role=${body.role}, name=${body.name || '(any)'}` };
        res.end(JSON.stringify(result));
        return;
      }

      const objectId = await resolveNodeToObjectId(sid, node.backendDOMNodeId);

      // 聚焦 + 清空
      await sendCDP('Runtime.callFunctionOn', {
        objectId,
        functionDeclaration: `function() {
          this.scrollIntoView({ block: 'center' });
          this.focus();
          if ('value' in this) { this.value = ''; }
          else if (this.isContentEditable) { this.textContent = ''; }
          this.dispatchEvent(new Event('input', { bubbles: true }));
        }`,
        awaitPromise: true,
      }, sid);

      // 输入文本
      await sendCDP('Input.insertText', { text: body.text }, sid);

      // 触发 change 事件
      await sendCDP('Runtime.callFunctionOn', {
        objectId,
        functionDeclaration: `function() {
          this.dispatchEvent(new Event('input', { bubbles: true }));
          this.dispatchEvent(new Event('change', { bubbles: true }));
        }`,
        awaitPromise: true,
      }, sid);

      const result = { typed: true, ref: node.refId, role: node.role, name: node.name, text: body.text };
      res.end(JSON.stringify(result));
    }

    // GET /logs?logFile=xxx - 读取操作日志（NDJSON 格式）
    else if (pathname === '/logs' && req.method === 'GET') {
      const lf = q.logFile;
      try {
        if (lf && fs.existsSync(lf)) {
          const content = fs.readFileSync(lf, 'utf-8');
          const lines = content.trim().split('\n').filter(Boolean).map(l => JSON.parse(l));
          res.end(JSON.stringify(lines, null, 2));
        } else {
          res.end('[]');
        }
      } catch {
        res.end('[]');
      }
      return;
    }

    // DELETE /logs?logFile=xxx - 清空操作日志
    else if (pathname === '/logs' && req.method === 'DELETE') {
      const lf = q.logFile;
      try {
        if (lf) fs.writeFileSync(lf, '');
      } catch { /* ignore */ }
      res.end(JSON.stringify({ cleared: true }));
      return;
    }

    else {
      res.statusCode = 404;
      res.end(JSON.stringify({
        error: '未知端点',
        endpoints: {
          '/health': 'GET - 健康检查',
          '/targets': 'GET - 列出所有页面 tab',
          '/new?url=': 'GET - 创建新后台 tab（自动等待加载）',
          '/close?target=': 'GET - 关闭 tab',
          '/navigate?target=&url=': 'GET - 导航（自动等待加载）',
          '/back?target=': 'GET - 后退',
          '/info?target=': 'GET - 页面标题/URL/状态',
          '/eval?target=': 'POST body=JS表达式 - 执行 JS',
          '/click?target=': 'POST body=CSS选择器 - 点击元素',
          '/clickAt?target=': 'POST body=CSS选择器 - 真实鼠标点击',
          '/setFiles?target=': 'POST JSON {selector, files} - 文件上传',
          '/scroll?target=&y=&direction=': 'GET - 滚动页面',
          '/screenshot?target=&file=': 'GET - 截图',
          '/aria-tree?target=': 'GET - Accessibility Tree（压缩语义树）',
          '/click-aria?target=': 'POST JSON {role, name} - 按语义点击',
          '/type-aria?target=': 'POST JSON {role, name, text} - 按语义输入',
          '/logs': 'GET - 读取操作日志 / DELETE - 清空日志',
        },
      }));
    }

    // --- 记录操作日志（排除查询类接口）---
    if (!NO_LOG_PATHS.has(pathname) && pathname !== '/logs') {
      const params = { ...q };
      if (req.method === 'POST') params._body = '(see request)';
      await logOperation(logFile, req.method, pathname, params, 'ok', Date.now() - startTime);
    }

  } catch (e) {
    res.statusCode = 500;
    res.end(JSON.stringify({ error: e.message }));
    await logOperation(logFile, req.method, pathname, q, e, Date.now() - startTime);
  }
});

// 检查端口是否被占用
function checkPortAvailable(port) {
  return new Promise((resolve) => {
    const s = net.createServer();
    s.once('error', () => resolve(false));
    s.once('listening', () => { s.close(); resolve(true); });
    s.listen(port, '127.0.0.1');
  });
}

async function main() {
  // 检查是否已有 proxy 在运行
  const available = await checkPortAvailable(PORT);
  if (!available) {
    // 验证已有实例是否健康
    try {
      const ok = await new Promise((resolve) => {
        http.get(`http://127.0.0.1:${PORT}/health`, { timeout: 2000 }, (res) => {
          let d = '';
          res.on('data', c => d += c);
          res.on('end', () => resolve(d.includes('"ok"')));
        }).on('error', () => resolve(false));
      });
      if (ok) {
        console.log(`[CDP Proxy] 已有实例运行在端口 ${PORT}，退出`);
        process.exit(0);
      }
    } catch { /* 端口占用但非 proxy，继续报错 */ }
    console.error(`[CDP Proxy] 端口 ${PORT} 已被占用`);
    process.exit(1);
  }

  server.listen(PORT, '127.0.0.1', () => {
    console.log(`[CDP Proxy] 运行在 http://localhost:${PORT}`);
    // 启动时尝试连接 Chrome（非阻塞）
    connect().catch(e => console.error('[CDP Proxy] 初始连接失败:', e.message, '（将在首次请求时重试）'));
  });
}

// 防止未捕获异常导致进程崩溃
process.on('uncaughtException', (e) => {
  console.error('[CDP Proxy] 未捕获异常:', e.message);
});
process.on('unhandledRejection', (e) => {
  console.error('[CDP Proxy] 未处理拒绝:', e?.message || e);
});

main();
