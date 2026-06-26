/**
 * UI 渲染器
 * 输出格式化的对比/推荐/分析报告
 */

import chalk from 'chalk';

/**
 * 渲染对比报告
 */
export function renderComparison(result, format = 'markdown') {
  if (format === 'json') {
    return JSON.stringify(result, null, 2);
  }
  
  let output = '';
  
  // 标题
  output += `\n${chalk.bold.blue('📊 线路对比报告')}\n`;
  output += `${chalk.gray('='.repeat(50))}\n\n`;
  
  // 一句话结论
  if (result.recommendation) {
    output += `${chalk.bold.green('✅ ' + result.recommendation.summary)}\n\n`;
  }
  
  // 对比表格
  output += renderComparisonTable(result.products);
  
  // 推荐排序
  output += `\n${chalk.bold('📋 推荐排序')}\n\n`;
  result.products.forEach((product, index) => {
    const medal = index === 0 ? '🥇' : index === 1 ? '🥈' : index === 2 ? '🥉' : '  ';
    const score = chalk.bold(product.score >= 80 ? chalk.green(product.score) : product.score >= 60 ? chalk.yellow(product.score) : chalk.red(product.score));
    output += `${medal} ${index + 1}. ${product.title} - ${score}分\n`;
    
    // 亮点
    const highlights = [];
    if (product.rating >= 4.8) highlights.push('评分高');
    if (product.shoppingStops === 0) highlights.push('0 购物');
    if (product.hotelStars >= 4) highlights.push('高星酒店');
    if (highlights.length > 0) {
      output += `   ${chalk.gray('亮点：' + highlights.join(' | '))}\n`;
    }
  });
  
  // 各维度最佳
  if (result.bestInCategory && Object.keys(result.bestInCategory).length > 0) {
    output += `\n${chalk.bold('🏆 各维度最佳')}\n\n`;
    const best = result.bestInCategory;
    if (best.price && best.price.title) {
      output += `💰 价格最低：${best.price.title} (¥${best.price.price})\n`;
    }
    if (best.rating && best.rating.title) {
      output += `⭐ 评分最高：${best.rating.title} (${best.rating.rating}分)\n`;
    }
    if (best.shopping && best.shopping.title) {
      output += `🛍️ 购物最少：${best.shopping.title} (${best.shopping.shoppingStops}个)\n`;
    }
    if (best.hotel && best.hotel.title) {
      output += `🏨 酒店最好：${best.hotel.title} (${best.hotel.hotelStars}钻)\n`;
    }
  }
  
  // 避坑提醒
  if (result.warnings && result.warnings.length > 0) {
    output += `\n${chalk.bold.red('⚠️  避坑提醒')}\n\n`;
    result.warnings.forEach(warning => {
      const icon = warning.severity === 'high' ? '🔴' : warning.severity === 'medium' ? '🟡' : '🟢';
      output += `${icon} ${warning.product}\n`;
      output += `   ${chalk.yellow(warning.type)}: ${warning.message}\n\n`;
    });
  }
  
  // 人群建议
  if (result.group) {
    output += `\n${chalk.bold('💡 选择建议')}\n\n`;
    output += `适合${result.group}的选择：${result.products[0]?.title}\n`;
    output += chalk.gray('理由：') + getGroupReason(result.products[0], result.group) + '\n';
  }
  
  // 深度对比分析
  if (result.deepComparison) {
    output += renderDeepComparison(result.deepComparison, result.products);
  }
  
  // 最终推荐
  output += renderFinalRecommendation(result);
  
  return output;
}

/**
 * 渲染深度对比分析
 */
function renderDeepComparison(deepComparison, products) {
  let output = '';
  
  output += `\n${chalk.bold.blue('🔍 深度对比分析')}\n`;
  output += `${chalk.gray('='.repeat(50))}\n\n`;
  
  // 优缺点对比
  output += `${chalk.bold('📋 优缺点对比')}\n\n`;
  products.forEach((product, index) => {
    output += `${chalk.bold(`商品${index + 1}: ${product.title}`)}\n`;
    
    if (product.pros && product.pros.length > 0) {
      output += `${chalk.green('✅ 优点')}:\n`;
      product.pros.forEach(pro => {
        output += `   • ${pro.message}\n`;
      });
    }
    
    if (product.cons && product.cons.length > 0) {
      output += `${chalk.red('❌ 缺点')}:\n`;
      product.cons.forEach(con => {
        output += `   • ${con.message}\n`;
      });
    }
    
    output += '\n';
  });
  
  // 性价比分析
  if (deepComparison.valueAnalysis && deepComparison.valueAnalysis.length > 0) {
    output += `${chalk.bold('💰 性价比分析')}\n\n`;
    deepComparison.valueAnalysis.forEach(analysis => {
      if (analysis.product) {
        output += `${chalk.green('✅ ' + analysis.product)}: ${analysis.message} (性价比指数：${analysis.score})\n`;
      } else {
        output += `${chalk.yellow('⚖️ ' + analysis.message)} (指数：${analysis.score1} vs ${analysis.score2})\n`;
      }
    });
    output += '\n';
  }
  
  // 决策因素
  if (deepComparison.decisionFactors && deepComparison.decisionFactors.length > 0) {
    output += `${chalk.bold('🎯 关键决策因素')}\n\n`;
    deepComparison.decisionFactors.forEach((factor, index) => {
      output += `${index + 1}. ${chalk.bold(factor.factor)}: ${factor.description}\n`;
      output += `   ${chalk.blue('建议：' + factor.suggestion)}\n\n`;
    });
  }
  
  // 场景化推荐
  if (deepComparison.scenarioRecommendations && deepComparison.scenarioRecommendations.length > 0) {
    output += `\n${chalk.bold('📍 怎么选')}\n\n`;
    deepComparison.scenarioRecommendations.forEach(rec => {
      const recTitle = typeof rec.recommendation === 'string' ? rec.recommendation : (rec.recommendation ? rec.recommendation.title : '未知');
      output += `${chalk.bold('• ')}${rec.scenario}: ${recTitle}\n`;
      output += `  ${chalk.gray('理由：' + rec.reason)}\n`;
    });
    output += '\n';
  }
  
  return output;
}

function renderComparisonTable(products) {
  if (products.length === 0) return '';
  
  let output = `${chalk.bold('对比总览')}\n\n`;
  
  // 表头
  const headers = ['维度', ...products.map((p, i) => `商品${i + 1}`)];
  
  // 找出各维度最佳值
  const bestValues = {
    price: Math.min(...products.map(p => p.price || Infinity)),
    rating: Math.max(...products.map(p => p.rating || 0)),
    shoppingStops: Math.min(...products.map(p => p.shoppingStops !== undefined ? p.shoppingStops : Infinity))
  };
  
  // 数据行
  const rows = [
    { label: '💰 价格', key: 'price', format: 'price', lowerBetter: true },
    { label: '⭐ 评分', key: 'rating', format: 'rating', lowerBetter: false },
    { label: '🛍️ 购物店', key: 'shoppingStops', format: 'number', lowerBetter: true },
    { label: '🏨 酒店', key: 'hotelStars', format: 'stars', lowerBetter: false },
    { label: '📅 天数', key: 'days', format: 'days', lowerBetter: false },
    { label: '📊 综合评分', key: 'score', format: 'score', lowerBetter: false }
  ];
  
  rows.forEach(row => {
    output += `${row.label}`;
    products.forEach(product => {
      const value = product[row.key];
      if (value !== undefined && value !== null) {
        const isBest = row.lowerBetter ? value === bestValues[row.key] : value === bestValues[row.key];
        const formatted = formatValue(value, row.format);
        output += `\t${isBest ? chalk.green(formatted) : formatted}`;
      } else {
        output += `\t${chalk.gray('-')}`;
      }
    });
    output += '\n';
  });
  
  output += '\n';
  return output;
}

function formatValue(value, format) {
  switch (format) {
    case 'price': return `¥${value}`;
    case 'rating': return `${value}`;
    case 'stars': return `${value}钻`;
    case 'days': return `${value}天`;
    case 'score': return `${value}分`;
    default: return String(value);
  }
}

function getGroupReason(product, group) {
  const reasons = [];
  if (group === '老人') {
    if (product.shoppingStops === 0) reasons.push('0 购物纯玩');
    if (product.rating >= 4.5) reasons.push('评分高口碑好');
    if (product.hotelStars >= 4) reasons.push('酒店舒适');
  } else if (group === '亲子') {
    if (product.features?.includes('亲子')) reasons.push('有亲子设施');
    if (product.rating >= 4.5) reasons.push('家庭出游首选');
  } else if (group === '蜜月') {
    if (product.hotelStars >= 5) reasons.push('高星酒店');
    if (product.shoppingStops === 0) reasons.push('私密性好');
  }
  return reasons.length > 0 ? reasons.join('，') : '综合评分最高';
}

/**
 * 渲染推荐报告
 */
export function renderRecommendation(result) {
  let output = '';
  
  output += `\n${chalk.bold.blue('🎯 智能推荐报告')}\n`;
  output += `${chalk.gray('='.repeat(50))}\n\n`;
  
  // 搜索条件
  output += `${chalk.gray('搜索条件：')}`;
  output += `${result.destination}`;
  if (result.budget) output += ` | 预算¥${result.budget}`;
  if (result.group) output += ` | ${result.group}`;
  if (result.days) output += ` | ${result.days}天`;
  output += `\n`;
  output += `${chalk.gray('共找到')} ${result.totalFound} ${chalk.gray('个匹配商品')}\n\n`;
  
  // 推荐理由
  if (result.recommendation) {
    output += `${chalk.bold('为什么推荐这个目的地')}\n\n`;
    if (result.recommendation.suitable) {
      result.recommendation.suitable.forEach(r => {
        output += `${chalk.green('✅')} ${r}\n`;
      });
    }
    if (result.recommendation.season) {
      output += `\n${chalk.gray('📅 最佳季节：')}\n`;
      result.recommendation.season.forEach(r => {
        output += `${chalk.green('✅')} ${r}\n`;
      });
    }
    output += '\n';
  }
  
  // Top3 推荐
  output += `${chalk.bold('🏆 推荐商品 Top3')}\n\n`;
  
  result.products.forEach((product, index) => {
    const medal = index === 0 ? '🥇' : index === 1 ? '🥈' : '🥉';
    output += `${medal} ${chalk.bold(product.title)}\n`;
    output += `   ${chalk.gray('平台：')}${product.platform} | ${chalk.gray('价格：')}¥${product.price} | ${chalk.gray('评分：')}${product.rating}\n`;
    
    if (product.features && product.features.length > 0) {
      output += `   ${chalk.gray('亮点：')}${product.features.join(' | ')}\n`;
    }
    output += '\n';
  });
  
  // 注意事项
  output += `${chalk.bold('⚠️  注意事项')}\n\n`;
  if (result.group === '老人') {
    output += `- 提前准备常用药物，确认行程强度\n`;
    output += `- 选择含接送机的产品，减少奔波\n`;
    output += `- 购买旅游意外险\n`;
  } else if (result.group === '亲子') {
    output += `- 确认酒店有亲子设施（泳池、儿童乐园等）\n`;
    output += `- 预留自由活动时间，避免行程过满\n`;
    output += `- 准备儿童常用药和防晒用品\n`;
  }
  
  return output;
}

/**
 * 渲染最终推荐
 */
function renderFinalRecommendation(result) {
  let output = '';
  
  output += `\n${chalk.bold.blue('💡 最终建议')}\n`;
  output += `${chalk.gray('='.repeat(50))}\n\n`;
  
  const [top1, top2] = result.products;
  
  // 如果两个商品差距很小
  if (top1 && top2 && Math.abs(top1.score - top2.score) <= 5) {
    output += chalk.yellow('两者差距不大，主要看你的需求：') + '\n\n';
    
    // 找出性价比更高的（价格低的那个）
    const cheaper = top1.price && top2.price && top1.price < top2.price ? top1 : top2;
    const premium = cheaper === top1 ? top2 : top1;
    
    output += `${chalk.bold('选 ' + cheaper.title)} 如果：\n`;
    output += `• 预算有限，追求性价比\n`;
    if (cheaper.days && cheaper.days <= 4) {
      output += `• 时间紧张，${cheaper.days}天够用\n`;
    }
    if (cheaper.features && cheaper.features.includes('全额退')) {
      output += `• 需要灵活退改\n`;
    }
    output += '\n';
    
    output += `${chalk.bold('选 ' + premium.title)} 如果：\n`;
    if (premium.groupSize && premium.groupSize <= 6) {
      output += `• 追求小团体验，人少更自由\n`;
    }
    if (premium.rating && premium.rating >= 5.0) {
      output += `• 看重完美评分\n`;
    }
    if (premium.days && premium.days > cheaper.days) {
      output += `• 时间充裕，想深度游\n`;
    }
    output += '\n';
  } else {
    // 差距明显
    output += `推荐 ${chalk.bold.green(top1?.title)}\n\n`;
    output += chalk.gray('综合评分更高，') + getGroupReason(top1, result.group) + '\n';
  }
  
  return output;
}

/**
 * 渲染分析报告
 */
export function renderAnalysis(result) {
  let output = '';
  
  output += `\n${chalk.bold.blue('🔍 商品深度分析报告')}\n`;
  output += `${chalk.gray('='.repeat(50))}\n\n`;
  
  // 商品信息
  output += `${chalk.bold(result.product.title)}\n`;
  output += `${chalk.gray('平台：')}${result.product.platform || '未知'} | ${chalk.gray('价格：')}¥${result.product.price || '未知'}\n\n`;
  
  // 综合评分
  const scoreColor = result.score >= 80 ? chalk.green : result.score >= 60 ? chalk.yellow : chalk.red;
  output += `${chalk.bold('综合评分：')}${scoreColor(result.score + '/100')}\n\n`;
  
  // 优点
  if (result.pros.length > 0) {
    output += `${chalk.bold.green('✅ 优点')}\n`;
    result.pros.forEach(pro => {
      output += `${chalk.green('•')} ${pro}\n`;
    });
    output += '\n';
  }
  
  // 缺点
  if (result.cons.length > 0) {
    output += `${chalk.bold.red('❌ 缺点')}\n`;
    result.cons.forEach(con => {
      output += `${chalk.red('•')} ${con}\n`;
    });
    output += '\n';
  }
  
  // 警告
  if (result.warnings.length > 0) {
    output += `${chalk.bold.yellow('⚠️  警告')}\n`;
    result.warnings.forEach(warning => {
      output += `${chalk.yellow('•')} [${warning.type}] ${warning.message}\n`;
    });
    output += '\n';
  }
  
  // 隐形消费
  if (result.hiddenCosts && result.hiddenCosts.length > 0) {
    output += `${chalk.bold('💰 隐形消费')}\n`;
    result.hiddenCosts.forEach(cost => {
      output += `${chalk.gray('•')} ${cost.name || cost}: ¥${cost.price || '未知'}\n`;
    });
    output += '\n';
  }
  
  // 建议
  if (result.suggestions.length > 0) {
    output += `${chalk.bold('💡 建议')}\n`;
    result.suggestions.forEach(suggestion => {
      output += `${chalk.blue('•')} ${suggestion}\n`;
    });
    output += '\n';
  }
  
  return output;
}
