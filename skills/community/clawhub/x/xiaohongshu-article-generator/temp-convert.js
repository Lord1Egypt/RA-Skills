import puppeteer from 'puppeteer';
import { readFileSync } from 'fs';
import { fileURLToPath } from 'url';
import { dirname, join, resolve } from 'path';
import { existsSync, mkdirSync } from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// 配置
const HTML_FILE = resolve(__dirname, 'C:/Users/Administrator/.openclaw/workspace/xiaohongshu-output/test/测试话题/测试话题.html');
const OUTPUT_DIR = resolve(__dirname, 'C:/Users/Administrator/.openclaw/workspace/xiaohongshu-output/test/测试话题/images');
const PAGE_WIDTH = 375;
const PAGE_HEIGHT = 667;

// 确保输出目录存在
if (!existsSync(OUTPUT_DIR)) {
  mkdirSync(OUTPUT_DIR, { recursive: true });
}

async function convertPagesToImages() {
  console.log('🚀 开始转换页面为图片...\n');
  
  let browser;
  try {
    // 读取 HTML 文件
    console.log(`📖 读取 HTML 文件: ${HTML_FILE}`);
    const htmlContent = readFileSync(HTML_FILE, 'utf-8');
    
    // 启动浏览器
    console.log('🌐 启动浏览器...');
    browser = await puppeteer.launch({
      headless: true,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    const page = await browser.newPage();
    
    // 设置视口大小
    await page.setViewport({
      width: PAGE_WIDTH,
      height: PAGE_HEIGHT,
      deviceScaleFactor: 2 // 2x 分辨率，获得更清晰的图片
    });
    
    // 加载 HTML 内容
    await page.setContent(htmlContent, {
      waitUntil: 'networkidle0'
    });
    
    // 等待字体和样式加载
    await page.evaluateHandle(() => document.fonts.ready);
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // 获取所有页面元素
    const pageElements = await page.$$('.page');
    console.log(`📄 找到 ${pageElements.length} 个页面\n`);
    
    // 为每个页面截图
    for (let i = 0; i < pageElements.length; i++) {
      const element = pageElements[i];
      
      // 获取页面标题或编号
      const pageInfo = await page.evaluate((el) => {
        const pageNumber = el.querySelector('.page-number')?.textContent?.trim() || '';
        const sectionTitle = el.querySelector('.section-title')?.textContent?.trim() || 
                           el.querySelector('.cover-title')?.textContent?.trim() ||
                           el.querySelector('.interaction-title')?.textContent?.trim() ||
                           'page';
        return { pageNumber, sectionTitle };
      }, element);
      
      // 生成文件名
      const pageNum = pageInfo.pageNumber || String(i + 1).padStart(2, '0');
      const fileName = `page-${pageNum}.png`;
      const filePath = join(OUTPUT_DIR, fileName);
      
      // 截图
      await element.screenshot({
        path: filePath,
        type: 'png',
        omitBackground: false
      });
      
      console.log(`✅ 已保存: ${fileName} (${pageInfo.sectionTitle || '页面'})`);
    }
    
    console.log(`\n✨ 完成！所有图片已保存到: ${OUTPUT_DIR}`);
    
  } catch (error) {
    console.error('❌ 发生错误:', error);
    throw error;
  } finally {
    if (browser) {
      await browser.close();
      console.log('🔒 浏览器已关闭');
    }
  }
}

// 运行转换
convertPagesToImages().catch(console.error);
