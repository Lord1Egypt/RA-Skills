import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const html = fs.readFileSync(path.join(__dirname, '..', 'blog-post-wechat.html'), 'utf-8');

// extractArticleContent
const startMarker = '<!-- ========== ARTICLE CONTENT START ========== -->';
const endMarker = '<!-- ========== ARTICLE CONTENT END ========== -->';
let content = html.substring(html.indexOf(startMarker) + startMarker.length, html.indexOf(endMarker)).trim();
const wrapperMatch = content.match(/^<div[^>]*(?:class="article-content"|id="articleContent")[^>]*>\s*([\s\S]*)\s*<\/div>\s*$/);
if (wrapperMatch) { content = wrapperMatch[1].trim(); }

// sanitizeForWechat
let result = content;
result = result.replace(/font-family\s*:[^;"]*(?:'[^']*'[^;"]*|"[^"]*"[^;"]*)*;?/g, '');
result = result.replace(/\s+id="[^"]*"/g, '');
result = result.replace(/\s+class="[^"]*"/g, '');
result = result.replace(/rgba\(255,\s*255,\s*255,\s*0\.12\)/g, '#FFFFFF1F');
result = result.replace(/rgba\(255,\s*255,\s*255,\s*0\.2\)/g, '#FFFFFF33');
result = result.replace(/rgba\(255,\s*255,\s*255,\s*0\.8\)/g, '#FFFFFFCC');
result = result.replace(/rgba\(255,\s*255,\s*255,\s*0\.55\)/g, '#FFFFFF8C');
result = result.replace(/rgba\(0,\s*0,\s*0,[\d.\s]+\)/g, '#00000026');
result = result.replace(/max-width\s*:\s*578px/g, 'width:100%');
result = result.replace(/position\s*:\s*[^;]+;?/g, '');
result = result.replace(/z-index\s*:\s*[^;]+;?/g, '');
result = result.replace(/;\s*;/g, ';');
result = result.replace(/style=";\s*/g, 'style="');
result = result.replace(/;\s*"/g, '"');

// compress
let compressed = result.replace(/<!--[\s\S]*?-->/g, '').replace(/>\s+</g, '><').replace(/\s{2,}/g, ' ').trim();

console.log('=== 前 600 字符 ===');
console.log(compressed.substring(0, 600));
console.log('');
console.log('=== 兼容性检查 ===');
console.log('rgba 残留:', (compressed.match(/rgba/g) || []).length);
console.log('max-width 残留:', (compressed.match(/max-width/g) || []).length);
console.log('id= 残留:', (compressed.match(/ id=/g) || []).length);
console.log('class= 残留:', (compressed.match(/ class=/g) || []).length);
console.log('style= 出现:', (compressed.match(/style=/g) || []).length);
console.log('background 出现:', (compressed.match(/background/g) || []).length);
console.log('border-left 出现:', (compressed.match(/border-left/g) || []).length);
console.log('总长度:', compressed.length);
