const mysql = require('mysql2/promise');
async function main() {
    const conn = await mysql.createConnection({
        host: '47.121.180.199', port: 3306, user: 'display', password: 'display999!', database: 'db_strategy'
    });

    // 查持有300308的策略的表名
    const ids = ['stg000007','stgat0007','stg000005','stgat0006','stgat0004','stgat0003','stgat0008','stgat0010','stgat0011','stgat0012','stgat0016'];
    const [strategies] = await conn.execute(
        `SELECT strategy_table, strategy_name_cn, strategy_id FROM strategy_information WHERE strategy_id IN (?)`,
        [ids]
    );
    
    for (const stg of strategies) {
        console.log(`策略:${stg.strategy_name_cn} | 表名:${stg.strategy_table} | ID:${stg.strategy_id}`);
        
        // 查最后一次持有300308的权重
        try {
            const [rows] = await conn.execute(
                `SELECT trading_info, trade_date FROM ${stg.strategy_table} WHERE trading_info LIKE '%300308%' ORDER BY trade_date DESC LIMIT 1`
            );
            if (rows.length > 0) {
                const parsed = JSON.parse(rows[0].trading_info);
                const w = parsed['300308.SZ'];
                console.log(`  最后持有日期:${rows[0].trade_date} 权重:${w} 持仓数:${Object.keys(parsed).length}`);
            }
        } catch(e) { console.log(`  查询失败:${e.message}`); }
    }

    // 推荐策略最新持仓Top5
    console.log('\n=== 推荐策略最新持仓Top5 ===');
    const [recStg] = await conn.execute('SELECT strategy_table, strategy_name_cn FROM strategy_information WHERE if_recommended=1');
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
        } catch(e) { console.log(`【${stg.strategy_name_cn}】查询失败:${e.message}`); }
    }

    await conn.end();
}
main().catch(e => console.error(e));
