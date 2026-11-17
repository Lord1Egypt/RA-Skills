/**
 * HTTP API 测试模板（通用版）
 * 
 * 使用方式：
 *   node scripts/http-test-template.cjs POST /your-endpoint '{"key":"value"}'
 *   node scripts/http-test-template.cjs GET /your-endpoint
 * 
 * 环境变量：
 *   TEST_HOST - 默认 localhost
 *   TEST_PORT - 默认读取 pipeline.json project.port
 *   TEST_TIMEOUT - 默认 10000 (ms)
 */

const http = require('http');

// 尝试从 pipeline.json 读取，fallback 到环境变量
let pipeline = {};
try {
  pipeline = require('../../../pipeline.json');
} catch (e) {
  // pipeline.json 不存在时使用环境变量
}

const HOST = process.env.TEST_HOST || (pipeline.project && pipeline.project.host) || 'localhost';
const PORT = parseInt(process.env.TEST_PORT || (pipeline.project && pipeline.project.port) || '3000', 10);
const TIMEOUT_MS = parseInt(process.env.TEST_TIMEOUT || '10000', 10);

const method = (process.argv[2] || 'GET').toUpperCase();
const path = process.argv[3] || '/';
const rawBody = process.argv[4] || null;

// --- Timeout guard ---
const TIMEOUT = setTimeout(() => {
  console.error(`FAIL: 请求超时（>${TIMEOUT_MS / 1000}秒未响应）`);
  process.exit(1);
}, TIMEOUT_MS);

// --- Validate JSON body ---
let body = null;
if (rawBody) {
  try {
    body = JSON.stringify(JSON.parse(rawBody));
  } catch (e) {
    console.error(`FAIL: JSON 格式错误: ${e.message}`);
    process.exit(1);
  }
}

// --- Build options ---
const options = {
  hostname: HOST,
  port: PORT,
  path: path,
  method: method,
  headers: { 'Content-Type': 'application/json' }
};

if (body) {
  options.headers['Content-Length'] = Buffer.byteLength(body);
}

// --- Execute ---
console.log(`[1/${body ? 3 : 2}] ${method} ${HOST}:${PORT}${path}`);
if (body) {
  console.log(`[2/3] Body: ${body}`);
}

const req = http.request(options, res => {
  clearTimeout(TIMEOUT);
  let data = '';
  res.on('data', c => data += c);
  res.on('end', () => {
    const step = body ? 3 : 2;
    const icon = res.statusCode >= 400 ? 'WARN' : 'OK';
    console.log(`[${step}/${step}] ${icon} HTTP ${res.statusCode}: ${data.substring(0, 500)}`);
    process.exit(res.statusCode >= 400 ? 1 : 0);
  });
});

req.on('error', e => {
  clearTimeout(TIMEOUT);
  console.error(`FAIL: ${e.message}`);
  process.exit(1);
});

if (body) req.write(body);
req.end();
