/**
 * 3.3.1-rc.4 — phrase-safety contract tests.
 *
 * Contract: NO agent tool registered by the TotalReclaw plugin may
 * generate, return, or accept a recovery phrase. The ONLY approved
 * agent-facilitated setup surface is `totalreclaw_pair` (browser-side
 * crypto keeps the phrase out of the LLM round-trip by construction).
 *
 * Governed by:
 *   ~/.claude/projects/-Users-pdiogo-Documents-code-totalreclaw-internal/
 *     memory/project_phrase_safety_rule.md
 *
 * Absolute rule: "recovery phrase MUST NEVER cross the LLM context in
 * ANY form — not echoed, not in tool-call stdout, not in tool-result
 * payloads, not in agent reasoning."
 *
 * What this test asserts:
 *   1. `totalreclaw_onboard` is NOT present as a `registerTool` name
 *      anywhere in `index.ts`. (rc.3 registered it; rc.4 removed it.)
 *   2. `totalreclaw_setup` and `totalreclaw_onboarding_start` are NOT
 *      present either. (rc.4 kept them as neutered pointer stubs; rc.5
 *      deletes both — see the rc.4 auto-QA carve-out in the PR body.)
 *   3. `totalreclaw_pair` IS present (the approved replacement).
 *   4. No tool name containing a phrase-adjacent token (`onboard_generate`,
 *      `restore_phrase`, `mnemonic`, `generate_phrase`) is registered.
 *   5. The scan is defense-in-depth — a text search, not an AST walk —
 *      because a new registration that accidentally ships a phrase
 *      surface would almost always include one of these tokens.
 *
 * Scan strategy: read index.ts as text and search for the
 * `api.registerTool({ name: '...' }` pattern and `{ name: '...' }` tool
 * registrations. We match on the `name:` literal inside the object
 * passed to `registerTool`. This is a coarser scan than parsing TS but
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
 * Extract the set of tool names passed to `api.registerTool({ name: '<name>', ... })`.
 *
 * Matches both single and double-quoted string literals. The regex is
 * anchored to the `registerTool(` opening so literals elsewhere in the
 * file (descriptions, comments, error messages) are not counted.
 */
function extractRegisteredToolNames(source: string): string[] {
  const names: string[] = [];
  // Find every `api.registerTool(` call and the next `name: '...'`
  // literal inside the same call block. We approximate "inside the same
  // call block" by taking the first `name:` literal within 2000 chars
  // of the opening paren — registerTool blocks are big (schemas + execute
  // bodies) but 2000 chars is enough for all current ones.
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

const registered = extractRegisteredToolNames(src);

// ---------------------------------------------------------------------------
// 1. totalreclaw_onboard is NOT registered
// ---------------------------------------------------------------------------
assert(
  !registered.includes('totalreclaw_onboard'),
  'phrase-safety: totalreclaw_onboard is NOT registered (removed in rc.4)',
);

// ---------------------------------------------------------------------------
// 1b. totalreclaw_setup and totalreclaw_onboarding_start are NOT
//     registered (rc.5 removes the rc.4 neutered stubs — closes the
//     auto-QA carve-out that flagged them as future-regression
//     surface even though they couldn't leak a phrase today).
// ---------------------------------------------------------------------------
assert(
  !registered.includes('totalreclaw_setup'),
  'phrase-safety: totalreclaw_setup is NOT registered (removed in rc.5)',
);
assert(
  !registered.includes('totalreclaw_onboarding_start'),
  'phrase-safety: totalreclaw_onboarding_start is NOT registered (removed in rc.5)',
);

// ---------------------------------------------------------------------------
// 2. totalreclaw_pair IS registered (the approved replacement)
// ---------------------------------------------------------------------------
assert(
  registered.includes('totalreclaw_pair'),
  'phrase-safety: totalreclaw_pair IS registered',
);

// ---------------------------------------------------------------------------
// 3. No other phrase-adjacent tool name is registered
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
// 4. Known-safe tool names ARE registered (regression guard — if this
// count drops unexpectedly the scan logic broke, not the registry)
// ---------------------------------------------------------------------------
const EXPECTED_SAFE = [
  'totalreclaw_remember',
  'totalreclaw_recall',
  'totalreclaw_forget',
  'totalreclaw_pair',
];
for (const t of EXPECTED_SAFE) {
  assert(
    registered.includes(t),
    `sanity: ${t} is registered (regression guard)`,
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
