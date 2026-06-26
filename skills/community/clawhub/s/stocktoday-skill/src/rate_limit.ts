// StockToday 透明限流器
// 设计原则: 用户(LLM)无感, 后端友好, 错误静默
//
// 三层防护 (从内到外):
//   1. Per-token 限流 (token bucket, 60/min 默认)  — 防止单用户打爆
//   2. 并发限流 (semaphore, 5 并发默认)            — 防止瞬时并发压垮后端
//   3. 错误静默 + 自动重试 (3 次指数退避)          — 429/5xx 自动恢复, 失败返 []

export interface RateLimitConfig {
  perMin: number;          // 每分钟每 token 最多调用次数
  maxConcurrent: number;   // 全局最大并发
  maxRetries: number;      // 单次请求最大重试次数
  backoffBaseMs: number;   // 指数退避基数 (1s, 2s, 4s...)
  queueTimeoutMs: number;  // 排队等待超时 (超时后静默返空)
}

export const DEFAULT_CONFIG: RateLimitConfig = {
  perMin: parseInt(process.env.STOCKTODAY_RATE_PER_MIN || '100', 10),
  maxConcurrent: parseInt(process.env.STOCKTODAY_MAX_CONCURRENT || '10', 10),
  maxRetries: parseInt(process.env.STOCKTODAY_MAX_RETRIES || '3', 10),
  backoffBaseMs: parseInt(process.env.STOCKTODAY_BACKOFF_MS || '1000', 10),
  queueTimeoutMs: parseInt(process.env.STOCKTODAY_QUEUE_TIMEOUT_MS || '60000', 10),
};

interface TokenBucket {
  tokens: number;
  lastRefill: number;  // ms epoch
  totalWaited: number; // total ms waited in queue (for metrics)
  totalAcquired: number;
  totalThrottled: number; // count of times we had to wait
}

export class RateLimiter {
  private buckets: Map<string, TokenBucket> = new Map();
  private activeCount: number = 0;
  private waitQueue: Array<() => void> = [];

  // 本分钟计数器 (给用户看)
  private currentMinute: number = Math.floor(Date.now() / 60000);
  private currentMinuteCount: number = 0;
  private lastQuotaWarn: number = 0;  // 上次发"接近限流"警告的分钟

  // Aggregate metrics
  public stats = {
    totalCalls: 0,
    totalThrottled: 0,    // had to wait
    totalRetries: 0,
    totalSilentFails: 0,  // returned empty after exhausting retries
    totalRealtimeMs: 0,   // total wall time
    peakConcurrency: 0,
  };

  constructor(public config: RateLimitConfig = DEFAULT_CONFIG) {}

  /** Get or create a bucket for this token */
  private getBucket(token: string): TokenBucket {
    let b = this.buckets.get(token);
    if (!b) {
      b = { tokens: this.config.perMin, lastRefill: Date.now(), totalWaited: 0, totalAcquired: 0, totalThrottled: 0 };
      this.buckets.set(token, b);
    }
    return b;
  }

  /** 跨分钟自动 reset */
  private bumpMinuteCount(): void {
    const now = Math.floor(Date.now() / 60000);
    if (now !== this.currentMinute) {
      this.currentMinute = now;
      this.currentMinuteCount = 0;
    }
    this.currentMinuteCount++;
  }

  /** 给用户看: 本分钟已用 / 100 */
  getCurrentMinuteUsed(): { used: number; limit: number; remaining: number; percent: number } {
    const now = Math.floor(Date.now() / 60000);
    if (now !== this.currentMinute) {
      this.currentMinute = now;
      this.currentMinuteCount = 0;
    }
    const percent = Math.round((this.currentMinuteCount / this.config.perMin) * 100);
    return {
      used: this.currentMinuteCount,
      limit: this.config.perMin,
      remaining: Math.max(0, this.config.perMin - this.currentMinuteCount),
      percent
    };
  }

  /** 80% 警告 (每分钟最多 1 次, 免得刷屏) */
  shouldWarnQuota(): boolean {
    const usage = this.getCurrentMinuteUsed();
    if (usage.percent >= 80 && this.lastQuotaWarn !== this.currentMinute) {
      this.lastQuotaWarn = this.currentMinute;
      return true;
    }
    return false;
  }

  /** Wait until: (a) a concurrency slot is free, (b) a token is available for this token-bucket */
  private async acquire(token: string): Promise<void> {
    const start = Date.now();

    // 1) Concurrency gate
    if (this.activeCount >= this.config.maxConcurrent) {
      this.stats.totalThrottled++;
      await new Promise<void>(resolve => {
        const timer = setTimeout(() => {
          // queue timeout — pop ourselves
          const idx = this.waitQueue.indexOf(release);
          if (idx >= 0) this.waitQueue.splice(idx, 1);
          resolve(); // proceed anyway, will be throttled by token bucket
        }, this.config.queueTimeoutMs);
        const release = () => {
          clearTimeout(timer);
          resolve();
        };
        this.waitQueue.push(release);
      });
    }
    this.activeCount++;
    if (this.activeCount > this.stats.peakConcurrency) this.stats.peakConcurrency = this.activeCount;

    // 2) Token-bucket gate (refill based on elapsed time)
    const bucket = this.getBucket(token);
    const now = Date.now();
    const elapsedSec = (now - bucket.lastRefill) / 1000;
    const refillRate = this.config.perMin / 60; // tokens per second
    bucket.tokens = Math.min(this.config.perMin, bucket.tokens + elapsedSec * refillRate);
    bucket.lastRefill = now;

    if (bucket.tokens < 1) {
      const waitMs = Math.ceil((1 - bucket.tokens) / refillRate * 1000);
      this.stats.totalThrottled++;
      bucket.totalThrottled++;
      await new Promise(r => setTimeout(r, waitMs));
      bucket.tokens = 0; // spent the one we waited for
    } else {
      bucket.tokens -= 1;
    }
    bucket.totalAcquired++;
    bucket.totalWaited += Date.now() - start;
  }

  private release(): void {
    this.activeCount--;
    const next = this.waitQueue.shift();
    if (next) next();
  }

  /**
   * Run `fn` under rate limit + concurrency gate.
   * Auto-retries on 429/5xx with exponential backoff.
   * Returns { ok: true, data } on success or { ok: false } on silent fail.
   */
  public async execute<T>(
    token: string,
    fn: () => Promise<{ status: number; data: T; raw: string }>
  ): Promise<{ ok: boolean; data?: T; silent?: boolean; error?: string }> {
    this.stats.totalCalls++;
    this.bumpMinuteCount();
    const start = Date.now();

    let lastErr: string = '';
    for (let attempt = 0; attempt < this.config.maxRetries; attempt++) {
      let releasedThisAttempt = false;
      try {
        await this.acquire(token);
        releasedThisAttempt = false;
        try {
          const res = await fn();
          // Success
          if (res.status === 200) {
            this.stats.totalRealtimeMs += Date.now() - start;
            this.release();
            releasedThisAttempt = true;
            return { ok: true, data: res.data };
          }
          // Retryable: 429 (rate limit) or 5xx (server error) or 0 (network)
          if (res.status === 429 || res.status === 0 || (res.status >= 500 && res.status < 600)) {
            this.stats.totalRetries++;
            lastErr = `HTTP ${res.status}`;
            this.release();
            releasedThisAttempt = true;
            const backoff = this.config.backoffBaseMs * Math.pow(2, attempt);
            await new Promise(r => setTimeout(r, backoff));
            continue;
          }
          // Non-retryable (400/404/etc) — return as-is to LLM
          this.stats.totalRealtimeMs += Date.now() - start;
          this.release();
          releasedThisAttempt = true;
          return { ok: true, data: res.data };
        } finally {
          if (!releasedThisAttempt) this.release();
        }
      } catch (e: any) {
        if (!releasedThisAttempt) this.release();
        lastErr = e?.message || String(e);
        this.stats.totalRetries++;
        // Unexpected errors are retryable
        const backoff = this.config.backoffBaseMs * Math.pow(2, attempt);
        await new Promise(r => setTimeout(r, backoff));
      }
    }

    // Exhausted retries — silent fail (return ok:false, no error to user)
    this.stats.totalSilentFails++;
    this.stats.totalRealtimeMs += Date.now() - start;
    console.error(`[rate_limit] silent fail after ${this.config.maxRetries} retries: ${lastErr}`);
    return { ok: false, silent: true };
  }

  /** Get snapshot of metrics for diagnostics */
  public getStats() {
    return {
      ...this.stats,
      bucketCount: this.buckets.size,
      activeCount: this.activeCount,
      queueLength: this.waitQueue.length,
    };
  }

  /** Per-token metrics */
  public getTokenStats() {
    const out: Record<string, any> = {};
    for (const [t, b] of this.buckets) {
      out[t.slice(0, 8) + '…'] = {
        tokens: b.tokens.toFixed(2),
        acquired: b.totalAcquired,
        throttled: b.totalThrottled,
        avgWaitMs: b.totalAcquired > 0 ? Math.round(b.totalWaited / b.totalAcquired) : 0,
      };
    }
    return out;
  }
}
