import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const filePath = path.join(__dirname, '..', 'blog-post-wechat.html');
let html = fs.readFileSync(filePath, 'utf-8');

let totalSaved = 0;

// 1. Pain card 中的 <p> 也有冗余样式 (margin:10px 0 0;font-size:15px;color:#6B6880;line-height:1.75)
// font-size 和 line-height 是必要的（不同于默认值），但可以缩短写法
// 保留不动，这些是必要的

// 2. 场景模板中大量的 &nbsp; 换成用 padding-left
// <span style="color:#5B4CDB;font-weight:600;">谁</span>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
// 这些 &nbsp; 每组有 6 个 = 30 字符，改成 margin-left 写法
// 但这改动比较大，先跳过

// 3. 精简 table cell 中重复的 padding:12px 14px
// 没有好办法，因为微信不支持 <style>

// 4. 精简 question list 4个 div 的重复样式
const questionStyle = 'background:#fff;border:1px solid #E8E6F0;border-radius:8px;padding:14px 18px;margin:8px 0;font-size:15px;line-height:1.75;color:#2D2A3E;';
// color:#2D2A3E 可继承，font-size:15px 和 line-height:1.75 不能省（和默认值不同）
// 去掉 color 可以省一些
const before = html.length;
html = html.replace(
  /(<div style="background:#fff;border:1px solid #E8E6F0;border-radius:8px;padding:14px 18px;margin:8px 0;font-size:15px;line-height:1\.75;)color:#2D2A3E;(")/g,
  '$1$2'
);
console.log(`question list color removal: saved ${before - html.length} chars`);
totalSaved += before - html.length;

// 5. 精简编号球样式 - 3种大小的编号球有大量重复
// 小球: display:inline-block;background:#5B4CDB;color:#fff;font-size:11px;font-weight:700;width:20px;height:20px;line-height:20px;text-align:center;border-radius:6px;margin-right:8px;vertical-align:middle
// 中球: display:inline-block;background:#5B4CDB;color:#fff;font-size:12px;font-weight:700;width:22px;height:22px;line-height:22px;text-align:center;border-radius:6px;margin-right:8px;vertical-align:middle
// 大球: display:inline-block;background:#5B4CDB;color:#fff;font-size:13px;font-weight:700;width:28px;height:28px;line-height:28px;text-align:center;border-radius:8px;margin-right:10px;vertical-align:middle
// 这些没法精简，每种的 size 不同

// 6. 精简 section 标题中重复的完整样式
// font-size:20px;font-weight:700;color:#1B1642;margin-top:48px;margin-bottom:16px;padding-left:14px;border-left:4px solid #5B4CDB
// 出现 6 次，但微信不支持 class，只能内联
// 试试缩短：margin-top:48px;margin-bottom:16px → margin:48px 0 16px
const before2 = html.length;
html = html.replace(
  /margin-top:48px;margin-bottom:16px/g,
  'margin:48px 0 16px'
);
html = html.replace(
  /margin-top:40px;margin-bottom:16px/g,
  'margin:40px 0 16px'
);
console.log(`margin shorthand: saved ${before2 - html.length} chars`);
totalSaved += before2 - html.length;

// 7. 精简 margin-top:36px;margin-bottom:14px → margin:36px 0 14px
const before3 = html.length;
html = html.replace(
  /margin-top:36px;margin-bottom:14px/g,
  'margin:36px 0 14px'
);
console.log(`phase margin shorthand: saved ${before3 - html.length} chars`);
totalSaved += before3 - html.length;

// 8. 场景模板的 &nbsp; 精简
// 统一把连续 &nbsp; 替换成 padding-left 方案... 太复杂
// 直接把多余的 &nbsp; 减少一些
const before4 = html.length;
html = html.replace(/&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;/g, '&nbsp;&nbsp;');
html = html.replace(/&nbsp;&nbsp;&nbsp;&nbsp;/g, '&nbsp;&nbsp;');
console.log(`nbsp reduction: saved ${before4 - html.length} chars`);
totalSaved += before4 - html.length;

// 9. 精简 table 中的 font-size:14px（如果外层有不同的默认值就不能省）
// 保留

// 10. 代码块中的 font-family 会被 sanitize 删掉，但源文件里可以先精简
const before5 = html.length;
html = html.replace(
  /font-family:'SF Mono','Fira Code',Menlo,Consolas,monospace;/g,
  ''
);
console.log(`code font-family removal: saved ${before5 - html.length} chars`);
totalSaved += before5 - html.length;

// 11. 移除空白的 &nbsp; 前后 的 &nbsp;
// 场景模板中 <span>谁</span>&nbsp;&nbsp; 可以缩短
// Actually let's try removing background:#fff from elements where white bg is default
const before6 = html.length;
// Pain cards and table cells have background:#fff which is default - can remove
html = html.replace(
  /(<div style="[^"]*);background:#fff;?(")/g,
  (m, pre, post) => {
    // Only if it's a card that already has border (so bg is just default)
    if (pre.includes('border:1px solid')) {
      return pre + post;
    }
    return m;
  }
);
console.log(`remove default bg:#fff from cards: saved ${before6 - html.length} chars`);
totalSaved += before6 - html.length;

// 12. Table cells: background:#fff is redundant (white is default)
const before7 = html.length;
html = html.replace(/(<td style="[^"]*);background:#fff;?(")/g, '$1$2');
console.log(`remove bg:#fff from td: saved ${before7 - html.length} chars`);
totalSaved += before7 - html.length;

console.log(`\nTotal saved: ${totalSaved} chars`);

// Write back
fs.writeFileSync(filePath, html, 'utf-8');
console.log('✅ 源文件已更新');

// Test final size
const startMarker = '<!-- ========== ARTICLE CONTENT START ========== -->';
const endMarker = '<!-- ========== ARTICLE CONTENT END ========== -->';
let content = html.substring(html.indexOf(startMarker) + startMarker.length, html.indexOf(endMarker));
content = content.replace(/<!--[\s\S]*?-->/g, '').trim();
let changed = true;
while (changed) {
  changed = false;
  const m = content.match(/^\s*<div(?:\s+(?:class|id)="[^"]*")*\s*>\s*([\s\S]*)\s*<\/div>\s*$/);
  if (m && !content.match(/^\s*<div[^>]*style=/)) {
    const openTag = content.match(/^\s*<div[^>]*>/);
    if (openTag && !openTag[0].includes('style=')) {
      content = m[1].trim();
      changed = true;
    }
  }
}
let result = content;
result = result.replace(/font-family\s*:[^;"]*(?:'[^']*'[^;"]*|"[^"]*"[^;"]*)*;?/g, '');
result = result.replace(/\s+id="[^"]*"/g, '');
result = result.replace(/\s+class="[^"]*"/g, '');
result = result.replace(/rgba\(255,\s*255,\s*255,\s*0\.12\)/g, '#FFFFFF1F');
result = result.replace(/rgba\(255,\s*255,\s*255,\s*0\.2\)/g, '#FFFFFF33');
result = result.replace(/rgba\(255,\s*255,\s*255,\s*0\.8\)/g, '#FFFFFFCC');
result = result.replace(/rgba\(255,\s*255,\s*255,\s*0\.55\)/g, '#FFFFFF8C');
result = result.replace(/rgba\(0,\s*0,\s*0,\s*[\d.]+\)/g, '#00000026');
result = result.replace(/max-width\s*:\s*578px/g, 'width:100%');
result = result.replace(/position\s*:\s*[^;]+;?/g, '');
result = result.replace(/z-index\s*:\s*[^;]+;?/g, '');
result = result.replace(/;color:#2D2A3E(?=[";}])/g, '');
result = result.replace(/color:#2D2A3E;/g, '');
result = result.replace(/;\s*;/g, ';');
result = result.replace(/style=";\s*/g, 'style="');
result = result.replace(/;\s*"/g, '"');
result = result.replace(/style="\s*"/g, '');

let compressed = result.replace(/<!--[\s\S]*?-->/g, '').replace(/>\s+</g, '><').replace(/\s{2,}/g, ' ').trim();
console.log('\n字符数:', compressed.length);
if (compressed.length > 20000) {
  console.log(`⚠️  还差 ${compressed.length - 20000} 字符！`);
} else {
  console.log(`✅ 在限制内！余量 ${20000 - compressed.length} 字符`);
}
