#!/usr/bin/env node

/**
 * 小艺联网搜索 - 华为云 AI 联网搜索 API
 * 根据 SKILL.md 说明实现
 * 
 * 用法: 
 *   node search.js "搜索关键词"
 *   node search.js "关键词" -n 5
 */

const axios = require('axios');

// API 配置
const API_URL = 'https://connect-api.cloud.huawei.com/api/aiNetworking/v1/webSearch';

// 华为云 API Token（从 SKILL.md 获取）
const TOKEN = 'eyJhbGciOiJQUzI1NiIsImtpZCI6IjNjMWZhNWQwNjIxNzRkYTA4MWNlY2E4NTY3NDViYTQxIiwidHlwIjoiSldUIn0.eyJhdWQiOiJodHRwczovL29hdXRoLWxvZ2luLmNsb3VkLmh1YXdlaS5jb20vb2F1dGgyL3YzL3Rva2VuIiwiaXNzIjoiMTE2OTAyNzI3IiwiaWF0IjoxNzcxMDQxOTAzLCJleHAiOjE3Nzg4MTc5MDN9.f0_MUN_7MfYO_4d70xC0rCwkHNDvi4wmEx3nlAk9G-BALtYyhUa1d8dZg3nqhbX_Xom48FZ_hWD7QhBCuOTNZWLWskSiZwRmPSTqujr7swiB0cx8c7AHF9xRr0xHQTDOlU0iFf-yjb1S8eZ8Xb4hAmvFwSGkHN2PPz1qMSNl7LMhLHIurm64TzzHAM1whzwOceuGOtb7QQmcnGGfxxpzO1VwEqtPQYHAtQAJiC2WQu3_GGLrr6JHSuwkEcong4yppV9HVhRD51sUt6mRyICJbEAuMdM7vE50c0JohFFHJIqe8bnl2ORk-xv_jXVxAlAEQw32CLE_kYg7bWoV62oFz_35okR0J9eZsAVcdOsP5US1T2LFJvKS0pkO3XW2VdTg0ANwcCkQnsZzwP7tguC6GuH8mMTtXhEN8tfX394GQKvLJyJtng7tz8burFuWcfLlpUhHg-muwB28uBBCP6NUvcw_XmOAS2_CbdiliCFTpMFLq88t-1GChvod91cLjWPafPXg1GqSf8gDOXCkyqecc_nXpsRrFAqT8Ektgpo4zrVwnq5XskCnsLudqeqg4H3EU_tfC21yRMDR1pb7FhiXLRPJfvjpT1l5vLJWVClXVGfp4Pvx3eXnm4IeoaZ9DTl9QmP2mdF4NJAj9lb9Rw0LWInlWAUtniL9UCsQUui-tuQ';

/**
 * 执行联网搜索
 * @param {string} query - 搜索关键词
 * @param {number} count - 返回结果数量（默认10，最大建议不超过20）
 * @returns {Promise<Array>} 搜索结果数组
 */
async function webSearch(query, count = 10) {
  try {
    const response = await axios.post(
      API_URL,
      {
        query: query,
        count: Math.min(count, 20) // 限制最大20条
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

    // 检查 API 返回状态
    if (data.code !== 0) {
      console.error(`❌ API 错误: ${data.msg || '未知错误'}`);
      return [];
    }

    // 返回搜索结果
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
    console.log('  node search.js "搜索关键词"              # 默认10条结果');
    console.log('  node search.js "关键词" -n 5            # 返回5条结果');
    console.log('');
    console.log('示例:');
    console.log('  node search.js "人工智能最新进展"');
    console.log('  node search.js "ChatGPT 新闻" -n 10');
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
