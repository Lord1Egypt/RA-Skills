const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

function arg(name, fallback = undefined) {
  const idx = process.argv.indexOf(`--${name}`);
  if (idx >= 0 && process.argv[idx + 1]) return process.argv[idx + 1];
  return process.env[`XHS_${name.toUpperCase().replace(/-/g, '_')}`] ?? fallback;
}

const USER_DATA_DIR = arg('user-data-dir', path.join(process.env.HOME, '.openclaw/browser/xhs-playwright-user-data'));
const ASSET_DIR = arg('asset-dir', '/tmp/openclaw/uploads/xhs_post_assets');
const TITLE = arg('title', '别再把 AI 当聊天机器人了｜很多人一开始就用错了');
const BODY = arg('body', `很多人用 AI，一开始方向就错了。

最常见的，不是不会用，
而是上来就盯着“哪个模型最强”“参数多不多”“跑分高不高”。

但模型 ≠ 结果。
如果你连自己要解决什么问题都没定义清楚，最后只会变成高级围观群众。

我现在对 AI 最大的感受是：

1. 别迷信一句提示词出奇迹
你给的信息越模糊，AI 越容易一本正经胡说。
真正拉开差距的，不是玄学 prompt，
而是你能不能把目标、背景、限制讲清楚。

2. AI 是工具，不是替身
现阶段它更像能力放大器，
不是能把脑子整包外包的打工人。
你没有判断力，它只会把混乱放大。

3. 真正有价值的是接进工作流
先研究工作流，不是先研究模型。
从高频重复动作切入，比如：
写总结、查资料、改文案、做翻译、整理会议纪要……

AI 最有价值的，不是惊艳你一次，
而是稳定帮你省时间。

真正拉开差距的，
不是最早听说 AI 的人，
而是最早把 AI 接进自己工作流里的人。

你现在用 AI，卡在哪一步？

#AI #人工智能 #AI工具 #效率提升 #工作流 #AI认知 #职场效率 #数字工具`);

function getImages(dir) {
  return fs.readdirSync(dir)
    .filter(f => /\.(png|jpg|jpeg|webp)$/i.test(f))
    .sort()
    .map(f => path.join(dir, f));
}

async function wait(ms) { return new Promise(r => setTimeout(r, ms)); }

async function clickByText(page, text) {
  const locator = page.getByText(text, { exact: true }).first();
  await locator.waitFor({ state: 'visible', timeout: 15000 });
  await locator.click();
}

async function ensureImagePublishPage(page) {
  if (!page.url().includes('target=image')) {
    await page.goto('https://creator.xiaohongshu.com/publish/publish?from=tab_switch&target=image', { waitUntil: 'domcontentloaded' });
    await page.waitForLoadState('networkidle').catch(() => {});
  }
}

async function waitForLoginIfNeeded(page) {
  const start = Date.now();
  while (Date.now() - start < 10 * 60 * 1000) {
    const url = page.url();
    if (url.includes('creator.xiaohongshu.com/publish')) return;
    await wait(1500);
  }
  throw new Error('Timed out waiting for login / publish page');
}

async function main() {
  const images = getImages(ASSET_DIR);
  if (!images.length) throw new Error(`No images found in ${ASSET_DIR}`);

  const context = await chromium.launchPersistentContext(USER_DATA_DIR, {
    headless: false,
    channel: 'chrome',
  });

  const page = context.pages()[0] || await context.newPage();
  await page.goto('https://creator.xiaohongshu.com/publish/publish?from=tab_switch&target=image', { waitUntil: 'domcontentloaded' });
  await page.waitForLoadState('networkidle').catch(() => {});

  await waitForLoginIfNeeded(page);
  await ensureImagePublishPage(page);

  let fileInput = page.locator('input[type="file"]').first();
  try {
    await fileInput.waitFor({ state: 'attached', timeout: 15000 });
  } catch {
    await clickByText(page, '上传图片').catch(() => {});
    await wait(1000);
    fileInput = page.locator('input[type="file"]').first();
    await fileInput.waitFor({ state: 'attached', timeout: 15000 });
  }

  await fileInput.setInputFiles(images);
  await wait(8000);

  const titleBox = page.locator('input[placeholder*="标题"], textarea[placeholder*="标题"]').first();
  await titleBox.waitFor({ state: 'visible', timeout: 30000 });
  await titleBox.fill(TITLE);

  const editor = page.locator('[contenteditable="true"]').last();
  await editor.waitFor({ state: 'visible', timeout: 30000 });
  await editor.click();
  await page.keyboard.press(process.platform === 'darwin' ? 'Meta+A' : 'Control+A').catch(() => {});
  await page.keyboard.type(BODY, { delay: 8 });

  console.log('READY_FOR_REVIEW');
  console.log(`Images: ${images.length}`);
  console.log(`Title: ${TITLE}`);
  console.log('Draft filled. Please review in browser and publish manually.');
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
