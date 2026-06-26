/**
 * 售后分析报表 API 控制器
 * 
 * 提供售后数据分析接口：
 * - getComplaintAnalytics(dateRange) - 投诉统计分析
 * - getRepeatOrderAnalytics(dateRange) - 返单统计分析
 * - getSatisfactionAnalytics(dateRange) - 满意度统计分析
 * - getCustomerRiskAnalysis() - 客户风险分析
 * - getProductQualityAnalysis() - 产品质量分析
 */

const path = require('path');
const dayjs = require('dayjs');
const weekOfYear = require('dayjs/plugin/weekOfYear');
const analyticsModel = require('../../models/analytics_model');

dayjs.extend(weekOfYear);

/**
 * 投诉统计分析
 * @param {string} dateRange - 日期范围 (格式：YYYY-MM-DD_YYYY-MM-DD)
 * @returns {Object} 投诉分析报告
 */
function getComplaintAnalytics(dateRange) {
  try {
    const stats = analyticsModel.getComplaintStats(dateRange);
    const { startDate, endDate } = analyticsModel.parseDateRange(dateRange);

    return {
      success: true,
      reportType: 'complaint_analytics',
      dateRange: { startDate, endDate },
      generatedAt: dayjs().format('YYYY-MM-DD HH:mm:ss'),
      data: stats
    };
  } catch (error) {
    return {
      success: false,
      error: error.message
    };
  }
}

/**
 * 返单统计分析
 * @param {string} dateRange - 日期范围 (格式：YYYY-MM-DD_YYYY-MM-DD)
 * @returns {Object} 返单分析报告
 */
function getRepeatOrderAnalytics(dateRange) {
  try {
    const stats = analyticsModel.getRepeatOrderStats(dateRange);
    const { startDate, endDate } = analyticsModel.parseDateRange(dateRange);

    return {
      success: true,
      reportType: 'repeat_order_analytics',
      dateRange: { startDate, endDate },
      generatedAt: dayjs().format('YYYY-MM-DD HH:mm:ss'),
      data: stats
    };
  } catch (error) {
    return {
      success: false,
      error: error.message
    };
  }
}

/**
 * 满意度统计分析
 * @param {string} dateRange - 日期范围 (格式：YYYY-MM-DD_YYYY-MM-DD)
 * @returns {Object} 满意度分析报告
 */
function getSatisfactionAnalytics(dateRange) {
  try {
    const stats = analyticsModel.getSatisfactionStats(dateRange);
    const { startDate, endDate } = analyticsModel.parseDateRange(dateRange);

    return {
      success: true,
      reportType: 'satisfaction_analytics',
      dateRange: { startDate, endDate },
      generatedAt: dayjs().format('YYYY-MM-DD HH:mm:ss'),
      data: stats
    };
  } catch (error) {
    return {
      success: false,
      error: error.message
    };
  }
}

/**
 * 客户风险分析
 * @returns {Object} 客户风险分析报告
 */
function getCustomerRiskAnalysis() {
  try {
    const analysis = analyticsModel.getCustomerRiskAnalysis();

    return {
      success: true,
      reportType: 'customer_risk_analysis',
      generatedAt: dayjs().format('YYYY-MM-DD HH:mm:ss'),
      data: analysis
    };
  } catch (error) {
    return {
      success: false,
      error: error.message
    };
  }
}

/**
 * 产品质量分析
 * @returns {Object} 产品质量分析报告
 */
function getProductQualityAnalysis() {
  try {
    const analysis = analyticsModel.getProductQualityAnalysis();

    return {
      success: true,
      reportType: 'product_quality_analysis',
      generatedAt: dayjs().format('YYYY-MM-DD HH:mm:ss'),
      data: analysis
    };
  } catch (error) {
    return {
      success: false,
      error: error.message
    };
  }
}

/**
 * 获取综合分析摘要
 * @param {string} dateRange - 日期范围
 * @returns {Object} 综合分析摘要
 */
function getAnalyticsSummary(dateRange) {
  try {
    const complaintData = getComplaintAnalytics(dateRange);
    const repeatOrderData = getRepeatOrderAnalytics(dateRange);
    const satisfactionData = getSatisfactionAnalytics(dateRange);
    const riskData = getCustomerRiskAnalysis();
    const qualityData = getProductQualityAnalysis();

    return {
      success: true,
      reportType: 'analytics_summary',
      generatedAt: dayjs().format('YYYY-MM-DD HH:mm:ss'),
      summary: {
        complaints: complaintData.data.summary,
        repeatOrders: repeatOrderData.data.summary,
        satisfaction: satisfactionData.data.summary,
        customerRisk: riskData.data.summary,
        productQuality: qualityData.data.summary
      }
    };
  } catch (error) {
    return {
      success: false,
      error: error.message
    };
  }
}

module.exports = {
  getComplaintAnalytics,
  getRepeatOrderAnalytics,
  getSatisfactionAnalytics,
  getCustomerRiskAnalysis,
  getProductQualityAnalysis,
  getAnalyticsSummary
};
