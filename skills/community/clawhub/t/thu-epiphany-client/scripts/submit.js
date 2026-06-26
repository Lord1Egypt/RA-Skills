#!/usr/bin/env node
/**
 * thu-epiphany 客户端 — 提交灵感
 *
 * 从同目录下的 config.js 读取令牌和服务端地址。
 *
 * 🔒 安全说明：本脚本仅向用户明确配置的 api_base 地址发送网络请求。
 *    所有发送的数据为用户主动提供的灵感内容。不收集任何个人信息。
 *    令牌仅用于 API 认证，不会发送到非用户配置的第三方地址。
 *
 * 用法:
 *   node scripts/submit.js --title "xxx" --thoughts "xxx" [--url "x"] [--from "@name"]
 *   node scripts/submit.js --status         检查服务器状态
 *   node scripts/submit.js --help
 */

const path = require('path');
const https = require('https');
const http = require('http');

// ---------------------------------------------------------------------------
// 从 config.js 加载配置（令牌已内嵌）
// ---------------------------------------------------------------------------
let config;
try {
  config = require(path.join(__dirname, 'config.js'));
} catch (e) {
  console.error('❌ 无法加载 config.js');
  console.error('   请确保 scripts/config.js 存在且包含有效的令牌配置');
  process.exit(1);
}

const API_BASE = config.api_base || 'http://localhost:18999';
const TOKEN = config.token && config.token.trim() !== '' ? config.token : 'sk_fox_YOUR_TOKEN_HERE';
const DEFAULT_FROM = config.default_from || '';

// ---------------------------------------------------------------------------
// 帮助
// ---------------------------------------------------------------------------
function getHelp() {
  return `
🦊 thu-epiphany 客户端 — 向亢慕义斋提交灵感
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  提交灵感:
    submit.js --title "xxx" --thoughts "xxx" [--url "x"] [--from "@name"]

  检查状态:
    submit.js --status

  配置文件: scripts/config.js（含令牌）
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
`;
}

// ---------------------------------------------------------------------------
// HTTP 请求
// ---------------------------------------------------------------------------
function apiRequest(method, pathname, body) {
  return new Promise((resolve, reject) => {
    const url = new URL(pathname, API_BASE);
    const isHttps = url.protocol === 'https:';
    const transport = isHttps ? https : http;

    const options = {
      hostname: url.hostname,
      port: url.port || (isHttps ? 443 : 80),
      path: url.pathname,
      method,
      headers: {
        'Content-Type': 'application/json',
        ...(TOKEN ? { 'Authorization': `Bearer ${TOKEN}` } : {}),
      },
    };

    const req = transport.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve({ status: res.statusCode, data: JSON.parse(data) });
        } catch {
          resolve({ status: res.statusCode, data: { raw: data } });
        }
      });
    });

    req.on('error', (err) => {
      if (err.code === 'ECONNREFUSED') {
        reject(new Error(`无法连接到服务端 ${API_BASE}，服务可能未启动`));
      } else {
        reject(err);
      }
    });

    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

// ---------------------------------------------------------------------------
// 主逻辑
// ---------------------------------------------------------------------------
async function main() {
  const args = process.argv.slice(2);

  if (args.includes('--help') || args.includes('-h')) {
    console.log(getHelp());
    return;
  }

  // 检查令牌是否已配置
  if (!TOKEN || TOKEN === 'sk_fox_YOUR_TOKEN_HERE') {
    console.error('❌ 令牌未配置');
    console.error('   请编辑 scripts/config.js，将 token 替换为你的真实令牌');
    process.exit(1);
  }

  if (args.includes('--status')) {
    console.log('📡 正在连接服务端...');
    try {
      const res = await apiRequest('GET', '/api/health');
      if (res.status === 200) {
        console.log(`✅ 服务端在线`);
        console.log(`   地址: ${API_BASE}`);
        console.log(`   缓冲: ${res.data.buffered} 条`);
        console.log(`   令牌: ${res.data.tokens} 个`);
      } else {
        console.log(`❌ 服务端错误: ${res.status}`);
      }
    } catch (err) {
      console.error(`❌ 连接失败: ${err.message}`);
    }
    return;
  }

  // 解析参数
  const getArg = (flag) => {
    const idx = args.indexOf(flag);
    return idx >= 0 ? args[idx + 1] : undefined;
  };

  const title = getArg('--title');
  const thoughts = getArg('--thoughts');
  const url = getArg('--url');
  const from = getArg('--from') || DEFAULT_FROM;

  if (!thoughts) {
    console.error('❌ 必须提供 --thoughts');
    console.log(getHelp());
    process.exit(1);
  }

  console.log(`📤 正在提交灵感: ${title || '未命名'}...`);

  try {
    const res = await apiRequest('POST', '/api/inspiration', {
      title: title || '未命名灵感',
      thoughts,
      url: url || '',
      from: from || undefined,
    });

    if (res.status === 200 && res.data.success) {
      console.log(`✅ 灵感已写入亢慕义斋灵感池!`);
      console.log(`   标题: ${res.data.entry?.title || title}`);
      console.log(`   区块: ${res.data.blocks} 个`);
    } else if (res.status === 401) {
      console.error(`❌ 令牌无效或已吊销，请联系圈管理员`);
    } else {
      console.error(`❌ 提交失败 (${res.status}):`, JSON.stringify(res.data));
    }
  } catch (err) {
    console.error(`❌ 请求失败: ${err.message}`);
    console.error(`   请稍后重试，或将内容暂存到本地文件`);
    process.exit(1);
  }
}

main();
