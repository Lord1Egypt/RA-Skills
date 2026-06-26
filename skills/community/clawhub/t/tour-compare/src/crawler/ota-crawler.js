/**
 * OTA 平台数据抓取模块
 * 
 * 支持平台：
 * - 携程 (ctrip.com)
 * - 飞猪 (fliggy.com)
 * - 同程 (ly.com)
 */

import puppeteer from 'puppeteer';
import * as cheerio from 'cheerio';

const PLATFORM_CONFIG = {
  // 携程系
  ctrip: {
    domain: 'ctrip.com',
    shortDomains: ['m.ctrip.com', 'you.ctrip.com'],
    selectors: {
      title: '.product-title, .h1-title, .title-txt',
      price: '.price, .current-price, .c-price',
      rating: '.comment-score, .rating-score, .score',
      reviewCount: '.comment-count, .review-count',
      days: '.days, .duration, .travel-day',
      hotel: '.hotel, .hotel-standard, .hotel-info',
      shoppingStops: '.shopping, .shopping-count, .shop-count'
    }
  },
  
  // 飞猪系
  fliggy: {
    domain: 'fliggy.com',
    shortDomains: ['a.feizhu.com', 'm.fliggy.com'],
    selectors: {
      title: '.product-title, .item-title, .goods-title',
      price: '.price, .current-price, .emphasize',
      rating: '.score, .rating, .point',
      reviewCount: '.comment-count, .sell-count',
      days: '.days, .duration, .trip-days',
      hotel: '.hotel, .hotel-level, .star',
      shoppingStops: '.shopping-count, .shop-count'
    }
  },
  
  // 同程系
  tongcheng: {
    domain: 'ly.com',
    shortDomains: ['m.ly.com', 'www.ly.com'],
    selectors: {
      title: '.product-title, .line-title, .t-main-title',
      price: '.price, .now-price, .c-price',
      rating: '.score, .satisfy, .mark',
      reviewCount: '.comment-count, .comment-num',
      days: '.days, .travel-days, .route-days',
      hotel: '.hotel, .hotel-info, .hotel-level',
      shoppingStops: '.shopping-count, .shop-count'
    }
  },
  
  // 马蜂窝
  mafengwo: {
    domain: 'mafengwo.cn',
    shortDomains: ['m.mafengwo.cn'],
    selectors: {
      title: '.product-title, .h1-title, .bd-title',
      price: '.price, .current-price, .num',
      rating: '.score, .rating, .star',
      reviewCount: '.comment-count, .review-num',
      days: '.days, .duration, .travel-days',
      hotel: '.hotel, .hotel-level, .star',
      shoppingStops: '.shopping-count, .shop-count'
    }
  },
  
  // 穷游
  qyer: {
    domain: 'qyer.com',
    shortDomains: ['m.qyer.com', 'product.qyer.com'],
    selectors: {
      title: '.product-title, .h1-title, .title',
      price: '.price, .current-price, .money',
      rating: '.score, .rating, .point',
      reviewCount: '.comment-count, .review-count',
      days: '.days, .duration, .travel-days',
      hotel: '.hotel, .hotel-level, .star',
      shoppingStops: '.shopping-count, .shop-count'
    }
  },
  
  // 美团旅行
  meituan: {
    domain: 'meituan.com',
    shortDomains: ['m.meituan.com', 'travel.meituan.com'],
    selectors: {
      title: '.product-title, .h1-title, .poi-name',
      price: '.price, .current-price, .money',
      rating: '.score, .rating, .point',
      reviewCount: '.comment-count, .review-count',
      days: '.days, .duration, .travel-days',
      hotel: '.hotel, .hotel-level, .star',
      shoppingStops: '.shopping-count, .shop-count'
    }
  },
  
  // 途牛
  tuniu: {
    domain: 'tuniu.com',
    shortDomains: ['m.tuniu.com', 'mobile.tuniu.com'],
    selectors: {
      title: '.product-title, .h1-title, .line-title',
      price: '.price, .current-price, .money',
      rating: '.score, .rating, .satisfy',
      reviewCount: '.comment-count, .review-count',
      days: '.days, .duration, .travel-days',
      hotel: '.hotel, .hotel-level, .star',
      shoppingStops: '.shopping-count, .shop-count'
    }
  },
  
  // 驴妈妈
  lvmama: {
    domain: 'lvmama.com',
    shortDomains: ['m.lvmama.com', 'touch.lvmama.com'],
    selectors: {
      title: '.product-title, .h1-title, .line-title',
      price: '.price, .current-price, .money',
      rating: '.score, .rating, .point',
      reviewCount: '.comment-count, .review-count',
      days: '.days, .duration, .travel-days',
      hotel: '.hotel, .hotel-level, .star',
      shoppingStops: '.shopping-count, .shop-count'
    }
  }
};

/**
 * 检测 URL 所属平台
 */
function detectPlatform(url) {
  for (const [platform, config] of Object.entries(PLATFORM_CONFIG)) {
    // 检查主域名
    if (url.includes(config.domain)) {
      return platform;
    }
    // 检查短域名
    if (config.shortDomains) {
      for (const shortDomain of config.shortDomains) {
        if (url.includes(shortDomain)) {
          return platform;
        }
      }
    }
  }
  return null;
}

/**
 * 抓取单个商品页面
 */
export async function fetchProduct(url, options = {}) {
  const { timeout = 30000, headless = true } = options;
  
  const platform = detectPlatform(url);
  if (!platform) {
    throw new Error(`不支持的平台：${url}`);
  }
  
  console.log(`🕷️  正在抓取 ${platform} 商品...`);
  
  let browser;
  try {
    browser = await puppeteer.launch({
      headless: headless ? 'new' : false,
      args: [
        '--no-sandbox',
        '--disable-setuid-sandbox',
        '--disable-dev-shm-usage'
      ]
    });
    
    const page = await browser.newPage();
    
    // 设置 User-Agent
    await page.setUserAgent('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36');
    
    // 设置超时
    await page.setDefaultNavigationTimeout(timeout);
    
    // 访问页面
    await page.goto(url, { waitUntil: 'networkidle2' });
    
    // 等待内容加载
    await page.waitForSelector('body', { timeout: 5000 });
    
    // 获取页面 HTML
    const html = await page.content();
    const $ = cheerio.load(html);
    
    // 提取商品信息
    const product = extractProductData($, platform, url);
    
    console.log(`✅ 抓取成功：${product.title}`);
    
    return product;
    
  } catch (error) {
    console.error(`❌ 抓取失败：${error.message}`);
    throw error;
  } finally {
    if (browser) {
      await browser.close();
    }
  }
}

/**
 * 从 HTML 中提取商品信息
 */
function extractProductData($, platform, url) {
  const config = PLATFORM_CONFIG[platform];
  const selectors = config.selectors;
  
  // 辅助函数：提取文本
  const getText = (selector) => {
    if (!selector) return '';
    const selectors = selector.split(',').map(s => s.trim());
    for (const sel of selectors) {
      const text = $(sel).first().text().trim();
      if (text) return text;
    }
    return '';
  };
  
  // 辅助函数：提取数字
  const getNumber = (selector) => {
    const text = getText(selector);
    const match = text.match(/[\d.]+/);
    return match ? parseFloat(match[0]) : null;
  };
  
  // 提取价格
  const priceText = getText(selectors.price);
  const price = parseInt(priceText.replace(/[^0-9]/g, '')) || null;
  
  // 提取评分
  const rating = getNumber(selectors.rating);
  
  // 提取评价数
  const reviewCount = getNumber(selectors.reviewCount);
  
  // 提取天数
  const daysText = getText(selectors.days);
  const days = parseInt(daysText.match(/(\d+)/)?.[1]) || null;
  
  // 提取酒店星级
  const hotelText = getText(selectors.hotel);
  const hotelStars = parseInt(hotelText.match(/(\d+)/)?.[1]) || null;
  const hotelStandard = hotelText.includes('钻') ? hotelText : null;
  
  // 提取购物店数量
  const shoppingText = getText(selectors.shoppingStops);
  const shoppingStops = parseInt(shoppingText.match(/(\d+)/)?.[1]) || 0;
  
  // 提取标题
  let title = getText(selectors.title);
  if (!title) {
    title = $('title').first().text().trim();
  }
  
  // 识别购物团/纯玩团
  const isPurePlay = shoppingStops === 0 || title.includes('纯玩') || title.includes('无购物');
  
  return {
    platform,
    url,
    title,
    price,
    rating,
    reviewCount,
    days,
    hotelStars,
    hotelStandard,
    shoppingStops,
    isPurePlay,
    fetchedAt: new Date().toISOString()
  };
}

/**
 * 批量抓取多个商品
 */
export async function fetchProducts(urls, options = {}) {
  const { concurrency = 3 } = options;
  
  console.log(`📦 开始批量抓取 ${urls.length} 个商品...\n`);
  
  const results = [];
  const errors = [];
  
  // 分批次抓取
  for (let i = 0; i < urls.length; i += concurrency) {
    const batch = urls.slice(i, i + concurrency);
    const promises = batch.map(url => 
      fetchProduct(url, options)
        .then(product => results.push(product))
        .catch(error => errors.push({ url, error: error.message }))
    );
    
    await Promise.all(promises);
    
    if (i + concurrency < urls.length) {
      // 避免请求过快，等待一下
      await new Promise(resolve => setTimeout(resolve, 1000));
    }
  }
  
  console.log(`\n✅ 抓取完成：成功 ${results.length} 个，失败 ${errors.length} 个`);
  
  if (errors.length > 0) {
    console.log('\n⚠️  失败列表:');
    errors.forEach(({ url, error }) => {
      console.log(`  - ${url}: ${error}`);
    });
  }
  
  return { results, errors };
}

/**
 * 从剪贴板/文本中提取 URL
 */
export function extractUrls(text) {
  const urlRegex = /https?:\/\/[^\s<>"{}|\\^`\[\]]+/gi;
  const matches = text.match(urlRegex) || [];
  
  // 去重
  return [...new Set(matches)];
}

export default {
  fetchProduct,
  fetchProducts,
  extractUrls,
  detectPlatform
};
