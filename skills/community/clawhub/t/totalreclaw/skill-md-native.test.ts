/**
 * skill-md-native.test.ts (3.3.12-rc.13 — native memory integration, PR #385)
 *
 * Asserts the content of skill/plugin/SKILL.md AND skill/SKILL.md.
 *
 * HISTORY — this file was renamed from `skill-md-hybrid-primary.test.ts` when
 * PR #383 retired the hybrid-primary flow and PR #385 rewrote SKILL.md for the
 * native `kind:"memory"` provider integration. The old test asserted the
 * retired flow (`hybrid-primary`, `recall --json`, `hybrid_mode` status field,
 * `.pair-pending.json`, `before_agent_start` hook injection, `totalreclaw_*`
 * tool binding). Those assertions are now INVERTED — they guard against the
 * retired flow leaking back into SKILL.md (same pattern manifest-shape.test.ts
 * uses for the retired `totalreclaw_*` contracts.tools entries).
 *
 * What this test now checks:
 *   1. Architecture truth (decentralized network / relay-based) — both files
 *   2. Hallucination-guard forbidden vocab denylist — both files
 *   3. Native-flow recall contract (memory_search / memory_get) — plugin file
 *   4. User-initiated `tr pair` (NOT auto-pair-on-load) — plugin file
 *   5. Autonomous `/totalreclaw-restart` (agent-driven, never user-manual) — plugin file
 *   6. Unconditional pair (no consent gate) — plugin file
 *   7. JSON output shapes documented (pair --json url/pin) — plugin file
 *   8. Verbatim / no-invent surface instruction — plugin file
 *   9. Version frontmatter shape — plugin file
 *  10. REGRESSION GUARDS — retired hybrid-primary flow must NOT reappear — plugin file
 *
 * The top-level skill/SKILL.md is intentionally NOT rewritten by PR #385
 * (it still ships the legacy hybrid-primary content for back-compat on older
 * runtimes). Assertions against it here cover only the stable invariants that
 * hold in BOTH the old and new phrasing: architecture truth, anti-centralized-
 * custody ban, and the forbidden-vocab denylist. Native-flow + regression
 * guards apply to the plugin file only.
 *
 * Run with: `npx tsx skill-md-native.test.ts`
 */

import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

let passed = 0;
let failed = 0;

function assert(cond: boolean, name: string): void {
  const n = passed + failed + 1;
  if (cond) {
    console.log(`ok ${n} - ${name}`);
    passed++;
  } else {
    console.log(`not ok ${n} - ${name}`);
    failed++;
  }
}

// ---------------------------------------------------------------------------
// File paths
// ---------------------------------------------------------------------------

const pluginSkillMdPath = path.join(__dirname, 'SKILL.md');
const topLevelSkillMdPath = path.resolve(__dirname, '..', '..', 'skill', 'SKILL.md');

const pluginSkillMd = fs.readFileSync(pluginSkillMdPath, 'utf8');
const topLevelSkillMd = fs.readFileSync(topLevelSkillMdPath, 'utf8');

// ---------------------------------------------------------------------------
// 1. Architecture truth (decentralized network / relay-based) — both files
// ---------------------------------------------------------------------------

// Phrasing migrated across versions: older "RELAY-BASED + NO local-only mode"
// → rc.2 "decentralized network" framing (relay forwards ciphertext, storage
// on-chain). All three phrasings are accurate; tests accept any.
const HAS_ARCHITECTURE_TRUTH_PLUGIN =
  pluginSkillMd.includes('TotalReclaw is RELAY-BASED') ||
  pluginSkillMd.includes('DECENTRALIZED NETWORK') ||
  pluginSkillMd.includes('decentralized network');

assert(
  HAS_ARCHITECTURE_TRUTH_PLUGIN,
  'skill/plugin/SKILL.md: contains architecture truth (RELAY-BASED or DECENTRALIZED NETWORK)',
);

const HAS_ARCHITECTURE_TRUTH_TOPLEVEL =
  topLevelSkillMd.includes('TotalReclaw is RELAY-BASED') ||
  topLevelSkillMd.includes('DECENTRALIZED NETWORK') ||
  topLevelSkillMd.includes('decentralized network');

assert(
  HAS_ARCHITECTURE_TRUTH_TOPLEVEL,
  'skill/SKILL.md: contains architecture truth (RELAY-BASED or DECENTRALIZED NETWORK)',
);

// Anti-centralized-custody ban (local-only OR single-company-server direction).
const HAS_NO_LOCAL_OR_NO_SERVER_PLUGIN =
  pluginSkillMd.includes('NO local-only mode') ||
  pluginSkillMd.includes('not on a single company server') ||
  pluginSkillMd.includes('not on any single company');

assert(
  HAS_NO_LOCAL_OR_NO_SERVER_PLUGIN,
  'skill/plugin/SKILL.md: anti-centralized-custody / no-local-only assertion present',
);

const HAS_NO_LOCAL_OR_NO_SERVER_TOPLEVEL =
  topLevelSkillMd.includes('NO local-only mode') ||
  topLevelSkillMd.includes('not on a single company server') ||
  topLevelSkillMd.includes('not on any single company');

assert(
  HAS_NO_LOCAL_OR_NO_SERVER_TOPLEVEL,
  'skill/SKILL.md: anti-centralized-custody / no-local-only assertion present',
);

// ---------------------------------------------------------------------------
// 2. Hallucination-guard forbidden vocab denylist — both files
// ---------------------------------------------------------------------------

// Common denylist that MUST appear in BOTH files. Note: PR #385's rewritten
// plugin SKILL.md dropped "local memory" and "local storage" from the explicit
// list (the remaining entries "local" and "local-only" already subsume them,
// and the new copy is much tighter). The top-level SKILL.md still carries the
// full legacy list. Assert the intersection here; assert the legacy extras
// against the top-level file only (below).
const COMMON_DENYLIST = [
  '"local"',
  '"local-only"',
  '"stored locally"',
  '"on disk"',
  '"without an account"',
];

for (const entry of COMMON_DENYLIST) {
  assert(
    pluginSkillMd.includes(entry),
    `skill/plugin/SKILL.md: forbidden vocabulary denylist contains ${entry}`,
  );
  assert(
    topLevelSkillMd.includes(entry),
    `skill/SKILL.md: forbidden vocabulary denylist contains ${entry}`,
  );
}

// Legacy denylist entries still present in the longer top-level SKILL.md.
// (Plugin SKILL.md no longer lists these explicitly — see comment above.)
const TOPLEVEL_ONLY_DENYLIST = ['"local memory"', '"local storage"'];
for (const entry of TOPLEVEL_ONLY_DENYLIST) {
  assert(
    topLevelSkillMd.includes(entry),
    `skill/SKILL.md: forbidden vocabulary denylist contains ${entry}`,
  );
}

// ---------------------------------------------------------------------------
// 3. Native-flow recall contract (memory_search / memory_get) — plugin file
// ---------------------------------------------------------------------------

// PR #383/385: recall runs through OpenClaw's native memory tools, NOT a
// plugin-registered totalreclaw_recall tool. SKILL.md MUST name both tools.
assert(
  pluginSkillMd.includes('memory_search'),
  'skill/plugin/SKILL.md: documents native recall tool memory_search',
);
assert(
  pluginSkillMd.includes('memory_get'),
  'skill/plugin/SKILL.md: documents native recall tool memory_get',
);

// ---------------------------------------------------------------------------
// 4. User-initiated `tr pair` (NOT auto-pair-on-load) — plugin file
// ---------------------------------------------------------------------------

// PR #385: pairing is a deliberate, user-initiated QR flow. SKILL.md MUST
// (a) name `tr pair --json`, and (b) state the plugin does NOT auto-pair.
assert(
  pluginSkillMd.includes('pair --json'),
  'skill/plugin/SKILL.md: CLI reference includes pair --json',
);
// SKILL.md renders this as "does **not** auto-pair" (markdown bold splits the
// phrase), so strip `**` before matching rather than trust literal spacing.
assert(
  /not\s+auto-pair/i.test(pluginSkillMd.replace(/\*\*/g, '')),
  'skill/plugin/SKILL.md: states plugin does NOT auto-pair on load',
);

// ---------------------------------------------------------------------------
// 5. Autonomous `/totalreclaw-restart` (agent-driven, never user-manual) — plugin file
// ---------------------------------------------------------------------------

// The restart slash command is issued AUTONOMOUSLY by the agent when native
// tools aren't bound; the user must NEVER be asked to do a manual restart.
assert(
  pluginSkillMd.includes('/totalreclaw-restart'),
  'skill/plugin/SKILL.md: references autonomous /totalreclaw-restart slash command',
);
assert(
  /\bautonomous/i.test(pluginSkillMd),
  'skill/plugin/SKILL.md: marks /totalreclaw-restart as autonomous (agent-driven)',
);

// ---------------------------------------------------------------------------
// 6. Unconditional pair (no consent gate) — plugin file
// ---------------------------------------------------------------------------

assert(
  pluginSkillMd.includes('no consent gate') || pluginSkillMd.includes('UNCONDITIONAL'),
  'skill/plugin/SKILL.md: pair step is unconditional (no consent gate)',
);

const STRICTLY_FORBIDDEN_CONSENT_PATTERNS = [
  'Should I set up an account?',
  'Do you want me to pair',
  'Shall I pair',
  'Ask the user before pairing',
];
for (const pattern of STRICTLY_FORBIDDEN_CONSENT_PATTERNS) {
  assert(
    !pluginSkillMd.includes(pattern),
    `skill/plugin/SKILL.md: does NOT instruct agent to ask: "${pattern}"`,
  );
}

// ---------------------------------------------------------------------------
// 7. JSON output shapes documented — plugin file
// ---------------------------------------------------------------------------

// CLI references that survived the rewrite.
assert(
  pluginSkillMd.includes('status --json'),
  'skill/plugin/SKILL.md: CLI reference includes status --json',
);
assert(
  pluginSkillMd.includes('remember --json'),
  'skill/plugin/SKILL.md: CLI reference includes remember --json',
);

// pair --json shape — url and pin keys.
assert(
  pluginSkillMd.includes('"url"') && pluginSkillMd.includes('"pin"'),
  'skill/plugin/SKILL.md: documents url and pin keys in pair --json output',
);

// ---------------------------------------------------------------------------
// 8. Verbatim / no-invent surface instruction — plugin file
// ---------------------------------------------------------------------------

// The agent must surface URL+PIN verbatim from the pair JSON and warned not
// to invent or modify the values.
assert(
  /VERBATIM/i.test(pluginSkillMd) || /verbatim/.test(pluginSkillMd),
  'skill/plugin/SKILL.md: instructs agent to surface URL+PIN verbatim',
);
assert(
  /never invent values|do not invent|never modify|do not modify/i.test(pluginSkillMd),
  'skill/plugin/SKILL.md: warns agent NOT to invent or modify pair values',
);

// Setup flow must NOT tell agent to wait for tool binding after install.
const FORBIDDEN_TOOLBIND_WAIT = [
  'wait for tool-bind',
  'confirm `totalreclaw_pair` is in your toolset',
  'confirm that `totalreclaw_pair` is bound',
];
for (const pattern of FORBIDDEN_TOOLBIND_WAIT) {
  assert(
    !pluginSkillMd.includes(pattern),
    `skill/plugin/SKILL.md: does NOT contain tool-binding wait: "${pattern}"`,
  );
}

// ---------------------------------------------------------------------------
// 9. Version frontmatter shape — plugin file
// ---------------------------------------------------------------------------

assert(
  /^version: 3\.3\.(9|1\d)-rc\./m.test(pluginSkillMd),
  'skill/plugin/SKILL.md: frontmatter version is 3.3.9-rc.N or 3.3.1[0-9]-rc.N',
);

// ---------------------------------------------------------------------------
// 10. REGRESSION GUARDS — retired hybrid-primary flow must NOT reappear
// ---------------------------------------------------------------------------
//
// These assertions are INVERTED from the old `skill-md-hybrid-primary.test.ts`.
// PR #383 retired the hybrid-primary flow and PR #385 rewrote SKILL.md. The
// patterns below were REQUIRED by the old test; they must now stay ABSENT so
// a future half-revert (re-introducing the retired framing) fails this test
// loudly. Same guard pattern manifest-shape.test.ts uses for the retired
// `totalreclaw_*` contracts.tools entries.

// 10a. "hybrid-primary" architecture framing — retired.
assert(
  !pluginSkillMd.includes('hybrid-primary'),
  'skill/plugin/SKILL.md: does NOT mention retired hybrid-primary architecture',
);

// 10b. "Never rely on totalreclaw_* tool binding" — retired (the tools are gone,
// not merely unreliable). SKILL.md now documents the native memory contract
// positively instead of hedging about tool binding.
assert(
  !pluginSkillMd.includes('Never rely on `totalreclaw_*` tool binding'),
  'skill/plugin/SKILL.md: does NOT instruct agent to avoid relying on tool binding (retired)',
);

// 10c. `recall --json` CLI — retired. Recall is now `memory_search`; the `tr
// recall` shim was removed in Task 3.3a.
assert(
  !pluginSkillMd.includes('recall --json'),
  'skill/plugin/SKILL.md: does NOT document retired recall --json CLI',
);

// 10d. `hybrid_mode` field in status --json — retired alongside hybrid-primary.
assert(
  !pluginSkillMd.includes('hybrid_mode'),
  'skill/plugin/SKILL.md: does NOT document retired hybrid_mode status field',
);

// 10e. `results` / `score` keys in recall --json — retired with recall --json.
// (Native memory_search has its own OpenClaw-defined shape; documenting the
// old `tr recall` shape here would mislead.)
assert(
  !(pluginSkillMd.includes('"results"') && pluginSkillMd.includes('"score"')),
  'skill/plugin/SKILL.md: does NOT document retired results/score recall-shape keys',
);

// 10f. `.pair-pending.json` file — retired. PR #385 replaced plugin-driven
// auto-pair + pair-pending file with user-initiated `tr pair`.
assert(
  !pluginSkillMd.includes('.pair-pending.json'),
  'skill/plugin/SKILL.md: does NOT reference retired .pair-pending.json file',
);

// 10g. `before_agent_start` hook injection — retired. The plugin no longer
// injects a setup-context block via this hook; SKILL.md is now the canonical
// setup surface.
assert(
  !/before_agent_start/.test(pluginSkillMd),
  'skill/plugin/SKILL.md: does NOT reference retired before_agent_start hook injection',
);

// 10h. `totalreclaw_remember` / `totalreclaw_recall` documented as agent tools.
// These are mentioned ONCE in SKILL.md (line ~78) as part of the sentence
// "The legacy totalreclaw_* agent tools and the tr recall CLI are retired".
// That retirement notice is expected and good. What's NOT allowed is a second
// occurrence that would indicate they're documented as live tools (parameter
// table, "when to use" section, etc.). Assert at most one occurrence of each.
{
  const countRemember = (pluginSkillMd.match(/totalreclaw_remember/g) ?? []).length;
  assert(
    countRemember <= 1,
    `skill/plugin/SKILL.md: totalreclaw_remember appears at most once (retirement notice only), got ${countRemember}`,
  );
  const countRecall = (pluginSkillMd.match(/totalreclaw_recall/g) ?? []).length;
  assert(
    countRecall <= 1,
    `skill/plugin/SKILL.md: totalreclaw_recall appears at most once (retirement notice only), got ${countRecall}`,
  );
}

// ---------------------------------------------------------------------------

console.log(`\n# ${passed} passed, ${failed} failed`);
process.exit(failed === 0 ? 0 : 1);
