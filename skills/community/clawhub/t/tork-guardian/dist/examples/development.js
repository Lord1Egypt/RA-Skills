"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.DEVELOPMENT_CONFIG = void 0;
/** Dev-friendly config — permissive policies, full logging. */
exports.DEVELOPMENT_CONFIG = {
    apiKey: process.env.TORK_API_KEY || 'REPLACE_ME',
    policy: 'minimal',
    redactPII: true,
    networkPolicy: 'default',
};
//# sourceMappingURL=development.js.map