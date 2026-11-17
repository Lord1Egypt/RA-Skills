const mysql = require('mysql2/promise');
const fs = require('fs');
async function main() {
    const conn = await mysql.createConnection({
        host: '47.121.180.199', port: 3306,
        user: 'display', password: 'display999!',
        database: 'db_strategy'
    });
    const [rows] = await conn.execute(
        'SELECT trade_date, trading_info FROM strategy_huaxiaetftiming_stgetf0001 ORDER BY trade_date ASC'
    );
    const result = rows.map(r => ({
        date: r.trade_date,
        holdings: typeof r.trading_info === 'string' ? JSON.parse(r.trading_info) : r.trading_info
    }));
    fs.writeFileSync('/tmp/holdings_stgetf0001.json', JSON.stringify(result));
    console.log('OK ' + result.length + ' days');
    await conn.end();
}
main().catch(e => { console.error(e.message); process.exit(1); });
