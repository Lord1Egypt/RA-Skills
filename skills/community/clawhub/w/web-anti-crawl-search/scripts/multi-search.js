#!/usr/bin/env node

/**
 * 多搜索引擎对照搜索脚本
 * 同时搜索Google和Bing，进行对照验证
 * 如果Google访问失败，使用夸克AI搜索替代
 */

const { chromium } = require('playwright-extra');
const stealthPlugin = require('puppeteer-extra-plugin-stealth');

// 注册 Stealth 插件以绕过反爬虫检测
chromium.use(stealthPlugin());

// 搜索引擎配置
const SEARCH_ENGINES = {
  'google': {
    name: 'Google',
    url: 'https://www.google.com/search?q={keyword}&num=10',
    selectors: [
      '#search .g',
      '#rso .g',
      '.g .yuRUbf',
      '[data-ved] .g'
    ],
    titleSel: 'h3, .DKV0Md, .LC20lb',
    linkSel: 'a[href^="http"]',
    snippetSel: '.VwiC3b, .s3v94d, .st, .IsZvec'
  },
  'bing': {
    name: 'Bing',
    url: 'https://www.bing.com/search?q={keyword}&count=10',
    selectors: [
      '.b_algo',
      '#b_results .b_algo',
      '.b_algo h2'
    ],
    titleSel: 'h2 a, .b_algo h2',
    linkSel: 'a[href^="http"]',
    snippetSel: '.b_caption p, .b_algo p'
  },
  'quark': {
    name: '夸克AI搜索',
    url: 'https://quark.sm.cn/s?q={keyword}&from=smor&safe=1',
    selectors: [
      '.result',
      '.result-item',
      '.res-list'
    ],
    titleSel: '.title, h3 a, .res-title',
    linkSel: 'a[href^="http"]',
    snippetSel: '.des, .res-desc, .abstract'
  }
};

/**
 * 延迟函数
 */
function delay(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

/**
 * 启动浏览器
 */
async function launchBrowser() {
  return await chromium.launch({
    headless: true,
    args: [
      '--no-sandbox',
      '--disable-setuid-sandbox',
      '--disable-dev-shm-usage',
      '--disable-accelerated-2d-canvas',
      '--disable-gpu',
      '--window-size=1920,1080'
    ]
  });
}

/**
 * 执行搜索
 */
async function performSearch(browser, engineKey, keyword, timeout = 30000) {
  const engine = SEARCH_ENGINES[engineKey];
  if (!engine) {
    throw new Error(`未知的搜索引擎: ${engineKey}`);
  }

  const url = engine.url.replace('{keyword}', encodeURIComponent(keyword));
  const results = [];
  let page;

  try {
    console.log(`🔍 [${engine.name}] 正在搜索: ${keyword}`);
    
    const context = await browser.newContext({
      viewport: { width: 1920, height: 1080 },
      userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    });
    
    page = await context.newPage();
    page.setDefaultTimeout(timeout);
    page.setDefaultNavigationTimeout(timeout);

    // 访问搜索页面
    await page.goto(url, { 
      waitUntil: 'domcontentloaded',
      timeout: timeout 
    });
    
    // 等待页面加载
    await delay(3000);
    
    // 滚动页面触发懒加载
    await page.evaluate(() => window.scrollTo(0, 800));
    await delay(1000);
    
    // 提取搜索结果
    const extractedResults = await page.evaluate((config) => {
      const items = [];
      const seenLinks = new Set();
      
      for (const selector of config.selectors) {
        const elements = document.querySelectorAll(selector);
        
        elements.forEach((el) => {
          if (items.length >= 10) return;
          
          let title = '';
          let link = '';
          let snippet = '';
          
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
            title = el.innerText.split('\n')[0].trim().substring(0, 100);
          }
          
          // 提取链接
          const linkEl = el.querySelector(config.linkSel) || (el.tagName === 'A' ? el : el.querySelector('a'));
          if (linkEl && linkEl.href) {
            link = linkEl.href;
          }
          
          // 提取摘要
          if (config.snippetSel) {
            const snippetEl = el.querySelector(config.snippetSel);
            if (snippetEl) {
              snippet = snippetEl.textContent.trim().substring(0, 300);
            }
          }
          
          if (title && title.length > 3 && link && !link.includes('javascript') && !seenLinks.has(link)) {
            items.push({ 
              title: title.substring(0, 120), 
              link,
              snippet: snippet.substring(0, 300)
            });
            seenLinks.add(link);
          }
        });
        
        if (items.length >= 5) break;
      }
      
      return items;
    }, engine);
    
    results.push(...extractedResults);
    
    console.log(`✅ [${engine.name}] 找到 ${extractedResults.length} 条结果`);
    
    await context.close();
    
  } catch (error) {
    console.error(`❌ [${engine.name}] 搜索出错: ${error.message}`);
    if (page) {
      try {
        await page.context().close();
      } catch (e) {}
    }
  }
  
  return results;
}

/**
 * 合并和对照搜索结果
 */
function mergeResults(googleResults, bingResults, quarkResults) {
  const merged = [];
  const seenLinks = new Set();
  const seenTitles = new Set();
  
  // 辅助函数：添加结果
  const addResult = (result, source) => {
    const normalizedLink = result.link.split('?')[0].replace(/\/+$/, '');
    const normalizedTitle = result.title.toLowerCase().trim();
    
    // 去重检查
    if (seenLinks.has(normalizedLink) || seenTitles.has(normalizedTitle)) {
      // 如果已存在，添加来源标记
      const existing = merged.find(r => 
        r.link.split('?')[0].replace(/\/+$/, '') === normalizedLink
      );
      if (existing && !existing.sources.includes(source)) {
        existing.sources.push(source);
      }
      return;
    }
    
    seenLinks.add(normalizedLink);
    seenTitles.add(normalizedTitle);
    
    merged.push({
      ...result,
      sources: [source]
    });
  };
  
  // 按优先级添加结果（交替添加，确保多样性）
  const maxLen = Math.max(
    googleResults.length, 
    bingResults.length, 
    quarkResults.length
  );
  
  for (let i = 0; i < maxLen; i++) {
    if (googleResults[i]) addResult(googleResults[i], 'Google');
    if (bingResults[i]) addResult(bingResults[i], 'Bing');
    if (quarkResults[i]) addResult(quarkResults[i], '夸克AI');
  }
  
  return merged;
}

/**
 * 主函数
 */
async function main() {
  const args = process.argv.slice(2);
  
  if (args.length < 1) {
    console.log('📖 用法: node multi-search.js <keyword> [options]');
    console.log('\n选项:');
    console.log('  --google-only    仅使用Google搜索');
    console.log('  --bing-only      仅使用Bing搜索');
    console.log('  --quark-only     仅使用夸克AI搜索');
    console.log('  --max-results=N  最多返回N条结果 (默认20)');
    console.log('  --format=md|json 输出格式 (默认md)');
    console.log('\n示例:');
    console.log('  node multi-search.js "A股今日走势"');
    console.log('  node multi-search.js "人工智能新闻" --max-results=30 --format=json');
    process.exit(1);
  }
  
  const keyword = args[0];
  const options = {
    googleOnly: args.includes('--google-only'),
    bingOnly: args.includes('--bing-only'),
    quarkOnly: args.includes('--quark-only'),
    maxResults: 20,
    format: 'md'
  };
  
  // 解析参数
  args.forEach(arg => {
    if (arg.startsWith('--max-results=')) {
      options.maxResults = parseInt(arg.split('=')[1]) || 20;
    }
    if (arg.startsWith('--format=')) {
      options.format = arg.split('=')[1] || 'md';
    }
  });
  
  console.log('='.repeat(60));
  console.log('🔍 多搜索引擎对照搜索');
  console.log('='.repeat(60));
  console.log(`关键词: ${keyword}`);
  console.log(`最大结果: ${options.maxResults}`);
  console.log(`输出格式: ${options.format}`);
  console.log('='.repeat(60));
  console.log();
  
  let browser;
  let googleResults = [];
  let bingResults = [];
  let quarkResults = [];
  
  try {
    browser = await launchBrowser();
    
    // Google搜索
    if (!options.bingOnly && !options.quarkOnly) {
      console.log('🌐 开始 Google 搜索...');
      console.log('-'.repeat(40));
      googleResults = await performSearch(browser, 'google', keyword);
      
      if (googleResults.length === 0) {
        console.log('⚠️ Google 搜索失败或无结果，将使用夸克AI作为替代');
        console.log('-'.repeat(40));
        quarkResults = await performSearch(browser, 'quark', keyword);
      }
      console.log();
    }
    
    // Bing搜索
    if (!options.googleOnly && !options.quarkOnly) {
      console.log('🌐 开始 Bing 搜索...');
      console.log('-'.repeat(40));
      bingResults = await performSearch(browser, 'bing', keyword);
      console.log();
    }
    
    // 夸克AI搜索（如果Google失败且没有禁用）
    if (!options.googleOnly && !options.bingOnly && quarkResults.length === 0 && googleResults.length === 0) {
      console.log('🌐 开始 夸克AI 搜索（Google替代）...');
      console.log('-'.repeat(40));
      quarkResults = await performSearch(browser, 'quark', keyword);
      console.log();
    }
    
  } catch (error) {
    console.error('❌ 搜索过程出错:', error.message);
  } finally {
    if (browser) {
      await browser.close();
    }
  }
  
  // 合并结果
  console.log('='.repeat(60));
  console.log('📊 搜索结果统计');
  console.log('='.repeat(60));
  console.log(`Google: ${googleResults.length} 条`);
  console.log(`Bing: ${bingResults.length} 条`);
  console.log(`夸克AI: ${quarkResults.length} 条`);
  console.log('='.repeat(60));
  console.log();
  
  const mergedResults = mergeResults(googleResults, bingResults, quarkResults);
  
  // 限制结果数量
  const finalResults = mergedResults.slice(0, options.maxResults);
  
  // 输出结果
  if (options.format === 'json') {
    console.log(JSON.stringify({
      keyword,
      summary: {
        google: googleResults.length,
        bing: bingResults.length,
        quark: quarkResults.length,
        merged: finalResults.length
      },
      results: finalResults
    }, null, 2));
  } else {
    console.log('='.repeat(60));
    console.log(`🔍 "${keyword}" 搜索结果（共 ${finalResults.length} 条）`);
    console.log('='.repeat(60));
    console.log();
    
    finalResults.forEach((r, i) => {
      const sources = r.sources ? r.sources.join(' + ') : 'Unknown';
      console.log(`${i + 1}. ${r.title}`);
      console.log(`   🔗 ${r.link}`);
      if (r.snippet) {
        console.log(`   📝 ${r.snippet.substring(0, 150)}${r.snippet.length > 150 ? '...' : ''}`);
      }
      console.log(`   📌 来源: ${sources}`);
      console.log();
    });
    
    console.log('='.repeat(60));
  }
}

// 运行主程序
main().catch(console.error);