#!/usr/bin/env node
/**
 * 内容提取器 - 多方案备份
 * 
 * 方案1: Tavily Extract API
 * 方案2: Web Fetch (Jina Reader)
 * 方案3: 使用搜索结果的描述
 */

import { homedir } from 'os';

const TAVILY_API_KEY = process.env.TAVILY_API_KEY;

/**
 * 方案1: Tavily Extract API
 */
async function extractWithTavily(url) {
  if (!TAVILY_API_KEY) {
    return null;
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
        extract_depth: 'basic',  // 使用 basic 而不是 advanced，更稳定
        include_images: false
      })
    });
    
    if (!response.ok) {
      return null;
    }
    
    const data = await response.json();
    
    if (data.results && data.results.length > 0) {
      const content = data.results[0].raw_content?.text || data.results[0].content;
      if (content && content.length > 100) {
        return content;
      }
    }
    
    return null;
  } catch (err) {
    return null;
  }
}

/**
 * 方案2: Jina Reader API (免费)
 */
async function extractWithJina(url) {
  try {
    const jinaUrl = `https://r.jina.ai/${url}`;
    
    const response = await fetch(jinaUrl, {
      headers: {
        'Accept': 'text/plain'
      }
    });
    
    if (!response.ok) {
      return null;
    }
    
    const content = await response.text();
    
    if (content && content.length > 100) {
      return content;
    }
    
    return null;
  } catch (err) {
    return null;
  }
}

/**
 * 方案3: Web Fetch (作为最后备选)
 */
async function extractWithFetch(url) {
  try {
    const response = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; HIIC-Bot/1.0)',
        'Accept': 'text/html,application/xhtml+xml'
      }
    });
    
    if (!response.ok) {
      return null;
    }
    
    const html = await response.text();
    
    // 简单提取文本（移除 HTML 标签）
    let text = html
      .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
      .replace(/<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>/gi, '')
      .replace(/<[^>]+>/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
    
    if (text && text.length > 100) {
      return text.slice(0, 5000);  // 限制长度
    }
    
    return null;
  } catch (err) {
    return null;
  }
}

/**
 * 智能提取：依次尝试多种方案
 */
export async function extractContent(url, verbose = false) {
  // 方案1: Tavily Extract
  if (verbose) process.stderr.write('   尝试 Tavily Extract...');
  let content = await extractWithTavily(url);
  if (content) {
    if (verbose) process.stderr.write(' ✅\n');
    return { content, method: 'tavily' };
  }
  if (verbose) process.stderr.write(' ❌\n');
  
  // 方案2: Jina Reader
  if (verbose) process.stderr.write('   尝试 Jina Reader...');
  content = await extractWithJina(url);
  if (content) {
    if (verbose) process.stderr.write(' ✅\n');
    return { content, method: 'jina' };
  }
  if (verbose) process.stderr.write(' ❌\n');
  
  // 方案3: Web Fetch
  if (verbose) process.stderr.write('   尝试 Web Fetch...');
  content = await extractWithFetch(url);
  if (content) {
    if (verbose) process.stderr.write(' ✅\n');
    return { content, method: 'fetch' };
  }
  if (verbose) process.stderr.write(' ❌\n');
  
  return null;
}

/**
 * 生成高质量摘要（60-200字）
 */
export function generateSummary(content, title, originalDesc, options = {}) {
  const minLength = options.minLength || 60;
  const maxLength = options.maxLength || 200;
  
  // 如果有完整内容，使用完整内容
  if (content && content.length > 0) {
    return summarizeText(content, minLength, maxLength);
  }
  
  // 如果有原始描述，使用原始描述
  if (originalDesc && originalDesc.length >= minLength) {
    return summarizeText(originalDesc, minLength, maxLength);
  }
  
  // 如果描述太短，尝试扩展
  if (originalDesc && originalDesc.length > 0) {
    let summary = originalDesc;
    
    // 如果有标题，添加标题信息
    if (title && !summary.includes(title.slice(0, 20))) {
      summary = `${title}：${summary}`;
    }
    
    // 如果还是太短，重复关键信息
    if (summary.length < minLength) {
      summary = summary.repeat(Math.ceil(minLength / summary.length)).slice(0, maxLength);
    }
    
    return summary;
  }
  
  return '暂无摘要信息';
}

/**
 * 文本摘要核心逻辑
 */
function summarizeText(text, minLength, maxLength) {
  // 清理文本
  let cleaned = text
    .replace(/\s+/g, ' ')
    .replace(/[\r\n]+/g, ' ')
    .trim();
  
  // 如果文本太短，直接返回
  if (cleaned.length <= maxLength) {
    return cleaned;
  }
  
  // 提取摘要
  let summary = cleaned.slice(0, maxLength);
  
  // 尝试在句号、问号、感叹号处截断
  const punctuations = ['。', '？', '！', '；', '.', '?', '!', ';'];
  let lastPunctuation = -1;
  
  for (const punct of punctuations) {
    const idx = summary.lastIndexOf(punct);
    if (idx > lastPunctuation && idx >= minLength * 0.5) {
      lastPunctuation = idx;
    }
  }
  
  if (lastPunctuation >= minLength * 0.7) {
    summary = summary.slice(0, lastPunctuation + 1);
  } else {
    // 如果没有找到合适的标点，在逗号处截断
    const lastComma = Math.max(
      summary.lastIndexOf('，'),
      summary.lastIndexOf(','),
      summary.lastIndexOf('、')
    );
    
    if (lastComma >= minLength * 0.7) {
      summary = summary.slice(0, lastComma);
    }
    summary = summary.trim() + '...';
  }
  
  return summary;
}

// 命令行测试
if (import.meta.url === `file://${process.argv[1]}`) {
  const url = process.argv[2];
  if (!url) {
    console.error('用法: node content-extractor.mjs <url>');
    process.exit(1);
  }
  
  console.error('📄 提取内容:', url);
  
  const result = await extractContent(url, true);
  
  if (result) {
    console.error(`\n✅ 提取成功 (${result.method})`);
    console.error(`   内容长度: ${result.content.length} 字符\n`);
    
    const summary = generateSummary(result.content, '', '', { minLength: 60, maxLength: 200 });
    console.error('📝 摘要:');
    console.log(summary);
    console.error(`\n   摘要长度: ${summary.length} 字`);
  } else {
    console.error('❌ 所有提取方案均失败');
  }
}
