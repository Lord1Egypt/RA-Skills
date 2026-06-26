const fs = require('fs');
const path = require('path');

function escapeXml(str = '') {
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

function wrapText(text, max = 18) {
  const chars = Array.from(String(text || ''));
  const lines = [];
  for (let i = 0; i < chars.length; i += max) lines.push(chars.slice(i, i + max).join(''));
  return lines;
}

function renderCard(page, index) {
  const width = 1242;
  const height = 1660;
  const isCover = index === 0 || (page.footer && String(page.footer).includes('封面'));
  const titleLines = wrapText(page.title || '', isCover ? 12 : 14);
  const subtitleLines = wrapText(page.subtitle || '', 18);
  const bullets = (page.bullets || []).slice(0, 4);

  let y = isCover ? 300 : 210;
  const titleSvg = titleLines.map(line => {
    const s = `<text x="96" y="${y}" font-size="${isCover ? 86 : 72}" font-weight="900" fill="#111111">${escapeXml(line)}</text>`;
    y += isCover ? 104 : 92;
    return s;
  }).join('\n');

  y += isCover ? 26 : 20;
  const subtitleSvg = subtitleLines.map(line => {
    const s = `<text x="96" y="${y}" font-size="${isCover ? 40 : 36}" font-weight="600" fill="#5F5F5F">${escapeXml(line)}</text>`;
    y += isCover ? 56 : 52;
    return s;
  }).join('\n');

  y += isCover ? 72 : 54;
  const bulletSvg = (isCover ? bullets.slice(0, 2) : bullets).map((b, idx) => {
    const lines = wrapText(b, 24);
    const startY = y;
    const box = `<rect x="96" y="${startY - 38}" width="1050" height="${Math.max(1, lines.length) * 52 + 34}" rx="28" fill="#FFFFFF" stroke="#F0E3D8" />`;
    const badge = `<circle cx="142" cy="${startY - 2}" r="18" fill="#ff2442" />\n<text x="136" y="${startY + 8}" font-size="24" font-weight="800" fill="#FFFFFF">${idx + 1}</text>`;
    const text = lines.map((line, i) => `<text x="184" y="${startY + i * 48}" font-size="34" font-weight="600" fill="#222222">${escapeXml(line)}</text>`).join('\n');
    y += Math.max(1, lines.length) * 52 + 52;
    return `${box}\n${badge}\n${text}`;
  }).join('\n');

  const chip = `<rect x="96" y="88" width="150" height="44" rx="22" fill="#FFE4EA" />\n<text x="122" y="117" font-size="20" font-weight="700" fill="#ff2442">AI</text>`;
  const footer = page.footer
    ? `<text x="96" y="1540" font-size="28" font-weight="700" fill="#8A817C">${escapeXml(page.footer)}</text>`
    : `<text x="96" y="1540" font-size="28" font-weight="700" fill="#8A817C">第 ${index + 1} 页</text>`;

  const coverAccent = isCover
    ? `<circle cx="1070" cy="220" r="140" fill="#FFE4EA" />\n<circle cx="980" cy="320" r="46" fill="#FFD36B" />`
    : '';

  return `<?xml version="1.0" encoding="UTF-8"?>
<svg width="${width}" height="${height}" viewBox="0 0 ${width} ${height}" fill="none" xmlns="http://www.w3.org/2000/svg">
  <rect width="${width}" height="${height}" rx="0" fill="#FFF8F2"/>
  <rect x="0" y="0" width="${width}" height="20" fill="#ff2442"/>
  <rect x="52" y="52" width="1138" height="1556" rx="52" fill="#FFFDFB" stroke="#F1E4DA" />
  ${chip}
  ${coverAccent}
  ${titleSvg}
  ${subtitleSvg}
  ${bulletSvg}
  ${footer}
</svg>`;
}

async function renderPngs(svgDir, pngDir) {
  const { chromium } = require('playwright');
  fs.mkdirSync(pngDir, { recursive: true });
  const browser = await chromium.launch({ headless: true, channel: 'chrome' });
  const page = await browser.newPage({ viewport: { width: 1242, height: 1660 }, deviceScaleFactor: 1 });
  const files = fs.readdirSync(svgDir).filter(f => f.endsWith('.svg')).sort();

  for (const file of files) {
    const full = path.join(svgDir, file);
    const svg = fs.readFileSync(full, 'utf8');
    await page.setContent(svg, { waitUntil: 'load' });
    const pngPath = path.join(pngDir, file.replace(/\.svg$/i, '.png'));
    await page.screenshot({ path: pngPath, type: 'png' });
  }

  await browser.close();
}

async function main() {
  const input = process.argv[2];
  const outDir = process.argv[3] || '/tmp/openclaw/uploads/xhs_generated_cards';
  const pngDir = process.argv[4] || path.join(outDir, 'png');
  if (!input) throw new Error('Usage: node generate_xhs_cards.js <pages.json> [svgOutDir] [pngOutDir]');

  const pages = JSON.parse(fs.readFileSync(input, 'utf8'));
  fs.mkdirSync(outDir, { recursive: true });

  pages.forEach((page, i) => {
    const svg = renderCard(page, i);
    const filename = path.join(outDir, `xhs_card_${String(i + 1).padStart(2, '0')}.svg`);
    fs.writeFileSync(filename, svg, 'utf8');
  });

  console.log(`Generated ${pages.length} SVG cards in ${outDir}`);
  await renderPngs(outDir, pngDir);
  console.log(`Generated ${pages.length} PNG cards in ${pngDir}`);
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
