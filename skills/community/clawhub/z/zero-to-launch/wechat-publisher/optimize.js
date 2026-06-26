import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const filePath = path.join(__dirname, '..', 'blog-post-wechat.html');
let html = fs.readFileSync(filePath, 'utf-8');

// 1. 精简所有 <p> 标签的标准样式
// 外层 div 已经有 font-size:16px;line-height:1.85;color:#2D2A3E
// <p> 不需要重复这些，只需 margin
let count = 0;

// Pattern A: standard p with full style
html = html.replace(
  /<p style="margin:14px 0;text-align:justify;color:#2D2A3E;font-size:16px;line-height:1\.85;">/g,
  () => { count++; return '<p style="margin:14px 0;">'; }
);
console.log(`Pattern A (standard p): ${count} replacements`);

// Pattern B: p with padding-left
let count2 = 0;
html = html.replace(
  /<p style="margin:10px 0;padding-left:20px;text-align:justify;color:#2D2A3E;font-size:16px;line-height:1\.85;">/g,
  () => { count2++; return '<p style="margin:10px 0;padding-left:20px;">'; }
);
console.log(`Pattern B (padding-left p): ${count2} replacements`);

// Pattern C: p with different margin but same redundant styles
let count3 = 0;
html = html.replace(
  /<p style="margin:14px 0;color:#2D2A3E;font-size:16px;line-height:1\.85;">/g,
  () => { count3++; return '<p style="margin:14px 0;">'; }
);
console.log(`Pattern C (no text-align p): ${count3} replacements`);

// 2. 精简引用块样式 - 去掉可继承的 color:#2D2A3E 和 line-height
let count4 = 0;
html = html.replace(
  /(<div style="[^"]*);color:#2D2A3E;line-height:1\.8;?(")/g,
  (m, before, after) => { count4++; return before + after; }
);
console.log(`Pattern D (quote block color/lh): ${count4} replacements`);

// 3. 精简 code block 中的 font-family 会被 sanitize 删掉，这里先不管

// 4. 把 &#9654; 简化为 ▶ （节省字符）
html = html.replace(/&#9654;/g, '▶');
html = html.replace(/&#10132;/g, '➔');

// 5. 精简 &nbsp; 连续使用
// 场景模板里有很多 &nbsp;&nbsp;&nbsp; 可以用短的写法

// Write back
fs.writeFileSync(filePath, html, 'utf-8');
console.log('\n✅ 源文件已更新');

// Now test the full pipeline
const startMarker = '<!-- ========== ARTICLE CONTENT START ========== -->';
const endMarker = '<!-- ========== ARTICLE CONTENT END ========== -->';
let content = html.substring(html.indexOf(startMarker) + startMarker.length, html.indexOf(endMarker));
content = content.replace(/<!--[\s\S]*?-->/g, '').trim();

// Strip wrappers
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

// Sanitize (simplified - just remove font-family, id, class, rgba, max-width, position)
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
// Remove redundant color declarations that match parent
result = result.replace(/;color:#2D2A3E(?=[";}])/g, '');
result = result.replace(/color:#2D2A3E;/g, '');
// Clean up
result = result.replace(/;\s*;/g, ';');
result = result.replace(/style=";\s*/g, 'style="');
result = result.replace(/;\s*"/g, '"');
result = result.replace(/style="\s*"/g, '');

// Compress
let compressed = result
  .replace(/<!--[\s\S]*?-->/g, '')
  .replace(/>\s+</g, '><')
  .replace(/\s{2,}/g, ' ')
  .trim();

console.log('\n=== 最终结果 ===');
console.log('字符数:', compressed.length);
console.log('style=:', (compressed.match(/style=/g) || []).length);
console.log('background:', (compressed.match(/background/g) || []).length);
console.log('border-left:', (compressed.match(/border-left/g) || []).length);

if (compressed.length > 20000) {
  console.log(`\n⚠️  还差 ${compressed.length - 20000} 字符！`);
} else {
  console.log(`\n✅ 在限制内！余量 ${20000 - compressed.length} 字符`);
}
