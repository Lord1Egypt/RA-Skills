const mysql = require('mysql2/promise');

async function main() {
    const conn = await mysql.createConnection({
        host: '47.121.180.199',
        port: 3306,
        user: 'display',
        password: 'display999!',
        database: 'db_strategy'
    });

    const [strategies] = await conn.execute('SELECT strategy_table, strategy_name_cn, strategy_id FROM strategy_information');
    
    const results = [];
    for (const stg of strategies) {
        try {
            const [rows] = await conn.execute(
                `SELECT trading_info, trade_date FROM ${stg.strategy_table} WHERE trading_info LIKE '%300308%'`
            );
            if (rows.length > 0) {
                const latest = rows[rows.length - 1];
                const oldest = rows[0];
                let lWeight = 'N/A';
                try { lWeight = JSON.parse(latest.trading_info)['300308.SZ'] || 'N/A'; } catch(e) {}
                results.push({
                    name: stg.strategy_name_cn,
                    id: stg.strategy_id,
                    firstDate: oldest.trade_date,
                    lastDate: latest.trade_date,
                    count: rows.length,
                    lastWeight: lWeight
                });
            }
        } catch(e) {
            // skip
        }
    }
    
    if (results.length > 0) {
        console.log('=== 历史上持有过300308.SZ(中际旭创)的策略 ===');
        results.sort((a,b) => b.count - a.count);
        results.forEach(r => {
            console.log(`策略:${r.name} | ID:${r.id} | 持有次数:${r.count} | 首次:${r.firstDate} | 末次:${r.lastDate} | 末次权重:${r.lastWeight}`);
        });
    } else {
        console.log('历史上也没有策略持有过300308.SZ');
    }
    
    // 额外查一下推荐策略最新持仓Top5
    console.log('\n=== 推荐策略最新持仓Top5 ===');
    const [recStg] = await conn.execute("SELECT strategy_table, strategy_name_cn FROM strategy_information WHERE if_recommended=1");
    for (const stg of recStg) {
        try {
            const [rows] = await conn.execute(
                `SELECT trading_info, trade_date FROM ${stg.strategy_table} ORDER BY trade_date DESC LIMIT 1`
            );
            if (rows.length > 0) {
                const parsed = JSON.parse(rows[0].trading_info);
                const sorted = Object.entries(parsed).sort((a,b) => b[1] - a[1]).slice(0, 5);
                console.log(`\n【${stg.strategy_name_cn}】 日期:${rows[0].trade_date}`);
                sorted.forEach(([code, weight]) => {
                    console.log(`  ${code}: ${(weight * 100).toFixed(2)}%`);
                });
            }
        } catch(e) {}
    }
    
    await conn.end();
}

main().catch(e => console.error(e));
