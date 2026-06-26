const { spawnSync } = require('child_process');
const path = require('path');
const { formatDate, formatDateTime } = require('./utils');

function executePythonScript(action, params) {
  try {
    const scriptPath = path.join(__dirname, '..', 'scripts', 'akshare_fetcher.py');
    const paramsJson = JSON.stringify(params);
    
    const result = spawnSync('py', ['-3.11', scriptPath, action], {
      input: paramsJson,
      encoding: 'utf8',
      timeout: 60000
    });
    
    if (result.error) {
      throw new Error(result.error.message);
    }
    
    if (result.stderr) {
      console.error('Python stderr:', result.stderr);
    }
    
    const output = result.stdout;
    const data = JSON.parse(output);
    
    if (data.error) {
      throw new Error(data.error);
    }
    
    return data;
  } catch (error) {
    console.error(`执行 Python 脚本失败: ${error.message}`);
    throw new Error(`执行 Python 脚本失败: ${error.message}`);
  }
}

function executePythonScriptLongRunning(action, params) {
  try {
    const scriptPath = path.join(__dirname, '..', 'scripts', 'akshare_fetcher.py');
    const paramsJson = JSON.stringify(params);
    
    const result = spawnSync('py', ['-3.11', scriptPath, action], {
      input: paramsJson,
      encoding: 'utf8',
      timeout: 3600000,
      maxBuffer: 1024 * 1024 * 10
    });
    
    if (result.error) {
      throw new Error(result.error.message);
    }
    
    if (result.stderr) {
      console.error('Python stderr:', result.stderr);
    }
    
    const output = result.stdout;
    const lines = output.trim().split('\n');
    const lastLine = lines[lines.length - 1];
    
    const data = JSON.parse(lastLine);
    
    if (data.error) {
      throw new Error(data.error);
    }
    
    return data;
  } catch (error) {
    console.error(`执行 Python 脚本失败: ${error.message}`);
    throw new Error(`执行 Python 脚本失败: ${error.message}`);
  }
}

// 获取行情数据
async function fetchMarketData(symbol, period = '1d', start_date, end_date) {
  try {
    const params = {
      symbol,
      period,
      start_date,
      end_date
    };
    
    const result = executePythonScript('market', params);
    return result;
  } catch (error) {
    console.error('获取行情数据失败:', error);
    throw new Error(`获取行情数据失败: ${error.message}`);
  }
}

// 获取财务数据
async function fetchFinanceData(symbol, report_type = 'quarter') {
  try {
    const params = {
      symbol,
      report_type
    };
    
    const result = executePythonScript('finance', params);
    return result;
  } catch (error) {
    console.error('获取财务数据失败:', error);
    throw new Error(`获取财务数据失败: ${error.message}`);
  }
}

// 获取资金流向数据
async function fetchFundFlowData(symbol) {
  try {
    const params = {
      symbol
    };
    
    const result = executePythonScript('fund_flow', params);
    return result;
  } catch (error) {
    console.error('获取资金流向数据失败:', error);
    throw new Error(`获取资金流向数据失败: ${error.message}`);
  }
}

// 获取舆情数据
async function fetchPublicOpinionData(symbol) {
  try {
    const params = {
      symbol
    };
    
    const result = executePythonScript('public_opinion', params);
    return result;
  } catch (error) {
    console.error('获取舆情数据失败:', error);
    throw new Error(`获取舆情数据失败: ${error.message}`);
  }
}

// 获取所有A股股票代码
async function fetchAllStockCodes() {
  try {
    const result = executePythonScript('stock_codes', {});
    return result;
  } catch (error) {
    console.error('获取股票代码失败:', error);
    throw new Error(`获取股票代码失败: ${error.message}`);
  }
}

async function batchFetchMarketData(options = {}) {
  try {
    const params = {
      status_file: options.status_file || 'config/fetch_status.json',
      data_path: options.data_path || 'data/market',
      default_years: options.default_years || 5,
      max_retries: options.max_retries || 3,
      progress_interval: options.progress_interval || 100
    };
    
    const scriptPath = path.join(__dirname, '..', 'scripts', 'akshare_fetcher.py');
    const paramsJson = JSON.stringify(params);
    
    const result = spawnSync('py', ['-3.11', scriptPath, 'batch_market'], {
      input: paramsJson,
      encoding: 'utf8',
      timeout: 3600000
    });
    
    if (result.error) {
      throw new Error(result.error.message);
    }
    
    if (result.stderr) {
      console.error('Python stderr:', result.stderr);
    }
    
    const output = result.stdout;
    const data = JSON.parse(output);
    
    if (data.error) {
      throw new Error(data.error);
    }
    
    return data;
  } catch (error) {
    console.error('批量拉取行情数据失败:', error);
    throw new Error(`批量拉取行情数据失败: ${error.message}`);
  }
}

async function batchFetchSentimentData(params = {}) {
  try {
    const defaultParams = {
      status_file: 'config/fetch_status.json',
      data_path: 'data/sentiment',
      default_years: 2,
      max_retries: 3,
      progress_interval: 50
    };
    
    const mergedParams = { ...defaultParams, ...params };
    
    const result = executePythonScriptLongRunning('batch_sentiment', mergedParams);
    return result;
  } catch (error) {
    console.error('批量获取舆情数据失败:', error);
    throw new Error(`批量获取舆情数据失败: ${error.message}`);
  }
}

async function batchFetchLhbData(statusFile = 'config/fetch_status.json', dataPath = 'data/lhb') {
  try {
    const params = {
      status_file: statusFile,
      data_path: dataPath
    };
    
    const result = executePythonScript('batch_lhb', params);
    return result;
  } catch (error) {
    console.error('批量获取龙虎榜数据失败:', error);
    throw new Error(`批量获取龙虎榜数据失败: ${error.message}`);
  }
}

// 批量获取北向资金数据
async function batchFetchNorthFlowData(params = {}) {
  try {
    const result = executePythonScript('batch_north_flow', params);
    return result;
  } catch (error) {
    console.error('批量获取北向资金数据失败:', error);
    throw new Error(`批量获取北向资金数据失败: ${error.message}`);
  }
}

async function batchFetchFinancialData(options = {}) {
  try {
    const params = {
      status_file: options.status_file || 'config/fetch_status.json',
      data_path: options.data_path || 'data/financial',
      default_years: options.default_years || 3,
      max_retries: options.max_retries || 3,
      progress_interval: options.progress_interval || 100
    };
    
    const scriptPath = path.join(__dirname, '..', 'scripts', 'akshare_fetcher.py');
    const paramsJson = JSON.stringify(params);
    
    const result = spawnSync('py', ['-3.11', scriptPath, 'batch_financial'], {
      input: paramsJson,
      encoding: 'utf8',
      timeout: 3600000
    });
    
    if (result.error) {
      throw new Error(result.error.message);
    }
    
    if (result.stderr) {
      console.error('Python stderr:', result.stderr);
    }
    
    const output = result.stdout;
    const data = JSON.parse(output);
    
    if (data.error) {
      throw new Error(data.error);
    }
    
    return data;
  } catch (error) {
    console.error('批量拉取财报数据失败:', error);
    throw new Error(`批量拉取财报数据失败: ${error.message}`);
  }
}

module.exports = {
  fetchMarketData,
  fetchFinanceData,
  fetchFundFlowData,
  fetchPublicOpinionData,
  fetchAllStockCodes,
  batchFetchMarketData,
  batchFetchSentimentData,
  batchFetchLhbData,
  batchFetchNorthFlowData,
  batchFetchFinancialData
};
