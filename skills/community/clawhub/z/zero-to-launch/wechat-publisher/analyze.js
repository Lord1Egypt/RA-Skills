import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const html = fs.readFileSync(path.join(__dirname, '..', 'blog-post-wechat.html'), 'utf-8');

// extractArticleContent
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

// Analyze which styles take up the most space
let compressed = content
  .replace(/<!--[\s\S]*?-->/g, '')
  .replace(/>\s+</g, '><')
  .replace(/\s{2,}/g, ' ')
  .trim();

// Count repeated style patterns
const styleMatches = compressed.match(/style="[^"]+"/g) || [];
console.log('Total style attributes:', styleMatches.length);
console.log('Total chars in styles:', styleMatches.reduce((a, s) => a + s.length, 0));

// Find most common style values
const styleCounts = {};
for (const s of styleMatches) {
  styleCounts[s] = (styleCounts[s] || 0) + 1;
}

const sorted = Object.entries(styleCounts)
  .sort((a, b) => (b[0].length * b[1]) - (a[0].length * a[1]))
  .slice(0, 15);

console.log('\nTop 15 style declarations by total space used:');
for (const [style, count] of sorted) {
  console.log(`  ${count}x (${style.length * count} chars) ${style.substring(0, 80)}...`);
}

// Count individual CSS properties
const propCounts = {};
for (const s of styleMatches) {
  const inner = s.slice(7, -1); // remove style=" and "
  const props = inner.split(';').map(p => p.split(':')[0].trim()).filter(Boolean);
  for (const p of props) {
    propCounts[p] = (propCounts[p] || 0) + 1;
  }
}

console.log('\nMost repeated CSS properties:');
Object.entries(propCounts)
  .sort((a, b) => b[1] - a[1])
  .slice(0, 20)
  .forEach(([prop, count]) => console.log(`  ${prop}: ${count}x`));
