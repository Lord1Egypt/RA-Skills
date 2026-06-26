#!/usr/bin/env node
/**
 * tavily-web-seeker v1.0.0
 */
const BASE_URL = process.env.TAVILY_BASE_URL || "https://api.tavily.com";

const PREFERENCES = {
  default_sites: ["wikipedia.org", "github.com", "stackoverflow.com"],
  preferred_topics: {
    tech: ["wikipedia.org", "github.com", "stackoverflow.com"],
    news: ["reuters.com", "apnews.com", "bbc.com"],
    finance: ["wsj.com", "bloomberg.com", "ft.com"],
    academic: ["scholar.google.com", "arxiv.org"]
  },
  critical_sources: {
    "官方": ["gov.cn"], "财经": ["wsj.com", "bloomberg.com"], "技术": ["github.com"]
  }
};

function loadApiKeys() {
  const keys = [];
  if (process.env.TAVILY_API_KEY) keys.push(process.env.TAVILY_API_KEY);
  for (let i = 2; i <= 10; i++) {
    const k = process.env[`TAVILY_API_KEY_${i}`];
    if (k) keys.push(k);
  }
  return keys.length ? keys : null;
}

function getApiKey(idx = 0) {
  const keys = loadApiKeys();
  if (!keys) throw new Error("No Tavily API key");
  return keys[idx % keys.length];
}

function recognizeIntent(q) {
  const l = q.toLowerCase();
  if (l.includes(" vs ") || l.includes("compare")) return "comparison";
  if (l.startsWith("how") || l.startsWith("如何")) return "how_to";
  if (l.includes("news") || l.includes("新闻")) return "news";
  if (l.includes("paper") || l.includes("研究")) return "academic";
  return "general";
}

function getDomainsForTopic(q) {
  const l = q.toLowerCase();
  if (l.match(/tech|code|编程/)) return PREFERENCES.preferred_topics.tech;
  if (l.match(/news|新闻/)) return PREFERENCES.preferred_topics.news;
  if (l.match(/finance|金融/)) return PREFERENCES.preferred_topics.finance;
  return PREFERENCES.default_sites;
}

function getTimeFilter(mode) {
  return { news: "day", recent: "week", research: "month" }[mode] || null;
}

function decomposeQuery(q, mode) {
  if (mode === "quick") return [q];
  return [`${q} - overview`, `${q} - latest`, `${q} - analysis`];
}

function generateNotFound(q, findings) {
  const missing = findings.filter(f => !f.found).map(f => f.category).join(", ");
  return {
    results_found: false,
    not_found_conclusion: `在核心信源 [${missing}] 中未找到"${q}"相关内容。`,
    suggestions: ["扩展搜索词", "放宽信源限制", "手动访问目标网站"]
  };
}

async function searchWithRetry(query, options, keyIdx = 0) {
  const apiKey = getApiKey(keyIdx);
  const body = { query, max_results: options.maxResults || 5, search_depth: options.searchDepth || "basic" };
  if (options.domains?.length) body.include_domains = options.domains;
  if (options.timeRange) body.time_range = options.timeRange;
  
  const resp = await fetch(`${BASE_URL}/search`, {
    method: "POST",
    headers: { "Content-Type": "application/json", "Authorization": `Bearer ${apiKey}`, "X-Client-Source": "tavily-web-seeker" },
    body: JSON.stringify(body),
    signal: AbortSignal.timeout(30000)
  });
  
  if (resp.status === 429 && keyIdx < 5) return searchWithRetry(query, options, keyIdx + 1);
  if (!resp.ok) throw new Error(`Search failed: ${resp.status}`);
  return { data: await resp.json(), keyUsed: keyIdx };
}

function generateDoc(options) {
  const fs = require("fs");
  const dir = `${process.env.HOME}/.openclaw/workspace/reports`;
  if (!fs.existsSync(dir)) fs.mkdirSync(dir, { recursive: true });
  const filepath = `${dir}/seeker-${Date.now()}.md`;
  let content = `# Web Seeker Report\n\nQuery: ${options.query}\nIntent: ${options.intent}\n\n`;
  if (options.notFound) {
    content += `\n## Not Found\n${options.notFound.not_found_conclusion}\n`;
  } else {
    content += `\n## Results\n${options.results.map((r, i) => `${i + 1}. ${r.title}\n${r.url}\n`).join("\n")}`;
  }
  fs.writeFileSync(filepath, content);
  return filepath;
}

async function webSeeker(query, options = {}) {
  const start = Date.now();
  const mode = options.mode || "quick";
  const intent = recognizeIntent(query);
  const domains = options.domains || getDomainsForTopic(query);
  const subQuestions = options.subQuestions || decomposeQuery(query, mode);
  const timeRange = options.timeRange || getTimeFilter(mode);
  
  const allResults = [];
  for (const sq of subQuestions.slice(0, 5)) {
    try {
      const { data } = await searchWithRetry(sq, { maxResults: 5, searchDepth: mode === "research" ? "advanced" : "basic", domains, timeRange });
      allResults.push(...(data.results || []));
    } catch (e) { console.error(e.message); }
  }
  
  const seen = new Set();
  const flatResults = allResults.filter(r => { if (seen.has(r.url)) return false; seen.add(r.url); return true; }).slice(0, 20);
  
  let sourceCoverage = { preferred: 0, total: flatResults.length };
  if (domains.length) {
    const prefSet = new Set(domains.map(d => d.toLowerCase()));
    sourceCoverage.preferred = flatResults.filter(r => { try { return prefSet.has(new URL(r.url).hostname.toLowerCase()); } catch {} return false; }).length;
  }
  
  let notFound = flatResults.length === 0 ? generateNotFound(query, []) : null;
  let docPath = options.exportDoc ? generateDoc({ query, intent, results: flatResults, notFound }) : null;
  
  return {
    original_query: query, intent, domains_used: domains,
    results_found: flatResults.length > 0, source_coverage: sourceCoverage,
    results: flatResults, summary: flatResults.map(r => r.content || r.snippet).join("\n\n"),
    ...(notFound || {}), doc_path: docPath,
    metadata: { mode, timeRange, tookMs: Date.now() - start }
  };
}

module.exports = { webSeeker, PREFERENCES };

if (require.main === module) {
  const args = process.argv.slice(2);
  if (!args.length) { console.error("Usage: node seeker.js <query>"); process.exit(1); }
  webSeeker(args.join(" ")).then(r => console.log(JSON.stringify(r, null, 2))).catch(e => { console.error(e.message); process.exit(1); });
}
