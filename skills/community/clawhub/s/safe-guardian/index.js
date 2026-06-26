#!/usr/bin/env node

/**
 * Safe Guardian - 安全的OpenClaw守护层
 * 核心功能：拦截危险工具调用，多层次安全过滤
 */

const fs = require('fs');
const path = require('path');

class SafeGuardian {
  constructor(options = {}) {
    this.config = {
      logPath: options.logPath || './logs/guardian.log',
      blacklistPath: options.blacklistPath || './config/blacklist.json',
      whitelistPath: options.whitelistPath || './config/whitelist.json',
      safeMode: options.safeMode !== false,
      strictMode: options.strictMode || false,
      ...options
    };

    this.initialize();
  }

  initialize() {
    // 确保目录存在
    const dirs = [
      path.dirname(this.config.logPath),
      './config',
      './logs/guardian'
    ];

    dirs.forEach(dir => {
      if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
      }
    });

    // 加载配置
    this.loadBlacklist();
    this.loadWhitelist();

    // 创建默认黑名单（如果不存在）
    this.createDefaultBlacklist();
  }

  loadBlacklist() {
    try {
      if (fs.existsSync(this.config.blacklistPath)) {
        const data = fs.readFileSync(this.config.blacklistPath, 'utf8');
        this.blacklist = JSON.parse(data);
      } else {
        this.blacklist = [];
      }
    } catch (error) {
      console.error('Failed to load blacklist:', error);
      this.blacklist = [];
    }
  }

  loadWhitelist() {
    try {
      if (fs.existsSync(this.config.whitelistPath)) {
        const data = fs.readFileSync(this.config.whitelistPath, 'utf8');
        this.whitelist = JSON.parse(data);
      } else {
        this.whitelist = [];
      }
    } catch (error) {
      console.error('Failed to load whitelist:', error);
      this.whitelist = [];
    }
  }

  createDefaultBlacklist() {
    const defaultBlacklist = [
      {
        name: 'dangerous-exec',
        patterns: [
          'rm -rf /',
          'mkfs',
          'dd if=/dev/zero',
          'fdisk',
          'format',
          'shutdown',
          'reboot',
          'killall -9',
          'systemctl stop',
          'systemctl disable'
        ],
        severity: 'critical'
      },
      {
        name: 'data-deletion',
        patterns: [
          'rm -rf .*',
          'del .*',
          'delete .*'
        ],
        severity: 'high'
      },
      {
        name: 'system-modification',
        patterns: [
          'useradd',
          'usermod',
          'chmod 777',
          'chown root',
          'su -'
        ],
        severity: 'high'
      },
      {
        name: 'network-operation',
        patterns: [
          'iptables -F',
          'iptables -X',
          'iptables -t nat -F',
          'iptables -P INPUT DROP',
          'iptables -P OUTPUT DROP'
        ],
        severity: 'medium'
      }
    ];

    // 保存默认黑名单
    fs.writeFileSync(
      this.config.blacklistPath,
      JSON.stringify(defaultBlacklist, null, 2)
    );
    this.blacklist = defaultBlacklist;
  }

  /**
   * 检查工具调用是否安全
   */
  checkToolCall(toolCall) {
    if (!this.config.safeMode) {
      return { allowed: true, reason: 'Safe mode disabled' };
    }

    // 检查白名单
    if (this.isWhitelisted(toolCall)) {
      return { 
        allowed: true, 
        reason: 'Whitelisted operation',
        type: 'whitelist'
      };
    }

    // 检查黑名单
    const blacklistCheck = this.checkBlacklist(toolCall);
    if (blacklistCheck.blocked) {
      return {
        allowed: false,
        reason: blacklistCheck.reason,
        type: 'blacklist'
      };
    }

    // 严格模式下进行意图验证
    if (this.config.strictMode) {
      const intentCheck = this.validateIntent(toolCall);
      if (!intentCheck.safe) {
        return {
          allowed: false,
          reason: `Intent validation failed: ${intentCheck.reason}`,
          type: 'intent'
        };
      }
    }

    return { 
      allowed: true, 
      reason: 'Allowed',
      type: 'passed'
    };
  }

  /**
   * 检查白名单
   */
  isWhitelisted(toolCall) {
    return this.whitelist.some(item => {
      // 简单的白名单匹配逻辑
      return (
        (item.pattern && item.pattern.test(toolCall)) ||
        (item.command && toolCall.includes(item.command))
      );
    });
  }

  /**
   * 检查黑名单
   */
  checkBlacklist(toolCall) {
    for (const rule of this.blacklist) {
      for (const pattern of rule.patterns) {
        const regex = new RegExp(pattern, 'i');
        if (regex.test(toolCall)) {
          return {
            blocked: true,
            reason: `Blocked by blacklist rule: ${rule.name}`,
            severity: rule.severity
          };
        }
      }
    }
    return { blocked: false };
  }

  /**
   * 验证意图（基于LLM）
   */
  validateIntent(toolCall) {
    // 这里可以实现更复杂的意图验证
    // 目前使用简单的规则引擎作为示例
    
    const suspiciousPatterns = [
      /rm -rf/gi,
      /dd if=\/dev/gi,
      /mkfs/gi,
      /format/gi
    ];

    for (const pattern of suspiciousPatterns) {
      if (pattern.test(toolCall)) {
        return {
          safe: false,
          reason: 'Suspicious pattern detected'
        };
      }
    }

    return { safe: true };
  }

  /**
   * 记录操作
   */
  logOperation(result, toolCall) {
    const logEntry = {
      timestamp: new Date().toISOString(),
      type: 'guardian_check',
      toolCall,
      result,
      mode: this.config.safeMode ? 'safe' : 'unsafe'
    };

    fs.appendFileSync(
      this.config.logPath,
      JSON.stringify(logEntry) + '\n'
    );

    return logEntry;
  }

  /**
   * 添加规则到黑名单
   */
  addBlacklistRule(rule) {
    this.blacklist.push({
      name: rule.name,
      patterns: rule.patterns || [],
      severity: rule.severity || 'medium'
    });

    fs.writeFileSync(
      this.config.blacklistPath,
      JSON.stringify(this.blacklist, null, 2)
    );

    return this.blacklist;
  }

  /**
   * 添加到白名单
   */
  addToWhitelist(item) {
    this.whitelist.push(item);
    fs.writeFileSync(
      this.config.whitelistPath,
      JSON.stringify(this.whitelist, null, 2)
    );
    return this.whitelist;
  }

  /**
   * 获取审计日志
   */
  getAuditLog() {
    try {
      if (fs.existsSync(this.config.logPath)) {
        const data = fs.readFileSync(this.config.logPath, 'utf8');
        const logs = data.trim().split('\n').filter(line => line);
        return logs.map(line => JSON.parse(line));
      }
    } catch (error) {
      console.error('Failed to read audit log:', error);
    }
    return [];
  }

  /**
   * 获取安全报告
   */
  getSecurityReport() {
    const logs = this.getAuditLog();
    const blockedCount = logs.filter(log => !log.result.allowed).length;
    const allowedCount = logs.filter(log => log.result.allowed).length;

    return {
      totalChecks: logs.length,
      blocked: blockedCount,
      allowed: allowedCount,
      blockRate: logs.length > 0 ? (blockedCount / logs.length * 100).toFixed(2) : 0,
      blacklistRules: this.blacklist.length,
      whitelistEntries: this.whitelist.length
    };
  }
}

// 导出
module.exports = SafeGuardian;
