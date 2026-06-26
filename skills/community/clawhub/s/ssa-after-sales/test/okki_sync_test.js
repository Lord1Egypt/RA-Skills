#!/usr/bin/env node

/**
 * OKKI 同步功能测试脚本
 */

const okkiSyncController = require('../api/controllers/okki_sync_controller');
const OkkiSyncLogModule = require('../models/okki_sync_log_model');

async function runTests() {
  console.log('🧪 OKKI 同步功能测试\n');
  
  let passed = 0;
  let failed = 0;
  
  // 测试 1: 检查控制器导出
  console.log('测试 1: 检查控制器导出...');
  if (okkiSyncController.syncComplaintToOKKI && 
      okkiSyncController.syncRepeatOrderToOKKI &&
      okkiSyncController.CONFIG) {
    console.log('✅ 通过 - 控制器函数已正确导出\n');
    passed++;
  } else {
    console.log('❌ 失败 - 控制器函数缺失\n');
    failed++;
  }
  
  // 测试 2: 检查日志模型导出
  console.log('测试 2: 检查日志模型导出...');
  if (OkkiSyncLogModule.create && 
      OkkiSyncLogModule.getById && 
      OkkiSyncLogModule.getRecent &&
      OkkiSyncLogModule.getFailed) {
    console.log('✅ 通过 - 日志模型函数已正确导出\n');
    passed++;
  } else {
    console.log('❌ 失败 - 日志模型函数缺失\n');
    failed++;
  }
  
  // 测试 3: 检查配置
  console.log('测试 3: 检查 OKKI 配置...');
  const config = okkiSyncController.CONFIG;
  if (config.TRAIL_TYPE.AFTER_SALES === 107) {
    console.log(`✅ 通过 - 售后跟进类型正确 (trail_type=${config.TRAIL_TYPE.AFTER_SALES})\n`);
    passed++;
  } else {
    console.log('❌ 失败 - 售后跟进类型错误\n');
    failed++;
  }
  
  // 测试 4: 创建测试日志
  console.log('测试 4: 创建测试日志...');
  try {
    const testLog = OkkiSyncLogModule.create({
      complaintId: 'TEST-001',
      status: 'success',
      syncType: 'complaint',
      trailId: 'TRAIL-TEST-001',
      companyId: 'COMPANY-TEST',
      matchType: 'customer_id'
    });
    
    if (testLog && testLog.id) {
      console.log(`✅ 通过 - 日志创建成功 (ID: ${testLog.id})\n`);
      passed++;
    } else {
      console.log('❌ 失败 - 日志创建失败\n');
      failed++;
    }
  } catch (error) {
    console.log(`❌ 失败 - ${error.message}\n`);
    failed++;
  }
  
  // 测试 5: 查询日志
  console.log('测试 5: 查询测试日志...');
  try {
    const log = OkkiSyncLogModule.getById('TEST-001');
    if (log && log.complaintId === 'TEST-001') {
      console.log(`✅ 通过 - 日志查询成功\n`);
      passed++;
    } else {
      console.log('❌ 失败 - 日志查询失败\n');
      failed++;
    }
  } catch (error) {
    console.log(`❌ 失败 - ${error.message}\n`);
    failed++;
  }
  
  // 测试 6: 获取最近日志
  console.log('测试 6: 获取最近日志...');
  try {
    const logs = OkkiSyncLogModule.getRecent(5);
    console.log(`✅ 通过 - 获取到 ${logs.length} 条日志\n`);
    passed++;
  } catch (error) {
    console.log(`❌ 失败 - ${error.message}\n`);
    failed++;
  }
  
  // 总结
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━');
  console.log(`测试完成：${passed + failed} 项`);
  console.log(`✅ 通过：${passed}`);
  console.log(`❌ 失败：${failed}`);
  console.log('━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n');
  
  return { passed, failed, total: passed + failed };
}

// 运行测试
runTests().then(result => {
  process.exit(result.failed > 0 ? 1 : 0);
}).catch(error => {
  console.error('测试执行失败:', error);
  process.exit(1);
});
