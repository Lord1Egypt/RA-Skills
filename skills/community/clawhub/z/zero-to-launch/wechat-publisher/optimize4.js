import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const filePath = path.join(__dirname, '..', 'blog-post-wechat.html');
let html = fs.readFileSync(filePath, 'utf-8');

// table header cells: background:#1B1642;border:1px solid #1B1642
// border 在深色背景上看不到，可以删掉
// 同理 background:#6B7280;border:1px solid #6B7280 和 #5B4CDB
const b1 = html.length;
html = html.replace(/background:#1B1642;border:1px solid #1B1642;/g, 'background:#1B1642;');
html = html.replace(/background:#6B7280;color:#fff;font-weight:600;border:1px solid #6B7280/g, 'background:#6B7280;color:#fff;font-weight:600');
html = html.replace(/background:#5B4CDB;color:#fff;font-weight:600;border:1px solid #5B4CDB/g, 'background:#5B4CDB;color:#fff;font-weight:600');
console.log(`table header borders: saved ${b1 - html.length}`);

// letter-spacing:0.5px on hero title - 可以省掉
const b2 = html.length;
html = html.replace(/;letter-spacing:0\.5px/g, '');
console.log(`letter-spacing: saved ${b2 - html.length}`);

// margin-bottom:20px on Product Sense Coach badge -> margin-bottom:20px
// 这个必要，保留

// vertical-align:middle 出现很多次 -> 可以省（影响对齐但不影响可读性）
// 实际上不能省，编号球的对齐需要这个

// text-align:center 在编号球上也是必须的

// 最终手段：去掉 footer 的一些样式
const b3 = html.length;
html = html.replace(
  /<div style="background:#fff;border:1px solid #E8E6F0;border-radius:8px;padding:24px 28px;margin-top:8px;text-align:center;color:#6B6880;font-size:14px;line-height:2;">/,
  '<div style="border:1px solid #E8E6F0;border-radius:8px;padding:24px 28px;margin-top:8px;text-align:center;color:#6B6880;font-size:14px;line-height:2;">'
);
console.log(`footer bg: saved ${b3 - html.length}`);

fs.writeFileSync(filePath, html, 'utf-8');

// Quick test
const startM = '<!-- ========== ARTICLE CONTENT START ========== -->';
const endM = '<!-- ========== ARTICLE CONTENT END ========== -->';
let c = html.substring(html.indexOf(startM) + startM.length, html.indexOf(endM));
c = c.replace(/<!--[\s\S]*?-->/g, '').trim();
let ch = true;
while (ch) {
  ch = false;
  const m = c.match(/^\s*<div(?:\s+(?:class|id)="[^"]*")*\s*>\s*([\s\S]*)\s*<\/div>\s*$/);
  if (m && !c.match(/^\s*<div[^>]*style=/)) {
    const t = c.match(/^\s*<div[^>]*>/);
    if (t && !t[0].includes('style=')) { c = m[1].trim(); ch = true; }
  }
}
let r = c;
r = r.replace(/font-family\s*:[^;"]*(?:'[^']*'[^;"]*|"[^"]*"[^;"]*)*;?/g, '');
r = r.replace(/\s+id="[^"]*"/g, '');
r = r.replace(/\s+class="[^"]*"/g, '');
r = r.replace(/rgba\(255,\s*255,\s*255,\s*0\.12\)/g, '#FFFFFF1F');
r = r.replace(/rgba\(255,\s*255,\s*255,\s*0\.2\)/g, '#FFFFFF33');
r = r.replace(/rgba\(255,\s*255,\s*255,\s*0\.8\)/g, '#FFFFFFCC');
r = r.replace(/rgba\(255,\s*255,\s*255,\s*0\.55\)/g, '#FFFFFF8C');
r = r.replace(/rgba\(0,\s*0,\s*0,\s*[\d.]+\)/g, '#00000026');
r = r.replace(/max-width\s*:\s*578px/g, 'width:100%');
r = r.replace(/position\s*:\s*[^;]+;?/g, '');
r = r.replace(/z-index\s*:\s*[^;]+;?/g, '');
r = r.replace(/;color:#2D2A3E(?=[";}])/g, '');
r = r.replace(/color:#2D2A3E;/g, '');
r = r.replace(/;\s*;/g, ';');
r = r.replace(/style=";\s*/g, 'style="');
r = r.replace(/;\s*"/g, '"');
r = r.replace(/style="\s*"/g, '');
let comp = r.replace(/<!--[\s\S]*?-->/g, '').replace(/>\s+</g, '><').replace(/\s{2,}/g, ' ').trim();
console.log('\n字符数:', comp.length);
if (comp.length > 20000) console.log(`⚠️  还差 ${comp.length - 20000}`);
else console.log(`✅ 在限制内！余量 ${20000 - comp.length}`);
