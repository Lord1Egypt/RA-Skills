/**
 * 嵌入模型管理模块
 * 统一管理和切换不同的嵌入模型
 */

import { EmbeddingProvider } from './EmbeddingProvider.js';
import { XenovaEmbedding } from './XenovaEmbedding.js';

// 尝试导入 OpenAIEmbedding，如果 openai 未安装则设为 null
let OpenAIEmbedding = null;
let openaiAvailable = false;

try {
  const openaiModule = await import('./OpenAIEmbedding.js');
  OpenAIEmbedding = openaiModule.OpenAIEmbedding;
  openaiAvailable = true;
} catch (error) {
  // openai 模块未安装，OpenAIEmbedding 保持为 null
  openaiAvailable = false;
}

// 导出所有嵌入类
export { EmbeddingProvider };
export { XenovaEmbedding };
export { OpenAIEmbedding };

/**
 * 创建嵌入模型实例的工厂函数
 * @param {string} provider - 提供者名称: 'xenova', 'openai', 'auto'
 * @param {object} options - 配置选项
 * @returns {EmbeddingProvider} - 嵌入模型实例
 */
export function createEmbeddingProvider(provider = 'auto', options = {}) {
  const normalizedProvider = provider.toLowerCase();

  switch (normalizedProvider) {
    case 'xenova':
    case 'local':
    case 'transformers':
      return new XenovaEmbedding(options);
    
    case 'openai':
      if (!OpenAIEmbedding) {
        throw new Error(
          'OpenAI 嵌入不可用。可能原因:\n' +
          '1. openai 模块未安装: npm install openai\n' +
          '2. 使用本地模型替代: createEmbeddingProvider("xenova")'
        );
      }
      return new OpenAIEmbedding(options);
    
    case 'auto':
      // 自动选择：优先使用本地模型，OpenAI 需要显式配置
      if (process.env.OPENAI_API_KEY && OpenAIEmbedding) {
        console.log('[EmbeddingFactory] 检测到 OPENAI_API_KEY，使用 OpenAI 嵌入');
        return new OpenAIEmbedding(options);
      } else {
        if (process.env.OPENAI_API_KEY && !OpenAIEmbedding) {
          console.log('[EmbeddingFactory] ⚠️ 检测到 OPENAI_API_KEY 但 openai 模块未安装');
          console.log('[EmbeddingFactory] 使用本地 Xenova 嵌入（运行: npm install openai 以启用 OpenAI）');
        } else {
          console.log('[EmbeddingFactory] 未检测到 API Key，使用本地 Xenova 嵌入');
        }
        return new XenovaEmbedding(options);
      }
    
    default:
      throw new Error(`未知的嵌入提供者: ${provider}。支持的选项: xenova, openai, auto`);
  }
}

/**
 * 获取所有可用的嵌入模型信息
 */
export function getAvailableProviders() {
  const providers = {
    xenova: {
      name: 'Xenova/Transformers',
      type: 'local',
      requiresApiKey: false,
      available: true,
      description: '本地运行，无需 API Key，支持多种开源模型',
      models: XenovaEmbedding.getSupportedModels()
    }
  };

  // 只在 OpenAIEmbedding 可用时添加
  if (OpenAIEmbedding) {
    providers.openai = {
      name: 'OpenAI',
      type: 'api',
      requiresApiKey: true,
      available: true,
      description: '云端 API，需要 OpenAI API Key',
      models: OpenAIEmbedding.getSupportedModels()
    };
  } else {
    providers.openai = {
      name: 'OpenAI',
      type: 'api',
      requiresApiKey: true,
      available: false,
      description: '未安装 openai 模块。运行: npm install openai',
      models: []
    };
  }

  return providers;
}

export default {
  EmbeddingProvider,
  XenovaEmbedding,
  OpenAIEmbedding,
  createEmbeddingProvider,
  getAvailableProviders
};
