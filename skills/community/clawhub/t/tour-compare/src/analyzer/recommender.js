/**
 * 智能推荐引擎
 * 根据用户需求推荐旅游商品
 */

import { getPersona } from '../config/personas.js';

/**
 * 推荐商品
 * @param {Object} options - 推荐选项
 * @returns {Object} 推荐结果
 */
export function recommendProducts(options) {
  const { destination, budget, group, days, preferences } = options;
  const persona = group ? getPersona(group) : null;
  
  // MVP 版本：返回示例推荐
  // TODO: 实现真实搜索逻辑
  const mockProducts = generateMockProducts(destination, budget, group, days);
  
  // 筛选
  let filtered = mockProducts;
  
  if (budget) {
    filtered = filtered.filter(p => p.price <= budget * 1.2); // 允许 20% 浮动
  }
  
  if (preferences) {
    if (preferences.includes('无购物')) {
      filtered = filtered.filter(p => p.shoppingStops === 0);
    }
    if (preferences.includes('直飞')) {
      filtered = filtered.filter(p => p.directFlight);
    }
    if (preferences.includes('高星酒店')) {
      filtered = filtered.filter(p => p.hotelStars >= 4);
    }
  }
  
  // 排序（根据人群画像）
  if (persona) {
    filtered.sort((a, b) => {
      const scoreA = calculateMatchScore(a, persona);
      const scoreB = calculateMatchScore(b, persona);
      return scoreB - scoreA;
    });
  } else {
    // 默认按评分排序
    filtered.sort((a, b) => (b.rating || 0) - (a.rating || 0));
  }
  
  // 取 Top3
  const top3 = filtered.slice(0, 3);
  
  // 生成推荐理由
  const recommendation = generateDestinationReasoning(destination, group, days);
  
  return {
    destination,
    group,
    budget,
    products: top3,
    recommendation,
    totalFound: filtered.length
  };
}

/**
 * 计算匹配度评分
 */
function calculateMatchScore(product, persona) {
  let score = 0;
  const weights = persona.weights;
  
  if (weights.shoppingStops && product.shoppingStops !== undefined) {
    score += (100 - product.shoppingStops * 20) * Math.abs(weights.shoppingStops);
  }
  if (weights.price && product.price) {
    score += (100 - product.price / 50) * weights.price;
  }
  if (weights.rating && product.rating) {
    score += product.rating * 20 * weights.rating;
  }
  if (weights.hotel && product.hotelStars) {
    score += product.hotelStars * 20 * weights.hotel;
  }
  
  return score;
}

/**
 * 生成目的地推荐理由
 */
function generateDestinationReasoning(destination, group, days) {
  const reasons = {
    suitable: [],
    season: [],
    budget: []
  };
  
  // 根据目的地生成理由
  if (destination.includes('云南')) {
    reasons.suitable.push('气候宜人，四季如春');
    reasons.suitable.push('医疗配套完善，昆明/丽江有三甲医院');
    if (group === '老人') {
      reasons.suitable.push('行程节奏可调节，适合老人');
    }
    reasons.season.push('3-5 月春暖花开，气温 15-25°C');
    reasons.season.push('避开暑期/国庆人流高峰');
  } else if (destination.includes('海南') || destination.includes('三亚')) {
    reasons.suitable.push('热带海滨，度假休闲');
    reasons.suitable.push('酒店配套成熟，亲子设施完善');
    reasons.season.push('10 月 - 次年 3 月为最佳季节');
  } else if (destination.includes('日本')) {
    reasons.suitable.push('购物 + 文化体验');
    reasons.suitable.push('服务品质高，适合家庭出游');
    reasons.season.push('春季赏樱，秋季赏枫');
  }
  
  // 预算建议
  if (group === '老人' && destination.includes('云南')) {
    reasons.budget.push('人均 3000-4000 可选择品质团');
    reasons.budget.push('建议预留 500-1000 元自费/购物预算');
  }
  
  return reasons;
}

/**
 * 生成示例商品（MVP 用）
 */
function generateMockProducts(destination, budget, group, days) {
  const basePrice = budget ? budget * 0.8 : 3000;
  
  return [
    {
      id: 'ctrip_001',
      platform: '携程',
      title: `${destination}${days || 6}天${(days || 6) - 1}晚品质团`,
      price: Math.round(basePrice * 0.9),
      rating: 4.8,
      reviewCount: 2341,
      shoppingStops: 0,
      hotelStars: 4,
      directFlight: true,
      days: days || 6,
      features: ['纯玩无购物', '接送机', '4 钻酒店']
    },
    {
      id: 'fliggy_001',
      platform: '飞猪',
      title: `${destination}${days || 6}日游尊享团`,
      price: Math.round(basePrice * 1.1),
      rating: 4.9,
      reviewCount: 892,
      shoppingStops: 1,
      hotelStars: 5,
      directFlight: true,
      days: days || 6,
      features: ['5 钻酒店', '小团出行', '特色餐']
    },
    {
      id: 'tongcheng_001',
      platform: '同程',
      title: `${destination}经典${days || 6}日游`,
      price: Math.round(basePrice * 0.7),
      rating: 4.5,
      reviewCount: 1567,
      shoppingStops: 3,
      hotelStars: 3,
      directFlight: false,
      days: days || 6,
      features: ['性价比高', '经典景点', '含部分餐']
    },
    {
      id: 'ctrip_002',
      platform: '携程',
      title: `${destination}私家团${days || 6}天`,
      price: Math.round(basePrice * 1.5),
      rating: 4.9,
      reviewCount: 456,
      shoppingStops: 0,
      hotelStars: 5,
      directFlight: true,
      days: days || 6,
      features: ['独立成团', '专车专导', '自由行']
    },
    {
      id: 'fliggy_002',
      platform: '飞猪',
      title: `${destination}经济团${days || 6}日游`,
      price: Math.round(basePrice * 0.6),
      rating: 4.2,
      reviewCount: 3421,
      shoppingStops: 5,
      hotelStars: 3,
      directFlight: false,
      days: days || 6,
      features: ['超值低价', '景点全', '购物优惠']
    }
  ];
}
