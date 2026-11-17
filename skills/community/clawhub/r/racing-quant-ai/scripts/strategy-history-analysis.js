#!/usr/bin/env node
/**
 * 策略历史持仓分析脚本
 * 用法: node strategy-history-analysis.js <strategy_id> <start_date> <end_date>
 * 示例: node strategy-history-analysis.js stgetf0001 2023-06-01 2024-02-29
 *
 * 输出:
 *   1. 策略基本信息
 *   2. 时间段内所有调仓日期列表
 *   3. 月度持仓快照（每月最后交易日）
 *   4. 月度换手率分析
 *   5. ETF/股票被持有天数统计
 *   6. 每日持仓数量变化统计
 */

const mysql = require('mysql2/promise');

const STRATEGY_ID = process.argv[2] || 'stgetf0001';
const START_DATE = process.argv[3] || '2023-06-01';
const END_DATE = process.argv[4] || '2024-02-29';

const DB_CONFIG = {
    host: '47.121.180.199',
    port: 3306,
    user: 'display',
    password: 'display999!',
    database: 'db_strategy'
};

async function main() {
    const conn = await mysql.createConnection(DB_CONFIG);

    // 1. 获取策略信息
    const [strategies] = await conn.execute(
        "SELECT * FROM strategy_information WHERE strategy_id = ?", [STRATEGY_ID]
    );
    if (strategies.length === 0) {
        console.log(`未找到策略ID: ${STRATEGY_ID}`);
        await conn.end();
        return;
    }
    const strat = strategies[0];
    const tableName = strat.strategy_table;

    console.log("=== 策略信息 ===");
    console.log("名称:", strat.strategy_name);
    console.log("中文名称:", strat.strategy_name_cn);
    console.log("策略ID:", strat.strategy_id);
    console.log("持仓表名:", tableName);
    console.log("对标:", strat.benchmark);
    console.log("调仓规则:", strat.how_to_trade);
    console.log("回测起始:", strat.start_date);

    // 2. 查询时间段内所有调仓日期
    const [dates] = await conn.execute(
        `SELECT DISTINCT trade_date FROM ${tableName}
         WHERE trade_date >= ? AND trade_date <= ?
         ORDER BY trade_date ASC`,
        [START_DATE, END_DATE]
    );
    console.log(`\n=== 调仓日期 (${START_DATE}~${END_DATE}) ===`);
    console.log("总交易日数:", dates.length);

    // 3. 获取每期持仓（trading_info 是 Object 不是 String!）
    const allHoldings = []; // [{date, holdings: {code: weight}}]
    for (const d of dates) {
        const [rows] = await conn.execute(
            `SELECT trade_date, trading_info FROM ${tableName}
             WHERE trade_date = ? ORDER BY update_time DESC LIMIT 1`,
            [d.trade_date]
        );
        if (rows.length > 0) {
            let holdings = rows[0].trading_info;
            if (typeof holdings === 'string') {
                try { holdings = JSON.parse(holdings); } catch(e) { holdings = {}; }
            }
            allHoldings.push({ date: d.trade_date, holdings });
        }
    }

    // 4. 月度快照
    const monthEnds = getMonthEndTradingDays(allHoldings.map(h => h.date));
    console.log("\n=== 月度持仓快照 ===");
    for (const me of monthEnds) {
        const snap = allHoldings.filter(h => h.date <= me).pop();
        if (!snap) continue;
        const codes = Object.keys(snap.holdings);
        const totalWeight = Object.values(snap.holdings).reduce((a, b) => a + parseFloat(b), 0);
        console.log(`\n--- ${snap.date} (目标月末: ${me}) | 持仓数: ${codes.length} | 总权重: ${totalWeight.toFixed(4)} ---`);
        Object.entries(snap.holdings)
            .sort((a, b) => parseFloat(b[1]) - parseFloat(a[1]))
            .forEach(([code, w]) => {
                console.log(`  ${code}: ${(parseFloat(w) * 100).toFixed(2)}%`);
            });
    }

    // 5. 月度换手率
    console.log("\n=== 月度换手率分析 ===");
    const snapshots = monthEnds.map(me => allHoldings.filter(h => h.date <= me).pop()).filter(Boolean);
    for (let i = 1; i < snapshots.length; i++) {
        const prev = new Set(Object.keys(snapshots[i-1].holdings));
        const curr = new Set(Object.keys(snapshots[i].holdings));
        const newIn = [...curr].filter(c => !prev.has(c));
        const cleared = [...prev].filter(c => !curr.has(c));
        const kept = [...curr].filter(c => prev.has(c));
        const turnover = (newIn.length + cleared.length) / Math.max(prev.size, curr.size) * 100;
        console.log(`\n--- ${snapshots[i-1].date} → ${snapshots[i].date} 换手率: ${turnover.toFixed(1)}% ---`);
        console.log(`  新进(${newIn.length}): ${newIn.join(', ') || '无'}`);
        console.log(`  清仓(${cleared.length}): ${cleared.join(', ') || '无'}`);
        console.log(`  保留(${kept.length}): ${kept.join(', ') || '无'}`);
    }

    // 6. 持有天数统计
    console.log("\n=== 被持有天数统计 ===");
    const holdDays = {};
    for (const h of allHoldings) {
        for (const code of Object.keys(h.holdings)) {
            holdDays[code] = (holdDays[code] || 0) + 1;
        }
    }
    const sortedHold = Object.entries(holdDays).sort((a, b) => b[1] - a[1]);
    console.log("ETF代码 | 被持有天数 | 占比");
    sortedHold.forEach(([code, days]) => {
        console.log(`  ${code}: ${days}天 (${(days / allHoldings.length * 100).toFixed(1)}%)`);
    });

    // 7. 每日持仓数量
    const counts = allHoldings.map(h => Object.keys(h.holdings).length);
    console.log("\n=== 每日持仓数量统计 ===");
    console.log(`最少持仓: ${Math.min(...counts)}只 (${allHoldings[counts.indexOf(Math.min(...counts))].date})`);
    console.log(`最多持仓: ${Math.max(...counts)}只 (${allHoldings[counts.indexOf(Math.max(...counts))].date})`);

    // 月度平均
    const monthGroups = {};
    for (const h of allHoldings) {
        const month = h.date.substring(0, 7);
        if (!monthGroups[month]) monthGroups[month] = [];
        monthGroups[month].push(Object.keys(h.holdings).length);
    }
    console.log("\n月度平均持仓数:");
    for (const [month, arr] of Object.entries(monthGroups)) {
        const avg = arr.reduce((a, b) => a + b, 0) / arr.length;
        console.log(`  ${month}: 平均${avg.toFixed(1)}只 (范围 ${Math.min(...arr)}~${Math.max(...arr)})`);
    }

    await conn.end();
}

// 获取每月最后一个交易日
function getMonthEndTradingDays(allDates) {
    const sorted = [...allDates].sort();
    const monthEnds = [];
    let lastMonth = '';
    let lastDate = '';
    for (const d of sorted) {
        const month = d.substring(0, 7);
        if (month !== lastMonth && lastMonth) {
            monthEnds.push(lastDate);
        }
        lastMonth = month;
        lastDate = d;
    }
    if (lastDate) monthEnds.push(lastDate);
    return monthEnds;
}

main().catch(e => { console.error("Error:", e.message); process.exit(1); });
