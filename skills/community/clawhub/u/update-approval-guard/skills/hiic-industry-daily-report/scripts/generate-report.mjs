#!/usr/bin/env node
/**
 * HIIC 产业日报生成器（v7.3 - 三引擎 + 飞书存储 + 优化摘要 + 自动翻译）
 * 
 * 核心功能：
 * 1. 三引擎搜索（Tavily + Brave + tech-news-digest）
 * 2. 严格24小时时效性
 * 3. 至少20条资讯
 * 4. 智能去重
 * 5. 代理支持
 * 6. 自动存储到飞书多维表格
 * 7. 优化摘要质量
 * 8. 自动翻译外网资讯（标题、摘要、正文）
 */

import { parseArgs } from 'util';
import { writeFileSync } from 'fs';
import { ProxyAgent, setGlobalDispatcher } from 'undici';
import { exec } from 'child_process';
import { promisify } from 'util';
const execAsync = promisify(exec);

// ==================== 翻译功能（使用translate-shell）====================

async function translateText(text, sourceLang = 'en', targetLang = 'zh') {
  if (!text || text.trim().length === 0) {
    return text;
  }
  
  // 检测是否已经是中文
  const chineseRatio = (text.match(/[\u4e00-\u9fa5]/g) || []).length / text.length;
  if (chineseRatio > 0.3) {
    return text; // 如果中文占比超过30%，直接返回
  }
  
  try {
    // 使用translate-shell（trans命令）进行翻译
    const { stdout, stderr } = await execAsync(
      `echo '${text.replace(/'/g, "'\"'\"'")}' | trans -b ${sourceLang}:${targetLang}`,
      {
        maxBuffer: 10 * 1024 * 1024, // 10MB buffer
        timeout: 10000 // 10秒超时
      }
    );
    
    const translated = stdout.trim();
    
    if (translated && translated.length > 0) {
      return translated;
    } else {
      return text; // 翻译失败时返回原文
    }
  } catch (error) {
    console.error(`⚠️  翻译失败: ${error.message}`);
    return text; // 翻译失败时返回原文
  }
}

async function translateNewsItem(item, verbose = false) {
  if (verbose) {
    process.stderr.write('   翻译中...');
  }
  
  try {
    // 并行翻译标题、摘要、正文
    const [translatedTitle, translatedSummary, translatedContent] = await Promise.all([
      translateText(item.title),
      translateText(item.summary),
      item.extractedContent ? translateText(item.extractedContent) : Promise.resolve(item.extractedContent)
    ]);
    
    // 清理翻译后的摘要（移除"标题："等噪音）
    const cleanedSummary = translatedSummary
      .replace(/^标题[：:]\s*/i, '')
      .replace(/标题[：:]\s*/i, '')
      .replace(/URL\s*来源[：:]\s*/i, '')
      .replace(/来源[：:]\s*/i, '')
      .replace(/发布时间[：:]\s*/i, '')
      .replace(/时间[：:]\s*/i, '')
      .trim();
    
    if (verbose) {
      process.stderr.write('✅\n');
    }
    
    return {
      ...item,
      title: translatedTitle,
      summary: cleanedSummary,
      extractedContent: translatedContent,
      originalTitle: item.title !== translatedTitle ? item.title : undefined,
      originalSummary: item.summary !== cleanedSummary ? item.summary : undefined
    };
  } catch (error) {
    if (verbose) {
      process.stderr.write('❌\n');
    }
    console.error(`   翻译错误: ${error.message}`);
    return item;
  }
}

const { values } = parseArgs({
  options: {
    keywords: { type: 'string', short: 'k' },
    industry: { type: 'string', short: 'i' },
    maxResults: { type: 'string', short: 'm', default: '30' },
    output: { type: 'string', short: 'o' },
    verbose: { type: 'boolean', short: 'v', default: false },
    proxy: { type: 'string', short: 'p', default: 'http://127.0.0.1:7899' },
    saveToBitable: { type: 'boolean', short: 's', default: true }
  },
  allowPositionals: true
});

const TAVILY_API_KEY = process.env.TAVILY_API_KEY;
const BRAVE_API_KEY = process.env.BRAVE_API_KEY;

// 配置代理
if (values.proxy && values.proxy !== 'none') {
  try {
    const proxyAgent = new ProxyAgent(values.proxy);
    setGlobalDispatcher(proxyAgent);
    if (values.verbose) {
      console.error(`🌐 代理已启用: ${values.proxy}\n`);
    }
  } catch (err) {
    if (values.verbose) {
      console.error(`⚠️  代理配置失败: ${err.message}\n`);
    }
  }
}

// ==================== 时间验证 ====================

function isWithin24Hours(dateStr) {
  if (!dateStr) return false;
  try {
    const date = new Date(dateStr);
    if (isNaN(date.getTime())) return false;
    const now = new Date();
    const hours24 = 24 * 60 * 60 * 1000;
    return (now - date) <= hours24 && (now - date) >= 0;
  } catch {
    return false;
  }
}

function formatRelativeTime(dateStr) {
  if (!dateStr) return '';
  try {
    const date = new Date(dateStr);
    if (isNaN(date.getTime())) return '';
    const now = new Date();
    const diffMs = now - date;
    const hours = Math.floor(diffMs / (60 * 60 * 1000));
    const minutes = Math.floor(diffMs / (60 * 1000));
    
    if (minutes < 60) return `${minutes}分钟前`;
    if (hours < 24) return `${hours}小时前`;
    return '';
  } catch {
    return '';
  }
}

function dateToTimestamp(dateStr) {
  if (!dateStr) return null;
  try {
    const date = new Date(dateStr);
    if (isNaN(date.getTime())) return null;
    return date.getTime();
  } catch {
    return null;
  }
}

// ==================== tech-news-digest 数据源 ====================

async function fetchFromTechDigest(industry, maxResults) {
  const scriptPath = new URL('./hiic-tech-digest-bridge.py', import.meta.url).pathname;
  
  try {
    const { stdout, stderr } = await execAsync(
      `python3 "${scriptPath}" --industry "${industry}" --hours 24 --max-items ${maxResults}`,
      {
        timeout: 120000,  // 2分钟超时
        maxBuffer: 10 * 1024 * 1024  // 10MB缓冲
      }
    );
    
    const data = JSON.parse(stdout);
    
    if (data.error) {
      if (values.verbose) {
        console.error(`  ⚠️  tech-news-digest 错误: ${data.error}`);
      }
      return [];
    }
    
    const articles = data.articles || [];
    
    // 转换为统一格式
    return articles.map(article => ({
      title: article.title || 'Untitled',
      url: article.url,
      description: article.summary || '',
      publishedDate: article.published_date || '',
      source: article.source_type || 'tech-news-digest',
      qualityScore: article.quality_score || 5
    }));
  } catch (err) {
    if (values.verbose) {
      console.error(`  ⚠️  tech-news-digest 执行失败: ${err.message}`);
    }
    return [];
  }
}

// ==================== 搜索功能（三引擎，全量抓取） ====================

async function searchTavily(query, maxResults) {
  if (!TAVILY_API_KEY) {
    if (values.verbose) console.error(`  ⚠️  Tavily API Key 未配置`);
    return [];
  }
  
  try {
    const response = await fetch('https://api.tavily.com/search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${TAVILY_API_KEY}`
      },
      body: JSON.stringify({
        query,
        max_results: maxResults,
        topic: 'news',
        days: 1
      }),
      signal: AbortSignal.timeout(15000)
    });
    
    if (!response.ok) {
      if (values.verbose) console.error(`  ⚠️  Tavily API 返回 ${response.status}`);
      return [];
    }
    
    const data = await response.json();
    
    // 严格过滤24小时
    const filtered = (data.results || []).filter(item => {
      if (!item.published_date) return false;
      return isWithin24Hours(item.published_date);
    });
    
    return filtered.map(item => ({
      title: item.title || 'Untitled',
      url: item.url,
      description: item.content || '',
      publishedDate: item.published_date,
      source: 'tavily'
    }));
  } catch (err) {
    if (values.verbose) console.error(`  ⚠️  Tavily 错误: ${err.message}`);
    return [];
  }
}

async function searchBrave(query, maxResults) {
  if (!BRAVE_API_KEY) {
    if (values.verbose) console.error(`  ⚠️  Brave API Key 未配置`);
    return [];
  }
  
  try {
    const url = new URL('https://api.search.brave.com/res/v1/web/search');
    url.searchParams.set('q', query);
    url.searchParams.set('count', String(maxResults));
    url.searchParams.set('freshness', 'pd');
    
    const response = await fetch(url.toString(), {
      headers: {
        'Accept': 'application/json',
        'X-Subscription-Token': BRAVE_API_KEY
      },
      signal: AbortSignal.timeout(15000)
    });
    
    if (!response.ok) {
      if (values.verbose) {
        console.error(`  ⚠️  Brave API 返回 ${response.status}`);
      }
      return [];
    }
    
    const data = await response.json();
    
    // 严格过滤24小时
    const filtered = (data.web?.results || []).filter(item => {
      if (!item.published && !item.page_age) return false;
      const dateStr = item.published || item.page_age;
      return isWithin24Hours(dateStr);
    });
    
    return filtered.map(item => ({
      title: item.title || 'Untitled',
      url: item.url,
      description: item.description || '',
      publishedDate: item.published || item.page_age,
      source: 'brave'
    }));
  } catch (err) {
    if (values.verbose) console.error(`  ⚠️  Brave 错误: ${err.message}`);
    return [];
  }
}

// ==================== 内容提取 ====================

async function extractWithJina(url) {
  try {
    const response = await fetch(`https://r.jina.ai/${url}`, {
      headers: { 'Accept': 'text/plain' },
      signal: AbortSignal.timeout(10000)
    });
    
    if (!response.ok) return null;
    
    const content = await response.text();
    
    if (content && content.length > 100 && !content.includes('Error')) {
      return content;
    }
    
    return null;
  } catch {
    return null;
  }
}

async function extractWithFetch(url) {
  try {
    const response = await fetch(url, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (compatible; HIIC-Bot/1.0)',
        'Accept': 'text/html'
      },
      signal: AbortSignal.timeout(10000)
    });
    
    if (!response.ok) return null;
    
    const html = await response.text();
    
    const text = html
      .replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '')
      .replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '')
      .replace(/<[^>]+>/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
    
    if (text && text.length > 200) return text;
    
    return null;
  } catch {
    return null;
  }
}

async function extractContent(url, verbose = false) {
  if (verbose) process.stderr.write('   提取中...');
  
  let content = await extractWithJina(url);
  if (content && content.length > 100) {
    if (verbose) process.stderr.write('✅\n');
    return { content, method: 'jina' };
  }
  
  content = await extractWithFetch(url);
  if (content) {
    if (verbose) process.stderr.write('✅\n');
    return { content, method: 'fetch' };
  }
  
  if (verbose) process.stderr.write('❌\n');
  return null;
}

// ==================== 标题和摘要优化 ====================

function optimizeTitle(originalTitle) {
  let title = originalTitle
    .replace(/^Title:\s*/i, '')
    .replace(/^[\s\-\s]+/, '')
    .trim();
  
  // 移除网站名称
  title = title
    .replace(/\s*[-|–—]\s*[^-|–—]+$/, '')  // 移除 " - 网站名"
    .replace(/\s*\|[^|]+$/, '')  // 移除 " | 网站名"
    .trim();
  
  if (title.length > 70) {
    const punctuations = ['。', '：', '、', ' ', '|'];
    for (const punct of punctuations) {
      const idx = title.indexOf(punct);
      if (idx > 20 && idx < 70) {
        title = title.slice(0, idx);
        break;
      }
    }
    
    if (title.length > 70) {
      title = title.slice(0, 70) + '...';
    }
  }
  
  return title;
}

function cleanSummary(text) {
  if (!text) return '';
  
  // 第一步：移除明显的噪音模式
  let cleaned = text
    // 移除 Markdown 标记
    .replace(/#{1,6}\s*/g, '')
    .replace(/\*\*?([^*]+)\*\*?/g, '$1')
    // 移除 Markdown 链接但保留文本
    .replace(/\[([^\]]+)\]\([^)]+\)/gi, '$1')
    // 移除空的链接
    .replace(/\[\]\([^)]+\)/gi, '')
    // 移除HTML标签
    .replace(/<[^>]+>/g, '')
    // 移除图片标记
    .replace(/!\[Image[^\]]*\]/gi, '')
    // 移除特殊HTML实体
    .replace(/&amp;/g, '&')
    .replace(/&nbsp;/g, ' ')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"');
  
  // 第二步：移除常见网站导航和元数据
  cleaned = cleaned
    .replace(/Markdown Content:\s*/gi, '')
    .replace(/Title Content:\s*/gi, '')
    .replace(/标题：\s*/gi, '')
    .replace(/标题\s*:\s*/gi, '')
    .replace(/URL\s*来源：\s*/gi, '')
    .replace(/来源：\s*/gi, '')
    .replace(/发布时间：\s*/gi, '')
    .replace(/时间：\s*/gi, '')
    .replace(/Continue to Site/gi, '')
    .replace(/Continue Reading/gi, '')
    .replace(/Read More/gi, '')
    .replace(/News Events/gi, '')
    .replace(/Latest News/gi, '')
    .replace(/TNW Conference[^.]*/gi, '')
    .replace(/The Robot Report/gi, '')
    .replace(/Skip to (primary |secondary |main )?(content|navigation)/gi, '')
    .replace(/Skip Navigation/gi, '')
    .replace(/Toggle Navigation/gi, '')
    .replace(/Primary Menu/gi, '')
    .replace(/Main Menu/gi, '')
    .replace(/网址来源：\s*/gi, '')
    .replace(/https?:\/\/[^\s]+/gi, '');
  
  // 第三步：移除特殊字符和多余标点
  cleaned = cleaned
    .replace(/[\u200B-\u200D\uFEFF]/g, '')
    .replace(/\.{4,}/g, '...')
    .replace(/\*{2,}/g, '')
    .replace(/#{2,}/g, '')
    .replace(/={2,}/g, '')
    .replace(/\s+/g, ' ')
    .trim();
  
  return cleaned;
}

async function generateSummaryWithAI(content, title, originalDesc, verbose = false) {
  const minLength = 50;
  const maxLength = 200;
  
  // 优先使用提取的网页内容，其次是搜索结果描述
  let sourceText = content || originalDesc;
  
  if (!sourceText || sourceText.trim().length === 0) {
    return `这是一篇关于${title}的资讯文章。具体内容请阅读全文了解详情。`;
  }
  
  // 清理内容
  sourceText = cleanSummary(sourceText);
  
  // 移除标题重复部分
  const titleWords = title.split(/\s+/).filter(w => w.length > 3);
  for (const word of titleWords.slice(0, 3)) {
    if (sourceText.startsWith(word)) {
      sourceText = sourceText.slice(word.length).trim();
    }
  }
  
  // 如果内容过短，直接返回
  if (sourceText.length < 20) {
    return sourceText;
  }
  
  // 分句并过滤
  const allSentences = sourceText.split(/[。！？.!?]+/).map(s => s.trim()).filter(s => {
    return s.length > 10 && 
           !s.match(/^(Image |图 \d+:|This copy|Skip to|Continue|Read More|标题：|标题|URL 来源|来源|发布时间|时间)/i) &&
           !s.match(/^(根据|Based on).*?(内容|content)/i) &&
           !s.match(/^(https?:|www\.)/i) &&
           !s.match(/^(Skip Navigation|Toggle|Menu|Search|Subscribe)/i);
  });
  
  if (allSentences.length === 0) {
    return sourceText.slice(0, maxLength);
  }
  
  // 评估句子重要性
  function scoreSentence(sentence) {
    let score = 0;
    
    // 包含关键数字（金额、百分比、数量）
    const numbers = sentence.match(/\d+[\.,\d]*\s*[%$€¥万亿亿]?/g) || [];
    score += numbers.length * 15;
    
    // 包含时间信息
    if (sentence.match(/\d{4}年|\d{1,2}月|\d{1,2}日|today|yesterday|本周|本月|最近|周一|周二|周三|周四|周五|周六|周日/i)) {
      score += 10;
    }
    
    // 包含机构/企业名称
    if (sentence.match(/[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+/g)) {
      score += 8;
    }
    
    // 包含关键动词（动作）
    if (sentence.match(/宣布|发布|收购|投资|合作|推出|突破|完成|获得|增长|下跌|上涨|批准|签署|达成|警告|会议|讨论/i)) {
      score += 12;
    }
    
    // 包含影响性词汇
    if (sentence.match(/影响|重要|首次|最大|最新|关键|核心|领先|突破|创|纪录|灾难|中断|供应/i)) {
      score += 10;
    }
    
    // 包含行业关键词
    if (sentence.match(/芯片|半导体|制造|技术|研发|市场|产业|公司|企业|石油|天然气|原油|油轮|海峡|OPEC/i)) {
      score += 8;
    }
    
    // 避免过短的句子
    if (sentence.length < 20) {
      score -= 15;
    }
    
    // 避免纯描述性句子
    if (sentence.match(/^(This|The|These|Those)\s+(is|are|was|were|copy|image|article)/i)) {
      score -= 30;
    }
    
    // 避免包含URL的句子
    if (sentence.match(/https?:\/\//)) {
      score -= 25;
    }
    
    // 避免包含"标题："等噪音
    if (sentence.match(/标题|URL|来源|发布时间|Skip Navigation/i)) {
      score -= 20;
    }
    
    return Math.max(0, score);
  }
  
  // 对句子评分
  const scoredSentences = allSentences.map((sentence, index) => ({
    text: sentence,
    score: scoreSentence(sentence),
    index: index
  }));
  
  // 按评分排序（降序）
  scoredSentences.sort((a, b) => b.score - a.score);
  
  // 选择最重要的句子，组合成摘要
  let summary = '';
  const selectedIndices = new Set();
  
  for (const item of scoredSentences) {
    if (summary.length + item.text.length > maxLength - 20) break;
    if (summary.length >= minLength && selectedIndices.size >= 3) break;
    
    summary += (summary ? '。' : '') + item.text;
    selectedIndices.add(item.index);
  }
  
  // 如果摘要太短，补充更多句子
  if (summary.length < minLength) {
    // 按原文顺序添加更多句子
    for (let i = 0; i < allSentences.length; i++) {
      if (selectedIndices.has(i)) continue;
      if (summary.length + allSentences[i].length > maxLength) break;
      
      summary += '。' + allSentences[i];
      selectedIndices.add(i);
      
      if (summary.length >= minLength) break;
    }
  }
  
  // 如果还是太短，直接截取原文
  if (summary.length < minLength) {
    summary = sourceText.slice(0, maxLength);
  }
  
  // 清理摘要
  summary = summary
    .replace(/^标题：.*?(\n|$)/gi, '')
    .replace(/标题：.*?(\n|$)/gi, '')
    .replace(/标题\s*:\s*.*?(\n|$)/gi, '')
    .replace(/URL\s*来源：.*?(\n|$)/gi, '')
    .replace(/来源：.*?(\n|$)/gi, '')
    .replace(/发布时间：.*?(\n|$)/gi, '')
    .replace(/时间：.*?(\n|$)/gi, '')
    .replace(/视频播放量.*$/, '')
    .replace(/弹幕量.*$/, '')
    .replace(/点赞数.*$/, '')
    .replace(/投硬币.*$/, '')
    .replace(/收藏人数.*$/, '')
    .replace(/转发人数.*$/, '')
    .replace(/作者简介.*$/, '')
    .replace(/, 相关视频.*$/, '')
    .trim();
  
  // 确保摘要以句号结尾
  if (!summary.match(/[。！？.!?]$/)) {
    summary += '。';
  }
  
  return summary.slice(0, maxLength);
}

// ==================== 提取真实来源 ====================

function extractSource(url) {
  try {
    const parsed = new URL(url);
    let domain = parsed.hostname.replace(/^www\./, '');
    
    const siteNameMap = {
      'reuters.com': '路透社',
      'bloomberg.com': '彭博社',
      'cnbc.com': 'CNBC',
      'wsj.com': '华尔街日报',
      'forbes.com': '福布斯',
      'worldoil.com': 'World Oil',
      'oilprice.com': 'OilPrice',
      'people.com.cn': '人民网',
      'xinhuanet.com': '新华网',
      'chinanews.com.cn': '中国新闻网',
      'ce.cn': '中国经济网',
      'caixin.com': '财新网',
      'yicai.com': '第一财经',
      'thepaper.cn': '澎湃新闻',
      'jiemian.com': '界面新闻',
      'sina.com.cn': '新浪',
      'sohu.com': '搜狐',
      '163.com': '网易',
      'qq.com': '腾讯',
      'eastmoney.com': '东方财富'
    };
    
    if (siteNameMap[domain]) return siteNameMap[domain];
    
    for (const [key, name] of Object.entries(siteNameMap)) {
      if (domain.includes(key) || key.includes(domain)) {
        return name;
      }
    }
    
    domain = domain.replace(/^(m\.|wap\.|mobile\.)/, '');
    return domain.charAt(0).toUpperCase() + domain.slice(1);
  } catch {
    return '网络来源';
  }
}

// ==================== URL处理 ====================

function normalizeUrl(url) {
  try {
    const parsed = new URL(url);
    ['utm_source', 'utm_medium', 'utm_campaign', 'ref', 'from', 'fbclid'].forEach(p => {
      parsed.searchParams.delete(p);
    });
    let path = parsed.pathname;
    if (path.endsWith('/') && path.length > 1) path = path.slice(0, -1);
    parsed.pathname = path;
    return parsed.toString().toLowerCase();
  } catch {
    return url.toLowerCase();
  }
}

function mergeAndDeduplicate(results, maxResults) {
  const seen = new Map();
  const deduped = [];
  
  for (const result of results) {
    const normalizedUrl = normalizeUrl(result.url);
    
    let isDuplicate = false;
    for (const [existingUrl] of seen) {
      if (existingUrl === normalizedUrl) {
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

// ==================== 飞书多维表格存储 ====================

import { saveRecordsToBitable } from './feishu-bitable-saver.mjs';

async function saveToBitable(records, industry) {
  if (!values.saveToBitable) {
    if (values.verbose) {
      console.error('\n⚠️  跳过飞书存储（--saveToBitable=false）\n');
    }
    return { success: true, stats: { saved: 0, skipped: records.length } };
  }
  
  // 调用真实的飞书API存储
  return await saveRecordsToBitable(records, industry, values.verbose);
}

// ==================== 主函数 ====================

async function main() {
  // 确定产业和关键词
  let industry = values.industry || '自定义';
  let keywords = [];
  
  if (values.keywords) {
    keywords = values.keywords.split(/[,，]/).map(k => k.trim()).filter(k => k);
  } else if (values.industry) {
    // 这里可以加载产业配置
    keywords = [values.industry];
  } else {
    console.error('❌ 请提供关键词或产业名称');
    console.error('用法: node scripts/generate-report-v7.3.mjs --keywords "关键词1,关键词2" --industry "产业名"');
    console.error('');
    console.error('选项:');
    console.error('  --keywords, -k    搜索关键词（逗号分隔）');
    console.error('  --industry, -i    产业名称');
    console.error('  --maxResults, -m  最大结果数（默认30）');
    console.error('  --output, -o      输出文件路径');
    console.error('  --verbose, -v     显示详细日志');
    console.error('  --proxy, -p       代理服务器（默认 http://127.0.0.1:7899）');
    console.error('  --saveToBitable, -s  存储到飞书多维表格（默认 true）');
    process.exit(1);
  }
  
  if (values.verbose) {
    console.error('📰 HIIC 产业日报生成器 v7.3（三引擎 + 飞书存储 + 优化摘要）\n');
    console.error(`✅ 产业: ${industry}`);
    console.error(`✅ 关键词: ${keywords.join(', ')}\n`);
    console.error(`📅 时间范围: 严格过去24小时`);
    console.error(`📊 目标数量: 至少${values.maxResults}条`);
    console.error(`🔍 搜索引擎: Tavily + Brave + tech-news-digest`);
    console.error(`🌐 代理: ${values.proxy}`);
    console.error(`💾 飞书存储: ${values.saveToBitable ? '启用' : '禁用'}\n`);
  }
  
  // 执行搜索
  const allResults = [];
  const maxResults = parseInt(values.maxResults) || 30;
  const perKeywordResults = Math.ceil(maxResults / keywords.length);
  
  for (const keyword of keywords) {
    if (values.verbose) console.error(`🔍 搜索: "${keyword}"`);
    
    // 并行搜索三个引擎
    const [tavilyResults, braveResults, techDigestResults] = await Promise.all([
      searchTavily(keyword, perKeywordResults),
      searchBrave(keyword, perKeywordResults),
      fetchFromTechDigest(industry, perKeywordResults)
    ]);
    
    if (values.verbose) {
      console.error(`   Tavily: ${tavilyResults.length}条（24小时内）`);
      console.error(`   Brave: ${braveResults.length}条（24小时内）`);
      console.error(`   tech-news-digest: ${techDigestResults.length}条（24小时内）\n`);
    }
    
    allResults.push(...tavilyResults, ...braveResults, ...techDigestResults);
  }
  
  // 去重
  const uniqueResults = mergeAndDeduplicate(allResults, maxResults);
  
  if (values.verbose) {
    console.error(`📊 合并去重后: ${uniqueResults.length}条资讯（严格24小时内）\n`);
  }
  
  if (uniqueResults.length === 0) {
    console.error('⚠️  未找到过去24小时内的相关资讯');
    console.error('💡 建议：');
    console.error('   1. 检查关键词是否过于特殊');
    console.error('   2. 增加更多关键词');
    console.error('   3. 检查 API 配置');
    console.error('   4. 检查代理服务器是否正常');
    process.exit(0);
  }
  
  // 提取内容并生成摘要
  const enhancedResults = [];
  const extractionStats = { success: 0, failed: 0 };
  
  for (let i = 0; i < uniqueResults.length; i++) {
    const result = uniqueResults[i];
    
    const optimizedTitle = optimizeTitle(result.title);
    
    if (values.verbose) {
      const relTime = result.publishedDate ? formatRelativeTime(result.publishedDate) : '';
      console.error(`📄 [${i + 1}/${uniqueResults.length}] ${optimizedTitle.slice(0, 40)}... ${relTime ? `(${relTime})` : ''}`);
    }
    
    const extracted = await extractContent(result.url, values.verbose);
    
    const source = extractSource(result.url);
    
    const summary = await generateSummaryWithAI(
      extracted?.content || null,
      optimizedTitle,
      result.description,
      values.verbose
    );
    
    // 最终清理摘要（确保没有"标题："等噪音）
    const cleanedSummary = summary
      .replace(/^标题[：:]\s*/i, '')
      .replace(/标题[：:]\s*/i, '')
      .replace(/URL\s*来源[：:]\s*/i, '')
      .replace(/来源[：:]\s*/i, '')
      .replace(/发布时间[：:]\s*/i, '')
      .replace(/时间[：:]\s*/i, '')
      .trim();
    
    enhancedResults.push({
      title: optimizedTitle,
      url: result.url,
      source: source,
      summary: cleanedSummary,
      publishedDate: result.publishedDate,
      relativeTime: result.publishedDate ? formatRelativeTime(result.publishedDate) : '',
      extracted: !!extracted,
      searchEngine: result.source
    });
    
    if (extracted) {
      extractionStats.success++;
    } else {
      extractionStats.failed++;
    }
    
    if ((i + 1) % 3 === 0 && i < uniqueResults.length - 1) {
      await new Promise(resolve => setTimeout(resolve, 100));
    }
  }
  
  if (values.verbose) {
    const successRate = ((uniqueResults.length - extractionStats.failed) / uniqueResults.length * 100).toFixed(1);
    console.error(`\n📊 提取成功率: ${successRate}%`);
    console.error(`   成功: ${extractionStats.success}条`);
    console.error(`   失败: ${extractionStats.failed}条\n`);
  }
  
  // 翻译所有资讯（标题、摘要、正文）
  if (values.verbose) {
    console.error(`🌐 开始翻译资讯（标题、摘要、正文）...\n`);
  }
  
  const translatedResults = [];
  for (let i = 0; i < enhancedResults.length; i++) {
    const result = enhancedResults[i];
    if (values.verbose) {
      process.stderr.write(`📄 [${i + 1}/${enhancedResults.length}] ${result.title.slice(0, 50)}... `);
    }
    const translatedItem = await translateNewsItem(result, values.verbose);
    translatedResults.push(translatedItem);
  }
  
  if (values.verbose) {
    console.error(`\n✅ 翻译完成\n`);
  }
  
  // 存储到飞书多维表格
  const saveResult = await saveToBitable(translatedResults, industry);
  
  // 生成简报（优化格式）
  const now = new Date();
  const dateStr = now.toLocaleDateString('zh-CN', { 
    year: 'numeric', 
    month: 'long', 
    day: 'numeric'
  });
  
  const successRate = ((uniqueResults.length - extractionStats.failed) / uniqueResults.length * 100).toFixed(1);
  
  // 获取产业的 emoji
  const industryEmojis = {
    '人工智能': '🤖',
    '机器人': '🦾',
    '智能机器人': '🦾',
    '新能源': '⚡',
    '智能网联汽车': '🚗',
    '量子信息': '⚛️',
    '生物医药': '🧬',
    '半导体与集成电路': '💡',
    '高端装备与仪器': '⚙️',
    '低空经济与空天': '🛸',
    '新材料': '🔬',
    '高端医疗器械': '🏥',
    '网络与通信': '📡',
    '软件与信息服务': '💻'
  };
  const industryEmoji = industryEmojis[industry] || '📊';
  
  let md = `${industryEmoji} ${industry}产业日报 | ${dateStr}\n\n`;
  md += `📅 今日收录 **${translatedResults.length}条** ${industry}领域最新资讯（过去24小时）\n\n`;
  md += `---\n\n`;
  
  // 分类资讯（简化版：全部作为头条要闻）
  let globalIndex = 1;
  
  for (const item of translatedResults) {
    md += `**${globalIndex}. ${item.title}**\n`;
    md += `*来源：${item.source}`;
    if (item.relativeTime) {
      md += ` | ${item.relativeTime}`;
    }
    md += '*\n\n';
    md += `${item.summary}\n\n`;
    md += `🔗 [阅读全文](${item.url})\n\n`;
    md += `---\n\n`;
    globalIndex++;
  }
  
  md += `<small>由 HIIC Industry Daily Report v7.3 自动生成 | 三引擎搜索 | 严格24小时时效性 | 飞书存储 | ${now.toISOString()}</small>\n`;
  
  // 输出
  if (values.output) {
    writeFileSync(values.output, md, 'utf-8');
    console.log(`✅ 简报已保存到: ${values.output}`);
  } else {
    console.log('\n' + '='.repeat(60) + '\n');
    console.log(md);
    console.log('\n' + '='.repeat(60));
  }
  
  // 输出存储信息
  if (saveResult.success && values.verbose) {
    console.error(`\n✅ 数据已准备存储到飞书多维表格`);
    console.error(`   记录数: ${saveResult.stats.saved}`);
    if (saveResult.outputPath) {
      console.error(`   导出路径: ${saveResult.outputPath}\n`);
    }
  }
}

main().catch(err => {
  console.error('❌ 错误:', err.message);
  if (values.verbose) console.error(err.stack);
  process.exit(1);
});
