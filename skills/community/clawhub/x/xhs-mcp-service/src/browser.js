/**
 * Browser Manager Module
 * Manages Puppeteer browser instance and page operations
 */

import puppeteer from 'puppeteer';
import fs from 'fs/promises';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);
const COOKIES_PATH = path.join(__dirname, '..', 'data', 'cookies.json');

/**
 * 浏览器管理类
 */
export class BrowserManager {
  constructor(options = {}) {
    this.browser = null;
    this.page = null;
    this.headless = options.headless !== false; // 默认无头模式
    this.proxy = options.proxy || process.env.XHS_PROXY || null;
  }

  /**
   * 初始化浏览器
   */
  async init() {
    if (this.browser) {
      return this.browser;
    }

    const launchOptions = {
      headless: this.headless,
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-blink-features=AutomationControlled',
        '--disable-web-security',
        '--disable-features=IsolateOrigins,site-per-process',
      ],
      defaultViewport: {
        width: 1280,
        height: 800,
      },
    };

    // 配置代理
    if (this.proxy) {
      launchOptions.args.push(`--proxy-server=${this.proxy}`);
    }

    this.browser = await puppeteer.launch(launchOptions);
    this.page = await this.browser.newPage();

    // 设置 User-Agent
    await this.page.setUserAgent(
      'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    );

    // 加载 cookies
    await this.loadCookies();

    return this.browser;
  }

  /**
   * 获取页面实例
   */
  async getPage() {
    if (!this.page) {
      await this.init();
    }
    return this.page;
  }

  /**
   * 加载 cookies
   */
  async loadCookies() {
    try {
      const cookiesString = await fs.readFile(COOKIES_PATH, 'utf-8');
      const cookies = JSON.parse(cookiesString);
      await this.page.setCookie(...cookies);
      console.error('✅ Cookies 加载成功');
    } catch (error) {
      console.error('⚠️  未找到 cookies 文件，需要登录');
    }
  }

  /**
   * 保存 cookies
   */
  async saveCookies() {
    const cookies = await this.page.cookies();
    await fs.mkdir(path.dirname(COOKIES_PATH), { recursive: true });
    await fs.writeFile(COOKIES_PATH, JSON.stringify(cookies, null, 2));
    console.error('✅ Cookies 保存成功');
  }

  /**
   * 删除 cookies
   */
  async deleteCookies() {
    try {
      await fs.unlink(COOKIES_PATH);
      console.error('✅ Cookies 删除成功');
      return true;
    } catch (error) {
      console.error('⚠️  删除 cookies 失败:', error.message);
      return false;
    }
  }

  /**
   * 检查 cookies 是否存在
   */
  async hasCookies() {
    try {
      await fs.access(COOKIES_PATH);
      return true;
    } catch {
      return false;
    }
  }

  /**
   * 关闭浏览器
   */
  async close() {
    if (this.browser) {
      await this.browser.close();
      this.browser = null;
      this.page = null;
    }
  }
}

// 单例实例
let browserInstance = null;

/**
 * 获取浏览器实例（单例）
 */
export async function getBrowser(options = {}) {
  if (!browserInstance) {
    browserInstance = new BrowserManager(options);
    await browserInstance.init();
  }
  return browserInstance;
}

/**
 * 关闭浏览器实例
 */
export async function closeBrowser() {
  if (browserInstance) {
    await browserInstance.close();
    browserInstance = null;
  }
}
