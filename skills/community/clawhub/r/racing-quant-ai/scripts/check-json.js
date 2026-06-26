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
  const dateQuery = `SELECT DISTINCT trade_date FROM ${tableName} ORDER BY trade_date DESC LIMIT 1`;
  connection.query(dateQuery, (err, dateResults) => {
    if (err) {
      console.error('查询错误:', err);
      connection.end();
      return;
    }
    const latestDate = dateResults[0].trade_date;
    console.log('Latest date:', latestDate);
    const posQuery = `SELECT * FROM ${tableName} WHERE trade_date = ? LIMIT 1`;
    connection.query(posQuery, [latestDate], (err, posResults) => {
      if (err) {
        console.error('查询错误:', err);
        connection.end();
        return;
      }
      console.log('\nRow type:', typeof posResults[0].trading_info);
      console.log('\nRow content:');
      console.dir(posResults[0], { depth: null });
      connection.end();
    });
  });
});
