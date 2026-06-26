#!/usr/bin/env node
/**
 * 电子签章 - 企业主体管理
 */

const path = require('path');

const libPath = path.resolve(__dirname, '../../lib');
const configPath = path.resolve(__dirname, '../../config.json');

const { init } = require(path.join(libPath, 'client'));
const sign = require(path.join(libPath, 'modules/sign'));

const config = require(configPath);
init(config);

function parseArgs() {
  const args = process.argv.slice(2);
  const params = { action: args[0] };
  
  for (let i = 1; i < args.length; i++) {
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
  const action = params.action;
  
  try {
    switch (action) {
      case 'create':
        if (!params.name || !params['credit-code']) {
          console.error('用法: node enterprise.js create --name "公司名称" --credit-code "统一社会信用代码"');
          process.exit(1);
        }
        const createResult = await sign.enterprise.create(params.name, params['credit-code']);
        console.log(JSON.stringify({ success: true, data: createResult }, null, 2));
        break;
        
      case 'list':
        const listResult = await sign.enterprise.list(params.name, params['credit-code']);
        console.log(JSON.stringify({ success: true, data: listResult }, null, 2));
        break;
        
      case 'detail':
        if (!params['user-id']) {
          console.error('用法: node enterprise.js detail --user-id "用户ID"');
          process.exit(1);
        }
        const detailResult = await sign.enterprise.detail(params['user-id']);
        console.log(JSON.stringify({ success: true, data: detailResult }, null, 2));
        break;
        
      case 'delete':
        if (!params['user-id']) {
          console.error('用法: node enterprise.js delete --user-id "用户ID"');
          process.exit(1);
        }
        const deleteResult = await sign.enterprise.delete(params['user-id']);
        console.log(JSON.stringify({ success: true, data: deleteResult }, null, 2));
        break;
        
      default:
        console.error('用法:');
        console.error('  node enterprise.js create --name "公司名称" --credit-code "统一社会信用代码"');
        console.error('  node enterprise.js list [--name "公司名称"] [--credit-code "信用代码"]');
        console.error('  node enterprise.js detail --user-id "用户ID"');
        console.error('  node enterprise.js delete --user-id "用户ID"');
        process.exit(1);
    }
  } catch (error) {
    console.error(JSON.stringify({ success: false, error: error.message }, null, 2));
    process.exit(1);
  }
}

main();