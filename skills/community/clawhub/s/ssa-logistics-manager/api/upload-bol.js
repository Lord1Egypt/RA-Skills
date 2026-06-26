const multer = require('multer');
const path = require('path');
const fs = require('fs');
const { LogisticsRecord } = require('../models/logistics_model');

// 配置 multer 用于文件存储
const bolStorage = multer.diskStorage({
  destination: (req, file, cb) => {
    const uploadPath = path.join(__dirname, '..', 'documents', 'bill_of_lading');
    fs.mkdirSync(uploadPath, { recursive: true });
    cb(null, uploadPath);
  },
  filename: (req, file, cb) => {
    cb(null, `${Date.now()}-${file.originalname}`);
  }
});

const uploadBol = multer({ storage: bolStorage });

/**
 * 上传并归档提单
 * @param {string} logisticsId - 物流记录 ID
 * @param {object} file - 上传的文件
 * @param {object} metadata - 提单元数据 (bolNumber, carrier, trackingNumber)
 * @returns {object} 更新后的物流记录
 */
async function uploadBillOfLading(logisticsId, file, metadata = {}) {
  // 在实际应用中，这里会从数据库加载记录
  // 简化版本：返回文件信息
  return {
    logisticsId,
    bolNumber: metadata.bolNumber || `BOL-${Date.now()}`,
    filepath: file.path,
    uploadDate: new Date(),
    carrier: metadata.carrier || '',
    trackingNumber: metadata.trackingNumber || ''
  };
}

module.exports = {
  uploadBol,
  uploadBillOfLading
};
