#!/usr/bin/env node
/**
 * Twitter/X 发推脚本
 * 支持：纯文字、图片、线程
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

require('dotenv').config();

class TwitterPoster {
  constructor() {
    this.username = process.env.TWITTER_USERNAME;
    this.password = process.env.TWITTER_PASSWORD;
    this.email = process.env.TWITTER_EMAIL;
    this.browser = null;
    this.page = null;
  }

  async init() {
    if (!this.username || !this.password) {
      console.error('❌ 请先配置 TWITTER_USERNAME 和 TWITTER_PASSWORD');
      process.exit(1);
    }

    this.browser = await puppeteer.launch({
      headless: false,
      args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    this.page = await this.browser.newPage();
    await this.page.setViewport({ width: 1280, height: 800 });
  }

  async login() {
    console.log('🔐 正在登录...');
    await this.page.goto('https://twitter.com/login', { waitUntil: 'networkidle2' });
    
    // 输入用户名
    await this.page.waitForSelector('input[autocomplete="username"]', { timeout: 10000 });
    await this.page.type('input[autocomplete="username"]', this.username);
    await this.page.keyboard.press('Enter');
    
    // 可能需要输入邮箱
    try {
      await this.page.waitForSelector('input[data-testid="ocfEnterTextTextInput"]', { timeout: 3000 });
      await this.page.type('input[data-testid="ocfEnterTextTextInput"]', this.email);
      await this.page.keyboard.press('Enter');
    } catch (e) {
      // 不需要邮箱验证
    }
    
    // 输入密码
    await this.page.waitForSelector('input[name="password"]', { timeout: 10000 });
    await this.page.type('input[name="password"]', this.password);
    await this.page.keyboard.press('Enter');
    
    await this.page.waitForNavigation({ waitUntil: 'networkidle2' });
    console.log('✅ 登录成功');
  }

  async post(text, imagePath = null) {
    console.log(`📝 正在发布: ${text.substring(0, 50)}...`);
    
    // 点击发推按钮
    await this.page.waitForSelector('[data-testid="tweetButtonInline"], a[href="/compose/tweet"]', { timeout: 10000 });
    
    // 打开发推界面
    const composeBtn = await this.page.$('a[href="/compose/tweet"]');
    if (composeBtn) await composeBtn.click();
    
    // 等待发推框
    await this.page.waitForSelector('[data-testid="tweetTextarea_0"]', { timeout: 10000 });
    
    // 输入内容
    await this.page.type('[data-testid="tweetTextarea_0"]', text);
    
    // 如果有图片，上传
    if (imagePath && fs.existsSync(imagePath)) {
      const fileInput = await this.page.$('input[type="file"]');
      if (fileInput) {
        await fileInput.uploadFile(imagePath);
        await this.page.waitForTimeout(2000); // 等待上传
      }
    }
    
    // 点击发送
    await this.page.waitForTimeout(1000);
    await this.page.click('[data-testid="tweetButton"]');
    await this.page.waitForTimeout(3000);
    
    console.log('✅ 推文发布成功');
  }

  async postThread(tweets) {
    console.log(`🧵 正在发布 ${tweets.length} 条线程...`);
    
    for (let i = 0; i < tweets.length; i++) {
      if (i > 0) {
        // 点击"添加另一条"按钮
        await this.page.click('[data-testid="addButton"]');
        await this.page.waitForTimeout(1000);
      }
      
      const textarea = await this.page.$(`[data-testid="tweetTextarea_${i}"]`);
      if (textarea) {
        await textarea.type(tweets[i]);
      }
    }
    
    // 发送整个线程
    await this.page.click('[data-testid="tweetButton"]');
    await this.page.waitForTimeout(3000);
    
    console.log('✅ 线程发布成功');
  }

  async close() {
    if (this.browser) {
      await this.browser.close();
    }
  }
}

// 主程序
async function main() {
  const args = process.argv.slice(2);
  
  const poster = new TwitterPoster();
  
  try {
    await poster.init();
    await poster.login();
    
    // 解析参数
    const imageIndex = args.indexOf('--image');
    const threadIndex = args.indexOf('--thread');
    
    if (threadIndex !== -1) {
      // 线程模式
      const tweets = args.slice(threadIndex + 1).join(' ').split('|').map(t => t.trim());
      await poster.postThread(tweets);
    } else if (imageIndex !== -1) {
      // 图片模式
      const imagePath = args[imageIndex + 1];
      const text = args.filter((_, i) => i !== imageIndex && i !== imageIndex + 1).join(' ');
      await poster.post(text, imagePath);
    } else {
      // 纯文字
      const text = args.join(' ');
      await poster.post(text);
    }
    
  } catch (error) {
    console.error('❌ 错误:', error.message);
  } finally {
    await poster.close();
  }
}

main();
