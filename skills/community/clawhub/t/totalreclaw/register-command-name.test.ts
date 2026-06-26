/**
 * Regression test for issue #215 follow-up (3.3.7-rc.2).
 *
 * 3.3.7-rc.1 registered the plugin's restart command as `name: 'restart'`,
 * which OpenClaw's plugin registry hard-rejects (`Command name "restart"
 * is reserved by a built-in command`). The 5-tier auth fallback never
 * ran because `register()` failed at the registry boundary. Pedro caught
 * this in manual integration testing 2026-05-03 — gateway log:
 *
 *   [gateway] [plugins] command registration failed: Command name
 *   "restart" is reserved by a built-in command
 *   (plugin=totalreclaw,
 *    source=/home/pdiogo/.openclaw/extensions/totalreclaw/dist/index.js)
 *
 * 3.3.7-rc.2 renamed the command to `totalreclaw-restart`. This test
 * locks the rename in two ways:
 *
 *   1. Static analysis of `index.ts`: every `api.registerCommand({...})`
 *      block whose handler-region mentions `resolveRestartAuth` MUST
 *      have `name: 'totalreclaw-restart'`. (This is the resolver's
 *      fingerprint — only the rc.1/rc.2 restart command uses it. Tests
 *      a NEW occurrence of `name: 'restart'` would not pass even if
 *      added by accident.)
 *
 *   2. Cross-check against OpenClaw's RESERVED_COMMANDS list: parse the
 *      installed `node_modules/openclaw/dist/registry-*.js` to extract
 *      the literal reserved-name set and assert our chosen name is
 *      NOT in it. If a future OpenClaw release adds
 *      `totalreclaw-restart` (unlikely — our namespace) or another
 *      reserved name we accidentally collide with, this test trips.
 *
 * Plus assertions on the SKILL.md / setup-guide user-facing prompts so
 * the agent isn't told to type `/restart` (which would land on the
 * built-in's allow-from gate, NOT our fallback).
 *
 * Run with: `npx tsx register-command-name.test.ts`
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
// 1. index.ts — assert the registerCommand call uses 'totalreclaw-restart'
// ---------------------------------------------------------------------------

const indexTsPath = path.join(__dirname, 'index.ts');
const indexTsSrc = fs.readFileSync(indexTsPath, 'utf8');

// Find every `api.registerCommand({` block and slice up to the next `});`.
// We look for the block that mentions `resolveRestartAuth` (the resolver's
// import name) — that uniquely fingerprints the restart command.
function findRegisterCommandBlocks(src: string): string[] {
  const blocks: string[] = [];
  const re = /api\.registerCommand\(\{[\s\S]*?\}\);/g;
  let m: RegExpExecArray | null;
  while ((m = re.exec(src)) !== null) {
    blocks.push(m[0]);
  }
  return blocks;
}

const allBlocks = findRegisterCommandBlocks(indexTsSrc);
const restartBlocks = allBlocks.filter((b) => b.includes('resolveRestartAuth'));

assert(
  restartBlocks.length === 1,
  'index.ts: exactly one registerCommand block uses resolveRestartAuth ' +
    `(found ${restartBlocks.length})`,
);

if (restartBlocks.length === 1) {
  const block = restartBlocks[0];

  assert(
    /name:\s*['"]totalreclaw-restart['"]/.test(block),
    "index.ts: restart-auth block registers as name: 'totalreclaw-restart'",
  );

  assert(
    !/name:\s*['"]restart['"]/.test(block),
    "index.ts: restart-auth block does NOT register as the reserved name 'restart'",
  );

  assert(
    /requireAuth:\s*false/.test(block),
    'index.ts: restart-auth block keeps requireAuth: false (channel-layer auth bypass)',
  );

  assert(
    block.includes('SIGUSR1'),
    'index.ts: restart-auth block still fires SIGUSR1 on allow',
  );
}

// ---------------------------------------------------------------------------
// 2. Cross-check the chosen name against OpenClaw's RESERVED_COMMANDS list
// ---------------------------------------------------------------------------
//
// Parse the installed openclaw dist to extract the literal reserved set.
// If the file isn't present (skill/ does not ship a node_modules in the
// worktree-run case), skip with a warning rather than fail — the test
// still passes the static-analysis check above. But in the canonical run
// (after `npm install`) the file is present and we assert the name is
// genuinely free.

function findOpenClawRegistryFile(): string | null {
  // Primary location: skill/node_modules/openclaw/dist/registry-*.js
  const skillRoot = path.resolve(__dirname, '..');
  const distDir = path.join(skillRoot, 'node_modules', 'openclaw', 'dist');
  if (!fs.existsSync(distDir)) return null;

  const candidates = fs
    .readdirSync(distDir)
    .filter((f) => /^registry-[A-Za-z0-9_-]+\.js$/.test(f))
    .map((f) => path.join(distDir, f));

  // Prefer the file that contains the RESERVED_COMMANDS literal; multiple
  // chunks may match the registry-*.js name pattern.
  for (const candidate of candidates) {
    const src = fs.readFileSync(candidate, 'utf8');
    if (src.includes('RESERVED_COMMANDS = new Set([')) return candidate;
  }
  return null;
}

function parseReservedNames(registrySrc: string): string[] {
  const m = /RESERVED_COMMANDS\s*=\s*new Set\(\[([\s\S]*?)\]\)/.exec(registrySrc);
  if (!m) return [];
  const body = m[1];
  const names: string[] = [];
  const re = /["']([a-z0-9_-]+)["']/g;
  let nm: RegExpExecArray | null;
  while ((nm = re.exec(body)) !== null) {
    names.push(nm[1]);
  }
  return names;
}

const registryFile = findOpenClawRegistryFile();

if (registryFile == null) {
  console.log(
    '# skip - openclaw dist not installed in skill/node_modules; ' +
      'static check above is sufficient. Run after `npm install` for the ' +
      'reserved-name cross-check.',
  );
} else {
  const registrySrc = fs.readFileSync(registryFile, 'utf8');
  const reservedNames = parseReservedNames(registrySrc);

  assert(
    reservedNames.length > 0,
    `parsed RESERVED_COMMANDS from ${path.basename(registryFile)} ` +
      `(${reservedNames.length} names)`,
  );

  assert(
    reservedNames.includes('restart'),
    "RESERVED_COMMANDS includes 'restart' (the bug we're working around)",
  );

  assert(
    !reservedNames.includes('totalreclaw-restart'),
    "RESERVED_COMMANDS does NOT include 'totalreclaw-restart' (chosen name is free)",
  );

  // Validate that the OpenClaw command-name regex accepts our name —
  // the upstream check is /^[a-z][a-z0-9_-]*$/.
  const validNameRe = /^[a-z][a-z0-9_-]*$/;
  assert(
    validNameRe.test('totalreclaw-restart'),
    "'totalreclaw-restart' matches OpenClaw's name validator regex",
  );
}

// ---------------------------------------------------------------------------
// 3. SKILL.md — agent-facing prompts must use the new name
// ---------------------------------------------------------------------------

const skillMdPath = path.join(__dirname, 'SKILL.md');
const skillMdSrc = fs.readFileSync(skillMdPath, 'utf8');

assert(
  skillMdSrc.includes('/totalreclaw-restart'),
  "skill/plugin/SKILL.md: mentions /totalreclaw-restart (agent's restart imperative)",
);

// The literal slash command "next message must be the literal slash command
// `/totalreclaw-restart`" is the canonical imperative. Lock it.
assert(
  /literal slash command\s+`\/totalreclaw-restart`/.test(skillMdSrc),
  'skill/plugin/SKILL.md: restart imperative tells the agent the literal ' +
    '`/totalreclaw-restart` command (not `/restart`)',
);

// ---------------------------------------------------------------------------
// 4. docs/guides/openclaw-setup.md — user-facing setup guide
// ---------------------------------------------------------------------------

const guidePath = path.resolve(__dirname, '..', '..', 'docs', 'guides', 'openclaw-setup.md');
const guideSrc = fs.readFileSync(guidePath, 'utf8');

assert(
  guideSrc.includes('/totalreclaw-restart'),
  'docs/guides/openclaw-setup.md: mentions /totalreclaw-restart',
);

assert(
  /literal slash command\s+`\/totalreclaw-restart`/.test(guideSrc),
  'docs/guides/openclaw-setup.md: restart imperative uses the new command name',
);

// ---------------------------------------------------------------------------
// 5. CHANGELOG entries exist for [3.3.7-rc.2], [3.3.7-rc.3], and [3.3.9-rc.1]
// ---------------------------------------------------------------------------

const changelogPath = path.join(__dirname, 'CHANGELOG.md');
const changelogSrc = fs.readFileSync(changelogPath, 'utf8');

assert(
  /\[3\.3\.7-rc\.2\]/.test(changelogSrc),
  'CHANGELOG: [3.3.7-rc.2] entry present',
);

assert(
  /reserved by a built-in command/.test(changelogSrc),
  'CHANGELOG: rc.2 entry references the upstream "reserved by a built-in command" rejection',
);

assert(
  /\[3\.3\.7-rc\.3\]/.test(changelogSrc),
  'CHANGELOG: [3.3.7-rc.3] entry present',
);

assert(
  /contracts\.tools/.test(changelogSrc),
  'CHANGELOG: rc.3 entry references the contracts.tools fix',
);

assert(
  /\[3\.3\.9-rc\.1\]/.test(changelogSrc),
  'CHANGELOG: [3.3.9-rc.1] entry present',
);

assert(
  /hybrid-primary/.test(changelogSrc),
  'CHANGELOG: 3.3.9-rc.1 entry references hybrid-primary pivot',
);

// ---------------------------------------------------------------------------
// 6. package.json + skill.json version bumps (must be >= rc.3)
// ---------------------------------------------------------------------------

const packageJson = JSON.parse(fs.readFileSync(path.join(__dirname, 'package.json'), 'utf8'));
const skillJson = JSON.parse(fs.readFileSync(path.join(__dirname, 'skill.json'), 'utf8'));

// Accept 3.3.7-rc.3+ OR 3.3.8-rc.N+ OR 3.3.9-rc.N+ OR 3.3.10-rc.N+ OR
// 3.3.<11+>-rc.N (versions bump with each patch wave; 3.3.10 series
// ships the shell-side `setsid -f` pair detach for the persistent 502).
const validVersionPattern = /^3\.3\.(7-rc\.[3-9]\d*|8-rc\.\d+|9-rc\.\d+|10-rc\.\d+|1[1-9]-rc\.\d+|[2-9]\d-rc\.\d+|[1-9]\d*\.\d+|[1-9]\d{2,}.*)$/;

assert(
  validVersionPattern.test(packageJson.version),
  `package.json: version is 3.3.7-rc.3+ / 3.3.8-rc.1+ / 3.3.9-rc.1+ / 3.3.10-rc.2+ (got ${packageJson.version})`,
);

assert(
  validVersionPattern.test(skillJson.version),
  `skill.json: version is 3.3.7-rc.3+ / 3.3.8-rc.1+ / 3.3.9-rc.1+ / 3.3.10-rc.2+ (got ${skillJson.version})`,
);

// ---------------------------------------------------------------------------

console.log(`\n# ${passed} passed, ${failed} failed`);
process.exit(failed === 0 ? 0 : 1);
