#!/usr/bin/env node
/**
 * 保管单组件 - 下载保管单
 */

const path = require('path');

const libPath = path.resolve(__dirname, '../../lib');
const configPath = path.resolve(__dirname, '../../config.json');

const { init } = require(path.join(libPath, 'client'));
const certificate = require(path.join(libPath, 'modules/certificate'));

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
  const certNo = params['cert-no'] || params.certNo;
  
  if (!certNo) {
    console.error('用法: node download.js --cert-no "存证编号"');
    process.exit(1);
  }
  
  try {
    const result = await certificate.download(certNo);
    console.log(JSON.stringify({ 
      success: true, 
      data: { url: result.url }
    }, null, 2));
  } catch (error) {
    console.error(JSON.stringify({ success: false, error: error.message }, null, 2));
    process.exit(1);
  }
}

main();