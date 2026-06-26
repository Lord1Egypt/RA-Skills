/**
 * 来源引用管理器
 * 自动为检索结果生成编号和溯源信息
 */

export class CitationManager {
  constructor(options = {}) {
    this.format = options.format || 'numbered';  // 引用格式: numbered, bracket, footnote
    this.includeMetadata = options.includeMetadata !== false;
    this.maxContentLength = options.maxContentLength || 500;
  }

  /**
   * 为检索结果添加引用标记
   * @param {Array} results - 检索结果列表
   * @param {Object} options - 配置选项
   * @returns {Array} - 带引用标记的结果
   */
  addCitations(results, options = {}) {
    const startIndex = options.startIndex || 1;
    
    return results.map((result, index) => {
      const citationNumber = startIndex + index;
      const citationMark = this.formatCitation(citationNumber);
      
      return {
        ...result,
        citation: {
          number: citationNumber,
          mark: citationMark,
          id: result.id,
          source: this.extractSource(result),
          content: this.truncateContent(result.content || result.text || '')
        }
      };
    });
  }

  /**
   * 格式化引用标记
   */
  formatCitation(number) {
    switch (this.format) {
      case 'bracket':
        return `[${number}]`;
      case 'footnote':
        return `[^${number}]`;
      case 'numbered':
      default:
        return `[${number}]`;
    }
  }

  /**
   * 提取来源信息
   */
  extractSource(result) {
    const metadata = result.metadata || {};
    
    return {
      id: result.id,
      title: metadata.title || metadata.source || '未知来源',
      url: metadata.url || metadata.link || null,
      author: metadata.author || null,
      date: metadata.date || metadata.timestamp || null,
      chunkIndex: metadata.chunkIndex,
      totalChunks: metadata.totalChunks,
      charStart: metadata.charStart,
      charEnd: metadata.charEnd
    };
  }

  /**
   * 截断内容
   */
  truncateContent(content) {
    if (!content || content.length <= this.maxContentLength) {
      return content;
    }
    return content.slice(0, this.maxContentLength) + '...';
  }

  /**
   * 生成格式化的上下文（用于 RAG）
   * @param {Array} results - 带引用的检索结果
   * @param {Object} options - 配置选项
   * @returns {string} - 格式化的上下文
   */
  generateContext(results, options = {}) {
    const includeCitations = options.includeCitations !== false;
    const separator = options.separator || '\n\n';
    
    if (!results || results.length === 0) {
      return '';
    }

    const contextParts = results.map((result, index) => {
      const citation = result.citation || this.addCitations([result], { startIndex: index + 1 })[0].citation;
      const content = citation.content || result.content || result.text || '';
      
      if (includeCitations) {
        return `${citation.mark} ${content}`;
      } else {
        return content;
      }
    });

    return contextParts.join(separator);
  }

  /**
   * 生成引用列表（用于显示来源）
   * @param {Array} results - 带引用的检索结果
   * @returns {string} - 格式化的引用列表
   */
  generateCitationList(results) {
    if (!results || results.length === 0) {
      return '';
    }

    const lines = results.map(result => {
      const citation = result.citation;
      if (!citation) return '';

      const source = citation.source;
      let line = `${citation.mark} `;
      
      if (source.title) {
        line += `**${source.title}**`;
      }
      
      if (source.url) {
        line += ` (${source.url})`;
      }
      
      if (source.author) {
        line += ` - ${source.author}`;
      }
      
      if (source.date) {
        line += `, ${source.date}`;
      }

      return line;
    }).filter(line => line.length > 0);

    return lines.join('\n');
  }

  /**
   * 生成完整的 RAG 提示词
   * @param {string} query - 用户查询
   * @param {Array} results - 带引用的检索结果
   * @param {Object} options - 配置选项
   * @returns {Object} - 包含提示词和元数据的对象
   */
  generateRAGPrompt(query, results, options = {}) {
    const systemPrompt = options.systemPrompt || this.getDefaultSystemPrompt();
    const context = this.generateContext(results, options);
    const citationList = this.generateCitationList(results);

    const fullPrompt = `${systemPrompt}

用户问题：${query}

参考信息：
${context}

请基于以上参考信息回答用户问题。如果参考信息不足以回答问题，请明确说明。

---
来源引用：
${citationList}`;

    return {
      query,
      context,
      citationList,
      fullPrompt,
      citations: results.map(r => r.citation),
      resultCount: results.length
    };
  }

  /**
   * 获取默认系统提示词
   */
  getDefaultSystemPrompt() {
    return `你是一个基于检索增强生成（RAG）的 AI 助手。
请根据提供的参考信息回答用户问题。
回答时请遵循以下规则：
1. 仅基于提供的参考信息回答问题
2. 如果参考信息不足，请明确说明
3. 引用信息时使用 [数字] 格式标注来源
4. 保持回答简洁准确`;
  }

  /**
   * 验证引用完整性
   */
  validateCitations(results) {
    const issues = [];
    
    results.forEach((result, index) => {
      if (!result.citation) {
        issues.push({
          index,
          issue: '缺少引用信息',
          result
        });
      } else {
        if (!result.citation.number) {
          issues.push({
            index,
            issue: '引用缺少编号',
            citation: result.citation
          });
        }
        if (!result.citation.source) {
          issues.push({
            index,
            issue: '引用缺少来源',
            citation: result.citation
          });
        }
      }
    });

    return {
      valid: issues.length === 0,
      issues,
      totalResults: results.length
    };
  }

  /**
   * 合并重复引用
   */
  deduplicateCitations(results) {
    const seen = new Map();
    const deduplicated = [];
    
    for (const result of results) {
      const id = result.id || result.citation?.id;
      
      if (seen.has(id)) {
        // 合并分数（取最高）
        const existing = seen.get(id);
        existing.score = Math.max(existing.score || 0, result.score || 0);
        existing.rrfScore = Math.max(existing.rrfScore || 0, result.rrfScore || 0);
        existing.rerankScore = Math.max(existing.rerankScore || 0, result.rerankScore || 0);
      } else {
        deduplicated.push(result);
        seen.set(id, result);
      }
    }

    // 重新编号
    return this.addCitations(deduplicated, { startIndex: 1 });
  }
}

export default CitationManager;
