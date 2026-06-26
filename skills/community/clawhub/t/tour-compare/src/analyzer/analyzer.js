/**
 * 商品深度分析引擎
 */

import { getPersona } from '../config/personas.js';

// 避坑规则库
const redFlags = [
  { keyword: '低价团', warning: '必有购物或自费项目，实际花费可能翻倍', severity: 'high' },
  { keyword: '准 X 钻', warning: '非官方星级，实际可能低一档', severity: 'medium' },
  { keyword: '车览', warning: '车上观看，不能下车游览', severity: 'medium' },
  { keyword: '远观', warning: '远距离观看，不进景点', severity: 'medium' },
  { keyword: '途经', warning: '路过不停靠', severity: 'low' },
  { keyword: '自理', warning: '费用不含，需额外支付', severity: 'medium' },
  { keyword: '赠送', warning: '可能强制消费或质量差', severity: 'medium' },
  { keyword: '视情况而定', warning: '可能无法安排，无保障', severity: 'low' }
];

/**
 * 深度分析单个商品
 */
export function analyzeProduct(product, options = {}) {
  const { deep = false } = options;
  
  const analysis = {
    product,
    score: calculateOverallScore(product),
    pros: [],
    cons: [],
    warnings: [],
    hiddenCosts: [],
    suggestions: []
  };
  
  // 价格分析
  analyzePrice(product, analysis);
  
  // 行程分析
  analyzeItinerary(product, analysis);
  
  // 住宿分析
  analyzeAccommodation(product, analysis);
  
  // 评价分析
  analyzeRating(product, analysis);
  
  // 避坑检查
  checkRedFlags(product, analysis);
  
  // 深度分析
  if (deep) {
    performDeepAnalysis(product, analysis);
  }
  
  // 生成建议
  generateSuggestions(product, analysis);
  
  return analysis;
}

function calculateOverallScore(product) {
  let score = 50; // 基础分
  
  // 价格（适中最好）
  if (product.price) {
    if (product.price < 2000) score -= 10; // 可能低价团
    else if (product.price < 4000) score += 10;
    else if (product.price < 6000) score += 5;
    else score -= 5; // 太贵
  }
  
  // 评分
  if (product.rating) {
    if (product.rating >= 4.8) score += 20;
    else if (product.rating >= 4.5) score += 15;
    else if (product.rating >= 4.0) score += 5;
    else score -= 10;
  }
  
  // 购物店
  if (product.shoppingStops !== undefined) {
    score -= product.shoppingStops * 5;
    if (product.shoppingStops === 0) score += 15;
  }
  
  // 酒店
  if (product.hotelStars) {
    score += product.hotelStars * 3;
  }
  
  return Math.max(0, Math.min(100, score));
}

function analyzePrice(product, analysis) {
  if (!product.price) return;
  
  if (product.price < 2000 && product.days >= 5) {
    analysis.cons.push('价格偏低，可能存在隐形消费');
    analysis.warnings.push({
      type: '低价团',
      message: '警惕低价团陷阱，实际花费可能远超团费'
    });
  } else if (product.price > 8000) {
    analysis.cons.push('价格偏高，性价比一般');
  } else {
    analysis.pros.push('价格适中，性价比合理');
  }
  
  // 检查自费项目
  if (product.selfPaidItems && product.selfPaidItems.length > 0) {
    analysis.hiddenCosts.push(...product.selfPaidItems);
  }
}

function analyzeItinerary(product, analysis) {
  if (!product.itinerary) return;
  
  const { days, attractions, shoppingStops, freeTime } = product.itinerary;
  
  // 行程密度
  if (attractions && days) {
    const perDay = attractions / days;
    if (perDay > 4) {
      analysis.cons.push('行程较紧凑，每天景点过多');
    } else if (perDay < 2) {
      analysis.pros.push('行程轻松，节奏适中');
    } else {
      analysis.pros.push('行程安排合理');
    }
  }
  
  // 购物店
  if (shoppingStops === 0) {
    analysis.pros.push('纯玩无购物，体验好');
  } else if (shoppingStops >= 3) {
    analysis.cons.push(`含${shoppingStops}个购物店，可能影响体验`);
    analysis.warnings.push({
      type: '购物团',
      message: '购物店较多，注意导游可能引导消费'
    });
  }
  
  // 自由时间
  if (freeTime && freeTime.includes('小时')) {
    const hours = parseInt(freeTime);
    if (hours >= 3) {
      analysis.pros.push('自由活动时间充足');
    } else if (hours < 1) {
      analysis.cons.push('自由活动时间较少');
    }
  }
}

function analyzeAccommodation(product, analysis) {
  if (!product.hotelStandard && !product.hotelStars) return;
  
  const standard = product.hotelStandard || `${product.hotelStars}钻`;
  
  if (standard.includes('准')) {
    analysis.warnings.push({
      type: '非官方星级',
      message: '"准 X 钻"不是官方评级，实际标准可能偏低'
    });
    analysis.cons.push('酒店星级标注不规范');
  } else if (product.hotelStars >= 5) {
    analysis.pros.push('高星酒店，住宿品质好');
  } else if (product.hotelStars >= 4) {
    analysis.pros.push('酒店标准不错');
  }
}

function analyzeRating(product, analysis) {
  if (!product.rating) return;
  
  const { rating, reviewCount } = product;
  
  if (rating >= 4.8) {
    analysis.pros.push(`评分优秀 (${rating}/5.0)`);
  } else if (rating >= 4.5) {
    analysis.pros.push(`评分良好 (${rating}/5.0)`);
  } else if (rating >= 4.0) {
    analysis.cons.push(`评分一般 (${rating}/5.0)`);
  } else {
    analysis.cons.push(`评分较低 (${rating}/5.0)，用户反馈差`);
    analysis.warnings.push({
      type: '低评分',
      message: '评分低于 4.0，建议谨慎选择'
    });
  }
  
  // 评价数量
  if (reviewCount) {
    if (reviewCount > 1000) {
      analysis.pros.push('评价数量多，数据可信');
    } else if (reviewCount < 100) {
      analysis.cons.push('评价数量少，参考性有限');
    }
  }
}

function checkRedFlags(product, analysis) {
  const text = JSON.stringify(product).toLowerCase();
  
  redFlags.forEach(flag => {
    if (text.includes(flag.keyword.toLowerCase())) {
      analysis.warnings.push({
        type: flag.keyword,
        message: flag.warning,
        severity: flag.severity
      });
    }
  });
}

function performDeepAnalysis(product, analysis) {
  // 行程节奏分析
  if (product.dailyItinerary) {
    const intensity = analyzeDailyIntensity(product.dailyItinerary);
    analysis.deepAnalysis = {
      intensity,
      restDays: product.dailyItinerary.filter(d => d.intensity === 'low').length,
      busyDays: product.dailyItinerary.filter(d => d.intensity === 'high').length
    };
  }
  
  // 性价比分析
  if (product.price && product.days) {
    const perDay = product.price / product.days;
    analysis.deepAnalysis = {
      ...analysis.deepAnalysis,
      perDayCost: perDay,
      valueRating: perDay < 500 ? '高' : perDay < 800 ? '中' : '低'
    };
  }
}

function analyzeDailyIntensity(itinerary) {
  const scores = itinerary.map(day => {
    let score = 0;
    if (day.attractions > 3) score += 2;
    if (day.transferTime > 3) score += 1;
    if (day.activities.includes('徒步')) score += 1;
    return score;
  });
  
  const avg = scores.reduce((a, b) => a + b, 0) / scores.length;
  return avg > 3 ? '高强度' : avg > 2 ? '中等' : '轻松';
}

function generateSuggestions(product, analysis) {
  if (analysis.warnings.some(w => w.type === '低价团')) {
    analysis.suggestions.push('建议对比同类产品，价格过低必有原因');
  }
  
  if (analysis.warnings.some(w => w.type === '购物团')) {
    analysis.suggestions.push('可考虑加钱升级纯玩团，体验更好');
  }
  
  if (product.selfPaidItems && product.selfPaidItems.length > 0) {
    const total = product.selfPaidItems.reduce((sum, item) => sum + (item.price || 0), 0);
    if (total > 500) {
      analysis.suggestions.push(`自费项目较多，预计额外支出${total}元`);
    }
  }
  
  if (!product.cancelPolicy || product.cancelPolicy.includes('不可取消')) {
    analysis.suggestions.push('退改政策严格，建议购买取消险');
  }
}
