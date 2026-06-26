#!/usr/bin/env node
/**
 * 内容摘要生成器 - 对搜索结果进行深度摘要
 * 
 * 用法:
 *   node summarize-content.mjs <url>
 *   node summarize-content.mjs --urls "url1,url2,url3"
 */

import { parseArgs } from 'util';
import { homedir } from 'os';
import path from 'path';
import { fileURLToPath } from 'url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

const { values, positionals } = parseArgs({
  options: {
    urls: { type: 'string' },
    maxLength: { type: 'string', default: '200' },
    minLength: { type: 'string', default: '60' }
  },
  allowPositionals: true
});

const TAVILY_API_KEY = process.env.TAVILY_API_KEY;

/**
 * 使用 Tavily Extract API 提取网页内容
 */
async function extractContent(url) {
  if (!TAVILY_API_KEY) {
    return { error: 'TAVILY_API_KEY not configured' };
  }
  
  try {
    const response = await fetch('https://api.tavily.com/extract', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${TAVILY_API_KEY}`
      },
      body: JSON.stringify({
        urls: [url],
        extract_depth: 'advanced',
        include_images: false
      })
    });
    
    if (!response.ok) {
      return { error: `API error: ${response.status}` };
    }
    
    const data = await response.json();
    
    if (data.results && data.results.length > 0) {
      const result = data.results[0];
      return {
        title: result.raw_content?.title || '',
        content: result.raw_content?.text || '',
        url: result.url
      };
    }
    
    return { error: 'No content extracted' };
  } catch (err) {
    return { error: err.message };
  }
}

/**
 * 生成摘要（简化版，实际应使用 LLM）
 */
function generateSummary(content, minLength, maxLength) {
  if (!content || content.length < minLength) {
    return content || '';
  }
  
  // 简单的摘要逻辑：提取前 maxLength 个字符
  // TODO: 实际应该调用 LLM 生成更智能的摘要
  let summary = content.slice(0, maxLength);
  
  // 尝试在句号处截断
  const lastPeriod = summary.lastIndexOf('。');
  const lastQuestion = summary.lastIndexOf('？');
  const lastExclamation = summary.lastIndexOf('！');
  const lastSentenceEnd = Math.max(lastPeriod, lastQuestion, lastExclamation);
  
  if (lastSentenceEnd > minLength * 0.7) {
    summary = summary.slice(0, lastSentenceEnd + 1);
  }
  
  return summary;
}

/**
 * 主函数
 */
async function main() {
  const urls = values.urls 
    ? values.urls.split(',').map(u => u.trim()).filter(u => u)
    : positionals;
  
  if (urls.length === 0) {
    console.error('❌ 请提供 URL');
    process.exit(1);
  }
  
  const minLength = parseInt(values.minLength) || 60;
  const maxLength = parseInt(values.maxLength) || 200;
  
  const results = [];
  
  for (const url of urls) {
    console.error(`📄 提取: ${url}`);
    
    const extracted = await extractContent(url);
    
    if (extracted.error) {
      console.error(`   ❌ ${extracted.error}`);
      results.push({
        url,
        error: extracted.error,
        summary: ''
      });
    } else {
      const summary = generateSummary(extracted.content, minLength, maxLength);
      console.error(`   ✅ 摘要长度: ${summary.length}字`);
      
      results.push({
        url,
        title: extracted.title,
        summary,
        contentLength: extracted.content.length
      });
    }
  }
  
  console.log(JSON.stringify(results, null, 2));
}

main().catch(err => {
  console.error('❌ 错误:', err.message);
  process.exit(1);
});
