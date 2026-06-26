/**
 * 小红书竞品监控 - 交互式登录版本
 * 等待用户手动登录，然后开始抓取
 */

const puppeteerCore = require('puppeteer-core');
const path = require('path');

// Chrome/Chromium 路径
const CHROMIUM_PATH = process.env.CHROMIUM_PATH || null;

const randomDelay = (min, max) => Math.floor(Math.random() * (max - min + 1)) + min;
const humanWait = async (min = 1000, max = 3000) => {
  return new Promise(resolve => setTimeout(resolve, randomDelay(min, max)));
};

const waitForLogin = async (page) => {
  console.log('\n👤 请用户在小红书页面登录账号...');
  console.log('   登录成功后告诉我，我继续～\n');
  
  // 检查是否已登录 (有用户头像)
  while (true) {
    await humanWait(3000, 5000);
    
    const isLoggedIn = await page.evaluate(() => {
      // 多种检测登录状态的方式
      const avatar = document.querySelector('.avatar, [class*="avatar"], img[class*="user"]');
      const userName = document.querySelector('.username, [class*="userName"], [class*="nick"]');
      
      return {
        hasAvatar: !!avatar,
        hasUserName: !!(userName && userName.innerText),
        url: window.location.href
      };
    });
    
    console.log('检查登录状态:', JSON.stringify(isLoggedIn));
    
    if (isLoggedIn.hasAvatar || isLoggedIn.hasUserName) {
      console.log('\n✅ 检测到已登录！开始抓取...\n');
      return true;
    }
    
    // 每30秒提醒一次
    console.log('   等待登录中... (请在浏览器里登录)');
  }
};

const searchAndScrape = async (page, accountName) => {
  console.log(`\n🔍 搜索账号: ${accountName}`);
  
  try {
    // 点击搜索框
    await page.click('#search-input').catch(async () => {
      const searchArea = await page.$('.search-bar, .search-box, #search');
      if (searchArea) await searchArea.click();
    });
    
    await humanWait(500, 1000);
    
    // 输入
    await page.keyboard.type(accountName, { delay: randomDelay(80, 150) });
    await humanWait(1000, 2000);
    
    // 回车
    await page.keyboard.press('Enter');
    await humanWait(4000, 6000);
    
    // 等待搜索结果
    await page.waitForSelector('[class*="user"], .user-list-item, .author-card', { timeout: 15000 }).catch(() => null);
    
    // 点击第一个用户结果
    const userResult = await page.$('[class*="userList"] a, .user-list-item a, .author-card a, a[href*="/user/"]');
    
    if (userResult) {
      console.log('   点击用户结果...');
      await userResult.click();
      await humanWait(3000, 5000);
      
      // 获取笔记
      const notes = await getNotes(page, accountName);
      return notes;
    }
    
    console.log('   ⚠️ 未找到用户结果');
    return [];
    
  } catch (error) {
    console.log(`   ❌ 搜索出错: ${error.message}`);
    return [];
  }
};

const getNotes = async (page, accountName) => {
  console.log(`\n📄 获取 ${accountName} 的笔记...`);
  
  try {
    // 滚动加载
    for (let i = 0; i < 3; i++) {
      const dist = Math.floor(Math.random() * (600 - 300 + 1)) + 300;
      await page.evaluate((d) => window.scrollBy(0, d), dist);
      await humanWait(1500, 3000);
    }
    
    // 获取笔记链接
    const notes = await page.evaluate(() => {
      const result = [];
      const links = document.querySelectorAll('a[href*="/note/"]');
      
      links.forEach((link, i) => {
        if (i < 3) {
          const noteId = link.href.match(/\/note\/([^\/\?]+)/);
          if (noteId) {
            result.push({
              noteId: noteId[1],
              url: link.href
            });
          }
        }
      });
      
      return result;
    });
    
    console.log(`   获取到 ${notes.length} 篇笔记`);
    return notes.map(n => ({
      ...n,
      text: '', // 暂时不获取文本内容
      accountName
    }));
    
  } catch (error) {
    console.log(`   ❌ 获取笔记出错: ${error.message}`);
    return [];
  }
};

// 主函数
const main = async (accountName) => {
  console.log('========== 小红书竞品监控 ==========\n');
  
  const browser = await puppeteerCore.launch({
    executablePath: CHROMIUM_PATH,
    headless: false,
    userDataDir: path.join(__dirname, '../data/xhs-session'),
    defaultViewport: { width: 1280, height: 900 },
    args: [
      '--disable-blink-features=AutomationControlled',
      '--no-sandbox',
    ]
  });
  
  const page = await browser.newPage();
  
  // 打开小红书
  console.log('🌐 打开小红书...');
  await page.goto('https://www.xiaohongshu.com/', { 
    waitUntil: 'domcontentloaded',
    timeout: 30000 
  });
  
  // 等待登录
  await waitForLogin(page);
  
  // 开始抓取
  const notes = await searchAndScrape(page, accountName);
  
  console.log('\n========== 抓取结果 ==========');
  console.log(JSON.stringify(notes, null, 2));
  
  // 保存结果
  const fs = require('fs');
  const dataPath = path.join(__dirname, '../data/notes.json');
  fs.writeFileSync(dataPath, JSON.stringify(notes, null, 2));
  console.log(`\n📁 结果已保存到: ${dataPath}`);
  
  console.log('\n浏览器保持打开，用户可以查看～');
};

const account = process.argv[2] || '示例账号';
main(account);
