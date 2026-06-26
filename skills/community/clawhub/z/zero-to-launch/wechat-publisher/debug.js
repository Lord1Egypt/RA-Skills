import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const html = fs.readFileSync(path.join(__dirname, '..', 'blog-post-wechat.html'), 'utf-8');

// Step 1: extractArticleContent
const startMarker = '<!-- ========== ARTICLE CONTENT START ========== -->';
const endMarker = '<!-- ========== ARTICLE CONTENT END ========== -->';
let content = html.substring(html.indexOf(startMarker) + startMarker.length, html.indexOf(endMarker)).trim();

// Strip wrapper
const wrapperMatch = content.match(/^<div[^>]*(?:class="article-content"|id="articleContent")[^>]*>\s*([\s\S]*)\s*<\/div>\s*$/);
if (wrapperMatch) {
  console.log('✅ wrapper 被剥离');
  content = wrapperMatch[1].trim();
} else {
  console.log('❌ wrapper 没有匹配到');
}

console.log('\n=== Step1: extractArticleContent 后前 500 字符 ===');
console.log(content.substring(0, 500));

// Step 2: sanitize (copy from publish.js)
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
result = result.replace(/;\s*;/g, ';');
result = result.replace(/style=";\s*/g, 'style="');
result = result.replace(/;\s*"/g, '"');

console.log('\n=== Step2: sanitize 后前 500 字符 ===');
console.log(result.substring(0, 500));

// Step 3: compress
let compressed = result
  .replace(/<!--[\s\S]*?-->/g, '')
  .replace(/>\s+</g, '><')
  .replace(/\s{2,}/g, ' ')
  .trim();

console.log('\n=== Step3: compress 后前 800 字符 ===');
console.log(compressed.substring(0, 800));

console.log('\n=== 统计 ===');
console.log('总长度:', compressed.length);
console.log('style=:', (compressed.match(/style=/g) || []).length);
console.log('background:', (compressed.match(/background/g) || []).length);
console.log('border-left:', (compressed.match(/border-left/g) || []).length);
console.log('font-size:', (compressed.match(/font-size/g) || []).length);
console.log('color:', (compressed.match(/color/g) || []).length);
console.log('padding:', (compressed.match(/padding/g) || []).length);
console.log('display:', (compressed.match(/display/g) || []).length);

// Save the compressed output for inspection
fs.writeFileSync(path.join(__dirname, 'debug-output.html'), compressed, 'utf-8');
console.log('\n已保存处理后的 HTML 到 debug-output.html');
