/**
 * manifest-shape.test.ts — Regression guard for the manifest/JS symmetry
 * required on OpenClaw 2026.5.2+ (re-added in 3.3.8-rc.1).
 *
 * Background — 2026.5.2 cold-start gate REVERSED the 3.3.0-rc.6 rule:
 *   OpenClaw 2026.5.2's `resolveGatewayStartupPluginPlanFromRegistry` calls
 *   `shouldConsiderForGatewayStartup()` which checks `plugin.startup.memory`,
 *   derived from `hasKind(record.kind, "memory")`. Without `"kind": "memory"`
 *   in the manifest, the plugin gets `startup.memory = false` and is
 *   EXCLUDED from the cold-start loading plan. It only loaded via SIGTERM
 *   hot-reload (different code path that bypasses the startup planner).
 *
 *   Fix (3.3.8-rc.1): re-add `"kind": "memory"` to `openclaw.plugin.json`.
 *   The JS plugin definition in `index.ts` already declares
 *   `kind: 'memory' as const`. Manifest now matches — gateway includes the
 *   plugin in its cold-start plan and loads it on every boot.
 *
 *   This reverses the 3.3.0-rc.6 removal. The upstream OpenClaw condition
 *   flipped between 2026.4.x (excluded memory plugins from startup unless
 *   they had a channel) and 2026.5.2 (REQUIRES kind=memory for cold-start).
 *
 * This test asserts BOTH sides of the new symmetry:
 *   1. The manifest DOES declare `kind: "memory"` (cold-start gate on 2026.5.2).
 *   2. The JS plugin source DOES declare `kind: 'memory' as const` (memory-slot
 *      behaviour preserved).
 *
 * Implementation note on assertion 2:
 *   `index.ts` has a heavy init chain (onnxruntime-node, HuggingFace
 *   transformers, viem, protobufjs, etc.) that requires native addons and
 *   cannot be dynamically imported in a bare test runner without a full mock
 *   harness. We therefore inspect the `index.ts` source as text — a node-based
 *   regex check is precise, deterministic, and unambiguous for the single
 *   declaration site. The test comment near that declaration (`// Plugin
 *   definition`) makes the location stable. If the declaration is ever moved or
 *   refactored, this test fails loudly, which is the desired behaviour.
 *
 * References:
 *   - Research: docs/notes/RESEARCH-openclaw-http-route-plumbing-20260420-1608.md
 *     (totalreclaw-internal)
 *   - PR comment: totalreclaw-internal#21 comment 4282038854
 *   - Upstream bug: see "Upstream OpenClaw bug" section in the rc.6 PR body.
 *
 * Run with: npx tsx manifest-shape.test.ts
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __dirname = path.dirname(fileURLToPath(import.meta.url));

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

function assertEq<T>(actual: T, expected: T, name: string): void {
  const ok = JSON.stringify(actual) === JSON.stringify(expected);
  if (!ok) {
    console.log(`  actual:   ${JSON.stringify(actual)}`);
    console.log(`  expected: ${JSON.stringify(expected)}`);
  }
  assert(ok, name);
}

// ---------------------------------------------------------------------------
// 1. Manifest assertions
// ---------------------------------------------------------------------------

const manifestPath = path.join(__dirname, 'openclaw.plugin.json');
let manifest: Record<string, unknown>;

{
  let parseOk = true;
  try {
    const raw = fs.readFileSync(manifestPath, 'utf8');
    manifest = JSON.parse(raw) as Record<string, unknown>;
  } catch (err) {
    parseOk = false;
    manifest = {};
    console.log(`  error: ${String(err)}`);
  }

  assert(parseOk, 'openclaw.plugin.json is valid JSON');
}

{
  // 1a. (3.3.8-rc.1 reversal) OpenClaw 2026.5.2's
  // `resolveGatewayStartupPluginPlanFromRegistry` calls
  // `shouldConsiderForGatewayStartup()` which checks `plugin.startup.memory`,
  // derived from `hasKind(record.kind, "memory")`. Without `"kind": "memory"`,
  // the plugin gets `startup.memory = false` and is EXCLUDED from cold-start.
  // Plugin only loaded via SIGTERM hot-reload (which bypasses startup planner).
  // Re-adding `"kind": "memory"` to the manifest restores cold-start loading
  // on every gateway boot. This reverses the 3.3.0-rc.6 removal — the
  // upstream condition flipped between 2026.4.x and 2026.5.2.
  assert(
    'kind' in manifest,
    'openclaw.plugin.json contains "kind" field (cold-start loading on 2026.5.2)',
  );
}

{
  // 1b. Manifest "kind" === "memory" so the gateway treats this as a memory
  // plugin and includes it in the cold-start plan.
  const kindValue = manifest['kind'];
  assertEq(
    kindValue,
    'memory',
    'openclaw.plugin.json "kind" === "memory"',
  );
}

{
  // 1c. Raw-string guard: regex must MATCH `"kind": "memory"` in the source
  // to catch silent removals via merge or accidental edits.
  const raw = fs.readFileSync(manifestPath, 'utf8');
  const hasKindMemory = /"kind"\s*:\s*"memory"/.test(raw);
  assert(
    hasKindMemory,
    'openclaw.plugin.json source matches /"kind"\\s*:\\s*"memory"/ (raw regex guard)',
  );
}

{
  // 1d. Manifest still has "id", "name", "description" — basic shape sanity.
  assertEq(manifest['id'], 'totalreclaw', 'manifest id === "totalreclaw"');
  assertEq(manifest['name'], 'TotalReclaw', 'manifest name === "TotalReclaw"');
  assert(
    typeof manifest['description'] === 'string' && (manifest['description'] as string).length > 0,
    'manifest description is a non-empty string',
  );
}

{
  // 1e. (Task 2.8) contracts.tools must be a string array.
  const tools = (manifest as { contracts?: { tools?: unknown } }).contracts?.tools;
  assert(Array.isArray(tools), 'manifest contracts.tools is an array');
  assert(
    Array.isArray(tools) && tools.every((t) => typeof t === 'string'),
    'manifest contracts.tools entries are all strings',
  );
}

{
  // 1f. (Task 2.8) The native OpenClaw contract tools `memory_search` and
  // `memory_get` MUST be declared. Task 2.7 registers them via
  // `api.registerTool(..., { names: ['memory_search', 'memory_get'] })` in
  // `registerNativeMemory`. OpenClaw's loader enforces registered⊆declared
  // (see registry.registerTool → findUndeclaredPluginToolNames): a registered
  // tool that is NOT in contracts.tools triggers a level:"error" diagnostic
  // and the registration is silently dropped. So the declaration here is
  // load-bearing, not cosmetic.
  const tools = ((manifest as { contracts?: { tools?: string[] } }).contracts?.tools) ?? [];
  assert(
    tools.includes('memory_search'),
    'manifest contracts.tools includes "memory_search" (native contract tool, registered by Task 2.7)',
  );
  assert(
    tools.includes('memory_get'),
    'manifest contracts.tools includes "memory_get" (native contract tool, registered by Task 2.7)',
  );
}

{
  // 1g. (Task 3.2 — LOCKSTEP GUARD, flipped from Task 2.8) The 17 legacy
  // `totalreclaw_*` agent-tool names MUST NO LONGER be declared in
  // contracts.tools. Phase 3.2 retired them: the `api.registerTool(...)`
  // calls were removed from index.ts AND their contracts.tools entries were
  // removed from openclaw.plugin.json IN THE SAME COMMIT (the lockstep).
  //
  // Why both sides in one commit: OpenClaw's loader enforces
  // registered⊆declared (registry.registerTool → findUndeclaredPluginToolNames).
  //   - manifest entry without registration  → dead declaration (noise, not fatal)
  //   - registration without manifest entry  → level:"error" diagnostic +
  //     the registration is silently dropped on every boot
  //   - test guard flipped to `!includes` in the same commit so a future
  //     half-revert (re-adding either side alone) fails this test loudly.
  //
  // (Task 2.8 originally asserted the opposite — `tools.includes(name)` — as
  // a sequencing guard to prevent a premature half-drop before 3.2 landed.
  // This is the flip that 2.8's comment promised would happen at 3.2 time.)
  const tools = ((manifest as { contracts?: { tools?: string[] } }).contracts?.tools) ?? [];
  const retiredLegacyTools = [
    'totalreclaw_remember',
    'totalreclaw_recall',
    'totalreclaw_forget',
    'totalreclaw_export',
    'totalreclaw_status',
    'totalreclaw_preload_embedder',
    'totalreclaw_consolidate',
    'totalreclaw_pin',
    'totalreclaw_unpin',
    'totalreclaw_retype',
    'totalreclaw_set_scope',
    'totalreclaw_import_from',
    'totalreclaw_import_batch',
    'totalreclaw_upgrade',
    'totalreclaw_migrate',
    'totalreclaw_pair',
    'totalreclaw_report_qa_bug',
  ];
  for (const name of retiredLegacyTools) {
    assert(
      !tools.includes(name),
      `manifest contracts.tools does NOT include "${name}" (Phase 3.2 retirement — totalreclaw_* agent tools removed)`,
    );
  }
}

{
  // 1h. (Task 2.8) activation.onStartup === false — the plugin must NOT be
  // auto-started by the gateway on cold boot; it activates lazily when the
  // memory slot resolves to it. Mirrors the bundled memory-core manifest
  // (extensions/memory-core/openclaw.plugin.json). Field shape confirmed via
  // normalizeManifestActivation in manifest loader (2026.6.8): only
  // { onStartup: boolean } is consumed here.
  const activation = (manifest as { activation?: { onStartup?: unknown } }).activation;
  assert(
    activation !== undefined && typeof activation === 'object',
    'manifest has an "activation" object',
  );
  assertEq(
    (activation as { onStartup?: unknown })?.onStartup,
    false,
    'manifest activation.onStartup === false (lazy activation, matches memory-core)',
  );
}

// ---------------------------------------------------------------------------
// 2. JS plugin definition assertions (source inspection)
// ---------------------------------------------------------------------------

const indexPath = path.join(__dirname, 'index.ts');
const indexSrc = fs.readFileSync(indexPath, 'utf8');

{
  // 2a. index.ts must declare `kind: 'memory' as const` in the plugin object.
  // The OpenClaw loader re-merges this into record.kind (line 2090), so
  // memory-slot matching (config.slots.memory === "totalreclaw") still works.
  const hasKindMemory = /kind:\s*'memory'\s*as\s*const/.test(indexSrc);
  assert(
    hasKindMemory,
    "index.ts plugin definition contains `kind: 'memory' as const` (memory-slot matching preserved)",
  );
}

{
  // 2b. Regression guard: the JS plugin object is `export default plugin` —
  // confirm the export is present so we know the declaration we found above
  // is the same object that OpenClaw's loader receives.
  const hasExportDefault = /^export default plugin;/m.test(indexSrc);
  assert(
    hasExportDefault,
    'index.ts has `export default plugin;` (loader receives the checked object)',
  );
}

{
  // 2c. The JS declaration must NOT use `'gateway'` or any other kind value.
  // This guards against someone changing the kind in JS while fixing a future
  // unrelated issue, which would break memory-slot matching silently.
  const hasWrongKind = /kind:\s*'gateway'\s*as\s*const/.test(indexSrc);
  assert(
    !hasWrongKind,
    "index.ts plugin definition does NOT use `kind: 'gateway' as const`",
  );
}

// ---------------------------------------------------------------------------
// Summary
// ---------------------------------------------------------------------------

console.log(`# fail: ${failed}`);
console.log(`# ${passed}/${passed + failed} passed`);
if (failed > 0) {
  console.log('SOME TESTS FAILED');
  process.exit(1);
}
console.log('ALL TESTS PASSED');
