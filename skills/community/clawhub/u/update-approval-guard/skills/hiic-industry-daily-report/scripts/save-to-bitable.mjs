#!/usr/bin/env node
/**
 * 飞书多维表格存储脚本
 * 将产业日报数据存储到飞书多维表格
 */

import { parseArgs } from 'util';
import { readFileSync, writeFileSync, existsSync } from 'fs';
import { homedir } from 'os';
import { join } from 'path';

const { values } = parseArgs({
  options: {
    input: { type: 'string', short: 'i' },
    industry: { type: 'string', short: 'n' },
    dryRun: { type: 'boolean', short: 'd', default: false },
    verbose: { type: 'boolean', short: 'v', default: false }
  },
  allowPositionals: true
});

// 多维表格配置
const BITABLE_CONFIG = {
  app_token: 'Xzklb57ztaYtqRseuRXcXDMsnEh',
  table_id: 'tbl08F2rfot9VODa',
  fields: {
    title: 'fldSbbPRXu',
    url: 'fldlcZID8h',
    source: 'fldgkborGD',
    summary: 'fldItHUOkg',
    publishedTime: 'fldXl9Lbum',
    industry: 'fldBKfPPQE',
    searchEngine: 'fld8P3lTiQ',
    createdTime: 'fldwxjj5Ki'
  }
};

// 配置文件路径
const CONFIG_FILE = join(homedir(), '.openclaw', 'workspace', 'hiic-bitable-config.json');

/**
 * 加载配置
 */
function loadConfig() {
  if (existsSync(CONFIG_FILE)) {
    const config = JSON.parse(readFileSync(CONFIG_FILE, 'utf-8'));
    return { ...BITABLE_CONFIG, ...config };
  }
  return BITABLE_CONFIG;
}

/**
 * 保存配置
 */
function saveConfig(config) {
  writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2), 'utf-8');
}

/**
 * 转换日期为时间戳（毫秒）
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
async function saveToBitable(record, config, industry) {
  if (values.dryRun) {
    if (values.verbose) {
      console.error('🔍 [DRY RUN] 将存储记录:', record.title);
    }
    return { success: true, dryRun: true };
  }

  try {
    // 调用 feishu_bitable_create_record 工具
    // 注意：这里需要通过某种方式调用 OpenClaw 的工具
    // 由于这是 Node.js 脚本，我们需要使用其他方式
    
    const response = await fetch('http://localhost:3000/api/feishu/bitable/record', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        app_token: config.app_token,
        table_id: config.table_id,
        fields: {
          [config.fields.title]: record.title,
          [config.fields.url]: {
            text: record.title,
            link: record.url
          },
          [config.fields.source]: record.source,
          [config.fields.summary]: record.summary,
          [config.fields.publishedTime]: dateToTimestamp(record.publishedDate),
          [config.fields.industry]: industry,
          [config.fields.searchEngine]: record.searchEngine === 'tavily' ? 'Tavily' : 
                                         record.searchEngine === 'brave' ? 'Brave' : '双引擎'
        }
      })
    });

    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }

    const result = await response.json();
    
    if (values.verbose) {
      console.error(`✅ 已存储: ${record.title}`);
    }
    
    return { success: true, record_id: result.record_id };
  } catch (err) {
    if (values.verbose) {
      console.error(`❌ 存储失败: ${record.title} - ${err.message}`);
    }
    return { success: false, error: err.message };
  }
}

/**
 * 批量存储记录
 */
async function saveRecords(records, industry) {
  const config = loadConfig();
  const stats = {
    total: records.length,
    success: 0,
    failed: 0,
    dryRun: 0
  };

  if (values.verbose) {
    console.error(`\n📤 开始存储到飞书多维表格`);
    console.error(`   表格: ${config.app_token}`);
    console.error(`   产业: ${industry}`);
    console.error(`   数量: ${records.length}条\n`);
  }

  for (const record of records) {
    const result = await saveToBitable(record, config, industry);
    
    if (result.success) {
      if (result.dryRun) {
        stats.dryRun++;
      } else {
        stats.success++;
      }
    } else {
      stats.failed++;
    }

    // 避免请求过快
    await new Promise(resolve => setTimeout(resolve, 200));
  }

  if (values.verbose) {
    console.error(`\n📊 存储统计:`);
    console.error(`   成功: ${stats.success}条`);
    if (stats.dryRun > 0) {
      console.error(`   模拟: ${stats.dryRun}条`);
    }
    console.error(`   失败: ${stats.failed}条\n`);
  }

  return stats;
}

/**
 * 主函数
 */
async function main() {
  if (!values.input) {
    console.error('❌ 请提供输入文件 (--input)');
    console.error('用法: node save-to-bitable.mjs --input <file> --industry <name>');
    process.exit(1);
  }

  if (!values.industry) {
    console.error('❌ 请提供产业名称 (--industry)');
    process.exit(1);
  }

  // 读取输入文件
  const inputFile = values.input;
  if (!existsSync(inputFile)) {
    console.error(`❌ 文件不存在: ${inputFile}`);
    process.exit(1);
  }

  const data = JSON.parse(readFileSync(inputFile, 'utf-8'));
  
  if (!data.results || !Array.isArray(data.results)) {
    console.error('❌ 输入文件格式错误，需要包含 results 数组');
    process.exit(1);
  }

  await saveRecords(data.results, values.industry);
}

main().catch(err => {
  console.error('❌ 错误:', err.message);
  process.exit(1);
});
