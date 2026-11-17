const mysql = require('mysql2/promise');

async function main() {
    const conn = await mysql.createConnection({
        host: '47.121.180.199',
        port: 3306,
        user: 'display',
        password: 'display999!',
        database: 'db_strategy'
    });

    // 1. 查询策略基本信息
    const [strategies] = await conn.execute(
        "SELECT * FROM strategy_information WHERE strategy_id = ?", ['stgetf0001']
    );
    
    if (strategies.length === 0) {
        console.log("未找到策略ID: stgetf0001");
        await conn.end();
        return;
    }
    
    const strat = strategies[0];
    console.log("=== 策略信息 ===");
    console.log("策略名称:", strat.strategy_name);
    console.log("中文名称:", strat.strategy_name_cn);
    console.log("策略ID:", strat.strategy_id);
    console.log("持仓表名:", strat.strategy_table);
    console.log("对标:", strat.benchmark);
    console.log("简介:", strat.strategy_summ);
    console.log("描述:", (strat.strategy_desc || '').substring(0, 500));
    console.log("调仓规则:", strat.how_to_trade);
    console.log("开始时间:", strat.start_date);
    console.log("上线时间:", strat.online_date);
    
    const tableName = strat.strategy_table;
    
    // 2. 查询2023-06到2024-02的持仓变化
    // 先看这个时间段有多少期调仓
    const [dates] = await conn.execute(
        `SELECT DISTINCT trade_date FROM ${tableName} 
         WHERE trade_date >= '2023-06-01' AND trade_date <= '2024-02-29'
         ORDER BY trade_date ASC`
    );
    
    console.log("\n=== 2023.06~2024.02 调仓日期列表 ===");
    console.log("总期数:", dates.length);
    dates.forEach((d, i) => {
        console.log(`  ${i+1}. ${d.trade_date}`);
    });
    
    // 3. 逐期输出持仓详情
    console.log("\n=== 逐期持仓详情 ===");
    for (const d of dates) {
        const [rows] = await conn.execute(
            `SELECT trade_date, strategy_name, trading_info, trade_price, update_time 
             FROM ${tableName} 
             WHERE trade_date = ? 
             ORDER BY update_time DESC 
             LIMIT 1`,
            [d.trade_date]
        );
        
        if (rows.length > 0) {
            const row = rows[0];
            let holdings = {};
            try {
                holdings = JSON.parse(row.trading_info);
            } catch(e) {
                holdings = { "parse_error": row.trading_info?.substring(0, 200) };
            }
            
            const stockCount = Object.keys(holdings).filter(k => !k.includes('parse_error')).length;
            console.log(`\n--- ${row.trade_date} | 持仓股票数: ${stockCount} | 价格: ${row.trade_price} ---`);
            
            // 按权重排序
            const sorted = Object.entries(holdings)
                .filter(([k, v]) => !k.includes('parse_error'))
                .sort((a, b) => parseFloat(b[1]) - parseFloat(a[1]));
            
            sorted.forEach(([code, weight]) => {
                console.log(`  ${code}: ${weight}`);
            });
        }
    }
    
    // 4. 查询调仓前一期(2023年5月最后一次)和调仓后一期(2024年3月第一次)作为对比
    const [beforeRows] = await conn.execute(
        `SELECT DISTINCT trade_date FROM ${tableName} 
         WHERE trade_date < '2023-06-01'
         ORDER BY trade_date DESC LIMIT 1`
    );
    
    const [afterRows] = await conn.execute(
        `SELECT DISTINCT trade_date FROM ${tableName} 
         WHERE trade_date > '2024-02-29'
         ORDER BY trade_date ASC LIMIT 1`
    );
    
    if (beforeRows.length > 0) {
        const beforeDate = beforeRows[0].trade_date;
        const [beforeHoldings] = await conn.execute(
            `SELECT trading_info, trade_price FROM ${tableName} 
             WHERE trade_date = ? ORDER BY update_time DESC LIMIT 1`,
            [beforeDate]
        );
        if (beforeHoldings.length > 0) {
            let holdings = {};
            try { holdings = JSON.parse(beforeHoldings[0].trading_info); } catch(e) {}
            console.log(`\n=== 对比: 调仓前 ${beforeDate} | 持仓数: ${Object.keys(holdings).length} ===`);
            Object.entries(holdings).sort((a,b) => parseFloat(b[1]) - parseFloat(a[1])).forEach(([code, w]) => {
                console.log(`  ${code}: ${w}`);
            });
        }
    }
    
    if (afterRows.length > 0) {
        const afterDate = afterRows[0].trade_date;
        const [afterHoldings] = await conn.execute(
            `SELECT trading_info, trade_price FROM ${tableName} 
             WHERE trade_date = ? ORDER BY update_time DESC LIMIT 1`,
            [afterDate]
        );
        if (afterHoldings.length > 0) {
            let holdings = {};
            try { holdings = JSON.parse(afterHoldings[0].trading_info); } catch(e) {}
            console.log(`\n=== 对比: 调仓后 ${afterDate} | 持仓数: ${Object.keys(holdings).length} ===`);
            Object.entries(holdings).sort((a,b) => parseFloat(b[1]) - parseFloat(a[1])).forEach(([code, w]) => {
                console.log(`  ${code}: ${w}`);
            });
        }
    }
    
    await conn.end();
}

main().catch(e => { console.error("Error:", e.message); process.exit(1); });
