const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/usr/bin/google-chrome-stable',
    args: ['--no-sandbox', '--disable-blink-features=AutomationControlled']
  });
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    viewport: { width: 1280, height: 800 },
    locale: 'zh-CN'
  });
  const page = await context.newPage();
  await page.addInitScript(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
  });

  // 打开闲鱼
  await page.goto('https://www.goofish.com', { waitUntil: 'networkidle', timeout: 30000 });
  let text = await page.innerText('body');
  console.log('=== 页面文字（前1000字）===');
  console.log(text.substring(0, 1000));
  console.log('...');
  console.log('\n=== 页面标题 ===');
  console.log(await page.title());
  await browser.close();
})();
