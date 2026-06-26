#!/usr/bin/env node
/**
 * market_monitor.js - A 股 AI 概念股行情监控
 *
 * 使用东方财富免费 API（无需 key），监控 AI 概念股实时涨跌。
 * 当出现大幅异动（涨跌幅超阈值）时输出告警。
 *
 * 用法:
 *   node market_monitor.js                    # 查看当前行情
 *   node market_monitor.js --threshold 3      # 涨跌幅超 3% 告警（默认 5%）
 *   node market_monitor.js --watch            # 持续监控模式（每60秒刷新）
 *   node market_monitor.js --json             # JSON 输出
 */

const EASTMONEY_API = 'https://push2.eastmoney.com/api/qt/ulist.np/get';

// ── AI 概念股监控池 ─────────────────────────────────────────────────
// secid 格式: 0.=深圳, 1.=上海
const WATCHLIST = [
  // 算力 / 光模块
  { secid: '0.300308', name: '中际旭创', sector: '光模块' },
  { secid: '0.300502', name: '新易盛', sector: '光模块' },
  { secid: '0.300394', name: '天孚通信', sector: '光模块' },
  { secid: '1.603019', name: '中科曙光', sector: 'AI服务器' },
  { secid: '0.000977', name: '浪潮信息', sector: 'AI服务器' },
  // AI 芯片
  { secid: '0.688256', name: '寒武纪', sector: 'AI芯片' },
  { secid: '0.688041', name: '海光信息', sector: 'AI芯片' },
  // 大模型 / 应用
  { secid: '0.002230', name: '科大讯飞', sector: '大模型' },
  { secid: '0.688111', name: '金山办公', sector: 'AI应用' },
  { secid: '0.300624', name: '万兴科技', sector: 'AI应用' },
  { secid: '0.300418', name: '昆仑万维', sector: '大模型' },
  { secid: '1.601360', name: '三六零', sector: 'AI应用' },
  // 机器人
  { secid: '1.601689', name: '拓普集团', sector: '机器人' },
  { secid: '0.002050', name: '三花智控', sector: '机器人' },
  { secid: '0.688017', name: '绿的谐波', sector: '机器人' },
  { secid: '0.300124', name: '汇川技术', sector: '机器人' },
  // 自动驾驶
  { secid: '0.002920', name: '德赛西威', sector: '自动驾驶' },
  { secid: '0.300496', name: '中科创达', sector: '自动驾驶' },
  // 指数
  { secid: '1.000001', name: '上证指数', sector: '指数' },
  { secid: '0.399006', name: '创业板指', sector: '指数' },
  { secid: '0.399005', name: '中小100', sector: '指数' },
];

function parseArgs(argv) {
  const out = { threshold: 5, watch: false, interval: 60, json: false, help: false };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (a === '--help' || a === '-h') out.help = true;
    else if (a === '--threshold' || a === '-t') out.threshold = Number(argv[++i]);
    else if (a === '--watch' || a === '-w') out.watch = true;
    else if (a === '--interval') out.interval = Number(argv[++i]);
    else if (a === '--json') out.json = true;
  }
  return out;
}

async function fetchQuotes() {
  const secids = WATCHLIST.map(w => w.secid).join(',');
  const url = `${EASTMONEY_API}?fltt=2&fields=f2,f3,f4,f12,f14&secids=${secids}`;

  const res = await fetch(url, {
    headers: { 'User-Agent': 'Mozilla/5.0 (compatible; AIStockInsider/1.0)' },
    signal: AbortSignal.timeout(10000),
  });

  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  const data = await res.json();

  if (!data?.data?.diff) return [];

  return data.data.diff.map(d => {
    const meta = WATCHLIST.find(w => w.secid.endsWith(d.f12)) || {};
    return {
      code: d.f12,
      name: d.f14 || meta.name || d.f12,
      price: d.f2,
      change_pct: d.f3,   // 涨跌幅 %
      change_amt: d.f4,   // 涨跌额
      sector: meta.sector || '',
    };
  });
}

function formatTable(quotes) {
  const lines = [];
  lines.push('');

  // 先输出指数
  const indices = quotes.filter(q => q.sector === '指数');
  if (indices.length) {
    lines.push('📊 大盘指数');
    for (const q of indices) {
      const arrow = q.change_pct > 0 ? '🔴' : q.change_pct < 0 ? '🟢' : '⚪';
      const sign = q.change_pct > 0 ? '+' : '';
      lines.push(`  ${arrow} ${q.name}  ${q.price}  ${sign}${q.change_pct}%`);
    }
    lines.push('');
  }

  // 按板块分组
  const sectors = {};
  for (const q of quotes) {
    if (q.sector === '指数') continue;
    if (!sectors[q.sector]) sectors[q.sector] = [];
    sectors[q.sector].push(q);
  }

  for (const [sector, stocks] of Object.entries(sectors)) {
    lines.push(`📈 ${sector}`);
    // 按涨跌幅排序
    stocks.sort((a, b) => b.change_pct - a.change_pct);
    for (const q of stocks) {
      const arrow = q.change_pct > 0 ? '🔴' : q.change_pct < 0 ? '🟢' : '⚪';
      const sign = q.change_pct > 0 ? '+' : '';
      lines.push(`  ${arrow} ${q.name}(${q.code})  ¥${q.price}  ${sign}${q.change_pct}%`);
    }
    lines.push('');
  }

  return lines.join('\n');
}

function checkAlerts(quotes, threshold) {
  const alerts = [];
  for (const q of quotes) {
    if (q.sector === '指数') continue;
    const abs = Math.abs(q.change_pct);
    if (abs >= threshold) {
      const direction = q.change_pct > 0 ? '大涨' : '大跌';
      const emoji = q.change_pct > 0 ? '🚀' : '⚠️';
      alerts.push({
        emoji,
        name: q.name,
        code: q.code,
        sector: q.sector,
        change_pct: q.change_pct,
        price: q.price,
        message: `${emoji} ${q.name}(${q.code}) ${direction} ${q.change_pct > 0 ? '+' : ''}${q.change_pct}%｜${q.sector}｜现价 ¥${q.price}`,
      });
    }
  }
  // 按绝对值排序
  alerts.sort((a, b) => Math.abs(b.change_pct) - Math.abs(a.change_pct));
  return alerts;
}

async function run(args) {
  const quotes = await fetchQuotes();
  if (!quotes.length) {
    console.error('[Monitor] 未获取到行情数据（可能非交易时段）');
    return;
  }

  const alerts = checkAlerts(quotes, args.threshold);

  if (args.json) {
    const output = {
      timestamp: new Date().toISOString(),
      threshold: args.threshold,
      total_stocks: quotes.length,
      alerts: alerts,
      quotes: quotes,
    };
    process.stdout.write(JSON.stringify(output, null, 2) + '\n');
  } else {
    const now = new Date().toLocaleString('zh-CN', { timeZone: 'Asia/Shanghai' });
    console.log(`\n⏰ ${now}  |  异动阈值: ±${args.threshold}%`);
    console.log(formatTable(quotes));

    if (alerts.length) {
      console.log('🔔 异动提醒');
      for (const a of alerts) {
        console.log(`  ${a.message}`);
      }
      console.log('');
    } else {
      console.log('✅ 当前无异动（所有标的涨跌幅均在 ±' + args.threshold + '% 以内）\n');
    }
  }
}

async function main() {
  const args = parseArgs(process.argv.slice(2));

  if (args.help) {
    console.error('Usage: node market_monitor.js [--threshold 5] [--watch] [--interval 60] [--json]');
    process.exit(0);
  }

  if (args.watch) {
    console.error(`[Monitor] 持续监控模式，每 ${args.interval} 秒刷新，异动阈值 ±${args.threshold}%`);
    console.error('[Monitor] 按 Ctrl+C 退出\n');
    while (true) {
      try {
        await run(args);
      } catch (e) {
        console.error(`[Monitor ERROR] ${e.message}`);
      }
      await new Promise(r => setTimeout(r, args.interval * 1000));
    }
  } else {
    await run(args);
  }
}

main().catch(e => {
  console.error(`Fatal: ${e.stack || e.message}`);
  process.exit(1);
});
