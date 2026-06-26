#!/usr/bin/env node
/**
 * WebSearch - Agent 专用搜索工具 v2.0
 * 基于 SearchAPI
 * 
 * 特点：
 * - 多种搜索类型：网页、新闻、视频、财经
 * - 错误自动重试，提高稳定性
 * - 结构化返回，Agent 直接可用
 * - 零外部依赖，易于迁移
 */

const https = require('https');
const querystring = require('querystring');
const fs = require('fs');
const path = require('path');

// ============ 配置 ============

const CONFIG_FILE = path.join(__dirname, 'config.json');
const DEFAULT_CONFIG = {
  apiKey: '',
  num: 5,
  lang: 'zh-CN',
  gl: 'cn',
  engine: 'google',
  maxRetries: 3,
  timeout: 15000
};

// 加载配置
function loadConfig() {
  try {
    if (fs.existsSync(CONFIG_FILE)) {
      return { ...DEFAULT_CONFIG, ...JSON.parse(fs.readFileSync(CONFIG_FILE, 'utf8')) };
    }
  } catch (e) {
    console.error('加载配置失败:', e.message);
  }
  return DEFAULT_CONFIG;
}

// 保存配置
function saveConfig(config) {
  fs.writeFileSync(CONFIG_FILE, JSON.stringify(config, null, 2));
  console.log('✅ 配置已保存到:', CONFIG_FILE);
}

// ============ 搜索核心 ============

const API_BASE = 'https://www.searchapi.io/api/v1/search';

// 搜索引擎映射
const ENGINES = {
  // 网页搜索
  web: 'google',
  google: 'google',
  // 新闻搜索
  news: 'google_news',
  // 视频搜索  
  video: 'google_videos',
  // 财经搜索
  finance: 'google_finance',
  stock: 'google_finance',
  // 地图搜索
  maps: 'google_maps',
  // 酒店搜索
  hotels: 'google_hotels',
  // 航班搜索
  flights: 'google_flights'
};

/**
 * 带重试的搜索请求
 */
async function searchWithRetry(query, options = {}, retryCount = 0) {
  const config = loadConfig();
  const maxRetries = options.maxRetries || config.maxRetries;
  const timeout = options.timeout || config.timeout;
  
  const engineName = options.type || 'web';
  const engine = ENGINES[engineName] || 'google';
  
  const params = {
    q: query,
    num: options.num || config.num,
    hl: options.lang || config.lang,
    gl: options.gl || config.gl,
    engine: engine,
    api_key: config.apiKey
  };
  
  // 财经搜索特殊参数
  if (engine === 'google_finance') {
    params.google_domain = 'google.com';
  }
  
  if (!params.api_key) {
    return {
      success: false,
      error: 'API Key 未配置。请运行: node WebSearchAPI config set-key YOUR_API_KEY',
      query
    };
  }
  
  try {
    return await executeSearch(params, timeout);
  } catch (error) {
    // 判断是否可重试
    const isRetryable = error.message.includes('timeout') || 
                        error.message.includes('ECONNREFUSED') ||
                        error.message.includes('ENOTFOUND');
    
    if (retryCount < maxRetries && isRetryable) {
      console.log(`⚠️ 请求失败，${retryCount + 1}/${maxRetries} 次重试...`);
      await new Promise(r => setTimeout(r, 1000 * (retryCount + 1))); // 指数退避
      return searchWithRetry(query, options, retryCount + 1);
    }
    
    return {
      success: false,
      error: error.message,
      query,
      retries: retryCount
    };
  }
}

/**
 * 执行搜索请求
 */
function executeSearch(params, timeout) {
  return new Promise((resolve, reject) => {
    const url = `${API_BASE}?${querystring.stringify(params)}`;
    
    const req = https.request(url, {
      method: 'GET',
      headers: {
        'Accept': 'application/json'
      }
    }, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          const result = JSON.parse(data);
          
          if (result.error) {
            resolve({
              success: false,
              error: result.error,
              query: params.q
            });
            return;
          }
          
          // 根据搜索类型格式化结果
          const formatted = formatResults(result, params.engine);
          
          resolve({
            success: true,
            query: result.search_parameters?.q || params.q,
            type: params.engine,
            count: formatted.results.length,
            results: formatted.results,
            metadata: {
              totalResults: result.search_information?.total_results || 0,
              timeTaken: result.search_information?.time_taken_displayed || 0,
              engine: params.engine
            }
          });
        } catch (e) {
          reject(new Error(`解析失败: ${e.message}`));
        }
      });
    });
    
    req.on('error', reject);
    req.setTimeout(timeout, () => {
      req.destroy();
      reject(new Error(`请求超时 (${timeout}ms)`));
    });
    
    req.end();
  });
}

/**
 * 格式化搜索结果
 */
function formatResults(result, engine) {
  // 根据不同搜索引擎提取结果
  let items = [];
  
  switch (engine) {
    case 'google':
    case 'google_videos':
      items = result.organic_results || [];
      break;
    case 'google_news':
      items = result.news_results || result.organic_results || [];
      break;
    case 'google_finance':
      items = result.finance_results || result.organic_results || [];
      break;
    case 'google_maps':
      items = result.maps_places || result.organic_results || [];
      break;
    case 'google_hotels':
      items = result.hotels_results || result.organic_results || [];
      break;
    case 'google_flights':
      items = result.flights_results || result.organic_results || [];
      break;
    default:
      items = result.organic_results || [];
  }
  
  // 统一格式化
  return {
    results: items.slice(0, 20).map(item => formatItem(item, engine))
  };
}

/**
 * 格式化单个结果
 */
function formatItem(item, engine) {
  const base = {
    title: item.title || item.name || '',
    link: item.link || item.url || item.url || '',
    source: item.source || item.publisher || ''
  };
  
  // 根据引擎添加特定字段
  switch (engine) {
    case 'google_news':
      return {
        ...base,
        snippet: item.snippet || item.description || '',
        date: item.date || item.published_date || null,
        thumbnail: item.thumbnail || null
      };
      
    case 'google_finance':
      return {
        ...base,
        price: item.price || item.price_change || null,
        change: item.price_change || item.price_change_percent || null,
        snippet: item.snippet || item.description || ''
      };
      
    case 'google_videos':
      return {
        ...base,
        snippet: item.snippet || item.description || '',
        duration: item.duration || null,
        source: item.source || item.channel || ''
      };
      
    case 'google_maps':
      return {
        ...base,
        address: item.address || item.location || '',
        rating: item.rating || null,
        reviews: item.reviews || null,
        phone: item.phone || null
      };
      
    case 'google_hotels':
      return {
        ...base,
        price: item.price || item.rate?.lowest || null,
        rating: item.rating || item.score || null,
        address: item.address || '',
        amenities: item.amenities || []
      };
      
    case 'google_flights':
      return {
        ...base,
        price: item.price || item.fare || null,
        airline: item.airline || item.carrier || '',
        departure: item.departure_time || item.departure || '',
        arrival: item.arrival_time || item.arrival || '',
        stops: item.stops || null,
        duration: item.duration || null
      };
      
    default: // web
      return {
        ...base,
        snippet: item.snippet?.substring(0, 300) || '',
        date: item.date || null
      };
  }
}

// ============ CLI 命令 ============

function help() {
  console.log(`
╔═══════════════════════════════════════════════════════════════╗
║           WebSearch v2.0 - Agent 专用搜索工具          ║
╠═══════════════════════════════════════════════════════════════╣
║  用法: node WebSearchAPI <命令> [参数]                     ║
╠═══════════════════════════════════════════════════════════════╣
║  搜索类型:                                                   ║
║    web      - 网页搜索 (默认)                                ║
║    news     - 新闻搜索                                       ║
║    video    - 视频搜索                                       ║
║    finance  - 财经/股票搜索                                  ║
║    maps     - 地图/地点搜索                                   ║
║    hotels   - 酒店搜索                                       ║
║    flights  - 航班搜索                                       ║
╠═══════════════════════════════════════════════════════════════╣
║  命令:                                                       ║
║    search <关键词>     执行搜索 (默认网页)                   ║
║    s <关键词>          简写形式                              ║
║    <type> <关键词>     指定类型搜索                          ║
║    config              查看当前配置                          ║
║    config set-key     设置 API Key                          ║
║    test               测试搜索功能                          ║
║    help               显示帮助                              ║
╠═══════════════════════════════════════════════════════════════╣
║  选项:                                                       ║
║    --num=<数字>       结果数量 (默认 5)                    ║
║    --lang=<代码>      语言 (默认 zh-CN)                     ║
║    --gl=<国家>        地区 (默认 cn)                        ║
║    --json             JSON 格式输出                         ║
║    --retry=<数字>     最大重试次数 (默认 3)                 ║
╠═══════════════════════════════════════════════════════════════╣
║  示例:                                                       ║
║    node WebSearchAPI search "MCP 协议"                     ║
║    node WebSearchAPI news "AI 发展"                        ║
║    node WebSearchAPI finance "AAPL 股票"                   ║
║    node WebSearchAPI video "Python 教程"                   ║
║    node WebSearchAPI s "AI" --num=10 --json              ║
╚═══════════════════════════════════════════════════════════════╝
`);
}

async function main() {
  const args = process.argv.slice(2);
  const command = args[0] || 'help';
  
  // 解析选项
  const options = {};
  const remainingArgs = args.slice(1).filter(arg => {
    if (arg.startsWith('--')) {
      const [key, value] = arg.substring(2).split('=');
      if (key === 'json') options.json = true;
      else if (key === 'num') options.num = parseInt(value);
      else if (key === 'lang') options.lang = value;
      else if (key === 'gl') options.gl = value;
      else if (key === 'retry') options.maxRetries = parseInt(value);
      else if (key === 'timeout') options.timeout = parseInt(value);
      return false;
    }
    return true;
  });
  
  // 检查是否是搜索类型命令
  const searchTypes = ['web', 'news', 'video', 'finance', 'stock', 'maps', 'hotels', 'flights'];
  
  try {
    // 搜索类型 + 关键词 (如: news "关键词")
    if (searchTypes.includes(command) && remainingArgs.length > 0) {
      options.type = command;
      const query = remainingArgs.join(' ');
      const result = await searchWithRetry(query, options);
      outputResult(result, options);
      return;
    }
    
    switch (command) {
      case 'help':
      case '-h':
        help();
        break;
        
      case 'search':
      case 's': {
        const query = remainingArgs.join(' ');
        if (!query) {
          console.error('❌ 错误: 请输入搜索关键词');
          process.exit(1);
        }
        const result = await searchWithRetry(query, options);
        outputResult(result, options);
        break;
      }
      
      case 'config': {
        const subCmd = remainingArgs[0];
        const config = loadConfig();
        
        if (!subCmd || subCmd === 'show') {
          console.log('当前配置:');
          // 隐藏 API Key 显示
          const safeConfig = { ...config, apiKey: config.apiKey ? '****' + config.apiKey.slice(-4) : '' };
          console.log(JSON.stringify(safeConfig, null, 2));
          break;
        }
        
        if (subCmd === 'set-key') {
          const apiKey = remainingArgs[1];
          if (!apiKey) {
            console.error('用法: config set-key YOUR_API_KEY');
            process.exit(1);
          }
          config.apiKey = apiKey;
          saveConfig(config);
          break;
        }
        
        if (subCmd === 'set-num') {
          config.num = parseInt(remainingArgs[1]) || 5;
          saveConfig(config);
          break;
        }
        
        if (subCmd === 'set-lang') {
          config.lang = remainingArgs[1] || 'zh-CN';
          saveConfig(config);
          break;
        }
        
        if (subCmd === 'set-gl') {
          config.gl = remainingArgs[1] || 'cn';
          saveConfig(config);
          break;
        }
        
        if (subCmd === 'set-retry') {
          config.maxRetries = parseInt(remainingArgs[1]) || 3;
          saveConfig(config);
          break;
        }
        
        console.log('未知配置命令。可用: set-key, set-num, set-lang, set-gl, set-retry');
        break;
      }
      
      case 'test': {
        console.log('🧪 测试搜索功能...');
        const result = await searchWithRetry('test', { num: 1 });
        if (result.success) {
          console.log('✅ 搜索功能正常!');
          console.log('   返回结果数:', result.count);
          console.log('   耗时:', result.metadata.timeTaken + 's');
        } else {
          console.log('❌ 搜索失败:', result.error);
          process.exit(1);
        }
        break;
      }
      
      default:
        // 尝试作为搜索类型处理
        if (remainingArgs.length > 0) {
          options.type = command;
          const result = await searchWithRetry(remainingArgs.join(' '), options);
          outputResult(result, options);
        } else {
          console.log(`❌ 未知命令: ${command}`);
          console.log('运行 --help 查看帮助');
        }
    }
  } catch (e) {
    console.error('❌ 错误:', e.message);
    process.exit(1);
  }
}

// 输出结果
function outputResult(result, options) {
  if (options.json) {
    console.log(JSON.stringify(result, null, 2));
  } else {
    printResult(result);
  }
}

// 格式化输出
function printResult(result) {
  if (!result.success) {
    console.log('❌ 搜索失败:', result.error);
    if (result.retries) console.log(`   已重试 ${result.retries} 次`);
    return;
  }
  
  const typeLabels = {
    google: '🔍 网页',
    google_news: '📰 新闻',
    google_videos: '🎬 视频',
    google_finance: '💰 财经',
    google_maps: '📍 地图',
    google_hotels: '🏨 酒店',
    google_flights: '✈️ 航班'
  };
  
  console.log(`\n${typeLabels[result.metadata.engine] || '🔍'} 查询: "${result.query}"`);
  console.log(`📊 找到 ${result.count} 条结果 (耗时 ${result.metadata.timeTaken}s)\n`);
  
  result.results.forEach((item, i) => {
    console.log(`${i + 1}. ${item.title}`);
    if (item.link) console.log(`   🔗 ${item.link}`);
    if (item.snippet) console.log(`   📝 ${item.snippet.substring(0, 80)}...`);
    
    // 类型特定字段
    const extras = [];
    if (item.price) extras.push(`💰 ${item.price}`);
    if (item.rating) extras.push(`⭐ ${item.rating}`);
    if (item.date) extras.push(`📅 ${item.date}`);
    if (item.source) extras.push(`📰 ${item.source}`);
    if (item.airline) extras.push(`✈️ ${item.airline}`);
    
    if (extras.length > 0) console.log(`   ${extras.join(' | ')}`);
    console.log('');
  });
}

// 导出
module.exports = { search: searchWithRetry, loadConfig };

// CLI 入口
if (require.main === module) {
  main();
}
