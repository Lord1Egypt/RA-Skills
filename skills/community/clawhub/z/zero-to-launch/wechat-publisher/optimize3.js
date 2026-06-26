import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const filePath = path.join(__dirname, '..', 'blog-post-wechat.html');
let html = fs.readFileSync(filePath, 'utf-8');
let totalSaved = 0;

// 1. Pain card <p> 标签: margin:10px 0 0;font-size:15px;color:#6B6880;line-height:1.75
// 可以去掉 line-height:1.75 (接近外层的 1.85，差别不大)
const b1 = html.length;
html = html.replace(
  /(<p style="margin:10px 0 0;font-size:15px;color:#6B6880;)line-height:1\.75;(")/g,
  '$1$2'
);
totalSaved += b1 - html.length;
console.log(`pain card line-height: saved ${b1 - html.length}`);

// 2. 去掉 pain card 中的 background:#fff (白色背景是默认值)
// pattern: background:#fff;border:1px solid
const b2 = html.length;
html = html.replace(
  /<div style="background:#fff;border:1px solid #E8E6F0/g,
  '<div style="border:1px solid #E8E6F0'
);
totalSaved += b2 - html.length;
console.log(`card bg:#fff: saved ${b2 - html.length}`);

// 3. 去掉 table cell 中 background:#FAFAFF → 这是浅色交替行，不能省
// 但 table header 的 border:1px solid #1B1642 在深色背景上根本看不到，可以去掉
const b3 = html.length;
html = html.replace(
  /;border:1px solid #1B1642"/g,
  '"'
);
totalSaved += b3 - html.length;
console.log(`table header border: saved ${b3 - html.length}`);

// 4. border:1px solid #6B7280 也类似
const b4 = html.length;
html = html.replace(/;border:1px solid #6B7280"/g, '"');
totalSaved += b4 - html.length;
console.log(`table grey border: saved ${b4 - html.length}`);

// 5. border:1px solid #5B4CDB 同理
const b5 = html.length;
html = html.replace(/;border:1px solid #5B4CDB"/g, '"');
totalSaved += b5 - html.length;
console.log(`table purple border: saved ${b5 - html.length}`);

// 6. 精简 padding:12px 14px → padding:12px 14px (已经最简了)
// 但可以简化成 padding:12px 14px (已经是了)

// 7. 进化流程中的 margin:3px 可以省掉 (不太影响)
const b7 = html.length;
html = html.replace(/;margin:3px"/g, '"');
html = html.replace(/;margin:0 4px"/g, '"');
totalSaved += b7 - html.length;
console.log(`evolution margins: saved ${b7 - html.length}`);

// 8. 精简 border-radius:8px → br:8px (不行，微信不认缩写)
// 无法精简

// 9. 去掉 footer div 中不必要的样式
// 10. 去掉 text-align:center 在小的元素上的冗余声明? 不行，这些是必要的

console.log(`\nTotal saved: ${totalSaved}`);
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
