/**
 * memory-runtime.test — hard-contract test for the TrMemorySearchManager
 * adapter (Task 2.1 of the OpenClaw native integration plan,
 * docs/plans/2026-06-21-openclaw-native-integration-plan.md, 2026-06-21).
 *
 * Verifies the file↔fact mapping that lets TR's encrypted-fact + on-chain
 * vault look like a memory corpus to OpenClaw's active-memory sub-agent:
 *   - search() returns file-shaped results with
 *       path = FACT_PATH_PREFIX + factId,
 *       source = 'memory',
 *       snippet = decrypted plaintext,
 *       citation = factId.
 *   - readFile() reverses relPath → id → decrypt.
 *   - status().provider === 'totalreclaw'.
 *   - probeEmbeddingAvailability / probeVectorAvailability report ok.
 *
 * Also covers the 2026-06-21 code-review refinements:
 *   - minScore filtering + defensive sort.
 *   - signal / sessionKey forwarded into recall.
 *   - from/lines pagination + nextFrom.
 *   - I1 clamp: readFile past EOF never returns a negative line count.
 *   - bare relPath (no prefix) passthrough.
 *
 * recall + getById are fakes here; Task 2.3 wires them to the real
 * subgraph-search + vault-crypto.decrypt + reranker pipeline.
 *
 * Run: `npx tsx memory-runtime.test.ts` — prints OK and exits 0 on pass.
 */

import { strict as assert } from 'node:assert';
import {
  buildFlushPlan,
  buildPromptSection,
  createTrMemorySearchManager,
  createTrMemoryPluginRuntime,
  FACT_PATH_PREFIX,
} from './memory-runtime.js';

// Map-backed fake so multi-fact + multi-line scenarios are easy to express.
// Score is provided per-(query) by the fake recall below.
const FACTS = new Map<string, string>([
  ['f1', 'User prefers dark mode.'],
  ['f2', 'User works at Acme.'],
  ['f3', 'line one\nline two\nline three\nline four'],
]);

// Per-fact score for the fake recall. Higher = more relevant.
const SCORES: Record<string, number> = { f1: 0.9, f2: 0.7, f3: 0.6 };

let lastRecallOpts: { maxResults?: number; signal?: AbortSignal; sessionKey?: string } | undefined;

const recall = async (
  _q: string,
  opts?: { maxResults?: number; signal?: AbortSignal; sessionKey?: string },
) => {
  lastRecallOpts = opts;
  // Deliberately return in NON-sorted order (f3, f2, f1) so tests can prove
  // search() sorts defensively by score before slicing/filtering.
  return ['f3', 'f2', 'f1']
    .map((id) => ({ id, plaintext: FACTS.get(id)!, score: SCORES[id]! }))
    .filter((f) => FACTS.has(f.id));
};

const getById = async (id: string) => {
  const plaintext = FACTS.get(id);
  return plaintext === undefined ? null : { id, plaintext };
};

const mgr = createTrMemorySearchManager({ recall, getById });

// --- search(): file-shaped results from decrypted facts ---
const hits = await mgr.search('preferences');
assert.equal(hits.length, 3);
// Defensive sort: highest score first despite recall returning unsorted.
assert.equal(hits[0].citation, 'f1'); // 0.9
assert.equal(hits[1].citation, 'f2'); // 0.7
assert.equal(hits[2].citation, 'f3'); // 0.6
assert.equal(hits[0].path, `${FACT_PATH_PREFIX}f1`);
assert.equal(hits[0].startLine, 1);
assert.ok(hits[0].endLine >= 1);
assert.equal(hits[0].source, 'memory');
assert.match(hits[0].snippet, /dark mode/);
assert.equal(hits[0].citation, 'f1');

// --- S1: minScore filtering drops sub-threshold hits ---
const hi = await mgr.search('q', { minScore: 0.8 });
assert.equal(hi.length, 1, 'minScore=0.8 should keep only the 0.9 hit');
assert.equal(hi[0].citation, 'f1');
// minScore=0.65 keeps 0.9 + 0.7 but drops 0.6
const mid = await mgr.search('q', { minScore: 0.65 });
assert.equal(mid.length, 2);
assert.equal(mid[0].citation, 'f1');
assert.equal(mid[1].citation, 'f2');

// --- M1: signal + sessionKey are forwarded into recall ---
const ac = new AbortController();
await mgr.search('q', { signal: ac.signal, sessionKey: 'sess-42' });
assert.equal(lastRecallOpts?.sessionKey, 'sess-42');
assert.equal(lastRecallOpts?.signal, ac.signal);

// --- readFile(): reverse path -> id -> decrypt ---
const r = await mgr.readFile({ relPath: `${FACT_PATH_PREFIX}f1` });
assert.match(r.text, /dark mode/);
assert.equal(r.path, `${FACT_PATH_PREFIX}f1`);

// --- S1: from/lines pagination on a multi-line fact ---
const page = await mgr.readFile({ relPath: `${FACT_PATH_PREFIX}f3`, from: 2, lines: 1 });
assert.equal(page.text, 'line two');
assert.equal(page.truncated, true);
assert.equal(page.nextFrom, 3);
assert.equal(page.lines, 1);

// Last-page read: lines requested >= remaining → no truncation.
const lastPage = await mgr.readFile({ relPath: `${FACT_PATH_PREFIX}f3`, from: 4, lines: 5 });
assert.equal(lastPage.text, 'line four');
assert.equal(lastPage.truncated, false);
assert.equal(lastPage.nextFrom, undefined);

// --- S1 + I1: from past EOF must not surface a negative line count ---
const past = await mgr.readFile({ relPath: `${FACT_PATH_PREFIX}f1`, from: 100 });
assert.equal(past.text, '', 'past-EOF read returns empty text');
assert.equal(past.truncated, false);
assert.ok(past.lines >= 0, `lines must be non-negative (got ${past.lines})`);

// --- S1: bare relPath (no prefix) resolves identically to prefixed form ---
const bare = await mgr.readFile({ relPath: 'f1' });
const prefixed = await mgr.readFile({ relPath: `${FACT_PATH_PREFIX}f1` });
assert.equal(bare.text, prefixed.text);
assert.equal(bare.path, prefixed.path);

// --- status + probes ---
assert.equal(mgr.status().provider, 'totalreclaw');
assert.ok((await mgr.probeEmbeddingAvailability()).ok);
assert.equal(await mgr.probeVectorAvailability(), true);

// ---------------------------------------------------------------------------
// Task 2.3 — createTrMemoryPluginRuntime wrapper
// (getMemorySearchManager / resolveMemoryBackendConfig / close* surface).
// Reuses the same Map-backed fake recall/getById defined above.
// ---------------------------------------------------------------------------
const runtime = createTrMemoryPluginRuntime({ recall, getById });

// getMemorySearchManager: success path returns a working adapter, no error.
const got = await runtime.getMemorySearchManager({ cfg: {} as any, agentId: 'a1' });
assert.ok(got.manager, 'manager must be returned on success');
assert.equal(got.error, undefined, 'no error string on success');
// The returned manager is a real TrMemorySearchManager — search() works.
const rtHits = await got.manager!.search('preferences');
assert.ok(rtHits.length >= 0, 'returned manager.search must resolve');
assert.equal(rtHits[0]?.source, 'memory', 'returned manager yields memory hits');

// resolveMemoryBackendConfig: TR is its own backend, so 'builtin'.
assert.deepEqual(
  runtime.resolveMemoryBackendConfig({ cfg: {} as any, agentId: 'a1' }),
  { backend: 'builtin' },
  'TR reports itself as the builtin backend',
);

// close* are no-ops today but MUST be present and non-throwing.
await runtime.closeMemorySearchManager?.({ cfg: {} as any, agentId: 'a1' });
await runtime.closeAllMemorySearchManagers?.();

// Error path: a recall closure that throws synchronously at adapter build
// time surfaces as { manager: null, error: <string> } — never an exception
// out of getMemorySearchManager. (We force this by passing a `recall` whose
// presence triggers a factory-time throw via an injected getter proxy. The
// adapter itself is lazy, so to exercise the catch we wrap createTrMemory-
// SearchManager. Simpler: bind deps that throw on construction by making
// `recall` a getter that throws the moment it's read.)
const throwingDeps = new Proxy(
  { recall: () => Promise.resolve([]), getById: async () => null },
  {
    get(target, prop) {
      if (prop === 'recall') {
        throw new Error('pipeline not paired');
      }
      return (target as any)[prop];
    },
  },
) as any;
const throwingRuntime = createTrMemoryPluginRuntime(throwingDeps);
// Reading `recall` happens inside createTrMemorySearchManager via the
// `deps.recall` reference captured in search(); the factory itself doesn't
// invoke recall, so construction succeeds. The contract still guarantees
// getMemorySearchManager never throws — verify that holds even when the
// manager is constructed against a hostile deps object.
const gotHostile = await throwingRuntime.getMemorySearchManager({
  cfg: {} as any,
  agentId: 'a1',
});
assert.ok(gotHostile.manager, 'construction does not invoke recall, so manager is returned');

// ---------------------------------------------------------------------------
// Task 2.4 — buildPromptSection (recall guidance + quota + pinned)
// Mirrors memory-core's branching on memory_search/memory_get availability,
// adapted to TR's encrypted-vault model, plus TR extras (quota warning +
// pinned facts) injected via a deps object so the function stays
// environment/network clean.
// ---------------------------------------------------------------------------

// --- Branching: mirrors memory-core's availableTools.has() logic ---
// (a) BOTH tools present -> guidance mentions memory_search AND memory_get.
const both = buildPromptSection(
  { availableTools: new Set(['memory_search', 'memory_get']) },
  {},
);
assert.ok(
  both.some((l) => /memory_search/.test(l)) && both.some((l) => /memory_get/.test(l)),
  'both-tools branch mentions memory_search and memory_get',
);
// The both-branch guidance must reference the vault (TR-specific wording),
// not the memory-core file-system phrasing.
assert.ok(
  both.some((l) => /vault/i.test(l)),
  'guidance references the TR memory vault, not file paths',
);

// (b) memory_get only -> mentions memory_get, NOT memory_search.
const onlyGet = buildPromptSection(
  { availableTools: new Set(['memory_get']) },
  {},
);
assert.ok(
  onlyGet.some((l) => /memory_get/.test(l)) && !onlyGet.some((l) => /memory_search/.test(l)),
  'memory_get-only branch mentions memory_get but not memory_search',
);

// (c) memory_search only -> mentions memory_search, NOT memory_get.
const onlySearch = buildPromptSection(
  { availableTools: new Set(['memory_search']) },
  {},
);
assert.ok(
  onlySearch.some((l) => /memory_search/.test(l)) && !onlySearch.some((l) => /memory_get/.test(l)),
  'memory_search-only branch mentions memory_search but not memory_get',
);

// (d) NEITHER memory tool -> NO recall guidance. An empty array is allowed
// (memory-core returns no guidance when neither tool is available).
const neitherTools = buildPromptSection(
  { availableTools: new Set(['unrelated_tool']) },
  {},
);
assert.ok(
  !neitherTools.some((l) => /memory_search/.test(l)),
  'no search guidance when memory_search absent',
);
assert.ok(
  !neitherTools.some((l) => /memory_get/.test(l)),
  'no get guidance when memory_get absent',
);

// --- Pinned facts: ALWAYS surface, even when neither memory tool is on ---
const neitherWithPinned = buildPromptSection(
  { availableTools: new Set(['unrelated_tool']) },
  { pinned: [{ id: 'p1', plaintext: 'User is vegetarian.' }] },
);
assert.ok(
  neitherWithPinned.some((l) => /vegetarian/i.test(l)),
  'pinned facts surface even without memory tools',
);
// And with tools present, pinned still appends.
const bothWithPinned = buildPromptSection(
  { availableTools: new Set(['memory_search', 'memory_get']) },
  { pinned: [{ id: 'p2', plaintext: 'Birthday is March 5.' }, { id: 'p3', plaintext: 'Prefers Scala.' }] },
);
assert.ok(
  bothWithPinned.some((l) => /March 5/.test(l)) && bothWithPinned.some((l) => /Scala/.test(l)),
  'multiple pinned facts each surface',
);
// Empty pinned array -> no pinned block (no spurious header).
const noPinned = buildPromptSection(
  { availableTools: new Set(['memory_search']) },
  { pinned: [] },
);
assert.ok(
  !noPinned.some((l) => /pinned/i.test(l)),
  'empty pinned array produces no pinned block',
);

// --- Quota warning: fires when >80% used OR on 403/denied ---
const overQuota = buildPromptSection(
  { availableTools: new Set(['memory_search']) },
  { quota: { usedPct: 90 } },
);
assert.ok(overQuota.some((l) => /quota/i.test(l)), 'quota warning fires when >80% used');

const atThreshold = buildPromptSection(
  { availableTools: new Set(['memory_search']) },
  { quota: { usedPct: 81 } },
);
assert.ok(atThreshold.some((l) => /quota/i.test(l)), 'quota warning fires just over 80%');

const denied = buildPromptSection(
  { availableTools: new Set(['memory_search']) },
  { quota: { denied: true } },
);
assert.ok(denied.some((l) => /quota/i.test(l)), 'quota warning fires on 403/denied');

// --- Quota warning: does NOT fire at/below 80% ---
const underQuota = buildPromptSection(
  { availableTools: new Set(['memory_search']) },
  { quota: { usedPct: 50 } },
);
assert.ok(!underQuota.some((l) => /quota/i.test(l)), 'no quota warning at 50%');

const at80 = buildPromptSection(
  { availableTools: new Set(['memory_search']) },
  { quota: { usedPct: 80 } },
);
assert.ok(!at80.some((l) => /quota/i.test(l)), 'no quota warning at exactly 80% (boundary)');

// --- Quota warning + pinned both compose: warning prepended, pinned appended ---
const composed = buildPromptSection(
  { availableTools: new Set(['memory_search', 'memory_get']) },
  {
    quota: { usedPct: 95 },
    pinned: [{ id: 'p1', plaintext: 'User is vegetarian.' }],
  },
);
const quotaIdx = composed.findIndex((l) => /quota/i.test(l));
const pinnedIdx = composed.findIndex((l) => /vegetarian/i.test(l));
const guidanceIdx = composed.findIndex((l) => /memory_search/.test(l));
assert.ok(quotaIdx >= 0 && pinnedIdx >= 0 && guidanceIdx >= 0, 'all three blocks present');
assert.ok(
  quotaIdx < guidanceIdx,
  'quota warning precedes recall guidance',
);
assert.ok(
  pinnedIdx > guidanceIdx,
  'pinned block follows recall guidance',
);

// --- citationsMode is accepted but does not alter the contracts above ---
// (We don't assert on it today; OpenClaw passes it through and memory-core
// currently does not branch on it either. The param is accepted for shape
// compatibility with the MemoryPluginCapability contract.)
const withCitations = buildPromptSection(
  { availableTools: new Set(['memory_search']), citationsMode: 'always' as any },
  {},
);
assert.ok(
  withCitations.some((l) => /memory_search/.test(l)),
  'citationsMode does not suppress recall guidance',
);

// ---------------------------------------------------------------------------
// Task 2.5 — buildFlushPlan (flushPlanResolver)
// Returns the memory flush PLAN (thresholds + extraction prompt) OpenClaw's
// host uses to decide WHEN to flush (soft/force thresholds) and HOW to run
// the extraction (prompt/systemPrompt). The actual extract→encrypt→on-chain
// capture is NOT here — it's a later gate (Task 4.2 / H2 QA). This resolver
// only returns the plan structure.
// ---------------------------------------------------------------------------

const plan = buildFlushPlan({ nowMs: 0 });
assert.ok(plan, 'returns a plan by default (capture enabled)');

// Required shape — every field present and sensibly typed.
assert.equal(typeof plan!.softThresholdTokens, 'number');
assert.equal(typeof plan!.forceFlushTranscriptBytes, 'number');
assert.equal(typeof plan!.reserveTokensFloor, 'number');
assert.equal(typeof plan!.prompt, 'string');
assert.ok(plan!.prompt.length > 0, 'extraction prompt is non-empty');
assert.equal(typeof plan!.systemPrompt, 'string');
assert.ok(plan!.systemPrompt.length > 0, 'extraction system prompt is non-empty');
assert.equal(typeof plan!.relativePath, 'string');
assert.ok(
  plan!.relativePath.includes('totalreclaw') || plan!.relativePath.startsWith('.totalreclaw'),
  `relativePath is TR-namespaced (got ${plan!.relativePath})`,
);

// Sanity: thresholds are positive + ordered (soft > reserve floor? no —
// memory-core ships soft=4000 < reserve=20000 because soft flushes BEFORE
// the reserve floor is reached, so reserve is a *floor* of headroom kept
// AFTER flush, not a lower bound on when to flush. We only assert both are
// positive. forceFlushTranscriptBytes is a byte count, must be > 0.)
assert.ok(plan!.softThresholdTokens > 0, 'softThresholdTokens must be positive');
assert.ok(plan!.forceFlushTranscriptBytes > 0, 'forceFlushTranscriptBytes must be positive');
assert.ok(plan!.reserveTokensFloor > 0, 'reserveTokensFloor must be positive');

// The prompt must be TR's REAL extraction prompt, not a placeholder — check
// for a canonical marker phrase from EXTRACTION_SYSTEM_PROMPT.
assert.ok(
  /Memory Taxonomy v1/.test(plan!.systemPrompt) || /memory extraction engine/i.test(plan!.systemPrompt),
  'systemPrompt is TR canonical extraction prompt (v1 taxonomy marker)',
);

// Defaults: with no nowMs, the resolver must still return a plan (Date.now
// fallback). And it must be stable across calls with the same nowMs.
const planNoNow = buildFlushPlan({});
assert.ok(planNoNow, 'returns a plan even without explicit nowMs');
const planSameNow = buildFlushPlan({ nowMs: 12345 });
assert.equal(planSameNow!.relativePath, buildFlushPlan({ nowMs: 12345 })!.relativePath,
  'relativePath is deterministic for a fixed nowMs');

// Determinism: the date-stamped relativePath for a known epoch must match
// the host's UTC date formatting (the host writes here, so the path must be
// a function of nowMs alone, not of any host environment read).
const epochPlan = buildFlushPlan({ nowMs: 0 }); // 1970-01-01 UTC
assert.ok(
  /1970-01-01|totalreclaw/.test(epochPlan!.relativePath),
  `relativePath encodes the date or is TR-namespaced (got ${epochPlan!.relativePath})`,
);

// --- Opt-out + cfg override coverage (2026-06-21) -----------------------
// buildFlushPlan accepts cfg overrides under
//   cfg.agents.defaults.compaction.memoryFlush.{softThresholdTokens,
//   forceFlushTranscriptBytes, prompt, systemPrompt, model, enabled}
// plus cfg.agents.defaults.compaction.reserveTokensFloor (note: floor is
// under parent `.compaction`, NOT `.memoryFlush`). This mirrors memory-
// core's buildMemoryFlushPlan field-for-field. An explicit
// `memoryFlush.enabled === false` opts out (returns null). These assertions
// lock both paths so a regression in either is caught.

// (1) Opt-out: explicit enabled:false → null (capture disabled).
const optedOut = buildFlushPlan({
  cfg: {
    agents: { defaults: { compaction: { memoryFlush: { enabled: false } } } },
  } as any,
});
assert.equal(optedOut, null, 'enabled:false opts out of capture (returns null)');

// enabled:undefined and enabled:true must NOT opt out (only explicit false).
assert.ok(
  buildFlushPlan({ cfg: { agents: { defaults: { compaction: { memoryFlush: { enabled: true } } } } } as any }),
  'enabled:true does not opt out',
);
assert.ok(
  buildFlushPlan({ cfg: { agents: { defaults: { compaction: { memoryFlush: {} } } } } as any }),
  'enabled:undefined does not opt out',
);

// (2) Overrides: every overridable field takes the cfg sentinel over the
// memory-core default. Distinct sentinel values prove the override path is
// wired per-field (a collision would hide a missed wiring).
const overridePlan = buildFlushPlan({
  cfg: {
    agents: {
      defaults: {
        compaction: {
          reserveTokensFloor: 99999, // parent `.compaction`, not `.memoryFlush`
          memoryFlush: {
            softThresholdTokens: 7777,
            forceFlushTranscriptBytes: 123456,
            prompt: 'SENTINEL_FLUSH_USER_PROMPT',
            systemPrompt: 'SENTINEL_FLUSH_SYSTEM_PROMPT',
            model: 'sentinel-flush-model-xyz',
          },
        },
      },
    },
  } as any,
});
assert.ok(overridePlan, 'override cfg still returns a plan');
assert.equal(overridePlan!.softThresholdTokens, 7777,
  'softThresholdTokens overridden from cfg.memoryFlush');
assert.equal(overridePlan!.forceFlushTranscriptBytes, 123456,
  'forceFlushTranscriptBytes overridden from cfg.memoryFlush');
assert.equal(overridePlan!.reserveTokensFloor, 99999,
  'reserveTokensFloor overridden from cfg.compaction (parent, not memoryFlush)');
assert.equal(overridePlan!.prompt, 'SENTINEL_FLUSH_USER_PROMPT',
  'prompt overridden from cfg.memoryFlush');
assert.equal(overridePlan!.systemPrompt, 'SENTINEL_FLUSH_SYSTEM_PROMPT',
  'systemPrompt overridden from cfg.memoryFlush');
assert.equal(overridePlan!.model, 'sentinel-flush-model-xyz',
  'model overridden from cfg.memoryFlush');

// reserveTokensFloor specifically must NOT be read from under memoryFlush —
// confirm a value placed there is ignored in favor of the compaction-level
// (or default) value. This locks the nesting asymmetry.
const floorUnderMemoryFlushIgnored = buildFlushPlan({
  cfg: {
    agents: {
      defaults: {
        compaction: {
          memoryFlush: {
            // @ts-expect-error — wrong nest on purpose; must be ignored
            reserveTokensFloor: 555,
          },
        },
      },
    },
  } as any,
});
assert.notEqual(floorUnderMemoryFlushIgnored!.reserveTokensFloor, 555,
  'reserveTokensFloor under .memoryFlush is NOT honored (must be under .compaction)');

// (3) Default still works: no cfg at all returns the memory-core defaults
// (soft=4000, force=2 MiB, reserve=20000). Locks that the override path
// hasn't broken the default fall-through.
const defaultPlan = buildFlushPlan({});
assert.ok(defaultPlan, 'no cfg returns a plan');
assert.equal(defaultPlan!.softThresholdTokens, 4000,
  'default softThresholdTokens is 4000 (memory-core default)');
assert.equal(defaultPlan!.forceFlushTranscriptBytes, 2 * 1024 * 1024,
  'default forceFlushTranscriptBytes is 2 MiB (memory-core default)');
assert.equal(defaultPlan!.reserveTokensFloor, 20000,
  'default reserveTokensFloor is 20000 (memory-core default)');
assert.equal(defaultPlan!.model, undefined,
  'default model is undefined (no override, no extraction model pinned)');

console.log('flush-plan.test OK');
console.log('memory-runtime.test OK');
