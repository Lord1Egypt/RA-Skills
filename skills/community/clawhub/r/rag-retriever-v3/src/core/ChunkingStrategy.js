/**
 * 文档分块策略
 * 支持多种分块策略，针对中文优化
 */

import { createHash } from 'crypto';

export class ChunkingStrategy {
  constructor(options = {}) {
    this.chunkSize = options.chunkSize || 500;        // 每块字符数
    this.overlap = options.overlap || 50;             // 重叠字符数
    this.separator = options.separator || '\n';       // 分隔符
    this.strategy = options.strategy || 'recursive';  // 分块策略
  }

  /**
   * 将文本分块
   * @param {string} text - 原始文本
   * @param {object} metadata - 元数据
   * @returns {Array} - 分块结果
   */
  chunk(text, metadata = {}) {
    switch (this.strategy) {
      case 'fixed':
        return this.fixedChunking(text, metadata);
      case 'recursive':
        return this.recursiveChunking(text, metadata);
      case 'semantic':
        return this.semanticChunking(text, metadata);
      default:
        return this.recursiveChunking(text, metadata);
    }
  }

  /**
   * 固定大小分块
   */
  fixedChunking(text, metadata = {}) {
    const chunks = [];
    const totalLength = text.length;
    let start = 0;
    let chunkIndex = 0;

    while (start < totalLength) {
      const end = Math.min(start + this.chunkSize, totalLength);
      const chunkContent = text.slice(start, end);

      chunks.push({
        id: this.generateId(chunkContent + chunkIndex),
        content: chunkContent.trim(),
        metadata: {
          ...metadata,
          chunkIndex,
          charStart: start,
          charEnd: end,
          totalChunks: Math.ceil(totalLength / (this.chunkSize - this.overlap))
        }
      });

      start = end - this.overlap;
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
   * 递归分块（优先在分隔符处分割）
   */
  recursiveChunking(text, metadata = {}) {
    const chunks = [];
    
    // 如果文本小于 chunkSize，直接返回
    if (text.length <= this.chunkSize) {
      return [{
        id: this.generateId(text),
        content: text.trim(),
        metadata: {
          ...metadata,
          chunkIndex: 0,
          totalChunks: 1,
          charStart: 0,
          charEnd: text.length
        }
      }];
    }

    // 定义分隔符优先级（从高到低）
    const separators = ['\n\n', '\n', '。', '；', '，', ' ', ''];
    
    let start = 0;
    let chunkIndex = 0;

    while (start < text.length) {
      let end = start + this.chunkSize;

      if (end < text.length) {
        // 尝试在分隔符处切断
        let cutPoint = -1;
        
        for (const sep of separators) {
          if (sep === '') {
            // 最后一个选项：直接切断
            cutPoint = end;
            break;
          }
          
          const searchStart = Math.max(start, end - this.chunkSize / 2);
          const searchEnd = end;
          const sepIndex = text.lastIndexOf(sep, searchEnd);
          
          if (sepIndex > searchStart) {
            cutPoint = sepIndex + sep.length;
            break;
          }
        }
        
        if (cutPoint > start) {
          end = cutPoint;
        }
      } else {
        end = text.length;
      }

      const chunkContent = text.slice(start, end);
      
      chunks.push({
        id: this.generateId(chunkContent + chunkIndex),
        content: chunkContent.trim(),
        metadata: {
          ...metadata,
          chunkIndex,
          charStart: start,
          charEnd: end
        }
      });

      // 移动起始位置（减去重叠部分）
      start = end - this.overlap;
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
   * 语义分块（基于段落和句子边界）
   */
  semanticChunking(text, metadata = {}) {
    // 首先按段落分割
    const paragraphs = text.split(/\n\n+/).filter(p => p.trim().length > 0);
    const chunks = [];
    let chunkIndex = 0;
    let currentChunk = '';
    let charStart = 0;
    let chunkStart = 0;

    for (const paragraph of paragraphs) {
      const paraLength = paragraph.length;
      
      // 如果当前段落加上已有内容超过 chunkSize，先保存当前块
      if (currentChunk.length + paraLength > this.chunkSize && currentChunk.length > 0) {
        chunks.push({
          id: this.generateId(currentChunk + chunkIndex),
          content: currentChunk.trim(),
          metadata: {
            ...metadata,
            chunkIndex,
            charStart: chunkStart,
            charEnd: charStart
          }
        });
        
        // 保留重叠部分
        if (currentChunk.length > this.overlap) {
          currentChunk = currentChunk.slice(-this.overlap);
          chunkStart = charStart - this.overlap;
        } else {
          currentChunk = '';
          chunkStart = charStart;
        }
        
        chunkIndex++;
      }

      // 如果段落本身超过 chunkSize，需要分割
      if (paraLength > this.chunkSize) {
        // 使用递归分块处理长段落
        const subChunks = this.recursiveChunking(paragraph, metadata);
        for (const subChunk of subChunks) {
          subChunk.id = this.generateId(subChunk.content + chunkIndex);
          subChunk.metadata.chunkIndex = chunkIndex;
          subChunk.metadata.charStart += chunkStart;
          subChunk.metadata.charEnd += chunkStart;
          chunks.push(subChunk);
          chunkIndex++;
        }
        currentChunk = '';
        chunkStart = charStart + paraLength;
      } else {
        currentChunk += (currentChunk ? '\n\n' : '') + paragraph;
      }
      
      charStart += paraLength + 2; // +2 for \n\n
    }

    // 保存最后一个块
    if (currentChunk.trim().length > 0) {
      chunks.push({
        id: this.generateId(currentChunk + chunkIndex),
        content: currentChunk.trim(),
        metadata: {
          ...metadata,
          chunkIndex,
          charStart: chunkStart,
          charEnd: charStart
        }
      });
    }

    // 更新总块数
    chunks.forEach(chunk => {
      chunk.metadata.totalChunks = chunks.length;
    });

    return chunks;
  }

  /**
   * 生成唯一 ID
   */
  generateId(content) {
    return createHash('sha256').update(content).digest('hex').slice(0, 16);
  }

  /**
   * 获取分块统计信息
   */
  getStats(chunks) {
    if (!chunks || chunks.length === 0) {
      return null;
    }

    const lengths = chunks.map(c => c.content.length);
    const totalLength = lengths.reduce((a, b) => a + b, 0);

    return {
      totalChunks: chunks.length,
      avgChunkSize: totalLength / chunks.length,
      minChunkSize: Math.min(...lengths),
      maxChunkSize: Math.max(...lengths),
      totalLength,
      strategy: this.strategy
    };
  }
}

export default ChunkingStrategy;
