/**
 * Plugin configuration — centralized env var reads.
 * This file ONLY reads process.env. No network calls, no I/O.
 * Other modules import config values from here.
 *
 * OpenClaw's security scanner flags files that contain BOTH process.env reads
 * AND network calls. By centralizing all env reads here, no other file needs
 * to touch process.env directly.
 *
 * v1 env var cleanup — see `docs/guides/env-vars-reference.md`.
 * Removed user-facing vars: TOTALRECLAW_CHAIN_ID, TOTALRECLAW_EMBEDDING_MODEL,
 * TOTALRECLAW_STORE_DEDUP, TOTALRECLAW_LLM_MODEL, TOTALRECLAW_TAXONOMY_VERSION.
 *
 * NOTE: ``TOTALRECLAW_SESSION_ID`` was in the removed list during the v1
 * cleanup and silently rejected with a warning. That broke Axiom log tracing
 * for QA — the qa-totalreclaw skill prescribes setting the var so relay logs
 * are searchable by ``X-TotalReclaw-Session``. Restored as a SUPPORTED
 * variable: read here, forwarded as the ``X-TotalReclaw-Session`` header on
 * every outbound relay call. Mirrors the Python-side fix
 * (`python/src/totalreclaw/agent/state.py`, v2.0.2). See internal#127.
 * Removed legacy gates: TOTALRECLAW_CLAIM_FORMAT, TOTALRECLAW_DIGEST_MODE,
 * TOTALRECLAW_AUTO_RESOLVE_MODE (the last one moved to an internal debug
 * module; see `contradiction-sync.ts`).
 *
 * Tuning knobs (cosine threshold, min importance, cache TTL, etc.) are now
 * delivered via the relay billing response. Env-var fallbacks are kept only
 * for self-hosted deployments where the server may not surface those values.
 */
import path from 'node:path';
const home = process.env.HOME ?? '/home/node';
/**
 * Removed env vars — warn once per process if still set so operators know
 * their config is a no-op. The removal list matches `docs/guides/env-vars-reference.md`.
 */
const REMOVED_ENV_VARS = [
    'TOTALRECLAW_CHAIN_ID',
    'TOTALRECLAW_EMBEDDING_MODEL',
    'TOTALRECLAW_STORE_DEDUP',
    'TOTALRECLAW_LLM_MODEL',
    // NOTE: TOTALRECLAW_SESSION_ID was here before; restored as SUPPORTED
    // (forwarded as X-TotalReclaw-Session header). Do NOT add it back to this
    // list — see file header + internal#127.
    'TOTALRECLAW_TAXONOMY_VERSION',
    'TOTALRECLAW_CLAIM_FORMAT',
    'TOTALRECLAW_DIGEST_MODE',
];
// Migration guide URL — kept as a constant so the regression test can assert
// the exact link text in the warning. Pointing at GitHub raw-blob is more
// useful than the relative repo path: operators copying the warning out of
// stderr usually do not have the repo cloned. rc.22 finding #4.
export const ENV_VARS_REFERENCE_URL = 'https://github.com/p-diogo/totalreclaw/blob/main/docs/guides/env-vars-reference.md';
function warnRemovedEnvVars(warn = console.warn) {
    const set = REMOVED_ENV_VARS.filter((name) => process.env[name] !== undefined);
    if (set.length === 0)
        return;
    warn(`TotalReclaw: ignoring removed env var(s): ${set.join(', ')}. ` +
        `Migration guide: ${ENV_VARS_REFERENCE_URL}`);
}
// Emit the warning once at import time. Safe because this module is loaded
// exactly once per process.
warnRemovedEnvVars();
/** Runtime override for recovery phrase (set by hot-reload after setup). */
let _recoveryPhraseOverride = null;
export function setRecoveryPhraseOverride(phrase) {
    _recoveryPhraseOverride = phrase;
}
export function getRecoveryPhrase() {
    return _recoveryPhraseOverride ?? process.env.TOTALRECLAW_RECOVERY_PHRASE ?? '';
}
/**
 * Read the QA / observability session tag from the environment.
 *
 * When set, every outbound relay call adds the ``X-TotalReclaw-Session``
 * header so relay logs (and Axiom queries) can be filtered by this tag —
 * this is what the qa-totalreclaw skill relies on to scope log searches per
 * QA run. When unset, returns ``null`` and the header is omitted.
 *
 * Read via getter (not snapshotted) so operators / test harnesses can flip
 * the var between calls without reloading the module.
 *
 * Mirrors the Python-side ``RelayClient._session_id`` resolution priority.
 * See internal#127 / `docs/guides/env-vars-reference.md`.
 */
export function getSessionId() {
    const raw = process.env.TOTALRECLAW_SESSION_ID;
    if (raw === undefined)
        return null;
    const trimmed = raw.trim();
    return trimmed.length > 0 ? trimmed : null;
}
/**
 * Runtime override for chain ID, set after the relay billing response is
 * read. Free tier stays on 84532 (Base Sepolia); Pro tier flips to 100
 * (Gnosis mainnet). The relay routes Pro writes to Gnosis, so Pro-tier
 * UserOps MUST be signed against chain 100 — otherwise the bundler rejects
 * the signature with AA23.
 *
 * See index.ts: after the billing lookup completes, call
 * `setChainIdOverride(100)` for Pro users. Free users can leave the
 * override unset.
 */
let _chainIdOverride = null;
export function setChainIdOverride(chainId) {
    _chainIdOverride = chainId;
}
/** Reset the chain override — used by tests. */
export function __resetChainIdOverrideForTests() {
    _chainIdOverride = null;
}
export const CONFIG = {
    // Core — recoveryPhrase reads from override first, then env var.
    // Use getRecoveryPhrase() for dynamic access; this property is for
    // backward-compat with code that reads CONFIG.recoveryPhrase at init time.
    get recoveryPhrase() {
        return getRecoveryPhrase();
    },
    /**
     * Optional QA / observability session tag forwarded to the relay as
     * ``X-TotalReclaw-Session``. See `getSessionId()` above. Getter form so
     * tests + harnesses can flip the env between calls. ``null`` when unset
     * (header omitted).
     */
    get sessionId() {
        return getSessionId();
    },
    // 3.3.12-rc.1 (F flip): source default is `api.totalreclaw.xyz` (production)
    // for BOTH stable and RC builds. Previously RC defaulted to staging, which
    // stranded users who picked `@rc` with their memories on staging. Staging
    // access is now opt-in via `TOTALRECLAW_SERVER_URL=https://api-staging.totalreclaw.xyz`.
    // No more publish-time URL rewrites — both release-types ship the same
    // production default, and the workflow guard rails simply assert that.
    // User overrides via `TOTALRECLAW_SERVER_URL=...` always win.
    serverUrl: (process.env.TOTALRECLAW_SERVER_URL || 'https://api.totalreclaw.xyz').replace(/\/+$/, ''),
    selfHosted: process.env.TOTALRECLAW_SELF_HOSTED === 'true',
    credentialsPath: process.env.TOTALRECLAW_CREDENTIALS_PATH || path.join(home, '.totalreclaw', 'credentials.json'),
    // cred-3 stage 1 — credential-provider abstraction.
    //
    // `file` (default) preserves the legacy behavior: read/write
    // `credentialsPath` directly via fs-helpers.
    //
    // `external` instructs the plugin to load credentials from an
    // out-of-process source at boot. Two transports are supported (mutually
    // exclusive — JSON wins if both set):
    //   1. `externalCredentialsJson` — raw JSON string of CredentialsFile,
    //      injected at process start by the secret manager (Railway secrets,
    //      Docker `--env-file`, K8s envFrom). Most ergonomic for cloud
    //      deployments where the secret manager already exposes secrets as
    //      env vars.
    //   2. `externalCredentialsPath` — filesystem path to a JSON file the
    //      secret manager mounts (Docker Compose `secrets:` block,
    //      K8s secret volumeMount, tmpfs populated by an ops wrapper that
    //      fetches from AWS Secrets Manager / Hetzner Vault before boot).
    //
    // `external` mode is read-only: write/clear are no-ops with a warning
    // (the secret manager owns the source of truth — the plugin must not
    // write back through this path).
    //
    // See `docs/guides/production-deployment.md` for the LUKS / dm-crypt
    // pattern and managed-secret-store wiring examples.
    credentialsProvider: (() => {
        const v = (process.env.TOTALRECLAW_CREDENTIALS_PROVIDER ?? '').trim().toLowerCase();
        return v === 'external' ? 'external' : 'file';
    })(),
    externalCredentialsJson: (() => {
        const v = (process.env.TOTALRECLAW_EXTERNAL_CREDENTIALS_JSON ?? '').trim();
        return v.length > 0 ? v : null;
    })(),
    externalCredentialsPath: (() => {
        const v = (process.env.TOTALRECLAW_EXTERNAL_CREDENTIALS_PATH ?? '').trim();
        return v.length > 0 ? v : null;
    })(),
    // 3.2.0 onboarding state file — separate from credentials.json so it
    // never contains secrets. Loaded on every plugin init + on every
    // before_tool_call gate check.
    onboardingStatePath: process.env.TOTALRECLAW_STATE_PATH || path.join(home, '.totalreclaw', 'state.json'),
    // 3.3.0 QR-pairing session store. Separate file from both credentials.json
    // and state.json so the session-store module does not have to touch either
    // (keeps scanner surface isolated). Contains ephemeral x25519 secret keys
    // for 15-min TTL windows; 0600 mode.
    pairSessionsPath: process.env.TOTALRECLAW_PAIR_SESSIONS_PATH || path.join(home, '.totalreclaw', 'pair-sessions.json'),
    // 3.3.1-rc.11 — pair-flow transport selector. Mirrors the Python-side
    // `TOTALRECLAW_PAIR_MODE` env (rc.10). `'relay'` (default) routes
    // `totalreclaw_pair` through the universal-reachability WebSocket relay at
    // `TOTALRECLAW_PAIR_RELAY_URL`. `'local'` preserves the rc.4–rc.10 loopback
    // HTTP flow (the plugin serves `/plugin/totalreclaw/pair/*` via
    // `pair-http.ts`). Air-gapped / self-hosted users can pin `'local'` here.
    pairMode: (() => {
        const v = (process.env.TOTALRECLAW_PAIR_MODE ?? '').trim().toLowerCase();
        return v === 'local' ? 'local' : 'relay';
    })(),
    // 3.3.1-rc.11 — relay base URL for the WebSocket-brokered pair flow.
    // `wss://` preferred; `https://` is rewritten in the remote-client.
    //
    // 3.3.12-rc.2 fix: derive from `TOTALRECLAW_SERVER_URL` when
    // `TOTALRECLAW_PAIR_RELAY_URL` is not explicitly set. Pair WS endpoint
    // lives on the SAME relay as the rest of the API — RC users who set
    // `TOTALRECLAW_SERVER_URL=https://api-staging.totalreclaw.xyz` (per F
    // flip / staging-opt-in flow) need pair to follow. Previous behavior
    // had pair default to prod independently, which 404'd on WS upgrade
    // because production relay version pre-dates the pair feature.
    pairRelayUrl: (process.env.TOTALRECLAW_PAIR_RELAY_URL
        || (process.env.TOTALRECLAW_SERVER_URL
            ? process.env.TOTALRECLAW_SERVER_URL.replace(/^https?:\/\//, 'wss://').replace(/^http:/, 'ws:')
            : 'wss://api.totalreclaw.xyz')).replace(/\/+$/, ''),
    // Chain — chainId is no longer user-configurable. It is auto-detected from
    // the relay billing response (free = Base Sepolia / 84532, Pro = Gnosis /
    // 100). The default here is used only before the first billing lookup
    // completes. Self-hosted users can still point at a custom DataEdge via
    // TOTALRECLAW_DATA_EDGE_ADDRESS / TOTALRECLAW_ENTRYPOINT_ADDRESS /
    // TOTALRECLAW_RPC_URL (undocumented; internal knobs).
    //
    // Reads the runtime override set by the billing auto-detect in index.ts.
    // Falls back to 84532 (free tier / pre-billing-lookup). Must be a getter,
    // not a literal — a literal would freeze all Pro-tier UserOps to the
    // wrong chainId and AA23 at the bundler.
    get chainId() {
        return _chainIdOverride ?? 84532;
    },
    dataEdgeAddress: process.env.TOTALRECLAW_DATA_EDGE_ADDRESS || '',
    entryPointAddress: process.env.TOTALRECLAW_ENTRYPOINT_ADDRESS || '',
    rpcUrl: process.env.TOTALRECLAW_RPC_URL || '',
    // 3.3.3-rc.1 (issue #187 — ONNX decouple): kill switch for the
    // non-blocking embedder bundle prefetch fired from register(). Set to
    // `1` in CI / sandboxed environments where the GitHub-Releases CDN is
    // unreachable. The next call to generateEmbedding() still triggers the
    // download via the same idempotent path.
    embedderPrefetchDisabled: process.env.TOTALRECLAW_DISABLE_EMBEDDER_PREFETCH === '1',
    // 3.3.3-rc.1 (PR #165 implementation): observable form of "did the user
    // explicitly override the bundled-default server URL via env?". Used
    // by the RC-staging banner check in index.ts so the banner suppresses
    // when the user has pinned a custom URL (production or self-hosted).
    // Lives here so index.ts stays free of process.env reads (scanner
    // env-harvesting rule).
    serverUrlEnvOverridden: !!process.env.TOTALRECLAW_SERVER_URL,
    // Tuning knobs — default values used only as local fallback for
    // self-hosted mode. Managed-service clients override these from the relay
    // billing response via `resolveTuning(...)`.
    // See: docs/specs/totalreclaw/client-consistency.md
    cosineThreshold: parseFloat(process.env.TOTALRECLAW_COSINE_THRESHOLD ?? '0.15'),
    extractInterval: parseInt(process.env.TOTALRECLAW_EXTRACT_INTERVAL ?? process.env.TOTALRECLAW_EXTRACT_EVERY_TURNS ?? '3', 10),
    relevanceThreshold: parseFloat(process.env.TOTALRECLAW_RELEVANCE_THRESHOLD ?? '0.3'),
    semanticSkipThreshold: parseFloat(process.env.TOTALRECLAW_SEMANTIC_SKIP_THRESHOLD ?? '0.85'),
    cacheTtlMs: parseInt(process.env.TOTALRECLAW_CACHE_TTL_MS ?? String(5 * 60 * 1000), 10),
    minImportance: Math.max(1, Math.min(10, Number(process.env.TOTALRECLAW_MIN_IMPORTANCE) || 6)),
    trapdoorBatchSize: parseInt(process.env.TOTALRECLAW_TRAPDOOR_BATCH_SIZE ?? '5', 10),
    pageSize: parseInt(process.env.TOTALRECLAW_SUBGRAPH_PAGE_SIZE ?? '1000', 10),
    // Store-time dedup is always ON. TOTALRECLAW_STORE_DEDUP was removed in v1.
    storeDedupEnabled: true,
    // LLM provider API keys (read once, passed to llm-client). Model selection
    // is entirely automatic via `deriveCheapModel(provider)` — the
    // TOTALRECLAW_LLM_MODEL override was removed in v1.
    llmApiKeys: {
        zai: process.env.ZAI_API_KEY || '',
        anthropic: process.env.ANTHROPIC_API_KEY || '',
        openai: process.env.OPENAI_API_KEY || '',
        gemini: process.env.GEMINI_API_KEY || '',
        google: process.env.GOOGLE_API_KEY || '',
        mistral: process.env.MISTRAL_API_KEY || '',
        groq: process.env.GROQ_API_KEY || '',
        deepseek: process.env.DEEPSEEK_API_KEY || '',
        openrouter: process.env.OPENROUTER_API_KEY || '',
        xai: process.env.XAI_API_KEY || '',
        together: process.env.TOGETHER_API_KEY || '',
        cerebras: process.env.CEREBRAS_API_KEY || '',
    },
    // 3.3.1-rc.3: zai base-URL override. Read via a getter so tests can
    // mutate `process.env.ZAI_BASE_URL` between calls — the value is NOT
    // frozen at module load. Default is the coding endpoint; the rc.3
    // auto-fallback flips to the standard endpoint on an "Insufficient
    // balance" 429.
    get zaiBaseUrl() {
        const override = process.env.ZAI_BASE_URL;
        if (override && override.trim())
            return override.trim().replace(/\/+$/, '');
        return 'https://api.z.ai/api/coding/paas/v4';
    },
    // 3.3.1-rc.3: retry budget for chatCompletion. Default 60s covers
    // multi-minute upstream outages. Read as a plain value (not getter)
    // so tests that patch env need to reload the module — but the default
    // suffices for production.
    llmRetryBudgetMs: (() => {
        const raw = process.env.TOTALRECLAW_LLM_RETRY_BUDGET_MS;
        const parsed = raw ? parseInt(raw, 10) : NaN;
        return Number.isFinite(parsed) && parsed > 0 ? parsed : 60_000;
    })(),
    // 3.3.1-rc.3: GitHub personal-access token used by the RC-gated
    // `totalreclaw_report_qa_bug` tool. `TOTALRECLAW_QA_GITHUB_TOKEN` is
    // the dedicated variable; `GITHUB_TOKEN` is a fallback for CI-style
    // setups where the same token is shared across tools. Read via getter
    // so operators can set the var after the process starts (e.g. via a
    // dotenv reload) and the next tool call picks it up.
    get qaGithubToken() {
        return process.env.TOTALRECLAW_QA_GITHUB_TOKEN || process.env.GITHUB_TOKEN || '';
    },
    // 3.3.1-rc.14: optional target-repo override for the RC-gated QA
    // bug-report tool. The `qa-bug-report` module enforces a
    // "slug ends in `-internal`" rule on whatever is resolved here, so
    // this override is only useful for forks / mirrors of the internal
    // tracker. Leaving unset uses the production default
    // (`p-diogo/totalreclaw-internal`). Read via getter so operators can
    // flip the var at runtime.
    get qaRepoOverride() {
        return process.env.TOTALRECLAW_QA_REPO || '';
    },
    // 3.3.1-rc.21 (issue #128): verbose-register flag. When enabled, the
    // plugin emits opt-in `info`-level breadcrumbs after sensitive
    // registerTool calls (currently `totalreclaw_pair`) to help ops/QA
    // grep gateway logs for definitive proof the tool was declared.
    // Default OFF — the breadcrumb is debug-grade and was bleeding into
    // `openclaw agent --json` stdout, breaking programmatic parsers.
    // Enable with either:
    //   TOTALRECLAW_VERBOSE_REGISTER=1   (specific opt-in)
    //   TOTALRECLAW_DEBUG=1              (general debug toggle)
    // Read via getter so flipping the env at runtime takes effect on the
    // next gateway start without a rebuild.
    get verboseRegister() {
        const specific = (process.env.TOTALRECLAW_VERBOSE_REGISTER ?? '').trim().toLowerCase();
        if (specific === '1' || specific === 'true' || specific === 'yes')
            return true;
        const general = (process.env.TOTALRECLAW_DEBUG ?? '').trim().toLowerCase();
        return general === '1' || general === 'true' || general === 'yes';
    },
    // Paths
    home,
    billingCachePath: path.join(home, '.totalreclaw', 'billing-cache.json'),
    cachePath: process.env.TOTALRECLAW_CACHE_PATH || path.join(home, '.totalreclaw', 'cache.enc'),
    openclawWorkspace: path.join(home, '.openclaw', 'workspace'),
    // 3.3.1-rc.22 — lazy embedder bundle cache. The embedder
    // (`@huggingface/transformers` + `onnxruntime-node` + the q4 ONNX
    // model) is no longer shipped inside the plugin tarball; it is fetched
    // on first `embed()` call from a versioned GitHub Release and cached
    // here. Separate path from `cachePath` (encrypted vault cache) so the
    // two never collide. See `embedder-loader.ts`.
    embedderCachePath: process.env.TOTALRECLAW_EMBEDDER_CACHE_PATH || path.join(home, '.totalreclaw', 'embedder'),
    // 3.3.1-rc.22 — override the GitHub-Releases URL templates. Only useful
    // for air-gapped / mirror deployments and self-hosted CI. Empty string
    // falls back to the static defaults baked into the embedder code path.
    embedderBundleUrlTemplate: process.env.TOTALRECLAW_EMBEDDER_BUNDLE_URL || '',
    embedderManifestUrlTemplate: process.env.TOTALRECLAW_EMBEDDER_MANIFEST_URL || '',
};
/**
 * Merge a billing-response tuning block with the local fallback values.
 *
 * Use this at the call-site that needs a threshold, passing the features
 * blob from the billing cache. No I/O here — callers read the cache once
 * and hand the features in.
 */
export function resolveTuning(features) {
    return {
        cosineThreshold: features?.cosine_threshold ?? CONFIG.cosineThreshold,
        relevanceThreshold: features?.relevance_threshold ?? CONFIG.relevanceThreshold,
        semanticSkipThreshold: features?.semantic_skip_threshold ?? CONFIG.semanticSkipThreshold,
        minImportance: features?.min_importance ?? CONFIG.minImportance,
        cacheTtlMs: features?.cache_ttl_ms ?? CONFIG.cacheTtlMs,
        trapdoorBatchSize: features?.trapdoor_batch_size ?? CONFIG.trapdoorBatchSize,
        pageSize: features?.subgraph_page_size ?? CONFIG.pageSize,
    };
}
// Exposed for tests that want to assert the removed-var warning behaviour.
export const __internal = {
    REMOVED_ENV_VARS,
    warnRemovedEnvVars,
};
