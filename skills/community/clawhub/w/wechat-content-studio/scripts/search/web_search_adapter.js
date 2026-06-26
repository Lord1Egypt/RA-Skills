#!/usr/bin/env node

/**
 * WorkBuddy WebSearch 适配器
 * 
 * 使用 WorkBuddy 内置的 web_search 工具替代 Brave Search
 * 支持 site: 语法进行站内搜索
 */

import { spawn } from 'child_process';
import path from 'path';
import { fileURLToPath } from 'url';
import fs from 'fs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const KEYWORD_SEARCH_DIR = path.join(__dirname, '../../../keyword-search');

/**
 * 调用 keyword-search 技能进行搜索
 * @param {string} keyword - 搜索关键词
 * @param {string[]} sites - 要搜索的站点列表（如 ['mp.weixin.qq.com', 'zhihu.com']）
 * @param {number} limit - 每关键词最多结果数
 * @returns {Promise<Array>} 搜索结果数组
 */
export async function searchWithWebSearch(keyword, sites = [], limit = 20) {
  return new Promise((resolve, reject) => {
    const siteQuery = sites.map(site => `site:${site}`).join(' OR ');
    const query = `"${keyword}" ${siteQuery}`;
    
    console.log(`  🔍 WorkBuddy WebSearch: ${query}`);
    
    // 构造临时脚本调用 keyword-search
    const tempScript = path.join(__dirname, '../../temp_search.js');
    const scriptContent = `
      const { multiSourceSearch } = require('./multi_source_search.js');
      
      async function main() {
        try {
          // 这里需要通过 Agent 调用 web_search 工具
          // 由于无法直接调用，我们返回查询字符串让 Agent 执行
          console.log(JSON.stringify({
            query: "${query.replace(/"/g, '\\"')}",
            keyword: "${keyword.replace(/"/g, '\\"')}",
            sites: ${JSON.stringify(sites)},
            limit: ${limit}
          }));
        } catch (err) {
          console.error(JSON.stringify({ error: err.message }));
          process.exit(1);
        }
      }
      
      main();
    `;
    
    // 注意：由于 web_search 是 Agent 专用工具，Node.js 脚本无法直接调用
    // 我们需要采用不同的策略：让 Agent 直接处理搜索逻辑
    
    // 返回查询信息，由 Agent 调用 web_search 工具
    resolve({
      query: query,
      keyword: keyword,
      sites: sites,
      limit: limit,
      message: '需要通过 Agent 调用 web_search 工具执行搜索'
    });
  });
}

/**
 * 微信公众号搜索适配器
 * @param {string} keyword - 关键词
 * @param {string} accountName - 公众号名称（可选，为空则全网搜索）
 * @param {number} maxResults - 最大结果数
 */
export async function searchWechatWithWebSearch(keyword, accountName = null, maxResults = 5) {
  const sites = ['mp.weixin.qq.com'];
  
  if (accountName) {
    // 有指定公众号名时，在关键词中包含
    keyword = `"${accountName}" ${keyword}`;
  }
  
  return searchWithWebSearch(keyword, sites, maxResults);
}

/**
 * 通用站点搜索适配器
 * @param {string} keyword - 关键词
 * @param {string} domain - 域名（如 'zhihu.com'）
 * @param {number} maxResults - 最大结果数
 */
export async function searchSiteWithWebSearch(keyword, domain, maxResults = 5) {
  return searchWithWebSearch(keyword, [domain], maxResults);
}

// 导出适配器函数
export default {
  searchWithWebSearch,
  searchWechatWithWebSearch,
  searchSiteWithWebSearch,
};
