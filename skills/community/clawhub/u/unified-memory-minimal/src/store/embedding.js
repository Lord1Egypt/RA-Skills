/**
 * Embedding Service - Migrated from memory-tencentdb
 * 
 * Supports two providers:
 * - "openai": OpenAI-compatible embedding APIs (OpenAI, Azure OpenAI, self-hosted)
 * - "local": node-llama-cpp with embeddinggemma-300m GGUF model (fully offline)
 * 
 * Design:
 * - Single `embed()` for one text, `embedBatch()` for multiple.
 * - `getDimensions()` returns configured vector dimensions.
 * - Throws on failure; callers decide fallback strategy.
 */

// ============================
// Types (JSDoc for documentation)
// ============================

/**
 * @typedef {Object} OpenAIEmbeddingConfig
 * @property {string} provider - Provider identifier (any value other than "local")
 * @property {string} baseUrl - API base URL (required)
 * @property {string} apiKey - API Key (required)
 * @property {string} model - Model name (required)
 * @property {number} dimensions - Output dimensions (required)
 */

/**
 * @typedef {Object} LocalEmbeddingConfig
 * @property {"local"} provider - Must be "local"
 * @property {string} [modelPath] - Custom GGUF model path
 * @property {string} [modelCacheDir] - Model cache directory
 */

/**
 * @typedef {OpenAIEmbeddingConfig | LocalEmbeddingConfig} EmbeddingConfig
 */

/**
 * @typedef {Object} EmbeddingProviderInfo
 * @property {string} provider - Provider identifier
 * @property {string} model - Model identifier
 */

/**
 * @typedef {Object} EmbeddingService
 * @property {(text: string) => Promise<Float32Array>} embed
 * @property {(texts: string[]) => Promise<Float32Array[]>} embedBatch
 * @property {() => number} getDimensions
 * @property {() => EmbeddingProviderInfo} getProviderInfo
 * @property {() => boolean} isReady
 * @property {() => void} startWarmup
 * @property {() => void | Promise<void>} [close]
 */

// ============================
// Logger interface
// ============================

/** @type {string} */
const TAG = "[memory-unified][embedding]";

// ============================
// Shared helpers
// ============================

/**
 * Sanitize NaN/Inf values and L2-normalize the vector.
 */
function sanitizeAndNormalize(vec) {
  const arr = Array.from(vec).map((v) => (Number.isFinite(v) ? v : 0));
  const magnitude = Math.sqrt(arr.reduce((sum, v) => sum + v * v, 0));
  if (magnitude < 1e-10) {
    return new Float32Array(arr);
  }
  return new Float32Array(arr.map((v) => v / magnitude));
}

// ============================
// Local (node-llama-cpp) implementation
// ============================

/** Default model: Google's embeddinggemma-300m, quantized Q8_0 (~300MB) */
const DEFAULT_LOCAL_MODEL = "hf:ggml-org/embeddinggemma-300m-qat-q8_0-GGUF/embeddinggemma-300m-qat-Q8_0.gguf";

/** embeddinggemma-300m outputs 768-dimensional vectors */
const LOCAL_DIMENSIONS = 768;

/**
 * embeddinggemma-300m has a 256-token context window.
 * We use 512 chars as a conservative universal limit.
 */
const LOCAL_MAX_INPUT_CHARS = 512;

/**
 * Error thrown when embed() / embedBatch() is called before the local
 * embedding model has finished downloading and loading.
 */
export class EmbeddingNotReadyError extends Error {
  constructor(message) {
    super(message ?? "Local embedding model is not ready yet (still downloading or loading)");
    this.name = "EmbeddingNotReadyError";
  }
}

/**
 * Initialization state for LocalEmbeddingService.
 * @typedef {"idle" | "initializing" | "ready" | "failed"} LocalInitState
 */

export class LocalEmbeddingService {
  /**
   * @param {LocalEmbeddingConfig} [config]
   * @param {Object} [logger]
   */
  constructor(config, logger) {
    this.modelPath = config?.modelPath?.trim() || DEFAULT_LOCAL_MODEL;
    this.modelCacheDir = config?.modelCacheDir?.trim();
    this.logger = logger;

    /** @type {LocalInitState} */
    this.initState = "idle";
    this.initPromise = null;
    this.initError = null;
    this.embeddingContext = null;
  }

  getDimensions() {
    return LOCAL_DIMENSIONS;
  }

  getProviderInfo() {
    return { provider: "local", model: this.modelPath };
  }

  isReady() {
    return this.initState === "ready" && this.embeddingContext !== null;
  }

  startWarmup() {
    if (this.initState === "initializing" || this.initState === "ready") {
      return;
    }
    this.logger?.info(`${TAG} Starting background warmup for local embedding model...`);
    this.initState = "initializing";
    this.initError = null;

    this.initPromise = this._doInitialize()
      .then(() => {
        this.initState = "ready";
        this.logger?.info(`${TAG} Background warmup complete — local embedding ready`);
      })
      .catch((err) => {
        this.initState = "failed";
        this.initError = err instanceof Error ? err : new Error(String(err));
        this.logger?.error(
          `${TAG} Background warmup failed: ${this.initError.message}. ` +
          `embed() calls will throw EmbeddingNotReadyError until retried.`,
        );
      });
  }

  async embed(text) {
    this.assertReady();
    const truncated = this.truncateInput(text);
    const embedding = await this.embeddingContext.getEmbeddingFor(truncated);
    return sanitizeAndNormalize(embedding.vector);
  }

  async embedBatch(texts) {
    if (texts.length === 0) return [];
    this.assertReady();

    const results = [];
    for (const text of texts) {
      const truncated = this.truncateInput(text);
      const embedding = await this.embeddingContext.getEmbeddingFor(truncated);
      results.push(sanitizeAndNormalize(embedding.vector));
    }
    return results;
  }

  close() {
    if (this.embeddingContext) {
      try {
        const ctx = this.embeddingContext;
        ctx.dispose?.();
      } catch {
        // best-effort cleanup
      }
      this.embeddingContext = null;
      this.initPromise = null;
      this.initState = "idle";
      this.initError = null;
      this.logger?.info(`${TAG} Local embedding resources released`);
    }
  }

  assertReady() {
    if (this.initState === "ready" && this.embeddingContext) {
      return;
    }
    if (this.initState === "failed") {
      throw new EmbeddingNotReadyError(
        `Local embedding model initialization failed: ${this.initError?.message ?? "unknown error"}. ` +
        `Call startWarmup() to retry.`,
      );
    }
    if (this.initState === "initializing") {
      throw new EmbeddingNotReadyError(
        "Local embedding model is still loading (download/initialization in progress). Please try again later.",
      );
    }
    throw new EmbeddingNotReadyError(
      "Local embedding model warmup has not been started. Call startWarmup() first.",
    );
  }

  truncateInput(text) {
    if (text.length <= LOCAL_MAX_INPUT_CHARS) return text;
    return text.slice(0, LOCAL_MAX_INPUT_CHARS);
  }

  async _doInitialize() {
    /** @type {Object} */
    let model;
    try {
      this.logger?.debug?.(`${TAG} Loading node-llama-cpp for local embedding...`);

      const { getLlama, resolveModelFile, LlamaLogLevel } = await import("node-llama-cpp");

      const llama = await getLlama({ logLevel: LlamaLogLevel.error });
      this.logger?.debug?.(`${TAG} Llama instance created`);

      const resolvedPath = await resolveModelFile(
        this.modelPath,
        this.modelCacheDir || undefined,
      );
      this.logger?.debug?.(`${TAG} Model resolved: ${resolvedPath}`);

      model = await llama.loadModel({ modelPath: resolvedPath });
      this.logger?.debug?.(`${TAG} Model loaded, creating embedding context...`);

      this.embeddingContext = await model.createEmbeddingContext();
      this.logger?.info(`${TAG} Local embedding ready (model=${this.modelPath}, dims=${LOCAL_DIMENSIONS})`);
    } catch (err) {
      if (model?.dispose) {
        try { model.dispose(); } catch { /* best-effort */ }
      }
      this.embeddingContext = null;
      throw err;
    }
  }

  async waitForReady() {
    if (this.initPromise) {
      await this.initPromise;
    }
  }
}

// ============================
// OpenAI-compatible implementation
// ============================

/** Max texts per batch */
const MAX_BATCH_SIZE = 256;

/** Max retries for API calls */
const MAX_RETRIES = 2;

/** Timeout per API call in milliseconds */
const API_TIMEOUT_MS = 90_000;

/**
 * Custom error class for embedding API errors that carries HTTP status code.
 */
export class EmbeddingApiError extends Error {
  /** @param {string} message @param {number} httpStatus */
  constructor(message, httpStatus) {
    super(message);
    this.name = "EmbeddingApiError";
    this.httpStatus = httpStatus;
  }

  isClientError() {
    return this.httpStatus >= 400 && this.httpStatus < 500 && this.httpStatus !== 429;
  }
}

/**
 * @typedef {Object} OpenAIEmbeddingResponse
 * @property {Array<{index: number, embedding: number[]}>} data
 * @property {{prompt_tokens: number, total_tokens: number}} [usage]
 */

export class OpenAIEmbeddingService {
  /**
   * @param {OpenAIEmbeddingConfig} config
   */
  constructor(config) {
    if (!config.apiKey) {
      throw new Error("EmbeddingService: apiKey is required for remote provider");
    }
    if (!config.baseUrl) {
      throw new Error("EmbeddingService: baseUrl is required for remote provider");
    }
    if (!config.model) {
      throw new Error("EmbeddingService: model is required for remote provider");
    }
    if (!config.dimensions || config.dimensions <= 0) {
      throw new Error("EmbeddingService: dimensions is required for remote provider (must be a positive integer)");
    }
    this.baseUrl = config.baseUrl.replace(/\/+$/, "");
    this.apiKey = config.apiKey;
    this.model = config.model;
    this.dims = config.dimensions;
    this.providerName = config.provider || "openai";
  }

  getDimensions() {
    return this.dims;
  }

  getProviderInfo() {
    return { provider: this.providerName, model: this.model };
  }

  isReady() {
    return true;
  }

  startWarmup() {
    // nothing to do — remote API is stateless
  }

  async embed(text) {
    const [result] = await this.embedBatch([text]);
    return result;
  }

  async embedBatch(texts) {
    if (texts.length === 0) return [];

    if (texts.length > MAX_BATCH_SIZE) {
      const results = [];
      for (let i = 0; i < texts.length; i += MAX_BATCH_SIZE) {
        const chunk = texts.slice(i, i + MAX_BATCH_SIZE);
        const chunkResults = await this._callApi(chunk);
        results.push(...chunkResults);
      }
      return results;
    }

    return this._callApi(texts);
  }

  /**
   * @param {string[]} texts
   * @returns {Promise<Float32Array[]>}
   */
  async _callApi(texts) {
    const body = {
      input: texts,
      model: this.model,
      dimensions: this.dims,
    };

    /** @type {Error|undefined} */
    let lastError;
    for (let attempt = 0; attempt <= MAX_RETRIES; attempt++) {
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), API_TIMEOUT_MS);

        try {
          const resp = await fetch(`${this.baseUrl}/embeddings`, {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              Authorization: `Bearer ${this.apiKey}`,
            },
            body: JSON.stringify(body),
            signal: controller.signal,
          });

          if (!resp.ok) {
            const errBody = await resp.text().catch(() => "(unable to read body)");
            const err = new EmbeddingApiError(
              `Embedding API error: HTTP ${resp.status} ${resp.statusText} — ${errBody.slice(0, 500)}`,
              resp.status,
            );
            if (resp.status >= 400 && resp.status < 500 && resp.status !== 429) {
              throw err;
            }
            lastError = err;
            continue;
          }

          /** @type {OpenAIEmbeddingResponse} */
          const json = await resp.json();

          if (!json.data || !Array.isArray(json.data)) {
            throw new Error("Embedding API returned unexpected format: missing 'data' array");
          }

          const sorted = [...json.data].sort((a, b) => a.index - b.index);
          return sorted.map((d) => sanitizeAndNormalize(d.embedding));
        } finally {
          clearTimeout(timeoutId);
        }
      } catch (err) {
        if (err instanceof EmbeddingApiError && err.isClientError()) {
          throw err;
        }
        lastError = err instanceof Error ? err : new Error(String(err));
        if (attempt < MAX_RETRIES) {
          const delay = 500 * (attempt + 1);
          await new Promise((r) => setTimeout(r, delay));
        }
      }
    }

    throw lastError ?? new Error("Embedding API call failed after retries");
  }
}

// ============================
// Factory
// ============================

/**
 * Create an EmbeddingService from config.
 * @param {EmbeddingConfig | undefined} config
 * @param {Object} [logger]
 * @returns {EmbeddingService}
 */
export function createEmbeddingService(config, logger) {
  if (config && config.provider !== "local" && "apiKey" in config && config.apiKey) {
    logger?.info(`${TAG} Using remote embedding (provider=${config.provider}, model=${config.model})`);
    return new OpenAIEmbeddingService(config);
  }

  if (config && config.provider === "local") {
    const localConfig = config;
    logger?.info(`${TAG} Using local embedding (node-llama-cpp, model=${localConfig.modelPath ?? DEFAULT_LOCAL_MODEL})`);
    return new LocalEmbeddingService(localConfig, logger);
  }

  logger?.info(`${TAG} No remote embedding configured, falling back to local embedding (node-llama-cpp)`);
  return new LocalEmbeddingService(undefined, logger);
}


