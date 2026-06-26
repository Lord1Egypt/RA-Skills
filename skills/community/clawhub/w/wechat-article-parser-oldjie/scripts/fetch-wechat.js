// 微信公众号文章抓取脚本
const { chromium } = require('playwright');
const cheerio = require('cheerio');

const CONTENT_SELECTOR = '#js_content';
const TITLE_SELECTOR = '#activity-name';
const AUTHOR_SELECTOR = '#js_name';
const TIME_SELECTOR = '#publish_time';

const WECHAT_UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 MicroMessenger/7.0.20.1781 NetType/WIFI MiniProgramEnv/Windows WindowsWechat/WMPF XWEB/8559';

// 从命令行参数获取 URL
const url = process.argv[2];

if (!url) {
  console.error('用法: node fetch-wechat.js <公众号文章链接>');
  console.error('示例: node fetch-wechat.js https://mp.weixin.qq.com/s/0d8x55t1t-SWQzG7jck7Pw');
  process.exit(1);
}

if (!url.includes('mp.weixin.qq.com')) {
  console.error('错误：请提供有效的微信公众号链接（mp.weixin.qq.com域名）');
  process.exit(1);
}

async function parseArticle() {
  let browser = null;
  try {
    browser = await chromium.launch({ headless: true });
    const page = await browser.newPage({
      userAgent: WECHAT_UA,
      javaScriptEnabled: true,
    });

    console.log('正在打开页面...');
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 30000 });
    await page.waitForTimeout(8000);
    await page.waitForSelector(CONTENT_SELECTOR, { timeout: 15000 });

    const html = await page.content();
    const $ = cheerio.load(html);

    const title = $(TITLE_SELECTOR).text().trim();
    const author = $(AUTHOR_SELECTOR).text().trim();
    const publishTime = $(TIME_SELECTOR).text().trim();
    const content = $(CONTENT_SELECTOR).text().trim().replace(/\s+/g, '\n\n');

    await browser.close();

    console.log(`标题：${title}`);
    console.log(`作者：${author}`);
    console.log(`发布时间：${publishTime}`);
    console.log('---正文---');
    console.log(content);

  } catch (error) {
    if (browser) await browser.close();
    console.error('解析失败:', error.message);
  }
}

parseArticle();
