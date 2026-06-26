import { edgecloudInferenceClient } from '../clients/edgecloudInference.js';
import { isStructuredError, thetaError } from '../errors.js';
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
function clampInt(value, fallback, min, max) {
    if (!Number.isFinite(value))
        return fallback;
    return Math.min(Math.max(Math.trunc(value), min), max);
}
function annotateEndpointReadinessError(error) {
    if (isStructuredError(error) && (error.status === 502 || error.status === 503)) {
        throw thetaError({
            ...error,
            code: 'THETA_DEDICATED_ENDPOINT_UPSTREAM_UNREADY',
            retriable: true,
            message: `Dedicated inference endpoint is not ready upstream (HTTP ${error.status}). ` +
                'Auth layer may be active while upstream service remains unavailable. ' +
                'Likely platform ingress/backend readiness mismatch; retry or verify endpoint health from Theta dashboard logs.'
        });
    }
    throw error;
}
export const inference = {
    models: async (cfg, endpoint) => {
        try {
            return await edgecloudInferenceClient.listModels(cfg, endpoint);
        }
        catch (error) {
            annotateEndpointReadinessError(error);
        }
    },
    chat: async (cfg, body, endpoint) => {
        if (cfg.dryRun)
            return { dryRun: true, endpoint, body };
        try {
            return await edgecloudInferenceClient.chat(cfg, body, endpoint);
        }
        catch (error) {
            annotateEndpointReadinessError(error);
        }
    },
    ready: async (cfg, opts = {}) => {
        const probe = opts.probe ?? 'openai';
        const timeoutMs = clampInt(opts.timeoutMs, 120000, 1000, 1800000);
        const intervalMs = clampInt(opts.intervalMs, 5000, 500, 60000);
        if (cfg.dryRun)
            return { dryRun: true, probe, timeoutMs, intervalMs };
        const startedAt = Date.now();
        const attempts = [];
        while (Date.now() - startedAt < timeoutMs) {
            const attemptStartedAt = Date.now();
            try {
                const response = probe === 'gradio'
                    ? await edgecloudInferenceClient.gradioConfig(cfg)
                    : await edgecloudInferenceClient.listModels(cfg);
                attempts.push({ ok: true, elapsedMs: Date.now() - attemptStartedAt });
                return {
                    ready: true,
                    probe,
                    elapsedMs: Date.now() - startedAt,
                    attempts,
                    response
                };
            }
            catch (error) {
                attempts.push({
                    ok: false,
                    elapsedMs: Date.now() - attemptStartedAt,
                    status: isStructuredError(error) ? error.status : undefined,
                    code: isStructuredError(error) ? error.code : error?.name,
                    message: error?.message ?? String(error)
                });
            }
            const remainingMs = timeoutMs - (Date.now() - startedAt);
            if (remainingMs <= 0)
                break;
            await sleep(Math.min(intervalMs, remainingMs));
        }
        return {
            ready: false,
            probe,
            elapsedMs: Date.now() - startedAt,
            attempts
        };
    }
};
