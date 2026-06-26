#!/usr/bin/env node
/**
 * fetch_sector_news.js - 抓取板块相关新闻/快讯
 *
 * 数据源：东方财富搜索接口（无需 API Key）
 * 输出：JSON
 *
 * 用法:
 *   node fetch_sector_news.js --sector 化工
 *   node fetch_sector_news.js --sector 医药 --limit 5
 */

function parseArgs(argv) {
  const out = { sector: null, limit: 5, help: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--help' || a === '-h') out.help = true;
    else if (a === '--sector' || a === '-s') out.sector = argv[++i];
    else if (a === '--limit' || a === '-n') out.limit = Number(argv[++i]);
    else if (!a.startsWith('-') && !out.sector) out.sector = a;
  }
  return out;
}

function stripHtml(s = '') {
  return s.replace(/<[^>]+>/g, '').replace(/\s+/g, ' ').trim();
}

function truncate(s = '', n = 60) {
  return s.length > n ? s.slice(0, n) + '...' : s;
}

async function main() {
  const args = parseArgs(process.argv.slice(2));
  if (args.help || !args.sector) {
    console.error('Usage: node fetch_sector_news.js --sector 化工 [--limit 5]');
    process.exit(args.help ? 0 : 2);
  }

  const param = {
    uid: '',
    keyword: args.sector,
    type: ['cmsArticleWebOld'],
    pageIndex: 1,
    pageSize: Math.max(3, Math.min(args.limit, 10)),
  };

  const url = 'https://search-api-web.eastmoney.com/search/jsonp?cb=&param=' + encodeURIComponent(JSON.stringify(param));
  const res = await fetch(url, {
    headers: { 'User-Agent': 'Mozilla/5.0 (compatible; AIStockInsider/1.0)' },
    signal: AbortSignal.timeout(10000),
  });
  if (!res.ok) throw new Error(`HTTP ${res.status}`);

  const text = await res.text();
  const m = text.match(/^\((.*)\)$/s);
  const jsonText = m ? m[1] : text;
  const data = JSON.parse(jsonText);
  const list = data?.result?.cmsArticleWebOld || [];

  const items = list.map(x => ({
    title: stripHtml(x.title),
    summary: truncate(stripHtml(x.content), 60),
    source: x.mediaName || '',
    time: x.date || '',
    url: x.url || '',
  }));

  // 去重（按标题前20字）
  const seen = new Set();
  const deduped = items.filter(x => {
    const key = x.title.slice(0, 20);
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });

  process.stdout.write(JSON.stringify({
    timestamp: new Date().toISOString(),
    sector: args.sector,
    total: deduped.length,
    news: deduped,
  }, null, 2) + '\n');
}

main().catch(e => {
  console.error(`Fatal: ${e.stack || e.message}`);
  process.exit(1);
});
