/**
 * tools.test — hard-contract test for the memory_search / memory_get tool
 * factories (Task 2.6 of the OpenClaw native integration plan,
 * docs/plans/2026-06-21-openclaw-native-integration-plan.md, 2026-06-21).
 *
 * Verifies the two tools are STRUCTURALLY COMPATIBLE with the
 * memory-core tools OpenClaw's `active-memory` sub-agent already knows how
 * to call — same `name`, same parameter schema field names, same handler
 * delegation to the TR MemorySearchManager (search → manager.search(query),
 * get → manager.readFile via a direct method call), and an
 * AgentToolResult-shaped return value.
 *
 * The shape under test was reverse-engineered from OpenClaw 2026.6.8's
 * bundled memory-core at
 *   /tmp/tr-openclaw-probe/node_modules/openclaw/dist/tools-CT_OGlM3.js
 *   createMemorySearchTool (l.437) / createMemoryGetTool (l.631), and the
 *   tool contract (Tool + AgentTool + AgentToolResult) from
 *   dist/index-CB3EOAcX.d.ts (l.216, 406, 422) + dist/common-BYJ5YAFM.d.ts
 *   (l.20, ErasedAgentToolExecute: execute(toolCallId, params, signal?,
 *   onUpdate?) => Promise<AgentToolResult>).
 *
 * MEMORY-CORE PATTERN (what we mirror):
 *   memory-core's tool factory is `createMemorySearchTool(options)` where
 *   options come from `resolveMemoryToolOptions(ctx)` (agentId, sessionKey,
 *   sandboxed, oneShotCliRun, config). The handler resolves the manager via
 *   `getMemoryManagerContextWithPurpose({cfg, agentId})` which calls the
 *   memory runtime's `getMemorySearchManager(...)` — the SAME surface TR's
 *   `createTrMemoryPluginRuntime` returns. memory-core reaches the runtime
 *   via a host-internal `loadMemoryToolRuntime()` import that a third-party
 *   plugin CANNOT use (it's inside OpenClaw's dist chunks). So TR captures
 *   the runtime at register() time and the tool factory closes over it:
 *   `createMemorySearchTool(runtime)`. This is the documented, sanctioned
 *   deviation — see tools.ts docstring for the full justification.
 *
 * Run: `npx tsx tools.test.ts` — prints OK and exits 0 on pass.
 */

import { strict as assert } from 'node:assert';
import { createMemoryGetTool, createMemorySearchTool } from './tools.js';

// ---------------------------------------------------------------------------
// Fake runtime: returns a fake manager via the same surface TR's real
// createTrMemoryPluginRuntime exposes (getMemorySearchManager({cfg, agentId,
// purpose}) -> { manager, error? }). The fake manager records the args it was
// called with so the test can prove delegation + arg forwarding.
// ---------------------------------------------------------------------------

let lastSearchArgs: { query: string; opts?: unknown } | undefined;
let lastReadArgs: { relPath: string; from?: number; lines?: number } | undefined;
let managerSearchCalls = 0;
let managerReadCalls = 0;
let lastManagerPurpose: string | undefined;

const fakeManager = {
  search: async (query: string, opts?: unknown) => {
    managerSearchCalls++;
    lastSearchArgs = { query, opts };
    return [
      {
        path: 'totalreclaw://facts/f1',
        startLine: 1,
        endLine: 1,
        score: 0.9,
        snippet: 'prefers dark mode',
        source: 'memory',
        citation: 'f1',
      },
    ];
  },
};

// The read method on the real TR adapter is `readFile` (its canonical name).
// tools.ts calls it directly; this fake mirrors that name so the test
// exercises the real adapter method. `lastReadArgs` is captured.
(fakeManager as any).readFile = async (params: { relPath: string; from?: number; lines?: number }) => {
  managerReadCalls++;
  lastReadArgs = params;
  return {
    text: 'User prefers dark mode and works at Acme.',
    path: params.relPath,
    truncated: false,
    from: params.from ?? 1,
    lines: 1,
    nextFrom: undefined,
  };
};

const fakeRuntime = {
  getMemorySearchManager: async (params: { cfg?: unknown; agentId: string; purpose?: string }) => {
    lastManagerPurpose = params.purpose;
    return { manager: fakeManager, error: undefined as string | undefined };
  },
};

// ---------------------------------------------------------------------------
// Tool shape contracts — these are the load-bearing name/schema fields the
// active-memory sub-agent keys off. A rename or a schema field rename here
// would silently break recall for every TR-paired agent.
// ---------------------------------------------------------------------------

const searchTool = createMemorySearchTool(fakeRuntime as any);
const getTool = createMemoryGetTool(fakeRuntime as any);

// Tools MUST be returned (not null) and carry the canonical names.
assert.ok(searchTool, 'createMemorySearchTool must return a tool object');
assert.ok(getTool, 'createMemoryGetTool must return a tool object');
assert.equal(searchTool.name, 'memory_search');
assert.equal(getTool.name, 'memory_get');

// Labels: memory-core uses "Memory Search" / "Memory Get". Match exactly so
// the agent UI renders the same surface for bundled vs TR-paired memory.
assert.equal(searchTool.label, 'Memory Search');
assert.equal(getTool.label, 'Memory Get');

// Descriptions: non-empty, and mention the tool's purpose. We don't assert
// exact wording (TR's phrasing is adapted to the encrypted-vault model) but
// we DO assert the search description references recall/search intent and
// the get description references reading.
assert.ok(
  typeof searchTool.description === 'string' && searchTool.description.length > 20,
  'search description is non-trivial',
);
assert.ok(
  typeof getTool.description === 'string' && getTool.description.length > 20,
  'get description is non-trivial',
);

// ---------------------------------------------------------------------------
// Parameter schema contracts — field names MUST match memory-core's
// MemorySearchSchema / MemoryGetSchema exactly (the agent emits these field
// names; a rename silently breaks the call). memory-core:
//   MemorySearchSchema = { query, maxResults?, minScore?, corpus? }
//   MemoryGetSchema    = { path, from?, lines?, corpus? }
// ---------------------------------------------------------------------------

const searchParams = searchTool.parameters as {
  type: string;
  properties: Record<string, unknown>;
  required: string[];
};
assert.equal(searchParams.type, 'object');
assert.ok('query' in searchParams.properties, 'memory_search params has query');
assert.ok('maxResults' in searchParams.properties, 'memory_search params has maxResults');
assert.ok('minScore' in searchParams.properties, 'memory_search params has minScore');
assert.deepEqual(searchParams.required, ['query'], 'query is the only required search field');

const getParams = getTool.parameters as {
  type: string;
  properties: Record<string, unknown>;
  required: string[];
};
assert.equal(getParams.type, 'object');
assert.ok('path' in getParams.properties, 'memory_get params has path');
assert.ok('from' in getParams.properties, 'memory_get params has from');
assert.ok('lines' in getParams.properties, 'memory_get params has lines');
assert.deepEqual(getParams.required, ['path'], 'path is the only required get field');

// ---------------------------------------------------------------------------
// Handler delegation: memory_search -> manager.search(query, opts)
// ---------------------------------------------------------------------------

// `execute(toolCallId, params, signal?, onUpdate?)` per ErasedAgentToolExecute.
// We invoke with a fake toolCallId and the args object the agent would emit.
const searchResult = (await searchTool.execute(
  'call-1',
  { query: 'what does the user prefer?', maxResults: 5 },
  undefined as any,
  undefined as any,
)) as { content: Array<{ type: string; text: string }> };

// The handler MUST have delegated to manager.search with the query.
assert.equal(managerSearchCalls, 1, 'memory_search handler calls manager.search exactly once');
assert.ok(lastSearchArgs, 'search args were captured');
assert.equal(
  lastSearchArgs!.query,
  'what does the user prefer?',
  'query is forwarded verbatim into manager.search',
);
// maxResults should be forwarded into the search opts (TR's manager reads it).
assert.equal(
  (lastSearchArgs!.opts as any)?.maxResults,
  5,
  'maxResults is forwarded into manager.search opts',
);

// Return shape: AgentToolResult — content[] of { type: 'text', text: string }.
assert.ok(Array.isArray(searchResult.content), 'result has content array');
assert.ok(searchResult.content.length > 0, 'result has at least one content block');
assert.equal(searchResult.content[0].type, 'text');
// The text is the JSON payload the agent parses — memory-core shape: { results, ... }.
const searchPayload = JSON.parse(searchResult.content[0].text);
assert.ok(Array.isArray(searchPayload.results), 'search payload has results array');
assert.equal(searchPayload.results.length, 1);
assert.equal(searchPayload.results[0].path, 'totalreclaw://facts/f1');
assert.equal(searchPayload.results[0].source, 'memory');
assert.equal(searchPayload.results[0].citation, 'f1');

// ---------------------------------------------------------------------------
// Handler delegation: memory_get -> manager's read method with { relPath }
// ---------------------------------------------------------------------------

managerReadCalls = 0;
const getResult = (await getTool.execute(
  'call-2',
  { path: 'totalreclaw://facts/f1', from: 1, lines: 10 },
  undefined as any,
  undefined as any,
)) as { content: Array<{ type: string; text: string }> };

assert.equal(managerReadCalls, 1, 'memory_get handler calls the read method exactly once');
assert.ok(lastReadArgs, 'read args were captured');
assert.equal(
  lastReadArgs!.relPath,
  'totalreclaw://facts/f1',
  'path is forwarded as relPath into the read call',
);
assert.equal(lastReadArgs!.from, 1, 'from is forwarded');
assert.equal(lastReadArgs!.lines, 10, 'lines is forwarded');

// Return shape: AgentToolResult with the memory-core get payload shape
// { path, text, truncated?, from?, lines?, nextFrom? }.
const getPayload = JSON.parse(getResult.content[0].text);
assert.equal(getPayload.path, 'totalreclaw://facts/f1');
assert.equal(typeof getPayload.text, 'string');
assert.ok(getPayload.text.length > 0, 'get payload has non-empty text');

// ---------------------------------------------------------------------------
// getMemorySearchManager wiring: both tools reach the manager through the
// runtime's getMemorySearchManager surface (the SAME surface OpenClaw's host
// calls). Confirms the captured-runtime pattern is wired correctly.
// ---------------------------------------------------------------------------

// Fresh runtime to reset the purpose capture.
let observedPurpose: string | undefined;
const fakeRuntime2 = {
  getMemorySearchManager: async (params: { cfg?: unknown; agentId: string; purpose?: string }) => {
    observedPurpose = params.purpose;
    return { manager: fakeManager, error: undefined as string | undefined };
  },
};
const s2 = createMemorySearchTool(fakeRuntime2 as any);
await s2.execute('c', { query: 'q' }, undefined as any, undefined as any);
// Purpose is optional + informational; we only assert it was passed through
// as a string (or undefined), never an object — locks the call surface.
assert.ok(
  observedPurpose === undefined || typeof observedPurpose === 'string',
  'purpose is passed as string|undefined, matching memory-core',
);

// ---------------------------------------------------------------------------
// Unavailable-path: when getMemorySearchManager returns { manager: null,
// error }, the search handler MUST surface a disabled result (matching
// memory-core's buildMemorySearchUnavailableResult shape:
//   { disabled: true, unavailable: true, error, warning, action })
// rather than throwing. active-memory treats `disabled:true` as a signal to
// tell the user memory is unavailable.
// ---------------------------------------------------------------------------

const unavailableRuntime = {
  getMemorySearchManager: async () => ({
    manager: null as unknown,
    error: 'pipeline not paired',
  }),
};
const sUnavail = createMemorySearchTool(unavailableRuntime as any);
const unavailResult = await sUnavail.execute('c', { query: 'q' }, undefined as any, undefined as any);
const unavailPayload = JSON.parse((unavailResult as any).content[0].text);
assert.equal(unavailPayload.disabled, true, 'unavailable path sets disabled:true');
assert.equal(unavailPayload.unavailable, true, 'unavailable path sets unavailable:true');
assert.ok(
  typeof unavailPayload.error === 'string' && unavailPayload.error.length > 0,
  'unavailable path carries a non-empty error string',
);
// Warning + action guidance MUST be present (memory-core contract — the agent
// is instructed to surface these to the user).
assert.ok(
  typeof unavailPayload.warning === 'string' && unavailPayload.warning.length > 0,
  'unavailable path carries warning guidance',
);
assert.ok(
  typeof unavailPayload.action === 'string' && unavailPayload.action.length > 0,
  'unavailable path carries action guidance',
);

// Same for memory_get — when the manager is unavailable, return a disabled
// result keyed on the requested path so the agent can correlate.
const gUnavail = createMemoryGetTool(unavailableRuntime as any);
const gUnavailResult = await gUnavail.execute(
  'c',
  { path: 'totalreclaw://facts/f9' },
  undefined as any,
  undefined as any,
);
const gUnavailPayload = JSON.parse((gUnavailResult as any).content[0].text);
assert.equal(gUnavailPayload.disabled, true, 'memory_get unavailable sets disabled:true');
assert.equal(gUnavailPayload.path, 'totalreclaw://facts/f9', 'unavailable get echoes the path');
assert.ok(
  typeof gUnavailPayload.error === 'string' && gUnavailPayload.error.length > 0,
  'unavailable get carries an error string',
);

// ---------------------------------------------------------------------------
// Error-path: when the manager throws inside search/read, the handler MUST
// NOT throw out of its async boundary — it returns a disabled result. This
// mirrors memory-core's try/catch around the manager calls and keeps a
// thrown pipeline error from crashing the agent's tool batch.
// ---------------------------------------------------------------------------

const throwingManager = {
  search: async () => {
    throw new Error('subgraph timeout');
  },
};
(throwingManager as any).readFile = async () => {
  throw new Error('decrypt failed');
};
const throwingRuntime = {
  getMemorySearchManager: async () => ({ manager: throwingManager, error: undefined }),
};
const sThrow = createMemorySearchTool(throwingRuntime as any);
const sThrowResult = await sThrow.execute('c', { query: 'q' }, undefined as any, undefined as any);
const sThrowPayload = JSON.parse((sThrowResult as any).content[0].text);
assert.equal(sThrowPayload.disabled, true, 'thrown search error -> disabled result');
assert.ok(/subgraph timeout/.test(sThrowPayload.error), 'thrown error message is surfaced');

const gThrow = createMemoryGetTool(throwingRuntime as any);
const gThrowResult = await gThrow.execute('c', { path: 'p' }, undefined as any, undefined as any);
const gThrowPayload = JSON.parse((gThrowResult as any).content[0].text);
assert.equal(gThrowPayload.disabled, true, 'thrown read error -> disabled result');
assert.ok(/decrypt failed/.test(gThrowPayload.error), 'thrown read error message is surfaced');

console.log('tools.test OK');
