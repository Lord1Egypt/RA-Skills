const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({
    headless: true,
    executablePath: '/usr/bin/google-chrome-stable',
    args: ['--no-sandbox', '--disable-blink-features=AutomationControlled']
  });
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36',
    locale: 'zh-CN'
  });
  const page = await context.newPage();
  await page.addInitScript(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
  });

  // 搜索数学建模相关
  await page.goto('https://www.goofish.com/search?keyword=数学建模&page=1', { waitUntil: 'networkidle', timeout: 30000 });
  let text = await page.innerText('body');
  console.log('=== 搜索"数学建模" ===');
  console.log(text.substring(0, 2000));
  console.log('\n==========\n');
  
  // 搜编程代写
  await page.goto('https://www.goofish.com/search?keyword=python代写&page=1', { waitUntil: 'networkidle', timeout: 30000 });
  text = await page.innerText('body');
  console.log('=== 搜索"python代写" ===');
  console.log(text.substring(0, 2000));
  
  await browser.close();
})();
