"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.TorkClient = void 0;
const axios_1 = __importDefault(require("axios"));
class TorkClient {
    constructor(apiKey, baseUrl = 'https://tork.network') {
        this.http = axios_1.default.create({
            baseURL: baseUrl,
            timeout: 5000,
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${apiKey}`,
                'X-Tork-SDK-Language': 'typescript',
                'X-Tork-Adapter': 'openclaw-guardian',
            },
        });
    }
    async govern(content, options) {
        try {
            const { data } = await this.http.post('/api/v1/govern', {
                content,
                options,
            });
            return data;
        }
        catch (error) {
            // Fail-open: if Tork is unreachable, allow the request through
            console.warn('[TorkGuardian] Governance API unreachable, failing open:', error instanceof Error ? error.message : error);
            return {
                action: 'allow',
                output: content,
            };
        }
    }
    async redact(content) {
        return this.govern(content, { mode: 'redact' });
    }
}
exports.TorkClient = TorkClient;
//# sourceMappingURL=client.js.map