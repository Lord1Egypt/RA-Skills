const { chromium } = require('playwright');
const CDP_WS = 'ws://127.0.0.1:9222/devtools/browser/b1422fcb-142f-4dff-852a-31953c499749';

(async () => {
  const browser = await chromium.connectOverCDP(CDP_WS);
  const pages = browser.contexts()[0]?.pages() || [];
  let page = pages.find(p => p.url().includes('goofish'));
  if (!page) page = await browser.newPage();

  // 直接访问首页，找技能分类
  await page.goto('https://www.goofish.com/', { waitUntil: 'networkidle', timeout: 20000 });
  
  // 获取导航分类链接
  const categories = await page.$$eval('a[href*="category"], a[href*="tag"]', els => {
    return els.map(el => ({
      text: (el.innerText || '').trim().substring(0, 30),
      href: (el.href || '').substring(0, 100)
    })).filter(e => e.text || e.href);
  });
  console.log('=== 分类链接 ===');
  categories.forEach((c,i) => console.log(` ${i+1}. ${c.text} → ${c.href}`));

  // 看看是否有"技能"标签的分类
  console.log('\n=== 点击"技能"分类 ===');
  const skillLinks = await page.$$('a');
  for (const link of skillLinks) {
    const text = await link.innerText();
    if (text.trim() === '技能') {
      console.log('找到"技能"链接，点击...');
      await link.click();
      await page.waitForTimeout(3000);
      break;
    }
  }
  
  const bodyText = await page.innerText('body');
  const lines = bodyText.split('\n').filter(l => l.trim().length > 3).map(l => l.trim());
  lines.slice(0, 50).forEach((l,i) => console.log(` ${i+1}. ${l.substring(0,80)}`));
  
  // 获取当前 URL
  console.log('\n当前URL:', page.url());

  await browser.close();
})();
