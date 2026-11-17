#!/usr/bin/env node
/* lint.js —— 交付前整辑 lint 质检（SKILL.md「交付标准」脚本化）
   解决缺口⑥后半：角色出场/相邻风格/实体锁色/DUR 与最后 cue 越界等人工易漏项。
   用法:
     node scripts/lint.js <目录> [--plan plan.json] [--json 报告.json]
   检查项（每页）:
     A DUR 存在且 3~180s 合理区间
     B cue 越界: on(毫秒) > DUR+2500 → FAIL；DUR<ms<=DUR+2500 → WARN（底盘尾帧宽限）
     C 角色出场（启发式）: 引用 anan/shery 立绘 png 的次数 ≥ 阈值（DUR<10s 短页=1，其余=2；>100s 超长页建议 3，不足 WARN）
     D 相邻风格: 读 </head> 前的 <!-- shot-meta style="..." --> 注释比对相邻页（无 meta 的页标记跳过）
     E 实体锁色: --plan 时按 plan.locks 检查——正文提到实体名的页应出现其锁定 hex（忽略大小写）
     F Google Fonts link 存在;  G emoji 检查（\u{1F300}-\u{1FAFF} 等出现在正文 → WARN，应换内联 SVG）
   退出码: 存在 FAIL=1。骨架未实现的页面被标 FAIL 属预期（提示哪些页还没做）。 */
const fs = require('fs'), path = require('path');
const argv = process.argv.slice(2);
const VAL_OPTS = ['plan', 'json'];
const dirArg = (() => { for (let i = 0; i < argv.length; i++) { if (!argv[i].startsWith('--')) return argv[i]; if (VAL_OPTS.includes(argv[i].slice(2))) i++; } return null; })();
if (!dirArg) die('用法: node scripts/lint.js <目录> [--plan plan.json] [--json 报告.json]');
const opt = k => { const i = argv.indexOf('--' + k); return i >= 0 ? argv[i + 1] : null; };
function die(m) { console.error('✗ ' + m); process.exit(1); }

const dir = path.resolve(dirArg);
if (!fs.existsSync(dir)) die('目录不存在: ' + dir);
let plan = null;
if (opt('plan')) {
  try { plan = JSON.parse(fs.readFileSync(path.resolve(opt('plan')), 'utf8')); }
  catch (e) { die('plan.json 读取失败: ' + e.message); }
}
const locks = (plan && plan.locks) || [];

const pages = fs.readdirSync(dir).filter(f => /^shot-.*\.html$/i.test(f) && !/_backup|\.bak/i.test(f)).sort();
if (!pages.length) die('目录内没有 shot-*.html');

const EMOJI_RE = /[\u{1F300}-\u{1FAFF}\u{2600}-\u{27BF}\u{FE0F}]/u;
const report = { dir, checked: pages.length, pages: [] };
let hasFail = false, metaMissing = 0;

pages.forEach((f, idx) => {
  const src = fs.readFileSync(path.join(dir, f), 'utf8');
  const F = [], W = [], I = [];
  const dm = src.match(/const\s+DUR\s*=\s*(\d+)/);
  const DUR = dm ? +dm[1] : null;
  // A DUR
  if (DUR === null) F.push('A 未找到 const DUR 定义');
  else {
    if (DUR < 3000 || DUR > 180000) W.push(`A DUR=${(DUR / 1000).toFixed(1)}s 超常见区间 3~180s`);
    if (DUR > 100000) W.push('A 超长页(>100s)：角色建议 3 次出场');
  }
  // B cue 越界
  let last = 0, over = 0;
  for (const m of src.matchAll(/^on\((\d+)\s*,/gm)) { const t = +m[1]; last = Math.max(last, t); if (DUR !== null && t > DUR) over++; }
  if (DUR !== null && last > DUR + 2500) F.push(`B 最后 cue ${last}ms 超出 DUR+2500=${DUR + 2500}ms（${over} 条越界）`);
  else if (DUR !== null && last > DUR) W.push(`B ${over} 条 cue 落在 DUR~DUR+2500 尾帧宽限区内`);
  else if (last) I.push(`B 最后 cue ${last}ms ≤ DUR ✓`);
  // C 角色出场（启发式：img 立绘引用数 与 on(...classList.add('show')) cue 数取较大者≈出场次数）
  const ananImg = (src.match(/anan - emotion rename\/[^"')]+\.png/g) || []).length;
  const sheryImg = (src.match(/shery - emotion rename\/[^"')]+\.png/g) || []).length;
  const showCue = (src.match(/on\(\d+[^)]*\)[^;\n]*\$\(['"]#(anan|shery)['"]\)[^;\n]*classList\.add\(['"]show['"]\)/g) || []);
  const ananCue = showCue.filter(s => s.includes('#anan')).length, sheryCue = showCue.length - ananCue;
  const ananN = Math.max(ananImg, ananCue), sheryN = Math.max(sheryImg, sheryCue);
  const shortPage = DUR !== null && DUR < 10000;
  const need = shortPage ? 1 : 2;
  if (DUR !== null && DUR > 100000 && ananN + sheryN < 3) W.push(`C 超长页角色出场 ${ananN} 次 <3`);
  else if (ananN + sheryN === 0) F.push(`C 角色完全未出场（img=${ananImg}+${sheryImg}, show-cue=${ananCue}+${sheryCue}）——骨架未实现或漏配`);
  else if (ananN + sheryN < need) W.push(`C 角色出场 ${ananN}+${sheryN} < ${need} 次${shortPage ? '（短页仅需结尾 1 次）' : '（中段快闪+结尾定场，SKILL 理想值）'}`);
  else I.push(`C 角色出场: anan×${ananN} shery×${sheryN} ≥${need} ✓`);
  // D 相邻风格（shot-meta）
  const meta = src.match(/<!--\s*shot-meta\s+style="([^"]+)"/);
  const prev = idx > 0 ? pages[idx - 1] : null;
  const prevSrc = prev ? fs.readFileSync(path.join(dir, prev), 'utf8') : '';
  const prevMeta = prevSrc.match(/<!--\s*shot-meta\s+style="([^"]+)"/);
  if (!meta) { W.push('D 缺 <!-- shot-meta style="..." --> 注释（init.js 骨架自带；改风格时须同步改）'); metaMissing++; }
  else if (prevMeta && prevMeta[1] === meta[1]) F.push(`D 与上一页 ${prev} 相邻同风格「${meta[1]}」`);
  else if (meta && prevMeta) I.push(`D 相邻风格不同 ✓ (${meta[1]})`);
  // E 实体锁色
  for (const l of locks) {
    if (!src.includes(l.entity)) continue;
    const hexes = [...new Set((src.match(/#[0-9a-fA-F]{6}\b/g) || []).map(h => h.toLowerCase()))];
    if (!hexes.includes(l.color.toLowerCase())) F.push(`E 提到「${l.entity}」但未出现锁色 ${l.color}（实体色跨页漂移）`);
    else I.push(`E ${l.entity} 锁色 ${l.color} ✓`);
  }
  // F 字体 / G emoji（剔除注释后粗查）
  const noComment = src.replace(/<!--[\s\S]*?-->/g, '').replace(/\/\*[\s\S]*?\*\//g, '').replace(/\/\/[^\n]*/g, '');
  if (!/fonts\.googleapis\.com/.test(src)) W.push('F 缺 Google Fonts link（本地字族整页会回退）');
  const em = noComment.match(EMOJI_RE);
  if (em) W.push(`G 检出 emoji「${em[0]}」→ 按 SKILL 反模式应换内联扁平 SVG`);
  if (F.length) hasFail = true;
  report.pages.push({ file: f, dur: DUR, lastCue: last, style: meta ? meta[1] : null, fail: F, warn: W, info: I });
});

// 汇总输出
let fN = 0, wN = 0, iN = 0;
console.log(`\n===== lint 报告: ${dir}（${pages.length} 页）=====`);
for (const p of report.pages) {
  fN += p.fail.length; wN += p.warn.length; iN += p.info.length;
  const tag = p.fail.length ? 'FAIL' : (p.warn.length ? 'WARN' : 'PASS');
  const durS = p.dur !== null ? (p.dur / 1000).toFixed(1) + 's' : '?';
  console.log(`\n[${tag}] ${p.file}  DUR=${durS}  风格=${p.style || '—'}`);
  p.fail.forEach(m => console.log('  ✗ ' + m));
  p.warn.forEach(m => console.log('  ⚠ ' + m));
  if (tag !== 'PASS') p.info.forEach(m => console.log('  ✓ ' + m));
}
const styles = report.pages.filter(p => p.style).map(p => p.style);
const dup = styles.filter((s, i) => styles.indexOf(s) !== i);
if (dup.length) console.log(`\n⚠ 整辑重复风格: ${[...new Set(dup)].join('、')}`);
else if (styles.length === pages.length) console.log('\n✓ 整辑风格零重复');
console.log(`\n===== 小计: ${report.checked} 页 / FAIL ${fN} / WARN ${wN} / 通过项 ${iN} =====`);
if (opt('json')) { const jp = path.resolve(opt('json')); fs.writeFileSync(jp, JSON.stringify(report, null, 2), 'utf8'); console.log('JSON 报告: ' + jp); }
if (metaMissing) console.log(`提示: ${metaMissing} 页缺 shot-meta（相邻风格校验跳过；补注释或用 init.js 重新生成）`);
process.exit(hasFail ? 1 : 0);
