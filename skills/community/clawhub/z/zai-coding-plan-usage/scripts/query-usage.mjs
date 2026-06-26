#!/usr/bin/env node

/**
 * 智谱用量查询脚本
 * 从 OpenClaw 配置文件或环境变量读取 API Key
 */

import https from 'https';
import fs from 'fs';
import path from 'path';
import os from 'os';

// 获取 API Key
const getApiKey = () => {
  const authPath = path.join(os.homedir(), '.openclaw', 'agents', 'main', 'agent', 'auth-profiles.json');
  
  // 优先从 OpenClaw 配置读取
  if (fs.existsSync(authPath)) {
    try {
      const authData = JSON.parse(fs.readFileSync(authPath, 'utf-8'));
      const key = authData?.profiles?.['zai:default']?.key;
      if (key) return key;
    } catch (e) {}
  }
  
  // 备用：从环境变量读取
  return process.env.ZAI_API_KEY || process.env.ZHIPU_API_KEY || '';
};

const apiKey = getApiKey();
if (!apiKey) process.exit(1);

// API 配置
const BASE_URL = 'open.bigmodel.cn';
const ENDPOINTS = {
  modelUsage: '/api/monitor/usage/model-usage',
  toolUsage: '/api/monitor/usage/tool-usage',
  quotaLimit: '/api/monitor/usage/quota/limit'
};

// 时间范围：过去 24 小时
const now = new Date();
const startDate = new Date(now.getTime() - 24 * 60 * 60 * 1000);
const formatDateTime = (date) => {
  const pad = (n) => String(n).padStart(2, '0');
  return `${date.getFullYear()}-${pad(date.getMonth() + 1)}-${pad(date.getDate())} ${pad(date.getHours())}:${pad(date.getMinutes())}:${pad(date.getSeconds())}`;
};
const startTime = formatDateTime(startDate);
const endTime = formatDateTime(now);

// HTTP 请求
const fetchData = (apiPath) => {
  return new Promise((resolve, reject) => {
    const queryParams = apiPath.includes('quota') ? '' : `?startTime=${encodeURIComponent(startTime)}&endTime=${encodeURIComponent(endTime)}`;
    const options = {
      hostname: BASE_URL,
      port: 443,
      path: apiPath + queryParams,
      method: 'GET',
      headers: {
        'Authorization': apiKey,
        'Accept-Language': 'zh-CN,zh',
        'Content-Type': 'application/json'
      }
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        if (res.statusCode !== 200) {
          reject(new Error(`HTTP ${res.statusCode}: ${data}`));
          return;
        }
        try {
          resolve(JSON.parse(data));
        } catch (e) {
          reject(new Error(`JSON 解析失败: ${data}`));
        }
      });
    });
    req.on('error', reject);
    req.end();
  });
};

// 处理配额数据
const processQuotaData = (data) => {
  if (!data?.data?.limits) return [];
  return data.data.limits.map(item => {
    if (item.type === 'TOKENS_LIMIT') {
      return {
        type: 'Token 用量 (5小时)',
        percentage: item.percentage + '%',
        status: item.percentage >= 90 ? '🔴' : item.percentage >= 70 ? '🟡' : '🟢'
      };
    }
    if (item.type === 'TIME_LIMIT') {
      return {
        type: 'MCP 用量 (1个月)',
        percentage: item.percentage + '%',
        currentUsage: item.currentValue || '-',
        total: item.usage || '-',
        status: item.percentage >= 90 ? '🔴' : item.percentage >= 70 ? '🟡' : '🟢'
      };
    }
    return item;
  });
};

// 主函数
const main = async () => {
  console.log('📊 智谱 AI 用量查询');
  console.log('━'.repeat(40));
  console.log(`⏰ ${startTime} ~ ${endTime}\n`);

  try {
    // 1. 配额
    console.log('📌 配额使用情况:');
    const quotaData = await fetchData(ENDPOINTS.quotaLimit);
    const limits = processQuotaData(quotaData);
    if (limits.length > 0) {
      limits.forEach(item => {
        console.log(`  ${item.type}: ${item.percentage} ${item.status || ''}`);
        if (item.currentUsage) console.log(`    已用: ${item.currentUsage} / 总量: ${item.total}`);
      });
    } else {
      console.log('  暂无数据');
    }
    console.log('');

    // 2. 模型
    console.log('📈 模型调用统计:');
    try {
      const modelData = await fetchData(ENDPOINTS.modelUsage);
      const usage = modelData?.data;
      if (Array.isArray(usage)) {
        usage.slice(0, 5).forEach(item => {
          console.log(`  ${item.model || item.name || '-'}: ${item.count || item.calls || '-'} 次`);
        });
      } else if (usage) {
        console.log(`  总调用: ${usage.totalCalls || '-'} 次`);
        console.log(`  总 Tokens: ${usage.totalTokens || '-'}`);
      } else {
        console.log('  暂无数据');
      }
    } catch (e) {
      console.log(`  ⚠️ ${e.message}`);
    }
    console.log('');

    // 3. 工具
    console.log('🔧 工具调用统计:');
    try {
      const toolData = await fetchData(ENDPOINTS.toolUsage);
      const usage = toolData?.data;
      if (Array.isArray(usage)) {
        usage.slice(0, 5).forEach(item => {
          console.log(`  ${item.tool || item.name || '-'}: ${item.count || item.calls || '-'} 次`);
        });
      } else if (usage) {
        console.log(`  总调用: ${usage.totalCalls || '-'} 次`);
      } else {
        console.log('  暂无数据');
      }
    } catch (e) {
      console.log(`  ⚠️ ${e.message}`);
    }

    console.log('\n' + '━'.repeat(40));
    console.log('✅ 查询完成');
  } catch (error) {
    console.error('\n❌ 查询失败:', error.message);
    process.exit(1);
  }
};

main();
