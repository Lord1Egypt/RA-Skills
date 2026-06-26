#!/usr/bin/env node

/**
 * 售后分析报表 CLI
 * 
 * 支持命令：
 * - complaint [--range=<date-range>] - 投诉统计
 * - repeat-order [--range=<date-range>] - 返单统计
 * - satisfaction [--range=<date-range>] - 满意度统计
 * - risk - 客户风险分析
 * - quality - 产品质量分析
 * - summary - 综合摘要
 * - help, --help, -h - 显示帮助
 */

const path = require('path');
const dayjs = require('dayjs');
const analyticsAPI = require('../api/controllers/analytics_api');

// 解析命令行参数
function parseArgs(args) {
  const command = args[0];
  const options = {};

  for (let i = 1; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith('--range=')) {
      options.range = arg.split('=')[1];
    } else if (arg.startsWith('--json')) {
      options.json = true;
    }
  }

  return { command, options };
}

// 格式化输出
function formatOutput(data, options) {
  if (options.json) {
    console.log(JSON.stringify(data, null, 2));
    return;
  }

  // 美化输出
  if (data.reportType === 'complaint_analytics') {
    console.log('\n=== 投诉统计分析 ===\n');
    console.log(`日期范围：${data.dateRange.startDate} 至 ${data.dateRange.endDate}`);
    console.log(`生成时间：${data.generatedAt}\n`);
    
    const summary = data.data.summary;
    console.log('📊 概要统计:');
    console.log(`  总投诉数：${summary.total}`);
    console.log(`  已解决：${summary.resolved}`);
    console.log(`  待处理：${summary.pending}`);
    console.log(`  解决率：${summary.resolutionRate}`);
    console.log(`  平均解决时间：${summary.avgResolutionDays} 天\n`);

    console.log('📋 按类型统计:');
    Object.entries(data.data.byType).forEach(([type, count]) => {
      console.log(`  ${type}: ${count}`);
    });
    console.log('');

    console.log('🔄 按状态统计:');
    Object.entries(data.data.byStatus).forEach(([status, count]) => {
      console.log(`  ${status}: ${count}`);
    });
    console.log('');

    console.log('⚠️ 按严重程度统计:');
    Object.entries(data.data.bySeverity).forEach(([severity, count]) => {
      console.log(`  ${severity}: ${count}`);
    });
  } 
  else if (data.reportType === 'repeat_order_analytics') {
    console.log('\n=== 返单统计分析 ===\n');
    console.log(`日期范围：${data.dateRange.startDate} 至 ${data.dateRange.endDate}`);
    console.log(`生成时间：${data.generatedAt}\n`);
    
    const summary = data.data.summary;
    console.log('📊 概要统计:');
    console.log(`  总返单数：${summary.total}`);
    console.log(`  转化率：${summary.conversionRate}`);
    console.log(`  总返单金额：¥${summary.totalAmount.toLocaleString()}`);
    console.log(`  平均返单金额：¥${parseFloat(summary.avgAmount).toLocaleString()}`);
    console.log(`  平均返单周期：${summary.avgDaysToRepeat} 天\n`);

    if (data.data.byCustomer.length > 0) {
      console.log('🏢 按客户统计:');
      data.data.byCustomer.forEach(c => {
        console.log(`  ${c.customerName}: ${c.count} 次返单，¥${c.totalAmount.toLocaleString()}`);
      });
    }
  }
  else if (data.reportType === 'satisfaction_analytics') {
    console.log('\n=== 满意度统计分析 ===\n');
    console.log(`日期范围：${data.dateRange.startDate} 至 ${data.dateRange.endDate}`);
    console.log(`生成时间：${data.generatedAt}\n`);
    
    const summary = data.data.summary;
    if (summary.total === 0) {
      console.log('暂无满意度调查数据');
    } else {
      console.log('📊 概要统计:');
      console.log(`  总调查数：${summary.total}`);
      console.log(`  综合平均分：${summary.avgOverallScore}/5.0`);
      console.log(`  产品质量：${summary.avgQualityScore}/5.0`);
      console.log(`  服务质量：${summary.avgServiceScore}/5.0`);
      console.log(`  物流配送：${summary.avgDeliveryScore}/5.0`);
      console.log(`  沟通效率：${summary.avgCommunicationScore}/5.0\n`);

      console.log('📈 分数分布:');
      Object.entries(data.data.distribution).forEach(([score, count]) => {
        const bar = '★'.repeat(parseInt(score)) + '☆'.repeat(5 - parseInt(score));
        console.log(`  ${bar} (${score}分): ${count} 票`);
      });
    }
  }
  else if (data.reportType === 'customer_risk_analysis') {
    console.log('\n=== 客户风险分析 ===\n');
    console.log(`生成时间：${data.generatedAt}\n`);
    
    const summary = data.data.summary;
    console.log('📊 概要统计:');
    console.log(`  总客户数：${summary.totalCustomers}`);
    console.log(`  低风险客户：${summary.lowRisk}`);
    console.log(`  中风险客户：${summary.mediumRisk}`);
    console.log(`  高风险客户：${summary.highRisk}`);
    console.log(`  高风险占比：${summary.highRiskRatio}\n`);

    if (data.data.highRiskCustomers.length > 0) {
      console.log('⚠️ 高风险客户列表:');
      data.data.highRiskCustomers.forEach(c => {
        console.log(`  ${c.customerName} (ID: ${c.customerId})`);
        console.log(`    订单数：${c.totalOrders}, 总金额：¥${c.totalAmount.toLocaleString()}`);
      });
    }
  }
  else if (data.reportType === 'product_quality_analysis') {
    console.log('\n=== 产品质量分析 ===\n');
    console.log(`生成时间：${data.generatedAt}\n`);
    
    const summary = data.data.summary;
    console.log('📊 概要统计:');
    console.log(`  总产品数：${summary.totalProducts}`);
    console.log(`  平均缺陷率：${(parseFloat(summary.avgDefectRate) * 100).toFixed(2)}%\n`);

    console.log('📦 按类别统计:');
    data.data.byCategory.forEach(c => {
      console.log(`  ${c.category}: ${c.productCount} 个产品，平均缺陷率 ${(parseFloat(c.avgDefectRate) * 100).toFixed(2)}%`);
    });
    console.log('');

    console.log('⚠️ 产品质量问题排行 (按缺陷率):');
    data.data.qualityIssues.slice(0, 5).forEach(p => {
      console.log(`  ${p.productName} (${p.category})`);
      console.log(`    缺陷率：${(p.defectRate * 100).toFixed(2)}%, 质量投诉：${p.qualityComplaints}`);
    });
  }
  else if (data.reportType === 'analytics_summary') {
    console.log('\n========================================');
    console.log('     售后分析综合摘要报告');
    console.log('========================================\n');
    console.log(`生成时间：${data.generatedAt}\n`);

    console.log('📊 投诉统计:');
    const c = data.summary.complaints;
    console.log(`  总数：${c.total} | 已解决：${c.resolved} | 解决率：${c.resolutionRate} | 平均解决时间：${c.avgResolutionDays}天\n`);

    console.log('🔄 返单统计:');
    const r = data.summary.repeatOrders;
    console.log(`  总数：${r.total} | 转化率：${r.conversionRate} | 总金额：¥${r.totalAmount.toLocaleString()} | 平均周期：${r.avgDaysToRepeat}天\n`);

    console.log('⭐ 满意度统计:');
    const s = data.summary.satisfaction;
    if (s.total > 0) {
      console.log(`  总调查数：${s.total} | 综合评分：${s.avgOverallScore}/5.0 | 质量：${s.avgQualityScore} | 服务：${s.avgServiceScore}\n`);
    } else {
      console.log(`  暂无数据\n`);
    }

    console.log('⚠️ 客户风险:');
    const risk = data.summary.customerRisk;
    console.log(`  总客户：${risk.totalCustomers} | 低：${risk.lowRisk} | 中：${risk.mediumRisk} | 高：${risk.highRisk} (${risk.highRiskRatio})\n`);

    console.log('📦 产品质量:');
    const q = data.summary.productQuality;
    console.log(`  总产品：${q.totalProducts} | 平均缺陷率：${(parseFloat(q.avgDefectRate) * 100).toFixed(2)}%\n`);

    console.log('========================================');
  }

  console.log('');
}

// 显示帮助
function showHelp() {
  console.log(`
售后分析报表 CLI

用法：node analytics_cli.js <command> [options]

命令:
  complaint      投诉统计分析
  repeat-order   返单统计分析
  satisfaction   满意度统计分析
  risk           客户风险分析
  quality        产品质量分析
  summary        综合摘要报告
  help           显示此帮助信息

选项:
  --range=<start_end>  日期范围 (格式：YYYY-MM-DD_YYYY-MM-DD)
                       例如：--range=2026-03-01_2026-03-31
  --json               以 JSON 格式输出

示例:
  node analytics_cli.js complaint
  node analytics_cli.js complaint --range=2026-03-01_2026-03-31
  node analytics_cli.js repeat-order --json
  node analytics_cli.js summary
`);
}

// 主函数
function main() {
  const args = process.argv.slice(2);
  
  if (args.length === 0 || args[0] === 'help' || args[0] === '--help' || args[0] === '-h') {
    showHelp();
    process.exit(0);
  }

  const { command, options } = parseArgs(args);
  let result;

  switch (command) {
    case 'complaint':
      result = analyticsAPI.getComplaintAnalytics(options.range);
      break;
    
    case 'repeat-order':
      result = analyticsAPI.getRepeatOrderAnalytics(options.range);
      break;
    
    case 'satisfaction':
      result = analyticsAPI.getSatisfactionAnalytics(options.range);
      break;
    
    case 'risk':
      result = analyticsAPI.getCustomerRiskAnalysis();
      break;
    
    case 'quality':
      result = analyticsAPI.getProductQualityAnalysis();
      break;
    
    case 'summary':
      result = analyticsAPI.getAnalyticsSummary(options.range);
      break;
    
    default:
      console.error(`错误：未知命令 "${command}"`);
      console.log('使用 "node analytics_cli.js help" 查看帮助');
      process.exit(1);
  }

  if (result.success) {
    formatOutput(result, options);
  } else {
    console.error('错误:', result.error);
    process.exit(1);
  }
}

// 运行 CLI
main();
