/**
 * skill-md-hybrid-primary.test.ts (3.3.9-rc.1)
 *
 * Asserts that both skill/plugin/SKILL.md and skill/SKILL.md contain:
 *   1. The relay-based architecture assertion ("TotalReclaw is RELAY-BASED")
 *   2. The hallucination-guard denylist (all required forbidden words)
 *   3. Hybrid-primary CLI path instructions (tr CLI as primary)
 *   4. Autonomous pair call (no consent gate language)
 *   5. JSON flag documentation in CLI reference
 *
 * Run with: `npx tsx skill-md-hybrid-primary.test.ts`
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
// 1. Relay-based architecture assertion (both files)
// ---------------------------------------------------------------------------

// 3.3.11-rc.2: phrasing migrated from "RELAY-BASED + NO local-only mode"
// to the more accurate "decentralized network" framing — relay forwards
// ciphertext but storage is on-chain. Tests now accept either phrasing
// (older versions kept the relay-based framing; rc.2+ adds decentralized).
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

// rc.2 added centralized-custody bans alongside the existing local-only bans.
// At least one of the two anti-centralization claims must be present.
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
// 2. Hallucination-guard denylist (both files)
// ---------------------------------------------------------------------------

const REQUIRED_DENYLIST_ENTRIES = [
  '"local"',
  '"local-only"',
  '"stored locally"',
  '"on disk"',
  '"without an account"',
  '"local memory"',
  '"local storage"',
];

for (const entry of REQUIRED_DENYLIST_ENTRIES) {
  assert(
    pluginSkillMd.includes(entry),
    `skill/plugin/SKILL.md: forbidden vocabulary denylist contains ${entry}`,
  );
  assert(
    topLevelSkillMd.includes(entry),
    `skill/SKILL.md: forbidden vocabulary denylist contains ${entry}`,
  );
}

// ---------------------------------------------------------------------------
// 3. Hybrid-primary CLI path (plugin SKILL.md)
// ---------------------------------------------------------------------------

assert(
  pluginSkillMd.includes('tr-cli.js'),
  'skill/plugin/SKILL.md: references tr-cli.js as primary path',
);

assert(
  pluginSkillMd.includes('hybrid-primary'),
  'skill/plugin/SKILL.md: mentions hybrid-primary architecture',
);

assert(
  pluginSkillMd.includes('Never rely on `totalreclaw_*` tool binding'),
  'skill/plugin/SKILL.md: instructs agent NOT to rely on tool binding',
);

assert(
  pluginSkillMd.includes('status --json'),
  'skill/plugin/SKILL.md: CLI reference includes status --json',
);

assert(
  pluginSkillMd.includes('pair --json'),
  'skill/plugin/SKILL.md: CLI reference includes pair --json',
);

assert(
  pluginSkillMd.includes('remember --json'),
  'skill/plugin/SKILL.md: CLI reference includes remember --json',
);

assert(
  pluginSkillMd.includes('recall --json'),
  'skill/plugin/SKILL.md: CLI reference includes recall --json',
);

// ---------------------------------------------------------------------------
// 4. Autonomous pair call — no consent gate language
// ---------------------------------------------------------------------------

// The plugin SKILL.md must say "no consent gate" or "UNCONDITIONAL"
assert(
  pluginSkillMd.includes('no consent gate') || pluginSkillMd.includes('UNCONDITIONAL'),
  'skill/plugin/SKILL.md: pair step is unconditional (no consent gate)',
);

// The SKILL.md must NOT instruct the agent TO ask permission before pairing.
// It's acceptable for consent-gate phrases to appear in "Do NOT ask X" examples.
// Patterns that would only appear if the agent was told TO ask:
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
// 5. JSON output shapes documented
// ---------------------------------------------------------------------------

// status --json shape
assert(
  pluginSkillMd.includes('"hybrid_mode"') || pluginSkillMd.includes('hybrid_mode'),
  'skill/plugin/SKILL.md: documents hybrid_mode field in status --json output',
);

// pair --json shape — url and pin keys
assert(
  pluginSkillMd.includes('"url"') && pluginSkillMd.includes('"pin"'),
  'skill/plugin/SKILL.md: documents url and pin keys in pair --json output',
);

// recall --json shape — results key
assert(
  pluginSkillMd.includes('"results"') && pluginSkillMd.includes('"score"'),
  'skill/plugin/SKILL.md: documents results and score keys in recall --json output',
);

// ---------------------------------------------------------------------------
// 6. Setup flow: CLI verify BEFORE tool-binding check
// ---------------------------------------------------------------------------

// The setup flow must NOT tell agent to wait for tool binding after install
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
// 7. Version consistency in plugin SKILL.md frontmatter
// ---------------------------------------------------------------------------

assert(
  /^version: 3\.3\.(9|1\d)-rc\./m.test(pluginSkillMd),
  'skill/plugin/SKILL.md: frontmatter version is 3.3.9-rc.N or 3.3.1[0-9]-rc.N',
);

// ---------------------------------------------------------------------------
// 8. Plugin-driven setup (3.3.12-rc.7 — SKILL.md collapse 2026-05-10)
// ---------------------------------------------------------------------------
//
// rc.7 removed the user-visible-line choreography from SKILL.md. The plugin now
// drives setup autonomously: it auto-creates a pair session, writes
// ~/.totalreclaw/.pair-pending.json with {url, pin, sid, expires_at_ms}, and
// injects a `before_agent_start` context block to the agent. The agent's job
// shrinks to: surface the injected URL+PIN verbatim. Tests that asserted
// "MANDATORY ACK", numbered-line wording, forbidden/required ack order, and
// "skipping line 1 entirely" were dropped because those rules were stripped
// from SKILL.md per the rc.7 collapse — the plugin's hook injection IS the
// line now, not the agent's narration.
//
// New assertions for the rc.7 pivot:

assert(
  pluginSkillMd.includes('.pair-pending.json'),
  'skill/plugin/SKILL.md: references the pair-pending file written by the plugin',
);

assert(
  /before_agent_start/.test(pluginSkillMd),
  'skill/plugin/SKILL.md: references the before_agent_start hook injection',
);

// The agent must be told to surface the injected values verbatim, not invent.
assert(
  /VERBATIM/i.test(pluginSkillMd) || /verbatim/.test(pluginSkillMd),
  'skill/plugin/SKILL.md: instructs agent to surface URL+PIN verbatim from injected context',
);

assert(
  /never invent values|do not invent|never modify|do not modify/i.test(pluginSkillMd),
  'skill/plugin/SKILL.md: warns agent NOT to invent or modify pair values',
);

// ---------------------------------------------------------------------------

console.log(`\n# ${passed} passed, ${failed} failed`);
process.exit(failed === 0 ? 0 : 1);
