#!/usr/bin/env node

/**
 * TikTok Shop Automation - API 集成测试
 * 测试所有核心功能
 */

import { createTikTokAPI } from './src/api.js';
import { createFeishuIntegration } from './src/feishu.js';
import { loadConfig, saveConfig } from './src/config.js';
import chalk from 'chalk';

console.log(chalk.green('\n🧪 TikTok Shop Automation - API 集成测试\n'));
console.log('=' .repeat(60));

async function runTests() {
  const results = {
    passed: 0,
    failed: 0,
    tests: []
  };

  // 加载配置
  console.log('\n📋 测试 1: 加载配置');
  try {
    const config = loadConfig();
    console.log(chalk.green('✓ 配置加载成功'));
    console.log(`  Mock 模式：${config.tiktok.useMock ? '是' : '否'}`);
    console.log(`  飞书集成：${config.feishu.enabled ? '已启用' : '未启用'}`);
    results.passed++;
    results.tests.push({ name: '加载配置', status: 'passed' });
  } catch (error) {
    console.log(chalk.red('✗ 配置加载失败'));
    results.failed++;
    results.tests.push({ name: '加载配置', status: 'failed', error: error.message });
  }

  // 测试 Mock API - 获取商品列表
  console.log('\n📦 测试 2: Mock API - 获取商品列表');
  try {
    const api = createTikTokAPI();
    const result = await api.listProducts('mock_shop');
    
    if (result.code === 0 && result.data?.products) {
      console.log(chalk.green('✓ 商品列表获取成功'));
      console.log(`  商品数量：${result.data.products.length}`);
      result.data.products.forEach(p => {
        console.log(`    - ${p.title} ($${p.price})`);
      });
      results.passed++;
      results.tests.push({ name: 'Mock API - 商品列表', status: 'passed' });
    } else {
      throw new Error('API 返回异常');
    }
  } catch (error) {
    console.log(chalk.red('✗ 商品列表获取失败'));
    results.failed++;
    results.tests.push({ name: 'Mock API - 商品列表', status: 'failed', error: error.message });
  }

  // 测试 Mock API - 获取订单列表
  console.log('\n📋 测试 3: Mock API - 获取订单列表');
  try {
    const api = createTikTokAPI();
    const result = await api.listOrders('mock_shop', { status: 'pending' });
    
    if (result.code === 0 && result.data?.orders) {
      console.log(chalk.green('✓ 订单列表获取成功'));
      console.log(`  待处理订单：${result.data.orders.length}`);
      result.data.orders.forEach(o => {
        console.log(`    - ${o.order_id}: $${o.amount}`);
      });
      results.passed++;
      results.tests.push({ name: 'Mock API - 订单列表', status: 'passed' });
    } else {
      throw new Error('API 返回异常');
    }
  } catch (error) {
    console.log(chalk.red('✗ 订单列表获取失败'));
    results.failed++;
    results.tests.push({ name: 'Mock API - 订单列表', status: 'failed', error: error.message });
  }

  // 测试 Mock API - 创建商品
  console.log('\n📦 测试 4: Mock API - 创建商品');
  try {
    const api = createTikTokAPI();
    const result = await api.createProduct('mock_shop', {
      title: 'Test Product',
      price: 99.99,
      stock: 100,
      description: 'Test description'
    });
    
    if (result.code === 0 && result.data?.product_id) {
      console.log(chalk.green('✓ 商品创建成功'));
      console.log(`  商品 ID: ${result.data.product_id}`);
      results.passed++;
      results.tests.push({ name: 'Mock API - 创建商品', status: 'passed' });
    } else {
      throw new Error('API 返回异常');
    }
  } catch (error) {
    console.log(chalk.red('✗ 商品创建失败'));
    results.failed++;
    results.tests.push({ name: 'Mock API - 创建商品', status: 'failed', error: error.message });
  }

  // 测试 Mock API - 更新订单状态
  console.log('\n📋 测试 5: Mock API - 更新订单状态');
  try {
    const api = createTikTokAPI();
    const result = await api.updateOrderStatus('mock_shop', 'ORD001', 'shipped', 'FX123456');
    
    if (result.code === 0 && result.data?.updated) {
      console.log(chalk.green('✓ 订单状态更新成功'));
      console.log(`  订单：ORD001, 状态：shipped`);
      results.passed++;
      results.tests.push({ name: 'Mock API - 更新订单', status: 'passed' });
    } else {
      throw new Error('API 返回异常');
    }
  } catch (error) {
    console.log(chalk.red('✗ 订单状态更新失败'));
    results.failed++;
    results.tests.push({ name: 'Mock API - 更新订单', status: 'failed', error: error.message });
  }

  // 测试 Mock API - 获取销售数据
  console.log('\n📊 测试 6: Mock API - 获取销售数据');
  try {
    const api = createTikTokAPI();
    const result = await api.getShopOverview('mock_shop', 'last_30_days');
    
    if (result.code === 0 && result.data?.total_sales) {
      console.log(chalk.green('✓ 销售数据获取成功'));
      console.log(`  总销售额：$${result.data.total_sales}`);
      console.log(`  总订单数：${result.data.total_orders}`);
      console.log(`  转化率：${result.data.conversion_rate}%`);
      results.passed++;
      results.tests.push({ name: 'Mock API - 销售数据', status: 'passed' });
    } else {
      throw new Error('API 返回异常');
    }
  } catch (error) {
    console.log(chalk.red('✗ 销售数据获取失败'));
    results.failed++;
    results.tests.push({ name: 'Mock API - 销售数据', status: 'failed', error: error.message });
  }

  // 测试飞书集成 - Mock 模式
  console.log('\n📤 测试 7: 飞书集成 - 发送消息（Mock）');
  try {
    const config = loadConfig();
    config.tiktok.useMock = true;
    config.feishu.enabled = true;
    config.feishu.webhookUrl = 'https://mock.feishu.cn/webhook';
    saveConfig(config);
    
    const feishu = createFeishuIntegration(config);
    const result = await feishu.sendWebhookMessage('测试消息', { type: 'text' });
    
    if (result.success) {
      console.log(chalk.green('✓ 飞书消息发送成功（Mock）'));
      results.passed++;
      results.tests.push({ name: '飞书集成 - 发送消息', status: 'passed' });
    } else {
      throw new Error('发送失败');
    }
  } catch (error) {
    console.log(chalk.red('✗ 飞书消息发送失败'));
    results.failed++;
    results.tests.push({ name: '飞书集成 - 发送消息', status: 'failed', error: error.message });
  }

  // 测试飞书集成 - 同步订单
  console.log('\n📊 测试 8: 飞书集成 - 同步订单（Mock）');
  try {
    const config = loadConfig();
    config.tiktok.useMock = true;
    config.feishu.enabled = true;
    config.feishu.appToken = 'mock_app_token';
    config.feishu.tableId = 'mock_table_id';
    saveConfig(config);
    
    const feishu = createFeishuIntegration(config);
    const mockOrders = [
      { order_id: 'TEST001', status: 'pending', amount: 29.99, customer: { name: 'Test' }, items: [], created_at: new Date().toISOString() }
    ];
    const result = await feishu.syncOrdersToBitable(mockOrders);
    
    if (result.success) {
      console.log(chalk.green('✓ 订单同步成功（Mock）'));
      console.log(`  同步记录数：${result.synced}`);
      results.passed++;
      results.tests.push({ name: '飞书集成 - 同步订单', status: 'passed' });
    } else {
      throw new Error('同步失败');
    }
  } catch (error) {
    console.log(chalk.red('✗ 订单同步失败'));
    results.failed++;
    results.tests.push({ name: '飞书集成 - 同步订单', status: 'failed', error: error.message });
  }

  // 测试配置管理
  console.log('\n⚙️  测试 9: 配置管理 - 保存和加载');
  try {
    const config = loadConfig();
    config.testField = 'test_value';
    saveConfig(config);
    
    const loadedConfig = loadConfig();
    if (loadedConfig.testField === 'test_value') {
      console.log(chalk.green('✓ 配置保存和加载成功'));
      results.passed++;
      results.tests.push({ name: '配置管理', status: 'passed' });
    } else {
      throw new Error('配置值不匹配');
    }
  } catch (error) {
    console.log(chalk.red('✗ 配置管理失败'));
    results.failed++;
    results.tests.push({ name: '配置管理', status: 'failed', error: error.message });
  }

  // 输出测试结果
  console.log('\n' + '='.repeat(60));
  console.log(chalk.green('\n📊 测试结果汇总:'));
  console.log(`  通过：${chalk.green(results.passed)}`);
  console.log(`  失败：${chalk.red(results.failed)}`);
  console.log(`  总计：${results.passed + results.failed}`);
  console.log(`  成功率：${((results.passed / (results.passed + results.failed)) * 100).toFixed(1)}%`);
  
  console.log('\n📋 详细结果:');
  results.tests.forEach(test => {
    const icon = test.status === 'passed' ? '✓' : '✗';
    const color = test.status === 'passed' ? chalk.green : chalk.red;
    console.log(`  ${color(icon)} ${test.name}`);
    if (test.error) {
      console.log(`      错误：${test.error}`);
    }
  });

  console.log('\n' + '='.repeat(60));
  
  if (results.failed === 0) {
    console.log(chalk.green('\n🎉 所有测试通过！API 集成完成！\n'));
    process.exit(0);
  } else {
    console.log(chalk.yellow('\n⚠️  部分测试失败，请检查错误信息\n'));
    process.exit(1);
  }
}

// 运行测试
runTests().catch(error => {
  console.error(chalk.red('\n✗ 测试执行失败:'), error);
  process.exit(1);
});
