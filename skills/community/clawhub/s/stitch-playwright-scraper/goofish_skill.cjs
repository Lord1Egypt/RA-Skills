const { chromium } = require('playwright');
const CDP_WS = 'ws://127.0.0.1:9222/devtools/browser/b1422fcb-142f-4dff-852a-31953c499749';

(async () => {
  const browser = await chromium.connectOverCDP(CDP_WS);
  const pages = browser.contexts()[0]?.pages() || [];
  let page = pages.find(p => p.url().includes('goofish'));
  if (!page) page = await browser.newPage();

  // 直接看技能频道
  await page.goto('https://www.goofish.com/category?tag=技能', { waitUntil: 'domcontentloaded', timeout: 15000 });
  await page.waitForTimeout(3000);
  
  console.log('=== 技能频道 ===');
  let text = await page.innerText('body');
  let lines = text.split('\n').filter(l => l.trim().length > 2).map(l => l.trim());
  lines.slice(0, 40).forEach((l,i) => console.log(` ${i+1}. ${l}`));
  
  console.log('\n==========\n');
  
  // 看看页面里有没有服务列表
  await page.goto('https://www.goofish.com/category?tag=代写', { waitUntil: 'domcontentloaded', timeout: 15000 });
  await page.waitForTimeout(3000);
  
  console.log('=== 代写频道 ===');
  text = await page.innerText('body');
  lines = text.split('\n').filter(l => l.trim().length > 2).map(l => l.trim());
  lines.slice(0, 40).forEach((l,i) => console.log(` ${i+1}. ${l}`));
  
  await browser.close();
})();
