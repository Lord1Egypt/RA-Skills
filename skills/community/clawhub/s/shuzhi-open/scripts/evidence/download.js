#!/usr/bin/env node
/**
 * 自动化取证 - 下载证据包
 */

const path = require('path');

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
  const attId = params['att-id'] || params.attId;
  
  if (!attId) {
    console.error('用法: node download.js --att-id "任务ID"');
    process.exit(1);
  }
  
  try {
    const result = await evidence.downloadZip(attId);
    console.log(JSON.stringify({ 
      success: true, 
      data: {
        url: result.url,
        expireTime: result.expire_time
      }
    }, null, 2));
  } catch (error) {
    console.error(JSON.stringify({ success: false, error: error.message }, null, 2));
    process.exit(1);
  }
}

main();