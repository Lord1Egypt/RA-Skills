#!/usr/bin/env node

/**
 * OKKI 同步 CLI
 * 用于同步投诉/返单记录到 OKKI CRM
 */

const path = require('path');
const okkiSyncController = require('../api/controllers/okki_sync_controller');
const OkkiSyncLogModule = require('../models/okki_sync_log_model');
const OkkiSyncLog = OkkiSyncLogModule.OkkiSyncLog;

// 命令行参数解析
const args = process.argv.slice(2);
const command = args[0];

/**
 * 显示帮助信息
 */
function showHelp() {
  console.log(`
OKKI 同步 CLI - 售后跟进记录同步工具

用法:
  node okki_sync_cli.js <command> [options]

命令:
  sync-complaint <id>       同步投诉记录到 OKKI
  sync-repeat-order <id>    同步返单报价到 OKKI
  status <id>               查看同步状态
  logs                      查看同步日志
  failed                    查看失败的同步记录
  help                      显示此帮助信息

示例:
  node okki_sync_cli.js sync-complaint CMP-001
  node okki_sync_cli.js sync-repeat-order RO-001
  node okki_sync_cli.js status CMP-001
  node okki_sync_cli.js logs --limit 10
  node okki_sync_cli.js failed

选项:
  --limit <n>               限制返回数量（默认：10）
  --json                    以 JSON 格式输出
`);
}

/**
 * 同步投诉到 OKKI
 */
async function syncComplaint(complaintId) {
  console.log(`🔄 正在同步投诉记录 ${complaintId} 到 OKKI...`);
  
  try {
    const result = await okkiSyncController.syncComplaintToOKKI(complaintId);
    
    if (result.success) {
      console.log(`✅ 同步成功!`);
      console.log(`   投诉 ID: ${result.complaintId}`);
      console.log(`   客户：${result.companyName} (${result.companyId})`);
      console.log(`   OKKI Trail ID: ${result.trailId}`);
      console.log(`   跟进类型：售后跟进 (trail_type=${result.trailType})`);
      console.log(`   匹配方式：${result.matchType}`);
      console.log(`   日志 ID: ${result.logId}`);
    } else {
      console.log(`❌ 同步失败!`);
      console.log(`   原因：${result.message}`);
      if (result.error) {
        console.log(`   错误：${result.error}`);
      }
      if (result.note) {
        console.log(`   提示：${result.note}`);
      }
    }
    
    return result;
  } catch (error) {
    console.error(`❌ 同步失败：${error.message}`);
    return { success: false, error: error.message };
  }
}

/**
 * 同步返单到 OKKI
 */
async function syncRepeatOrder(repeatOrderId) {
  console.log(`🔄 正在同步返单报价 ${repeatOrderId} 到 OKKI...`);
  
  try {
    const result = await okkiSyncController.syncRepeatOrderToOKKI(repeatOrderId);
    
    if (result.success) {
      console.log(`✅ 同步成功!`);
      console.log(`   返单 ID: ${result.repeatOrderId}`);
      console.log(`   客户：${result.companyName} (${result.companyId})`);
      console.log(`   OKKI Trail ID: ${result.trailId}`);
      console.log(`   跟进类型：售后跟进 (trail_type=${result.trailType})`);
      console.log(`   匹配方式：${result.matchType}`);
      console.log(`   日志 ID: ${result.logId}`);
    } else {
      console.log(`❌ 同步失败!`);
      console.log(`   原因：${result.message}`);
      if (result.error) {
        console.log(`   错误：${result.error}`);
      }
      if (result.note) {
        console.log(`   提示：${result.note}`);
      }
    }
    
    return result;
  } catch (error) {
    console.error(`❌ 同步失败：${error.message}`);
    return { success: false, error: error.message };
  }
}

/**
 * 查看同步状态
 */
function showStatus(id) {
  console.log(`📊 查询同步状态：${id}`);
  
  const log = OkkiSyncLogModule.getById(id);
  
  if (!log) {
    console.log(`❌ 未找到同步记录`);
    return null;
  }
  
  console.log(`\n📋 同步日志详情:`);
  console.log(`   日志 ID: ${log.id}`);
  console.log(`   类型：${log.syncType === 'complaint' ? '投诉' : '返单'}`);
  
  if (log.complaintId) {
    console.log(`   投诉 ID: ${log.complaintId}`);
  }
  if (log.repeatOrderId) {
    console.log(`   返单 ID: ${log.repeatOrderId}`);
  }
  
  console.log(`   客户 ID: ${log.companyId || '(未关联)'}`);
  console.log(`   OKKI Trail ID: ${log.trailId || '(未生成)'}`);
  console.log(`   状态：${log.status === 'success' ? '✅ 成功' : log.status === 'failed' ? '❌ 失败' : '⏳ 待处理'}`);
  console.log(`   匹配方式：${log.matchType || '(无)'}`);
  console.log(`   同步时间：${log.syncedAt}`);
  
  if (log.errorMessage) {
    console.log(`   错误信息：${log.errorMessage}`);
  }
  if (log.retryCount > 0) {
    console.log(`   重试次数：${log.retryCount}`);
  }
  
  return log.toObject();
}

/**
 * 查看同步日志
 */
function showLogs(options = {}) {
  const limit = options.limit || 10;
  const logs = OkkiSyncLogModule.getRecent(limit);
  
  if (logs.length === 0) {
    console.log(`📭 暂无同步日志`);
    return [];
  }
  
  console.log(`\n📋 最近 ${logs.length} 条同步日志:\n`);
  
  logs.forEach((log, index) => {
    const statusIcon = log.status === 'success' ? '✅' : log.status === 'failed' ? '❌' : '⏳';
    const typeLabel = log.syncType === 'complaint' ? '投诉' : '返单';
    const businessId = log.complaintId || log.repeatOrderId;
    
    console.log(`${index + 1}. ${statusIcon} [${typeLabel}] ${businessId}`);
    console.log(`   日志 ID: ${log.id}`);
    console.log(`   客户 ID: ${log.companyId || '(未关联)'}`);
    console.log(`   Trail ID: ${log.trailId || '(未生成)'}`);
    console.log(`   时间：${log.syncedAt}`);
    if (log.errorMessage) {
      console.log(`   错误：${log.errorMessage}`);
    }
    console.log('');
  });
  
  return logs.map(log => log.toObject());
}

/**
 * 查看失败的同步记录
 */
function showFailed() {
  const logs = OkkiSyncLogModule.getFailed();
  
  if (logs.length === 0) {
    console.log(`✅ 没有失败的同步记录`);
    return [];
  }
  
  console.log(`\n❌ 失败的同步记录 (${logs.length}条):\n`);
  
  logs.forEach((log, index) => {
    const typeLabel = log.syncType === 'complaint' ? '投诉' : '返单';
    const businessId = log.complaintId || log.repeatOrderId;
    
    console.log(`${index + 1}. [${typeLabel}] ${businessId}`);
    console.log(`   日志 ID: ${log.id}`);
    console.log(`   错误：${log.errorMessage}`);
    console.log(`   时间：${log.syncedAt}`);
    if (log.retryCount > 0) {
      console.log(`   重试：${log.retryCount}次`);
    }
    console.log('');
  });
  
  return logs.map(log => log.toObject());
}

/**
 * 主函数
 */
async function main() {
  if (!command || command === 'help' || command === '--help' || command === '-h') {
    showHelp();
    return;
  }
  
  switch (command) {
    case 'sync-complaint':
      if (!args[1]) {
        console.error('❌ 错误：请提供投诉 ID');
        console.log('用法：node okki_sync_cli.js sync-complaint <id>');
        process.exit(1);
      }
      await syncComplaint(args[1]);
      break;
      
    case 'sync-repeat-order':
      if (!args[1]) {
        console.error('❌ 错误：请提供返单 ID');
        console.log('用法：node okki_sync_cli.js sync-repeat-order <id>');
        process.exit(1);
      }
      await syncRepeatOrder(args[1]);
      break;
      
    case 'status':
      if (!args[1]) {
        console.error('❌ 错误：请提供 ID');
        console.log('用法：node okki_sync_cli.js status <id>');
        process.exit(1);
      }
      showStatus(args[1]);
      break;
      
    case 'logs':
      {
        const limitIndex = args.indexOf('--limit');
        const limit = limitIndex !== -1 && args[limitIndex + 1] 
          ? parseInt(args[limitIndex + 1]) 
          : 10;
        showLogs({ limit });
      }
      break;
      
    case 'failed':
      showFailed();
      break;
      
    default:
      console.error(`❌ 未知命令：${command}`);
      showHelp();
      process.exit(1);
  }
}

// 执行主函数
main().catch(error => {
  console.error('❌ 发生错误:', error.message);
  process.exit(1);
});
