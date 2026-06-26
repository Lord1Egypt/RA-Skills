/**
 * 小红书竞品监控 - 守护进程
 * 保持浏览器持续运行，不关闭
 */

const puppeteerCore = require('puppeteer-core');
const path = require('path');

// Chrome/Chromium 路径
const CHROMIUM_PATH = process.env.CHROMIUM_PATH || null;
const USER_DATA_DIR = path.join(__dirname, '../data/browser-session');
const PAGE_URL = 'https://www.xiaohongshu.com/';

let browser = null;
let page = null;

const initBrowser = async () => {
  try {
    console.log('🚀 启动浏览器...');
    
    browser = await puppeteerCore.launch({
      executablePath: CHROMIUM_PATH,
      headless: false,
      userDataDir: USER_DATA_DIR,
      defaultViewport: { width: 1280, height: 900 },
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
      ]
    });
    
    page = await browser.newPage();
    
    console.log('🌐 打开小红书...');
    await page.goto(PAGE_URL, { waitUntil: 'networkidle2' });
    
    console.log('✅ 浏览器已就绪！');
    console.log('========================================');
    console.log('请用户在浏览器中操作：');
    console.log('1. 扫码登录小红书');
    console.log('2. 搜索要监控的账号');
    console.log('3. 告诉美绪"好了"开始抓取');
    console.log('========================================');
    
    // 监听页面关闭
    browser.on('disconnected', () => {
      console.log('⚠️ 浏览器断开连接，5秒后重新启动...');
      setTimeout(initBrowser, 5000);
    });
    
  } catch (error) {
    console.error('❌ 启动失败:', error.message);
    console.log('5秒后重试...');
    setTimeout(initBrowser, 5000);
  }
};

// 导出一个控制接口
const getPage = () => page;
const getBrowser = () => browser;

module.exports = { getPage, getBrowser, initBrowser };

// 如果直接运行
if (require.main === module) {
  initBrowser();
  
  // 保持进程
  setInterval(() => {}, 100000);
}
