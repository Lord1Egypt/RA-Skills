#!/usr/bin/env node
const fs = require('fs');
const path = require('path');
const { listThemes } = require('../../yuanfang-html-image/scripts/render');

const SCRIPT_DIR = __dirname;
const REPO_ROOT = path.join(SCRIPT_DIR, '..', '..');
const DESIGN_DIR = path.join(REPO_ROOT, 'yuanfang-design');
const HTML_LAYOUT = path.join(DESIGN_DIR, 'layout-types', 'cover.html');
const BASE_CSS = path.join(DESIGN_DIR, 'base.css');

const PLATFORMS = [
  { id: 'xiaohongshu-v',  width: 1080, height: 1440, label: '3:4 竖版' },
  { id: 'moments',        width: 1080, height: 1080, label: '1:1 方版' },
  { id: 'bilibili-cover', width: 1920, height: 1080, label: '16:9 横版' },
  { id: 'wechat-cover',   width: 900,  height: 383,  label: '2.35:1 封面' },
  { id: 'twitter',        width: 1200, height: 675,  label: '1.9:1 OG' },
  { id: 'douyin-cover',   width: 1080, height: 1920, label: '9:16 长竖' },
];

const SAMPLE = {
  title: 'AI 重塑创作',
  body: '从文案到配图，AI 改变内容工作流。',
  points: ['效率 10x', '零门槛', '增强而非替代'],
  source: '示例内容',
  badge: 'FEATURED',
  brand: 'Yuanfang',
};

function main() {
  const themes = listThemes();
  const html = fs.readFileSync(HTML_LAYOUT, 'utf-8');
  const baseCSS = fs.readFileSync(BASE_CSS, 'utf-8');

  const outDir = path.join(SCRIPT_DIR, 'output');
  fs.mkdirSync(outDir, { recursive: true });

  const cells = [];
  for (const theme of themes) {
    for (const p of PLATFORMS) {
      const themeCSS = fs.readFileSync(path.join(DESIGN_DIR, 'themes', `${theme}.css`), 'utf-8');
      const fullHtml = `<!DOCTYPE html><html lang="zh-CN" data-theme="${theme}"><head><meta charset="utf-8"><style>${baseCSS}${themeCSS}body{margin:0;padding:0;width:${p.width}px;height:${p.height}px;overflow:hidden}.cover{width:${p.width}px;height:${p.height}px}</style></head><body>${html.replace(/\{\{(\w+)\}\}/g, (_, k) => SAMPLE[k.toLowerCase()] || '')}</body></html>`;
      const fileName = `${theme}_${p.id}.html`;
      fs.writeFileSync(path.join(outDir, fileName), fullHtml, 'utf-8');
      cells.push(`<div class="cell"><div class="label">${theme} · ${p.label}</div><iframe src="output/${fileName}" style="aspect-ratio:${p.width}/${p.height}"></iframe></div>`);
    }
  }

  const showcase = `<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<title>Cover Showcase — 12 themes × 6 platforms</title>
<style>
body { font-family: system-ui, sans-serif; background: #f5f5f5; padding: 24px; }
h1 { font-size: 24px; margin-bottom: 24px; }
.grid { display: grid; grid-template-columns: repeat(6, 1fr); gap: 16px; }
.cell { background: white; border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,.1); }
.label { font-size: 11px; padding: 6px 10px; background: #f0f0f0; color: #333; }
iframe { width: 100%; height: 200px; border: 0; display: block; }
</style>
</head>
<body>
<h1>Cover Showcase — ${themes.length} themes × ${PLATFORMS.length} platforms = ${themes.length * PLATFORMS.length}</h1>
<div class="grid">
${cells.join('\n')}
</div>
</body>
</html>`;

  fs.writeFileSync(path.join(SCRIPT_DIR, 'cover-showcase.html'), showcase, 'utf-8');
  console.log(`Generated ${themes.length * PLATFORMS.length} cells`);
  console.log(`Open: file://${path.join(SCRIPT_DIR, 'cover-showcase.html')}`);
}

if (require.main === module) main();
module.exports = { main };
