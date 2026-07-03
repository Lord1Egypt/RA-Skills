/**
 * Phrase-safety registry contract tests (current surfaces, after Phase 3.2).
 *
 * Contract: NO agent tool registered by the TotalReclaw plugin may
 * generate, return, or accept a recovery phrase. The ONLY approved
 * agent-facilitated setup surface is the QR-PAIR flow (browser-side
 * crypto keeps the phrase out of the LLM round-trip by construction),
 * exposed in 3.2+ as the `openclaw totalreclaw onboard [--pair-only]`
 * CLI wizard + the four `/pair/*` HTTP routes.
 *
 * Governed by:
 *   ~/.claude/projects/-Users-pdiogo-Documents-code-totalreclaw-internal/
 *     memory/project_phrase_safety_rule.md
 *
 * Absolute rule: "recovery phrase MUST NEVER cross the LLM context in
 * ANY form — not echoed, not in tool-call stdout, not in tool-result
 * payloads, not in agent reasoning."
 *
 * HISTORY — why this test was rewritten for the after-3.2 surfaces:
 *   Phase 3.2 (commit cd21176 "retire totalreclaw_* agent tools")
 *   retired the `totalreclaw_pair` / `remember` / `recall` / `forget`
 *   agent tools. The pair surface moved to the CLI wizard
 *   (`api.registerCli`) + four HTTP routes (`api.registerHttpRoute`);
 *   recall moved to the native `memory_search` / `memory_get` tools
 *   registered via the OpenClaw-native
 *   `api.registerTool(tool, { names: [...] })` signature (not the
 *   `api.registerTool({ name: '...' })` object form the old test
 *   scanned for). The memory_* tools operate on the ENCRYPTION key
 *   and never touch the recovery phrase, so they are NOT in scope for
 *   this registry (inclusion criterion: "could this surface generate,
 *   accept, or return a recovery phrase?").
 *
 * What this test asserts (current contract):
 *   1. The retired phrase-adjacent agent tool names (`totalreclaw_onboard`,
 *      `totalreclaw_setup`, `totalreclaw_onboarding_start`) are NOT
 *      registered as agent tools anywhere in `index.ts`.
 *   2. The retired `totalreclaw_remember` / `recall` / `forget` / `pair`
 *      agent tools are NOT registered (they were the pre-3.2 capture
 *      surface; Phase 3.2 deleted them in lockstep).
 *   3. The pair surface — the load-bearing agent-facilitated setup path
 *      the guard protects — IS registered, via BOTH of its current
 *      surfaces: (a) the `api.registerCli` call that wires
 *      `openclaw totalreclaw onboard` / `pair`, and (b) the four
 *      `api.registerHttpRoute` calls that expose the `/pair/*` HTTP
 *      routes the QR-pairing browser page calls (the actual path shapes
 *      are asserted in `pair-http-route-registration.test.ts`).
 *   4. No `api.registerTool({ name: '<phrase-adjacent-token>' })` call
 *      exists — defense-in-depth: any future tool registration that
 *      accidentally reintroduces a phrase-handling surface would almost
 *      always include one of the forbidden substrings.
 *
 * Scan strategy: read index.ts as text and search for the registration
 * call patterns (`api.registerTool`, `api.registerCli`,
 * `api.registerHttpRoute`). We match on the `name:` literal inside the
 * object passed to `registerTool`, the `path:` literal inside the
 * object passed to `registerHttpRoute`, and the literal `api.registerCli`
 * token for the CLI surface. This is a coarser scan than parsing TS but
 * sufficient for catching an accidental re-registration.
 *
 * Run with: `npx tsx phrase-safety-registry.test.ts`
 */

import fs from 'node:fs';
import path from 'node:path';

let passed = 0;
let failed = 0;

function assert(condition: boolean, name: string): void {
  const n = passed + failed + 1;
  if (condition) {
    console.log(`ok ${n} - ${name}`);
    passed++;
  } else {
    console.log(`not ok ${n} - ${name}`);
    failed++;
  }
}

const INDEX_PATH = path.resolve(import.meta.dirname, 'index.ts');
const src = fs.readFileSync(INDEX_PATH, 'utf-8');

/**
 * Extract tool names from `api.registerTool({ name: '<name>', ... })`
 * (the object-form registration). The native memory tools use a
 * different signature — `api.registerTool(tool, { names: [...] })` —
 * and are intentionally NOT captured here: memory_search/memory_get
 * operate on the encryption key, never the recovery phrase, so they
 * are out of scope for this registry.
 */
function extractRegisteredToolNames(source: string): string[] {
  const names: string[] = [];
  const openerRe = /api\.registerTool\s*\(\s*\{/g;
  let m: RegExpExecArray | null;
  while ((m = openerRe.exec(source)) !== null) {
    const start = m.index + m[0].length;
    const window = source.slice(start, start + 3000);
    const nameRe = /\bname:\s*['"]([a-zA-Z0-9_]+)['"]/;
    const nm = nameRe.exec(window);
    if (nm) names.push(nm[1]);
  }
  return names;
}

/**
 * Count `api.registerHttpRoute` calls. The pair surface registers its
 * four `/pair/*` routes this way. The path values at the call site are
 * variable references (`bundle.finishPath`, etc.) resolved from
 * `pair-http.ts`'s `${apiBase}/finish` templates — not string literals
 * — so this scan counts the registration calls themselves. The actual
 * path shapes (all four must contain `/pair/`) are covered by
 * `pair-http-route-registration.test.ts`.
 */
function countRegisteredHttpRoutes(source: string): number {
  const matches = source.match(/api\.registerHttpRoute!?\s*\(/g);
  return matches ? matches.length : 0;
}

const registered = extractRegisteredToolNames(src);
const httpRouteCount = countRegisteredHttpRoutes(src);

// ---------------------------------------------------------------------------
// 1. Retired phrase-adjacent agent tools are NOT registered
// ---------------------------------------------------------------------------
const RETIRED_PHRASE_ADJACENT = [
  'totalreclaw_onboard', // removed in rc.4
  'totalreclaw_setup', // removed in rc.5
  'totalreclaw_onboarding_start', // removed in rc.5
];
for (const t of RETIRED_PHRASE_ADJACENT) {
  assert(
    !registered.includes(t),
    `phrase-safety: ${t} is NOT registered (retired)`,
  );
}

// ---------------------------------------------------------------------------
// 2. Retired totalreclaw_* capture tools are NOT registered
//    (Phase 3.2 — commit cd21176. The pair surface moved to CLI + HTTP;
//    recall moved to native memory_search/memory_get which operate on
//    the encryption key, not the phrase, and use a different signature.)
// ---------------------------------------------------------------------------
const RETIRED_CAPTURE_TOOLS = [
  'totalreclaw_pair',
  'totalreclaw_remember',
  'totalreclaw_recall',
  'totalreclaw_forget',
];
for (const t of RETIRED_CAPTURE_TOOLS) {
  assert(
    !registered.includes(t),
    `phrase-safety: ${t} is NOT registered (retired in Phase 3.2 — moved to CLI/HTTP/native)`,
  );
}

// ---------------------------------------------------------------------------
// 3. The pair surface IS registered (load-bearing phrase-safety surface)
//
// The QR-pair flow is the ONLY agent-facilitated setup path the guard
// protects. After 3.2 it is registered through two surfaces, BOTH of
// which must remain present:
//   (a) api.registerCli — wires `openclaw totalreclaw onboard` / `pair`
//       (the leak-free TTY wizard where a phrase is generated/accepted).
//   (b) api.registerHttpRoute — the four `/pair/*` HTTP routes the
//       browser pairing page calls (start/respond/finish/status).
// ---------------------------------------------------------------------------
assert(
  /api\.registerCli\s*\(/.test(src),
  'phrase-safety: pair CLI surface is registered (api.registerCli call present — wires `openclaw totalreclaw pair/onboard`)',
);

const pairRoutes = httpRouteCount;
assert(
  pairRoutes >= 4,
  `phrase-safety: pair HTTP surface is registered (>=4 registerHttpRoute calls for the /pair/* routes; found ${pairRoutes})`,
);

// ---------------------------------------------------------------------------
// 4. No phrase-adjacent agent-tool name is registered (defense-in-depth)
// ---------------------------------------------------------------------------
const FORBIDDEN_SUBSTRINGS = [
  'onboard_generate',
  'generate_phrase',
  'generate_mnemonic',
  'restore_phrase',
  'restore_mnemonic',
  'mnemonic',
];
for (const forbidden of FORBIDDEN_SUBSTRINGS) {
  const hits = registered.filter((n) => n.toLowerCase().includes(forbidden));
  assert(
    hits.length === 0,
    `phrase-safety: no registered tool name contains "${forbidden}" (hits: ${JSON.stringify(hits)})`,
  );
}

// ---------------------------------------------------------------------------
// 5. Summary
// ---------------------------------------------------------------------------
console.log(`# fail: ${failed}`);
console.log(`# ${passed}/${passed + failed} passed`);
if (failed > 0) {
  console.log('SOME TESTS FAILED');
  process.exit(1);
}
console.log('ALL TESTS PASSED');
