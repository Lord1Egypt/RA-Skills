#!/usr/bin/env node
/* gen-index.js —— index 总览页自动生成（第 3 步工具化）
   解决缺口⑦：index 卡片信息可从文件名 + <title> + DUR + shot-meta 风格标签自动汇总。
   用法:
     node scripts/gen-index.js <目录> [--title "辑名"] [--subtitle "副题"] [--out index.html]
   提取规则:
     - 页面: shot-*.html（排除 _backup/.bak 与旧 index）
     - 编号: 文件名 shot-(\d+-\d+[a-z]?)_；标题: <title> 中 「·」 之后部分（缺省用文件名）
     - 时长: const DUR= 毫秒 → 秒；风格: <!-- shot-meta style="..." -->（无则显示 —）
     - 分章: 按编号第一段数字（00/01/02…），章名可 --chapters "00=引子,02=实测" 覆盖
   已存在 index.html 时自动备份为 index.backup.<时间戳>.html（版本规范见 SKILL.md）。 */
const fs = require('fs'), path = require('path');

function die(m) { console.error('✗ ' + m); process.exit(1); }
const argv = process.argv.slice(2);
const VAL_OPTS = ['title', 'subtitle', 'out', 'chapters'];
const dirArg = (() => { for (let i = 0; i < argv.length; i++) { if (!argv[i].startsWith('--')) return argv[i]; if (VAL_OPTS.includes(argv[i].slice(2))) i++; } return null; })();
if (!dirArg) die('用法: node scripts/gen-index.js <目录> [--title 辑名] [--chapters "00=引子,01=基准"]');
const opt = k => { const i = argv.indexOf('--' + k); return i >= 0 ? argv[i + 1] : null; };
const dir = path.resolve(dirArg);
if (!fs.existsSync(dir)) die('目录不存在: ' + dir);

const title = opt('title') || path.basename(dir);
const subtitle = opt('subtitle') || 'video-shot-demos 自动总览';
const chapMap = {};
if (opt('chapters')) for (const kv of opt('chapters').split(',')) { const [k, v] = kv.split('='); if (k && v) chapMap[k.trim()] = v.trim(); }

const pages = fs.readdirSync(dir).filter(f => /^shot-.*\.html$/i.test(f) && !/_backup|\.bak/i.test(f)).sort();
if (!pages.length) die('目录内没有 shot-*.html');

const cards = pages.map(f => {
  const src = fs.readFileSync(path.join(dir, f), 'utf8');
  const id = (f.match(/^shot-(\d+-\d+[a-z]?)_/i) || [, '?'])[1];
  const tm = src.match(/<title>([^<]*)<\/title>/);
  let name = tm ? tm[1].split('·').pop().trim() : f.replace(/^shot-[\da-z-]+_/i, '').replace(/\.html$/i, '');
  const dm = src.match(/const\s+DUR\s*=\s*(\d+)/);
  const dur = dm ? Math.round(+dm[1] / 1000) : null;
  const sm = src.match(/<!--\s*shot-meta\s+style="([^"]+)"/);
  return { file: f, id, name, dur, style: sm ? sm[1] : null, chap: id.split('-')[0].padStart(2, '0') };
});

const total = cards.reduce((s, c) => s + (c.dur || 0), 0);
const styleN = new Set(cards.filter(c => c.style).map(c => c.style)).size;
const chapOrder = [...new Set(cards.map(c => c.chap))].sort();
const mm = Math.floor(total / 60), ss = String(total % 60).padStart(2, '0');

const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/"/g, '&quot;');
let body = '';
for (const ch of chapOrder) {
  const list = cards.filter(c => c.chap === ch);
  const cDur = list.reduce((s, c) => s + (c.dur || 0), 0);
  body += `<section class="chap"><div class="chapHead"><span class="cNo">第 ${ch} 章</span><h2>${esc(chapMap[ch] || '')}</h2><span class="cTime">${Math.floor(cDur / 60)}:${String(cDur % 60).padStart(2, '0')}</span></div><div class="grid">\n`;
  for (const c of list) {
    body += `  <a class="card" href="./${encodeURIComponent(c.file)}"><span class="cNo">${esc(c.id)}</span><span class="cDur">${c.dur !== null ? c.dur + 's' : '?'}</span><div class="cTitle">${esc(c.name)}</div><div class="cStyle">${esc(c.style || '—')}</div><svg class="cPlay" viewBox="0 0 24 24" width="26" height="26"><path d="M8 5v14l11-7z" fill="currentColor"/></svg></a>\n`;
  }
  body += `</div></section>\n`;
}

const html = `<!DOCTYPE html><html lang="zh-CN"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>${esc(title)} · 分镜总览</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Noto+Serif+SC:wght@600;900&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#efe8d5;font-family:'Noto Serif SC',serif;color:#2c2a26;padding:44px 5vw 70px}
.wrap{max-width:1180px;margin:0 auto}
.kicker{font-family:'Share Tech Mono';letter-spacing:6px;font-size:13px;color:#8a8272}
h1{font-family:'Playfair Display','Noto Serif SC';font-size:52px;letter-spacing:2px;margin:10px 0 4px}
.stamp{display:inline-block;transform:rotate(-6deg);border:3px solid #b53929;color:#b53929;font-weight:900;border-radius:8px;padding:4px 14px;font-size:15px;letter-spacing:3px;margin-left:14px;vertical-align:middle}
.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:26px 0 8px}
.stats div{background:#fffdf4;border:2px solid #2c2a26;border-radius:12px;padding:14px 10px;text-align:center;box-shadow:6px 6px 0 rgba(44,42,38,.15)}
.stats b{display:block;font-family:'Playfair Display';font-size:30px}
.stats span{font-size:13px;color:#6b6355}
.note{font-family:'Share Tech Mono';font-size:12px;color:#8a8272;margin:14px 0 30px;letter-spacing:1px}
.chap{margin-bottom:34px}
.chapHead{display:flex;align-items:baseline;gap:14px;border-bottom:3px double #2c2a26;padding-bottom:8px;margin-bottom:16px}
.chapHead .cNo{font-family:'Share Tech Mono';color:#b53929;letter-spacing:2px}
.chapHead h2{font-size:22px;flex:1}
.chapHead .cTime{font-family:'Share Tech Mono';color:#8a8272}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px}
.card{position:relative;display:block;background:#fffdf4;border:2px solid #2c2a26;border-radius:14px;padding:16px 16px 14px;text-decoration:none;color:#2c2a26;box-shadow:6px 6px 0 rgba(44,42,38,.14);transition:transform .18s,box-shadow .18s}
.card:hover{transform:translate(-2px,-3px);box-shadow:10px 12px 0 rgba(44,42,38,.2)}
.card .cNo{font-family:'Share Tech Mono';color:#b53929;font-size:14px;letter-spacing:2px}
.card .cDur{float:right;font-family:'Share Tech Mono';font-size:13px;color:#8a8272}
.card .cTitle{font-weight:900;font-size:19px;margin:8px 0 6px;line-height:1.35}
.card .cStyle{font-size:12px;color:#6b6355;border-top:1px dashed #c9c0ab;padding-top:7px}
.card .cPlay{position:absolute;right:12px;bottom:12px;color:#b53929;opacity:.55}
footer{margin-top:44px;text-align:center;font-family:'Share Tech Mono';font-size:12px;color:#8a8272;letter-spacing:2px}
</style></head><body><div class="wrap">
<div class="kicker">SHOT INDEX / ${cards.length} PAGES</div>
<h1>${esc(title)}<span class="stamp">分镜总览</span></h1>
<div class="stats"><div><b>${cards.length}</b><span>镜头</span></div><div><b>${mm}:${ss}</b><span>总时长</span></div><div><b>${styleN}</b><span>风格(去重)</span></div><div><b>${chapOrder.length}</b><span>章节</span></div></div>
<div class="note">subtitle: ${esc(subtitle)} ｜ generated by scripts/gen-index.js ｜ 点击卡片逐页打开</div>
${body}<footer>video-shot-demos · auto-generated index</footer></div></body></html>`;

const outPath = path.join(dir, opt('out') || 'index.html');
if (fs.existsSync(outPath)) {
  const bak = outPath.replace(/\.html$/i, '') + '.backup.' + new Date().toISOString().replace(/[-:T]/g, '').slice(0, 14) + '.html';
  fs.copyFileSync(outPath, bak);
  console.log('已备份旧 index → ' + path.basename(bak));
}
fs.writeFileSync(outPath, html, 'utf8');
console.log(`已生成: ${outPath}`);
console.log(`汇总: ${cards.length} 页 / 总时长 ${mm}:${ss} / 风格 ${styleN} 种 / ${chapOrder.length} 章`);
const miss = cards.filter(c => !c.style || c.dur === null);
if (miss.length) console.log(`提示: ${miss.length} 页缺 shot-meta 风格或 DUR（卡片显示 — / ?）: ${miss.map(c => c.file).join('、')}`);
