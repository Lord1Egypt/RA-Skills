import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const html = fs.readFileSync(path.join(__dirname, '..', 'blog-post-wechat.html'), 'utf-8');

// ---- extractArticleContent (new version) ----
const startMarker = '<!-- ========== ARTICLE CONTENT START ========== -->';
const endMarker = '<!-- ========== ARTICLE CONTENT END ========== -->';
let content = html.substring(html.indexOf(startMarker) + startMarker.length, html.indexOf(endMarker));
content = content.replace(/<!--[\s\S]*?-->/g, '').trim();

// Strip wrappers without style
let changed = true;
while (changed) {
  changed = false;
  const m = content.match(/^\s*<div(?:\s+(?:class|id)="[^"]*")*\s*>\s*([\s\S]*)\s*<\/div>\s*$/);
  if (m && !content.match(/^\s*<div[^>]*style=/)) {
    const openTag = content.match(/^\s*<div[^>]*>/);
    if (openTag && !openTag[0].includes('style=')) {
      content = m[1].trim();
      changed = true;
      console.log('✅ 剥离了一层 wrapper');
    }
  }
}

// ---- sanitizeForWechat (new version) ----
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

// 样式精简
result = result.replace(
  /(<p\s+style=")margin:14px 0;text-align:justify;color:#2D2A3E;font-size:16px;line-height:1\.85(")/g,
  '$1margin:14px 0;text-align:justify$2'
);
result = result.replace(
  /(<p\s+style=")margin:10px 0;padding-left:20px;text-align:justify;color:#2D2A3E;font-size:16px;line-height:1\.85(")/g,
  '$1margin:10px 0;padding-left:20px;text-align:justify$2'
);
result = result.replace(/;color:#2D2A3E(?=[";}])/g, '');
result = result.replace(/color:#2D2A3E;/g, '');

// 清理
result = result.replace(/;\s*;/g, ';');
result = result.replace(/style=";\s*/g, 'style="');
result = result.replace(/;\s*"/g, '"');
result = result.replace(/style="\s*"/g, '');

// ---- compressHTML ----
let compressed = result
  .replace(/<!--[\s\S]*?-->/g, '')
  .replace(/>\s+</g, '><')
  .replace(/\s{2,}/g, ' ')
  .trim();

console.log('\n=== 前 500 字符 ===');
console.log(compressed.substring(0, 500));
console.log('\n=== 统计 ===');
console.log('总字符数:', compressed.length);
console.log('style=:', (compressed.match(/style=/g) || []).length);
console.log('background:', (compressed.match(/background/g) || []).length);
console.log('border-left:', (compressed.match(/border-left/g) || []).length);
console.log('color:', (compressed.match(/color/g) || []).length);

if (compressed.length > 20000) {
  console.log('\n⚠️  还是超过 2 万字符！需要进一步精简 HTML 源文件');
  console.log('   需要减少:', compressed.length - 20000, '字符');
} else {
  console.log('\n✅ 在 2 万字符限制以内！');
}

fs.writeFileSync(path.join(__dirname, 'debug-output2.html'), compressed, 'utf-8');
