const mysql = require('mysql2');

// 数据库连接配置
const dbConfig = {
  host: '47.121.180.199',
  port: 3306,
  user: 'display',
  password: 'display999!',
  database: 'db_strategy'
};

function getStrategyDetail(strategyNameCn) {
  return new Promise((resolve, reject) => {
    const connection = mysql.createConnection(dbConfig);
    connection.connect((err) => {
      if (err) {
        reject(err);
        connection.end();
        return;
      }
      const query = 'SELECT * FROM strategy_information WHERE strategy_name_cn LIKE ?';
      connection.query(query, [`%${strategyNameCn}%`], (err, results) => {
        if (err) {
          reject(err);
          connection.end();
          return;
        }
        resolve(results);
        connection.end();
      });
    });
  });
}

// 搜索波动自适应
getStrategyDetail('波动自适应')
  .then(results => {
    console.log(`找到 ${results.length} 条结果:\n`);
    results.forEach((row, i) => {
      console.log(`${i+1}. 策略名称: ${row.strategy_name_cn}`);
      console.log(`   持仓表: ${row.strategy_table}`);
      console.log(`   描述: ${row.strategy_desc}`);
      console.log();
    });
  })
  .catch(err => {
    console.error('错误:', err);
  });
