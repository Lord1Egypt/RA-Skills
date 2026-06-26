/**
 * 闲鱼浏览器自动化核心库
 * 提供与闲鱼网页版交互的基础功能
 */

const path = require('path');

/**
 * 闲鱼发布页面URL
 */
const XIANYU_PUBLISH_URL = 'https://2.taobao.com/publish/xianyu';

/**
 * 闲鱼商品列表页面
 */
const XIANYU_LIST_URL = 'https://2.taobao.com/commodity/manage/listing';

/**
 * 闲鱼首页
 */
const XIANYU_HOME_URL = 'https://2.taobao.com/';

/**
 * 登录页面
 */
const LOGIN_URL = 'https://login.taobao.com';

class XianyuBrowser {
  /**
   * @param {Object} browser - 浏览器实例
   */
  constructor(browser) {
    this.browser = browser;
    this.page = null;
  }

  /**
   * 初始化页面
   */
  async init() {
    this.page = await this.browser.newPage();
    await this.page.setViewport({ width: 1280, height: 800 });
  }

  /**
   * 登录闲鱼
   * @param {Function} onScanQRCode - 扫码回调
   */
  async login(onScanQRCode) {
    console.log('打开登录页面...');
    await this.page.goto(LOGIN_URL, { waitUntil: 'networkidle' });
    
    // 等待二维码出现
    await this.page.waitForSelector('.qrcode', { timeout: 10000 });
    
    // 获取二维码图片
    const qrcodeData = await this.page.evaluate(() => {
      const img = document.querySelector('.qrcode img');
      return img ? img.src : null;
    });
    
    if (onScanQRCode && qrcodeData) {
      onScanQRCode(qrcodeData);
    }
    
    // 等待登录成功
    try {
      await this.page.waitForSelector('.shop-name, .user-nick', { timeout: 60000 });
      console.log('登录成功!');
      return true;
    } catch (e) {
      console.log('登录超时，请重试');
      return false;
    }
  }

  /**
   * 打开发布页面
   */
  async goToPublishPage() {
    console.log('打开发布页面...');
    await this.page.goto(XIANYU_PUBLISH_URL, { waitUntil: 'networkidle' });
    
    // 检查是否需要登录
    const needLogin = await this.page.evaluate(() => {
      return window.location.href.includes('login');
    });
    
    if (needLogin) {
      throw new Error('请先登录');
    }
    
    return true;
  }

  /**
   * 填写商品信息
   * @param {Object} product - 商品信息
   */
  async fillProduct(product) {
    const { title, price, description, category, tags } = product;
    
    // 填写标题
    console.log('填写标题...');
    await this.page.type('input[placeholder*="标题"]', title, { delay: 100 });
    
    // 填写价格
    console.log('填写价格...');
    await this.page.type('input[placeholder*="价格"]', price.toString(), { delay: 100 });
    
    // 填写描述
    if (description) {
      console.log('填写描述...');
      await this.page.type('textarea[placeholder*="描述"]', description, { delay: 50 });
    }
    
    // 选择类目
    if (category) {
      console.log('选择类目...');
      await this.selectCategory(category);
    }
    
    // 添加标签
    if (tags && tags.length > 0) {
      console.log('添加标签...');
      await this.addTags(tags);
    }
    
    return true;
  }

  /**
   * 选择商品类目
   * @param {string} category - 类目名称
   */
  async selectCategory(category) {
    const categoryMap = {
      '手机': '50013820',
      '电脑': '50013822',
      '相机': '50013824',
      '耳机': '50013825',
      '图书': '50014812',
      '服装': '50014809',
      '鞋': '50014810',
      '包': '50014811'
    };
    
    const categoryId = categoryMap[category] || category;
    
    // 点击类目选择器
    await this.page.click('.category-selector');
    await this.page.waitForSelector('.category-list');
    
    // 选择类目
    await this.page.evaluate((catId) => {
      const items = document.querySelectorAll('.category-item');
      for (const item of items) {
        if (item.dataset.categoryId === catId) {
          item.click();
          return true;
        }
      }
    }, categoryId);
  }

  /**
   * 添加商品标签
   * @param {Array<string>} tags - 标签数组
   */
  async addTags(tags) {
    for (const tag of tags) {
      await this.page.type('input[placeholder*="标签"]', tag, { delay: 100 });
      await this.page.waitForTimeout(500);
      // 按回车确认
      await this.page.press('Enter');
    }
  }

  /**
   * 上传商品图片
   * @param {Array<string>} imagePaths - 图片路径数组
   */
  async uploadImages(imagePaths) {
    console.log(`上传 ${imagePaths.length} 张图片...`);
    
    // 点击上传按钮
    await this.page.click('.upload-btn');
    await this.page.waitForSelector('input[type="file"]', { visible: true });
    
    // 选择文件上传
    const input = await this.page.$('input[type="file"]');
    
    for (const imagePath of imagePaths) {
      await input.uploadFile(imagePath);
      await this.page.waitForTimeout(1000);
    }
    
    // 等待图片上传完成
    await this.page.waitForSelector('.upload-progress[data-complete="true"]', { timeout: 30000 });
    
    console.log('图片上传完成');
    return true;
  }

  /**
   * 发布商品
   */
  async publish() {
    console.log('点击发布按钮...');
    await this.page.click('button:has-text("发布")');
    
    // 等待发布成功
    try {
      await this.page.waitForSelector('.success-tips, .publish-success', { timeout: 15000 });
      console.log('商品发布成功!');
      return true;
    } catch (e) {
      // 检查是否有错误
      const error = await this.page.evaluate(() => {
        const errEl = document.querySelector('.error-tips, .publish-error');
        return errEl ? errEl.textContent : null;
      });
      
      if (error) {
        console.error(`发布失败: ${error}`);
        throw new Error(error);
      }
      
      throw new Error('发布超时');
    }
  }

  /**
   * 获取商品列表
   * @param {string} status - 状态: selling/sold/removed
   */
  async getProductList(status = 'selling') {
    console.log(`获取商品列表: ${status}`);
    
    await this.page.goto(XIANYU_LIST_URL, { waitUntil: 'networkidle' });
    
    // 等待商品列表加载
    await this.page.waitForSelector('.commodity-list, .item-list', { timeout: 10000 });
    
    // 提取商品信息
    const items = await this.page.evaluate((statusFilter) => {
      const itemEls = document.querySelectorAll('.commodity-item, .item');
      const items = [];
      
      for (const el of itemEls) {
        const status = el.dataset.status || el.querySelector('.status')?.textContent;
        
        if (statusFilter && status !== statusFilter) continue;
        
        const title = el.querySelector('.title, .item-title')?.textContent?.trim();
        const price = el.querySelector('.price, .item-price')?.textContent?.trim();
        const id = el.dataset.itemId || el.dataset.id;
        
        if (title && id) {
          items.push({ id, title, price, status });
        }
      }
      
      return items;
    }, status);
    
    return items;
  }

  /**
   * 下架商品
   * @param {string} itemId - 商品ID
   */
  async unpublish(itemId) {
    console.log(`下架商品: ${itemId}`);
    
    // 找到对应商品
    const itemEl = await this.page.$(`[data-item-id="${itemId}"], [data-id="${itemId}"]`);
    
    if (!itemEl) {
      throw new Error(`商品不存在: ${itemId}`);
    }
    
    // 点击下架按钮
    await itemEl.click();
    await this.page.waitForTimeout(500);
    
    // 确认下架
    await this.page.click('button:has-text("确认下架"), button:has-text("确定")');
    await this.page.waitForTimeout(1000);
    
    console.log('商品已下架');
    return true;
  }

  /**
   * 获取商品详情
   * @param {string} itemId - 商品ID
   */
  async getProductDetail(itemId) {
    console.log(`获取商品详情: ${itemId}`);
    
    const detailUrl = `https://2.taobao.com/commodity/detail/${itemId}`;
    await this.page.goto(detailUrl, { waitUntil: 'networkidle' });
    
    // 提取商品详情
    const detail = await this.page.evaluate(() => {
      const title = document.querySelector('.title, h1')?.textContent?.trim();
      const price = document.querySelector('.price, .product-price')?.textContent?.trim();
      const desc = document.querySelector('.description, .detail')?.textContent?.trim();
      
      return { title, price, description: desc };
    });
    
    return { ...detail, id: itemId };
  }

  /**
   * 刷新商品曝光
   * @param {string} itemId - 商品ID
   */
  async refreshItem(itemId) {
    console.log(`刷新商品曝光: ${itemId}`);
    
    // 打开商品编辑页面
    const editUrl = `https://2.taobao.com/commodity/edit/${itemId}`;
    await this.page.goto(editUrl, { waitUntil: 'networkidle' });
    
    // 点击刷新按钮
    await this.page.click('button:has-text("刷新"), .refresh-btn');
    await this.page.waitForTimeout(1000);
    
    console.log('刷新成功');
    return true;
  }

  /**
   * 关闭浏览器
   */
  async close() {
    if (this.page) {
      await this.page.close();
    }
  }
}

/**
 * 导出
 */
module.exports = { XianyuBrowser };

// 如果直接运行此文件
if (require.main === module) {
  console.log(`
闲鱼浏览器自动化库
------------------
用法: const { XianyuBrowser } = require('./lib/xianyu-browser');
      
      const browser = await puppeteer.launch();
      const xianyu = new XianyuBrowser(browser);
      await xianyu.init();
      await xianyu.login();
`);
}