#!/usr/bin/env node

/**
 * 酒云网当日商品统计摘要脚本
 *
 * 获取当日新上商品的统计摘要，包括按国家、类型、酒庄、产区的分布情况。
 */

const https = require('https');

const API_URL = 'https://wxapp.vinehoo.com/openai/v3/product/statistics_summary';

/**
 * 发起 HTTPS POST 请求
 */
function httpsRequest(url, data = {}) {
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
 * 获取当日商品统计摘要
 */
async function getStatisticsSummary() {
  // 发起 POST 请求（无需参数）
  const result = await httpsRequest(API_URL, {});

  // 检查业务错误码
  if (result.error_code !== 0) {
    throw new Error(`接口业务错误: ${result.error_msg || '未知错误'}`);
  }

  return result;
}

/**
 * 主函数
 */
async function main() {
  try {
    // 调用统计接口
    const result = await getStatisticsSummary();

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

module.exports = { getStatisticsSummary };
