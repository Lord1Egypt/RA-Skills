#!/usr/bin/env node
// apply.mjs — 确保 WorkBuddy 以调试模式运行，然后注入皮肤
import { readFileSync } from 'node:fs';
import { execSync, spawn } from 'node:child_process';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const PORT = 9223;
const ROOT = join(dirname(fileURLToPath(import.meta.url)), '..');

const sleep = ms => new Promise(r => setTimeout(r, ms));

async function cdpReady() {
  try {
    const list = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json();
    return list.find(t => t.type === 'page' && t.url.includes('renderer/index.html'));
  } catch { return null; }
}

function wbRunning() {
  try { execSync('pgrep -f "WorkBuddy.app/Contents/MacOS/Electron"', { stdio: 'pipe' }); return true; }
  catch { return false; }
}

function hasDebugFlag() {
  try {
    return execSync('ps -eo command | grep "WorkBuddy.app/Contents/MacOS/Electron" | grep -c "remote-debugging-port"', { stdio: 'pipe' }).toString().trim() !== '0';
  } catch { return false; }
}

async function ensureDebugMode() {
  if (await cdpReady()) return;
  if (wbRunning() && hasDebugFlag()) {
    // 已带调试端口（install-flag 引子），只是 renderer 还没起好——等，不要重启
    console.log('· WorkBuddy 启动中（调试端口已带），等待 renderer…');
    for (let i = 0; i < 40; i++) {
      await sleep(1000);
      if (await cdpReady()) return;
    }
    throw new Error('等待 renderer 超时');
  }
  if (wbRunning()) {
    console.log('· WorkBuddy 运行中但非调试模式，重启为调试模式…');
    try { execSync('osascript -e \'quit app "WorkBuddy"\''); } catch {}
    await sleep(3000);
    try { execSync('pkill -f "WorkBuddy.app"'); } catch {}
    await sleep(3000);
  }
  spawn('open', ['-a', 'WorkBuddy', '--args', `--remote-debugging-port=${PORT}`], { detached: true, stdio: 'ignore' }).unref();
  for (let i = 0; i < 30; i++) {
    await sleep(1000);
    if (await cdpReady()) return;
  }
  throw new Error('等待调试端口超时');
}

async function evaluate(page, expression) {
  const ws = new WebSocket(page.webSocketDebuggerUrl);
  await new Promise((res, rej) => { ws.onopen = res; ws.onerror = rej; });
  const result = await new Promise((resolve, reject) => {
    ws.onmessage = ev => { const m = JSON.parse(ev.data); if (m.id === 1) resolve(m); };
    ws.send(JSON.stringify({ id: 1, method: 'Runtime.evaluate', params: { expression, returnByValue: true } }));
    setTimeout(() => reject(new Error('evaluate timeout')), 15000);
  });
  ws.close();
  if (result.result?.exceptionDetails) throw new Error(result.result.exceptionDetails.text);
  return result.result?.result?.value;
}

async function main() {
  await ensureDebugMode();
  const page = await cdpReady();
  const css = readFileSync(join(ROOT, 'src/theme.css'), 'utf8');
  const bg = readFileSync(join(ROOT, 'assets/bg.jpg')).toString('base64');
  const themed = css.replace('/*__BG__*/"";/*__END__*/', () => JSON.stringify(`data:image/jpeg;base64,${bg}`));
  const muyuAudio = readFileSync(join(ROOT, 'assets/muyu.wav')).toString('base64');
  const mode = JSON.parse(readFileSync(join(ROOT, 'mode.json'), 'utf8')).mode || 'static';
  const payload = readFileSync(join(ROOT, 'src/inject.js'), 'utf8')
    .replace("/*__CSS__*/'';/*__END__*/", () => JSON.stringify(themed))
    .replace('/*__MODE__*/"static";/*__END__*/', () => JSON.stringify(mode))
    .replace("/*__VIDEO_URL__*/'';/*__END__*/", () => JSON.stringify('file://' + join(ROOT, 'assets/bg.mp4')))
    .replace('/*__MUYU_AUDIO__*/"";/*__END__*/', () => JSON.stringify(muyuAudio));
  const r = await evaluate(page, payload);
  console.log('✓ 皮肤已注入:', r);
  console.log('· 顶部日历条 + Arc 方块入口已生效；WorkBuddy 完全重启后需重新运行本脚本');
}
main().catch(e => { console.error('✗', e.message); process.exit(1); });
