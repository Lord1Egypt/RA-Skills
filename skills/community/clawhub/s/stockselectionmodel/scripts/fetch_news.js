#!/usr/bin/env node
/**
 * fetch_news.js - AI 行业新闻抓取（双通道）
 *
 * 优先用 Tavily（需 TAVILY_API_KEY），无 key 时自动降级到免费网页抓取。
 * 输出去重、打分、压缩后的 JSON，供 agent 研判。
 *
 * 用法:
 *   node fetch_news.js                          # 自动选择数据源
 *   node fetch_news.js --query "自定义搜索词"
 *   node fetch_news.js --market cn|us|all
 *   node fetch_news.js --source tavily|web      # 强制指定数据源
 */

const TAVILY_ENDPOINT = 'https://api.tavily.com/search';

// ── 免费数据源 URL 列表 ──────────────────────────────────────────────
const FREE_SOURCES = [
  { name: 'Yahoo Finance AI', url: 'https://finance.yahoo.com/topic/artificial-intelligence/' },
  { name: 'Reuters Tech', url: 'https://www.reuters.com/technology/artificial-intelligence/' },
  { name: 'CNBC AI', url: 'https://www.cnbc.com/artificial-intelligence/' },
  { name: 'TechCrunch AI', url: 'https://techcrunch.com/category/artificial-intelligence/' },
  { name: 'The Verge AI', url: 'https://www.theverge.com/ai-artificial-intelligence' },
];

// ── Tavily 搜索查询 ─────────────────────────────────────────────────
const TAVILY_QUERIES = {
  all: [
    'AI artificial intelligence latest news stock market impact today',
    'AI 人工智能 最新消息 股票 今日',
  ],
  cn: [
    'AI 人工智能 A股 最新消息 今日',
    'AI 芯片 算力 大模型 概念股',
  ],
  us: [
    'AI artificial intelligence stock market news today',
    'NVIDIA OpenAI Google AI announcement today',
  ],
};

// ── AI 相关关键词（用于打分和过滤）────────────────────────────────────
const AI_KEYWORDS = [
  'openai', 'nvidia', 'nvda', 'gpu', 'ai chip', 'ai model', 'llm',
  'chatgpt', 'gemini', 'claude', 'copilot', 'sora', 'midjourney',
  'deepseek', 'anthropic', 'meta ai', 'llama', 'mistral',
  'datacenter', 'data center', 'inference', 'training',
  'robot', 'optimus', 'humanoid', 'autonomous', 'self-driving',
  'semiconductor', 'tsmc', 'amd', 'broadcom', 'marvell',
  '人工智能', '大模型', '算力', '芯片', '光模块', '机器人',
  'ai agent', 'agi', 'artificial intelligence',
];

// ── 工具函数 ─────────────────────────────────────────────────────────

function parseArgs(argv) {
  const out = { query: null, market: 'all', maxPerQuery: 5, source: 'auto', help: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--help' || a === '-h') out.help = true;
    else if (a === '--query' || a === '-q') out.query = argv[++i];
    else if (a === '--market' || a === '-m') out.market = argv[++i];
    else if (a === '--max' || a === '-n') out.maxPerQuery = Number(argv[++i]);
    else if (a === '--source' || a === '-s') out.source = argv[++i];
  }
  return out;
}

function scoreArticle(title, content) {
  const text = `${title} ${content}`.toLowerCase();
  let score = 0;
  for (const kw of AI_KEYWORDS) {
    if (text.includes(kw)) score += 1;
  }
  return score;
}

function truncate(str, maxLen = 200) {
  if (!str || str.length <= maxLen) return str || '';
  return str.substring(0, maxLen) + '...';
}

function dedup(results) {
  const seen = new Set();
  return results.filter(r => {
    const key = r.url || r.title;
    if (!key || seen.has(key)) return false;
    seen.add(key);
    return true;
  });
}

// ── Tavily 抓取 ─────────────────────────────────────────────────────

async function fetchViaTavily(queries, maxPerQuery, apiKey) {
  const allResults = [];
  for (const q of queries) {
    try {
      console.error(`  [Tavily] "${q.substring(0, 50)}..."`);
      const res = await fetch(TAVILY_ENDPOINT, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${apiKey}`,
        },
        body: JSON.stringify({ query: q, max_results: maxPerQuery }),
      });
      if (!res.ok) continue;
      const data = await res.json();
      if (data.results) {
        allResults.push(...data.results.map(r => ({
          title: r.title || '',
          url: r.url || '',
          content: truncate(r.content, 200),
          source: 'tavily',
        })));
      }
    } catch (e) {
      console.error(`  [Tavily WARN] ${e.message}`);
    }
  }
  return allResults;
}

// ── 免费网页抓取（通过 agent 的 web_fetch 能力）─────────────────────
// 这个函数生成一个"抓取指令"JSON，供 agent 用 web_fetch 执行。
// 如果在 Node 环境直接运行，则尝试用 fetch 抓取并提取文本。

async function fetchViaWeb(sources) {
  const allResults = [];
  for (const src of sources) {
    try {
      console.error(`  [Web] ${src.name}: ${src.url}`);
      const res = await fetch(src.url, {
        headers: {
          'User-Agent': 'Mozilla/5.0 (compatible; AIStockInsider/1.0)',
          'Accept': 'text/html,application/xhtml+xml',
        },
        signal: AbortSignal.timeout(10000),
      });
      if (!res.ok) {
        console.error(`    HTTP ${res.status}`);
        continue;
      }
      const html = await res.text();
      // 简单提取：找所有看起来像新闻标题的文本
      const titles = extractTitles(html);
      for (const t of titles) {
        allResults.push({
          title: t.title,
          url: t.url || src.url,
          content: truncate(t.snippet, 200),
          source: src.name,
        });
      }
      console.error(`    Found ${titles.length} items`);
    } catch (e) {
      console.error(`    [Web WARN] ${e.message}`);
    }
  }
  return allResults;
}

function extractTitles(html) {
  // 轻量 HTML 标题提取：匹配 <h2>, <h3>, <a> 中的文本
  const results = [];
  // 匹配带 href 的链接中的标题文本
  const linkRe = /<a[^>]*href="([^"]*)"[^>]*>([^<]{10,120})<\/a>/gi;
  let m;
  while ((m = linkRe.exec(html)) !== null && results.length < 20) {
    const url = m[1];
    let title = m[2].replace(/\s+/g, ' ').trim();
    // 过滤掉导航链接、太短的文本
    if (title.length < 15) continue;
    if (/sign in|log in|subscribe|cookie|privacy/i.test(title)) continue;
    results.push({ title, url, snippet: '' });
  }
  // 匹配 h2/h3 标签
  const hRe = /<h[23][^>]*>([^<]{10,120})<\/h[23]>/gi;
  while ((m = hRe.exec(html)) !== null && results.length < 30) {
    let title = m[1].replace(/\s+/g, ' ').trim();
    if (title.length < 15) continue;
    results.push({ title, url: '', snippet: '' });
  }
  return results;
}

// ── 主流程 ───────────────────────────────────────────────────────────

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.help) {
    console.error('Usage: node fetch_news.js [--query "..."] [--market all|cn|us] [--source tavily|web|auto]');
    process.exit(0);
  }

  const apiKey = process.env.TAVILY_API_KEY;
  const useSource = args.source === 'auto'
    ? (apiKey ? 'tavily' : 'web')
    : args.source;

  console.error(`[AI Stock Insider] Source: ${useSource} | Market: ${args.market}`);

  let rawResults = [];

  if (useSource === 'tavily') {
    if (!apiKey) {
      console.error('[ERROR] --source tavily requires TAVILY_API_KEY');
      process.exit(2);
    }
    const queries = args.query ? [args.query] : (TAVILY_QUERIES[args.market] || TAVILY_QUERIES.all);
    rawResults = await fetchViaTavily(queries, args.maxPerQuery, apiKey);
  } else {
    rawResults = await fetchViaWeb(FREE_SOURCES);
  }

  // 去重
  let results = dedup(rawResults);

  // 打分 + 排序
  results = results.map(r => ({
    ...r,
    relevance: scoreArticle(r.title, r.content),
  }));
  results.sort((a, b) => b.relevance - a.relevance);

  // 只保留前 8 条高相关
  results = results.filter(r => r.relevance > 0).slice(0, 8);

  // 如果过滤后太少，补回一些
  if (results.length < 3) {
    const extras = dedup(rawResults)
      .filter(r => !results.find(x => x.url === r.url))
      .slice(0, 5 - results.length);
    results.push(...extras.map(r => ({ ...r, relevance: 0 })));
  }

  const output = {
    timestamp: new Date().toISOString(),
    source: useSource,
    market: args.market,
    total: results.length,
    articles: results.map(r => ({
      title: r.title,
      url: r.url,
      summary: r.content,
      source: r.source,
      relevance: r.relevance,
    })),
  };

  console.error(`[AI Stock Insider] Output: ${results.length} articles`);
  process.stdout.write(JSON.stringify(output, null, 2) + '\n');
}

main().catch(e => {
  console.error(`Fatal: ${e.stack || e.message}`);
  process.exit(1);
});
