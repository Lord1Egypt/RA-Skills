/**
 * import-upgrade-cli.test.ts (3.3.13)
 *
 * Phase 3.2 retired the totalreclaw_import_from / import_status / import_abort
 * / upgrade agent tools but left the handlers alive in index.ts (auto-resume
 * still calls handlePluginImportFrom on gateway restart). With no user-facing
 * entry point wired, users could NOT start a new import — only auto-resume
 * worked. This was a pre-RC1 must-fix gap.
 *
 * 3.3.13 restored the surfaces as `openclaw totalreclaw` subcommands:
 *   - `import from <source> [...]`        → handlePluginImportFrom
 *   - `import status [--id <importId>]`   → handleImportStatus
 *   - `import abort <importId>`           → handleImportAbort
 *   - `upgrade`                           → relay billing checkout (Stripe URL)
 *
 * This test statically verifies the wiring inside the registerCli block
 * (dynamic invocation requires a live gateway, commander program, and the
 * plugin runtime with module-level auth state). Pattern follows
 * register-command-name.test.ts + tr-cli-json-output.test.ts.
 *
 * WHY STATIC: the registerCli callback runs inside the gateway process where
 * `handlePluginImportFrom` + module-level state (authKeyHex / encryptionKey /
 * subgraphOwner) are in scope. The test fake-api approach used by
 * pair-cli-default-mode.test.ts works for pair (self-contained module) but
 * NOT here — import reaches deep into index.ts internals (extractFacts,
 * storeExtractedFacts, runSmartImportPipeline). Static analysis of the
 * wiring is precise and deterministic for the registration fingerprint.
 *
 * Run with: `npx tsx import-upgrade-cli.test.ts`
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

const indexTsPath = path.join(__dirname, 'index.ts');
const indexSrc = fs.readFileSync(indexTsPath, 'utf8');

// ---------------------------------------------------------------------------
// 1. The handlers still exist (3.2 retired the agent tools, not the logic)
// ---------------------------------------------------------------------------

assert(
  /async function handlePluginImportFrom\(/.test(indexSrc),
  'index.ts: handlePluginImportFrom handler defined (logic kept after 3.2)',
);

assert(
  /async function handleImportStatus\(/.test(indexSrc),
  'index.ts: handleImportStatus handler defined',
);

assert(
  /async function handleImportAbort\(/.test(indexSrc),
  'index.ts: handleImportAbort handler defined',
);

// ---------------------------------------------------------------------------
// 2. registerCli block wires `import from` / `import status` / `import abort`
// ---------------------------------------------------------------------------

// Slice the registerCli block to bound the search. The import/upgrade wiring
// landed inside the registerCli callback (same block as registerOnboardingCli
// + registerPairCli). We extract everything between `api.registerCli(` and
// the matching `{ commands: ['totalreclaw'] }` options terminator. The
// callback contains nested braces, so a naive non-greedy match stops too
// early — instead we find the start index and slice up to the options line.
const registerCliStart = indexSrc.indexOf('api.registerCli(');
const commandsMarker = "{ commands: ['totalreclaw'] }";
const registerCliEnd = indexSrc.indexOf(commandsMarker, registerCliStart);
assert(
  registerCliStart !== -1 && registerCliEnd !== -1,
  "index.ts: registerCli callback block found (commands: ['totalreclaw'])",
);

const registerCliBody = registerCliStart !== -1 && registerCliEnd !== -1
  ? indexSrc.slice(registerCliStart, registerCliEnd)
  : '';

assert(
  registerCliBody.length > 0,
  'index.ts: registerCli callback body is non-empty',
);

// `import` parent command
assert(
  /tr\.command\(['"]import['"]\)/.test(registerCliBody),
  "index.ts: registerCli wires `tr.command('import')` (parent command)",
);

// `import from` (default subcommand) — calls handlePluginImportFrom
const importFromMatch = registerCliBody.match(
  /importCmd[\s\S]*?\.command\(['"]from['"],\s*\{\s*isDefault:\s*true\s*\}\)/,
);
assert(
  importFromMatch !== null,
  "index.ts: registerCli wires `import from` as the default `import` subcommand",
);

assert(
  registerCliBody.includes('handlePluginImportFrom'),
  'index.ts: import `from` subcommand calls handlePluginImportFrom',
);

// `import status` — calls handleImportStatus
assert(
  /importCmd\s*\n?\s*\.command\(['"]status['"]\)/.test(registerCliBody),
  "index.ts: registerCli wires `import status` subcommand",
);
assert(
  registerCliBody.includes('handleImportStatus'),
  'index.ts: `import status` subcommand calls handleImportStatus',
);

// `import abort` — calls handleImportAbort
assert(
  /importCmd\s*\n?\s*\.command\(['"]abort['"]\)/.test(registerCliBody),
  "index.ts: registerCli wires `import abort` subcommand",
);
assert(
  registerCliBody.includes('handleImportAbort'),
  'index.ts: `import abort` subcommand calls handleImportAbort',
);

// ---------------------------------------------------------------------------
// 3. import `from` argument + option wiring (matches handler input shape)
// ---------------------------------------------------------------------------

// <source> positional argument
assert(
  /\.argument\(['"]<source>['"]/.test(registerCliBody),
  "index.ts: import `from` takes a <source> positional argument",
);

// Source enum must match validSources in handlePluginImportFrom
assert(
  /mem0\s*\|\s*mcp-memory\s*\|\s*chatgpt\s*\|\s*claude\s*\|\s*gemini/.test(registerCliBody),
  'index.ts: import `from` help lists all 5 valid sources (mem0, mcp-memory, chatgpt, claude, gemini)',
);

// The handler params must be wired through: file_path, content, api_key,
// source_user_id, dry_run, resume_id. Check that the option→handler mapping
// references these keys (commander kebab-case → handler snake_case).
assert(
  /file_path:\s*opts\.file/.test(registerCliBody),
  'index.ts: import `from` maps --file → file_path (handler param)',
);
assert(
  /content:\s*opts\.content/.test(registerCliBody),
  'index.ts: import `from` maps --content → content (handler param)',
);
assert(
  /api_key:\s*opts\.apiKey/.test(registerCliBody),
  'index.ts: import `from` maps --api-key → api_key (handler param)',
);
assert(
  /dry_run:\s*opts\.dryRun/.test(registerCliBody),
  'index.ts: import `from` maps --dry-run → dry_run (handler param)',
);
assert(
  /resume_id:\s*opts\.resume/.test(registerCliBody),
  'index.ts: import `from` maps --resume → resume_id (handler param)',
);

// requireFullSetup is called before the handler (same guard the retired
// agent tools used — needs initialized auth/encryption state).
assert(
  /await requireFullSetup\(api\.logger\)/.test(registerCliBody),
  'index.ts: import subcommands call requireFullSetup before handler (auth guard)',
);

// ---------------------------------------------------------------------------
// 4. --json output on all import subcommands
// ---------------------------------------------------------------------------

assert(
  (registerCliBody.match(/option\(['"]--json['"]/g) || []).length >= 4,
  'index.ts: all 4 subcommands (import from, import status, import abort, upgrade) accept --json',
);

// JSON branch emits a single JSON.stringify line on stdout (agent-parseable)
assert(
  /opts\.json[\s\S]{0,200}JSON\.stringify\(result\)/.test(registerCliBody),
  'index.ts: import subcommands emit JSON.stringify(result) on --json',
);

// ---------------------------------------------------------------------------
// 5. `upgrade` subcommand — restores the retired totalreclaw_upgrade
// ---------------------------------------------------------------------------

assert(
  /tr\.command\(['"]upgrade['"]\)/.test(registerCliBody),
  "index.ts: registerCli wires `tr.command('upgrade')` subcommand",
);

// Upgrade must hit /v1/billing/checkout (the relay endpoint the retired
// totalreclaw_upgrade used — same logic, different entry point).
assert(
  /\/v1\/billing\/checkout/.test(registerCliBody),
  'index.ts: upgrade subcommand hits /v1/billing/checkout (restores retired tool logic)',
);

// Body shape: { wallet_address, tier: 'pro' }
assert(
  /wallet_address:\s*walletAddr[\s\S]*?tier:\s*['"]pro['"]/.test(registerCliBody),
  'index.ts: upgrade checkout body includes { wallet_address, tier: "pro" }',
);

// Headers include Authorization Bearer (relay auth)
assert(
  /Authorization['"]:\s*`Bearer \$\{authKeyHex\}`/.test(registerCliBody),
  'index.ts: upgrade sends Authorization: Bearer authKeyHex header',
);

// checkout_url is surfaced in the output
assert(
  /checkout_url/.test(registerCliBody),
  'index.ts: upgrade surfaces checkout_url in output',
);

// ---------------------------------------------------------------------------
// 6. User-facing copy updated (no more "follow-up" placeholders)
// ---------------------------------------------------------------------------

// The Free-tier welcome message must point at the new surface, not say
// "a CLI upgrade surface will ship in a follow-up".
assert(
  !/CLI upgrade surface will ship in a follow-up/.test(indexSrc),
  'index.ts: Free-tier welcome no longer says "CLI upgrade surface will ship in a follow-up"',
);
assert(
  /openclaw totalreclaw upgrade/.test(indexSrc),
  'index.ts: Free-tier welcome points at `openclaw totalreclaw upgrade`',
);

// Import handler messages must point at the new status/abort surfaces.
assert(
  !/CLI status surface will ship in a follow-up/.test(indexSrc),
  'index.ts: import handler no longer says "CLI status surface will ship in a follow-up"',
);
assert(
  !/CLI import surface will ship in a follow-up/.test(indexSrc),
  'index.ts: import status no longer says "CLI import surface will ship in a follow-up"',
);
assert(
  !/CLI resume surface will ship in a follow-up/.test(indexSrc),
  'index.ts: import stale message no longer says "CLI resume surface will ship in a follow-up"',
);

// ---------------------------------------------------------------------------
// 7. Standalone `tr` CLI binary points users at the gateway subcommand
// ---------------------------------------------------------------------------

const trCliPath = path.join(__dirname, 'tr-cli.ts');
const trCliSrc = fs.readFileSync(trCliPath, 'utf8');

// `tr import` and `tr upgrade` must NOT silently no-op; they must die() with
// a pointer to the gateway subcommand (the handlers are not reachable from
// the standalone binary — see the case comment in tr-cli.ts).
assert(
  /case 'import':/.test(trCliSrc) && /case 'upgrade':/.test(trCliSrc),
  "tr-cli.ts: dispatch has 'import' + 'upgrade' cases (pointer for stale prompts)",
);

const trImportUpgradeCase = trCliSrc.match(/case 'import':[\s\S]*?\);\s*\n\s*\n\s*case undefined:/);
assert(
  trImportUpgradeCase !== null,
  "tr-cli.ts: 'import' + 'upgrade' dispatch cases found (die() with pointer, before --help)",
);

if (trImportUpgradeCase) {
  const caseBody = trImportUpgradeCase[0];
  // The die() message builds the subcommand via a template literal:
  //   `openclaw totalreclaw ${cmd === 'import' ? 'import from <source>' : 'upgrade'}`
  // So the literal fragments appear split. Assert the building blocks.
  assert(
    caseBody.includes('openclaw totalreclaw') && caseBody.includes('import from <source>'),
    "tr-cli.ts: 'import' case points at `openclaw totalreclaw import from <source>`",
  );
  assert(
    caseBody.includes("'upgrade'") && /upgrade.*--json/.test(caseBody),
    "tr-cli.ts: 'upgrade' case points at `openclaw totalreclaw upgrade`",
  );
}

// --help text documents the import/upgrade surfaces
assert(
  /Import \+ Upgrade: NOT on the standalone/.test(trCliSrc),
  'tr-cli.ts: --help explains import/upgrade are NOT on the standalone binary',
);
assert(
  /openclaw totalreclaw import from/.test(trCliSrc),
  'tr-cli.ts: --help lists the import subcommand chain',
);

// ---------------------------------------------------------------------------

console.log(`\n# ${passed} passed, ${failed} failed`);
process.exit(failed === 0 ? 0 : 1);
