#!/usr/bin/env node

/**
 * 酒云网商品搜索脚本
 *
 * 调用酒云网接口搜索商品列表，支持关键词、价格区间、国家、类型等筛选。
 */

const https = require('https');

const API_URL = 'https://wxapp.vinehoo.com/openai/v3/product/list';

// 支持的国家列表
const SUPPORTED_COUNTRIES = [
  '中国', '法国', '意大利', '澳大利亚', '葡萄牙', '德国', '西班牙',
  '新西兰', '智利', '阿根廷', '美国', '奥地利', '南非', '日本'
];

// 支持的商品类型列表
const SUPPORTED_CATEGORIES = [
  '红葡萄酒', '白葡萄酒', '起泡酒', '香槟', '甜酒', '烈酒', '白酒/黄酒',
  '清酒', '果酒/米酒', '食品/生鲜', '饮料', '自然酒', '加强酒',
  '桃红葡萄酒', '其他酒', '酒具'
];

/**
 * 发起 HTTPS POST 请求
 */
function httpsRequest(url, data) {
  return new Promise((resolve, reject) => {
    const urlObj = new URL(url);
    const options = {
      hostname: urlObj.hostname,
      path: urlObj.pathname,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(JSON.stringify(data))
      }
    };

    const req = https.request(options, (res) => {
      let responseData = '';

      res.on('data', (chunk) => {
        responseData += chunk;
      });

      res.on('end', () => {
        if (res.statusCode >= 400) {
          reject(new Error(`HTTP请求失败: 状态码 ${res.statusCode}, 响应内容: ${responseData}`));
        } else {
          try {
            const jsonData = JSON.parse(responseData);
            resolve(jsonData);
          } catch (e) {
            reject(new Error(`JSON解析失败: ${e.message}`));
          }
        }
      });
    });

    req.on('error', (e) => {
      reject(new Error(`接口调用失败: ${e.message}`));
    });

    req.write(JSON.stringify(data));
    req.end();
  });
}

/**
 * 搜索商品
 */
async function searchProducts(options) {
  const {
    page = 1,
    limit = 10,
    keywords,
    price_gte,
    price_lte,
    countries,
    product_category
  } = options;

  // 构建请求参数
  const payload = {
    page,
    limit
  };

  // 添加可选参数
  if (keywords) {
    payload.keywords = keywords;
  }
  if (price_gte !== undefined && price_gte !== null) {
    payload.price_gte = price_gte;
  }
  if (price_lte !== undefined && price_lte !== null) {
    payload.price_lte = price_lte;
  }

  // 添加筛选参数
  const filters = {};

  if (countries && countries.length > 0) {
    // 验证国家是否支持
    const invalidCountries = countries.filter(c => !SUPPORTED_COUNTRIES.includes(c));
    if (invalidCountries.length > 0) {
      throw new Error(`不支持的国家: ${invalidCountries.join(', ')}. 支持的国家: ${SUPPORTED_COUNTRIES.join(', ')}`);
    }
    filters.country = countries;
  }

  if (product_category) {
    // 验证商品类型是否支持
    if (!SUPPORTED_CATEGORIES.includes(product_category)) {
      throw new Error(`不支持的商品类型: ${product_category}. 支持的类型: ${SUPPORTED_CATEGORIES.join(', ')}`);
    }
    filters.product_category = [product_category];
  }

  if (Object.keys(filters).length > 0) {
    payload.filters = filters;
  }

  // 发起请求
  const result = await httpsRequest(API_URL, payload);

  // 检查业务错误码
  if (result.error_code !== 0) {
    throw new Error(`接口业务错误: ${result.error_msg || '未知错误'}`);
  }

  return result;
}

/**
 * 解析命令行参数
 */
function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    page: 1,
    limit: 10
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];
    const nextArg = args[i + 1];

    switch (arg) {
      case '--page':
        options.page = parseInt(nextArg, 10);
        i++;
        break;
      case '--limit':
        options.limit = parseInt(nextArg, 10);
        i++;
        break;
      case '--keywords':
        options.keywords = nextArg;
        i++;
        break;
      case '--price-gte':
        options.price_gte = parseFloat(nextArg);
        i++;
        break;
      case '--price-lte':
        options.price_lte = parseFloat(nextArg);
        i++;
        break;
      case '--countries':
        // 收集所有国家参数
        options.countries = [];
        i++;
        while (i < args.length && !args[i].startsWith('--')) {
          options.countries.push(args[i]);
          i++;
        }
        i--;
        break;
      case '--category':
        options.product_category = nextArg;
        i++;
        break;
    }
  }

  return options;
}

/**
 * 主函数
 */
async function main() {
  try {
    // 解析命令行参数
    const options = parseArgs();

    // 验证必需参数
    if (!options.page) {
      console.error('错误: --page 参数是必需的');
      process.exit(1);
    }

    // 调用搜索接口
    const result = await searchProducts(options);

    // 输出结果（JSON 格式）
    console.log(JSON.stringify(result, null, 2));

  } catch (error) {
    console.error(`错误: ${error.message}`);
    process.exit(1);
  }
}

// 如果直接运行此脚本，则执行主函数
if (require.main === module) {
  main();
}

module.exports = { searchProducts };
