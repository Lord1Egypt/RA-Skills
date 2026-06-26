const { chromium } = require('playwright');

const CDP_WS = 'ws://127.0.0.1:9222/devtools/browser/b1422fcb-142f-4dff-852a-31953c499749';

(async () => {
  const browser = await chromium.connectOverCDP(CDP_WS);
  const pages = browser.contexts()[0]?.pages() || [];
  let page = pages.find(p => p.url().includes('goofish'));
  
  if (!page) {
    console.log('❌ 没找到闲鱼');
    await browser.close();
    return;
  }

  // 搜索数学建模
  await page.goto('https://www.goofish.com/search?keyword=数学建模', { waitUntil: 'networkidle', timeout: 15000 });
  await page.waitForTimeout(2000);
  let text = await page.innerText('body');
  let items = text.split('\n').filter(l => l.includes('¥') || l.includes('数学') || l.includes('建模') || l.includes('代写'));
  console.log('=== 数学建模搜索结果 ===');
  items.slice(0, 20).forEach(i => console.log(' ', i));
  
  console.log('\n==========\n');
  
  // 搜索 python
  await page.goto('https://www.goofish.com/search?keyword=python', { waitUntil: 'networkidle', timeout: 15000 });
  await page.waitForTimeout(2000);
  text = await page.innerText('body');
  items = text.split('\n').filter(l => l.includes('¥') || l.includes('python') || l.includes('Python') || l.includes('编程') || l.includes('代写') || l.includes('代码'));
  console.log('=== python 搜索结果 ===');
  items.slice(0, 20).forEach(i => console.log(' ', i));

  await browser.close();
})();
