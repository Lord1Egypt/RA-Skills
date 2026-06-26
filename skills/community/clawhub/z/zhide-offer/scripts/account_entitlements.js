#!/usr/bin/env node
/**
 * 查询当前账号权益和今日剩余额度
 * 用法: node account_entitlements.js
 */
const { mcpCall } = require('./mcp_client');

async function main() {
  const result = await mcpCall('account.entitlements', {});
  const data = result?.data || result || {};
  const limit = Number(data.mcpDailyLimit || 0);
  const used = Number(data.mcpUsedToday || 0);
  const remaining = Math.max(limit - used, 0);

  console.log('========== 账号权益 ==========');
  console.log('用户等级:   ' + (data.userLevelDesc || data.userLevel || '-'));
  console.log('到期时间:   ' + (data.expirationTime || '-'));
  console.log('每日限额:   ' + (limit || '-'));
  console.log('今日已用:   ' + used);
  console.log('今日剩余:   ' + remaining);
}

main().catch(e => { console.error('错误:', e.message); process.exit(1); });
