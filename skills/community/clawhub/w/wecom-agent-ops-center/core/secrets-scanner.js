#!/usr/bin/env node

/**
 * 企微 Agent Ops Center — 敏感信息扫描器 (v2.4)
 *
 * 职责：在消息发送到企微前，扫描并阻断敏感信息泄露
 * 对比竞品 feishu-evolver-wrapper 的 Secrets 防护：
 *   - SECRET_PATTERNS 扫描机制（竞品有，我们补齐）
 *   - API Key、私钥、Token、密码等敏感信息检测
 *   - 可配置：阻断/脱敏/仅告警三种模式
 *
 * 设计原则：
 *   - 内置 15+ 种常见敏感信息正则模式
 *   - 支持自定义模式扩展
 *   - 三种处理策略：block（阻断）/ redact（脱敏）/ warn（仅告警）
 *   - 扫描结果可推送到企微群（管理告警）
 */

const { EventEmitter } = require('events');

/**
 * 内置敏感信息检测模式库
 *
 * 覆盖类型：
 *   - API Keys (OpenAI / AWS / GitHub / Stripe 等)
 *   - 私钥 (RSA / EC / DSA / OpenSSH)
 *   - Tokens (JWT / OAuth / Bearer)
 *   - 密码 / 凭证
 *   - 连接字符串 (数据库 / Redis / 云服务)
 *   - 证书内容
 *
 * ⚠️ JS 正则不支持 (?i) 内联修饰符，必须用 /regex/i 的 flags 方式
 */
const BUILTIN_PATTERNS = [
  // ── API Keys ──────────────────────────────────────
  {
    name: 'OpenAI API Key',
    pattern: /sk-[A-Za-z0-9]{32,}/g,
    severity: 'high',
    category: 'api_key',
  },
  {
    name: 'GitHub Token',
    pattern: /gh[pousr]_[A-Za-z0-9_]{36,}/gi,
    severity: 'high',
    category: 'api_key',
  },
  {
    name: 'AWS Access Key',
    pattern: /AKIA[0-9A-Z]{16}/g,
    severity: 'high',
    category: 'api_key',
  },
  {
    name: 'AWS Secret Key',
    // JS 不支持零宽断言内插值，改用较宽松匹配
    pattern: /aws.{0,30}(secret|key).{0,5}[:=]\s*['"]?[A-Za-z0-9/+]{20,40}['"]?\s/gi,
    severity: 'critical',
    category: 'api_key',
  },
  {
    name: 'Stripe Live Key',
    pattern: /sk_live_[0-9a-zA-Z]{24,}/g,
    severity: 'critical',
    category: 'api_key',
  },
  {
    name: 'Stripe Test Key',
    pattern: /sk_test_[0-9a-zA-Z]{24,}/g,
    severity: 'medium',
    category: 'api_key',
  },
  {
    name: 'Slack Bot Token',
    pattern: /xox[baprs]-[0-9a-zA-Z-]{10,}/g,
    severity: 'high',
    category: 'api_key',
  },
  {
    name: 'Slack Webhook',
    pattern: /https:\/\/hooks\.slack\.com\/services\/[A-Za-z0-9/]+/g,
    severity: 'medium',
    category: 'api_key',
  },
  {
    name: 'Generic API Key Pattern',
    pattern: /(api[_-]?key|apikey|api[_-]?secret).{0,5}?[:=]\s*['"]?[A-Za-z0-9_\-]{20,}[^'"]?/gi,
    severity: 'high',
    category: 'api_key',
  },
  {
    name: 'Generic Secret/Token Pattern',
    pattern: /(secret|token|password|passwd).{0,5}?[:=]\s*['"]?([^\s'"]{8,})/gi,
    severity: 'high',
    category: 'credential',
  },
  {
    name: 'WeChat Bot Secret',
    pattern: /[A-Za-z0-9_-]{32,64}/g,
    severity: 'medium',
    category: 'api_key',
    contextCheck: (text, match) => {
      const ctx = text.substring(Math.max(0, match.index - 50), match.index + match[0].length + 50);
      return /(secret|bot|token|key)/i.test(ctx);
    },
  },

  // ── 私钥 ─────────────────────────────────────────
  {
    name: 'RSA Private Key',
    pattern: /-----BEGIN RSA PRIVATE KEY-----[\s\S]{20,}-----END RSA PRIVATE KEY-----/g,
    severity: 'critical',
    category: 'private_key',
  },
  {
    name: 'EC Private Key',
    pattern: /-----BEGIN EC PRIVATE KEY-----[\s\S]{20,}-----END EC PRIVATE KEY-----/g,
    severity: 'critical',
    category: 'private_key',
  },
  {
    name: 'OpenSSH Private Key',
    pattern: /-----BEGIN OPENSSH PRIVATE KEY-----[\s\S]{20,}-----END OPENSSH PRIVATE KEY-----/g,
    severity: 'critical',
    category: 'private_key',
  },
  {
    name: 'Generic Private Key',
    pattern: /-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]{20,}-----END [A-Z ]*PRIVATE KEY-----/g,
    severity: 'critical',
    category: 'private_key',
  },

  // ── Tokens ─────────────────────────────────────────
  {
    name: 'JWT Token',
    pattern: /eyJ[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}\.[A-Za-z0-9_-]{10,}/g,
    severity: 'medium',
    category: 'token',
  },
  {
    name: 'Bearer Token in Header',
    pattern: /authorization.{0,10}bearer\s+[A-Za-z0-9_\-\.]{20,}/gi,
    severity: 'high',
    category: 'token',
  },

  // ── 连接字符串 ──────────────────────────────────────
  {
    name: 'Database Connection String',
    pattern: /(mongodb|mysql|postgres|postgresql|redis|sqlite):\/\/[^@\s]+:[^@\s]+@[^\s]+/gi,
    severity: 'high',
    category: 'connection_string',
  },
  {
    name: 'JDBC Connection String',
    pattern: /jdbc:[a-z]+:\/\/[^@\s]+:[^@\s]+@[^\s]+/gi,
    severity: 'high',
    category: 'connection_string',
  },

  // ── 其他 ─────────────────────────────────────────
  {
    name: 'Tencent Cloud SecretId',
    pattern: /AKID[0-9A-Za-z]{32,48}/g,
    severity: 'high',
    category: 'api_key',
  },
  {
    name: 'Alibaba Cloud AccessKey',
    pattern: /LTAI[0-9A-Za-z]{16,24}/g,
    severity: 'high',
    category: 'api_key',
  },
  {
    name: 'Generic Hex Secret',
    pattern: /(secret|key|token).{0,10}[:=]\s*['"]?([0-9a-fA-F]{32,64})['"]?/gi,
    severity: 'medium',
    category: 'credential',
  },
];

class SecretsScanner extends EventEmitter {
  constructor(config = {}) {
    super();
    this.config = {
      mode: config.mode || 'block',     // 'block' | 'redact' | 'warn'
      customPatterns: config.customPatterns || [],
      enabledCategories: config.enabledCategories || null, // null = all
      ignorePatterns: config.ignorePatterns || [],  // 白名单（已知无害模式）
      maxScanLength: config.maxScanLength || 100_000, // 最大扫描长度
    };

    // 合并内置 + 自定义模式
    this._patterns = [...BUILTIN_PATTERNS];
    for (const p of this.config.customPatterns) {
      if (p.name && p.pattern) {
        this._patterns.push({
          name: p.name,
          // 自定义 pattern 支持字符串或 RegExp 对象
          pattern: typeof p.pattern === 'string' ? new RegExp(p.pattern, 'gi') : p.pattern,
          severity: p.severity || 'medium',
          category: p.category || 'custom',
        });
      }
    }

    // 按分类过滤
    if (this.config.enabledCategories) {
      this._patterns = this._patterns.filter(p =>
        this.config.enabledCategories.includes(p.category)
      );
    }
  }

  /**
   * 扫描文本，返回检测到的所有敏感信息
   * @param {string} text - 待扫描文本
   * @param {object} [context] - 附加上下文（来源、时间等）
   * @returns {{ findings: Finding[], safe: boolean }}
   */
  scan(text, context = {}) {
    if (!text || typeof text !== 'string') return { findings: [], safe: true };

    const scanText = text.length > this.config.maxScanLength
      ? text.substring(0, this.config.maxScanLength)
      : text;

    const findings = [];

    for (const rule of this._patterns) {
      // 每次重置 lastIndex（全局正则必须）
      const re = new RegExp(rule.pattern.source, rule.pattern.flags);
      let match;
      while ((match = re.exec(scanText)) !== null) {
        const matched = match[0];

        // 白名单检查
        if (this._isWhitelisted(matched)) continue;

        // 上下文检查（如配置）
        if (rule.contextCheck && !rule.contextCheck(scanText, match)) continue;

        findings.push({
          rule: rule.name,
          category: rule.category,
          severity: rule.severity,
          matched: matched.substring(0, 50), // 截断避免日志过大
          index: match.index,
          length: matched.length,
          context: this._getContext(scanText, match.index, Math.min(matched.length, 50)),
          timestamp: Date.now(),
        });
      }
    }

    // 去重（同一位置同一规则只保留一条）
    const unique = this._deduplicate(findings);

    if (unique.length > 0) {
      this.emit('secrets:detected', {
        count: unique.length,
        findings: unique,
        source: context.source || 'unknown',
        timestamp: Date.now(),
      });
    }

    return { findings: unique, safe: unique.length === 0 };
  }

  /**
   * 扫描并处理：根据 mode 执行相应操作
   * @returns {{ safe: boolean, text: string, findings: Finding[], blocked: boolean }}
   */
  process(text, context = {}) {
    const { findings, safe } = this.scan(text, context);

    if (safe) return { safe: true, text, findings: [], blocked: false };

    // 检查是否有 critical 级别的泄漏
    const hasCritical = findings.some(f => f.severity === 'critical');

    switch (this.config.mode) {
      case 'block':
        // 阻断：不发送
        this.emit('secrets:blocked', { findings, text, context });
        return { safe: false, text: '', findings, blocked: true };

      case 'redact':
        // 脱敏：替换匹配内容为 [REDACTED]
        let redactedText = text;
        // 按位置倒序替换（避免索引偏移）
        const sorted = [...findings].sort((a, b) => b.index - a.index);
        for (const f of sorted) {
          const redacted = `[${f.category.toUpperCase()}_REDACTED]`;
          redactedText = redactedText.substring(0, f.index) + redacted + redactedText.substring(f.index + f.length);
        }
        this.emit('secrets:redacted', { originalCount: findings.length, redactedText });
        return { safe: true, text: redactedText, findings, blocked: false };

      case 'warn':
      default:
        // 仅告警：原样发送，但推送告警
        this.emit('secrets:warning', { findings, text, context });
        return { safe: true, text, findings, blocked: false };
    }
  }

  /**
   * 获取统计信息
   */
  getStats() {
    return {
      totalPatterns: this._patterns.length,
      byCategory: this._patterns.reduce((acc, p) => {
        acc[p.category] = (acc[p.category] || 0) + 1;
        return acc;
      }, {}),
      bySeverity: this._patterns.reduce((acc, p) => {
        acc[p.severity] = (acc[p.severity] || 0) + 1;
        return acc;
      }, {}),
      mode: this.config.mode,
    };
  }

  /**
   * 添加自定义模式
   */
  addPattern(pattern) {
    if (!pattern.name || !pattern.pattern) {
      throw new Error('Pattern requires name and pattern');
    }
    this._patterns.push({
      name: pattern.name,
      pattern: typeof pattern.pattern === 'string' ? new RegExp(pattern.pattern, 'gi') : pattern.pattern,
      severity: pattern.severity || 'medium',
      category: pattern.category || 'custom',
      contextCheck: pattern.contextCheck || null,
    });
  }

  /**
   * 切换模式
   */
  setMode(mode) {
    if (!['block', 'redact', 'warn'].includes(mode)) {
      throw new Error(`Invalid mode: ${mode}. Must be block|redact|warn`);
    }
    this.config.mode = mode;
  }

  // ─── 内部方法 ──────────────────────────────────────────────

  _isWhitelisted(matched) {
    if (!this.config.ignorePatterns || this.config.ignorePatterns.length === 0) return false;
    for (const p of this.config.ignorePatterns) {
      const re = typeof p === 'string' ? new RegExp(p, 'i') : p;
      if (re.test(matched)) return true;
    }
    return false;
  }

  _getContext(text, index, length) {
    const ctxLen = 40;
    const start = Math.max(0, index - ctxLen);
    const end = Math.min(text.length, index + length + ctxLen);
    const prefix = start > 0 ? '...' : '';
    const suffix = end < text.length ? '...' : '';
    return prefix + text.substring(start, end) + suffix;
  }

  _deduplicate(findings) {
    const seen = new Set();
    return findings.filter(f => {
      const key = `${f.rule}|${f.index}|${f.length}`;
      if (seen.has(key)) return false;
      seen.add(key);
      return true;
    });
  }

  /**
   * 获取所有启用的规则摘要（供 dashboard 展示）
   * 不返回完整正则对象（无法序列化），只返回元数据
   */
  getRules() {
    return this._patterns.map(p => ({
      name: p.name,
      category: p.category,
      severity: p.severity,
      hasContextCheck: typeof p.contextCheck === 'function',
    }));
  }
}

module.exports = { SecretsScanner, BUILTIN_PATTERNS };
