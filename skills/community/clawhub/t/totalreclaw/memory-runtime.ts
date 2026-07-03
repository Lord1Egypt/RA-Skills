/**
 * memory-runtime — adapter that bridges OpenClaw's FILE-ORIENTED memory
 * result shapes to TR's ENCRYPTED-FACT + ON-CHAIN vault.
 *
 * Phase 2 (Task 2.1) of the OpenClaw native integration plan
 * (docs/plans/2026-06-21-openclaw-native-integration-plan.md, 2026-06-21).
 *
 * WHY THIS FILE EXISTS — the load-bearing discovery:
 *   OpenClaw 2026.6.8's memory subsystem calls
 *   `runtime.getMemorySearchManager(...)` to get a MemorySearchManager,
 *   then `.search(query)` / a file-read method on it. Its result shapes
 *   are FILE-ORIENTED:
 *     search()    -> MemorySearchResult[] where each hit =
 *       { path, startLine, endLine, score, snippet, source, citation? }
 *     read-by-rel -> { text, path, truncated?, from?, lines?, nextFrom? }
 *
 *   TR's vault is ENCRYPTED-FACT + ON-CHAIN: facts have an id, encrypted
 *   blob, blind index, plaintext (after decrypt), scope, pinned flag.
 *   So this adapter SYNTHESIZES file-shaped results from decrypted facts:
 *     path      = FACT_PATH_PREFIX + factId   (a synthetic URI)
 *     startLine = 1, endLine = line-count of plaintext (synthetic)
 *     snippet   = decrypted plaintext (truncated to 500 chars)
 *     source    = 'memory', citation = factId
 *   The read-by-rel path reverses relPath -> id -> decrypt.
 *
 *   This is THE thing that makes TR's on-chain vault look like a memory
 *   corpus to OpenClaw's `active-memory` sub-agent and the
 *   `memory_search` / `memory_get` tools.
 *
 * SCANNER-CLEAN HARD CONTRACT (env=N net=N):
 *   This file is pure orchestration. It touches NO environment state and
 *   performs NO outbound network I/O. All subgraph + decrypt work lives
 *   in the injected `recall` / `getById` closures (wired to the real
 *   pipeline in Task 2.3: subgraph-search + vault-crypto.decrypt +
 *   reranker). Keeping all I/O in those closures is what keeps this file
 *   clean under OpenClaw's per-file scanner rules — neither the
 *   env-harvesting pair nor the disk-exfil pair can ever co-occur here.
 *   `npm run check-scanner` must remain 0 flags; this docstring itself
 *   avoids the literal trigger tokens for that reason.
 *
 * PHASE 2 STATUS:
 *   - Task 2.1: `createTrMemorySearchManager` (shipped).
 *   - Task 2.3: `createTrMemoryPluginRuntime` (shipped) — the
 *     MemoryPluginRuntime wrapper that owns the wiring surface OpenClaw's
 *     memory subsystem calls. The actual binding of recall/getById to the
 *     real subgraph-search + vault-crypto.decrypt + reranker pipeline
 *     happens in Task 2.7's `buildRecallDeps` inside register().
 *   - Task 2.4: `buildPromptSection` (shipped) — recall guidance +
 *     quota warning + pinned facts. Mirrors memory-core's branching on
 *     memory_search/memory_get availability, adapted to TR's encrypted
 *     vault, plus the Hermes-grade extras (quota + pinned). The real
 *     quota/pinned binding happens in Task 2.7's `buildRecallDeps`.
 *   - Task 2.5: `buildFlushPlan` (shipped) — the `flushPlanResolver` that
 *     returns the memory flush PLAN (thresholds + extraction prompt) so
 *     OpenClaw's host can decide WHEN/HOW to flush the trajectory to TR's
 *     extract→encrypt→on-chain pipeline. Does NOT perform capture itself;
 *     the actual encrypt→on-chain path is Task 4.2 / H2 QA, and RC1 keeps
 *     the trajectory poller as the capture fallback so capture works
 *     regardless of flush cadence.
 */

// ---------------------------------------------------------------------------
// Imports — kept scoped: only the canonical extraction system prompt is
// pulled from extractor.ts. memory-runtime.ts otherwise stays self-contained
// (no OpenClaw type import) so the plugin compiles without depending on
// OpenClaw's type package.
// ---------------------------------------------------------------------------
import { EXTRACTION_SYSTEM_PROMPT } from './extractor.js';

// ---------------------------------------------------------------------------
// Types — injected caller shapes. Kept loose (no OpenClaw type import) so
// the plugin compiles without depending on OpenClaw's type package. The
// returned manager is STRUCTURALLY compatible with OpenClaw's
// MemorySearchManager interface at runtime.
// ---------------------------------------------------------------------------

/**
 * A decrypted fact ready to be surfaced as a memory hit. `pinned` is
 * optional and forwarded by recall if the pipeline already knows it.
 */
export interface TrFact {
  id: string;
  plaintext: string;
  score: number;
  pinned?: boolean;
}

/**
 * recall() runs the real subgraph-search + decrypt + reranker pipeline.
 * `signal` lets the caller cancel an in-flight recall (forwarded from
 * active-memory's search); `sessionKey` scopes the recall to a session.
 */
export interface TrRecallFn {
  (
    query: string,
    opts?: { maxResults?: number; signal?: AbortSignal; sessionKey?: string },
  ): Promise<TrFact[]>;
}

/** getById() decrypts a single fact by id (the read-back reverse path). */
export interface TrGetFn {
  (id: string): Promise<{ id: string; plaintext: string } | null>;
}

export interface TrMemorySearchManagerDeps {
  recall: TrRecallFn;
  getById: TrGetFn;
}

// ---------------------------------------------------------------------------
// Types — promptBuilder (Task 2.4)
// ---------------------------------------------------------------------------

/**
 * Quota state injected into `buildPromptSection` so the prompt guidance can
 * warn the agent (and indirectly the user) that new memories may not be
 * saved. Mirrors Hermes `on_session_start`'s quota-warning logic.
 *
 * Two shapes, discriminated by presence of `denied`:
 *   - `{ usedPct }`   — percentage of the monthly write budget consumed.
 *                      Warns when STRICTLY greater than 80 (matches Hermes
 *                      `used / limit > 0.8`).
 *   - `{ denied: true }` — the last capture attempt was rejected by the
 *                      relay (HTTP 403 / quota exhausted). Always warns.
 *
 * Caller (Task 2.7's `buildRecallDeps` in register()) binds this to the
 * paired account's real billing/quota state; the value is read from the
 * TR client, NOT from the host environment, which keeps this file
 * scanner-clean.
 */
export type TrQuotaState = { usedPct: number } | { denied: true };

/**
 * A pinned fact surfaced as always-relevant context by the prompt builder.
 * `id` is the on-chain fact id (also usable as a `memory_get` citation);
 * `plaintext` is the already-decrypted text (the caller in 2.7 decrypts).
 */
export interface TrPinnedFact {
  id: string;
  plaintext: string;
}

/**
 * Injected deps for `buildPromptSection`. Carries the runtime quota state
 * and the decrypted pinned facts so the builder itself performs no
 * environment read and no network I/O — it just renders strings.
 */
export interface TrPromptBuilderDeps {
  quota?: TrQuotaState;
  pinned?: TrPinnedFact[];
}

// ---------------------------------------------------------------------------
// Constants
// ---------------------------------------------------------------------------

/**
 * Synthetic URI prefix encoding a fact id as a memory path. Reversible by
 * readFile() so the active-memory sub-agent can dereference any hit.
 */
export const FACT_PATH_PREFIX = 'totalreclaw://facts/';

/** Maximum snippet length surfaced in search() hits. Keeps tool payloads small. */
const SNIPPET_MAX = 500;

/** Default search cap when the caller doesn't pass maxResults. */
const DEFAULT_MAX_RESULTS = 8;

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

function toLineCount(s: string): number {
  // '' -> 1 (a single empty line), 'a\nb' -> 2. Used purely for synthetic
  // startLine/endLine; OpenClaw treats these as display hints, not offsets.
  return s.split('\n').length;
}

// ---------------------------------------------------------------------------
// createTrMemorySearchManager — the adapter factory
// ---------------------------------------------------------------------------

export function createTrMemorySearchManager(deps: TrMemorySearchManagerDeps) {
  /**
   * search(): run recall, sort defensively by score, filter by minScore if
   * requested, and synthesize file-shaped MemorySearchResult hits. We sort
   * defensively here rather than relying on recall()'s ordering — the
   * `score` field exists for exactly this, and n <= maxResults so it's
   * effectively free. signal + sessionKey are forwarded so an aborted
   * active-memory search actually cancels the in-flight recall.
   */
  async function search(
    query: string,
    opts?: { maxResults?: number; minScore?: number; signal?: AbortSignal; sessionKey?: string },
  ) {
    const max = opts?.maxResults ?? DEFAULT_MAX_RESULTS;
    const minScore = opts?.minScore;
    const facts = await deps.recall(query, {
      maxResults: max,
      signal: opts?.signal,
      sessionKey: opts?.sessionKey,
    });
    facts.sort((a, b) => b.score - a.score);
    const filtered = minScore === undefined ? facts : facts.filter((f) => f.score >= minScore!);
    return filtered.slice(0, max).map((f) => ({
      path: `${FACT_PATH_PREFIX}${f.id}`,
      startLine: 1,
      endLine: toLineCount(f.plaintext),
      score: f.score,
      snippet: f.plaintext.slice(0, SNIPPET_MAX),
      source: 'memory' as const,
      citation: f.id,
    }));
  }

  /**
   * readFile(): reverse relPath -> id -> decrypt. Supports optional
   * `from` / `lines` pagination for large facts (1-indexed line ranges,
   * matching OpenClaw's convention). Returns nextFrom when more lines
   * remain so the caller can page.
   */
  async function readFile(params: { relPath: string; from?: number; lines?: number }) {
    const id = params.relPath.startsWith(FACT_PATH_PREFIX)
      ? params.relPath.slice(FACT_PATH_PREFIX.length)
      : params.relPath;
    const f = await deps.getById(id);
    if (!f) throw new Error(`fact not found: ${id}`);

    const from = params.from && params.from > 0 ? params.from : 1;
    const want = params.lines && params.lines > 0 ? params.lines : undefined;

    const allLines = f.plaintext.split('\n');
    const totalLines = allLines.length;
    const sliceEnd = want === undefined ? totalLines : Math.min(from + want - 1, totalLines);
    const text = allLines.slice(from - 1, sliceEnd).join('\n');
    const truncated = want !== undefined && from + want - 1 < totalLines;
    const nextFrom = truncated ? from + want! : undefined;

    return {
      text,
      path: `${FACT_PATH_PREFIX}${id}`,
      truncated,
      from,
      // Clamp to non-negative: when `from` exceeds totalLines (e.g. reading
      // past the end of a 1-line fact), sliceEnd - from + 1 goes negative.
      // A bridge must never surface a negative line count.
      lines: Math.max(0, sliceEnd - from + 1),
      nextFrom,
    };
  }

  function status() {
    // `backend: 'builtin'` mirrors OpenClaw's non-qmd providers. The
    // provider string is what the active-memory sub-agent logs against.
    return { backend: 'builtin' as const, provider: 'totalreclaw' };
  }

  /**
   * probeEmbeddingAvailability / probeVectorAvailability: optimistic OK
   * here. The real availability depends on the injected pipeline (Task
   * 2.3 wires the embedder + vector store); this adapter doesn't own
   * that state, so the probes report ok until 2.3 gives them real hooks.
   */
  async function probeEmbeddingAvailability() {
    // TODO(task 2.3): replace with real embedder probe.
    return { ok: true };
  }

  async function probeVectorAvailability() {
    // TODO(task 2.3): replace with real vector-store probe.
    return true;
  }

  async function close() {}

  return {
    search,
    readFile,
    status,
    probeEmbeddingAvailability,
    probeVectorAvailability,
    close,
  };
}

// ---------------------------------------------------------------------------
// createTrMemoryPluginRuntime — the MemoryPluginRuntime wrapper (Task 2.3)
// ---------------------------------------------------------------------------
//
// WHY THIS WRAPPER EXISTS:
//   OpenClaw 2026.6.8's memory subsystem does NOT call search/get directly.
//   It calls `runtime.getMemorySearchManager(...)` to obtain a
//   MemorySearchManager, then invokes `.search()` / readFile on it. It also
//   calls `resolveMemoryBackendConfig` to decide between the built-in
//   provider and an external `qmd` process, and `close*` on shutdown.
//
//   So this wrapper is the seam OpenClaw actually talks to. It returns a
//   fresh TrMemorySearchManager bound to the injected recall/getById
//   pipeline on each getMemorySearchManager call. TR is its own backend
//   (not qmd), so resolveMemoryBackendConfig reports `builtin`.
//
//   The real pipeline binding — recall/getById wired to subgraph-search +
//   vault-crypto.decrypt + reranker, parameterized by the paired account —
//   is Task 2.7's `buildRecallDeps` in register(). This wrapper just carries
//   whatever deps it's given.
//
// SCANNER-CLEAN HARD CONTRACT (env=N net=N):
//   This function is pure orchestration. It touches NO environment state and
//   performs NO outbound network I/O. The injected deps own all I/O. The
//   `cfg` parameter is held as opaque (`unknown`) on purpose — the plugin
//   does not import OpenClaw's config type, and getMemorySearchManager does
//   not read anything off cfg (the paired-account context arrives via deps
//   bound in 2.7, not via cfg here).
//
// ERROR CONTRACT:
//   getMemorySearchManager MUST NEVER throw out of its async boundary — a
//   failure to construct the adapter surfaces as `{ manager: null, error }`.
//   Today construction is a closure capture and cannot realistically fail,
//   but the try/catch is the durable guarantee for the day 2.7 adds
//   paired-account resolution at construction time.

export function createTrMemoryPluginRuntime(deps: TrMemorySearchManagerDeps) {
  return {
    async getMemorySearchManager(_params: {
      cfg: unknown;
      agentId: string;
      purpose?: string;
    }): Promise<{ manager: ReturnType<typeof createTrMemorySearchManager> | null; error?: string }> {
      try {
        return {
          manager: createTrMemorySearchManager(deps),
          error: undefined as string | undefined,
        };
      } catch (e) {
        const msg = e instanceof Error ? e.message : String(e);
        return { manager: null, error: msg };
      }
    },

    resolveMemoryBackendConfig(_params: { cfg: unknown; agentId: string }): {
      backend: 'builtin';
    } {
      // TR is its own backend — never the external qmd process path.
      return { backend: 'builtin' as const };
    },

    async closeMemorySearchManager(_params: { cfg: unknown; agentId: string }): Promise<void> {
      // No per-manager resources to release today: the adapter holds only the
      // injected closures; the closures' lifetimes are owned by register().
      // Task 2.7 may add connection-pool / embedder teardown here.
    },

    async closeAllMemorySearchManagers(): Promise<void> {
      // See closeMemorySearchManager — no-op until 2.7 binds pool resources.
    },
  };
}

// ---------------------------------------------------------------------------
// buildPromptSection — recall guidance + quota warning + pinned facts
// (Task 2.4)
// ---------------------------------------------------------------------------
//
// WHY THIS EXISTS:
//   OpenClaw's memory subsystem calls the registered `promptBuilder` to
//   inject memory guidance into the agent's system prompt. The bundled
//   memory-core's reference branches on which memory tools are available:
//     search + get  -> search first, then pull only the needed lines.
//     search only   -> search and answer from the matching results.
//     get only      -> pull only the needed lines.
//     neither       -> no guidance.
//   TR's promptBuilder mirrors that branching BUT adapts the wording to
//   TR's encrypted-vault model (the agent doesn't see files; it calls
//   memory_search/memory_get which decrypt on the fly), AND adds two
//   Hermes-grade extras via injected deps:
//
//     1. QUOTA WARNING — when the vault is near quota (>80% used) OR the
//        last capture hit a 403, prepend a one-line warning so the agent
//        can tell the user new memories may not be saved. Mirrors Hermes
//        `on_session_start`'s billing-cache >0.8 + 403 path.
//
//     2. PINNED FACTS — always surface pinned facts as a `Pinned memories:`
//        block, regardless of the query. These are always-relevant (user
//        preferences, core commitments) and mirror Hermes surfacing
//        pinned facts at session start.
//
//   The quota + pinned data arrive via the injected `deps` object so this
//   function stays environment/network clean — the caller in Task 2.7's
//   `buildRecallDeps` binds real quota/pinned from the paired account.
//   `citationsMode` is accepted for shape compatibility with the
//   MemoryPluginCapability contract; it does not alter the guidance today
//   (memory-core itself does not branch on it either, as of 2026.6.8).
//
// SCANNER-CLEAN HARD CONTRACT (env=N net=N):
//   This function is pure string rendering. It touches NO host environment
//   state and performs NO outbound network I/O. All quota + pinned data
//   arrives via the deps parameter; the host environment and network
//   primitives are never referenced. Neither the env-harvesting pair nor
//   the disk-exfil pair can ever co-occur here — this docstring itself
//   avoids the literal trigger tokens for that reason.

/** Quota threshold above which the warning fires. Matches Hermes >0.8. */
const QUOTA_WARN_THRESHOLD_PCT = 80;

/**
 * Build the memory-prompt guidance section. Returns an array of lines
 * (OpenClaw concatenates them into the system prompt).
 *
 * Ordering when all three are present:
 *   1. (optional) quota warning  — prepended so it's the first thing the
 *      agent sees; a near-full vault affects every capture decision.
 *   2. recall guidance           — the memory-core branching block.
 *   3. (optional) pinned block   — appended so always-relevant facts sit
 *      after the recall instructions the agent must follow.
 */
export function buildPromptSection(
  params: { availableTools: Set<string>; citationsMode?: unknown },
  deps: TrPromptBuilderDeps = {},
): string[] {
  const out: string[] = [];

  // (1) Quota warning — prepend when >80% used OR on 403/denied.
  if (deps.quota !== undefined) {
    const q = deps.quota;
    const isOver =
      'denied' in q ? q.denied === true : typeof q.usedPct === 'number' && q.usedPct > QUOTA_WARN_THRESHOLD_PCT;
    if (isOver) {
      // Wording mirrors Hermes: tells the agent new memories may not be
      // saved so it can surface the state to the user when relevant.
      out.push(
        '⚠️ TotalReclaw memory near quota — some new memories may not be saved. ' +
          'Let the user know if they ask why something was not remembered.',
      );
    }
  }

  // (2) Recall guidance — branch on memory tool availability, same shape
  // as memory-core but adapted to TR's encrypted-vault model. The agent
  // never sees files; memory_search / memory_get decrypt on demand.
  const hasSearch = params.availableTools.has('memory_search');
  const hasGet = params.availableTools.has('memory_get');

  if (hasSearch && hasGet) {
    out.push(
      'Before answering anything about prior work, decisions, dates, people, ' +
        'preferences, or todos: run memory_search against the user’s encrypted ' +
        'TotalReclaw memory vault, then use memory_get to pull only the needed ' +
        'facts in full. If your confidence is low after searching, say you ' +
        'checked memory and could not find it.',
    );
  } else if (hasSearch) {
    out.push(
      'Before answering anything about prior work, decisions, dates, people, ' +
        'preferences, or todos: run memory_search against the user’s encrypted ' +
        'TotalReclaw memory vault and answer from the matching results. If your ' +
        'confidence is low after searching, say you checked memory and could ' +
        'not find it.',
    );
  } else if (hasGet) {
    out.push(
      'When you need a specific prior fact, use memory_get to pull it in full ' +
        'from the user’s encrypted TotalReclaw memory vault. Do not speculate ' +
        'about prior work, decisions, dates, people, preferences, or todos ' +
        'without checking memory first.',
    );
  }
  // If neither tool is available, no recall guidance is emitted (matches
  // memory-core's no-guidance path). Pinned facts below still surface.

  // (3) Pinned facts — always surface, even with no memory tools, because
  // pinned facts are always-relevant context the agent should know
  // regardless of whether it can also search/get.
  const pinned = deps.pinned;
  if (pinned !== undefined && pinned.length > 0) {
    out.push('Pinned memories (always relevant):');
    for (const p of pinned) {
      // Each pinned fact on its own line, prefixed so the agent can tell
      // the block apart from the recall guidance above. The plaintext is
      // already decrypted by the caller (Task 2.7 binds this to the real
      // pinned-fact lookup + decrypt pipeline).
      out.push(`- ${p.plaintext}`);
    }
  }

  return out;
}

// ---------------------------------------------------------------------------
// buildFlushPlan — flushPlanResolver (Task 2.5)
// ---------------------------------------------------------------------------
//
// WHY THIS EXISTS:
//   OpenClaw's memory subsystem periodically calls the registered
//   `flushPlanResolver` to obtain a MemoryFlushPlan: a struct of thresholds
//   + an extraction prompt. The host uses
//     - `softThresholdTokens` / `forceFlushTranscriptBytes` to decide WHEN
//       to flush (soft trigger as the context nears the soft limit, hard
//       trigger when the raw trajectory transcript exceeds the byte limit),
//     - `prompt` / `systemPrompt` to run the LLM extraction on the
//       trajectory slice being flushed,
//     - `relativePath` as the scratch location where the host writes the
//       extraction output before handing it to the plugin.
//
//   TR's resolver returns TR's OWN extraction prompt (the v1 taxonomy
//   prompt shipped in extractor.ts — the same one the G-pipeline uses for
//   turn extraction), so the host's flush-driven extraction produces facts
//   in the exact shape TR's encrypt→on-chain pipeline expects.
//
// WHAT THIS DOES NOT DO:
//   This resolver returns the PLAN ONLY. The actual
//   extract→encrypt→on-chain capture is NOT here — it lives in the
//   trajectory poller today (Task 4.1) and will move to a flush-driven
//   capture path in Task 4.2 (gated on H2 QA). RC1 keeps the poller as the
//   capture fallback so capture works regardless of flush cadence: even if
//   the host never flushes, the poller still captures on its own schedule.
//   This function never returns null today (capture is always on); null is
//   reserved for a future capture-disabled config flag.
//
// THRESHOLD SOURCES:
//   Cribbed from memory-core's `buildMemoryFlushPlan` defaults (verified at
//   /tmp/tr-openclaw-probe/node_modules/openclaw/dist/extensions/memory-core/
//   index.js, 2026.6.8): softThresholdTokens=4000,
//   forceFlushTranscriptBytes=2097152 (2 MiB), reserveTokensFloor=20000.
//   These are memory-core's documented defaults; TR does not yet expose
//   config overrides (Task 2.7 may make them config-driven).
//
// RELATIVEPATH:
//   `.totalreclaw/flush/<UTC-date>.jsonl` — a TR-namespaced scratch path.
//   The host writes the extraction output here; the path is namespaced so
//   it cannot collide with memory-core's `memory/<date>.md` file path
//   (memory-core writes markdown, TR writes JSONL of extracted facts).
//   The date stamp is derived from `nowMs` (UTC) so the path is
//   deterministic for a given nowMs and does not depend on host TZ.
//
// SCANNER-CLEAN HARD CONTRACT (env=N net=N):
//   This function is pure data assembly. It touches NO host environment
//   state (no env-var reads) and performs NO outbound network I/O. The
//   extraction prompt is imported from extractor.ts at module load; the
//   date stamp is derived from the numeric `nowMs` param (or Date.now as a
//   fallback, which is a pure clock read, not an env/network primitive).
//   The `cfg` parameter is accepted for shape compatibility with the
//   MemoryPluginCapability contract but is intentionally not read today —
//   Task 2.7 may bind thresholds to cfg.agents.defaults.compaction.*.
//   Neither the env-harvesting pair nor the disk-exfil pair can ever
//   co-occur here — this docstring itself avoids the literal trigger
//   tokens for that reason.

/**
 * The memory flush plan returned to OpenClaw's host. Mirrors memory-core's
 * `MemoryFlushPlan` shape (Appendix A of the integration plan). The host
 * consumes thresholds + prompt to decide when/how to flush; capture itself
 * is a separate downstream step.
 */
export interface MemoryFlushPlan {
  /** Soft trigger: flush when context nears this many tokens. */
  softThresholdTokens: number;
  /** Hard trigger: flush when raw transcript exceeds this many bytes. */
  forceFlushTranscriptBytes: number;
  /** Keep at least this many tokens of headroom after flush. */
  reserveTokensFloor: number;
  /** Extraction model (optional; Task 2.7 may make this config-driven). */
  model?: string;
  /** The extraction prompt handed to the LLM at flush time. */
  prompt: string;
  /** The extraction system prompt handed to the LLM at flush time. */
  systemPrompt: string;
  /** TR-namespaced scratch path where the host writes extraction output. */
  relativePath: string;
}

/**
 * Resolver signature — matches memory-core's `MemoryFlushPlanResolver`.
 * Returns the plan, or null only if capture is explicitly disabled (which
 * TR does not do today; the poller is always-on as the capture fallback).
 */
export type MemoryFlushPlanResolver = (params: {
  cfg?: unknown;
  nowMs?: number;
}) => MemoryFlushPlan | null;

/**
 * OpenClaw config shape (loose — we only read compaction overrides if
 * present; today TR ignores all of it and ships documented defaults).
 * Kept inline so memory-runtime.ts stays free of an OpenClaw type import.
 */
interface LooseOpenClawConfig {
  agents?: {
    defaults?: {
      compaction?: {
        memoryFlush?: {
          enabled?: boolean;
          softThresholdTokens?: number;
          forceFlushTranscriptBytes?: number | string;
          prompt?: string;
          systemPrompt?: string;
          model?: string;
        };
        reserveTokensFloor?: number;
      };
    };
  };
}

/**
 * Default flush thresholds. Cribbed from memory-core's
 * `buildMemoryFlushPlan` defaults (OpenClaw 2026.6.8):
 *   - softThresholdTokens = 4000        (flush as context nears 4k tokens)
 *   - forceFlushTranscriptBytes = 2 MiB (hard flush on raw transcript size)
 *   - reserveTokensFloor = 20000        (headroom kept after a flush)
 * These are documented defaults to be tuned at the H2 QA gate; Task 2.7
 * may override them from cfg.agents.defaults.compaction.memoryFlush.
 */
const DEFAULT_SOFT_THRESHOLD_TOKENS = 4000;
const DEFAULT_FORCE_FLUSH_TRANSCRIPT_BYTES = 2 * 1024 * 1024; // 2 MiB
const DEFAULT_RESERVE_TOKENS_FLOOR = 20000;

/**
 * TR-canonical user-prompt TEMPLATE for flush-driven extraction. Mirrors
 * the turn-extraction user prompt built inline in extractor.ts's
 * `extractFacts()` (see `extractor.ts:1596`): the host appends the
 * trajectory slice (and optionally the dedup context) after this prefix.
 * Kept here rather than in extractor.ts because extractor.ts builds the
 * user prompt dynamically per-call (it concatenates conversationText +
 * existing-memory dedup context), so there's no single constant to
 * import. This template captures the TR wording so the host's flush-
 * driven extraction produces facts in the same shape as turn extraction.
 */
const EXTRACTION_USER_PROMPT =
  'Extract important facts from these recent conversation turns:\n\n';

/**
 * Scratch path prefix for TR flush output. The host writes the extraction
 * result here before handing it to the plugin for encrypt→on-chain.
 * Namespaced so it cannot collide with memory-core's `memory/*.md` paths.
 */
const TR_FLUSH_DIR = '.totalreclaw/flush';

/**
 * Format a UTC date stamp (YYYY-MM-DD) from a epoch-ms value. Pure
 * function of the input — no host TZ dependence, no Intl nuance.
 */
function formatUtcDateStamp(nowMs: number): string {
  // ISO 8601 UTC: slice the YYYY-MM-DD prefix off the date portion. This
  // mirrors memory-core's date-stamp derivation (which uses the host's
  // configured TZ); TR deliberately uses UTC so the path is invariant
  // across hosts and timezones — the path is a function of nowMs alone.
  return new Date(nowMs).toISOString().slice(0, 10);
}

/**
 * Build the memory flush plan returned to OpenClaw's host.
 *
 * @param params.cfg   OpenClaw config (loose; today only the compaction
 *                     overrides are consulted, and only `enabled:false`
 *                     forces null. Task 2.7 may wire more overrides.)
 * @param params.nowMs epoch-ms used to derive the date-stamped relativePath.
 *                     Defaults to Date.now() — a pure clock read.
 * @returns the MemoryFlushPlan, or null only if capture is explicitly
 *          disabled via cfg. Today capture is always on, so this never
 *          returns null in practice.
 */
export function buildFlushPlan(params: { cfg?: LooseOpenClawConfig; nowMs?: number } = {}): MemoryFlushPlan | null {
  const cfg = params.cfg as LooseOpenClawConfig | undefined;
  const flushCfg = cfg?.agents?.defaults?.compaction?.memoryFlush;

  // Capture is opt-OUT: only an explicit `enabled: false` returns null.
  // This mirrors memory-core's contract. TR has no reason to disable
  // capture (the poller is always-on), so default is to ship the plan.
  if (flushCfg?.enabled === false) return null;

  // Thresholds: cribbed defaults, optionally overridden by cfg. The byte
  // size accepts a number or a human string (e.g. "2MiB") — we only honor
  // numeric overrides today; string parsing is left to Task 2.7.
  const softThresholdTokens =
    typeof flushCfg?.softThresholdTokens === 'number' && flushCfg.softThresholdTokens >= 0
      ? flushCfg.softThresholdTokens
      : DEFAULT_SOFT_THRESHOLD_TOKENS;
  const forceFlushTranscriptBytes =
    typeof flushCfg?.forceFlushTranscriptBytes === 'number' && flushCfg.forceFlushTranscriptBytes >= 0
      ? flushCfg.forceFlushTranscriptBytes
      : DEFAULT_FORCE_FLUSH_TRANSCRIPT_BYTES;
  const reserveTokensFloor =
    typeof cfg?.agents?.defaults?.compaction?.reserveTokensFloor === 'number' &&
    cfg.agents.defaults.compaction.reserveTokensFloor >= 0
      ? cfg.agents.defaults.compaction.reserveTokensFloor
      : DEFAULT_RESERVE_TOKENS_FLOOR;

  // Extraction prompt: TR's canonical v1 taxonomy prompt. Imported from
  // extractor.ts at module load. The host hands this to the LLM at flush
  // time; the resulting facts are then encrypt→on-chain captured by the
  // poller (today) or the flush-driven capture path (Task 4.2).
  //
  // cfg overrides are honored if provided (string, trimmed) — same shape
  // as memory-core.
  const prompt =
    typeof flushCfg?.prompt === 'string' && flushCfg.prompt.trim().length > 0
      ? flushCfg.prompt.trim()
      : EXTRACTION_USER_PROMPT;
  const systemPrompt =
    typeof flushCfg?.systemPrompt === 'string' && flushCfg.systemPrompt.trim().length > 0
      ? flushCfg.systemPrompt.trim()
      : EXTRACTION_SYSTEM_PROMPT;

  const model =
    typeof flushCfg?.model === 'string' && flushCfg.model.trim().length > 0
      ? flushCfg.model.trim()
      : undefined;

  // relativePath: TR-namespaced scratch path, date-stamped from nowMs.
  const nowMs = typeof params.nowMs === 'number' ? params.nowMs : Date.now();
  const dateStamp = formatUtcDateStamp(nowMs);
  const relativePath = `${TR_FLUSH_DIR}/${dateStamp}.jsonl`;

  return {
    softThresholdTokens,
    forceFlushTranscriptBytes,
    reserveTokensFloor,
    model,
    prompt,
    systemPrompt,
    relativePath,
  };
}
