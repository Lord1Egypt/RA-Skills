const mysql = require('mysql2');

// 数据库连接配置
const dbConfig = {
  host: '47.121.180.199',
  port: 3306,
  user: 'display',
  password: 'display999!',
  database: 'db_strategy'
};

function getLatestPositions(tableName, limit = 10) {
  return new Promise((resolve, reject) => {
    const connection = mysql.createConnection(dbConfig);
    connection.connect((err) => {
      if (err) {
        reject(err);
        connection.end();
        return;
      }
      // 获取最新一期日期
      const dateQuery = `SELECT DISTINCT trade_date FROM ${tableName} ORDER BY trade_date DESC LIMIT 1`;
      connection.query(dateQuery, (err, dateResults) => {
        if (err) {
          reject(err);
          connection.end();
          return;
        }
        if (dateResults.length === 0) {
          resolve([]);
          connection.end();
          return;
        }
        const latestDate = dateResults[0].trade_date;
        // 获取最新一期持仓，按权重排序取前N
        const posQuery = `SELECT * FROM ${tableName} WHERE trade_date = ? ORDER BY weight DESC LIMIT ?`;
        connection.query(posQuery, [latestDate, limit], (err, posResults) => {
          if (err) {
            reject(err);
            connection.end();
            return;
          }
          resolve({
            latestDate,
            positions: posResults
          });
          connection.end();
        });
      });
    });
  });
}

// 获取短周期机器学习趋势增强版的持仓
const tableName = 'strategy_train4pdtlag1wadj_stgml0002';
getLatestPositions(tableName, 10)
  .then(result => {
    console.log(`最新持仓日期: ${result.latestDate}`);
    console.log(`前10大权重持仓:\n`);
    result.positions.forEach((pos, i) => {
      console.log(`${i+1}. 股票代码: ${pos.stock_code}, 名称: ${pos.stock_name || 'N/A'}, 权重: ${(pos.weight * 100).toFixed(2)}%`);
    });
  })
  .catch(err => {
    console.error('错误:', err);
  });
