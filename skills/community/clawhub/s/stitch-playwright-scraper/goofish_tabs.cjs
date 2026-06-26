const { chromium } = require('playwright');
const CDP_WS = 'ws://127.0.0.1:9222/devtools/browser/b1422fcb-142f-4dff-852a-31953c499749';

(async () => {
  const browser = await chromium.connectOverCDP(CDP_WS);
  const pages = browser.contexts()[0]?.pages() || [];
  let page = pages.find(p => p.url().includes('goofish'));
  if (!page) page = await browser.newPage();

  // 先看首页是什么结构
  await page.goto('https://www.goofish.com/', { waitUntil: 'networkidle', timeout: 20000 });
  
  // 获取页面所有可点击的链接/按钮
  const clickables = await page.$$eval('a, button, [role="button"], [role="tab"], [role="menuitem"]', els => {
    return els.slice(0, 50).map(el => ({
      text: (el.innerText || el.textContent || '').trim().substring(0, 30),
      href: (el.href || '').substring(0, 80),
      role: el.getAttribute('role') || el.tagName
    })).filter(e => e.text || e.href);
  });
  
  console.log('=== 首页可点击元素 ===');
  clickables.slice(0, 30).forEach((c,i) => console.log(` ${i+1}. [${c.role}] ${c.text || '无文字'} ${c.href ? '→ '+c.href : ''}`));

  // 看看能不能找到"技能"或者"服务"的入口
  const allText = await page.innerText('body');
  const relevant = allText.split('\n').filter(l => 
    l.includes('技能') || l.includes('服务') || l.includes('服务') || 
    l.includes('代写') || l.includes('接单') || l.includes('数学')
  );
  console.log('\n=== 相关文字 ===');
  relevant.forEach((l,i) => console.log(` ${i+1}. ${l.substring(0,60)}`));

  await browser.close();
})();
