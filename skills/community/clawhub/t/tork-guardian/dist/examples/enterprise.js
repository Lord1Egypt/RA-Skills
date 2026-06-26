"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ENTERPRISE_CONFIG = void 0;
/** Enterprise lockdown — strict network, explicit domain allowlist, tight rate limits. */
exports.ENTERPRISE_CONFIG = {
    apiKey: process.env.TORK_API_KEY || 'REPLACE_ME',
    policy: 'strict',
    redactPII: true,
    networkPolicy: 'strict',
    allowedDomains: [
        'api.openai.com',
        'api.anthropic.com',
        'tork.network',
        'tork.network',
        'api.tork.network',
    ],
    maxConnectionsPerMinute: 20,
};
//# sourceMappingURL=enterprise.js.map