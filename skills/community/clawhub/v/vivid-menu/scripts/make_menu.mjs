#!/usr/bin/env node
/* ============================================================
 * make_menu.mjs — 无头菜单生成器
 *
 * 把文字菜单 / JSON 菜单 / 内置示例，直接渲染成 SVG（可选 PNG），
 * 并输出质检报告。完全不依赖浏览器界面，供 Agent 在终端里调用。
 *
 * 用法示例见 SKILL.md。
 * ============================================================ */

import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { spawnSync } from 'node:child_process';
import { fileURLToPath, pathToFileURL } from 'node:url';

const HERE = path.dirname(fileURLToPath(import.meta.url));
const APP = path.resolve(HERE, '..', 'assets', 'app');

/* ---------------- 参数解析 ---------------- */

function parseArgs(argv) {
  const o = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (!a.startsWith('--')) { o._.push(a); continue; }
    const key = a.slice(2);
    const next = argv[i + 1];
    if (next === undefined || next.startsWith('--')) { o[key] = true; }
    else { o[key] = next; i++; }
  }
  return o;
}

const argv = parseArgs(process.argv.slice(2));
const die = (msg, code = 2) => { console.error('✗ ' + msg); process.exit(code); };

if (argv.help || argv.h) {
  console.log(`make_menu.mjs — 无头菜单生成器

输入（三选一）
  --text <file|->        文字菜单：每行一道菜，可带【分节】标题
  --json <file>          菜单 JSON（结构见 references/data-model.md）
  --demo <0|1|2>         内置示例（0 川味小馆 / 1 夜灯小食堂 / 2 山间茶事）

菜单信息
  --name <店名>          --subtitle <副标题>
  --footer <页脚说明>    --seal <印章二字>
  --theme <id>           见 --themes

输出
  --out <file.svg>       默认 ./menu.svg
  --png [file.png]       另存 PNG（自动找 Edge/Chrome 无头渲染，2 倍分辨率）
  --report <file.json>   质检报告落盘
  --preview <file.html>  生成可直接双击查看的 HTML

行为
  --no-fix               关闭自动修复，只看原始质检结果
  --allow-errors         有 error 也返回退出码 0
  --themes               列出可用配色主题
  --quiet                只输出结果路径
`);
  process.exit(0);
}

if (!fs.existsSync(APP)) die(`找不到应用资产目录：${APP}`);

/* ---------------- 载入应用模块 ---------------- */

const M = await import(pathToFileURL(path.join(APP, 'js', 'model.js')).href);
const R = await import(pathToFileURL(path.join(APP, 'js', 'render.js')).href);
const I = await import(pathToFileURL(path.join(APP, 'js', 'inspect.js')).href);
const P = await import(pathToFileURL(path.join(APP, 'js', 'parse.js')).href);
const D = await import(pathToFileURL(path.join(APP, 'js', 'driver.js')).href);
const S = await import(pathToFileURL(path.join(APP, 'js', 'store.js')).href);
const T = await import(pathToFileURL(path.join(APP, 'js', 'protocol.js')).href);

const { blankMenu, THEME_LIST, THEMES } = M;

if (argv.themes) {
  for (const t of THEME_LIST) console.log(`${t.id.padEnd(8)} ${t.label}   纸 ${t.paper}  墨 ${t.ink}  点缀 ${t.accent}`);
  process.exit(0);
}

/* ---------------- 组装菜单 ---------------- */

async function fromText(text) {
  let menu = blankMenu({ name: '' });
  const ctx = {
    getMenu: () => menu,
    setMenu: (m) => { menu = m; },
    getSource: () => ({ text, dataUrl: '', width: 0, height: 0 }),
    pushEvent: () => {},
    takeEvent: () => null,
    cropSource: async () => ({ dataUrl: '', width: 0, height: 0 }),
  };
  const toolset = T.createToolset(ctx);
  const res = await D.runLocal(ctx, toolset, { pace: 0 });
  if (!res.ok) die(res.error + '\n  提示：' + (res.hint || ''), 3);
  return { menu, parsed: res, source: 'text' };
}

function fromJson(file) {
  let raw;
  try { raw = JSON.parse(fs.readFileSync(file, 'utf8')); }
  catch (e) { die(`JSON 读取失败：${e.message}`); }
  const list = Array.isArray(raw) ? raw : raw.dishes;
  if (!Array.isArray(list)) die('JSON 需要是数组，或含 dishes 数组的对象');
  const menu = blankMenu({
    name: raw.name || raw.shopName || '',
    name_original: raw.name_original || '',
    subtitle: raw.subtitle || '',
    footer: raw.footer || '',
    seal: raw.seal || '',
    theme: raw.theme || 'rice',
    dishes: list.map((d) => M.blankDish(d)),
  });
  return { menu, source: 'json' };
}

let built;
if (argv.json) {
  built = fromJson(String(argv.json));
} else if (argv.demo !== undefined) {
  const idx = Number(argv.demo) || 0;
  const preset = S.PRESETS[idx];
  if (!preset) die(`没有第 ${idx} 个示例（共 ${S.PRESETS.length} 个）`);
  built = { menu: structuredClone(preset), source: 'demo' };
} else if (argv.text) {
  const file = String(argv.text);
  const text = file === '-' ? fs.readFileSync(0, 'utf8') : fs.readFileSync(file, 'utf8');
  built = await fromText(text);
} else {
  die('缺少输入。用 --text / --json / --demo 指定，或 --help 看完整用法。');
}

let menu = built.menu;

/* ---------------- 覆盖菜单信息 ---------------- */

if (argv.theme) {
  if (!THEMES[argv.theme]) die(`未知配色「${argv.theme}」，可用：${Object.keys(THEMES).join(' / ')}`);
  menu.theme = argv.theme;
}
for (const [flag, field] of [['name', 'name'], ['subtitle', 'subtitle'], ['footer', 'footer'], ['seal', 'seal']]) {
  if (typeof argv[flag] === 'string') menu[field] = argv[flag];
}
if (!menu.name) menu.name = '未命名小馆';
if (!menu.seal && !argv.seal) menu.seal = menu.name.replace(/[·\s].*$/, '').slice(0, 2);

/* ---------------- 自动修复 + 质检 ---------------- */

const before = I.inspectMenu(menu);
let fixLog = built.parsed?.fixed || [];
if (!argv['no-fix']) {
  const fixed = D.autoFix(menu);
  menu = fixed.menu;
  fixLog = [...new Set([...fixLog, ...fixed.log])];
}
const report = I.inspectMenu(menu);

/* ---------------- 渲染 ---------------- */

const { svg, layout } = R.renderMenu(menu, { hitAreas: false });

const outFile = path.resolve(String(argv.out || 'menu.svg'));
fs.mkdirSync(path.dirname(outFile), { recursive: true });
fs.writeFileSync(outFile, svg, 'utf8');

/* ---------------- PNG ---------------- */

const BROWSERS = [
  'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',
  'C:/Program Files/Microsoft/Edge/Application/msedge.exe',
  'C:/Program Files/Google/Chrome/Application/chrome.exe',
  'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe',
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
  '/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser', '/usr/bin/microsoft-edge',
];
const findBrowser = () => BROWSERS.find((p) => { try { return fs.statSync(p).isFile(); } catch { return false; } })
  || ['google-chrome', 'chromium', 'chromium-browser', 'microsoft-edge', 'msedge']
    .find((cmd) => spawnSync(cmd, ['--version']).status === 0);

function toPng(pngPath, scale = 2) {
  const browser = findBrowser();
  if (!browser) return { ok: false, reason: '未找到 Edge / Chrome，PNG 导出跳过（SVG 仍可用）' };

  const W = layout.width;
  const H = Math.ceil(layout.height);
  const html = `<!doctype html><meta charset="utf-8">
<style>html,body{margin:0;padding:0;background:#fff}svg{display:block;width:${W}px;height:${H}px}</style>
${svg}`;
  const tmpHtml = path.join(os.tmpdir(), `vm-${Date.now()}.html`);
  fs.writeFileSync(tmpHtml, html, 'utf8');
  const profile = path.join(os.tmpdir(), `vm-prof-${Date.now()}`);
  fs.mkdirSync(pngPath ? path.dirname(pngPath) : '.', { recursive: true });

  spawnSync(browser, [
    '--headless=new', '--disable-gpu', '--no-sandbox', '--no-first-run',
    '--hide-scrollbars', '--disable-extensions',
    `--force-device-scale-factor=${scale}`,
    `--user-data-dir=${profile}`,
    `--screenshot=${pngPath}`,
    `--window-size=${W},${H}`,
    pathToFileURL(tmpHtml).href,
  ], { timeout: 90000, stdio: 'ignore' });

  // 无头浏览器落盘有延迟，轮询等待
  for (let i = 0; i < 40; i++) {
    if (fs.existsSync(pngPath) && fs.statSync(pngPath).size > 2048) {
      try { fs.rmSync(profile, { recursive: true, force: true }); } catch {}
      try { fs.unlinkSync(tmpHtml); } catch {}
      return { ok: true, path: pngPath };
    }
    spawnSync(process.execPath, ['-e', 'setTimeout(()=>{},150)']);
  }
  return { ok: false, reason: '浏览器未产出 PNG 文件' };
}

let pngResult = null;
if (argv.png) {
  const pngPath = typeof argv.png === 'string'
    ? path.resolve(argv.png)
    : outFile.replace(/\.svg$/i, '') + '.png';
  pngResult = toPng(pngPath, Number(argv.scale) || 2);
}

/* ---------------- 预览 HTML ---------------- */

if (argv.preview) {
  const p = path.resolve(String(argv.preview));
  fs.mkdirSync(path.dirname(p), { recursive: true });
  fs.writeFileSync(p, `<!doctype html><meta charset="utf-8">
<title>${menu.name}</title>
<style>body{margin:0;padding:32px;background:#151310;display:flex;justify-content:center}
svg{max-width:100%;height:auto;box-shadow:0 20px 60px rgba(0,0,0,.6)}</style>
${svg}`, 'utf8');
}

/* ---------------- 报告 ---------------- */

const reportPath = argv.report ? path.resolve(String(argv.report)) : null;
if (reportPath) {
  fs.mkdirSync(path.dirname(reportPath), { recursive: true });
  fs.writeFileSync(reportPath, JSON.stringify({
    shop: menu.name, theme: menu.theme,
    dishes: menu.dishes.length,
    height: report.metrics.height,
    ...report,
    autoFixed: fixLog,
  }, null, 2), 'utf8');
}

if (!argv.quiet) {
  const st = M.stats(menu);
  console.log(`\n${menu.name}　${THEMES[menu.theme].label}　${st.count} 道菜 / ${st.sections.length} 分节 / ${st.signatureCount} 招牌`);
  console.log(`版面 ${layout.width}×${Math.round(layout.height)}　纸墨对比度 ${report.metrics.contrast}:1`);
  console.log(`质检 ${report.errors} error / ${report.warns} warn`);
  for (const i of report.issues) {
    const tag = i.level === 'error' ? '✗' : '!';
    console.log(`  ${tag} [${i.code}] ${i.msg}`);
  }
  if (fixLog.length) console.log(`自动修复 ${fixLog.length} 项：${fixLog.join('；')}`);
  console.log(`\n→ ${outFile}`);
  if (pngResult?.ok) console.log(`→ ${pngResult.path}`);
  if (pngResult && !pngResult.ok) console.log(`  (${pngResult.reason})`);
  if (reportPath) console.log(`→ ${reportPath}`);
  if (argv.preview) console.log(`→ ${path.resolve(String(argv.preview))}`);
}

if (report.errors > 0 && !argv['allow-errors']) process.exit(1);
