#!/usr/bin/env node

/**
 * Shuttle AI Chatbot Skill (Optimized)
 * 直接调用后端 /chat_direct API，无需浏览器自动化
 * 
 * 优化：
 * - 移除浏览器自动化（不稳定）
 * 直接使用 curl 调用本地 AI 服务
 * - session_id 格式：shuttle-cli-YYYYMMDD
 * - 更快速、更稳定
 */

const { program } = require('commander');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');
const crypto = require('crypto');
const util = require('util');
const execPromise = util.promisify(exec);

// 生成日期格式的 session_id：shuttle-cli-{隨機16碼}_{YYYYMMDD}
function generateSessionId() {
  const today = new Date();
  const yyyy = today.getFullYear();
  const mm = String(today.getMonth() + 1).padStart(2, '0');
  const dd = String(today.getDate()).padStart(2, '0');
  const datePart = `${yyyy}${mm}${dd}`;
  
  // 生成 16 字節隨機碼（32 個十六進制字符）
  const randomPart = crypto.randomBytes(8).toString('hex');
  
  return `shuttle-cli-${randomPart}_${datePart}`;
}

/**
 * 执行單次查詢 - 直接调用 API
 */
async function runQuery(query, options) {
  const startTime = Date.now();
  
  try {
    // 構建 session_id（使用日期格式）
    const sessionId = generateSessionId();
    
    // 構建 curl 命令
    const curlCmd = `curl -s -X POST ${options.url}/chat_direct \\\n` +
                   `  -H "Content-Type: application/json" \\\n` +
                   `  -d '{"question":${JSON.stringify(query)},"session_id":"${sessionId}","lang":"${options.lang || 'zh'}"}'`;
    
    console.log(`📡 發送查詢到 ${options.url}/chat_direct`);
    console.log(`🆔 Session ID: ${sessionId}`);
    
    // 執行 curl
    const { stdout } = await execPromise(curlCmd);
    
    // 解析回應
    let result;
    try {
      result = JSON.parse(stdout);
    } catch (e) {
      throw new Error(`API 返回無效 JSON: ${stdout.substring(0, 200)}...`);
    }
    
    // 檢查是否有錯誤
    if (result.error || result.message === '抱歉，產品規格查詢時發生錯誤，請稍後再試。') {
      throw new Error(result.error || result.message || 'API 返回錯誤');
    }
    
    // 提取回應內容
    const response = result.result || result.response || result.data || '無回應內容';
    
    const elapsed = ((Date.now() - startTime) / 1000).toFixed(2);
    
    return {
      query,
      response,
      url: options.url,
      elapsed: `${elapsed}s`,
      timestamp: new Date().toISOString(),
      sessionId
    };
  } catch (error) {
    console.error('❌ API 調用失敗:', error.message);
    throw error;
  }
}

/**
 * 讀取批次查詢檔案
 */
function readQueries(filePath) {
  const fullPath = path.resolve(filePath);
  const content = fs.readFileSync(fullPath, 'utf-8');
  return content
    .split('\n')
    .map(line => line.trim())
    .filter(line => line && !line.startsWith('#'));
}

/**
 * 輸出結果
 */
function outputResult(result, format) {
  if (format === 'json') {
    console.log(JSON.stringify(result, null, 2));
  } else {
    console.log(`🔍 查詢：${result.query}`);
    console.log(`🆔 Session：${result.sessionId}`);
    console.log(`⏱️  耗時：${result.elapsed}`);
    console.log(`📅 時間：${result.timestamp}`);
    console.log('\n📋 回應內容：');
    console.log(result.response);
  }
}

// CLI 定義
program
  .name('shuttle-ai-chatbot')
  .description('Shuttle AI Chatbot 自動化查詢工具 (Optimized v2.0.1)')
  .version('2.0.1');

// 單次查詢
program
  .command('query')
  .description('執行單次查詢')
  .argument('<text>', '查詢文字')
  .option('--url <url>', '目標網頁 URL', 'http://192.168.100.98:8888')
  .option('--timeout <seconds>', '等待回應超時秒數（保留相容）', '30')
  .option('--output <format>', '輸出格式: json 或 text', 'json')
  .option('--lang <language>', '回覆語言: zh 或 en', 'zh')
  .action(async (text, options) => {
    try {
      const result = await runQuery(text, options);
      outputResult(result, options.output);
    } catch (error) {
      console.error('❌ 執行失敗:', error.message);
      process.exit(1);
    }
  });

// 批次查詢
program
  .command('batch')
  .description('批次執行查詢')
  .argument('<file>', '查詢列表檔案（每行一筆）')
  .option('--url <url>', '目標網頁 URL', 'http://192.168.100.98:8888')
  .option('--timeout <seconds>', '等待回應超時秒數（保留相容）', '30')
  .option('--output <format>', '輸出格式: json 或 text', 'json')
  .option('--lang <language>', '回覆語言: zh 或 en', 'zh')
  .action(async (file, options) => {
    try {
      const queries = readQueries(file);
      const results = [];

      for (const query of queries) {
        console.log(`🔍 執行查詢: ${query}`);
        const result = await runQuery(query, options);
        results.push(result);

        if (options.output === 'text') {
          console.log('\n' + '='.repeat(50) + '\n');
        }
      }

      if (options.output === 'json') {
        console.log(JSON.stringify(results, null, 2));
      }
    } catch (error) {
      console.error('❌ 批次執行失敗:', error.message);
      process.exit(1);
    }
  });

// 執行 CLI
program.parse();