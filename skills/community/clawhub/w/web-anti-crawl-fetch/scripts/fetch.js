#!/usr/bin/env node

const { chromium } = require('playwright-extra');
const stealthPlugin = require('puppeteer-extra-plugin-stealth');
const TurndownService = require('turndown');

// 注册 Stealth 插件
chromium.use(stealthPlugin());

const turndownService = new TurndownService({
  headingStyle: 'atx',
  codeBlockStyle: 'fenced'
});

// 自定义规则：忽略 base64 图片
turndownService.addRule('ignore-base64-images', {
  filter: (node) => {
    return (
      node.nodeName === 'IMG' && 
      node.getAttribute('src') && 
      node.getAttribute('src').startsWith('data:image/')
    );
  },
  replacement: () => ''
});

async function fetchUrl(url) {
  console.log(`🌐 正在获取内容: ${url}`);
  console.log('---');

  let browser;
  try {
    browser = await chromium.launch({ 
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const context = await browser.newContext({
      viewport: { width: 1920, height: 1080 }
    });
    
    const page = await context.newPage();
    page.setDefaultTimeout(60000);
    
    // 模拟真实用户行为
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
    
    // 向下滚动三次触发懒加载内容
    console.log('📜 正在向下滚动页面以加载更多内容...');
    for (let i = 0; i < 3; i++) {
      await page.evaluate(() => window.scrollBy(0, window.innerHeight));
      await page.waitForTimeout(1000);
    }
    
    // 最后等待核心内容加载完成
    await page.waitForTimeout(2000);
    
    // 提取页面内容
    const pageData = await page.evaluate(() => {
      // 移除干扰元素
      const selectors = [
        'script', 'style', 'noscript', 'iframe', 
        'ad', '.ads', '#ads',
        'img[src^="data:image/"]' // 移除 base64 图片
      ];
      
      selectors.forEach(sel => {
        document.querySelectorAll(sel).forEach(tag => tag.remove());
      });
      
      return {
        title: document.title,
        html: document.body.innerHTML
      };
    });

    console.log(`✅ 页面标题: ${pageData.title}`);
    console.log('---');
    
    // 转换为 Markdown
    const markdown = turndownService.turndown(pageData.html);
    
    if (!markdown || markdown.trim().length === 0) {
      console.log('⚠️ 无法提取到有效正文内容');
    } else {
      // 输出前 1000 个字符
      console.log(markdown.substring(0, 20000));
      if (markdown.length > 20000) {
        console.log('\n... (内容已截断)');
      }
    }
    
  } catch (error) {
    console.error(`❌ 获取内容出错: ${error.message}`);
  } finally {
    if (browser) await browser.close();
  }
}

// 主程序
const args = process.argv.slice(2);

if (args.length < 1) {
  console.log('📖 用法: node fetch.js <url>');
  console.log('\n示例:');
  console.log('  node fetch.js "https://finance.sina.com.cn/stock/"');
  process.exit(1);
}

const targetUrl = args[0];
fetchUrl(targetUrl);
