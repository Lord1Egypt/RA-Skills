/**
 * tr-cli-json-output.test.ts (3.3.9-rc.1)
 *
 * Asserts that tr-cli.ts correctly handles --json flag for all commands
 * by statically analysing the source. Since the CLI requires live relay
 * credentials for functional calls, we verify the code structure:
 *
 *   1. status --json: cmdStatus receives jsonMode param and writes JSON
 *   2. remember --json: cmdRemember pops --json flag, outputs JSON shape
 *   3. recall --json: cmdRecall pops --json flag + --limit, outputs JSON shape
 *   4. pair --json: delegates to pair-cli-relay outputMode='json' path
 *   5. All JSON outputs contain the expected required keys (via source grep)
 *
 * Additionally, verifies the --limit flag is handled in cmdRecall.
 *
 * Run with: `npx tsx tr-cli-json-output.test.ts`
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

const trCliPath = path.join(__dirname, 'tr-cli.ts');
const src = fs.readFileSync(trCliPath, 'utf8');

// ---------------------------------------------------------------------------
// 1. popFlag helper exists (used by status, remember, recall)
// ---------------------------------------------------------------------------

assert(
  /function popFlag/.test(src),
  'tr-cli.ts: popFlag helper function defined',
);

assert(
  /function popLimitFlag/.test(src),
  'tr-cli.ts: popLimitFlag helper function defined',
);

// ---------------------------------------------------------------------------
// 2. status --json
// ---------------------------------------------------------------------------

assert(
  /async function cmdStatus\(jsonMode: boolean\)/.test(src),
  'tr-cli.ts: cmdStatus accepts jsonMode: boolean parameter',
);

assert(
  /if \(jsonMode\)/.test(src),
  'tr-cli.ts: cmdStatus has JSON branch (if jsonMode)',
);

// Required keys in status JSON output
assert(
  src.includes('"version"') && src.includes('"onboarded"') && src.includes('"hybrid_mode"'),
  'tr-cli.ts: status --json output includes version, onboarded, hybrid_mode keys',
);

assert(
  src.includes('"next_step"'),
  'tr-cli.ts: status --json output includes next_step key',
);

assert(
  src.includes('"tool_count"'),
  'tr-cli.ts: status --json output includes tool_count key',
);

// ---------------------------------------------------------------------------
// 3. remember --json
// ---------------------------------------------------------------------------

assert(
  /async function cmdRemember\(rawArgs: string\[\]\)/.test(src),
  'tr-cli.ts: cmdRemember accepts rawArgs parameter',
);

assert(
  /popFlag\(rawArgs, '--json'\)/.test(src),
  "tr-cli.ts: cmdRemember calls popFlag(rawArgs, '--json')",
);

// JSON shape: {"ok":true,"id":"...","claim_count":N}
assert(
  src.includes('"ok"') && src.includes('"id"') && src.includes('"claim_count"'),
  'tr-cli.ts: remember --json output includes ok, id, claim_count keys',
);

// ---------------------------------------------------------------------------
// 4. recall --json + --limit
// ---------------------------------------------------------------------------

assert(
  /async function cmdRecall\(rawArgs: string\[\]\)/.test(src),
  'tr-cli.ts: cmdRecall accepts rawArgs parameter',
);

assert(
  /popFlag\(rawArgs, '--json'\)/.test(src) || /popFlag\(argsAfterJson.*'--json'\)/.test(src),
  "tr-cli.ts: cmdRecall calls popFlag for --json",
);

assert(
  /popLimitFlag/.test(src),
  'tr-cli.ts: cmdRecall uses popLimitFlag for --limit',
);

// JSON shape: {"results":[{"text":"...","score":0.8}]}
assert(
  src.includes('"results"'),
  'tr-cli.ts: recall --json output includes results key',
);

// Each result object must have text and score
assert(
  src.includes('"text"') && src.includes('"score"'),
  'tr-cli.ts: recall --json result objects include text and score keys',
);

// ---------------------------------------------------------------------------
// 5. pair --json: delegates to pair-cli-relay with json outputMode
// ---------------------------------------------------------------------------

assert(
  /outputMode.*'json'/.test(src) || /'json'.*outputMode/.test(src),
  "tr-cli.ts: cmdPair sets outputMode='json' when --json flag present",
);

assert(
  src.includes('pair-cli-relay'),
  'tr-cli.ts: cmdPair delegates to pair-cli-relay.js',
);

// ---------------------------------------------------------------------------
// 6. PLUGIN_VERSION constant present (auto-synced by sync-version.mjs from
//    package.json — accept any 3.3.x-rc.N format from rc.9-rc.1 onwards)
// ---------------------------------------------------------------------------

assert(
  /const PLUGIN_VERSION = '3\.3\.\d+(?:-rc\.\d+)?';/.test(src),
  "tr-cli.ts: const PLUGIN_VERSION declares a 3.3.x version (auto-synced by sync-version.mjs)",
);

// ---------------------------------------------------------------------------
// 7. --help documents JSON shapes
// ---------------------------------------------------------------------------

assert(
  src.includes('--json'),
  'tr-cli.ts: --help mentions --json flag',
);

assert(
  src.includes('JSON output shapes') || src.includes('--json'),
  'tr-cli.ts: --help references JSON output',
);

// ---------------------------------------------------------------------------
// 7b. On-chain wiring (3.3.12-rc.4) — remember/recall/forget MUST use the
//     subgraph + UserOp paths, NOT the defunct /v1/store and /v1/search
//     HTTP endpoints (those return 404 since the on-chain pivot).
// ---------------------------------------------------------------------------

assert(
  /from '\.\/subgraph-store\.js'/.test(src),
  "tr-cli.ts: imports from subgraph-store.js (on-chain submission path)",
);

assert(
  src.includes('submitFactBatchOnChain') && src.includes('encodeFactProtobuf'),
  "tr-cli.ts: imports submitFactBatchOnChain + encodeFactProtobuf for on-chain writes",
);

assert(
  src.includes('deriveSmartAccountAddress'),
  "tr-cli.ts: imports deriveSmartAccountAddress (Smart Account owner derivation)",
);

assert(
  /from '\.\/subgraph-search\.js'/.test(src),
  "tr-cli.ts: imports from subgraph-search.js (subgraph query path)",
);

assert(
  src.includes('searchSubgraph'),
  "tr-cli.ts: imports searchSubgraph for recall (replaces api.search /v1/search)",
);

// cmdRemember must call the on-chain path
const rememberFn = src.match(/async function cmdRemember[\s\S]*?\n\}\n/);
assert(
  rememberFn !== null && rememberFn[0].includes('submitFactBatchOnChain'),
  "tr-cli.ts: cmdRemember calls submitFactBatchOnChain (NOT api.store)",
);
assert(
  rememberFn !== null && !/ctx\.apiClient\.store\b/.test(rememberFn[0]),
  "tr-cli.ts: cmdRemember does NOT call ctx.apiClient.store (the /v1/store path is dead)",
);

// cmdRecall must call searchSubgraph
const recallFn = src.match(/async function cmdRecall[\s\S]*?\n\}\n/);
assert(
  recallFn !== null && recallFn[0].includes('searchSubgraph'),
  "tr-cli.ts: cmdRecall calls searchSubgraph (NOT api.search)",
);
assert(
  recallFn !== null && !/ctx\.apiClient\.search\b/.test(recallFn[0]),
  "tr-cli.ts: cmdRecall does NOT call ctx.apiClient.search (the /v1/search path is dead)",
);

// cmdForget must exist + call submitFactBatchOnChain (tombstone path)
assert(
  /async function cmdForget/.test(src),
  "tr-cli.ts: cmdForget defined (3.3.12-rc.4 — tombstone via UserOp)",
);
const forgetFn = src.match(/async function cmdForget[\s\S]*?\n\}\n/);
assert(
  forgetFn !== null && forgetFn[0].includes('submitFactBatchOnChain'),
  "tr-cli.ts: cmdForget submits an on-chain tombstone via submitFactBatchOnChain",
);
assert(
  forgetFn !== null && forgetFn[0].includes("source: 'tombstone'"),
  "tr-cli.ts: cmdForget writes a tombstone payload (source='tombstone')",
);

// cmdExport must exist + use the subgraph helper
assert(
  /async function cmdExport/.test(src),
  "tr-cli.ts: cmdExport defined (3.3.12-rc.4 — paginated subgraph dump)",
);
const exportFn = src.match(/async function cmdExport[\s\S]*?\n\}\n/);
assert(
  exportFn !== null && exportFn[0].includes('exportAllFacts'),
  "tr-cli.ts: cmdExport delegates to exportAllFacts (scanner-isolated helper)",
);

// buildContext must derive the wallet address (Smart Account) from the mnemonic
assert(
  /walletAddress\s*=\s*await\s+deriveSmartAccountAddress/.test(src),
  "tr-cli.ts: buildContext derives walletAddress from mnemonic via deriveSmartAccountAddress",
);

assert(
  /setRecoveryPhraseOverride\s*\(/.test(src),
  "tr-cli.ts: buildContext calls setRecoveryPhraseOverride so getSubgraphConfig sees the mnemonic",
);

// CRITICAL: verify NO calls to api.store / api.search (the defunct
// /v1/store and /v1/search HTTP paths). Comments may mention the strings
// for context — we only care that the methods aren't INVOKED.
assert(
  !/\bapiClient\.store\s*\(/.test(src) && !/\bapiClient\.search\s*\(/.test(src),
  "tr-cli.ts: never invokes apiClient.store / apiClient.search (defunct /v1/store + /v1/search)",
);

// ---------------------------------------------------------------------------
// 8. Phrase safety — mnemonic never in stdout
// ---------------------------------------------------------------------------

// The CLI must not write mnemonic to stdout — verify no mnemonic/recovery_phrase
// variable reaches process.stdout.write or log()
// Static check: mnemonic is read but not passed to log()
assert(
  !src.includes('log(mnemonic)') && !src.includes('log(recoveryPhrase)'),
  'tr-cli.ts: mnemonic/recoveryPhrase not passed to log() (phrase safety)',
);

// ---------------------------------------------------------------------------

console.log(`\n# ${passed} passed, ${failed} failed`);
process.exit(failed === 0 ? 0 : 1);
