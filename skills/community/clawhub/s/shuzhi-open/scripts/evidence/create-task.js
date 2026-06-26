#!/usr/bin/env node
/**
 * 自动化取证 - 创建取证任务
 * 
 * 用法:
 *   node create-task.js --batch-id "批次ID" --att-id "保全号" --url "https://..." --type 1
 *   node create-task.js --file tasks.json
 */

const path = require('path');
const fs = require('fs');

const libPath = path.resolve(__dirname, '../../lib');
const configPath = path.resolve(__dirname, '../../config.json');

const { init } = require(path.join(libPath, 'client'));
const evidence = require(path.join(libPath, 'modules/evidence'));

const config = require(configPath);
init(config);

function parseArgs() {
  const args = process.argv.slice(2);
  const params = {};
  
  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    if (arg.startsWith('--')) {
      const key = arg.slice(2);
      const value = args[i + 1];
      if (value && !value.startsWith('--')) {
        params[key] = value;
        i++;
      }
    }
  }
  
  return params;
}

async function main() {
  const params = parseArgs();
  
  // 从文件读取任务
  if (params.file) {
    const filePath = path.resolve(params.file);
    const data = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
    
    try {
      const result = await evidence.createTask(data.batchId, data.tasks);
      console.log(JSON.stringify({ success: true, data: result }, null, 2));
    } catch (error) {
      console.error(JSON.stringify({ success: false, error: error.message }, null, 2));
      process.exit(1);
    }
    return;
  }
  
  // 单个任务
  const batchId = params['batch-id'] || params.batchId;
  const attId = params['att-id'] || params.attId;
  const url = params.url;
  const type = parseInt(params.type || '1');
  const evidenceName = params['evidence-name'] || params.name || '取证任务';
  
  if (!batchId || !attId || !url) {
    console.error('用法:');
    console.error('  node create-task.js --batch-id "批次ID" --att-id "保全号" --url "https://..." --type 1');
    console.error('  node create-task.js --file tasks.json');
    console.error('');
    console.error('取证类型:');
    console.error('  1 = 拼多多电商取证');
    console.error('  3 = 淘宝电商取证');
    console.error('  4 = 抖音电商取证');
    process.exit(1);
  }
  
  const tasks = [{
    att_id: attId,
    url,
    evidence_name: evidenceName,
    type
  }];
  
  try {
    const result = await evidence.createTask(batchId, tasks);
    console.log(JSON.stringify({ 
      success: true, 
      data: {
        batchId: result.batch_id,
        wsUrl: result.ws_url,
        pageUrl: result.url,
        bindTime: result.bind_time
      }
    }, null, 2));
  } catch (error) {
    console.error(JSON.stringify({ success: false, error: error.message }, null, 2));
    process.exit(1);
  }
}

main();