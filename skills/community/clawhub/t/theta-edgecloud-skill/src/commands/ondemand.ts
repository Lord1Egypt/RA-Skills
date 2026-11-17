import { ThetaConfig } from '../config.js';
import { onDemandApiClient, type OnDemandInferOptions } from '../clients/ondemandApi.js';
import {
  isOnDemandChatService,
  listOnDemandServices,
  ONDEMAND_CHAT_SERVICE_SLUGS,
  ONDEMAND_SERVICE_CATALOG,
  OPENAI_CHAT_COMPLETION_SERVICES,
  TOOL_CALLING_CHAT_SERVICES,
  type OnDemandServiceSpec
} from './ondemandCatalog.js';
import { isStructuredError } from '../errors.js';
import { boundChatParams } from '../approval.js';

type PollOpts = {
  intervalMs?: number;
  timeoutMs?: number;
  maxAttempts?: number;
};

type InferRequestLike = {
  id?: string;
  state?: string;
  input?: Record<string, unknown>;
};

type OnDemandLiveServiceListResponse = {
  status?: string;
  body?: {
    services?: Array<Record<string, unknown>>;
  };
};

type ListServicesOptions = {
  category?: string;
};

export type OnDemandChatMessage = {
  role: string;
  content: string | null;
  tool_calls?: Array<Record<string, unknown>>;
  tool_call_id?: string;
};

export type OnDemandChatOptions = {
  maxTokens?: number;
  temperature?: number;
  topP?: number;
  stream?: boolean;
  wait?: number;
  prediction?: string;
  variant?: string;
  webhook?: string;
  reasoningEffort?: string;
  enableThinking?: boolean;
  tools?: Array<Record<string, unknown>>;
  toolChoice?: unknown;
  parallelToolCalls?: boolean;
  extraInput?: Record<string, unknown>;
  allowUnknownService?: boolean;
  allowUnverifiedTools?: boolean;
  confirm?: boolean;
};

function getFirstInferRequest(payload: unknown): InferRequestLike | undefined {
  if (!payload || typeof payload !== 'object') return undefined;
  const body = (payload as { body?: { infer_requests?: InferRequestLike[] } }).body;
  if (!body?.infer_requests?.length) return undefined;
  return body.infer_requests[0];
}

function isTerminal(state?: string): boolean {
  return state === 'success' || state === 'error' || state === 'failed' || state === 'cancelled';
}

function clampInt(value: number | undefined, fallback: number, min: number, max: number): number {
  if (!Number.isFinite(value)) return fallback;
  return Math.min(Math.max(Math.trunc(value as number), min), max);
}

function clampFloat(value: number | undefined, fallback: number, min: number, max: number): number {
  if (!Number.isFinite(value)) return fallback;
  return Math.min(Math.max(value as number, min), max);
}

function roundUpMs(value: number, bucketMs: number): number {
  return Math.ceil(value / bucketMs) * bucketMs;
}

function readPositiveInt(value: unknown): number | undefined {
  const parsed = Number(value);
  if (!Number.isInteger(parsed) || parsed <= 0) return undefined;
  return parsed;
}

function deriveAdaptivePollTimeoutMs(inferRequest?: InferRequestLike): number | undefined {
  const input = inferRequest?.input;
  if (!input || typeof input !== 'object') return undefined;

  const frames = readPositiveInt(input.frames);
  if (!frames) return undefined;

  const fps = readPositiveInt(input.fps) ?? 10;
  const renderSeconds = Math.max(1, Math.ceil(frames / Math.max(1, fps)));
  const queueAndVarianceBufferMs = 240000;
  const frameScaledMs = frames * 4000;
  const durationScaledMs = renderSeconds * 60000;
  const derivedMs = queueAndVarianceBufferMs + Math.max(frameScaledMs, durationScaledMs);
  const roundedMs = roundUpMs(derivedMs, 30000);

  return Math.min(1800000, Math.max(360000, roundedMs));
}

function errorSummary(error: unknown): Record<string, unknown> {
  if (isStructuredError(error)) {
    return {
      code: error.code,
      message: error.message,
      retriable: error.retriable,
      status: error.status,
      service: error.service
    };
  }

  const asError = error as { name?: string; message?: string } | undefined;
  return {
    code: asError?.name ?? 'ERROR',
    message: asError?.message ?? String(error ?? 'Unknown error')
  };
}

function normalizeMessages(messages: OnDemandChatMessage[]): OnDemandChatMessage[] {
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
    const toolOnly = message.role === 'assistant' && Array.isArray(message.tool_calls) && message.tool_calls.length > 0;
    if ((typeof message.content !== 'string' || !message.content.trim()) && !toolOnly) {
      throw new Error(`messages[${index}].content must be a non-empty string`);
    }
    if (message.role === 'tool' && !message.tool_call_id?.trim()) throw new Error(`messages[${index}].tool_call_id is required`);
    return { role: message.role.trim(), content: message.content,
      ...(message.tool_calls ? { tool_calls: message.tool_calls } : {}),
      ...(message.tool_call_id ? { tool_call_id: message.tool_call_id } : {}) };
  });
}

function resolveDefaultMaxTokens(service: string | undefined): number {
  if (service === 'gpt_oss_120b') return 1800;
  // Ling writes its reasoning into content; 16-200 token limits returned only reasoning (2026-10-03).
  if (service === 'ling_3_0_flash_fin') return 2048;
  return 500;
}

function buildChatPayload(messages: OnDemandChatMessage[], opts: OnDemandChatOptions = {}, service?: string) {
  const permittedExtra = new Set(['stop', 'seed', 'presence_penalty', 'frequency_penalty', 'response_format', 'top_k', 'reasoning_effort', 'enable_thinking', 'variant', 'style_image_filename', 'image_filename', 'input_img', 'frames', 'fps', 'duration', 'ratio', 'resolution', 'reference_image_url', 'reference_video_url', 'reference_audio_url', 'generate_audio', 'watermark', 'audio_filename', 'detection_prompt', 'question', 'prompt', 'filename', 'strength', 'guidance_scale', 'negative_prompt']);
  const safeExtra = Object.fromEntries(Object.entries(opts.extraInput ?? {}).filter(([key]) => permittedExtra.has(key)));
  const input: Record<string, unknown> = {
    ...safeExtra,
    messages: normalizeMessages(messages),
    max_tokens: clampInt(opts.maxTokens, resolveDefaultMaxTokens(service), 1, 5000),
    temperature: clampFloat(opts.temperature, 0.5, 0, 2),
    top_p: clampFloat(opts.topP, 0.7, 0, 1),
    stream: opts.stream ?? false
  };

  if (opts.reasoningEffort !== undefined) {
    input.reasoning_effort = opts.reasoningEffort;
  }
  if (opts.enableThinking !== undefined) {
    input.enable_thinking = opts.enableThinking;
  }
  if (opts.tools !== undefined) input.tools = opts.tools;
  if (opts.toolChoice !== undefined) input.tool_choice = opts.toolChoice;
  if (opts.parallelToolCalls !== undefined) input.parallel_tool_calls = opts.parallelToolCalls;

  // Same bounds the client enforces, applied here too so dry-run previews show the exact body sent.
  const payload: Record<string, unknown> = { input: boundChatParams(input, resolveDefaultMaxTokens(service)) };
  if (opts.variant) payload.variant = opts.variant;
  if (opts.webhook) payload.webhook = opts.webhook;

  const requestOptions: OnDemandInferOptions = {
    wait: clampInt(opts.wait, 30, 0, 60),
    prediction: opts.prediction ?? 'completions'
  };

  return { payload, requestOptions };
}

function summarizeLiveService(service: Record<string, unknown>): Record<string, unknown> {
  const predictions = service.predictions && typeof service.predictions === 'object'
    ? (service.predictions as Record<string, Record<string, unknown>>)
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
    category: categorizeOnDemandService(service),
    state: service.state,
    workloadType: service.workload_type,
    rank: service.rank,
    defaultPrediction,
    inputFields: inputVars ? Object.keys(inputVars) : [],
    inputExample: inputVars ? buildInputExample(inputVars as Record<string, unknown>) : {},
    variants: prediction?.variants,
    workers: service.workers,
    updateTime: service.update_time,
    pricing: prediction?.instructions,
    inputSchema: inputVars,
    predictions,
    openrouter: prediction?.openrouter_metadata
  };
}

function normalizeCategory(value: unknown): string | undefined {
  if (typeof value !== 'string') return undefined;
  const normalized = value.trim().toLowerCase();
  return normalized || undefined;
}

export function categorizeOnDemandService(service: Record<string, unknown>): string {
  const alias = typeof service.alias === 'string' ? service.alias.toLowerCase() : '';
  const name = typeof service.name === 'string' ? service.name.toLowerCase() : '';
  const text = `${alias} ${name}`;
  if (text.includes('whisper') || text.includes('audio') || text.includes('voice')) return 'audio';
  if (text.includes('video') || text.includes('talking_head')) return 'video';
  if (text.includes('llava') || text.includes('vision')) return 'vision';
  if (text.includes('blip') || text.includes('grounding') || text.includes('dino')) return 'vision';
  if (text.includes('flux') || text.includes('stable') || text.includes('sdxl') || text.includes('image') || text.includes('upscale') || text.includes('esrgan')) return 'image';
  if (text.includes('glm') || text.includes('qwen') || text.includes('gpt') || text.includes('llama') || text.includes('mistral') || text.includes('chat')) return 'text';
  return 'other';
}

function categorizeCatalogService(service: OnDemandServiceSpec): string {
  const category = service.category.toLowerCase();
  if (category.includes('speech') || category.includes('audio') || category.includes('voice')) return 'audio';
  if (category.includes('video')) return 'video';
  if (category.includes('vision') || category.includes('caption') || category.includes('detection')) return 'vision';
  if (category.includes('image')) return 'image';
  if (category.includes('llm') || category.includes('text')) return 'text';
  return 'other';
}

function buildInputExample(inputVars: Record<string, unknown>): Record<string, unknown> {
  const example: Record<string, unknown> = {};
  for (const [field, rawSpec] of Object.entries(inputVars)) {
    const spec = rawSpec && typeof rawSpec === 'object' ? rawSpec as Record<string, unknown> : {};
    const defaultValue = spec.default_value ?? spec.default;
    const type = typeof spec.type === 'string' ? spec.type : '';
    if (defaultValue !== undefined) {
      example[field] = defaultValue;
    } else if (field === 'messages' || type === 'chat_array') {
      example[field] = [{ role: 'user', content: 'Hello' }];
    } else if (field.includes('filename') || field.includes('input_img') || type === 'filename') {
      example[field] = '<filename from get_upload_url>';
    } else if (field === 'prompt') {
      example[field] = 'Your prompt here';
    } else if (type === 'integer' || type === 'number' || type === 'float') {
      example[field] = 1;
    } else if (type === 'bool' || type === 'boolean') {
      example[field] = false;
    } else {
      example[field] = 'string value';
    }
  }
  return example;
}

function filterLiveSummaries(services: Array<Record<string, unknown>>, opts: ListServicesOptions = {}) {
  const category = normalizeCategory(opts.category);
  return services
    .map(summarizeLiveService)
    .filter((service) => !category || service.category === category);
}

function filterCatalogServices(opts: ListServicesOptions = {}) {
  const category = normalizeCategory(opts.category);
  return listOnDemandServices()
    .filter((service) => !category || categorizeCatalogService(service) === category)
    .map((service) => ({
      ...service,
      normalizedCategory: categorizeCatalogService(service)
    }));
}

const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

export const ondemand = {
  catalog: ONDEMAND_SERVICE_CATALOG,
  listServices: (opts: ListServicesOptions = {}) => filterCatalogServices(opts),

  listLiveServices: async (cfg: ThetaConfig, opts: ListServicesOptions = {}) => {
    try {
      const response = await onDemandApiClient.listServices(cfg) as OnDemandLiveServiceListResponse;
      const live = response.body?.services ?? [];
      return {
        source: 'live',
        category: normalizeCategory(opts.category),
        services: filterLiveSummaries(live, opts),
        catalogFallbackAvailable: true
      };
    } catch (error) {
      return {
        source: 'catalog',
        category: normalizeCategory(opts.category),
        warning: 'Live service discovery failed; returning bundled catalog fallback.',
        error: errorSummary(error),
        services: filterCatalogServices(opts)
      };
    }
  },

  // Sends the payload to Theta on-demand inference (billable). The client enforces the approval
  // allowlist (video/unknown services and webhooks need confirm:true) and chat token bounds.
  infer: (cfg: ThetaConfig, service: string, payload: Record<string, unknown>, opts?: OnDemandInferOptions) =>
    cfg.dryRun
      ? { dryRun: true, service, payload: payload?.input && typeof payload.input === 'object' && !Array.isArray(payload.input) ? { ...payload, input: boundChatParams(payload.input as Record<string, unknown>) } : payload, requestOptions: opts }
      : onDemandApiClient.createInferRequest(cfg, service, payload, opts),

  chat: (cfg: ThetaConfig, service: string, messages: OnDemandChatMessage[], opts: OnDemandChatOptions = {}) => {
    if (!opts.allowUnknownService && !isOnDemandChatService(service)) {
      throw new Error(`Unsupported on-demand chat service: ${service}. Known chat services: ${ONDEMAND_CHAT_SERVICE_SLUGS.join(', ')}`);
    }

    if (opts.tools?.length && opts.allowUnverifiedTools !== true && !TOOL_CALLING_CHAT_SERVICES.includes(service)) {
      // Theta silently drops tools for these models and answers in plain text; fail loudly instead.
      throw new Error(`Service ${service} does not return structured tool calls (live-verified 2026-10-03). Use ${TOOL_CALLING_CHAT_SERVICES.filter((x) => x !== 'gpt_oss_120b').join(' or ')} for tool use, or set allowUnverifiedTools:true (exactly) to send anyway.`);
    }

    const effectiveOpts = service === 'qwen3'
      ? { ...opts, stream: opts.stream ?? true, wait: opts.wait ?? 60 }
      : ['gpt_oss_120b', 'glm_5_3', 'glm_5_3_flash'].includes(service)
        ? { ...opts, reasoningEffort: opts.reasoningEffort ?? 'low' }
      : opts;
    const { payload, requestOptions } = buildChatPayload(messages, effectiveOpts, service);
    if (OPENAI_CHAT_COMPLETION_SERVICES.includes(service)) {
      const input = payload.input as Record<string, unknown>;
      const body = {
        ...input,
        model: service
      } as {
        model: string;
        messages: OnDemandChatMessage[];
        max_tokens?: number;
        temperature?: number;
        top_p?: number;
        stream?: boolean;
        reasoning_effort?: string;
        enable_thinking?: boolean;
      };
      return cfg.dryRun
        ? { dryRun: true, service, endpoint: 'chat/completions', payload: body }
        : onDemandApiClient.createChatCompletionRequest(cfg, body, { confirm: opts.confirm, allowUnverifiedTools: opts.allowUnverifiedTools === true });
    }

    return cfg.dryRun
      ? { dryRun: true, service, payload, requestOptions }
      : onDemandApiClient.createInferRequest(cfg, service, payload, { ...requestOptions, confirm: opts.confirm, allowUnverifiedTools: opts.allowUnverifiedTools === true });
  },

  status: (cfg: ThetaConfig, requestId: string) => onDemandApiClient.getInferRequest(cfg, requestId),

  inputPresignedUrls: (cfg: ThetaConfig, service: string, inputFields?: string[]) =>
    cfg.dryRun ? { dryRun: true, service, inputFields } : onDemandApiClient.createInputPresignedUrls(cfg, service, inputFields),

  pollUntilDone: async (cfg: ThetaConfig, requestId: string, opts: PollOpts = {}) => {
    if (!requestId) throw new Error('requestId is required');

    const intervalMs = clampInt(opts.intervalMs, 3000, 100, 60000);
    const explicitTimeoutMs = opts.timeoutMs === undefined
      ? undefined
      : clampInt(opts.timeoutMs, 120000, 1000, 3600000);
    let timeoutMs = explicitTimeoutMs ?? 120000;
    const maxAttempts = clampInt(opts.maxAttempts, 1000, 1, 20000);

    const startedAt = Date.now();
    let attempts = 0;
    let lastResult: unknown;

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
        if (adaptiveTimeoutMs !== undefined) timeoutMs = adaptiveTimeoutMs;
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
      if (sleepMs > 0) await sleep(sleepMs);
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
