/**
 * RAG Retriever V3 - 主入口
 * 
 * RAG 3.0 特性：
 * - 语义嵌入支持（OpenAI + BGE + MiniLM 多模型）
 * - 混合检索（向量相似度 + BM25 关键词 + RRF 融合）
 * - 重排序模块（Cross-Encoder 重打分）
 * - 来源引用（自动编号 + 溯源）
 * - 中文优化（jieba 分词）
 */

// 核心模块
import { RAGRetrieverV3, ChunkingStrategy, CitationManager } from './core/index.js';

// 嵌入模块
import { 
  EmbeddingProvider, 
  XenovaEmbedding, 
  OpenAIEmbedding,
  createEmbeddingProvider,
  getAvailableProviders 
} from './embeddings/index.js';

// 搜索模块
import { BM25Search } from './search/BM25Search.js';
import { RRFFusion } from './search/RRFFusion.js';

// 重排序模块
import { CrossEncoderReranker, createReranker, getAvailableRerankers } from './rerank/index.js';

// 版本信息
export const VERSION = '3.0.0';

// 导出所有模块
export {
  // 核心
  RAGRetrieverV3,
  ChunkingStrategy,
  CitationManager,
  
  // 嵌入
  EmbeddingProvider,
  XenovaEmbedding,
  OpenAIEmbedding,
  createEmbeddingProvider,
  getAvailableProviders,
  
  // 搜索
  BM25Search,
  RRFFusion,
  
  // 重排序
  CrossEncoderReranker,
  createReranker,
  getAvailableRerankers
};

// 默认导出
export default {
  RAGRetrieverV3,
  ChunkingStrategy,
  CitationManager,
  EmbeddingProvider,
  XenovaEmbedding,
  OpenAIEmbedding,
  createEmbeddingProvider,
  getAvailableProviders,
  BM25Search,
  RRFFusion,
  CrossEncoderReranker,
  createReranker,
  getAvailableRerankers,
  VERSION
};

// 打印版本信息
console.log(`🦞 RAG Retriever V3 ${VERSION} - 高级检索增强生成系统`);
