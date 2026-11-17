// Data flow: sends the on-demand Bearer token plus user prompts, messages and input filenames to
// https://ondemand.thetaedgecloud.com only. Inference is billable; video, unknown/high-cost
// services and webhooks require confirm:true.
import { ThetaConfig } from '../config.js';
import { fromHttpError, fromTransportError, isRetriableHttpError, isStructuredError } from '../errors.js';
import { getJson, postJson } from './http.js';
import { thetaUrl, pathSegment } from '../security.js';

const DEFAULT_BASE = 'https://ondemand.thetaedgecloud.com';
const RETRIABLE_STATUS = new Set([408, 425, 429, 500, 502, 503, 504]);

function baseUrl(cfg: ThetaConfig): string {
  const raw = cfg.onDemandApiBaseUrl?.trim() || DEFAULT_BASE;
  return thetaUrl(raw, 'ondemand');
}

function h(cfg: ThetaConfig): HeadersInit {
  if (!cfg.onDemandApiToken) throw new Error('THETA_ONDEMAND_API_TOKEN missing');
  return {
    Authorization: `Bearer ${cfg.onDemandApiToken}`,
    'content-type': 'application/json'
  };
}

function optionalHeaders(cfg: ThetaConfig): HeadersInit {
  return cfg.onDemandApiToken
    ? { Authorization: `Bearer ${cfg.onDemandApiToken}`, 'content-type': 'application/json' }
    : { 'content-type': 'application/json' };
}

function net(cfg: ThetaConfig) {
  return {
    headers: h(cfg),
    service: 'theta-ondemand-api',
    timeoutMs: cfg.httpTimeoutMs,
    maxRetries: cfg.httpMaxRetries,
    retryBackoffMs: cfg.httpRetryBackoffMs
  };
}

function optionalNet(cfg: ThetaConfig) {
  return {
    headers: optionalHeaders(cfg),
    service: 'theta-ondemand-api',
    timeoutMs: cfg.httpTimeoutMs,
    maxRetries: cfg.httpMaxRetries,
    retryBackoffMs: cfg.httpRetryBackoffMs
  };
}

import { assertApproved, assertLive, boundChatParams, findCallbackFields, snapshotBody } from '../approval.js';
import { inferenceRequiresConfirm, OPENAI_CHAT_COMPLETION_SERVICES, TOOL_CALLING_CHAT_SERVICES } from '../commands/ondemandCatalog.js';

export type OnDemandInferOptions = {
  wait?: number;
  prediction?: string;
  confirm?: boolean;
  allowUnverifiedTools?: boolean;
};

export type OnDemandChatCompletionBody = {
  model: string;
  messages: Array<{ role: string; content: string | null; tool_calls?: Array<Record<string, unknown>>; tool_call_id?: string }>;
  max_tokens?: number;
  temperature?: number;
  top_p?: number;
  stream?: boolean;
  [key: string]: unknown;
};

function encodePathSegment(value: string, label: string): string {
  return pathSegment(value, label);
}

function inferPath(service: string, opts: OnDemandInferOptions = {}): string {
  const params = new URLSearchParams();
  if (opts.wait !== undefined) {
    const wait = Number(opts.wait);
    params.set('wait', String(Number.isFinite(wait) ? Math.min(Math.max(Math.trunc(wait), 0), 60) : 30));
  }
  if (opts.prediction) params.set('prediction', opts.prediction);
  const query = params.toString();
  return `/infer_request/${encodePathSegment(service, 'service')}${query ? `?${query}` : ''}`;
}

function chatCompletionsPath(): string {
  return '/infer_request/chat/completions';
}

function roundUpMs(value: number, bucketMs: number): number {
  return Math.ceil(value / bucketMs) * bucketMs;
}

function readPositiveInt(value: unknown): number | undefined {
  const parsed = Number(value);
  if (!Number.isInteger(parsed) || parsed <= 0) return undefined;
  return parsed;
}

function isTimeoutAbort(error: unknown): boolean {
  if (!error || typeof error !== 'object') return false;
  const err = error as { name?: unknown; message?: unknown };
  const name = typeof err.name === 'string' ? err.name : '';
  const message = typeof err.message === 'string' ? err.message.toLowerCase() : '';
  return name === 'TimeoutError'
    || name === 'AbortError'
    || message.includes('operation was aborted')
    || message.includes('timeout');
}

function normalizeInferPayload(payload: Record<string, unknown>): Record<string, unknown> {
  const sourceInput = payload.input;
  const input = sourceInput && typeof sourceInput === 'object' && !Array.isArray(sourceInput)
    ? { ...(sourceInput as Record<string, unknown>) }
    : { ...payload };

  const normalized: Record<string, unknown> = sourceInput && typeof sourceInput === 'object' && !Array.isArray(sourceInput)
    ? { ...payload, input }
    : { input };

  if (Array.isArray(input.messages) && input.stream === undefined) {
    input.stream = false;
  }

  return normalized;
}

function resolveStepVideoFrames(payload: Record<string, unknown>): number | undefined {
  const input = payload.input && typeof payload.input === 'object' && !Array.isArray(payload.input)
    ? payload.input as Record<string, unknown>
    : payload;
  return readPositiveInt(input.frames);
}

function resolveCreateInferTimeoutMs(cfg: ThetaConfig, service: string, payload: Record<string, unknown>): number {
  if (service.trim().toLowerCase() === 'step_video') {
    const frames = resolveStepVideoFrames(payload) ?? 30;
    const derivedMs = 120000 + (frames * 500);
    return Math.min(300000, Math.max(cfg.httpTimeoutMs, roundUpMs(derivedMs, 5000)));
  }

  const input = payload.input && typeof payload.input === 'object' && !Array.isArray(payload.input)
    ? payload.input as Record<string, unknown>
    : payload;
  if (Array.isArray(input.messages)) {
    // LLM calls can legitimately take longer than image/status calls, especially
    // Qwen3 Parallax streaming, which live testing has returned after ~45s.
    return Math.max(cfg.httpTimeoutMs, 120000);
  }

  return cfg.httpTimeoutMs;
}

function parseSseResponse(text: string): Record<string, unknown> | undefined {
  if (!/^data:/m.test(text)) return undefined;

  let id: string | undefined;
  let model: string | undefined;
  let finishReason: string | null | undefined;
  let usage: unknown;
  let message = '';
  let reasoning = '';
  const toolCalls = new Map<number, any>();
  const chunks: unknown[] = [];
  let done = false;
  let malformed = false;

  for (const line of text.split(/\r?\n/)) {
    if (!line.startsWith('data:')) continue;
    const data = line.slice('data:'.length).trim();
    if (data === '[DONE]') { done = true; continue; }
    if (!data) continue;

    try {
      const chunk = JSON.parse(data);
      chunks.push(chunk);
      id = id ?? chunk.id;
      model = model ?? chunk.model;
      usage = chunk.usage ?? usage;
      const choice = Array.isArray(chunk.choices) ? chunk.choices[0] : undefined;
      finishReason = choice?.finish_reason ?? finishReason;
      const delta = choice?.delta && typeof choice.delta === 'object'
        ? choice.delta as Record<string, unknown>
        : {};
      const messageObj = choice?.message && typeof choice.message === 'object'
        ? choice.message as Record<string, unknown>
        : {};
      const content = delta.content ?? messageObj.content ?? choice?.text;
      const reasoningChunk = delta.reasoning_content ?? delta.reasoning ?? messageObj.reasoning_content ?? messageObj.reasoning;
      if (typeof content === 'string') message += content;
      if (typeof reasoningChunk === 'string') reasoning += reasoningChunk;
      const incoming = delta.tool_calls ?? messageObj.tool_calls;
      if (Array.isArray(incoming)) for (const [position, part] of incoming.entries()) {
        const index = part.index ?? position;
        const current = toolCalls.get(index) ?? { type: 'function', function: { name: '', arguments: '' } };
        if (part.id) current.id = part.id;
        if (part.type) current.type = part.type;
        if (part.function?.name) current.function.name += part.function.name;
        if (part.function?.arguments) current.function.arguments += part.function.arguments;
        toolCalls.set(index, current);
      }
    } catch {
      malformed = true;
    }
  }

  if (malformed || !chunks.length || (!done && !finishReason)) throw new Error('Malformed or incomplete Theta event stream');
  return {
    status: 'success',
    body: {
      stream: true,
      infer_requests: [
        {
          id: id ?? 'streaming-response',
          state: 'success',
          output: { message, ...(toolCalls.size ? { tool_calls: [...toolCalls.entries()].sort(([a], [b]) => a - b).map(([, call]) => call) } : {}) },
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

function normalizeChatCompletionsJson(payload: unknown): Record<string, unknown> {
  const body = payload && typeof payload === 'object'
    ? payload as Record<string, unknown>
    : {};
  const choices = Array.isArray(body.choices) ? body.choices : [];
  const firstChoice = choices[0] && typeof choices[0] === 'object'
    ? choices[0] as Record<string, unknown>
    : {};
  const messageObj = firstChoice.message && typeof firstChoice.message === 'object'
    ? firstChoice.message as Record<string, unknown>
    : {};
  const message =
    typeof messageObj.content === 'string' ? messageObj.content :
    typeof firstChoice.text === 'string' ? firstChoice.text :
    null;
  const reasoning =
    typeof messageObj.reasoning_content === 'string' ? messageObj.reasoning_content :
    typeof messageObj.reasoning === 'string' ? messageObj.reasoning :
    typeof firstChoice.reasoning === 'string' ? firstChoice.reasoning :
    '';
  const usage = body.usage && typeof body.usage === 'object'
    ? { ...(body.usage as Record<string, unknown>) }
    : body.usage;

  return {
    status: 'success',
    body: {
      chat_completions: body,
      infer_requests: [
        {
          id: body.id ?? 'chat-completions-response',
          state: 'success',
          output: { message, ...(Array.isArray(messageObj.tool_calls) ? { tool_calls: messageObj.tool_calls } : {}) },
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

async function postJsonOrSse(cfg: ThetaConfig, url: string, body: Record<string, unknown>, timeoutMs: number): Promise<unknown> {
  for (let attempt = 0; attempt < 1; attempt += 1) {
    const canRetry = false;

    try {
      const res = await fetch(url, {
        redirect: 'error',
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
      } catch {
        const parsedSse = parseSseResponse(text);
        if (parsedSse) return parsedSse;
        return { status: 'success', raw: text };
      }
    } catch (error) {
      if (isStructuredError(error)) throw error;
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

function backoffDelayMs(attempt: number, baseMs: number): number {
  return baseMs * Math.max(1, 2 ** (attempt - 1));
}

const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

function enforceWebhookGate(cfg: ThetaConfig, body: unknown, confirm: unknown): void {
  const hooks = findCallbackFields(body);
  for (const hook of hooks) {
    let url: URL;
    try { url = new URL(String(hook.value)); } catch { throw new Error(`${hook.path} must be an https URL`); }
    if (url.protocol !== 'https:') throw new Error(`${hook.path} must be an https URL`);
  }
  if (hooks.length) assertApproved(cfg, confirm, 'Sending inference results to a webhook');
}

const PREDICTION_NAME = /^[A-Za-z0-9_.-]{1,64}$/;

// Tools are only sent to models that return structured tool calls, unless the caller sets
// allowUnverifiedTools to exactly true (then results carry no tool-call guarantee).
function enforceToolSupport(model: string, body: Record<string, unknown>, allowUnverifiedTools: unknown): void {
  const input = body.input && typeof body.input === 'object' ? body.input as Record<string, unknown> : {};
  const hasTools = ['tools', 'tool_choice', 'functions'].some((k) => body[k] !== undefined || input[k] !== undefined);
  if (hasTools && !TOOL_CALLING_CHAT_SERVICES.includes(model) && allowUnverifiedTools !== true) {
    throw new Error(`Service ${model} does not return structured tool calls. Use glm_5_3 or glm_5_3_flash, or set allowUnverifiedTools:true (exactly) to send anyway.`);
  }
}

export const onDemandApiClient = {
  listServices: (cfg: ThetaConfig) => getJson(`${baseUrl(cfg)}/service/list?expand=template_id`, optionalNet(cfg)),

  createInferRequest: (cfg: ThetaConfig, service: string, payload: Record<string, unknown>, opts?: OnDemandInferOptions) => {
    assertLive(cfg, 'On-demand inference');
    encodePathSegment(service, 'service');
    if (opts?.prediction !== undefined && (typeof opts.prediction !== 'string' || !PREDICTION_NAME.test(opts.prediction))) {
      throw new Error('prediction must be a prediction name string');
    }
    if (opts?.wait !== undefined && !Number.isFinite(Number(opts.wait))) throw new Error('wait must be a number');
    const raw = normalizeInferPayload(snapshotBody(payload));
    const bounded = raw.input && typeof raw.input === 'object' && !Array.isArray(raw.input)
      ? { ...boundChatParams(raw), input: boundChatParams(raw.input as Record<string, unknown>) }
      : boundChatParams(raw);
    // Live 2026-10-03: multi-prediction services (image_to_image) ignore ?prediction= and run
    // their default prediction; the body field is honoured. Send both.
    const finalBody = opts?.prediction && bounded.prediction === undefined ? { ...bounded, prediction: opts.prediction } : bounded;
    // Every check below runs on the exact final body that is serialized and sent.
    if (finalBody.prediction !== undefined && (typeof finalBody.prediction !== 'string' || !PREDICTION_NAME.test(finalBody.prediction))) {
      throw new Error('prediction must be a prediction name string');
    }
    if (inferenceRequiresConfirm(service)) assertApproved(cfg, opts?.confirm, `Inference on ${service} (video, unknown, retired or high-cost service)`);
    enforceWebhookGate(cfg, finalBody, opts?.confirm);
    enforceToolSupport(service, finalBody, opts?.allowUnverifiedTools);
    const timeoutMs = resolveCreateInferTimeoutMs(cfg, service, finalBody);
    return postJsonOrSse(cfg, `${baseUrl(cfg)}${inferPath(service, { wait: opts?.wait, prediction: opts?.prediction })}`, finalBody, timeoutMs);
  },

  createChatCompletionRequest: async (cfg: ThetaConfig, rawBody: OnDemandChatCompletionBody, opts?: { confirm?: boolean; allowUnverifiedTools?: boolean }) => {
    assertLive(cfg, 'On-demand chat completion');
    const snapshot = snapshotBody(rawBody);
    const body = snapshot.input && typeof snapshot.input === 'object' && !Array.isArray(snapshot.input)
      ? { ...boundChatParams(snapshot), input: boundChatParams(snapshot.input as Record<string, unknown>) }
      : boundChatParams(snapshot);
    // Every check below runs on the exact final body that is serialized and sent.
    if (!Array.isArray(body.messages) || !body.messages.length) throw new Error('messages must be a non-empty array');
    const model = String(body.model);
    if (!OPENAI_CHAT_COMPLETION_SERVICES.includes(model) || inferenceRequiresConfirm(model)) {
      assertApproved(cfg, opts?.confirm, `Chat completion on retired or unlisted model ${model}`);
    }
    enforceWebhookGate(cfg, body, opts?.confirm);
    enforceToolSupport(model, body, opts?.allowUnverifiedTools);
    const timeoutMs = Array.isArray(body.messages) && body.stream === false
      ? Math.max(cfg.httpTimeoutMs, 120000)
      : cfg.httpTimeoutMs;
    const result = await postJsonOrSse(cfg, `${baseUrl(cfg)}${chatCompletionsPath()}`, body, timeoutMs);
    if (result && typeof result === 'object' && (result as Record<string, unknown>).body) return result;
    return normalizeChatCompletionsJson(result);
  },

  getInferRequest: (cfg: ThetaConfig, requestId: string) => getJson(`${baseUrl(cfg)}/infer_request/${encodePathSegment(requestId, 'requestId')}`, net(cfg)),

  createInputPresignedUrls: async (cfg: ThetaConfig, service: string, inputFields?: string[]) => {
    assertLive(cfg, 'Presigned upload URL creation');
    return normalizePresignedUrls(await postJson(`${baseUrl(cfg)}/infer_request/${encodePathSegment(service, 'service')}/input_presigned_urls`, inputFields?.length ? { input_fields: inputFields } : {}, net(cfg)));
  }
};

// Live response (2026-10-03): body[field] = {presigned_url, filename}. The legacy npm MCP 0.1.7
// expected body.urls[field].upload_url. Normalise to one shape and state the upload contract.
export const PRESIGNED_UPLOAD_CONTENT_TYPE = 'application/octet-stream';

function normalizePresignedUrls(response: unknown): unknown {
  if (!response || typeof response !== 'object') return response;
  const body = (response as { body?: Record<string, unknown> }).body;
  if (!body || typeof body !== 'object') return response;
  const source = (body.urls && typeof body.urls === 'object' ? body.urls : body) as Record<string, unknown>;
  const uploads: Record<string, { upload_url: string; filename: string }> = {};
  for (const [field, raw] of Object.entries(source)) {
    if (!raw || typeof raw !== 'object') continue;
    const info = raw as Record<string, unknown>;
    const uploadUrl = info.presigned_url ?? info.upload_url;
    if (typeof uploadUrl === 'string' && /^https:\/\//i.test(uploadUrl) && typeof info.filename === 'string') {
      uploads[field] = { upload_url: uploadUrl, filename: info.filename };
    }
  }
  return {
    ...(response as Record<string, unknown>),
    uploads,
    uploadInstructions: `PUT the file bytes to upload_url with header Content-Type: ${PRESIGNED_UPLOAD_CONTENT_TYPE} (any other type fails signature check with 403), then pass filename as the input field value.`
  };
}
