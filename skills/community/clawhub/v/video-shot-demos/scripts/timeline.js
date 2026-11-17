#!/usr/bin/env node
/* timeline.js —— 口播时间戳 ⇄ cue 毫秒 换算与校验（第 1 步配套工具）
   解决缺口⑤：口播时间戳→cue 毫秒换算无工具易错位。
   用法:
     node scripts/timeline.js calc <口播起始> <口播结束>     # 例: calc 5:01 5:06 → 输出 5000ms
     node scripts/timeline.js table <页面.html> [--base m:ss] # 列出全部 cue 与口播注释对照表
   时间格式支持 m:ss / mm:ss / h:mm:ss（成片口播时间轴）。
   table 模式逐行扫描 on(毫秒,...) 与行尾 // m:ss「口播句」注释：
     - 带 --base（本镜头口播起始，如 5:01）时校验: (注释时间戳 - base) 是否等于 cue 毫秒（±300ms 容差）
     - 无注释的 cue 标记 [无口播注释]，提示补齐；无 --base 时仅输出对照表不校验。 */
const fs = require('fs'), path = require('path');

function die(msg) { console.error('✗ ' + msg); process.exit(1); }
function parseTs(s) {
  const m = String(s || '').trim().match(/^(\d{1,2}):(\d{1,2})(?::(\d{1,2}))?$/);
  if (!m) return null;
  if (m[3] !== undefined) return (+m[1]) * 3600000 + (+m[2]) * 60000 + (+m[3]) * 1000;  // h:mm:ss
  return (+m[1]) * 60000 + (+m[2]) * 1000;                                            // m:ss
}
function fmtMs(ms) { return (ms / 1000).toFixed(2).replace(/\.?0+$/, '') + 's'; }

const [, , cmd, arg] = process.argv;
const argv = process.argv.slice(2);
const opt = k => { const i = argv.indexOf('--' + k); return i >= 0 ? argv[i + 1] : null; };

if (cmd === 'calc') {
  const [, , , a, b] = process.argv;
  const ta = parseTs(a), tb = parseTs(b);
  if (ta === null || tb === null) die('时间格式应为 m:ss 或 h:mm:ss，如 5:06 或 1:02:03');
  const d = tb - ta;
  console.log(`${a} → ${b}: 差值 ${d}ms（${fmtMs(d)}）`);
  console.log(`cue 写法: on(${d}, ...);   // ${b}「口播句」`);
  process.exit(d < 0 ? 1 : 0);
}

if (cmd === 'table') {
  if (!arg) die('用法: node scripts/timeline.js table <页面.html> [--base m:ss]');
  const f = path.resolve(arg);
  if (!fs.existsSync(f)) die('文件不存在: ' + f);
  const baseRaw = opt('base');
  const base = baseRaw ? parseTs(baseRaw) : null;
  if (baseRaw && base === null) die('--base 时间格式应为 m:ss 或 h:mm:ss');
  const src = fs.readFileSync(f, 'utf8');
  const durM = src.match(/const\s+DUR\s*=\s*(\d+)/);
  const DUR = durM ? +durM[1] : null;
  const lines = src.split(/\r?\n/);
  const rows = []; let lastCue = 0;
  lines.forEach((ln, i) => {
    const t = ln.trim().match(/^on\((\d+)\s*,/);
    if (!t) return;
    const ms = +t[1]; lastCue = Math.max(lastCue, ms);
    const cm = ln.match(/\/\/\s*(\d{1,2}:\d{2}(?::\d{2})?)/);
    rows.push({ line: i + 1, ms, note: cm ? cm[1] : null });
  });
  console.log(`\n===== cue 对照表: ${path.basename(f)}${DUR !== null ? `（DUR=${DUR}ms=${fmtMs(DUR)}）` : '（未找到 DUR!）'} =====`);
  if (base !== null) console.log(`口播基准 --base ${baseRaw} = ${base}ms`);
  let ok = 0, off = 0, noNote = 0;
  for (const r of rows) {
    let mark, extra = '';
    if (r.note && base !== null) {
      const nts = parseTs(r.note), expect = nts - base, dev = r.ms - expect;
      if (Math.abs(dev) <= 300) { mark = '✓'; ok++; }
      else { mark = '±'; off++; extra = ` 偏差 ${dev > 0 ? '+' : ''}${dev}ms（注释应落在 ${(expect / 1000).toFixed(1)}s）`; }
    } else if (r.note) { mark = '·'; ok++; }
    else { mark = '?'; noNote++; }
    const over = DUR !== null && r.ms > DUR ? '  [越界>DUR]' : '';
    console.log(`  ${mark} L${String(r.line).padStart(4)}  on(${r.ms}) = ${fmtMs(r.ms)}  ${r.note ? '// ' + r.note : '[无口播注释]'}${over}${extra}`);
  }
  console.log(`\n小计: ${rows.length} 条 cue / 对齐 ${ok} / 偏差 ${off} / 缺注释 ${noNote}${DUR !== null ? ` / 最后 cue ${fmtMs(lastCue)}（DUR ${fmtMs(DUR)}，${lastCue > DUR ? '越界!' : 'OK'}）` : ''}`);
  if (noNote) console.log('提示: 关键叙事 cue 应带 // m:ss「口播句」注释（SKILL.md 音画同步标准）');
  process.exit(off > 0 ? 1 : 0);
}

console.log('用法:\n  node scripts/timeline.js calc <口播起始> <口播结束>      换算毫秒\n  node scripts/timeline.js table <页面.html> [--base m:ss]  cue/口播对照与校验');
