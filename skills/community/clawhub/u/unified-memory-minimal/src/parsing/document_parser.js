/**
 * 文档解析器 - Document Parser
 * 借鉴 OpenViking 的文档解析机制
 */

import { logger } from '../utils/logger.js';

/**
 * 解析结果
 */
export class ParseResult {
  constructor(options) {
    this.uri = options.uri;
    this.format = options.format;
    this.content = options.content;
    this.sections = options.sections || [];
    this.tokens = options.tokens || 0;
    this.metadata = options.metadata || {};
  }
  
  toJSON() {
    return {
      uri: this.uri,
      format: this.format,
      content: this.content,
      sections: this.sections,
      tokens: this.tokens,
      metadata: this.metadata
    };
  }
}

/**
 * 解析器基类
 */
export class BaseParser {
  constructor(options = {}) {
    this.options = options;
    this.maxTokens = options.maxTokens || 8192;
  }
  
  async parse(file, options = {}) {
    throw new Error('Subclass must implement parse()');
  }
  
  detectFormat(filename) {
    const ext = filename.split('.').pop().toLowerCase();
    return ext;
  }
  
  estimateTokens(text) {
    // 简单估算：1 token ≈ 4 字符
    return Math.ceil(text.length / 4);
  }
  
  splitIntoSections(text, maxTokens) {
    const sections = [];
    const paragraphs = text.split(/\n\n+/);
    
    let currentSection = '';
    let currentTokens = 0;
    
    for (const paragraph of paragraphs) {
      const paragraphTokens = this.estimateTokens(paragraph);
      
      if (currentTokens + paragraphTokens > maxTokens) {
        if (currentSection) {
          sections.push({
            content: currentSection.trim(),
            tokens: currentTokens
          });
        }
        
        currentSection = paragraph;
        currentTokens = paragraphTokens;
      } else {
        currentSection += '\n\n' + paragraph;
        currentTokens += paragraphTokens;
      }
    }
    
    if (currentSection) {
      sections.push({
        content: currentSection.trim(),
        tokens: currentTokens
      });
    }
    
    return sections;
  }
}

/**
 * Markdown 解析器
 */
export class MarkdownParser extends BaseParser {
  async parse(file, options = {}) {
    const content = typeof file === 'string' ? file : file.toString();
    
    logger.debug(`[MarkdownParser] 解析 Markdown，${content.length} 字符`);
    
    // 提取标题结构
    const headings = this.extractHeadings(content);
    
    // 分段
    const sections = this.splitMarkdownSections(content);
    
    return new ParseResult({
      uri: options.uri,
      format: 'markdown',
      content: content,
      sections: sections,
      tokens: this.estimateTokens(content),
      metadata: {
        headings: headings,
        sectionCount: sections.length
      }
    });
  }
  
  extractHeadings(content) {
    const headings = [];
    const lines = content.split('\n');
    
    for (const line of lines) {
      const match = line.match(/^(#{1,6})\s+(.+)$/);
      
      if (match) {
        headings.push({
          level: match[1].length,
          text: match[2],
          anchor: match[2].toLowerCase().replace(/\s+/g, '-')
        });
      }
    }
    
    return headings;
  }
  
  splitMarkdownSections(content) {
    const sections = [];
    const lines = content.split('\n');
    
    let currentSection = { title: '', content: '', level: 0 };
    
    for (const line of lines) {
      const match = line.match(/^(#{1,6})\s+(.+)$/);
      
      if (match) {
        // 保存当前 section
        if (currentSection.content.trim()) {
          sections.push({
            title: currentSection.title,
            content: currentSection.content.trim(),
            level: currentSection.level,
            tokens: this.estimateTokens(currentSection.content)
          });
        }
        
        // 开始新 section
        currentSection = {
          title: match[2],
          content: '',
          level: match[1].length
        };
      } else {
        currentSection.content += line + '\n';
      }
    }
    
    // 保存最后一个 section
    if (currentSection.content.trim()) {
      sections.push({
        title: currentSection.title,
        content: currentSection.content.trim(),
        level: currentSection.level,
        tokens: this.estimateTokens(currentSection.content)
      });
    }
    
    return sections;
  }
}

/**
 * 文本解析器
 */
export class TextParser extends BaseParser {
  async parse(file, options = {}) {
    const content = typeof file === 'string' ? file : file.toString();
    
    logger.debug(`[TextParser] 解析文本，${content.length} 字符`);
    
    // 分段
    const sections = this.splitIntoSections(content, this.maxTokens);
    
    return new ParseResult({
      uri: options.uri,
      format: 'text',
      content: content,
      sections: sections,
      tokens: this.estimateTokens(content),
      metadata: {
        lineCount: content.split('\n').length,
        sectionCount: sections.length
      }
    });
  }
}

/**
 * PDF 解析器（简化版）
 */
export class PDFParser extends BaseParser {
  async parse(file, options = {}) {
    logger.debug(`[PDFParser] 解析 PDF`);
    
    // 实际实现需要使用 PDF 解析库
    // 这里提供简化版本
    
    let content = '';
    
    if (Buffer.isBuffer(file)) {
      // 尝试提取文本
      content = file.toString('utf8');
    } else {
      content = file.toString();
    }
    
    // 清理非文本内容
    content = content.replace(/[^\x20-\x7E\n\r\t]/g, ' ');
    content = content.replace(/\s+/g, ' ').trim();
    
    const sections = this.splitIntoSections(content, this.maxTokens);
    
    return new ParseResult({
      uri: options.uri,
      format: 'pdf',
      content: content,
      sections: sections,
      tokens: this.estimateTokens(content),
      metadata: {
        sectionCount: sections.length
      }
    });
  }
}

/**
 * HTML 解析器
 */
export class HTMLParser extends BaseParser {
  async parse(file, options = {}) {
    const content = typeof file === 'string' ? file : file.toString();
    
    logger.debug(`[HTMLParser] 解析 HTML，${content.length} 字符`);
    
    // 提取文本内容
    const text = this.extractText(content);
    
    // 提取标题
    const title = this.extractTitle(content);
    
    // 提取链接
    const links = this.extractLinks(content);
    
    const sections = this.splitIntoSections(text, this.maxTokens);
    
    return new ParseResult({
      uri: options.uri,
      format: 'html',
      content: text,
      sections: sections,
      tokens: this.estimateTokens(text),
      metadata: {
        title: title,
        linkCount: links.length,
        sectionCount: sections.length
      }
    });
  }
  
  extractText(html) {
    // 移除 script 和 style
    let text = html.replace(/<script[^>]*>[\s\S]*?<\/script>/gi, '');
    text = text.replace(/<style[^>]*>[\s\S]*?<\/style>/gi, '');
    
    // 移除标签
    text = text.replace(/<[^>]+>/g, ' ');
    
    // 清理空白
    text = text.replace(/\s+/g, ' ').trim();
    
    return text;
  }
  
  extractTitle(html) {
    const match = html.match(/<title[^>]*>([^<]+)<\/title>/i);
    return match ? match[1].trim() : '';
  }
  
  extractLinks(html) {
    const links = [];
    const regex = /<a[^>]+href=["']([^"']+)["'][^>]*>([^<]+)<\/a>/gi;
    
    let match;
    while ((match = regex.exec(html)) !== null) {
      links.push({
        url: match[1],
        text: match[2].trim()
      });
    }
    
    return links;
  }
}

/**
 * 代码解析器
 */
export class CodeParser extends BaseParser {
  constructor(options = {}) {
    super(options);
    this.language = options.language || 'auto';
  }
  
  async parse(file, options = {}) {
    const content = typeof file === 'string' ? file : file.toString();
    
    logger.debug(`[CodeParser] 解析代码，${content.length} 字符`);
    
    // 检测语言
    const language = this.detectLanguage(options.filename || '', content);
    
    // 提取结构
    const structure = this.extractStructure(content, language);
    
    const sections = this.splitIntoSections(content, this.maxTokens);
    
    return new ParseResult({
      uri: options.uri,
      format: 'code',
      content: content,
      sections: sections,
      tokens: this.estimateTokens(content),
      metadata: {
        language: language,
        structure: structure,
        sectionCount: sections.length
      }
    });
  }
  
  detectLanguage(filename, content) {
    if (this.language !== 'auto') {
      return this.language;
    }
    
    const ext = filename.split('.').pop().toLowerCase();
    
    const extMap = {
      'js': 'javascript',
      'ts': 'typescript',
      'py': 'python',
      'go': 'go',
      'java': 'java',
      'c': 'c',
      'cpp': 'cpp',
      'rs': 'rust',
      'rb': 'ruby',
      'php': 'php'
    };
    
    return extMap[ext] || 'unknown';
  }
  
  extractStructure(content, language) {
    const structure = {
      imports: [],
      classes: [],
      functions: [],
      variables: []
    };
    
    // 根据语言提取结构
    switch (language) {
      case 'javascript':
      case 'typescript':
        this.extractJSStructure(content, structure);
        break;
      
      case 'python':
        this.extractPythonStructure(content, structure);
        break;
      
      case 'go':
        this.extractGoStructure(content, structure);
        break;
    }
    
    return structure;
  }
  
  extractJSStructure(content, structure) {
    // 提取 imports
    const importRegex = /import\s+.*?from\s+['"]([^'"]+)['"]/g;
    let match;
    while ((match = importRegex.exec(content)) !== null) {
      structure.imports.push(match[1]);
    }
    
    // 提取 classes
    const classRegex = /class\s+(\w+)/g;
    while ((match = classRegex.exec(content)) !== null) {
      structure.classes.push(match[1]);
    }
    
    // 提取 functions
    const funcRegex = /(?:function\s+(\w+)|(?:const|let|var)\s+(\w+)\s*=\s*(?:async\s+)?function|\(([^)]*)\)\s*=>)/g;
    while ((match = funcRegex.exec(content)) !== null) {
      structure.functions.push(match[1] || match[2] || 'anonymous');
    }
  }
  
  extractPythonStructure(content, structure) {
    // 提取 imports
    const importRegex = /import\s+(\w+)|from\s+(\w+)\s+import/g;
    let match;
    while ((match = importRegex.exec(content)) !== null) {
      structure.imports.push(match[1] || match[2]);
    }
    
    // 提取 classes
    const classRegex = /class\s+(\w+)/g;
    while ((match = classRegex.exec(content)) !== null) {
      structure.classes.push(match[1]);
    }
    
    // 提取 functions
    const funcRegex = /def\s+(\w+)/g;
    while ((match = funcRegex.exec(content)) !== null) {
      structure.functions.push(match[1]);
    }
  }
  
  extractGoStructure(content, structure) {
    // 提取 imports
    const importRegex = /import\s+(?:\(([^)]+)\)|"([^"]+)")/g;
    let match;
    while ((match = importRegex.exec(content)) !== null) {
      if (match[1]) {
        const imports = match[1].match(/"([^"]+)"/g);
        if (imports) {
          structure.imports.push(...imports.map(i => i.replace(/"/g, '')));
        }
      } else if (match[2]) {
        structure.imports.push(match[2]);
      }
    }
    
    // 提取 structs
    const structRegex = /type\s+(\w+)\s+struct/g;
    while ((match = structRegex.exec(content)) !== null) {
      structure.classes.push(match[1]);
    }
    
    // 提取 functions
    const funcRegex = /func\s+(?:\([^)]+\)\s+)?(\w+)/g;
    while ((match = funcRegex.exec(content)) !== null) {
      structure.functions.push(match[1]);
    }
  }
}

/**
 * 解析器注册表
 */
export class ParserRegistry {
  constructor() {
    this.parsers = new Map();
    
    // 注册默认解析器
    this.register('md', new MarkdownParser());
    this.register('markdown', new MarkdownParser());
    this.register('txt', new TextParser());
    this.register('pdf', new PDFParser());
    this.register('html', new HTMLParser());
    this.register('htm', new HTMLParser());
    
    // 代码解析器
    const codeParser = new CodeParser();
    this.register('js', codeParser);
    this.register('ts', codeParser);
    this.register('py', codeParser);
    this.register('go', codeParser);
    this.register('java', codeParser);
    this.register('c', codeParser);
    this.register('cpp', codeParser);
    this.register('rs', codeParser);
    this.register('rb', codeParser);
    this.register('php', codeParser);
  }
  
  register(extension, parser) {
    this.parsers.set(extension.toLowerCase(), parser);
  }
  
  getParser(extension) {
    return this.parsers.get(extension.toLowerCase());
  }
  
  hasParser(extension) {
    return this.parsers.has(extension.toLowerCase());
  }
  
  getSupportedFormats() {
    return Array.from(this.parsers.keys());
  }
  
  async parse(file, options = {}) {
    const ext = options.extension || 
      (options.filename ? options.filename.split('.').pop() : 'txt');
    
    const parser = this.getParser(ext);
    
    if (!parser) {
      logger.warn(`[ParserRegistry] 未找到解析器: ${ext}，使用文本解析器`);
      return new TextParser().parse(file, options);
    }
    
    return parser.parse(file, options);
  }
}

/**
 * 获取解析器注册表实例
 */
let defaultRegistry = null;

export function getParserRegistry() {
  if (!defaultRegistry) {
    defaultRegistry = new ParserRegistry();
  }
  return defaultRegistry;
}

export default ParserRegistry;
