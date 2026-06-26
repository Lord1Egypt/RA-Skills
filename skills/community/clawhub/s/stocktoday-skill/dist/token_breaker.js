"use strict";
// Token Circuit Breaker
// 设计目标: token 错时立即熔断, 防止触发 gateway IP ban
//
// 状态机:
//   CLOSED (正常) → 1 次 auth_error → 警告 + 暂停 30s
//                  → 2 次 auth_error → 熔断 OPEN (5min)
//   OPEN (熔断)    → 5min 后 → HALF_OPEN
//   HALF_OPEN       → 成功 → CLOSED / 失败 → OPEN (再 5min)
Object.defineProperty(exports, "__esModule", { value: true });
exports.tokenBreaker = exports.TokenCircuitBreaker = void 0;
const FAIL_THRESHOLD_WARN = 1; // 第 1 次错 → 警告
const FAIL_THRESHOLD_OPEN = 2; // 第 2 次错 → 熔断
const OPEN_DURATION_MS = 5 * 60 * 1000; // 熔断 5 分钟
const WARN_DURATION_MS = 30 * 1000; // 警告 30 秒
class TokenCircuitBreaker {
    constructor() {
        this.state = 'CLOSED';
        this.failCount = 0;
        this.lastFailTime = 0;
        this.firstFailTime = 0; // 第一次失败时间 (用于 30s 警告)
        this.openTime = 0;
    }
    /**
     * gateway 返 auth_error (token 错/无效) 时调用
     * @returns 熔断状态 + 给用户的友好提示
     */
    recordAuthError() {
        this.failCount++;
        const now = Date.now();
        this.lastFailTime = now;
        if (this.failCount === FAIL_THRESHOLD_WARN) {
            this.firstFailTime = now;
            console.error(`[token_breaker] ⚠️ token 错, 30s 内暂停请求, 请检查 STOCKTODAY_TOKEN`);
            return {
                open: false,
                state: 'CLOSED',
                message: '⚠️ token 似乎无效, 暂停 30s 防止触发 IP ban. 请检查 .mcp.json 里的 STOCKTODAY_TOKEN (从 https://stocktoday.cn 申请)',
                failCount: this.failCount,
            };
        }
        if (this.failCount >= FAIL_THRESHOLD_OPEN) {
            this.state = 'OPEN';
            this.openTime = now;
            console.error(`[token_breaker] 🚨 token 错 ${this.failCount} 次, 熔断 5min 防止 IP ban`);
            return {
                open: true,
                state: 'OPEN',
                message: `🚨 token 错误熔断中 (失败 ${this.failCount} 次), 剩 ${Math.ceil(OPEN_DURATION_MS / 1000)}s 自动恢复. 请立即检查 STOCKTODAY_TOKEN`,
                remainingSeconds: Math.ceil(OPEN_DURATION_MS / 1000),
                failCount: this.failCount,
            };
        }
        return { open: false, state: this.state, failCount: this.failCount };
    }
    /**
     * 调用前检查, 决定是否放行
     */
    check() {
        if (this.state === 'CLOSED') {
            // 检查 30s 警告是否过期
            if (this.failCount >= FAIL_THRESHOLD_WARN && Date.now() - this.firstFailTime < WARN_DURATION_MS) {
                const remain = Math.ceil((WARN_DURATION_MS - (Date.now() - this.firstFailTime)) / 1000);
                return {
                    open: false,
                    state: 'CLOSED',
                    message: `⚠️ token 错过, 还剩 ${remain}s 暂停, 请检查 STOCKTODAY_TOKEN`,
                    remainingSeconds: remain,
                    failCount: this.failCount,
                };
            }
            return { open: false, state: 'CLOSED', failCount: this.failCount };
        }
        if (this.state === 'OPEN') {
            const elapsed = Date.now() - this.openTime;
            if (elapsed >= OPEN_DURATION_MS) {
                this.state = 'HALF_OPEN';
                console.error('[token_breaker] ⚠️→HALF_OPEN, 让用户重试');
                return { open: false, state: 'HALF_OPEN', failCount: this.failCount };
            }
            const remain = Math.ceil((OPEN_DURATION_MS - elapsed) / 1000);
            return {
                open: true,
                state: 'OPEN',
                message: `🚨 token 错误熔断中, 剩 ${remain}s 自动恢复. 请立即检查 STOCKTODAY_TOKEN`,
                remainingSeconds: remain,
                failCount: this.failCount,
            };
        }
        // HALF_OPEN: 放行, 让用户试
        return { open: false, state: 'HALF_OPEN', failCount: this.failCount };
    }
    /**
     * 调用成功时调用, 重置 failCount
     */
    recordSuccess() {
        if (this.state === 'HALF_OPEN') {
            console.error('[token_breaker] ✓ HALF_OPEN→CLOSED, token 验证通过');
            this.state = 'CLOSED';
        }
        this.failCount = 0;
    }
    getState() {
        return this.state;
    }
}
exports.TokenCircuitBreaker = TokenCircuitBreaker;
exports.tokenBreaker = new TokenCircuitBreaker();
