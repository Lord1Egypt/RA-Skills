"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.loadConfig = void 0;
/**
 * config.ts — loads environment variables into a typed BotConfig.
 * env vars:
 *   SOLANA_RPC_URL         — solana RPC endpoint (required, fallback: RPC_URL)
 *   VAULT_CREATOR          — vault creator pubkey (required)
 *   SOLANA_PRIVATE_KEY     — disposable controller keypair, base58 or JSON byte array (optional)
 *   SCAN_INTERVAL_MS       — ms between scan cycles (default 30000, min 5000)
 *   SCAN_LIMIT             — max tokens to scan per cycle (default 50, 0 = unlimited)
 *   MIN_AGENT_BALANCE_SOL  — pause liquidations below this balance (default 0.01)
 *   LOG_LEVEL              — debug | info | warn | error (default info)
 *   LOG_FORMAT             — text | json (default text)
 */
const torchsdk_1 = require("torchsdk");
const constants_1 = require("./constants");
const loadConfig = () => {
    const rpcUrl = process.env.SOLANA_RPC_URL ?? process.env.RPC_URL;
    if (!rpcUrl) {
        throw new Error('SOLANA_RPC_URL env var is required (fallback: RPC_URL)');
    }
    const vaultCreator = process.env.VAULT_CREATOR;
    if (!vaultCreator) {
        throw new Error('VAULT_CREATOR env var is required (vault creator pubkey)');
    }
    const privateKey = process.env.SOLANA_PRIVATE_KEY ?? null;
    const scanIntervalMs = parseInt(process.env.SCAN_INTERVAL_MS ?? '30000', 10);
    if (isNaN(scanIntervalMs) || scanIntervalMs < 5000) {
        throw new Error('SCAN_INTERVAL_MS must be a number >= 5000');
    }
    const scanLimit = parseInt(process.env.SCAN_LIMIT ?? '50', 10);
    if (isNaN(scanLimit) || scanLimit < 0) {
        throw new Error('SCAN_LIMIT must be a non-negative number (0 = unlimited)');
    }
    const minAgentBalanceSol = parseFloat(process.env.MIN_AGENT_BALANCE_SOL ?? '0.01');
    if (isNaN(minAgentBalanceSol) || minAgentBalanceSol < 0) {
        throw new Error('MIN_AGENT_BALANCE_SOL must be a non-negative number');
    }
    const minAgentBalanceLamports = Math.floor(minAgentBalanceSol * torchsdk_1.LAMPORTS_PER_SOL);
    const logLevel = (process.env.LOG_LEVEL ?? 'info');
    if (!constants_1.LOG_LEVELS.includes(logLevel)) {
        throw new Error(`LOG_LEVEL must be one of: ${constants_1.LOG_LEVELS.join(', ')}`);
    }
    const logFormat = (process.env.LOG_FORMAT ?? 'text');
    if (!constants_1.LOG_FORMATS.includes(logFormat)) {
        throw new Error(`LOG_FORMAT must be one of: ${constants_1.LOG_FORMATS.join(', ')}`);
    }
    return {
        rpcUrl,
        vaultCreator,
        privateKey,
        scanIntervalMs,
        scanLimit,
        minAgentBalanceLamports,
        logLevel,
        logFormat,
    };
};
exports.loadConfig = loadConfig;
//# sourceMappingURL=config.js.map