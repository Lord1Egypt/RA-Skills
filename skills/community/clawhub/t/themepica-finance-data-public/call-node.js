/**
 * 语势科技金融数据公开API 调用脚本
 * 
 * 仅包含公开版API（APPCODE认证），不含私有API
 */

const https = require('https');
const fs = require('fs');
const path = require('path');

// 读取配置（优先环境变量，其次配置文件）
const CONFIG_PATH = path.join(__dirname, 'mcp_config.json');
let config = {};
try {
  config = JSON.parse(fs.readFileSync(CONFIG_PATH, 'utf8'));
} catch (e) {
  // 配置文件不存在时忽略
}

const APPCODE = process.env.THEMEPICA_APPCODE || config.appcode || '';

// 服务地址
const BASE_URL = 'https://data.api.themepica.com';

// API端点映射（仅公开API）
const API_ENDPOINTS = {
  // 主题
  'themes': { path: '/themes', method: 'GET' },
  'theme_indices': { path: '/theme/indices', method: 'GET' },
  'theme_etfs': { path: '/theme/etfs', method: 'GET' },
  'theme_diagnose': { path: '/theme/diagnose', method: 'GET' },
  'theme_subs_diagnose': { path: '/theme/subs/diagnose', method: 'GET' },
  'theme_narratives': { path: '/theme/narratives', method: 'GET' },
  'theme_contents': { path: '/theme/contents', method: 'GET' },
  
  // 榜单
  'board_hotspots': { path: '/board/hotspots', method: 'GET' },
  'board_hotspots_detail': { path: '/board/hotspots/detail', method: 'POST' },
  'board_hotspots_latest_detail': { path: '/board/hotspots/latest/detail', method: 'GET' },
  'board_indices': { path: '/board/indices', method: 'GET' },
  
  // 热点
  'hotspot_heats': { path: '/hotspot/heats', method: 'POST' },
  'hotspot_emotions': { path: '/hotspot/emotions', method: 'POST' },
  'hotspot_news': { path: '/hotspot/news', method: 'GET' },
  'hotspot_viewpoints': { path: '/hotspot/viewpoints', method: 'GET' },
  'hotspot_securities': { path: '/hotspot/securities', method: 'GET' },
  'hotspot_indices': { path: '/hotspot/indices', method: 'GET' },
  'hotspot_themes': { path: '/hotspot/themes', method: 'GET' },
  'hotspot_etfs': { path: '/hotspot/etfs', method: 'GET' },
  'hotspot_policies': { path: '/hotspot/policies', method: 'GET' },
  'hotspot_funds': { path: '/hotspot/funds', method: 'GET' },
  
  // 基金
  'fund_narratives': { path: '/v2.1/fund/narratives', method: 'GET' },
  
  // 指数
  'index_detail': { path: '/index/detail', method: 'GET' },
  'index_daily': { path: '/index/daily', method: 'GET' },
  
  // ETF
  'etf_narratives': { path: '/etf/narratives', method: 'GET' },
  
};

/**
 * 构建查询字符串
 */
function buildQueryString(params) {
  if (!params || Object.keys(params).length === 0) return '';
  const parts = [];
  for (const [key, value] of Object.entries(params)) {
    if (value !== undefined && value !== null) {
      parts.push(`${encodeURIComponent(key)}=${encodeURIComponent(value)}`);
    }
  }
  return parts.length > 0 ? '?' + parts.join('&') : '';
}

/**
 * 发送HTTP请求
 */
function makeRequest(options, body = null) {
  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => { data += chunk; });
      res.on('end', () => {
        try {
          const json = JSON.parse(data);
          resolve({ statusCode: res.statusCode, data: json });
        } catch (e) {
          resolve({ statusCode: res.statusCode, data: data });
        }
      });
    });
    
    req.on('error', reject);
    req.on('timeout', () => {
      req.destroy();
      reject(new Error('Request timeout'));
    });
    
    if (body) {
      req.write(JSON.stringify(body));
    }
    req.end();
  });
}

/**
 * 调用公开API
 * @param {string} apiName - API名称
 * @param {object} params - 请求参数（GET请求的query参数或POST请求的body）
 * @returns {Promise<object>} API响应
 */
async function call(apiName, params = {}) {
  const endpoint = API_ENDPOINTS[apiName];
  if (!endpoint) {
    throw new Error(`Unknown API: ${apiName}`);
  }
  
  if (!APPCODE) {
    throw new Error(`APPCODE not configured. Please set appcode in mcp_config.json`);
  }
  
  // 构建请求
  const queryString = endpoint.method === 'GET' ? buildQueryString(params) : '';
  const url = new URL(BASE_URL + endpoint.path + queryString);
  
  const options = {
    hostname: url.hostname,
    port: 443,
    path: url.pathname + url.search,
    method: endpoint.method,
    headers: {
      'Authorization': `APPCODE ${APPCODE}`,
      'Content-Type': 'application/json',
      'Accept': 'application/json'
    },
    timeout: 60000
  };
  
  const body = endpoint.method === 'POST' ? params : null;
  
  try {
    const response = await makeRequest(options, body);
    return response;
  } catch (error) {
    throw new Error(`API call failed: ${error.message}`);
  }
}

/**
 * 列出所有可用的API
 */
function listAPIs() {
  const apis = [];
  for (const [name, endpoint] of Object.entries(API_ENDPOINTS)) {
    apis.push({ name, path: endpoint.path, method: endpoint.method });
  }
  return apis;
}

// 导出
module.exports = {
  call,
  listAPIs,
  API_ENDPOINTS
};

// 命令行调用
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length === 0 || args[0] === '--list') {
    console.log('Usage: node call-node.js <apiName> <paramsJSON>');
    console.log('       node call-node.js --list');
    console.log('\nAvailable Public APIs:');
    const apis = listAPIs();
    apis.forEach(api => console.log(`  ${api.name} (${api.method} ${api.path})`));
    process.exit(0);
  }
  
  const apiName = args[0];
  let params = {};
  
  // 解析参数
  for (let i = 1; i < args.length; i++) {
    if (args[i].startsWith('{')) {
      try {
        params = JSON.parse(args[i]);
      } catch (e) {
        console.error('Invalid JSON params:', args[i]);
        process.exit(1);
      }
    }
  }
  
  call(apiName, params)
    .then(response => {
      console.log(JSON.stringify(response, null, 2));
    })
    .catch(error => {
      console.error('Error:', error.message);
      process.exit(1);
    });
}