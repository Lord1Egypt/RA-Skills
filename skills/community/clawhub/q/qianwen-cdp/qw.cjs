'use strict';
/**
 * qw.cjs — 千问浏览器原生 CDP 驱动（绕过 agent-browser 的 --cdp 限制）
 *
 * 关键结论（已验证）：
 *   千问对已存在的页面 target 做外部 CDP 调用会静默/挂死，但用 browser 级 WS
 *   调 Target.createTarget 自己新建的页面 target 完全可控（Runtime/DOM/Input 均可用）。
 *   因此本工具一律「自建新 tab」来驱动，登录态由真实 profile 保留。
 *
 * 用法：
 *   node qw.cjs check                       诊断：9666 是否就绪 / 千问是否在跑 / 主进程是否带端口
 *   node qw.cjs ensure                      确保 CDP 可用：9666 在就直接连（不起实例）；不在则提示用 launch 或自行打开
 *   node qw.cjs launch                      仅在明确需要时起实例：先优雅关在跑的千问，再起带 9666 的（避免单例冲突）
 *   node qw.cjs open <url>                  新建 tab 并导航，输出 targetId
 *   node qw.cjs navigate <id> <url>         已有 tab 导航
 *   node qw.cjs eval <id> <js表达式>        执行 JS，输出返回值
 *   node qw.cjs snapshot <id> [selector]    取页面简化快照（文本/链接/输入）
 *   node qw.cjs click <id> <css选择器>      点击元素
 *   node qw.cjs type <id> <css选择器> <文本> 向输入框填入文本
 *   node qw.cjs screenshot <id> [out.png]   截图
 *   node qw.cjs list                        列出当前所有 target
 *   node qw.cjs close <id>                  关闭 tab
 */

const http = require('http');
const fs = require('fs');
const os = require('os');
const path = require('path');

const HOME = os.homedir(); // e.g. C:\Users\<用户名>
// ws 依赖：环境变量 QW_WS_PATH 优先，其次常见安装位置（xbrowser 技能 / OpenClaw tools）
const WS_CANDIDATES = [
  process.env.QW_WS_PATH,
  path.join(HOME, '.workbuddy', 'skills', 'xbrowser', 'scripts', 'src', 'node_modules', 'ws'),
  path.join(HOME, '.openclaw', 'tools', 'xbrowser', 'node_modules', 'ws'),
].filter(Boolean);
let WebSocket = null;
for (const p of WS_CANDIDATES) {
  try { WebSocket = require(p); break; } catch (e) { /* try next */ }
}
if (!WebSocket) {
  console.error('[qw] 找不到 ws 模块（已尝试：' + WS_CANDIDATES.join(' ; ') + '）');
  console.error('     安装含 ws 依赖的环境，或设置环境变量 QW_WS_PATH 指向 ws 模块目录后重试。');
  process.exit(1);
}

const QW_EXE = process.env.QW_EXE || path.join(HOME, 'AppData', 'Local', 'Programs', 'QianwenApp', 'qianwen.exe');
const QW_PROFILE = process.env.QW_PROFILE || path.join(HOME, 'AppData', 'Local', 'Qianwen', 'User Data');
const CDP_PORT = Number(process.env.QW_CDP_PORT) || 9666;
const PROBE_TIMEOUT = 12000;

// ---------------------------------------------------------------------------
function httpGet(path) {
  return new Promise((resolve, reject) => {
    const req = http.get({ host: '127.0.0.1', port: CDP_PORT, path, timeout: 4000 }, (res) => {
      let d = '';
      res.on('data', (c) => (d += c));
      res.on('end', () => { try { resolve(JSON.parse(d)); } catch (e) { reject(e); } });
    });
    req.on('error', reject);
    req.on('timeout', () => { req.destroy(); reject(new Error('http timeout ' + path)); });
  });
}

function newWs(url) {
  return new Promise((resolve, reject) => {
    const ws = new WebSocket(url);
    ws.on('open', () => resolve(ws));
    ws.on('error', reject);
  });
}

// 在指定 ws 上发 CDP 命令并等待结果
function cdp(ws, method, params = {}, timeout = 10000) {
  return new Promise((resolve, reject) => {
    const id = Math.floor(Math.random() * 1e9);
    const timer = setTimeout(() => { ws.removeListener('message', onMsg); reject(new Error('cdp timeout: ' + method)); }, timeout);
    const onMsg = (raw) => {
      let m; try { m = JSON.parse(raw); } catch { return; }
      if (m.id === id) { clearTimeout(timer); ws.removeListener('message', onMsg); resolve(m); }
    };
    ws.on('message', onMsg);
    ws.send(JSON.stringify({ id, method, params }));
  });
}

// 同 cdp，但返回 m.result（多数 CDP 命令的结果都嵌在 result 里）
function cdpR(ws, method, params = {}, timeout = 10000) {
  return cdp(ws, method, params, timeout).then((m) => m.result);
}

async function getBrowserWs() {
  const ver = await httpGet('/json/version');
  return newWs(ver.webSocketDebuggerUrl);
}

async function getTargetWs(targetId) {
  const list = await httpGet('/json/list');
  const t = list.find((x) => x.id === targetId);
  if (!t || !t.webSocketDebuggerUrl) throw new Error('找不到 target ' + targetId + ' 的 ws');
  return newWs(t.webSocketDebuggerUrl);
}

// ---------------------------------------------------------------------------
// 诊断当前状态：9666 是否已就绪 + 千问进程是否在跑 + 主进程是否带端口
async function checkStatus() {
  let cdpUp = false;
  try { await httpGet('/json/version'); cdpUp = true; } catch {}

  let qianwenRunning = false;
  let qianwenCount = 0;
  try {
    const out = require('child_process').execSync('tasklist /fi "IMAGENAME eq qianwen.exe"', { encoding: 'utf8' });
    qianwenCount = out.split('\n').filter((l) => l.includes('qianwen.exe')).length;
    qianwenRunning = qianwenCount > 0;
  } catch {}

  // 注：不再用 wmic（Win11 已移除）检测主进程命令行是否带端口——
  // cdpUp 已足够决策；若 9666 在监听即说明端口生效。
  return { cdpUp, qianwenRunning, qianwenCount };
}

// 确保千问 CDP 在跑 —— 关键纪律：先检查，已有就直接连，绝不复读/复起第二个实例
//   · 9666 已在监听 → 直接连（老板日常千问自带端口，最常见情况）
//   · 9666 没在     → 不再 spawn 裸实例（会与单例冲突、占窗口、刷回收站）
//                     改由 boss 自己从快捷方式/菜单/自启动打开（入口都是 9666），或显式调 `launch`
async function ensureInstance() {
  try {
    await httpGet('/json/version');
    return { ok: true, alreadyUp: true, note: '检测到 9666 已在监听（老板日常千问自带端口），直接连接，未起任何实例' };
  } catch {
    return {
      ok: false,
      alreadyUp: false,
      needLaunch: true,
      note: '9666 未监听。禁止 spawn 第二个实例。请老板从自带 9666 的快捷方式/菜单/自启动打开千问，或显式执行 `launch`。',
    };
  }
}

// 仅在明确需要时才用的「启动」命令：先优雅关掉在跑的千问（避免单例冲突），再起一个带 9666 的实例
async function launchInstance() {
  // 先优雅关闭任何在跑的千问（单例机制：不关掉新实例起不来）
  try { require('child_process').execSync('taskkill /IM qianwen.exe', { stdio: 'ignore', timeout: 10000 }); } catch {}
  await new Promise((r) => setTimeout(r, 3000));

  const { spawn } = require('child_process');
  const child = spawn(QW_EXE, [
    '--remote-debugging-port=' + CDP_PORT,
    '--user-data-dir=' + QW_PROFILE,
    '--no-first-run', '--no-default-browser-check',
  ], { detached: true, stdio: 'ignore' });
  child.unref();

  const deadline = Date.now() + PROBE_TIMEOUT;
  while (Date.now() < deadline) {
    try { await httpGet('/json/version'); return { ok: true, launched: true }; }
    catch { await new Promise((r) => setTimeout(r, 500)); }
  }
  throw new Error('launch 后 CDP 未在 ' + PROBE_TIMEOUT + 'ms 内就绪');
}

// 新建 tab 并导航，返回 targetId
async function openTab(url) {
  const bws = await getBrowserWs();
  const { targetId } = await cdpR(bws, 'Target.createTarget', { url });
  bws.close();
  // 等待加载
  await new Promise((r) => setTimeout(r, 2500));
  return targetId;
}

async function navigate(targetId, url) {
  const tws = await getTargetWs(targetId);
  await cdp(tws, 'Page.enable');
  await cdp(tws, 'Page.navigate', { url });
  tws.close();
  await new Promise((r) => setTimeout(r, 2500));
}

async function evalJS(targetId, expr) {
  const tws = await getTargetWs(targetId);
  await cdp(tws, 'Runtime.enable');
  const r = await cdpR(tws, 'Runtime.evaluate', { expression: expr, returnByValue: true });
  tws.close();
  return r;
}

// 简化快照：标题 + 可见文本片段 + 链接 + 输入框
async function snapshot(targetId, selector) {
  const tws = await getTargetWs(targetId);
  await cdp(tws, 'Runtime.enable');
  const expr = `
  (function(){
    var root = ${selector ? `document.querySelector(${JSON.stringify(selector)})` : 'document.body'};
    if(!root) return {error:'no element'};
    var text = (root.innerText||'').replace(/\\s+/g,' ').trim().slice(0,2000);
    var links = [].slice.call(root.querySelectorAll('a')).slice(0,30).map(function(a){return {t:a.innerText.trim().slice(0,60), h:a.href};});
    var inputs = [].slice.call(root.querySelectorAll('input,textarea')).slice(0,20).map(function(i){return {type:i.type||i.tagName, name:i.name||i.id, placeholder:i.placeholder||'', value:i.value||''};});
    return {title:document.title, text:text, links:links, inputs:inputs};
  })()`;
  const r = await cdp(tws, 'Runtime.evaluate', { expression: expr, returnByValue: true });
  tws.close();
  return r.result;
}

async function click(targetId, selector) {
  const tws = await getTargetWs(targetId);
  await cdp(tws, 'Runtime.enable');
  const expr = `
  (function(){
    var el = document.querySelector(${JSON.stringify(selector)});
    if(!el) return {ok:false, error:'no element '+${JSON.stringify(selector)}};
    el.scrollIntoView({block:'center'});
    var r = el.getBoundingClientRect();
    return {ok:true, x:r.x+r.width/2, y:r.y+r.height/2};
  })()`;
  const r = await cdpR(tws, 'Runtime.evaluate', { expression: expr, returnByValue: true });
  tws.close();
  if (!r || !r.value || !r.value.ok) return r;
  const { x, y } = r.value;
  // 用 Input 域点击坐标（需重连开启 Input）
  const tws2 = await getTargetWs(targetId);
  await cdp(tws2, 'Input.enable');
  await cdp(tws2, 'Input.dispatchMouseEvent', { type: 'mousePressed', x, y, button: 'left', clickCount: 1 });
  await cdp(tws2, 'Input.dispatchMouseEvent', { type: 'mouseReleased', x, y, button: 'left', clickCount: 1 });
  tws2.close();
  await new Promise((res) => setTimeout(res, 800));
  return { ok: true, x, y };
}

async function typeText(targetId, selector, text) {
  const tws = await getTargetWs(targetId);
  await cdp(tws, 'Runtime.enable');
  const focusExpr = `
  (function(){
    var el = document.querySelector(${JSON.stringify(selector)});
    if(!el) return {ok:false};
    el.focus(); el.value=''; return {ok:true};
  })()`;
  await cdp(tws, 'Runtime.evaluate', { expression: focusExpr, returnByValue: true });
  tws.close();
  const tws2 = await getTargetWs(targetId);
  await cdp(tws2, 'Input.enable');
  for (const ch of text) {
    await cdp(tws2, 'Input.insertText', { text: ch });
  }
  tws2.close();
  await new Promise((res) => setTimeout(res, 300));
  return { ok: true };
}

async function screenshot(targetId, out) {
  const tws = await getTargetWs(targetId);
  await cdp(tws, 'Page.enable');
  const r = await cdpR(tws, 'Page.captureScreenshot', { format: 'png', captureBeyondViewport: true });
  tws.close();
  const data = r.data;
  const file = out || ('C:/tmp/qw_shot_' + targetId + '.png');
  fs.writeFileSync(file, Buffer.from(data, 'base64'));
  return { ok: true, file };
}

async function listTargets() {
  return httpGet('/json/list');
}

async function closeTab(targetId) {
  const bws = await getBrowserWs();
  await cdp(bws, 'Target.closeTarget', { targetId });
  bws.close();
  return { ok: true };
}

// ---------------------------------------------------------------------------
async function main() {
  const [cmd, ...args] = process.argv.slice(2);
  let out;
  switch (cmd) {
    case 'check': out = await checkStatus(); break;
    case 'ensure': out = await ensureInstance(); break;
    case 'launch':
      // 仅在 9666 未就绪且确认要起时才用；会先优雅关闭在跑的千问避免单例冲突
      try { await httpGet('/json/version'); out = { ok: true, alreadyUp: true, note: '9666 已在，无需 launch' }; }
      catch { out = await launchInstance(); }
      break;
    case 'relaunch':
      // 优雅关闭（不发 /F），让 Chromium 正常退出清理 DB/缓存，避免脏文件丢回收站
      try { require('child_process').execSync('taskkill /IM qianwen.exe', { stdio: 'ignore', timeout: 10000 }); } catch {}
      await new Promise((r) => setTimeout(r, 3000));
      out = await ensureInstance();
      break;
    case 'open': out = { targetId: await openTab(args[0]) }; break;
    case 'navigate': await navigate(args[0], args[1]); out = { ok: true }; break;
    case 'eval': out = await evalJS(args[0], args.slice(1).join(' ')); break;
    case 'snapshot': out = await snapshot(args[0], args[1]); break;
    case 'click': out = await click(args[0], args[1]); break;
    case 'type': out = await typeText(args[0], args[1], args.slice(2).join(' ')); break;
    case 'screenshot': out = await screenshot(args[0], args[1]); break;
    case 'list': out = await listTargets(); break;
    case 'close': out = await closeTab(args[0]); break;
    default: out = { error: 'unknown command: ' + cmd }; break;
  }
  console.log(JSON.stringify(out, null, 2));
}

main().catch((e) => { console.error('ERR', e.message || e); process.exit(1); });
