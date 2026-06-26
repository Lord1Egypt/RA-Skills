"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.GovernanceDeniedError = void 0;
exports.governLLMRequest = governLLMRequest;
async function governLLMRequest(client, request, config) {
    if (!config.redactPII) {
        return { request, governed: false, receipts: [], pii_found: false };
    }
    const governedMessages = [...request.messages];
    const receipts = [];
    let piiFound = false;
    for (let i = 0; i < governedMessages.length; i++) {
        const msg = governedMessages[i];
        if (!msg.content || typeof msg.content !== 'string')
            continue;
        const mode = config.policy === 'strict' ? 'deny' : 'redact';
        const result = await client.govern(msg.content, { mode });
        if (result.receipt?.receipt_id) {
            receipts.push(result.receipt.receipt_id);
        }
        if (result.pii_detected && result.pii_detected.length > 0) {
            piiFound = true;
        }
        if (result.action === 'deny') {
            throw new GovernanceDeniedError(`PII detected in message ${i} (${msg.role}). Policy '${config.policy}' denies this request.`, result);
        }
        if (result.action === 'redact') {
            governedMessages[i] = { ...msg, content: result.output };
        }
    }
    return {
        request: { ...request, messages: governedMessages },
        governed: true,
        receipts,
        pii_found: piiFound,
    };
}
class GovernanceDeniedError extends Error {
    constructor(message, response) {
        super(message);
        this.name = 'GovernanceDeniedError';
        this.governResponse = response;
    }
}
exports.GovernanceDeniedError = GovernanceDeniedError;
//# sourceMappingURL=llm.js.map