#!/usr/bin/env node
/**
 * Search Aggregator - 整合 Tavily + Brave Search，合并去重
 * 
 * 用法:
 *   node search-aggregator.mjs "关键词" [options]
 * 
 * 选项:
 *   --days <n>    搜索最近 n 天的内容
 *   --max <n>     最大结果数 (默认 20)
 *   --json        输出 JSON 格式
 *   --verbose     显示详细信息
 */

import { parseArgs } from 'util';
import { homedir } from 'os';
import path from 'path';
import { fileURLToPath } from 'url';
import { spawn, execSync } from 'child_process';
import { readFileSync } from 'fs';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

// 解析命令行参数
const { values, positionals } = parseArgs({
  options: {
    days: { type: 'string', short: 'd' },
    max: { type: 'string', short: 'm', default: '20' },
    json: { type: 'boolean', default: false },
    verbose: { type: 'boolean', short: 'v', default: false }
  },
  allowPositionals: true
});

const query = positionals[0];
if (!query) {
  console.error('❌ 请提供搜索关键词');
  console.error('用法: node search-aggregator.mjs "关键词" [options]');
  process.exit(1);
}

const maxResults = parseInt(values.max) || 20;
const days = values.days ? parseInt(values.days) : null;

/**
 * 使用 Tavily API 直接搜索
 */
async function searchTavily(query, maxResults, days) {
  const apiKey = process.env.TAVILY_API_KEY;
  if (!apiKey) {
    if (values.verbose) console.error('⚠️  TAVILY_API_KEY 未配置');
    return [];
  }
  
  try {
    const body = {
      query,
      max_results: Math.ceil(maxResults / 2),
      include_answer: false,
      include_raw_content: false
    };
    
    if (days) {
      body.days = days;
    }
    
    const response = await fetch('https://api.tavily.com/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${apiKey}`
      },
      body: JSON.stringify(body)
    });
    
    if (!response.ok) {
      if (values.verbose) console.error('⚠️  Tavily API 错误:', response.status);
      return [];
    }
    
    const data = await response.json();
    
    return (data.results || []).map(item => ({
      title: item.title || 'Untitled',
      url: item.url,
      description: item.content || '',
      source: 'tavily',
      score: item.score || 0
    }));
  } catch (err) {
    if (values.verbose) console.error('❌ Tavily 搜索错误:', err.message);
    return [];
  }
}

/**
 * 使用 Brave Search API
 */
async function searchBrave(query, maxResults, days) {
  const apiKey = process.env.BRAVE_API_KEY;
  if (!apiKey) {
    if (values.verbose) console.error('⚠️  BRAVE_API_KEY 未配置');
    return [];
  }
  
  try {
    const url = new URL('https://api.search.brave.com/res/v1/web/search');
    url.searchParams.set('q', query);
    url.searchParams.set('count', String(Math.ceil(maxResults / 2)));
    
    if (days) {
      const freshOffset = new Date();
      freshOffset.setDate(freshOffset.getDate() - days);
      url.searchParams.set('freshness', freshOffset.toISOString().split('T')[0]);
    }
    
    const response = await fetch(url.toString(), {
      headers: {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip',
        'X-Subscription-Token': apiKey
      }
    });
    
    if (!response.ok) {
      if (values.verbose) console.error('⚠️  Brave API 错误:', response.status);
      return [];
    }
    
    const data = await response.json();
    
    return (data.web?.results || []).map(item => ({
      title: item.title,
      url: item.url,
      description: item.description || '',
      source: 'brave',
      published: item.published
    }));
  } catch (err) {
    if (values.verbose) console.error('❌ Brave 搜索错误:', err.message);
    return [];
  }
}

/**
 * 计算字符串相似度 (Jaccard similarity)
 */
function similarity(str1, str2) {
  const s1 = str1.toLowerCase();
  const s2 = str2.toLowerCase();
  
  if (s1 === s2) return 1.0;
  if (!s1 || !s2) return 0;
  
  const set1 = new Set(s1.split(/\s+/));
  const set2 = new Set(s2.split(/\s+/));
  
  const intersection = new Set([...set1].filter(x => set2.has(x)));
  const union = new Set([...set1, ...set2]);
  
  return intersection.size / union.size;
}

/**
 * URL 规范化
 */
function normalizeUrl(url) {
  try {
    const parsed = new URL(url);
    // 移除常见的跟踪参数
    parsed.searchParams.delete('utm_source');
    parsed.searchParams.delete('utm_medium');
    parsed.searchParams.delete('utm_campaign');
    parsed.searchParams.delete('ref');
    parsed.searchParams.delete('from');
    parsed.searchParams.delete('fbclid');
    parsed.searchParams.delete('gclid');
    // 移除末尾斜杠
    let path = parsed.pathname;
    if (path.endsWith('/') && path.length > 1) path = path.slice(0, -1);
    parsed.pathname = path;
    return parsed.toString().toLowerCase();
  } catch {
    return url.toLowerCase();
  }
}

/**
 * 合并去重结果
 */
function mergeAndDeduplicate(tavilyResults, braveResults, maxResults, threshold = 0.75) {
  const allResults = [...tavilyResults, ...braveResults];
  const seen = new Map();
  const deduped = [];
  
  for (const result of allResults) {
    const normalizedUrl = normalizeUrl(result.url);
    
    // 检查是否已存在
    let isDuplicate = false;
    
    for (const [existingUrl, existingResult] of seen) {
      // URL 完全匹配
      if (existingUrl === normalizedUrl) {
        isDuplicate = true;
        break;
      }
      
      // 标题高度相似
      if (similarity(existingResult.title, result.title) > threshold) {
        isDuplicate = true;
        break;
      }
    }
    
    if (!isDuplicate) {
      seen.set(normalizedUrl, result);
      deduped.push(result);
    }
    
    if (deduped.length >= maxResults) break;
  }
  
  return deduped;
}

/**
 * 主函数
 */
async function main() {
  if (values.verbose) {
    console.error('🔍 搜索关键词:', query);
    console.error('📊 最大结果数:', maxResults);
    if (days) console.error('📅 时间范围: 最近', days, '天');
  }
  
  // 并行执行两个搜索
  const [tavilyResults, braveResults] = await Promise.all([
    searchTavily(query, maxResults, days),
    searchBrave(query, maxResults)
  ]);
  
  if (values.verbose) {
    console.error('✅ Tavily 结果:', tavilyResults.length, '条');
    console.error('✅ Brave 结果:', braveResults.length, '条');
  }
  
  // 合并去重
  const merged = mergeAndDeduplicate(tavilyResults, braveResults, maxResults);
  
  if (values.verbose) {
    console.error('🔗 合并去重后:', merged.length, '条');
  }
  
  // 输出结果
  if (values.json) {
    console.log(JSON.stringify({
      query,
      total: merged.length,
      sources: {
        tavily: tavilyResults.length,
        brave: braveResults.length
      },
      results: merged
    }, null, 2));
  } else {
    console.log(`\n## 搜索结果: "${query}"\n`);
    console.log(`找到 ${merged.length} 条结果 (Tavily: ${tavilyResults.length}, Brave: ${braveResults.length})\n`);
    
    merged.forEach((item, idx) => {
      console.log(`### ${idx + 1}. ${item.title}`);
      console.log(`- 来源: ${item.source === 'tavily' ? 'Tavily' : 'Brave'}`);
      if (item.description) {
        const desc = item.description.slice(0, 150);
        console.log(`- 摘要: ${desc}${item.description.length > 150 ? '...' : ''}`);
      }
      console.log(`- 链接: ${item.url}\n`);
    });
  }
}

main().catch(err => {
  console.error('❌ 错误:', err.message);
  if (values.verbose) console.error(err.stack);
  process.exit(1);
});
