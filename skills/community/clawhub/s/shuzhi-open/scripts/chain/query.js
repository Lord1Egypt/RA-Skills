#!/usr/bin/env node
/**
 * 区块链API服务 - 批量查询上链结果
 * 
 * 用法:
 *   node query.js --index "交易索引"
 *   node query.js --index "索引1,索引2,索引3"
 */

const path = require('path');

const libPath = path.resolve(__dirname, '../../lib');
const configPath = path.resolve(__dirname, '../../config.json');

const { init } = require(path.join(libPath, 'client'));
const chain = require(path.join(libPath, 'modules/chain'));

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
  
  const index = params.index || params.i;
  
  if (!index) {
    console.error('用法: node query.js --index "交易索引"');
    console.error('      node query.js --index "索引1,索引2,索引3"');
    process.exit(1);
  }
  
  // 支持逗号分隔的多个索引
  const indexList = index.split(',').map(s => s.trim());
  
  try {
    const result = await chain.queryResult(indexList);
    
    // 添加状态说明
    if (result && result.length > 0) {
      result.forEach(item => {
        if (item.chain_results) {
          item.chain_results.forEach(r => {
            r.statusText = chain.getStatusText(r.status);
          });
        }
      });
    }
    
    console.log(JSON.stringify({ success: true, data: result }, null, 2));
  } catch (error) {
    console.error(JSON.stringify({ success: false, error: error.message }, null, 2));
    process.exit(1);
  }
}

main();