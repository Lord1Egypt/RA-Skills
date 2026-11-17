const mysql = require('mysql2/promise');

async function main() {
    const conn = await mysql.createConnection({
        host: '47.121.180.199',
        port: 3306,
        user: 'display',
        password: 'display999!',
        database: 'db_strategy'
    });

    const tableName = 'strategy_huaxiaetftiming_stgetf0001';

    // 1. 全部交易日期范围
    const [allDates] = await conn.execute(
        `SELECT MIN(trade_date) as min_date, MAX(trade_date) as max_date, COUNT(DISTINCT trade_date) as total_days FROM ${tableName}`
    );
    console.log("=== 策略全周期 ===");
    console.log("起止:", allDates[0].min_date, "~", allDates[0].max_date, "| 总交易日:", allDates[0].total_days);

    // 2. 按月统计：月末持仓数 + 月均持仓数
    const [months] = await conn.execute(
        `SELECT DATE_FORMAT(trade_date, '%Y-%m') as month, 
                COUNT(DISTINCT trade_date) as trading_days,
                COUNT(DISTINCT DATE_FORMAT(DATE_SUB(trade_date, INTERVAL WEEKDAY(trade_date) DAY), '%Y-%m-%d')) as weeks
         FROM ${tableName} 
         GROUP BY DATE_FORMAT(trade_date, '%Y-%m')
         ORDER BY month ASC`
    );

    console.log("\n=== 月度统计 ===");
    console.log("月份 | 交易日数 | 月末持仓数 | 月均持仓数 | 月末持仓ETF列表");
    
    for (const m of months) {
        // 月末最后一个交易日
        const [lastDay] = await conn.execute(
            `SELECT trade_date, trading_info FROM ${tableName} 
             WHERE DATE_FORMAT(trade_date, '%Y-%m') = ? 
             ORDER BY trade_date DESC LIMIT 1`,
            [m.month]
        );
        
        // 月均持仓数
        const [allDays] = await conn.execute(
            `SELECT trade_date, trading_info FROM ${tableName} 
             WHERE DATE_FORMAT(trade_date, '%Y-%m') = ? 
             ORDER BY trade_date ASC`,
            [m.month]
        );
        
        let countSum = 0;
        let countList = [];
        for (const d of allDays) {
            let holdings = {};
            try { 
                if (typeof d.trading_info === 'string') holdings = JSON.parse(d.trading_info);
                else holdings = d.trading_info;
            } catch(e) {}
            const cnt = Object.keys(holdings).length;
            countSum += cnt;
            countList.push(cnt);
        }
        const avgCount = allDays.length > 0 ? (countSum / allDays.length).toFixed(1) : 'N/A';
        const minCount = Math.min(...countList);
        const maxCount = Math.max(...countList);
        
        let monthEndHoldings = {};
        if (lastDay.length > 0) {
            try {
                if (typeof lastDay[0].trading_info === 'string') monthEndHoldings = JSON.parse(lastDay[0].trading_info);
                else monthEndHoldings = lastDay[0].trading_info;
            } catch(e) {}
        }
        const meCount = Object.keys(monthEndHoldings).length;
        const meList = Object.keys(monthEndHoldings).join(', ');
        
        console.log(`${m.month} | ${m.trading_days}天 | 月末${meCount}只 | 月均${avgCount}只 (${minCount}~${maxCount}) | ${meList}`);
    }

    // 3. 全周期持仓ETF出现频次
    const [allRows] = await conn.execute(
        `SELECT trade_date, trading_info FROM ${tableName} ORDER BY trade_date ASC`
    );
    
    const etfDays = {};
    const etfFirstDate = {};
    const etfLastDate = {};
    let totalCount = 0;
    
    for (const row of allRows) {
        let holdings = {};
        try {
            if (typeof row.trading_info === 'string') holdings = JSON.parse(row.trading_info);
            else holdings = row.trading_info;
        } catch(e) {}
        
        for (const code of Object.keys(holdings)) {
            etfDays[code] = (etfDays[code] || 0) + 1;
            if (!etfFirstDate[code]) etfFirstDate[code] = row.trade_date;
            etfLastDate[code] = row.trade_date;
        }
        totalCount++;
    }
    
    console.log("\n=== 全周期ETF被持有天数排名 ===");
    console.log(`总交易日: ${totalCount}`);
    const sortedETFs = Object.entries(etfDays).sort((a, b) => b[1] - a[1]);
    for (const [code, days] of sortedETFs) {
        console.log(`  ${code}: ${days}天 (${(days/totalCount*100).toFixed(1)}%) | ${etfFirstDate[code]} ~ ${etfLastDate[code]}`);
    }
    
    // 4. 统计不同时间段持仓数变化趋势
    // 分段: 2023.06-2023.12 (熊市), 2024.01-2024.08 (震荡筑底), 2024.09-2024.12 (反弹), 2025.01+ (如果有)
    const periods = [
        { name: '2023.06-2023.12 (下跌期)', start: '2023-06-01', end: '2023-12-31' },
        { name: '2024.01-2024.08 (筑底期)', start: '2024-01-01', end: '2024-08-31' },
        { name: '2024.09-2024.12 (924反弹)', start: '2024-09-01', end: '2024-12-31' },
        { name: '2025.01-至今 (最新)', start: '2025-01-01', end: '2030-12-31' },
    ];
    
    console.log("\n=== 分阶段对比 ===");
    for (const p of periods) {
        const [rows] = await conn.execute(
            `SELECT trade_date, trading_info FROM ${tableName} 
             WHERE trade_date >= ? AND trade_date <= ? 
             ORDER BY trade_date ASC`,
            [p.start, p.end]
        );
        
        if (rows.length === 0) {
            console.log(`${p.name}: 无数据`);
            continue;
        }
        
        let countSum = 0;
        let counts = [];
        for (const r of rows) {
            let h = {};
            try {
                if (typeof r.trading_info === 'string') h = JSON.parse(r.trading_info);
                else h = r.trading_info;
            } catch(e) {}
            counts.push(Object.keys(h).length);
            countSum += Object.keys(h).length;
        }
        
        const avg = (countSum / rows.length).toFixed(1);
        const minC = Math.min(...counts);
        const maxC = Math.max(...counts);
        
        // 换手率
        let turnoverSum = 0;
        let turnoverCount = 0;
        for (let i = 1; i < rows.length; i++) {
            let prevH = {}, currH = {};
            try {
                if (typeof rows[i-1].trading_info === 'string') prevH = JSON.parse(rows[i-1].trading_info);
                else prevH = rows[i-1].trading_info;
                if (typeof rows[i].trading_info === 'string') currH = JSON.parse(rows[i].trading_info);
                else currH = rows[i].trading_info;
            } catch(e) {}
            
            const prevKeys = new Set(Object.keys(prevH));
            const currKeys = new Set(Object.keys(currH));
            let changed = 0;
            for (const k of currKeys) if (!prevKeys.has(k)) changed++;
            for (const k of prevKeys) if (!currKeys.has(k)) changed++;
            const total = prevKeys.size + currKeys.size;
            turnoverSum += total > 0 ? changed / total * 100 : 0;
            turnoverCount++;
        }
        const avgTurnover = turnoverCount > 0 ? (turnoverSum / turnoverCount).toFixed(1) : 'N/A';
        
        console.log(`${p.name}: ${rows.length}天 | 月均持仓${avg}只 (${minC}~${maxC}) | 日均换手${avgTurnover}% | 起止${rows[0].trade_date}~${rows[rows.length-1].trade_date}`);
    }

    await conn.end();
}

main().catch(e => { console.error("Error:", e.message); process.exit(1); });
