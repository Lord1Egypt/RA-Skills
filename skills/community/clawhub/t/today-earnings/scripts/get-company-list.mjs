#!/usr/bin/env node
// scripts/get-company-list.mjs
// Node CLI 入口 - 通过 Unix socket 向 Native Host 发送财报抓取请求
//
// 用法:
//   node get-company-list.mjs <YYYY-MM-DD>
//
// 示例:
//   node get-company-list.mjs 2026-03-14
//
// 成功: stdout 输出 JSON 数组，exit 0
// 失败: stderr 输出错误信息，exit 1
//
// 前置条件:
//   1. Chrome 已启动
//   2. Today Earnings 扩展已加载
//   3. Native Host 已安装（native-host/install.sh）

import net from 'net';

const SOCKET_PATH = '/tmp/today-earnings.sock';
const TIMEOUT_MS = 60000;

// ─── 市值解析 ─────────────────────────────────────────────────────────────────

/**
 * 解析市值字符串为纯数字（单位：美元）
 * 支持后缀：K（千）、M（百万）、B（十亿）、T（万亿）
 * 无效/缺失值返回 null
 *
 * @param {string} str - 如 "28.37B"、"500M"、"1.5T"、"--"
 * @returns {number|null}
 */
function parseMarketCap(str) {
  if (!str || str === '--') return null;
  const m = str.trim().toUpperCase().match(/^(\d+(?:\.\d+)?)\s*([KMBT])$/);
  if (!m) return null;
  const num = parseFloat(m[1]);
  const unit = m[2];
  if (unit === 'T') return num * 1e12;
  if (unit === 'B') return num * 1e9;
  if (unit === 'M') return num * 1e6;
  if (unit === 'K') return num * 1e3;
  return null;
}

/**
 * 将原始财报数组转换为固定输出格式
 * - 只保留 code、earningType、marketCap 三个字段
 * - marketCap 转为纯数字，无法解析的条目排除
 * - earningType 保留 AMC、BMO、TNS
 *
 * @param {Array} data - 原始财报数组
 * @returns {Array}
 */
function transformData(data) {
  const result = [];
  for (const item of data) {
    const cap = parseMarketCap(item.marketCap);
    if (cap === null) continue; // 无有效市值数据，排除
    result.push({
      code: item.code,
      earningType: item.earningType,
      marketCap: cap,
    });
  }
  return result;
}

// ─── 参数校验 ────────────────────────────────────────────────────────────────

const args = process.argv.slice(2);
const date = args.find(a => /^\d{4}-\d{2}-\d{2}$/.test(a));

if (!date) {
  process.stderr.write('用法: node get-company-list.mjs <YYYY-MM-DD>\n');
  process.stderr.write('示例: node get-company-list.mjs 2026-03-14\n');
  process.exit(1);
}

// ─── Socket 通信 ─────────────────────────────────────────────────────────────

const requestLine = JSON.stringify({ type: 'fetchEarnings', date }) + '\n';

const client = net.createConnection(SOCKET_PATH);

let buf = '';
let timer;

client.on('connect', () => {
  client.write(requestLine);
});

client.on('data', (chunk) => {
  buf += chunk.toString('utf8');
});

client.on('end', () => {
  clearTimeout(timer);
  const line = buf.trim();
  if (!line) {
    process.stderr.write('错误: 未收到响应\n');
    process.exit(1);
  }

  let response;
  try {
    response = JSON.parse(line);
  } catch (_) {
    process.stderr.write(`错误: 响应格式无效 - ${line}\n`);
    process.exit(1);
  }

  if (!response.ok) {
    const msg = response.error?.message ?? JSON.stringify(response.error);
    process.stderr.write(`错误: ${msg}\n`);
    process.exit(1);
  }

  const output = transformData(response.data);
  process.stdout.write(JSON.stringify(output) + '\n');
  process.exit(0);
});

client.on('error', (err) => {
  clearTimeout(timer);
  if (err.code === 'ENOENT' || err.code === 'ECONNREFUSED') {
    process.stderr.write(
      '错误: 无法连接 Native Host（' + SOCKET_PATH + '）\n' +
      '请确认以下条件已满足:\n' +
      '  1. Chrome 已启动\n' +
      '  2. Today Earnings 扩展已加载并激活\n' +
      '  3. Native Host 已安装: ./native-host/install.sh <扩展ID>\n'
    );
  } else {
    process.stderr.write(`错误: ${err.message}\n`);
  }
  process.exit(1);
});

timer = setTimeout(() => {
  client.destroy();
  process.stderr.write(`错误: 请求超时（${TIMEOUT_MS / 1000}s）\n`);
  process.exit(1);
}, TIMEOUT_MS);
