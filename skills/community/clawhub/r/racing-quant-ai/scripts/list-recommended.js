const mysql = require('mysql2');

// 数据库连接配置
const dbConfig = {
  host: '47.121.180.199',
  port: 3306,
  user: 'display',
  password: 'display999!',
  database: 'db_strategy'
};

function listRecommended() {
  return new Promise((resolve, reject) => {
    const connection = mysql.createConnection(dbConfig);
    connection.connect((err) => {
      if (err) {
        reject(err);
        connection.end();
        return;
      }
      const query = 'SELECT strategy_name_cn, strategy_table, strategy_desc, if_recommended FROM strategy_information WHERE if_recommended = 1';
      connection.query(query, (err, results) => {
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

listRecommended()
  .then(results => {
    console.log(`推荐策略列表 (共 ${results.length} 条):\n`);
    results.forEach((row, i) => {
      console.log(`${i+1}. **${row.strategy_name_cn}**`);
      console.log(`   持仓表: ${row.strategy_table}`);
      console.log(`   描述: ${row.strategy_desc}`);
      console.log();
    });
  })
  .catch(err => {
    console.error('错误:', err);
  });
