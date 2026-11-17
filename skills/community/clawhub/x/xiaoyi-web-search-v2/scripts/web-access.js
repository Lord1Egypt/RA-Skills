#!/usr/bin/env node

/**
 * 小艺联网搜索 - 华为云 AI 联网搜索 API
 * 根据 SKILL.md 说明实现
 *
 * 用法:
 *   node web-access.js "搜索关键词"
 *   node web-access.js "关键词" -n 10
 *
 * ⚙️ 首次使用前必须配置 TOKEN，详见 SKILL.md 的「安装后必读：配置TOKEN」章节
 */

const axios = require('axios');
const fs = require('fs');


// API 配置
// 🔑 必填：请填入你的华为云 AI 联网增强 Token
// 开通指南：https://developer.huawei.com/consumer/cn/doc/AppGallery-connect-Guides/agc-ainetworking-serviceopen-0000002370503878
const API_URL = 'https://connect-api.cloud.huawei.com/api/aiNetworking/v1/webSearch';
const TOKEN = '';


/**
 * 执行联网搜索
 * @param {string} query - 搜索关键词
 * @param {number} count - 返回结果数量（默认10，最大建议不超过20）
 * @returns {Promise<Array>} 搜索结果数组
 */
async function webSearch(query, count = 10) {
  try {
	// 请求接口
    const response = await axios.post(
        API_URL,
        {
          query: query,
          count: Math.min(count, 10) // 限制最大20条
        },
        {
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${TOKEN}`
          },
          timeout: 30000
        }
    );
    const data = response.data;

    // 检查API返回状态，并返回结果
    if (data.code !== 0) {
      console.error(`❌ API 错误: ${data.msg || '未知错误'}`);
      return [];
    }
    return data.webResult || [];
  } catch (error) {
    if (error.response) {
      console.error(`❌ API 请求失败: ${error.response.status} - ${error.response.statusText}`);
      if (error.response.status === 401) {
        console.error('⚠️ Token 可能已过期，请更新 Token');
      }
    } else if (error.request) {
      console.error('❌ 网络错误: 无法连接到华为云 API');
    } else {
      console.error(`❌ 错误: ${error.message}`);
    }
    return [];
  }
}

/**
 * 格式化输出搜索结果
 * @param {Array} results - 搜索结果数组
 * @param {string} query - 搜索关键词
 */
function formatResults(results, query) {
  if (!results || results.length === 0) {
    console.log(`🔍 搜索 "${query}" 未找到结果`);
    return;
  }

  console.log(`\n🔍 搜索结果: "${query}"`);
  console.log(`✅ 找到 ${results.length} 条相关结果\n`);
  console.log('='.repeat(80));

  results.forEach((item, index) => {
    console.log(`\n📌 ${index + 1}. ${item.title || 'N/A'}`);
    console.log(`🔗 ${item.url || 'N/A'}`);

    if (item.chunk) {
      const snippet = item.chunk.length > 200 ? item.chunk.substring(0, 200) + '...' : item.chunk;
      console.log(`📝 ${snippet}`);
    }

    if (item.siteName) {
      console.log(`🏷️ 来源: ${item.siteName}`);
    }

    console.log('-'.repeat(80));
  });

  console.log(`\n💡 共找到 ${results.length} 条相关结果`);
}

/**
 * 解析命令行参数
 */
function parseArgs() {
  const args = process.argv.slice(2);
  const options = {
    query: '',
    count: 10
  };

  for (let i = 0; i < args.length; i++) {
    const arg = args[i];

    if (arg === '-n' || arg === '--count') {
      const next = args[i + 1];
      if (next && !next.startsWith('-')) {
        options.count = parseInt(next, 10);
        i++;
      }
    } else if (!arg.startsWith('-')) {
      options.query = arg;
    }
  }

  return options;
}

// 主程序
async function main() {
  const options = parseArgs();

  if (!options.query) {
    console.log('小艺联网搜索 - 华为云 AI 联网搜索');
    console.log('');
    console.log('用法:');
    console.log('  node web-access.js "搜索关键词"              # 默认10条结果');
    console.log('  node web-access.js "关键词" -n 10            # 返回10条结果');
    console.log('');
    console.log('⚠️  首次使用前请先配置 TOKEN（见 SKILL.md）');
    console.log('');
    console.log('示例:');
    console.log('  node web-access.js "人工智能最新进展"');
    console.log('  node web-access.js "ChatGPT 新闻" -n 10');
    process.exit(0);
  }

  const results = await webSearch(options.query, options.count);
  formatResults(results, options.query);
}

// 导出函数供外部调用
module.exports = { webSearch };

// 如果直接运行则执行主程序
if (require.main === module) {
  main();
}
