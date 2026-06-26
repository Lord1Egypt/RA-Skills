"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.callWorldLoopsBrief = callWorldLoopsBrief;
const DEFAULT_API_BASE_URL = 'https://api.worldloops.ai';
function getApiBaseUrl() {
    const baseUrl = process.env.WORLDLOOPS_API_BASE_URL ?? DEFAULT_API_BASE_URL;
    return baseUrl.replace(/\/$/, '');
}
async function callWorldLoopsBrief(input) {
    const apiKey = process.env.WORLDLOOPS_API_KEY;
    const baseUrl = getApiBaseUrl();
    const response = await fetch(`${baseUrl}/api/v1/openclaw/brief`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            ...(apiKey ? { Authorization: `Bearer ${apiKey}` } : {}),
        },
        body: JSON.stringify({
            signals: input.signals,
            mode: input.mode ?? (apiKey ? 'connected' : 'demo'),
        }),
    });
    const json = (await response.json());
    if (!response.ok) {
        return {
            ok: false,
            error: {
                code: `HTTP_${response.status}`,
                message: json.error?.message ?? response.statusText,
            },
            safety: {
                externalWrite: false,
            },
        };
    }
    return {
        ...json,
        safety: {
            ...(json.safety ?? {}),
            externalWrite: false,
        },
    };
}
//# sourceMappingURL=brief.js.map