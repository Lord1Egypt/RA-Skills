/**
 * 9 图 HTML → 高清 JPG 渲染器
 * 由 xhs-auto-publisher skill 生成
 *
 * 使用：node render_slides.js <slides.html> <output_dir>
 *   slides.html 里需要有 #s1, #s2, ..., #s9 共 9 个 slide 容器
 *   渲染分辨率：1080×1440 @ 2x = 2160×2880
 */

const puppeteer = require('puppeteer');
const path = require('path');
const fs = require('fs');

const htmlPath = process.argv[2] || path.join(process.cwd(), 'slides.html');
const outDir   = process.argv[3] || path.join(process.cwd(), 'images');
const pageCount = parseInt(process.env.SLIDE_COUNT || '9', 10);

(async () => {
  if (!fs.existsSync(htmlPath)) {
    console.error('✗ 找不到 HTML:', htmlPath);
    process.exit(1);
  }
  if (!fs.existsSync(outDir)) fs.mkdirSync(outDir, { recursive: true });

  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--font-render-hinting=none'],
  });
  const page = await browser.newPage();
  await page.setViewport({ width: 1080, height: 1440, deviceScaleFactor: 2 });
  await page.goto('file://' + path.resolve(htmlPath), { waitUntil: 'networkidle0' });
  await page.evaluate(() => document.fonts.ready);
  await new Promise(r => setTimeout(r, 800));

  for (let i = 1; i <= pageCount; i++) {
    const el = await page.$('#s' + i);
    if (!el) { console.log('⚠ 跳过 #s' + i + '（未找到）'); continue; }
    const out = path.join(outDir, String(i).padStart(2, '0') + '.jpg');
    await el.screenshot({ path: out, type: 'jpeg', quality: 94 });
    console.log('✓', out);
  }
  await browser.close();
  console.log('done.');
})();
