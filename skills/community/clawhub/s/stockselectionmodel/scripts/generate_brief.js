#!/usr/bin/env node
/**
 * generate_brief.js - 一键总控入口
 *
 * 三种模式：sector / ai-news / monitor
 *
 * 用法:
 *   node generate_brief.js --mode sector --sector 医药 --output pretty
 *   node generate_brief.js --mode ai-news --output pretty
 *   node generate_brief.js --mode monitor --threshold 4 --output pretty
 */

const fs = require('fs');
const path = require('path');
const { execFileSync } = require('child_process');

const SCRIPT_DIR = __dirname;
const ROOT_DIR = path.resolve(SCRIPT_DIR, '..');
const LOCAL_DIR = path.join(ROOT_DIR, '.local');
fs.mkdirSync(LOCAL_DIR, { recursive: true });

function parseArgs(argv) {
  const out = {
    mode: 'sector', sector: null, threshold: 5,
    market: 'all', source: 'auto', output: 'json', help: false,
  };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--help' || a === '-h') out.help = true;
    else if (a === '--mode' || a === '-m') out.mode = argv[++i];
    else if (a === '--sector' || a === '-s') out.sector = argv[++i];
    else if (a === '--threshold' || a === '-t') out.threshold = Number(argv[++i]);
    else if (a === '--market') out.market = argv[++i];
    else if (a === '--source') out.source = argv[++i];
    else if (a === '--output' || a === '-o') out.output = argv[++i];
    else if (!a.startsWith('-') && !out.sector && out.mode === 'sector') out.sector = a;
  }
  return out;
}

function runNode(scriptName, args = []) {
  return execFileSync('node', [path.join(SCRIPT_DIR, scriptName), ...args], {
    cwd: ROOT_DIR, encoding: 'utf-8', stdio: ['pipe', 'pipe', 'pipe'], env: process.env,
  });
}

function saveJson(name, data) {
  const file = path.join(LOCAL_DIR, `${name}_${Date.now()}.json`);
  fs.writeFileSync(file, JSON.stringify(data, null, 2), 'utf-8');
  return file;
}

function pct(v) {
  if (typeof v !== 'number' || Number.isNaN(v)) return '0%';
  return `${v > 0 ? '+' : ''}${v.toFixed(2)}%`;
}

// ── 板块简报 ────────────────────────────────────────────────────────

function buildSectorMarkdown(data, sectorNews = { news: [] }, usData = { us_stocks: [], events: [] }) {
  const top = data.top_gainers?.slice(0, 6) || [];
  const bottom = data.top_losers?.slice(0, 5) || [];
  const news = (sectorNews.news || []).slice(0, 4);
  const usStocks = usData.us_stocks || [];
  const events = (usData.events || []).slice(0, 3);
  const limitUp = top.filter(s => s.change_pct >= 9.9).length;
  const limitDown = bottom.filter(s => s.change_pct <= -9.9).length;
  const upCount = top.filter(s => s.change_pct > 0).length;
  const downCount = bottom.filter(s => s.change_pct < 0).length;
  const now = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai', hour12: false });

  // ── 趋势判断 ──
  let trendIcon, trendText, trendDetail;
  if (limitUp >= 5 && limitDown === 0) {
    trendIcon = '🔴'; trendText = '强势';
    trendDetail = `涨停 ${limitUp} 家，无跌停，板块情绪高涨。`;
  } else if (limitUp >= 3) {
    trendIcon = '🟠'; trendText = '偏强';
    trendDetail = `涨停 ${limitUp} 家，多头占优，但需关注持续性。`;
  } else if (limitUp >= 1) {
    trendIcon = '🟡'; trendText = '活跃';
    trendDetail = `有涨停个股出现，板块有局部热度。`;
  } else if (downCount > upCount) {
    trendIcon = '🟢'; trendText = '偏弱';
    trendDetail = `下跌家数多于上涨，板块整体承压。`;
  } else {
    trendIcon = '⚪'; trendText = '震荡';
    trendDetail = `涨跌互现，暂无明确方向。`;
  }

  // ── 驱动逻辑（从新闻提取） ──
  const newsText = news.map(n => `${n.title} ${n.summary || ''}`).join(' ');
  const drivers = [];
  if (/主力资金.*流入|抢筹|净流入/.test(newsText)) drivers.push('主力资金流入');
  if (/涨价|价格.*上涨|价格获支撑|暴涨/.test(newsText)) drivers.push('产品涨价');
  if (/政策|补贴|扶持|利好/.test(newsText)) drivers.push('政策利好');
  if (/地缘|冲突|制裁|中东/.test(newsText)) drivers.push('地缘催化');
  if (/景气|修复|盈利|业绩/.test(newsText)) drivers.push('景气修复');
  if (/ETF.*申购|净申购/.test(newsText)) drivers.push('ETF资金流入');
  if (/券商.*金股|推荐/.test(newsText)) drivers.push('机构推荐');
  if (/涨停潮|领涨|表现活跃/.test(newsText)) drivers.push('短线情绪升温');

  // ── 风险提示 ──
  const risks = [];
  if (/波动加剧|不宜.*追涨|控制风险/.test(newsText)) risks.push('波动加大，不宜追高');
  if (bottom.some(s => s.change_pct <= -5)) risks.push('板块内部已有分化');
  if (limitUp >= 5) risks.push('短线涨幅过大，注意获利回吐');
  if (risks.length === 0) risks.push('关注龙头股能否持续放量');

  // ── 推断预测 ──
  let forecast;
  if (limitUp >= 5 && drivers.length >= 2) {
    forecast = '多重催化叠加，短线有望延续强势，但需警惕加速后的分歧。';
  } else if (limitUp >= 3 && drivers.length >= 1) {
    forecast = '板块情绪偏强，若龙头继续封板，跟风股有望扩散。';
  } else if (bottom.some(s => s.change_pct <= -5) && limitUp >= 1) {
    forecast = '板块内部分化明显，后续更可能走结构性行情，选股重于选板块。';
  } else if (downCount > upCount) {
    forecast = '板块整体偏弱，短线建议观望为主，等待企稳信号。';
  } else {
    forecast = '短线方向不明，建议轻仓观察，关注龙头股的方向选择。';
  }

  // ── 涨跌比可视化 ──
  const barLen = 20;
  const totalBar = upCount + downCount || 1;
  const upBar = Math.round((upCount / totalBar) * barLen);
  const bar = '🟥'.repeat(upBar) + '🟩'.repeat(barLen - upBar);

  // ── 组装输出 ──
  const L = [];

  L.push(`内容科学｜Content Science`);
  L.push(`📊 ${data.description} · 板块研报`);
  L.push(`${now}`);
  L.push(``);

  // 趋势判断
  L.push(`▎趋势判断`);
  L.push(`${trendIcon} ${trendText}  ·  成分股 ${data.total_stocks} 只  ·  涨停 ${limitUp}  跌停 ${limitDown}`);
  L.push(`${trendDetail}`);
  L.push(``);

  // 核心指标表格
  L.push(`▎核心指标`);
  L.push(`| 指标 | 数值 |`);
  L.push(`|------|------|`);
  L.push(`| 趋势 | ${trendIcon} ${trendText} |`);
  L.push(`| 成分股 | ${data.total_stocks} 只 |`);
  L.push(`| 涨停 | ${limitUp} 只 |`);
  L.push(`| 跌停 | ${limitDown} 只 |`);
  L.push(`| 涨跌比 | 涨 ${upCount} / 跌 ${downCount} |`);
  L.push(``);

  // 板块动态
  L.push(`▎板块动态`);
  if (news.length) {
    L.push(`| 资讯摘要 | 时间 | 来源 | 链接 |`);
    L.push(`|----------|------|------|------|`);
    for (const n of news) {
      const timeShort = (n.time || '').slice(5, 16);
      const summary = (n.summary || n.title || '').replace(/\|/g, '｜');
      const source = (n.source || '').replace(/\|/g, '｜');
      const link = n.url ? `[查看](${n.url})` : '-';
      L.push(`| ${summary} | ${timeShort} | ${source} | ${link} |`);
    }
  } else {
    L.push(`暂无明显相关新闻`);
  }
  L.push(``);

  // 驱动逻辑
  if (drivers.length) {
    L.push(`▎驱动逻辑`);
    L.push(drivers.map(d => `• ${d}`).join('\n'));
    L.push(``);
  }

  // 涨跌比
  L.push(`▎涨跌分布`);
  L.push(`${bar}`);
  L.push(`涨 ${upCount}  ·  跌 ${downCount}  ·  涨停 ${limitUp}  ·  跌停 ${limitDown}`);
  L.push(``);

  // 领涨表格
  L.push(`▎领涨个股`);
  L.push(`| 股票 | 代码 | 涨跌幅 | 状态 |`);
  L.push(`|------|------|--------|------|`);
  for (const s of top) {
    let tag = '';
    if (s.change_pct >= 19.9) tag = '🔥20cm涨停';
    else if (s.change_pct >= 9.9) tag = '🔥涨停';
    else if (s.change_pct >= 5) tag = '🚀强势';
    else tag = '↑';
    L.push(`| ${s.name} | ${s.code} | ${pct(s.change_pct)} | ${tag} |`);
  }
  L.push(``);

  // 领跌表格
  if (bottom.length) {
    L.push(`▎领跌个股`);
    L.push(`| 股票 | 代码 | 涨跌幅 | 状态 |`);
    L.push(`|------|------|--------|------|`);
    for (const s of bottom) {
      let tag = '';
      if (s.change_pct <= -9.9) tag = '💀跌停';
      else if (s.change_pct <= -5) tag = '⚠️弱势';
      else tag = '↓';
      L.push(`| ${s.name} | ${s.code} | ${pct(s.change_pct)} | ${tag} |`);
    }
    L.push(``);
  }

  // 推断预测
  L.push(`▎观点与预测`);
  L.push(`🔮 ${forecast}`);
  L.push(``);

  // 美股关联
  if (usStocks.length) {
    L.push(`▎美股关联`);
    L.push(`| 美股标的 | 代码 | 关联说明 |`);
    L.push(`|----------|------|----------|`);
    for (const u of usStocks) {
      L.push(`| ${u.name} | ${u.ticker} | ${u.desc} |`);
    }
    L.push(``);
  }

  // 大事件 / 利好利空
  const allNewsText = [...news, ...events].map(n => `${n.title} ${n.summary || ''}`).join(' ');
  const bullish = [];
  const bearish = [];
  if (/主力资金.*流入|抢筹|净流入|净申购/.test(allNewsText)) bullish.push('主力资金持续流入');
  if (/涨价|价格.*上涨|价格获支撑|供应.*收缩|供应紧张/.test(allNewsText)) bullish.push('产品涨价/供应收缩');
  if (/政策.*利好|补贴|扶持/.test(allNewsText)) bullish.push('政策利好');
  if (/券商.*金股|机构.*推荐|人气/.test(allNewsText)) bullish.push('机构看好/推荐');
  if (/景气.*修复|盈利.*改善|业绩.*超预期/.test(allNewsText)) bullish.push('行业景气修复');
  if (/地缘.*催化|冲突.*推升|能源.*暴涨/.test(allNewsText)) bullish.push('地缘事件催化涨价');

  if (/波动加剧|不宜.*追涨|控制风险/.test(allNewsText)) bearish.push('短线波动加大');
  if (/下跌|走低|承压|回调/.test(allNewsText)) bearish.push('部分标的回调压力');
  if (/制裁|限制|出口管制/.test(allNewsText)) bearish.push('政策/制裁风险');
  if (/产能过剩|供过于求/.test(allNewsText)) bearish.push('产能过剩隐忧');

  if (bullish.length || bearish.length) {
    L.push(`▎利好 / 利空`);
    if (bullish.length) {
      L.push(`📈 利好因素`);
      for (const b of bullish) L.push(`  ✅ ${b}`);
    }
    if (bearish.length) {
      L.push(`📉 利空因素`);
      for (const b of bearish) L.push(`  ❌ ${b}`);
    }
    L.push(``);
  }

  // 近期大事件
  if (events.length) {
    L.push(`▎近期大事件`);
    L.push(`| 事件概括 | 时间 | 来源 | 链接 |`);
    L.push(`|----------|------|------|------|`);
    for (let i = 0; i < events.length; i++) {
      const e = events[i];
      const timeShort = (e.time || '').slice(5, 16);
      const summary = (e.summary || e.title || '').replace(/\|/g, '｜');
      const source = (e.source || '').replace(/\|/g, '｜');
      const link = e.url ? `[详情](${e.url})` : '-';
      L.push(`| ${summary} | ${timeShort} | ${source} | ${link} |`);
    }
    L.push(``);
  }

  // 关注要点
  L.push(`▎关注要点`);
  L.push(`1. 龙头股次日能否继续走强或连板`);
  L.push(`2. 板块涨停家数是否扩散`);
  L.push(`3. 成交量能否持续放大`);
  L.push(``);

  // 风险提示
  L.push(`▎风险提示`);
  for (const r of risks) L.push(`⚠️ ${r}`);
  L.push(``);

  L.push(`— 内容科学｜Content Science · 以上内容由 AI 基于公开数据生成，仅供参考，不构成投资建议 —`);

  return L.join('\n');
}

// ── AI 新闻简报 ─────────────────────────────────────────────────────

function buildAiNewsMarkdown(news, stocks) {
  const L = [];
  L.push('内容科学｜Content Science');
  L.push('📊 AI 股票内参简报');
  L.push('');
  L.push(`▎核心新闻`);
  for (const a of (news.articles || []).slice(0, 5)) L.push(`• ${a.title}`);
  L.push('');
  L.push(`▎A股候选标的`);
  for (const s of (stocks.a_shares || []).slice(0, 8)) L.push(`${s.name}（${s.code}）— ${s.reason}`);
  L.push('');
  L.push('— 内容科学｜Content Science · 仅供参考，不构成投资建议 —');
  return L.join('\n');
}

// ── 异动监控 ────────────────────────────────────────────────────────

function buildMonitorMarkdown(data) {
  const alerts = data.alerts || [];
  const L = [];
  L.push('内容科学｜Content Science');
  L.push('🔔 AI 概念股异动提醒');
  L.push('');
  L.push(`监控阈值：±${data.threshold}%  ·  告警：${alerts.length} 条`);
  L.push('');
  if (alerts.length) for (const a of alerts) L.push(`• ${a.message}`);
  else L.push('当前无明显异动');
  L.push('');
  L.push('— 内容科学｜Content Science · 仅供参考，不构成投资建议 —');
  return L.join('\n');
}

// ── 模式执行 ────────────────────────────────────────────────────────

function runSectorMode(args) {
  if (!args.sector) throw new Error('sector 模式需要 --sector 参数');

  const sectorRaw = runNode('sector_analyze.js', ['--sector', args.sector, '--json']);
  const sectorData = JSON.parse(sectorRaw);
  const sectorFile = saveJson(`sector_${sectorData.sector}`, sectorData);

  let sectorNews = { news: [] };
  try {
    const newsRaw = runNode('fetch_sector_news.js', ['--sector', sectorData.description || args.sector, '--limit', '5']);
    sectorNews = JSON.parse(newsRaw);
  } catch (e) {
    console.error(`[WARN] Sector news fetch failed: ${e.message}`);
  }

  let usData = { us_stocks: [], events: [] };
  try {
    const usRaw = runNode('fetch_us_related.js', ['--sector', sectorData.description || args.sector]);
    usData = JSON.parse(usRaw);
  } catch (e) {
    console.error(`[WARN] US related fetch failed: ${e.message}`);
  }

  const markdown = buildSectorMarkdown(sectorData, sectorNews, usData);

  return {
    mode: 'sector', sector: sectorData.sector, description: sectorData.description,
    markdown, data_file: sectorFile, data: sectorData, news: sectorNews, us: usData,
  };
}

function runAiNewsMode(args) {
  const newsRaw = runNode('fetch_news.js', ['--market', args.market, '--source', args.source]);
  const newsData = JSON.parse(newsRaw);
  const newsFile = saveJson('ai_news', newsData);

  const stocksRaw = execFileSync('node', [path.join(SCRIPT_DIR, 'map_stocks.js')], {
    cwd: ROOT_DIR, input: JSON.stringify(newsData),
    encoding: 'utf-8', stdio: ['pipe', 'pipe', 'pipe'], env: process.env,
  });
  const stocksData = JSON.parse(stocksRaw);
  const stocksFile = saveJson('ai_stocks', stocksData);
  const markdown = buildAiNewsMarkdown(newsData, stocksData);

  return { mode: 'ai-news', markdown, news_file: newsFile, stocks_file: stocksFile, news: newsData, stocks: stocksData };
}

function runMonitorMode(args) {
  const raw = runNode('market_monitor.js', ['--threshold', String(args.threshold), '--json']);
  const data = JSON.parse(raw);
  const dataFile = saveJson('monitor', data);
  const markdown = buildMonitorMarkdown(data);
  return { mode: 'monitor', markdown, data_file: dataFile, data };
}

function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.help) {
    console.log(`Usage:
  node scripts/generate_brief.js --mode sector --sector 医药
  node scripts/generate_brief.js --mode ai-news
  node scripts/generate_brief.js --mode monitor --threshold 4
Options: --mode, --sector, --threshold, --market, --source, --output (json|pretty)`);
    process.exit(0);
  }

  let result;
  if (args.mode === 'sector') result = runSectorMode(args);
  else if (args.mode === 'ai-news') result = runAiNewsMode(args);
  else if (args.mode === 'monitor') result = runMonitorMode(args);
  else throw new Error(`未知 mode: ${args.mode}`);

  if (args.output === 'pretty') {
    console.log(result.markdown);
  } else {
    process.stdout.write(JSON.stringify(result, null, 2) + '\n');
  }
}

main();
