import { onDemandApiClient } from '../clients/ondemandApi.js';
import { isOnDemandChatService, listOnDemandServices, ONDEMAND_SERVICE_CATALOG } from './ondemandCatalog.js';
import { isStructuredError } from '../errors.js';
function getFirstInferRequest(payload) {
    if (!payload || typeof payload !== 'object')
        return undefined;
    const body = payload.body;
    if (!body?.infer_requests?.length)
        return undefined;
    return body.infer_requests[0];
}
function isTerminal(state) {
    return state === 'success' || state === 'error' || state === 'failed' || state === 'cancelled';
}
function clampInt(value, fallback, min, max) {
    if (!Number.isFinite(value))
        return fallback;
    return Math.min(Math.max(Math.trunc(value), min), max);
}
function clampFloat(value, fallback, min, max) {
    if (!Number.isFinite(value))
        return fallback;
    return Math.min(Math.max(value, min), max);
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
function deriveAdaptivePollTimeoutMs(inferRequest) {
    const input = inferRequest?.input;
    if (!input || typeof input !== 'object')
        return undefined;
    const frames = readPositiveInt(input.frames);
    if (!frames)
        return undefined;
    const fps = readPositiveInt(input.fps) ?? 10;
    const renderSeconds = Math.max(1, Math.ceil(frames / Math.max(1, fps)));
    const queueAndVarianceBufferMs = 240000;
    const frameScaledMs = frames * 4000;
    const durationScaledMs = renderSeconds * 60000;
    const derivedMs = queueAndVarianceBufferMs + Math.max(frameScaledMs, durationScaledMs);
    const roundedMs = roundUpMs(derivedMs, 30000);
    return Math.min(1800000, Math.max(360000, roundedMs));
}
function errorSummary(error) {
    if (isStructuredError(error)) {
        return {
            code: error.code,
            message: error.message,
            retriable: error.retriable,
            status: error.status,
            service: error.service
        };
    }
    const asError = error;
    return {
        code: asError?.name ?? 'ERROR',
        message: asError?.message ?? String(error ?? 'Unknown error')
    };
}
function normalizeMessages(messages) {
    if (!Array.isArray(messages) || messages.length === 0) {
        throw new Error('messages must be a non-empty array');
    }
    return messages.map((message, index) => {
        if (!message || typeof message !== 'object') {
            throw new Error(`messages[${index}] must be an object`);
        }
        if (typeof message.role !== 'string' || !message.role.trim()) {
            throw new Error(`messages[${index}].role must be a non-empty string`);
        }
        if (typeof message.content !== 'string' || !message.content.trim()) {
            throw new Error(`messages[${index}].content must be a non-empty string`);
        }
        return { role: message.role.trim(), content: message.content };
    });
}
function resolveDefaultMaxTokens(service) {
    return service === 'gpt_oss_120b' ? 1800 : 500;
}
function buildChatPayload(messages, opts = {}, service) {
    const input = {
        ...(opts.extraInput ?? {}),
        messages: normalizeMessages(messages),
        max_tokens: clampInt(opts.maxTokens, resolveDefaultMaxTokens(service), 1, 5000),
        temperature: clampFloat(opts.temperature, 0.5, 0, 2),
        top_p: clampFloat(opts.topP, 0.7, 0, 1),
        stream: opts.stream ?? false
    };
    if (opts.reasoningEffort !== undefined) {
        input.reasoning_effort = opts.reasoningEffort;
    }
    const payload = { input };
    if (opts.variant)
        payload.variant = opts.variant;
    if (opts.webhook)
        payload.webhook = opts.webhook;
    const requestOptions = {
        wait: clampInt(opts.wait, 30, 0, 60),
        prediction: opts.prediction ?? 'completions'
    };
    return { payload, requestOptions };
}
function summarizeLiveService(service) {
    const predictions = service.predictions && typeof service.predictions === 'object'
        ? service.predictions
        : {};
    const defaultPrediction = typeof service.default_prediction === 'string'
        ? service.default_prediction
        : Object.keys(predictions)[0];
    const prediction = defaultPrediction ? predictions[defaultPrediction] : undefined;
    const inputVars = prediction?.input_vars && typeof prediction.input_vars === 'object'
        ? prediction.input_vars
        : undefined;
    return {
        source: 'live',
        alias: service.alias,
        name: service.name,
        category: categorizeService(service),
        state: service.state,
        workloadType: service.workload_type,
        rank: service.rank,
        defaultPrediction,
        inputFields: inputVars ? Object.keys(inputVars) : [],
        inputExample: inputVars ? buildInputExample(inputVars) : {},
        variants: prediction?.variants,
        workers: service.workers,
        updateTime: service.update_time,
        pricing: prediction?.instructions,
        openrouter: prediction?.openrouter_metadata
    };
}
function normalizeCategory(value) {
    if (typeof value !== 'string')
        return undefined;
    const normalized = value.trim().toLowerCase();
    return normalized || undefined;
}
function categorizeService(service) {
    const alias = typeof service.alias === 'string' ? service.alias.toLowerCase() : '';
    const name = typeof service.name === 'string' ? service.name.toLowerCase() : '';
    const text = `${alias} ${name}`;
    if (text.includes('whisper') || text.includes('audio') || text.includes('voice'))
        return 'audio';
    if (text.includes('video') || text.includes('talking_head'))
        return 'video';
    if (text.includes('llava') || text.includes('vision'))
        return 'vision';
    if (text.includes('blip') || text.includes('grounding') || text.includes('dino'))
        return 'vision';
    if (text.includes('flux') || text.includes('stable') || text.includes('sdxl') || text.includes('image') || text.includes('upscale'))
        return 'image';
    if (text.includes('qwen') || text.includes('gpt') || text.includes('llama') || text.includes('mistral') || text.includes('chat'))
        return 'text';
    return 'other';
}
function categorizeCatalogService(service) {
    const category = service.category.toLowerCase();
    if (category.includes('speech') || category.includes('audio') || category.includes('voice'))
        return 'audio';
    if (category.includes('video'))
        return 'video';
    if (category.includes('vision') || category.includes('caption') || category.includes('detection'))
        return 'vision';
    if (category.includes('image'))
        return 'image';
    if (category.includes('llm') || category.includes('text'))
        return 'text';
    return 'other';
}
function buildInputExample(inputVars) {
    const example = {};
    for (const [field, rawSpec] of Object.entries(inputVars)) {
        const spec = rawSpec && typeof rawSpec === 'object' ? rawSpec : {};
        const defaultValue = spec.default_value ?? spec.default;
        const type = typeof spec.type === 'string' ? spec.type : '';
        if (defaultValue !== undefined) {
            example[field] = defaultValue;
        }
        else if (field === 'messages' || type === 'chat_array') {
            example[field] = [{ role: 'user', content: 'Hello' }];
        }
        else if (field.includes('filename') || field.includes('input_img') || type === 'filename') {
            example[field] = 'https://example.com/file';
        }
        else if (field === 'prompt') {
            example[field] = 'Your prompt here';
        }
        else if (type === 'integer' || type === 'number' || type === 'float') {
            example[field] = 1;
        }
        else if (type === 'bool' || type === 'boolean') {
            example[field] = false;
        }
        else {
            example[field] = 'string value';
        }
    }
    return example;
}
function filterLiveSummaries(services, opts = {}) {
    const category = normalizeCategory(opts.category);
    return services
        .map(summarizeLiveService)
        .filter((service) => !category || service.category === category);
}
function filterCatalogServices(opts = {}) {
    const category = normalizeCategory(opts.category);
    return listOnDemandServices()
        .filter((service) => !category || categorizeCatalogService(service) === category)
        .map((service) => ({
        ...service,
        normalizedCategory: categorizeCatalogService(service)
    }));
}
const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
export const ondemand = {
    catalog: ONDEMAND_SERVICE_CATALOG,
    listServices: (opts = {}) => filterCatalogServices(opts),
    listLiveServices: async (cfg, opts = {}) => {
        try {
            const response = await onDemandApiClient.listServices(cfg);
            const live = response.body?.services ?? [];
            return {
                source: 'live',
                category: normalizeCategory(opts.category),
                services: filterLiveSummaries(live, opts),
                catalogFallbackAvailable: true
            };
        }
        catch (error) {
            return {
                source: 'catalog',
                category: normalizeCategory(opts.category),
                warning: 'Live service discovery failed; returning bundled catalog fallback.',
                error: errorSummary(error),
                services: filterCatalogServices(opts)
            };
        }
    },
    infer: (cfg, service, payload, opts) => cfg.dryRun ? { dryRun: true, service, payload, requestOptions: opts } : onDemandApiClient.createInferRequest(cfg, service, payload, opts),
    chat: (cfg, service, messages, opts = {}) => {
        if (!opts.allowUnknownService && !isOnDemandChatService(service)) {
            throw new Error(`Unsupported on-demand chat service: ${service}. Known chat services: qwen3, minimax_m2_5, gpt_oss_120b, llama_3_1_70b, llama_3_8b`);
        }
        const effectiveOpts = service === 'qwen3'
            ? { ...opts, stream: opts.stream ?? true, wait: opts.wait ?? 60 }
            : service === 'gpt_oss_120b'
                ? { ...opts, reasoningEffort: opts.reasoningEffort ?? 'low' }
                : opts;
        const { payload, requestOptions } = buildChatPayload(messages, effectiveOpts, service);
        if (service === 'gpt_oss_120b') {
            const input = payload.input;
            const body = {
                ...input,
                model: service
            };
            return cfg.dryRun
                ? { dryRun: true, service, endpoint: 'chat/completions', payload: body }
                : onDemandApiClient.createChatCompletionRequest(cfg, body);
        }
        return cfg.dryRun
            ? { dryRun: true, service, payload, requestOptions }
            : onDemandApiClient.createInferRequest(cfg, service, payload, requestOptions);
    },
    status: (cfg, requestId) => onDemandApiClient.getInferRequest(cfg, requestId),
    inputPresignedUrls: (cfg, service, inputFields) => cfg.dryRun ? { dryRun: true, service, inputFields } : onDemandApiClient.createInputPresignedUrls(cfg, service, inputFields),
    pollUntilDone: async (cfg, requestId, opts = {}) => {
        if (!requestId)
            throw new Error('requestId is required');
        const intervalMs = clampInt(opts.intervalMs, 3000, 100, 60000);
        const explicitTimeoutMs = opts.timeoutMs === undefined
            ? undefined
            : clampInt(opts.timeoutMs, 120000, 1000, 3600000);
        let timeoutMs = explicitTimeoutMs ?? 120000;
        const maxAttempts = clampInt(opts.maxAttempts, 1000, 1, 20000);
        const startedAt = Date.now();
        let attempts = 0;
        let lastResult;
        while (attempts < maxAttempts) {
            const elapsedBeforeRequest = Date.now() - startedAt;
            if (elapsedBeforeRequest >= timeoutMs) {
                return {
                    attempts,
                    elapsedMs: elapsedBeforeRequest,
                    terminalState: 'timeout',
                    result: lastResult
                };
            }
            attempts += 1;
            const result = await onDemandApiClient.getInferRequest(cfg, requestId);
            lastResult = result;
            const inferRequest = getFirstInferRequest(result);
            if (explicitTimeoutMs === undefined) {
                const adaptiveTimeoutMs = deriveAdaptivePollTimeoutMs(inferRequest);
                if (adaptiveTimeoutMs !== undefined)
                    timeoutMs = adaptiveTimeoutMs;
            }
            if (isTerminal(inferRequest?.state)) {
                return {
                    attempts,
                    elapsedMs: Date.now() - startedAt,
                    terminalState: inferRequest?.state,
                    result
                };
            }
            const elapsedAfterRequest = Date.now() - startedAt;
            if (elapsedAfterRequest >= timeoutMs) {
                return {
                    attempts,
                    elapsedMs: elapsedAfterRequest,
                    terminalState: 'timeout',
                    result
                };
            }
            const sleepMs = Math.min(intervalMs, Math.max(0, timeoutMs - elapsedAfterRequest));
            if (sleepMs > 0)
                await sleep(sleepMs);
        }
        return {
            attempts,
            elapsedMs: Date.now() - startedAt,
            terminalState: 'max-attempts',
            result: lastResult
        };
    }
};
export const buildOnDemandChatPayloadForTest = buildChatPayload;
