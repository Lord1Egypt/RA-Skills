#!/usr/bin/env node
/* init.js —— 项目初始化脚手架（第 0 步工具化）
   解决缺口①③：无项目初始化脚本、素材资产不稳定（空目录/路径漂移/缺 cp 前校验）。
   功能：建输出目录 → 校验并复制角色立绘/图标素材 → 按 plan.json 批量生成带命名与 shot-meta 的 shot 骨架。
   用法:
     node scripts/init.js <plan.json> --root <输出根目录> [--anan-source glm-5.3-range-test] [--force]
   plan.json 由 plan.js new 生成。骨架 = template.html 副本，已替换 title/DUR/HUD 行，
   并在 </head> 前注入 <!-- shot-meta style="..." chapter="..." -->（lint.js / gen-index.js 依赖该注释）。
   素材校验失败默认中止并列出缺失清单；--force 可跳过素材复制继续生成骨架（不推荐）。 */
const fs = require('fs'), path = require('path');
const SKILL = path.resolve(__dirname, '..');
const DB = JSON.parse(fs.readFileSync(path.join(__dirname, 'styles.json'), 'utf8'));

function die(msg) { console.error('✗ ' + msg); process.exit(1); }
function copyDir(src, dst) {
  fs.mkdirSync(dst, { recursive: true });
  let n = 0;
  for (const f of fs.readdirSync(src)) {
    const s = path.join(src, f), d = path.join(dst, f);
    const st = fs.statSync(s);
    if (st.isDirectory()) n += copyDir(s, d);
    else { fs.copyFileSync(s, d); n++; }
  }
  return n;
}
function safeName(t) { return String(t).replace(/[\\/:*?"<>|\s]+/g, '').slice(0, 24) || '未命名'; }

/* ---------- 参数 ---------- */
const args = process.argv.slice(2);
const VAL_OPTS = ['root', 'anan-source'];
const opt = k => { const i = args.indexOf('--' + k); return i >= 0 ? args[i + 1] : null; };
const planPath = (() => { for (let i = 0; i < args.length; i++) { if (!args[i].startsWith('--')) return args[i]; if (VAL_OPTS.includes(args[i].slice(2))) i++; } return null; })();
if (!planPath) die('用法: node scripts/init.js <plan.json> --root <输出根目录> [--anan-source ...] [--force]');
const root = opt('root');
if (!root) die('缺少 --root <输出根目录>');
const FORCE = args.includes('--force');

let plan;
try { plan = JSON.parse(fs.readFileSync(path.resolve(planPath), 'utf8')); }
catch (e) { die('plan.json 读取/解析失败: ' + e.message); }
if (!plan.project || !Array.isArray(plan.assign) || !plan.assign.length) die('plan.json 缺少 project 或 assign（请先用 plan.js new 生成）');
const ananSource = opt('anan-source') || plan.ananSource || 'glm-5.3-range-test';

/* ---------- 1. 建输出目录 ---------- */
const outDir = path.resolve(root, plan.project);
if (fs.existsSync(outDir)) {
  const exist = fs.readdirSync(outDir);
  if (exist.some(f => /^shot-.*\.html$/.test(f)) && !FORCE) die(`输出目录已存在且含 shot 页面: ${outDir}\n  如需追加/覆盖请加 --force（已有同名文件会被跳过，不会覆盖）`);
}
fs.mkdirSync(outDir, { recursive: true });
console.log(`项目目录: ${outDir}`);

/* ---------- 2. 素材校验 + 复制（缺口①：cp 前校验） ---------- */
const ananSrc = path.join(SKILL, 'assets', 'examples', ananSource, 'anan - emotion rename');
const sherySrc = path.join(SKILL, 'assets', 'shery - emotion rename');
const iconsSrc = path.join(SKILL, 'assets', 'examples', ananSource, 'icons');
let assetsOK = true;

const check = (label, dir, min, expect) => {
  if (!fs.existsSync(dir)) { console.error(`  ✗ [素材] ${label} 目录不存在: ${dir}`); assetsOK = false; return; }
  const pngs = fs.readdirSync(dir).filter(f => /\.png$/i.test(f));
  if (pngs.length < min) { console.error(`  ✗ [素材] ${label} 仅 ${pngs.length} 张 PNG（期望 ${expect}）: ${dir}`); assetsOK = false; return; }
  if (pngs.length !== expect) console.warn(`  ⚠ [素材] ${label} ${pngs.length} 张（期望 ${expect}），数量不一致但已达下限`);
  const n = copyDir(dir, path.join(outDir, path.basename(dir)));
  console.log(`  ✓ ${label}: 复制 ${n} 个文件 → ${path.basename(dir)}/`);
};
console.log('素材校验与复制:');
check('安安立绘(anan)', ananSrc, 15, 15);
check('橘雪莉立绘(shery)', sherySrc, 20, 20);
if (fs.existsSync(iconsSrc)) { const n = copyDir(iconsSrc, path.join(outDir, 'icons')); console.log(`  ✓ 项目图标: 复制 ${n} 个文件 → icons/`); }
else console.warn('  ⚠ [素材] icons 目录不存在，跳过（本辑不需要图标时可忽略）');

if (!assetsOK && !FORCE) {
  console.error('\n素材校验未通过，已中止（骨架未生成）。排查后重跑，或 --force 跳过素材继续。');
  process.exit(1);
}

/* ---------- 3. 生成骨架 ---------- */
const tpl = fs.readFileSync(path.join(SKILL, 'assets', 'template.html'), 'utf8');
const dupShots = [];
const created = [];
for (const a of plan.assign) {
  const fname = `shot-${a.id}_${safeName(a.title)}.html`;
  const fpath = path.join(outDir, fname);
  if (fs.existsSync(fpath)) { dupShots.push(fname); continue; }
  const chap = String(a.id).split('-')[0].padStart(2, '0');
  let html = tpl;
  html = html.replace('<title>镜头 X-X · 【改成镜头标题】</title>', `<title>镜头 ${a.id} · ${a.title}</title>`);
  html = html.replace(/const DUR=\d+;/, `const DUR=${Math.round(a.dur * 1000)};`);
  html = html.replace('<span>镜头 X-X · 标题 · 12s</span>', `<span>镜头 ${a.id} · ${a.title} · ${a.dur}s</span>`);
  html = html.replace('<div class="corner" id="chap">0X / 章节名</div>', `<div class="corner" id="chap">${chap} / ${plan.project}</div>`);
  html = html.replace('</head>', `<!-- shot-meta style="${a.style}" chapter="${chap}" fonts="${a.fonts}" palette="${a.palette}" -->\n</head>`);
  html = html.replace(/<span class="no">SHOT X-X<\/span>/, `<span class="no">SHOT ${a.id}</span>`);
  fs.writeFileSync(fpath, html, 'utf8');
  created.push({ fname, style: a.style });
}
console.log(`\n骨架生成: 新建 ${created.length} 个 shot 页面${dupShots.length ? `，跳过已存在 ${dupShots.length} 个: ${dupShots.join('、')}` : ''}`);
console.log('风格分配(来自 plan.json):');
for (const c of created) console.log(`  ${c.fname}  →  ${c.style}`);
console.log(`\n下一步:\n  cd "${outDir}"\n  逐页打开骨架，按 shot-meta 注释与 SKILL.md 第 1 步改标记区\n  质检: node "${path.join(SKILL, 'scripts', 'lint.js')}" "${outDir}" --plan "${path.resolve(planPath)}"`);
