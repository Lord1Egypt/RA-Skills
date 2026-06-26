const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({
    executablePath: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    headless: false
  });
  
  const context = await browser.createBrowserContext();
  const page = await context.newPage();
  
  try {
    console.log('📖 打开 apidance.pro 文档...');
    await page.goto('https://doc.apidance.pro', { waitUntil: 'networkidle' });
    console.log('✅ 文档已打开，请在浏览器中查看');
    
    // 保持浏览器开放 30 秒
    await new Promise(r => setTimeout(r, 30000));
  } catch (err) {
    console.error('❌ 错误:', err.message);
  } finally {
    await browser.close();
  }
})();
