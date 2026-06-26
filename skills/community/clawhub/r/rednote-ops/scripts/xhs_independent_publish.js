const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const { spawnSync } = require('child_process');

function arg(name, fallback = undefined) {
  const idx = process.argv.indexOf(`--${name}`);
  if (idx >= 0 && process.argv[idx + 1]) return process.argv[idx + 1];
  return fallback;
}

function shortenTitle(input, max = 20) {
  const s = String(input || '').replace(/[\n\r]+/g, ' ').trim();
  if ([...s].length <= max) return s;

  const rules = [
    [/大多数人还没意识到/g, '很多人没意识到'],
    [/真正淘汰的是/g, '真正淘汰的'],
    [/会提问的人很多，但会把AI接进工作的人还不多/g, '会提问不等于会用AI'],
    [/会用AI的人变多了，但真正拉开差距的人还很少/g, 'AI拉开差距的是工作流'],
    [/你以为大家都在学AI，其实真正赚钱的人在搭流程/g, '赚钱的人都在搭AI流程'],
    [/大多数人学 AI 的方向一开始就错了/g, '大多数人学AI方向错了'],
    [/很多人只盯模型参数，却没看见Anthropic真正重视的是harness/g, 'Anthropic更重视harness'],
    [/Anthropic/gi, 'Anthropic'],
    [/OpenAI/gi, 'OpenAI'],
    [/harness engineering/gi, 'harness'],
    [/computer use/gi, 'computer use']
  ];

  let out = s;
  for (const [pattern, replacement] of rules) out = out.replace(pattern, replacement);
  out = out.replace(/[｜|].*$/, '').trim();
  if ([...out].length > max) out = [...out].slice(0, max).join('');
  return out;
}

(async () => {
  const userDataDir = path.join(process.env.HOME, '.openclaw/browser/xhs-independent-user-data');
  const assetDir = arg('asset-dir', '/tmp/openclaw/uploads/xhs_test_run/png');
  const rawTitle = arg('title', 'AI真正拉开差距的是工作流');
  const title = shortenTitle(rawTitle, 20);
  const body = arg('body', '');
  const selector = '#web > div > div > div.publish-page-container > div.publish-page-publish-btn > button.d-button.d-button-default.d-button-with-content.--color-static.bold.--color-bg-fill.--color-text-paragraph.custom-button.bg-red';

  // Ensure prior independent browser instance does not hold the profile lock.
  spawnSync('pkill', ['-f', 'xhs-independent-user-data'], { stdio: 'ignore' });
  await new Promise(r => setTimeout(r, 1500));

  const context = await chromium.launchPersistentContext(userDataDir, {
    headless: false,
    channel: 'chrome',
  });

  const page = context.pages()[0] || await context.newPage();
  await page.goto('https://creator.xiaohongshu.com/publish/publish?from=tab_switch&target=image', { waitUntil: 'domcontentloaded' });
  await page.waitForLoadState('networkidle').catch(() => {});

  let fileInput = page.locator('input[type="file"]').first();
  try {
    await fileInput.waitFor({ state: 'attached', timeout: 15000 });
  } catch {
    await page.getByText('上传图片', { exact: true }).click().catch(() => {});
    await page.waitForTimeout(1000);
    fileInput = page.locator('input[type="file"]').first();
    await fileInput.waitFor({ state: 'attached', timeout: 15000 });
  }

  const files = fs.readdirSync(assetDir).filter(f => /\.(png|jpg|jpeg|webp)$/i.test(f)).sort().map(f => path.join(assetDir, f));
  await fileInput.setInputFiles(files);
  await page.waitForTimeout(8000);

  const titleBox = page.locator('input[placeholder*="标题"], textarea[placeholder*="标题"]').first();
  await titleBox.waitFor({ state: 'visible', timeout: 30000 });
  await titleBox.fill(title);
  console.log(`TITLE_USED=${title}`);

  const editor = page.locator('[contenteditable="true"]').last();
  await editor.waitFor({ state: 'visible', timeout: 30000 });
  await editor.click();
  await page.keyboard.press(process.platform === 'darwin' ? 'Meta+A' : 'Control+A').catch(() => {});
  await page.keyboard.type(body, { delay: 8 });

  await page.waitForSelector(selector, { timeout: 20000 });
  await page.click(selector);
  await page.waitForTimeout(3000);

  const pageUrl = page.url();
  const pageText = await page.locator('body').innerText().catch(() => '');
  console.log('INDEPENDENT_PUBLISH_CLICKED');
  console.log(`PAGE_URL=${pageUrl}`);
  if (pageText.includes('标题最多输入20字')) console.log('PUBLISH_HINT=TITLE_TOO_LONG');
  if (pageText.includes('发布成功') || pageText.includes('笔记管理')) console.log('PUBLISH_STATUS=LIKELY_SUCCESS');
})();
