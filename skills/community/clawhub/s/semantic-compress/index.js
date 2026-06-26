/**
 * Semantic Compress - 导出主接口
 */

const { semanticCompress, compressFromFile } = require('./scripts/compress.js');

module.exports = {
  semanticCompress,
  compressFromFile,
  version: '1.0.0'
};
