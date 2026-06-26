/**
 * Security Guard - 内容安全审查
 * 输入/输出安全检查
 */

import { EventEmitter } from 'events';

/**
 * 内容安全审查器
 */
export class ContentSafety extends EventEmitter {
  constructor(config = {}) {
    super();
    
    // 敏感词列表
    this.sensitiveWords = config.sensitiveWords || [
      // 恶意代码相关
      'rm -rf', 'format', 'del /f', 'drop table', 'delete from',
      // 隐私相关
      'password', 'secret', 'token', 'api_key', 'private_key',
      // 危险操作
      'exec', 'eval', 'system', 'child_process'
    ];
    
    // 从配置添加额外的敏感词
    if (config.blockedPatterns) {
      this.sensitiveWords = [...this.sensitiveWords, ...config.blockedPatterns];
    }
    
    // 最大输入长度
    this.maxInputLength = config.maxInputLength || 10000;
    
    // 危险模式
    this.dangerousPatterns = [
      /rm\s+-rf\s+\//,  // 删除根目录
      />\s*\/dev\/null/,  // 重定向到 null
      /curl\s+.*\|\s*sh/,  // 管道到 shell
      /wget\s+.*\|\s*sh/,
      /eval\s*\(/,  // eval 函数
      /Function\s*\(/,  // Function 构造器
      /child_process/,
      /require\s*\(\s*['"]child_process['"]\s*\)/
    ];
    
    // 个人身份信息 (PII) 模式
    this.piiPatterns = [
      { type: 'email', pattern: /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b/ },
      { type: 'phone', pattern: /\b\d{3}[-.]?\d{3}[-.]?\d{4}\b/ },
      { type: 'ssn', pattern: /\b\d{3}[-]?\d{2}[-]?\d{4}\b/ },
      { type: 'credit_card', pattern: /\b(?:\d[ -]*?){13,16}\b/ },
      { type: 'api_key', pattern: /(?:api[_-]?key|apikey)\s*[:=]\s*['"]?[a-zA-Z0-9]{16,}['"]?/i }
    ];
  }

  /**
   * 检查输入安全
   */
  checkInput(text) {
    const result = {
      safe: true,
      warnings: [],
      blocked: false,
      sanitized: text
    };

    // 检查输入长度
    if (text.length > this.maxInputLength) {
      result.blocked = true;
      result.warnings.push({
        type: 'input_too_long',
        severity: 'high',
        length: text.length,
        maxLength: this.maxInputLength,
        message: `Input exceeds maximum length of ${this.maxInputLength} characters`
      });
      result.safe = false;
      return result;
    }

    // 检查敏感词
    for (const word of this.sensitiveWords) {
      if (text.toLowerCase().includes(word.toLowerCase())) {
        result.warnings.push({
          type: 'sensitive_word',
          severity: 'medium',
          word: word,
          message: `Input contains sensitive word: "${word}"`
        });
      }
    }

    // 检查危险模式
    for (const pattern of this.dangerousPatterns) {
      if (pattern.test(text)) {
        result.blocked = true;
        result.warnings.push({
          type: 'dangerous_pattern',
          severity: 'high',
          pattern: pattern.toString(),
          message: 'Input contains dangerous pattern'
        });
      }
    }

    // 检查 PII
    for (const pii of this.piiPatterns) {
      const matches = text.match(pii.pattern);
      if (matches) {
        result.warnings.push({
          type: 'pii_detected',
          severity: 'medium',
          piiType: pii.type,
          count: matches.length,
          message: `Detected ${matches.length} potential ${pii.type}(s)`
        });
        
        // 脱敏处理
        result.sanitized = this.sanitizePII(result.sanitized, pii);
      }
    }

    result.safe = !result.blocked && result.warnings.filter(w => w.severity === 'high').length === 0;
    
    if (!result.safe) {
      this.emit('input-blocked', { text, result });
    }

    return result;
  }

  /**
   * 检查输出安全
   */
  checkOutput(text) {
    const result = {
      safe: true,
      warnings: [],
      sanitized: text
    };

    // 检查是否包含执行结果中的敏感信息
    const sensitivePatterns = [
      { pattern: /password[:\s]+(\S+)/i, type: 'password' },
      { pattern: /token[:\s]+([a-zA-Z0-9]{20,})/i, type: 'token' },
      { pattern: /key[:\s]+([a-zA-Z0-9]{20,})/i, type: 'key' }
    ];

    for (const sp of sensitivePatterns) {
      const matches = text.match(sp.pattern);
      if (matches) {
        result.warnings.push({
          type: 'sensitive_output',
          severity: 'high',
          detected: sp.type,
          message: `Output may contain ${sp.type}`
        });
        
        // 脱敏
        result.sanitized = result.sanitized.replace(
          matches[1],
          '***REDACTED***'
        );
      }
    }

    result.safe = result.warnings.filter(w => w.severity === 'high').length === 0;
    
    return result;
  }

  /**
   * 脱敏 PII
   */
  sanitizePII(text, pii) {
    switch (pii.type) {
      case 'email':
        return text.replace(pii.pattern, '[EMAIL_REDACTED]');
      case 'phone':
        return text.replace(pii.pattern, '[PHONE_REDACTED]');
      case 'ssn':
        return text.replace(pii.pattern, '[SSN_REDACTED]');
      case 'credit_card':
        return text.replace(pii.pattern, '[CARD_REDACTED]');
      case 'api_key':
        return text.replace(pii.pattern, 'api_key: [KEY_REDACTED]');
      default:
        return text.replace(pii.pattern, '[PII_REDACTED]');
    }
  }

  /**
   * 添加敏感词
   */
  addSensitiveWord(word) {
    if (!this.sensitiveWords.includes(word)) {
      this.sensitiveWords.push(word);
    }
  }

  /**
   * 移除敏感词
   */
  removeSensitiveWord(word) {
    this.sensitiveWords = this.sensitiveWords.filter(w => w !== word);
  }

  /**
   * 添加危险模式
   */
  addDangerousPattern(pattern) {
    this.dangerousPatterns.push(pattern);
  }

  /**
   * 检查代码安全
   */
  checkCode(code, language = 'javascript') {
    const result = {
      safe: true,
      warnings: [],
      imports: [],
      functions: []
    };

    // 检查危险导入
    const importPatterns = {
      javascript: /require\s*\(\s*['"]([^'"]+)['"]\s*\)|import\s+.*?\s+from\s+['"]([^'"]+)['"]/g,
      python: /import\s+(\S+)|from\s+(\S+)\s+import/g
    };

    const pattern = importPatterns[language];
    if (pattern) {
      const matches = code.matchAll(pattern);
      for (const match of matches) {
        const module = match[1] || match[2];
        result.imports.push(module);
        
        // 检查危险模块
        const dangerousModules = ['child_process', 'fs', 'os', 'subprocess', 'sys'];
        if (dangerousModules.some(dm => module.includes(dm))) {
          result.warnings.push({
            type: 'dangerous_import',
            severity: 'medium',
            module,
            message: `Import of potentially dangerous module: ${module}`
          });
        }
      }
    }

    // 检查危险函数
    const dangerousFunctions = ['eval', 'exec', 'system', 'spawn', 'popen'];
    for (const func of dangerousFunctions) {
      const pattern = new RegExp(`\\b${func}\\s*\\(`);
      if (pattern.test(code)) {
        result.warnings.push({
          type: 'dangerous_function',
          severity: 'high',
          function: func,
          message: `Use of dangerous function: ${func}()`
        });
        result.safe = false;
      }
    }

    return result;
  }
}

export default ContentSafety;
