/**
 * 标准化输出模板
 * 
 * 输出结构：
 * 1. 文字版对比总结（核心差异 + 推荐）
 * 2. 可视化报告链接（HTML 页面）
 * 3. 相关问题追问（引导深入）
 */

import chalk from 'chalk';

/**
 * 生成标准化对比总结
 */
export function generateSummary(result, options = {}) {
  const { products, deepComparison, recommendation } = result;
  
  let output = '';
  
  // 1. 标题
  output += `\n${chalk.bold.blue('📊 旅游商品对比分析')}\n`;
  output += `${chalk.gray('='.repeat(50))}\n\n`;
  
  // 2. 一句话结论
  if (recommendation) {
    output += `${chalk.bold.green('✅ ' + recommendation.summary)}\n\n`;
  }
  
  // 3. 核心差异对比（表格）
  output += `${chalk.bold('📋 核心差异')}\n\n`;
  output += generateQuickComparison(products);
  
  // 4. 关键决策因素
  if (deepComparison && deepComparison.decisionFactors) {
    output += `\n${chalk.bold('🎯 关键决策因素')}\n\n`;
    deepComparison.decisionFactors.forEach((factor, index) => {
      output += `${index + 1}. ${chalk.bold(factor.factor)}: ${factor.description}\n`;
      output += `   ${chalk.blue('💡 ' + factor.suggestion)}\n\n`;
    });
  }
  
  // 5. 性价比分析
  if (deepComparison && deepComparison.valueAnalysis) {
    output += `\n${chalk.bold('💰 性价比分析')}\n\n`;
    deepComparison.valueAnalysis.forEach(analysis => {
      if (analysis.product) {
        output += `${chalk.green('✅ ' + analysis.product)}: ${analysis.message}\n`;
      }
    });
    output += '\n';
  }
  
  // 6. 场景化推荐
  if (deepComparison && deepComparison.scenarioRecommendations) {
    output += `\n${chalk.bold('📍 怎么选')}\n\n`;
    deepComparison.scenarioRecommendations.forEach(rec => {
      const recTitle = typeof rec.recommendation === 'string' 
        ? rec.recommendation 
        : (rec.recommendation ? rec.recommendation.title : '未知');
      output += `${chalk.bold('• ')}${rec.scenario}: ${recTitle}\n`;
      output += `  ${chalk.gray('理由：' + rec.reason)}\n`;
    });
    output += '\n';
  }
  
  // 7. 可视化报告链接
  output += generateReportLink(options.reportType);
  
  // 8. 相关问题追问
  output += generateFollowUpQuestions(products, options);
  
  return output;
}

/**
 * 生成快速对比表格
 */
function generateQuickComparison(products) {
  if (products.length === 0) return '';
  
  let output = '';
  
  // 表头
  const headers = ['维度', ...products.map((p, i) => `商品${i + 1}`)];
  output += formatRow(headers) + '\n';
  
  // 分隔线
  output += formatRow(headers.map(() => '─'.repeat(12))) + '\n';
  
  // 数据行
  const rows = [
    ['💰 价格', ...products.map(p => p.price ? `¥${p.price}` : '-')],
    ['⭐ 评分', ...products.map(p => p.rating ? `${p.rating}分` : '-')],
    ['📅 天数', ...products.map(p => p.days ? `${p.days}天` : '-')],
    ['🏨 酒店', ...products.map(p => p.hotelStars ? `${p.hotelStars}钻` : '-')],
    ['🛍️ 购物', ...products.map(p => p.shoppingStops !== undefined ? `${p.shoppingStops}个` : '-')]
  ];
  
  rows.forEach(row => {
    output += formatRow(row) + '\n';
  });
  
  return output;
}

/**
 * 格式化表格行
 */
function formatRow(cells) {
  return cells.map(cell => cell.padEnd(12)).join('  ');
}

/**
 * 生成报告链接
 */
function generateReportLink(reportType = 'packages') {
  let output = '';
  
  output += `\n${chalk.bold.blue('📄 可视化报告')}\n`;
  output += `${chalk.gray('='.repeat(50))}\n\n`;
  
  if (reportType === 'destinations') {
    output += `🔗 ${chalk.cyan('file:///Users/zihui/.openclaw/workspace/tour-compare-destinations.html')}\n`;
    output += `${chalk.gray('跨目的地对比：日本 vs 云南')}\n\n`;
  } else {
    output += `🔗 ${chalk.cyan('file:///Users/zihui/.openclaw/workspace/tour-compare-packages.html')}\n`;
    output += `${chalk.gray('同目的地套餐对比：经济型 vs 舒适型 vs 独立团')}\n\n`;
  }
  
  output += `${chalk.gray('💡 提示：点击链接在浏览器中打开完整报告')}\n\n`;
  
  return output;
}

/**
 * 生成相关问题追问
 */
function generateFollowUpQuestions(products, options) {
  let output = '';
  
  output += `\n${chalk.bold('💬 相关问题')}\n`;
  output += `${chalk.gray('='.repeat(50))}\n\n`;
  
  const questions = [];
  
  // 基于价格差异
  if (products.length >= 2 && products[0].price && products[1].price) {
    const priceGap = Math.abs(products[0].price - products[1].price);
    if (priceGap > 500) {
      questions.push('想知道价格差异主要体现在哪些方面吗？（酒店/餐饮/景点）');
    }
  }
  
  // 基于行程
  if (products.some(p => p.days)) {
    questions.push('需要我详细对比每日行程安排吗？');
  }
  
  // 基于酒店
  if (products.some(p => p.hotelStars)) {
    questions.push('想了解具体酒店信息和位置吗？');
  }
  
  // 基于用户评价
  if (products.some(p => p.reviewCount)) {
    questions.push('需要查看真实用户评价摘要吗？（好评/差评关键词）');
  }
  
  // 基于退改政策
  questions.push('需要对比退改政策和风险提示吗？');
  
  // 基于目的地
  if (options.reportType === 'destinations') {
    questions.push('想知道这两个目的地的最佳旅行时间吗？');
    questions.push('需要我分析签证/语言/货币等差异吗？');
  }
  
  // 通用问题
  questions.push('需要我推荐其他类似商品吗？');
  
  // 输出问题（最多 3 个）
  questions.slice(0, 3).forEach((q, index) => {
    output += `${index + 1}. ${q}\n`;
  });
  
  output += `\n${chalk.gray('有任何问题随时问我！🦐')}\n`;
  
  return output;
}

/**
 * 生成跨目的地对比总结
 */
export function generateDestinationSummary(result) {
  const { products, deepComparison } = result;
  
  let output = '';
  
  output += `\n${chalk.bold.blue('🌏 目的地决策分析')}\n`;
  output += `${chalk.gray('='.repeat(50))}\n\n`;
  
  // 一句话结论
  output += `${chalk.bold('这是两个完全不同的旅行体验')}\n`;
  output += `${chalk.gray('根据你的偏好，我来帮你分析哪个更适合')}\n\n`;
  
  // 核心差异
  output += `${chalk.bold('📋 核心差异')}\n\n`;
  output += `| 维度 | ${products[0]?.title || '目的地 A'} | ${products[1]?.title || '目的地 B'} |\n`;
  output += `|─────|${'─'.repeat(20)}|${'─'.repeat(20)}|\n`;
  output += `| 💰 价格 | ¥${products[0]?.price || '-'} | ¥${products[1]?.price || '-'} |\n`;
  output += `| 📅 天数 | ${products[0]?.days || '-'}天 | ${products[1]?.days || '-'}天 |\n`;
  output += `| 🛂 签证 | ${products[0]?.visa || '需确认'} | ${products[1]?.visa || '需确认'} |\n`;
  output += `| 🎯 体验 | ${products[0]?.experience || '城市购物'} | ${products[1]?.experience || '自然风光'} |\n\n`;
  
  // 决策建议
  output += `${chalk.bold('💡 怎么选')}\n\n`;
  output += `选 ${products[0]?.title || '目的地 A'} 如果：\n`;
  output += `• 预算充足、喜欢购物美食、想体验异国文化\n\n`;
  output += `选 ${products[1]?.title || '目的地 B'} 如果：\n`;
  output += `• 预算有限、喜欢自然风光、带老人小孩\n\n`;
  
  // 报告链接
  output += generateReportLink('destinations');
  
  // 相关问题
  output += `\n${chalk.bold('💬 相关问题')}\n`;
  output += `${chalk.gray('='.repeat(50))}\n\n`;
  output += `1. 想知道这两个地方的最佳旅行时间吗？\n`;
  output += `2. 需要我详细对比预算明细吗？（团费 + 餐饮 + 购物）\n`;
  output += `3. 想了解签证办理流程和费用吗？\n`;
  output += `4. 需要推荐其他类似目的地吗？\n\n`;
  output += `${chalk.gray('有任何问题随时问我！🦐')}\n`;
  
  return output;
}

export default {
  generateSummary,
  generateDestinationSummary
};
