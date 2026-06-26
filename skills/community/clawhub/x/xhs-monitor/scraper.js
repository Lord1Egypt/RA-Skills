/**
 * 小红书竞品监控 - 拟人化采集引擎 V2
 * 基于 puppeteer-extra + stealth 插件
 * 优化了 selector 和错误处理
 */

const puppeteerCore = require('puppeteer-core');
const puppeteerExtra = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
const fs = require('fs');
const path = require('path');

// 使用 stealth 插件
puppeteerExtra.use(StealthPlugin());

// Chrome/Chromium 路径
// Windows: 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'
// Mac: '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
// Linux: '/usr/bin/google-chrome'
// 或使用 puppeteer 自动下载的 Chromium
const CHROMIUM_PATH = process.env.CHROMIUM_PATH || null; // 如未设置则尝试自动检测

// 反风控配置
const HUMAN_DELAY = {
  MIN_BEFORE: 1000,
  MAX_BEFORE: 3000,
  MIN_AFTER: 2000,
  MAX_AFTER: 5000,
  TYPE_CHAR: 80,
};

const randomDelay = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;

const humanWait = async (min = HUMAN_DELAY.MIN_BEFORE, max = HUMAN_DELAY.MAX_BEFORE) => {
  const delay = randomDelay(min, max);
  console.log(`  ⏳ 等待 ${delay}ms...`);
  return new Promise(resolve => setTimeout(resolve, delay));
};

const humanScroll = async (page) => {
  await page.evaluate((dist) => window.scrollBy(0, dist), randomDelay(200, 500));
  await humanWait(1000, 3000);
};

// 尝试多个 selector
const tryClick = async (page, selectors) => {
  for (const selector of selectors) {
    try {
      const element = await page.$(selector);
      if (element) {
        await element.click();
        console.log(`  ✅ 点击成功: ${selector}`);
        return true;
      }
    } catch (e) {
      // continue
    }
  }
  console.log(`  ⚠️ 未找到任何可点击元素`);
  return false;
};

// 搜索账号
const searchAccount = async (page, accountName) => {
  console.log(`\n🔍 搜索账号: ${accountName}`);
  
  try {
    // 多种方式尝试找到搜索框
    const searchInputSelectors = [
      '#search-input',
      'input[placeholder*="搜索"]',
      'input.search-input',
      '.search-input input',
      'input[type="search"]',
      'input.xs-search-input',
    ];
    
    let clicked = false;
    for (const selector of searchInputSelectors) {
      try {
        const input = await page.$(selector);
        if (input) {
          await input.click();
          clicked = true;
          console.log(`  ✅ 找到搜索框: ${selector}`);
          break;
        }
      } catch (e) {
        continue;
      }
    }
    
    if (!clicked) {
      // 尝试点击整个搜索区域
      const searchAreaSelectors = ['.search-bar', '.search-box', '#search'];
      for (const selector of searchAreaSelectors) {
        try {
          const area = await page.$(selector);
          if (area) {
            await area.click();
            await humanWait(500, 1000);
            clicked = true;
            console.log(`  ✅ 点击搜索区域: ${selector}`);
            break;
          }
        } catch (e) {
          continue;
        }
      }
    }
    
    if (!clicked) {
      console.log('  ⚠️ 未找到搜索框，尝试直接输入...');
    }
    
    await humanWait(500, 1000);
    
    // 输入账号名
    await page.keyboard.type(accountName, { delay: randomDelay(50, 150) });
    console.log(`  ✅ 输入: ${accountName}`);
    
    await humanWait(1000, 2000);
    
    // 按回车
    await page.keyboard.press('Enter');
    console.log(`  ✅ 按下回车`);
    
    await humanWait(3000, 5000);
    
    // 等待搜索结果
    await page.waitForSelector('.user-list-item, .user-list, .author-card, .search-result', { timeout: 10000 }).catch(() => null);
    
    // 获取搜索结果
    const users = await page.$$('.user-list-item, .user-list .item, .author-card, .search-user-item, [class*="user"]');
    
    if (users.length > 0) {
      const index = Math.min(randomDelay(0, Math.min(2, users.length - 1)), users.length - 1);
      console.log(`  👤 点击第 ${index + 1} 个结果 (共${users.length}个)`);
      await users[index].click();
      await humanWait(2000, 4000);
      return true;
    }
    
    console.log('  ⚠️ 未找到用户搜索结果');
    return false;
    
  } catch (error) {
    console.log(`  ❌ 搜索出错: ${error.message}`);
    return false;
  }
};

// 获取最新笔记
const getLatestNotes = async (page, accountName, maxNotes = 3) => {
  console.log(`\n📄 获取 ${accountName} 的最新笔记...`);
  
  try {
    await humanWait(2000, 4000);
    
    // 滚动加载
    for (let i = 0; i < 3; i++) {
      await humanScroll(page);
    }
    
    // 尝试多种笔记 selector
    const noteSelectors = [
      '.note-item',
      '.feed-item',
      '.post-card',
      '[class*="note-item"]',
      '[class*="feed-item"]',
      '.item',
    ];
    
    let notes = [];
    for (const selector of noteSelectors) {
      notes = await page.$$(selector);
      if (notes.length > 0) {
        console.log(`  ✅ 找到 ${notes.length} 个笔记: ${selector}`);
        break;
      }
    }
    
    if (notes.length === 0) {
      console.log('  ⚠️ 未找到笔记列表');
      return [];
    }
    
    const noteData = [];
    
    for (let i = 0; i < Math.min(maxNotes, notes.length); i++) {
      try {
        const noteInfo = await page.evaluate((el) => {
          // 尝试多种方式获取笔记链接
          const links = el.querySelectorAll('a[href*="/note/"]');
          let url = null;
          let noteId = null;
          
          for (const link of links) {
            const href = link.href;
            if (href && href.includes('/note/')) {
              url = href;
              const match = href.match(/\/note\/([^\/\?]+)/);
              noteId = match ? match[1] : null;
              break;
            }
          }
          
          // 获取文本内容
          let text = '';
          const textSelectors = ['.desc', '.content', '.title', '.text', '.note-desc', '[class*="desc"]'];
          for (const sel of textSelectors) {
            const el2 = el.querySelector(sel);
            if (el2) {
              text += el2.innerText + ' ';
            }
          }
          
          return { url, noteId, text: text.trim().substring(0, 500) };
        }, notes[i]);
        
        if (noteInfo.noteId) {
          noteData.push({
            noteId: noteInfo.noteId,
            url: noteInfo.url,
            text: noteInfo.text,
            accountName: accountName,
          });
          console.log(`  ✅ 笔记 ${i + 1}: ${noteInfo.noteId} - ${noteInfo.text.substring(0, 50)}...`);
        }
        
        await humanWait(500, 1500);
        
      } catch (err) {
        console.log(`  ❌ 获取笔记 ${i + 1} 失败: ${err.message}`);
      }
    }
    
    return noteData;
    
  } catch (error) {
    console.log(`  ❌ 获取笔记出错: ${error.message}`);
    return [];
  }
};

// 主函数
const scrapeAccount = async (accountName) => {
  let browser;
  
  try {
    console.log(`\n========== 开始采集: ${accountName} ==========`);
    
    // 启动浏览器
    browser = await puppeteerCore.launch({
      executablePath: CHROMIUM_PATH,
      headless: false,
      args: [
        '--disable-blink-features=AutomationControlled',
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage',
        '--disable-accelerated-2d-canvas',
        '--no-first-run',
        '--no-zygote',
        '--disable-gpu',
        '--disable-extensions',
        '--disable-background-networking',
        '--disable-default-apps',
        '--disable-sync',
        '--disable-translate',
        '--metrics-recording-only',
        '--mute-audio',
        '--no-report-upload',
        '--hide-scrollbars',
      ],
      userDataDir: path.join(__dirname, '../data/user-data-' + Date.now()),
      defaultViewport: { width: 1280, height: 900 },
    });
    
    const page = await browser.newPage();
    
    // 设置视口
    await page.setViewport({
      width: randomDelay(1200, 1400),
      height: randomDelay(800, 900),
      deviceScaleFactor: randomDelay(1, 2),
    });
    
    // 访问小红书
    console.log('🌐 打开小红书...');
    await page.goto('https://www.xiaohongshu.com/', {
      waitUntil: 'domcontentloaded',
      timeout: 30000,
    });
    
    await humanWait(3000, 6000);
    
    // 检查是否需要登录
    const needLogin = await page.$('text=立即登录, text=登录');
    if (needLogin) {
      console.log('  ⚠️ 检测到登录弹窗，尝试关闭...');
      const closeBtn = await page.$('.close, .icon-close, [class*="close"]');
      if (closeBtn) {
        await closeBtn.click();
        await humanWait(1000, 2000);
      }
    }
    
    // 搜索账号
    const found = await searchAccount(page, accountName);
    
    if (!found) {
      console.log('  ❌ 账号未找到');
      return [];
    }
    
    // 获取笔记
    const notes = await getLatestNotes(page, accountName);
    
    console.log(`\n========== 采集完成: ${accountName} ==========`);
    console.log(`获取到 ${notes.length} 篇笔记\n`);
    
    return notes;
    
  } catch (error) {
    console.error(`  💥 采集出错: ${error.message}`);
    return [];
  } finally {
    if (browser) {
      // await browser.close(); // 调试时保持浏览器打开
    }
  }
};

// 导出
module.exports = { scrapeAccount };

// 直接运行
if (require.main === module) {
  const accountName = process.argv[2] || '示例账号';
  scrapeAccount(accountName).then(notes => {
    console.log('\n📊 采集结果:');
    console.log(JSON.stringify(notes, null, 2));
    process.exit(0);
  });
}
