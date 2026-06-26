#!/usr/bin/env node

const { Command } = require('commander');
const axios = require('axios');
const crypto = require('crypto');

const program = new Command();

// 安全处理API密钥
function secureProcessApiKey(key) {
  if (!key) {
    return '';
  }
  return crypto.createHash('md5').update(key).digest('hex');
}

// 全局API密钥选项
let apiKey;
let secureApiKey;

// 安全日志记录函数
function secureLog(message) {
  // 替换API密钥为掩码
  if (secureApiKey) {
    return message.replace(new RegExp(secureApiKey, 'g'), '***API_KEY_MASKED***');
  }
  return message;
}

program
  .name('xhcj-finance') 
  .description('Xinhua Finance API CLI tool')
  .version('1.0.8')
  .option('--api-key <key>', 'API key for Xinhua Finance API');

// 解析命令行参数
const options = program.opts();

// 获取API密钥
apiKey = options.apiKey;

// 安全存储API密钥
secureApiKey = secureProcessApiKey(apiKey);

// 清除原始API密钥引用，减少内存中的暴露
apiKey = undefined;

// 记录程序启动信息
console.log('Xinhua Finance API CLI tool started');
if (secureApiKey) {
  console.log(`API key loaded: ${secureLog(secureApiKey)} ✓`);
}
console.log('API client initialized: ✓');

// 创建axios实例
const apiClient = axios.create({
  baseURL: 'https://xhcj-h5-zg.cnfin.com/xhcj-bun/func/openclaw', // 假设的API基础URL
  headers: {
    'Content-Type': 'application/json'
  }
});

// 添加请求拦截器，确保API密钥安全传输
apiClient.interceptors.request.use(
  (config) => {
    // 在发送请求前添加Authorization头
    if (secureApiKey) {
      config.headers.Authorization = `Bearer ${secureApiKey}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 添加响应拦截器，确保API密钥不会在响应中泄露
apiClient.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // 安全处理错误，避免API密钥泄露
    if (error.config) {
      // 移除错误对象中的Authorization头
      delete error.config.headers.Authorization;
    }
    return Promise.reject(error);
  }
);

// 行情数据命令
program
  .command('market')
  .description('Query market data')
  .option('--symbol <symbol>', 'A股股票代码，如000001.SZ')
  .action(async (options) => {
    if (!secureApiKey) {
      console.error('Error: --api-key is required');
      return;
    }
    if (!options.symbol) {
      console.error('Error: --symbol is required');
      return;
    }

    try {
      const response = await apiClient.post('/finance-data', {
        path: 'real',
        params: {
          symbol: options.symbol
        }
      });
      console.log('Market data:', JSON.stringify(response.data.data, null, 2));
    } catch (error) {
      // 安全处理错误，避免API密钥泄露
      if (error.response) {
        console.error('Error fetching market data: API request failed with status', error.response.status);
      } else if (error.request) {
        console.error('Error fetching market data: No response received from server');
      } else {
        console.error('Error fetching market data:', error.message);
      }
    }
  });

// 行情Kline数据命令
program
  .command('kline')
  .description('Query market kline data')
  .option('--symbol <symbol>', 'A股股票代码，如000001.SZ')
  .action(async (options) => {
    if (!secureApiKey) {
      console.error('Error: --api-key is required');
      return;
    }
    if (!options.symbol) {
      console.error('Error: --symbol is required');
      return;
    }

    try {
      const response = await apiClient.post('/finance-data', {
        path: 'kline',
        params: {
          symbol: options.symbol
        }
      });
      console.log('Kline data:', JSON.stringify(response.data.data, null, 2));
    } catch (error) {
      // 安全处理错误，避免API密钥泄露
      if (error.response) {
        console.error('Error fetching kline data: API request failed with status', error.response.status);
      } else if (error.request) {
        console.error('Error fetching kline data: No response received from server');
      } else {
        console.error('Error fetching kline data:', error.message);
      }
    }
  });

// 股票代码查询命令
program
  .command('symbol')
  .description('Query stock symbol')
  .option('--name <name>', '股票名称模糊查询，如"中国平安"，也可以是股票代码如"601318"')
  .action(async (options) => {
    if (!secureApiKey) {
      console.error('Error: --api-key is required');
      return;
    }
    if (!options.name) {
      console.error('Error: --name is required');
      return;
    }

    try {
      const response = await apiClient.post('/finance-data', {
        path: 'query_code',
        params: {
          name: options.name
        }
      });
      console.log('Symbol data:', JSON.stringify(response.data.data, null, 2));
    } catch (error) {
      // 安全处理错误，避免API密钥泄露
      if (error.response) {
        console.error('Error fetching symbol data: API request failed with status', error.response.status);
      } else if (error.request) {
        console.error('Error fetching symbol data: No response received from server');
      } else {
        console.error('Error fetching symbol data:', error.message);
      }
    }
  });

// 资讯命令
program
  .command('news')
  .description('Get news')
  .option('--category <category>', '新闻资讯分类：1-股票 2-商品期货 3-外汇 4-债券 5-宏观 9-全部, default 9', '9') 
  .option('--limit <number>', 'Limit results, default 10, max 20', '10')
  .action(async (options) => {
    if (!secureApiKey) {
      console.error('Error: --api-key is required');
      return;
    }
    try {
      const response = await apiClient.post('/finance-data', {
        path: 'news', 
        params: {
          category: options.category,
          limit: options.limit
        }
      });
      console.log('News:', JSON.stringify(response.data.data, null, 2));
    } catch (error) {
      // 安全处理错误，避免API密钥泄露
      if (error.response) {
        console.error('Error fetching news: API request failed with status', error.response.status);
      } else if (error.request) {
        console.error('Error fetching news: No response received from server');
      } else {
        console.error('Error fetching news:', error.message);
      }
    }
  });

program.parse(process.argv);