#!/usr/bin/env node

/**
 * 执行后钩子
 */

async function postExecution(result, context) {
  const duration = context.endTime - context.startTime;
  const durationSec = Math.round(duration / 1000);
  
  if (result.status === 'success') {
    console.log(`✅ Tech Radar Daily 执行成功！用时 ${durationSec} 秒`);
    
    // 记录成功日志
    logExecution({
      status: 'success',
      duration: durationSec,
      timestamp: new Date().toISOString(),
      itemCount: result.itemCount || 0
    });
  } else {
    console.error(`❌ Tech Radar Daily 执行失败:`, result.error);
    
    // 记录失败日志
    logExecution({
      status: 'failed',
      duration: durationSec,
      timestamp: new Date().toISOString(),
      error: result.error?.message || 'Unknown error'
    });
  }
}

function logExecution(data) {
  const fs = require('fs');
  const path = require('path');
  
  const logFile = path.join(__dirname, '../logs/execution.log');
  const logLine = JSON.stringify(data) + '\n';
  
  try {
    fs.appendFileSync(logFile, logLine);
  } catch (e) {
    console.error('写入日志失败:', e.message);
  }
}

module.exports = { postExecution };
