/**
 * TotalReclaw Plugin - Local Embedding via lazy GitHub-Releases bundle
 *
 * Generates text embeddings locally using an ONNX model. Preserves the
 * E2EE guarantee — embeddings are computed on the user's machine and
 * never leave it. The model itself, plus the heavy native dependencies
 * (`@huggingface/transformers`, `onnxruntime-node`), is fetched on
 * first use from a versioned GitHub Release tarball rather than shipped
 * inside the npm/ClawHub plugin tarball.
 *
 * Why lazy retrieval (rc.22):
 *   rc.21 OOM-killed the OpenClaw gateway during `openclaw plugins install`
 *   on a 3.7 GB Hetzner VPS — the heavy native deps required ~700 MB+
 *   peak install RAM, and a partial install left orphaned
 *   `~/.openclaw/extensions/.openclaw-install-stage-*` directories that
 *   the loader then auto-discovered on every boot, crashing the CLI.
 *   rc.22 splits the heavy bits out of the install path: the plugin
 *   tarball stays ~5-10 MB (ClawHub-friendly), the model + native deps
 *   are downloaded lazily when the user actually invokes a memory tool,
 *   and per-turn OOM is recoverable in a way install-time OOM is not.
 *
 * Locked to Harrier-OSS-v1-270M (640d, q4, ~344MB, pre-pooled). Changing
 * the embedding model breaks search across an existing vault, so the
 * `TOTALRECLAW_EMBEDDING_MODEL` user-facing env var was removed in v1.
 *
 * Forward-compat (rc.22): every claim is tagged with `embedding_model_id`
 * (see `getEmbeddingModelId()`) so a future distillation can be detected
 * and rescoped per claim without breaking the active vault.
 */

import os from 'node:os';
import path from 'node:path';
import { loadEmbedder } from './embedder-loader.js';

interface ModelConfig {
  /** Semantic model id surfaced to claims via `embedding_model_id`. */
  semanticId: string;
  /** Hugging Face / ONNX repo id used by the bundled `transformers` lib. */
  hfId: string;
  dims: number;
  /** 'sentence_embedding' for models with pre-pooled output, 'mean' / 'last_token' for pipeline models. */
  pooling: string;
  size: string;
  /** ONNX quantization dtype. Must match an available variant in the HF repo. */
  dtype: string;
}

const HARRIER_MODEL: ModelConfig = {
  semanticId: 'harrier-oss-270m-q4',
  hfId: 'onnx-community/harrier-oss-v1-270m-ONNX',
  dims: 640,
  pooling: 'sentence_embedding',
  size: '~344MB',
  dtype: 'q4',
};

function getModelConfig(): ModelConfig {
  return HARRIER_MODEL;
}

/**
 * Configuration for the lazy embedder bundle.
 *
 * Set ONCE at plugin init via `configureEmbedder({ ... })` from index.ts.
 * Centralising the env resolution upstream keeps this module scanner-clean.
 */
export interface EmbedderRuntimeConfig {
  /** Top-level cache directory (e.g. `~/.totalreclaw/embedder/`). */
  cacheRoot: string;
  /** RC tag used to build the GitHub-Releases URL, e.g. `"3.3.1-rc.22"`. */
  rcTag: string;
}

let runtimeConfig: EmbedderRuntimeConfig | null = null;

export function configureEmbedder(cfg: EmbedderRuntimeConfig): void {
  runtimeConfig = cfg;
}

/**
 * Default cache root. Used when `configureEmbedder()` was not called —
 * production code always calls it from index.ts; tests may rely on this
 * default.
 */
function defaultCacheRoot(): string {
  return path.join(os.homedir(), '.totalreclaw', 'embedder');
}

/**
 * Last-known-good embedder bundle tag. Used ONLY as a hard-fallback when
 * `configureEmbedder()` is never called by the orchestrator (defensive
 * path — production code always wires it via index.ts register()).
 *
 * 3.3.4-rc.1 — pinned to v3.3.3-rc.1 because that is the most recent
 * release at fix-time with a published `embedder-v1.tar.gz` asset. Earlier
 * fallback `'0.0.0-dev'` (rc.22 → 3.3.3-rc.1) hard-coded a placeholder
 * that resolved to a 404 GitHub Release URL; QA on 3.3.3-rc.1 (Pedro
 * 2026-04-30) caught it because the cascade-cause (broken
 * `readPluginVersion()` resolution) made the fallback fire on every cold
 * start. Bumping this constant per RC is fine — the publish workflow auto-
 * publishes the bundle for every RC tag (see scripts/build-embedder-
 * bundle.mjs in the public repo).
 */
const LAST_KNOWN_GOOD_RC_TAG = '3.3.3-rc.1';

function activeRuntimeConfig(): EmbedderRuntimeConfig {
  if (runtimeConfig) return runtimeConfig;
  return { cacheRoot: defaultCacheRoot(), rcTag: LAST_KNOWN_GOOD_RC_TAG };
}

/**
 * 3.3.3-rc.1 (issue #187 — ONNX decouple): prefetch the embedder bundle
 * WITHOUT loading the model into memory. Used to download the
 * ~700 MB tarball pre-pair so the user does not hit the network round-trip
 * mid-conversation. Idempotent — subsequent calls are cache-hit no-ops.
 *
 * Returns:
 *   - `'cache_hit'` if the bundle was already extracted + verified.
 *   - `'fetched'` if the bundle was downloaded this call.
 *   - throws on transport / extraction failure.
 *
 * Pre-flight is the caller's job (disk-space, network reachability) — this
 * function focuses on the cache-resolve + fetch-on-miss path so it can also
 * be reused as a fast cache-validation probe.
 */
export async function prefetchEmbedderBundle(opts?: { log?: (msg: string) => void }): Promise<'cache_hit' | 'fetched'> {
  const cfg = activeRuntimeConfig();
  const loaded = await loadEmbedder({
    cacheRoot: cfg.cacheRoot,
    rcTag: cfg.rcTag,
    log: opts?.log,
  });
  return loaded.wasFetched ? 'fetched' : 'cache_hit';
}

/** Lazily initialized state. */
let pipelineExtractor: any = null;
let autoTokenizer: any = null;
let autoModel: any = null;
let activeModel: ModelConfig | null = null;

/**
 * Generate an embedding vector for the given text.
 *
 * On first call, downloads the embedder bundle (transformers + onnxruntime
 * + the q4 ONNX model) from the pinned GitHub Release, verifies the
 * tarball SHA-256 against the manifest, extracts to
 * `~/.totalreclaw/embedder/v1/`, then loads the model into memory.
 * Subsequent calls reuse the loaded model and run in ~100 ms.
 */
export async function generateEmbedding(
  text: string,
  options?: { isQuery?: boolean },
): Promise<number[]> {
  if (!activeModel) {
    activeModel = getModelConfig();
    const cfg = activeRuntimeConfig();
    console.error(
      `[TotalReclaw] Embedding model first-call: fetching bundle ${activeModel.size} from GitHub Releases for v${cfg.rcTag} (cached at ${cfg.cacheRoot}).`,
    );

    const loaded = await loadEmbedder({
      cacheRoot: cfg.cacheRoot,
      rcTag: cfg.rcTag,
    });
    if (loaded.manifest.dimension !== activeModel.dims) {
      throw new Error(
        `embedder bundle dimension ${loaded.manifest.dimension} does not match plugin-expected ${activeModel.dims}. ` +
          `Refusing to use mismatched embedder — vector space drift would corrupt cosine search.`,
      );
    }
    if (loaded.manifest.model_id !== activeModel.semanticId) {
      console.error(
        `[TotalReclaw] WARNING: bundled model_id "${loaded.manifest.model_id}" != plugin-expected "${activeModel.semanticId}". Continuing — distillation forward-compat path.`,
      );
    }

    // Resolve the transformers entrypoint via the cache-bound ESM import.
    // The bundled package was generated by `scripts/build-embedder-bundle.mjs`
    // and lives at `<cache>/v1/node_modules/@huggingface/transformers`.
    //
    // Why ESM `import()` and not `require()`: `@huggingface/transformers` v4
    // ships dual CJS/ESM. On Node 24 the CJS `require()` interop returns the
    // module namespace but leaves the named ESM-first exports (`AutoModel`,
    // `AutoTokenizer`, `pipeline`) `undefined`, which surfaces as
    // `autoModel is not a function` and degrades recall to word-only. ESM
    // dynamic `import()` of the resolved entry file URL populates the named
    // exports correctly on every Node version we support. See
    // `makeCacheImport` in embedder-loader.ts.
    //
    // Defensive access (#394 follow-up): `cacheImport` normalizes the
    // namespace so named exports are always top-level, but if the bundle
    // is corrupt or a future Node version changes interop again, we want
    // a CLEAR error here ("transformers bundle did not expose AutoModel")
    // rather than the opaque downstream `autoModel is not a function`.
    // The previous fix silently returned undefined and let the inference
    // call site crash with a misleading message; this guard turns that
    // into an actionable one.
    const transformers = await loaded.cacheImport('@huggingface/transformers') as {
      AutoTokenizer?: unknown;
      AutoModel?: unknown;
      pipeline?: unknown;
      default?: { AutoTokenizer?: unknown; AutoModel?: unknown; pipeline?: unknown };
    };
    let AutoTokenizer = transformers.AutoTokenizer;
    let AutoModel = transformers.AutoModel;
    let pipeline = transformers.pipeline;
    // Final `.default` fallback — covers any future regression where the
    // loader's normalizer does not run (e.g. a hand-rolled caller).
    if ((!AutoModel || !AutoTokenizer || !pipeline) && transformers.default) {
      AutoTokenizer = AutoTokenizer ?? transformers.default.AutoTokenizer;
      AutoModel = AutoModel ?? transformers.default.AutoModel;
      pipeline = pipeline ?? transformers.default.pipeline;
    }
    if (typeof AutoModel !== 'function' && typeof AutoModel !== 'object') {
      throw new Error(
        `transformers bundle did not expose AutoModel (typeof=${typeof AutoModel}). ` +
          `Bundle may be corrupt or Node ${process.version} ESM-CJS interop ` +
          `incompatible with the bundled @huggingface/transformers entry. ` +
          `Cache at ${cfg.cacheRoot}/v1/.`,
      );
    }

    if (activeModel.pooling === 'sentence_embedding') {
      autoTokenizer = await AutoTokenizer.from_pretrained(activeModel.hfId);
      autoModel = await AutoModel.from_pretrained(activeModel.hfId, {
        dtype: activeModel.dtype as any,
      });
    } else {
      pipelineExtractor = await pipeline('feature-extraction', activeModel.hfId, {
        dtype: activeModel.dtype as any,
      });
    }
    console.error('[TotalReclaw] Embedding model ready. Future calls are in-memory.');
  }

  const model = activeModel!;

  if (model.pooling === 'sentence_embedding') {
    const inputs = await autoTokenizer(text, { return_tensors: 'pt', padding: true });
    const output = await autoModel(inputs);
    return Array.from(output.sentence_embedding.data as Float32Array);
  } else {
    const input = model.pooling === 'mean' && options?.isQuery
      ? `query: ${text}`
      : text;
    const output = await pipelineExtractor(input, { pooling: model.pooling as any, normalize: true });
    return Array.from(output.data as Float32Array);
  }
}

/**
 * Get the embedding vector dimensionality.
 * Returns 640 for Harrier-OSS-270M-q4.
 */
export function getEmbeddingDims(): number {
  return getModelConfig().dims;
}

/**
 * Get the semantic embedding-model id stamped on each new claim (rc.22+).
 *
 * Forward-compat marker: if a future plugin version distills to a smaller
 * model, claims tagged with the prior id can be re-embedded selectively
 * instead of forcing a vault-wide rebuild. Defaults to the v1 Harrier id —
 * plugin code always tags new claims via this constant, never trusts the
 * model id from a downloaded bundle for write-time tagging.
 */
export function getEmbeddingModelId(): string {
  return getModelConfig().semanticId;
}
