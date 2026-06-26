/**
 * 数据分析模块
 * 销售数据、广告分析、竞品监控
 */

import { getCurrentAccount, loadConfig } from './init.js';
import { createTikTokAPI } from '../src/api.js';
import { createFeishuIntegration } from '../src/feishu.js';
import fs from 'fs';
import path from 'path';

/**
 * 生成日报
 */
export async function dailyReport(options) {
  const account = getCurrentAccount();
  const config = loadConfig();

  console.log('📊 生成日报...');
  console.log(`  日期：${options.date}`);
  console.log(`  格式：${options.format}`);

  try {
    const tiktokAPI = createTikTokAPI(config);
    const shopId = account?.shopId || config.tiktok?.shopId || 'mock_shop';
    
    // 获取店铺概览
    const overview = await tiktokAPI.getShopOverview(shopId, 'last_30_days');
    
    // 获取销售数据
    const salesData = await tiktokAPI.getDailySales(
      shopId,
      options.date,
      options.date
    );

    const report = {
      date: options.date,
      generated_at: new Date().toISOString(),
      shop_id: shopId,
      overview: overview.data,
      sales: salesData.data
    };

    // 生成报告文件
    const reportDir = path.join(process.cwd(), 'reports');
    if (!fs.existsSync(reportDir)) {
      fs.mkdirSync(reportDir, { recursive: true });
    }

    const reportPath = path.join(reportDir, `daily_report_${options.date}.${options.format}`);
    
    if (options.format === 'json') {
      fs.writeFileSync(reportPath, JSON.stringify(report, null, 2));
    } else if (options.format === 'csv') {
      const csvContent = generateCSV(report);
      fs.writeFileSync(reportPath, csvContent);
    } else {
      // 默认 JSON
      fs.writeFileSync(reportPath.replace(`.${options.format}`, '.json'), JSON.stringify(report, null, 2));
    }

    console.log(`✓ 日报生成成功`);
    console.log(`  路径：${reportPath}`);

    // 发送邮件
    if (options.email) {
      console.log(`  发送到：${options.email}`);
      // TODO: 实现邮件发送
    }

    // 发送飞书通知
    if (config.feishu?.enabled) {
      const feishu = createFeishuIntegration(config);
      await feishu.sendDailyReport({
        date: options.date,
        totalSales: overview.data?.total_sales || 0,
        totalOrders: overview.data?.total_orders || 0,
        conversionRate: overview.data?.conversion_rate || 0
      });
    }

    return {
      path: reportPath,
      report
    };
    
  } catch (error) {
    console.error('✗ 生成失败:', error.message);
    throw error;
  }
}

/**
 * 广告数据分析
 */
export async function adAnalytics(options) {
  const account = getCurrentAccount();
  const config = loadConfig();

  console.log('📈 分析广告数据...');
  console.log(`  活动 ID: ${options.campaignId || '全部'}`);
  console.log(`  指标：${options.metrics || 'roas,ctr,cpc'}`);
  console.log(`  周期：${options.period || 'last_7_days'}`);

  try {
    // Mock 广告数据
    const analytics = {
      roas: 3.5,
      ctr: 2.8,
      cpc: 0.45,
      impressions: 125000,
      clicks: 3500,
      spend: 1575.00,
      revenue: 5512.50,
      period: options.period
    };

    console.log('\n📈 关键指标:');
    console.log(`   ROAS: ${analytics.roas}`);
    console.log(`   CTR: ${analytics.ctr}%`);
    console.log(`   CPC: $${analytics.cpc}`);
    console.log(`   展示：${analytics.impressions}`);
    console.log(`   点击：${analytics.clicks}`);
    console.log(`   花费：$${analytics.spend}`);
    console.log(`   收入：$${analytics.revenue}`);

    return analytics;
    
  } catch (error) {
    console.error('✗ 分析失败:', error.message);
    throw error;
  }
}

/**
 * 监控竞品
 */
export async function trackCompetitors(options) {
  const account = getCurrentAccount();
  const config = loadConfig();

  console.log('🔍 监控竞品...');
  console.log(`  竞品店铺：${options.shops}`);
  console.log(`  监控指标：${options.metrics || 'price,bestseller,reviews'}`);
  console.log(`  预警类型：${options.alert || 'new-product'}`);

  try {
    const shops = options.shops.split(',');
    const metrics = options.metrics ? options.metrics.split(',') : ['price', 'bestseller', 'reviews'];
    
    // Mock 竞品数据
    const competitorData = shops.map(shop => ({
      shop_name: shop,
      products_count: Math.floor(Math.random() * 100) + 50,
      avg_price: (Math.random() * 50 + 10).toFixed(2),
      bestsellers: [
        { name: 'Product A', sales: Math.floor(Math.random() * 1000) },
        { name: 'Product B', sales: Math.floor(Math.random() * 800) }
      ],
      avg_rating: (Math.random() * 2 + 3).toFixed(1),
      new_products: Math.floor(Math.random() * 10)
    }));

    console.log('\n✓ 竞品监控数据:');
    competitorData.forEach(data => {
      console.log(`\n  店铺：${data.shop_name}`);
      console.log(`    商品数：${data.products_count}`);
      console.log(`    平均价格：$${data.avg_price}`);
      console.log(`    平均评分：${data.avg_rating}`);
      console.log(`    新品数量：${data.new_products}`);
    });

    // 发送预警
    if (options.alert) {
      const feishu = createFeishuIntegration(config);
      
      const alertMessage = `🔍 竞品监控预警\n\n发现 ${competitorData.length} 个竞品店铺有新动态:\n` +
        competitorData
          .filter(d => d.new_products > 5)
          .map(d => `- ${d.shop_name}: 新增 ${d.new_products} 个商品`)
          .join('\n') || '暂无预警';

      await feishu.sendWebhookMessage(alertMessage, { type: 'text' });
    }

    return {
      competitors: competitorData,
      timestamp: new Date().toISOString()
    };
    
  } catch (error) {
    console.error('✗ 监控失败:', error.message);
    throw error;
  }
}

/**
 * 生成 CSV 格式报告
 */
function generateCSV(report) {
  const headers = ['指标', '数值'];
  const rows = [
    ['日期', report.date],
    ['总销售额', report.overview?.total_sales || 0],
    ['总订单数', report.overview?.total_orders || 0],
    ['转化率', `${report.overview?.conversion_rate || 0}%`],
    ['商品总数', report.overview?.total_products || 0]
  ];

  return [headers, ...rows].map(row => row.join(',')).join('\n');
}
