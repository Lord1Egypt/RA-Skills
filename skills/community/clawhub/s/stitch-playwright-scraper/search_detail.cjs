const { chromium } = require('playwright');
const CDP_WS = 'ws://127.0.0.1:9222/devtools/browser/b1422fcb-142f-4dff-852a-31953c499749';

(async () => {
  const browser = await chromium.connectOverCDP(CDP_WS);
  const pages = browser.contexts()[0]?.pages() || [];
  let page = pages.find(p => p.url().includes('goofish'));
  
  if (!page) {
    // 如果当前没有闲鱼页面，新开一个
    page = await browser.newPage();
    page.setDefaultTimeout(15000);
  }

  // 搜索"代写"
  await page.goto('https://www.goofish.com/search?keyword=代写', { waitUntil: 'domcontentloaded', timeout: 15000 });
  await page.waitForTimeout(3000);

  // 获取所有商品卡片
  const cards = await page.$$eval('[class*="card"], [class*="item"], .card-item, [class*="Card"], li', (els) => {
    return els.slice(0, 20).map(el => {
      const text = el.innerText || '';
      if (text.length < 5) return null;
      const price = text.match(/¥[\d.]+/);
      return {
        text: text.substring(0, 80).replace(/\n/g, ' | '),
        price: price ? price[0] : '无价格'
      };
    }).filter(Boolean);
  });
  
  console.log('=== "代写" 搜索结果 ===');
  cards.forEach((c, i) => console.log(` ${i+1}. [${c.price}] ${c.text}`));
  
  console.log('\n==========\n');
  
  // 搜索"数学建模"
  await page.goto('https://www.goofish.com/search?keyword=数学建模', { waitUntil: 'domcontentloaded', timeout: 15000 });
  await page.waitForTimeout(3000);
  
  const cards2 = await page.$$eval('[class*="card"], [class*="item"], .card-item, [class*="Card"], li', (els) => {
    return els.slice(0, 20).map(el => {
      const text = el.innerText || '';
      if (text.length < 5) return null;
      const price = text.match(/¥[\d.]+/);
      return {
        text: text.substring(0, 80).replace(/\n/g, ' | '),
        price: price ? price[0] : '无价格'
      };
    }).filter(Boolean);
  });
  
  console.log('=== "数学建模" 搜索结果 ===');
  cards2.forEach((c, i) => console.log(` ${i+1}. [${c.price}] ${c.text}`));

  await browser.close();
})();
