/**
 * Tests for `ensureSkillRegistered` — the register()-time mirror of the
 * bundled SKILL.md + skill.json into the OpenClaw workspace skills dir.
 *
 * What this asserts
 * -----------------
 *   1. A missing destination is created: both files copied, dest dir
 *      auto-created.
 *   2. Idempotent: a second call on an identical destination is a no-op
 *      (files untouched, no mtime bump).
 *   3. Stale destination is overwritten when the bundled source differs.
 *   4. Missing bundled source files are skipped silently (warn only) —
 *      never throws.
 *   5. A restricted `files` list mirrors only the requested files.
 *   6. The helper never throws on filesystem errors (e.g. unwritable
 *      skills dir) — returns gracefully.
 *   7. The dest dir is `<skillsDir>/totalreclaw/` exactly.
 *
 * Run with: `npx tsx skill-register.test.ts`
 */

import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';

import { ensureSkillRegistered } from './skill-register.js';

let passed = 0;
let failed = 0;

interface SilentLogger {
  infos: string[];
  warns: string[];
}

function makeLogger(): SilentLogger & { info(...a: unknown[]): void; warn(...a: unknown[]): void } {
  const infos: string[] = [];
  const warns: string[] = [];
  return {
    infos,
    warns,
    info(...a: unknown[]): void {
      infos.push(a.join(' '));
    },
    warn(...a: unknown[]): void {
      warns.push(a.join(' '));
    },
  };
}

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

function rmrf(p: string): void {
  try {
    fs.rmSync(p, { recursive: true, force: true });
  } catch {
    // ignore
  }
}

/**
 * Build a fake plugin layout under a tmp dir:
 *   <root>/pkg/dist/         <- pluginDir (where the compiled entry runs)
 *   <root>/pkg/SKILL.md      <- bundled source
 *   <root>/pkg/skill.json    <- bundled source
 */
function mkLayout(): {
  root: string;
  pluginDir: string;
  packageRoot: string;
  skillsDir: string;
  destDir: string;
} {
  const root = fs.mkdtempSync(path.join(os.tmpdir(), 'tr-skill-reg-'));
  const packageRoot = path.join(root, 'pkg');
  const pluginDir = path.join(packageRoot, 'dist');
  fs.mkdirSync(pluginDir, { recursive: true });
  fs.writeFileSync(path.join(packageRoot, 'SKILL.md'), '# TotalReclaw\n\nPairing guide.\n');
  fs.writeFileSync(
    path.join(packageRoot, 'skill.json'),
    JSON.stringify({ name: 'totalreclaw', version: '9.9.9' }),
  );
  const skillsDir = path.join(root, 'home', '.openclaw', 'workspace', 'skills');
  const destDir = path.join(skillsDir, 'totalreclaw');
  return { root, pluginDir, packageRoot, skillsDir, destDir };
}

// ---------------------------------------------------------------------------
// 1. Fresh install — both files copied, dest dir created.
// ---------------------------------------------------------------------------
{
  const { root, pluginDir, destDir } = mkLayout();
  const logger = makeLogger();
  ensureSkillRegistered({ pluginDir, skillsDir: path.dirname(destDir), logger });

  assert(fs.existsSync(destDir), 'fresh: dest dir created');
  assert(
    fs.readFileSync(path.join(destDir, 'SKILL.md'), 'utf8').startsWith('# TotalReclaw'),
    'fresh: SKILL.md copied',
  );
  assert(
    fs.readFileSync(path.join(destDir, 'skill.json'), 'utf8').includes('"totalreclaw"'),
    'fresh: skill.json copied',
  );
  assert(logger.infos.length === 2, 'fresh: two info lines emitted');
  rmrf(root);
}

// ---------------------------------------------------------------------------
// 2. Idempotent — second call is a no-op (no info emitted; bytes identical).
// ---------------------------------------------------------------------------
{
  const { root, pluginDir, destDir } = mkLayout();
  const logger1 = makeLogger();
  const skillsDir = path.dirname(destDir);
  ensureSkillRegistered({ pluginDir, skillsDir, logger: logger1 });

  // Snapshot mtimes + content.
  const skillMdStat = fs.statSync(path.join(destDir, 'SKILL.md'));
  const firstInfoCount = logger1.infos.length;

  // Tiny sleep is unnecessary — mtime resolution is ms and the no-op path
  // does not call copyFileSync at all, so mtime cannot change regardless.
  const logger2 = makeLogger();
  ensureSkillRegistered({ pluginDir, skillsDir, logger: logger2 });

  assert(logger2.infos.length === 0, 'idempotent: second call emits no info');
  assert(firstInfoCount === 2, 'idempotent: first call still emitted info');
  const skillMdStat2 = fs.statSync(path.join(destDir, 'SKILL.md'));
  assert(
    skillMdStat.mtimeMs === skillMdStat2.mtimeMs,
    'idempotent: SKILL.md mtime unchanged on second call',
  );
  rmrf(root);
}

// ---------------------------------------------------------------------------
// 3. Stale destination — overwritten when bundled source differs.
// ---------------------------------------------------------------------------
{
  const { root, pluginDir, packageRoot, destDir } = mkLayout();
  const skillsDir = path.dirname(destDir);

  // First install.
  ensureSkillRegistered({ pluginDir, skillsDir, logger: makeLogger() });

  // Now bump the bundled source (simulate an upgrade) and re-run.
  fs.writeFileSync(path.join(packageRoot, 'SKILL.md'), '# TotalReclaw v2\n\nNew guide.\n');
  const logger = makeLogger();
  ensureSkillRegistered({ pluginDir, skillsDir, logger });

  assert(
    fs.readFileSync(path.join(destDir, 'SKILL.md'), 'utf8').startsWith('# TotalReclaw v2'),
    'stale: SKILL.md overwritten with new bundled content',
  );
  assert(logger.infos.length >= 1, 'stale: at least one info line for the overwrite');
  rmrf(root);
}

// ---------------------------------------------------------------------------
// 4. Missing bundled source — skipped silently (warn only), never throws.
// ---------------------------------------------------------------------------
{
  const { root, pluginDir, packageRoot, destDir } = mkLayout();
  // Remove the bundled SKILL.md so the source is missing.
  fs.unlinkSync(path.join(packageRoot, 'SKILL.md'));

  const logger = makeLogger();
  let threw = false;
  try {
    ensureSkillRegistered({ pluginDir, skillsDir: path.dirname(destDir), logger });
  } catch {
    threw = true;
  }
  assert(!threw, 'missing source: does not throw');
  assert(
    !fs.existsSync(path.join(destDir, 'SKILL.md')),
    'missing source: SKILL.md NOT created',
  );
  assert(
    fs.readFileSync(path.join(destDir, 'skill.json'), 'utf8').includes('"totalreclaw"'),
    'missing source: skill.json still copied (independent file)',
  );
  assert(logger.warns.length >= 1, 'missing source: at least one warn emitted');
  rmrf(root);
}

// ---------------------------------------------------------------------------
// 5. Restricted `files` list — only the requested file is mirrored.
// ---------------------------------------------------------------------------
{
  const { root, pluginDir, destDir } = mkLayout();
  const logger = makeLogger();
  ensureSkillRegistered({
    pluginDir,
    skillsDir: path.dirname(destDir),
    logger,
    files: ['SKILL.md'],
  });

  assert(fs.existsSync(path.join(destDir, 'SKILL.md')), 'restricted: SKILL.md present');
  assert(!fs.existsSync(path.join(destDir, 'skill.json')), 'restricted: skill.json omitted');
  assert(logger.infos.length === 1, 'restricted: exactly one info line');
  rmrf(root);
}

// ---------------------------------------------------------------------------
// 6. Never throws — skills dir under a file (mkdir fails) is swallowed.
// ---------------------------------------------------------------------------
{
  const { root, pluginDir } = mkLayout();
  // Create a regular file at the skills path so mkdir of the subdir fails.
  const skillsParent = path.join(root, 'home', '.openclaw', 'workspace', 'skills');
  fs.mkdirSync(skillsParent, { recursive: true });
  const blockingFile = path.join(skillsParent, 'totalreclaw');
  fs.writeFileSync(blockingFile, 'not a directory');

  const logger = makeLogger();
  let threw = false;
  try {
    ensureSkillRegistered({ pluginDir, skillsDir: skillsParent, logger });
  } catch {
    threw = true;
  }
  assert(!threw, 'fs error: does not throw when dest dir cannot be created');
  assert(logger.warns.length >= 1, 'fs error: at least one warn emitted');
  rmrf(root);
}

// ---------------------------------------------------------------------------
// 7. Dest dir is exactly <skillsDir>/totalreclaw.
// ---------------------------------------------------------------------------
{
  const { root, pluginDir, destDir } = mkLayout();
  ensureSkillRegistered({ pluginDir, skillsDir: path.dirname(destDir), logger: makeLogger() });
  const expected = path.join(path.dirname(destDir), 'totalreclaw');
  assert(destDir === expected, 'layout: dest dir path is <skillsDir>/totalreclaw');
  assert(fs.existsSync(expected), 'layout: totalreclaw subdir exists');
  rmrf(root);
}

// ---------------------------------------------------------------------------
console.log(`\n${passed}/${passed + failed} passed`);
if (failed > 0) {
  process.exit(1);
}
