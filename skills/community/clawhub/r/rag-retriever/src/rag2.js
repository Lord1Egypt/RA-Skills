// RAG 2.0 - 主入口
// 集成 Embedding、BM25、混合搜索、重排序、来源引用

import { HybridSearch } from './hybrid-search.js';
import { createEmbeddingProvider } from './embeddings.js';
import { readFileSync, existsSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

/**
 * RAG 2.0 检索器
 */
export class RAG2Retriever {
  constructor(options = {}) {
    this.config = {
      embeddingType: options.embeddingType || 'simple', // 'openai' | 'simple'
      embeddingOptions: options.embeddingOptions || {},
      vectorWeight: options.vectorWeight || 0.7,
      bm25Weight: options.bm25Weight || 0.3,
      chunkSize: options.chunkSize || 500,
      chunkOverlap: options.chunkOverlap || 50,
      ...options
    };

    // 支持直接传入 embeddingProvider
    if (options.embeddingProvider) {
      this.embedding = options.embeddingProvider;
    } else {
      this.embedding = createEmbeddingProvider(
        this.config.embeddingType,
        this.config.embeddingOptions
      );
    }

    this.search = new HybridSearch({
      embeddingProvider: this.embedding,
      vectorWeight: this.config.vectorWeight,
      bm25Weight: this.config.bm25Weight
    });

    this.documents = [];
  }

  /**
   * 文档分块
   */
  chunkDocument(content, metadata = {}) {
    const chunks = [];
    const { chunkSize = 500, chunkOverlap = 50 } = this.config;

    if (content.length <= chunkSize) {
      chunks.push({
        content: content.trim(),
        metadata: {
          ...metadata,
          chunkIndex: 0,
          totalChunks: 1,
          charStart: 0,
          charEnd: content.length
        }
      });
      return chunks;
    }

    let start = 0;
    let chunkIndex = 0;
    const separator = '\n';

    while (start < content.length) {
      let end = start + chunkSize;

      if (end < content.length) {
        const sepIndex = content.lastIndexOf(separator, end);
        if (sepIndex > start) {
          end = sepIndex + separator.length;
        }
      }

      chunks.push({
        content: content.slice(start, end).trim(),
        metadata: {
          ...metadata,
          chunkIndex,
          charStart: start,
          charEnd: end
        }
      });

      start = end - chunkOverlap;
      if (start < 0) start = end;
      chunkIndex++;
    }

    // 更新总块数
    chunks.forEach(chunk => {
      chunk.metadata.totalChunks = chunks.length;
    });

    return chunks;
  }

  /**
   * 添加文档
   */
  async addDocument(content, metadata = {}) {
    const chunks = this.chunkDocument(content, metadata);
    const docs = chunks.map((chunk, i) => ({
      id: `${metadata.source || 'doc'}_${i}_${Date.now()}`,
      content: chunk.content,
      metadata: {
        ...chunk.metadata,
        source: metadata.source,
        title: metadata.title,
        url: metadata.url
      }
    }));

    await this.search.addDocuments(docs);
    this.documents.push(...docs);

    return {
      added: docs.length,
      total: this.documents.length
    };
  }

  /**
   * 从文件添加文档
   */
  async addFile(filePath, metadata = {}) {
    if (!existsSync(filePath)) {
      throw new Error(`File not found: ${filePath}`);
    }

    const content = readFileSync(filePath, 'utf-8');
    const filename = filePath.split(/[/\\]/).pop();

    return this.addDocument(content, {
      ...metadata,
      source: filePath,
      title: metadata.title || filename,
      filename
    });
  }

  /**
   * 搜索
   */
  async query(query, options = {}) {
    const {
      topK = 5,
      method = 'hybrid', // 'vector' | 'bm25' | 'hybrid' | 'weighted'
      includeCitations = true
    } = options;

    const results = await this.search.searchWithCitations(
      query,
      topK,
      method
    );

    // 格式化输出
    const formatted = {
      query,
      method,
      resultsCount: results.length,
      results: results.map(r => ({
        content: r.content,
        score: Math.round(r.score * 1000) / 1000,
        vectorScore: Math.round(r.vectorScore * 1000) / 1000,
        bm25Score: Math.round(r.bm25Score * 1000) / 1000,
        reference: r.reference,
        citation: includeCitations ? r.citation : null,
        metadata: {
          source: r.metadata.source,
          chunkIndex: r.metadata.chunkIndex,
          totalChunks: r.metadata.totalChunks
        }
      })),
      citations: includeCitations ? this.formatCitations(results) : null
    };

    return formatted;
  }

  /**
   * 格式化引用列表
   */
  formatCitations(results) {
    return results.map((r, i) => {
      const citation = r.citation;
      if (!citation) return null;

      let ref = `[${i + 1}]`;
      if (citation.source && citation.source !== 'unknown') {
        ref += ` ${citation.source}`;
      }
      if (citation.chunkIndex !== null) {
        ref += ` (chunk ${citation.chunkIndex + 1}/${citation.totalChunks})`;
      }
      if (citation.url) {
        ref += ` - ${citation.url}`;
      }

      return ref;
    }).filter(Boolean);
  }

  /**
   * 生成 RAG 增强的上下文
   */
  async augmentContext(query, options = {}) {
    const { topK = 3, separator = '\n---\n' } = options;
    
    const results = await this.query(query, { topK, includeCitations: true });

    if (results.resultsCount === 0) {
      return {
        context: '',
        hasResults: false,
        query
      };
    }

    const contextParts = results.results.map((r, i) => {
      return `[${i + 1}] ${r.content}`;
    });

    return {
      context: contextParts.join(separator),
      hasResults: true,
      query,
      resultsCount: results.resultsCount,
      citations: results.citations,
      prompt: this.buildAugmentedPrompt(query, contextParts)
    };
  }

  /**
   * 构建增强提示词
   */
  buildAugmentedPrompt(query, contextParts) {
    return `Based on the following context, answer the question. Use citations [1], [2], etc. to reference sources.

Context:
${contextParts.join('\n\n')}

Question: ${query}

Answer:`;
  }

  /**
   * 获取统计信息
   */
  getStats() {
    const embeddingInfo = this.embedding.getInfo ? this.embedding.getInfo() : { type: this.config.embeddingType };
    
    return {
      ...this.search.getStats(),
      embedding: embeddingInfo,
      config: {
        embeddingType: embeddingInfo.type || this.config.embeddingType,
        vectorWeight: this.config.vectorWeight,
        bm25Weight: this.config.bm25Weight,
        chunkSize: this.config.chunkSize,
        chunkOverlap: this.config.chunkOverlap
      }
    };
  }

  /**
   * 清空索引
   */
  clear() {
    this.search.clear();
    this.documents = [];
  }
}

// 默认导出
export default RAG2Retriever;
