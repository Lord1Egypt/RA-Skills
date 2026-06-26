"use strict";
// StockToday 透明限流器
// 设计原则: 用户(LLM)无感, 后端友好, 错误静默
//
// 三层防护 (从内到外):
//   1. Per-token 限流 (token bucket, 60/min 默认)  — 防止单用户打爆
//   2. 并发限流 (semaphore, 5 并发默认)            — 防止瞬时并发压垮后端
//   3. 错误静默 + 自动重试 (3 次指数退避)          — 429/5xx 自动恢复, 失败返 []
Object.defineProperty(exports, "__esModule", { value: true });
exports.RateLimiter = exports.DEFAULT_CONFIG = void 0;
exports.DEFAULT_CONFIG = {
    perMin: parseInt(process.env.STOCKTODAY_RATE_PER_MIN || '100', 10),
    maxConcurrent: parseInt(process.env.STOCKTODAY_MAX_CONCURRENT || '10', 10),
    maxRetries: parseInt(process.env.STOCKTODAY_MAX_RETRIES || '3', 10),
    backoffBaseMs: parseInt(process.env.STOCKTODAY_BACKOFF_MS || '1000', 10),
    queueTimeoutMs: parseInt(process.env.STOCKTODAY_QUEUE_TIMEOUT_MS || '60000', 10),
};
class RateLimiter {
    constructor(config = exports.DEFAULT_CONFIG) {
        this.config = config;
        this.buckets = new Map();
        this.activeCount = 0;
        this.waitQueue = [];
        // 本分钟计数器 (给用户看)
        this.currentMinute = Math.floor(Date.now() / 60000);
        this.currentMinuteCount = 0;
        this.lastQuotaWarn = 0; // 上次发"接近限流"警告的分钟
        // Aggregate metrics
        this.stats = {
            totalCalls: 0,
            totalThrottled: 0, // had to wait
            totalRetries: 0,
            totalSilentFails: 0, // returned empty after exhausting retries
            totalRealtimeMs: 0, // total wall time
            peakConcurrency: 0,
        };
    }
    /** Get or create a bucket for this token */
    getBucket(token) {
        let b = this.buckets.get(token);
        if (!b) {
            b = { tokens: this.config.perMin, lastRefill: Date.now(), totalWaited: 0, totalAcquired: 0, totalThrottled: 0 };
            this.buckets.set(token, b);
        }
        return b;
    }
    /** 跨分钟自动 reset */
    bumpMinuteCount() {
        const now = Math.floor(Date.now() / 60000);
        if (now !== this.currentMinute) {
            this.currentMinute = now;
            this.currentMinuteCount = 0;
        }
        this.currentMinuteCount++;
    }
    /** 给用户看: 本分钟已用 / 100 */
    getCurrentMinuteUsed() {
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
    shouldWarnQuota() {
        const usage = this.getCurrentMinuteUsed();
        if (usage.percent >= 80 && this.lastQuotaWarn !== this.currentMinute) {
            this.lastQuotaWarn = this.currentMinute;
            return true;
        }
        return false;
    }
    /** Wait until: (a) a concurrency slot is free, (b) a token is available for this token-bucket */
    async acquire(token) {
        const start = Date.now();
        // 1) Concurrency gate
        if (this.activeCount >= this.config.maxConcurrent) {
            this.stats.totalThrottled++;
            await new Promise(resolve => {
                const timer = setTimeout(() => {
                    // queue timeout — pop ourselves
                    const idx = this.waitQueue.indexOf(release);
                    if (idx >= 0)
                        this.waitQueue.splice(idx, 1);
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
        if (this.activeCount > this.stats.peakConcurrency)
            this.stats.peakConcurrency = this.activeCount;
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
        }
        else {
            bucket.tokens -= 1;
        }
        bucket.totalAcquired++;
        bucket.totalWaited += Date.now() - start;
    }
    release() {
        this.activeCount--;
        const next = this.waitQueue.shift();
        if (next)
            next();
    }
    /**
     * Run `fn` under rate limit + concurrency gate.
     * Auto-retries on 429/5xx with exponential backoff.
     * Returns { ok: true, data } on success or { ok: false } on silent fail.
     */
    async execute(token, fn) {
        this.stats.totalCalls++;
        this.bumpMinuteCount();
        const start = Date.now();
        let lastErr = '';
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
                }
                finally {
                    if (!releasedThisAttempt)
                        this.release();
                }
            }
            catch (e) {
                if (!releasedThisAttempt)
                    this.release();
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
    getStats() {
        return {
            ...this.stats,
            bucketCount: this.buckets.size,
            activeCount: this.activeCount,
            queueLength: this.waitQueue.length,
        };
    }
    /** Per-token metrics */
    getTokenStats() {
        const out = {};
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
exports.RateLimiter = RateLimiter;
