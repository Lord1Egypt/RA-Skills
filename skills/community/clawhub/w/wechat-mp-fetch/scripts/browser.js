const { chromium } = require('playwright');

/**
 * 浏览器管理模块
 * 负责创建和管理浏览器实例
 */

class BrowserManager {
  constructor() {
    this.browser = null;
  }

  /**
   * 创建浏览器实例
   * @returns {Promise<Browser>} 浏览器实例
   */
  async createBrowser() {
    if (!this.browser) {
      this.browser = await chromium.launch({ headless: true });
    }
    return this.browser;
  }

  /**
   * 关闭浏览器实例
   * @returns {Promise<void>}
   */
  async closeBrowser() {
    if (this.browser) {
      await this.browser.close();
      this.browser = null;
    }
  }

  /**
   * 创建新页面
   * @returns {Promise<Page>} 页面实例
   */
  async createPage() {
    const browser = await this.createBrowser();
    return await browser.newPage();
  }
}

// 导出单例实例
module.exports = new BrowserManager();
