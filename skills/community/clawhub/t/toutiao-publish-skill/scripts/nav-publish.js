/**
 * 头条号导航脚本 - 打开发布页
 * 用法：node nav-publish.js
 */

const puppeteer = require('puppeteer-core');

(async () => {
  try {
    const browser = await puppeteer.connect({
      browserURL: 'http://127.0.0.1:28800',
      defaultViewport: null
    });

    // 查找或创建头条页面
    let page = (await browser.pages()).find(p => p.url().includes('mp.toutiao.com'));

    if (!page) {
      page = await browser.newPage();
    }

    console.log('正在导航到发布页...');
    await page.goto('https://mp.toutiao.com/profile_v4/graphic/publish', {
      waitUntil: 'networkidle2',
      timeout: 30000
    });

    console.log('当前 URL:', page.url());
    console.log('页面标题:', await page.title());

    process.exit(0);

  } catch (error) {
    console.error('ERROR:', error.message);
    process.exit(1);
  }
})();
