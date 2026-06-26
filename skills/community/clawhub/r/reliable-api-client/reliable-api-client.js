/**
 * Node.js Reliable API Client - 黄金标准 v3.3.0
 * 
 * 整合: 多Endpoint(各配单Key) + 可配置路径 + 可配置鉴权 + 限流 + 熔断器
 * 
 * @author node_e540d71c4944e33a
 * @version 3.3.0
 */

const EventEmitter = require('events');
const https = require('https');
const http = require('http');
const { URL } = require('url');

// ==================== 0. Endpoint 管理器 ====================
class EndpointManager {
  constructor(options = {}) {
    this.endpoints = [];  // [{ url, key, priority, paths: {}, auth: {}, ... }]
    this.strategy = options.strategy || 'priority';
    this.healthCheck = options.healthCheck !== false;
    this.failover = options.failover !== false;
    this.healthCheckInterval = options.healthCheckInterval || 30000;
    this.errorCooldown = options.errorCooldown || 60000;
    this.authCooldown = options.authCooldown || 3600000; // 401/403 冷却 1小时
    
    this.currentIndex = 0;
    this.stats = {};
    
    if (this.healthCheck) this.startHealthCheck();
  }
  
  /**
   * 添加 Endpoint + Key + 配置
   */
  addEndpoint(url, key, options = {}) {
    const fullUrl = url.startsWith('http') ? url : `https://${url}`;
    
    const existing = this.endpoints.find(e => e.url === fullUrl);
    const entry = {
      url: fullUrl,
      key,
      priority: options.priority || 0,
      // 路径配置
      paths: {
        chat: options.chatPath || '/v1/chat/completions',
        completions: options.completionsPath || '/v1/completions',
        embeddings: options.embeddingsPath || '/v1/embeddings'
      },
      // 鉴权配置
      auth: {
        header: options.authHeader || 'Authorization',
        prefix: options.authPrefix !== undefined ? options.authPrefix : 'Bearer'
      }
    };
    
    if (existing) {
      Object.assign(existing, entry);
      existing.priority = Math.max(existing.priority, options.priority || 0);
    } else {
      this.endpoints.push(entry);
    }
    
    if (!this.stats[fullUrl]) {
      this.stats[fullUrl] = {
        requests: 0,
        errors: 0,
        lastUsed: null,
        healthy: true,
        cooldownUntil: null,
        disabled: false,  // 永久禁用
        latency: null
      };
    }
  }
  
  /**
   * 获取下一个可用的 Endpoint
   */
  getNextEndpoint() {
    const healthy = this.endpoints.filter(e => this.isHealthy(e.url));
    
    if (healthy.length === 0) {
      if (this.endpoints.length > 0) {
        console.warn('[EndpointManager] No healthy, returning highest priority');
        return [...this.endpoints].sort((a, b) => b.priority - a.priority)[0];
      }
      return null;
    }
    
    let selected;
    
    if (this.strategy === 'priority') {
      selected = [...healthy].sort((a, b) => b.priority - a.priority)[0];
    } else if (this.strategy === 'least-used') {
      selected = healthy.reduce((min, e) =>
        (this.stats[e.url]?.requests || 0) < (this.stats[min.url]?.requests || 0) ? e : min
      );
    } else {
      // round-robin
      let attempts = 0;
      while (attempts < healthy.length) {
        const e = healthy[this.currentIndex % healthy.length];
        this.currentIndex++;
        if (this.isHealthy(e.url)) { selected = e; break; }
        attempts++;
      }
    }
    
    if (selected) {
      this.stats[selected.url].requests++;
      this.stats[selected.url].lastUsed = Date.now();
    }
    
    return selected;
  }
  
  isHealthy(url) {
    const s = this.stats[url];
    if (!s) return false;
    if (s.disabled) return false;  // 永久禁用
    if (!s.healthy) {
      if (s.cooldownUntil && Date.now() > s.cooldownUntil) {
        s.healthy = true;
        s.cooldownUntil = null;
        console.log(`[EndpointManager] Recovered: ${this.mask(url)}`);
        return true;
      }
      return false;
    }
    return true;
  }
  
  markError(url, errorType) {
    const s = this.stats[url];
    if (!s) return;
    
    s.errors++;
    s.lastUsed = Date.now();
    
    const et = String(errorType).toLowerCase();
    
    // 429 rate limit - 临时冷却
    if (et.includes('429') || et.includes('rate limit')) {
      if (this.failover) {
        s.healthy = false;
        s.cooldownUntil = Date.now() + this.errorCooldown;
        console.warn(`[EndpointManager] Rate limited: ${this.mask(url)}, cooldown ${this.errorCooldown}ms`);
      }
    }
    // 5xx - 临时冷却
    else if (et.includes('5')) {
      s.healthy = false;
      s.cooldownUntil = Date.now() + this.errorCooldown;
      console.warn(`[EndpointManager] 5xx: ${this.mask(url)}, cooldown ${this.errorCooldown}ms`);
    }
    // 401/403 - 永久禁用
    else if (et.includes('401') || et.includes('unauthorized') || et.includes('403') || et.includes('forbidden')) {
      s.healthy = false;
      s.disabled = true;
      console.error(`[EndpointManager] Auth failed (permanent): ${this.mask(url)}`);
    }
  }
  
  /**
   * 手动启用被禁用的 endpoint
   */
  enableEndpoint(url) {
    if (this.stats[url]) {
      this.stats[url].disabled = false;
      this.stats[url].healthy = true;
      this.stats[url].cooldownUntil = null;
    }
  }
  
  /**
   * 列出所有 endpoint 状态
   */
  listEndpoints() {
    return this.endpoints.map(e => ({
      url: this.mask(e.url),
      priority: e.priority,
      paths: e.paths,
      auth: { header: e.auth.header, prefix: e.auth.prefix ? e.auth.prefix + ' ' : '' },
      healthy: this.isHealthy(e.url),
      stats: this.stats[e.url]
    }));
  }
  
  updateLatency(url, latencyMs) {
    if (this.stats[url]) this.stats[url].latency = latencyMs;
  }
  
  mask(url) {
    try { const u = new URL(url); return `${u.protocol}//${u.hostname}:***`; }
    catch { return '****'; }
  }
  
  getStats() {
    return {
      total: this.endpoints.length,
      healthy: this.endpoints.filter(e => this.isHealthy(e.url)).length,
      details: this.stats
    };
  }
  
  startHealthCheck() {
    this.healthCheckTimer = setInterval(() => {
      this.endpoints.forEach(e => this.isHealthy(e.url));
    }, this.healthCheckInterval);
  }
  
  stopHealthCheck() {
    if (this.healthCheckTimer) clearInterval(this.healthCheckTimer);
  }
}

// ==================== 1. 限流器 ====================
class SlidingWindowRateLimiter {
  constructor(options = {}) {
    this.maxQPS = options.maxQPS || 10;
    this.windowMs = options.windowMs || 1000;
    this.requests = [];
  }
  
  async acquire() {
    const now = Date.now();
    this.requests = this.requests.filter(t => now - t < this.windowMs);
    if (this.requests.length >= this.maxQPS) {
      const wait = this.windowMs - (now - this.requests[0]);
      if (wait > 0) await this.sleep(wait);
      return this.acquire();
    }
    this.requests.push(now);
    return true;
  }
  
  sleep(ms) { return new Promise(r => setTimeout(r, ms)); }
}

// ==================== 2. 连接池 ====================
class ConnectionPool {
  constructor(options = {}) {
    this.maxSize = options.poolSize || 20;
    this.pool = [];
    this.waiting = [];
  }
  
  async acquire() {
    if (this.pool.length > 0) return this.pool.pop();
    if (this.pool.length < this.maxSize) return { id: Date.now() };
    return new Promise(r => this.waiting.push(r));
  }
  
  release(conn) {
    if (this.waiting.length > 0) this.waiting.shift()(conn);
    else if (this.pool.length < this.maxSize) this.pool.push(conn);
  }
}

// ==================== 3. 熔断器 ====================
class CircuitBreaker extends EventEmitter {
  static STATES = { CLOSED: 'closed', OPEN: 'open', HALF_OPEN: 'half_open' };
  
  constructor(options = {}) {
    super();
    this.failureThreshold = options.failureThreshold || 5;
    this.successThreshold = options.successThreshold || 2;
    this.timeout = options.timeout || 30000;
    this.state = CircuitBreaker.STATES.CLOSED;
    this.failures = 0;
    this.successes = 0;
    this.lastFailureTime = null;
  }
  
  async execute(fn) {
    if (this.state === CircuitBreaker.STATES.OPEN) {
      if (Date.now() - this.lastFailureTime > this.timeout) {
        this.state = CircuitBreaker.STATES.HALF_OPEN;
      } else {
        throw new Error('Circuit breaker is OPEN');
      }
    }
    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (e) {
      this.onFailure();
      throw e;
    }
  }
  
  onSuccess() {
    this.failures = 0;
    if (this.state === CircuitBreaker.STATES.HALF_OPEN) {
      this.successes++;
      if (this.successes >= this.successThreshold) {
        this.state = CircuitBreaker.STATES.CLOSED;
        this.successes = 0;
      }
    }
  }
  
  onFailure() {
    this.failures++;
    this.lastFailureTime = Date.now();
    if (this.state === CircuitBreaker.STATES.HALF_OPEN || this.failures >= this.failureThreshold) {
      this.state = CircuitBreaker.STATES.OPEN;
    }
  }
  
  getState() { return this.state; }
}

// ==================== 4. 指数退避 ====================
class ExponentialBackoff {
  constructor(options = {}) {
    this.maxRetries = options.maxRetries || 3;
    this.baseDelay = options.baseDelay || 1000;
    this.maxDelay = options.maxDelay || 30000;
    this.jitter = options.jitter !== false;
  }
  
  async retry(fn) {
    let lastError;
    for (let i = 0; i < this.maxRetries; i++) {
      try { return await fn(); } 
      catch (e) {
        lastError = e;
        if (!this.shouldRetry(e)) throw e;
        await this.sleep(this.calculateDelay(i));
      }
    }
    throw lastError;
  }
  
  shouldRetry(e) {
    const codes = ['ETIMEDOUT', 'ECONNRESET', 'ECONNREFUSED'];
    const status = e?.status || e?.response?.status;
    return (e.code && codes.includes(e.code)) || (status && [408,429,500,502,503,504].includes(status));
  }
  
  calculateDelay(attempt) {
    const d = Math.min(this.baseDelay * Math.pow(2, attempt), this.maxDelay);
    return d + (this.jitter ? Math.random() * 1000 : 0);
  }
  
  sleep(ms) { return new Promise(r => setTimeout(r, ms)); }
}

// ==================== 5. 主客户端 (OpenAI兼容) ====================
class ReliableAPIClient {
  constructor(options = {}) {
    this.baseURL = options.baseURL || '';
    this.timeout = options.timeout || 60000;
    this.model = options.model || 'gpt-3.5-turbo';
    
    // 默认路径
    this.defaultPaths = {
      chat: '/v1/chat/completions',
      completions: '/v1/completions',
      embeddings: '/v1/embeddings'
    };
    
    // 默认鉴权
    this.defaultAuth = {
      header: 'Authorization',
      prefix: 'Bearer'
    };
    
    // Endpoint 管理器
    this.endpointManager = new EndpointManager({
      strategy: options.strategy || 'priority',
      healthCheck: options.healthCheck !== false,
      failover: options.failover !== false,
      errorCooldown: options.errorCooldown || 60000,
      authCooldown: options.authCooldown || 3600000
    });
    
    // 添加 Endpoints
    if (options.endpoints && Array.isArray(options.endpoints)) {
      options.endpoints.forEach(e => {
        if (typeof e === 'string') {
          this.endpointManager.addEndpoint(e, options.apiKey);
        } else {
          this.endpointManager.addEndpoint(e.url, e.key, {
            priority: e.priority,
            chatPath: e.chatPath,
            completionsPath: e.completionsPath,
            embeddingsPath: e.embeddingsPath,
            authHeader: e.authHeader,
            authPrefix: e.authPrefix
          });
        }
      });
    }
    
    this.rateLimiter = new SlidingWindowRateLimiter({
      maxQPS: options.maxQPS || 10,
      windowMs: options.windowMs || 1000
    });
    
    this.pool = new ConnectionPool({ poolSize: options.poolSize || 20 });
    this.circuitBreakers = {};
    this.backoff = new ExponentialBackoff({
      maxRetries: options.maxRetries || 3,
      baseDelay: options.retryDelay || 1000
    });
    
    this.headers = { 
      'Content-Type': 'application/json',
      ...options.headers 
    };
  }
  
  /**
   * 添加 Endpoint
   */
  addEndpoint(url, key, options = {}) {
    this.endpointManager.addEndpoint(url, key, options);
    const fullUrl = url.startsWith('http') ? url : `https://${url}`;
    if (!this.circuitBreakers[fullUrl]) {
      this.circuitBreakers[fullUrl] = new CircuitBreaker();
    }
  }
  
  /**
   * 启用被禁用的 endpoint
   */
  enableEndpoint(url) {
    this.endpointManager.enableEndpoint(url);
  }
  
  /**
   * 列出所有 endpoint 状态
   */
  listEndpoints() {
    return this.endpointManager.listEndpoints();
  }
  
  getStats() {
    return this.endpointManager.getStats();
  }
  
  // ==================== OpenAI 兼容接口 ====================
  
  /**
   * chat.completions - 聊天完成
   */
  async chatCompletions(messages, options = {}) {
    const payload = {
      model: options.model || this.model,
      messages,
      temperature: options.temperature ?? 0.7,
      max_tokens: options.max_tokens,
      stream: options.stream || false
    };
    
    const response = await this.post('/chat/completions', payload, { type: 'chat' });
    return JSON.parse(response.data);
  }
  
  /**
   * completions - 文本补全
   */
  async completions(prompt, options = {}) {
    const payload = {
      model: options.model || this.model,
      prompt,
      temperature: options.temperature ?? 0.7,
      max_tokens: options.max_tokens,
      stream: options.stream || false
    };
    
    const response = await this.post('/completions', payload, { type: 'completions' });
    return JSON.parse(response.data);
  }
  
  /**
   * embeddings - 向量嵌入
   */
  async embeddings(input, options = {}) {
    const payload = {
      model: options.model || 'text-embedding-ada-002',
      input
    };
    
    const response = await this.post('/embeddings', payload, { type: 'embeddings' });
    return JSON.parse(response.data);
  }
  
  // ==================== 底层请求 ====================
  
  async request(path, method = 'GET', data = null, options = {}) {
    await this.rateLimiter.acquire();
    const conn = await this.pool.acquire();
    
    try {
      return await this.executeWithFailover(path, method, data, options, conn);
    } finally {
      this.pool.release(conn);
    }
  }
  
  get(path, options = {}) { return this.request(path, 'GET', null, options); }
  post(path, data, options = {}) { return this.request(path, 'POST', data, options); }
  put(path, data, options = {}) { return this.request(path, 'PUT', data, options); }
  delete(path, options = {}) { return this.request(path, 'DELETE', null, options); }
  
  async executeWithFailover(path, method, data, options, conn) {
    const entries = this.endpointManager.endpoints;
    const maxAttempts = entries.length * (this.backoff.maxRetries + 1);
    let attempt = 0;
    let lastError;
    
    while (attempt < maxAttempts) {
      const entry = this.endpointManager.getNextEndpoint();
      if (!entry) throw new Error('No available endpoints');
      
      if (!this.circuitBreakers[entry.url]) {
        this.circuitBreakers[entry.url] = new CircuitBreaker();
      }
      const cb = this.circuitBreakers[entry.url];
      
      // 解析路径
      const resolvedPath = this.resolvePath(path, entry, options.type);
      
      const url = resolvedPath.startsWith('http') ? resolvedPath : entry.url + resolvedPath;
      attempt++;
      
      try {
        return await cb.execute(async () => {
          return await this.backoff.retry(async () => {
            try {
              return await this.doRequest(url, method, data, entry.key, entry.auth, options);
            } catch (err) {
              this.endpointManager.markError(entry.url, this.extractErrorType(err));
              throw err;
            }
          });
        });
      } catch (err) {
        lastError = err;
        if (err.message === 'Circuit breaker is OPEN') continue;
        if (attempt >= maxAttempts) throw err;
        await this.backoff.sleep(1000);
      }
    }
    
    throw lastError;
  }
  
  /**
   * 解析路径 - 根据 endpoint 配置和请求类型
   */
  resolvePath(path, entry, type) {
    // 如果传入完整 URL，直接返回
    if (path.startsWith('http')) return path;
    
    // 从 path 推断类型
    if (!type) {
      if (path.includes('chat')) type = 'chat';
      else if (path.includes('completions') && !path.includes('chat')) type = 'completions';
      else if (path.includes('embeddings')) type = 'embeddings';
    }
    
    // 使用 endpoint 配置的路径，或默认路径
    const paths = entry.paths || this.defaultPaths;
    const basePath = paths[type] || this.defaultPaths[type] || path;
    
    return basePath;
  }
  
  extractErrorType(e) {
    const s = e?.status;
    if (s === 429) return '429';
    if (s === 401) return '401';
    if (s === 403) return '403';
    const m = String(e?.message || e || '').toLowerCase();
    if (m.includes('429') || m.includes('rate limit')) return '429';
    if (m.includes('401') || m.includes('unauthorized')) return '401';
    if (m.includes('403') || m.includes('forbidden')) return '403';
    return 'unknown';
  }
  
  doRequest(url, method, data, apiKey, auth, options) {
    return new Promise((resolve, reject) => {
      const parsed = new URL(url);
      const isHttps = parsed.protocol === 'https:';
      const client = isHttps ? https : http;
      
      const body = data ? (typeof data === 'string' ? data : JSON.stringify(data)) : null;
      
      // 构建鉴权头（prefix 允许为空；默认行为会在 prefix 与 key 之间加一个空格）
      const prefix = auth?.prefix;
      const authValue = (prefix === '' || prefix == null)
        ? String(apiKey)
        : `${String(prefix).trimEnd()} ${apiKey}`;
      
      const req = client.request({
        hostname: parsed.hostname,
        port: parsed.port || (isHttps ? 443 : 80),
        path: parsed.pathname + parsed.search,
        method,
        headers: {
          'User-Agent': 'ReliableAPIClient/3.3',
          [auth.header]: authValue,
          ...this.headers,
          ...options.headers
        },
        timeout: this.timeout
      }, (res) => {
        let data = '';
        res.on('data', c => data += c);
        res.on('end', () => {
          if (res.statusCode === 429) { const e = new Error('429'); e.status = 429; reject(e); return; }
          if (res.statusCode === 401) { const e = new Error('401'); e.status = 401; reject(e); return; }
          if (res.statusCode === 403) { const e = new Error('403'); e.status = 403; reject(e); return; }
          resolve({ status: res.statusCode, headers: res.headers, data });
        });
      });
      
      req.on('error', reject);
      req.on('timeout', () => { req.destroy(); reject(new Error('ETIMEDOUT')); });
      if (body) req.write(body);
      req.end();
    });
  }
}

// 导出
module.exports = ReliableAPIClient;
module.exports.EndpointManager = EndpointManager;
module.exports.SlidingWindowRateLimiter = SlidingWindowRateLimiter;
module.exports.ConnectionPool = ConnectionPool;
module.exports.CircuitBreaker = CircuitBreaker;
module.exports.ExponentialBackoff = ExponentialBackoff;
