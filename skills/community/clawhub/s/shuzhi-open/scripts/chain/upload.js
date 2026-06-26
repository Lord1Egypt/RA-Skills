#!/usr/bin/env node
/**
 * 区块链API服务 - 数据上链
 * 
 * 用法:
 *   node upload.js --data "业务数据"
 *   node upload.js --data '{"ano":"BQ123","sha256":"xxx"}' --business EVIDENCE_PRESERVATION --source BQ_INTERNATIONAL
 */

const path = require('path');

// 加载模块
const libPath = path.resolve(__dirname, '../../lib');
const configPath = path.resolve(__dirname, '../../config.json');

const { init } = require(path.join(libPath, 'client'));
const chain = require(path.join(libPath, 'modules/chain'));

// 初始化
const config = require(configPath);
init(config);

// 解析参数
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
      } else {
        params[key] = true;
      }
    }
  }
  
  return params;
}

async function main() {
  const params = parseArgs();
  
  const data = params.data || params.d;
  
  if (!data) {
    console.error('用法: node upload.js --data "业务数据"');
    console.error('      node upload.js --data \'{"ano":"BQ123"}\' --business EVIDENCE_PRESERVATION --source BQ_INTERNATIONAL');
    console.error('');
    console.error('可选参数:');
    console.error('  --business   业务名（多个用逗号分隔）');
    console.error('  --source     来源（多个用逗号分隔）');
    console.error('  --requestId  请求ID（不传则自动生成）');
    process.exit(1);
  }
  
  // 构建选项
  const options = {};
  
  if (params.business) {
    options.business = params.business.split(',').map(s => s.trim());
  }
  if (params.source) {
    options.source = params.source.split(',').map(s => s.trim());
  }
  if (params.requestId) {
    options.requestId = params.requestId;
  }
  
  try {
    const result = await chain.upload(data, options);
    console.log(JSON.stringify({ 
      success: true, 
      data: {
        index: result.index,
        requestId: result.requestId
      }
    }, null, 2));
  } catch (error) {
    console.error(JSON.stringify({ success: false, error: error.message }, null, 2));
    process.exit(1);
  }
}

main();