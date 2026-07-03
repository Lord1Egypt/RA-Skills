/**
 * native-memory — the OpenClaw-native MemoryPluginCapability wiring helper
 * for the TR plugin (Task 2.7 of the OpenClaw native integration plan,
 * docs/plans/2026-06-21-openclaw-native-integration-plan.md, 2026-06-21).
 *
 * WHY THIS FILE EXISTS:
 *   This is THE integration point. OpenClaw 2026.6.8 exposes a
 *   `api.registerMemoryCapability({ promptBuilder, flushPlanResolver, runtime })`
 *   host surface plus the conventional `api.registerTool(...)` calls for the
 *   `memory_search` / `memory_get` tools the active-memory sub-agent already
 *   knows how to drive. For TR to BE the memory backend (not just a tool
 *   plugin), it must register all four against TR's own pipeline.
 *
 *   This helper takes a single `deps` object (built by `buildRecallDeps` in
 *   index.ts) carrying:
 *     - recall / getById (the real subgraph-search + decrypt + reranker
 *       pipeline, parameterized by the paired account — wired in index.ts
 *       because that is where the unexported pipeline helpers + the
 *       module-level auth/encryption/owner state live)
 *     - quota / pinned (prompt-builder inputs; default to "no warning" /
 *       "no pinned" when the caller does not supply them — see TODO markers
 *       in index.ts's buildRecallDeps for the H1 QA gate)
 *
 *   and performs the canonical four-call registration in the order memory-core
 *   itself registers them (verified at
 *   /tmp/tr-openclaw-probe/node_modules/openclaw/dist/extensions/memory-core/
 *   index.js, 2026.6.8):
 *     1. api.registerMemoryCapability({ promptBuilder, flushPlanResolver, runtime })
 *     2. api.registerTool(() => createMemorySearchTool(runtime), { names: ['memory_search'] })
 *     3. api.registerTool(() => createMemoryGetTool(runtime),    { names: ['memory_get'] })
 *
 *   The SAME `runtime` instance is handed to the capability AND both tool
 *   factories. This is load-bearing: the host calls
 *   `runtime.getMemorySearchManager(...)` to obtain a manager, and the
 *   tools obtain a manager via the same surface. A distinct runtime per
 *   registration would still work today (each construction is a pure
 *   closure capture) but would violate the memory-core invariant and
 *   break the day runtime owns real per-manager resources (embedder pool,
 *   connection cache). register-native.test.ts asserts the identity.
 *
 * DESIGN: WHY THE DEPS OBJECT IS PRE-BUILT, NOT BUILT HERE.
 *   `buildRecallDeps` lives in index.ts (not here) on purpose:
 *     1. The real recall/getById closures capture unexported index.ts helpers
 *        (ensureInitialized, generateBlindIndices, generateEmbedding,
 *        getLSHHasher, computeCandidatePool, isDigestBlob, readClaimFromBlob,
 *        searchSubgraph, fetchFactById) AND module-level state
 *        (authKeyHex / encryptionKey / userId / subgraphOwner). Moving them
 *        here would force either (a) exporting all of those from index.ts
 *        (high blast-radius refactor with scanner-trap risk) or (b)
 *        re-plumbing them through this file's signature. Neither is in scope
 *        for Task 2.7.
 *     2. The paired-account context is resolved LAZILY by `ensureInitialized()`
 *        on the first tool/hook call, NOT synchronously at register() time.
 *        So the closures must call `ensureInitialized(logger)` internally —
 *        they cannot be resolved at register() time even if we wanted to.
 *     3. Keeping this file scanner-trivial: it touches NO host environment
 *        state and performs NO outbound network I/O. The closures live in
 *        index.ts alongside the rest of the plugin's network surface.
 *
 * SCANNER-CLEAN HARD CONTRACT (env=N net=N):
 *   This file is pure orchestration. It contains no environment-variable
 *   read token and no outbound network primitive, so neither the
 *   env-harvesting pair nor the disk-exfiltration pair can ever co-occur
 *   here. It also contains no dynamic-code-evaluation primitive (no
 *   runtime `eval` call, no `new Function` constructor). `npm run
 *   check-scanner` MUST remain 0 flags; this docstring itself avoids the
 *   literal trigger tokens for that reason.
 *
 *   `npm run build` uses `--noCheck`, so the loose typing (the api object
 *   is typed against a minimal local interface) is safe — the plugin does
 *   not import OpenClaw's type package.
 */

import {
  createTrMemoryPluginRuntime,
  buildPromptSection,
  buildFlushPlan,
  type TrRecallFn,
  type TrGetFn,
  type TrQuotaState,
  type TrPinnedFact,
} from './memory-runtime.js';
import { createMemorySearchTool, createMemoryGetTool } from './tools.js';

// ---------------------------------------------------------------------------
// Types — the combined deps shape. Reconciles the two dep shapes the
// underlying factories expect (createTrMemoryPluginRuntime + the search
// manager need {recall, getById}; buildPromptSection needs {quota?, pinned?})
// into ONE object the caller in index.ts builds once and passes here.
// ---------------------------------------------------------------------------

/**
 * The combined deps object `buildRecallDeps` in index.ts produces. Carries
 * everything `registerNativeMemory` needs to wire the capability + both
 * tools + the prompt builder.
 *
 * `recall` / `getById` are the load-bearing closures — they bind the real
 * subgraph-search + decrypt + reranker pipeline (Task 2.7's `buildRecallDeps`
 * in index.ts). `quota` / `pinned` are prompt-builder inputs; they are
 * optional and default to no-warning / no-pinned when the caller omits them
 * (documented as TODO(task 2.7b / H1 gate) at the build site).
 */
export interface TrNativeMemoryDeps {
  /** Recall closure: blind-index → subgraph → decrypt → rerank → TrFact[]. */
  recall: TrRecallFn;
  /** getById closure: fetchFactById → decrypt → {id, plaintext} | null. */
  getById: TrGetFn;
  /** Optional quota state for the prompt builder's warning path. */
  quota?: TrQuotaState;
  /** Optional pinned-facts block surfaced by the prompt builder. */
  pinned?: TrPinnedFact[];
}

/**
 * Minimal subset of OpenClawPluginApi this helper needs. Kept local (not
 * imported) so this file compiles without the SDK type package. The runtime
 * shape is structurally identical to OpenClawPluginApi's
 * registerMemoryCapability / registerTool surface.
 *
 * `registerMemoryCapability` is OpenClaw 2026.6.8's host surface for a
 * memory-kind plugin. The shape of the capability object is exactly:
 *   { promptBuilder, flushPlanResolver, runtime }
 * — verified at /tmp/tr-openclaw-probe/node_modules/openclaw/dist/extensions/
 *   memory-core/index.js (l.270-273).
 */
export interface NativeMemoryApiSurface {
  registerMemoryCapability(capability: {
    promptBuilder: (params: {
      availableTools: Set<string>;
      citationsMode?: unknown;
    }) => string[];
    flushPlanResolver: (params: { cfg?: unknown; nowMs?: number }) => unknown;
    runtime: ReturnType<typeof createTrMemoryPluginRuntime>;
  }): void;
  registerTool(
    factory: () => unknown,
    opts?: { name?: string; names?: string[] },
  ): void;
}

// ---------------------------------------------------------------------------
// registerNativeMemory — the canonical four-call wiring
// ---------------------------------------------------------------------------

/**
 * Wire TR's native MemoryPluginCapability + the two memory tools into the
 * OpenClaw host. Performs the canonical registration in the order memory-core
 * itself registers them (capability first, then both tools).
 *
 * The SAME `runtime` instance is passed to:
 *   - api.registerMemoryCapability({ ..., runtime })   (host surface)
 *   - createMemorySearchTool(runtime)                  (memory_search factory)
 *   - createMemoryGetTool(runtime)                     (memory_get factory)
 *
 * Identity is load-bearing — see file header. register-native.test.ts
 * asserts the same `runtime` reaches all three.
 *
 * @param api    the OpenClaw plugin api (registerMemoryCapability + registerTool)
 * @param deps   the combined deps object from buildRecallDeps in index.ts
 * @returns      the runtime that was registered (for callers that want to
 *               hold a reference, e.g. for close on plugin stop)
 */
export function registerNativeMemory(
  api: NativeMemoryApiSurface,
  deps: TrNativeMemoryDeps,
): ReturnType<typeof createTrMemoryPluginRuntime> {
  // Build the runtime ONCE. This is the single object that flows into the
  // capability AND both tool factories below — identity is asserted by
  // register-native.test.ts.
  const runtime = createTrMemoryPluginRuntime({
    recall: deps.recall,
    getById: deps.getById,
  });

  // (1) Register the capability. The prompt builder closes over deps.quota
  // and deps.pinned directly (it needs no runtime state — it's pure string
  // rendering, see memory-runtime.ts buildPromptSection). flushPlanResolver
  // is stateless (it returns TR's canonical extraction plan; capture is not
  // required, we hand the function reference verbatim).
  api.registerMemoryCapability({
    promptBuilder: (params) => buildPromptSection(params, { quota: deps.quota, pinned: deps.pinned }),
    flushPlanResolver: buildFlushPlan,
    runtime,
  });

  // (2) + (3) Register the two tools. The factories capture the SAME runtime
  // (the captured-runtime design — see tools.ts header). The conventional
  // tool names survive the tool-policy strip in OC 2026.5.x (issue #223):
  // they are passed via the `names` opts so the SDK's name bookkeeping sees
  // them even though the tool object's own `name` field is the visible
  // registration name.
  api.registerTool(() => createMemorySearchTool(runtime), { names: ['memory_search'] });
  api.registerTool(() => createMemoryGetTool(runtime), { names: ['memory_get'] });

  return runtime;
}
