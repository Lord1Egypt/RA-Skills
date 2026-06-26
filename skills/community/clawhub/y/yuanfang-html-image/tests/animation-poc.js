// Animation POC for yuanfang-html-image.
// Renders a sequence of frames showing CSS animations on a cover. The
// foundation: when ffmpeg is installed, frames can be composited into
// GIF/MP4 via `ffmpeg -i frame-%04dms.png -r 4 out.gif`.
//
// Usage:
//   node tests/animation-poc.js                  # 4 frames at 0/300/600/1000ms
//   node tests/animation-poc.js --output <dir>   # custom output dir

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const FRAMES = [0, 300, 600, 1000];

const SAMPLE = {
  title: 'MiniMax',
  body: 'AI 智能客服平台',
  points: ['AI 应用', '大语言模型', '编码'],
  brand: 'MiniMax',
  brandImage: null,
  badge: 'FEATURED',
  qr: 'https://aics.financialagent.cc/',
};

const ANIMATION_CSS = `
@keyframes yuanfang-fade-in {
  from { opacity: 0; transform: translateY(-8px); }
  to   { opacity: 1; transform: translateY(0); }
}
.cover__badge { animation: yuanfang-fade-in 1s ease-out both; }
@keyframes yuanfang-slide-in {
  from { opacity: 0; transform: translateX(-12px); }
  to   { opacity: 1; transform: translateX(0); }
}
.cover__points li { animation: yuanfang-slide-in 0.6s ease-out both; }
.cover__points li:nth-child(1) { animation-delay: 0.2s; }
.cover__points li:nth-child(2) { animation-delay: 0.4s; }
.cover__points li:nth-child(3) { animation-delay: 0.6s; }
`;

const HTML = `<!DOCTYPE html>
<html lang="zh-CN" data-theme="minimal-white">
<head>
<meta charset="utf-8">
<style>
body { margin: 0; padding: 0; width: 1080px; height: 1440px; overflow: hidden; font-family: "PingFang SC", system-ui, sans-serif; }
.cover { width: 1080px; height: 1440px; padding: 80px; box-sizing: border-box; background: #fff; position: relative; }
.cover__badge { color: #5856E9; font-weight: 600; letter-spacing: 0.25em; text-transform: uppercase; font-size: 32px; margin-bottom: 60px; }
.cover__title { font-size: 96px; font-weight: 900; line-height: 1.05; margin: 0 0 40px; color: #181E25; }
.cover__content { font-size: 38px; line-height: 1.7; color: #5a5a5a; margin: 0 0 60px; }
.cover__points { list-style: none; padding: 0; margin: 0; display: flex; flex-wrap: wrap; gap: 16px; }
.cover__points li { font-size: 30px; color: #5856E9; padding: 8px 16px; border-top: 1px solid #5856E9; }
.cover__brand { position: absolute; bottom: 60px; left: 80px; font-size: 30px; font-weight: 700; }
${ANIMATION_CSS}
</style>
</head>
<body>
<div class="cover">
  <div class="cover__badge">${SAMPLE.badge}</div>
  <h1 class="cover__title">${SAMPLE.title}</h1>
  <p class="cover__content">${SAMPLE.body}</p>
  <ul class="cover__points">
    ${SAMPLE.points.map(p => `<li>${p}</li>`).join('')}
  </ul>
  <div class="cover__brand">${SAMPLE.brand}</div>
</div>
</body>
</html>`;

async function main() {
  const args = process.argv.slice(2);
  const outFlag = args.indexOf('--output');
  const outDir = outFlag > -1 ? args[outFlag + 1] : path.join(__dirname, '.animation-out');
  fs.mkdirSync(outDir, { recursive: true });

  const htmlPath = path.join(outDir, 'frame-source.html');
  fs.writeFileSync(htmlPath, HTML);

  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1440 } });
  await page.goto(`file://${htmlPath}`);

  let prevMs = 0;
  for (const ms of FRAMES) {
    if (ms > prevMs) await page.waitForTimeout(ms - prevMs);
    const outPath = path.join(outDir, `frame-${String(ms).padStart(4, '0')}ms.png`);
    await page.screenshot({ path: outPath, type: 'png' });
    console.log(`  ✔ ${ms}ms -> ${outPath}`);
    prevMs = ms;
  }
  await browser.close();
  console.log(`\nDone. ${FRAMES.length} frames in ${outDir}`);
  console.log('Foundation ready. To compose to GIF (when ffmpeg installed):');
  console.log(`  ffmpeg -i "${outDir}/frame-%04dms.png" -r 4 "${outDir}/animated.gif"`);
}

main().catch(err => { console.error(err.message); process.exit(1); });
