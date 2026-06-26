const { chromium } = require('playwright');

const CDP_WS_URL = 'ws://127.0.0.1:9222/devtools/browser/b1422fcb-142f-4dff-852a-31953c499749';

(async () => {
  // 通过 CDP 连接到 Windows Chrome
  const browser = await chromium.connectOverCDP(CDP_WS_URL);
  
  // 获取所有页面
  const contexts = browser.contexts();
  const pages = contexts[0]?.pages() || [];
  
  console.log('=== 当前标签页 ===');
  for (const page of pages) {
    const title = await page.title();
    const url = page.url();
    console.log(`  📄 ${title.substring(0,50)}`);
    console.log(`     ${url.substring(0,80)}`);
  }

  // 找到闲鱼页面
  let goofishPage = pages.find(p => p.url().includes('goofish'));
  
  if (goofishPage) {
    console.log('\n=== 闲鱼页面内容 ===');
    await goofishPage.bringToFront();
    
    // 看导航栏
    const navText = await goofishPage.innerText('.nav-items, nav, header').catch(() => '');
    console.log(' 导航:', navText.substring(0, 300));
    
    // 搜搜索框
    const hasSearch = await goofishPage.$('input[placeholder*="搜索"]');
    console.log(' 有搜索框:', !!hasSearch);
    
    // 搜"技能/卡券"分类
    const bodyText = await goofishPage.innerText('body');
    const lines = bodyText.split('\n').filter(l => l.includes('技能') || l.includes('服务') || l.includes('代写'));
    console.log('\n 相关分类:', lines.slice(0, 10));
    
  } else {
    console.log('\n❌ 没找到闲鱼页面，请先打开 goofish.com');
  }
  
  await browser.close();
})();
