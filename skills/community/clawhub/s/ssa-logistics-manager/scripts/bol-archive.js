/**
 * 提单（Bill of Lading）归档模块
 * 
 * 功能：
 * 1. 保存提单 PDF 到本地归档目录
 * 2. 从邮件附件提取提单并归档
 * 3. 查询/下载已归档提单
 */

const fs = require('fs');
const path = require('path');

const BOL_ARCHIVE_DIR = path.join(__dirname, '../bill_of_lading');

/**
 * 确保归档目录存在
 */
function ensureArchiveDir() {
  if (!fs.existsSync(BOL_ARCHIVE_DIR)) {
    fs.mkdirSync(BOL_ARCHIVE_DIR, { recursive: true });
  }
}

/**
 * 保存提单 PDF 到归档目录
 * @param {string} logisticsId - 物流记录 ID
 * @param {Buffer} pdfBuffer - PDF 文件内容
 * @param {string} filename - 文件名（可选）
 * @returns {string} 保存后的文件路径
 */
function saveBol(logisticsId, pdfBuffer, filename = null) {
  ensureArchiveDir();
  
  const ext = filename ? path.extname(filename) : '.pdf';
  const safeLogisticsId = logisticsId.replace(/[^a-zA-Z0-9-_]/g, '_');
  const bolFilename = filename || `${safeLogisticsId}_BOL${ext}`;
  const bolPath = path.join(BOL_ARCHIVE_DIR, bolFilename);
  
  fs.writeFileSync(bolPath, pdfBuffer);
  
  console.log(`✅ 提单已归档：${bolPath}`);
  return bolPath;
}

/**
 * 从文件路径保存提单（用于本地文件归档）
 * @param {string} logisticsId - 物流记录 ID
 * @param {string} sourcePath - 源文件路径
 * @returns {string} 归档后的文件路径
 */
function saveBolFromFile(logisticsId, sourcePath) {
  ensureArchiveDir();
  
  if (!fs.existsSync(sourcePath)) {
    throw new Error(`源文件不存在：${sourcePath}`);
  }
  
  const ext = path.extname(sourcePath);
  const safeLogisticsId = logisticsId.replace(/[^a-zA-Z0-9-_]/g, '_');
  const bolFilename = `${safeLogisticsId}_BOL${ext}`;
  const bolPath = path.join(BOL_ARCHIVE_DIR, bolFilename);
  
  fs.copyFileSync(sourcePath, bolPath);
  
  console.log(`✅ 提单已归档：${bolPath}`);
  return bolPath;
}

/**
 * 获取物流记录的所有提单文件列表
 * @param {string} logisticsId - 物流记录 ID
 * @returns {Array<{filename: string, path: string, size: number, createdAt: Date}>}
 */
function listBols(logisticsId) {
  ensureArchiveDir();
  
  if (!fs.existsSync(BOL_ARCHIVE_DIR)) {
    return [];
  }
  
  const safeLogisticsId = logisticsId.replace(/[^a-zA-Z0-9-_]/g, '_');
  const prefix = `${safeLogisticsId}_BOL`;
  
  return fs.readdirSync(BOL_ARCHIVE_DIR)
    .filter(filename => filename.startsWith(prefix))
    .map(filename => {
      const filePath = path.join(BOL_ARCHIVE_DIR, filename);
      const stats = fs.statSync(filePath);
      return {
        filename,
        path: filePath,
        size: stats.size,
        createdAt: stats.birthtime
      };
    });
}

/**
 * 下载/读取提单文件
 * @param {string} filePath - 文件路径
 * @returns {Buffer} 文件内容
 */
function getBol(filePath) {
  if (!fs.existsSync(filePath)) {
    throw new Error(`文件不存在：${filePath}`);
  }
  return fs.readFileSync(filePath);
}

/**
 * 删除提单文件
 * @param {string} filePath - 文件路径
 */
function deleteBol(filePath) {
  if (fs.existsSync(filePath)) {
    fs.unlinkSync(filePath);
    console.log(`✅ 提单已删除：${filePath}`);
  }
}

module.exports = {
  saveBol,
  saveBolFromFile,
  listBols,
  getBol,
  deleteBol,
  BOL_ARCHIVE_DIR
};
