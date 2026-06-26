#!/usr/bin/env node
/**
 * 飞书多维表格存储工具
 * 自动将日报数据存储到飞书多维表格
 */

import { readFileSync } from 'fs';
import { homedir } from 'os';
import { join } from 'path';

// 飞书配置
const FEISHU_CONFIG = {
  app_token: 'Xzklb57ztaYtqRseuRXcXDMsnEh',
  table_id: 'tbly9gn6j0jjvxXD',  // 修复：使用正确的 table_id
  // 使用字段名称（而不是ID）
  fieldNames: {
    title: '标题',
    url: '链接',
    source: '来源',
    summary: '摘要',
    content: '正文',
    publishedTime: '发布时间',
    industry: '产业类别/输入关键词',  // 修复：使用完整的字段名
    searchEngine: '搜索引擎',
    createdTime: '创建时间'
  },
  app_id: 'cli_a92fba8c65e35cc4',
  app_secret: 'UFUvM2wNSkErIxe7t63ZrgyecakLwNQR'
};

// 缓存 tenant_access_token
let cachedToken = null;
let tokenExpireTime = 0;

/**
 * 获取飞书 tenant_access_token
 */
async function getTenantAccessToken() {
  // 检查缓存
  if (cachedToken && Date.now() < tokenExpireTime) {
    return cachedToken;
  }
  
  try {
    const response = await fetch('https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        app_id: FEISHU_CONFIG.app_id,
        app_secret: FEISHU_CONFIG.app_secret
      })
    });
    
    const data = await response.json();
    
    if (data.code !== 0) {
      console.error('❌ 获取 tenant_access_token 失败:', data.msg);
      return null;
    }
    
    // 缓存 token（提前5分钟过期）
    cachedToken = data.tenant_access_token;
    tokenExpireTime = Date.now() + (data.expire - 300) * 1000;
    
    return cachedToken;
  } catch (err) {
    console.error('❌ 获取 tenant_access_token 失败:', err.message);
    return null;
  }
}

/**
 * 将时间戳转换为毫秒
 */
function dateToTimestamp(dateStr) {
  if (!dateStr) return null;
  try {
    const date = new Date(dateStr);
    if (isNaN(date.getTime())) return null;
    return date.getTime();
  } catch {
    return null;
  }
}

/**
 * 存储单条记录到飞书多维表格
 */
async function saveRecordToBitable(record, industry, accessToken) {
  const url = `https://open.feishu.cn/open-apis/bitable/v1/apps/${FEISHU_CONFIG.app_token}/tables/${FEISHU_CONFIG.table_id}/records`;
  
  // 构造字段数据 - 根据飞书表格的实际字段类型
  const fieldData = {};
  
  // 1. 文本字段
  if (record.title) fieldData['标题'] = record.title;
  if (record.source) fieldData['来源'] = record.source;
  if (record.summary) fieldData['摘要'] = record.summary;
  if (record.content) fieldData['正文'] = record.content;
  
  // 2. URL 字段（特殊格式）
  if (record.url) {
    fieldData['链接'] = {
      link: record.url,
      text: record.url
    };
  }
  
  // 3. 发布时间（文本字段，不是时间戳）
  if (record.publishedDate) {
    fieldData['发布时间'] = record.publishedDate;
  }
  
  // 4. SingleSelect 字段（直接使用字符串值）
  if (industry) {
    fieldData['产业类别/输入关键词'] = industry;
  }
  
  if (record.searchEngine) {
    // 根据搜索引擎名称映射到选项值
    const engineMap = {
      'tavily': 'Tavily',
      'brave': 'Brave',
      'tech-news-digest': 'tech-news-digest'
    };
    fieldData['搜索引擎'] = engineMap[record.searchEngine] || record.searchEngine;
  }
  
  // 5. 创建时间（文本字段）
  fieldData['创建时间'] = new Date().toISOString();
  
  try {
    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        fields: fieldData
      })
    });
    
    if (!response.ok) {
      const errorText = await response.text();
      console.error(`  ❌ 存储失败 (${response.status}): ${errorText}`);
      return { success: false, error: errorText };
    }
    
    const data = await response.json();
    
    if (data.code !== 0) {
      console.error(`  ❌ API错误 (${data.code}): ${data.msg}`);
      return { success: false, error: data.msg };
    }
    
    return { success: true, record_id: data.data.record.record_id };
  } catch (err) {
    console.error(`  ❌ 网络错误: ${err.message}`);
    return { success: false, error: err.message };
  }
}

/**
 * 批量存储记录到飞书多维表格
 */
async function saveRecordsToBitable(records, industry, verbose = false) {
  console.log('\n📤 存储到飞书多维表格...');
  console.log(`   App Token: ${FEISHU_CONFIG.app_token}`);
  console.log(`   Table ID: ${FEISHU_CONFIG.table_id}`);
  console.log(`   记录数: ${records.length}\n`);
  
  // 获取 tenant_access_token
  const accessToken = await getTenantAccessToken();
  
  if (!accessToken) {
    console.error('❌ 无法获取飞书 tenant_access_token\n');
    return {
      success: false,
      stats: { success: 0, failed: records.length }
    };
  }
  
  const stats = {
    success: 0,
    failed: 0
  };
  
  // 逐条存储（避免并发限制）
  for (let i = 0; i < records.length; i++) {
    const record = records[i];
    
    if (verbose) {
      process.stderr.write(`   [${i + 1}/${records.length}] ${record.title.slice(0, 40)}... `);
    }
    
    const result = await saveRecordToBitable(record, industry, accessToken);
    
    if (result.success) {
      stats.success++;
      if (verbose) {
        process.stderr.write('✅\n');
      }
    } else {
      stats.failed++;
      if (verbose) {
        process.stderr.write('❌\n');
      }
    }
    
    // 避免频率限制
    if (i < records.length - 1) {
      await new Promise(resolve => setTimeout(resolve, 200));
    }
  }
  
  console.log(`\n📊 存储统计:`);
  console.log(`   成功: ${stats.success}条`);
  console.log(`   失败: ${stats.failed}条\n`);
  
  return {
    success: stats.failed === 0,
    stats
  };
}

// 导出函数
export { saveRecordsToBitable, getTenantAccessToken };

// 如果直接运行，显示帮助
if (import.meta.url === `file://${process.argv[1]}`) {
  console.log('飞书多维表格存储工具');
  console.log('');
  console.log('用法:');
  console.log('  import { saveRecordsToBitable } from "./feishu-bitable-saver.mjs";');
  console.log('  await saveRecordsToBitable(records, "石油", true);');
}
