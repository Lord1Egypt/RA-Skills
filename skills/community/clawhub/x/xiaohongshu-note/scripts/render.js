#!/usr/bin/env node
/* 小红书图文笔记：渲染 3:4 高清 PNG，每次随机一套风格（可指定） */
const path = require('path');
const { chromium } = require('playwright');
const fs = require('fs');
let themes;
try { themes = require('./themes.js'); }
catch (e) { themes = require(path.join(__dirname, 'themes.js')); }
const { THEMES, THEME_KEYS, pickTheme } = themes;

const BASE = __dirname;
// 定位 slides.html：优先脚本同目录，其次 ../assets/template/（skill 内直接运行时）
function findHtml() {
  const candidates = [
    path.join(BASE, 'slides.html'),
    path.join(BASE, '..', 'assets', 'template', 'slides.html'),
  ];
  for (const c of candidates) if (fs.existsSync(c)) return c;
  return candidates[0];
}
const HTML_FILE = findHtml();
const OUT_DIR = path.join(path.dirname(HTML_FILE), 'export');
const W = 1080, H = 1440, SCALE = 2; // 3:4 竖版，2x 高清

(async () => {
  const themeArg = process.argv[2];
  if (themeArg === 'list') {
    console.log('可用主题：'); THEME_KEYS.forEach(k => console.log(`  ${k}  ${THEMES[k].label}`));
    return;
  }
  const theme = pickTheme(themeArg);
  if (!theme) return;
  console.log(`🎨 使用风格：${theme.label} (${theme.name})`);

  // 生成 CSS 变量注入块
  const cssVars = `
    :root{
      --cream:${theme.bg}; --ink:${theme.ink}; --cocoa:${theme.cocoa};
      --caramel:${theme.caramel}; --oat:${theme.oat}; --matcha:${theme.matcha};
      --peach:${theme.peach}; --muted:${theme.muted}; --line:${theme.line};
      --cover1:${theme.cover1}; --cover2:${theme.cover2}; --pageBg:${theme.pageBg};
      --dot:${theme.dot};
    }`;

  // 读取 HTML，把 <!-- THEME --> 占位替换成 CSS 变量
  let html = fs.readFileSync(HTML_FILE, 'utf8');
  if (html.includes('<!-- THEME -->')) {
    html = html.replace('<!-- THEME -->', cssVars);
  } else {
    // 兼容：无占位符时插到 </style> 前
    html = html.replace('</style>', cssVars + '\n</style>');
  }
  const tmpHtml = path.join(BASE, '_themed.html');
  fs.writeFileSync(tmpHtml, html, 'utf8');

  fs.mkdirSync(OUT_DIR, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: SCALE });
  await page.goto('file://' + tmpHtml);

  const total = await page.evaluate(() => document.querySelectorAll('.slide').length);
  console.log('共', total, '页，开始导出 3:4 高清图文...');

  for (let i = 0; i < total; i++) {
    await page.evaluate((n) => {
      const slides = document.querySelectorAll('.slide');
      slides.forEach((s, k) => s.classList.toggle('active', k === n));
    }, i);
    await page.waitForTimeout(150);
    await page.screenshot({ path: path.join(OUT_DIR, `图${String(i + 1).padStart(2, '0')}.png`) });
    console.log(`  已导出 ${i + 1}/${total}`);
  }

  await browser.close();
  fs.unlinkSync(tmpHtml);
  console.log(`\n✅ 完成（风格：${theme.label}）→`, OUT_DIR);
})().catch(e => { console.error('导出失败:', e.message); process.exit(1); });
