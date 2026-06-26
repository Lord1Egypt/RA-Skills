const mysql = require('mysql2');

// 数据库连接配置
const dbConfig = {
  host: '47.121.180.199',
  port: 3306,
  user: 'display',
  password: 'display999!',
  database: 'db_strategy'
};

function getLatestHoldings(tableName) {
  return new Promise((resolve, reject) => {
    const connection = mysql.createConnection(dbConfig);
    connection.connect((err) => {
      if (err) {
        reject(err);
        connection.end();
        return;
      }
      // 获取最新持仓日期
      const dateQuery = `SELECT DISTINCT trade_date FROM ${tableName} ORDER BY trade_date DESC LIMIT 1`;
      connection.query(dateQuery, (err, dateResult) => {
        if (err) {
          reject(err);
          connection.end();
          return;
        }
        const latestDate = dateResult[0].trade_date;
        // 获取最新持仓
        const holdingsQuery = `SELECT trading_info FROM ${tableName} WHERE trade_date = ?`;
        connection.query(holdingsQuery, [latestDate], (err, holdingsResult) => {
          if (err) {
            reject(err);
            connection.end();
            return;
          }
          if (holdingsResult.length === 0) {
            reject('没有找到持仓数据');
            connection.end();
            return;
          }
          const tradingInfo = JSON.parse(holdingsResult[0].trading_info);
          let holdings = [];
          if (Array.isArray(tradingInfo)) {
            holdings = tradingInfo;
          } else if (tradingInfo.holdings) {
            holdings = tradingInfo.holdings;
          } else if (tradingInfo.stocks) {
            holdings = tradingInfo.stocks;
          }
          resolve({
            latestDate: latestDate,
            holdings: holdings
          });
          connection.end();
        });
      });
    });
  });
}

// 机器学习1号持仓表
const tableName = 'strategy_ml16w1lg_stg000001';
getLatestHoldings(tableName)
  .then(result => {
    console.log(`### 机器学习1号 - 最新持仓\n`);
    console.log(`**持仓日期**: ${result.latestDate}\n`);
    console.log(`**持仓个股 (共 ${result.holdings.length} 只):\n`);
    console.log(`| # | 代码 | 名称 | 权重 |`);
    console.log(`|---|------|------|------|`);
    result.holdings.forEach((row, i) => {
      const code = row.code || row.stock_code || row.ticker;
      const name = row.name || row.stock_name;
      const weight = row.weight || row.weight_pct || 5;
      console.log(`| ${i+1} | ${code} | ${name} | ${(weight*100).toFixed(2)}% |`);
    });
    console.log(`\n`);
  })
  .catch(err => {
    console.error('错误:', err);
  });
