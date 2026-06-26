#!/usr/bin/env node

/**
 * 酒云网统计商品查询脚本
 *
 * 根据统计摘要的维度查询具体商品列表，支持按国家、类型、产区、酒庄筛选。
 */

const https = require('https');

const API_URL = 'https://wxapp.vinehoo.com/openai/v3/product/statistics_products';

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
 * 查询统计商品
 */
async function getStatisticsProducts(options) {
  const {
    page = 1,
    limit = 10,
    country,
    category,
    region,
    winery
  } = options;

  // 构建请求参数
  const payload = {
    page,
    limit
  };

  // 添加可选参数
  if (country) {
    payload.country = country;
  }
  if (category) {
    payload.category = category;
  }
  if (region) {
    payload.region = region;
  }
  if (winery) {
    payload.winery = winery;
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
      case '--country':
        options.country = nextArg;
        i++;
        break;
      case '--category':
        options.category = nextArg;
        i++;
        break;
      case '--region':
        options.region = nextArg;
        i++;
        break;
      case '--winery':
        options.winery = nextArg;
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

    // 调用统计商品查询接口
    const result = await getStatisticsProducts(options);

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

module.exports = { getStatisticsProducts };
