/**
 * 知乎技术博客生成器 - 论文解析工具
 */

const fs = require('fs');
const path = require('path');

class PaperParser {
  constructor(logger) {
    this.logger = logger;
  }

  /**
   * 解析论文 PDF
     * 注：需要安装 pdf-parse 依赖
   */
  async parsePDF(pdfPath) {
    this.logger.info(`解析论文: ${pdfPath}`);
    
    try {
      const pdfParse = require('pdf-parse');
      const dataBuffer = fs.readFileSync(pdfPath);
      const data = await pdfParse(dataBuffer);
      
      return {
        text: data.text,
        numpages: data.numpages,
        info: data.info,
        metadata: data.metadata,
      };
    } catch (error) {
      this.logger.error(`解析论文失败: ${error.message}`);
      return null;
    }
  }

  /**
   * 提取论文关键信息
   */
  extractKeyInfo(pdfText) {
    const info = {
      title: this.extractTitle(pdfText),
      authors: this.extractAuthors(pdfText),
      abstract: this.extractAbstract(pdfText),
      keywords: this.extractKeywords(pdfText),
      conclusions: this.extractConclusions(pdfText),
      contributions: this.extractContributions(pdfText),
    };
    
    return info;
  }

  /**
   * 提取标题
   */
  extractTitle(text) {
    // 通常标题在文档开头
    const lines = text.split('\n').filter(l => l.trim());
    if (lines.length > 0) {
      // 取前3行中最长的一行作为标题
      return lines.slice(0, 3).reduce((a, b) => a.length > b.length ? a : b);
    }
    return 'Unknown Title';
  }

  /**
   * 提取作者
   */
  extractAuthors(text) {
    // 作者通常在标题下方
    // 这里简化处理，实际应该使用更复杂的模式匹配
    const lines = text.split('\n').slice(0, 10);
    const authors = [];
    
    // 查找包含 @ 或常见作者标识的行
    for (const line of lines) {
      if (line.includes('@') || /university|institute|lab/i.test(line)) {
        const possibleAuthors = line.split(/,|and|·/).map(s => s.trim()).filter(s => s);
        authors.push(...possibleAuthors);
      }
    }
    
    return authors.slice(0, 5); // 最多取5个作者
  }

  /**
   * 提取摘要
   */
  extractAbstract(text) {
    const abstractMatch = text.match(/abstract[\s:]*([^\n]+(?:\n(?![\dA-Z][\.]?\s)[^\n]+)*)/i);
    if (abstractMatch) {
      return abstractMatch[1].trim();
    }
    
    // 如果找不到 Abstract 标签，取前500字符作为摘要
    return text.slice(0, 500).trim();
  }

  /**
   * 提取关键词
   */
  extractKeywords(text) {
    const keywordsMatch = text.match(/keywords[\s:]*([^\n]+)/i);
    if (keywordsMatch) {
      return keywordsMatch[1].split(/[,;]/).map(k => k.trim()).filter(k => k);
    }
    return [];
  }

  /**
   * 提取结论
   */
  extractConclusions(text) {
    const conclusionMatch = text.match(/conclusion[s]?[\s:]*([^]+?)(?:references|acknowledgment|$)/i);
    if (conclusionMatch) {
      return conclusionMatch[1].trim().slice(0, 1000);
    }
    return '';
  }

  /**
   * 提取核心贡献
   */
  extractContributions(text) {
    const contributions = [];
    
    // 查找贡献相关的段落
    const patterns = [
      /contribution[s]?[\s:]*([^]+?)(?:\d+\.|related work|$)/i,
      /we (?:propose|introduce|present|develop)[^\.]+\./gi,
      /our (?:main|key|primary) contribution[^\.]+\./gi,
    ];
    
    for (const pattern of patterns) {
      const matches = text.match(pattern);
      if (matches) {
        contributions.push(...matches.map(m => m.trim()));
      }
    }
    
    return contributions.slice(0, 5);
  }

  /**
   * 提取图表信息
   * 注：PDF解析提取图片需要额外的库，如 pdf2pic
   */
  async extractFigures(pdfPath, outputDir) {
    this.logger.info(`提取论文图表: ${pdfPath}`);
    
    // 这里需要实现图表提取
    // 可以使用 pdf2pic 或其他 PDF 图像提取工具
    
    const figures = [];
    
    // 示例：返回提取的图表信息
    // {
    //   page: 3,
    //   type: 'figure',
    //   caption: 'Figure 1: Architecture',
    //   path: 'output/fig1.png'
    // }
    
    return figures;
  }

  /**
   * 生成论文摘要 Markdown
   */
  generateSummaryMarkdown(paperInfo) {
    return `## 论文信息

**标题**: ${paperInfo.title}

**作者**: ${paperInfo.authors.join(', ')}

**关键词**: ${paperInfo.keywords.join(', ')}

### 摘要

${paperInfo.abstract}

### 核心贡献

${paperInfo.contributions.map(c => `- ${c}`).join('\n')}

### 结论

${paperInfo.conclusions}
`;
  }

  /**
   * 计算论文与主题的相关性
   */
  calculateRelevance(paperInfo, topic) {
    const topicLower = topic.toLowerCase();
    const text = `${paperInfo.title} ${paperInfo.abstract} ${paperInfo.keywords.join(' ')}`.toLowerCase();
    
    // 简单的相关性计算
    const topicWords = topicLower.split(/\s+/);
    let matchCount = 0;
    
    for (const word of topicWords) {
      if (text.includes(word)) {
        matchCount++;
      }
    }
    
    return matchCount / topicWords.length;
  }
}

module.exports = PaperParser;
