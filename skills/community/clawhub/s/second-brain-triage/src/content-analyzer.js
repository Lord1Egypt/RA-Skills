/**
 * Content Analyzer - 内容分析器
 * 识别内容类型，提取元数据
 */

class ContentAnalyzer {
  constructor() {
    // 内容类型定义
    this.contentTypes = {
      ARTICLE: 'article',      // 文章/博客
      VIDEO: 'video',          // 视频
      PODCAST: 'podcast',      // 播客
      BOOK: 'book',            // 书籍
      PAPER: 'paper',          // 论文
      TWEET: 'tweet',          // 社交媒体帖子
      EMAIL: 'email',          // 邮件
      NOTE: 'note',            // 笔记
      TASK: 'task',            // 任务
      IDEA: 'idea',            // 想法/灵感
      CODE: 'code',            // 代码片段
      DOCUMENT: 'document',    // 文档
      LINK: 'link',            // 纯链接
      IMAGE: 'image',          // 图片
      FILE: 'file',            // 文件
    };

    // 类型检测规则
    this.typeRules = [
      { type: 'video', patterns: [/youtube\.com/, /youtu\.be/, /vimeo\.com/, /bilibili\.com/, /douyin\.com/, /tiktok\.com/] },
      { type: 'podcast', patterns: [/podcast/, /anchor\.fm/, /spotify\.com\/episode/, /apple\.com\/podcast/] },
      { type: 'paper', patterns: [/arxiv\.org/, /doi\.org/, /researchgate\.net/, /ieee\.org/, /academia\.edu/] },
      { type: 'book', patterns: [/goodreads\.com/, /amazon\.com.*book/, /douban\.com.*book/] },
      { type: 'tweet', patterns: [/twitter\.com/, /x\.com/, /weibo\.com/] },
      { type: 'code', patterns: [/github\.com/, /gitlab\.com/, /stackoverflow\.com/, /codepen\.io/] },
      { type: 'image', patterns: [/\.(jpg|jpeg|png|gif|webp|svg)$/i] },
      { type: 'document', patterns: [/\.(pdf|doc|docx|ppt|pptx|xls|xlsx)$/i] },
    ];
  }

  /**
   * 分析内容，返回类型和元数据
   * @param {string} content - 输入内容（文本或URL）
   * @returns {Object} 分析结果
   */
  analyze(content) {
    if (!content || typeof content !== 'string') {
      return { type: 'unknown', metadata: {}, confidence: 0 };
    }

    const trimmed = content.trim();
    
    // 检测是否为URL
    const isUrl = this._isUrl(trimmed);
    
    // 检测内容类型
    const typeResult = this._detectType(trimmed, isUrl);
    
    // 提取元数据
    const metadata = this._extractMetadata(trimmed, typeResult.type, isUrl);
    
    return {
      type: typeResult.type,
      subtype: typeResult.subtype,
      metadata,
      confidence: typeResult.confidence,
      isUrl,
      wordCount: this._countWords(trimmed),
      readingTime: this._estimateReadingTime(trimmed),
    };
  }

  /**
   * 检测是否为URL
   */
  _isUrl(text) {
    const urlPattern = /^(https?:\/\/)?([\da-z.-]+)\.([a-z.]{2,6})([/\w .-]*)*\/?$/i;
    return urlPattern.test(text);
  }

  /**
   * 检测内容类型
   */
  _detectType(text, isUrl) {
    // 如果是纯URL，先根据域名判断
    if (isUrl) {
      for (const rule of this.typeRules) {
        for (const pattern of rule.patterns) {
          if (pattern.test(text)) {
            return { type: rule.type, subtype: null, confidence: 0.9 };
          }
        }
      }
      return { type: 'link', subtype: null, confidence: 0.7 };
    }

    // 检测任务格式
    if (this._isTask(text)) {
      return { type: 'task', subtype: this._detectTaskType(text), confidence: 0.85 };
    }

    // 检测代码
    if (this._isCode(text)) {
      return { type: 'code', subtype: this._detectLanguage(text), confidence: 0.9 };
    }

    // 检测邮件格式
    if (this._isEmail(text)) {
      return { type: 'email', subtype: null, confidence: 0.9 };
    }

    // 检测想法/灵感（短文本，包含关键词）
    if (this._isIdea(text)) {
      return { type: 'idea', subtype: null, confidence: 0.75 };
    }

    // 检测文章（长文本，有段落结构）
    if (this._isArticle(text)) {
      return { type: 'article', subtype: null, confidence: 0.8 };
    }

    // 默认视为笔记
    return { type: 'note', subtype: null, confidence: 0.6 };
  }

  /**
   * 检测是否为任务
   */
  _isTask(text) {
    const taskPatterns = [
      /^(TODO|todo|待办|任务|需要|必须|应该)\s*[：:]/,
      /^[-*]\s*\[.?\]/,  // Markdown任务列表
      /^(完成|搞定|处理|解决|修复|实现|部署|发布|测试|review|Review)/,
    ];
    return taskPatterns.some(p => p.test(text));
  }

  /**
   * 检测任务类型
   */
  _detectTaskType(text) {
    if (/bug|fix|修复|解决|问题/i.test(text)) return 'bugfix';
    if (/feature|功能|实现|开发|新增/i.test(text)) return 'feature';
    if (/review|review|审核|检查/i.test(text)) return 'review';
    if (/meeting|会议|讨论|沟通/i.test(text)) return 'meeting';
    if (/learn|study|学习|阅读|了解/i.test(text)) return 'learning';
    return 'general';
  }

  /**
   * 检测是否为代码
   */
  _isCode(text) {
    const codeIndicators = [
      /^(const|let|var|function|class|import|export|def|class)\s+/m,
      /[{;]\s*$/m,
      /^(\s{2,4}|\t)/m,  // 缩进
      /[{}[\];]/.test(text) && text.split('\n').length > 2,
    ];
    return codeIndicators.some(i => i === true || (typeof i === 'object' && i.test(text)));
  }

  /**
   * 检测编程语言
   */
  _detectLanguage(text) {
    const langPatterns = {
      javascript: /(const|let|var|function|=>|console\.log)/,
      python: /(def |import |print\(|class.*:)/,
      java: /(public class|private|protected|void|static)/,
      go: /(func |package |import \(|defer )/,
      rust: /(fn |let mut|impl |match |use )/,
      bash: /(#!\/bin\/bash|echo |cd |ls |grep )/,
      sql: /(SELECT|INSERT|UPDATE|DELETE|FROM|WHERE|JOIN)/i,
    };
    
    for (const [lang, pattern] of Object.entries(langPatterns)) {
      if (pattern.test(text)) return lang;
    }
    return 'unknown';
  }

  /**
   * 检测是否为邮件
   */
  _isEmail(text) {
    return /^(From:|To:|Subject:|Date:)/m.test(text) || 
           /^[\w.-]+@[\w.-]+\.\w+/.test(text);
  }

  /**
   * 检测是否为想法/灵感
   */
  _isIdea(text) {
    const ideaKeywords = ['想法', '灵感', '突然想到', '或许可以', '如果', 'idea', 'thought', 'maybe', 'what if'];
    const hasKeyword = ideaKeywords.some(k => text.toLowerCase().includes(k));
    const isShort = text.length < 500;
    return hasKeyword && isShort;
  }

  /**
   * 检测是否为文章
   */
  _isArticle(text) {
    const hasStructure = /\n/.test(text);  // 有换行
    const hasPunctuation = /[。！？.!?]/.test(text);
    const isLongEnough = text.length > 50;
    return hasStructure && hasPunctuation && isLongEnough;
  }

  /**
   * 提取元数据
   */
  _extractMetadata(text, type, isUrl) {
    const metadata = {
      title: this._extractTitle(text, type),
      description: this._extractDescription(text, type),
      tags: this._extractTags(text),
      mentions: this._extractMentions(text),
      urls: this._extractUrls(text),
      dates: this._extractDates(text),
    };

    if (isUrl) {
      metadata.domain = this._extractDomain(text);
    }

    // 类型特定元数据
    switch (type) {
      case 'task':
        metadata.priority = this._extractPriority(text);
        metadata.dueDate = this._extractDueDate(text);
        break;
      case 'code':
        metadata.language = this._detectLanguage(text);
        break;
      case 'book':
        metadata.author = this._extractAuthor(text);
        break;
    }

    return metadata;
  }

  /**
   * 提取标题
   */
  _extractTitle(text, type) {
    // 第一行非空内容
    const lines = text.split('\n').filter(l => l.trim());
    if (lines.length === 0) return null;
    
    const firstLine = lines[0].trim();
    
    // 如果是Markdown标题
    if (firstLine.startsWith('#')) {
      return firstLine.replace(/^#+\s*/, '');
    }
    
    // 限制长度
    return firstLine.length > 100 ? firstLine.slice(0, 100) + '...' : firstLine;
  }

  /**
   * 提取描述
   */
  _extractDescription(text, type) {
    const lines = text.split('\n').filter(l => l.trim());
    if (lines.length <= 1) return null;
    
    // 取第二行或前几行
    const desc = lines.slice(1, 4).join(' ').trim();
    return desc.length > 300 ? desc.slice(0, 300) + '...' : desc;
  }

  /**
   * 提取标签
   */
  _extractTags(text) {
    const tagPattern = /#([\w\u4e00-\u9fa5]+)/g;
    const matches = text.match(tagPattern);
    return matches ? matches.map(t => t.slice(1)) : [];
  }

  /**
   * 提取@提及
   */
  _extractMentions(text) {
    const mentionPattern = /@([\w\u4e00-\u9fa5]+)/g;
    const matches = text.match(mentionPattern);
    return matches ? matches.map(m => m.slice(1)) : [];
  }

  /**
   * 提取URL
   */
  _extractUrls(text) {
    const urlPattern = /(https?:\/\/[^\s]+)/g;
    const matches = text.match(urlPattern);
    return matches || [];
  }

  /**
   * 提取日期
   */
  _extractDates(text) {
    const datePatterns = [
      /(\d{4}[-/年]\d{1,2}[-/月]\d{1,2}[日]?)/,
      /(\d{1,2}[-/月]\d{1,2}[日]?)/,
      /(明天|后天|下周|下周一|下周二|下周三|下周四|下周五)/,
    ];
    const dates = [];
    for (const pattern of datePatterns) {
      const match = text.match(pattern);
      if (match) dates.push(match[1]);
    }
    return dates;
  }

  /**
   * 提取域名
   */
  _extractDomain(url) {
    try {
      const match = url.match(/^(https?:\/\/)?([^/]+)/);
      return match ? match[2] : null;
    } catch {
      return null;
    }
  }

  /**
   * 提取优先级
   */
  _extractPriority(text) {
    if (/P0|紧急|urgent|critical| ASAP/i.test(text)) return 'critical';
    if (/P1|高优先级|high|重要/i.test(text)) return 'high';
    if (/P2|中优先级|medium|一般/i.test(text)) return 'medium';
    if (/P3|低优先级|low|不急/i.test(text)) return 'low';
    return 'normal';
  }

  /**
   * 提取截止日期
   */
  _extractDueDate(text) {
    const patterns = [
      /截止[日期]?[：:]\s*(\d{4}[-/年]\d{1,2}[-/月]\d{1,2})/,
      /due[：:]\s*(\d{4}[-/]\d{1,2}[-/]\d{1,2})/i,
      /(明天|后天|下周[一二三四五六日])/,
    ];
    for (const pattern of patterns) {
      const match = text.match(pattern);
      if (match) return match[1];
    }
    return null;
  }

  /**
   * 提取作者
   */
  _extractAuthor(text) {
    const patterns = [
      /作者[：:]\s*([^\n]+)/,
      /author[：:]\s*([^\n]+)/i,
      /by\s+([^\n]{2,30})/i,
    ];
    for (const pattern of patterns) {
      const match = text.match(pattern);
      if (match) return match[1].trim();
    }
    return null;
  }

  /**
   * 统计字数
   */
  _countWords(text) {
    // 中文字符
    const cnChars = (text.match(/[\u4e00-\u9fa5]/g) || []).length;
    // 英文单词
    const enWords = (text.match(/[a-zA-Z]+/g) || []).length;
    return cnChars + enWords;
  }

  /**
   * 估算阅读时间（分钟）
   */
  _estimateReadingTime(text) {
    const wordCount = this._countWords(text);
    // 平均阅读速度：中文300字/分钟，英文200词/分钟
    return Math.ceil(wordCount / 250);
  }
}

module.exports = ContentAnalyzer;