#!/usr/bin/env node
/**
 * 板块异动分析脚本
 * 用法:
 *   node analyze-sector-anomaly.mjs [--date=YYYY-MM-DD] [--min-members=3] [--top=15]
 *
 * 数据源:
 *   - data/stock-pool-v2.json  板块映射
 *   - data/stock_analyzer.db   daily_quotes / fundflow_cache / longhubang_daily
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import Database from 'better-sqlite3';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
// 支持通过环境变量 STOCK_ANALYZER_ROOT 覆盖项目根目录，默认取脚本上级目录
const ROOT = process.env.STOCK_ANALYZER_ROOT || path.resolve(__dirname, '../../../');
const DB_PATH = path.resolve(ROOT, 'data/stock_analyzer.db');
const POOL_PATH = path.resolve(ROOT, 'data/stock-pool-v2.json');

function parseArgs(argv) {
  const args = { date: null, minMembers: 3, top: 15 };
  for (const a of argv) {
    if (a.startsWith('--date=')) args.date = a.split('=')[1];
    if (a.startsWith('--min-members=')) args.minMembers = Number(a.split('=')[1]);
    if (a.startsWith('--top=')) args.top = Number(a.split('=')[1]);
  }
  return args;
}

function loadPool() {
  const raw = JSON.parse(fs.readFileSync(POOL_PATH, 'utf8'));
  const map = new Map();
  for (const s of raw) map.set(s.code, s);
  return { list: raw, map };
}

function main() {
  const args = parseArgs(process.argv.slice(2));
  const db = new Database(DB_PATH, { readonly: true });
  const pool = loadPool();

  // 确定分析日期
  const latest = db.prepare(
    "SELECT MAX(trade_date) d FROM daily_quotes WHERE close IS NOT NULL AND close > 0"
  ).get().d;
  const date = args.date || latest;

  // 当日行情
  const quotes = db.prepare(`
    SELECT stock_code, close, high, low, volume, amount, change_pct, ma20, ma60, rsi14
    FROM daily_quotes WHERE trade_date=? AND close>0
  `).all(date);

  // 资金流（含5日历史用于趋势）
  const flows = db.prepare(
    "SELECT stock_code, data FROM fundflow_cache WHERE fetch_date=?"
  ).all(date);
  const flowMap = new Map();
  let flowDate = date;
  for (const f of flows) {
    try {
      const j = JSON.parse(f.data);
      if (j.date) flowDate = j.date; // 资金流数据本身的基准日（可能滞后一日）
      flowMap.set(f.stock_code, j);
    } catch {}
  }

  // 龙虎榜
  const lhb = db.prepare(
    "SELECT stock_code, net_buy_amount, institutional_buy, institutional_sell FROM longhubang_daily WHERE trade_date=?"
  ).all(date);
  const lhbMap = new Map();
  for (const r of lhb) {
    if (!lhbMap.has(r.stock_code)) lhbMap.set(r.stock_code, []);
    lhbMap.get(r.stock_code).push(r);
  }

  // 全市场平均涨幅（用于超额收益）
  const allChg = quotes.filter(q => q.change_pct !== null).map(q => q.change_pct);
  const marketAvg = allChg.length ? allChg.reduce((s, v) => s + v, 0) / allChg.length : 0;

  // 全市场当日成交额（用于资金集中度）
  const marketAmount = quotes.reduce((s, q) => s + (q.amount || 0), 0);

  // 按板块聚合
  const sectors = new Map();
  for (const q of quotes) {
    const meta = pool.map.get(q.stock_code);
    const sectorName = meta?.sector || '未分类';
    if (!sectors.has(sectorName)) {
      sectors.set(sectorName, {
        name: sectorName,
        members: 0,
        upCount: 0,
        limitUpCount: 0,
        sumChg: 0,
        weightedChg: 0,
        amount: 0,
        mainForce: 0,
        positiveFlowCount: 0,
        flow5d: 0,
        flowPositiveDays: 0,
        topStocks: [],
      });
    }
    const sec = sectors.get(sectorName);
    sec.members++;
    if ((q.change_pct ?? 0) > 0) sec.upCount++;
    // 涨停: 主板9.5%+，创业板/科创板19.5%+
    const isBoard = q.stock_code.includes('.SZ') || q.stock_code.includes('.SH');
    const threshold = q.stock_code.includes('30') || q.stock_code.includes('688') ? 19.5 : 9.5;
    if ((q.change_pct ?? 0) >= threshold && isBoard) sec.limitUpCount++;
    sec.sumChg += q.change_pct ?? 0;
    sec.weightedChg += (q.change_pct ?? 0) * (q.amount || 0);
    sec.amount += q.amount || 0;
    const fl = flowMap.get(q.stock_code);
    if (fl) {
      sec.mainForce += fl.mainForce || 0;
      if ((fl.mainForce || 0) > 0) sec.positiveFlowCount++;
      const hist = Array.isArray(fl.history) ? fl.history.slice(-5) : [];
      for (const h of hist) {
        sec.flow5d += h.mainForce || 0;
        if ((h.mainForce || 0) > 0) sec.flowPositiveDays++;
      }
    }
    const lhbRows = lhbMap.get(q.stock_code) || [];
    const lhbNet = lhbRows.reduce((s, r) => s + (r.net_buy_amount || 0), 0);
    sec.topStocks.push({
      code: q.stock_code,
      name: pool.map.get(q.stock_code)?.name || q.stock_code,
      chg: q.change_pct ?? 0,
      amount: q.amount || 0,
      mainForce: fl?.mainForce || 0,
      ratio: fl?.ratio || 0,
      lhbNet,
      close: q.close,
    });
  }

  // 计算评分并排序
  const results = [];
  for (const sec of sectors.values()) {
    if (sec.members < args.minMembers || sec.sumChg === 0) continue;
    const avgChg = sec.sumChg / sec.members;
    const excess = avgChg - marketAvg;
    const upRatio = sec.members ? sec.upCount / sec.members : 0;
    const flowRatio = sec.amount > 0 ? sec.mainForce / sec.amount : 0;
    const amountShare = marketAmount > 0 ? sec.amount / marketAmount : 0;

    let score = 0;
    score += excess > 2 ? 20 : excess > 1 ? 15 : excess > 0.5 ? 8 : 0;
    score += sec.mainForce > 0 ? 15 : sec.mainForce < -sec.amount * 0.03 ? -10 : 0;
    score += sec.flowPositiveDays >= 4 ? 15 : sec.flowPositiveDays >= 3 ? 10 : 0;
    score += upRatio > 0.8 ? 20 : upRatio > 0.6 ? 12 : upRatio > 0.4 ? 5 : 0;
    score += sec.limitUpCount >= 2 ? 15 : sec.limitUpCount === 1 ? 8 : 0;
    score += sec.positiveFlowCount / sec.members > 0.6 ? 10 : 0;
    score += amountShare > 0.05 ? 8 : amountShare > 0.02 ? 4 : 0;

    // 龙头 = 涨幅最大且成交额>3000万
    const leaders = sec.topStocks
      .filter(s => s.amount > 30000000)
      .sort((a, b) => b.chg - a.chg)
      .slice(0, 3);

    results.push({
      ...sec,
      avgChg,
      excess,
      upRatio,
      amountShare,
      flowRatio,
      flow5d: sec.flow5d,
      flowPositiveDays: sec.flowPositiveDays,
      score,
      leaders,
    });
  }

  results.sort((a, b) => b.score - a.score);

  // 输出
  const flowNote = flowDate !== date ? `（资金流基准日 ${flowDate}，晚于行情一日）` : '';
  console.log(`# 板块异动报告 ${date}\n`);
  console.log(`市场平均涨幅: ${marketAvg.toFixed(2)}% | 板块数: ${results.length} | 资金流: ${flowNote || flowDate}\n`);
  console.log(`| 排名 | 板块 | 平均涨幅 | 超额 | 上涨占比 | 成交占比 | 主力净流入 | 5日资金 | 涨停 | 评分 | 龙头 |`);
  console.log(`| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |`);
  const topN = results.slice(0, args.top);
  for (const [i, r] of topN.entries()) {
    const lead = r.leaders.map(l => `${l.name}(${l.chg.toFixed(1)}%)`).join(' ');
    const flowCN = r.mainForce > 0 ? `+${(r.mainForce / 1e8).toFixed(2)}亿` : `${(r.mainForce / 1e8).toFixed(2)}亿`;
    const flow5 = r.flow5d > 0 ? `+${(r.flow5d / 1e8).toFixed(2)}亿` : `${(r.flow5d / 1e8).toFixed(2)}亿`;
    console.log(`| ${i + 1} | ${r.name} | ${r.avgChg.toFixed(2)}% | ${r.excess > 0 ? '+' : ''}${r.excess.toFixed(2)}% | ${(r.upRatio * 100).toFixed(0)}% | ${(r.amountShare * 100).toFixed(1)}% | ${flowCN} | ${flow5} | ${r.limitUpCount} | ${r.score} | ${lead} |`);
  }

  console.log(`\n## 强势异动板块（评分前5）`);
  for (const r of topN.slice(0, 5)) {
    console.log(`\n### ${r.name} (${r.score}分)`);
    console.log(`- 平均涨幅 ${r.avgChg.toFixed(2)}% (超额 ${r.excess > 0 ? '+' : ''}${r.excess.toFixed(2)}%) | 上涨占比 ${(r.upRatio * 100).toFixed(0)}% | 成交占比 ${(r.amountShare * 100).toFixed(1)}%`);
    const totalFlowDays = r.members * 5;
    console.log(`- 主力净流入 ${(r.mainForce / 1e8).toFixed(2)}亿 | 5日累计净流入 ${(r.flow5d / 1e8).toFixed(2)}亿 | 个股正流入天数 ${r.flowPositiveDays}/${totalFlowDays} (${(r.flowPositiveDays / totalFlowDays * 100).toFixed(0)}%) | 涨停 ${r.limitUpCount}只 | 资金为正个股 ${r.positiveFlowCount}/${r.members}`);
    if (r.leaders.length) {
      console.log(`- 龙头: ${r.leaders.map(l => `${l.name}(${l.chg.toFixed(1)}%, 主力${(l.mainForce / 1e8).toFixed(2)}亿)`).join('、')}`);
    }
    const judgment = r.score >= 60 ? '强势异动，关注是否持续放量' : r.score >= 40 ? '温和异动，观察资金延续' : '弱异动，暂不参与';
    console.log(`- 判断: ${judgment}`);
  }

  console.log(`\n---`);
  console.log(`免责声明：本报告基于公开行情数据与本地数据库自动整理，仅供研究参考，不构成任何投资建议。市场有风险，决策需独立判断。`);

  db.close();
}

main();
