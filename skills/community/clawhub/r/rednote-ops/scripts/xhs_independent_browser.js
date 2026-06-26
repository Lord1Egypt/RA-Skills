const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const userDataDir = path.join(process.env.HOME, '.openclaw/browser/xhs-independent-user-data');
  const context = await chromium.launchPersistentContext(userDataDir, {
    headless: false,
    channel: 'chrome',
  });
  const page = context.pages()[0] || await context.newPage();
  await page.goto('https://creator.xiaohongshu.com/publish/publish?from=tab_switch&target=image', { waitUntil: 'domcontentloaded' });
  console.log('XHS_INDEPENDENT_BROWSER_READY');
  console.log(`USER_DATA_DIR=${userDataDir}`);
})();
