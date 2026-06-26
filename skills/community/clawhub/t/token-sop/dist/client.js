"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.ClawMindClient = void 0;
class ClawMindClient {
    config;
    constructor(config) {
        this.config = { timeout: 30000, ...config };
    }
    async contribute(data) {
        const response = await fetch(`${this.config.apiUrl}/v1/contribute`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ ...data, nodeId: this.config.nodeId }),
            signal: AbortSignal.timeout(this.config.timeout),
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(`Contribution failed: ${error.error}`);
        }
        return response.json();
    }
    async match(data) {
        const response = await fetch(`${this.config.apiUrl}/v1/match`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
            signal: AbortSignal.timeout(this.config.timeout),
        });
        if (response.status === 404)
            return null;
        if (!response.ok) {
            const error = await response.json();
            throw new Error(`Match failed: ${error.error}`);
        }
        return response.json();
    }
    async reportSuccess(macroId) {
        const response = await fetch(`${this.config.apiUrl}/v1/feedback`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ macroId, nodeId: this.config.nodeId, success: true }),
            signal: AbortSignal.timeout(this.config.timeout),
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(`Feedback failed: ${error.error}`);
        }
        return response.json();
    }
    async reportFailure(macroId, failedStepIndex, errorType, domSnapshot) {
        const response = await fetch(`${this.config.apiUrl}/v1/feedback`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                macroId,
                nodeId: this.config.nodeId,
                success: false,
                failedStepIndex,
                errorType,
                domSnapshot,
            }),
            signal: AbortSignal.timeout(this.config.timeout),
        });
        if (!response.ok) {
            const error = await response.json();
            throw new Error(`Feedback failed: ${error.error}`);
        }
        return response.json();
    }
}
exports.ClawMindClient = ClawMindClient;
//# sourceMappingURL=client.js.map