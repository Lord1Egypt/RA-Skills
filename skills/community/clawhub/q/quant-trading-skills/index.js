const { getCache, setCache, log, validateParams } = require('./lib/utils');
const { fetchMarketData, fetchFinanceData, fetchFundFlowData, fetchPublicOpinionData, fetchAllStockCodes, batchFetchMarketData, batchFetchLhbData, batchFetchNorthFlowData, batchFetchSentimentData, batchFetchFinancialData } = require('./lib/dataFetcher');

async function execute(params, context) {
  try {
    log('info', '开始执行 quant_trading-skills Skill', { params, context });
    
    const validationErrors = validateParams(params);
    if (validationErrors.length > 0) {
      log('error', '参数校验失败', { errors: validationErrors });
      return {
        success: false,
        data: null,
        message: `参数校验失败: ${validationErrors.join(', ')}`
      };
    }
    
    if (params.type === 'batch_sentiment') {
      log('info', '开始批量拉取舆情数据');
      const result = await batchFetchSentimentData(params);
      log('info', '批量拉取舆情数据完成', { stats: result.stats });
      return {
        success: result.success,
        data: result.stats,
        message: result.message
      };
    }
    
    if (params.type === 'batch_market') {
      log('info', '开始批量拉取行情数据');
      const options = params.batch_market || {};
      const result = await batchFetchMarketData({
        status_file: options.status_file,
        data_path: options.data_path,
        default_years: options.default_years || 5,
        max_retries: options.max_retries || 3,
        progress_interval: options.progress_interval || 100
      });
      log('info', '批量拉取行情数据完成', { stats: result.stats });
      return {
        success: result.success,
        data: result,
        message: result.message
      };
    }
    
    if (params.type === 'batch_financial') {
      log('info', '开始批量拉取财报数据');
      const options = params.batch_financial || {};
      const result = await batchFetchFinancialData({
        status_file: options.status_file,
        data_path: options.data_path,
        default_years: options.default_years || 3,
        max_retries: options.max_retries || 3,
        progress_interval: options.progress_interval || 100
      });
      log('info', '批量拉取财报数据完成', { stats: result });
      return {
        success: true,
        data: result,
        message: '批量拉取财报数据完成'
      };
    }
    
    const cacheKey = `${params.type}_${params.symbol}_${params.period || ''}_${params.report_type || ''}`;
    
    const cachedData = getCache(cacheKey);
    if (cachedData) {
      log('info', '从缓存获取数据', { cacheKey });
      return {
        success: true,
        data: cachedData,
        message: '从缓存获取数据成功'
      };
    }
    
    let result;
    switch (params.type) {
      case 'market':
        result = await fetchMarketData(params.symbol, params.period, params.start_date, params.end_date);
        break;
      case 'finance':
        result = await fetchFinanceData(params.symbol, params.report_type);
        break;
      case 'fund_flow':
        result = await fetchFundFlowData(params.symbol);
        break;
      case 'public_opinion':
        result = await fetchPublicOpinionData(params.symbol);
        break;
      case 'stock_codes':
        result = await fetchAllStockCodes();
        break;
      case 'batch_lhb':
        result = await batchFetchLhbData(params.status_file, params.data_path);
        break;
      case 'batch_north_flow':
        result = await batchFetchNorthFlowData({
          status_file: params.status_file,
          data_path: params.data_path,
          default_years: params.default_years
        });
        break;
      default:
        throw new Error('不支持的数据类型');
    }
    
    setCache(cacheKey, result);
    log('info', '数据缓存成功', { cacheKey });
    
    log('info', '数据获取成功', { type: params.type, symbol: params.symbol });
    return {
      success: true,
      data: result,
      message: '数据获取成功'
    };
  } catch (error) {
    log('error', '执行失败', { error: error.message });
    return {
      success: false,
      data: null,
      message: `执行失败: ${error.message}`
    };
  }
}

module.exports = {
  execute
};
