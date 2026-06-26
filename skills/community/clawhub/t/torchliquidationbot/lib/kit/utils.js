"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.createLogger = exports.withRetry = exports.withTimeout = exports.bpsToPercent = exports.sol = void 0;
const torchsdk_1 = require("torchsdk");
const constants_1 = require("./constants");
const sol = (lamports) => (lamports / torchsdk_1.LAMPORTS_PER_SOL).toFixed(4);
exports.sol = sol;
const bpsToPercent = (bps) => (bps / 100).toFixed(2) + '%';
exports.bpsToPercent = bpsToPercent;
const withTimeout = async (promise, label) => {
    return Promise.race([
        promise,
        new Promise((_, reject) => setTimeout(() => reject(new Error(`${label} timed out after ${constants_1.RPC_TIMEOUT_MS}ms`)), constants_1.RPC_TIMEOUT_MS)),
    ]);
};
exports.withTimeout = withTimeout;
// retry an async operation with exponential backoff.
// retries transient failures up to `attempts` times with 1s, 2s, 4s delays.
// re-throws the last error if all attempts fail. Set `onRetry` to track retry counts in metrics.
const withRetry = async (fn, label, attempts = constants_1.DEFAULT_RETRY_ATTEMPTS, onRetry) => {
    let lastErr = new Error(`${label} failed with no attempts`);
    for (let i = 0; i < attempts; i++) {
        try {
            return await fn();
        }
        catch (err) {
            lastErr = err;
            if (i < attempts - 1) {
                onRetry?.();
                await new Promise((r) => setTimeout(r, constants_1.RETRY_BASE_DELAY_MS * Math.pow(2, i)));
            }
        }
    }
    throw lastErr;
};
exports.withRetry = withRetry;
const createLogger = (minLevel, format = 'text') => {
    const minIdx = constants_1.LOG_LEVELS.indexOf(minLevel);
    return (level, msg, extra) => {
        if (constants_1.LOG_LEVELS.indexOf(level) < minIdx)
            return;
        const ts = new Date().toISOString();
        if (format === 'json') {
            console.log(JSON.stringify({ ts, level, msg, ...(extra ?? {}) }));
            return;
        }
        const tsShort = ts.substr(11, 12);
        const tag = level.toUpperCase().padEnd(5);
        const extraStr = extra ? ' ' + JSON.stringify(extra) : '';
        console.log(`[${tsShort}] ${tag} ${msg}${extraStr}`);
    };
};
exports.createLogger = createLogger;
//# sourceMappingURL=utils.js.map