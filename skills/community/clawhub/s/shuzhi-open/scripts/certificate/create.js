#!/usr/bin/env node
/**
 * 保管单组件 - 生成保管单
 */

const path = require('path');
const fs = require('fs');

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
  
  if (params.file) {
    const filePath = path.resolve(params.file);
    const data = JSON.parse(fs.readFileSync(filePath, 'utf-8'));
    
    try {
      const result = await certificate.create(data);
      console.log(JSON.stringify({ success: true, data: result }, null, 2));
    } catch (error) {
      console.error(JSON.stringify({ success: false, error: error.message }, null, 2));
      process.exit(1);
    }
    return;
  }
  
  console.error('用法: node create.js --file params.json');
  console.error('');
  console.error('params.json 格式:');
  console.error(JSON.stringify({
    templateId: "模板ID",
    certNo: "证书编号（可选）",
    defaultFields: {
      applicantName: "申请人名称",
      applicantIdCard: "身份证号"
    },
    customFields: []
  }, null, 2));
  process.exit(1);
}

main();