#!/usr/bin/env node
/**
 * 自动化取证 - 设备管理
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
      } else {
        params[key] = true;
      }
    }
  }
  
  return params;
}

async function main() {
  const params = parseArgs();
  
  if (params.check) {
    // 检查设备
    try {
      const result = await evidence.checkDevice();
      console.log(JSON.stringify({ 
        success: true, 
        data: { hasDevice: result.has_device }
      }, null, 2));
    } catch (error) {
      console.error(JSON.stringify({ success: false, error: error.message }, null, 2));
      process.exit(1);
    }
  } else if (params.assign) {
    // 分配设备
    const batchId = params['batch-id'] || params.batchId;
    const callbackUrl = params['callback-url'];
    
    if (!batchId) {
      console.error('用法: node device.js --assign --batch-id "批次ID" [--callback-url "回调地址"]');
      process.exit(1);
    }
    
    try {
      const result = await evidence.assignDevice(batchId, callbackUrl);
      console.log(JSON.stringify({ 
        success: true, 
        data: {
          wsUrl: result.ws_url,
          assignedTime: result.assigned_time
        }
      }, null, 2));
    } catch (error) {
      console.error(JSON.stringify({ success: false, error: error.message }, null, 2));
      process.exit(1);
    }
  } else {
    console.error('用法:');
    console.error('  node device.js --check');
    console.error('  node device.js --assign --batch-id "批次ID"');
    process.exit(1);
  }
}

main();