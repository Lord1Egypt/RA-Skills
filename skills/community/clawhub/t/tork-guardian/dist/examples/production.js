"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.PRODUCTION_CONFIG = void 0;
/** Production config — standard policies, blocked domains, all detection on. */
exports.PRODUCTION_CONFIG = {
    apiKey: process.env.TORK_API_KEY || 'REPLACE_ME',
    policy: 'standard',
    redactPII: true,
    networkPolicy: 'default',
    blockedDomains: [
        'pastebin.com',
        'requestbin.com',
        'ngrok.io',
        'burpcollaborator.net',
        'interact.sh',
        'oastify.com',
        'webhook.site',
    ],
};
//# sourceMappingURL=production.js.map