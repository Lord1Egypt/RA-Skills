#!/usr/bin/env node
const fs = require('fs');
const path = require('path');

const DEFAULT_FILE = path.resolve(process.cwd(), 'stocks-data', 'stocklist.txt');

function parseArgs(argv) {
  const args = [...argv];
  let file = DEFAULT_FILE;
  for (let i = 0; i < args.length; i++) {
    if (args[i] === '--file') {
      if (!args[i + 1]) throw new Error('--file 缺少路径');
      file = path.resolve(args[i + 1]);
      args.splice(i, 2);
      i -= 1;
    }
  }
  return { args, file };
}

function ensureDirForFile(file) {
  fs.mkdirSync(path.dirname(file), { recursive: true });
}

function validateCode(code) {
  if (!/^\d{6}$/.test(code)) {
    throw new Error(`无效股票代码: ${code}，必须是6位数字`);
  }
}

function normalizeName(name) {
  return String(name || '').trim();
}

function readStockList(file) {
  if (!fs.existsSync(file)) return [];
  const text = fs.readFileSync(file, 'utf8');
  return text
    .split(/\r?\n/)
    .map((line) => line.trim())
    .filter(Boolean)
    .map((line) => {
      const [code, ...rest] = line.split('|');
      const name = rest.join('|').trim();
      if (!/^\d{6}$/.test((code || '').trim())) return null;
      return { code: code.trim(), name };
    })
    .filter(Boolean);
}

function writeStockList(file, list) {
  ensureDirForFile(file);
  const content = list.map((item) => `${item.code}|${item.name}`).join('\n');
  fs.writeFileSync(file, content ? `${content}\n` : '', 'utf8');
}

function addStock(file, code, name) {
  validateCode(code);
  const stockName = normalizeName(name);
  if (!stockName) throw new Error('股票名称不能为空');
  const list = readStockList(file);
  const idx = list.findIndex((x) => x.code === code);
  if (idx >= 0) {
    list[idx].name = stockName;
    writeStockList(file, list);
    return { action: 'updated', item: list[idx] };
  }
  const item = { code, name: stockName };
  list.push(item);
  writeStockList(file, list);
  return { action: 'added', item };
}

function removeStock(file, code) {
  validateCode(code);
  const list = readStockList(file);
  const next = list.filter((x) => x.code !== code);
  const removed = list.find((x) => x.code === code) || null;
  writeStockList(file, next);
  return { removed };
}

function clearStocks(file) {
  writeStockList(file, []);
}

function formatList(list) {
  if (!list.length) return '自选股列表为空';
  return list.map((x) => `${x.code} ${x.name}`).join('\n');
}

async function main() {
  const { args, file } = parseArgs(process.argv.slice(2));
  const [command, ...rest] = args;
  if (!command || ['help', '--help', '-h'].includes(command)) {
    console.log([
      '用法:',
      '  node stock_tools.js list [--file path]',
      '  node stock_tools.js add <code> <name> [--file path]',
      '  node stock_tools.js remove <code> [--file path]',
      '  node stock_tools.js clear [--file path]',
      '',
      '说明: 此脚本仅用于本地自选股持久化管理，不负责联网获取行情。'
    ].join('\n'));
    return;
  }

  if (command === 'list') {
    console.log(formatList(readStockList(file)));
    return;
  }
  if (command === 'add') {
    const [code, ...nameParts] = rest;
    const result = addStock(file, code, nameParts.join(' '));
    console.log(`${result.action === 'added' ? '已添加' : '已更新'}：${result.item.code} ${result.item.name}`);
    return;
  }
  if (command === 'remove') {
    const [code] = rest;
    const result = removeStock(file, code);
    console.log(result.removed ? `已删除：${result.removed.code} ${result.removed.name}` : `未找到：${code}`);
    return;
  }
  if (command === 'clear') {
    clearStocks(file);
    console.log('已清空自选股列表');
    return;
  }

  throw new Error(`未知命令: ${command}`);
}

main().catch((error) => {
  console.error(`错误：${error.message}`);
  process.exit(1);
});
