
const mysql = require('mysql2/promise');
async function main() {
    const conn = await mysql.createConnection({
        host: '47.121.180.199', port: 3306,
        user: 'display', password: 'display999!',
        database: 'db_strategy'
    });
    
    const [strategies] = await conn.execute('SELECT strategy_id, strategy_name_cn, strategy_table, if_recommended FROM strategy_information');
    console.log('总策略数: ' + strategies.length);
    
    let holders = [];
    for (const s of strategies) {
        try {
            const [rows] = await conn.execute('SELECT trade_date, trading_info FROM ' + s.strategy_table + ' ORDER BY trade_date DESC LIMIT 1');
            if (rows.length > 0) {
                let info = rows[0].trading_info;
                if (typeof info === 'string') { try { info = JSON.parse(info); } catch(e) { info = {}; } }
                const keys = Object.keys(info);
                const found = keys.filter(k => k.includes('688146'));
                if (found.length > 0) {
                    holders.push({
                        strategy: s.strategy_name_cn,
                        recommended: s.if_recommended,
                        date: rows[0].trade_date,
                        weight: info[found[0]]
                    });
                }
            }
        } catch(e) {}
    }
    
    console.log('\n=== 策略持仓扫描 ===');
    if (holders.length > 0) {
        holders.forEach(h => {
            console.log('策略: ' + h.strategy + ' | 推荐: ' + h.recommended + ' | 日期: ' + h.date + ' | 权重: ' + h.weight);
        });
    } else {
        console.log('当前无策略持有 688146');
    }
    
    await conn.end();
}
main().catch(e => console.error(e.message));
