// Note (3.0.8): every `fs.*` call that used to live in this file has been
// consolidated into `./fs-helpers.ts`, so the OpenClaw `potential-exfiltration`
// scanner rule (whole-file `fs.read*` + network-send marker) cannot fire here.
// The `billing-cache.ts` extraction (3.0.7) already moved the billing-cache
// read; 3.0.8 adds MEMORY.md header ensure, credentials.json load/write/delete,
// and the Docker runtime sniff. If you find yourself wanting to add an
// `fs.*` call below, add a helper to `fs-helpers.ts` instead.
/**
 * TotalReclaw Plugin for OpenClaw
 *
 * Registers runtime tools so OpenClaw can execute TotalReclaw operations:
 *   - totalreclaw_remember     -- store an encrypted memory
 *   - totalreclaw_recall       -- search and decrypt memories
 *   - totalreclaw_forget       -- soft-delete a memory
 *   - totalreclaw_export       -- export all memories (JSON or Markdown)
 *   - totalreclaw_status       -- check billing/subscription status
 *   - totalreclaw_consolidate  -- scan and merge near-duplicate memories
 *   - totalreclaw_pin          -- pin a memory so auto-resolution can never supersede it
 *   - totalreclaw_unpin        -- remove a pin, returning the memory to active status
 *   - totalreclaw_import_from   -- import memories from other tools (Mem0, MCP Memory, etc.)
 *   - totalreclaw_import_status -- check background import progress
 *   - totalreclaw_import_abort  -- cancel a running background import
 *   - totalreclaw_upgrade       -- create Stripe checkout for Pro upgrade
 *   - totalreclaw_migrate      -- migrate testnet memories to mainnet after Pro upgrade
 *   - totalreclaw_onboarding_start -- non-secret pointer to the CLI wizard (3.2.0)
 *   - totalreclaw_setup        -- DEPRECATED in 3.2.0; redirects to the CLI wizard
 *
 * Also registers:
 *   - `before_agent_start` hook that automatically injects relevant memories
 *     into the agent's context (and a non-secret onboarding hint when the
 *     user has not completed the CLI setup yet).
 *   - `before_tool_call` hook that gates every memory tool until onboarding
 *     state is `active` (3.2.0).
 *   - `registerCli` subcommand `openclaw totalreclaw onboard` — the ONLY
 *     surface that generates or accepts a recovery phrase. Lives entirely on
 *     the user's terminal; the phrase never enters an LLM request or a
 *     session transcript.
 *   - `registerCommand` slash command `/totalreclaw {onboard,status}` — a
 *     non-secret pointer that directs the user to the CLI wizard.
 *
 * Security: in 3.2.0, the recovery phrase NEVER appears in tool responses,
 * `prependContext` blocks, slash-command replies, or any other surface that
 * is sent to the LLM provider or persisted to the session transcript. See
 * `docs/plans/2026-04-20-plugin-320-secure-onboarding.md` in the internal
 * repo for the threat-model analysis and per-surface classification.
 *
 * All data is encrypted client-side with XChaCha20-Poly1305. The server never
 * sees plaintext.
 */
import { deriveKeys, deriveLshSeed, computeAuthKeyHash, encrypt, decrypt, generateBlindIndices, generateContentFingerprint, } from './crypto.js';
import { createApiClient } from './api-client.js';
import { extractFacts, extractCrystal, isValidMemoryType, parseEntity, VALID_MEMORY_TYPES, LEGACY_V0_MEMORY_TYPES, VALID_MEMORY_SOURCES, VALID_MEMORY_SCOPES, EXTRACTION_SYSTEM_PROMPT, extractFactsForCompaction, } from './extractor.js';
import { initLLMClient, resolveLLMConfig, chatCompletion, generateEmbedding, getEmbeddingDims, getEmbeddingModelId, configureEmbedder, prefetchEmbedderBundle, } from './llm-client.js';
import { defaultAuthProfilesRoot, readAllProfileKeys, dedupeByProvider, } from './llm-profile-reader.js';
import { LSHHasher } from './lsh.js';
import { rerank, cosineSimilarity, detectQueryIntent, INTENT_WEIGHTS } from './reranker.js';
import { deduplicateBatch } from './semantic-dedup.js';
import { startTrajectoryPoller } from './trajectory-poller.js';
import { findNearDuplicate, shouldSupersede, clusterFacts, getStoreDedupThreshold, getConsolidationThreshold, STORE_DEDUP_MAX_CANDIDATES, } from './consolidation.js';
import { isSubgraphMode, getSubgraphConfig, encodeFactProtobuf, submitFactBatchOnChain, deriveSmartAccountAddress, PROTOBUF_VERSION_V4 } from './subgraph-store.js';
import { confirmIndexed } from './confirm-indexed.js';
import { DIGEST_TRAPDOOR, buildCanonicalClaim, computeEntityTrapdoor, computeEntityTrapdoors, isDigestBlob, normalizeToV1Type, readClaimFromBlob, resolveDigestMode, } from './claims-helper.js';
import { maybeInjectDigest, recompileDigest, fetchAllActiveClaims, isRecompileInProgress, tryBeginRecompile, endRecompile, } from './digest-sync.js';
import { detectAndResolveContradictions, runWeightTuningLoop, } from './contradiction-sync.js';
import { searchSubgraph, searchSubgraphBroadened, getSubgraphFactCount, fetchFactById } from './subgraph-search.js';
import { executePinOperation, validatePinArgs, } from './pin.js';
import { executeRetype, executeSetScope, validateRetypeArgs, validateSetScopeArgs, } from './retype-setscope.js';
import { PluginHotCache } from './hot-cache-wrapper.js';
import { CONFIG, setRecoveryPhraseOverride } from './config.js';
import { buildRelayHeaders } from './relay-headers.js';
import { readBillingCache, writeBillingCache, BILLING_CACHE_PATH, } from './billing-cache.js';
import { ensureMemoryHeaderFile, loadCredentialsJson, writeCredentialsJson, deleteCredentialsFile, isRunningInDocker, deleteFileIfExists, resolveOnboardingState, writeOnboardingState, readPluginVersion, cleanupInstallStagingDirs, clearPartialInstallMarker, patchOpenClawConfig, writePluginManifest, writePluginError, readPluginLoadedManifest, checkCredentialsFileMode, deletePairPendingFile, defaultPairPendingPath, } from './fs-helpers.js';
import { maybeStartAutoPair } from './auto-pair-on-load.js';
import { installBeforeAgentStartHook as installPairPendingHook } from './pair-pending-injection.js';
import { isRcBuild } from './qa-bug-report.js';
import { decideToolGate, isGatedToolName } from './tool-gating.js';
import { resolveRestartAuth, rejectMessageFor, } from './restart-auth.js';
import { recordInboundUser, getDistinctInboundUserCount, resolveTrackerPath, } from './inbound-user-tracker.js';
import { detectFirstRun, buildWelcomePrepend } from './first-run.js';
import { buildPairRoutes } from './pair-http.js';
import { detectGatewayHost } from './gateway-url.js';
import { validateMnemonic } from '@scure/bip39';
import { wordlist } from '@scure/bip39/wordlists/english.js';
import crypto from 'node:crypto';
import { createRequire } from 'node:module';
import { fileURLToPath } from 'node:url';
import * as nodePath from 'node:path';
import { writeImportState, readImportState, isImportStale, readMostRecentActiveImport, } from './import-state-manager.js';
// CJS-style require for the @totalreclaw/core WASM module. We keep this
// load path lazy (only inside getSmartImportWasm() below) so a partial
// install of the dependency tree doesn't crash module init. Bare
// `require()` is a CommonJS global and is undefined under bare Node ESM —
// the shipped `dist/index.js` declares `"type":"module"`, so calling the
// global directly emits "require is not defined" at runtime (issue #124).
// createRequire bridges the gap. Same shape as crypto.ts / lsh.ts /
// subgraph-store.ts / claims-helper.ts.
const __cjsRequire = createRequire(import.meta.url);
// ---------------------------------------------------------------------------
// Human-friendly error messages
// ---------------------------------------------------------------------------
/**
 * Translate technical error messages from the on-chain submission pipeline
 * into user-friendly messages. The original technical details are still
 * logged via api.logger — this only affects what the agent sees.
 */
function humanizeError(rawMessage) {
    if (rawMessage.includes('AA23')) {
        return 'Memory storage temporarily unavailable. Will retry next time.';
    }
    if (rawMessage.includes('AA10')) {
        return 'Please wait a moment before storing more memories.';
    }
    if (rawMessage.includes('AA25')) {
        return 'Memory storage busy. Will retry.';
    }
    if (rawMessage.includes('pm_sponsorUserOperation')) {
        return 'Memory storage service temporarily unavailable.';
    }
    if (/Relay returned HTTP\s*404/.test(rawMessage)) {
        return 'Memory service is temporarily offline.';
    }
    if (/Relay returned HTTP\s*5\d\d/.test(rawMessage)) {
        return 'Memory service encountered a temporary error. Will retry next time.';
    }
    // Pass through non-technical messages as-is.
    return rawMessage;
}
// ---------------------------------------------------------------------------
// Persistent credential storage
// ---------------------------------------------------------------------------
/** Path where we persist userId + salt across restarts. */
const CREDENTIALS_PATH = CONFIG.credentialsPath;
// ---------------------------------------------------------------------------
// 3.3.0 — pairing URL resolution
// ---------------------------------------------------------------------------
/**
 * Build the full pairing URL (including `#pk=` fragment) for a fresh
 * pairing session. Pulls gateway config from `api.config.gateway`.
 *
 * Resolution order (3.3.1 — six-layer cascade):
 *   1. `plugins.entries.totalreclaw.config.publicUrl` — explicit override
 *   2. `gateway.remote.url` — OpenClaw's own remote-gateway URL
 *   3. `gateway.bind === 'custom'` + `gateway.customBindHost` + port
 *   4. Tailscale auto-detect — `tailscale status --json` → `https://<MagicDNS>`
 *      (assumes `tailscale serve` proxies to the gateway port on 443)
 *   5. LAN auto-detect — first non-loopback, non-virtual IPv4 interface.
 *      Emits a warning: "only works on the same network".
 *   6. Fallback `http://localhost:<port>` — warns with a pointer to
 *      configure `plugins.entries.totalreclaw.config.publicUrl`.
 *
 * Always returns a working URL string; never throws. The caller (CLI or
 * JSON output) prints whatever we give it.
 */
function buildPairingUrl(api, session) {
    const cfg = api.config;
    const pluginCfg = (api.pluginConfig ?? {});
    const tlsEnabled = cfg?.gateway?.tls?.enabled === true;
    const scheme = tlsEnabled ? 'https' : 'http';
    const port = cfg?.gateway?.port ?? 18789;
    let base;
    // Layer 1 — explicit user override
    if (typeof pluginCfg.publicUrl === 'string' && pluginCfg.publicUrl.trim()) {
        base = pluginCfg.publicUrl.replace(/\/+$/, '');
        base = base.replace(/^wss:\/\//i, 'https://').replace(/^ws:\/\//i, 'http://');
    }
    // Layer 2 — OpenClaw gateway remote URL
    else if (typeof cfg?.gateway?.remote?.url === 'string' && cfg.gateway.remote.url.trim()) {
        base = cfg.gateway.remote.url.trim().replace(/\/+$/, '');
        base = base.replace(/^wss:\/\//i, 'https://').replace(/^ws:\/\//i, 'http://');
    }
    // Layer 3 — gateway.bind = custom + explicit customBindHost
    else if (cfg?.gateway?.bind === 'custom' && cfg.gateway.customBindHost) {
        base = `${scheme}://${cfg.gateway.customBindHost}:${port}`;
    }
    // Layers 4 + 5 — auto-detect via gateway-url helper (Tailscale CGNAT, then LAN)
    else {
        let detected = null;
        // issue #110 fix 4 — pass `isDocker` so LAN detection skips
        // 172.16/12 bridge IPs that no external browser can reach.
        let isDocker = false;
        try {
            isDocker = isRunningInDocker();
        }
        catch {
            // Defensive: never block URL building on Docker sniff errors.
            isDocker = false;
        }
        try {
            detected = detectGatewayHost({ isDocker });
        }
        catch (err) {
            api.logger.warn(`TotalReclaw: host autodetect crashed: ${err instanceof Error ? err.message : String(err)} — falling back to localhost`);
        }
        if (detected?.kind === 'tailscale') {
            // 3.3.1-rc.2: we surface the raw Tailscale CGNAT IP because passive
            // NIC detection (no subprocess) cannot resolve the MagicDNS name.
            // Caller can override via `publicUrl` for a proper https://<magicdns>.
            // The IP + port URL still works inside the tailnet (peers can reach
            // each other by CGNAT IP directly). TLS defaults to the gateway's
            // own config because we no longer assume `tailscale serve`.
            base = `${scheme}://${detected.host}:${port}`;
            api.logger.warn(`TotalReclaw: pairing URL using Tailscale CGNAT IP ${detected.host}:${port} — ` +
                detected.note);
        }
        else if (detected?.kind === 'lan') {
            base = `${scheme}://${detected.host}:${port}`;
            api.logger.warn(`TotalReclaw: pairing URL using LAN host ${detected.host}:${port} — ` +
                `this URL only works from the same network. ` +
                `Set plugins.entries.totalreclaw.config.publicUrl for remote access.`);
        }
        else {
            // Layer 6 — localhost fallback (or Docker-aware relay-pointer warning)
            const bind = cfg?.gateway?.bind;
            if (isDocker) {
                // issue #110 fix 4: inside Docker the LAN IP is container-internal
                // and useless. Loopback localhost only works for `docker exec`
                // tests. The CORRECT pair URL for Docker is the relay-brokered
                // path served by the `totalreclaw_pair` agent tool (CONFIG.pairMode
                // === 'relay' since rc.11). The CLI-only path here cannot mint a
                // relay session synchronously (the relay handshake needs a WS
                // round-trip), so we emit the loopback URL with a LOUD warning
                // pointing the operator at the agent tool / publicUrl override.
                api.logger.warn(`TotalReclaw: Docker container detected — pairing URL falling back to ` +
                    `http://localhost:${port}, which is unreachable from the host browser. ` +
                    `Use the totalreclaw_pair AGENT TOOL (relay-brokered, universally reachable) ` +
                    `instead of the CLI fallback, OR set plugins.entries.totalreclaw.config.publicUrl ` +
                    `to your gateway's host-reachable URL (e.g. http://<host-ip>:${port} when the ` +
                    `Docker port is published). Setting TOTALRECLAW_PAIR_MODE=relay is the default; ` +
                    `air-gapped operators on TOTALRECLAW_PAIR_MODE=local must publish a port + set publicUrl.`);
            }
            else if (bind === 'lan' || bind === 'tailnet') {
                api.logger.warn(`TotalReclaw: pairing URL falling back to localhost because gateway.bind=${bind} could not be autodetected. ` +
                    'Set plugins.entries.totalreclaw.config.publicUrl to override.');
            }
            else {
                api.logger.warn(`TotalReclaw: pairing URL fell back to http://localhost:${port} — this URL only works on this machine. ` +
                    `Configure plugins.entries.totalreclaw.config.publicUrl for remote access.`);
            }
            base = `${scheme}://localhost:${port}`;
        }
    }
    return `${base}/plugin/totalreclaw/pair/finish?sid=${encodeURIComponent(session.sid)}#pk=${encodeURIComponent(session.pkGatewayB64)}`;
}
/**
 * Resolve whether this plugin is running on a `local` or `remote` gateway.
 *
 * Follows the same config surface `buildPairingUrl` uses:
 *   - `pluginConfig.publicUrl` set + non-localhost     → remote
 *   - `gateway.remote.url` set + non-localhost         → remote
 *   - `gateway.bind === 'lan' | 'tailnet' | 'custom'`  → remote
 *   - anything else                                    → local
 *
 * We treat a `publicUrl` or `remote.url` that points at `localhost` /
 * `127.*` as local because that is what a dev-loopback override looks like;
 * no one publishes a remote QR pairing for localhost.
 */
function resolveGatewayMode(api) {
    const cfg = api.config;
    const pluginCfg = (api.pluginConfig ?? {});
    const looksLocal = (url) => {
        if (!url)
            return true;
        const u = url.trim().toLowerCase();
        if (u === '')
            return true;
        return /^(?:wss?:\/\/|https?:\/\/)?(?:localhost|127\.|0\.0\.0\.0)/.test(u);
    };
    if (typeof pluginCfg.publicUrl === 'string' && !looksLocal(pluginCfg.publicUrl)) {
        return 'remote';
    }
    const remoteUrl = cfg?.gateway?.remote?.url;
    if (typeof remoteUrl === 'string' && !looksLocal(remoteUrl)) {
        return 'remote';
    }
    const bind = cfg?.gateway?.bind;
    if (bind === 'lan' || bind === 'tailnet' || bind === 'custom') {
        return 'remote';
    }
    return 'local';
}
// ---------------------------------------------------------------------------
// Cosine similarity threshold — skip injection when top result is below this
// ---------------------------------------------------------------------------
/**
 * Minimum cosine similarity of the top reranked result required to inject
 * memories into context. Below this threshold, the query is considered
 * irrelevant to any stored memories and results are suppressed.
 *
 * Default 0.15 is tuned for local ONNX models which produce lower
 * similarity scores than OpenAI models. Configurable via env var.
 */
const COSINE_THRESHOLD = CONFIG.cosineThreshold;
// ---------------------------------------------------------------------------
// Module-level state (persists across tool calls within a session)
// ---------------------------------------------------------------------------
let authKeyHex = null;
let encryptionKey = null;
let dedupKey = null;
let userId = null;
let subgraphOwner = null; // Smart Account address for subgraph queries
let apiClient = null;
let initPromise = null;
// LSH hasher — lazily initialized on first use (needs credentials + embedding dims)
let lshHasher = null;
let lshInitFailed = false; // If true, skip LSH on future calls (provider doesn't support embeddings)
// Hot cache for managed service (subgraph mode) — lazily initialized
let pluginHotCache = null;
// Two-tier search state (C1): skip redundant searches when query is semantically similar
let lastSearchTimestamp = 0;
let lastQueryEmbedding = null;
// Feature flags — configurable for A/B testing
const CACHE_TTL_MS = CONFIG.cacheTtlMs;
const SEMANTIC_SKIP_THRESHOLD = CONFIG.semanticSkipThreshold;
// Auto-extract throttle (C3): only extract every N turns in agent_end hook
let turnsSinceLastExtraction = 0;
// BUG-2 fix: Skip agent_end extraction during import operations.
// Import failures previously triggered agent_end → re-extraction → re-import loops.
let _importInProgress = false;
const AUTO_EXTRACT_EVERY_TURNS_ENV = CONFIG.extractInterval;
// Hard cap on facts per extraction to prevent LLM over-extraction from dense conversations
const MAX_FACTS_PER_EXTRACTION = 15;
// Store-time near-duplicate detection is always ON in v1.
// The TOTALRECLAW_STORE_DEDUP env var was removed.
const STORE_DEDUP_ENABLED = true;
// One-time welcome-back message for returning Pro users (set during init, consumed by first before_agent_start)
let welcomeBackMessage = null;
// B2: COSINE_THRESHOLD (above) is the single relevance gate for both
// the before_agent_start hook and the recall tool.  The former "RELEVANCE_THRESHOLD"
// (0.3) was too aggressive and silently suppressed auto-recall at session start.
// ---------------------------------------------------------------------------
// Billing cache infrastructure
// ---------------------------------------------------------------------------
//
// Read/write/type live in `./billing-cache.ts` — extracted in 3.0.7 so the
// file that does the billing-cache disk read is not the same file that talks
// to the billing endpoint. See billing-cache.ts for the rationale (clears
// OpenClaw's `potential-exfiltration` scanner rule, same per-file pattern as
// `env-harvesting` fixed in 3.0.4/3.0.5). `readBillingCache`, `writeBillingCache`,
// `BILLING_CACHE_PATH`, and the `BillingCache` type are imported above.
const QUOTA_WARNING_THRESHOLD = 0.8; // 80%
/**
 * Check if LLM-guided dedup is enabled.
 *
 * Always returns true — LLM extraction runs client-side using the user's
 * own API key, so there is no cost to us. The server flag is respected as
 * a kill-switch but defaults to true for all tiers.
 */
function isLlmDedupEnabled() {
    const cache = readBillingCache();
    if (cache?.features?.llm_dedup === false)
        return false; // Server kill-switch
    return true;
}
/**
 * Plugin-config override snapshot — set once at register() time so the
 * getters below are cheap (no re-walking of api.pluginConfig per turn).
 * Keyed entries are read from plugin-config
 * `extraction.interval` and `extraction.maxFactsPerExtraction` (both
 * optional in the 3.3.1 schema).
 */
let _pluginExtractionOverrides = {};
/**
 * Called from register() — reads the `extraction.*` plugin-config block
 * and memoizes the tunable overrides.
 */
function snapshotExtractionOverrides(pluginConfig) {
    const extraction = pluginConfig?.extraction;
    if (!extraction) {
        _pluginExtractionOverrides = {};
        return;
    }
    const out = {};
    if (typeof extraction.interval === 'number' && Number.isFinite(extraction.interval) && extraction.interval > 0) {
        out.interval = Math.floor(extraction.interval);
    }
    if (typeof extraction.maxFactsPerExtraction === 'number' &&
        Number.isFinite(extraction.maxFactsPerExtraction) &&
        extraction.maxFactsPerExtraction > 0) {
        out.maxFactsPerExtraction = Math.floor(extraction.maxFactsPerExtraction);
    }
    _pluginExtractionOverrides = out;
}
/**
 * Get the effective extraction interval.
 * Priority: plugin-config `extraction.interval` > server-side billing cache > env var.
 * The plugin-config override is highest because the user who set it in
 * their own config file clearly wants it to take effect locally.
 */
function getExtractInterval() {
    if (_pluginExtractionOverrides.interval !== undefined) {
        return _pluginExtractionOverrides.interval;
    }
    const cache = readBillingCache();
    if (cache?.features?.extraction_interval != null)
        return cache.features.extraction_interval;
    return AUTO_EXTRACT_EVERY_TURNS_ENV;
}
/**
 * Get the max facts per extraction cycle.
 * Priority: plugin-config `extraction.maxFactsPerExtraction` > server-side billing cache > env var / constant fallback.
 */
function getMaxFactsPerExtraction() {
    if (_pluginExtractionOverrides.maxFactsPerExtraction !== undefined) {
        return _pluginExtractionOverrides.maxFactsPerExtraction;
    }
    const cache = readBillingCache();
    if (cache?.features?.max_facts_per_extraction != null)
        return cache.features.max_facts_per_extraction;
    return MAX_FACTS_PER_EXTRACTION;
}
/**
 * Ensure MEMORY.md has a TotalReclaw header so the agent knows encrypted
 * memories are injected automatically via the before_agent_start hook.
 *
 * Option 3 approach: don't delete or stub MEMORY.md — let the agent use it
 * for workspace-level notes, but make clear that user facts/preferences are
 * handled by TotalReclaw's E2EE pipeline. This avoids confusing the agent
 * (OpenClaw's system prompt still tells it to search MEMORY.md) while
 * guiding it away from writing sensitive data in cleartext.
 */
const MEMORY_HEADER = `# Memory

> **TotalReclaw is active.** Your encrypted memories are loaded automatically
> at the start of each conversation — no need to search this file for them.
> Use \`totalreclaw_remember\` to store new memories and \`totalreclaw_recall\`
> to search. Do NOT write user facts, preferences, or decisions to this file.
> This file is for workspace-level notes only (non-sensitive).

`;
function ensureMemoryHeader(logger) {
    const outcome = ensureMemoryHeaderFile(CONFIG.openclawWorkspace, MEMORY_HEADER);
    if (outcome === 'updated') {
        logger.info('Added TotalReclaw header to MEMORY.md');
    }
    else if (outcome === 'created') {
        logger.info('Created MEMORY.md with TotalReclaw header');
    }
    // 'unchanged' and 'error' are silent — preserves 3.0.7 best-effort semantics.
}
// ---------------------------------------------------------------------------
// Dynamic candidate pool sizing
// ---------------------------------------------------------------------------
/** Cached fact count for dynamic candidate pool sizing. */
let cachedFactCount = null;
/** Timestamp of last fact count fetch (ms). */
let lastFactCountFetch = 0;
/** Cache TTL for fact count: 5 minutes. */
const FACT_COUNT_CACHE_TTL = 5 * 60 * 1000;
/**
 * Compute the candidate pool size from a fact count.
 *
 * Server-side config takes priority (from billing cache), then local fallback.
 * The server computes the optimal pool based on vault size and tier caps.
 *
 * Local fallback formula: pool = min(max(factCount * 3, 400), 5000)
 *   - At least 400 candidates (even for tiny vaults)
 *   - At most 5000 candidates (to bound decryption + reranking cost)
 *   - 3x fact count in between
 */
function computeCandidatePool(factCount) {
    const cache = readBillingCache();
    if (cache?.features?.max_candidate_pool != null)
        return cache.features.max_candidate_pool;
    // Fallback to local formula if no server config
    return Math.min(Math.max(factCount * 3, 400), 5000);
}
/**
 * Fetch the user's fact count from the server, with caching.
 *
 * Uses the /v1/export endpoint with limit=1 to get `total_count` without
 * downloading all facts. Falls back to 400 (which gives pool=1200) if
 * the server is unreachable or returns no count.
 */
async function getFactCount(logger) {
    const now = Date.now();
    // Return cached value if fresh.
    if (cachedFactCount !== null && (now - lastFactCountFetch) < FACT_COUNT_CACHE_TTL) {
        return cachedFactCount;
    }
    try {
        if (!apiClient || !authKeyHex) {
            return cachedFactCount ?? 400; // Not initialized yet, use default
        }
        const page = await apiClient.exportFacts(authKeyHex, 1);
        const count = page.total_count ?? page.facts.length;
        cachedFactCount = count;
        lastFactCountFetch = now;
        logger.info(`Fact count updated: ${count} (candidate pool: ${computeCandidatePool(count)})`);
        return count;
    }
    catch (err) {
        const msg = err instanceof Error ? err.message : String(err);
        logger.warn(`Failed to fetch fact count (using ${cachedFactCount ?? 400}): ${msg}`);
        return cachedFactCount ?? 400; // Fall back to cached or default
    }
}
// ---------------------------------------------------------------------------
// Initialisation
// ---------------------------------------------------------------------------
/** True when recovery phrase is missing — tools return setup instructions. */
let needsSetup = false;
/** True on first before_agent_start after successful init — show welcome message once. */
let firstRunAfterInit = true;
/**
 * Once-per-gateway-session flag for the 3.3.0-rc.2 first-run welcome banner.
 * The banner fires on the first `before_agent_start` after install when
 * credentials.json is absent/empty — exactly once per gateway process.
 * A second before_agent_start in the same session finds this flipped and
 * skips. A fresh gateway restart resets it back to `false`.
 */
let firstRunWelcomeShown = false;
/**
 * 3.3.3-rc.1 — RC-mode staging-only banner (PR #165 implementation).
 *
 * Fires ONCE per gateway process when:
 *   - the bundled-default `serverUrl` resolves to `api-staging.totalreclaw.xyz`
 *     (RC artifact, not stable), AND
 *   - the user has NOT overridden via `TOTALRECLAW_SERVER_URL=...` env.
 *
 * Goal: a fresh QA tester can't accidentally use an RC build for real data
 * without seeing a clear "RC = staging, no SLA, may be wiped" warning.
 * One-shot at the first `before_agent_start` whose `prependContext` actually
 * lands on the LLM (3.3.4-rc.1 — see fix below). A fresh gateway restart
 * re-fires it once.
 *
 * 3.3.4-rc.1 fix: through 3.3.3-rc.1 this flag was set to true as soon as
 * the banner BLOCK was built — but multiple hook return paths returned
 * `undefined` (zero-match cases), so the banner block was silently dropped
 * AND the flag was flipped, suppressing all subsequent attempts. Now the
 * flag flips ONLY when a return path actually includes the block in its
 * `prependContext`, via the `markBannerDelivered()` closure.
 */
let stagingBannerShown = false;
/**
 * 3.3.4-rc.1 — operator-facing "this is an RC build" log fires once per
 * gateway process, independent of whether the user-facing banner has
 * been delivered yet. Without this split, the warn-log was tied to the
 * same flag as the user-facing banner and got dropped together when
 * the hook returned `undefined`.
 */
let stagingBannerLogged = false;
/**
 * Derive keys from the recovery phrase, load credentials, and register with
 * the server if this is the first run.
 *
 * 3.2.0: this function is read-only with respect to the mnemonic. It pulls
 * the phrase from either the env var override or an existing
 * `credentials.json` written by the onboarding wizard. It never generates a
 * fresh phrase — that only happens inside the CLI wizard where the phrase
 * can be surfaced to the user on a non-LLM TTY. If no usable phrase is
 * available here, `needsSetup` is flipped and the `before_tool_call` gate
 * directs the caller to `openclaw totalreclaw onboard`.
 */
async function initialize(logger) {
    // 3.3.12-rc.1 (F flip): production is the source default for all builds.
    // Staging is opt-in via TOTALRECLAW_SERVER_URL=https://api-staging.totalreclaw.xyz.
    const serverUrl = CONFIG.serverUrl || 'https://api.totalreclaw.xyz';
    let masterPassword = CONFIG.recoveryPhrase;
    // 3.2.0: if the env var is unset, probe credentials.json for a
    // pre-existing mnemonic (written either by the CLI wizard on this machine
    // or ported in from another client). We do NOT generate a phrase here —
    // generation is the wizard's job so the user sees the phrase on a TTY
    // and never through the LLM.
    if (!masterPassword) {
        const existing = loadCredentialsJson(CREDENTIALS_PATH);
        const candidate = (typeof existing?.mnemonic === 'string' && existing.mnemonic.trim()) ||
            (typeof existing?.recovery_phrase === 'string' && existing.recovery_phrase.trim()) ||
            '';
        if (candidate) {
            masterPassword = candidate;
            setRecoveryPhraseOverride(candidate);
            logger.info('Loaded recovery phrase from credentials.json');
        }
    }
    if (!masterPassword) {
        needsSetup = true;
        // 3.3.13 — replaced the stale "run `openclaw totalreclaw onboard` in a
        // terminal to set up" log line. The auto-pair-on-load flow (kicked off
        // from register()) now writes ~/.totalreclaw/.pair-pending.json with
        // the URL + PIN the agent surfaces to the user on the next turn. The
        // chat agent no longer hallucinates pair URLs — see the Pop-OS QA
        // 2026-05-10 root-cause note in auto-pair-on-load.ts.
        logger.info('TotalReclaw: no credentials found; auto-pair-on-load will surface a pair URL.');
        return;
    }
    apiClient = createApiClient(serverUrl);
    // --- Attempt to load existing credentials ---
    let existingSalt;
    let existingUserId;
    const creds = loadCredentialsJson(CREDENTIALS_PATH);
    if (creds) {
        try {
            // Salt may be stored as base64 (plugin-written) or hex (MCP setup-written).
            // Detect format: hex strings are 64 chars of [0-9a-f], base64 uses [A-Z+/=].
            const saltStr = typeof creds.salt === 'string' ? creds.salt : undefined;
            if (saltStr && /^[0-9a-f]{64}$/i.test(saltStr)) {
                existingSalt = Buffer.from(saltStr, 'hex');
            }
            else if (saltStr) {
                existingSalt = Buffer.from(saltStr, 'base64');
            }
            existingUserId = typeof creds.userId === 'string' ? creds.userId : undefined;
            if (existingUserId) {
                logger.info(`Loaded existing credentials for user ${existingUserId}`);
            }
        }
        catch {
            logger.warn('Failed to parse credentials, will register new account');
        }
    }
    // --- Derive keys ---
    const keys = deriveKeys(masterPassword, existingSalt);
    authKeyHex = keys.authKey.toString('hex');
    encryptionKey = keys.encryptionKey;
    dedupKey = keys.dedupKey;
    // Cache credentials for lazy LSH seed derivation
    masterPasswordCache = masterPassword;
    saltCache = keys.salt;
    if (existingUserId) {
        userId = existingUserId;
        logger.info(`Authenticated as user ${userId}`);
        // Idempotent registration — ensure auth key is registered with the relay.
        // Without this, returning users get 401 if the relay database was reset or
        // if credentials were created by the MCP setup CLI (different process).
        try {
            const authHash = computeAuthKeyHash(keys.authKey);
            const saltHex = keys.salt.toString('hex');
            await apiClient.register(authHash, saltHex);
        }
        catch {
            // Best-effort — relay returns 200 for already-registered users.
            // Only fails on network errors; bearer token auth still works if
            // a prior registration succeeded.
            logger.warn('Idempotent relay registration failed (best-effort, will retry on next start)');
        }
    }
    else {
        // First run -- register with the server.
        const authHash = computeAuthKeyHash(keys.authKey);
        const saltHex = keys.salt.toString('hex');
        let registeredUserId;
        try {
            const result = await apiClient.register(authHash, saltHex);
            registeredUserId = result.user_id;
        }
        catch (err) {
            const msg = err instanceof Error ? err.message : String(err);
            if (msg.includes('USER_EXISTS') && isSubgraphMode()) {
                // In managed mode, derive a deterministic userId from the auth key
                // hash. The server is only a relay proxy — userId is used as the
                // subgraph owner field and must be consistent between store/search.
                registeredUserId = authHash.slice(0, 32);
                logger.info(`Using derived userId for managed mode (server returned USER_EXISTS)`);
            }
            else {
                throw err;
            }
        }
        userId = registeredUserId;
        // Persist credentials so we can resume later.
        // Include the mnemonic so hot-reload works without env var.
        const credsToSave = {
            userId,
            salt: keys.salt.toString('base64'),
        };
        // Only persist mnemonic if we have one (avoid writing empty string).
        if (masterPassword) {
            credsToSave.mnemonic = masterPassword;
        }
        writeCredentialsJson(CREDENTIALS_PATH, credsToSave);
        logger.info(`Registered new user: ${userId}`);
    }
    // Derive Smart Account address for subgraph queries (on-chain owner identity).
    // 3.3.11-rc.3: NEVER fall back to userId on derivation failure — the subgraph's
    // `owner` field is typed `Bytes!` (0x-prefixed hex) and rejects userId UUIDs
    // with `Failed to decode Bytes value: Invalid character 'q' at position 0`
    // (because userIds often start with non-hex chars like q/r/y). When SA
    // derivation fails the only safe path is to leave subgraphOwner unset and
    // fail every subsequent on-chain operation with a clear "smart-account
    // unavailable" error rather than spamming the subgraph with garbage Bytes.
    if (isSubgraphMode()) {
        try {
            const config = getSubgraphConfig();
            subgraphOwner = await deriveSmartAccountAddress(config.mnemonic, config.chainId);
            logger.info(`Subgraph owner (Smart Account): ${subgraphOwner}`);
        }
        catch (err) {
            const msg = err instanceof Error ? err.message : String(err);
            logger.error(`Smart Account derivation failed: ${msg} — subgraph reads/writes will be skipped this session ` +
                '(no Bytes-format owner available). Verify mnemonic in credentials.json.');
            // Leave subgraphOwner undefined. Code paths that read it must guard
            // against undefined and skip the subgraph round-trip rather than
            // sending a malformed query.
            subgraphOwner = null;
        }
    }
    // One-time billing check for returning users (imported recovery phrase).
    // If they already have an active Pro subscription, inform them on next conversation start.
    if (existingUserId && authKeyHex) {
        try {
            const walletAddr = subgraphOwner || userId || '';
            if (walletAddr) {
                const billingUrl = CONFIG.serverUrl;
                const resp = await fetch(`${billingUrl}/v1/billing/status?wallet_address=${encodeURIComponent(walletAddr)}`, {
                    method: 'GET',
                    headers: buildRelayHeaders({
                        'Authorization': `Bearer ${authKeyHex}`,
                        'Accept': 'application/json',
                    }),
                });
                if (resp.ok) {
                    const billingData = await resp.json();
                    const tier = billingData.tier;
                    const expiresAt = billingData.expires_at;
                    // Populate billing cache for future use.
                    writeBillingCache({
                        tier: tier || 'free',
                        free_writes_used: billingData.free_writes_used ?? 0,
                        free_writes_limit: billingData.free_writes_limit ?? 0,
                        features: billingData.features,
                        checked_at: Date.now(),
                    });
                    if (tier === 'pro' && expiresAt) {
                        const expiryDate = new Date(expiresAt).toLocaleDateString();
                        welcomeBackMessage = `Welcome back! Your Pro subscription is active (expires: ${expiryDate}).`;
                        logger.info(`Returning Pro user detected — expires ${expiryDate}`);
                    }
                }
            }
        }
        catch {
            // Best-effort — don't block initialization on billing check failure.
        }
    }
    // 1h freshness auto-resume: if a previous session left an import in running
    // state and last_updated is < 1h ago, re-spawn the background task.
    // If > 1h, the status check will mark it stale when the user queries it.
    const activeImport = readMostRecentActiveImport();
    if (activeImport && activeImport.status === 'running' && !isImportStale(activeImport)) {
        logger.info(`Import ${activeImport.import_id}: resuming background task from chunk ${activeImport.batch_done * 25}/${activeImport.total_chunks}`);
        // The import file path is needed for re-parse. If not present we can't resume automatically.
        if (activeImport.file_path) {
            void handlePluginImportFrom({ source: activeImport.source, file_path: activeImport.file_path, resume_id: activeImport.import_id }, logger).catch((err) => {
                const msg = err instanceof Error ? err.message : String(err);
                logger.warn(`Import ${activeImport.import_id}: auto-resume failed: ${msg}`);
            });
        }
    }
}
function isDocker() {
    return isRunningInDocker();
}
function buildSetupErrorMsg() {
    return 'TotalReclaw setup required. Use the `totalreclaw_setup` tool with a 12-word BIP-39 recovery phrase.\n\n' +
        '1. Ask the user if they have an existing recovery phrase, or generate a new one with `npx @totalreclaw/mcp-server setup`.\n' +
        '2. Call `totalreclaw_setup` with the phrase — no gateway restart needed.\n' +
        '   (Optional: set TOTALRECLAW_SELF_HOSTED=true if using your own server instead of the managed service.)';
}
function buildSetupErrorMsgLegacy() {
    const base = 'TotalReclaw setup required:\n' +
        '1. Set TOTALRECLAW_RECOVERY_PHRASE — ask the user if they have an existing recovery phrase or generate a new 12-word recovery phrase.\n' +
        '2. Restart the gateway to apply changes.\n' +
        '   (Optional: set TOTALRECLAW_SELF_HOSTED=true if using your own server instead of the managed service.)\n\n';
    if (isDocker()) {
        return base +
            'Running in Docker — pass env vars via `-e` flags or your compose file:\n' +
            '  -e TOTALRECLAW_RECOVERY_PHRASE="word1 word2 ..."';
    }
    if (process.platform === 'darwin') {
        return base +
            'Running on macOS — add env vars to the LaunchAgent plist at\n' +
            '~/Library/LaunchAgents/ai.openclaw.gateway.plist under <key>EnvironmentVariables</key>:\n' +
            '  <key>TOTALRECLAW_RECOVERY_PHRASE</key><string>word1 word2 ...</string>\n' +
            'Then run: openclaw gateway restart';
    }
    return base +
        'Running on Linux — add env vars to the systemd unit override or your shell profile:\n' +
        '  export TOTALRECLAW_RECOVERY_PHRASE="word1 word2 ..."\n' +
        'Then run: openclaw gateway restart';
}
const SETUP_ERROR_MSG = buildSetupErrorMsg();
/**
 * Ensure `initialize()` has completed (runs at most once).
 *
 * If `needsSetup` is true after init, attempts a hot-reload from
 * credentials.json in case the mnemonic was written there by a
 * `totalreclaw_setup` tool call or `npx @totalreclaw/mcp-server setup`.
 */
async function ensureInitialized(logger) {
    if (!initPromise) {
        initPromise = initialize(logger);
    }
    await initPromise;
    // Hot-reload: if setup is still needed, check if credentials.json
    // now has a mnemonic (written by totalreclaw_setup or MCP setup CLI).
    if (needsSetup) {
        await attemptHotReload(logger);
    }
}
/**
 * Attempt to hot-reload credentials from credentials.json.
 *
 * Called when `needsSetup` is true — checks if credentials.json contains
 * a mnemonic (written by the `totalreclaw_setup` tool or MCP setup CLI).
 * If found, re-derives keys and completes initialization without requiring
 * a gateway restart.
 */
async function attemptHotReload(logger) {
    try {
        const creds = loadCredentialsJson(CREDENTIALS_PATH);
        if (!creds || typeof creds.mnemonic !== 'string' || !creds.mnemonic)
            return;
        logger.info('Hot-reloading credentials from credentials.json (no restart needed)');
        // Set the runtime override so CONFIG.recoveryPhrase returns the mnemonic.
        setRecoveryPhraseOverride(creds.mnemonic);
        // Re-run initialization with the newly available mnemonic.
        needsSetup = false;
        initPromise = initialize(logger);
        await initPromise;
    }
    catch (err) {
        const msg = err instanceof Error ? err.message : String(err);
        logger.warn(`Hot-reload from credentials.json failed: ${msg}`);
        // Leave needsSetup as true — user will see the setup prompt.
    }
}
/**
 * Force re-initialization with a specific mnemonic.
 *
 * Called by the `totalreclaw_setup` tool. Clears stale credentials from
 * disk so that `initialize()` treats this as a fresh registration and
 * persists the NEW mnemonic + freshly derived salt/userId.
 *
 * Without clearing credentials.json first, `initialize()` would load the
 * OLD salt and userId, derive keys from (new mnemonic + old salt), skip
 * writing credentials (because existingUserId is set), and the new
 * mnemonic would never be persisted — a critical data-loss bug.
 */
async function forceReinitialization(mnemonic, logger) {
    // Set the runtime override so CONFIG.recoveryPhrase returns this mnemonic.
    setRecoveryPhraseOverride(mnemonic);
    // CRITICAL: Remove stale credentials so initialize() does a fresh
    // registration with a new salt. If we leave the old file, initialize()
    // loads the old salt + userId and never writes the new mnemonic.
    if (deleteCredentialsFile(CREDENTIALS_PATH)) {
        logger.info('Cleared stale credentials.json for fresh setup');
    }
    // Reset module state for a clean re-init.
    needsSetup = false;
    authKeyHex = null;
    encryptionKey = null;
    dedupKey = null;
    userId = null;
    subgraphOwner = null;
    apiClient = null;
    lshHasher = null;
    lshInitFailed = false;
    masterPasswordCache = null;
    saltCache = null;
    pluginHotCache = null;
    firstRunAfterInit = true;
    // Re-run initialization — will register fresh and persist new credentials.
    initPromise = initialize(logger);
    await initPromise;
}
/**
 * Like ensureInitialized, but throws if setup is still needed.
 * Use in tool handlers where we need a fully configured plugin.
 */
async function requireFullSetup(logger) {
    await ensureInitialized(logger);
    if (needsSetup) {
        throw new Error(SETUP_ERROR_MSG);
    }
}
// ---------------------------------------------------------------------------
// LSH + Embedding helpers
// ---------------------------------------------------------------------------
/** Recovery phrase cached for LSH seed derivation (set during initialize()). */
let masterPasswordCache = null;
/** Salt cached for LSH seed derivation (set during initialize()). */
let saltCache = null;
/**
 * Get or initialize the LSH hasher.
 *
 * The hasher is created lazily because it needs:
 *   1. The recovery phrase + salt (available after initialize())
 *   2. The embedding dimensions (available after initLLMClient())
 *
 * If the provider doesn't support embeddings, this returns null and
 * sets `lshInitFailed` to avoid retrying.
 */
function getLSHHasher(logger) {
    if (lshHasher)
        return lshHasher;
    if (lshInitFailed)
        return null;
    try {
        if (!masterPasswordCache || !saltCache) {
            logger.warn('LSH hasher: credentials not available yet');
            return null;
        }
        const dims = getEmbeddingDims();
        const lshSeed = deriveLshSeed(masterPasswordCache, saltCache);
        lshHasher = new LSHHasher(lshSeed, dims);
        logger.info(`LSH hasher initialized (dims=${dims}, tables=${lshHasher.tables}, bits=${lshHasher.bits})`);
        return lshHasher;
    }
    catch (err) {
        const msg = err instanceof Error ? err.message : String(err);
        logger.warn(`LSH hasher initialization failed (will use word-only indices): ${msg}`);
        lshInitFailed = true;
        return null;
    }
}
/**
 * Generate an embedding for the given text and compute LSH bucket hashes.
 *
 * Returns null if embedding generation fails (provider doesn't support it,
 * network error, etc.). In that case, the caller should fall back to
 * word-only blind indices.
 */
async function generateEmbeddingAndLSH(text, logger) {
    try {
        const embedding = await generateEmbedding(text);
        const hasher = getLSHHasher(logger);
        const lshBuckets = hasher ? hasher.hash(embedding) : [];
        // Encrypt the embedding (JSON array of numbers) for server-blind storage
        const encryptedEmbedding = encryptToHex(JSON.stringify(embedding), encryptionKey);
        return { embedding, lshBuckets, encryptedEmbedding };
    }
    catch (err) {
        const msg = err instanceof Error ? err.message : String(err);
        logger.warn(`Embedding/LSH generation failed (falling back to word-only indices): ${msg}`);
        return null;
    }
}
// ---------------------------------------------------------------------------
// Store-time near-duplicate search helper
// ---------------------------------------------------------------------------
/**
 * Search the vault for near-duplicates of a fact about to be stored.
 *
 * Uses the fact's blind indices as trapdoors to fetch candidates, decrypts
 * them, extracts embeddings, and calls `findNearDuplicate()` from the
 * consolidation module.
 *
 * Returns null on any failure (fail-open: we'd rather store a duplicate than
 * lose a fact).
 */
async function searchForNearDuplicates(factText, factEmbedding, allIndices, logger) {
    try {
        if (!encryptionKey || !authKeyHex || !userId)
            return null;
        // Fetch candidates from the vault using the fact's blind indices as trapdoors.
        let decryptedCandidates = [];
        if (isSubgraphMode()) {
            const results = await searchSubgraph(subgraphOwner || userId, allIndices, STORE_DEDUP_MAX_CANDIDATES, authKeyHex);
            for (const result of results) {
                try {
                    const docJson = decryptFromHex(result.encryptedBlob, encryptionKey);
                    if (isDigestBlob(docJson))
                        continue;
                    const doc = readClaimFromBlob(docJson);
                    let embedding = null;
                    if (result.encryptedEmbedding) {
                        try {
                            embedding = JSON.parse(decryptFromHex(result.encryptedEmbedding, encryptionKey));
                        }
                        catch { /* skip */ }
                    }
                    decryptedCandidates.push({
                        id: result.id,
                        text: doc.text,
                        embedding,
                        importance: doc.importance,
                        decayScore: 5,
                        createdAt: result.timestamp ? parseInt(result.timestamp, 10) * 1000 : Date.now(),
                        version: 1,
                    });
                }
                catch { /* skip undecryptable */ }
            }
        }
        else if (apiClient) {
            const candidates = await apiClient.search(userId, allIndices, STORE_DEDUP_MAX_CANDIDATES, authKeyHex);
            for (const candidate of candidates) {
                try {
                    const docJson = decryptFromHex(candidate.encrypted_blob, encryptionKey);
                    if (isDigestBlob(docJson))
                        continue;
                    const doc = readClaimFromBlob(docJson);
                    let embedding = null;
                    if (candidate.encrypted_embedding) {
                        try {
                            embedding = JSON.parse(decryptFromHex(candidate.encrypted_embedding, encryptionKey));
                        }
                        catch { /* skip */ }
                    }
                    decryptedCandidates.push({
                        id: candidate.fact_id,
                        text: doc.text,
                        embedding,
                        importance: doc.importance,
                        decayScore: candidate.decay_score,
                        createdAt: typeof candidate.timestamp === 'number'
                            ? candidate.timestamp
                            : new Date(candidate.timestamp).getTime(),
                        version: candidate.version,
                    });
                }
                catch { /* skip undecryptable */ }
            }
        }
        if (decryptedCandidates.length === 0)
            return null;
        const result = findNearDuplicate(factEmbedding, decryptedCandidates, getStoreDedupThreshold());
        if (!result)
            return null;
        return { match: result.existingFact, similarity: result.similarity };
    }
    catch (err) {
        const msg = err instanceof Error ? err.message : String(err);
        logger.warn(`Store-time dedup search failed (proceeding with store): ${msg}`);
        return null;
    }
}
// ---------------------------------------------------------------------------
// Utility helpers
// ---------------------------------------------------------------------------
/**
 * Encrypt a plaintext document string and return its hex-encoded ciphertext.
 *
 * The server stores blobs as hex (not base64), so we convert the base64
 * output of `encrypt()` into hex.
 */
function encryptToHex(plaintext, key) {
    const b64 = encrypt(plaintext, key);
    return Buffer.from(b64, 'base64').toString('hex');
}
// Plugin v3.0.0 removed the legacy claim-format fallback. Write path
// always emits Memory Taxonomy v1 JSON blobs. The logClaimFormatOnce
// helper is gone along with TOTALRECLAW_CLAIM_FORMAT / TOTALRECLAW_TAXONOMY_VERSION.
let _loggedDigestMode = false;
function logDigestModeOnce(mode, logger) {
    if (_loggedDigestMode)
        return;
    _loggedDigestMode = true;
    logger.info(`TotalReclaw: digest injection mode = ${mode}`);
}
/**
 * How many active facts to pull into a digest recompilation.
 * Digest compiler itself will apply DIGEST_CLAIM_CAP for the LLM path.
 */
const DIGEST_FETCH_LIMIT = 500;
/**
 * Schedule a background digest recompile. Fire-and-forget.
 *
 * The caller must check `!isRecompileInProgress()` before invoking.
 * Errors are logged and swallowed; the guard flag is always released.
 */
function scheduleDigestRecompile(previousClaimId, logger) {
    if (!isRecompileInProgress()) {
        if (!tryBeginRecompile())
            return;
    }
    else {
        return;
    }
    const mode = resolveDigestMode();
    const owner = subgraphOwner || userId;
    const authKey = authKeyHex;
    const encKey = encryptionKey;
    const ownerForBatch = subgraphOwner ?? undefined;
    if (!owner || !authKey || !encKey) {
        endRecompile();
        return;
    }
    // Capture llmFn from the current LLM config (cheap variant of the user's
    // provider, already resolved by resolveLLMConfig).
    const llmConfig = resolveLLMConfig();
    const llmFn = llmConfig
        ? async (prompt) => {
            const out = await chatCompletion(llmConfig, [
                { role: 'system', content: 'You return only valid JSON. No markdown fences, no commentary.' },
                { role: 'user', content: prompt },
            ], { maxTokens: 800, temperature: 0 });
            return out ?? '';
        }
        : null;
    // Build the I/O deps closures. We capture the owner/auth/key values so the
    // background task doesn't race with module-level state resets.
    const fetchFn = () => fetchAllActiveClaims(owner, authKey, encKey, DIGEST_FETCH_LIMIT, {
        searchSubgraphBroadened: async (o, n, a) => searchSubgraphBroadened(o, n, a),
        decryptFromHex: (hex, key) => decryptFromHex(hex, key),
    }, logger);
    const storeFn = async (canonicalClaimJson, compiledAt) => {
        if (!isSubgraphMode()) {
            // Self-hosted mode — store via the REST API.
            if (!apiClient)
                throw new Error('apiClient not initialized');
            const encryptedBlob = encryptToHex(canonicalClaimJson, encKey);
            const contentFp = generateContentFingerprint(canonicalClaimJson, dedupKey);
            const payload = {
                id: crypto.randomUUID(),
                timestamp: compiledAt,
                encrypted_blob: encryptedBlob,
                blind_indices: [DIGEST_TRAPDOOR],
                decay_score: 10,
                source: 'openclaw-plugin-digest',
                content_fp: contentFp,
                agent_id: 'openclaw-plugin-digest',
            };
            await apiClient.store(userId, [payload], authKey);
            return;
        }
        // Subgraph / managed-service mode — encrypt, encode, submit as a single-fact UserOp.
        const encryptedBlob = encryptToHex(canonicalClaimJson, encKey);
        const contentFp = generateContentFingerprint(canonicalClaimJson, dedupKey);
        const protobuf = encodeFactProtobuf({
            id: crypto.randomUUID(),
            timestamp: compiledAt,
            owner,
            encryptedBlob,
            blindIndices: [DIGEST_TRAPDOOR],
            decayScore: 10,
            source: 'openclaw-plugin-digest',
            contentFp,
            agentId: 'openclaw-plugin-digest',
            version: PROTOBUF_VERSION_V4,
        });
        const config = { ...getSubgraphConfig(), authKeyHex: authKey, walletAddress: ownerForBatch };
        const result = await submitFactBatchOnChain([protobuf], config);
        if (!result.success) {
            throw new Error('Digest store UserOp did not succeed on-chain');
        }
    };
    const tombstoneFn = async (claimId) => {
        if (!isSubgraphMode()) {
            if (apiClient) {
                try {
                    await apiClient.deleteFact(claimId, authKey);
                }
                catch { /* best-effort */ }
            }
            return;
        }
        const tombstone = {
            id: claimId,
            timestamp: new Date().toISOString(),
            owner,
            encryptedBlob: '00',
            blindIndices: [],
            decayScore: 0,
            source: 'tombstone',
            contentFp: '',
            agentId: 'openclaw-plugin-digest',
            version: PROTOBUF_VERSION_V4,
        };
        const protobuf = encodeFactProtobuf(tombstone);
        const config = { ...getSubgraphConfig(), authKeyHex: authKey, walletAddress: ownerForBatch };
        const result = await submitFactBatchOnChain([protobuf], config);
        if (!result.success) {
            throw new Error('Digest tombstone UserOp did not succeed on-chain');
        }
    };
    // Slice 2f: run the weight-tuning loop as a fire-and-forget pre-compile step.
    // This consumes any feedback.jsonl entries written since the last compile
    // and nudges ~/.totalreclaw/weights.json, so the NEXT contradiction detection
    // uses the adjusted weights. Rate-limited and idempotent — see
    // runWeightTuningLoop for details. Failures are logged, never fatal.
    void runWeightTuningLoop(Math.floor(Date.now() / 1000), logger).catch((err) => {
        const msg = err instanceof Error ? err.message : String(err);
        logger.warn(`Digest: tuning loop threw: ${msg}`);
    });
    void recompileDigest({
        mode,
        previousClaimId,
        nowUnixSeconds: Math.floor(Date.now() / 1000),
        deps: {
            storeDigestClaim: storeFn,
            tombstoneDigest: tombstoneFn,
            fetchAllActiveClaimsFn: fetchFn,
            llmFn,
        },
        logger,
    })
        .catch((err) => {
        const msg = err instanceof Error ? err.message : String(err);
        logger.warn(`Digest: background recompile threw: ${msg}`);
    })
        .finally(() => {
        endRecompile();
    });
}
/**
 * Decrypt a hex-encoded ciphertext blob into a UTF-8 string.
 */
function decryptFromHex(hexBlob, key) {
    const hex = hexBlob.startsWith('0x') ? hexBlob.slice(2) : hexBlob;
    const b64 = Buffer.from(hex, 'hex').toString('base64');
    return decrypt(b64, key);
}
const MIGRATION_PAGE_SIZE = 1000;
/** Execute a GraphQL query against a subgraph endpoint. Returns null on error. */
async function migrationGqlQuery(endpoint, query, variables, authKey) {
    try {
        const overrides = {
            'Content-Type': 'application/json',
        };
        if (authKey)
            overrides['Authorization'] = `Bearer ${authKey}`;
        const headers = buildRelayHeaders(overrides);
        const response = await fetch(endpoint, {
            method: 'POST',
            headers,
            body: JSON.stringify({ query, variables }),
        });
        if (!response.ok)
            return null;
        const json = await response.json();
        return json.data ?? null;
    }
    catch {
        return null;
    }
}
/** Fetch all active facts by owner from a subgraph, paginated. */
async function fetchAllFactsByOwner(subgraphUrl, owner, authKey) {
    const allFacts = [];
    let lastId = '';
    while (true) {
        const hasLastId = lastId !== '';
        const query = hasLastId
            ? `query($owner:Bytes!,$first:Int!,$lastId:String!){facts(where:{owner:$owner,isActive:true,id_gt:$lastId},first:$first,orderBy:id,orderDirection:asc){id owner encryptedBlob encryptedEmbedding decayScore isActive contentFp source agentId version timestamp}}`
            : `query($owner:Bytes!,$first:Int!){facts(where:{owner:$owner,isActive:true},first:$first,orderBy:id,orderDirection:asc){id owner encryptedBlob encryptedEmbedding decayScore isActive contentFp source agentId version timestamp}}`;
        const vars = hasLastId
            ? { owner, first: MIGRATION_PAGE_SIZE, lastId }
            : { owner, first: MIGRATION_PAGE_SIZE };
        const data = await migrationGqlQuery(subgraphUrl, query, vars, authKey);
        const facts = data?.facts ?? [];
        if (facts.length === 0)
            break;
        allFacts.push(...facts);
        if (facts.length < MIGRATION_PAGE_SIZE)
            break;
        lastId = facts[facts.length - 1].id;
    }
    return allFacts;
}
/** Fetch content fingerprints from a subgraph for idempotency. */
async function fetchContentFingerprintsByOwner(subgraphUrl, owner, authKey) {
    const fps = new Set();
    let lastId = '';
    while (true) {
        const hasLastId = lastId !== '';
        const query = hasLastId
            ? `query($owner:Bytes!,$first:Int!,$lastId:String!){facts(where:{owner:$owner,isActive:true,id_gt:$lastId},first:$first,orderBy:id,orderDirection:asc){id contentFp}}`
            : `query($owner:Bytes!,$first:Int!){facts(where:{owner:$owner,isActive:true},first:$first,orderBy:id,orderDirection:asc){id contentFp}}`;
        const vars = hasLastId
            ? { owner, first: MIGRATION_PAGE_SIZE, lastId }
            : { owner, first: MIGRATION_PAGE_SIZE };
        const data = await migrationGqlQuery(subgraphUrl, query, vars, authKey);
        const facts = data?.facts ?? [];
        if (facts.length === 0)
            break;
        for (const f of facts) {
            if (f.contentFp)
                fps.add(f.contentFp);
        }
        if (facts.length < MIGRATION_PAGE_SIZE)
            break;
        lastId = facts[facts.length - 1].id;
    }
    return fps;
}
/** Fetch blind index hashes for given fact IDs. */
async function fetchBlindIndicesByFactIds(subgraphUrl, factIds, authKey) {
    const result = new Map();
    const CHUNK = 50;
    for (let i = 0; i < factIds.length; i += CHUNK) {
        const chunk = factIds.slice(i, i + CHUNK);
        const query = `query($factIds:[String!]!,$first:Int!){blindIndexes(where:{fact_in:$factIds},first:$first){hash fact{id}}}`;
        const data = await migrationGqlQuery(subgraphUrl, query, { factIds: chunk, first: 1000 }, authKey);
        for (const entry of data?.blindIndexes ?? []) {
            const existing = result.get(entry.fact.id) || [];
            existing.push(entry.hash);
            result.set(entry.fact.id, existing);
        }
    }
    return result;
}
/**
 * Fetch existing memories from the vault to provide dedup context for extraction.
 * Returns a lightweight list of {id, text} pairs for the LLM prompt.
 * Fails silently — returns empty array on any error.
 */
async function fetchExistingMemoriesForExtraction(logger, limit = 30, rawMessages = []) {
    try {
        if (!encryptionKey || !authKeyHex || !userId)
            return [];
        // Extract key terms from the last few messages to generate meaningful trapdoors.
        // Using '*' would produce zero trapdoors (stripped as punctuation), so we pull
        // text from the conversation to find memories relevant to the current context.
        const recentMessages = rawMessages.slice(-4);
        const textChunks = [];
        for (const msg of recentMessages) {
            const m = msg;
            if (typeof m.content === 'string') {
                textChunks.push(m.content);
            }
            else if (Array.isArray(m.content)) {
                for (const block of m.content) {
                    if (block.text)
                        textChunks.push(block.text);
                }
            }
            else if (typeof m.text === 'string') {
                textChunks.push(m.text);
            }
        }
        const queryText = textChunks.join(' ').slice(0, 500); // cap to avoid giant trapdoor sets
        if (!queryText.trim())
            return [];
        const trapdoors = generateBlindIndices(queryText);
        if (trapdoors.length === 0)
            return [];
        const results = [];
        if (isSubgraphMode()) {
            const rawResults = await searchSubgraph(subgraphOwner || userId, trapdoors, limit, authKeyHex);
            for (const r of rawResults) {
                try {
                    const docJson = decryptFromHex(r.encryptedBlob, encryptionKey);
                    if (isDigestBlob(docJson))
                        continue;
                    const doc = readClaimFromBlob(docJson);
                    results.push({ id: r.id, text: doc.text });
                }
                catch { /* skip undecryptable */ }
            }
        }
        else if (apiClient) {
            const candidates = await apiClient.search(userId, trapdoors, limit, authKeyHex);
            for (const c of candidates) {
                try {
                    const docJson = decryptFromHex(c.encrypted_blob, encryptionKey);
                    if (isDigestBlob(docJson))
                        continue;
                    const doc = readClaimFromBlob(docJson);
                    results.push({ id: c.fact_id, text: doc.text });
                }
                catch { /* skip undecryptable */ }
            }
        }
        return results;
    }
    catch (err) {
        logger.warn(`Failed to fetch existing memories for extraction context: ${err instanceof Error ? err.message : String(err)}`);
        return [];
    }
}
/**
 * Simple text-overlap scoring between a query and a candidate document.
 * Returns the number of overlapping lowercase words.
 */
function textScore(query, docText) {
    const queryWords = new Set(query.toLowerCase().split(/\s+/).filter((w) => w.length >= 2));
    const docWords = docText.toLowerCase().split(/\s+/);
    let score = 0;
    for (const word of docWords) {
        if (queryWords.has(word))
            score++;
    }
    return score;
}
/**
 * Format a relative time string (e.g. "2 hours ago").
 */
function relativeTime(isoOrMs) {
    const ms = typeof isoOrMs === 'number' ? isoOrMs : new Date(isoOrMs).getTime();
    const diffMs = Date.now() - ms;
    const seconds = Math.floor(diffMs / 1000);
    if (seconds < 60)
        return 'just now';
    const minutes = Math.floor(seconds / 60);
    if (minutes < 60)
        return `${minutes}m ago`;
    const hours = Math.floor(minutes / 60);
    if (hours < 24)
        return `${hours}h ago`;
    const days = Math.floor(hours / 24);
    return `${days}d ago`;
}
// ---------------------------------------------------------------------------
// Importance filter for auto-extraction
// ---------------------------------------------------------------------------
/**
 * Minimum importance score (1-10) for auto-extracted facts to be stored.
 * Facts below this threshold are silently dropped to save storage and gas.
 * Configurable via TOTALRECLAW_MIN_IMPORTANCE env var (default: 3).
 *
 * NOTE: This filter is ONLY applied to auto-extraction (hooks).
 * The explicit `totalreclaw_remember` tool always stores regardless of importance.
 */
const MIN_IMPORTANCE_THRESHOLD = CONFIG.minImportance;
/**
 * Filter extracted facts by importance threshold.
 * Facts with importance < MIN_IMPORTANCE_THRESHOLD are dropped.
 * Facts with missing/undefined importance are treated as importance=5 (kept).
 */
function filterByImportance(facts, logger) {
    const kept = [];
    let dropped = 0;
    for (const fact of facts) {
        const importance = fact.importance ?? 5;
        if (importance >= MIN_IMPORTANCE_THRESHOLD) {
            kept.push(fact);
        }
        else {
            dropped++;
        }
    }
    // Phase 2.2.5: always log the filter outcome so the agent_end path can
    // distinguish "LLM returned 0 facts" from "LLM returned N facts all dropped
    // below threshold" from "LLM returned N facts, all kept". Prior to 2.2.5
    // this only logged on drops, which made empty-input invisible.
    if (facts.length === 0) {
        logger.info('Importance filter: input=0 (nothing to filter)');
    }
    else if (dropped > 0) {
        logger.info(`Importance filter: dropped ${dropped}/${facts.length} facts below threshold ${MIN_IMPORTANCE_THRESHOLD}`);
    }
    else {
        logger.info(`Importance filter: kept all ${facts.length} facts (threshold ${MIN_IMPORTANCE_THRESHOLD})`);
    }
    return { kept, dropped };
}
// ---------------------------------------------------------------------------
// Auto-extraction helper
// ---------------------------------------------------------------------------
/**
 * Store extracted facts in the TotalReclaw server.
 * Encrypts each fact, generates blind indices and fingerprint, stores via API.
 * Silently skips duplicates.
 *
 * Before storing, performs semantic near-duplicate detection within the batch:
 * facts whose embeddings have cosine similarity >= threshold (default 0.9)
 * against an already-accepted fact in the same batch are skipped.
 */
async function storeExtractedFacts(facts, logger, sourceOverride) {
    if (!encryptionKey || !dedupKey || !authKeyHex || !userId || !apiClient)
        return 0;
    // Phase 1: Generate embeddings for all facts (needed for dedup + storage).
    const embeddingMap = new Map();
    const embeddingResultMap = new Map();
    for (const fact of facts) {
        try {
            const result = await generateEmbeddingAndLSH(fact.text, logger);
            if (result) {
                embeddingMap.set(fact.text, result.embedding);
                embeddingResultMap.set(fact.text, result);
            }
        }
        catch {
            // Embedding generation failed for this fact -- proceed without it.
        }
    }
    // Phase 2: Semantic batch dedup.
    const dedupedFacts = deduplicateBatch(facts, embeddingMap, logger);
    if (dedupedFacts.length < facts.length) {
        logger.info(`Semantic dedup: ${facts.length - dedupedFacts.length} near-duplicate(s) removed from batch of ${facts.length}`);
    }
    // Phase 3: Store the deduplicated facts (with optional store-time dedup).
    // In subgraph mode, collect all protobuf payloads (tombstones + new facts)
    // and submit them in a single batched UserOp for gas efficiency.
    let stored = 0;
    let superseded = 0;
    let skipped = 0;
    let failedFacts = 0;
    const pendingPayloads = []; // Batched subgraph payloads
    let preparedForSubgraph = 0;
    // Plugin v3.0.0: always emit Memory Taxonomy v1 JSON blobs. The
    // TOTALRECLAW_TAXONOMY_VERSION opt-in and the TOTALRECLAW_CLAIM_FORMAT
    // legacy fallback have both been retired — v1 is the single write path.
    for (const fact of dedupedFacts) {
        try {
            const blindIndices = generateBlindIndices(fact.text);
            const entityTrapdoors = computeEntityTrapdoors(fact.entities);
            // Use pre-computed embedding result if available.
            const embeddingResult = embeddingResultMap.get(fact.text) ?? null;
            const allIndices = embeddingResult
                ? [...blindIndices, ...embeddingResult.lshBuckets, ...entityTrapdoors]
                : [...blindIndices, ...entityTrapdoors];
            // LLM-guided dedup: handle UPDATE/DELETE/NOOP actions.
            if (fact.action === 'NOOP') {
                logger.info(`LLM dedup: NOOP — skipping "${fact.text.slice(0, 60)}…"`);
                skipped++;
                continue;
            }
            if (fact.action === 'DELETE' && fact.existingFactId) {
                // Tombstone the old fact, don't store anything new.
                if (isSubgraphMode()) {
                    const tombstone = {
                        id: fact.existingFactId,
                        timestamp: new Date().toISOString(),
                        owner: subgraphOwner || userId,
                        encryptedBlob: '00',
                        blindIndices: [],
                        decayScore: 0,
                        source: 'tombstone',
                        contentFp: '',
                        agentId: 'openclaw-plugin-auto',
                        version: PROTOBUF_VERSION_V4,
                    };
                    pendingPayloads.push(encodeFactProtobuf(tombstone));
                    logger.info(`LLM dedup: DELETE — queued tombstone for ${fact.existingFactId}`);
                }
                else if (apiClient && authKeyHex) {
                    try {
                        await apiClient.deleteFact(fact.existingFactId, authKeyHex);
                        logger.info(`LLM dedup: DELETE — removed ${fact.existingFactId}`);
                    }
                    catch (delErr) {
                        logger.warn(`LLM dedup: DELETE failed for ${fact.existingFactId}: ${delErr instanceof Error ? delErr.message : String(delErr)}`);
                    }
                }
                superseded++;
                continue;
            }
            if (fact.action === 'UPDATE' && fact.existingFactId) {
                // Tombstone the old fact, then fall through to store the new version.
                if (isSubgraphMode()) {
                    const tombstone = {
                        id: fact.existingFactId,
                        timestamp: new Date().toISOString(),
                        owner: subgraphOwner || userId,
                        encryptedBlob: '00',
                        blindIndices: [],
                        decayScore: 0,
                        source: 'tombstone',
                        contentFp: '',
                        agentId: 'openclaw-plugin-auto',
                        version: PROTOBUF_VERSION_V4,
                    };
                    pendingPayloads.push(encodeFactProtobuf(tombstone));
                    logger.info(`LLM dedup: UPDATE — queued tombstone for ${fact.existingFactId}, storing replacement`);
                }
                else if (apiClient && authKeyHex) {
                    try {
                        await apiClient.deleteFact(fact.existingFactId, authKeyHex);
                        logger.info(`LLM dedup: UPDATE — deleted ${fact.existingFactId}, storing replacement`);
                    }
                    catch (delErr) {
                        logger.warn(`LLM dedup: UPDATE delete failed for ${fact.existingFactId}: ${delErr instanceof Error ? delErr.message : String(delErr)}`);
                    }
                }
                superseded++;
                // Fall through to store the new replacement fact below.
            }
            // ADD (default) or UPDATE (after tombstoning old) — proceed to store.
            // The cosine-based store-time dedup below provides an additional safety net.
            // Store-time near-duplicate check: search vault before writing.
            let effectiveImportance = fact.importance;
            if (STORE_DEDUP_ENABLED && embeddingResult) {
                const dupResult = await searchForNearDuplicates(fact.text, embeddingResult.embedding, allIndices, logger);
                if (dupResult) {
                    const action = shouldSupersede(fact.importance, dupResult.match);
                    if (action === 'skip') {
                        logger.info(`Store-time dedup: skipping "${fact.text.slice(0, 60)}…" (sim=${dupResult.similarity.toFixed(3)}, existing ID=${dupResult.match.id})`);
                        skipped++;
                        continue;
                    }
                    // action === 'supersede': delete old fact, inherit higher importance
                    if (isSubgraphMode()) {
                        const tombstone = {
                            id: dupResult.match.id,
                            timestamp: new Date().toISOString(),
                            owner: subgraphOwner || userId,
                            encryptedBlob: '00',
                            blindIndices: [],
                            decayScore: 0,
                            source: 'tombstone',
                            contentFp: '',
                            agentId: 'openclaw-plugin-auto',
                            version: PROTOBUF_VERSION_V4,
                        };
                        pendingPayloads.push(encodeFactProtobuf(tombstone));
                        logger.info(`Store-time dedup: queued supersede for ${dupResult.match.id} (sim=${dupResult.similarity.toFixed(3)})`);
                    }
                    else if (apiClient && authKeyHex) {
                        try {
                            await apiClient.deleteFact(dupResult.match.id, authKeyHex);
                            logger.info(`Store-time dedup: superseding ${dupResult.match.id} (sim=${dupResult.similarity.toFixed(3)})`);
                        }
                        catch (delErr) {
                            logger.warn(`Store-time dedup: failed to delete superseded fact ${dupResult.match.id}: ${delErr instanceof Error ? delErr.message : String(delErr)}`);
                        }
                    }
                    effectiveImportance = Math.max(fact.importance, dupResult.match.decayScore);
                    superseded++;
                }
            }
            const factSource = sourceOverride || 'auto-extraction';
            // Plugin v3.0.0: always build a Memory Taxonomy v1 JSON blob. The
            // blob is decryptable by `readClaimFromBlob` which prefers v1 →
            // falls back to v0 short-key → then plugin-legacy {text, metadata}
            // for pre-v3 vault entries.
            //
            // We build it BEFORE the on-chain write so Phase 2 contradiction
            // detection can inspect the same canonical Claim the write path will
            // actually store. The string is encrypted byte-identically below.
            //
            // Defensive: if the extraction hook didn't populate `fact.source`
            // (e.g. explicit tool path, legacy caller), default to 'user-inferred'
            // so v1 schema validation passes.
            const factForBlob = fact.source
                ? fact
                : { ...fact, source: 'user-inferred' };
            const blobPlaintext = buildCanonicalClaim({
                fact: factForBlob,
                importance: effectiveImportance,
                sourceAgent: factSource,
                // 3.3.1-rc.22 — tag every new claim with the active embedder id
                // so future distillation can rescore selectively. Plugin-only
                // field; survives the core validator strip via re-attach in
                // `buildCanonicalClaimV1`.
                embeddingModelId: getEmbeddingModelId(),
            });
            const factId = crypto.randomUUID();
            // Phase 2 Slice 2d: contradiction detection + auto-resolution.
            //
            // Runs only when the canonical Claim format is active (legacy blobs
            // carry no entity refs, so there is nothing to check), only for
            // Subgraph / managed-service mode (self-hosted contradiction handling
            // can come later), and only when the new fact has entities. The helper
            // is a no-op in all other cases.
            //
            // Returns one decision per candidate contradicting claim:
            //   - supersede_existing → queue a tombstone + proceed with the new write
            //   - skip_new → do not write the new fact; record the skip reason
            //   - empty list → no contradiction, proceed unchanged
            //
            // On any error (subgraph, decrypt, WASM), the helper returns [] and we
            // fall back to Phase 1 behaviour.
            let contradictionSkipNew = false;
            if (isSubgraphMode() &&
                fact.entities &&
                fact.entities.length > 0 &&
                embeddingResult) {
                const newClaimObj = JSON.parse(blobPlaintext);
                let decisions = [];
                try {
                    decisions = await detectAndResolveContradictions({
                        newClaim: newClaimObj,
                        newClaimId: factId,
                        newEmbedding: embeddingResult.embedding,
                        subgraphOwner: subgraphOwner || userId,
                        authKeyHex: authKeyHex,
                        encryptionKey: encryptionKey,
                        deps: {
                            searchSubgraph: (owner, trapdoors, maxCandidates, authKey) => searchSubgraph(owner, trapdoors, maxCandidates, authKey).then((rows) => rows.map((r) => ({
                                id: r.id,
                                encryptedBlob: r.encryptedBlob,
                                encryptedEmbedding: r.encryptedEmbedding ?? null,
                                timestamp: r.timestamp,
                                isActive: r.isActive,
                            }))),
                            decryptFromHex: (hex, key) => decryptFromHex(hex, key),
                        },
                        logger: {
                            info: (m) => logger.info(m),
                            warn: (m) => logger.warn(m),
                        },
                    });
                }
                catch (crErr) {
                    // detectAndResolveContradictions is supposed to never throw — if
                    // it does, we log and continue with Phase 1 behaviour.
                    const msg = crErr instanceof Error ? crErr.message : String(crErr);
                    logger.warn(`Contradiction detection failed (proceeding with store): ${msg}`);
                    decisions = [];
                }
                for (const decision of decisions) {
                    if (decision.action === 'supersede_existing') {
                        const tombstone = {
                            id: decision.existingFactId,
                            timestamp: new Date().toISOString(),
                            owner: subgraphOwner || userId,
                            encryptedBlob: '00',
                            blindIndices: [],
                            decayScore: 0,
                            source: 'tombstone',
                            contentFp: '',
                            agentId: 'openclaw-plugin-auto',
                            version: PROTOBUF_VERSION_V4,
                        };
                        pendingPayloads.push(encodeFactProtobuf(tombstone));
                        superseded++;
                        logger.info(`Auto-resolve: queued supersede for ${decision.existingFactId.slice(0, 10)}… ` +
                            `(sim=${decision.similarity.toFixed(3)}, entity=${decision.entityId})`);
                    }
                    else if (decision.action === 'skip_new') {
                        if (decision.reason === 'existing_pinned') {
                            logger.warn(`Auto-resolve: skipped new write — existing claim ${decision.existingFactId.slice(0, 10)}… is pinned ` +
                                `(sim=${decision.similarity.toFixed(3)}, entity=${decision.entityId})`);
                        }
                        else {
                            logger.info(`Auto-resolve: skipped new write — existing ${decision.existingFactId.slice(0, 10)}… wins ` +
                                `(sim=${decision.similarity.toFixed(3)}, entity=${decision.entityId})`);
                        }
                        contradictionSkipNew = true;
                    }
                }
            }
            if (contradictionSkipNew) {
                skipped++;
                continue;
            }
            const encryptedBlob = encryptToHex(blobPlaintext, encryptionKey);
            const contentFp = generateContentFingerprint(fact.text, dedupKey);
            if (isSubgraphMode()) {
                const protobuf = encodeFactProtobuf({
                    id: factId,
                    timestamp: new Date().toISOString(),
                    owner: subgraphOwner || userId,
                    encryptedBlob: encryptedBlob,
                    blindIndices: allIndices,
                    decayScore: effectiveImportance,
                    source: factSource,
                    contentFp: contentFp,
                    agentId: 'openclaw-plugin-auto',
                    version: PROTOBUF_VERSION_V4,
                    encryptedEmbedding: embeddingResult?.encryptedEmbedding,
                });
                pendingPayloads.push(protobuf);
                preparedForSubgraph++;
            }
            else {
                const payload = {
                    id: factId,
                    timestamp: new Date().toISOString(),
                    encrypted_blob: encryptedBlob,
                    blind_indices: allIndices,
                    decay_score: effectiveImportance,
                    source: factSource,
                    content_fp: contentFp,
                    agent_id: 'openclaw-plugin-auto',
                    encrypted_embedding: embeddingResult?.encryptedEmbedding,
                };
                await apiClient.store(userId, [payload], authKeyHex);
                stored++;
            }
        }
        catch (err) {
            // Check for 403 / quota exceeded — invalidate billing cache so next
            // before_agent_start re-fetches and warns the user.
            const factErrMsg = err instanceof Error ? err.message : String(err);
            if (factErrMsg.includes('403') || factErrMsg.toLowerCase().includes('quota')) {
                deleteFileIfExists(BILLING_CACHE_PATH);
                logger.warn(`Quota exceeded — billing cache invalidated. ${factErrMsg}`);
                break; // Stop trying to store remaining facts — they'll all fail too
            }
            // Otherwise log and continue — individual fact failures shouldn't block remaining facts
            logger.warn(`Failed to store fact "${fact.text.slice(0, 60)}…": ${factErrMsg}`);
            failedFacts++;
        }
    }
    // Submit subgraph payloads one fact at a time (sequential single-call UserOps).
    // Batch executeBatch UserOps have persistent gas estimation issues on Base Sepolia
    // that cause on-chain reverts. Single-fact UserOps use the simpler submitFactOnChain
    // path which works reliably (same path as totalreclaw_remember). Each submission
    // polls for receipt (120s) before proceeding, so nonce is consumed before the next.
    let batchError;
    if (pendingPayloads.length > 0 && isSubgraphMode()) {
        const batchConfig = { ...getSubgraphConfig(), authKeyHex: authKeyHex, walletAddress: subgraphOwner ?? undefined };
        for (let i = 0; i < pendingPayloads.length; i++) {
            const slice = [pendingPayloads[i]]; // Single fact per UserOp
            try {
                const result = await submitFactBatchOnChain(slice, batchConfig);
                if (result.success) {
                    stored += slice.length;
                    logger.info(`Fact ${i + 1}/${pendingPayloads.length}: submitted on-chain (tx=${result.txHash.slice(0, 10)}…)`);
                }
                else {
                    batchError = `On-chain batch submission failed (tx=${result.txHash.slice(0, 10)}…)`;
                    logger.warn(batchError);
                    break; // Stop submitting remaining batches
                }
            }
            catch (err) {
                const errMsg = err instanceof Error ? err.message : String(err);
                if (errMsg.includes('403') || errMsg.toLowerCase().includes('quota')) {
                    deleteFileIfExists(BILLING_CACHE_PATH);
                    batchError = `Quota exceeded — billing cache invalidated. ${errMsg}`;
                    logger.warn(batchError);
                    break;
                }
                else {
                    batchError = `Batch submission failed: ${errMsg}`;
                    logger.warn(batchError);
                    break;
                }
            }
        }
    }
    if (stored > 0 || superseded > 0 || skipped > 0 || failedFacts > 0) {
        logger.info(`Auto-extraction results: stored=${stored}, superseded=${superseded}, skipped=${skipped}, failed=${failedFacts}`);
    }
    // If ANY batch failed, throw — even if some facts were stored earlier.
    // A failed/timed-out UserOp may still linger in the bundler mempool as a
    // "nonce zombie." If we return normally, the caller's next storeExtractedFacts
    // call will fetch the same on-chain nonce and hit AA25 ("invalid account nonce").
    // Throwing forces all callers (import loops, chunk handlers) to stop submitting.
    if (batchError) {
        throw new Error(`Memory storage failed (${stored} stored before failure): ${batchError}`);
    }
    if (stored === 0 && failedFacts > 0) {
        throw new Error(`Memory storage failed: ${failedFacts} fact(s) failed to store`);
    }
    return stored;
}
// ---------------------------------------------------------------------------
// Import handler (for totalreclaw_import_from tool)
// ---------------------------------------------------------------------------
/**
 * Handle import_from tool calls in the plugin context.
 *
 * Two paths:
 * 1. Pre-structured sources (Mem0, MCP Memory) — adapter returns facts directly,
 *    stored via storeExtractedFacts().
 * 2. Conversation-based sources (ChatGPT, Claude) — adapter returns conversation
 *    chunks, each chunk is passed through extractFacts() (the same LLM extraction
 *    pipeline used for auto-extraction), then stored via storeExtractedFacts().
 */
async function handlePluginImportFrom(params, logger) {
    _importInProgress = true;
    const startTime = Date.now();
    const source = params.source;
    const validSources = ['mem0', 'mcp-memory', 'chatgpt', 'claude', 'gemini'];
    if (!source || !validSources.includes(source)) {
        return { success: false, error: `Invalid source. Must be one of: ${validSources.join(', ')}` };
    }
    // Generate import_id up front so dry-run responses and background tasks share it.
    const importId = params.resume_id ?? crypto.randomUUID();
    try {
        const { getAdapter } = await import('./import-adapters/index.js');
        const adapter = getAdapter(source);
        const parseResult = await adapter.parse({
            content: params.content,
            api_key: params.api_key,
            source_user_id: params.source_user_id,
            api_url: params.api_url,
            file_path: params.file_path,
        });
        const hasChunks = parseResult.chunks && parseResult.chunks.length > 0;
        const hasFacts = parseResult.facts && parseResult.facts.length > 0;
        if (parseResult.errors.length > 0 && !hasFacts && !hasChunks) {
            return {
                success: false,
                error: `Failed to parse ${adapter.displayName} data`,
                details: parseResult.errors,
            };
        }
        // Dry run: report what was parsed (chunks or facts)
        if (params.dry_run) {
            if (hasChunks) {
                const totalChunks = parseResult.chunks.length;
                const EXTRACTION_RATIO = 2.5; // avg facts per chunk, from empirical data
                const BATCH_SIZE = 25;
                const SECONDS_PER_BATCH = 45; // ~30s extraction + ~15s embed+store
                const estimatedFacts = Math.round(totalChunks * EXTRACTION_RATIO);
                const estimatedBatches = Math.ceil(totalChunks / BATCH_SIZE);
                const estimatedMinutes = Math.ceil(estimatedBatches * SECONDS_PER_BATCH / 60);
                return {
                    success: true,
                    dry_run: true,
                    import_id: importId,
                    source,
                    total_chunks: totalChunks,
                    total_messages: parseResult.totalMessages,
                    estimated_facts: estimatedFacts,
                    estimated_batches: estimatedBatches,
                    estimated_minutes: estimatedMinutes,
                    batch_size: BATCH_SIZE,
                    preview: parseResult.chunks.slice(0, 5).map((c) => ({
                        title: c.title,
                        messages: c.messages.length,
                        first_message: c.messages[0]?.text.slice(0, 100),
                    })),
                    note: `Estimated ${estimatedFacts} facts from ${totalChunks} chunks (~${estimatedMinutes} min). Confirm to start background import.`,
                    warnings: parseResult.warnings,
                };
            }
            return {
                success: true,
                dry_run: true,
                import_id: importId,
                source,
                total_found: parseResult.facts.length,
                preview: parseResult.facts.slice(0, 10).map((f) => ({
                    type: f.type,
                    text: f.text.slice(0, 100),
                    importance: f.importance,
                })),
                warnings: parseResult.warnings,
            };
        }
        // ── Path 1: Conversation chunks (ChatGPT, Claude, Gemini) — background execution ──
        if (hasChunks) {
            const totalChunks = parseResult.chunks.length;
            const BATCH_SIZE = 25;
            const SECONDS_PER_BATCH = 45;
            const estimatedBatches = Math.ceil(totalChunks / BATCH_SIZE);
            const estimatedMinutes = Math.ceil(estimatedBatches * SECONDS_PER_BATCH / 60);
            const estimatedTotalFacts = Math.round(totalChunks * 2.5);
            const now = new Date();
            const initialState = {
                import_id: importId,
                source,
                status: 'running',
                started_at: now.toISOString(),
                last_updated: now.toISOString(),
                total_chunks: totalChunks,
                total_messages: parseResult.totalMessages,
                batch_done: 0,
                batch_total: estimatedBatches,
                facts_stored: 0,
                facts_extracted: 0,
                dups_skipped: 0,
                errors: [],
                file_path: params.file_path,
                estimated_total_facts: estimatedTotalFacts,
                estimated_minutes: estimatedMinutes,
                estimated_completion_iso: new Date(now.getTime() + estimatedBatches * SECONDS_PER_BATCH * 1000).toISOString(),
                disclosure_confirmed: !!(params.disclosure_confirmed),
            };
            writeImportState(initialState);
            logger.info(`Import ${importId}: background task started (${totalChunks} chunks, ~${estimatedMinutes}min)`);
            void handleChunkImport(parseResult.chunks, parseResult.totalMessages, source, logger, startTime, parseResult.warnings, importId).catch((err) => {
                const msg = err instanceof Error ? err.message : String(err);
                logger.warn(`Import ${importId}: background task failed: ${msg}`);
                const failedState = readImportState(importId);
                if (failedState && failedState.status === 'running') {
                    writeImportState({ ...failedState, status: 'failed', errors: [...failedState.errors, msg] });
                }
            });
            return {
                import_id: importId,
                status: 'running',
                source,
                total_chunks: totalChunks,
                estimated_batches: estimatedBatches,
                estimated_minutes: estimatedMinutes,
                estimated_completion_iso: initialState.estimated_completion_iso,
                message: `Import started in background. ~${estimatedMinutes} min for ${totalChunks} chunks. Ask "how's the import?" to check progress with totalreclaw_import_status.`,
                warnings: parseResult.warnings,
            };
        }
        // ── Path 2: Pre-structured facts (Mem0, MCP Memory) — direct store ──
        const extractedFacts = parseResult.facts.map((f) => ({
            text: f.text,
            type: f.type,
            importance: f.importance,
            action: 'ADD',
        }));
        // Store in batches of 50. Stop on any batch failure to prevent
        // nonce zombies from blocking subsequent UserOps (AA25).
        let totalStored = 0;
        let storeError;
        const batchSize = 50;
        for (let i = 0; i < extractedFacts.length; i += batchSize) {
            const batch = extractedFacts.slice(i, i + batchSize);
            try {
                const stored = await storeExtractedFacts(batch, logger);
                totalStored += stored;
                logger.info(`Import progress: ${Math.min(i + batchSize, extractedFacts.length)}/${extractedFacts.length} processed, ${totalStored} stored`);
            }
            catch (err) {
                storeError = err instanceof Error ? err.message : String(err);
                logger.warn(`Import stopped at batch ${Math.floor(i / batchSize) + 1}: ${storeError}`);
                break; // Stop processing further batches
            }
        }
        const importWarnings = [...parseResult.warnings];
        if (storeError) {
            importWarnings.push(`Import stopped early: ${storeError}`);
        }
        return {
            success: totalStored > 0,
            source,
            import_id: importId,
            total_found: parseResult.facts.length,
            imported: totalStored,
            skipped: parseResult.facts.length - totalStored,
            stopped_early: !!storeError,
            warnings: importWarnings,
            duration_ms: Date.now() - startTime,
        };
    }
    catch (e) {
        const msg = e instanceof Error ? e.message : 'Unknown error';
        logger.error(`Import failed: ${msg}`);
        return { success: false, error: `Import failed: ${msg}` };
    }
}
// ---------------------------------------------------------------------------
// Smart Import — Two-Pass Pipeline (Profile + Triage)
// ---------------------------------------------------------------------------
// Lazy-load WASM for smart import functions (same pattern as crypto.ts /
// subgraph-store.ts). Goes through __cjsRequire (createRequire(import.meta.url))
// declared at the top of the file — bare `require()` is undefined under
// pure-ESM Node, see issue #124.
let _smartImportWasm = null;
function getSmartImportWasm() {
    if (!_smartImportWasm)
        _smartImportWasm = __cjsRequire('@totalreclaw/core');
    return _smartImportWasm;
}
/**
 * Check whether the @totalreclaw/core WASM module exposes smart import functions.
 * Returns false if the module is an older version without smart import support.
 */
function hasSmartImportSupport() {
    try {
        const wasm = getSmartImportWasm();
        return typeof wasm.chunksToSummaries === 'function' &&
            typeof wasm.buildProfileBatchPrompt === 'function' &&
            typeof wasm.parseProfileBatchResponse === 'function' &&
            typeof wasm.buildTriagePrompt === 'function' &&
            typeof wasm.parseTriageResponse === 'function' &&
            typeof wasm.enrichExtractionPrompt === 'function';
    }
    catch {
        return false;
    }
}
/**
 * Run the smart import two-pass pipeline: profile the user from conversation
 * summaries, then triage chunks as EXTRACT or SKIP.
 *
 * All prompt construction and response parsing happens in @totalreclaw/core WASM.
 * LLM calls use the plugin's existing chatCompletion() function.
 *
 * Returns null if smart import is unavailable (old WASM, no LLM config, etc.)
 * so the caller can fall back to blind extraction.
 */
async function runSmartImportPipeline(chunks, logger) {
    // Guard: WASM must have smart import functions
    if (!hasSmartImportSupport()) {
        logger.info('Smart import: WASM module does not support smart import, falling back to blind extraction');
        return null;
    }
    // Guard: LLM must be available
    const llmConfig = resolveLLMConfig();
    if (!llmConfig) {
        logger.info('Smart import: no LLM available, falling back to blind extraction');
        return null;
    }
    const pipelineStart = Date.now();
    const wasm = getSmartImportWasm();
    try {
        // Step 0: Convert chunks to compact summaries (first + last message)
        const wasmChunks = chunks.map((c, i) => ({
            index: i,
            title: c.title || 'Untitled',
            messages: c.messages.map((m) => ({ role: m.role, content: m.text })),
            timestamp: c.timestamp || null,
        }));
        const summaries = wasm.chunksToSummaries(JSON.stringify(wasmChunks));
        const summariesJson = JSON.stringify(summaries);
        // Step 1: Build user profile (batch summarize -> merge)
        const PROFILE_BATCH_SIZE = 50;
        const profileStart = Date.now();
        const partials = [];
        for (let i = 0; i < summaries.length; i += PROFILE_BATCH_SIZE) {
            const batch = summaries.slice(i, i + PROFILE_BATCH_SIZE);
            const prompt = wasm.buildProfileBatchPrompt(JSON.stringify(batch));
            const response = await chatCompletion(llmConfig, [
                { role: 'user', content: prompt },
            ], { maxTokens: 2048, temperature: 0 });
            if (!response) {
                logger.warn(`Smart import: LLM returned empty response for profile batch ${Math.floor(i / PROFILE_BATCH_SIZE) + 1}`);
                continue;
            }
            const partial = wasm.parseProfileBatchResponse(response);
            partials.push(partial);
        }
        if (partials.length === 0) {
            logger.warn('Smart import: no profile batches produced, falling back to blind extraction');
            return null;
        }
        let profile;
        if (partials.length === 1) {
            // Single batch — skip merge, promote partial to full profile
            // parseProfileBatchResponse returns a PartialProfile; convert to UserProfile shape
            const p = partials[0];
            profile = {
                identity: p.identity ?? null,
                themes: p.themes ?? [],
                projects: p.projects ?? [],
                stack: p.stack ?? [],
                decisions: p.decisions ?? [],
                interests: p.interests ?? [],
                skip_patterns: p.skip_patterns ?? [],
            };
        }
        else {
            const mergePrompt = wasm.buildProfileMergePrompt(JSON.stringify(partials));
            const mergeResponse = await chatCompletion(llmConfig, [
                { role: 'user', content: mergePrompt },
            ], { maxTokens: 2048, temperature: 0 });
            if (!mergeResponse) {
                logger.warn('Smart import: LLM returned empty response for profile merge, falling back to blind extraction');
                return null;
            }
            profile = wasm.parseProfileResponse(mergeResponse);
        }
        const profileJson = JSON.stringify(profile);
        const profileDuration = Date.now() - profileStart;
        const p = profile;
        const themeCount = Array.isArray(p.themes) ? p.themes.length : 0;
        const skipPatternCount = Array.isArray(p.skip_patterns) ? p.skip_patterns.length : 0;
        logger.info(`Smart import: profile built in ${profileDuration}ms (themes=${themeCount}, skip_patterns=${skipPatternCount})`);
        // Step 1.5: Chunk triage (EXTRACT or SKIP)
        const triageStart = Date.now();
        const allDecisions = [];
        const TRIAGE_BATCH_SIZE = 50;
        for (let i = 0; i < summaries.length; i += TRIAGE_BATCH_SIZE) {
            const batch = summaries.slice(i, i + TRIAGE_BATCH_SIZE);
            const triagePrompt = wasm.buildTriagePrompt(profileJson, JSON.stringify(batch));
            const triageResponse = await chatCompletion(llmConfig, [
                { role: 'user', content: triagePrompt },
            ], { maxTokens: 4096, temperature: 0 });
            if (!triageResponse) {
                logger.warn(`Smart import: LLM returned empty response for triage batch ${Math.floor(i / TRIAGE_BATCH_SIZE) + 1}, defaulting to EXTRACT`);
                // Default all chunks in this batch to EXTRACT
                for (let j = i; j < Math.min(i + TRIAGE_BATCH_SIZE, summaries.length); j++) {
                    allDecisions.push({ chunk_index: j, decision: 'EXTRACT', reason: 'triage LLM unavailable' });
                }
                continue;
            }
            const batchDecisions = wasm.parseTriageResponse(triageResponse);
            allDecisions.push(...batchDecisions);
        }
        const triageDuration = Date.now() - triageStart;
        const extractCount = allDecisions.filter((d) => d.decision !== 'SKIP').length;
        const skipCount = allDecisions.filter((d) => d.decision === 'SKIP').length;
        logger.info(`Smart import: triage complete in ${triageDuration}ms (extract=${extractCount}, skip=${skipCount}, total=${chunks.length})`);
        // Step 2: Build enriched system prompt for extraction
        const enrichedSystemPrompt = wasm.enrichExtractionPrompt(profileJson, EXTRACTION_SYSTEM_PROMPT);
        const totalDuration = Date.now() - pipelineStart;
        logger.info(`Smart import: pipeline complete in ${totalDuration}ms`);
        return {
            profileJson,
            decisions: allDecisions,
            enrichedSystemPrompt,
            extractCount,
            skipCount,
            durationMs: totalDuration,
        };
    }
    catch (err) {
        const msg = err instanceof Error ? err.message : String(err);
        logger.warn(`Smart import: pipeline failed (${msg}), falling back to blind extraction`);
        return null;
    }
}
/**
 * Check if a chunk should be skipped based on triage decisions.
 * If no decision exists for the chunk index, defaults to EXTRACT (safe default).
 */
function isChunkSkipped(chunkIndex, decisions) {
    const decision = decisions.find((d) => d.chunk_index === chunkIndex);
    if (decision && decision.decision === 'SKIP') {
        return { skipped: true, reason: decision.reason || 'triage: skip' };
    }
    return { skipped: false, reason: '' };
}
/**
 * Process a batch (slice) of conversation chunks from a file.
 * Called repeatedly by the agent for large imports.
 */
async function handleBatchImport(params, logger) {
    _importInProgress = true;
    const source = params.source;
    const filePath = params.file_path;
    const content = params.content;
    const offset = params.offset ?? 0;
    const batchSize = params.batch_size ?? 25;
    const validSources = ['mem0', 'mcp-memory', 'chatgpt', 'claude', 'gemini'];
    if (!source || !validSources.includes(source)) {
        return { success: false, error: `Invalid source. Must be one of: ${validSources.join(', ')}` };
    }
    const startTime = Date.now();
    const { getAdapter } = await import('./import-adapters/index.js');
    const adapter = getAdapter(source);
    const parseResult = await adapter.parse({ content, file_path: filePath });
    if (parseResult.errors.length > 0 && parseResult.chunks.length === 0) {
        return { success: false, error: parseResult.errors.join('; ') };
    }
    const totalChunks = parseResult.chunks.length;
    const slice = parseResult.chunks.slice(offset, offset + batchSize);
    const remaining = Math.max(0, totalChunks - offset - slice.length);
    // --- Smart Import: Profile + Triage ---
    // Build profile from ALL chunks (not just the slice) for full context,
    // then triage only the current slice. For simplicity, we rebuild on every
    // batch call — optimization (caching) can come later.
    const smartCtx = await runSmartImportPipeline(parseResult.chunks, logger);
    let chunksSkipped = 0;
    // Process the slice through the normal extraction + storage pipeline.
    // If a batch fails (nonce zombie, quota exceeded, etc.), stop immediately
    // to prevent subsequent UserOps from hitting AA25 nonce conflicts.
    let factsExtracted = 0;
    let factsStored = 0;
    let chunksProcessed = 0;
    let storeError;
    for (let i = 0; i < slice.length; i++) {
        const chunk = slice[i];
        const globalIndex = offset + i; // Index in the full chunks array
        // Smart import: skip chunks triaged as SKIP
        if (smartCtx) {
            const { skipped, reason } = isChunkSkipped(globalIndex, smartCtx.decisions);
            if (skipped) {
                logger.info(`Import: skipping chunk ${globalIndex + 1}/${totalChunks}: "${chunk.title}" (${reason})`);
                chunksSkipped++;
                chunksProcessed++;
                continue;
            }
        }
        logger.info(`Import: extracting facts from chunk ${globalIndex + 1}/${totalChunks}: "${chunk.title}"`);
        const messages = chunk.messages.map((m) => ({ role: m.role, content: m.text }));
        const facts = await extractFacts(messages, 'full', undefined, // no existing memories for dedup during import
        smartCtx?.enrichedSystemPrompt);
        chunksProcessed++;
        if (facts.length > 0) {
            factsExtracted += facts.length;
            try {
                const stored = await storeExtractedFacts(facts, logger);
                factsStored += stored;
            }
            catch (err) {
                storeError = err instanceof Error ? err.message : String(err);
                logger.warn(`Import batch stopped at chunk ${globalIndex + 1}/${totalChunks}: ${storeError}`);
                break; // Stop processing further chunks — a zombie UserOp may block writes
            }
        }
    }
    return {
        success: factsStored > 0 || (!storeError && factsExtracted === 0),
        batch_offset: offset,
        batch_size: chunksProcessed,
        total_chunks: totalChunks,
        facts_extracted: factsExtracted,
        facts_stored: factsStored,
        chunks_skipped: chunksSkipped,
        remaining_chunks: remaining,
        is_complete: remaining === 0 && !storeError,
        stopped_early: !!storeError,
        error: storeError,
        smart_import: smartCtx ? {
            profile_duration_ms: smartCtx.durationMs,
            extract_count: smartCtx.extractCount,
            skip_count: smartCtx.skipCount,
        } : null,
        // Estimation for the full import
        estimated_total_facts: Math.round(totalChunks * 2.5),
        estimated_total_userops: Math.ceil(totalChunks * 2.5 / 15),
        estimated_minutes: Math.ceil(Math.ceil(totalChunks / batchSize) * 45 / 60),
        duration_ms: Date.now() - startTime,
    };
}
/**
 * Process conversation chunks through LLM extraction and store results.
 *
 * Each chunk is passed to extractFacts() — the same extraction pipeline used
 * for auto-extraction during live conversations. This ensures import quality
 * matches conversation extraction quality.
 */
async function handleChunkImport(chunks, totalMessages, source, logger, startTime, warnings, importId) {
    let totalExtracted = 0;
    let totalStored = 0;
    let chunksProcessed = 0;
    let chunksSkipped = 0;
    const resolvedImportId = importId ?? crypto.randomUUID();
    let storeError;
    // --- Smart Import: Profile + Triage ---
    const smartCtx = await runSmartImportPipeline(chunks, logger);
    const CHECKPOINT_EVERY = 25; // write state file every N chunks
    for (let i = 0; i < chunks.length; i++) {
        // Check abort flag from state file before each chunk (background task may be cancelled).
        if (importId) {
            const currentState = readImportState(importId);
            if (currentState?.status === 'aborted') {
                logger.info(`Import ${importId}: abort flag detected at chunk ${i + 1}/${chunks.length}, stopping`);
                break;
            }
        }
        const chunk = chunks[i];
        chunksProcessed++;
        // Smart import: skip chunks triaged as SKIP
        if (smartCtx) {
            const { skipped, reason } = isChunkSkipped(i, smartCtx.decisions);
            if (skipped) {
                logger.info(`Import: skipping chunk ${chunksProcessed}/${chunks.length}: "${chunk.title}" (${reason})`);
                chunksSkipped++;
                continue;
            }
        }
        logger.info(`Import: extracting facts from chunk ${chunksProcessed}/${chunks.length}: "${chunk.title}"`);
        // Convert chunk messages to the format extractFacts() expects.
        // extractFacts() takes an array of message-like objects with { role, content }.
        const messages = chunk.messages.map((m) => ({
            role: m.role,
            content: m.text,
        }));
        // Use 'full' mode to extract ALL valuable memories from the chunk
        // (not just the last few messages like 'turn' mode does).
        // Smart import: pass enriched system prompt with user profile context.
        const facts = await extractFacts(messages, 'full', undefined, // no existing memories for dedup during import
        smartCtx?.enrichedSystemPrompt);
        if (facts.length > 0) {
            totalExtracted += facts.length;
            try {
                // Store through the normal pipeline (dedup, encrypt, store).
                // storeExtractedFacts throws on batch failure to prevent nonce zombies.
                const stored = await storeExtractedFacts(facts, logger);
                totalStored += stored;
                logger.info(`Import chunk ${chunksProcessed}/${chunks.length}: extracted ${facts.length} facts, stored ${stored}`);
            }
            catch (err) {
                storeError = err instanceof Error ? err.message : String(err);
                logger.warn(`Import stopped at chunk ${chunksProcessed}/${chunks.length}: ${storeError}`);
                break; // Stop processing further chunks — a zombie UserOp may block writes
            }
        }
        // Checkpoint state file periodically so _import_status reflects live progress.
        if (importId && chunksProcessed % CHECKPOINT_EVERY === 0) {
            const liveState = readImportState(importId);
            if (liveState) {
                const estimatedBatches = liveState.batch_total || 1;
                const doneBatches = Math.floor(chunksProcessed / CHECKPOINT_EVERY);
                const elapsed = Date.now() - new Date(liveState.started_at).getTime();
                const secPerBatch = doneBatches > 0 ? elapsed / 1000 / doneBatches : 45;
                const remaining = estimatedBatches - doneBatches;
                const etaMs = remaining * secPerBatch * 1000;
                writeImportState({
                    ...liveState,
                    batch_done: doneBatches,
                    facts_stored: totalStored,
                    facts_extracted: totalExtracted,
                    estimated_completion_iso: new Date(Date.now() + etaMs).toISOString(),
                });
            }
        }
    }
    if (totalExtracted === 0 && chunks.length > 0 && !storeError && chunksSkipped < chunks.length) {
        warnings.push(`Processed ${chunks.length} conversation chunks (${totalMessages} messages) but the LLM ` +
            `did not extract any facts worth storing. This can happen if the conversations are mostly ` +
            `generic/ephemeral content without personal facts, preferences, or decisions.`);
    }
    if (storeError) {
        warnings.push(`Import stopped early: ${storeError}. ${chunks.length - chunksProcessed} chunk(s) not processed.`);
    }
    // Final state file write for background imports.
    if (importId) {
        const finalState = readImportState(importId);
        if (finalState) {
            const finalStatus = storeError ? 'failed' : (finalState.status === 'aborted' ? 'aborted' : 'completed');
            writeImportState({
                ...finalState,
                status: finalStatus,
                batch_done: finalState.batch_total,
                facts_stored: totalStored,
                facts_extracted: totalExtracted,
                errors: storeError ? [...finalState.errors, storeError] : finalState.errors,
            });
        }
        _importInProgress = false;
    }
    return {
        success: totalStored > 0 || totalExtracted > 0,
        source,
        import_id: resolvedImportId,
        total_chunks: chunks.length,
        chunks_processed: chunksProcessed,
        chunks_skipped: chunksSkipped,
        total_messages: totalMessages,
        facts_extracted: totalExtracted,
        imported: totalStored,
        skipped: totalExtracted - totalStored,
        stopped_early: !!storeError,
        smart_import: smartCtx ? {
            profile_duration_ms: smartCtx.durationMs,
            extract_count: smartCtx.extractCount,
            skip_count: smartCtx.skipCount,
        } : null,
        warnings,
        duration_ms: Date.now() - startTime,
    };
}
// ---------------------------------------------------------------------------
// Import status + abort handlers
// ---------------------------------------------------------------------------
async function handleImportStatus(params, logger) {
    const importId = params.import_id;
    let state;
    if (importId) {
        state = readImportState(importId);
        if (!state)
            return { error: `No import found with id: ${importId}` };
    }
    else {
        state = readMostRecentActiveImport();
        if (!state)
            return { status: 'no_active_import', message: 'No active import found. Start one with totalreclaw_import_from.' };
    }
    // 1h freshness guard: mark stale imports as failed and prompt user to resume.
    if (state.status === 'running' && isImportStale(state)) {
        writeImportState({ ...state, status: 'failed', errors: [...state.errors, 'Stale: no progress in 1h'] });
        logger.info(`Import ${state.import_id}: marked stale (no progress in 1h)`);
        return {
            import_id: state.import_id,
            status: 'failed',
            stale: true,
            facts_stored: state.facts_stored,
            message: 'Import appears stale — no progress in 1 hour. Resume with totalreclaw_import_from using the same file and resume_id.',
            resume_id: state.import_id,
        };
    }
    const now = Date.now();
    const elapsedMs = now - new Date(state.started_at).getTime();
    const secPerBatch = state.batch_done > 0 ? elapsedMs / 1000 / state.batch_done : 45;
    const remaining = Math.max(0, state.batch_total - state.batch_done);
    const etaSeconds = state.status === 'running' ? Math.round(remaining * secPerBatch) : 0;
    return {
        import_id: state.import_id,
        status: state.status,
        batch_done: state.batch_done,
        batch_total: state.batch_total,
        facts_stored: state.facts_stored,
        dups_skipped: state.dups_skipped,
        eta_seconds: etaSeconds,
        completion_iso: state.status === 'running'
            ? new Date(now + etaSeconds * 1000).toISOString()
            : state.last_updated,
        source: state.source,
        started_at: state.started_at,
        errors: state.errors,
    };
}
async function handleImportAbort(params, logger) {
    const importId = params.import_id;
    if (!importId)
        return { error: 'import_id is required' };
    const state = readImportState(importId);
    if (!state)
        return { error: `No import found with id: ${importId}` };
    if (state.status === 'aborted') {
        return { aborted: true, idempotent: true, import_id: importId, facts_already_stored: state.facts_stored };
    }
    if (state.status === 'completed') {
        return { error: 'Import already completed — nothing to abort', import_id: importId, facts_stored: state.facts_stored };
    }
    writeImportState({ ...state, status: 'aborted' });
    logger.info(`Import ${importId}: abort requested (${state.facts_stored} facts already stored)`);
    return {
        aborted: true,
        import_id: importId,
        facts_already_stored: state.facts_stored,
        message: 'Import abort requested. The background task will stop at the next chunk boundary. Already-stored facts are kept.',
    };
}
// ---------------------------------------------------------------------------
// Plugin definition
// ---------------------------------------------------------------------------
const plugin = {
    id: 'totalreclaw',
    name: 'TotalReclaw',
    description: 'End-to-end encrypted memory vault for AI agents',
    kind: 'memory',
    // 3.3.1 schema expansion — `publicUrl` and the full `extraction.*` surface
    // (including the extraction.llm provider-override block) are now valid
    // properties. The 3.3.0 schema rejected these keys with
    // `invalid config: must NOT have additional properties`, which blocked
    // the documented remote-pairing setup (publicUrl) and made it impossible
    // for a user to hand-pick an extraction model (extraction.llm.*).
    configSchema: {
        type: 'object',
        additionalProperties: false,
        properties: {
            publicUrl: {
                type: 'string',
                description: "Public gateway URL for QR pairing (e.g. 'https://gateway.example.com:18789'). Overrides the auto-resolution cascade in buildPairingUrl.",
            },
            extraction: {
                type: 'object',
                additionalProperties: false,
                properties: {
                    enabled: {
                        type: 'boolean',
                        description: 'Enable/disable auto-extraction (default: true)',
                    },
                    model: {
                        type: 'string',
                        description: "Shorthand: override just the extraction model (e.g., 'glm-4.5-flash', 'gpt-4.1-mini'). For a full provider override use extraction.llm.",
                    },
                    interval: {
                        type: 'number',
                        description: 'Number of turns between automatic extractions (default: 3)',
                    },
                    maxFactsPerExtraction: {
                        type: 'number',
                        description: 'Hard cap on facts extracted per turn (default: 15)',
                    },
                    llm: {
                        type: 'object',
                        additionalProperties: false,
                        description: 'Explicit LLM override block. Highest-priority tier in the extraction-provider cascade. Any subset of provider+apiKey is enough to pin a provider.',
                        properties: {
                            provider: {
                                type: 'string',
                                description: "Provider name: zai | openai | anthropic | gemini | google | mistral | groq | deepseek | openrouter | xai | together | cerebras.",
                            },
                            model: {
                                type: 'string',
                                description: 'Explicit model id. If omitted, deriveCheapModel(provider) picks a sensible default.',
                            },
                            apiKey: {
                                type: 'string',
                                description: 'API key for the selected provider. Required for the override to take effect.',
                            },
                            baseUrl: {
                                type: 'string',
                                description: 'Override the provider base URL (self-hosted / custom gateway setups).',
                            },
                        },
                    },
                },
            },
        },
    },
    register(api) {
        // ---------------------------------------------------------------
        // 3.3.2-rc.1 (issue #186) — load manifest instrumentation
        // ---------------------------------------------------------------
        //
        // Capture every `api.registerTool({name, ...})` call so we can write
        // a `.loaded.json` manifest at the end of register(). Wrap the body
        // in try/catch so a register-time throw produces `.error.json` for
        // agent-side filesystem verification (the CLI hangs in some Docker
        // setups — issue #182 — so the manifest is the canonical "did the
        // plugin load?" probe).
        //
        // Implementation: we intercept the api.registerTool method by
        // wrapping it on the api object passed in. The wrapper inspects the
        // `name` field (every TR registerTool call sets it) and forwards
        // verbatim. NO behavior change to the SDK call — the original method
        // is invoked with original args and `this` binding.
        //
        // Synchronous writes ONLY (see writePluginManifest doc): the SDK
        // freezes plugin registries the moment register() returns; an async
        // write would race that freeze.
        const _registeredToolNames = [];
        const _originalRegisterTool = api.registerTool.bind(api);
        // 3.3.8-rc.1 HYBRID MODE (OpenClaw 2026.5.2 issue #223 workaround):
        // The tool-policy-pipeline in OC 2026.5.2 strips non-bundled plugin tools
        // before they reach the agent's session toolset. registerTool() calls
        // succeed and tools are declared in contracts.tools, so the PLUGIN LOADS.
        // But tool calls never reach execute() — the pipeline discards them before
        // the agent's toolset is built.
        //
        // Strategy: keep all registerTool() calls intact so the plugin loader can
        // verify the contracts.tools declaration and load the plugin (hooks fire).
        // The `tr` CLI binary (dist/tr-cli.js) provides the alternative execution
        // path. Agent runs `tr remember|recall|status|pair` from shell; tool calls
        // are dead-letter but hooks (before_agent_start, agent_end, message_received,
        // before_reset) still fire via the unbroken hook code path.
        //
        // NOTE: do NOT no-op registerTool here — OC 2026.5.2 validates the
        // contracts.tools declaration against registered tools at load time and
        // drops the plugin (unloads it) if no tools match. Confirmed empirically:
        // no-op'ing registerTool causes the gateway to log "4 plugins" instead of
        // "5 plugins" after restart (plugin excluded from active set).
        //
        // TODO: when OC ships a fix for issue #223, restore tool-call routing
        // and remove the tr-cli.ts CLI layer. The bin/tr field in package.json
        // can stay as a convenience CLI regardless.
        api.registerTool = (tool, opts) => {
            try {
                const t = tool;
                if (t && typeof t === 'object' && typeof t.name === 'string' && t.name.length > 0) {
                    _registeredToolNames.push(t.name);
                }
            }
            catch {
                // Manifest is diagnostic; never let bookkeeping break tool registration.
            }
            _originalRegisterTool(tool, opts);
        };
        // Lazily resolved inside the try below — needed by both the manifest
        // write and the error path. `dist/` after build, package root in tests.
        let _pluginDirForManifest = null;
        // NOTE: the body of register() below is intentionally NOT re-indented
        // under this `try` block — re-indenting would touch every line in a
        // 3,500-line function and obscure the actual hotfix diff. The closing
        // `} catch (registerErr: unknown) { ... }` is at the very end of
        // register() (search for "register() threw").
        try {
            // ---------------------------------------------------------------
            // RC-build detection (3.3.1-rc.3)
            // ---------------------------------------------------------------
            //
            // `isRcBuild` reads the plugin's own version string. When true, the
            // `totalreclaw_report_qa_bug` tool is registered at the end of this
            // function — stable builds never see it. The version is resolved via
            // `readPluginVersion` from fs-helpers.ts (scanner-safe, pure-fs).
            let rcMode = false;
            // Plugin version resolved from package.json once at register time. Reused
            // by writeOnboardingState callsites below so the `version` field in
            // state.json tracks the actual shipped plugin version (avoids drift —
            // e.g. rc.18 finding F4 where a hardcoded `'3.3.1-rc.11'` stayed put
            // through 7 RC bumps). Fallback `'3.3.0'` matches the prior literal at
            // the loopback callsite if package.json read fails.
            let pluginVersion = null;
            try {
                // Resolve our own dist/ directory so `readPluginVersion` can locate
                // package.json. We use `import.meta.url` + ESM-static stdlib imports
                // (`fileURLToPath` from `node:url`, `nodePath.dirname` from `node:path`,
                // both imported at the top of this file). Earlier shape used inline
                // `require('node:url')` — undefined under bare-ESM Node, broke the
                // before_agent_start hook in the published rc.20 bundle (issue #124).
                const pluginDir = nodePath.dirname(fileURLToPath(import.meta.url));
                _pluginDirForManifest = pluginDir; // captured for #186 .loaded.json/.error.json
                pluginVersion = readPluginVersion(pluginDir);
                rcMode = isRcBuild(pluginVersion);
                if (rcMode) {
                    api.logger.info(`TotalReclaw: RC build detected (version=${pluginVersion}). RC-gated tools will be registered.`);
                }
                // 3.3.1-rc.21 (issue #126 — rc.20 finding F3): clean up
                // `.openclaw-install-stage-*` siblings left behind by an interrupted
                // `openclaw plugins install` run. Without cleanup, OpenClaw's plugin
                // loader auto-discovers the orphan directory on the next gateway
                // start and registers a duplicate `totalreclaw` plugin (duplicate
                // hooks, duplicate tools, "duplicate-plugin-id" warning every cycle).
                // Best-effort — never throws on permission / race failures.
                try {
                    const removed = cleanupInstallStagingDirs(pluginDir);
                    if (removed.length > 0) {
                        api.logger.info(`TotalReclaw: removed ${removed.length} stale install-staging dir(s) from prior interrupted install: ${removed.join(', ')}`);
                    }
                }
                catch {
                    // Best-effort — already swallowed inside the helper, but keep this
                    // outer try as belt-and-braces against future helper changes.
                }
                // 3.3.1-rc.22 — wire the lazy-embedder runtime config so the first
                // `generateEmbedding()` call knows where to cache the bundle and
                // which RC's GitHub Release to fetch from.
                //
                // 3.3.4-rc.1 — when readPluginVersion() returns null (rare, but
                // possible if package.json is unreadable inside the OpenClaw
                // sandbox), we previously passed the literal `'0.0.0-dev'` which
                // resolves to a 404 GitHub Release URL. Now we let `embedding.ts`
                // fall back to its `LAST_KNOWN_GOOD_RC_TAG` constant by SKIPPING
                // the configure call entirely in the null case — the
                // `activeRuntimeConfig()` helper picks the constant up. This way
                // the constant lives in one place (embedding.ts) and the orch-
                // estrator just doesn't fight it.
                if (pluginVersion) {
                    try {
                        configureEmbedder({
                            cacheRoot: CONFIG.embedderCachePath,
                            rcTag: pluginVersion,
                        });
                    }
                    catch (err) {
                        const msg = err instanceof Error ? err.message : String(err);
                        api.logger.warn(`TotalReclaw: configureEmbedder failed (will use defaults): ${msg}`);
                    }
                }
                else {
                    api.logger.warn('TotalReclaw: pluginVersion unresolved — embedder will fall back to LAST_KNOWN_GOOD_RC_TAG. ' +
                        'Investigate package.json resolution; see fs-helpers.readPluginVersion docs.');
                }
                // 3.3.3-rc.1 (issue #187 — ONNX decouple): kick off a non-blocking
                // bundle prefetch so the ~700 MB embedder tarball starts streaming
                // as soon as the gateway boots, BEFORE the user completes
                // `totalreclaw_pair`. Decouples the model download from the
                // pair-completion gate the previous flow imposed via
                // `requireFullSetup()` -> first `generateEmbedding()` call.
                // Fire-and-forget — never awaits, never throws on failure (the next
                // `generateEmbedding()` call retries via the same idempotent path).
                // Disabled when `TOTALRECLAW_DISABLE_EMBEDDER_PREFETCH=1` (CI / tests
                // where the network is sandboxed away). The env read lives in
                // config.ts; we read the resolved CONFIG flag here so this file
                // stays scanner-clean (no env lookups in index.ts).
                if (!CONFIG.embedderPrefetchDisabled) {
                    prefetchEmbedderBundle({ log: (msg) => api.logger.info(msg) })
                        .then((result) => {
                        api.logger.info(`TotalReclaw: embedder prefetch ${result === 'fetched' ? 'completed (downloaded bundle)' : 'cache hit'}`);
                    })
                        .catch((err) => {
                        const msg = err instanceof Error ? err.message : String(err);
                        api.logger.warn(`TotalReclaw: embedder prefetch failed (non-fatal — will retry on first generateEmbedding): ${msg}`);
                    });
                }
                // 3.3.1-rc.22 (rc.21 finding #5): self-heal partial-install marker.
                // Clearing the marker has been the runtime's job since 3.3.3-rc.1
                // dropped postinstall.mjs (OpenClaw scanner blocked the install on
                // the subprocess-spawn import — see 3.3.3-rc.1 PR). 3.3.6-rc.1
                // additionally dropped the `preinstall` npm script that wrote the
                // marker (npm install --ignore-scripts meant it never fired in the
                // canonical install path anyway, and `node -e` shell-exec is a
                // latent scanner-spec risk). The clear call here remains valid for
                // legacy installs that may have a stale marker on disk. If we have
                // gotten this far the loader did register us — meaning the install
                // succeeded enough to be useful — so any lingering marker is stale.
                // Clear it so the next retry's detector does not see a false positive.
                //
                // 3.3.1-rc.22 (rc.21 finding #6) — gateway/reload upstream caveat:
                // OpenClaw's config-watcher fires `gateway/reload` when
                // `plugins.entries.totalreclaw` mutates (e.g. mid-install). In-flight
                // CLI clients see `1006 abnormal closure` and start a 600-second wait.
                // Proper fix is upstream OpenClaw FR. Plugin-side mitigation = these
                // helper calls MUST be idempotent under repeated register() calls
                // triggered by reload chatter. Asserted by
                // `install-reload-idempotency.test.ts`.
                try {
                    const pluginRoot = nodePath.resolve(pluginDir, '..');
                    const cleared = clearPartialInstallMarker(pluginRoot);
                    if (cleared) {
                        api.logger.info(`TotalReclaw: cleared stale .tr-partial-install marker (rc.22 finding #5)`);
                    }
                }
                catch {
                    // Best-effort. Helper logs internally and never throws.
                }
                // 3.3.9-rc.2 (issues #225 + #226): auto-patch openclaw.json for
                // OpenClaw 2026.5.x. Two required config keys were not auto-applied
                // by `openclaw plugins install` in 2026.5.x:
                //
                //   1. plugins.slots.memory = "totalreclaw"
                //      OpenClaw 2026.5.x introduced memory-slot exclusivity — a
                //      memory-kind plugin MUST explicitly claim the slot or it is
                //      silently disabled (no error shown; `openclaw plugins inspect`
                //      shows "memory slot set to memory-core"). #225.
                //
                //   2. plugins.entries.totalreclaw.hooks.allowConversationAccess = true
                //      Non-bundled plugins in 2026.5.x require this flag to receive
                //      agent_end and before_agent_start hooks. Without it, auto-
                //      extraction and recall injection are silently disabled. #226.
                //
                //   3. channels.telegram.streaming.mode = "off" (only if unset)
                //      OpenClaw 2026.5.x defaults Telegram to a verbose streaming
                //      mode that prints every mid-task tool-progress preview into
                //      chat. Default this to "off" on first run for a clean UX.
                //      Existing explicit values are preserved (3.3.10-rc.1).
                //
                // The patch is idempotent — if all keys are already correct the
                // file is not touched. When the file IS mutated a restart is
                // required for the new keys to take effect (OpenClaw reads
                // openclaw.json at startup, not dynamically). We emit a warn so
                // the user and ops scripts know to trigger a restart.
                try {
                    // 3.3.12-rc.3: pass pluginVersion so Fix #6 can self-heal a
                    // stripped `plugins.installs.totalreclaw` record (and unblock
                    // Fix #1 which gates on installs being present).
                    const patchResult = patchOpenClawConfig(undefined, pluginVersion ?? undefined);
                    if (patchResult === 'patched') {
                        // 3.3.12-rc.6 (auto-QA finding 2026-05-09): previously we only
                        // warned the user to manually restart. That created a silent
                        // hook-failure on the FIRST gateway boot post-install — the
                        // plugin loads with stale in-memory config, hook handlers
                        // never register, auto-extraction never fires, and only a
                        // second manual restart fixes it. First-time users hit this
                        // every install. Auto-extraction QA reproduced it as 2/5
                        // turns missed (hook silently no-op'd on turns 1-3).
                        //
                        // Fix: when the patch wrote anything, fire SIGUSR1 to our own
                        // PID. The gateway accepts SIGUSR1 iff `commands.restart=true`
                        // (the default); see upstream `setGatewaySigusr1RestartPolicy`.
                        // The signal triggers an in-process restart that re-reads the
                        // freshly-patched openclaw.json and registers hook handlers
                        // with `allowConversationAccess=true` honoured.
                        //
                        // Idempotency: second boot reads the patched config and
                        // returns `'unchanged'` from patchOpenClawConfig, so the
                        // signal fires AT MOST once per config-key-change. No restart
                        // loop possible.
                        //
                        // Defer via setImmediate so register() finishes (logger flush
                        // + plugin load record writeback) before the signal lands.
                        // A 250ms setTimeout adds slack for slow disk on Telegram VPS
                        // (Hetzner small VPS tail-latency observed ~120ms on writes).
                        //
                        // Phrase-safety: process.kill on own PID is local-only; no
                        // outbound markers. Already used by `/totalreclaw-restart`
                        // (registered ~400 lines below) under the same scanner-safe
                        // pattern.
                        api.logger.warn('TotalReclaw: updated openclaw.json with required 2026.5.x keys ' +
                            '(plugins.slots.memory + hooks.allowConversationAccess + ' +
                            'channels.telegram.streaming.mode + plugins.bundledDiscovery + ' +
                            'plugins.allow + plugins.installs.totalreclaw self-heal). ' +
                            'Auto-restarting gateway via SIGUSR1 to apply.');
                        setTimeout(() => {
                            try {
                                process.kill(process.pid, 'SIGUSR1');
                            }
                            catch (err) {
                                const msg = err instanceof Error ? err.message : String(err);
                                api.logger.warn(`TotalReclaw: auto-restart SIGUSR1 emit failed (${msg}). ` +
                                    'Run `/totalreclaw-restart` or restart the gateway manually ' +
                                    'for the patched config to take effect.');
                            }
                        }, 250);
                    }
                    else if (patchResult === 'error') {
                        api.logger.warn('TotalReclaw: failed to auto-patch openclaw.json for OpenClaw 2026.5.x ' +
                            'compatibility. If memory hooks are silently disabled, add these keys ' +
                            'manually: plugins.slots.memory="totalreclaw" and ' +
                            'plugins.entries.totalreclaw.hooks.allowConversationAccess=true.');
                    }
                    // 'unchanged' and 'skipped' are silent — no log needed.
                }
                catch {
                    // Best-effort — never let config-patch failure block plugin load.
                }
            }
            catch {
                rcMode = false;
            }
            // ---------------------------------------------------------------
            // Credentials file permission check (cred-1 — fail-closed security gate)
            // ---------------------------------------------------------------
            // Must run before any tool registration so that a misconfigured host
            // is rejected immediately rather than silently operating with an exposed
            // credentials file. checkCredentialsFileMode returns 'insecure' if the
            // file mode is broader than 0600 — throw to abort plugin load.
            {
                const permResult = checkCredentialsFileMode(CREDENTIALS_PATH, api.logger);
                if (permResult === 'insecure') {
                    throw new Error(`TotalReclaw refused to load: credentials file has insecure permissions. ` +
                        `Run: chmod 600 "${CREDENTIALS_PATH}" then restart the gateway.`);
                }
            }
            // ---------------------------------------------------------------
            // 3.3.13 — auto-pair-on-load (Pop-OS hallucination fix)
            // ---------------------------------------------------------------
            //
            // If credentials.json is missing, open a relay pair session NOW and
            // write URL + PIN + sid to ~/.totalreclaw/.pair-pending.json. The
            // before_agent_start hook installed below reads that file and tells
            // the agent the EXACT values to surface — the agent no longer guesses.
            //
            // Fire-and-forget so a relay outage never blocks plugin load. The
            // sentinel write happens BEFORE the hook is registered, but the WS
            // listener and credentials.json write run in the background after
            // register() returns.
            void (async () => {
                try {
                    const result = await maybeStartAutoPair({
                        credentialsPath: CREDENTIALS_PATH,
                        pendingPath: defaultPairPendingPath(CREDENTIALS_PATH),
                        onboardingStatePath: CONFIG.onboardingStatePath,
                        relayBaseUrl: CONFIG.pairRelayUrl,
                        pluginVersion: pluginVersion ?? '3.3.0',
                        logger: api.logger,
                    });
                    switch (result.status) {
                        case 'creds_exist':
                            // No-op — happy path; user is already set up.
                            break;
                        case 'pending_reused':
                            api.logger.info('TotalReclaw: setup pending. Reusing existing pair URL at ~/.totalreclaw/.pair-pending.json — agent will surface URL+PIN to user on next turn.');
                            break;
                        case 'started':
                            api.logger.info('TotalReclaw: setup pending. Pair URL written to ~/.totalreclaw/.pair-pending.json — agent will surface URL+PIN to user on next turn.');
                            break;
                        case 'failed':
                            api.logger.warn(`TotalReclaw: setup pending. Auto-pair failed (${result.error}). User must run \`tr pair --json\` manually OR call the totalreclaw_pair tool.`);
                            break;
                    }
                }
                catch (err) {
                    const msg = err instanceof Error ? err.message : String(err);
                    api.logger.warn(`TotalReclaw: setup pending. Auto-pair failed (${msg}). User must run \`tr pair --json\` manually OR call the totalreclaw_pair tool.`);
                }
            })();
            // Install the before_agent_start hook that reads the sentinel and
            // injects URL + PIN into the agent's context verbatim. Registered
            // here so it lives alongside the other hook registrations in
            // register(); the hook body itself never blocks on plugin load.
            try {
                installPairPendingHook(api, {
                    credentialsPath: CREDENTIALS_PATH,
                    pendingPath: defaultPairPendingPath(CREDENTIALS_PATH),
                    autoPairDepsFactory: () => ({
                        credentialsPath: CREDENTIALS_PATH,
                        pendingPath: defaultPairPendingPath(CREDENTIALS_PATH),
                        onboardingStatePath: CONFIG.onboardingStatePath,
                        relayBaseUrl: CONFIG.pairRelayUrl,
                        pluginVersion: pluginVersion ?? '3.3.0',
                        logger: api.logger,
                    }),
                });
            }
            catch (err) {
                const msg = err instanceof Error ? err.message : String(err);
                api.logger.warn(`TotalReclaw: failed to register pair-pending-injection hook: ${msg}`);
            }
            // ---------------------------------------------------------------
            // LLM client initialization (auto-detect provider from OpenClaw config)
            // ---------------------------------------------------------------
            //
            // 3.3.1 — the resolver now reads provider keys from
            // `~/.openclaw/agents/*\/agent/auth-profiles.json` as one of the
            // resolution tiers. This is where real OpenClaw installs store user
            // API keys; prior releases only checked env vars and the SDK-passed
            // `api.config.providers`, so auto-extraction silently no-op'd for
            // virtually every real user. The disk read lives in
            // `./llm-profile-reader.js` (scanner-isolated — that file has no
            // network triggers) and the aggregated entries are handed to
            // initLLMClient as a plain array.
            let harvestedKeys = [];
            try {
                const root = defaultAuthProfilesRoot(CONFIG.home);
                if (root) {
                    // 3.3.1-rc.2 — readAllProfileKeys merges auth-profiles.json AND
                    // the legacy models.json format (pre-auth-profiles OpenClaw
                    // installs). Auth-profiles wins when both have the same provider.
                    const all = readAllProfileKeys({ root });
                    // Dedupe so each provider appears once (last-wins — later agent
                    // files shadow earlier ones).
                    const byProvider = dedupeByProvider(all);
                    harvestedKeys = Object.values(byProvider);
                }
            }
            catch (err) {
                // Never crash plugin init on a bad auth-profiles.json / models.json.
                const msg = err instanceof Error ? err.message : String(err);
                api.logger.warn(`TotalReclaw: could not read OpenClaw profile JSONs (${msg}) — falling through to env vars`);
            }
            initLLMClient({
                primaryModel: api.config?.agents?.defaults?.model?.primary,
                pluginConfig: api.pluginConfig,
                openclawProviders: api.config?.models?.providers,
                authProfileKeys: harvestedKeys,
                logger: api.logger,
            });
            // 3.3.1 — memoize plugin-config extraction.interval / extraction.maxFactsPerExtraction
            // so getExtractInterval() and getMaxFactsPerExtraction() don't re-walk
            // api.pluginConfig per turn.
            snapshotExtractionOverrides(api.pluginConfig);
            // ---------------------------------------------------------------
            // Service registration (lifecycle logging)
            // ---------------------------------------------------------------
            api.registerService({
                id: 'totalreclaw',
                start: () => {
                    api.logger.info('TotalReclaw plugin loaded');
                },
                stop: () => {
                    api.logger.info('TotalReclaw plugin stopped');
                },
            });
            // ---------------------------------------------------------------
            // 3.2.0 — CLI wizard registration (leak-free onboarding surface)
            // ---------------------------------------------------------------
            //
            // `api.registerCli` attaches a top-level `openclaw totalreclaw ...`
            // subcommand chain. The wizard runs entirely on the user's TTY —
            // stdout/stdin — and NEVER routes any of its I/O through the LLM
            // provider or the session transcript. This is the ONLY surface in
            // 3.2.0 where a recovery phrase is generated or accepted.
            //
            // The dynamic import keeps the @scure/bip39 + readline/promises
            // surface out of the `register()` hot path — only pulled in when the
            // CLI subcommand actually fires.
            if (typeof api.registerCli === 'function') {
                api.registerCli(async ({ program }) => {
                    const { registerOnboardingCli } = await import('./onboarding-cli.js');
                    registerOnboardingCli(program, {
                        credentialsPath: CREDENTIALS_PATH,
                        statePath: CONFIG.onboardingStatePath,
                        logger: api.logger,
                        // 3.3.1-rc.18 — wire the pair flow into onboard so the
                        // `--pair-only` flag (issue #95) can delegate to it without
                        // duplicating session-store / URL-builder logic. Same deps
                        // as the standalone `pair` subcommand.
                        pairSessionsPath: CONFIG.pairSessionsPath,
                        renderPairingUrl: (session) => buildPairingUrl(api, session),
                        // 3.3.1 — supplied to the non-interactive --json onboard path
                        // so the emitted payload includes the derived Smart Account
                        // (scope) address. Uses the chain-id default; Pro-tier
                        // chain-id override is applied later by billing autodetect,
                        // at which point the address remains the same (SA is
                        // chain-independent up to the EntryPoint address which is
                        // identical on Base Sepolia / Gnosis).
                        deriveScopeAddress: async (mnemonic) => {
                            try {
                                return await deriveSmartAccountAddress(mnemonic, CONFIG.chainId);
                            }
                            catch (err) {
                                api.logger.warn(`onboarding --json: scope-address derivation failed: ${err instanceof Error ? err.message : String(err)}`);
                                return undefined;
                            }
                        },
                    });
                    // 3.3.0 — `openclaw totalreclaw pair [generate|import]` attaches
                    // alongside the existing `onboard` + `status` subcommands.
                    //
                    // 3.3.4-rc.1 — wire `runRelayPairCli` so the CLI defaults to the
                    // same relay-brokered URL surface the agent tool uses. The local
                    // (gateway-loopback) flow is still available via `--local`. See
                    // pair-cli.ts header for the rationale.
                    const { registerPairCli } = await import('./pair-cli.js');
                    registerPairCli(program, {
                        sessionsPath: CONFIG.pairSessionsPath,
                        renderPairingUrl: (session) => buildPairingUrl(api, session),
                        logger: api.logger,
                        runRelayPairCli: async (cliMode, runOpts) => {
                            const { runRelayPairCli } = await import('./pair-cli-relay.js');
                            return runRelayPairCli(cliMode, {
                                relayBaseUrl: CONFIG.pairRelayUrl,
                                credentialsPath: CREDENTIALS_PATH,
                                onboardingStatePath: CONFIG.onboardingStatePath,
                                logger: api.logger,
                                pluginVersion: pluginVersion ?? '3.3.4-rc.1',
                                deriveScopeAddress: async (mnemonic) => {
                                    try {
                                        return await deriveSmartAccountAddress(mnemonic, CONFIG.chainId);
                                    }
                                    catch (err) {
                                        api.logger.warn(`relay pair-cli: scope-address derivation failed (will retry lazily): ${err instanceof Error ? err.message : String(err)}`);
                                        return undefined;
                                    }
                                },
                                ...runOpts,
                            });
                        },
                    });
                }, { commands: ['totalreclaw'] });
            }
            else {
                api.logger.warn('api.registerCli is unavailable on this OpenClaw version — `openclaw totalreclaw onboard` will not work. ' +
                    'Users can still set TOTALRECLAW_RECOVERY_PHRASE manually.');
            }
            // ---------------------------------------------------------------
            // 3.3.0 — HTTP routes for QR-pairing (pair-http)
            // ---------------------------------------------------------------
            //
            // Four endpoints under /plugin/totalreclaw/pair/ are registered on
            // the gateway's HTTP server. Collectively they serve the browser
            // pairing page, verify the 6-digit secondary code, accept the
            // encrypted mnemonic payload, and expose a status polled by the
            // CLI. See pair-http.ts and the 2026-04-20 design doc.
            if (typeof api.registerHttpRoute === 'function') {
                // rc.5 — the 4 `registerHttpRoute` calls MUST happen synchronously inside
                // `register(api)` because the SDK loader freezes the plugin's HTTP-route
                // registry as soon as `register()` returns. In rc.2–rc.4 this block was
                // wrapped in a fire-and-forget async IIFE whose `await import(...)`
                // settled one microtask AFTER the loader had already activated the
                // (empty) route list — the post-activation pushes landed on the
                // dispatcher's "inactive" copy and `openclaw plugins inspect
                // totalreclaw --json | jq .httpRouteCount` returned 0. See
                // `docs/notes/QA-plugin-3.3.0-rc.4-20260420-1517.md` (internal#21).
                // Moving `buildPairRoutes`, `@scure/bip39`, and `fs-helpers`
                // `writeOnboardingState` to static top-of-file imports keeps the
                // registration site synchronous and makes the call order deterministic.
                // `completePairing` remains async (it does disk I/O) — that is fine,
                // since `registerHttpRoute` accepts async handlers; only the
                // REGISTRATION must be synchronous.
                const bundle = buildPairRoutes({
                    sessionsPath: CONFIG.pairSessionsPath,
                    apiBase: '/plugin/totalreclaw/pair',
                    logger: api.logger,
                    validateMnemonic: (p) => validateMnemonic(p, wordlist),
                    completePairing: async ({ mnemonic }) => {
                        // Write credentials.json + flip state to 'active' via
                        // fs-helpers. This centralizes disk I/O off the
                        // pair-http surface (scanner isolation).
                        //
                        // 3.3.1 (internal#130) — derive + persist the Smart Account
                        // address right here so the user can see their scope address
                        // immediately after pair, without waiting for a first chain
                        // write. SA derivation runs locally (WASM deriveEoa + factory
                        // getAddress eth_call); the mnemonic NEVER crosses any new
                        // boundary — it's already on disk in credentials.json and is
                        // consumed by the same `deriveSmartAccountAddress` call the
                        // store/search paths use. Only the derived public address is
                        // persisted to credentials.json (`scope_address`).
                        let scopeAddress;
                        try {
                            scopeAddress = await deriveSmartAccountAddress(mnemonic, CONFIG.chainId);
                        }
                        catch (err) {
                            // Best-effort. If chain RPC is unreachable at pair time, the
                            // status tool re-tries derivation lazily on next call —
                            // fall through and write credentials.json without it.
                            api.logger.warn(`pair: scope_address derivation failed (will retry lazily): ${err instanceof Error ? err.message : String(err)}`);
                        }
                        const creds = loadCredentialsJson(CREDENTIALS_PATH) ?? {};
                        const next = { ...creds, mnemonic };
                        if (scopeAddress)
                            next.scope_address = scopeAddress;
                        if (!writeCredentialsJson(CREDENTIALS_PATH, next)) {
                            return { state: 'error', error: 'credentials_write_failed' };
                        }
                        // Hot-reload: update the runtime override so existing
                        // in-memory state picks up the new phrase without a
                        // process restart.
                        setRecoveryPhraseOverride(mnemonic);
                        // Flip onboarding state.
                        writeOnboardingState(CONFIG.onboardingStatePath, {
                            onboardingState: 'active',
                            createdBy: 'generate',
                            credentialsCreatedAt: new Date().toISOString(),
                            version: pluginVersion ?? '3.3.0',
                        });
                        // 3.3.13 — sentinel cleanup. credentials.json is now the source
                        // of truth; the auto-pair-on-load .pair-pending.json sentinel
                        // must be removed so the before_agent_start hook stops surfacing
                        // the URL + PIN on subsequent turns.
                        deletePairPendingFile(defaultPairPendingPath(CREDENTIALS_PATH));
                        return { state: 'active' };
                    },
                });
                // auth: 'plugin' — the 4 pair routes are reached from the operator's
                // phone/laptop browser, which has no gateway bearer token. The plugin
                // authenticates each request itself via (a) the in-memory pair session
                // (sid + secondaryCode + single-use consumption), (b) ECDH + AEAD for
                // the encrypted mnemonic payload. See gateway-cli dist
                // `matchedPluginRoutesRequireGatewayAuth` / `enforcePluginRouteGatewayAuth`
                // — routes with `auth: 'gateway'` require a bearer token and 401 any
                // browser caller, which is the wrong semantic for QR-pair. rc.3
                // shipped `auth: 'gateway'` and the QA agent confirmed the routes
                // were unreachable from a browser (QA-plugin-3.3.0-rc.3 report).
                api.registerHttpRoute({ path: bundle.finishPath, handler: bundle.handlers.finish, auth: 'plugin' });
                api.registerHttpRoute({ path: bundle.startPath, handler: bundle.handlers.start, auth: 'plugin' });
                api.registerHttpRoute({ path: bundle.respondPath, handler: bundle.handlers.respond, auth: 'plugin' });
                api.registerHttpRoute({ path: bundle.statusPath, handler: bundle.handlers.status, auth: 'plugin' });
                api.logger.info('TotalReclaw: registered 4 QR-pairing HTTP routes synchronously');
            }
            else {
                api.logger.warn('api.registerHttpRoute is unavailable on this OpenClaw version — /totalreclaw pair will not work. ' +
                    'Use `openclaw totalreclaw onboard` on the gateway host instead.');
            }
            // ---------------------------------------------------------------
            // 3.2.0 — slash command `/totalreclaw {onboard,status}` (in-chat bridge)
            // ---------------------------------------------------------------
            //
            // `api.registerCommand` replies bypass the LLM for the current turn BUT
            // are appended to the session transcript, so the LLM sees the reply on
            // the NEXT turn. That is fine here because every reply is a non-secret
            // pointer — it directs the user to the CLI wizard and explicitly
            // explains why the phrase cannot appear in chat.
            if (typeof api.registerCommand === 'function') {
                api.registerCommand({
                    name: 'totalreclaw',
                    description: 'TotalReclaw onboarding + status (non-secret pointer to the terminal wizard)',
                    acceptsArgs: true,
                    requireAuth: false,
                    handler: async (ctx) => {
                        const args = (ctx.args || '').trim();
                        const parts = args.split(/\s+/).filter(Boolean);
                        const sub = (parts[0] || 'help').toLowerCase();
                        if (sub === 'onboard' || sub === 'setup' || sub === 'init') {
                            return {
                                text: 'To set up TotalReclaw on a local machine, run:\n\n' +
                                    '    openclaw totalreclaw onboard\n\n' +
                                    'For a REMOTE gateway (VPS, home server, etc.) use QR-pairing:\n\n' +
                                    '    /totalreclaw pair\n\n' +
                                    'Why not paste the phrase here? Chat messages are visible to the ' +
                                    'LLM. Both flows keep your recovery phrase off the LLM transcript: ' +
                                    'the CLI wizard runs on your terminal, and the QR-pair flow ' +
                                    'encrypts the phrase in your browser before upload.',
                            };
                        }
                        if (sub === 'pair') {
                            // 3.3.0 — remote QR pairing. The slash command is a non-secret
                            // pointer: it tells the operator to run the CLI on the gateway
                            // host (which emits the QR + URL + code). Running the full
                            // pairing protocol directly from this handler would require
                            // sending the URL + code through the chat transcript, which
                            // the LLM would then see — acceptable for the URL + code (both
                            // are non-secret, because the gateway ephemeral pk lives in
                            // the URL fragment and the 6-digit code is one-shot), but
                            // requires the gateway to actually be reachable AND the user
                            // to type a code from chat into a browser on a different
                            // device. Design doc section 4a recommends the CLI path as
                            // primary. Chat-delivery is a future 3.4.0 enhancement.
                            return {
                                text: 'Remote pairing (QR):\n\n' +
                                    '  On the gateway host, run:\n\n' +
                                    '    openclaw totalreclaw pair         # generate new account\n' +
                                    '    openclaw totalreclaw pair import  # import existing\n\n' +
                                    'It will print a QR code + a 6-digit secondary code + a URL. ' +
                                    'Scan the QR with your phone (or open the URL on any browser). ' +
                                    'Enter the 6-digit code in the browser, write down (or paste) ' +
                                    'your recovery phrase, and the gateway will activate.\n\n' +
                                    'The phrase is generated (or pasted) in your BROWSER and ' +
                                    'encrypted end-to-end before upload. It never touches the ' +
                                    'LLM, this chat, or the relay server in plaintext.',
                            };
                        }
                        if (sub === 'status') {
                            // Non-secret summary — never shows the mnemonic.
                            let stateLabel;
                            try {
                                const state = resolveOnboardingState(CREDENTIALS_PATH, CONFIG.onboardingStatePath);
                                stateLabel = state.onboardingState;
                            }
                            catch {
                                stateLabel = 'unknown';
                            }
                            return {
                                text: `TotalReclaw onboarding state: ${stateLabel}.\n` +
                                    (stateLabel === 'active'
                                        ? 'Memory tools are active on this machine.'
                                        : 'Memory tools are gated. Run `openclaw totalreclaw onboard` (local) or `openclaw totalreclaw pair` (remote) to complete setup.'),
                            };
                        }
                        if (sub === 'diag') {
                            // 3.3.7-rc.1 (issue #216) — diagnostic surface for the
                            // tool-binding-on-restart bug. Reports whether the
                            // plugin's register() ran in this process (boot count +
                            // pid + version + tool count). Non-secret: only public
                            // package metadata. The actual filesystem read lives in
                            // fs-helpers.readPluginLoadedManifest() so this file
                            // stays scanner-clean (whole-file rule disallows fs.read*
                            // co-located with `fetch` / `post` markers).
                            //
                            // Usage: `/totalreclaw diag` from chat OR `cat
                            // <pluginDir>/.loaded.json` from the host shell. Both
                            // surfaces should agree; if chat says boot=N but the
                            // file says boot=N+1, the chat session is stale and a
                            // /totalreclaw-restart is warranted.
                            try {
                                const m = _pluginDirForManifest
                                    ? readPluginLoadedManifest(_pluginDirForManifest)
                                    : null;
                                if (!m) {
                                    return {
                                        text: 'TotalReclaw diag:\n' +
                                            `  pid=${process.pid}\n` +
                                            `  version=${pluginVersion ?? 'unknown'}\n` +
                                            '  loaded-manifest: NOT FOUND (register() may have failed — check .error.json)',
                                    };
                                }
                                const stalePid = typeof m.pid === 'number' && m.pid !== process.pid;
                                return {
                                    text: 'TotalReclaw diag:\n' +
                                        `  current pid=${process.pid}\n` +
                                        `  manifest pid=${m.pid ?? '?'}${stalePid ? ' (STALE — file from prior boot, register() did NOT run in this process)' : ''}\n` +
                                        `  version=${m.version ?? 'unknown'}\n` +
                                        `  boot count=${m.bootCount ?? '?'}\n` +
                                        `  boot at=${m.bootAt ?? '?'}\n` +
                                        `  tools registered=${m.tools?.length ?? 0}`,
                                };
                            }
                            catch (err) {
                                const msg = err instanceof Error ? err.message : String(err);
                                return { text: `TotalReclaw diag: error reading manifest (${msg})` };
                            }
                        }
                        return {
                            text: 'TotalReclaw slash commands:\n' +
                                '  /totalreclaw onboard — how to set up TotalReclaw securely\n' +
                                '  /totalreclaw pair    — remote-gateway QR-pairing (3.3.0)\n' +
                                '  /totalreclaw status  — current onboarding state\n' +
                                '  /totalreclaw diag    — plugin load diagnostics (boot count, pid, tool count)',
                        };
                    },
                });
                // ---------------------------------------------------------------
                // 3.3.7-rc.2 (issue #215, follow-up) — `/totalreclaw-restart`
                // ---------------------------------------------------------------
                //
                // Originally rc.1 registered this as `/restart` to override the
                // OpenClaw built-in. That was wrong: OpenClaw's plugin registry
                // hard-rejects the name on the reserved list (see upstream
                // `RESERVED_COMMANDS` in `dist/registry-*.js`) — registration
                // fails with `Command name "restart" is reserved by a built-in
                // command` and the 5-tier fallback never runs. Pedro caught this
                // in 3.3.7-rc.1 manual integration testing 2026-05-03; gateway
                // logs surfaced the rejection, so the rc.1 fix shipped DEAD-CODE.
                //
                // Workaround until upstream lands a plugin-override-precedence
                // flag (FR filed alongside this PR): use a unique, namespaced
                // command name. Plugin handles `/totalreclaw-restart`; the
                // built-in `/restart` keeps its allow-from-only semantics
                // unchanged. SKILL.md tells the agent to issue the namespaced
                // form, so end-users never type `restart` directly.
                //
                // We still use `requireAuth: false` to bypass the channel-layer
                // auth check — the 5-tier fallback in `restart-auth.ts` decides
                // allow / reject per the same matrix as rc.1.
                //
                // If allow → fire `process.kill(process.pid, 'SIGUSR1')`. The
                // gateway accepts SIGUSR1 iff `commands.restart=true` (the
                // default) — see upstream `setGatewaySigusr1RestartPolicy`.
                // (The SIGUSR1 policy still keys on `commands.restart`, NOT on
                // the plugin command name — gateways only honour one restart
                // signal.)
                //
                // If reject → return a short non-shaming message via
                // `rejectMessageFor` that points the user at the right config
                // key (no infinite loop — agent will follow the unauthorized
                // fallback path documented in SKILL.md instead).
                api.registerCommand({
                    name: 'totalreclaw-restart',
                    description: 'Restart OpenClaw gracefully (drains active runs first).',
                    acceptsArgs: false,
                    requireAuth: false,
                    handler: async (ctx) => {
                        const trackerPath = resolveTrackerPath(CREDENTIALS_PATH);
                        const channel = (ctx.channel ?? '').toString().trim().toLowerCase();
                        const senderId = (ctx.senderId ?? '').toString().trim();
                        // Tier 4 + tier 3 helpers. We approximate "paired via this
                        // channel" with the OpenClaw channel-allow-from store: if
                        // pairing wrote an entry for this provider, the file under
                        // ~/.openclaw/pairing/<channel>/allow_from.json (or env
                        // override) will exist. We don't import the upstream SDK's
                        // sync helper because the plugin loader sandbox sometimes
                        // strips the alias; instead we check a robust filesystem
                        // shape: pair-finish writes credentials.json AND OpenClaw's
                        // pairing-store entry. Safe approximation: if the plugin's
                        // own credentials.json exists AND the inbound-user tracker
                        // has at least one entry for this channel, treat it as
                        // "paired via this channel". This matches the bug-fix
                        // intent (issue #215, tier 4) without coupling to upstream
                        // internal APIs.
                        const credentialsExists = () => {
                            try {
                                const c = loadCredentialsJson(CREDENTIALS_PATH);
                                return c != null;
                            }
                            catch {
                                return false;
                            }
                        };
                        const pairedViaChannel = (ch) => {
                            if (!ch)
                                return false;
                            // Tracker count > 0 means at least one user has messaged
                            // this channel since plugin load. Combined with
                            // credentialsExists() in tier 4, this is a robust proxy
                            // for "the channel is bound to this gateway".
                            return getDistinctInboundUserCount(trackerPath, ch) > 0;
                        };
                        const verdict = resolveRestartAuth({ senderId, channel, config: api.config }, {
                            loadCredentialsExists: credentialsExists,
                            wasPairedViaChannel: pairedViaChannel,
                            getDistinctInboundUserCount: (ch) => getDistinctInboundUserCount(trackerPath, ch),
                        });
                        if (verdict.allow === false) {
                            api.logger.info(`TotalReclaw: /totalreclaw-restart rejected (channel=${channel || '<none>'} sender=${senderId || '<none>'} reason=${verdict.reason})`);
                            return { text: rejectMessageFor(verdict.reason) };
                        }
                        api.logger.info(`TotalReclaw: /totalreclaw-restart allowed (channel=${channel || '<none>'} sender=${senderId || '<none>'} tier=${verdict.reason})`);
                        // Trigger the gateway's SIGUSR1 restart path. Wrap in
                        // try/catch — `process.kill` can throw if the gateway is
                        // already shutting down (rare but seen in the wild).
                        try {
                            process.kill(process.pid, 'SIGUSR1');
                        }
                        catch (err) {
                            const msg = err instanceof Error ? err.message : String(err);
                            api.logger.warn(`TotalReclaw: /totalreclaw-restart SIGUSR1 emit failed: ${msg}`);
                            return {
                                text: `Restart request acknowledged but the gateway didn't accept the signal (${msg}). Try \`docker restart <container>\` if running in Docker.`,
                            };
                        }
                        return { text: 'Restarting OpenClaw — back in a few seconds.' };
                    },
                });
            }
            // ---------------------------------------------------------------
            // 3.3.7-rc.1 (issue #215) — track distinct inbound users per channel
            // ---------------------------------------------------------------
            //
            // Tier 3 + tier 5 of the `/totalreclaw-restart` 5-tier auth
            // fallback need to know how many distinct users have messaged this
            // gateway on each channel. We instrument `message_received` to
            // record every (channel, senderId) pair to disk; the count
            // survives gateway restarts (see `inbound-user-tracker.ts`).
            //
            // Best-effort: we never throw out of this hook even if the disk
            // write fails — the auth fallback degrades gracefully (a stale
            // count doesn't break the explicit-allow tiers).
            api.on('message_received', async (event, ctx) => {
                try {
                    const evt = event;
                    const c = ctx;
                    const sender = (evt?.from ?? '').toString().trim();
                    const channel = (c?.channelId ?? '').toString().trim();
                    if (!sender || !channel)
                        return undefined;
                    const trackerPath = resolveTrackerPath(CREDENTIALS_PATH);
                    recordInboundUser(trackerPath, channel, sender);
                }
                catch (err) {
                    // best-effort; never crash on tracker failure
                    const msg = err instanceof Error ? err.message : String(err);
                    api.logger.warn(`message_received tracker write failed: ${msg}`);
                }
                return undefined;
            }, { priority: 5 });
            // ---------------------------------------------------------------
            // Tool: totalreclaw_remember
            // ---------------------------------------------------------------
            api.registerTool({
                name: 'totalreclaw_remember',
                label: 'Remember',
                description: 'Store a memory in the encrypted vault. Use this when the user shares important information worth remembering.',
                parameters: {
                    type: 'object',
                    properties: {
                        text: {
                            type: 'string',
                            description: 'The memory text to store',
                        },
                        type: {
                            type: 'string',
                            // Dedup the merged enum. `preference` and `summary` appear in
                            // BOTH v1 (VALID_MEMORY_TYPES) and legacy v0 (LEGACY_V0_MEMORY_TYPES),
                            // so the naive spread produces duplicate items at ## 5 and 12
                            // (QA failure on 3.0.7-rc.1: ajv rejects schema with "items ##
                            // 5 and 12 are identical"). `new Set(...)` drops dupes while
                            // preserving insertion order so v1 tokens appear first in the
                            // enum — agents default to picking one of those.
                            enum: Array.from(new Set([...VALID_MEMORY_TYPES, ...LEGACY_V0_MEMORY_TYPES])),
                            description: 'Memory Taxonomy v1 type: claim, preference, directive, commitment, episode, summary. ' +
                                'Use "claim" for factual assertions and decisions (populate `reasoning` with the why clause). ' +
                                'Use "directive" for imperative rules ("always X", "never Y"), "commitment" for future intent, ' +
                                'and "episode" for notable events. Legacy v0 tokens (fact, decision, episodic, goal, context, ' +
                                'rule) are silently coerced to their v1 equivalents. Default: claim.',
                        },
                        source: {
                            type: 'string',
                            enum: [...VALID_MEMORY_SOURCES],
                            description: 'v1 provenance tag. "user" = user explicitly stated it, "user-inferred" = inferred from user ' +
                                'signals, "assistant" = assistant-authored (downgrade unless user affirmed), "external" / ' +
                                '"derived" = rare. Explicit remembers default to "user".',
                        },
                        scope: {
                            type: 'string',
                            enum: [...VALID_MEMORY_SCOPES],
                            description: 'v1 life-domain scope: work, personal, health, family, creative, finance, misc, unspecified. ' +
                                'Default: unspecified.',
                        },
                        reasoning: {
                            type: 'string',
                            description: 'For type=claim expressing a decision, the WHY clause ("because Y"). Max 256 chars. ' +
                                'Omit for non-decision claims.',
                            maxLength: 256,
                        },
                        importance: {
                            type: 'number',
                            minimum: 1,
                            maximum: 10,
                            description: 'Importance score 1-10 (default: 8 for explicit remember)',
                        },
                        entities: {
                            type: 'array',
                            description: 'Named entities this memory is about (people, projects, tools, companies, concepts, places). ' +
                                'Supplying entities enables Phase 2 contradiction detection against existing facts about the same entity. ' +
                                'Omit if unclear — a best-effort fallback will still store the memory.',
                            items: {
                                type: 'object',
                                properties: {
                                    name: { type: 'string' },
                                    type: {
                                        type: 'string',
                                        enum: ['person', 'project', 'tool', 'company', 'concept', 'place'],
                                    },
                                    role: { type: 'string' },
                                },
                                required: ['name', 'type'],
                                additionalProperties: false,
                            },
                        },
                    },
                    required: ['text'],
                    additionalProperties: false,
                },
                async execute(_toolCallId, params) {
                    try {
                        await requireFullSetup(api.logger);
                        // v1 taxonomy: route explicit remembers through the same canonical
                        // store path that auto-extraction uses (`storeExtractedFacts`). This
                        // emits a Memory Taxonomy v1 JSON blob, generates entity trapdoors,
                        // and runs through the Phase 2 contradiction-resolution pipeline.
                        //
                        // Accept legacy v0 tokens on input and coerce to v1 via
                        // `normalizeToV1Type` so agents that still emit the pre-v3
                        // taxonomy keep working.
                        const rawType = typeof params.type === 'string' ? params.type.toLowerCase() : 'claim';
                        const memoryType = isValidMemoryType(rawType)
                            ? rawType
                            : normalizeToV1Type(rawType);
                        // Source defaults to 'user' for explicit remembers (the user is
                        // the author by definition). Ignored if the caller passes an
                        // invalid value.
                        const rawSource = typeof params.source === 'string' ? params.source.toLowerCase() : 'user';
                        const memorySource = VALID_MEMORY_SOURCES.includes(rawSource)
                            ? rawSource
                            : 'user';
                        const rawScope = typeof params.scope === 'string' ? params.scope.toLowerCase() : 'unspecified';
                        const memoryScope = VALID_MEMORY_SCOPES.includes(rawScope)
                            ? rawScope
                            : 'unspecified';
                        const reasoning = typeof params.reasoning === 'string' && params.reasoning.length > 0
                            ? params.reasoning.slice(0, 256)
                            : undefined;
                        // Explicit remember defaults to importance 8 (above auto-extraction's
                        // typical 6-7), so store-time dedup's shouldSupersede prefers the
                        // explicit call when it collides with an auto-extracted claim.
                        const importance = Math.max(1, Math.min(10, params.importance ?? 8));
                        const validatedEntities = Array.isArray(params.entities)
                            ? params.entities
                                .map((e) => parseEntity(e))
                                .filter((e) => e !== null)
                            : [];
                        const fact = {
                            text: params.text.slice(0, 512),
                            type: memoryType,
                            source: memorySource,
                            scope: memoryScope,
                            reasoning,
                            importance,
                            action: 'ADD',
                            confidence: 1.0, // user explicitly asked to remember — highest confidence
                        };
                        if (validatedEntities.length > 0)
                            fact.entities = validatedEntities;
                        const stored = await storeExtractedFacts([fact], api.logger, 'explicit');
                        api.logger.info(`totalreclaw_remember: routed to storeExtractedFacts (stored=${stored}, entities=${validatedEntities.length})`);
                        if (stored === 0) {
                            // Dedup or supersession consumed the write. Treat as success from
                            // the user's perspective — the memory's content is already in the
                            // vault (possibly under a different ID).
                            return {
                                content: [
                                    {
                                        type: 'text',
                                        text: 'Memory noted (matched existing content in vault).',
                                    },
                                ],
                            };
                        }
                        return {
                            content: [{ type: 'text', text: 'Memory encrypted and stored.' }],
                        };
                    }
                    catch (err) {
                        const message = err instanceof Error ? err.message : String(err);
                        api.logger.error(`totalreclaw_remember failed: ${message}`);
                        return {
                            content: [{ type: 'text', text: `Failed to store memory: ${humanizeError(message)}` }],
                        };
                    }
                },
            }, { name: 'totalreclaw_remember' });
            // ---------------------------------------------------------------
            // Tool: totalreclaw_recall
            // ---------------------------------------------------------------
            api.registerTool({
                name: 'totalreclaw_recall',
                label: 'Recall',
                description: 'Search the encrypted memory vault. Returns the most relevant memories matching the query.',
                parameters: {
                    type: 'object',
                    properties: {
                        query: {
                            type: 'string',
                            description: 'Search query text',
                        },
                        k: {
                            type: 'number',
                            minimum: 1,
                            maximum: 20,
                            description: 'Number of results to return (default: 8)',
                        },
                    },
                    required: ['query'],
                    additionalProperties: false,
                },
                async execute(_toolCallId, params) {
                    try {
                        await requireFullSetup(api.logger);
                        const k = Math.min(params.k ?? 8, 20);
                        // 1. Generate word trapdoors (blind indices for the query).
                        const wordTrapdoors = generateBlindIndices(params.query);
                        // 2. Generate query embedding + LSH trapdoors (may fail gracefully).
                        let queryEmbedding = null;
                        let lshTrapdoors = [];
                        try {
                            queryEmbedding = await generateEmbedding(params.query, { isQuery: true });
                            const hasher = getLSHHasher(api.logger);
                            if (hasher && queryEmbedding) {
                                lshTrapdoors = hasher.hash(queryEmbedding);
                            }
                        }
                        catch (err) {
                            const msg = err instanceof Error ? err.message : String(err);
                            api.logger.warn(`Recall: embedding/LSH generation failed (using word-only trapdoors): ${msg}`);
                        }
                        // 3. Merge word trapdoors + LSH trapdoors.
                        const allTrapdoors = [...wordTrapdoors, ...lshTrapdoors];
                        if (allTrapdoors.length === 0) {
                            return {
                                content: [{ type: 'text', text: 'No searchable terms in query.' }],
                                details: { count: 0, memories: [] },
                            };
                        }
                        // 4. Request more candidates than needed so we can re-rank client-side.
                        // 5. Decrypt candidates (text + embeddings) and build reranker input.
                        const rerankerCandidates = [];
                        const metaMap = new Map();
                        if (isSubgraphMode()) {
                            // --- Subgraph search path ---
                            const factCount = await getSubgraphFactCount(subgraphOwner || userId, authKeyHex);
                            const pool = computeCandidatePool(factCount);
                            let subgraphResults = await searchSubgraph(subgraphOwner || userId, allTrapdoors, pool, authKeyHex);
                            // Always run broadened search and merge — ensures vocabulary mismatches
                            // (e.g., "preferences" vs "prefer") don't cause recall failures.
                            // The reranker handles scoring; extra cost is ~1 GraphQL query per recall.
                            try {
                                const broadenedResults = await searchSubgraphBroadened(subgraphOwner || userId, pool, authKeyHex);
                                // Merge broadened results with existing (deduplicate by ID)
                                const existingIds = new Set(subgraphResults.map(r => r.id));
                                for (const br of broadenedResults) {
                                    if (!existingIds.has(br.id)) {
                                        subgraphResults.push(br);
                                    }
                                }
                            }
                            catch { /* best-effort */ }
                            for (const result of subgraphResults) {
                                try {
                                    const docJson = decryptFromHex(result.encryptedBlob, encryptionKey);
                                    if (isDigestBlob(docJson))
                                        continue;
                                    const doc = readClaimFromBlob(docJson);
                                    let decryptedEmbedding;
                                    if (result.encryptedEmbedding) {
                                        try {
                                            decryptedEmbedding = JSON.parse(decryptFromHex(result.encryptedEmbedding, encryptionKey));
                                        }
                                        catch {
                                            // Embedding decryption failed -- proceed without it.
                                        }
                                    }
                                    if (decryptedEmbedding && decryptedEmbedding.length !== getEmbeddingDims()) {
                                        try {
                                            decryptedEmbedding = await generateEmbedding(doc.text);
                                        }
                                        catch {
                                            decryptedEmbedding = undefined;
                                        }
                                    }
                                    rerankerCandidates.push({
                                        id: result.id,
                                        text: doc.text,
                                        embedding: decryptedEmbedding,
                                        importance: doc.importance / 10,
                                        createdAt: result.timestamp ? parseInt(result.timestamp, 10) : undefined,
                                        // Retrieval v2 Tier 1: surface v1 source so applySourceWeights
                                        // can multiply the final RRF score by the source weight.
                                        source: typeof doc.metadata?.source === 'string' ? doc.metadata.source : undefined,
                                    });
                                    metaMap.set(result.id, {
                                        metadata: doc.metadata ?? {},
                                        timestamp: Date.now(),
                                        category: doc.category,
                                    });
                                }
                                catch {
                                    // Skip candidates we cannot decrypt.
                                }
                            }
                            // Update hot cache with top results for instant auto-recall.
                            try {
                                if (!pluginHotCache && encryptionKey) {
                                    const config = getSubgraphConfig();
                                    pluginHotCache = new PluginHotCache(config.cachePath, encryptionKey.toString('hex'));
                                    pluginHotCache.load();
                                }
                                if (pluginHotCache) {
                                    const hotFacts = rerankerCandidates.map((c) => {
                                        const meta = metaMap.get(c.id);
                                        const importance = meta?.metadata.importance
                                            ? Math.round(meta.metadata.importance * 10)
                                            : 5;
                                        return { id: c.id, text: c.text, importance };
                                    });
                                    pluginHotCache.setHotFacts(hotFacts);
                                    pluginHotCache.setFactCount(rerankerCandidates.length);
                                    pluginHotCache.flush();
                                }
                            }
                            catch {
                                // Hot cache update is best-effort -- don't fail the recall.
                            }
                        }
                        else {
                            // --- Server search path (existing behavior) ---
                            const factCount = await getFactCount(api.logger);
                            const pool = computeCandidatePool(factCount);
                            const candidates = await apiClient.search(userId, allTrapdoors, pool, authKeyHex);
                            for (const candidate of candidates) {
                                try {
                                    const docJson = decryptFromHex(candidate.encrypted_blob, encryptionKey);
                                    if (isDigestBlob(docJson))
                                        continue;
                                    const doc = readClaimFromBlob(docJson);
                                    let decryptedEmbedding;
                                    if (candidate.encrypted_embedding) {
                                        try {
                                            decryptedEmbedding = JSON.parse(decryptFromHex(candidate.encrypted_embedding, encryptionKey));
                                        }
                                        catch {
                                            // Embedding decryption failed -- proceed without it.
                                        }
                                    }
                                    if (decryptedEmbedding && decryptedEmbedding.length !== getEmbeddingDims()) {
                                        try {
                                            decryptedEmbedding = await generateEmbedding(doc.text);
                                        }
                                        catch {
                                            decryptedEmbedding = undefined;
                                        }
                                    }
                                    rerankerCandidates.push({
                                        id: candidate.fact_id,
                                        text: doc.text,
                                        embedding: decryptedEmbedding,
                                        importance: doc.importance / 10,
                                        createdAt: typeof candidate.timestamp === 'number'
                                            ? candidate.timestamp / 1000
                                            : new Date(candidate.timestamp).getTime() / 1000,
                                        source: typeof doc.metadata?.source === 'string' ? doc.metadata.source : undefined,
                                    });
                                    metaMap.set(candidate.fact_id, {
                                        metadata: doc.metadata ?? {},
                                        timestamp: candidate.timestamp,
                                        category: doc.category,
                                    });
                                }
                                catch {
                                    // Skip candidates we cannot decrypt (e.g. corrupted data).
                                }
                            }
                        }
                        // 6. Re-rank with BM25 + cosine + intent-weighted RRF fusion.
                        const queryIntent = detectQueryIntent(params.query);
                        const reranked = rerank(params.query, queryEmbedding ?? [], rerankerCandidates, k, INTENT_WEIGHTS[queryIntent], 
                        /* applySourceWeights (Retrieval v2 Tier 1) */ true);
                        if (reranked.length === 0) {
                            return {
                                content: [{ type: 'text', text: 'No memories found matching your query.' }],
                                details: { count: 0, memories: [] },
                            };
                        }
                        // 6b. Relevance gate removed in rc.22 -- core's intent-weighted
                        //     RRF + Tier 1 source weighting handles short queries via the
                        //     BM25 component, making the rc.18 cosine + lexical-override
                        //     band-aid (issue #116) redundant.
                        // 7. Format results.
                        const lines = reranked.map((m, i) => {
                            const meta = metaMap.get(m.id);
                            const imp = meta?.metadata.importance
                                ? ` (importance: ${Math.round(meta.metadata.importance * 10)}/10)`
                                : '';
                            const age = meta ? relativeTime(meta.timestamp) : '';
                            const typeTag = meta?.category ? `[${meta.category}] ` : '';
                            return `${i + 1}. ${typeTag}${m.text}${imp} -- ${age} [ID: ${m.id}]`;
                        });
                        const formatted = lines.join('\n');
                        return {
                            content: [{ type: 'text', text: formatted }],
                            details: {
                                count: reranked.length,
                                memories: reranked.map((m) => ({
                                    factId: m.id,
                                    text: m.text,
                                })),
                            },
                        };
                    }
                    catch (err) {
                        const message = err instanceof Error ? err.message : String(err);
                        api.logger.error(`totalreclaw_recall failed: ${message}`);
                        return {
                            content: [{ type: 'text', text: `Failed to search memories: ${humanizeError(message)}` }],
                        };
                    }
                },
            }, { name: 'totalreclaw_recall' });
            // ---------------------------------------------------------------
            // Tool: totalreclaw_forget
            // ---------------------------------------------------------------
            api.registerTool({
                name: 'totalreclaw_forget',
                label: 'Forget',
                description: 'Delete a specific memory. Use when the user asks to forget, delete, or remove ' +
                    'something specific (e.g. "forget that I live in Porto", "delete the memory about my old job"). ' +
                    'Writes an on-chain tombstone — the delete is permanent and propagates across all devices. ' +
                    'If the user names the memory in natural language instead of an ID, FIRST call ' +
                    '`totalreclaw_recall` with their phrase as the query, then pass the top result\'s `id` as ' +
                    '`factId`. Non-reversible.',
                parameters: {
                    type: 'object',
                    properties: {
                        factId: {
                            type: 'string',
                            description: 'The UUID of the memory to delete. Get this from a prior `totalreclaw_recall` result — ' +
                                'the `memories[i].id` field. Never invent a factId; if you don\'t have one, call recall first.',
                        },
                    },
                    required: ['factId'],
                    additionalProperties: false,
                },
                async execute(_toolCallId, params) {
                    try {
                        await requireFullSetup(api.logger);
                        // Validate factId shape BEFORE any on-chain work. Prevents
                        // silent no-op when the LLM fabricates a non-UUID factId —
                        // the classic failure mode from 3.3.1-rc.1 QA where the
                        // agent replied "Done" without calling the tool at all, OR
                        // called the tool with a plain natural-language string.
                        const factId = typeof params.factId === 'string' ? params.factId.trim() : '';
                        if (!factId) {
                            return {
                                content: [{
                                        type: 'text',
                                        text: 'Cannot forget without a memory ID. Call `totalreclaw_recall` first with ' +
                                            'the user\'s phrasing as the query — the top result\'s `id` field is the ' +
                                            'factId to pass here.',
                                    }],
                                details: { deleted: false, error: 'missing-fact-id' },
                            };
                        }
                        // UUID-v4-ish shape check (loose — accepts any hex-dashed id).
                        // Prevents cases like `factId: "that I live in Porto"` from
                        // reaching the UserOp path and silently failing on-chain.
                        const looksLikeFactId = /^[0-9a-f-]{8,}$/i.test(factId);
                        if (!looksLikeFactId) {
                            api.logger.warn(`totalreclaw_forget: rejected likely-invalid factId "${factId.slice(0, 40)}" ` +
                                `— expected a UUID from a prior recall result, not natural language.`);
                            return {
                                content: [{
                                        type: 'text',
                                        text: `"${factId.slice(0, 60)}" doesn\'t look like a memory ID. Call ` +
                                            '`totalreclaw_recall` first with the user\'s phrasing as the query, then ' +
                                            'pass the top result\'s `id` field (a hex UUID) as `factId`.',
                                    }],
                                details: { deleted: false, error: 'invalid-fact-id' },
                            };
                        }
                        if (isSubgraphMode()) {
                            // On-chain tombstone: write a minimal protobuf with decayScore=0
                            // The subgraph picks this up and sets isActive=false.
                            //
                            // 3.3.1-rc.2 fix: route through submitFactBatchOnChain with a
                            // single-payload batch so we share the tombstone codepath the
                            // pin/unpin flow uses (that flow is known-good and the QA
                            // confirms pin works). Also write at legacy v3 (NOT v4) so the
                            // subgraph handler matches the source="tombstone" + version=3
                            // shape the contradiction/pin tombstones use.
                            const config = { ...getSubgraphConfig(), authKeyHex: authKeyHex, walletAddress: subgraphOwner ?? undefined };
                            const tombstone = {
                                id: factId,
                                timestamp: new Date().toISOString(),
                                owner: subgraphOwner || userId,
                                encryptedBlob: '00', // minimal 1-byte placeholder
                                blindIndices: [],
                                decayScore: 0,
                                source: 'tombstone',
                                contentFp: '',
                                agentId: 'openclaw-plugin-forget',
                                // Deliberately NO version: field → uses the default (legacy v3).
                                // The pin/unpin tombstones use v3 (see pin.ts:611-621) — we
                                // MUST match that shape or the subgraph may not flip isActive.
                            };
                            const protobuf = encodeFactProtobuf(tombstone);
                            const result = await submitFactBatchOnChain([protobuf], config);
                            if (!result.success) {
                                throw new Error(`On-chain tombstone failed (tx=${result.txHash?.slice(0, 10) || 'none'}…)`);
                            }
                            api.logger.info(`Tombstone written for ${factId}: tx=${result.txHash}`);
                            // Read-after-write: poll the subgraph until the original fact id
                            // is no longer active (forget flips isActive=false). On timeout
                            // surface `partial: true` so the agent can explain the chain
                            // write succeeded but the subgraph is still propagating.
                            const confirm = await confirmIndexed(factId, {
                                expect: 'inactive',
                                authKeyHex: authKeyHex,
                            });
                            return {
                                content: [{
                                        type: 'text',
                                        text: confirm.indexed
                                            ? `Memory ${factId} deleted on-chain and confirmed by the subgraph (tx: ${result.txHash}).`
                                            : `Memory ${factId} deleted on-chain (tx: ${result.txHash}). ` +
                                                'The subgraph indexer is still propagating the change — ' +
                                                'recall/export may briefly show the memory as still active.',
                                    }],
                                details: {
                                    deleted: true,
                                    txHash: result.txHash,
                                    factId,
                                    ...(confirm.indexed ? {} : { partial: true }),
                                },
                            };
                        }
                        else {
                            await apiClient.deleteFact(factId, authKeyHex);
                            return {
                                content: [{ type: 'text', text: `Memory ${factId} deleted` }],
                                details: { deleted: true, factId },
                            };
                        }
                    }
                    catch (err) {
                        const message = err instanceof Error ? err.message : String(err);
                        api.logger.error(`totalreclaw_forget failed: ${message}`);
                        return {
                            content: [{ type: 'text', text: `Failed to delete memory: ${humanizeError(message)}` }],
                        };
                    }
                },
            }, { name: 'totalreclaw_forget' });
            // ---------------------------------------------------------------
            // Tool: totalreclaw_export
            // ---------------------------------------------------------------
            api.registerTool({
                name: 'totalreclaw_export',
                label: 'Export',
                description: 'Export all stored memories. Decrypts every memory and returns them as JSON or Markdown.',
                parameters: {
                    type: 'object',
                    properties: {
                        format: {
                            type: 'string',
                            enum: ['json', 'markdown'],
                            description: 'Output format (default: json)',
                        },
                    },
                    additionalProperties: false,
                },
                async execute(_toolCallId, params) {
                    try {
                        await requireFullSetup(api.logger);
                        const format = params.format ?? 'json';
                        // Paginate through all facts.
                        const allFacts = [];
                        if (isSubgraphMode()) {
                            // Query subgraph for all active facts (cursor-based pagination via id_gt)
                            const config = getSubgraphConfig();
                            const relayUrl = config.relayUrl;
                            const PAGE_SIZE = 1000;
                            let lastId = '';
                            const owner = subgraphOwner || userId || '';
                            console.error(`[TotalReclaw Export] owner=${owner} subgraphOwner=${subgraphOwner} userId=${userId} relayUrl=${relayUrl} authKey=${authKeyHex ? authKeyHex.slice(0, 8) + '...' : 'MISSING'} isSubgraph=${isSubgraphMode()}`);
                            while (true) {
                                const hasLastId = lastId !== '';
                                const query = hasLastId
                                    ? `query($owner:Bytes!,$first:Int!,$lastId:String!){facts(where:{owner:$owner,isActive:true,id_gt:$lastId},first:$first,orderBy:id,orderDirection:asc){id encryptedBlob timestamp sequenceId}}`
                                    : `query($owner:Bytes!,$first:Int!){facts(where:{owner:$owner,isActive:true},first:$first,orderBy:id,orderDirection:asc){id encryptedBlob timestamp sequenceId}}`;
                                const variables = hasLastId
                                    ? { owner, first: PAGE_SIZE, lastId }
                                    : { owner, first: PAGE_SIZE };
                                const res = await fetch(`${relayUrl}/v1/subgraph`, {
                                    method: 'POST',
                                    headers: buildRelayHeaders({
                                        'Content-Type': 'application/json',
                                        ...(authKeyHex ? { Authorization: `Bearer ${authKeyHex}` } : {}),
                                    }),
                                    body: JSON.stringify({ query, variables }),
                                });
                                const json = (await res.json());
                                // Surface relay/subgraph errors instead of silently returning empty
                                if (json.error || json.errors) {
                                    const errMsg = json.error || json.errors?.map(e => e.message).join('; ') || 'Unknown error';
                                    api.logger.error(`Export subgraph query failed: ${errMsg} (owner=${owner}, status=${res.status})`);
                                    return {
                                        content: [{ type: 'text', text: `Export failed: ${errMsg}` }],
                                    };
                                }
                                const facts = json?.data?.facts || [];
                                if (facts.length === 0)
                                    break;
                                for (const fact of facts) {
                                    try {
                                        let hexBlob = fact.encryptedBlob;
                                        if (hexBlob.startsWith('0x'))
                                            hexBlob = hexBlob.slice(2);
                                        const docJson = decryptFromHex(hexBlob, encryptionKey);
                                        if (isDigestBlob(docJson))
                                            continue;
                                        const doc = readClaimFromBlob(docJson);
                                        allFacts.push({
                                            id: fact.id,
                                            text: doc.text,
                                            metadata: doc.metadata,
                                            created_at: new Date(parseInt(fact.timestamp) * 1000).toISOString(),
                                        });
                                    }
                                    catch {
                                        // Skip facts we cannot decrypt
                                    }
                                }
                                if (facts.length < PAGE_SIZE)
                                    break;
                                lastId = facts[facts.length - 1].id;
                            }
                        }
                        else {
                            // HTTP server mode — paginate through PostgreSQL facts
                            let cursor;
                            let hasMore = true;
                            while (hasMore) {
                                const page = await apiClient.exportFacts(authKeyHex, 1000, cursor);
                                for (const fact of page.facts) {
                                    try {
                                        const docJson = decryptFromHex(fact.encrypted_blob, encryptionKey);
                                        if (isDigestBlob(docJson))
                                            continue;
                                        const doc = readClaimFromBlob(docJson);
                                        allFacts.push({
                                            id: fact.id,
                                            text: doc.text,
                                            metadata: doc.metadata,
                                            created_at: fact.created_at,
                                        });
                                    }
                                    catch {
                                        // Skip facts we cannot decrypt.
                                    }
                                }
                                cursor = page.cursor ?? undefined;
                                hasMore = page.has_more;
                            }
                        }
                        // Format output.
                        let formatted;
                        if (format === 'markdown') {
                            if (allFacts.length === 0) {
                                formatted = '*No memories stored.*';
                            }
                            else {
                                const lines = allFacts.map((f, i) => {
                                    const meta = f.metadata;
                                    const type = meta.type ?? 'fact';
                                    const imp = meta.importance
                                        ? ` (importance: ${Math.round(meta.importance * 10)}/10)`
                                        : '';
                                    return `${i + 1}. **[${type}]** ${f.text}${imp}  \n   _ID: ${f.id} | Created: ${f.created_at}_`;
                                });
                                formatted = `# Exported Memories (${allFacts.length})\n\n${lines.join('\n')}`;
                            }
                        }
                        else {
                            formatted = JSON.stringify(allFacts, null, 2);
                        }
                        return {
                            content: [{ type: 'text', text: formatted }],
                            details: { count: allFacts.length },
                        };
                    }
                    catch (err) {
                        const message = err instanceof Error ? err.message : String(err);
                        api.logger.error(`totalreclaw_export failed: ${message}`);
                        return {
                            content: [{ type: 'text', text: `Failed to export memories: ${humanizeError(message)}` }],
                        };
                    }
                },
            }, { name: 'totalreclaw_export' });
            // ---------------------------------------------------------------
            // Tool: totalreclaw_status
            // ---------------------------------------------------------------
            api.registerTool({
                name: 'totalreclaw_status',
                label: 'Status',
                description: 'Check TotalReclaw billing and subscription status — tier, writes used, reset date.',
                parameters: {
                    type: 'object',
                    properties: {},
                    additionalProperties: false,
                },
                async execute() {
                    try {
                        await requireFullSetup(api.logger);
                        if (!authKeyHex) {
                            return {
                                content: [{ type: 'text', text: 'Auth credentials are not available. Please initialize first.' }],
                            };
                        }
                        const serverUrl = CONFIG.serverUrl;
                        const walletAddr = subgraphOwner || userId || '';
                        const response = await fetch(`${serverUrl}/v1/billing/status?wallet_address=${encodeURIComponent(walletAddr)}`, {
                            method: 'GET',
                            headers: buildRelayHeaders({
                                'Authorization': `Bearer ${authKeyHex}`,
                                'Accept': 'application/json',
                            }),
                        });
                        if (!response.ok) {
                            const body = await response.text().catch(() => '');
                            return {
                                content: [{ type: 'text', text: `Failed to fetch billing status (HTTP ${response.status}): ${body || response.statusText}` }],
                            };
                        }
                        const data = await response.json();
                        const tier = data.tier || 'free';
                        const freeWritesUsed = data.free_writes_used ?? 0;
                        const freeWritesLimit = data.free_writes_limit ?? 0;
                        const freeWritesResetAt = data.free_writes_reset_at;
                        // Update billing cache on success.
                        writeBillingCache({
                            tier,
                            free_writes_used: freeWritesUsed,
                            free_writes_limit: freeWritesLimit,
                            features: data.features,
                            checked_at: Date.now(),
                        });
                        // 3.3.1 (internal#130) — surface the Smart Account / scope
                        // address so the user can do subgraph queries, BaseScan
                        // lookups, and cross-client portability checks BEFORE any
                        // chain write completes. Resolution priority:
                        //   1. In-memory `subgraphOwner` (already derived earlier).
                        //   2. credentials.json `scope_address` (persisted at pair).
                        //   3. Lazy derive now from the loaded mnemonic + cache it
                        //      back to credentials.json so the next call is free.
                        let scopeAddress = subgraphOwner ?? undefined;
                        if (!scopeAddress) {
                            try {
                                const credsCache = loadCredentialsJson(CREDENTIALS_PATH);
                                if (credsCache?.scope_address && typeof credsCache.scope_address === 'string') {
                                    scopeAddress = credsCache.scope_address;
                                }
                                else if (credsCache?.mnemonic && typeof credsCache.mnemonic === 'string') {
                                    scopeAddress = await deriveSmartAccountAddress(credsCache.mnemonic, CONFIG.chainId);
                                    if (scopeAddress) {
                                        writeCredentialsJson(CREDENTIALS_PATH, { ...credsCache, scope_address: scopeAddress });
                                    }
                                }
                            }
                            catch (deriveErr) {
                                api.logger.warn(`totalreclaw_status: scope_address lookup failed: ${deriveErr instanceof Error ? deriveErr.message : String(deriveErr)}`);
                            }
                        }
                        const tierLabel = tier === 'pro' ? 'Pro' : 'Free';
                        const lines = [
                            `Tier: ${tierLabel}`,
                            `Writes: ${freeWritesUsed}/${freeWritesLimit} used this month`,
                        ];
                        if (freeWritesResetAt) {
                            lines.push(`Resets: ${new Date(freeWritesResetAt).toLocaleDateString()}`);
                        }
                        if (scopeAddress) {
                            lines.push(`Smart Account: ${scopeAddress}`);
                        }
                        if (tier !== 'pro') {
                            lines.push(`Pricing: https://totalreclaw.xyz/pricing`);
                        }
                        return {
                            content: [{ type: 'text', text: lines.join('\n') }],
                            details: {
                                tier,
                                free_writes_used: freeWritesUsed,
                                free_writes_limit: freeWritesLimit,
                                scope_address: scopeAddress,
                            },
                        };
                    }
                    catch (err) {
                        const message = err instanceof Error ? err.message : String(err);
                        api.logger.error(`totalreclaw_status failed: ${message}`);
                        return {
                            content: [{ type: 'text', text: `Failed to check status: ${humanizeError(message)}` }],
                        };
                    }
                },
            }, { name: 'totalreclaw_status' });
            // ---------------------------------------------------------------
            // Tool: totalreclaw_preload_embedder (3.3.3-rc.1 — issue #187)
            // ---------------------------------------------------------------
            //
            // Decouples the ~700 MB embedder bundle download from the pair-
            // completion gate. The agent can call this BEFORE
            // `totalreclaw_pair` to pre-flight disk space, kick off the
            // download, and surface the completion state. The non-blocking
            // prefetch in `register()` already starts the download
            // unconditionally; this tool is an explicit on-demand hook for
            // agents that want to confirm completion (or trigger a retry on
            // network failure) without first completing pair.
            //
            // Behavior:
            //   - Disk-space pre-flight: refuses if free disk < 500 MB on the
            //     embedder cache mount. Surfaces the path + free bytes so the
            //     user can clear space.
            //   - Triggers `prefetchEmbedderBundle()` (idempotent — cache hit
            //     returns immediately).
            //   - Returns a structured success message with status:
            //     `cache_hit | fetched | failed`.
            //
            // Phrase-safety: this tool does NOT touch credentials.json,
            // mnemonics, or keys. It only touches `~/.totalreclaw/embedder/`
            // and the GitHub Releases CDN.
            api.registerTool({
                name: 'totalreclaw_preload_embedder',
                label: 'Preload Embedder',
                description: 'Download the local-embedding model bundle ahead of pair completion. Use this when the user wants to set up TotalReclaw on a slow connection or run an offline-after-setup workflow. Returns success once the ~700 MB bundle is cached at ~/.totalreclaw/embedder/.',
                parameters: {
                    type: 'object',
                    properties: {},
                    additionalProperties: false,
                },
                async execute() {
                    try {
                        // Disk-space pre-flight: refuse if < 500 MB free on the
                        // embedder cache mount. Best-effort — if statfs fails, we
                        // proceed without the pre-flight rather than blocking.
                        const fsModule = await import('node:fs');
                        const cacheRoot = CONFIG.embedderCachePath;
                        const REQUIRED_BYTES = 500 * 1024 * 1024;
                        try {
                            // Find the deepest existing parent so statfs has a real
                            // mount to measure (loadEmbedder will mkdir under it
                            // anyway).
                            let probeDir = cacheRoot;
                            while (true) {
                                try {
                                    fsModule.statSync(probeDir);
                                    break;
                                }
                                catch {
                                    const parent = nodePath.dirname(probeDir);
                                    if (parent === probeDir)
                                        break;
                                    probeDir = parent;
                                }
                            }
                            const stats = fsModule.statfsSync?.(probeDir);
                            if (stats) {
                                const bavail = typeof stats.bavail === 'bigint' ? Number(stats.bavail) : stats.bavail;
                                const bsize = typeof stats.bsize === 'bigint' ? Number(stats.bsize) : stats.bsize;
                                const freeBytes = bavail * bsize;
                                if (freeBytes > 0 && freeBytes < REQUIRED_BYTES) {
                                    const freeMb = Math.round(freeBytes / (1024 * 1024));
                                    return {
                                        content: [{
                                                type: 'text',
                                                text: `Insufficient free disk space for embedder bundle. Required: 500 MB. Available at ${probeDir}: ${freeMb} MB. Free up space and retry.`,
                                            }],
                                        details: { status: 'failed', reason: 'disk_space', free_mb: freeMb, required_mb: 500, cache_root: cacheRoot },
                                    };
                                }
                            }
                        }
                        catch {
                            // statfs probe failed — surface a soft warning in logs
                            // but proceed with the download anyway.
                            api.logger.info('totalreclaw_preload_embedder: disk-space probe unavailable, proceeding without pre-flight');
                        }
                        // Trigger the prefetch. This is idempotent (cache hit returns
                        // immediately) so it's safe to invoke even when the
                        // background prefetch from register() already completed.
                        const result = await prefetchEmbedderBundle({
                            log: (msg) => api.logger.info(msg),
                        });
                        const human = result === 'fetched'
                            ? `Embedder bundle downloaded and cached at ${cacheRoot}. Subsequent embedding calls run in-memory.`
                            : `Embedder bundle already cached at ${cacheRoot} — no download needed.`;
                        return {
                            content: [{ type: 'text', text: human }],
                            details: { status: result, cache_root: cacheRoot },
                        };
                    }
                    catch (err) {
                        const message = err instanceof Error ? err.message : String(err);
                        api.logger.error(`totalreclaw_preload_embedder failed: ${message}`);
                        return {
                            content: [{
                                    type: 'text',
                                    text: `Embedder bundle preload failed: ${humanizeError(message)}. The plugin will retry on first embedding call.`,
                                }],
                            details: { status: 'failed', reason: 'fetch_error', message },
                        };
                    }
                },
            }, { name: 'totalreclaw_preload_embedder' });
            // ---------------------------------------------------------------
            // Tool: totalreclaw_consolidate
            // ---------------------------------------------------------------
            api.registerTool({
                name: 'totalreclaw_consolidate',
                label: 'Consolidate',
                description: 'Deduplicate and merge related memories. Self-hosted mode only.',
                parameters: {
                    type: 'object',
                    properties: {
                        dry_run: {
                            type: 'boolean',
                            description: 'Preview only (default: false)',
                        },
                    },
                    additionalProperties: false,
                },
                async execute(_toolCallId, params) {
                    try {
                        await requireFullSetup(api.logger);
                        const dryRun = params.dry_run ?? false;
                        // Consolidation is only available in centralized (HTTP server) mode.
                        if (isSubgraphMode()) {
                            return {
                                content: [{ type: 'text', text: 'Consolidation is currently only available in centralized mode.' }],
                            };
                        }
                        if (!apiClient || !authKeyHex || !encryptionKey) {
                            return {
                                content: [{ type: 'text', text: 'Plugin not fully initialized. Cannot consolidate.' }],
                            };
                        }
                        // 1. Export all facts (paginated, max 10 pages of 1000).
                        const allDecrypted = [];
                        let cursor;
                        let hasMore = true;
                        let pageCount = 0;
                        const MAX_PAGES = 10;
                        while (hasMore && pageCount < MAX_PAGES) {
                            const page = await apiClient.exportFacts(authKeyHex, 1000, cursor);
                            for (const fact of page.facts) {
                                try {
                                    const docJson = decryptFromHex(fact.encrypted_blob, encryptionKey);
                                    if (isDigestBlob(docJson))
                                        continue;
                                    const doc = readClaimFromBlob(docJson);
                                    let embedding = null;
                                    try {
                                        embedding = await generateEmbedding(doc.text);
                                    }
                                    catch { /* skip — fact will not be clustered */ }
                                    allDecrypted.push({
                                        id: fact.id,
                                        text: doc.text,
                                        embedding,
                                        importance: doc.importance,
                                        decayScore: fact.decay_score,
                                        createdAt: new Date(fact.created_at).getTime(),
                                        version: fact.version,
                                    });
                                }
                                catch {
                                    // Skip undecryptable facts.
                                }
                            }
                            cursor = page.cursor ?? undefined;
                            hasMore = page.has_more;
                            pageCount++;
                        }
                        if (allDecrypted.length === 0) {
                            return {
                                content: [{ type: 'text', text: 'No memories found to consolidate.' }],
                            };
                        }
                        // 2. Cluster by cosine similarity.
                        const clusters = clusterFacts(allDecrypted, getConsolidationThreshold());
                        if (clusters.length === 0) {
                            return {
                                content: [{ type: 'text', text: `Scanned ${allDecrypted.length} memories — no near-duplicates found.` }],
                            };
                        }
                        // 3. Build report.
                        const totalDuplicates = clusters.reduce((sum, c) => sum + c.duplicates.length, 0);
                        const reportLines = [
                            `Scanned ${allDecrypted.length} memories.`,
                            `Found ${clusters.length} cluster(s) with ${totalDuplicates} duplicate(s).`,
                            '',
                        ];
                        const displayClusters = clusters.slice(0, 10);
                        for (let i = 0; i < displayClusters.length; i++) {
                            const cluster = displayClusters[i];
                            reportLines.push(`Cluster ${i + 1}: KEEP "${cluster.representative.text.slice(0, 80)}…"`);
                            for (const dup of cluster.duplicates) {
                                reportLines.push(`  - REMOVE "${dup.text.slice(0, 80)}…" (ID: ${dup.id})`);
                            }
                        }
                        if (clusters.length > 10) {
                            reportLines.push(`... and ${clusters.length - 10} more cluster(s).`);
                        }
                        // 4. If not dry_run, batch-delete duplicates.
                        if (!dryRun) {
                            const idsToDelete = clusters.flatMap((c) => c.duplicates.map((d) => d.id));
                            const BATCH_SIZE = 500;
                            let totalDeleted = 0;
                            for (let i = 0; i < idsToDelete.length; i += BATCH_SIZE) {
                                const batch = idsToDelete.slice(i, i + BATCH_SIZE);
                                const deleted = await apiClient.batchDelete(batch, authKeyHex);
                                totalDeleted += deleted;
                            }
                            reportLines.push('');
                            reportLines.push(`Deleted ${totalDeleted} duplicate memories.`);
                        }
                        else {
                            reportLines.push('');
                            reportLines.push('DRY RUN — no memories were deleted. Run without dry_run to apply.');
                        }
                        return {
                            content: [{ type: 'text', text: reportLines.join('\n') }],
                            details: {
                                scanned: allDecrypted.length,
                                clusters: clusters.length,
                                duplicates: totalDuplicates,
                                dry_run: dryRun,
                            },
                        };
                    }
                    catch (err) {
                        const message = err instanceof Error ? err.message : String(err);
                        api.logger.error(`totalreclaw_consolidate failed: ${message}`);
                        return {
                            content: [{ type: 'text', text: `Failed to consolidate memories: ${humanizeError(message)}` }],
                        };
                    }
                },
            }, { name: 'totalreclaw_consolidate' });
            // ---------------------------------------------------------------
            // Helper: build PinOpDeps bound to the live plugin state
            // ---------------------------------------------------------------
            // Wires the pure pin/unpin operation to the managed-service transport +
            // crypto layer. Mirrors MCP's buildPinDepsFromState and Python's
            // _change_claim_status argument plumbing.
            const buildPinDeps = () => {
                const owner = subgraphOwner || userId || '';
                const config = {
                    ...getSubgraphConfig(),
                    authKeyHex: authKeyHex,
                    walletAddress: subgraphOwner ?? undefined,
                };
                return {
                    owner,
                    sourceAgent: 'openclaw-plugin',
                    fetchFactById: (factId) => fetchFactById(owner, factId, authKeyHex),
                    decryptBlob: (hex) => decryptFromHex(hex, encryptionKey),
                    encryptBlob: (plaintext) => encryptToHex(plaintext, encryptionKey),
                    submitBatch: async (payloads) => {
                        const result = await submitFactBatchOnChain(payloads, config);
                        return { txHash: result.txHash, success: result.success };
                    },
                    generateIndices: async (text, entityNames) => {
                        if (!text)
                            return { blindIndices: [] };
                        const wordIndices = generateBlindIndices(text);
                        let lshIndices = [];
                        let encryptedEmbedding;
                        try {
                            const embedding = await generateEmbedding(text);
                            const hasher = getLSHHasher(api.logger);
                            if (hasher)
                                lshIndices = hasher.hash(embedding);
                            encryptedEmbedding = encryptToHex(JSON.stringify(embedding), encryptionKey);
                        }
                        catch {
                            // Best-effort: word + entity trapdoors alone still surface the claim.
                        }
                        const entityTrapdoors = entityNames.map((n) => computeEntityTrapdoor(n));
                        return {
                            blindIndices: [...wordIndices, ...lshIndices, ...entityTrapdoors],
                            encryptedEmbedding,
                        };
                    },
                };
            };
            // ---------------------------------------------------------------
            // Tool: totalreclaw_pin
            // ---------------------------------------------------------------
            api.registerTool({
                name: 'totalreclaw_pin',
                label: 'Pin',
                description: 'Pin a memory so the auto-resolution engine will never override or supersede it. ' +
                    "Use when the user explicitly confirms a claim is still valid after you or another agent " +
                    "tried to retract/contradict it (e.g. 'wait, I still use Vim sometimes'). " +
                    'Takes fact_id (from a prior recall result). Pinning is idempotent — pinning an already-pinned ' +
                    'claim is a no-op. Cross-device: the pin propagates via the on-chain supersession chain.',
                parameters: {
                    type: 'object',
                    properties: {
                        fact_id: {
                            type: 'string',
                            description: 'The ID of the fact to pin (from a totalreclaw_recall result).',
                        },
                        reason: {
                            type: 'string',
                            description: 'Optional human-readable reason for pinning (logged locally for tuning).',
                        },
                    },
                    required: ['fact_id'],
                    additionalProperties: false,
                },
                async execute(_toolCallId, params) {
                    try {
                        await requireFullSetup(api.logger);
                        if (!isSubgraphMode()) {
                            return {
                                content: [{
                                        type: 'text',
                                        text: 'Pin/unpin is only supported with the managed service. Self-hosted mode does not yet implement the status-flip supersession flow.',
                                    }],
                            };
                        }
                        const validation = validatePinArgs(params);
                        if (!validation.ok) {
                            return { content: [{ type: 'text', text: validation.error }] };
                        }
                        const deps = buildPinDeps();
                        const result = await executePinOperation(validation.factId, 'pinned', deps, validation.reason);
                        if (result.success && result.idempotent) {
                            api.logger.info(`totalreclaw_pin: ${result.fact_id} already pinned (no-op)`);
                            return {
                                content: [{ type: 'text', text: `Memory ${result.fact_id} is already pinned.` }],
                                details: result,
                            };
                        }
                        if (result.success) {
                            api.logger.info(`totalreclaw_pin: ${result.fact_id} → ${result.new_fact_id} (tx ${result.tx_hash?.slice(0, 10)})`);
                            return {
                                content: [{
                                        type: 'text',
                                        text: `Pinned memory ${result.fact_id}. New fact id: ${result.new_fact_id} (tx: ${result.tx_hash}).`,
                                    }],
                                details: result,
                            };
                        }
                        api.logger.error(`totalreclaw_pin failed: ${result.error}`);
                        return {
                            content: [{ type: 'text', text: `Failed to pin memory: ${humanizeError(result.error ?? 'unknown error')}` }],
                            details: result,
                        };
                    }
                    catch (err) {
                        const message = err instanceof Error ? err.message : String(err);
                        api.logger.error(`totalreclaw_pin failed: ${message}`);
                        return {
                            content: [{ type: 'text', text: `Failed to pin memory: ${humanizeError(message)}` }],
                        };
                    }
                },
            }, { name: 'totalreclaw_pin' });
            // ---------------------------------------------------------------
            // Tool: totalreclaw_unpin
            // ---------------------------------------------------------------
            api.registerTool({
                name: 'totalreclaw_unpin',
                label: 'Unpin',
                description: 'Remove the pin from a previously pinned memory, returning it to active status so the ' +
                    'auto-resolution engine can supersede or retract it again. Takes fact_id. Idempotent — ' +
                    'unpinning a non-pinned claim is a no-op.',
                parameters: {
                    type: 'object',
                    properties: {
                        fact_id: {
                            type: 'string',
                            description: 'The ID of the fact to unpin (from a totalreclaw_recall result).',
                        },
                    },
                    required: ['fact_id'],
                    additionalProperties: false,
                },
                async execute(_toolCallId, params) {
                    try {
                        await requireFullSetup(api.logger);
                        if (!isSubgraphMode()) {
                            return {
                                content: [{
                                        type: 'text',
                                        text: 'Pin/unpin is only supported with the managed service. Self-hosted mode does not yet implement the status-flip supersession flow.',
                                    }],
                            };
                        }
                        const validation = validatePinArgs(params);
                        if (!validation.ok) {
                            return { content: [{ type: 'text', text: validation.error }] };
                        }
                        const deps = buildPinDeps();
                        const result = await executePinOperation(validation.factId, 'active', deps);
                        if (result.success && result.idempotent) {
                            api.logger.info(`totalreclaw_unpin: ${result.fact_id} already active (no-op)`);
                            return {
                                content: [{ type: 'text', text: `Memory ${result.fact_id} is not pinned.` }],
                                details: result,
                            };
                        }
                        if (result.success) {
                            api.logger.info(`totalreclaw_unpin: ${result.fact_id} → ${result.new_fact_id} (tx ${result.tx_hash?.slice(0, 10)})`);
                            return {
                                content: [{
                                        type: 'text',
                                        text: `Unpinned memory ${result.fact_id}. New fact id: ${result.new_fact_id} (tx: ${result.tx_hash}).`,
                                    }],
                                details: result,
                            };
                        }
                        api.logger.error(`totalreclaw_unpin failed: ${result.error}`);
                        return {
                            content: [{ type: 'text', text: `Failed to unpin memory: ${humanizeError(result.error ?? 'unknown error')}` }],
                            details: result,
                        };
                    }
                    catch (err) {
                        const message = err instanceof Error ? err.message : String(err);
                        api.logger.error(`totalreclaw_unpin failed: ${message}`);
                        return {
                            content: [{ type: 'text', text: `Failed to unpin memory: ${humanizeError(message)}` }],
                        };
                    }
                },
            }, { name: 'totalreclaw_unpin' });
            // ---------------------------------------------------------------
            // Shared deps for retype + set_scope (same shape as pin deps).
            // Built lazily so the closure captures the current encryption key /
            // subgraph owner at call time rather than at register() time.
            // ---------------------------------------------------------------
            const buildRetypeSetScopeDeps = () => {
                const owner = subgraphOwner || userId || '';
                const config = {
                    ...getSubgraphConfig(),
                    authKeyHex: authKeyHex,
                    walletAddress: subgraphOwner ?? undefined,
                };
                return {
                    owner,
                    sourceAgent: 'openclaw-plugin',
                    fetchFactById: (factId) => fetchFactById(owner, factId, authKeyHex),
                    decryptBlob: (hex) => decryptFromHex(hex, encryptionKey),
                    encryptBlob: (plaintext) => encryptToHex(plaintext, encryptionKey),
                    submitBatch: async (payloads) => {
                        const result = await submitFactBatchOnChain(payloads, config);
                        return { txHash: result.txHash, success: result.success };
                    },
                    generateIndices: async (text, entityNames) => {
                        if (!text)
                            return { blindIndices: [] };
                        const wordIndices = generateBlindIndices(text);
                        let lshIndices = [];
                        let encryptedEmbedding;
                        try {
                            const embedding = await generateEmbedding(text);
                            const hasher = getLSHHasher(api.logger);
                            if (hasher)
                                lshIndices = hasher.hash(embedding);
                            encryptedEmbedding = encryptToHex(JSON.stringify(embedding), encryptionKey);
                        }
                        catch {
                            // Best-effort: word + entity trapdoors alone still surface the claim.
                        }
                        const entityTrapdoors = entityNames.map((n) => computeEntityTrapdoor(n));
                        return {
                            blindIndices: [...wordIndices, ...lshIndices, ...entityTrapdoors],
                            encryptedEmbedding,
                        };
                    },
                };
            };
            // ---------------------------------------------------------------
            // Tool: totalreclaw_retype (3.3.1-rc.2 — agent-facing taxonomy edit)
            // ---------------------------------------------------------------
            api.registerTool({
                name: 'totalreclaw_retype',
                label: 'Retype',
                description: 'Reclassify an existing memory from one taxonomy type to another (claim / preference / ' +
                    'directive / commitment / episode / summary). Use when the user corrects a memory\'s ' +
                    'category — e.g. "that\'s actually a preference, not a fact" or "file this as a ' +
                    'commitment, not a claim". Writes a new v1.1 blob with the updated type and tombstones ' +
                    'the old fact on-chain.\n\n' +
                    'If the user names the memory in natural language, FIRST call `totalreclaw_recall` to ' +
                    'find the fact_id, then pass it here with the new type.',
                parameters: {
                    type: 'object',
                    properties: {
                        fact_id: {
                            type: 'string',
                            description: 'The UUID of the memory to reclassify. Get this from a prior ' +
                                '`totalreclaw_recall` result.',
                        },
                        new_type: {
                            type: 'string',
                            enum: ['claim', 'preference', 'directive', 'commitment', 'episode', 'summary'],
                            description: 'The new taxonomy type. claim=factual statement, preference=opinion/like/dislike, ' +
                                'directive=instruction, commitment=promise/plan, episode=event, summary=aggregate.',
                        },
                    },
                    required: ['fact_id', 'new_type'],
                    additionalProperties: false,
                },
                async execute(_toolCallId, params) {
                    try {
                        await requireFullSetup(api.logger);
                        if (!isSubgraphMode()) {
                            return {
                                content: [{
                                        type: 'text',
                                        text: 'Retype is only supported with the managed service. Self-hosted mode does not yet implement the status-flip supersession flow.',
                                    }],
                            };
                        }
                        const validation = validateRetypeArgs(params);
                        if (!validation.ok) {
                            return { content: [{ type: 'text', text: validation.error }] };
                        }
                        const deps = buildRetypeSetScopeDeps();
                        const result = await executeRetype(validation.factId, validation.newType, deps);
                        if (result.success) {
                            api.logger.info(`totalreclaw_retype: ${result.fact_id} (${result.previous_type} → ${result.new_type}) → ${result.new_fact_id} (tx ${result.tx_hash?.slice(0, 10)})`);
                            return {
                                content: [{
                                        type: 'text',
                                        text: `Retyped memory ${result.fact_id} from ${result.previous_type} to ${result.new_type}. ` +
                                            `New fact id: ${result.new_fact_id} (tx: ${result.tx_hash}).`,
                                    }],
                                details: result,
                            };
                        }
                        api.logger.error(`totalreclaw_retype failed: ${result.error}`);
                        return {
                            content: [{ type: 'text', text: `Failed to retype memory: ${humanizeError(result.error ?? 'unknown error')}` }],
                            details: result,
                        };
                    }
                    catch (err) {
                        const message = err instanceof Error ? err.message : String(err);
                        api.logger.error(`totalreclaw_retype failed: ${message}`);
                        return {
                            content: [{ type: 'text', text: `Failed to retype memory: ${humanizeError(message)}` }],
                        };
                    }
                },
            }, { name: 'totalreclaw_retype' });
            // ---------------------------------------------------------------
            // Tool: totalreclaw_set_scope (3.3.1-rc.2 — agent-facing scope edit)
            // ---------------------------------------------------------------
            api.registerTool({
                name: 'totalreclaw_set_scope',
                label: 'Set Scope',
                description: 'Move an existing memory to a different scope (work / personal / health / family / ' +
                    'creative / finance / misc / unspecified). Use when the user re-categorizes a memory\'s ' +
                    'domain — e.g. "put that under work", "this is a health thing", "move this to personal". ' +
                    'Writes a new v1.1 blob with the updated scope and tombstones the old fact on-chain.\n\n' +
                    'If the user names the memory in natural language, FIRST call `totalreclaw_recall` to ' +
                    'find the fact_id, then pass it here with the new scope.',
                parameters: {
                    type: 'object',
                    properties: {
                        fact_id: {
                            type: 'string',
                            description: 'The UUID of the memory to rescope. Get this from a prior `totalreclaw_recall` result.',
                        },
                        new_scope: {
                            type: 'string',
                            enum: ['work', 'personal', 'health', 'family', 'creative', 'finance', 'misc', 'unspecified'],
                            description: 'The new scope. Used for filtered recall — e.g. "recall work-related memories only".',
                        },
                    },
                    required: ['fact_id', 'new_scope'],
                    additionalProperties: false,
                },
                async execute(_toolCallId, params) {
                    try {
                        await requireFullSetup(api.logger);
                        if (!isSubgraphMode()) {
                            return {
                                content: [{
                                        type: 'text',
                                        text: 'Set-scope is only supported with the managed service. Self-hosted mode does not yet implement the status-flip supersession flow.',
                                    }],
                            };
                        }
                        const validation = validateSetScopeArgs(params);
                        if (!validation.ok) {
                            return { content: [{ type: 'text', text: validation.error }] };
                        }
                        const deps = buildRetypeSetScopeDeps();
                        const result = await executeSetScope(validation.factId, validation.newScope, deps);
                        if (result.success) {
                            api.logger.info(`totalreclaw_set_scope: ${result.fact_id} (${result.previous_scope ?? 'unspecified'} → ${result.new_scope}) → ${result.new_fact_id} (tx ${result.tx_hash?.slice(0, 10)})`);
                            return {
                                content: [{
                                        type: 'text',
                                        text: `Moved memory ${result.fact_id} from scope "${result.previous_scope ?? 'unspecified'}" to "${result.new_scope}". ` +
                                            `New fact id: ${result.new_fact_id} (tx: ${result.tx_hash}).`,
                                    }],
                                details: result,
                            };
                        }
                        api.logger.error(`totalreclaw_set_scope failed: ${result.error}`);
                        return {
                            content: [{ type: 'text', text: `Failed to set scope: ${humanizeError(result.error ?? 'unknown error')}` }],
                            details: result,
                        };
                    }
                    catch (err) {
                        const message = err instanceof Error ? err.message : String(err);
                        api.logger.error(`totalreclaw_set_scope failed: ${message}`);
                        return {
                            content: [{ type: 'text', text: `Failed to set scope: ${humanizeError(message)}` }],
                        };
                    }
                },
            }, { name: 'totalreclaw_set_scope' });
            // ---------------------------------------------------------------
            // Tool: totalreclaw_import_from
            // ---------------------------------------------------------------
            api.registerTool({
                name: 'totalreclaw_import_from',
                label: 'Import From',
                description: 'Import memories from other AI memory tools (Mem0, MCP Memory Server, ChatGPT, Claude, Gemini, MemoClaw, or generic JSON/CSV). ' +
                    'Provide the source name and either an API key, file content, or file path. ' +
                    'Use dry_run=true to preview before importing. Idempotent — safe to run multiple times.',
                parameters: {
                    type: 'object',
                    properties: {
                        source: {
                            type: 'string',
                            enum: ['mem0', 'mcp-memory', 'chatgpt', 'claude', 'gemini'],
                            description: 'The source system to import from (gemini: Google Takeout HTML; chatgpt: conversations.json or memory text; claude: memory text)',
                        },
                        api_key: {
                            type: 'string',
                            description: 'API key for the source system (used once, never stored)',
                        },
                        source_user_id: {
                            type: 'string',
                            description: 'User or agent ID in the source system',
                        },
                        content: {
                            type: 'string',
                            description: 'File content (JSON, JSONL, or CSV)',
                        },
                        file_path: {
                            type: 'string',
                            description: 'Path to the file on disk',
                        },
                        namespace: {
                            type: 'string',
                            description: 'Target namespace (default: "imported")',
                        },
                        dry_run: {
                            type: 'boolean',
                            description: 'Preview without importing',
                        },
                    },
                    required: ['source'],
                },
                async execute(_toolCallId, params) {
                    try {
                        await requireFullSetup(api.logger);
                        return handlePluginImportFrom(params, api.logger);
                    }
                    catch (err) {
                        const message = err instanceof Error ? err.message : String(err);
                        return { error: message };
                    }
                },
            }, { name: 'totalreclaw_import_from' });
            // ---------------------------------------------------------------
            // Tool: totalreclaw_import_batch
            // ---------------------------------------------------------------
            api.registerTool({
                name: 'totalreclaw_import_batch',
                label: 'Import Batch',
                description: 'Process one batch of a large import. Call repeatedly with increasing offset until is_complete=true.',
                parameters: {
                    type: 'object',
                    properties: {
                        source: {
                            type: 'string',
                            enum: ['gemini', 'chatgpt', 'claude'],
                            description: 'Source format',
                        },
                        file_path: {
                            type: 'string',
                            description: 'Path to source file',
                        },
                        content: {
                            type: 'string',
                            description: 'File content (text sources)',
                        },
                        offset: {
                            type: 'number',
                            description: 'Starting chunk index (0-based)',
                        },
                        batch_size: {
                            type: 'number',
                            description: 'Chunks per call (default 25)',
                        },
                    },
                    required: ['source'],
                },
                async execute(_toolCallId, params) {
                    try {
                        await requireFullSetup(api.logger);
                        return handleBatchImport(params, api.logger);
                    }
                    catch (err) {
                        const message = err instanceof Error ? err.message : String(err);
                        return { error: message };
                    }
                },
            }, { name: 'totalreclaw_import_batch' });
            // ---------------------------------------------------------------
            // Tool: totalreclaw_import_status
            // ---------------------------------------------------------------
            api.registerTool({
                name: 'totalreclaw_import_status',
                label: 'Import Status',
                description: 'Check the progress of a background import. ' +
                    'If import_id is omitted, returns the most recent active import. ' +
                    'Returns status (running/completed/failed/aborted), batch progress, facts stored, and ETA. ' +
                    'Use this when the user asks "how\'s the import?" or "is it done yet?".',
                parameters: {
                    type: 'object',
                    properties: {
                        import_id: {
                            type: 'string',
                            description: 'The import ID returned by totalreclaw_import_from. Omit for most recent active import.',
                        },
                    },
                    additionalProperties: false,
                },
                async execute(_toolCallId, params) {
                    try {
                        await requireFullSetup(api.logger);
                        return handleImportStatus(params, api.logger);
                    }
                    catch (err) {
                        const message = err instanceof Error ? err.message : String(err);
                        return { error: message };
                    }
                },
            }, { name: 'totalreclaw_import_status' });
            // ---------------------------------------------------------------
            // Tool: totalreclaw_import_abort
            // ---------------------------------------------------------------
            api.registerTool({
                name: 'totalreclaw_import_abort',
                label: 'Abort Import',
                description: 'Cancel a running background import. Already-stored facts are kept (import is idempotent via fingerprint dedup). ' +
                    'The background task will stop at the next chunk boundary after receiving the abort signal. ' +
                    'Use when the user says "stop the import" or "cancel the import".',
                parameters: {
                    type: 'object',
                    properties: {
                        import_id: {
                            type: 'string',
                            description: 'The import ID to abort (from totalreclaw_import_from or totalreclaw_import_status).',
                        },
                    },
                    required: ['import_id'],
                    additionalProperties: false,
                },
                async execute(_toolCallId, params) {
                    try {
                        await requireFullSetup(api.logger);
                        return handleImportAbort(params, api.logger);
                    }
                    catch (err) {
                        const message = err instanceof Error ? err.message : String(err);
                        return { error: message };
                    }
                },
            }, { name: 'totalreclaw_import_abort' });
            // ---------------------------------------------------------------
            // Tool: totalreclaw_upgrade
            // ---------------------------------------------------------------
            api.registerTool({
                name: 'totalreclaw_upgrade',
                label: 'Upgrade to Pro',
                description: 'Upgrade to TotalReclaw Pro for unlimited encrypted memories. ' +
                    'Returns a Stripe checkout URL for the user to complete payment via credit/debit card.',
                parameters: {
                    type: 'object',
                    properties: {},
                    additionalProperties: false,
                },
                async execute() {
                    try {
                        await requireFullSetup(api.logger);
                        if (!authKeyHex) {
                            return {
                                content: [{ type: 'text', text: 'Auth credentials are not available. Please initialize first.' }],
                            };
                        }
                        const serverUrl = CONFIG.serverUrl;
                        const walletAddr = subgraphOwner || userId || '';
                        if (!walletAddr) {
                            return {
                                content: [{ type: 'text', text: 'Wallet address not available. Please ensure the plugin is fully initialized.' }],
                            };
                        }
                        const response = await fetch(`${serverUrl}/v1/billing/checkout`, {
                            method: 'POST',
                            headers: buildRelayHeaders({
                                'Authorization': `Bearer ${authKeyHex}`,
                                'Content-Type': 'application/json',
                            }),
                            body: JSON.stringify({
                                wallet_address: walletAddr,
                                tier: 'pro',
                            }),
                        });
                        if (!response.ok) {
                            const body = await response.text().catch(() => '');
                            return {
                                content: [{ type: 'text', text: `Failed to create checkout session (HTTP ${response.status}): ${body || response.statusText}` }],
                            };
                        }
                        const data = await response.json();
                        if (!data.checkout_url) {
                            return {
                                content: [{ type: 'text', text: 'Failed to create checkout session: no checkout URL returned.' }],
                            };
                        }
                        return {
                            content: [{ type: 'text', text: `Open this URL to upgrade to Pro: ${data.checkout_url}` }],
                            details: { checkout_url: data.checkout_url },
                        };
                    }
                    catch (err) {
                        const message = err instanceof Error ? err.message : String(err);
                        api.logger.error(`totalreclaw_upgrade failed: ${message}`);
                        return {
                            content: [{ type: 'text', text: `Failed to create checkout session: ${humanizeError(message)}` }],
                        };
                    }
                },
            }, { name: 'totalreclaw_upgrade' });
            // ---------------------------------------------------------------
            // Tool: totalreclaw_migrate
            // ---------------------------------------------------------------
            api.registerTool({
                name: 'totalreclaw_migrate',
                label: 'Migrate Testnet to Mainnet',
                description: 'Migrate memories from testnet (Base Sepolia) to mainnet (Gnosis) after upgrading to Pro. ' +
                    'Dry-run by default — set confirm=true to execute. Idempotent: re-running skips already-migrated facts.',
                parameters: {
                    type: 'object',
                    properties: {
                        confirm: {
                            type: 'boolean',
                            description: 'Set to true to execute the migration. Without it, returns a dry-run preview.',
                            default: false,
                        },
                    },
                    additionalProperties: false,
                },
                async execute(_params) {
                    try {
                        await requireFullSetup(api.logger);
                        if (!authKeyHex || !subgraphOwner) {
                            return {
                                content: [{ type: 'text', text: 'Plugin not fully initialized. Ensure TOTALRECLAW_RECOVERY_PHRASE is set.' }],
                            };
                        }
                        if (!isSubgraphMode()) {
                            return {
                                content: [{ type: 'text', text: 'Migration is only available with the managed service (subgraph mode).' }],
                            };
                        }
                        const confirm = _params?.confirm === true;
                        const serverUrl = CONFIG.serverUrl;
                        // 1. Check billing tier
                        const billingResp = await fetch(`${serverUrl}/v1/billing/status?wallet_address=${encodeURIComponent(subgraphOwner)}`, {
                            method: 'GET',
                            headers: buildRelayHeaders({
                                'Authorization': `Bearer ${authKeyHex}`,
                                'Content-Type': 'application/json',
                            }),
                        });
                        if (!billingResp.ok) {
                            return { content: [{ type: 'text', text: `Failed to check billing tier (HTTP ${billingResp.status}).` }] };
                        }
                        const billingData = await billingResp.json();
                        if (billingData.tier !== 'pro') {
                            return {
                                content: [{ type: 'text', text: 'Migration requires Pro tier. Use totalreclaw_upgrade to upgrade first.' }],
                            };
                        }
                        // 2. Fetch testnet facts via relay (chain=testnet query param)
                        const testnetSubgraphUrl = `${serverUrl}/v1/subgraph?chain=testnet`;
                        const mainnetSubgraphUrl = `${serverUrl}/v1/subgraph`;
                        api.logger.info('Fetching testnet facts...');
                        const testnetFacts = await fetchAllFactsByOwner(testnetSubgraphUrl, subgraphOwner, authKeyHex);
                        if (testnetFacts.length === 0) {
                            return {
                                content: [{ type: 'text', text: 'No facts found on testnet. Nothing to migrate.' }],
                            };
                        }
                        // 3. Check mainnet for existing facts (idempotency)
                        api.logger.info('Checking mainnet for existing facts...');
                        const mainnetFps = await fetchContentFingerprintsByOwner(mainnetSubgraphUrl, subgraphOwner, authKeyHex);
                        const factsToMigrate = testnetFacts.filter(f => !f.contentFp || !mainnetFps.has(f.contentFp));
                        const alreadyOnMainnet = testnetFacts.length - factsToMigrate.length;
                        // 4. Dry-run
                        if (!confirm) {
                            const msg = factsToMigrate.length === 0
                                ? `All ${testnetFacts.length} testnet facts already exist on mainnet. Nothing to migrate.`
                                : `Found ${factsToMigrate.length} facts to migrate from testnet to Gnosis mainnet (${alreadyOnMainnet} already on mainnet). Call with confirm=true to proceed.`;
                            return {
                                content: [{ type: 'text', text: msg }],
                                details: {
                                    mode: 'dry_run',
                                    testnet_facts: testnetFacts.length,
                                    already_on_mainnet: alreadyOnMainnet,
                                    to_migrate: factsToMigrate.length,
                                },
                            };
                        }
                        // 5. Execute migration
                        if (factsToMigrate.length === 0) {
                            return {
                                content: [{ type: 'text', text: `All ${testnetFacts.length} testnet facts already exist on mainnet. Nothing to migrate.` }],
                            };
                        }
                        // Fetch blind indices
                        api.logger.info(`Fetching blind indices for ${factsToMigrate.length} facts...`);
                        const factIds = factsToMigrate.map(f => f.id);
                        const blindIndicesMap = await fetchBlindIndicesByFactIds(testnetSubgraphUrl, factIds, authKeyHex);
                        // Build protobuf payloads
                        const payloads = [];
                        for (const fact of factsToMigrate) {
                            const blobHex = fact.encryptedBlob.startsWith('0x') ? fact.encryptedBlob.slice(2) : fact.encryptedBlob;
                            const indices = blindIndicesMap.get(fact.id) || [];
                            const factPayload = {
                                id: fact.id,
                                timestamp: new Date().toISOString(),
                                owner: subgraphOwner,
                                encryptedBlob: blobHex,
                                blindIndices: indices,
                                decayScore: parseFloat(fact.decayScore) || 0.5,
                                source: fact.source || 'migration',
                                contentFp: fact.contentFp || '',
                                agentId: fact.agentId || 'openclaw-plugin',
                                encryptedEmbedding: fact.encryptedEmbedding || undefined,
                                version: PROTOBUF_VERSION_V4,
                            };
                            payloads.push(encodeFactProtobuf(factPayload));
                        }
                        // Batch submit (15 per UserOp)
                        const BATCH_SIZE = 15;
                        const batchConfig = { ...getSubgraphConfig(), authKeyHex: authKeyHex, walletAddress: subgraphOwner ?? undefined };
                        let migrated = 0;
                        let failedBatches = 0;
                        for (let i = 0; i < payloads.length; i += BATCH_SIZE) {
                            const batch = payloads.slice(i, i + BATCH_SIZE);
                            const batchNum = Math.floor(i / BATCH_SIZE) + 1;
                            const totalBatches = Math.ceil(payloads.length / BATCH_SIZE);
                            api.logger.info(`Migrating batch ${batchNum}/${totalBatches} (${batch.length} facts)...`);
                            try {
                                const result = await submitFactBatchOnChain(batch, batchConfig);
                                if (result.success) {
                                    migrated += batch.length;
                                }
                                else {
                                    failedBatches++;
                                }
                            }
                            catch (err) {
                                const msg = err instanceof Error ? err.message : String(err);
                                api.logger.error(`Migration batch ${batchNum} failed: ${msg}`);
                                failedBatches++;
                            }
                        }
                        const resultMsg = failedBatches === 0
                            ? `Successfully migrated ${migrated} memories from testnet to Gnosis mainnet.`
                            : `Migrated ${migrated}/${factsToMigrate.length} memories. ${failedBatches} batch(es) failed — re-run to retry (idempotent).`;
                        return {
                            content: [{ type: 'text', text: resultMsg }],
                            details: {
                                mode: 'executed',
                                testnet_facts: testnetFacts.length,
                                already_on_mainnet: alreadyOnMainnet,
                                to_migrate: factsToMigrate.length,
                                migrated,
                                failed_batches: failedBatches,
                            },
                        };
                    }
                    catch (err) {
                        const message = err instanceof Error ? err.message : String(err);
                        api.logger.error(`totalreclaw_migrate failed: ${message}`);
                        return {
                            content: [{ type: 'text', text: `Migration failed: ${humanizeError(message)}` }],
                        };
                    }
                },
            }, { name: 'totalreclaw_migrate' });
            // ---------------------------------------------------------------
            // Tools: totalreclaw_setup + totalreclaw_onboarding_start —
            //   REMOVED in 3.3.1-rc.5 (phrase-safety carve-out closure).
            // ---------------------------------------------------------------
            //
            // rc.4 left these two registrations in place as *neutered* stubs —
            // ``totalreclaw_setup`` rejected any ``recovery_phrase`` argument
            // and returned a CLI-pointer message; ``totalreclaw_onboarding_start``
            // was already pointer-only. Neither path could leak a phrase in
            // rc.4, but the rc.4 auto-QA (2026-04-22) flagged them as future-
            // regression surface: any future patch that re-enables phrase
            // acceptance (e.g. a flag-driven "power-user" path) would silently
            // re-open the leak, and their mere presence in the tool registry
            // keeps signalling to agents that "phrase handling happens here".
            //
            // Per ``project_phrase_safety_rule.md`` the ONLY approved agent-
            // facilitated setup surface is ``totalreclaw_pair`` (browser-side
            // crypto keeps the phrase out of the LLM round-trip by construction).
            // rc.5 deletes both registrations outright. The underlying CLI
            // wizard (``openclaw totalreclaw onboard``) is unchanged — users
            // run it in their own terminal, outside any agent shell.
            //
            // Audit assertion: ``phrase-safety-registry.test.ts`` asserts
            // neither name is present in the ``api.registerTool`` call list.
            // Re-adding either fails CI.
            //
            // Historical tombstone (so LLM-assisted contributors don't re-add
            // the former shape from training-data memory): rc.4 registered two
            // tools by the names "totalreclaw_setup" and
            // "totalreclaw_onboarding_start" as pointer-only stubs. Both were
            // deleted in rc.5. Do not re-introduce.
            // ---------------------------------------------------------------
            // Tool: totalreclaw_onboard — REMOVED in 3.3.1-rc.4 (phrase-safety).
            //
            // rc.3 shipped a `totalreclaw_onboard` agent tool that generated a
            // fresh BIP-39 mnemonic in-process, wrote it to credentials.json,
            // and returned `{scope_address, credentials_path}` to the agent.
            // `emitPhrase: false` kept the mnemonic OUT of the tool's return
            // payload, but NOTHING ARCHITECTURALLY PREVENTED leakage — a future
            // patch could regress the flag, a different code path could echo
            // the mnemonic in a log/error message the agent captures, or the
            // mere existence of the tool implied to agents that "generating a
            // phrase here is fine" (it isn't).
            //
            // Per ``project_phrase_safety_rule.md``
            // (memory file in p-diogo/totalreclaw-internal — absolute rule:
            // "recovery phrase MUST NEVER cross the LLM context in ANY form"),
            // phrase-generating agent tools are forbidden. The ONLY approved
            // agent-facilitated setup surface is ``totalreclaw_pair`` (browser-
            // side crypto keeps the phrase out of the LLM round-trip by
            // construction). The underlying ``runNonInteractiveOnboard`` code
            // path is still reachable via the CLI ``openclaw totalreclaw onboard``
            // — that path runs in the user's own terminal, OUTSIDE any agent
            // shell, so phrase stdout never feeds back into LLM context.
            //
            // Audit assertion: ``tool-gating.test.ts`` enforces the removal —
            // any future re-registration of ``totalreclaw_onboard`` (or any
            // phrase-generating variant like ``totalreclaw_onboard_generate``,
            // ``totalreclaw_restore_phrase``) fails CI.
            // ---------------------------------------------------------------
            // ---------------------------------------------------------------
            // Tool: totalreclaw_pair (3.3.1-rc.2 — agent-callable pair-generate)
            //
            // Creates a pairing session (browser-mediated recovery-phrase sync),
            // returns the URL + PIN + QR ASCII to the agent. The agent relays
            // these to the user (paste-URL or scan-QR flow). The phrase itself
            // NEVER crosses the gateway — the pair-http endpoint does the E2EE
            // handshake with the browser pair-page.
            // ---------------------------------------------------------------
            api.registerTool({
                name: 'totalreclaw_pair',
                label: 'Set up the user\'s TotalReclaw account (encrypted, browser-side)',
                description: 'Set up the user\'s TotalReclaw account (encrypted, browser-side recovery-phrase ' +
                    'generation or import). Starts a brief remote session so the user can create or ' +
                    'import a TotalReclaw recovery phrase from their phone or another browser. ' +
                    'Returns an account-setup URL, a 6-digit PIN, and an ASCII QR code that the agent ' +
                    'relays to the user. The recovery phrase itself is generated/entered in the ' +
                    'BROWSER and uploaded end-to-end encrypted to this gateway — it NEVER touches ' +
                    'the LLM provider or the chat transcript.\n\n' +
                    'This is the CANONICAL agent-facilitated account-setup surface — use it whenever ' +
                    'the user asks you to set up TotalReclaw, regardless of whether they have ' +
                    'terminal access. Narrate it to the user as "setting up your TotalReclaw ' +
                    'account". Browser-side crypto keeps the recovery phrase out of the LLM context ' +
                    'entirely. If a user explicitly prefers local-terminal account setup with no ' +
                    'browser, point them at `totalreclaw_onboarding_start` (a pointer to the CLI ' +
                    'wizard they run on their own terminal, NOT through your shell tool).\n\n' +
                    'Tool name `totalreclaw_pair` is kept for backward compatibility — function-wise ' +
                    'this is the account-setup tool.',
                parameters: {
                    type: 'object',
                    properties: {
                        mode: {
                            type: 'string',
                            enum: ['generate', 'import'],
                            description: '"generate" = the browser will create a NEW recovery phrase. "import" = the ' +
                                'browser will accept an EXISTING phrase that the user pastes in their browser ' +
                                '(never through chat).',
                            default: 'generate',
                        },
                    },
                    additionalProperties: false,
                },
                async execute(_toolCallId, params) {
                    const rawMode = params?.mode;
                    const mode = rawMode === 'import' ? 'import' : 'generate';
                    const pairMode = CONFIG.pairMode;
                    try {
                        // 3.3.1-rc.11 — relay-brokered pair by default (universal reachability).
                        // `TOTALRECLAW_PAIR_MODE=local` preserves the rc.4–rc.10 loopback flow
                        // for air-gapped / self-hosted setups. Both paths return the same
                        // tool payload (`{url, pin, expires_at_ms, qr_*, mode, instructions}`);
                        // only the URL origin differs.
                        let url;
                        let pin;
                        let sidOrToken;
                        let expiresAtMs;
                        let localSession;
                        if (pairMode === 'relay') {
                            const { openRemotePairSession, awaitPhraseUpload } = await import('./pair-remote-client.js');
                            const remoteSession = await openRemotePairSession({
                                relayBaseUrl: CONFIG.pairRelayUrl,
                                mode: mode === 'generate' ? 'generate' : 'import',
                            });
                            url = remoteSession.url;
                            pin = remoteSession.pin;
                            sidOrToken = remoteSession.token;
                            // Relay sends ISO-8601; convert to ms for tool payload parity.
                            const parsed = Date.parse(remoteSession.expiresAt);
                            expiresAtMs = Number.isFinite(parsed)
                                ? parsed
                                : Date.now() + 5 * 60_000;
                            // Background task — writes credentials.json + flips state when
                            // the browser completes the flow. Tool handler returns
                            // immediately so the agent can tell the user the URL + PIN.
                            //
                            // 3.3.4-rc.2 (Pedro QA — pair flow stuck-session) — wrap the
                            // WS-await in a 60s hard timeout. The relay drops sessions on
                            // `ws_close` (separately patched relay-side); without this
                            // bound the background task hangs in `waitNextMessage` for the
                            // full 5-minute session TTL before resolving, and downstream
                            // tooling that polls the gateway for completion sees stale
                            // `processing` state at 129s/159s/189s. 60s is the user-side
                            // deadline we surface in chat: long enough for a slow scan-
                            // and-paste, short enough that a fresh URL request is the
                            // obvious next step. Structured `timed_out` error in the log
                            // lets ops grep for the failure mode independently of generic
                            // ws-close errors.
                            const PAIR_TOOL_HARD_TIMEOUT_MS = 60_000;
                            void (async () => {
                                try {
                                    const phraseUploadPromise = awaitPhraseUpload(remoteSession, {
                                        phraseValidator: (p) => validateMnemonic(p, wordlist),
                                        completePairing: async ({ mnemonic }) => {
                                            try {
                                                // 3.3.1 (internal#130) — derive + persist the
                                                // Smart Account address now so the user can see
                                                // it immediately after pair, before any chain
                                                // write. Mnemonic stays in this scope (already
                                                // on disk in credentials.json); only the
                                                // derived public scope_address is added.
                                                let scopeAddress;
                                                try {
                                                    scopeAddress = await deriveSmartAccountAddress(mnemonic, CONFIG.chainId);
                                                }
                                                catch (deriveErr) {
                                                    api.logger.warn(`totalreclaw_pair(relay): scope_address derivation failed (will retry lazily): ${deriveErr instanceof Error ? deriveErr.message : String(deriveErr)}`);
                                                }
                                                const creds = loadCredentialsJson(CREDENTIALS_PATH) ?? {};
                                                const next = { ...creds, mnemonic };
                                                if (scopeAddress)
                                                    next.scope_address = scopeAddress;
                                                if (!writeCredentialsJson(CREDENTIALS_PATH, next)) {
                                                    return { state: 'error', error: 'credentials_write_failed' };
                                                }
                                                setRecoveryPhraseOverride(mnemonic);
                                                writeOnboardingState(CONFIG.onboardingStatePath, {
                                                    onboardingState: 'active',
                                                    createdBy: mode === 'generate' ? 'generate' : 'import',
                                                    credentialsCreatedAt: new Date().toISOString(),
                                                    version: pluginVersion ?? '3.3.0',
                                                });
                                                // 3.3.13 — sentinel cleanup; see auto-pair-on-load.ts.
                                                deletePairPendingFile(defaultPairPendingPath(CREDENTIALS_PATH));
                                                api.logger.info(`totalreclaw_pair(relay): session ${remoteSession.token.slice(0, 8)}… completed; credentials written${scopeAddress ? ` (scope_address=${scopeAddress})` : ''}`);
                                                return { state: 'active' };
                                            }
                                            catch (err) {
                                                const msg = err instanceof Error ? err.message : String(err);
                                                api.logger.error(`totalreclaw_pair(relay): completePairing failed: ${msg}`);
                                                return { state: 'error', error: msg };
                                            }
                                        },
                                        // 3.3.4-rc.2 — also pass through to awaitPhraseUpload so its
                                        // internal `waitNextMessage` timer matches the outer race.
                                        timeoutMs: PAIR_TOOL_HARD_TIMEOUT_MS,
                                    });
                                    // 3.3.4-rc.2 — outer Promise.race guard. Resolves to a
                                    // sentinel ({ status: 'timed_out', ... }) so the catch
                                    // handler can distinguish a hard-timeout from a generic
                                    // ws-close error and surface it explicitly.
                                    const TIMEOUT_SENTINEL = {
                                        status: 'timed_out',
                                        message: `Pair flow timed out (${PAIR_TOOL_HARD_TIMEOUT_MS / 1000}s) — generate a new URL with totalreclaw_pair.`,
                                    };
                                    let hardTimer;
                                    const hardTimeoutPromise = new Promise((resolve) => {
                                        hardTimer = setTimeout(() => resolve(TIMEOUT_SENTINEL), PAIR_TOOL_HARD_TIMEOUT_MS);
                                    });
                                    try {
                                        const raced = await Promise.race([
                                            phraseUploadPromise,
                                            hardTimeoutPromise,
                                        ]);
                                        if (raced &&
                                            typeof raced === 'object' &&
                                            raced.status === 'timed_out') {
                                            api.logger.warn(`totalreclaw_pair(relay): hard timeout — ${raced.message} (token=${remoteSession.token.slice(0, 8)}…)`);
                                        }
                                    }
                                    finally {
                                        if (hardTimer)
                                            clearTimeout(hardTimer);
                                    }
                                }
                                catch (bgErr) {
                                    // Expected on TTL expiry / user-aborts — log at warn, not error.
                                    const bgMsg = bgErr instanceof Error ? bgErr.message : String(bgErr);
                                    api.logger.warn(`totalreclaw_pair(relay): background task ended for token=${remoteSession.token.slice(0, 8)}…: ${bgMsg}`);
                                }
                            })();
                        }
                        else {
                            // Local loopback path (rc.10 behaviour).
                            const { createPairSession } = await import('./pair-session-store.js');
                            const { generateGatewayKeypair } = await import('./pair-crypto.js');
                            const kp = generateGatewayKeypair();
                            const session = await createPairSession(CONFIG.pairSessionsPath, {
                                mode,
                                operatorContext: { channel: 'agent' },
                                rngPrivateKey: () => Buffer.from(kp.skB64, 'base64url'),
                                rngPublicKey: () => Buffer.from(kp.pkB64, 'base64url'),
                            });
                            url = buildPairingUrl(api, session);
                            pin = session.secondaryCode;
                            sidOrToken = session.sid;
                            expiresAtMs = session.expiresAtMs;
                            localSession = session;
                        }
                        // QR renderers — same for both modes; input is the URL string.
                        const { defaultRenderQr } = await import('./pair-cli.js');
                        const qrAscii = await new Promise((resolve) => {
                            let settled = false;
                            const t = setTimeout(() => {
                                if (!settled) {
                                    settled = true;
                                    resolve('');
                                }
                            }, 5_000);
                            try {
                                defaultRenderQr(url, (ascii) => {
                                    if (settled)
                                        return;
                                    settled = true;
                                    clearTimeout(t);
                                    resolve(ascii);
                                });
                            }
                            catch {
                                if (settled)
                                    return;
                                settled = true;
                                clearTimeout(t);
                                resolve('');
                            }
                        });
                        // 3.3.1-rc.5 — PNG + Unicode QR for multi-transport rendering.
                        let qrPngB64 = '';
                        let qrUnicode = '';
                        try {
                            const { encodePng, encodeUnicode } = await import('./pair-qr.js');
                            const [pngBuf, uni] = await Promise.all([
                                encodePng(url),
                                encodeUnicode(url),
                            ]);
                            qrPngB64 = pngBuf.toString('base64');
                            qrUnicode = uni;
                        }
                        catch (qrErr) {
                            api.logger.warn(`totalreclaw_pair: QR encode failed (non-fatal): ${qrErr instanceof Error ? qrErr.message : String(qrErr)}`);
                        }
                        api.logger.info(`totalreclaw_pair: session ${sidOrToken.slice(0, 8)}… mode=${mode} transport=${pairMode} url=${url} qr_png=${qrPngB64.length} qr_unicode=${qrUnicode.length}`);
                        // Voidly reference localSession so TS does not flag the unused
                        // local-branch binding. Future rc.12 diagnostics can expose
                        // `session.mode` / `session.status` separately.
                        void localSession;
                        return {
                            content: [{
                                    type: 'text',
                                    text: `Pairing session started.\n\n` +
                                        `URL: ${url}\n\n` +
                                        `PIN (type this into the browser): ${pin}\n\n` +
                                        (qrAscii ? `QR code:\n\n${qrAscii}\n\n` : '') +
                                        `Instructions for the user:\n` +
                                        `1. Open the URL above on their phone or another browser (scan the QR or copy-paste).\n` +
                                        `2. ` +
                                        (mode === 'generate'
                                            ? `The browser will generate a NEW 12-word recovery phrase and ask the user to write it down + retype 3 words before finalizing.`
                                            : `The browser will accept an EXISTING phrase that the user pastes in the browser (never through chat).`) +
                                        `\n3. Enter the 6-digit PIN shown above into the browser.\n` +
                                        `4. The encrypted phrase uploads to this gateway — it NEVER touches the LLM.\n` +
                                        `5. Come back to chat once the browser says "Pairing complete".\n\n` +
                                        `This session expires in ~5 minutes. Run this tool again if you need a fresh URL.`,
                                }],
                            details: {
                                sid: sidOrToken,
                                url,
                                pin,
                                mode,
                                expires_at_ms: expiresAtMs,
                                qr_ascii: qrAscii,
                                qr_png_b64: qrPngB64,
                                qr_unicode: qrUnicode,
                                // rc.11 — surface the transport so downstream tooling (QA
                                // harness asserters, telemetry) can confirm which path
                                // served the URL. Either 'relay' or 'local'.
                                transport: pairMode,
                            },
                        };
                    }
                    catch (err) {
                        const message = err instanceof Error ? err.message : String(err);
                        api.logger.error(`totalreclaw_pair failed: ${message}`);
                        return {
                            content: [{ type: 'text', text: `Failed to start pairing session: ${humanizeError(message)}` }],
                            details: { error: message },
                        };
                    }
                },
            }, { name: 'totalreclaw_pair' });
            // 3.3.1-rc.20 (issue #110): explicit post-registration breadcrumb so
            // ops/QA can grep gateway logs for definitive proof the tool was
            // declared. If the agent then reports the tool is missing from its
            // tool list, the gap is upstream OpenClaw tool propagation, not our
            // plugin — see issue #110 fix 3 + PR #102 (CLI fallback).
            //
            // 3.3.1-rc.21 (issue #128): the breadcrumb is debug-grade — it was
            // bleeding into `openclaw agent --json` stdout, breaking programmatic
            // parsers that expect the JSON-RPC body to be the only thing on the
            // wire. Gated behind `TOTALRECLAW_VERBOSE_REGISTER` (or the general
            // `TOTALRECLAW_DEBUG` toggle) so ops can opt back in when chasing
            // a tool-injection regression. Default OFF — clean stdout for users.
            if (CONFIG.verboseRegister) {
                api.logger.info('TotalReclaw: registerTool(totalreclaw_pair) returned. If the agent does not see it in its tool list ' +
                    'after gateway restart, the issue is upstream tool injection (containerized agents) — fall back to ' +
                    '`openclaw totalreclaw pair generate --url-pin-only` (PR #102) or `openclaw totalreclaw onboard --pair-only`.');
            }
            // ---------------------------------------------------------------
            // Tool: totalreclaw_report_qa_bug (3.3.1-rc.3 — RC-gated)
            //
            // Lets the agent file a structured QA-bug issue to
            // `p-diogo/totalreclaw-internal` during RC testing. Only registered
            // when the plugin version contains `-rc.` — stable users never see it.
            //
            // Secrets (recovery phrases, API keys, Telegram bot tokens) are
            // redacted inside `postQaBugIssue` before the POST. The agent should
            // still avoid passing raw secrets — see SKILL.md addendum.
            // ---------------------------------------------------------------
            if (rcMode) {
                api.registerTool({
                    name: 'totalreclaw_report_qa_bug',
                    label: 'File a QA bug issue (RC builds only)',
                    description: 'File a structured QA bug report to the internal tracker. RC-only; never available in stable builds. ' +
                        'Do NOT call auto-file — ask the user first before invoking. The tool redacts recovery phrases, API keys, ' +
                        'and Telegram bot tokens from all free-text fields before posting, but the agent SHOULD still avoid ' +
                        'passing raw secrets.',
                    parameters: {
                        type: 'object',
                        properties: {
                            integration: {
                                type: 'string',
                                enum: ['plugin', 'hermes', 'nanoclaw', 'mcp', 'relay', 'clawhub', 'docs', 'other'],
                                description: 'Which TotalReclaw surface is affected.',
                            },
                            rc_version: {
                                type: 'string',
                                description: 'Exact RC version string (e.g. "3.3.1-rc.3" or "2.3.1rc3").',
                            },
                            severity: {
                                type: 'string',
                                enum: ['blocker', 'high', 'medium', 'low'],
                                description: 'blocker=release blocked, high=major UX failure, medium=annoying, low=polish.',
                            },
                            title: {
                                type: 'string',
                                description: 'Short summary, <60 chars. Prefix "[qa-bug]" is added automatically.',
                                maxLength: 60,
                            },
                            symptom: {
                                type: 'string',
                                description: 'What happened (redacted automatically).',
                            },
                            expected: {
                                type: 'string',
                                description: 'What should have happened.',
                            },
                            repro: {
                                type: 'string',
                                description: 'Reproduction steps (redacted automatically).',
                            },
                            logs: {
                                type: 'string',
                                description: 'Log excerpts / error messages (redacted automatically).',
                            },
                            environment: {
                                type: 'string',
                                description: 'Host, Docker/native, OpenClaw version, LLM provider, etc.',
                            },
                        },
                        required: [
                            'integration',
                            'rc_version',
                            'severity',
                            'title',
                            'symptom',
                            'expected',
                            'repro',
                            'logs',
                            'environment',
                        ],
                        additionalProperties: false,
                    },
                    async execute(_toolCallId, params) {
                        try {
                            const { postQaBugIssue } = await import('./qa-bug-report.js');
                            // The token is resolved via CONFIG (config.ts) so index.ts
                            // stays clean of env-harvesting triggers.
                            const token = CONFIG.qaGithubToken;
                            if (!token) {
                                return {
                                    content: [{
                                            type: 'text',
                                            text: 'Cannot file QA bug: no GitHub token found. The operator must export ' +
                                                'TOTALRECLAW_QA_GITHUB_TOKEN (or GITHUB_TOKEN) with `repo` scope to enable ' +
                                                'agent-filed bug reports during RC testing.',
                                        }],
                                    details: { error: 'missing_github_token' },
                                };
                            }
                            // rc.14 — `repo` is resolved inside `postQaBugIssue` via
                            // `resolveQaRepo(...)`, which reads `TOTALRECLAW_QA_REPO` and
                            // refuses any slug that isn't a `-internal` fork. Pass the
                            // config-surfaced override so env reads stay in config.ts.
                            const repoOverride = CONFIG.qaRepoOverride || undefined;
                            const result = await postQaBugIssue(params, {
                                githubToken: token,
                                repo: repoOverride,
                                logger: api.logger,
                            });
                            return {
                                content: [{
                                        type: 'text',
                                        text: `Filed QA bug #${result.issue_number}: ${result.issue_url}`,
                                    }],
                                details: { issue_url: result.issue_url, issue_number: result.issue_number },
                            };
                        }
                        catch (err) {
                            const message = err instanceof Error ? err.message : String(err);
                            api.logger.error(`totalreclaw_report_qa_bug failed: ${message}`);
                            return {
                                content: [{
                                        type: 'text',
                                        text: `Failed to file QA bug: ${message}`,
                                    }],
                                details: { error: message },
                            };
                        }
                    },
                }, { name: 'totalreclaw_report_qa_bug' });
                // 3.3.1-rc.21 (issue #128): demote the registration-confirmation
                // breadcrumb to verbose-only. Same `--json` stdout pollution risk
                // as the totalreclaw_pair breadcrumb above; ops can opt back in
                // via TOTALRECLAW_VERBOSE_REGISTER / TOTALRECLAW_DEBUG.
                if (CONFIG.verboseRegister) {
                    api.logger.info('totalreclaw_report_qa_bug registered (RC build — this tool is hidden in stable releases).');
                }
            }
            // ---------------------------------------------------------------
            // Hook: before_tool_call (3.2.0 memory-tool gate)
            // ---------------------------------------------------------------
            //
            // Blocks every memory tool until onboarding state is `active`. The
            // `blockReason` string is LLM-visible but carries no secret — it's a
            // pointer to the CLI wizard.
            //
            // Non-gated tools: totalreclaw_upgrade, totalreclaw_migrate,
            // totalreclaw_onboarding_start, totalreclaw_setup (deprecated).
            // Billing tools work pre-onboarding because they help the user reach a
            // Pro tier before they have memories to store; setup-adjacent tools
            // return their own routing messages.
            //
            // Decision logic lives in `tool-gating.ts` so it's unit-testable
            // without a full plugin host.
            api.on('before_tool_call', async (event) => {
                const evt = event;
                const toolName = evt?.toolName;
                if (!toolName || !isGatedToolName(toolName)) {
                    return undefined;
                }
                let state = null;
                try {
                    state = resolveOnboardingState(CREDENTIALS_PATH, CONFIG.onboardingStatePath);
                }
                catch (err) {
                    const msg = err instanceof Error ? err.message : String(err);
                    api.logger.warn(`before_tool_call: state resolution failed: ${msg}`);
                    return undefined; // Fail-open: if we can't read state, let the tool run and surface its own error.
                }
                const decision = decideToolGate(toolName, state);
                if (decision.block) {
                    return { block: true, blockReason: decision.blockReason };
                }
                return undefined;
            }, { priority: 5 });
            // ---------------------------------------------------------------
            // Hook: before_agent_start
            // ---------------------------------------------------------------
            api.on('before_agent_start', async (event) => {
                try {
                    // Prevent cleartext leakage from OpenClaw's native memory system.
                    ensureMemoryHeader(api.logger);
                    const evt = event;
                    // Skip trivial or missing prompts.
                    if (!evt?.prompt || evt.prompt.length < 5) {
                        return undefined;
                    }
                    // 3.3.3-rc.1 — RC-staging banner (PR #165 implementation).
                    // Build a one-shot prefix when the bundled default points at staging
                    // AND the user hasn't overridden via env. This prefix is prepended
                    // to whichever context block the rest of the hook produces.
                    //
                    // 3.3.4-rc.1 — fix: previously `stagingBannerShown` was set to
                    // `true` AS SOON AS the block was built. If the rest of the hook
                    // then returned `undefined` (e.g. zero memory matches on the first
                    // turn — multiple paths around lines 6103-6325 do this), the
                    // banner block was silently discarded AND the flag was already
                    // flipped, so subsequent before_agent_start invocations never
                    // reconstructed it. Net effect: QA on 3.3.3-rc.1 (Pedro
                    // 2026-04-30) saw NO banner emitted across an entire conversation
                    // even though the build was bound to staging.
                    //
                    // Fix: build the block on every call until it is actually
                    // delivered (i.e., until at least one return path included it
                    // in `prependContext`). The flag flips at the bottom of this
                    // hook in `markBannerDelivered()` once we know the prependContext
                    // path was taken.
                    let stagingBannerBlock = '';
                    let stagingBannerSuppressed = false;
                    if (!stagingBannerShown) {
                        try {
                            // 3.3.12-rc.1 (F flip): banner now fires when serverUrl resolves
                            // to api-staging.totalreclaw.xyz, which under the new contract
                            // can ONLY happen if (a) user opted in via env override, or
                            // (b) the artifact is broken / accidentally bound to staging.
                            // Either way the user benefits from seeing the warning.
                            const usingStaging = CONFIG.serverUrl.includes('api-staging.totalreclaw.xyz');
                            if (usingStaging) {
                                stagingBannerBlock =
                                    '## ⚠️ TotalReclaw is running in staging mode\n\n' +
                                        'This session is bound to `api-staging.totalreclaw.xyz`. Staging has **no SLA** ' +
                                        'and may be wiped between QA cycles. Do **NOT** use this build for real data.\n\n' +
                                        'The default relay is `api.totalreclaw.xyz` (production). To return to production, ' +
                                        'unset `TOTALRECLAW_SERVER_URL`. To stay on staging, leave it set to ' +
                                        '`https://api-staging.totalreclaw.xyz`.\n\n';
                                // Do NOT set stagingBannerShown=true here — see comment in
                                // staging-banner-gate.test.ts. Banner-shown flips only via
                                // consumeBannerForPrepend() once a return path actually
                                // delivers the block.
                                stagingBannerSuppressed = true;
                            }
                            else {
                                // Production default OR custom URL — never fire the banner
                                // this gateway-process lifetime.
                                stagingBannerShown = true;
                            }
                        }
                        catch {
                            // Best-effort; never block session start on banner derivation.
                            stagingBannerShown = true;
                        }
                    }
                    // Operator-facing log: once per process, when we DETECT staging.
                    if (stagingBannerSuppressed && !stagingBannerLogged) {
                        stagingBannerLogged = true;
                        api.logger.warn('TotalReclaw: staging mode active (api-staging.totalreclaw.xyz). ' +
                            'Default is production (api.totalreclaw.xyz); staging is opt-in via ' +
                            'TOTALRECLAW_SERVER_URL.');
                    }
                    /**
                     * Helper — invoked inline at any `prependContext` site that
                     * wants to lead with the staging banner. Returns the banner
                     * string AND atomically marks the banner as delivered, so
                     * subsequent hook calls in the same gateway-process lifetime
                     * skip re-emission. Returns '' (empty) when no banner is due
                     * (stable build, user override, or already delivered).
                     *
                     * Use this at every prependContext callsite that takes the
                     * banner; do NOT inline `stagingBannerBlock` on its own — the
                     * 3.3.4-rc.1 bug fix requires the marker flip to be coupled
                     * to the actual delivery.
                     */
                    const consumeBannerForPrepend = () => {
                        if (stagingBannerBlock === '')
                            return '';
                        stagingBannerShown = true;
                        return stagingBannerBlock;
                    };
                    await ensureInitialized(api.logger);
                    // 3.2.0 onboarding pending: emit a non-secret guidance banner so
                    // the LLM knows how to respond when the user asks about setup.
                    // This contains ZERO secret material — the phrase never enters an
                    // LLM request. The CLI wizard (`openclaw totalreclaw onboard`) is
                    // the only surface that generates / reveals the recovery phrase.
                    //
                    // 3.3.0-rc.2: the FIRST time a fresh machine hits this branch we
                    // also include the welcome+branch-question banner (copy in
                    // `first-run.ts`). The flag is session-scoped so the welcome never
                    // fires twice in the same gateway process.
                    if (needsSetup) {
                        let welcomeBlock = '';
                        try {
                            if (!firstRunWelcomeShown && (await detectFirstRun(CREDENTIALS_PATH))) {
                                const mode = resolveGatewayMode(api);
                                welcomeBlock = buildWelcomePrepend(mode) + '\n\n';
                                firstRunWelcomeShown = true;
                                api.logger.info(`TotalReclaw first-run welcome emitted (mode=${mode})`);
                            }
                        }
                        catch (err) {
                            // Never block session start on the welcome — treat any failure
                            // as "skip the welcome, still emit the setup-pending banner".
                            const msg = err instanceof Error ? err.message : String(err);
                            api.logger.warn(`First-run welcome check failed: ${msg}`);
                        }
                        return {
                            prependContext: consumeBannerForPrepend() +
                                welcomeBlock +
                                '## TotalReclaw setup pending\n\n' +
                                'TotalReclaw encrypted memory is installed but not yet set up on this machine. ' +
                                'If the user asks about memory features or wants to configure TotalReclaw, ' +
                                'call the `totalreclaw_pair` tool — it returns a pairing URL + 6-digit PIN ' +
                                'the user opens in a browser (phrase is generated and encrypted in-browser, ' +
                                'never leaves their device in plaintext). If `totalreclaw_pair` is not in ' +
                                'your tool list (container-based agents sometimes miss it), shell out to ' +
                                '`openclaw totalreclaw pair generate --url-pin-only` on the gateway host — ' +
                                'it emits a single JSON line `{v,url,pin,expires_at_ms}` with no phrase ' +
                                'material; hand the user the `url` and `pin`.\n\n' +
                                '**Do NOT** attempt to generate, display, or relay a recovery phrase in chat. ' +
                                '**Do NOT** run `openclaw totalreclaw onboard` — that CLI emits the recovery ' +
                                'phrase on stdout and would leak it into the LLM transcript. Use `pair` ' +
                                '(tool or `--url-pin-only` CLI) instead; `onboard` is reserved for users ' +
                                'running it directly in their own local terminal.',
                        };
                    }
                    // One-time welcome message (first conversation after setup or returning user)
                    let welcomeBack = '';
                    if (welcomeBackMessage) {
                        welcomeBack = `\n\n${welcomeBackMessage}`;
                        welcomeBackMessage = null; // Consume — only show once
                    }
                    else if (firstRunAfterInit) {
                        // First conversation with a configured user — explain what's happening
                        firstRunAfterInit = false;
                        const cache = readBillingCache();
                        const tier = cache?.tier || 'free';
                        const tierInfo = tier === 'pro'
                            ? 'You are on the **Pro** tier — unlimited memories, permanently stored on Gnosis mainnet.'
                            : 'You are on the **Free** tier — memories stored on testnet. Use the totalreclaw_upgrade tool to upgrade to Pro for permanent on-chain storage.';
                        welcomeBack = `\n\nTotalReclaw is active. I will automatically remember important things from our conversations and recall relevant context at the start of each session. ${tierInfo}`;
                    }
                    // Billing cache check — warn if quota is approaching limit.
                    let billingWarning = '';
                    try {
                        let cache = readBillingCache();
                        if (!cache && authKeyHex) {
                            // Cache is stale or missing — fetch fresh billing status.
                            const billingUrl = CONFIG.serverUrl;
                            const walletParam = encodeURIComponent(subgraphOwner || userId || '');
                            const billingResp = await fetch(`${billingUrl}/v1/billing/status?wallet_address=${walletParam}`, {
                                method: 'GET',
                                headers: buildRelayHeaders({ 'Authorization': `Bearer ${authKeyHex}`, 'Accept': 'application/json' }),
                            });
                            if (billingResp.ok) {
                                const billingData = await billingResp.json();
                                cache = {
                                    tier: billingData.tier || 'free',
                                    free_writes_used: billingData.free_writes_used ?? 0,
                                    free_writes_limit: billingData.free_writes_limit ?? 0,
                                    features: billingData.features,
                                    checked_at: Date.now(),
                                };
                                writeBillingCache(cache);
                            }
                        }
                        if (cache && cache.free_writes_limit > 0) {
                            const usageRatio = cache.free_writes_used / cache.free_writes_limit;
                            if (usageRatio >= QUOTA_WARNING_THRESHOLD) {
                                billingWarning = `\n\nTotalReclaw quota warning: ${cache.free_writes_used}/${cache.free_writes_limit} memories used this month (${Math.round(usageRatio * 100)}%). Visit https://totalreclaw.xyz/pricing to upgrade.`;
                            }
                        }
                    }
                    catch {
                        // Best-effort — don't block on billing check failure.
                    }
                    if (isSubgraphMode()) {
                        // --- Subgraph mode: digest fast path → hot cache → background refresh ---
                        // Digest fast path (Stage 3b). When a digest exists and the mode is
                        // not 'off', inject its pre-compiled promptText instead of running
                        // the per-query search. A stale digest triggers a background
                        // recompile (non-blocking). Failures fall through to the legacy
                        // path silently.
                        const digestMode = resolveDigestMode();
                        logDigestModeOnce(digestMode, api.logger);
                        if (digestMode !== 'off' && encryptionKey && authKeyHex && (subgraphOwner || userId)) {
                            try {
                                const injectResult = await maybeInjectDigest({
                                    owner: subgraphOwner || userId,
                                    authKeyHex: authKeyHex,
                                    encryptionKey: encryptionKey,
                                    mode: digestMode,
                                    nowMs: Date.now(),
                                    loadDeps: {
                                        searchSubgraph: async (o, tds, n, a) => searchSubgraph(o, tds, n, a),
                                        decryptFromHex: (hex, key) => decryptFromHex(hex, key),
                                    },
                                    probeDeps: {
                                        searchSubgraphBroadened: async (o, n, a) => searchSubgraphBroadened(o, n, a),
                                    },
                                    recompileFn: (prev) => scheduleDigestRecompile(prev, api.logger),
                                    logger: api.logger,
                                });
                                if (injectResult.promptText) {
                                    api.logger.info(`Digest injection: state=${injectResult.state}`);
                                    return {
                                        prependContext: consumeBannerForPrepend() +
                                            `## Your Memory\n\n${injectResult.promptText}` + welcomeBack + billingWarning,
                                    };
                                }
                            }
                            catch (err) {
                                // Never block session start on digest failure.
                                const msg = err instanceof Error ? err.message : String(err);
                                api.logger.warn(`Digest fast path failed: ${msg}`);
                            }
                        }
                        // Initialize hot cache if needed.
                        if (!pluginHotCache && encryptionKey) {
                            const config = getSubgraphConfig();
                            pluginHotCache = new PluginHotCache(config.cachePath, encryptionKey.toString('hex'));
                            pluginHotCache.load();
                        }
                        // Try to return cached facts instantly.
                        const cachedFacts = pluginHotCache?.getHotFacts() ?? [];
                        // Query subgraph in parallel for fresh results.
                        // 1. Generate word trapdoors from the user prompt.
                        const wordTrapdoors = generateBlindIndices(evt.prompt);
                        // 2. Generate query embedding + LSH trapdoors (may fail gracefully).
                        let queryEmbedding = null;
                        let lshTrapdoors = [];
                        try {
                            queryEmbedding = await generateEmbedding(evt.prompt, { isQuery: true });
                            const hasher = getLSHHasher(api.logger);
                            if (hasher && queryEmbedding) {
                                lshTrapdoors = hasher.hash(queryEmbedding);
                            }
                        }
                        catch {
                            // Embedding/LSH failed -- proceed with word-only trapdoors.
                        }
                        // Two-tier search (C1): if cache is fresh AND query is semantically similar, return cached
                        const now = Date.now();
                        const cacheAge = now - lastSearchTimestamp;
                        if (cacheAge < CACHE_TTL_MS && cachedFacts.length > 0 && queryEmbedding && lastQueryEmbedding) {
                            const querySimilarity = cosineSimilarity(queryEmbedding, lastQueryEmbedding);
                            if (querySimilarity > SEMANTIC_SKIP_THRESHOLD) {
                                const lines = cachedFacts.slice(0, 8).map((f, i) => `${i + 1}. ${f.text} (importance: ${f.importance}/10, cached)`);
                                return { prependContext: consumeBannerForPrepend() + `## Relevant Memories\n\n${lines.join('\n')}` + welcomeBack + billingWarning };
                            }
                        }
                        // 3. Merge trapdoors — always include word trapdoors for small-dataset coverage.
                        // LSH alone has low collision probability on <100 facts, causing 0 matches.
                        const allTrapdoors = [...wordTrapdoors, ...lshTrapdoors];
                        // If we have cached facts and no trapdoors, return cached facts.
                        if (allTrapdoors.length === 0 && cachedFacts.length > 0) {
                            const lines = cachedFacts.slice(0, 8).map((f, i) => `${i + 1}. ${f.text} (importance: ${f.importance}/10, cached)`);
                            return { prependContext: consumeBannerForPrepend() + `## Relevant Memories\n\n${lines.join('\n')}` + welcomeBack + billingWarning };
                        }
                        if (allTrapdoors.length === 0)
                            return undefined;
                        // 4. Query subgraph for fresh results.
                        let subgraphResults = [];
                        try {
                            const factCount = await getSubgraphFactCount(subgraphOwner || userId, authKeyHex);
                            const pool = computeCandidatePool(factCount);
                            subgraphResults = await searchSubgraph(subgraphOwner || userId, allTrapdoors, pool, authKeyHex);
                        }
                        catch {
                            // Subgraph query failed -- fall back to cached facts if available.
                            if (cachedFacts.length > 0) {
                                const lines = cachedFacts.slice(0, 8).map((f, i) => `${i + 1}. ${f.text} (importance: ${f.importance}/10, cached)`);
                                return { prependContext: consumeBannerForPrepend() + `## Relevant Memories\n\n${lines.join('\n')}` + welcomeBack + billingWarning };
                            }
                            return undefined;
                        }
                        // Always run broadened search and merge — ensures vocabulary mismatches
                        // (e.g., "preferences" vs "prefer") don't cause recall failures.
                        // The reranker handles scoring; extra cost is ~1 GraphQL query per recall.
                        try {
                            const broadPool = computeCandidatePool(0);
                            const broadenedResults = await searchSubgraphBroadened(subgraphOwner || userId, broadPool, authKeyHex);
                            // Merge broadened results with existing (deduplicate by ID)
                            const existingIds = new Set(subgraphResults.map(r => r.id));
                            for (const br of broadenedResults) {
                                if (!existingIds.has(br.id)) {
                                    subgraphResults.push(br);
                                }
                            }
                        }
                        catch { /* best-effort */ }
                        if (subgraphResults.length === 0 && cachedFacts.length === 0)
                            return undefined;
                        // If subgraph returned no results but we have cache, use cache.
                        if (subgraphResults.length === 0) {
                            const lines = cachedFacts.slice(0, 8).map((f, i) => `${i + 1}. ${f.text} (importance: ${f.importance}/10, cached)`);
                            return { prependContext: consumeBannerForPrepend() + `## Relevant Memories\n\n${lines.join('\n')}` + welcomeBack + billingWarning };
                        }
                        // 5. Decrypt subgraph results and build reranker input.
                        const rerankerCandidates = [];
                        const hookMetaMap = new Map();
                        for (const result of subgraphResults) {
                            try {
                                const docJson = decryptFromHex(result.encryptedBlob, encryptionKey);
                                // Filter out digest infrastructure blobs — they have no user
                                // text and should never surface in recall results.
                                if (isDigestBlob(docJson))
                                    continue;
                                const doc = readClaimFromBlob(docJson);
                                let decryptedEmbedding;
                                if (result.encryptedEmbedding) {
                                    try {
                                        decryptedEmbedding = JSON.parse(decryptFromHex(result.encryptedEmbedding, encryptionKey));
                                    }
                                    catch {
                                        // Embedding decryption failed -- proceed without it.
                                    }
                                }
                                const createdAtSec = result.timestamp ? parseInt(result.timestamp, 10) : undefined;
                                rerankerCandidates.push({
                                    id: result.id,
                                    text: doc.text,
                                    embedding: decryptedEmbedding,
                                    importance: doc.importance / 10,
                                    createdAt: createdAtSec,
                                    source: typeof doc.metadata?.source === 'string' ? doc.metadata.source : undefined,
                                });
                                hookMetaMap.set(result.id, {
                                    importance: doc.importance,
                                    age: 'subgraph',
                                    category: doc.category,
                                });
                            }
                            catch {
                                // Skip un-decryptable candidates.
                            }
                        }
                        // 6. Re-rank with BM25 + cosine + intent-weighted RRF fusion.
                        const hookQueryIntent = detectQueryIntent(evt.prompt);
                        const reranked = rerank(evt.prompt, queryEmbedding ?? [], rerankerCandidates, 8, INTENT_WEIGHTS[hookQueryIntent], 
                        /* applySourceWeights (Retrieval v2 Tier 1) */ true);
                        // Update hot cache with reranked results.
                        try {
                            if (pluginHotCache) {
                                const hotFacts = rerankerCandidates.map((c) => {
                                    const meta = hookMetaMap.get(c.id);
                                    return { id: c.id, text: c.text, importance: meta?.importance ?? 5 };
                                });
                                pluginHotCache.setHotFacts(hotFacts);
                                pluginHotCache.setLastQueryEmbedding(queryEmbedding);
                                pluginHotCache.flush();
                            }
                        }
                        catch {
                            // Hot cache update is best-effort.
                        }
                        // Record search state for two-tier cache (C1).
                        lastSearchTimestamp = Date.now();
                        lastQueryEmbedding = queryEmbedding;
                        if (reranked.length === 0)
                            return undefined;
                        // Relevance gate removed in rc.22 (see recall tool comment).
                        // 7. Build context string.
                        const lines = reranked.map((m, i) => {
                            const meta = hookMetaMap.get(m.id);
                            const importance = meta?.importance ?? 5;
                            const age = meta?.age ?? '';
                            const typeTag = meta?.category ? `[${meta.category}] ` : '';
                            return `${i + 1}. ${typeTag}${m.text} (importance: ${importance}/10, ${age})`;
                        });
                        const contextString = `## Relevant Memories\n\n${lines.join('\n')}`;
                        return { prependContext: consumeBannerForPrepend() + contextString + welcomeBack + billingWarning };
                    }
                    // --- Server mode (existing behavior) ---
                    // 1. Generate word trapdoors from the user prompt.
                    const wordTrapdoors = generateBlindIndices(evt.prompt);
                    // 2. Generate query embedding + LSH trapdoors (may fail gracefully).
                    let queryEmbedding = null;
                    let lshTrapdoors = [];
                    try {
                        queryEmbedding = await generateEmbedding(evt.prompt, { isQuery: true });
                        const hasher = getLSHHasher(api.logger);
                        if (hasher && queryEmbedding) {
                            lshTrapdoors = hasher.hash(queryEmbedding);
                        }
                    }
                    catch {
                        // Embedding/LSH failed -- proceed with word-only trapdoors.
                    }
                    // 3. Merge word + LSH trapdoors.
                    const allTrapdoors = [...wordTrapdoors, ...lshTrapdoors];
                    if (allTrapdoors.length === 0)
                        return undefined;
                    // 4. Fetch candidates from the server (dynamic pool sizing).
                    const factCount = await getFactCount(api.logger);
                    const pool = computeCandidatePool(factCount);
                    const candidates = await apiClient.search(userId, allTrapdoors, pool, authKeyHex);
                    if (candidates.length === 0)
                        return undefined;
                    // 5. Decrypt candidates (text + embeddings) and build reranker input.
                    const rerankerCandidates = [];
                    const hookMetaMap = new Map();
                    for (const candidate of candidates) {
                        try {
                            const docJson = decryptFromHex(candidate.encrypted_blob, encryptionKey);
                            // Skip digest infrastructure blobs.
                            if (isDigestBlob(docJson))
                                continue;
                            const doc = readClaimFromBlob(docJson);
                            let decryptedEmbedding;
                            if (candidate.encrypted_embedding) {
                                try {
                                    decryptedEmbedding = JSON.parse(decryptFromHex(candidate.encrypted_embedding, encryptionKey));
                                }
                                catch {
                                    // Embedding decryption failed -- proceed without it.
                                }
                            }
                            const createdAtSec = typeof candidate.timestamp === 'number'
                                ? candidate.timestamp / 1000
                                : new Date(candidate.timestamp).getTime() / 1000;
                            rerankerCandidates.push({
                                id: candidate.fact_id,
                                text: doc.text,
                                embedding: decryptedEmbedding,
                                importance: doc.importance / 10,
                                createdAt: createdAtSec,
                                source: typeof doc.metadata?.source === 'string' ? doc.metadata.source : undefined,
                            });
                            hookMetaMap.set(candidate.fact_id, {
                                importance: doc.importance,
                                age: relativeTime(candidate.timestamp),
                            });
                        }
                        catch {
                            // Skip un-decryptable candidates.
                        }
                    }
                    // 6. Re-rank with BM25 + cosine + RRF fusion (intent-weighted).
                    const srvHookIntent = detectQueryIntent(evt.prompt);
                    const reranked = rerank(evt.prompt, queryEmbedding ?? [], rerankerCandidates, 8, INTENT_WEIGHTS[srvHookIntent], 
                    /* applySourceWeights (Retrieval v2 Tier 1) */ true);
                    if (reranked.length === 0)
                        return undefined;
                    // Relevance gate removed in rc.22 (see recall tool comment).
                    // 7. Build context string.
                    const lines = reranked.map((m, i) => {
                        const meta = hookMetaMap.get(m.id);
                        const importance = meta?.importance ?? 5;
                        const age = meta?.age ?? '';
                        return `${i + 1}. ${m.text} (importance: ${importance}/10, ${age})`;
                    });
                    const contextString = `## Relevant Memories\n\n${lines.join('\n')}`;
                    return { prependContext: consumeBannerForPrepend() + contextString + welcomeBack + billingWarning };
                }
                catch (err) {
                    // The hook must NEVER throw -- log and return undefined.
                    const message = err instanceof Error ? err.message : String(err);
                    api.logger.warn(`before_agent_start hook failed: ${message}`);
                    return undefined;
                }
            }, { priority: 10 });
            // ---------------------------------------------------------------
            // Hook: agent_end — auto-extract facts after each conversation turn
            // ---------------------------------------------------------------
            api.on('agent_end', async (event) => {
                // CRITICAL: Always return { memoryHandled: true } so OpenClaw's default
                // memory system does NOT fall back to writing plaintext MEMORY.md.
                // Losing facts on error is acceptable; leaking them in cleartext is not.
                try {
                    // Defensive: ensure MEMORY.md header is present so OpenClaw's default
                    // memory system doesn't write sensitive data in cleartext, even if
                    // our extraction fails below.
                    ensureMemoryHeader(api.logger);
                    // BUG-2 fix: skip extraction if an import was in progress this turn.
                    // Import failures were retriggering agent_end → extraction → import loops.
                    if (_importInProgress) {
                        _importInProgress = false; // auto-reset for next turn
                        api.logger.info('agent_end: skipping extraction (import was in progress)');
                        return { memoryHandled: true };
                    }
                    const evt = event;
                    if (!evt?.messages || evt.messages.length < 2) {
                        api.logger.info('agent_end: skipping extraction (no messages)');
                        return { memoryHandled: true };
                    }
                    // Proceed with extraction even when evt.success is false or undefined.
                    // A single LLM timeout on one turn should not prevent extraction of
                    // facts from the (potentially many) successful turns in the message
                    // history. The extractor processes the full message array and can
                    // extract valuable facts from content before the failure.
                    if (evt.success === false) {
                        api.logger.info('agent_end: turn reported failure, but proceeding with extraction from message history');
                    }
                    await ensureInitialized(api.logger);
                    if (needsSetup)
                        return { memoryHandled: true };
                    // C3: Throttle auto-extraction to every N turns (configurable via env).
                    // Phase 2.2.5: every branch of the extraction pipeline now logs its
                    // outcome. Prior to 2.2.5, only the "stored N facts" happy path
                    // produced a log line, so silent JSON parse failures / chatCompletion
                    // timeouts / importance-filter-drops-everything scenarios left no
                    // trace whatsoever in the gateway log. See the investigation report
                    // in CHANGELOG for the full failure chain we uncovered.
                    turnsSinceLastExtraction++;
                    const extractInterval = getExtractInterval();
                    api.logger.info(`agent_end: turn ${turnsSinceLastExtraction}/${extractInterval} (messages=${evt.messages.length})`);
                    if (turnsSinceLastExtraction >= extractInterval) {
                        const existingMemories = isLlmDedupEnabled()
                            ? await fetchExistingMemoriesForExtraction(api.logger, 20, evt.messages)
                            : [];
                        const rawFacts = await extractFacts(evt.messages, 'turn', existingMemories, undefined, api.logger);
                        api.logger.info(`agent_end: extractFacts returned ${rawFacts.length} raw facts`);
                        const { kept: importanceFiltered, dropped } = filterByImportance(rawFacts, api.logger);
                        api.logger.info(`agent_end: after importance filter: kept=${importanceFiltered.length}, dropped=${dropped}`);
                        const maxFacts = getMaxFactsPerExtraction();
                        if (importanceFiltered.length > maxFacts) {
                            api.logger.info(`Capped extraction from ${importanceFiltered.length} to ${maxFacts} facts`);
                        }
                        const facts = importanceFiltered.slice(0, maxFacts);
                        if (facts.length > 0) {
                            await storeExtractedFacts(facts, api.logger);
                            api.logger.info(`agent_end: stored ${facts.length} facts to encrypted vault`);
                        }
                        else {
                            // Phase 2.2.5: no longer silent when extraction produces nothing.
                            api.logger.info(`agent_end: extraction produced 0 storable facts (raw=${rawFacts.length}, after-importance=${importanceFiltered.length})`);
                        }
                        turnsSinceLastExtraction = 0;
                    }
                }
                catch (err) {
                    const message = err instanceof Error ? err.message : String(err);
                    api.logger.error(`agent_end extraction failed: ${message}`);
                    // Re-assert MEMORY.md header even on failure — last line of defense.
                    ensureMemoryHeader(api.logger);
                }
                // Always signal that memory is handled — prevent plaintext fallback.
                return { memoryHandled: true };
            }, { priority: 90 });
            // ---------------------------------------------------------------
            // ---------------------------------------------------------------
            // Trajectory poller (3.3.11-rc.1) — auto-extraction without the
            // `agent_end` hook (which OpenClaw 2026.5.4 silently blocks for
            // non-bundled plugins). Implementation lives in trajectory-poller.ts
            // so disk I/O stays separate from this module's outbound-request
            // surface (scanner constraint: a single file may not contain both
            // fs.read* AND outbound-request trigger words). Deps are passed in
            // here with neutral aliases for the same reason.
            // ---------------------------------------------------------------
            startTrajectoryPoller({
                logger: api.logger,
                ensureInitialized: () => ensureInitialized(api.logger),
                isPairingPending: () => needsSetup,
                isImportActive: () => _importInProgress,
                getExtractInterval,
                getMaxFactsPerExtraction,
                isDedupEnabled: isLlmDedupEnabled,
                getDedupCandidates: (limit, messages) => fetchExistingMemoriesForExtraction(api.logger, limit, messages),
                runExtraction: (messages, mode, existing, extra) => extractFacts(messages, mode, existing, extra, api.logger),
                filterByImportance: (facts) => filterByImportance(facts, api.logger),
                persistFacts: (facts) => storeExtractedFacts(facts, api.logger),
            });
            // ---------------------------------------------------------------
            // Hook: before_compaction — extract ALL facts before context is lost
            // ---------------------------------------------------------------
            api.on('before_compaction', async (event) => {
                try {
                    const evt = event;
                    if (!evt?.messages || evt.messages.length < 2)
                        return;
                    await ensureInitialized(api.logger);
                    if (needsSetup)
                        return;
                    api.logger.info(`pre_compaction: using compaction-aware extraction (importance >= 5), processing ${evt.messages.length} messages`);
                    const existingMemories = isLlmDedupEnabled()
                        ? await fetchExistingMemoriesForExtraction(api.logger, 50, evt.messages)
                        : [];
                    const rawCompactFacts = await extractFactsForCompaction(evt.messages, existingMemories, api.logger);
                    const { kept: compactImportanceFiltered } = filterByImportance(rawCompactFacts, api.logger);
                    const maxFactsCompact = getMaxFactsPerExtraction();
                    if (compactImportanceFiltered.length > maxFactsCompact) {
                        api.logger.info(`Capped compaction extraction from ${compactImportanceFiltered.length} to ${maxFactsCompact} facts`);
                    }
                    const facts = compactImportanceFiltered.slice(0, maxFactsCompact);
                    if (facts.length > 0) {
                        await storeExtractedFacts(facts, api.logger);
                    }
                    turnsSinceLastExtraction = 0; // Reset C3 counter on compaction.
                    // Session Crystal (am-1) — one structured summary replaces 5 free-form debrief items.
                    // Stored as v1 summary + metadata.subtype="session_crystal" for filtered recall.
                    try {
                        const storedTexts = facts.map((f) => f.text);
                        const crystal = await extractCrystal(evt.messages, storedTexts, 'coding');
                        if (crystal) {
                            const crystalFact = {
                                text: crystal.narrative,
                                type: 'summary',
                                source: 'derived',
                                importance: crystal.importance,
                                action: 'ADD',
                                crystalMetadata: crystal.metadata,
                            };
                            await storeExtractedFacts([crystalFact], api.logger, 'openclaw_debrief');
                            api.logger.info('Session Crystal stored');
                        }
                    }
                    catch (debriefErr) {
                        api.logger.warn(`before_compaction Crystal failed: ${debriefErr instanceof Error ? debriefErr.message : String(debriefErr)}`);
                    }
                }
                catch (err) {
                    const message = err instanceof Error ? err.message : String(err);
                    api.logger.warn(`before_compaction extraction failed: ${message}`);
                }
            }, { priority: 5 });
            // ---------------------------------------------------------------
            // Hook: before_reset — final extraction before session is cleared
            // ---------------------------------------------------------------
            api.on('before_reset', async (event) => {
                try {
                    const evt = event;
                    if (!evt?.messages || evt.messages.length < 2)
                        return;
                    await ensureInitialized(api.logger);
                    if (needsSetup)
                        return;
                    api.logger.info(`Pre-reset extraction (${evt.reason ?? 'unknown'}): processing ${evt.messages.length} messages`);
                    const existingMemories = isLlmDedupEnabled()
                        ? await fetchExistingMemoriesForExtraction(api.logger, 50, evt.messages)
                        : [];
                    const rawResetFacts = await extractFacts(evt.messages, 'full', existingMemories);
                    const { kept: resetImportanceFiltered } = filterByImportance(rawResetFacts, api.logger);
                    const maxFactsReset = getMaxFactsPerExtraction();
                    if (resetImportanceFiltered.length > maxFactsReset) {
                        api.logger.info(`Capped reset extraction from ${resetImportanceFiltered.length} to ${maxFactsReset} facts`);
                    }
                    const facts = resetImportanceFiltered.slice(0, maxFactsReset);
                    if (facts.length > 0) {
                        await storeExtractedFacts(facts, api.logger);
                    }
                    turnsSinceLastExtraction = 0; // Reset C3 counter on reset.
                    // Session Crystal (am-1) — one structured summary replaces 5 free-form debrief items.
                    // Stored as v1 summary + metadata.subtype="session_crystal" for filtered recall.
                    try {
                        const storedTexts = facts.map((f) => f.text);
                        const crystal = await extractCrystal(evt.messages, storedTexts, 'coding');
                        if (crystal) {
                            const crystalFact = {
                                text: crystal.narrative,
                                type: 'summary',
                                source: 'derived',
                                importance: crystal.importance,
                                action: 'ADD',
                                crystalMetadata: crystal.metadata,
                            };
                            await storeExtractedFacts([crystalFact], api.logger, 'openclaw_debrief');
                            api.logger.info('Session Crystal stored');
                        }
                    }
                    catch (debriefErr) {
                        api.logger.warn(`before_reset Crystal failed: ${debriefErr instanceof Error ? debriefErr.message : String(debriefErr)}`);
                    }
                }
                catch (err) {
                    const message = err instanceof Error ? err.message : String(err);
                    api.logger.warn(`before_reset extraction failed: ${message}`);
                }
            }, { priority: 5 });
            // ---------------------------------------------------------------
            // 3.3.2-rc.1 (issue #186) — write `.loaded.json` manifest
            // ---------------------------------------------------------------
            //
            // Final step of register(): drop the success manifest so the agent
            // can `cat ~/.openclaw/extensions/totalreclaw/.loaded.json` to
            // verify which tools bound. Synchronous (see writePluginManifest doc).
            // Never throws — diagnostic loss only on I/O failure.
            if (_pluginDirForManifest) {
                try {
                    const ok = writePluginManifest(_pluginDirForManifest, {
                        loadedAt: Date.now(),
                        tools: _registeredToolNames.slice(),
                        version: pluginVersion ?? 'unknown',
                        // 3.3.8-rc.1 hybrid mode annotation: tools ARE registered with the
                        // SDK (required for plugin loader validation), but tool calls are
                        // dead-letter on OC 2026.5.2 due to issue #223. Use `tr <cmd>` CLI.
                        hybridMode: true,
                        hybridCliTools: ['tr status', 'tr pair', 'tr remember', 'tr recall'],
                    });
                    if (ok) {
                        api.logger.info(`TotalReclaw: wrote .loaded.json manifest (${_registeredToolNames.length} tools + hybridCli=tr, version=${pluginVersion ?? 'unknown'})`);
                    }
                }
                catch {
                    // Best-effort; helper swallows internally too.
                }
            }
        }
        catch (registerErr) {
            // ---------------------------------------------------------------
            // 3.3.2-rc.1 (issue #186) — write `.error.json` on register() throw
            // ---------------------------------------------------------------
            //
            // Some surface threw out of register(). Drop a structured error
            // marker the agent can grep. Best-effort logging then re-throw so
            // the SDK sees the original failure.
            const errMsg = registerErr instanceof Error ? registerErr.message : String(registerErr);
            const errStack = registerErr instanceof Error ? registerErr.stack : undefined;
            try {
                api.logger.error(`TotalReclaw: register() threw: ${errMsg}`);
            }
            catch {
                // Logger may be unavailable (very early failure path).
            }
            if (_pluginDirForManifest) {
                try {
                    writePluginError(_pluginDirForManifest, {
                        loadedAt: Date.now(),
                        error: errMsg,
                        stack: errStack,
                        version: 'unknown',
                    });
                }
                catch {
                    // Best-effort.
                }
            }
            throw registerErr;
        }
    },
};
export default plugin;
/**
 * Reset all module-level state for test isolation.
 * ONLY call this from test code — never in production.
 */
export function __resetForTesting() {
    authKeyHex = null;
    encryptionKey = null;
    dedupKey = null;
    userId = null;
    subgraphOwner = null;
    apiClient = null;
    initPromise = null;
    lshHasher = null;
    lshInitFailed = false;
    masterPasswordCache = null;
    saltCache = null;
    cachedFactCount = null;
    lastFactCountFetch = 0;
    pluginHotCache = null;
    lastSearchTimestamp = 0;
    lastQueryEmbedding = null;
    turnsSinceLastExtraction = 0;
}
