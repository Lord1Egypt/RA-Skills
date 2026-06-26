// skills/logistics/api/logistics_api.js
const { LogisticsRecord, LogisticsStatus, TransportMode } = require('../models/logistics_model');

// 内存存储（后续替换为实际数据库）
let logisticsRecords = [];

/**
 * 创建物流记录
 * @param {object} recordData - 物流记录数据
 * @returns {LogisticsRecord} 创建的物流记录对象
 */
async function createLogisticsRecord(recordData) {
  if (!recordData.orderId || !recordData.customerId) {
    throw new Error('创建物流记录需要 orderId 和 customerId。');
  }
  const newRecord = new LogisticsRecord(recordData);
  logisticsRecords.push(newRecord);
  return newRecord.toObject();
}

/**
 * 查询物流记录列表
 * @param {object} filters - 过滤条件
 * @returns {Array<object>}
 */
async function listLogisticsRecords(filters = {}) {
  let filtered = logisticsRecords;
  if (filters.status) filtered = filtered.filter(r => r.status === filters.status);
  if (filters.orderId) filtered = filtered.filter(r => r.orderId === filters.orderId);
  return filtered.map(r => r.getOverview());
}

/**
 * 获取物流记录详情
 * @param {string} logisticsId - 物流 ID
 * @returns {object|null}
 */
async function getLogisticsDetails(logisticsId) {
  const rec = logisticsRecords.find(r => r.logisticsId === logisticsId);
  return rec ? rec.toObject() : null;
}

/**
 * 更新物流状态
 * @param {string} logisticsId - 物流 ID
 * @param {string} newStatus - 新状态
 * @returns {object}
 */
async function updateLogisticsStatus(logisticsId, newStatus) {
  const rec = logisticsRecords.find(r => r.logisticsId === logisticsId);
  if (!rec) throw new Error(`物流记录 ${logisticsId} 未找到。`);
  rec.updateStatus(newStatus);
  return rec.toObject();
}

/**
 * 更新物流追踪信息
 * @param {string} logisticsId - 物流 ID
 * @param {object} trackingData - 追踪数据
 * @returns {object}
 */
async function updateTrackingInfo(logisticsId, trackingData) {
  const rec = logisticsRecords.find(r => r.logisticsId === logisticsId);
  if (!rec) throw new Error(`物流记录 ${logisticsId} 未找到。`);
  rec.updateTracking(trackingData);
  return rec.toObject();
}

/**
 * 生成报关单据
 * @param {string} logisticsId - 物流 ID
 * @param {string} docType - 单据类型 (invoice/packing_list/contract)
 * @returns {object}
 */
async function generateCustomsDoc(logisticsId, docType) {
  const rec = logisticsRecords.find(r => r.logisticsId === logisticsId);
  if (!rec) throw new Error(`物流记录 ${logisticsId} 未找到。`);
  return rec.generateCustomsDoc(docType);
}

module.exports = {
  createLogisticsRecord,
  listLogisticsRecords,
  getLogisticsDetails,
  updateLogisticsStatus,
  updateTrackingInfo,
  generateCustomsDoc,
  LogisticsStatus,
  TransportMode
};
