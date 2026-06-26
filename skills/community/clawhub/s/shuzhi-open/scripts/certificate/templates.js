#!/usr/bin/env node
/**
 * CAP-保管单组件 - 获取模板列表
 */

const path = require('path');

const libPath = path.resolve(__dirname, '../../lib');
const configPath = path.resolve(__dirname, '../../config.json');

const { init } = require(path.join(libPath, 'client'));
const certificate = require(path.join(libPath, 'modules/certificate'));

const config = require(configPath);
init(config);

async function main() {
  try {
    const result = await certificate.listTemplates();
    console.log(JSON.stringify({ success: true, data: result }, null, 2));
  } catch (error) {
    console.error(JSON.stringify({ success: false, error: error.message }, null, 2));
    process.exit(1);
  }
}

main();