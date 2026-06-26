/**
 * 商品对比引擎
 * 核心对比逻辑和评分算法
 */

import { getPersona, getDefaultWeights } from '../config/personas.js';

/**
 * 对比多个商品
 * @param {Array} products - 商品列表
 * @param {string} group - 人群类型
 * @returns {Object} 对比结果
 */
export function compareProducts(products, group = null) {
  const persona = group ? getPersona(group) : null;
  
  // 计算每个商品的评分
  const scoredProducts = products.map(product => ({
    ...product,
    score: calculateScore(product, persona),
    breakdown: calculateBreakdown(product, persona),
    pros: analyzePros(product),
    cons: analyzeCons(product)
  }));
  
  // 排序
  scoredProducts.sort((a, b) => b.score - a.score);
  
  // 找出各维度最佳
  const bestInCategory = findBestInCategory(scoredProducts);
  
  // 生成推荐语
  const recommendation = generateRecommendation(scoredProducts, persona);
  
  // 避坑提醒
  const warnings = generateWarnings(scoredProducts);
  
  // 深度对比分析
  const deepComparison = generateDeepComparison(scoredProducts, persona);
  
  return {
    products: scoredProducts,
    bestInCategory,
    recommendation,
    warnings,
    group,
    deepComparison
  };
}

/**
 * 计算综合评分
 */
function calculateScore(product, persona) {
  const weights = persona ? persona.weights : getDefaultWeights();
  
  let score = 0;
  let totalWeight = 0;
  
  // 价格分（越低越好，归一化到 0-100）
  if (weights.price && product.price) {
    const priceScore = Math.max(0, 100 - (product.price / 100));
    score += priceScore * Math.abs(weights.price);
    totalWeight += Math.abs(weights.price);
  }
  
  // 评分分（直接转换）
  if (weights.rating && product.rating) {
    const ratingScore = product.rating * 20; // 5 分制 → 100 分制
    score += ratingScore * weights.rating;
    totalWeight += weights.rating;
  }
  
  // 购物店扣分
  if (weights.shoppingStops && product.shoppingStops !== undefined) {
    const shoppingScore = Math.max(0, 100 - (product.shoppingStops * 20));
    score += shoppingScore * Math.abs(weights.shoppingStops);
    totalWeight += Math.abs(weights.shoppingStops);
  }
  
  // 酒店星级
  if (weights.hotel && product.hotelStars) {
    const hotelScore = product.hotelStars * 20; // 5 星制 → 100 分制
    score += hotelScore * weights.hotel;
    totalWeight += weights.hotel;
  }
  
  // 归一化到 0-100
  return totalWeight > 0 ? Math.round(score / totalWeight) : 0;
}

/**
 * 计算各维度得分明细
 */
function calculateBreakdown(product, persona) {
  return {
    price: product.price ? Math.max(0, 100 - (product.price / 100)) : null,
    rating: product.rating ? product.rating * 20 : null,
    shopping: product.shoppingStops !== undefined ? Math.max(0, 100 - (product.shoppingStops * 20)) : null,
    hotel: product.hotelStars ? product.hotelStars * 20 : null
  };
}

/**
 * 找出各维度最佳商品
 */
function findBestInCategory(products) {
  const best = {};
  
  // 价格最低
  const cheapest = products.reduce((min, p) => 
    (!min || (p.price && p.price < min.price)) ? p : min, null);
  if (cheapest) best.price = cheapest;
  
  // 评分最高
  const highestRated = products.reduce((max, p) => 
    (!max || (p.rating && p.rating > max.rating)) ? p : max, null);
  if (highestRated) best.rating = highestRated;
  
  // 购物店最少
  const leastShopping = products.reduce((min, p) => 
    (!min || (p.shoppingStops !== undefined && p.shoppingStops < min.shoppingStops)) ? p : min, null);
  if (leastShopping) best.shopping = leastShopping;
  
  // 酒店最好
  const bestHotel = products.reduce((max, p) => 
    (!max || (p.hotelStars && p.hotelStars > max.hotelStars)) ? p : max, null);
  if (bestHotel) best.hotel = bestHotel;
  
  return best;
}

/**
 * 生成推荐语
 */
function generateRecommendation(products, persona) {
  if (products.length === 0) return null;
  
  const top = products[0];
  const reasons = [];
  
  if (top.rating >= 4.5) reasons.push('评分高');
  if (top.shoppingStops === 0) reasons.push('0 购物纯玩');
  if (top.price < 3000) reasons.push('性价比高');
  if (top.hotelStars >= 4) reasons.push('酒店品质好');
  
  let summary = `推荐"${top.title}"`;
  if (reasons.length > 0) {
    summary += ` - ${reasons.join('、')}`;
  }
  
  if (persona) {
    summary += `，适合${persona.name}出行`;
  }
  
  return {
    summary,
    productId: top.id || top.platform,
    reasons
  };
}

/**
 * 分析商品优点
 */
function analyzePros(product) {
  const pros = [];
  
  // 价格优势
  if (product.price && product.price < 600) {
    pros.push({ type: '价格', message: '价格亲民，性价比高', weight: 3 });
  }
  
  // 评分优势
  if (product.rating && product.rating >= 4.9) {
    pros.push({ type: '口碑', message: '评分极高，口碑优秀', weight: 3 });
  } else if (product.rating && product.rating >= 4.5) {
    pros.push({ type: '口碑', message: '评分良好，用户认可', weight: 2 });
  }
  
  // 纯玩优势
  if (product.shoppingStops === 0) {
    pros.push({ type: '体验', message: '纯玩无购物，体验好', weight: 3 });
  }
  
  // 小团优势
  if (product.groupSize && product.groupSize <= 6) {
    pros.push({ type: '体验', message: '小团出行，更自由', weight: 2 });
  } else if (product.groupSize && product.groupSize <= 15) {
    pros.push({ type: '体验', message: '小团出行，人少体验好', weight: 1 });
  }
  
  // 好评率优势
  if (product.goodRate) {
    const rate = parseFloat(product.goodRate);
    if (rate >= 98) {
      pros.push({ type: '口碑', message: `好评率${product.goodRate}，几乎零差评`, weight: 2 });
    } else if (rate >= 95) {
      pros.push({ type: '口碑', message: `好评率${product.goodRate}，口碑不错`, weight: 1 });
    }
  }
  
  // 保障优势
  if (product.features && product.features.includes('无自费')) {
    pros.push({ type: '保障', message: '无自费项目，透明消费', weight: 2 });
  }
  if (product.features && product.features.includes('赠保险')) {
    pros.push({ type: '保障', message: '赠送旅游险，有保障', weight: 1 });
  }
  if (product.features && product.features.includes('全额退')) {
    pros.push({ type: '保障', message: '支持全额退改，灵活性好', weight: 2 });
  }
  
  // 销量优势
  if (product.sales && product.sales >= 300) {
    pros.push({ type: '热度', message: '销量高，受欢迎', weight: 1 });
  }
  
  return pros;
}

/**
 * 分析商品缺点
 */
function analyzeCons(product) {
  const cons = [];
  
  // 评价数少
  if (product.reviewCount && product.reviewCount < 50) {
    cons.push({ type: '参考性', message: `评价数较少 (${product.reviewCount}条)，参考性有限`, weight: 2 });
  }
  
  // 酒店标准低
  if (product.hotelStars && product.hotelStars <= 3) {
    cons.push({ type: '住宿', message: '酒店标准一般', weight: 1 });
  }
  
  // 行程紧张
  if (product.days && product.days <= 4) {
    cons.push({ type: '行程', message: '行程较短，可能走马观花', weight: 1 });
  }
  
  // 缺少特色
  if (!product.features || product.features.length === 0) {
    cons.push({ type: '特色', message: '缺少特色服务', weight: 1 });
  }
  
  return cons;
}

/**
 * 生成深度对比分析
 */
function generateDeepComparison(products, persona) {
  if (products.length < 2) return null;
  
  const [top1, top2] = products;
  
  const analysis = {
    priceGap: null,
    ratingGap: null,
    valueAnalysis: [],
    scenarioRecommendations: [],
    decisionFactors: []
  };
  
  // 价格差距分析
  if (top1.price && top2.price) {
    const gap = Math.abs(top1.price - top2.price);
    const percentage = Math.round((gap / Math.max(top1.price, top2.price)) * 100);
    analysis.priceGap = {
      absolute: gap,
      percentage,
      cheaper: top1.price < top2.price ? top1 : top2
    };
  }
  
  // 评分差距
  if (top1.rating && top2.rating) {
    analysis.ratingGap = {
      gap: Math.abs(top1.rating - top2.rating),
      better: top1.rating > top2.rating ? top1 : top2
    };
  }
  
  // 性价比分析
  if (top1.price && top2.price) {
    const value1 = top1.score / top1.price * 1000;
    const value2 = top2.score / top2.price * 1000;
    
    if (value1 > value2 * 1.1) {
      analysis.valueAnalysis.push({
        product: top1.title,
        message: '性价比明显更高',
        score: Math.round(value1)
      });
    } else if (value2 > value1 * 1.1) {
      analysis.valueAnalysis.push({
        product: top2.title,
        message: '性价比明显更高',
        score: Math.round(value2)
      });
    } else {
      analysis.valueAnalysis.push({
        message: '两者性价比接近',
        score1: Math.round(value1),
        score2: Math.round(value2)
      });
    }
  }
  
  // 场景化推荐
  const cheapest = products.reduce((min, p) => (p.price && (!min || p.price < min.price)) ? p : min, null);
  const highestRated = products.reduce((max, p) => (p.rating && (!max || p.rating > max.rating)) ? p : max, null);
  const purePlay = products.find(p => p.shoppingStops === 0);
  const smallGroup = products.find(p => p.groupSize && p.groupSize <= 6);
  
  analysis.scenarioRecommendations = [
    {
      scenario: '追求性价比',
      recommendation: cheapest || products[0],
      reason: cheapest ? '价格最低' : '综合最优'
    },
    {
      scenario: '追求品质',
      recommendation: highestRated || products[0],
      reason: highestRated ? '评分最高' : '综合最优'
    },
    {
      scenario: '带老人/小孩',
      recommendation: purePlay || products[0],
      reason: purePlay ? '纯玩无购物，轻松不累' : '综合最优'
    },
    {
      scenario: '年轻人/朋友出行',
      recommendation: smallGroup || products[0],
      reason: smallGroup ? '小团自由，体验更好' : '综合最优'
    }
  ];
  
  // 决策因素
  const decisionFactors = [];
  
  if (analysis.priceGap && analysis.priceGap.percentage > 20) {
    decisionFactors.push({
      factor: '价格差距大',
      description: `相差¥${analysis.priceGap.absolute} (${analysis.priceGap.percentage}%)`,
      suggestion: '预算有限选便宜的，追求品质选贵的'
    });
  }
  
  if (analysis.ratingGap && analysis.ratingGap.gap >= 0.3) {
    decisionFactors.push({
      factor: '评分差距明显',
      description: `相差${analysis.ratingGap.gap}分`,
      suggestion: '优先选择评分高的，口碑更可靠'
    });
  }
  
  const purePlayCount = products.filter(p => p.shoppingStops === 0).length;
  if (purePlayCount === 1) {
    decisionFactors.push({
      factor: '纯玩优势',
      description: '仅 1 个纯玩团',
      suggestion: '纯玩团体验更好，避免购物浪费时间'
    });
  }
  
  const hasSmallGroup = products.find(p => p.groupSize && p.groupSize <= 6);
  if (hasSmallGroup) {
    decisionFactors.push({
      factor: '小团优势',
      description: `${hasSmallGroup.groupSize}人小团`,
      suggestion: '人少更自由，导游照顾更周到'
    });
  }
  
  analysis.decisionFactors = decisionFactors;
  
  return analysis;
}

/**
 * 生成避坑提醒
 */
function generateWarnings(products) {
  const warnings = [];
  
  products.forEach(product => {
    // 低价团警告
    if (product.price && product.price < 2000 && product.days && product.days >= 5) {
      warnings.push({
        product: product.title,
        type: '低价团',
        message: '价格过低，可能含有购物或自费项目',
        severity: 'high'
      });
    }
    
    // 购物店多警告
    if (product.shoppingStops && product.shoppingStops >= 3) {
      warnings.push({
        product: product.title,
        type: '购物团',
        message: `含${product.shoppingStops}个购物店，注意隐形消费`,
        severity: 'high'
      });
    }
    
    // 评分低警告
    if (product.rating && product.rating < 4.0) {
      warnings.push({
        product: product.title,
        type: '低评分',
        message: `评分仅${product.rating}，用户反馈较差`,
        severity: 'medium'
      });
    }
    
    // 准 X 钻警告
    if (product.hotelStandard && product.hotelStandard.includes('准')) {
      warnings.push({
        product: product.title,
        type: '非官方星级',
        message: '"准 X 钻"非官方星级，实际可能低一档',
        severity: 'medium'
      });
    }
    
    // 评价数少警告
    if (product.reviewCount && product.reviewCount < 20) {
      warnings.push({
        product: product.title,
        type: '参考性有限',
        message: `评价数仅${product.reviewCount}条，数据参考性有限`,
        severity: 'low'
      });
    }
    
    // 好评率低于 90%
    if (product.goodRate) {
      const rate = parseFloat(product.goodRate);
      if (rate < 90) {
        warnings.push({
          product: product.title,
          type: '好评率低',
          message: `好评率${product.goodRate}，低于平均水平`,
          severity: 'medium'
        });
      }
    }
  });
  
  return warnings;
}
