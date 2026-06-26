import { fromHttpError, fromTransportError, isRetriableHttpError, isStructuredError } from '../errors.js';
import { getJson, postJson } from './http.js';
const DEFAULT_BASE = 'https://ondemand.thetaedgecloud.com';
const RETRIABLE_STATUS = new Set([408, 425, 429, 500, 502, 503, 504]);
function baseUrl(cfg) {
    const raw = cfg.onDemandApiBaseUrl?.trim() || DEFAULT_BASE;
    return raw.replace(/\/+$/, '');
}
function h(cfg) {
    if (!cfg.onDemandApiToken)
        throw new Error('THETA_ONDEMAND_API_TOKEN missing');
    return {
        Authorization: `Bearer ${cfg.onDemandApiToken}`,
        'content-type': 'application/json'
    };
}
function optionalHeaders(cfg) {
    return cfg.onDemandApiToken
        ? { Authorization: `Bearer ${cfg.onDemandApiToken}`, 'content-type': 'application/json' }
        : { 'content-type': 'application/json' };
}
function net(cfg) {
    return {
        headers: h(cfg),
        service: 'theta-ondemand-api',
        timeoutMs: cfg.httpTimeoutMs,
        maxRetries: cfg.httpMaxRetries,
        retryBackoffMs: cfg.httpRetryBackoffMs
    };
}
function optionalNet(cfg) {
    return {
        headers: optionalHeaders(cfg),
        service: 'theta-ondemand-api',
        timeoutMs: cfg.httpTimeoutMs,
        maxRetries: cfg.httpMaxRetries,
        retryBackoffMs: cfg.httpRetryBackoffMs
    };
}
function encodePathSegment(value, label) {
    if (typeof value !== 'string' || !value.trim()) {
        throw new Error(`${label} must be a non-empty string`);
    }
    return encodeURIComponent(value.trim());
}
function inferPath(service, opts = {}) {
    const params = new URLSearchParams();
    if (opts.wait !== undefined)
        params.set('wait', String(opts.wait));
    if (opts.prediction)
        params.set('prediction', opts.prediction);
    const query = params.toString();
    return `/infer_request/${encodePathSegment(service, 'service')}${query ? `?${query}` : ''}`;
}
function chatCompletionsPath() {
    return '/infer_request/chat/completions';
}
function roundUpMs(value, bucketMs) {
    return Math.ceil(value / bucketMs) * bucketMs;
}
function readPositiveInt(value) {
    const parsed = Number(value);
    if (!Number.isInteger(parsed) || parsed <= 0)
        return undefined;
    return parsed;
}
function isTimeoutAbort(error) {
    if (!error || typeof error !== 'object')
        return false;
    const err = error;
    const name = typeof err.name === 'string' ? err.name : '';
    const message = typeof err.message === 'string' ? err.message.toLowerCase() : '';
    return name === 'TimeoutError'
        || name === 'AbortError'
        || message.includes('operation was aborted')
        || message.includes('timeout');
}
function normalizeInferPayload(payload) {
    const sourceInput = payload.input;
    const input = sourceInput && typeof sourceInput === 'object' && !Array.isArray(sourceInput)
        ? { ...sourceInput }
        : { ...payload };
    const normalized = sourceInput && typeof sourceInput === 'object' && !Array.isArray(sourceInput)
        ? { ...payload, input }
        : { input };
    if (Array.isArray(input.messages) && input.stream === undefined) {
        input.stream = false;
    }
    return normalized;
}
function resolveStepVideoFrames(payload) {
    const input = payload.input && typeof payload.input === 'object' && !Array.isArray(payload.input)
        ? payload.input
        : payload;
    return readPositiveInt(input.frames);
}
function resolveCreateInferTimeoutMs(cfg, service, payload) {
    if (service.trim().toLowerCase() === 'step_video') {
        const frames = resolveStepVideoFrames(payload) ?? 30;
        const derivedMs = 120000 + (frames * 500);
        return Math.min(300000, Math.max(cfg.httpTimeoutMs, roundUpMs(derivedMs, 5000)));
    }
    const input = payload.input && typeof payload.input === 'object' && !Array.isArray(payload.input)
        ? payload.input
        : payload;
    if (Array.isArray(input.messages)) {
        // LLM calls can legitimately take longer than image/status calls, especially
        // Qwen3 Parallax streaming, which live testing has returned after ~45s.
        return Math.max(cfg.httpTimeoutMs, 120000);
    }
    return cfg.httpTimeoutMs;
}
function parseSseResponse(text) {
    if (!/^data:/m.test(text))
        return undefined;
    let id;
    let model;
    let finishReason;
    let usage;
    let message = '';
    let reasoning = '';
    const chunks = [];
    for (const line of text.split(/\r?\n/)) {
        if (!line.startsWith('data:'))
            continue;
        const data = line.slice('data:'.length).trim();
        if (!data || data === '[DONE]')
            continue;
        try {
            const chunk = JSON.parse(data);
            chunks.push(chunk);
            id = id ?? chunk.id;
            model = model ?? chunk.model;
            usage = chunk.usage ?? usage;
            const choice = Array.isArray(chunk.choices) ? chunk.choices[0] : undefined;
            finishReason = choice?.finish_reason ?? finishReason;
            const delta = choice?.delta && typeof choice.delta === 'object'
                ? choice.delta
                : {};
            const messageObj = choice?.message && typeof choice.message === 'object'
                ? choice.message
                : {};
            const content = delta.content ?? messageObj.content ?? choice?.text;
            const reasoningChunk = delta.reasoning ?? messageObj.reasoning;
            if (typeof content === 'string')
                message += content;
            if (typeof reasoningChunk === 'string')
                reasoning += reasoningChunk;
        }
        catch {
            // Ignore malformed SSE data lines; retain successfully parsed chunks.
        }
    }
    return {
        status: 'success',
        body: {
            stream: true,
            infer_requests: [
                {
                    id: id ?? 'streaming-response',
                    state: 'success',
                    output: { message },
                    model,
                    finish_reason: finishReason,
                    usage,
                    metadata: {
                        reasoning,
                        reasoning_length: reasoning.length,
                        content_length: message.length
                    },
                    chunks
                }
            ]
        }
    };
}
function normalizeChatCompletionsJson(payload) {
    const body = payload && typeof payload === 'object'
        ? payload
        : {};
    const choices = Array.isArray(body.choices) ? body.choices : [];
    const firstChoice = choices[0] && typeof choices[0] === 'object'
        ? choices[0]
        : {};
    const messageObj = firstChoice.message && typeof firstChoice.message === 'object'
        ? firstChoice.message
        : {};
    const message = typeof messageObj.content === 'string' ? messageObj.content :
        typeof firstChoice.text === 'string' ? firstChoice.text :
            null;
    const reasoning = typeof messageObj.reasoning === 'string' ? messageObj.reasoning :
        typeof firstChoice.reasoning === 'string' ? firstChoice.reasoning :
            '';
    const usage = body.usage && typeof body.usage === 'object'
        ? { ...body.usage }
        : body.usage;
    return {
        status: 'success',
        body: {
            chat_completions: body,
            infer_requests: [
                {
                    id: body.id ?? 'chat-completions-response',
                    state: 'success',
                    output: { message },
                    model: body.model,
                    finish_reason: firstChoice.finish_reason,
                    usage,
                    metadata: {
                        reasoning,
                        reasoning_length: reasoning.length,
                        content_length: typeof message === 'string' ? message.length : 0
                    }
                }
            ]
        }
    };
}
async function postJsonOrSse(cfg, url, body, timeoutMs) {
    for (let attempt = 0; attempt <= cfg.httpMaxRetries; attempt += 1) {
        const canRetry = attempt < cfg.httpMaxRetries;
        try {
            const res = await fetch(url, {
                method: 'POST',
                headers: h(cfg),
                body: JSON.stringify(body),
                signal: AbortSignal.timeout(timeoutMs)
            });
            const text = await res.text();
            if (!res.ok) {
                if (canRetry && (RETRIABLE_STATUS.has(res.status) || isRetriableHttpError(res.status, text))) {
                    await sleep(backoffDelayMs(attempt + 1, cfg.httpRetryBackoffMs));
                    continue;
                }
                throw fromHttpError('theta-ondemand-api', url, res.status, text);
            }
            try {
                return JSON.parse(text);
            }
            catch {
                const parsedSse = parseSseResponse(text);
                if (parsedSse)
                    return parsedSse;
                return { status: 'success', raw: text };
            }
        }
        catch (error) {
            if (isStructuredError(error))
                throw error;
            if (isTimeoutAbort(error)) {
                throw fromTransportError('theta-ondemand-api', url, error);
            }
            if (canRetry) {
                await sleep(backoffDelayMs(attempt + 1, cfg.httpRetryBackoffMs));
                continue;
            }
            throw fromTransportError('theta-ondemand-api', url, error);
        }
    }
    throw fromTransportError('theta-ondemand-api', url, new Error('HTTP request failed after retries'));
}
function backoffDelayMs(attempt, baseMs) {
    return baseMs * Math.max(1, 2 ** (attempt - 1));
}
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
export const onDemandApiClient = {
    listServices: (cfg) => getJson(`${baseUrl(cfg)}/service/list?expand=template_id`, optionalNet(cfg)),
    createInferRequest: (cfg, service, payload, opts) => {
        const body = normalizeInferPayload(payload);
        const timeoutMs = resolveCreateInferTimeoutMs(cfg, service, body);
        return postJsonOrSse(cfg, `${baseUrl(cfg)}${inferPath(service, opts)}`, body, timeoutMs);
    },
    createChatCompletionRequest: async (cfg, body) => {
        const timeoutMs = Array.isArray(body.messages) && body.stream === false
            ? Math.max(cfg.httpTimeoutMs, 120000)
            : cfg.httpTimeoutMs;
        const result = await postJsonOrSse(cfg, `${baseUrl(cfg)}${chatCompletionsPath()}`, body, timeoutMs);
        if (result && typeof result === 'object' && result.body)
            return result;
        return normalizeChatCompletionsJson(result);
    },
    getInferRequest: (cfg, requestId) => getJson(`${baseUrl(cfg)}/infer_request/${encodePathSegment(requestId, 'requestId')}`, net(cfg)),
    createInputPresignedUrls: (cfg, service, inputFields) => postJson(`${baseUrl(cfg)}/infer_request/${encodePathSegment(service, 'service')}/input_presigned_urls`, inputFields?.length ? { input_fields: inputFields } : {}, net(cfg))
};
