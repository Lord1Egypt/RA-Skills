const mysql = require('mysql2');

// 数据库连接配置
const dbConfig = {
  host: '47.121.180.199',
  port: 3306,
  user: 'display',
  password: 'display999!',
  database: 'db_strategy'
};

/**
 * 获取所有策略
 * @returns {Promise<Array>} 策略列表
 */
function getAllStrategies() {
  return new Promise((resolve, reject) => {
    const connection = mysql.createConnection(dbConfig);
    connection.connect((err) => {
      if (err) {
        reject(err);
        connection.end();
        return;
      }
      const query = 'SELECT * FROM strategy_information ORDER BY online_date DESC';
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

/**
 * 根据关键词搜索策略（搜索中文名称、简介、描述）
 * @param {string} keyword 搜索关键词
 * @returns {Promise<Array>} 匹配的策略列表
 */
function searchStrategies(keyword) {
  return new Promise((resolve, reject) => {
    const connection = mysql.createConnection(dbConfig);
    connection.connect((err) => {
      if (err) {
        reject(err);
        connection.end();
        return;
      }
      const query = `SELECT * FROM strategy_information WHERE (strategy_name_cn LIKE ? OR strategy_summ LIKE ? OR strategy_desc LIKE ?) ORDER BY online_date DESC`;
      const searchKey = `%${keyword}%`;
      connection.query(query, [searchKey, searchKey, searchKey], (err, results) => {
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

/**
 * 根据策略分类筛选
 * @param {string} category 分类名称
 * @returns {Promise<Array>} 筛选后的策略列表
 */
function getStrategiesByCategory(category) {
  return new Promise((resolve, reject) => {
    const connection = mysql.createConnection(dbConfig);
    connection.connect((err) => {
      if (err) {
        reject(err);
        connection.end();
        return;
      }
      const query = `SELECT * FROM strategy_information WHERE strategy_cat = ? ORDER BY online_date DESC`;
      connection.query(query, [category], (err, results) => {
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

/**
 * 根据用户需求匹配推荐策略，从描述中匹配关键词
 * @param {string} requirement 用户需求描述
 * @returns {Promise<Array>} 匹配的推荐策略列表
 */
function matchStrategiesByRequirement(requirement) {
  return new Promise((resolve, reject) => {
    const connection = mysql.createConnection(dbConfig);
    connection.connect((err) => {
      if (err) {
        reject(err);
        connection.end();
        return;
      }
      // 匹配策略描述、简介、中文名称中包含需求关键词的策略
      const query = `SELECT * FROM strategy_information WHERE (strategy_desc LIKE ? OR strategy_summ LIKE ? OR strategy_name_cn LIKE ?) ORDER BY if_recommended DESC, online_date DESC`;
      const searchKey = `%${requirement}%`;
      connection.query(query, [searchKey, searchKey, searchKey], (err, results) => {
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

/**
 * 根据策略名称获取策略最新持仓，并且匹配股票最新基础信息
 * @param {string} strategyName 策略名称（中文或英文）
 * @returns {Promise<Object|null>} 最新持仓信息，包含每只股票的最新信息，找不到返回null
 */
function getStrategyLatestPosition(strategyName) {
  return new Promise((resolve, reject) => {
    const connection = mysql.createConnection(dbConfig);
    connection.connect((err) => {
      if (err) {
        reject(err);
        connection.end();
        return;
      }
      // 先找到策略对应的持仓表名
      let query = `SELECT * FROM strategy_information WHERE strategy_name_cn LIKE ? OR strategy_name = ? LIMIT 1`;
      connection.query(query, [`%${strategyName}%`, strategyName], (err, strategyResults) => {
        if (err) {
          reject(err);
          connection.end();
          return;
        }
        if (strategyResults.length === 0) {
          resolve(null);
          connection.end();
          return;
        }
        const strategyInfo = strategyResults[0];
        const tableName = strategyInfo.strategy_table;
        if (!tableName) {
          resolve(null);
          connection.end();
          return;
        }
        // 从持仓表按日期排序，取最新一条记录
        query = `SELECT * FROM ${connection.escapeId(tableName)} ORDER BY trade_date DESC LIMIT 1`;
        connection.query(query, (err, positionResults) => {
          if (err) {
            reject(err);
            connection.end();
            return;
          }
          if (positionResults.length === 0) {
            resolve({strategy: strategyInfo, positions: []});
            connection.end();
            return;
          }
          
          const latestPosition = positionResults[0];
          // 提取所有股票代码，匹配每个股票的最新信息
          // 持仓表中，股票代码字段一般是code，权重weight
          const positions = [];
          // 遍历持仓对象，收集所有股票代码
          // 假设格式：每只股票是 code: 000598.SZ, weight: 0.0909 这样的结构
          // 我们遍历所有字段，提取出所有code和weight对
          const stockCodes = [];
          const stockWeights = {};
          
          for (const key in latestPosition) {
            if (key.endsWith('_code') || key === 'code') {
              let stockCode = latestPosition[key];
              if (stockCode) {
                // 处理可能没有后缀.SZ/.SH的情况
                if (!stockCode.includes('.')) {
                  // 简单处理：0开头是SZ，6开头是SH
                  if (stockCode.startsWith('0') || stockCode.startsWith('3')) {
                    stockCode = `${stockCode}.SZ`;
                  } else if (stockCode.startsWith('6') || stockCode.startsWith('9')) {
                    stockCode = `${stockCode}.SH`;
                  }
                }
                stockCodes.push(stockCode);
                // 找对应的权重
                let weightKey = key.replace('_code', '_weight');
                if (latestPosition[weightKey] !== undefined) {
                  stockWeights[stockCode] = latestPosition[weightKey];
                } else if (key === 'code') {
                  // 可能是多行格式，刚才假设不对，单条记录就是一个持仓
                  // 直接处理成一个
                  if (stockWeights[stockCode] === undefined && latestPosition.weight !== undefined) {
                    stockWeights[stockCode] = latestPosition.weight;
                  }
                }
              }
            }
          }
          
          // 如果上面没提取到，说明表结构是每行一个持仓，我们取所有最新交易日的持仓
          if (stockCodes.length === 0) {
            // 重新获取该交易日所有持仓
            const tradeDate = latestPosition.trade_date;
            query = `SELECT * FROM ${connection.escapeId(tableName)} WHERE trade_date = ?`;
            connection.query(query, [tradeDate], (err, allPositions) => {
              if (err) {
                reject(err);
                connection.end();
                return;
              }
              allPositions.forEach(pos => {
                let stockCode = pos.code || pos.stock_code;
                if (!stockCode) return;
                if (!stockCode.includes('.')) {
                  if (stockCode.startsWith('0') || stockCode.startsWith('3')) {
                    stockCode = `${stockCode}.SZ`;
                  } else if (stockCode.startsWith('6') || stockCode.startsWith('9')) {
                    stockCode = `${stockCode}.SH`;
                  }
                }
                stockCodes.push(stockCode);
                stockWeights[stockCode] = pos.weight || pos.weight_pct || 0;
              });
              
              // 查询股票信息并返回
              fetchStockInfos(stockCodes, stockWeights, connection, strategyInfo, latestPosition, resolve, reject);
            });
          } else {
            // 单条记录多只股票格式，直接查询
            fetchStockInfos(stockCodes, stockWeights, connection, strategyInfo, latestPosition, resolve, reject);
          }
        });
      });
    });
  });
}

/**
 * 内部方法：批量查询股票最新信息
 */
function fetchStockInfos(stockCodes, stockWeights, connection, strategyInfo, latestPosition, resolve, reject) {
  if (stockCodes.length === 0) {
    resolve({
      strategy: strategyInfo,
      latestTradeDate: latestPosition.trade_date,
      positions: [],
      updateTime: latestPosition.update_time || latestPosition.updatetime || null
    });
    connection.end();
    return;
  }
  
  // 对每个股票代码，取它最新交易日的信息
  const placeholders = stockCodes.map(() => '?').join(',');
  const query = `
    SELECT * FROM stock_info_display 
    WHERE code IN (${placeholders}) 
    ORDER BY code, trade_date DESC
  `;
  
  connection.query(query, stockCodes, (err, results) => {
    if (err) {
      reject(err);
      connection.end();
      return;
    }
    
    // 每个股票只取最新一条
    const latestStockInfos = {};
    results.forEach(row => {
      if (!latestStockInfos[row.code] || row.trade_date > latestStockInfos[row.code].trade_date) {
        latestStockInfos[row.code] = row;
      }
    });
    
    // 整合结果
    const positions = stockCodes.map(code => {
      const info = latestStockInfos[code] || {};
      return {
        code: code,
        name: info.name || '未知名称',
        industryL1: info.ind_swl1 || '未知行业',
        industryL2: info.ind_swl2 || '未知细分',
        weight: stockWeights[code] || 0,
        change1d: info.pct_change_1d || null,
        change5d: info.pct_change_5d || null,
        change20d: info.pct_change_20d || null
      };
    });
    
    resolve({
      strategy: {
        id: strategyInfo.strategy_id,
        name: strategyInfo.strategy_name_cn || strategyInfo.strategy_name,
        table: strategyInfo.strategy_table
      },
      latestTradeDate: latestPosition.trade_date,
      updateTime: latestPosition.update_time || latestPosition.updatetime || null,
      positions: positions.sort((a, b) => b.weight - a.weight)
    });
    
    connection.end();
  });
}

// 命令行参数处理
if (require.main === module) {
  const args = process.argv.slice(2);
  const action = args[0];
  
  if (!action || action === 'list') {
    // 默认列出所有策略
    getAllStrategies()
      .then(results => {
        console.log(JSON.stringify(results, null, 2));
        console.log(`\n共查询到 ${results.length} 条策略`);
        process.exit(0);
      })
      .catch(err => {
        console.error('查询错误:', err);
        process.exit(1);
      });
  } else if (action === 'search' && args[1]) {
    // 搜索关键词
    searchStrategies(args[1])
      .then(results => {
        console.log(JSON.stringify(results, null, 2));
        console.log(`\n找到 ${results.length} 条匹配结果`);
        process.exit(0);
      })
      .catch(err => {
        console.error('搜索错误:', err);
        process.exit(1);
      });
  } else if (action === 'match' && args[1]) {
    // 需求匹配推荐
    matchStrategiesByRequirement(args[1])
      .then(results => {
        console.log(JSON.stringify(results, null, 2));
        console.log(`\n找到 ${results.length} 条匹配策略`);
        process.exit(0);
      })
      .catch(err => {
        console.error('匹配错误:', err);
        process.exit(1);
      });
  } else if (action === 'position' && args[1]) {
    // 获取最新持仓
    getStrategyLatestPosition(args[1])
      .then(result => {
        if (!result) {
          console.log('未找到对应策略或持仓信息');
          process.exit(0);
        }
        console.log(`
策略名称: ${result.strategy.name}
策略ID: ${result.strategy.id}
持仓日期: ${result.latestTradeDate}
更新时间: ${result.updateTime || '未知'}
----------------------------------------
持仓明细 (按权重从高到低):
`);
        // 表格输出
        console.log('| 股票代码 | 股票名称 | 行业 | 权重(%) | 日涨跌(%) | 5日涨跌(%) | 20日涨跌(%) |');
        console.log('|----------|----------|------|----------|-----------|------------|-------------|');
        result.positions.forEach(pos => {
          const weight = (pos.weight * 100).toFixed(2);
          const c1d = pos.change1d !== null ? pos.change1d.toFixed(2) : '-';
          const c5d = pos.change5d !== null ? pos.change5d.toFixed(2) : '-';
          const c20d = pos.change20d !== null ? pos.change20d.toFixed(2) : '-';
          console.log(`| ${pos.code} | ${pos.name} | ${pos.industryL2 || pos.industryL1} | ${weight} | ${c1d} | ${c5d} | ${c20d} |`);
        });
        console.log(`\n总计: ${result.positions.length} 只股票`);
        process.exit(0);
      })
      .catch(err => {
        console.error('查询错误:', err);
        process.exit(1);
      });
  } else if (action === 'analyze' && args[1]) {
    // 分析持仓，输出结构化分析数据
    getStrategyPositionWithAnalyzeData(args[1])
      .then(result => {
        if (!result) {
          console.log('未找到对应策略或持仓信息');
          process.exit(0);
        }
        // 输出JSON格式分析数据，供AI分析
        console.log(JSON.stringify(result, null, 2));
        process.exit(0);
      })
      .catch(err => {
        console.error('分析错误:', err);
        process.exit(1);
      });
  } else {
    console.log(`
用法: node read-strategies.js [action] [parameter]

Actions:
  list               - 列出所有策略 (默认)
  search <keyword>   - 关键词搜索策略
  match <requirement> - 根据用户需求匹配推荐策略
  position <name>    - 获取策略最新持仓（含股票最新信息）
  analyze <name>     - 输出策略持仓结构化数据，用于AI分析
    `);
    process.exit(0);
  }
}

/**
 * 获取策略最新持仓并生成分析数据表格，用于后续分析推荐
 * @param {string} strategyName 策略名称
 * @returns {Promise<Object>} 包含持仓和股票信息的完整分析数据
 */
async function getStrategyPositionWithAnalyzeData(strategyName) {
  const positionData = await getStrategyLatestPosition(strategyName);
  if (!positionData) {
    return null;
  }
  
  // 整理分析需要的数据，输出结构化数据给分析模块
  const analyzeData = {
    ...positionData,
    // 整理每只股票的关键指标，供后续基本面和行情分析
    stocks: positionData.positions.map(pos => ({
      code: pos.code,
      name: pos.name,
      industry: `${pos.industryL1} - ${pos.industryL2}`,
      weight: pos.weight,
      recentPerformance: {
        change1d: pos.change1d,
        change5d: pos.change5d,
        change20d: pos.change20d
      }
    }))
  };
  
  return analyzeData;
}

module.exports = {
  getAllStrategies,
  searchStrategies,
  getStrategiesByCategory,
  matchStrategiesByRequirement,
  getStrategyLatestPosition,
  getStrategyPositionWithAnalyzeData
};
