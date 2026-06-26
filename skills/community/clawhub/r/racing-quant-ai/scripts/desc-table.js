const mysql = require('mysql2');

const dbConfig = {
  host: '47.121.180.199',
  port: 3306,
  user: 'display',
  password: 'display999!',
  database: 'db_strategy'
};

const connection = mysql.createConnection(dbConfig);
const tableName = 'strategy_train4pdtlag1wadj_stgml0002';

connection.connect((err) => {
  if (err) {
    console.error('连接错误:', err);
    process.exit(1);
  }
  connection.query(`DESCRIBE ${tableName}`, (err, results) => {
    if (err) {
      console.error('查询错误:', err);
      connection.end();
      return;
    }
    console.log('表结构:');
    console.log(results);
    connection.end();
  });
});
