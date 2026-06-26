/**
 * 截图 OCR 识别模块
 * 
 * 功能：
 * - 识别用户上传的旅游商品截图
 * - 提取关键信息（价格、评分、标题、酒店等）
 * - 支持携程/飞猪/同程等主流 OTA 平台
 * 
 * 技术栈：
 * - Tesseract.js - OCR 文字识别
 * - 正则表达式 - 信息提取
 */

import Tesseract from 'tesseract.js';

/**
 * 从截图提取商品信息
 * @param {string} imagePath - 图片路径
 * @returns {Promise<Object>} 商品信息
 */
export async function recognizeProductFromImage(imagePath) {
  try {
    console.log('🔍 开始识别截图...');
    
    // OCR 识别
    const { data: { text } } = await Tesseract.recognize(
      imagePath,
      'chi_sim+eng',
      {
        logger: m => {
          if (m.status === 'recognizing text') {
            console.log(`识别进度：${Math.round(m.progress * 100)}%`);
          }
        }
      }
    );
    
    console.log('✅ OCR 识别完成');
    
    // 解析文本提取信息
    const product = parseProductInfo(text);
    
    return {
      success: true,
      text,
      product
    };
    
  } catch (error) {
    console.error('❌ OCR 识别失败:', error.message);
    return {
      success: false,
      error: error.message
    };
  }
}

/**
 * 从 OCR 文本解析商品信息
 */
function parseProductInfo(text) {
  const product = {
    platform: detectPlatformFromText(text),
    title: '',
    price: null,
    rating: null,
    reviewCount: null,
    shoppingStops: 0,
    hotelStars: null,
    days: null,
    features: []
  };
  
  // 提取价格（匹配 ¥ 或 元）
  const priceMatch = text.match(/[¥￥]\s*(\d+(?:\.\d+)?)/i) || text.match(/(\d+(?:\.\d+)?)\s*元/i);
  if (priceMatch) {
    product.price = parseFloat(priceMatch[1]);
  }
  
  // 提取评分（匹配 X.X 分）
  const ratingMatch = text.match(/(\d\.\d)\s*分/i);
  if (ratingMatch) {
    product.rating = parseFloat(ratingMatch[1]);
  }
  
  // 提取评价数
  const reviewMatch = text.match(/(\d+(?:,\d{3})*|\d+)\s*条评价/i);
  if (reviewMatch) {
    product.reviewCount = parseInt(reviewMatch[1].replace(/,/g, ''));
  }
  
  // 提取天数（匹配 X 天 X 晚）
  const daysMatch = text.match(/(\d+)\s*天\s*(\d+)\s*晚/i);
  if (daysMatch) {
    product.days = parseInt(daysMatch[1]);
    product.nights = parseInt(daysMatch[2]);
  }
  
  // 提取酒店星级
  const hotelMatch = text.match(/(\d+)\s*钻/i) || text.match(/(\d+)\s*星级/i);
  if (hotelMatch) {
    product.hotelStars = parseInt(hotelMatch[1]);
  }
  
  // 提取购物店数量
  const shoppingMatch = text.match(/(\d+)\s*个购物店/i) || text.match(/(\d+)\s*个购物/i);
  if (shoppingMatch) {
    product.shoppingStops = parseInt(shoppingMatch[1]);
  }
  
  // 检测是否纯玩
  if (text.includes('纯玩') || text.includes('无购物')) {
    product.shoppingStops = 0;
    product.features.push('纯玩无购物');
  }
  
  // 提取其他特征
  if (text.includes('小团')) {
    product.features.push('小团出行');
    const groupMatch = text.match(/(\d+)\s*人小团/i);
    if (groupMatch) {
      product.groupSize = parseInt(groupMatch[1]);
    }
  }
  
  if (text.includes('独立团')) {
    product.features.push('独立团');
  }
  
  if (text.includes('全额退') || text.includes('随时退')) {
    product.features.push('灵活退改');
  }
  
  if (text.includes('赠保险') || text.includes('送保险')) {
    product.features.push('赠保险');
  }
  
  // 提取标题（取第一行非空文本）
  const lines = text.split('\n').filter(line => line.trim().length > 2 && line.trim().length < 50);
  if (lines.length > 0) {
    product.title = lines[0].trim();
  }
  
  return product;
}

/**
 * 从文本识别平台
 */
function detectPlatformFromText(text) {
  if (text.includes('携程') || text.includes('ctrip')) {
    return 'ctrip';
  }
  if (text.includes('飞猪') || text.includes('fliggy') || text.includes('阿里旅行')) {
    return 'fliggy';
  }
  if (text.includes('同程') || text.includes('ly.com') || text.includes('艺龙')) {
    return 'tongcheng';
  }
  return 'unknown';
}

/**
 * 批量识别多张截图
 */
export async function recognizeMultipleImages(imagePaths) {
  const results = [];
  
  for (let i = 0; i < imagePaths.length; i++) {
    console.log(`\n正在识别第 ${i + 1}/${imagePaths.length} 张截图...`);
    const result = await recognizeProductFromImage(imagePaths[i]);
    results.push({
      index: i + 1,
      ...result
    });
  }
  
  return results;
}

/**
 * 对比两张截图的商品信息
 */
export async function compareImages(imagePath1, imagePath2) {
  console.log('📊 开始对比两张截图...\n');
  
  const [result1, result2] = await Promise.all([
    recognizeProductFromImage(imagePath1),
    recognizeProductFromImage(imagePath2)
  ]);
  
  if (!result1.success || !result2.success) {
    return {
      success: false,
      error: '部分截图识别失败'
    };
  }
  
  return {
    success: true,
    product1: result1.product,
    product2: result2.product
  };
}

export default {
  recognizeProductFromImage,
  recognizeMultipleImages,
  compareImages
};
