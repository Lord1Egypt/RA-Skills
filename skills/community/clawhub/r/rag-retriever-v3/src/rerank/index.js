/**
 * 重排序模块
 * 提供多种重排序策略
 */

import { CrossEncoderReranker } from './CrossEncoderReranker.js';

export { CrossEncoderReranker };

/**
 * 重排序器工厂函数
 * @param {string} type - 重排序器类型
 * @param {object} options - 配置选项
 * @returns {CrossEncoderReranker} - 重排序器实例
 */
export function createReranker(type = 'cross-encoder', options = {}) {
  switch (type.toLowerCase()) {
    case 'cross-encoder':
    case 'crossencoder':
    case 'ce':
      return new CrossEncoderReranker(options);
    default:
      throw new Error(`未知的重排序器类型: ${type}。支持的选项: cross-encoder`);
  }
}

/**
 * 获取所有可用的重排序器信息
 */
export function getAvailableRerankers() {
  return {
    'cross-encoder': {
      name: 'Cross-Encoder',
      type: 'local',
      requiresApiKey: false,
      description: '使用本地 Cross-Encoder 模型进行精确重排序',
      models: CrossEncoderReranker.getSupportedModels()
    }
  };
}

export default {
  CrossEncoderReranker,
  createReranker,
  getAvailableRerankers
};
