#!/usr/bin/env node
/**
 * screenshot_wechat.js — Screenshot a WeChat Official Account article
 *
 * Saves a full-article PNG using the #js_article selector (includes title,
 * author, date, and body). Hides WeChat UI chrome (like/share bars, ads,
 * subscription prompts) before capture. Scrolls page first to trigger
 * lazy-loaded images.
 *
 * Usage:
 *   node screenshot_wechat.js <url> [--out=/path/to/output.png]
 *
 * Output path defaults to /tmp/wechat_screenshot.png
 */

let chromium;
try {
  ({ chromium } = require('playwright-core'));
} catch {
  const { execSync } = require('child_process');
  const searchDirs = [
    process.env.NVM_DIR || `${process.env.HOME}/.nvm`,
    '/usr/lib/node_modules',
    '/usr/local/lib/node_modules',
    '/usr',
  ].join(' ');
  const found = execSync(
    `find ${searchDirs} -name 'playwright-core' -path '*/node_modules/*' -type d 2>/dev/null | head -1`,
    { encoding: 'utf-8' }
  ).trim();
  if (!found) {
    console.error('Error: playwright-core not found.');
    process.exit(1);
  }
  ({ chromium } = require(found));
}

function findChrome() {
  const candidates = [
    '/usr/bin/google-chrome-stable',
    '/usr/bin/google-chrome',
    '/usr/bin/chromium-browser',
    '/usr/bin/chromium',
    '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  ];
  const fs = require('fs');
  for (const p of candidates) { if (fs.existsSync(p)) return p; }
  try {
    const { execSync } = require('child_process');
    return execSync('which google-chrome-stable || which google-chrome || which chromium', { encoding: 'utf-8' }).trim().split('\n')[0];
  } catch { return null; }
}

const args = process.argv.slice(2);
const url = args.find(a => a.startsWith('http'));
const outArg = args.find(a => a.startsWith('--out='));
const outPath = outArg ? outArg.split('=').slice(1).join('=') : '/tmp/wechat_screenshot.png';
const chromePath = (() => {
  const a = args.find(a => a.startsWith('--chrome-path='));
  return a ? a.split('=').slice(1).join('=') : findChrome();
})();

if (!url) {
  console.error('Usage: node screenshot_wechat.js <url> [--out=path.png] [--chrome-path=PATH]');
  process.exit(1);
}

(async () => {
  const browser = await chromium.launch({
    headless: true,
    executablePath: chromePath,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-blink-features=AutomationControlled'],
  });

  const ctx = await browser.newContext({
    userAgent: 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
    viewport: { width: 390, height: 844 },
    locale: 'zh-CN',
    timezoneId: 'Asia/Shanghai',
  });
  await ctx.addInitScript(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
  });

  const page = await ctx.newPage();
  await page.goto(url, { waitUntil: 'load', timeout: 30000 });
  await page.waitForTimeout(2000);

  // Scroll through the page to trigger lazy-loaded images
  await page.evaluate(async () => {
    await new Promise((resolve) => {
      let totalHeight = 0;
      const distance = 300;
      const timer = setInterval(() => {
        window.scrollBy(0, distance);
        totalHeight += distance;
        if (totalHeight >= document.body.scrollHeight) {
          clearInterval(timer);
          window.scrollTo(0, 0); // scroll back to top
          resolve();
        }
      }, 100);
    });
  });
  await page.waitForTimeout(2000); // wait for images to finish loading

  // Hide WeChat UI chrome before screenshotting.
  // Step 1: Hide known fixed chrome by class/id
  await page.addStyleTag({ content: `
    #js_like_area, .rich_media_area_primary_top, .rich_media_tool,
    .share_notice, .wx_follow_tip, #js_pc_qr_code,
    .reward_qrcode_area, .weui-panel, #js_subscribe_btn,
    .js_editor_audio, .rich_media_area_extra,
    .wx_follow_area, .wx_profile_card, .wx_profile_card_inner,
    .weui-sticky-footer, .weui-sticky-header,
    #js_top_ad_area, .top_banner { display: none !important; }
  ` });
  // Step 2: Hide ALL fixed/sticky elements via JS (catches any dynamic overlays
  // that WeChat injects regardless of class name), then force them to static
  // so they don't bleed into the article bounding box
  await page.evaluate(() => {
    document.querySelectorAll('*').forEach(el => {
      const pos = window.getComputedStyle(el).position;
      if (pos === 'fixed' || pos === 'sticky') {
        el.style.setProperty('display', 'none', 'important');
        el.style.setProperty('position', 'static', 'important');
      }
    });
  });
  await page.waitForTimeout(800); // let WeChat JS settle before capture

  // Target the full article area including title, author, date, and body
  // Priority: #js_article > .rich_media_wrp > #js_content (body only, no title)
  // Exclude: WeChat footer, subscription prompts, contact sections
  const selectors = ['#js_article', '.rich_media_wrp', '#js_content'];
  let articleEl = null;
  for (const sel of selectors) {
    articleEl = await page.$(sel);
    if (articleEl) {
      console.error(`Using selector: ${sel}`);
      break;
    }
  }

  if (articleEl) {
    // Use page.screenshot with fullPage:true and clip to element bbox,
    // instead of elementHandle.screenshot(), to avoid fixed-overlay bleed.
    const bbox = await articleEl.boundingBox();
    await page.screenshot({
      path: outPath,
      fullPage: true,
      clip: { x: bbox.x, y: bbox.y, width: bbox.width, height: bbox.height },
    });
  } else {
    // Fallback: full page
    await page.screenshot({ path: outPath, fullPage: true });
    console.error('Warning: no article container found, fell back to full-page screenshot');
  }

  await browser.close();
  console.log(outPath);
})();
