const { chromium } = require('playwright');
const CDP_WS = 'ws://127.0.0.1:9222/devtools/browser/b1422fcb-142f-4dff-852a-31953c499749';

(async () => {
  const browser = await chromium.connectOverCDP(CDP_WS);
  const pages = browser.contexts()[0]?.pages() || [];
  let page = pages.find(p => p.url().includes('goofish'));
  if (!page) page = await browser.newPage();

  // 搜索"PPT制作"
  await page.goto('https://www.goofish.com/search?q=PPT%E5%88%B6%E4%BD%9C', { waitUntil: 'networkidle', timeout: 20000 });
  await page.waitForTimeout(2000);
  
  // 等页面完全加载
  await page.waitForSelector('body', { timeout: 5000 });
  
  // 获取所有的商品卡片的原始HTML，用evaluate获取innerText里面的内容
  const items = await page.evaluate(() => {
    const results = [];
    // 各种可能的卡片选择器
    const selectors = ['[class*="card"]', '[class*="item"]', '[class*="Card"]', 'li', '[class*="title"]'];
    for (const sel of selectors) {
      const els = document.querySelectorAll(sel);
      for (const el of els) {
        const text = el.innerText || '';
        if (text.length > 5 && (text.includes('¥') || text.includes('元') || 
            text.includes('PPT') || text.includes('制作') || text.includes('代做'))) {
          results.push(text.substring(0, 100).replace(/\n/g, ' | '));
        }
      }
    }
    return [...new Set(results)].slice(0, 20);
  });
  
  console.log('=== "PPT制作" 搜索结果 ===');
  items.forEach((item, i) => console.log(` ${i+1}. ${item}`));

  console.log('\n==========\n');
  
  // 搜索"数学"
  await page.goto('https://www.goofish.com/search?q=%E6%95%B0%E5%AD%A6%E4%BB%A3%E5%86%99', { waitUntil: 'networkidle', timeout: 20000 });
  await page.waitForTimeout(2000);
  
  const items2 = await page.evaluate(() => {
    const results = [];
    const selectors = ['[class*="card"]', '[class*="item"]', '[class*="Card"]', 'li', '[class*="title"]'];
    for (const sel of selectors) {
      const els = document.querySelectorAll(sel);
      for (const el of els) {
        const text = el.innerText || '';
        if (text.length > 5) {
          results.push(text.substring(0, 100).replace(/\n/g, ' | '));
        }
      }
    }
    return [...new Set(results)].slice(0, 20);
  });
  
  console.log('=== "数学代写" 搜索结果 ===');
  items2.forEach((item, i) => console.log(` ${i+1}. ${item}`));

  await browser.close();
})();
