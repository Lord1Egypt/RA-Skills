const mysql = require('mysql2');

// 数据库连接配置
const dbConfig = {
  host: '47.121.180.199',
  port: 3306,
  user: 'display',
  password: 'display999!',
  database: 'db_strategy'
};

const connection = mysql.createConnection(dbConfig);
connection.connect((err) => {
  if (err) {
    console.error('连接错误', err);
    return;
  }
  // 检查表结构
  const query = `DESCRIBE strategy_ml16w1lg_stg000001`;
  connection.query(query, (err, result) => {
    if (err) {
      console.error('查询错误', err);
      connection.end();
      return;
    }
    console.log('表结构:');
    console.log(result);
    connection.end();
  });
});
