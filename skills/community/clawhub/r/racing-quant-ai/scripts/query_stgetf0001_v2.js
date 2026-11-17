const mysql = require('mysql2/promise');

async function main() {
    const conn = await mysql.createConnection({
        host: '47.121.180.199',
        port: 3306,
        user: 'display',
        password: 'display999!',
        database: 'db_strategy'
    });

    // 1. 先看一行数据的原始结构
    const [sample] = await conn.execute(
        `SELECT trade_date, trading_info, trade_price, update_time 
         FROM strategy_huaxiaetftiming_stgetf0001 
         WHERE trade_date = '2023-06-27' 
         ORDER BY update_time DESC LIMIT 1`
    );
    
    if (sample.length > 0) {
        const row = sample[0];
        console.log("=== 原始数据样本 (2023-06-27) ===");
        console.log("trade_date:", row.trade_date, typeof row.trade_date);
        console.log("trading_info type:", typeof row.trading_info);
        console.log("trading_info raw:", JSON.stringify(row.trading_info));
        console.log("trading_info String:", String(row.trading_info));
        console.log("trade_price:", row.trade_price, typeof row.trade_price);
        
        // 如果是对象直接用，如果是字符串则parse
        let holdings = row.trading_info;
        if (typeof holdings === 'string') {
            try { holdings = JSON.parse(holdings); } catch(e) { console.log("parse error:", e.message); }
        }
        console.log("holdings type:", typeof holdings);
        console.log("holdings keys:", Object.keys(holdings || {}));
        console.log("holdings sample:", JSON.stringify(holdings).substring(0, 500));
    }
    
    // 2. 获取月度快照 - 每月最后一个交易日
    const monthEnds = [
        '2023-06-30', '2023-07-31', '2023-08-31', '2023-09-28',
        '2023-10-31', '2023-11-30', '2023-12-29',
        '2024-01-31', '2024-02-29'
    ];
    
    console.log("\n=== 月末持仓快照 ===");
    
    for (const dateStr of monthEnds) {
        // 找该日或之前最近的交易日
        const [rows] = await conn.execute(
            `SELECT trade_date, trading_info, trade_price 
             FROM strategy_huaxiaetftiming_stgetf0001 
             WHERE trade_date <= ? 
             ORDER BY trade_date DESC 
             LIMIT 1`,
            [dateStr]
        );
        
        if (rows.length > 0) {
            const row = rows[0];
            let holdings = row.trading_info;
            if (typeof holdings === 'string') {
                try { holdings = JSON.parse(holdings); } catch(e) { holdings = {}; }
            }
            
            const codes = Object.keys(holdings || {});
            const totalWeight = Object.values(holdings || {}).reduce((a, b) => a + parseFloat(b), 0);
            
            console.log(`\n--- ${row.trade_date} (目标: ${dateStr}) | 持仓ETF数: ${codes.length} | 总权重: ${totalWeight.toFixed(4)} ---`);
            
            const sorted = Object.entries(holdings || {})
                .sort((a, b) => parseFloat(b[1]) - parseFloat(a[1]));
            
            sorted.forEach(([code, weight]) => {
                console.log(`  ${code}: ${(parseFloat(weight) * 100).toFixed(2)}%`);
            });
        }
    }
    
    // 3. 计算每月换手率
    console.log("\n=== 月度换手率分析 ===");
    
    const months = [
        { name: '2023-07', start: '2023-06-30', end: '2023-07-31' },
        { name: '2023-08', start: '2023-07-31', end: '2023-08-31' },
        { name: '2023-09', start: '2023-08-31', end: '2023-09-28' },
        { name: '2023-10', start: '2023-09-28', end: '2023-10-31' },
        { name: '2023-11', start: '2023-10-31', end: '2023-11-30' },
        { name: '2023-12', start: '2023-11-30', end: '2023-12-29' },
        { name: '2024-01', start: '2023-12-29', end: '2024-01-31' },
        { name: '2024-02', start: '2024-01-31', end: '2024-02-29' },
    ];
    
    for (const m of months) {
        const [startRows] = await conn.execute(
            `SELECT trading_info FROM strategy_huaxiaetftiming_stgetf0001 
             WHERE trade_date <= ? ORDER BY trade_date DESC LIMIT 1`, [m.start]
        );
        const [endRows] = await conn.execute(
            `SELECT trading_info FROM strategy_huaxiaetftiming_stgetf0001 
             WHERE trade_date <= ? ORDER BY trade_date DESC LIMIT 1`, [m.end]
        );
        
        if (startRows.length > 0 && endRows.length > 0) {
            let startH = startRows[0].trading_info;
            let endH = endRows[0].trading_info;
            if (typeof startH === 'string') { try { startH = JSON.parse(startH); } catch(e) { startH = {}; } }
            if (typeof endH === 'string') { try { endH = JSON.parse(endH); } catch(e) { endH = {}; } }
            
            const startCodes = new Set(Object.keys(startH || {}));
            const endCodes = new Set(Object.keys(endH || {}));
            
            const added = [...endCodes].filter(c => !startCodes.has(c));
            const removed = [...startCodes].filter(c => !endCodes.has(c));
            const kept = [...startCodes].filter(c => endCodes.has(c));
            
            // 计算权重变化
            const weightChanges = [];
            for (const code of kept) {
                const change = parseFloat(endH[code]) - parseFloat(startH[code]);
                if (Math.abs(change) > 0.001) {
                    weightChanges.push({ code, start: parseFloat(startH[code]), end: parseFloat(endH[code]), change });
                }
            }
            
            const turnoverRate = (added.length + removed.length) / Math.max(startCodes.size, endCodes.size, 1) * 100;
            
            console.log(`\n--- ${m.name} 换手率: ${turnoverRate.toFixed(1)}% (新进${added.length} / 清仓${removed.length} / 保留${kept.length}) ---`);
            if (added.length > 0) console.log(`  新进: ${added.join(', ')}`);
            if (removed.length > 0) console.log(`  清仓: ${removed.join(', ')}`);
            if (weightChanges.length > 0) {
                console.log(`  权重变动>0.1%:`);
                weightChanges.sort((a,b) => Math.abs(b.change) - Math.abs(a.change)).forEach(w => {
                    console.log(`    ${w.code}: ${(w.start*100).toFixed(1)}% → ${(w.end*100).toFixed(1)}% (${(w.change*100).toFixed(1)}%)`);
                });
            }
        }
    }
    
    // 4. ETF被持有天数统计
    console.log("\n=== ETF被持有天数统计（2023.06~2024.02 共158个交易日）===");
    const [allDates] = await conn.execute(
        `SELECT DISTINCT trade_date FROM strategy_huaxiaetftiming_stgetf0001 
         WHERE trade_date >= '2023-06-01' AND trade_date <= '2024-02-29'
         ORDER BY trade_date ASC`
    );
    
    const etfDays = {};
    for (const d of allDates) {
        const [rows] = await conn.execute(
            `SELECT trading_info FROM strategy_huaxiaetftiming_stgetf0001 
             WHERE trade_date = ? ORDER BY update_time DESC LIMIT 1`, [d.trade_date]
        );
        if (rows.length > 0) {
            let h = rows[0].trading_info;
            if (typeof h === 'string') { try { h = JSON.parse(h); } catch(e) { h = {}; } }
            for (const code of Object.keys(h || {})) {
                etfDays[code] = (etfDays[code] || 0) + 1;
            }
        }
    }
    
    const sortedETFs = Object.entries(etfDays).sort((a,b) => b[1] - a[1]);
    console.log("ETF代码 | 被持有天数 | 占比");
    sortedETFs.forEach(([code, days]) => {
        console.log(`  ${code}: ${days}天 (${(days/allDates.length*100).toFixed(1)}%)`);
    });
    
    // 5. 每日持仓数量统计
    console.log("\n=== 每日持仓ETF数量变化 ===");
    let minCount = 999, maxCount = 0;
    let minDate = '', maxDate = '';
    const dailyCounts = [];
    
    for (const d of allDates) {
        const [rows] = await conn.execute(
            `SELECT trading_info FROM strategy_huaxiaetftiming_stgetf0001 
             WHERE trade_date = ? ORDER BY update_time DESC LIMIT 1`, [d.trade_date]
        );
        if (rows.length > 0) {
            let h = rows[0].trading_info;
            if (typeof h === 'string') { try { h = JSON.parse(h); } catch(e) { h = {}; } }
            const count = Object.keys(h || {}).length;
            dailyCounts.push({ date: d.trade_date, count });
            if (count < minCount) { minCount = count; minDate = d.trade_date; }
            if (count > maxCount) { maxCount = count; maxDate = d.trade_date; }
        }
    }
    
    console.log(`最少持仓: ${minCount}只 (${minDate})`);
    console.log(`最多持仓: ${maxCount}只 (${maxDate})`);
    
    // 按月统计平均持仓数
    const monthlyAvg = {};
    for (const dc of dailyCounts) {
        const month = String(dc.date).substring(0, 7);
        if (!monthlyAvg[month]) monthlyAvg[month] = [];
        monthlyAvg[month].push(dc.count);
    }
    console.log("\n月度平均持仓ETF数:");
    for (const [month, counts] of Object.entries(monthlyAvg)) {
        const avg = counts.reduce((a,b) => a+b, 0) / counts.length;
        console.log(`  ${month}: 平均${avg.toFixed(1)}只 (范围 ${Math.min(...counts)}~${Math.max(...counts)})`);
    }
    
    await conn.end();
}

main().catch(e => { console.error("Error:", e); process.exit(1); });
