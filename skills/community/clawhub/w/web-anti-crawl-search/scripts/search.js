#!/usr/bin/env node

const { chromium } = require('playwright-extra');
const stealthPlugin = require('puppeteer-extra-plugin-stealth');

// 注册 Stealth 插件以绕过反爬虫检测
chromium.use(stealthPlugin());

const SEARCH_ENGINES = {
  // 国内搜索引擎
  'baidu': {
    url: 'https://www.baidu.com/s?wd={keyword}',
    selectors: [
      '.result, .c-container',
      '#content_left .c-container',
      '.new-packet .c-container'
    ],
    titleSel: 'a.t, .c-title a, h3 a',
    linkSel: 'a'
  },
  'bing-cn': {
    url: 'https://cn.bing.com/search?q={keyword}',
    selectors: ['.b_algo', '#b_results .b_algo'],
    titleSel: 'h2 a, h3 a',
    linkSel: 'a'
  },
  '360': {
    url: 'https://www.so.com/s?q={keyword}',
    selectors: ['.res-list', '.result'],
    titleSel: '.res-title a, h3 a',
    linkSel: 'a'
  },
  'sogou': {
    url: 'https://sogou.com/web?query={keyword}',
    selectors: ['.vrwrap', '.rb', '.result'],
    titleSel: 'h3 a, .vr-title a',
    linkSel: 'a'
  },
  'toutiao': {
    url: 'https://so.toutiao.com/search?keyword={keyword}',
    selectors: ['.article', '.news-item', '.result'],
    titleSel: '.title, h3',
    linkSel: 'a'
  },
  // 国际搜索引擎
  'duckduckgo': {
    url: 'https://duckduckgo.com/html/?q={keyword}',
    selectors: ['.result', '.links'],
    titleSel: '.result__title, .result__a',
    linkSel: 'a'
  },
  'brave': {
    url: 'https://search.brave.com/search?q={keyword}',
    selectors: ['.snippet', '.result'],
    titleSel: 'h3, .title',
    linkSel: 'a'
  },
  'yahoo': {
    url: 'https://search.yahoo.com/search?p={keyword}',
    selectors: ['.algo', '.sr'],
    titleSel: 'h3 a, .title',
    linkSel: 'a'
  }
};

// 新闻网站直接抓取
const NEWS_SITES = {
  'sina': {
    name: '新浪财经',
    url: 'https://finance.sina.com.cn/stock/',
    selectors: ['.news-list .news-item', '.data-list .item', 'article'],
    titleSel: 'h3, .title, a',
    linkSel: 'a'
  },
  'eastmoney': {
    name: '东方财富',
    url: 'https://stock.eastmoney.com/',
    selectors: ['.news-list li', '.article-item', '.list-item'],
    titleSel: 'h3, .title, a',
    linkSel: 'a'
  },
  'tencent': {
    name: '腾讯财经',
    url: 'https://finance.qq.com/stock/',
    selectors: ['.news-list li', '.article-item'],
    titleSel: 'h3, .title',
    linkSel: 'a'
  }
};

async function search(engine, keyword) {
  // 如果是新闻网站
  if (NEWS_SITES[engine]) {
    return await fetchNews(NEWS_SITES[engine], keyword);
  }

  const engineConfig = SEARCH_ENGINES[engine.toLowerCase()];
  
  if (!engineConfig) {
    console.error(`错误: 未知的搜索引擎/新闻源 "${engine}"`);
    console.log('\n支持的搜索引擎:');
    Object.keys(SEARCH_ENGINES).forEach(e => console.log(`  - ${e}`));
    console.log('\n支持的新闻网站:');
    Object.keys(NEWS_SITES).forEach(e => console.log(`  - ${e}: ${NEWS_SITES[e].name}`));
    process.exit(1);
  }

  const url = engineConfig.url.replace('{keyword}', encodeURIComponent(keyword));
  
  console.log(`🔍 正在搜索: ${keyword}`);
  console.log(`🌐 搜索引擎: ${engine}`);
  console.log(`📎 URL: ${url}`);
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
    page.setDefaultTimeout(45000);
    
    await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
    await page.waitForTimeout(3000);
    
    // 滚动页面触发加载
    await page.evaluate(() => window.scrollTo(0, 500));
    await page.waitForTimeout(1000);
    
    // 提取搜索结果
    const results = await page.evaluate((config) => {
      const items = [];
      const seenLinks = new Set();
      
      for (const sel of config.selectors) {
        const elements = document.querySelectorAll(sel);
        
        elements.forEach((el) => {
          if (items.length >= 15) return;
          
          let title = '';
          let link = '';
          
          // 提取标题
          const titleEl = el.querySelector(config.titleSel);
          if (titleEl) {
            title = titleEl.textContent.trim();
          }
          
          if (!title) {
            const hEl = el.querySelector('h1, h2, h3, h4');
            if (hEl) title = hEl.textContent.trim();
          }
          
          if (!title) {
            title = el.innerText.split('\n')[0].trim().substring(0, 80);
          }
          
          // 提取链接
          const linkEl = el.querySelector(config.linkSel) || (el.tagName === 'A' ? el : null);
          if (linkEl && linkEl.href) {
            link = linkEl.href;
          }
          
          if (title && title.length > 2 && link && !link.includes('javascript') && !seenLinks.has(link)) {
            items.push({ title: title.substring(0, 100), link });
            seenLinks.add(link);
          }
        });
        
        if (items.length > 5) break;
      }
      
      return items;
    }, engineConfig);
    
    if (results.length === 0) {
      console.log('⚠️ 未找到搜索结果');
    } else {
      console.log(`✅ 找到 ${results.length} 条结果:\n`);
      results.forEach((r, i) => {
        console.log(`${i + 1}. ${r.title}`);
        console.log(`   🔗 ${r.link}\n`);
      });
    }
    
  } catch (error) {
    console.error(`❌ 搜索出错: ${error.message}`);
  } finally {
    if (browser) await browser.close();
  }
}

async function fetchNews(siteConfig, keyword) {
  console.log(`📰 正在获取 ${siteConfig.name} 新闻`);
  console.log(`🔍 关键词: ${keyword || '热门'}`);
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
    page.setDefaultTimeout(45000);
    
    await page.goto(siteConfig.url, { waitUntil: 'domcontentloaded', timeout: 45000 });
    await page.waitForTimeout(2000);
    
    const results = await page.evaluate((config) => {
      const items = [];
      const seenLinks = new Set();
      
      for (const sel of config.selectors) {
        const elements = document.querySelectorAll(sel);
        
        elements.forEach((el) => {
          if (items.length >= 15) return;
          
          let title = '';
          let link = '';
          
          const titleEl = el.querySelector(config.titleSel);
          if (titleEl) title = titleEl.textContent.trim();
          
          if (!title) {
            title = el.innerText.split('\n')[0].trim().substring(0, 80);
          }
          
          const linkEl = el.querySelector(config.linkSel) || (el.tagName === 'A' ? el : null);
          if (linkEl && linkEl.href) link = linkEl.href;
          
          if (title && title.length > 2 && link && !seenLinks.has(link)) {
            items.push({ title: title.substring(0, 100), link });
            seenLinks.add(link);
          }
        });
        
        if (items.length > 5) break;
      }
      
      return items;
    }, siteConfig);
    
    if (results.length === 0) {
      console.log('⚠️ 未获取到新闻');
    } else {
      console.log(`✅ 获取到 ${results.length} 条新闻:\n`);
      results.forEach((r, i) => {
        console.log(`${i + 1}. ${r.title}`);
        console.log(`   🔗 ${r.link}\n`);
      });
    }
    
  } catch (error) {
    console.error(`❌ 获取新闻出错: ${error.message}`);
  } finally {
    if (browser) await browser.close();
  }
}

// 主程序
const args = process.argv.slice(2);

if (args.length < 2) {
  console.log('📖 用法: node search.js <engine> <keyword>');
  console.log('\n示例:');
  console.log('  node search.js baidu "瑞幸咖啡"');
  console.log('  node search.js 360 "A股今日走势"');
  console.log('  node search.js duckduckgo "stock market news"');
  console.log('\n支持的搜索引擎:');
  Object.keys(SEARCH_ENGINES).forEach(e => console.log(`  - ${e}`));
  console.log('\n支持的新闻网站:');
  Object.keys(NEWS_SITES).forEach(e => console.log(`  - ${e}: ${NEWS_SITES[e].name}`));
  process.exit(1);
}

const engine = args[0];
const keyword = args.slice(1).join(' ');

search(engine, keyword);