#!/usr/bin/env node

/**
 * 企微 Agent Ops Center — 网络请求守卫 (v2.4)
 *
 * 职责：拦截所有外发 HTTP/HTTPS 请求，校验域名/IP 白名单
 * 对比竞品 feishu-evolver-wrapper 的域名白名单：
 *   - 限定请求域名（竞品限定 open.feishu.cn，我们有可配置白名单）
 *   - 未授权域名自动阻断 + 日志记录
 *   - 支持 IP 白名单 + 域名白名单 + CIDR 范围
 *
 * 设计原则：
 *   - Monkey-patch http/https.request（全局拦截，零侵入）
 *   - 启动时一次性安装，之后所有模块的 HTTP 请求都被守卫
 *   - 支持 bypass 列表（内部/localhost 自动放行）
 *   - 违规请求记录 + 可选的企微告警
 */

const http = require('http');
const https = require('https');
const { EventEmitter } = require('events');
const url = require('url');

const DEFAULTS = {
  mode: 'block',                // 'block' | 'log' | 'off'
  domains: [],                  // 允许的域名列表
  ips: [],                      // 允许的 IP 列表
  cidrs: [],                    // 允许的 CIDR 范围
  autoAllowInternal: true,      // 自动放行 localhost/内网
  internalCIDRs: [              // 内网 CIDR（自动放行）
    '127.0.0.0/8',
    '10.0.0.0/8',
    '172.16.0.0/12',
    '192.168.0.0/16',
    '0.0.0.0/8',
    '::1/128',
  ],
  logBlocked: true,
  logAllowed: false,
};

class NetworkGuard extends EventEmitter {
  constructor(config = {}) {
    super();
    this.config = { ...DEFAULTS, ...config };
    this._installed = false;
    this._stats = {
      total: 0,
      allowed: 0,
      blocked: 0,
      logged: 0,
    };
    this._blockedLog = []; // 最近 100 条阻断记录

    // 编译 CIDR 规则
    this._compiledCIDRs = [
      ...(this.config.autoAllowInternal ? this.config.internalCIDRs : []),
      ...(this.config.cidrs || []),
    ].map(cidr => this._parseCIDR(cidr)).filter(Boolean);

    // 编译域名匹配（支持通配符 *.example.com）
    this._domainPatterns = (this.config.domains || []).map(d => this._compileDomain(d));
    this._ipSet = new Set(this.config.ips || []);
  }

  /**
   * 安装网络拦截（全局生效）
   * 调用后，所有模块的 http/https.request 都会被守卫
   */
  install() {
    if (this._installed) return;
    this._installed = true;

    const guard = this;

    // 保存原始方法
    const _httpRequest = http.request;
    const _httpsRequest = https.request;
    const _httpGet = http.get;
    const _httpsGet = https.get;

    // 包装 http.request
    http.request = function (options, callback) {
      const check = guard._check(options);
      if (!check.allowed) {
        guard._onBlocked(options, check.reason);
        return _blockedRequest(options, callback, check.reason);
      }
      guard._onAllowed(options);
      return _httpRequest.apply(this, arguments);
    };

    // 包装 https.request
    https.request = function (options, callback) {
      const check = guard._check(options);
      if (!check.allowed) {
        guard._onBlocked(options, check.reason);
        return _blockedRequest(options, callback, check.reason);
      }
      guard._onAllowed(options);
      return _httpsRequest.apply(this, arguments);
    };

    // 包装 http.get
    http.get = function (options, callback) {
      const check = guard._check(options);
      if (!check.allowed) {
        guard._onBlocked(options, check.reason);
        return _blockedRequest(options, callback, check.reason);
      }
      guard._onAllowed(options);
      return _httpGet.apply(this, arguments);
    };

    // 包装 https.get
    https.get = function (options, callback) {
      const check = guard._check(options);
      if (!check.allowed) {
        guard._onBlocked(options, check.reason);
        return _blockedRequest(options, callback, check.reason);
      }
      guard._onAllowed(options);
      return _httpsGet.apply(this, arguments);
    };

    // 存储原始方法引用（供 uninstall 使用）
    this._originals = { _httpRequest, _httpsRequest, _httpGet, _httpsGet };

    console.log(`[NetworkGuard] 已安装网络拦截（模式: ${this.config.mode}，白名单域名: ${this.config.domains.length}，白名单IP: ${this.config.ips.length}）`);
  }

  /**
   * 卸载网络拦截（恢复原始方法）
   */
  uninstall() {
    if (!this._installed) return;
    http.request = this._originals._httpRequest;
    https.request = this._originals._httpsRequest;
    http.get = this._originals._httpGet;
    https.get = this._originals._httpsGet;
    this._installed = false;
    console.log('[NetworkGuard] 已卸载网络拦截');
  }

  /**
   * 检查一个请求是否允许
   * @param {string|object} options - URL 字符串或 http.request options
   * @returns {{ allowed: boolean, reason?: string }}
   */
  check(options) {
    return this._check(options);
  }

  /**
   * 获取统计信息
   */
  getStats() {
    return {
      ...this._stats,
      installed: this._installed,
      mode: this.config.mode,
      blockedLog: this._blockedLog.slice(-10),
    };
  }

  /**
   * 获取允许列表
   */
  getAllowedList() {
    return {
      domains: this.config.domains,
      ips: [...this._ipSet],
      cidrs: this._compiledCIDRs.map(c => c.original),
    };
  }

  /**
   * 添加允许域名
   */
  allowDomain(domain) {
    if (!this.config.domains.includes(domain)) {
      this.config.domains.push(domain);
      this._domainPatterns.push(this._compileDomain(domain));
    }
  }

  /**
   * 添加允许 IP
   */
  allowIP(ip) {
    this._ipSet.add(ip);
  }

  // ─── 内部方法 ───────────────────────────────────────────────

  _check(options) {
    this._stats.total++;

    // 解析目标主机名
    let hostname = '';
    let port = 0;

    if (typeof options === 'string') {
      try {
        const parsed = new url.URL(options);
        hostname = parsed.hostname;
        port = parsed.port ? parseInt(parsed.port, 10) : (parsed.protocol === 'https:' ? 443 : 80);
      } catch {
        // 可能是仅路径
        try {
          const parsed = new url.URL('http://' + options);
          hostname = parsed.hostname;
        } catch {
          return { allowed: false, reason: `无法解析: ${options}` };
        }
      }
    } else if (options.hostname || options.host) {
      hostname = options.hostname || options.host;
      port = options.port || (options.protocol === 'https:' ? 443 : 80);
    } else if (options.href) {
      try {
        const parsed = new url.URL(options.href);
        hostname = parsed.hostname;
      } catch {
        return { allowed: false, reason: `无法解析 href: ${options.href}` };
      }
    } else {
      // 无法确定目标，放行（Unix socket / pipe 等）
      return { allowed: true };
    }

    if (!hostname) return { allowed: false, reason: 'hostname 为空' };

    // 1. 检查 IP 白名单（直接匹配）
    if (this._ipSet.has(hostname)) {
      return { allowed: true };
    }

    // 2. 检查 CIDR 范围
    if (this._compiledCIDRs.length > 0) {
      const ip = this._resolveHostname(hostname);
      if (ip) {
        for (const cidr of this._compiledCIDRs) {
          if (this._ipInCIDR(ip, cidr)) {
            return { allowed: true };
          }
        }
      }
    }

    // 3. 检查域名白名单
    if (this._domainPatterns.length > 0) {
      for (const pattern of this._domainPatterns) {
        if (pattern.test(hostname)) {
          return { allowed: true };
        }
      }
    }

    // 4. 无匹配 → 阻断或记录
    return { allowed: false, reason: `${hostname}:${port} 不在白名单中` };
  }

  _onAllowed(options) {
    this._stats.allowed++;
    if (this.config.logAllowed) {
      const host = this._extractHost(options);
      console.log(`[NetworkGuard] ✅ ${host}`);
    }
  }

  _onBlocked(options, reason) {
    this._stats.blocked++;
    const host = this._extractHost(options);

    // 记录阻断日志
    const entry = {
      host,
      reason,
      timestamp: Date.now(),
      stack: new Error().stack?.split('\n').slice(2, 6).join('\n') || '',
    };
    this._blockedLog.push(entry);
    if (this._blockedLog.length > 100) this._blockedLog.shift();

    if (this.config.logBlocked) {
      console.warn(`[NetworkGuard] 🔒 阻断: ${host} — ${reason}`);
    }

    this.emit('request:blocked', entry);
  }

  _extractHost(options) {
    if (typeof options === 'string') return options;
    if (options.hostname) return `${options.hostname}:${options.port || 80}`;
    if (options.host) return `${options.host}:${options.port || 80}`;
    if (options.href) return options.href;
    return JSON.stringify(options).substring(0, 80);
  }

  /**
   * 编译域名为匹配函数
   * 支持通配符: *.example.com → 匹配 a.example.com, b.c.example.com
   */
  _compileDomain(domain) {
    if (domain.startsWith('*.')) {
      const suffix = domain.slice(2);
      // *.example.com → /(^|\.)example\.com$/
      return new RegExp(`(^|\\.)${this._escapeRegex(suffix)}$`, 'i');
    }
    // 精确匹配
    return new RegExp(`^${this._escapeRegex(domain)}$`, 'i');
  }

  _escapeRegex(str) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  /**
   * 解析 CIDR 字符串为 { ip, prefix }
   */
  _parseCIDR(cidr) {
    try {
      const [ip, prefix] = cidr.split('/');
      if (!ip || !prefix) return null;
      return {
        original: cidr,
        ip: ip.trim(),
        prefix: parseInt(prefix, 10),
        mask: this._prefixToMask(parseInt(prefix, 10)),
      };
    } catch {
      return null;
    }
  }

  /**
   * CIDR prefix → 子网掩码（IPv4）
   */
  _prefixToMask(prefix) {
    if (prefix === 0) return 0;
    return (~0) << (32 - prefix);
  }

  /**
   * IPv4 地址转整数
   */
  _ipToInt(ip) {
    const parts = ip.split('.');
    return (parseInt(parts[0]) << 24) |
           (parseInt(parts[1]) << 16) |
           (parseInt(parts[2]) << 8) |
           parseInt(parts[3]);
  }

  /**
   * 检查 IP 是否在 CIDR 范围内
   */
  _ipInCIDR(ip, cidr) {
    try {
      const ipInt = this._ipToInt(ip);
      const netInt = this._ipToInt(cidr.ip);
      return (ipInt & cidr.mask) === (netInt & cidr.mask);
    } catch {
      return false;
    }
  }

  /**
   * 解析 hostname 是否为 IP 地址
   */
  _resolveHostname(hostname) {
    // 简单判断：如果是纯 IP 格式直接返回
    const ipv4Regex = /^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/;
    if (ipv4Regex.test(hostname)) return hostname;

    // 如果是 localhost
    if (hostname === 'localhost' || hostname === '127.0.0.1') return '127.0.0.1';

    return null; // 域名无法直接解析为 IP（不做 DNS 解析，性能考虑）
  }
}

/**
 * 创建一个假的请求对象，立即返回错误（阻断用）
 */
function _blockedRequest(options, callback, reason) {
  const blockedReq = new http.ClientRequest('http://blocked.invalid');
  blockedReq._blocked = true;

  // 模拟 EventEmitter 行为
  process.nextTick(() => {
    const err = new Error(`[NetworkGuard] 请求被阻断: ${reason}`);
    err.code = 'NETWORK_BLOCKED';

    if (callback) {
      blockedReq.once = (event, cb) => {
        if (event === 'response') {
          // 不触发 response
        }
        return blockedReq;
      };
    }

    // 给调用方一个错误事件
    blockedReq.emit('error', err);

    // 如果调用方监听了 error，上面的 emit 已经触发了
    // 如果没有（大多数情况），这里会被 auto-background 吞掉
  });

  return blockedReq;
}

module.exports = { NetworkGuard };
