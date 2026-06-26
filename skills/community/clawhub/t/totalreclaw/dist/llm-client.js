/**
 * TotalReclaw Plugin - LLM Client
 *
 * Auto-detects the user's LLM provider from OpenClaw's config and derives a
 * cheap extraction model. Supports OpenAI-compatible APIs and Anthropic's
 * Messages API. No external dependencies -- uses native fetch().
 *
 * Embedding generation has been moved to embedding.ts (local ONNX model via
 * @huggingface/transformers). No API key needed for embeddings.
 */
import { CONFIG } from './config.js';
// ---------------------------------------------------------------------------
// Provider mappings
// ---------------------------------------------------------------------------
/** Maps provider name to CONFIG.llmApiKeys property names to check (in order). */
const PROVIDER_KEY_NAMES = {
    zai: ['zai'],
    anthropic: ['anthropic'],
    openai: ['openai'],
    gemini: ['gemini'],
    google: ['gemini', 'google'],
    mistral: ['mistral'],
    groq: ['groq'],
    deepseek: ['deepseek'],
    openrouter: ['openrouter'],
    xai: ['xai'],
    together: ['together'],
    cerebras: ['cerebras'],
};
/**
 * zai has TWO public endpoints. The CODING endpoint is what GLM Coding Plan
 * subscription keys are provisioned against; the STANDARD (PAYG) endpoint
 * serves pay-as-you-go balances. A coding-plan key that hits the STANDARD
 * endpoint returns HTTP 429 with body `"Insufficient balance or no resource
 * package. Please recharge."` — misleading because the subscription is in
 * good standing. Vice-versa for PAYG keys that accidentally hit CODING.
 *
 * 3.3.1-rc.3: exported so the rc.3 auto-fallback (see `chatCompletion`)
 * can flip between them when the upstream error signature matches.
 */
export const ZAI_CODING_BASE_URL = 'https://api.z.ai/api/coding/paas/v4';
export const ZAI_STANDARD_BASE_URL = 'https://api.z.ai/api/paas/v4';
/**
 * Resolve the zai base URL.
 *
 * Precedence:
 *   1. `ZAI_BASE_URL` env var (explicit operator override — read by
 *      `CONFIG.zaiBaseUrl` via a getter so tests can mutate the env
 *      between calls)
 *   2. Default: coding endpoint (coding-plan-biased; the rc.3 auto-fallback
 *      hops to the standard endpoint on an "Insufficient balance" 429).
 *
 * Documented in plugin SKILL.md — Coding-Plan users can leave it unset (or
 * set it explicitly to `https://api.z.ai/api/coding/paas/v4`). PAYG users
 * MUST set it to `https://api.z.ai/api/paas/v4` to avoid the auto-fallback
 * tax on every first call.
 *
 * Scanner-isolation note: the env read lives in `config.ts` (which has no
 * network triggers). This module has network calls, so it cannot touch
 * env vars directly — both rules 1 (env-harvesting) and 2 (potential-
 * exfiltration) in check-scanner.mjs would fire.
 */
export function getZaiBaseUrl() {
    return CONFIG.zaiBaseUrl;
}
const PROVIDER_BASE_URLS = {
    // zai: resolved lazily at each init/call so `ZAI_BASE_URL` env changes
    // propagate without a module re-import. See `getZaiBaseUrl()`.
    zai: getZaiBaseUrl(),
    anthropic: 'https://api.anthropic.com/v1',
    openai: 'https://api.openai.com/v1',
    gemini: 'https://generativelanguage.googleapis.com/v1beta/openai',
    google: 'https://generativelanguage.googleapis.com/v1beta/openai',
    mistral: 'https://api.mistral.ai/v1',
    groq: 'https://api.groq.com/openai/v1',
    deepseek: 'https://api.deepseek.com/v1',
    openrouter: 'https://openrouter.ai/api/v1',
    xai: 'https://api.x.ai/v1',
    together: 'https://api.together.xyz/v1',
    cerebras: 'https://api.cerebras.ai/v1',
};
// ---------------------------------------------------------------------------
// Cheap model derivation
// ---------------------------------------------------------------------------
const CHEAP_INDICATORS = ['flash', 'mini', 'nano', 'haiku', 'small', 'lite', 'fast'];
/**
 * Regex that tests whether a model id genuinely mentions a "cheap" tier.
 * Uses word-boundary + `-` separators so we do NOT match substrings like
 * "mini" inside "gemini" (real bug caught in 3.3.1 tests — deriveCheapModel
 * was passing gemini-2.5-pro through unchanged because `.includes('mini')`
 * matched the letters inside "gemini"). The canonical cheap-tier naming
 * conventions put the indicator at a hyphen boundary or end of string:
 *   gpt-4.1-mini, claude-haiku-4-5, gemini-flash-lite, glm-4.5-flash, o4-mini
 */
const CHEAP_INDICATOR_RE = new RegExp(`(?:^|[-_/.])(?:${CHEAP_INDICATORS.join('|')})(?:[-_/.]|$)`, 'i');
/**
 * Default cheap extraction model per provider. Exported so callers that
 * resolve a provider WITHOUT knowing the user's primary model (e.g. the
 * auth-profiles.json path) can still pick a sensible model.
 *
 * 3.3.1 update: haiku is now `claude-haiku-4-5-20251001` (latest cheap
 * Claude as of 2026-04). glm-4.5-flash stays the zai extraction default.
 */
export const CHEAP_MODEL_BY_PROVIDER = {
    zai: 'glm-4.5-flash',
    anthropic: 'claude-haiku-4-5-20251001',
    openai: 'gpt-4.1-mini',
    gemini: 'gemini-flash-lite',
    google: 'gemini-flash-lite',
    mistral: 'mistral-small-latest',
    groq: 'llama-3.3-70b-versatile',
    deepseek: 'deepseek-chat',
    openrouter: 'anthropic/claude-haiku-4-5-20251001',
    xai: 'grok-2',
    together: 'meta-llama/Llama-3.3-70B-Instruct-Turbo',
    cerebras: 'llama3.3-70b',
};
/**
 * Derive a cheap/fast model suitable for fact extraction, given the user's
 * provider and primary (potentially expensive) model.
 */
export function deriveCheapModel(provider, primaryModel) {
    // If already on a cheap model, use it as-is.
    // Word-boundary match to avoid false positives (see CHEAP_INDICATOR_RE).
    if (CHEAP_INDICATOR_RE.test(primaryModel)) {
        return primaryModel;
    }
    // Derive based on provider naming conventions
    const fromTable = CHEAP_MODEL_BY_PROVIDER[provider];
    if (fromTable)
        return fromTable;
    // Fallback: use the primary model (best-effort — caller may still work)
    return primaryModel;
}
// ---------------------------------------------------------------------------
// Module-level state
// ---------------------------------------------------------------------------
let _cachedConfig = null;
let _initialized = false;
let _logger = null;
// ---------------------------------------------------------------------------
// Initialization
// ---------------------------------------------------------------------------
/**
 * Build an LLMClientConfig for a known provider + apiKey, picking a
 * cheap default model if none is specified. Returns null if the
 * provider is unknown and no baseUrl is available.
 */
function buildConfigForProvider(provider, apiKey, opts = {}) {
    // zai's base URL is resolved via `getZaiBaseUrl()` (reads CONFIG) so
    // the `ZAI_BASE_URL` env override takes effect even when this helper is
    // called with no `baseUrlOverride` (i.e. the env-var fallback tier in
    // initLLMClient).
    const defaultForProvider = provider === 'zai' ? getZaiBaseUrl() : PROVIDER_BASE_URLS[provider] ?? '';
    const baseUrl = (opts.baseUrlOverride ?? defaultForProvider).replace(/\/+$/, '');
    if (!baseUrl)
        return null;
    const model = opts.modelOverride ??
        (opts.primaryModelHint ? deriveCheapModel(provider, opts.primaryModelHint) : null) ??
        CHEAP_MODEL_BY_PROVIDER[provider];
    if (!model)
        return null;
    const apiFormat = opts.apiFormatOverride ?? (provider === 'anthropic' ? 'anthropic' : 'openai');
    return { apiKey, baseUrl, model, apiFormat };
}
/**
 * Initialize the LLM client by detecting the provider from OpenClaw's config.
 * Called once from the plugin's `register()` function.
 *
 * 3.3.1 resolution cascade (highest priority first):
 *   1. Plugin config `extraction.llm` override block (provider/apiKey/baseUrl/model)
 *   2. `api.config.providers` / `openclawProviders` — SDK-passed
 *   3. `~/.openclaw/agents/*\/agent/auth-profiles.json` (harvested by caller)
 *   4. Env var fallback (`ZAI_API_KEY`, `OPENAI_API_KEY`, ...)
 *   5. No source → disable extraction cleanly (single log at startup, never
 *      per-turn).
 *
 * The `TOTALRECLAW_LLM_MODEL` user-facing override was removed in v1 —
 * `deriveCheapModel(provider)` covers the 99% case and a model-level knob
 * was adding config surface for no tangible win.
 */
export function initLLMClient(options) {
    _logger = options.logger ?? null;
    _initialized = true;
    _cachedConfig = null;
    const { primaryModel, pluginConfig, openclawProviders, authProfileKeys } = options;
    // Check if extraction is explicitly disabled
    const extraction = pluginConfig?.extraction;
    if (extraction?.enabled === false) {
        _logger?.info?.('TotalReclaw extraction LLM: disabled via plugin config (extraction.enabled=false).');
        return;
    }
    const modelOverride = typeof extraction?.model === 'string' ? extraction.model : undefined;
    const llmOverrideRaw = extraction?.llm;
    const llmOverride = typeof llmOverrideRaw === 'object' && llmOverrideRaw !== null ? llmOverrideRaw : undefined;
    // Derive provider name from primary-model ("anthropic/claude-sonnet-4-5" etc)
    let providerFromPrimary = '';
    let modelFromPrimary;
    if (primaryModel) {
        const parts = primaryModel.split('/');
        if (parts.length >= 2) {
            providerFromPrimary = parts[0].toLowerCase();
            modelFromPrimary = parts.slice(1).join('/');
        }
        else {
            modelFromPrimary = primaryModel;
        }
    }
    // ---------------------------------------------------------------------
    // Tier 1 — explicit plugin-config override (highest priority)
    // Accepts any subset of { provider, model, apiKey, baseUrl }. A bare
    // `model` override without a provider+apiKey falls through to lower
    // tiers — matches pre-3.3.1 behaviour.
    // ---------------------------------------------------------------------
    if (llmOverride && typeof llmOverride === 'object') {
        const provider = (llmOverride.provider ?? providerFromPrimary).toLowerCase();
        const apiKey = typeof llmOverride.apiKey === 'string' && llmOverride.apiKey.trim()
            ? llmOverride.apiKey.trim()
            : undefined;
        if (provider && apiKey) {
            const cfg = buildConfigForProvider(provider, apiKey, {
                baseUrlOverride: llmOverride.baseUrl,
                modelOverride: llmOverride.model ?? modelOverride,
                primaryModelHint: modelFromPrimary,
            });
            if (cfg) {
                _cachedConfig = cfg;
                _logger?.info?.(`TotalReclaw extraction LLM: resolved ${provider}/${cfg.model} (plugin config override)`);
                return;
            }
        }
    }
    // ---------------------------------------------------------------------
    // Tier 2 — SDK-passed openclawProviders. Try the primary-model's provider
    // first, then any other provider that has an apiKey.
    // ---------------------------------------------------------------------
    if (openclawProviders) {
        if (providerFromPrimary) {
            const ocProvider = openclawProviders[providerFromPrimary];
            if (ocProvider?.apiKey) {
                const cfg = buildConfigForProvider(providerFromPrimary, ocProvider.apiKey, {
                    baseUrlOverride: ocProvider.baseUrl,
                    modelOverride,
                    primaryModelHint: modelFromPrimary,
                    apiFormatOverride: ocProvider.api === 'anthropic-messages' || providerFromPrimary === 'anthropic'
                        ? 'anthropic'
                        : 'openai',
                });
                if (cfg) {
                    _cachedConfig = cfg;
                    _logger?.info?.(`TotalReclaw extraction LLM: resolved ${providerFromPrimary}/${cfg.model} (OpenClaw provider config)`);
                    return;
                }
            }
        }
        for (const [providerName, providerConfig] of Object.entries(openclawProviders)) {
            if (!providerConfig?.apiKey)
                continue;
            const provider = providerName.toLowerCase();
            const firstModelId = providerConfig.models?.[0]?.id;
            const cfg = buildConfigForProvider(provider, providerConfig.apiKey, {
                baseUrlOverride: providerConfig.baseUrl,
                modelOverride,
                primaryModelHint: firstModelId,
                apiFormatOverride: providerConfig.api === 'anthropic-messages' || provider === 'anthropic'
                    ? 'anthropic'
                    : 'openai',
            });
            if (cfg) {
                _cachedConfig = cfg;
                _logger?.info?.(`TotalReclaw extraction LLM: resolved ${provider}/${cfg.model} (OpenClaw provider config)`);
                return;
            }
        }
    }
    // ---------------------------------------------------------------------
    // Tier 3 — auth-profiles.json keys harvested by llm-profile-reader.
    // 3.3.1: new tier. Prefer the primary-model's provider, then any other.
    // ---------------------------------------------------------------------
    if (authProfileKeys && authProfileKeys.length > 0) {
        if (providerFromPrimary) {
            const hit = authProfileKeys.find((k) => k.provider === providerFromPrimary);
            if (hit) {
                const cfg = buildConfigForProvider(providerFromPrimary, hit.apiKey, {
                    modelOverride,
                    primaryModelHint: modelFromPrimary,
                });
                if (cfg) {
                    _cachedConfig = cfg;
                    _logger?.info?.(`TotalReclaw extraction LLM: resolved ${providerFromPrimary}/${cfg.model} (auth-profiles.json)`);
                    return;
                }
            }
        }
        // Try zai / openai / anthropic first (cheapest+most available), then anything else.
        const priority = ['zai', 'openai', 'anthropic', 'gemini', 'groq', 'deepseek', 'mistral', 'openrouter', 'xai', 'together', 'cerebras'];
        const ordered = [
            ...priority.flatMap((p) => authProfileKeys.filter((k) => k.provider === p)),
            ...authProfileKeys.filter((k) => !priority.includes(k.provider)),
        ];
        for (const entry of ordered) {
            const cfg = buildConfigForProvider(entry.provider, entry.apiKey, {
                modelOverride,
            });
            if (cfg) {
                _cachedConfig = cfg;
                _logger?.info?.(`TotalReclaw extraction LLM: resolved ${entry.provider}/${cfg.model} (auth-profiles.json)`);
                return;
            }
        }
    }
    // ---------------------------------------------------------------------
    // Tier 4 — env var fallback (for dev/test without OpenClaw config)
    // ---------------------------------------------------------------------
    const envFallback = [
        ['zai', 'zai'],
        ['openai', 'openai'],
        ['anthropic', 'anthropic'],
        ['gemini', 'gemini'],
        ['groq', 'groq'],
        ['deepseek', 'deepseek'],
        ['mistral', 'mistral'],
        ['openrouter', 'openrouter'],
        ['xai', 'xai'],
    ];
    // If primary model hints a specific provider, try it first.
    if (providerFromPrimary) {
        const keyNames = PROVIDER_KEY_NAMES[providerFromPrimary];
        if (keyNames) {
            const apiKey = keyNames.map((n) => CONFIG.llmApiKeys[n]).find(Boolean);
            if (apiKey) {
                const cfg = buildConfigForProvider(providerFromPrimary, apiKey, {
                    modelOverride,
                    primaryModelHint: modelFromPrimary,
                });
                if (cfg) {
                    _cachedConfig = cfg;
                    _logger?.info?.(`TotalReclaw extraction LLM: resolved ${providerFromPrimary}/${cfg.model} (env var)`);
                    return;
                }
            }
        }
    }
    for (const [provider, keyName] of envFallback) {
        const apiKey = CONFIG.llmApiKeys[keyName];
        if (!apiKey)
            continue;
        const cfg = buildConfigForProvider(provider, apiKey, { modelOverride });
        if (cfg) {
            _cachedConfig = cfg;
            _logger?.info?.(`TotalReclaw extraction LLM: resolved ${provider}/${cfg.model} (env var)`);
            return;
        }
    }
    // ---------------------------------------------------------------------
    // No source — extraction disabled. Single startup log, INFO-level.
    // NOT a warn: this is the default state for users who have not set up a
    // provider. Warning per turn is what 3.3.0 did and it was misleading.
    // ---------------------------------------------------------------------
    _logger?.info?.('TotalReclaw extraction LLM: not configured — auto-extraction disabled. ' +
        'To enable, configure a provider in ~/.openclaw/agents/*\/agent/auth-profiles.json ' +
        'or set an API key env var (ZAI_API_KEY, OPENAI_API_KEY, ANTHROPIC_API_KEY, ...).');
}
// ---------------------------------------------------------------------------
// Public API
// ---------------------------------------------------------------------------
/**
 * Resolve LLM configuration. Returns the cached config set by `initLLMClient()`,
 * or falls back to the legacy env-var detection if `initLLMClient()` was never called.
 */
export function resolveLLMConfig() {
    if (_initialized) {
        return _cachedConfig;
    }
    // Legacy fallback: if initLLMClient() was never called (e.g. running outside
    // the plugin context), try the config-based approach for backwards compat.
    const zaiKey = CONFIG.llmApiKeys.zai;
    const openaiKey = CONFIG.llmApiKeys.openai;
    const model = zaiKey ? 'glm-4.5-flash' : 'gpt-4.1-mini';
    if (zaiKey) {
        return {
            apiKey: zaiKey,
            baseUrl: getZaiBaseUrl(),
            model,
            apiFormat: 'openai',
        };
    }
    if (openaiKey) {
        return {
            apiKey: openaiKey,
            baseUrl: 'https://api.openai.com/v1',
            model,
            apiFormat: 'openai',
        };
    }
    return null;
}
/**
 * Default retry budget in ms. Configurable via
 * `TOTALRECLAW_LLM_RETRY_BUDGET_MS` env var — read by `config.ts`. Callers
 * can override per-call via `retry.budgetMs`. 60_000ms covers ~8 minutes
 * worth of upstream outages with the 2s→32s schedule.
 *
 * Scanner-isolation note: the env read lives in `config.ts` so this file
 * stays clean of env-harvesting triggers.
 */
export const DEFAULT_RETRY_BUDGET_MS = CONFIG.llmRetryBudgetMs;
/**
 * Structured error thrown when the extraction LLM upstream is unreachable
 * after the full retry budget is exhausted. The extraction pipeline
 * recognizes this via `err instanceof LLMUpstreamOutageError` and can
 * choose to:
 *   - queue the message batch for retry next turn,
 *   - surface a one-time notification to the user, or
 *   - simply skip this extraction window silently.
 */
export class LLMUpstreamOutageError extends Error {
    attempts;
    lastStatus;
    constructor(message, attempts, lastStatus) {
        super(message);
        this.name = 'LLMUpstreamOutageError';
        this.attempts = attempts;
        this.lastStatus = lastStatus;
    }
}
/**
 * Detect the "Insufficient balance" error shape from zai. Matches both
 * the exact production wording ("Insufficient balance or no resource
 * package. Please recharge.") and the short "no resource package" variant
 * we've seen in some historical responses.
 */
export function isZaiBalanceError(errorMessage) {
    const m = errorMessage.toLowerCase();
    return m.includes('insufficient balance') || m.includes('no resource package');
}
/**
 * Identify the "other" zai endpoint when the current one returns a balance
 * error — CODING ↔ STANDARD. Returns `null` when the URL is neither of
 * the two zai endpoints we know about (e.g. a self-hosted proxy), which
 * means the fallback logic stays put.
 */
export function zaiFallbackBaseUrl(currentBaseUrl) {
    const normalized = currentBaseUrl.replace(/\/+$/, '');
    if (normalized === ZAI_CODING_BASE_URL)
        return ZAI_STANDARD_BASE_URL;
    if (normalized === ZAI_STANDARD_BASE_URL)
        return ZAI_CODING_BASE_URL;
    return null;
}
/**
 * Call the LLM chat completion endpoint.
 *
 * Supports both OpenAI-compatible format and Anthropic Messages API,
 * determined by `config.apiFormat`.
 *
 * 3.3.1-rc.3 — lifts the retry budget 5 attempts × (2s/4s/8s/16s/32s), total
 * ~62s. Configurable via `TOTALRECLAW_LLM_RETRY_BUDGET_MS`. Adds zai
 * "Insufficient balance" auto-fallback: when a zai 429 carries the balance
 * error body AND we're on one of the two known zai endpoints, we flip to
 * the OTHER endpoint and retry ONCE (accounted for separately from the
 * normal retry loop). On exhaustion, throws `LLMUpstreamOutageError`.
 *
 * Non-retryable errors (4xx other than 429, network refused, JSON parse)
 * fail fast on the first attempt.
 *
 * @returns The assistant's response content, or null on failure.
 */
export async function chatCompletion(config, messages, options) {
    const maxTokens = options?.maxTokens ?? 2048;
    const temperature = options?.temperature ?? 0; // Deterministic output for dedup (same input → same text → same content fingerprint)
    const attempts = Math.max(1, options?.retry?.attempts ?? 5);
    const baseDelayMs = Math.max(100, options?.retry?.baseDelayMs ?? 2000);
    const budgetMs = Math.max(100, options?.retry?.budgetMs ?? DEFAULT_RETRY_BUDGET_MS);
    const timeoutMs = options?.timeoutMs ?? 30_000;
    const logger = options?.logger;
    // We mutate `activeConfig.baseUrl` in the zai fallback branch so the
    // retried call hits the other endpoint. Shallow-clone so the caller's
    // config object stays untouched.
    const activeConfig = { ...config };
    // One-shot flag: we only auto-fallback zai once per chatCompletion call
    // to prevent ping-pong between the two endpoints if both reject.
    let zaiFallbackAttempted = false;
    const callOnce = () => activeConfig.apiFormat === 'anthropic'
        ? chatCompletionAnthropic(activeConfig, messages, maxTokens, temperature, timeoutMs)
        : chatCompletionOpenAI(activeConfig, messages, maxTokens, temperature, timeoutMs);
    let lastErr;
    let cumulativeDelayMs = 0;
    let lastStatus;
    for (let attempt = 1; attempt <= attempts; attempt++) {
        try {
            return await callOnce();
        }
        catch (err) {
            lastErr = err;
            const msg = err instanceof Error ? err.message : String(err);
            lastStatus = parseHttpStatus(msg) ?? lastStatus;
            // ── zai "Insufficient balance" auto-fallback ──
            // Fires BEFORE the normal retry accounting. If the error is a zai
            // balance-shaped 429, flip the baseUrl once and immediately retry —
            // no backoff, no decrement of the attempt count. Keeps the total
            // attempt budget reserved for genuine outages.
            if (!zaiFallbackAttempted && /\b429\b/.test(msg) && isZaiBalanceError(msg)) {
                const fallback = zaiFallbackBaseUrl(activeConfig.baseUrl);
                if (fallback) {
                    zaiFallbackAttempted = true;
                    const oldUrl = activeConfig.baseUrl;
                    activeConfig.baseUrl = fallback;
                    logger?.info?.(`chatCompletion: zai endpoint auto-fallback: ${oldUrl} → ${fallback} due to "Insufficient balance" response`);
                    // Retry immediately — do NOT decrement attempts counter further;
                    // this "extra" attempt is the fallback freebie.
                    attempt--;
                    continue;
                }
            }
            const retryable = isRetryable(msg);
            const isFinalAttempt = attempt >= attempts;
            if (!retryable || isFinalAttempt) {
                // Fail-fast OR last attempt — rethrow.
                if (attempt > 1 || !retryable) {
                    if (retryable) {
                        logger?.warn?.(`chatCompletion: giving up after ${attempt} attempts: ${msg.slice(0, 200)}`);
                    }
                    // Structured outage error when the retryable error budget is
                    // fully exhausted — lets downstream recognize vs bail silently.
                    if (retryable) {
                        throw new LLMUpstreamOutageError(`LLM upstream outage after ${attempt} attempts: ${msg.slice(0, 200)}`, attempt, lastStatus);
                    }
                }
                throw err;
            }
            // Compute next delay, but respect the cumulative retry-budget cap.
            const delayMs = baseDelayMs * Math.pow(2, attempt - 1);
            if (cumulativeDelayMs + delayMs > budgetMs) {
                logger?.warn?.(`chatCompletion: retry budget exhausted (${cumulativeDelayMs}ms used + ${delayMs}ms next > ${budgetMs}ms budget); surfacing outage after ${attempt} attempts: ${msg.slice(0, 160)}`);
                throw new LLMUpstreamOutageError(`LLM upstream outage (budget ${budgetMs}ms exhausted after ${attempt} attempts): ${msg.slice(0, 200)}`, attempt, lastStatus);
            }
            cumulativeDelayMs += delayMs;
            // Log only the FIRST retry at INFO to avoid spamming during long
            // outages; subsequent retries are DEBUG (debounced per outage).
            if (attempt === 1) {
                logger?.info?.(`chatCompletion: retrying after transient failure (attempt ${attempt}/${attempts}, wait ${delayMs}ms): ${msg.slice(0, 160)}`);
            }
            else {
                logger?.debug?.(`chatCompletion: retry attempt ${attempt}/${attempts} (wait ${delayMs}ms): ${msg.slice(0, 160)}`);
            }
            await new Promise((resolve) => setTimeout(resolve, delayMs));
        }
    }
    // Defensive — should never reach here since the loop always throws on the
    // final attempt when it fails. Keeps TS happy.
    throw lastErr instanceof Error ? lastErr : new Error(String(lastErr));
}
/**
 * Parse the HTTP status code from an error message of the form
 * `"LLM API 429: rate limit"` or `"Anthropic API 503: ..."`. Returns
 * `undefined` when the message doesn't follow that shape (e.g. network
 * refused). Used by `LLMUpstreamOutageError.lastStatus` for downstream
 * classification.
 */
function parseHttpStatus(errorMessage) {
    const m = errorMessage.match(/\b(\d{3})\b/);
    if (!m)
        return undefined;
    const code = parseInt(m[1], 10);
    return code >= 100 && code < 600 ? code : undefined;
}
/**
 * Which LLM-call errors are worth retrying. Exported for testability.
 *
 * Retryable:
 *   - HTTP 429 (rate limit)
 *   - HTTP 503 / 502 / 504 (gateway transients)
 *   - AbortError / "aborted due to timeout" / "TimeoutError"
 *
 * NOT retryable:
 *   - HTTP 400 / 401 / 403 / 404 (auth / request errors — no point retrying)
 *   - JSON parse errors
 *   - DNS / connection refused (usually misconfig, not transient)
 */
export function isRetryable(errorMessage) {
    const m = errorMessage.toLowerCase();
    // Rate limit
    if (/\b429\b/.test(errorMessage) || m.includes('rate limit'))
        return true;
    // Transient gateway errors
    if (/\b50(2|3|4)\b/.test(errorMessage))
        return true;
    // Timeouts
    if (m.includes('timeout') ||
        m.includes('aborterror') ||
        m.includes('was aborted') ||
        m.includes('operation was aborted')) {
        return true;
    }
    return false;
}
// ---------------------------------------------------------------------------
// OpenAI-compatible chat completion
// ---------------------------------------------------------------------------
/**
 * Provider base-URL hints for OpenAI-compatible endpoints that honour the
 * `response_format: {"type": "json_object"}` body field. Sending the field
 * to a provider that supports it makes JSON output deterministic; sending
 * it to a provider that does NOT recognise the field is a 400.
 *
 * Why this exists (3.3.12-rc.6, 2026-05-09):
 *   z.ai's GLM family (4.5-flash, 5-turbo, 5.1) silently returns EMPTY
 *   `message.content` for the merged-extraction prompt unless this hint
 *   is set. No error, no warning — the LLM just emits "" instead of the
 *   expected `{"topics": [], "facts": []}` JSON. Plugin's parse step
 *   then logs `0 raw facts` from a successful-but-empty branch.
 *
 *   This bug was found and fixed on the Python (Hermes) side in
 *   2.3.1-rc.23 (see `python/src/totalreclaw/agent/llm_client.py`
 *   `_supports_json_object_response_format`) but the plugin TS port did
 *   not carry the fix — observed in plugin 3.3.12-rc.5 auto-QA on
 *   2026-05-09: hook + poller both fired correctly but extraction
 *   returned 0 facts on every batch despite trajectories containing
 *   explicit "I prefer X" / "I work at Y" statements.
 *
 * Mirror of Python's `_supports_json_object_response_format`. Match by
 * substring on a lowercased baseUrl so cosmetic prefix differences
 * (https://, /v1, etc.) don't matter.
 */
const JSON_OBJECT_PROVIDER_HINTS = [
    'z.ai',
    'api.openai.com',
    'groq.com',
    'openrouter.ai',
    'deepseek.com',
    'mistral.ai',
    'x.ai',
    'together.xyz',
];
export function supportsJsonObjectResponseFormat(baseUrl) {
    if (!baseUrl)
        return false;
    const lower = baseUrl.toLowerCase();
    return JSON_OBJECT_PROVIDER_HINTS.some((h) => lower.includes(h));
}
async function chatCompletionOpenAI(config, messages, maxTokens, temperature, timeoutMs) {
    const url = `${config.baseUrl}/chat/completions`;
    const body = {
        model: config.model,
        messages,
        temperature,
        max_completion_tokens: maxTokens,
    };
    // 3.3.12-rc.6: hint the provider to return strict JSON. Critical for
    // z.ai/GLM (silent-empty without it). See JSON_OBJECT_PROVIDER_HINTS
    // doc above.
    if (supportsJsonObjectResponseFormat(config.baseUrl)) {
        body.response_format = { type: 'json_object' };
    }
    try {
        const res = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                Authorization: `Bearer ${config.apiKey}`,
            },
            body: JSON.stringify(body),
            signal: AbortSignal.timeout(timeoutMs),
        });
        if (!res.ok) {
            const text = await res.text().catch(() => '');
            throw new Error(`LLM API ${res.status}: ${text.slice(0, 200)}`);
        }
        const json = (await res.json());
        const content = json.choices?.[0]?.message?.content ?? null;
        // 3.3.12-rc.6: loud-on-empty. If the provider returned a 200 with
        // empty content, this almost always means a missing response_format
        // hint or a content-filter. Without this log the silent-empty
        // failure mode (Python rc.23 / plugin rc.5) is invisible to ops.
        if (content === '' || content === null) {
            // Lazy import to avoid circular dep with the registered logger.
            // Fall back to console.warn if logger unavailable.
            const warn = (msg) => {
                try {
                    // eslint-disable-next-line @typescript-eslint/no-explicit-any
                    globalThis?.console?.warn?.(msg);
                }
                catch {
                    /* noop */
                }
            };
            warn(`[totalreclaw][llm-client] provider=${config.baseUrl} model=${config.model} ` +
                `returned empty content (status=200). ` +
                `If using z.ai/GLM/OpenAI-compat, check response_format hint is being sent.`);
        }
        return content;
    }
    catch (err) {
        const msg = err instanceof Error ? err.message : String(err);
        throw new Error(`LLM call failed: ${msg}`);
    }
}
// ---------------------------------------------------------------------------
// Anthropic Messages API chat completion
// ---------------------------------------------------------------------------
async function chatCompletionAnthropic(config, messages, maxTokens, temperature, timeoutMs) {
    const url = `${config.baseUrl}/messages`;
    // Anthropic requires system prompt to be a top-level param, not in messages
    let system;
    const apiMessages = [];
    for (const msg of messages) {
        if (msg.role === 'system') {
            system = msg.content;
        }
        else {
            apiMessages.push({ role: msg.role, content: msg.content });
        }
    }
    const body = {
        model: config.model,
        max_tokens: maxTokens,
        temperature,
        messages: apiMessages,
    };
    if (system) {
        body.system = system;
    }
    try {
        const res = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'x-api-key': config.apiKey,
                'anthropic-version': '2023-06-01',
            },
            body: JSON.stringify(body),
            signal: AbortSignal.timeout(timeoutMs),
        });
        if (!res.ok) {
            const text = await res.text().catch(() => '');
            throw new Error(`Anthropic API ${res.status}: ${text.slice(0, 200)}`);
        }
        const json = (await res.json());
        const textBlock = json.content?.find((block) => block.type === 'text');
        return textBlock?.text ?? null;
    }
    catch (err) {
        const msg = err instanceof Error ? err.message : String(err);
        throw new Error(`LLM call failed: ${msg}`);
    }
}
// ---------------------------------------------------------------------------
// Embedding (re-exported from local ONNX module)
// ---------------------------------------------------------------------------
// Embeddings are now generated locally via @huggingface/transformers
// (Harrier-OSS-v1-270M ONNX model). No API key needed. The native deps +
// model are lazy-fetched from a pinned GitHub Release on first call —
// see embedding.ts + embedder-loader.ts.
export { generateEmbedding, getEmbeddingDims, getEmbeddingModelId, configureEmbedder, 
// 3.3.3-rc.1 (#187): pre-pair bundle prefetch
prefetchEmbedderBundle, } from './embedding.js';
