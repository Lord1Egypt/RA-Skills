/**
 * 职得Offer MCP 公共模块
 * 从 scripts/config.json 或环境变量 ZHIDE_OFFER_KEY 读取 API Key
 */
const https = require('https');
const path = require('path');
const fs = require('fs');

function getKey() {
  if (process.env.ZHIDE_OFFER_KEY) return process.env.ZHIDE_OFFER_KEY;
  const cfgPath = path.join(__dirname, 'config.json');
  if (fs.existsSync(cfgPath)) {
    const cfg = JSON.parse(fs.readFileSync(cfgPath, 'utf8'));
    if (cfg.zhideOfferKey) return cfg.zhideOfferKey;
  }
  throw new Error('未找到 API Key。请在 scripts/config.json 中设置 zhideOfferKey，或设置环境变量 ZHIDE_OFFER_KEY');
}

function post(key, body) {
  return new Promise((resolve, reject) => {
    const data = JSON.stringify(body);
    const r = https.request({
      hostname: 'offer.yxzrkj.cn',
      port: 443,
      path: '/mcp',
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json, text/event-stream',
        'Authorization': 'Bearer ' + key,
        'Content-Length': Buffer.byteLength(data)
      },
      timeout: 30000
    }, res => {
      let b = '';
      res.on('data', d => b += d);
      res.on('end', () => resolve({ status: res.statusCode, body: b }));
    });
    r.on('error', reject);
    r.on('timeout', () => { r.destroy(); reject(new Error('请求超时（30s）')); });
    r.write(data);
    r.end();
  });
}

async function mcpCall(toolName, args) {
  const key = getKey();
  // Step 1: initialize
  await post(key, {
    jsonrpc: '2.0', id: 0, method: 'initialize',
    params: { protocolVersion: '2024-11-05', capabilities: {}, clientInfo: { name: 'zhide-offer-skill', version: '1.0' } }
  });
  // Step 2: tools/call
  const r = await post(key, {
    jsonrpc: '2.0', id: 1, method: 'tools/call',
    params: { name: toolName, arguments: args }
  });
  const d = JSON.parse(r.body);
  if (d?.result?.isError) throw new Error('接口返回错误: ' + JSON.stringify(d.result));
  return d?.result?.structuredContent || d?.result;
}

module.exports = { mcpCall };
