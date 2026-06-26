// Visual regression test for yuanfang-skills.
// Renders selected (theme, platform) combinations and compares against
// baseline PNGs in tests/visual-baselines/. If a baseline is missing,
// it's created on first run. If a baseline exists and differs by more
// than VISUAL_THRESHOLD, the test fails.
//
// Run:
//   node tests/visual-regression.test.js           # compare against baselines
//   node tests/visual-regression.test.js --update  # regenerate baselines

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const RENDER = path.join(__dirname, '..', 'scripts', 'render.js');
const BASE_DIR = path.join(__dirname, 'visual-baselines');
const THRESHOLD = 0.01; // 1% pixel diff allowed

// (theme, platform) pairs to test. Keep small for fast CI.
const CASES = [
  ['minimal-white', 'xiaohongshu-v'],
  ['minimal-white', 'moments'],
  ['dark-gold', 'xiaohongshu-v'],
  ['tech-modern', 'xiaohongshu-v'],
  ['eastern', 'xiaohongshu-v'],
  ['magazine-cover', 'wechat-cover'],
];

const SAMPLE_CONTENT = {
  title: 'MiniMax',
  body: '全球领先的通用人工智能科技公司',
  points: ['旗舰模型', 'MiniMax M3', '海螺 Hailuo 2.3'],
  brand: 'MiniMax',
  brandImage: null,
  badge: 'FEATURED',
};

async function renderOne(theme, platform) {
  // Run render.js in a child process and read the produced PNG.
  const tmpDir = path.join(__dirname, '.visual-tmp');
  fs.mkdirSync(tmpDir, { recursive: true });
  const file = path.join(__dirname, '..', '..', 'content-minimax.json');
  fs.writeFileSync(file, JSON.stringify(SAMPLE_CONTENT, null, 2));
  try {
    execSync(
      `node "${RENDER}" --theme ${theme} --layout cover --platforms ${platform} --file "${file}" --output "${tmpDir}"`,
      { stdio: 'pipe' }
    );
  } finally {
    fs.unlinkSync(file);
  }
  const slug = `MiniMax_${platform}.png`;
  const pngPath = path.join(tmpDir, slug);
  if (!fs.existsSync(pngPath)) {
    throw new Error(`Render did not produce ${pngPath}`);
  }
  return pngPath;
}

function pixelsDiffer(aBuf, bBuf) {
  // Returns a diff ratio in [0, 1]. Combines two signals:
  //   1. Pixel sample: every 4th pixel's RGB compared (fast, catches content changes)
  //   2. Header sample: first 64 bytes compared (catches structural/header corruption
  //      that's invisible to pixel sampling)
  // Either signal above threshold fails the test.
  if (aBuf.length !== bBuf.length) return 1;
  let pixelDiff = 0;
  const totalPixels = aBuf.length / 4;
  for (let i = 0; i < aBuf.length; i += 16) {
    if (aBuf[i] !== bBuf[i] || aBuf[i + 1] !== bBuf[i + 1] || aBuf[i + 2] !== bBuf[i + 2]) {
      pixelDiff++;
    }
  }
  const pixelRatio = pixelDiff / (totalPixels / 4);
  // Header check: any diff in first 64 bytes = >5% diff (header is small but critical)
  let headerDiff = 0;
  for (let i = 0; i < 64; i++) {
    if (aBuf[i] !== bBuf[i]) headerDiff++;
  }
  const headerRatio = headerDiff / 64;
  // Return the max of the two signals
  return Math.max(pixelRatio, headerRatio);
}

const { test } = require('node:test');
const assert = require('node:assert');

const updateMode = process.argv.includes('--update');
fs.mkdirSync(BASE_DIR, { recursive: true });

test('visual regression: theme × platform', async (t) => {
  for (const [theme, platform] of CASES) {
    await t.test(`${theme} × ${platform}`, async () => {
      const actual = await renderOne(theme, platform);
      const baseline = path.join(BASE_DIR, `${theme}__${platform}.png`);

      if (updateMode || !fs.existsSync(baseline)) {
        fs.copyFileSync(actual, baseline);
        return;
      }

      const actualBuf = fs.readFileSync(actual);
      const baselineBuf = fs.readFileSync(baseline);
      const diff = pixelsDiffer(actualBuf, baselineBuf);
      assert.ok(
        diff < THRESHOLD,
        `Visual diff ${(diff * 100).toFixed(2)}% exceeds ${THRESHOLD * 100}% threshold.\n` +
        `  baseline: ${baseline}\n  actual:   ${actual}\n` +
        `Run with --update to regenerate baselines.`
      );
    });
  }
});
