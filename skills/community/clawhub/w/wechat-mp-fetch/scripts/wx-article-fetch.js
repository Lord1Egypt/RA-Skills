const { program } = require('commander');
const browserManager = require('./browser');
const { validateWeChatUrl, validateUrlFormat } = require('./validator');
const { extractAll } = require('./extractor');
const { format } = require('./formatter');

/**
 * 微信公众号文章抓取
 * 
 * 使用方式：
 *   node wx-article-fetch.js <url>
 *   node wx-article-fetch.js --url <url> --format <format>
 * 
 * 参数：
 *   url - 微信公众号文章链接（mp.weixin.qq.com/s/xxx）
 *   format - 输出格式（json, markdown），默认为 json
 *   timeout - 超时时间（毫秒），默认为 30000
 *   debug - 启用调试模式
 */

// 解析命令行参数
program
  .version('1.0.1')
  .description('WeChat Article Fetch Tool')
  .option('-u, --url <url>', 'WeChat article URL')
  .option('-f, --format <format>', 'Output format (json, markdown)', 'json')
  .option('-t, --timeout <ms>', 'Timeout in milliseconds', '30000')
  .option('-d, --debug', 'Enable debug mode')
  .parse(process.argv);

const options = program.opts();

// 获取URL（优先使用命令行参数，其次使用位置参数）
let url = options.url || process.argv[2];

async function fetchArticle() {
  // 验证URL
  if (!url) {
    console.error('错误: 请提供微信公众号文章链接');
    console.error('用法: node wx-article-fetch.js <url>');
    console.error('或: node wx-article-fetch.js --url <url> --format <format>');
    process.exit(1);
  }
  
  if (!validateUrlFormat(url)) {
    console.error('错误: 请提供有效的URL格式');
    process.exit(1);
  }
  
  if (!validateWeChatUrl(url)) {
    console.error('错误: 请提供有效的微信公众号文章链接（mp.weixin.qq.com/s/xxx）');
    process.exit(1);
  }

  let page = null;
  
  try {
    // 创建页面
    page = await browserManager.createPage();
    
    // 设置超时
    const timeout = parseInt(options.timeout) || 30000;
    
    // 访问URL
    if (options.debug) {
      console.log(`正在访问: ${url}`);
      console.log(`超时设置: ${timeout}ms`);
    }
    
    await page.goto(url, { timeout });
    await page.waitForFunction(() => !document.URL.includes('login') && document.readyState === 'complete', { timeout: timeout / 2 });
    
    try {
      await page.waitForSelector('#js_content', { timeout: timeout / 2 });
    } catch {
      console.error('错误: 无法加载文章内容（可能需要登录或文章已删除）');
      return {
        success: false,
        error: '无法加载文章内容（可能需要登录或文章已删除）'
      };
    }
    
    // 提取内容
    if (options.debug) {
      console.log('正在提取文章内容...');
    }
    
    const data = await extractAll(page);
    
    // 格式化输出
    const result = {
      success: true,
      ...data
    };
    
    console.log(format(result, options.format));
    
    return result;
    
  } catch (error) {
    console.error(`错误: 抓取失败 - ${error.message}`);
    return {
      success: false,
      error: error.message
    };
  } finally {
    // 关闭页面
    if (page) {
      await page.close();
    }
  }
}

// 执行抓取
(async () => {
  try {
    await fetchArticle();
  } catch (error) {
    console.error(`错误: ${error.message}`);
  } finally {
    // 关闭浏览器
    await browserManager.closeBrowser();
  }
})();
