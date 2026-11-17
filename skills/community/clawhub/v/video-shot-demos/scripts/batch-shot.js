#!/usr/bin/env node
/* batch-shot.js —— 整辑批量无头截图（第 2 步工具化，shot.js 的批量包装）
   解决缺口⑥前半：质检仅单页单点截图。底层逐次调用 scripts/shot.js（原单页单点功能不动）。
   用法:
     node scripts/batch-shot.js <目录> [--times 25,50,75,95] [--out _shots] [--only 关键词] [--limit N] [--keep-failed]
   默认对目录内全部 shot-*.html（排除 index/_backup/.bak）按 DUR 百分比取 4 个节拍点截图。
   --times 可改为绝对毫秒列表（如 3000,8000）。输出 <目录>/<out>/页面名@毫秒.png。
   汇总成功/失败；失败多为：页面缺 __startPlayback 底盘、DUR 缺失、浏览器未找到（设 BROWSER_PATH）。 */
const fs = require('fs'), path = require('path'), { spawnSync } = require('child_process');
const SHOT_JS = path.join(__dirname, 'shot.js');

function die(m) { console.error('✗ ' + m); process.exit(1); }
const argv = process.argv.slice(2);
const VAL_OPTS = ['times', 'out', 'only', 'limit'];
const dirArg = (() => { for (let i = 0; i < argv.length; i++) { if (!argv[i].startsWith('--')) return argv[i]; if (VAL_OPTS.includes(argv[i].slice(2))) i++; } return null; })();
const opt = k => { const i = argv.indexOf('--' + k); return i >= 0 ? argv[i + 1] : null; };

const dir = path.resolve(dirArg);
if (!fs.existsSync(dir) || !fs.statSync(dir).isDirectory()) die('目录不存在: ' + dir);
const only = opt('only'), limit = opt('limit') ? +opt('limit') : Infinity;
const outRaw = opt('out') || '_shots';
const outDir = path.isAbsolute(outRaw) ? outRaw : path.resolve(dir, outRaw);   // 绝对路径时输出到目录外（如 temp）
fs.mkdirSync(outDir, { recursive: true });

const pages = fs.readdirSync(dir)
  .filter(f => /^shot-.*\.html$/i.test(f) && !/_backup|\.bak/i.test(f))
  .filter(f => !only || f.includes(only))
  .sort();
if (!pages.length) die('目录内没有匹配的 shot-*.html 页面');
const todo = pages.slice(0, limit);
console.log(`批量截图: ${todo.length}/${pages.length} 页 × 节拍点 → ${outDir}\n`);

let okN = 0, failN = 0; const fails = [];
for (const page of todo) {
  const src = fs.readFileSync(path.join(dir, page), 'utf8');
  const dm = src.match(/const\s+DUR\s*=\s*(\d+)/);
  if (!dm) { console.log(`  ✗ ${page}: 缺 DUR 定义，跳过`); fails.push(page + '(无DUR)'); failN++; continue; }
  const DUR = +dm[1];
  let tms;
  const t = opt('times') || '25,50,75,95';
  if (/^\d+(,\d+)+$/.test(t) && t.split(',').every(x => +x > 1000)) tms = t.split(',').map(Number);         // 绝对毫秒
  else tms = t.split(',').map(p => Math.round(DUR * (+p) / 100));                                            // 百分比
  for (const ms of tms) {
    const png = path.join(outDir, page.replace(/\.html$/i, '') + '@' + ms + '.png');
    const r = spawnSync(process.execPath, [SHOT_JS, page, String(ms), png], { cwd: dir, encoding: 'utf8' });
    if (r.status === 0 && fs.existsSync(png)) { okN++; console.log(`  ✓ ${page} @${ms}ms (${(100 * ms / DUR).toFixed(0)}%)`); }
    else { failN++; const why = (r.stderr || r.stdout || '').split('\n').filter(Boolean).pop() || '未知错误'; console.log(`  ✗ ${page} @${ms}ms: ${why}`); fails.push(`${page}@${ms}`); }
  }
}
console.log(`\n===== 完成: 成功 ${okN} / 失败 ${failN} =====`);
if (fails.length) { console.log('失败清单:'); fails.forEach(f => console.log('  - ' + f)); process.exit(1); }
