const https = require('https');
const http = require('http');
const fs = require('fs');
const path = require('path');

/**
 * 加载配置：优先读取环境变量，其次读取 config.json
 * 环境变量：VALIDATE_BASE_URL / VALIDATE_TOKEN / VALIDATE_APP_ID
 */
function loadConfig() {
  // 方式1：环境变量（推荐用于 CI/自动化）
  if (process.env.VALIDATE_BASE_URL && process.env.VALIDATE_TOKEN) {
    return {
      baseUrl: process.env.VALIDATE_BASE_URL.replace(/\/$/, ''),
      token: process.env.VALIDATE_TOKEN,
      appId: process.env.VALIDATE_APP_ID || ''
    };
  }

  // 方式2：config.json（从脚本目录或 CWD 向上查找）
  const searchDirs = [
    process.cwd(),
    path.join(process.cwd(), '..'),
    path.dirname(process.argv[1]),
    path.join(path.dirname(process.argv[1]), '..'),
    path.join(path.dirname(process.argv[1]), '../..')
  ];

  for (const dir of searchDirs) {
    const configPath = path.join(dir, 'config.json');
    if (fs.existsSync(configPath)) {
      const config = JSON.parse(fs.readFileSync(configPath, 'utf8'));
      const missing = ['baseUrl', 'token'].filter(f => !config[f]);
      if (missing.length > 0) throw new Error(`config.json 缺少字段: ${missing.join(', ')}`);
      config.baseUrl = config.baseUrl.replace(/\/$/, '');
      return config;
    }
  }

  throw new Error(
    '未找到配置。请选择以下任一方式：\n' +
    '  1. 设置环境变量：VALIDATE_BASE_URL=http://... VALIDATE_TOKEN=xxx node scripts/cli.js ...\n' +
    '  2. 在项目根目录创建 config.json：{ "baseUrl": "...", "token": "...", "appId": "..." }'
  );
}

/**
 * 发送 HTTP/HTTPS 请求
 */
function request(url, options = {}) {
  return new Promise((resolve, reject) => {
    const isHttps = url.startsWith('https:');
    const client = isHttps ? https : http;
    const urlObj = new URL(url);

    const reqOptions = {
      hostname: urlObj.hostname,
      port: urlObj.port || (isHttps ? 443 : 80),
      path: urlObj.pathname + urlObj.search,
      method: options.method || 'GET',
      headers: options.headers || {},
      timeout: 30000
    };

    const req = client.request(reqOptions, (res) => {
      let raw = '';
      res.on('data', chunk => raw += chunk);
      res.on('end', () => {
        try {
          resolve({ statusCode: res.statusCode, data: JSON.parse(raw) });
        } catch {
          resolve({ statusCode: res.statusCode, data: raw });
        }
      });
    });

    req.on('timeout', () => {
      req.destroy();
      reject(new Error(`请求超时（30s）：${url}`));
    });

    req.on('error', err => reject(new Error(`网络错误：${err.message}`)));

    if (options.body) req.write(options.body);
    req.end();
  });
}

/**
 * 调用 API
 */
async function apiRequest(endpoint, method = 'POST', body = null) {
  const config = loadConfig();
  const url = `${config.baseUrl}${endpoint}`;

  const options = {
    method,
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'X-Access-Token': config.token
    }
  };

  if (body) {
    const bodyStr = JSON.stringify(body);
    options.body = bodyStr;
    options.headers['Content-Length'] = Buffer.byteLength(bodyStr);
  }

  const response = await request(url, options);

  if (response.statusCode >= 400) {
    const msg = response.data?.message || response.data?.errorMsg || `HTTP ${response.statusCode}`;
    throw new Error(`API 错误 [${response.statusCode}]: ${msg}`);
  }

  // 业务层错误检查（success: false）
  if (response.data && response.data.success === false) {
    const msg = response.data.errorMsg || response.data.message || '业务处理失败';
    throw new Error(`业务错误: ${msg}`);
  }

  return response.data;
}

module.exports = { loadConfig, apiRequest };
