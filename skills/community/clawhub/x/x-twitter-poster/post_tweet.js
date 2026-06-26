const { chromium } = require('playwright');

/**
 * X/Twitter 发推脚本
 * 使用 Playwright 连接用户 Chrome 并发送推文
 * 
 * 安全警告：
 * - CDP 端口可访问所有浏览器数据，请仅在信任代码时启用
 * - 建议使用单独 Chrome 账号测试
 * - Windows 请使用 Control+Enter 发送
 */

const CONFIG = {
  CDP_URL: process.env.CDP_URL || 'http://127.0.0.1:28800',
  // HOME_URL 在 postTweet 中动态构造
};

/**
 * 发送推文
 * @param {string} content - 推文内容
 * @param {string} username - X 用户名（不含 @）
 * @returns {Promise<{success: boolean, message: string}>}
 */
async function postTweet(content, username = 'woaijug') {
  console.log('🚀 Starting tweet poster...');
  console.log('   Target user:', username);
  console.log('   Content:', content.substring(0, 50) + '...');
  
  // 动态构造 HOME_URL
  const HOME_URL = `https://x.com/${username}`;
  
  // 检测平台，使用正确的发送快捷键
  const isMac = process.platform === 'darwin';
  const sendKey = isMac ? 'Meta+Enter' : 'Control+Enter';
  console.log('   Platform:', process.platform, '→ Send key:', sendKey);
  
  try {
    // 1. 连接 Chrome
    console.log('1️⃣ Connecting to Chrome...');
    const browser = await chromium.connectOverCDP(CONFIG.CDP_URL);
    const context = browser.contexts()[0];
    const page = context.pages()[0];
    console.log('   ✓ Connected, current URL:', page.url());
    
    // 2. 打开发帖页面
    console.log('2️⃣ Opening compose page...');
    await page.goto('https://x.com/compose/post');
    await page.waitForTimeout(3000);
    console.log('   ✓ Navigated');
    
    // 3. 点击输入框
    console.log('3️⃣ Clicking textarea...');
    await page.click('[data-testid="tweetTextarea_0"]');
    await page.waitForTimeout(500);
    console.log('   ✓ Clicked');
    
    // 4. 用键盘输入内容（触发 React 状态更新！）
    console.log('4️⃣ Typing content...');
    await page.keyboard.type(content, { delay: 30 });
    console.log('   ✓ Typed!');
    
    // 5. 用键盘快捷键发送（Mac: Meta+Enter, Windows/Linux: Control+Enter）
    console.log('5️⃣ Sending (' + sendKey + ')...');
    await page.keyboard.press(sendKey);
    console.log('   ✓ Sent!');
    
    // 6. 等待跳转
    await page.waitForTimeout(3000);
    console.log('6️⃣ Waiting for redirect...');
    
    // 7. 验证结果
    console.log('7️⃣ Checking result...');
    const finalUrl = page.url();
    
    if (finalUrl.includes('/home') || finalUrl.includes('/' + username)) {
      console.log('   ✓ Success! URL:', finalUrl);
      await browser.close();
      return { success: true, message: '推文发送成功！', url: finalUrl };
    } else {
      console.log('   ⚠️ Unexpected URL:', finalUrl);
      await browser.close();
      return { success: false, message: '发送状态未知，请检查', url: finalUrl };
    }
    
  } catch (error) {
    console.error('❌ Error:', error.message);
    return { success: false, message: error.message };
  }
}

/**
 * 获取用户主页最新推文
 * @param {string} username - X 用户名
 * @returns {Promise<Array>}
 */
async function getRecentTweets(username = 'woaijug') {
  try {
    const browser = await chromium.connectOverCDP(CONFIG.CDP_URL);
    const page = browser.contexts()[0].pages()[0];
    
    await page.goto(`https://x.com/${username}`);
    await page.waitForTimeout(3000);
    
    const tweets = await page.evaluate(() => {
      const items = document.querySelectorAll('[data-testid="tweet"]');
      return Array.from(items).slice(0, 5).map(t => ({
        text: t.innerText.substring(0, 150)
      }));
    });
    
    await browser.close();
    return tweets;
  } catch (error) {
    console.error('Error getting tweets:', error.message);
    return [];
  }
}

// 如果直接运行此脚本
if (require.main === module) {
  const username = process.env.X_USERNAME || 'woaijug';
  const content = process.argv[2] || '🔥 Web3 测试推文 - Skill 测试';
  postTweet(content, username)
    .then(result => {
      console.log('\n📊 Result:', result);
      process.exit(result.success ? 0 : 1);
    });
}

module.exports = { postTweet, getRecentTweets };
