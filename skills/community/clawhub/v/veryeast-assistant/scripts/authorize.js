#!/usr/bin/env node
/* Store/clear veryeast api_key in skill config.json（client 从 config.json 的 api_key 读取）。
   用法：
     node scripts/authorize.js '<api_key>'     # 写入 config.json（权限 600）
     node scripts/authorize.js --show          # 查看（打码）
     node scripts/authorize.js --clear         # 清除 */
const fs = require('fs');
const path = require('path');

const API_KEY_ENV_VAR = 'VEAST_API_KEY';

function findSkillDir() {
  if (process.env.VEAST_SKILL_DIR) return process.env.VEAST_SKILL_DIR;
  return path.dirname(path.dirname(__filename));
}

const configPath = path.join(findSkillDir(), 'config.json');

function mask(k) { return k.length <= 8 ? '****' : k.slice(0, 4) + '****' + k.slice(-4); }

function show() {
  if (process.env[API_KEY_ENV_VAR]) {
    console.log('api_key:', mask(process.env[API_KEY_ENV_VAR]), '(from env VEAST_API_KEY)');
    return;
  }
  if (!fs.existsSync(configPath)) { console.log('api_key: 未设置 (env VEAST_API_KEY 也未设置)'); return; }
  let k = '';
  try { k = JSON.parse(fs.readFileSync(configPath, 'utf8')).api_key || ''; }
  catch (e) { console.log('api_key: config.json 已损坏，可 --clear 后重新写入'); return; }
  console.log(k ? 'api_key: ' + mask(k) + ' (from config.json)' : 'api_key: 未设置 (config.json 无 api_key)');
}

const args = process.argv.slice(2);
if (args.length === 0 || args[0] === '--show') {
  show();
} else if (args[0] === '--clear') {
  if (fs.existsSync(configPath)) { fs.unlinkSync(configPath); console.log('已清除 config.json'); }
  else console.log('没有 config.json 可清除');
} else {
  fs.writeFileSync(configPath, JSON.stringify({ api_key: args[0] }, null, 2), { mode: 0o600 });
  console.log('已保存到 config.json（权限 600，仅当前用户可读）');
  console.log('Tip: 也可以设置环境变量 VEAST_API_KEY 更安全');
}
