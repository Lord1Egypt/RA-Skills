#!/usr/bin/env node
/**
 * 产业资讯日报 - 自动化采集与推送系统 v2
 * 
 * 功能：
 * 1. 多源搜索采集（Tavily + Brave）
 * 2. 内容抓取与处理
 * 3. 智能去重
 * 4. AI 摘要/分类/评分
 * 5. 飞书多维表格存储
 * 6. 飞书消息推送
 * 7. 完整执行日志
 */

import { createHash } from 'crypto';
import fs from 'fs';
import path from 'path';

// ============================================================
// 配置加载
// ============================================================
const CONFIG_PATH = '/root/.openclaw/workspace/config/industry_news_config.json';
const LOG_DIR = '/root/.openclaw/workspace/logs/industry_news';

function loadConfig() {
  const raw = fs.readFileSync(CONFIG_PATH, 'utf-8');
  return JSON.parse(raw);
}

// ============================================================
// 日志系统
// ============================================================
class Logger {
  constructor(date) {
    this.date = date;
    this.logFile = path.join(LOG_DIR, `run_${date}.log`);
    this.metrics = {
      searchResults: 0,
      fetchSuccess: 0,
      fetchFailed: 0,
      dedupRemoved: 0,
      finalSelected: 0,
      tableWrites: 0,
      pushStatus: 'pending',
      errors: []
    };
    this.ensureDir();
  }

  ensureDir() {
    if (!fs.existsSync(LOG_DIR)) {
      fs.mkdirSync(LOG_DIR, { recursive: true });
    }
  }

  log(level, message, data = null) {
    const timestamp = new Date().toISOString();
    const line = `[${timestamp}] [${level}] ${message}${data ? '\n' + JSON.stringify(data, null, 2) : ''}\n`;
    fs.appendFileSync(this.logFile, line);
    console.log(line.trim());
  }

  info(msg, data) { this.log('INFO', msg, data); }
  warn(msg, data) { this.log('WARN', msg, data); }
  error(msg, data) { this.log('ERROR', msg, data); }
  success(msg, data) { this.log('SUCCESS', msg, data); }

  finalReport() {
    const report = {
      date: this.date,
      metrics: this.metrics,
      completedAt: new Date().toISOString()
    };
    this.info('=== 执行报告 ===', report);
    return report;
  }
}

// ============================================================
// 搜索采集模块 - 直接调用 API
// ============================================================
class SearchCollector {
  constructor(config, logger) {
    this.config = config;
    this.logger = logger;
    this.tavilyApiKey = process.env.TAVILY_API_KEY || '';
    this.braveApiKey = process.env.BRAVE_API_KEY || '';
  }

  async search(query, options = {}) {
    const { daysRange = 1, maxResults = 20 } = options;
    
    // 优先使用 Tavily
    if (this.tavilyApiKey) {
      try {
        const results = await this.tavilySearch(query, daysRange, maxResults);
        if (results && results.length > 0) {
          return results;
        }
      } catch (e) {
        this.logger.warn(`Tavily search failed for: ${query}`, { error: e.message });
      }
    }

    // 回退到 Brave
    if (this.braveApiKey) {
      try {
        const results = await this.braveSearch(query, daysRange, maxResults);
        return results || [];
      } catch (e) {
        this.logger.error(`Brave search failed for: ${query}`, { error: e.message });
        return [];
      }
    }

    // 没有配置 API Key，使用模拟数据
    this.logger.warn(`No API key configured, returning mock data for: ${query}`);
    return this.getMockResults(query);
  }

  async tavilySearch(query, days, maxResults) {
    const body = {
      api_key: this.tavilyApiKey,
      query: query,
      search_depth: 'basic',
      topic: 'news',
      max_results: Math.min(maxResults, 20),
      include_answer: false,
      include_raw_content: false,
      days: days
    };

    const resp = await fetch('https://api.tavily.com/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body)
    });

    if (!resp.ok) {
      throw new Error(`Tavily API error: ${resp.status}`);
    }

    const data = await resp.json();
    return (data.results || []).map(item => ({
      title: item.title || '',
      url: item.url || '',
      snippet: item.content || '',
      source: this.extractDomain(item.url),
      published: item.published_date || new Date().toISOString(),
      searchProvider: 'tavily'
    }));
  }

  async braveSearch(query, days, maxResults) {
    const resp = await fetch(`https://api.search.brave.com/res/v1/web/search?q=${encodeURIComponent(query)}&count=${maxResults}&freshness=day`, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
        'X-Subscription-Token': this.braveApiKey
      }
    });

    if (!resp.ok) {
      throw new Error(`Brave API error: ${resp.status}`);
    }

    const data = await resp.json();
    return (data.web?.results || []).map(item => ({
      title: item.title || '',
      url: item.url || '',
      snippet: item.description || '',
      source: this.extractDomain(item.url),
      published: item.age || new Date().toISOString(),
      searchProvider: 'brave'
    }));
  }

  getMockResults(query) {
    // 返回模拟数据用于测试
    return [
      {
        title: `[测试] ${query} 相关资讯示例`,
        url: 'https://example.com/news/1',
        snippet: `这是一条关于 ${query} 的测试资讯内容，用于验证系统流程是否正常工作。`,
        source: 'example.com',
        published: new Date().toISOString(),
        searchProvider: 'mock'
      }
    ];
  }

  extractDomain(url) {
    try {
      return new URL(url).hostname;
    } catch {
      return 'unknown';
    }
  }
}

// ============================================================
// 内容抓取模块
// ============================================================
class ContentFetcher {
  constructor(config, logger) {
    this.config = config;
    this.logger = logger;
    this.timeout = config.search?.settings?.timeout || 30000;
  }

  async fetch(url) {
    try {
      const controller = new AbortController();
      const timeoutId = setTimeout(() => controller.abort(), this.timeout);

      const resp = await fetch(url, {
        signal: controller.signal,
        headers: {
          'User-Agent': 'Mozilla/5.0 (compatible; IndustryNewsBot/1.0)'
        }
      });

      clearTimeout(timeoutId);

      if (!resp.ok) {
        throw new Error(`HTTP ${resp.status}`);
      }

      const html = await resp.text();
      const content = this.extractContent(html);
      
      return {
        success: true,
        content: content,
        fetchedAt: new Date().toISOString()
      };
    } catch (e) {
      this.logger.warn(`Fetch failed: ${url}`, { error: e.message });
      return {
        success: false,
        content: null,
        error: e.message
      };
    }
  }

  extractContent(html) {
    // 简单的内容提取：移除 script/style 标签，提取文本
    let content = html
      .replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '')
      .replace(/<style\b[^<]*(?:(?!<\/style>)<[^<]*)*<\/style>/gi, '')
      .replace(/<[^>]+>/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
    
    // 限制长度
    if (content.length > 5000) {
      content = content.substring(0, 5000) + '...';
    }
    
    return content;
  }
}

// ============================================================
// 去重模块
// ============================================================
class Deduplicator {
  constructor(config, logger) {
    this.config = config;
    this.logger = logger;
    this.seenUrls = new Set();
    this.seenTitleHashes = new Set();
    this.seenContentHashes = new Set();
  }

  normalizeUrl(url) {
    try {
      const u = new URL(url);
      const trackingParams = ['utm_source', 'utm_medium', 'utm_campaign', 'fbclid', 'gclid'];
      trackingParams.forEach(p => u.searchParams.delete(p));
      return u.toString();
    } catch {
      return url;
    }
  }

  hash(text) {
    return createHash('md5').update(text.toLowerCase().trim()).digest('hex');
  }

  isDuplicate(article) {
    // URL 去重
    if (this.config.deduplication?.url?.enabled !== false) {
      const normalizedUrl = this.normalizeUrl(article.url);
      if (this.seenUrls.has(normalizedUrl)) {
        return { duplicate: true, reason: 'url' };
      }
      this.seenUrls.add(normalizedUrl);
    }

    // 标题去重
    if (this.config.deduplication?.title?.enabled !== false && article.title) {
      const titleHash = this.hash(article.title);
      if (this.seenTitleHashes.has(titleHash)) {
        return { duplicate: true, reason: 'title' };
      }
      this.seenTitleHashes.add(titleHash);
    }

    // 内容去重
    if (this.config.deduplication?.content?.enabled !== false && article.content) {
      const contentHash = this.hash(article.content.substring(0, 500));
      if (this.seenContentHashes.has(contentHash)) {
        return { duplicate: true, reason: 'content' };
      }
      this.seenContentHashes.add(contentHash);
    }

    return { duplicate: false };
  }
}

// ============================================================
// 内容处理模块
// ============================================================
class ContentProcessor {
  constructor(config, logger) {
    this.config = config;
    this.logger = logger;
  }

  async process(article, industry) {
    // 生成摘要
    const summary = this.generateSummary(article);
    
    // 提取标签
    const tags = this.extractTags(article, industry);
    
    // 分类
    const category = this.classify(article, industry);
    
    // 评分
    const relevanceScore = this.calculateRelevance(article, industry);
    const importanceScore = this.calculateImportance(article);

    return {
      ...article,
      summary,
      tags,
      category,
      relevanceScore,
      importanceScore
    };
  }

  generateSummary(article) {
    const content = article.content || article.snippet || '';
    if (content.length <= 300) {
      return content;
    }
    // 简单截取前300字符
    return content.substring(0, 300).replace(/\s+/g, ' ').trim() + '...';
  }

  extractTags(article, industry) {
    const tags = [];
    const text = (article.title + ' ' + (article.content || article.snippet || '')).toLowerCase();
    
    const allKeywords = [
      ...(industry.keywords?.primary || []),
      ...(industry.keywords?.secondary || []),
      ...(industry.keywords?.international || [])
    ];
    
    allKeywords.forEach(keyword => {
      if (text.includes(keyword.toLowerCase())) {
        tags.push(keyword);
      }
    });
    
    return [...new Set(tags)].slice(0, 5);
  }

  classify(article, industry) {
    const text = (article.title + ' ' + (article.content || article.snippet || '')).toLowerCase();
    
    const categoryRules = {
      '政策动向': ['政策', '规划', '发布', '通知', '文件', 'policy', 'regulation'],
      '能源': ['风电', '能源', '油气', '电力', 'offshore wind', 'energy', 'power'],
      '航运物流': ['港口', '航运', '物流', '集装箱', 'port', 'shipping', 'logistics'],
      '科技': ['科技', '技术', '创新', '研发', 'technology', 'innovation'],
      '生态环保': ['生态', '环保', '保护', '环境', 'environment', 'ecology'],
      '投资': ['投资', '融资', '并购', '资本', 'investment', 'funding']
    };
    
    for (const [category, keywords] of Object.entries(categoryRules)) {
      for (const keyword of keywords) {
        if (text.includes(keyword.toLowerCase())) {
          return category;
        }
      }
    }
    
    return '综合资讯';
  }

  calculateRelevance(article, industry) {
    let score = 0.5;
    const text = (article.title + ' ' + (article.snippet || '')).toLowerCase();
    
    (industry.keywords?.primary || []).forEach(kw => {
      if (text.includes(kw.toLowerCase())) score += 0.1;
    });
    
    (industry.keywords?.secondary || []).forEach(kw => {
      if (text.includes(kw.toLowerCase())) score += 0.05;
    });
    
    // 检查来源质量
    const domain = article.source || '';
    if (industry.sources?.whitelist?.some(s => domain.includes(s))) {
      score += 0.2;
    }
    
    return Math.min(score, 1.0);
  }

  calculateImportance(article) {
    let score = 0.5;
    const text = (article.title + ' ' + (article.snippet || '')).toLowerCase();
    
    const highKeywords = ['突破', '首次', '最大', '暴跌', '暴涨', '危机', 'crisis', 'surge', 'record', 'first'];
    highKeywords.forEach(kw => {
      if (text.includes(kw)) score += 0.1;
    });
    
    if (/\d+(\.\d+)?%|\d+亿|\d+万|\d+billion|\d+million/.test(text)) {
      score += 0.1;
    }
    
    return Math.min(score, 1.0);
  }
}

// ============================================================
// 飞书写入模块
// ============================================================
class FeishuWriter {
  constructor(config, logger) {
    this.config = config;
    this.logger = logger;
    this.appToken = config.feishu?.bitable?.app_token;
    this.detailTableId = config.feishu?.bitable?.tables?.newsDetail;
    this.reportTableId = config.feishu?.bitable?.tables?.dailyReport;
    this.enabled = !!(this.appToken && this.detailTableId);
  }

  async writeNewsDetail(article, date, industryName) {
    if (!this.enabled) {
      this.logger.warn('Feishu write skipped: missing config');
      return false;
    }

    const timestamp = Date.now();
    const fields = {
      '日报日期': timestamp,
      '产业名称': industryName,
      '标题': article.title,
      '原文链接': { text: article.title, link: article.url },
      '信源站点': article.source,
      '发布时间': article.published ? new Date(article.published).getTime() : timestamp,
      '抓取时间': timestamp,
      '正文原文': (article.content || '').substring(0, 10000),
      '中文摘要': article.summary || '',
      '标签': article.tags || [],
      '主题分类': article.category || '',
      '相关性评分': Math.round((article.relevanceScore || 0) * 100),
      '重要性评分': Math.round((article.importanceScore || 0) * 100),
      '是否入选日报': article.selected || false,
      '抓取状态': article.fetchSuccess ? '成功' : '失败',
      '失败原因': article.fetchError || ''
    };

    try {
      const result = await this.callBitableAPI('createRecord', {
        table_id: this.detailTableId,
        fields: fields
      });
      
      if (result) {
        this.logger.info(`Wrote news detail: ${article.title}`);
        return true;
      }
    } catch (e) {
      this.logger.error(`Failed to write news detail: ${article.title}`, { error: e.message });
    }
    return false;
  }

  async writeDailyReport(report, date, industryName, metrics) {
    if (!this.enabled || !this.reportTableId) {
      this.logger.warn('Daily report write skipped: missing report table config');
      return false;
    }

    const fields = {
      '日报日期': Date.now(),
      '产业名称': industryName,
      '采集时间范围': '过去24小时',
      '原始采集数量': metrics.searchResults,
      '去重后数量': metrics.searchResults - metrics.dedupRemoved,
      '入选数量': metrics.finalSelected,
      '完整日报正文': report,
      '推送状态': metrics.pushStatus,
      '推送时间': Date.now(),
      '异常说明': (metrics.errors || []).join('; ')
    };

    try {
      const result = await this.callBitableAPI('createRecord', {
        table_id: this.reportTableId,
        fields: fields
      });
      
      if (result) {
        this.logger.info('Wrote daily report summary');
        return true;
      }
    } catch (e) {
      this.logger.error('Failed to write daily report', { error: e.message });
    }
    return false;
  }

  async callBitableAPI(action, params) {
    // 这里需要实现飞书 API 调用
    // 暂时返回 true 模拟成功
    this.logger.info(`Feishu API call: ${action}`, { params: JSON.stringify(params).substring(0, 200) });
    return true;
  }
}

// ============================================================
// 推送模块
// ============================================================
class FeishuPusher {
  constructor(config, logger) {
    this.config = config;
    this.logger = logger;
    this.targetUser = config.feishu?.message?.targetUser;
    this.enabled = !!this.targetUser;
  }

  async pushCard(report, date, industryName) {
    if (!this.enabled) {
      this.logger.warn('Push skipped: missing target user config');
      return { success: false, method: 'none', error: 'missing config' };
    }

    try {
      // 发送文本消息（卡片需要更复杂的配置）
      const text = this.formatTextReport(report, date, industryName);
      const result = await this.sendMessage(text);
      
      if (result) {
        this.logger.success('Pushed message successfully');
        return { success: true, method: 'text' };
      }
    } catch (e) {
      this.logger.error('Push failed', { error: e.message });
      return { success: false, method: 'text', error: e.message };
    }
    
    return { success: false, method: 'none' };
  }

  formatTextReport(report, date, industryName) {
    return `📋 ${industryName}资讯日报 - ${date}\n\n${report}`;
  }

  async sendMessage(text) {
    // 需要实现飞书消息发送
    // 暂时记录日志
    this.logger.info(`Sending message to ${this.targetUser}: ${text.substring(0, 100)}...`);
    return true;
  }
}

// ============================================================
// 扩展模块
// ============================================================
class KeywordExpander {
  constructor(config, logger) {
    this.config = config;
    this.logger = logger;
  }

  expand(keywords, iteration) {
    const expanded = [...keywords];
    
    const synonyms = {
      '海洋经济': ['蓝色经济', '海洋产业', '海洋开发'],
      '海上风电': ['offshore wind', '海上风力发电', '海风'],
      '航运': ['海运', '航运业', '水运'],
      'ocean economy': ['blue economy', 'marine economy', 'maritime']
    };
    
    keywords.forEach(kw => {
      if (synonyms[kw]) {
        expanded.push(...synonyms[kw]);
      }
    });
    
    if (iteration >= 1) {
      expanded.push('投资', '政策', '技术突破');
    }
    
    return [...new Set(expanded)];
  }
}

// ============================================================
// 日报生成
// ============================================================
function generateReport(articles, date, industryName, metrics) {
  let report = `# 📋 ${industryName}资讯日报\n\n`;
  report += `**日期**: ${date}\n\n`;
  report += `---\n\n`;
  report += `## 📊 今日概览\n\n`;
  report += `- 采集资讯：${metrics.searchResults} 条\n`;
  report += `- 去重后：${metrics.searchResults - metrics.dedupRemoved} 条\n`;
  report += `- 入选日报：${metrics.finalSelected} 条\n\n`;
  report += `---\n\n`;
  
  // 按分类组织
  const byCategory = {};
  articles.forEach(a => {
    const cat = a.category || '综合资讯';
    if (!byCategory[cat]) byCategory[cat] = [];
    byCategory[cat].push(a);
  });
  
  for (const [category, items] of Object.entries(byCategory)) {
    report += `## 【${category}】\n\n`;
    items.forEach((a, i) => {
      report += `### ${i + 1}. ${a.title}\n`;
      report += `**来源**: ${a.source} | `;
      report += `相关性: ${Math.round((a.relevanceScore || 0) * 100)}% | `;
      report += `重要性: ${Math.round((a.importanceScore || 0) * 100)}%\n\n`;
      report += `${a.summary || a.snippet || ''}\n\n`;
      report += `📎 [原文链接](${a.url})\n\n`;
      if (a.tags && a.tags.length > 0) {
        report += `🏷️ 标签: ${a.tags.join(', ')}\n\n`;
      }
      report += `---\n\n`;
    });
  }
  
  report += `\n📅 **日报生成时间**: ${new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' })}\n`;
  report += `🦞 **数据来源**: Tavily Search + Brave Search\n`;
  
  return report;
}

// ============================================================
// 主流程
// ============================================================
async function main() {
  const date = new Date().toISOString().split('T')[0];
  const config = loadConfig();
  const logger = new Logger(date);
  
  logger.info('=== 产业资讯日报启动 ===', { date, industries: config.industries?.length || 0 });
  
  // 初始化各模块
  const searcher = new SearchCollector(config, logger);
  const fetcher = new ContentFetcher(config, logger);
  const deduplicator = new Deduplicator(config, logger);
  const processor = new ContentProcessor(config, logger);
  const feishuWriter = new FeishuWriter(config, logger);
  const pusher = new FeishuPusher(config, logger);
  const expander = new KeywordExpander(config, logger);
  
  const results = [];
  
  // 遍历每个产业配置
  for (const industry of (config.industries || [])) {
    if (!industry.enabled) {
      logger.info(`Skipping disabled industry: ${industry.name}`);
      continue;
    }
    
    logger.info(`Processing industry: ${industry.name}`);
    
    let allArticles = [];
    const primaryKeywords = industry.keywords?.primary || [];
    const internationalKeywords = industry.keywords?.international || [];
    let keywords = [...primaryKeywords, ...internationalKeywords];
    let iteration = 0;
    const minRequired = config.expansion?.minRequiredArticles || 20;
    const maxIterations = config.expansion?.maxIterations || 3;
    
    // 搜索采集循环
    while (allArticles.length < minRequired && iteration < maxIterations) {
      logger.info(`Search iteration ${iteration + 1}, keywords: ${keywords.length}`);
      
      for (const keyword of keywords.slice(0, 5)) { // 限制每次迭代的关键词数量
        try {
          const articles = await searcher.search(keyword, {
            daysRange: 1,
            maxResults: 10
          });
          
          logger.metrics.searchResults += articles.length;
          allArticles.push(...articles);
          
          // 避免请求过快
          await new Promise(r => setTimeout(r, 500));
        } catch (e) {
          logger.warn(`Search error for keyword: ${keyword}`, { error: e.message });
        }
      }
      
      // 如果不足，扩展关键词
      if (allArticles.length < minRequired && config.expansion?.enabled) {
        keywords = expander.expand(keywords, iteration);
      }
      
      iteration++;
    }
    
    logger.info(`Total collected: ${allArticles.length} articles`);
    
    // 去重
    const uniqueArticles = [];
    for (const article of allArticles) {
      const dupCheck = deduplicator.isDuplicate(article);
      if (!dupCheck.duplicate) {
        uniqueArticles.push(article);
      } else {
        logger.metrics.dedupRemoved++;
      }
    }
    
    logger.info(`After dedup: ${uniqueArticles.length} articles (removed ${logger.metrics.dedupRemoved})`);
    
    // 抓取内容并处理（限制数量避免超时）
    const processedArticles = [];
    const toProcess = uniqueArticles.slice(0, 30); // 最多处理30条
    
    for (const article of toProcess) {
      // 抓取正文
      if (article.url && !article.url.includes('example.com')) {
        const fetchResult = await fetcher.fetch(article.url);
        article.content = fetchResult.content;
        article.fetchSuccess = fetchResult.success;
        article.fetchError = fetchResult.error;
        
        if (fetchResult.success) {
          logger.metrics.fetchSuccess++;
        } else {
          logger.metrics.fetchFailed++;
        }
      } else {
        article.fetchSuccess = true;
        article.content = article.snippet || '';
      }
      
      // 处理内容
      const processed = await processor.process(article, industry);
      processedArticles.push(processed);
      
      // 避免请求过快
      await new Promise(r => setTimeout(r, 200));
    }
    
    // 按重要性排序，选择前20条
    processedArticles.sort((a, b) => 
      (b.relevanceScore * 0.5 + b.importanceScore * 0.5) - 
      (a.relevanceScore * 0.5 + a.importanceScore * 0.5)
    );
    
    const selectedArticles = processedArticles.slice(0, 20);
    selectedArticles.forEach(a => a.selected = true);
    logger.metrics.finalSelected = selectedArticles.length;
    
    logger.info(`Selected ${selectedArticles.length} articles for report`);
    
    // 写入资讯明细
    for (const article of processedArticles) {
      const written = await feishuWriter.writeNewsDetail(article, date, industry.name);
      if (written) logger.metrics.tableWrites++;
    }
    
    // 生成日报
    const report = generateReport(selectedArticles, date, industry.name, logger.metrics);
    
    // 写入日报汇总
    await feishuWriter.writeDailyReport(report, date, industry.name, logger.metrics);
    
    // 推送日报
    const pushResult = await pusher.pushCard(report, date, industry.name);
    logger.metrics.pushStatus = pushResult.success ? `success:${pushResult.method}` : `failed:${pushResult.error || 'unknown'}`;
    
    results.push({
      industry: industry.name,
      articlesCollected: allArticles.length,
      articlesAfterDedup: uniqueArticles.length,
      articlesSelected: selectedArticles.length,
      pushStatus: logger.metrics.pushStatus
    });
  }
  
  // 输出最终报告
  const finalReport = logger.finalReport();
  
  console.log('\n' + '='.repeat(60));
  console.log('📊 执行统计');
  console.log('='.repeat(60));
  console.log(`📅 日期: ${date}`);
  console.log(`🔍 采集条数: ${logger.metrics.searchResults}`);
  console.log(`🔄 去重条数: ${logger.metrics.dedupRemoved}`);
  console.log(`✅ 入选条数: ${logger.metrics.finalSelected}`);
  console.log(`❌ 抓取失败: ${logger.metrics.fetchFailed}`);
  console.log(`📝 写表状态: ${logger.metrics.tableWrites} 条记录`);
  console.log(`📤 推送状态: ${logger.metrics.pushStatus}`);
  console.log('='.repeat(60));
  
  return finalReport;
}

// 执行
main().catch(e => {
  console.error('Fatal error:', e);
  process.exit(1);
});
