#!/usr/bin/env node
/**
 * ldm - LDM OS CLI
 * The kernel for agent-native software.
 *
 * Commands:
 *   ldm init              Scaffold ~/.ldm/ and write version.json
 *   ldm install <target>  Detect interfaces + deploy + register
 *   ldm install           Install/update all registered components
 *   ldm doctor            Check health of all extensions
 *   ldm status            Show LDM OS version and extension count
 *   ldm backup            Run a full backup now
 *   ldm backup --dry-run  Preview what would be backed up (with sizes)
 *   ldm backup --pin "x"  Pin the latest backup so rotation skips it
 *   ldm sessions          List active sessions
 *   ldm msg send <to> <b> Send a message to a session
 *   ldm msg list          List pending messages
 *   ldm msg broadcast <b> Send to all sessions
 *   ldm updates           Show available updates
 *   ldm --version         Show version
 */

import { existsSync, readFileSync, writeFileSync, mkdirSync, readdirSync, cpSync, chmodSync, unlinkSync, readlinkSync, renameSync, statSync, lstatSync, symlinkSync } from 'node:fs';
import { join, basename, resolve, dirname } from 'node:path';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const HOME = process.env.HOME || '';
const LDM_ROOT = join(HOME, '.ldm');
const LDM_EXTENSIONS = join(LDM_ROOT, 'extensions');
const VERSION_PATH = join(LDM_ROOT, 'version.json');
const REGISTRY_PATH = join(LDM_EXTENSIONS, 'registry.json');
const LDM_TMP = join(LDM_ROOT, 'tmp');

// Install log (#101): append to ~/.ldm/logs/install.log
import { appendFileSync } from 'node:fs';
const LOG_DIR = join(LDM_ROOT, 'logs');
const LOG_PATH = join(LOG_DIR, 'install.log');
function installLog(msg) {
  try {
    mkdirSync(LOG_DIR, { recursive: true });
    appendFileSync(LOG_PATH, `[${new Date().toISOString()}] ${msg}\n`);
  } catch {}
}

// ── Semver comparison (#XX) ──
// Proper semver comparison that handles prereleases correctly.
// 0.4.73-alpha.1 > 0.4.72 (higher base version, prerelease doesn't matter)
// 0.4.72-alpha.1 < 0.4.72 (same base version, prerelease is older than stable)
// 0.4.73 > 0.4.72 (straightforward)
// Returns true if version `a` is strictly newer than version `b`.
function semverNewer(a, b) {
  if (!a || !b || a === b) return false;
  // Split into base and prerelease: "0.4.73-alpha.1" -> ["0.4.73", "alpha.1"]
  const [aBase, aPre] = a.split('-', 2);
  const [bBase, bPre] = b.split('-', 2);
  const aParts = aBase.split('.').map(Number);
  const bParts = bBase.split('.').map(Number);
  // Compare base version (major.minor.patch)
  for (let i = 0; i < 3; i++) {
    const av = aParts[i] || 0;
    const bv = bParts[i] || 0;
    if (av > bv) return true;
    if (av < bv) return false;
  }
  // Base versions are equal. Stable > prerelease.
  // If a has no prerelease and b does, a is newer (stable release of same base).
  // If a has prerelease and b doesn't, a is older (prerelease of same base).
  if (!aPre && bPre) return true;   // a=0.4.72, b=0.4.72-alpha.1 -> a is newer
  if (aPre && !bPre) return false;  // a=0.4.72-alpha.1, b=0.4.72 -> a is older
  // Both have prereleases with same base. Compare prerelease segments lexically.
  if (aPre && bPre) {
    const aSegs = aPre.split('.');
    const bSegs = bPre.split('.');
    for (let i = 0; i < Math.max(aSegs.length, bSegs.length); i++) {
      const as = aSegs[i] || '';
      const bs = bSegs[i] || '';
      // Numeric segments compared numerically
      const an = /^\d+$/.test(as) ? Number(as) : NaN;
      const bn = /^\d+$/.test(bs) ? Number(bs) : NaN;
      if (!isNaN(an) && !isNaN(bn)) {
        if (an > bn) return true;
        if (an < bn) return false;
      } else {
        if (as > bs) return true;
        if (as < bs) return false;
      }
    }
  }
  return false;
}

// Read our own version from package.json
const pkgPath = join(__dirname, '..', 'package.json');
let PKG_VERSION = '0.2.0';
try {
  PKG_VERSION = JSON.parse(readFileSync(pkgPath, 'utf8')).version;
} catch {}

// Read catalog: prefer ~/.ldm/catalog.json (user-editable), fall back to npm package (#262)
const localCatalogPath = join(LDM_ROOT, 'catalog.json');
const packageCatalogPath = join(__dirname, '..', 'catalog.json');
let CATALOG = { components: [] };
try {
  if (existsSync(localCatalogPath)) {
    CATALOG = JSON.parse(readFileSync(localCatalogPath, 'utf8'));
  } else {
    CATALOG = JSON.parse(readFileSync(packageCatalogPath, 'utf8'));
  }
} catch {}

// Auto-sync version.json when CLI version drifts (#33)
// npm install -g updates the binary but not version.json. Fix it on any CLI invocation.
if (existsSync(VERSION_PATH)) {
  try {
    const v = JSON.parse(readFileSync(VERSION_PATH, 'utf8'));
    if (v.version && v.version !== PKG_VERSION) {
      v.version = PKG_VERSION;
      v.installed = new Date().toISOString(); // #86: update install date on CLI upgrade
      v.updated = new Date().toISOString();
      writeFileSync(VERSION_PATH, JSON.stringify(v, null, 2) + '\n');
    }
  } catch {}
}

// ── Install lockfile (#57) ──

const LOCK_PATH = join(LDM_ROOT, 'state', '.ldm-install.lock');

function acquireInstallLock() {
  try {
    // Child processes spawned by `ldm install` inherit this env var
    if (process.env.LDM_INSTALL_LOCK_PID) return true;

    if (existsSync(LOCK_PATH)) {
      const lock = JSON.parse(readFileSync(LOCK_PATH, 'utf8'));
      // Re-entrant: if we already hold the lock, allow it
      if (lock.pid === process.pid) return true;
      // Check if PID is still alive
      try {
        process.kill(lock.pid, 0); // signal 0 = just check if alive
        console.log(`  Another ldm install is running (PID ${lock.pid}, started ${lock.started}).`);
        console.log(`  Wait for it to finish, or remove ~/.ldm/state/.ldm-install.lock`);
        return false;
      } catch {
        // PID is dead, stale lock. Auto-clean.
        try { unlinkSync(LOCK_PATH); } catch {}
        console.log(`  Cleaned stale install lock (PID ${lock.pid} is dead).`);
      }
    }
    mkdirSync(dirname(LOCK_PATH), { recursive: true });
    writeFileSync(LOCK_PATH, JSON.stringify({ pid: process.pid, started: new Date().toISOString() }));
    process.env.LDM_INSTALL_LOCK_PID = String(process.pid);

    // Clean up on exit
    const cleanup = () => { try { if (existsSync(LOCK_PATH)) { const l = JSON.parse(readFileSync(LOCK_PATH, 'utf8')); if (l.pid === process.pid) unlinkSync(LOCK_PATH); } } catch {} };
    process.on('exit', cleanup);
    process.on('SIGINT', () => { cleanup(); process.exit(1); });
    process.on('SIGTERM', () => { cleanup(); process.exit(1); });
    return true;
  } catch {
    return true; // if lock fails, allow install anyway
  }
}

const args = process.argv.slice(2);

// Normalize dry-run flag variants before parsing (#239)
// --dryrun -> --dry-run
// --dry run (two words) -> --dry-run (consume the stray "run" so it doesn't
//   become a package target and install random npm packages)
for (let i = 0; i < args.length; i++) {
  if (args[i] === '--dryrun') {
    args[i] = '--dry-run';
  } else if (args[i] === '--dry') {
    if (args[i + 1] === 'run') {
      args[i] = '--dry-run';
      args.splice(i + 1, 1);
    } else {
      // Bare --dry with no "run" after it. Treat as --dry-run since there
      // is no other --dry flag and the intent is obvious.
      args[i] = '--dry-run';
    }
  }
}

const command = args[0];
const DRY_RUN = args.includes('--dry-run');
const JSON_OUTPUT = args.includes('--json');
const YES_FLAG = args.includes('--yes') || args.includes('-y');
const NONE_FLAG = args.includes('--none');
const FIX_FLAG = args.includes('--fix');
const CLEANUP_FLAG = args.includes('--cleanup');
const CHECK_FLAG = args.includes('--check');
const ALPHA_FLAG = args.includes('--alpha');
const BETA_FLAG = args.includes('--beta');

function readJSON(path) {
  try {
    return JSON.parse(readFileSync(path, 'utf8'));
  } catch {
    return null;
  }
}

function writeJSON(path, data) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, JSON.stringify(data, null, 2) + '\n');
}

// ── CLI version check (#29) ──

function checkCliVersion() {
  try {
    const result = execSync('npm view @wipcomputer/wip-ldm-os version 2>/dev/null', {
      encoding: 'utf8',
      timeout: 10000,
    }).trim();
    if (result && semverNewer(result, PKG_VERSION)) {
      console.log('');
      console.log(`  CLI is outdated: v${PKG_VERSION} installed, v${result} available.`);
      console.log(`  Run: npm install -g @wipcomputer/wip-ldm-os@${result}`);
    }
  } catch {
    // npm check failed, skip silently
  }
}

// ── Dead backup trigger cleanup (#207) ──
// Three backup systems were competing. Only ai.openclaw.ldm-backup (3am) works.
// This removes: broken cron entry (LDMDevTools.app), old com.wipcomputer.daily-backup.

function cleanDeadBackupTriggers() {
  let cleaned = 0;

  // 1. Remove broken cron entries referencing LDMDevTools.app
  // Matches both "LDMDevTools.app" and "LDM Dev Tools.app" (old naming)
  try {
    const crontab = execSync('crontab -l 2>/dev/null', { encoding: 'utf8' });
    const lines = crontab.split('\n');
    const filtered = lines.filter(line => {
      const lower = line.toLowerCase();
      // Remove any line (active or commented) that references LDMDevTools
      if (lower.includes('ldmdevtools.app') || lower.includes('ldm dev tools.app')) {
        cleaned++;
        return false;
      }
      // Remove orphaned descriptive comment for the old backup verification cron
      if (line.trim() === '# Verify daily backup ran - 00:30 PST') return false;
      return true;
    });
    if (cleaned > 0) {
      // Write filtered crontab via temp file (avoids shell escaping issues)
      const tmpCron = join(LDM_TMP, 'crontab.tmp');
      mkdirSync(LDM_TMP, { recursive: true });
      writeFileSync(tmpCron, filtered.join('\n'));
      execSync(`crontab "${tmpCron}"`, { stdio: 'pipe' });
      try { unlinkSync(tmpCron); } catch {}
      console.log(`  + Removed ${cleaned} dead cron entry(s) (LDMDevTools.app)`);
    }
  } catch {
    // No crontab or crontab command failed. Not critical.
  }

  // 2. Unload and disable com.wipcomputer.daily-backup LaunchAgent
  const oldPlist = join(HOME, 'Library', 'LaunchAgents', 'com.wipcomputer.daily-backup.plist');
  const disabledPlist = oldPlist + '.disabled';
  if (existsSync(oldPlist)) {
    try { execSync(`launchctl unload "${oldPlist}" 2>/dev/null`, { stdio: 'pipe' }); } catch {}
    try {
      renameSync(oldPlist, disabledPlist);
    } catch {
      // If rename fails, just try to remove it
      try { unlinkSync(oldPlist); } catch {}
    }
    console.log('  + Disabled dead LaunchAgent: com.wipcomputer.daily-backup');
    cleaned++;
  }

  // 3. Unload and disable com.wipcomputer.cc-watcher LaunchAgent
  // Broken since Mar 24 migration (old iCloud path, wrong node path).
  // The agent communication channel needs redesign, not screen automation.
  const ccWatcherPlist = join(HOME, 'Library', 'LaunchAgents', 'com.wipcomputer.cc-watcher.plist');
  const ccWatcherDisabled = ccWatcherPlist + '.disabled';
  if (existsSync(ccWatcherPlist)) {
    try { execSync(`launchctl unload "${ccWatcherPlist}" 2>/dev/null`, { stdio: 'pipe' }); } catch {}
    try {
      renameSync(ccWatcherPlist, ccWatcherDisabled);
    } catch {
      try { unlinkSync(ccWatcherPlist); } catch {}
    }
    console.log('  + Disabled dead LaunchAgent: com.wipcomputer.cc-watcher');
    cleaned++;
  }

  return cleaned;
}

// ── Stale hook cleanup (#30) ──

function cleanStaleHooks() {
  const settingsPath = join(HOME, '.claude', 'settings.json');
  const settings = readJSON(settingsPath);
  if (!settings?.hooks) return 0;

  let cleaned = 0;

  for (const [event, hookGroups] of Object.entries(settings.hooks)) {
    if (!Array.isArray(hookGroups)) continue;

    // Filter out hook groups where ALL hooks point to non-existent paths
    const original = hookGroups.length;
    settings.hooks[event] = hookGroups.filter(group => {
      const hooks = group.hooks || [];
      if (hooks.length === 0) return true; // keep empty groups (matcher-only)

      // Check each hook command for stale paths
      const liveHooks = hooks.filter(h => {
        if (!h.command) return true;
        // Extract the path from "node /path/to/file.mjs" or "node \"/path/to/file.mjs\""
        const match = h.command.match(/node\s+"?([^"]+)"?\s*$/);
        if (!match) return true; // keep non-node commands
        const scriptPath = match[1];
        // /tmp/ paths will vanish on reboot, always treat as stale
        const isTmp = scriptPath.startsWith('/tmp/') || scriptPath.startsWith('/private/tmp/');
        if (existsSync(scriptPath) && !isTmp) return true;
        const reason = isTmp ? '(temp path, will break on reboot)' : '(missing)';
        console.log(`  + Removed stale hook: ${event} -> ${scriptPath} ${reason}`);
        cleaned++;
        return false;
      });

      // Keep the group if it still has live hooks
      group.hooks = liveHooks;
      return liveHooks.length > 0;
    });
  }

  if (cleaned > 0) {
    writeFileSync(settingsPath, JSON.stringify(settings, null, 2) + '\n');
  }

  return cleaned;
}

// ── Boot hook sync (#49) ──

function syncBootHook() {
  const srcBoot = join(__dirname, '..', 'src', 'boot', 'boot-hook.mjs');
  const destBoot = join(LDM_ROOT, 'library', 'boot', 'boot-hook.mjs');

  if (!existsSync(srcBoot)) return false;

  try {
    const srcContent = readFileSync(srcBoot, 'utf8');
    let destContent = '';
    try { destContent = readFileSync(destBoot, 'utf8'); } catch {}

    if (srcContent !== destContent) {
      mkdirSync(dirname(destBoot), { recursive: true });
      writeFileSync(destBoot, srcContent);
      return true;
    }
  } catch {}
  return false;
}

// ── Inbox check hook sync ──
//
// Deploys src/hooks/inbox-check-hook.mjs to ~/.ldm/library/hooks/ and
// wires it into ~/.claude/settings.json as a UserPromptSubmit hook so
// that pending bridge messages in ~/.ldm/messages/ are surfaced as
// additionalContext before CC responds to each user prompt.
//
// Closes the loop between lesa-bridge fire-and-forget sends and
// CC-side message delivery. Without this hook, Claude Code only sees
// bridge messages when it explicitly calls lesa_check_inbox, which
// requires manual discipline and loses messages in practice.
//
// Idempotent: subsequent installs update the file only if its contents
// changed, and only add the settings.json entry if it isn't already
// wired to the exact same command path.
//
// See:
//   ai/product/plans-prds/bridge/2026-04-06--cc-mini--bridge-master-product-plan.md
//   ai/product/bugs/bridge/2026-04-06--cc-mini--bridge-async-inbox-plan.md
//   ai/product/bugs/bridge/2026-04-10--cc-mini--bridge-reply-addressing-mismatch.md
function syncInboxCheckHook() {
  const srcHook = join(__dirname, '..', 'src', 'hooks', 'inbox-check-hook.mjs');
  const destHook = join(LDM_ROOT, 'library', 'hooks', 'inbox-check-hook.mjs');
  let changed = false;

  if (!existsSync(srcHook)) return false;

  // 1. File deploy: copy src/hooks/inbox-check-hook.mjs to ~/.ldm/library/hooks/
  try {
    const srcContent = readFileSync(srcHook, 'utf8');
    let destContent = '';
    try { destContent = readFileSync(destHook, 'utf8'); } catch {}

    if (srcContent !== destContent) {
      mkdirSync(dirname(destHook), { recursive: true });
      writeFileSync(destHook, srcContent);
      changed = true;
    }
  } catch {
    return false;
  }

  // 2. Settings.json patch: wire the hook into hooks.UserPromptSubmit if absent.
  const settingsPath = join(HOME, '.claude', 'settings.json');
  if (!existsSync(settingsPath)) return changed;

  try {
    const raw = readFileSync(settingsPath, 'utf8');
    const settings = JSON.parse(raw);
    if (!settings.hooks) settings.hooks = {};
    if (!settings.hooks.UserPromptSubmit) settings.hooks.UserPromptSubmit = [];

    const hookCommand = `node ${destHook}`;
    const alreadyWired = settings.hooks.UserPromptSubmit.some(group =>
      Array.isArray(group.hooks) &&
      group.hooks.some(h => h.type === 'command' && h.command === hookCommand)
    );

    if (!alreadyWired) {
      settings.hooks.UserPromptSubmit.push({
        hooks: [{
          type: 'command',
          command: hookCommand,
          timeout: 5,
        }],
      });
      writeFileSync(settingsPath, JSON.stringify(settings, null, 2) + '\n');
      changed = true;
    }
  } catch {
    // Settings file malformed or unreadable. File deploy still succeeded
    // if changed was true; leave settings.json untouched and let the user
    // see the file deploy message without the wire-up.
  }

  return changed;
}

// ── Inbox rewake hook sync ──
//
// Deploys src/hooks/inbox-rewake-hook.mjs to ~/.ldm/library/hooks/ and
// wires it into ~/.claude/settings.json as a Stop hook with
// `asyncRewake: true`. This is the autonomous push layer that wakes
// an idle Claude Code session when a bridge message arrives, without
// the user having to type anything.
//
// Mechanics: the Stop hook fires after every CC turn. The rewake hook
// acquires a per-session lock file (so concurrent Stop-event spawns do
// not stack), then holds a long-lived fs.watch on ~/.ldm/messages/.
// When a matching message file arrives, the hook writes the message to
// stderr and exits with code 2. The CC harness wraps that stderr into
// a system-reminder task-notification that wakes the idle model or
// gets injected mid-query if the model is busy. See Claude Code's
// `src/utils/hooks.ts` asyncRewake path for the exact mechanism.
//
// This closes the layer 1 gap from:
//   ai/product/plans-prds/bridge/2026-04-11--cc-mini--autonomous-push-architecture.md
//
// Layers 2-4 (UserPromptSubmit inbox-check hook, SessionStart boot
// hook, manual lesa_check_inbox) remain as independent fallbacks.
//
// Idempotent: subsequent installs update the file only if its contents
// changed, and only add the settings.json entry if it isn't already
// wired to the exact same command path.
function syncInboxRewakeHook() {
  const srcHook = join(__dirname, '..', 'src', 'hooks', 'inbox-rewake-hook.mjs');
  const destHook = join(LDM_ROOT, 'library', 'hooks', 'inbox-rewake-hook.mjs');
  let changed = false;

  if (!existsSync(srcHook)) return false;

  // 1. File deploy: copy src/hooks/inbox-rewake-hook.mjs to ~/.ldm/library/hooks/
  try {
    const srcContent = readFileSync(srcHook, 'utf8');
    let destContent = '';
    try { destContent = readFileSync(destHook, 'utf8'); } catch {}

    if (srcContent !== destContent) {
      mkdirSync(dirname(destHook), { recursive: true });
      writeFileSync(destHook, srcContent);
      changed = true;
    }
  } catch {
    return false;
  }

  // 2. Settings.json patch: wire the hook into hooks.Stop as an
  //    asyncRewake background hook if absent.
  const settingsPath = join(HOME, '.claude', 'settings.json');
  if (!existsSync(settingsPath)) return changed;

  try {
    const raw = readFileSync(settingsPath, 'utf8');
    const settings = JSON.parse(raw);
    if (!settings.hooks) settings.hooks = {};
    if (!settings.hooks.Stop) settings.hooks.Stop = [];

    const hookCommand = `node ${destHook}`;
    const alreadyWired = settings.hooks.Stop.some(group =>
      Array.isArray(group.hooks) &&
      group.hooks.some(h =>
        h.type === 'command' &&
        h.command === hookCommand &&
        h.asyncRewake === true,
      ),
    );

    if (!alreadyWired) {
      settings.hooks.Stop.push({
        hooks: [{
          type: 'command',
          command: hookCommand,
          async: true,
          asyncRewake: true,
          // 6 hours: matches the rewake hook's internal hard timeout.
          // The hook self-terminates well before this on parent death,
          // hard cancel, or match, so this is just a runaway guard.
          timeout: 21600,
        }],
      });
      writeFileSync(settingsPath, JSON.stringify(settings, null, 2) + '\n');
      changed = true;
    }
  } catch {
    // Settings file malformed or unreadable. Leave it alone.
  }

  return changed;
}

// ── Catalog helpers ──

function loadCatalog() {
  return CATALOG.components || [];
}

// Seed ~/.ldm/catalog.json from the npm package if it doesn't exist (#262)
function seedLocalCatalog() {
  if (existsSync(localCatalogPath)) return false;
  try {
    const pkgCatalog = readFileSync(packageCatalogPath, 'utf8');
    mkdirSync(LDM_ROOT, { recursive: true });
    writeFileSync(localCatalogPath, pkgCatalog);
    return true;
  } catch {
    return false;
  }
}

function findInCatalog(id) {
  const q = id.toLowerCase();
  // Strip org/ prefix for matching (e.g. "wipcomputer/openclaw-tavily" -> "openclaw-tavily")
  const qBase = q.includes('/') ? q.split('/').pop() : q;
  const catalog = loadCatalog();
  // Exact id match
  const exact = catalog.find(c => c.id === id || c.id === qBase);
  if (exact) return exact;
  // Exact repo match (e.g. "wipcomputer/openclaw-tavily" matches repo field directly)
  const byRepo = catalog.find(c => c.repo && c.repo.toLowerCase() === q);
  if (byRepo) return byRepo;
  // Partial id match (e.g. "xai-grok" matches "wip-xai-grok")
  // Check both directions but require word-boundary alignment (hyphen or start of string)
  // to prevent "openclaw" matching "openclaw-tavily"
  const partial = catalog.find(c => {
    const cid = c.id.toLowerCase();
    if (cid === qBase) return false;
    // Query is suffix of catalog id: "xai-grok" matches "wip-xai-grok"
    if (cid.endsWith(qBase) && (cid.length === qBase.length || cid[cid.length - qBase.length - 1] === '-')) return true;
    // Catalog id is suffix of query: "wip-xai-grok" matches when query is "wip-xai-grok-private"
    if (qBase.endsWith(cid) && (qBase.length === cid.length || qBase[qBase.length - cid.length - 1] === '-')) return true;
    return false;
  });
  if (partial) return partial;
  // Name match (case-insensitive, e.g. "xAI Grok")
  const byName = catalog.find(c => c.name && c.name.toLowerCase() === q);
  if (byName) return byName;
  // registryMatches match
  const byRegistry = catalog.find(c => (c.registryMatches || []).some(m => m.toLowerCase() === q || m.toLowerCase() === qBase));
  if (byRegistry) return byRegistry;
  return null;
}

// Install a single catalog component directly (no subprocess).
// Replaces the old execSync('ldm install ${c.repo}') which spawned
// a full installer process for each component.
async function installCatalogComponent(c) {
  const { installFromPath, setFlags: setDeployFlags } = await import('../lib/deploy.mjs');
  setDeployFlags({ dryRun: DRY_RUN, jsonOutput: JSON_OUTPUT, origin: 'catalog' }); // #262
  const repoTarget = c.repo;
  const repoName = basename(repoTarget);
  const repoPath = join(LDM_TMP, repoName);
  const httpsUrl = `https://github.com/${repoTarget}.git`;
  const sshUrl = `git@github.com:${repoTarget}.git`;

  mkdirSync(LDM_TMP, { recursive: true });
  console.log(`  Cloning ${repoTarget}...`);
  try {
    if (existsSync(repoPath)) {
      execSync(`rm -rf "${repoPath}"`, { stdio: 'pipe' });
    }
    try {
      execSync(`git clone --depth 1 "${httpsUrl}" "${repoPath}"`, { stdio: 'pipe' });
    } catch {
      console.log(`  HTTPS failed. Trying SSH...`);
      if (existsSync(repoPath)) execSync(`rm -rf "${repoPath}"`, { stdio: 'pipe' });
      execSync(`git clone --depth 1 "${sshUrl}" "${repoPath}"`, { stdio: 'pipe' });
    }
  } catch (e) {
    console.error(`  x Clone failed: ${e.message}`);
    return;
  }

  await installFromPath(repoPath);

  // Clean up staging clone
  if (repoPath.startsWith(LDM_TMP)) {
    try { execSync(`rm -rf "${repoPath}"`, { stdio: 'pipe' }); } catch {}
  }
  console.log(`  ✓ Installed ${c.name}`);
}

// ── Bridge deploy (#245) ──
// Deploy all scripts from scripts/ to ~/.ldm/bin/
// Called from both cmdInit() and cmdInstallCatalog() so script fixes land on every update.
function deployScripts() {
  const scriptsSrc = join(__dirname, '..', 'scripts');
  if (!existsSync(scriptsSrc)) return 0;
  mkdirSync(join(LDM_ROOT, 'bin'), { recursive: true });
  let count = 0;
  for (const file of readdirSync(scriptsSrc)) {
    if (!file.endsWith('.sh')) continue;
    const src = join(scriptsSrc, file);
    const dest = join(LDM_ROOT, 'bin', file);
    cpSync(src, dest);
    chmodSync(dest, 0o755);
    count++;
  }
  if (count > 0) {
    console.log(`  + ${count} script(s) deployed to ~/.ldm/bin/`);
  }
  return count;
}

// Deploy personalized docs to both settings/docs/ and library/documentation/
// Called from both cmdInit() and cmdInstallCatalog() so doc fixes land on every update.
function deployDocs() {
  const docsSrc = join(__dirname, '..', 'shared', 'docs');
  if (!existsSync(docsSrc)) return 0;

  let workspacePath = '';
  try {
    const ldmConfig = JSON.parse(readFileSync(join(LDM_ROOT, 'config.json'), 'utf8'));
    workspacePath = (ldmConfig.workspace || '').replace('~', HOME);
  } catch { return 0; }
  if (!workspacePath || !existsSync(workspacePath)) return 0;

  // Read config for template vars
  let ldmConfig;
  try {
    ldmConfig = JSON.parse(readFileSync(join(LDM_ROOT, 'config.json'), 'utf8'));
  } catch { return 0; }

  const sc = ldmConfig;

  // Agents from config (rich objects with harness/machine/prefix)
  const agentsObj = sc.agents || {};
  const agentsList = Object.entries(agentsObj).map(([id, a]) => `${id} (${a.harness} on ${a.machine})`).join(', ');
  const agentsDetail = Object.entries(agentsObj).map(([id, a]) => `- **${id}**: ${a.harness} on ${a.machine}, branch prefix \`${a.prefix}/\``).join('\n');

  // Harnesses from config
  const harnessConfig = sc.harnesses || {};
  const harnessesDetected = Object.entries(harnessConfig).filter(([,h]) => h.detected).map(([name]) => name);
  const harnessesList = harnessesDetected.length > 0 ? harnessesDetected.join(', ') : 'run ldm install to detect';

  const templateVars = {
    'name': sc.name || '',
    'org': sc.org || '',
    'timezone': sc.timezone || '',
    'paths.workspace': (sc.paths?.workspace || '').replace('~', HOME),
    'paths.ldm': (sc.paths?.ldm || '').replace('~', HOME),
    'paths.openclaw': (sc.paths?.openclaw || '').replace('~', HOME),
    'paths.icloud': (sc.paths?.icloud || '').replace('~', HOME),
    'memory.local': (sc.memory?.local || '').replace('~', HOME),
    'deploy.website': sc.deploy?.website || '',
    'backup.keep': String(sc.backup?.keep || 7),
    'agents_list': agentsList,
    'agents_detail': agentsDetail,
    'harnesses_list': harnessesList,
  };

  function renderTemplates(destDir) {
    mkdirSync(destDir, { recursive: true });
    let count = 0;
    for (const file of readdirSync(docsSrc)) {
      if (!file.endsWith('.tmpl')) continue;
      let content = readFileSync(join(docsSrc, file), 'utf8');
      content = content.replace(/\{\{([^}]+)\}\}/g, (match, key) => {
        return templateVars[key.trim()] || match;
      });
      const outName = file.replace('.tmpl', '');
      writeFileSync(join(destDir, outName), content);
      count++;
    }
    return count;
  }

  // Deploy to library/documentation/ (the canonical doc path since Mar 28 rename).
  // Previously also deployed to settings/docs/ which Parker renamed to library/documentation/.
  // That created a ghost folder on every install. Removed 2026-04-05 per INST-1.
  const libraryDest = join(workspacePath, 'library', 'documentation');
  mkdirSync(libraryDest, { recursive: true });
  const docsCount = renderTemplates(libraryDest);
  if (docsCount > 0) {
    console.log(`  + ${docsCount} personalized doc(s) deployed to ${libraryDest.replace(HOME, '~')}/`);
  }

  // Also deploy to ~/.ldm/library/documentation/ (the agent library, for internal docs
  // like dev-guide-wipcomputerinc.md that should be available to agents but not
  // surfaced in the human-facing workspace library).
  // Added 2026-04-19 as part of retiring the sourceless `~/.ldm/shared/` deploy path
  // for the private dev guide. The shared -> library migration across the board is
  // pending; this change moves one file cleanly into the new location without
  // pre-empting the broader migration.
  const agentLibraryDest = join(LDM_ROOT, 'library', 'documentation');
  mkdirSync(agentLibraryDest, { recursive: true });
  const agentDocsCount = renderTemplates(agentLibraryDest);
  if (agentDocsCount > 0) {
    console.log(`  + ${agentDocsCount} personalized doc(s) deployed to ${agentLibraryDest.replace(HOME, '~')}/`);
  }

  return docsCount + agentDocsCount;
}

// Check backup health: is a trigger configured, did it run recently, is iCloud set up?
// Called from cmdInstallCatalog() on every install.
function checkBackupHealth() {
  const config = readJSON(join(LDM_ROOT, 'config.json'));
  if (!config) return;

  const backup = config.backup || {};
  const issues = [];

  // Check iCloud offsite
  const icloudPath = config.paths?.icloudBackup || backup.icloudPath;
  if (!icloudPath) {
    issues.push('iCloud offsite not configured. Add paths.icloudBackup to ~/.ldm/config.json');
  } else {
    const expandedPath = icloudPath.replace(/^~/, HOME);
    if (!existsSync(expandedPath)) {
      try { mkdirSync(expandedPath, { recursive: true }); } catch {}
      if (!existsSync(expandedPath)) {
        issues.push(`iCloud path does not exist: ${icloudPath}`);
      }
    }
  }

  // Check LaunchAgent
  try {
    const label = backup.triggerLabel || 'ai.openclaw.ldm-backup';
    const result = execSync(`launchctl list ${label} 2>/dev/null`, { encoding: 'utf8', timeout: 3000 });
    if (!result) issues.push(`LaunchAgent ${label} not loaded`);
  } catch {
    issues.push('Backup LaunchAgent not loaded. Backups may not run automatically.');
  }

  // Check last backup age
  const backupRoot = join(LDM_ROOT, 'backups');
  if (existsSync(backupRoot)) {
    const dirs = readdirSync(backupRoot)
      .filter(d => d.match(/^20\d{2}-\d{2}-\d{2}--/) && statSync(join(backupRoot, d)).isDirectory())
      .sort()
      .reverse();
    if (dirs.length > 0) {
      const latest = dirs[0];
      const latestDate = latest.replace(/--.*/, '').replace(/-/g, '/');
      const age = Date.now() - new Date(latestDate).getTime();
      const hours = Math.round(age / (1000 * 60 * 60));
      if (hours > 36) {
        issues.push(`Last backup is ${hours} hours old (${latest}). Expected within 24 hours.`);
      }
    } else {
      issues.push('No backups found. Run: ldm backup');
    }
  }

  // Check backup script exists
  const scriptPath = join(LDM_ROOT, 'bin', 'ldm-backup.sh');
  if (!existsSync(scriptPath)) {
    issues.push('Backup script missing at ~/.ldm/bin/ldm-backup.sh. Run: ldm init');
  }

  if (issues.length > 0) {
    for (const issue of issues) {
      console.log(`  ! Backup: ${issue}`);
    }
  }
}

// The bridge (src/bridge/) builds to dist/bridge/ and ships in the npm package.
// After `npm install -g`, the updated files live at the npm package location but
// never get copied to ~/.ldm/extensions/lesa-bridge/dist/. This function fixes that.

function deployRules() {
  const rulesSrc = join(__dirname, '..', 'shared', 'rules');
  const rulesDest = join(LDM_ROOT, 'library', 'rules');
  if (!existsSync(rulesSrc)) return;
  mkdirSync(rulesDest, { recursive: true });
  let rulesCount = 0;
  for (const file of readdirSync(rulesSrc)) {
    if (!file.endsWith('.md')) continue;
    cpSync(join(rulesSrc, file), join(rulesDest, file));
    rulesCount++;
  }
  if (rulesCount > 0) {
    console.log(`  + ${rulesCount} shared rules deployed to ~/.ldm/library/rules/`);
    // Deploy to Claude Code harness (~/.claude/rules/)
    const claudeRules = join(HOME, '.claude', 'rules');
    if (existsSync(join(HOME, '.claude'))) {
      mkdirSync(claudeRules, { recursive: true });
      for (const file of readdirSync(rulesDest)) {
        if (!file.endsWith('.md')) continue;
        cpSync(join(rulesDest, file), join(claudeRules, file));
      }
      console.log(`  + rules deployed to ~/.claude/rules/`);
    }
    // Deploy to OpenClaw harness (~/.openclaw/workspace/DEV-RULES.md)
    const ocWorkspace = join(HOME, '.openclaw', 'workspace');
    if (existsSync(ocWorkspace)) {
      let combined = '# Dev Rules (deployed by ldm install)\n\n';
      combined += '> Do not edit this file. It is regenerated by `ldm install`.\n';
      combined += '> Source: ~/.ldm/library/rules/\n\n';
      for (const file of readdirSync(rulesDest).sort()) {
        if (!file.endsWith('.md')) continue;
        combined += readFileSync(join(rulesDest, file), 'utf8') + '\n\n---\n\n';
      }
      writeFileSync(join(ocWorkspace, 'DEV-RULES.md'), combined);
      console.log(`  + rules deployed to ~/.openclaw/workspace/DEV-RULES.md`);
    }
  }
}

function deployBridge() {
  const ldmBridgeDir = join(LDM_EXTENSIONS, 'lesa-bridge');
  const ocBridgeDir = join(HOME, '.openclaw', 'extensions', 'lesa-bridge');

  // Deploy targets: LDM path (canonical) and OpenClaw path (where the plugin loads)
  // Create dirs if missing so first-time deploy works (don't skip with filter)
  const targets = [
    { dir: ldmBridgeDir, label: '~/.ldm/extensions/lesa-bridge/dist/' },
    { dir: ocBridgeDir, label: '~/.openclaw/extensions/lesa-bridge/dist/' },
  ];
  for (const t of targets) {
    if (!existsSync(t.dir)) mkdirSync(t.dir, { recursive: true });
  }

  // Find the npm package bridge files. Try require.resolve first, fall back to known path.
  let bridgeSrc = '';
  try {
    const pkgJson = join(__dirname, '..', 'dist', 'bridge');
    if (existsSync(pkgJson)) {
      bridgeSrc = pkgJson;
    }
  } catch {}

  if (!bridgeSrc) {
    // Fallback: check common global npm locations
    const candidates = [
      '/opt/homebrew/lib/node_modules/@wipcomputer/wip-ldm-os/dist/bridge',
      join(HOME, '.npm-global/lib/node_modules/@wipcomputer/wip-ldm-os/dist/bridge'),
    ];
    for (const c of candidates) {
      if (existsSync(c)) {
        bridgeSrc = c;
        break;
      }
    }
  }

  if (!bridgeSrc || !existsSync(bridgeSrc)) return 0;

  // Check if files differ (compare against the LDM target, or first available)
  const checkDest = join(targets[0].dir, 'dist');
  let changed = false;
  try {
    const srcFiles = readdirSync(bridgeSrc).filter(f => f.endsWith('.js') || f.endsWith('.d.ts'));
    for (const file of srcFiles) {
      const srcPath = join(bridgeSrc, file);
      const destPath = join(checkDest, file);
      if (!existsSync(destPath)) {
        changed = true;
        break;
      }
      const srcContent = readFileSync(srcPath);
      const destContent = readFileSync(destPath);
      if (!srcContent.equals(destContent)) {
        changed = true;
        break;
      }
    }
    // Also check if there are stale files in the target that aren't in the source
    if (!changed) {
      const destFiles = readdirSync(checkDest).filter(f => f.endsWith('.js'));
      const srcFileSet = new Set(srcFiles);
      for (const file of destFiles) {
        if (!srcFileSet.has(file)) {
          changed = true; // stale chunk file found
          break;
        }
      }
    }
  } catch {
    changed = true; // if comparison fails, copy anyway
  }

  if (!changed) return 0;

  if (DRY_RUN) {
    console.log(`  + would deploy bridge files to ${targets.map(t => t.label).join(' + ')}`);
    return 0;
  }

  const srcFiles = readdirSync(bridgeSrc).filter(f => f.endsWith('.js') || f.endsWith('.d.ts'));
  let totalDeployed = 0;

  for (const target of targets) {
    const dest = join(target.dir, 'dist');
    try {
      mkdirSync(dest, { recursive: true });

      // Clean stale .js files before copying (chunk hashes change between builds)
      try {
        const existing = readdirSync(dest).filter(f => f.endsWith('.js'));
        const srcFileSet = new Set(srcFiles.filter(f => f.endsWith('.js')));
        for (const file of existing) {
          if (!srcFileSet.has(file)) {
            unlinkSync(join(dest, file));
          }
        }
      } catch {}

      for (const file of srcFiles) {
        cpSync(join(bridgeSrc, file), join(dest, file));
      }
      console.log(`  + bridge deployed to ${target.label} (${srcFiles.length} files)`);
      installLog(`Bridge deployed: ${srcFiles.length} files to ${target.label}`);
      totalDeployed += srcFiles.length;
    } catch (e) {
      console.log(`  ! bridge deploy to ${target.label} failed: ${e.message}`);
    }
  }

  // Re-register MCP server to point to the canonical LDM path
  if (totalDeployed > 0 && existsSync(join(ldmBridgeDir, 'dist', 'mcp-server.js'))) {
    try {
      const mcpPath = join(ldmBridgeDir, 'dist', 'mcp-server.js');
      execSync(`claude mcp add lesa-bridge --scope user -- node ${mcpPath}`, {
        stdio: 'pipe',
        timeout: 10000,
      });
      console.log(`  + MCP registration updated: lesa-bridge -> ~/.ldm/extensions/lesa-bridge/dist/mcp-server.js`);
      installLog('MCP registration updated: lesa-bridge -> ~/.ldm/extensions/lesa-bridge/dist/mcp-server.js');
    } catch (e) {
      // Non-fatal: MCP registration is a convenience, not a requirement
      console.log(`  ! MCP registration update failed: ${e.message}`);
    }
  }

  return totalDeployed;
}

// ── ldm init ──

async function cmdInit() {
  console.log('');
  console.log('  ldm init');
  console.log('  ────────────────────────────────────');

  const dirs = [
    join(LDM_ROOT, 'extensions'),
    join(LDM_ROOT, 'agents'),
    join(LDM_ROOT, 'memory'),
    join(LDM_ROOT, 'state'),
    join(LDM_ROOT, 'sessions'),
    join(LDM_ROOT, 'messages'),
    join(LDM_ROOT, 'library', 'boot'),
    join(LDM_ROOT, 'library', 'cron'),
    join(LDM_ROOT, 'library', 'rules'),
    join(LDM_ROOT, 'library', 'prompts'),
    join(LDM_ROOT, 'hooks'),
  ];

  // Migrate config-from-home.json into config.json (one-time merge)
  // config-from-home.json held org identity (coAuthors, paths, agents, backup, etc.)
  // config.json held runtime/harness info. Now they are one file.
  const configFromHomePath = join(LDM_ROOT, 'config-from-home.json');
  if (existsSync(configFromHomePath) && existsSync(join(LDM_ROOT, 'config.json'))) {
    try {
      const existing = JSON.parse(readFileSync(join(LDM_ROOT, 'config.json'), 'utf8'));
      const fromHome = JSON.parse(readFileSync(configFromHomePath, 'utf8'));
      // Merge: config-from-home.json wins where keys overlap (richer data)
      const merged = { ...existing, ...fromHome };
      // Preserve harnesses from existing config (not in config-from-home.json)
      if (existing.harnesses) merged.harnesses = existing.harnesses;
      // Preserve version and created from existing config
      if (existing.version) merged.version = existing.version;
      if (existing.created) merged.created = existing.created;
      // Update timestamp
      merged.updatedAt = new Date().toISOString();
      writeFileSync(join(LDM_ROOT, 'config.json'), JSON.stringify(merged, null, 2) + '\n');
      renameSync(configFromHomePath, configFromHomePath + '.migrated');
      console.log(`  + config-from-home.json merged into config.json`);
      console.log(`  + config-from-home.json renamed to config-from-home.json.migrated`);
    } catch (e) {
      console.log(`  ! config-from-home.json migration failed: ${e.message}`);
    }
  }

  // Scaffold per-agent memory dirs
  try {
    const config = JSON.parse(readFileSync(join(LDM_ROOT, 'config.json'), 'utf8'));
    const agents = config.agents || [];
    const agentList = Array.isArray(agents) ? agents : Object.keys(agents);
    for (const agentId of agentList) {
      for (const sub of ['memory/daily', 'memory/journals', 'memory/sessions', 'memory/transcripts']) {
        dirs.push(join(LDM_ROOT, 'agents', agentId, sub));
      }
    }

    // Scaffold workspace output dirs if workspace is configured
    const workspace = config.workspace;
    if (workspace && existsSync(workspace)) {
      // Per-agent workspace dirs.
      // Resolve the team folder name from config.json agents[id].teamFolder
      // so agents with unicode names or custom folder names don't get ghost
      // folders created from their agent ID. Falls back to agent ID if no
      // override is configured. Fixed 2026-04-05 per INST-1: previously
      // hardcoded a map that only knew three agents and created ghost folders
      // for any others.
      for (const agentId of agentList) {
        const agentObj = typeof agentsObj[agentId] === 'object' ? agentsObj[agentId] : {};
        const teamName = agentObj.teamFolder || agentObj.name || agentId;
        for (const sub of ['journals', 'automated/memory/summaries/daily', 'automated/memory/summaries/weekly', 'automated/memory/summaries/monthly', 'automated/memory/summaries/quarterly']) {
          dirs.push(join(workspace, 'team', teamName, sub));
        }
      }
      // Org-wide dirs
      for (const track of ['team', 'dev']) {
        for (const cadence of ['daily', 'weekly', 'monthly', 'quarterly']) {
          dirs.push(join(workspace, 'operations', 'updates', track, cadence));
        }
      }
    }
  } catch {} // config.json may not exist on first init

  const existing = existsSync(VERSION_PATH);

  if (DRY_RUN) {
    for (const dir of dirs) {
      if (existsSync(dir)) {
        console.log(`  - ${dir} (exists)`);
      } else {
        console.log(`  + would create ${dir}`);
      }
    }
    if (existing) {
      const v = readJSON(VERSION_PATH);
      console.log(`  - version.json exists (v${v?.version})`);
    } else {
      console.log(`  + would write version.json (v${PKG_VERSION})`);
    }
    console.log('');
    console.log('  Dry run complete. No changes made.');
    console.log('');
    return;
  }

  let created = 0;
  for (const dir of dirs) {
    if (!existsSync(dir)) {
      mkdirSync(dir, { recursive: true });
      console.log(`  + ${dir}`);
      created++;
    } else {
      console.log(`  - ${dir} (exists)`);
    }
  }

  // Write or update version.json
  const now = new Date().toISOString();
  if (existing) {
    const v = readJSON(VERSION_PATH);
    v.version = PKG_VERSION;
    v.updated = now;
    writeJSON(VERSION_PATH, v);
    console.log(`  + version.json updated to v${PKG_VERSION}`);
  } else {
    writeJSON(VERSION_PATH, {
      version: PKG_VERSION,
      installed: now,
      updated: now,
    });
    console.log(`  + version.json created (v${PKG_VERSION})`);
  }

  // Seed registry if missing
  if (!existsSync(REGISTRY_PATH)) {
    writeJSON(REGISTRY_PATH, { _format: 'v2', extensions: {} });
    console.log(`  + registry.json created`);
  }

  // Seed local catalog from npm package (#262)
  if (seedLocalCatalog()) {
    console.log(`  + catalog.json seeded to ~/.ldm/catalog.json`);
  }

  // Install global git pre-commit hook (blocks commits on main)
  const hooksDir = join(LDM_ROOT, 'hooks');
  const preCommitDest = join(hooksDir, 'pre-commit');
  const preCommitSrc = join(__dirname, '..', 'templates', 'hooks', 'pre-commit');
  if (!existsSync(hooksDir)) mkdirSync(hooksDir, { recursive: true });
  if (existsSync(preCommitSrc)) {
    cpSync(preCommitSrc, preCommitDest);
    chmodSync(preCommitDest, 0o755);
    // Set global hooksPath if not already set to somewhere else
    try {
      const currentHooksPath = execSync('git config --global core.hooksPath', { encoding: 'utf8' }).trim();
      if (currentHooksPath !== hooksDir) {
        console.log(`  ! core.hooksPath already set to ${currentHooksPath}. Not overwriting.`);
      }
    } catch {
      // Not set. Set it.
      execSync(`git config --global core.hooksPath "${hooksDir}"`);
      console.log(`  + git pre-commit hook installed (blocks commits on main)`);
    }
  }

  // Deploy process monitor (#75)
  const monitorSrc = join(__dirname, '..', 'bin', 'process-monitor.sh');
  const monitorDest = join(LDM_ROOT, 'bin', 'process-monitor.sh');
  if (existsSync(monitorSrc)) {
    mkdirSync(join(LDM_ROOT, 'bin'), { recursive: true });
    cpSync(monitorSrc, monitorDest);
    chmodSync(monitorDest, 0o755);
    // Add cron entry if not already there
    try {
      const crontab = execSync('crontab -l 2>/dev/null', { encoding: 'utf8' });
      if (!crontab.includes('process-monitor')) {
        execSync(`(crontab -l 2>/dev/null; echo "*/3 * * * * ${monitorDest}") | crontab -`);
        console.log(`  + process monitor installed (every 3 min, kills zombie processes)`);
      }
    } catch {
      try {
        execSync(`echo "*/3 * * * * ${monitorDest}" | crontab -`);
        console.log(`  + process monitor installed (every 3 min)`);
      } catch {}
    }
  }

  // Deploy all scripts from scripts/ to ~/.ldm/bin/ (#119)
  deployScripts();

  deployRules();

  // Deploy boot-config.json to ~/.ldm/library/boot/
  const bootSrc = join(__dirname, '..', 'shared', 'boot');
  const bootDest = join(LDM_ROOT, 'library', 'boot');
  if (existsSync(bootSrc)) {
    mkdirSync(bootDest, { recursive: true });
    const bootConfig = join(bootSrc, 'boot-config.json');
    if (existsSync(bootConfig)) {
      cpSync(bootConfig, join(bootDest, 'boot-config.json'));
      console.log(`  + boot-config.json deployed to ~/.ldm/library/boot/`);
    }
  }

  // CLAUDE.md files are NEVER deployed by the installer.
  // They are git-tracked files in their respective repos:
  //   ~/.claude/CLAUDE.md           ... wipcomputer-ldmos-wipcomputerinc-dot-claude-private
  //   ~/wipcomputerinc/CLAUDE.md    ... wipcomputerinc repo
  //   ~/.openclaw/CLAUDE.md         ... openclaw repo
  // Changes go through branches and PRs like any other file.
  // See: 2026-03-27--cc-mini--single-source-of-truth-reversed.md

  // Deploy shared templates to workspace library/templates/
  const templatesSrc = join(__dirname, '..', 'shared', 'templates');
  if (existsSync(templatesSrc)) {
    // Read workspace path from ~/.ldm/config.json
    let workspacePath = '';
    try {
      const ldmConfig = JSON.parse(readFileSync(join(LDM_ROOT, 'config.json'), 'utf8'));
      workspacePath = (ldmConfig.workspace || '').replace('~', HOME);
    } catch {}
    if (workspacePath && existsSync(workspacePath)) {
      const templatesDest = join(workspacePath, 'library', 'templates');
      mkdirSync(templatesDest, { recursive: true });
      let templatesCount = 0;
      for (const file of readdirSync(templatesSrc)) {
        if (file === 'claude-md-level1.md') continue; // deployed separately above
        cpSync(join(templatesSrc, file), join(templatesDest, file));
        templatesCount++;
      }
      if (templatesCount > 0) {
        console.log(`  + ${templatesCount} template(s) deployed to ${templatesDest.replace(HOME, '~')}/`);
      }
    }
  }

  // Deploy shared prompts to ~/.ldm/library/prompts/
  const promptsSrc = join(__dirname, '..', 'shared', 'prompts');
  const promptsDest = join(LDM_ROOT, 'library', 'prompts');
  if (existsSync(promptsSrc)) {
    mkdirSync(promptsDest, { recursive: true });
    let promptsCount = 0;
    for (const file of readdirSync(promptsSrc)) {
      if (!file.endsWith('.md')) continue;
      cpSync(join(promptsSrc, file), join(promptsDest, file));
      promptsCount++;
    }
    if (promptsCount > 0) {
      console.log(`  + ${promptsCount} shared prompts deployed to ~/.ldm/library/prompts/`);
    }
  }

  // Backward-compat symlink: ~/.ldm/shared -> ~/.ldm/library
  // Anything still referencing shared/ will follow the symlink
  {
    const sharedPath = join(LDM_ROOT, 'shared');
    const libraryPath = join(LDM_ROOT, 'library');
    try {
      const stat = lstatSync(sharedPath);
      if (stat.isSymbolicLink()) {
        // Already a symlink, update target if needed
        const target = readlinkSync(sharedPath);
        if (target !== libraryPath) {
          unlinkSync(sharedPath);
          symlinkSync(libraryPath, sharedPath);
        }
      } else if (stat.isDirectory()) {
        // shared/ is a real directory (pre-rename state). Don't touch it.
        // The migration will handle this in a dedicated session.
      }
    } catch {
      // shared/ doesn't exist. Create symlink.
      try {
        symlinkSync(libraryPath, sharedPath);
      } catch {}
    }
  }

  // Detect installed harnesses (CC, OC, Codex, Cursor, Claude macOS)
  try {
    const { detectHarnesses } = await import('../lib/deploy.mjs');
    const { harnesses } = detectHarnesses();
    const detected = Object.entries(harnesses).filter(([,h]) => h.detected).map(([name]) => name);
    if (detected.length > 0) {
      console.log(`  + Harnesses detected: ${detected.join(', ')}`);
    }
  } catch {}

  // Deploy personalized docs to settings/docs/ and library/documentation/
  deployDocs();

  // Deploy LaunchAgents to ~/Library/LaunchAgents/
  // Templates use {{HOME}} and {{OPENCLAW_GATEWAY_TOKEN}} placeholders, replaced at deploy time.
  const launchSrc = join(__dirname, '..', 'shared', 'launchagents');
  const launchDest = join(HOME, 'Library', 'LaunchAgents');
  if (existsSync(launchSrc) && existsSync(launchDest)) {
    // Ensure log directory exists for LaunchAgent output
    mkdirSync(join(LDM_ROOT, 'logs'), { recursive: true });

    // Read gateway token from openclaw.json (if it exists)
    let gatewayToken = '';
    try {
      const ocConfig = JSON.parse(readFileSync(join(HOME, '.openclaw', 'openclaw.json'), 'utf8'));
      gatewayToken = ocConfig?.gateway?.auth?.token || '';
    } catch {}

    let launchCount = 0;
    let launchUpToDate = 0;
    for (const file of readdirSync(launchSrc)) {
      if (!file.endsWith('.plist')) continue;
      const src = join(launchSrc, file);
      const dest = join(launchDest, file);
      // Replace template placeholders with actual values
      let srcContent = readFileSync(src, 'utf8');
      srcContent = srcContent.replace(/\{\{HOME\}\}/g, HOME);
      srcContent = srcContent.replace(/\{\{OPENCLAW_GATEWAY_TOKEN\}\}/g, gatewayToken);
      const destContent = existsSync(dest) ? readFileSync(dest, 'utf8') : '';
      if (srcContent !== destContent) {
        // Unload old agent before overwriting
        try { execSync(`launchctl unload "${dest}" 2>/dev/null`, { stdio: 'pipe' }); } catch {}
        writeFileSync(dest, srcContent);
        try { execSync(`launchctl load "${dest}" 2>/dev/null`, { stdio: 'pipe' }); } catch {}
        const label = file.replace('.plist', '');
        console.log(`  + ${label} deployed and loaded`);
        installLog(`LaunchAgent deployed: ${file}`);
        launchCount++;
      } else {
        launchUpToDate++;
      }
    }
    if (launchCount > 0) {
      console.log(`  + ${launchCount} LaunchAgent(s) deployed to ~/Library/LaunchAgents/`);
    }
    if (launchUpToDate > 0) {
      console.log(`  - ${launchUpToDate} LaunchAgent(s) already up to date`);
    }
  }

  // Deploy bridge files to all targets and re-register MCP (#245, #251)
  deployBridge();

  // Clean up dead backup triggers (#207)
  // Bug: three backup systems were competing. Only ai.openclaw.ldm-backup (3am) works.
  // The old cron entry (LDMDevTools.app) and com.wipcomputer.daily-backup are dead.
  cleanDeadBackupTriggers();

  console.log('');
  console.log(`  LDM OS v${PKG_VERSION} initialized at ${LDM_ROOT}`);
  console.log('');

  // Show catalog picker (unless --none or --dry-run)
  if (!NONE_FLAG && !DRY_RUN) {
    await showCatalogPicker();
  }
}

async function showCatalogPicker() {
  const components = loadCatalog();
  if (components.length === 0) return;

  // Check what's already installed
  const registry = readJSON(REGISTRY_PATH);
  const installed = Object.keys(registry?.extensions || {});

  const available = components.filter(c => c.status !== 'coming-soon' && !installed.includes(c.id));
  const comingSoon = components.filter(c => c.status === 'coming-soon');

  if (available.length === 0 && comingSoon.length === 0) return;

  console.log('  Available components:');
  console.log('');

  let idx = 1;
  const selectable = [];
  for (const c of available) {
    const rec = c.recommended ? ' (recommended)' : '';
    console.log(`    ${idx}. ${c.name}${rec}`);
    console.log(`       ${c.description}`);
    console.log('');
    selectable.push(c);
    idx++;
  }

  for (const c of comingSoon) {
    console.log(`    ${idx}. ${c.name} (coming soon)`);
    console.log(`       ${c.description}`);
    console.log('');
    idx++;
  }

  // If --yes, install recommended only
  if (YES_FLAG) {
    const recommended = selectable.filter(c => c.recommended);
    if (recommended.length > 0) {
      for (const c of recommended) {
        console.log(`  Installing ${c.name}...`);
        try {
          await installCatalogComponent(c);
        } catch (e) {
          console.error(`  x Failed to install ${c.name}: ${e.message}`);
        }
      }
    }
    return;
  }

  // Interactive prompt (skip if not a TTY)
  if (!process.stdin.isTTY) return;

  const { createInterface } = await import('node:readline');
  const rl = createInterface({ input: process.stdin, output: process.stdout });

  const answer = await new Promise((resolve) => {
    rl.question('  Install components? [1,2,all,none]: ', (a) => {
      rl.close();
      resolve(a.trim().toLowerCase());
    });
  });

  if (!answer || answer === 'none' || answer === 'n') return;

  let toInstall = [];
  if (answer === 'all' || answer === 'a') {
    toInstall = selectable;
  } else {
    const nums = answer.split(',').map(s => parseInt(s.trim(), 10)).filter(n => !isNaN(n));
    toInstall = nums.map(n => selectable[n - 1]).filter(Boolean);
  }

  for (const c of toInstall) {
    console.log('');
    console.log(`  Installing ${c.name}...`);
    try {
      await installCatalogComponent(c);
    } catch (e) {
      console.error(`  x Failed to install ${c.name}: ${e.message}`);
    }
  }
}

// ── ldm install ──

async function cmdInstall() {
  if (!DRY_RUN && !acquireInstallLock()) return;

  // Ensure LDM is initialized
  if (!existsSync(VERSION_PATH)) {
    console.log('  LDM OS not initialized. Running init first...');
    console.log('');
    cmdInit();
  }

  const { setFlags, installFromPath, installSingleTool, installToolbox, detectHarnesses } = await import('../lib/deploy.mjs');
  const { detectInterfacesJSON } = await import('../lib/detect.mjs');

  // Refresh harness detection (catches newly installed harnesses)
  detectHarnesses();

  setFlags({ dryRun: DRY_RUN, jsonOutput: JSON_OUTPUT, origin: 'manual' });

  // --help flag (#81)
  if (args.includes('--help') || args.includes('-h')) {
    console.log(`
  ldm install                    Update all registered extensions + CLIs
  ldm install <org/repo>         Install from GitHub
  ldm install <npm-package>      Install from npm
  ldm install <path>             Install from local directory

  Flags:
    --dry-run    Show what would change, don't install
    --json       JSON output
    --yes        Auto-accept catalog prompts
    --none       Skip catalog prompts
    --alpha      Check @alpha npm tag for updates (prerelease track)
    --beta       Check @beta npm tag for updates (prerelease track)
`);
    process.exit(0);
  }

  // Find the target (skip flags)
  const target = args.slice(1).find(a => !a.startsWith('--'));

  if (!target) {
    // Bare `ldm install`: show catalog status + update registered
    return cmdInstallCatalog();
  }

  // If target is a private repo (org/name-private), redirect to public (#134)
  let resolvedTarget = target;
  if (target.match(/^[\w-]+\/[\w.-]+-private$/) && !existsSync(resolve(target))) {
    const publicRepo = target.replace(/-private$/, '');
    const catalogHit = findInCatalog(basename(publicRepo));
    if (catalogHit) {
      console.log(`  Redirecting ${target} to public repo: ${catalogHit.repo}`);
      resolvedTarget = catalogHit.repo;
    } else {
      console.log(`  Redirecting ${target} to public repo: ${publicRepo}`);
      resolvedTarget = publicRepo;
    }
  }

  // Check if target is a catalog ID (e.g. "memory-crystal")
  const catalogEntry = findInCatalog(resolvedTarget);
  if (catalogEntry) {
    setFlags({ dryRun: DRY_RUN, jsonOutput: JSON_OUTPUT, origin: 'catalog' }); // #262
    console.log('');
    console.log(`  Resolved "${target}" via catalog to ${catalogEntry.repo}`);

    // Use the repo field to clone from GitHub
    const repoTarget = catalogEntry.repo;
    const repoName = basename(repoTarget);
    const repoPath = join(LDM_TMP, repoName);
    const httpsUrl = `https://github.com/${repoTarget}.git`;
    const sshUrl = `git@github.com:${repoTarget}.git`;

    mkdirSync(LDM_TMP, { recursive: true });
    console.log(`  Cloning ${repoTarget}...`);
    try {
      if (existsSync(repoPath)) {
        execSync(`rm -rf "${repoPath}"`, { stdio: 'pipe' });
      }
      try {
        execSync(`git clone "${httpsUrl}" "${repoPath}"`, { stdio: 'pipe' });
      } catch {
        console.log(`  HTTPS failed. Trying SSH...`);
        if (existsSync(repoPath)) execSync(`rm -rf "${repoPath}"`, { stdio: 'pipe' });
        execSync(`git clone "${sshUrl}" "${repoPath}"`, { stdio: 'pipe' });
      }
      console.log(`  + Cloned to ${repoPath}`);
    } catch (e) {
      console.error(`  x Clone failed: ${e.message}`);
      process.exit(1);
    }

    if (JSON_OUTPUT) {
      const result = detectInterfacesJSON(repoPath);
      console.log(JSON.stringify(result, null, 2));
      if (DRY_RUN) process.exit(0);
    }

    await installFromPath(repoPath);

    // Clean up staging clone after install (#32, #135)
    if (!DRY_RUN && repoPath.startsWith(LDM_TMP)) {
      try { execSync(`rm -rf "${repoPath}"`, { stdio: 'pipe' }); } catch {}
    }
    return;
  }

  // Resolve target: npm package, GitHub URL, org/repo shorthand, or local path
  let repoPath;

  // Check if target looks like an npm package (starts with @ or is a plain name without /)
  if (resolvedTarget.startsWith('@') || (!resolvedTarget.includes('/') && !existsSync(resolve(resolvedTarget)))) {
    // Try npm pack + tar extract to temp dir
    // npm install --prefix silently fails for scoped packages in temp directories...
    // it creates the lock file but doesn't extract files. npm pack is reliable.
    const npmName = resolvedTarget;
    const tempDir = join(LDM_TMP, `npm-${Date.now()}`);
    console.log('');
    console.log(`  Installing ${npmName} from npm...`);
    try {
      mkdirSync(tempDir, { recursive: true });
      // Use npm pack + tar instead of npm install --prefix
      const tarball = execSync(`npm pack ${npmName} --pack-destination "${tempDir}" 2>/dev/null`, {
        encoding: 'utf8', timeout: 60000, cwd: tempDir,
      }).trim();
      const tarPath = join(tempDir, tarball);
      if (existsSync(tarPath)) {
        execSync(`tar xzf "${tarPath}" -C "${tempDir}"`, { stdio: 'pipe' });
        const extracted = join(tempDir, 'package');
        if (existsSync(extracted)) {
          console.log(`  + Installed from npm`);
          repoPath = extracted;
        } else {
          console.error(`  x npm pack succeeded but extraction failed`);
        }
      } else {
        console.error(`  x npm pack failed: tarball not found`);
      }
    } catch (e) {
      // npm failed, fall through to git clone or path resolution
      console.log(`  npm install failed, trying other methods...`);
      try { execSync(`rm -rf "${tempDir}"`, { stdio: 'pipe' }); } catch {}
    }
  }

  if (!repoPath && (resolvedTarget.startsWith('http') || resolvedTarget.startsWith('git@') || resolvedTarget.match(/^[\w-]+\/[\w.-]+$/))) {
    const isShorthand = resolvedTarget.match(/^[\w-]+\/[\w.-]+$/);
    const httpsUrl = isShorthand
      ? `https://github.com/${resolvedTarget}.git`
      : resolvedTarget;
    const sshUrl = isShorthand
      ? `git@github.com:${resolvedTarget}.git`
      : resolvedTarget.replace(/^https:\/\/github\.com\//, 'git@github.com:');
    const repoName = basename(httpsUrl).replace('.git', '');
    repoPath = join(LDM_TMP, repoName);

    mkdirSync(LDM_TMP, { recursive: true });
    console.log('');
    console.log(`  Cloning ${isShorthand ? resolvedTarget : httpsUrl}...`);
    try {
      if (existsSync(repoPath)) {
        execSync(`rm -rf "${repoPath}"`, { stdio: 'pipe' });
      }
      try {
        execSync(`git clone "${httpsUrl}" "${repoPath}"`, { stdio: 'pipe' });
      } catch {
        console.log(`  HTTPS failed. Trying SSH...`);
        if (existsSync(repoPath)) execSync(`rm -rf "${repoPath}"`, { stdio: 'pipe' });
        execSync(`git clone "${sshUrl}" "${repoPath}"`, { stdio: 'pipe' });
      }
      console.log(`  + Cloned to ${repoPath}`);
    } catch (e) {
      console.error(`  x Clone failed: ${e.message}`);
      process.exit(1);
    }
  } else if (!repoPath) {
    repoPath = resolve(resolvedTarget);
    if (!existsSync(repoPath)) {
      console.error(`  x Path not found: ${repoPath}`);
      process.exit(1);
    }
  }

  if (JSON_OUTPUT) {
    const result = detectInterfacesJSON(repoPath);
    console.log(JSON.stringify(result, null, 2));
    if (DRY_RUN) process.exit(0);
  }

  await installFromPath(repoPath);

  // Clean up staging clone after install (#32, #135)
  if (!DRY_RUN && repoPath.startsWith(LDM_TMP)) {
    try { execSync(`rm -rf "${repoPath}"`, { stdio: 'pipe' }); } catch {}
  }
}

// ── Registry migration (#262) ──
// Upgrades old v1 registry entries to v2 format with source info.
// Runs once per install. Idempotent: entries that already have source are skipped.

function migrateRegistry() {
  const registry = readJSON(REGISTRY_PATH);
  if (!registry?.extensions) return 0;

  const components = loadCatalog();
  let migrated = 0;

  for (const [name, entry] of Object.entries(registry.extensions)) {
    // Skip entries that have already been migrated to v2 format.
    // An entry is fully migrated if it has: installed (object), paths, origin,
    // and source is either structured (object with type) or explicitly null.
    const hasV2Installed = entry.installed && typeof entry.installed === 'object' && entry.installed.version;
    const sourceIsResolved = entry.source === null || (typeof entry.source === 'object' && entry.source?.type);
    if (hasV2Installed && entry.paths && entry.origin && sourceIsResolved) continue;

    const newSource = { type: 'github' };
    let hasSource = false;

    // Try 1: match against catalog for source info
    const catalogMatch = components.find(c => {
      const matches = c.registryMatches || [c.id];
      return matches.includes(name) || c.id === name;
    });
    if (catalogMatch) {
      if (catalogMatch.repo) { newSource.repo = catalogMatch.repo; hasSource = true; }
      if (catalogMatch.npm) { newSource.npm = catalogMatch.npm; hasSource = true; }
      if (!entry.origin) entry.origin = 'catalog';
    }

    // Try 2: read from the installed extension's package.json repository field
    if (!hasSource || !newSource.repo) {
      const extPkgPath = join(LDM_EXTENSIONS, name, 'package.json');
      const extPkg = readJSON(extPkgPath);
      if (extPkg?.name && !newSource.npm) {
        newSource.npm = extPkg.name;
        hasSource = true;
      }
      if (extPkg?.repository) {
        const raw = typeof extPkg.repository === 'string'
          ? extPkg.repository
          : extPkg.repository.url || '';
        const ghMatch = raw.match(/github\.com[:/]([^/]+\/[^/.]+)/);
        if (ghMatch) {
          newSource.repo = ghMatch[1].replace(/\.git$/, '');
          hasSource = true;
        }
      }
    }

    if (hasSource) {
      entry.source = newSource;
    } else if (typeof entry.source === 'string') {
      // Legacy string source (path or URL). Clear it since we couldn't build structured source.
      entry.source = null;
    }

    // Migrate flat version to installed block
    if (!entry.installed || typeof entry.installed !== 'object') {
      entry.installed = {
        version: entry.version || 'unknown',
        installedAt: entry.updatedAt || new Date().toISOString(),
        updatedAt: entry.updatedAt || new Date().toISOString(),
      };
    }

    // Migrate flat paths to paths block
    if (!entry.paths) {
      entry.paths = {};
      if (entry.ldmPath) entry.paths.ldm = entry.ldmPath;
      if (entry.ocPath) entry.paths.openclaw = entry.ocPath;
    }

    // Set origin if missing
    if (!entry.origin) {
      entry.origin = 'manual';
    }

    migrated++;
  }

  if (migrated > 0) {
    registry._format = 'v2';
    writeJSON(REGISTRY_PATH, registry);
  }

  return migrated;
}

// ── Auto-detect unregistered extensions ──

function autoDetectExtensions() {
  if (!existsSync(LDM_EXTENSIONS)) return;
  const registry = readJSON(REGISTRY_PATH);
  if (!registry) return;

  const registered = Object.keys(registry.extensions || {});
  let found = 0;

  try {
    const dirs = readdirSync(LDM_EXTENSIONS, { withFileTypes: true });
    for (const dir of dirs) {
      if (!dir.isDirectory()) continue;
      if (dir.name === '_trash' || dir.name.startsWith('.') || dir.name.startsWith('ldm-install-')) continue;

      const extPath = join(LDM_EXTENSIONS, dir.name);
      const pkgPath = join(extPath, 'package.json');
      if (!existsSync(pkgPath)) continue;

      // Check if already registered (by directory name or by ldmPath)
      const alreadyRegistered = registered.some(name => {
        const info = registry.extensions[name];
        return name === dir.name || info?.ldmPath === extPath;
      });
      if (alreadyRegistered) continue;

      // Auto-register
      const pkg = readJSON(pkgPath);
      if (!pkg) continue;

      registry.extensions[dir.name] = {
        name: dir.name,
        version: pkg.version || '?',
        source: null,
        interfaces: [],
        ldmPath: extPath,
        updatedAt: new Date().toISOString(),
        autoDetected: true,
      };
      found++;
    }
  } catch {}

  if (found > 0) {
    writeJSON(REGISTRY_PATH, registry);
  }
  return found;
}

// ── Claude Code env override cleanup ──

/**
 * Strip stale Claude Code env overrides from ~/.claude/settings.json.
 *
 * These env vars were set manually during the Opus 4.6 era to force max
 * effort and disable adaptive thinking. With Opus 4.7+ the model picks
 * sensible defaults on its own and these forced overrides interfere with
 * adaptive behavior. They were never deployed by a template, so there is
 * no source-of-truth to fix ... the only place they exist is the user's
 * deployed settings.json.
 *
 * Idempotent: removes only the listed STALE_ENV_KEYS if present, drops
 * the env block entirely if it becomes empty, preserves any other env
 * keys untouched, silent no-op if nothing to remove.
 *
 * Adding more obsolete env keys to STALE_ENV_KEYS is the maintenance path
 * if other forced overrides need cleanup later.
 */
function cleanupStaleClaudeCodeEnv() {
  const settingsPath = join(HOME, '.claude/settings.json');
  if (!existsSync(settingsPath)) return false;

  const STALE_ENV_KEYS = [
    'CLAUDE_CODE_EFFORT_LEVEL',
    'CLAUDE_CODE_DISABLE_ADAPTIVE_THINKING',
  ];

  let settings;
  try {
    settings = JSON.parse(readFileSync(settingsPath, 'utf-8'));
  } catch (err) {
    console.log(`  - Could not parse ~/.claude/settings.json: ${err.message}`);
    return false;
  }

  if (!settings.env || typeof settings.env !== 'object') return false;

  const removed = [];
  for (const key of STALE_ENV_KEYS) {
    if (key in settings.env) {
      delete settings.env[key];
      removed.push(key);
    }
  }

  if (removed.length === 0) return false;

  if (Object.keys(settings.env).length === 0) {
    delete settings.env;
  }

  if (DRY_RUN) {
    console.log(`  [dry run] Would remove stale env keys from ~/.claude/settings.json: ${removed.join(', ')}`);
    return false;
  }

  try {
    writeFileSync(settingsPath, JSON.stringify(settings, null, 2) + '\n');
    console.log(`  + Removed stale env keys from ~/.claude/settings.json: ${removed.join(', ')}`);
    console.log(`    New CC sessions will use Opus 4.7+ default effort and adaptive thinking`);
    return true;
  } catch (err) {
    console.log(`  - Could not write ~/.claude/settings.json: ${err.message}`);
    return false;
  }
}

// ── 1Password SA token shell profile setup ──

/**
 * Ensure the 1Password SA token is exported in the user's shell profile so
 * Claude Code sessions, MCP servers, cron jobs, and launch agents can all
 * read secrets on demand via `op` without a biometric popup.
 *
 * Background: The op-secrets plugin injects OP_SERVICE_ACCOUNT_TOKEN into
 * the OpenClaw gateway process env at startup. But processes outside the
 * gateway's inheritance tree (Claude Code sessions, their hooks, MCPs, cron
 * jobs) never see it. The cleanest fix is to put it in the user's shell
 * profile so every shell and every CC session inherits it, and hooks can
 * then do `op read` on demand to fetch actual API keys. Only the SA token
 * (the key that unlocks other keys) lands in env; actual API keys stay in
 * 1Password and are fetched per-process.
 *
 * Idempotent. Skips if marker already present. Creates the profile file if
 * none of the candidates exist.
 *
 * See: ai/product/bugs/memory-crystal/2026-04-15--cc-mini--sa-token-env-and-hook-failfast.md
 */
function ensureShellProfileSaToken() {
  const saTokenPath = join(HOME, '.openclaw/secrets/op-sa-token');
  if (!existsSync(saTokenPath)) return false;

  const marker = '# LDM OS: 1Password SA token (for headless op CLI lookups)';
  const block = `\n${marker}\nif [ -f "$HOME/.openclaw/secrets/op-sa-token" ]; then\n  export OP_SERVICE_ACCOUNT_TOKEN="$(cat "$HOME/.openclaw/secrets/op-sa-token")"\nfi\n`;

  const shell = process.env.SHELL || '';
  const isZsh = shell.includes('zsh') || !shell;
  const candidates = isZsh
    ? [join(HOME, '.zprofile'), join(HOME, '.zshrc')]
    : [join(HOME, '.bash_profile'), join(HOME, '.profile'), join(HOME, '.bashrc')];

  let targetPath = candidates.find(p => existsSync(p));
  if (!targetPath) targetPath = isZsh ? candidates[1] : candidates[0];

  let existing = '';
  try {
    if (existsSync(targetPath)) existing = readFileSync(targetPath, 'utf-8');
  } catch {}

  if (existing.includes(marker)) return false;

  if (DRY_RUN) {
    console.log(`  [dry run] Would append OP_SERVICE_ACCOUNT_TOKEN export to ${targetPath.replace(HOME, '~')}`);
    return false;
  }

  try {
    appendFileSync(targetPath, block);
    const displayPath = targetPath.replace(HOME, '~');
    console.log(`  + Shell profile updated: appended OP_SERVICE_ACCOUNT_TOKEN export to ${displayPath}`);
    console.log(`    Open a new terminal or run: source ${displayPath}`);
    return true;
  } catch (err) {
    console.log(`  - Could not update ${targetPath.replace(HOME, '~')}: ${err.message}`);
    return false;
  }
}

// ── ldm install (bare): scan system, show real state, update if needed ──

async function cmdInstallCatalog() {
  // No lock here. cmdInstall() already holds it when calling this.
  installLog(`ldm install started (v${PKG_VERSION}, DRY_RUN=${DRY_RUN})`);

  // Self-update: check if CLI itself is outdated. Update first, then re-exec.
  // This breaks the chicken-and-egg: new features in ldm install are always
  // available because the installer upgrades itself before doing anything else.
  // --alpha and --beta flags check the corresponding npm dist-tag instead of @latest.
  if (!DRY_RUN && !process.env.LDM_SELF_UPDATED) {
    try {
      const npmTag = ALPHA_FLAG ? 'alpha' : BETA_FLAG ? 'beta' : 'latest';
      const trackLabel = npmTag === 'latest' ? '' : ` (${npmTag} track)`;
      const npmViewCmd = npmTag === 'latest'
        ? 'npm view @wipcomputer/wip-ldm-os version 2>/dev/null'
        : `npm view @wipcomputer/wip-ldm-os dist-tags.${npmTag} 2>/dev/null`;
      const latest = execSync(npmViewCmd, {
        encoding: 'utf8', timeout: 15000,
      }).trim();
      if (latest && semverNewer(latest, PKG_VERSION)) {
        console.log(`  LDM OS CLI v${PKG_VERSION} -> v${latest}${trackLabel}. Updating first...`);
        try {
          execSync(`npm install -g @wipcomputer/wip-ldm-os@${latest}`, { stdio: 'inherit', timeout: 60000 });
          console.log(`  CLI updated to v${latest}. Re-running with new code...`);
          console.log('');
          // Re-exec with the new binary. LDM_SELF_UPDATED prevents infinite loop.
          // process.argv.slice(2) skips 'node' and the script path, keeps just 'install' + flags
          const reArgs = process.argv.slice(2).join(' ') || 'install';
          execSync(`LDM_SELF_UPDATED=1 ldm ${reArgs}`, { stdio: 'inherit' });
          process.exit(0);
        } catch (e) {
          console.log(`  ! Self-update failed: ${e.message}. Continuing with v${PKG_VERSION}.`);
        }
      }
    } catch {}
  }

  autoDetectExtensions();

  // Migrate old registry entries to v2 format (#262)
  const migrated = migrateRegistry();
  if (migrated > 0) {
    console.log(`  + Migrated ${migrated} registry entries to v2 format (source info added)`);
  }

  // Aggregate the bin ownership manifest BEFORE seedLocalCatalog,
  // deployBridge, deployScripts, and the heal walk run. If two
  // declarers claim the same file in ~/.ldm/bin/ we cannot safely
  // decide ownership, so install must abort before catalog.json,
  // bridge files, or any ~/.ldm/bin/ shim is written. See
  // ai/product/plans-prds/current/2026-04-28--cc-mini--ldm-bin-ownership-manifest-design.md
  const { aggregateBinManifest, healBinManifest } = await import('../lib/bin-manifest.mjs');
  const ldmCliRoot = join(__dirname, '..');
  const binManifestRegistry = readJSON(REGISTRY_PATH) || { extensions: {} };
  const manifest = aggregateBinManifest({
    ldmCliRoot,
    extensionsRoot: LDM_EXTENSIONS,
    binDir: join(LDM_ROOT, 'bin'),
    registry: binManifestRegistry,
  });
  if (manifest.conflicts.length > 0) {
    console.log('');
    console.log('  x bin manifest conflict ... aborting before seedLocalCatalog/deployBridge/deployScripts run:');
    for (const c of manifest.conflicts) {
      console.log(`    "${c.name}" claimed by ${c.declarers.length} declarers:`);
      for (const d of c.declarers) {
        console.log(`        ${d.declarer}: ${d.sourcePath.replace(HOME, '~')}`);
      }
    }
    console.log('');
    console.log('  Resolve ownership in the package manifests, then re-run.');
    installLog(`ldm install aborted: ${manifest.conflicts.length} bin manifest conflict(s)`);
    process.exit(1);
  }

  // Seed local catalog if missing (#262)
  if (seedLocalCatalog()) {
    console.log(`  + catalog.json seeded to ~/.ldm/catalog.json`);
  }

  // Deploy bridge files after self-update or on every catalog install (#245, #251)
  // After npm install -g, the new bridge files are in the npm package but not
  // in the extension directories. This copies them to both LDM and OpenClaw targets.
  deployBridge();

  // Deploy scripts, docs, and rules on every install so fixes land without re-init
  deployScripts();
  deployDocs();
  deployRules();

  // Manifest-driven self-heal. deployScripts() above wrote LDM CLI's own
  // *.sh files; this pass covers the rest of the manifest (LDM CLI files
  // deployed elsewhere, e.g. process-monitor.sh, plus extension-owned
  // shims like crystal-capture.sh). Read-only entries that already match
  // the manifest are no-ops.
  if (manifest.entries.length > 0) {
    const heal = healBinManifest(manifest.entries, { heal: !DRY_RUN });
    for (const e of heal.healed) {
      console.log(`  + Restored ${e.name} from ${e.sourcePath.replace(HOME, '~')} (declarer: ${e.declarer})`);
    }
    for (const f of heal.failed) {
      console.log(`  ! ${f.entry.name}: ${f.reason} (declarer: ${f.entry.declarer})`);
    }
    if (heal.ok.length > 0 && heal.healed.length === 0 && heal.failed.length === 0) {
      console.log(`  + bin manifest: ${heal.ok.length} entr${heal.ok.length === 1 ? 'y' : 'ies'} verified`);
    }
  }

  // Check backup configuration
  checkBackupHealth();

  const { detectSystemState, reconcileState, formatReconciliation } = await import('../lib/state.mjs');
  const state = detectSystemState();
  const reconciled = reconcileState(state);

  // Check catalog: use registryMatches + cliMatches to detect what's really installed
  const registry = readJSON(REGISTRY_PATH);
  const components = loadCatalog();

  // Clean ghost entries from registry (#134, #135)
  // Run BEFORE system state display so ghosts don't appear in the installed list.
  if (registry?.extensions) {
    const names = Object.keys(registry.extensions);
    let cleaned = 0;
    for (const name of names) {
      // Remove -private duplicates (e.g. wip-xai-grok-private when wip-xai-grok exists)
      // Only public versions should be installed as extensions. Private repos are for development.
      const publicName = name.replace(/-private$/, '');
      if (name !== publicName && registry.extensions[publicName]) {
        delete registry.extensions[name];
        if (!DRY_RUN) {
          for (const base of [LDM_EXTENSIONS, join(HOME, '.openclaw', 'extensions')]) {
            const ghostDir = join(base, name);
            if (existsSync(ghostDir)) {
              const trashDir = join(LDM_TRASH, `${name}.ghost-${Date.now()}`);
              try { execSync(`mv "${ghostDir}" "${trashDir}"`, { stdio: 'pipe' }); } catch {}
            }
          }
        }
        cleaned++;
        continue;
      }
      // Fix -private path mismatch: registry says "wip-xai-x" but paths point to "wip-xai-x-private".
      // This happens when the installer cloned a public repo whose package.json had a -private name.
      // Rename the directories to match the public registry name.
      const ext = registry.extensions[name];
      if (ext && !name.endsWith('-private')) {
        const privateName = name + '-private';
        let pathFixed = false;
        for (const [pathKey, base] of [['ldmPath', LDM_EXTENSIONS], ['ocPath', join(HOME, '.openclaw', 'extensions')]]) {
          if (ext[pathKey] && ext[pathKey].endsWith(privateName)) {
            const privateDir = join(base, privateName);
            const publicDir = join(base, name);
            if (!DRY_RUN && existsSync(privateDir) && !existsSync(publicDir)) {
              try { execSync(`mv "${privateDir}" "${publicDir}"`, { stdio: 'pipe' }); } catch {}
            }
            ext[pathKey] = publicDir;
            pathFixed = true;
          }
        }
        if (pathFixed) cleaned++;
      }
      // Rename ldm-install- prefixed entries to clean names (#141)
      if (name.startsWith('ldm-install-')) {
        const cleanName = name.replace(/^ldm-install-/, '');
        // Transfer registry entry to clean name
        if (!registry.extensions[cleanName]) {
          registry.extensions[cleanName] = { ...registry.extensions[name] };
        }
        delete registry.extensions[name];
        // Rename the actual directory if it exists
        if (!DRY_RUN) {
          const ghostDir = join(LDM_EXTENSIONS, name);
          const cleanDir = join(LDM_EXTENSIONS, cleanName);
          if (existsSync(ghostDir) && !existsSync(cleanDir)) {
            try {
              execSync(`mv "${ghostDir}" "${cleanDir}"`, { stdio: 'pipe' });
            } catch {}
          } else if (existsSync(ghostDir) && existsSync(cleanDir)) {
            // Clean version exists, remove ghost
            try { execSync(`rm -rf "${ghostDir}"`, { stdio: 'pipe' }); } catch {}
          }
          // Same for OC extensions
          const ocGhost = join(HOME, '.openclaw', 'extensions', name);
          const ocClean = join(HOME, '.openclaw', 'extensions', cleanName);
          if (existsSync(ocGhost) && !existsSync(ocClean)) {
            try { execSync(`mv "${ocGhost}" "${ocClean}"`, { stdio: 'pipe' }); } catch {}
          } else if (existsSync(ocGhost) && existsSync(ocClean)) {
            try { execSync(`rm -rf "${ocGhost}"`, { stdio: 'pipe' }); } catch {}
          }
        }
        cleaned++;
      }
    }
    if (cleaned > 0 && !DRY_RUN) {
      writeFileSync(REGISTRY_PATH, JSON.stringify(registry, null, 2));
      installLog(`Cleaned ${cleaned} ghost registry entries`);
    }
  }

  // Clean orphaned -private directories (#132)
  // Pre-v0.4.30 installs could create -private extension dirs that linger
  // even after registry entries are cleaned. If the public name is in the
  // registry, rename the directory (or trash it if public dir already exists).
  try {
    const extDirs = readdirSync(LDM_EXTENSIONS, { withFileTypes: true })
      .filter(d => d.isDirectory() && d.name.endsWith('-private'));
    for (const d of extDirs) {
      const publicName = d.name.replace(/-private$/, '');
      // Only act if the public name is known (registry entry or catalog match)
      const inRegistry = !!registry?.extensions?.[publicName];
      const inCatalog = components.some(c =>
        c.id === publicName || (c.registryMatches || []).includes(publicName)
      );
      if (!inRegistry && !inCatalog) continue;

      const ghostDir = join(LDM_EXTENSIONS, d.name);
      const publicDir = join(LDM_EXTENSIONS, publicName);

      if (!DRY_RUN) {
        if (!existsSync(publicDir)) {
          // No public dir yet. Rename -private to public name.
          console.log(`  Renaming ghost: ${d.name} -> ${publicName}`);
          try { execSync(`mv "${ghostDir}" "${publicDir}"`, { stdio: 'pipe' }); } catch {}
        } else {
          // Public dir exists. Trash the ghost.
          console.log(`  Trashing ghost: ${d.name} (public "${publicName}" exists)`);
          const trashDir = join(LDM_EXTENSIONS, '_trash', d.name + '--' + new Date().toISOString().slice(0, 10));
          try {
            mkdirSync(join(LDM_EXTENSIONS, '_trash'), { recursive: true });
            execSync(`mv "${ghostDir}" "${trashDir}"`, { stdio: 'pipe' });
          } catch {}
        }
        // Fix registry paths that still reference the -private name
        if (registry?.extensions?.[publicName]) {
          const entry = registry.extensions[publicName];
          if (entry.ldmPath && entry.ldmPath.includes(d.name)) {
            entry.ldmPath = entry.ldmPath.replace(d.name, publicName);
          }
          if (entry.ocPath && entry.ocPath.includes(d.name)) {
            entry.ocPath = entry.ocPath.replace(d.name, publicName);
          }
          writeFileSync(REGISTRY_PATH, JSON.stringify(registry, null, 2));
        }
      } else {
        if (!existsSync(publicDir)) {
          console.log(`  Would rename ghost: ${d.name} -> ${publicName}`);
        } else {
          console.log(`  Would trash ghost: ${d.name} (public "${publicName}" exists)`);
        }
      }
      // Remove from reconciled so it doesn't appear in installed list or update checks
      delete reconciled[d.name];
    }
    // Same for OC extensions
    const ocExtDir = join(HOME, '.openclaw', 'extensions');
    if (existsSync(ocExtDir)) {
      const ocDirs = readdirSync(ocExtDir, { withFileTypes: true })
        .filter(d => d.isDirectory() && d.name.endsWith('-private'));
      for (const d of ocDirs) {
        const publicName = d.name.replace(/-private$/, '');
        const publicDir = join(ocExtDir, publicName);
        const ghostDir = join(ocExtDir, d.name);
        const inCatalog = components.some(c =>
          c.id === publicName || (c.registryMatches || []).includes(publicName)
        );
        if (!inCatalog) continue;
        if (!DRY_RUN) {
          if (!existsSync(publicDir)) {
            try { execSync(`mv "${ghostDir}" "${publicDir}"`, { stdio: 'pipe' }); } catch {}
          } else {
            const trashDir = join(ocExtDir, '_trash', d.name + '--' + new Date().toISOString().slice(0, 10));
            try {
              mkdirSync(join(ocExtDir, '_trash'), { recursive: true });
              execSync(`mv "${ghostDir}" "${trashDir}"`, { stdio: 'pipe' });
            } catch {}
          }
        }
        delete reconciled[d.name];
      }
    }
  } catch {}

  // Show the system state (after ghost cleanup, so ghosts don't appear)
  console.log(formatReconciliation(reconciled));

  const registeredNames = Object.keys(registry?.extensions || {});
  const reconciledNames = Object.keys(reconciled);

  function isCatalogItemInstalled(c) {
    // Direct ID match
    if (registeredNames.includes(c.id) || reconciled[c.id]) return true;
    // Check registryMatches (aliases)
    const matches = c.registryMatches || [];
    if (matches.some(m => registeredNames.includes(m) || reconciled[m])) return true;
    // Check CLI binaries
    const cliMatches = c.cliMatches || [];
    if (cliMatches.some(b => state.cliBinaries[b])) return true;
    return false;
  }

  const available = components.filter(c =>
    c.status !== 'coming-soon' && !isCatalogItemInstalled(c)
  );

  if (available.length > 0) {
    console.log('  Available in catalog (not yet installed):');
    for (const c of available) {
      console.log(`    [ ] ${c.name} ... ${c.description}`);
    }
    console.log('');
  } else {
    console.log('  All catalog components are installed.');
    console.log('');
  }

  // Build the update plan from REGISTRY entries (#262)
  // The registry is the source of truth. Each entry has source info (npm, repo)
  // that tells us where to check for updates.
  const npmUpdates = [];

  // Check CLI self-update (#132)
  try {
    const cliLatest = execSync('npm view @wipcomputer/wip-ldm-os version 2>/dev/null', {
      encoding: 'utf8', timeout: 10000,
    }).trim();
    if (cliLatest && semverNewer(cliLatest, PKG_VERSION)) {
      npmUpdates.push({
        name: 'LDM OS CLI',
        catalogNpm: '@wipcomputer/wip-ldm-os',
        currentVersion: PKG_VERSION,
        latestVersion: cliLatest,
        hasUpdate: true,
        isCLI: true,
      });
    }
  } catch {}

  // Check every registered extension for updates (#262)
  // Source of truth: registry entry's source.npm and source.repo fields.
  // Fallback: extension's package.json (for old entries without source info).
  console.log('  Checking for updates...');
  const registryEntries = Object.entries(registry?.extensions || {});
  const checkedNames = new Set(); // track what we've checked

  for (const [name, regEntry] of registryEntries) {
    // Skip entries with no installed version
    const currentVersion = regEntry?.installed?.version || regEntry?.version;
    if (!currentVersion) continue;

    // Skip pinned components (e.g. OpenClaw)
    const catalogEntry = components.find(c => {
      const matches = c.registryMatches || [c.id];
      return matches.includes(name) || c.id === name;
    });
    if (catalogEntry?.pinned) continue;

    // Get npm package name from registry source (v2) or extension's package.json (legacy)
    const sourceNpm = regEntry?.source?.npm;
    const sourceRepo = regEntry?.source?.repo;
    let npmPkg = sourceNpm || null;

    // Fallback: read from installed extension's package.json
    if (!npmPkg) {
      const extPkgPath = join(LDM_EXTENSIONS, name, 'package.json');
      const extPkg = readJSON(extPkgPath);
      npmPkg = extPkg?.name || null;
    }

    // Determine repo URL for cloning updates
    let repoUrl = sourceRepo || catalogEntry?.repo || null;
    if (!repoUrl) {
      const extPkgPath = join(LDM_EXTENSIONS, name, 'package.json');
      const extPkg = readJSON(extPkgPath);
      if (extPkg?.repository) {
        const raw = typeof extPkg.repository === 'string'
          ? extPkg.repository
          : extPkg.repository.url || '';
        const ghMatch = raw.match(/github\.com[:/]([^/]+\/[^/.]+)/);
        if (ghMatch) repoUrl = ghMatch[1];
      }
    }

    // Check npm for updates (fast, one HTTP call)
    // --alpha and --beta flags check the corresponding npm dist-tag
    if (npmPkg) {
      try {
        const npmTag = ALPHA_FLAG ? 'alpha' : BETA_FLAG ? 'beta' : 'latest';
        const npmViewCmd = npmTag === 'latest'
          ? `npm view ${npmPkg} version 2>/dev/null`
          : `npm view ${npmPkg} dist-tags.${npmTag} 2>/dev/null`;
        const latestVersion = execSync(npmViewCmd, {
          encoding: 'utf8', timeout: 10000,
        }).trim();

        if (latestVersion && semverNewer(latestVersion, currentVersion)) {
          npmUpdates.push({
            name,
            catalogRepo: repoUrl,
            catalogNpm: npmPkg,
            currentVersion,
            latestVersion,
            hasUpdate: true,
          });
        }
      } catch {}
      checkedNames.add(name);
      continue;
    }

    // No npm package. Check GitHub tags via git ls-remote (#262).
    // Works for private repos with SSH access.
    if (repoUrl) {
      try {
        const sshUrl = `git@github.com:${repoUrl}.git`;
        const tags = execSync(`git ls-remote --tags --sort=-v:refname "${sshUrl}" 2>/dev/null`, {
          encoding: 'utf8', timeout: 15000,
        });
        // Parse latest semver tag
        const tagMatch = tags.match(/refs\/tags\/v?(\d+\.\d+\.\d+)/);
        if (tagMatch) {
          const latestVersion = tagMatch[1];
          if (semverNewer(latestVersion, currentVersion)) {
            npmUpdates.push({
              name,
              catalogRepo: repoUrl,
              catalogNpm: repoUrl, // display repo URL since no npm package
              currentVersion,
              latestVersion,
              hasUpdate: true,
            });
          }
        }
      } catch {}
      checkedNames.add(name);
    }
  }

  // Check global CLIs not tracked by registry (#81)
  for (const [binName, binInfo] of Object.entries(state.cliBinaries || {})) {
    if (checkedNames.has(binName)) continue;
    const catalogComp = components.find(c =>
      (c.cliMatches || []).includes(binName)
    );
    if (!catalogComp || !catalogComp.npm) continue;
    // Skip if already covered by extension loop
    if (npmUpdates.some(e =>
      e.catalogNpm === catalogComp.npm ||
      (catalogComp.registryMatches || []).includes(e.name)
    )) continue;

    const currentVersion = binInfo.version;
    if (!currentVersion) continue;

    try {
      const npmTag = ALPHA_FLAG ? 'alpha' : BETA_FLAG ? 'beta' : 'latest';
      const npmViewCmd = npmTag === 'latest'
        ? `npm view ${catalogComp.npm} version 2>/dev/null`
        : `npm view ${catalogComp.npm} dist-tags.${npmTag} 2>/dev/null`;
      const latestVersion = execSync(npmViewCmd, {
        encoding: 'utf8', timeout: 10000,
      }).trim();
      if (latestVersion && semverNewer(latestVersion, currentVersion)) {
        npmUpdates.push({
          name: binName,
          catalogRepo: catalogComp.repo,
          catalogNpm: catalogComp.npm,
          currentVersion,
          latestVersion,
          hasUpdate: true,
          cliOnly: true,
        });
      }
    } catch {}
  }

  // Check parent packages for toolbox-style repos (#132)
  // If sub-tools are installed but the parent npm package has a newer version,
  // report the parent as needing an update (not the individual sub-tool).
  const checkedParentNpm = new Set();
  for (const comp of components) {
    if (!comp.npm || checkedParentNpm.has(comp.npm)) continue;
    if (!comp.registryMatches || comp.registryMatches.length === 0) continue;

    // If any registryMatch is installed, check the parent package
    const installedMatch = comp.registryMatches.find(m => registry?.extensions?.[m]);
    if (!installedMatch) continue;

    const matchEntry = registry.extensions[installedMatch];
    const currentVersion = matchEntry?.installed?.version || matchEntry?.version || '?';

    try {
      const npmTag = ALPHA_FLAG ? 'alpha' : BETA_FLAG ? 'beta' : 'latest';
      const npmViewCmd = npmTag === 'latest'
        ? `npm view ${comp.npm} version 2>/dev/null`
        : `npm view ${comp.npm} dist-tags.${npmTag} 2>/dev/null`;
      const latest = execSync(npmViewCmd, {
        encoding: 'utf8', timeout: 10000,
      }).trim();
      if (latest && semverNewer(latest, currentVersion)) {
        // Remove any sub-tool entries that belong to this parent.
        const parentMatches = new Set(comp.registryMatches || []);
        for (let i = npmUpdates.length - 1; i >= 0; i--) {
          if (!npmUpdates[i].isCLI && parentMatches.has(npmUpdates[i].name)) {
            npmUpdates.splice(i, 1);
          }
        }
        npmUpdates.push({
          name: comp.id,
          catalogRepo: comp.repo,
          catalogNpm: comp.npm,
          currentVersion,
          latestVersion: latest,
          hasUpdate: true,
          isParent: true,
          registryMatches: comp.registryMatches,
        });
      }
    } catch {}
    checkedParentNpm.add(comp.npm);
  }

  const totalUpdates = npmUpdates.length;

  if (DRY_RUN) {
    // Summary block (#80)
    const cliUpdate = npmUpdates.find(u => u.isCLI);

    const agentDirs = (() => {
      try {
        return readdirSync(join(LDM_ROOT, 'agents'), { withFileTypes: true })
          .filter(d => d.isDirectory() && d.name !== '_trash').map(d => d.name);
      } catch { return []; }
    })();

    const totalExtensions = Object.keys(reconciled).length;
    const majorBumps = npmUpdates.filter(e => {
      const curMajor = parseInt(e.currentVersion.split('.')[0], 10);
      const latMajor = parseInt(e.latestVersion.split('.')[0], 10);
      return latMajor > curMajor;
    });

    console.log('');
    console.log('  Summary');
    console.log('  ────────────────────────────────────');
    if (cliUpdate) {
      console.log(`  LDM OS CLI       v${PKG_VERSION}  ->  v${cliUpdate.latestVersion}`);
    } else {
      console.log(`  LDM OS CLI       v${PKG_VERSION} (latest)`);
    }
    if (npmUpdates.length > 0) {
      console.log(`  Extensions       ${totalExtensions} installed, ${npmUpdates.length} update(s)`);
    } else {
      console.log(`  Extensions       ${totalExtensions} installed, all up to date`);
    }
    for (const m of majorBumps) {
      console.log(`  Major bump       ${m.name} v${m.currentVersion} -> v${m.latestVersion}`);
    }
    if (agentDirs.length > 0) {
      console.log(`  Agents           ${agentDirs.join(', ')} (no change)`);
    }
    console.log(`  Data             crystal.db, agent files, secrets (never touched)`);

    if (npmUpdates.length > 0) {
      // Table output
      const nameW = Math.max(10, ...npmUpdates.map(e => e.name.length));
      const curW = Math.max(7, ...npmUpdates.map(e => e.currentVersion.length + 1));
      const latW = Math.max(9, ...npmUpdates.map(e => e.latestVersion.length + 1));
      const pkgW = Math.max(7, ...npmUpdates.map(e => e.catalogNpm.length));

      const pad = (s, w) => s + ' '.repeat(Math.max(0, w - s.length));
      const hr = `  ${'─'.repeat(nameW + curW + latW + pkgW + 13)}`;

      console.log('');
      console.log(`  ${npmUpdates.length} update(s) available:`);
      console.log('');
      console.log(`  ${pad('Extension', nameW)} │ ${pad('Current', curW)} │ ${pad('Available', latW)} │ ${pad('Package', pkgW)}`);
      console.log(hr);
      for (const e of npmUpdates) {
        console.log(`  ${pad(e.name, nameW)} │ ${pad('v' + e.currentVersion, curW)} │ ${pad('v' + e.latestVersion, latW)} │ ${pad(e.catalogNpm, pkgW)}`);
      }
      console.log('');
      console.log('  Old versions would be moved to ~/.ldm/_trash/ (never deleted).');
    }

    // Health check preview (dry-run)
    const healthIssues = [];

    // Check missing CLIs
    for (const comp of components) {
      if (!comp.npm || !comp.cliMatches || comp.cliMatches.length === 0) continue;
      if (!isCatalogItemInstalled(comp)) continue;
      for (const binName of comp.cliMatches) {
        try { execSync(`which ${binName} 2>/dev/null`, { encoding: 'utf8' }); }
        catch { healthIssues.push(`  ! CLI "${binName}" missing (would reinstall ${comp.npm})`); }
      }
    }

    // Check /tmp/ symlinks
    try {
      const npmPrefix = execSync('npm config get prefix', { encoding: 'utf8', timeout: 5000 }).trim();
      const globalModules = join(npmPrefix, 'lib', 'node_modules', '@wipcomputer');
      if (existsSync(globalModules)) {
        for (const entry of readdirSync(globalModules, { withFileTypes: true })) {
          if (!entry.isSymbolicLink()) continue;
          try {
            const target = readlinkSync(join(globalModules, entry.name));
            if (target.includes('/tmp/') || target.includes('/private/tmp/')) {
              healthIssues.push(`  ! @wipcomputer/${entry.name} symlinked to /tmp/ (would reinstall from npm)`);
            }
          } catch {}
        }
      }
    } catch {}

    // Check orphaned staging dirs (old /tmp/ and new ~/.ldm/tmp/)
    try {
      const tmpCount = readdirSync('/private/tmp').filter(d => d.startsWith('ldm-install-')).length;
      if (tmpCount > 0) {
        healthIssues.push(`  ! ${tmpCount} orphaned /tmp/ldm-install-* dirs (would clean up)`);
      }
    } catch {}
    try {
      if (existsSync(LDM_TMP)) {
        const ldmTmpCount = readdirSync(LDM_TMP).filter(d => d.startsWith('ldm-install-')).length;
        if (ldmTmpCount > 0) {
          healthIssues.push(`  ! ${ldmTmpCount} orphaned ~/.ldm/tmp/ldm-install-* dirs (would clean up)`);
        }
      }
    } catch {}

    if (healthIssues.length > 0) {
      console.log('');
      console.log('  Health issues (would fix on install):');
      for (const h of healthIssues) console.log(h);
    }

    console.log('');
    console.log('  Dry run complete. No changes made.');
    console.log('');
    return;
  }

  if (totalUpdates === 0 && available.length === 0) {
    console.log('  Everything is up to date.');
    console.log('');
    return;
  }

  if (totalUpdates === 0 && available.length > 0) {
    // Nothing to update, but catalog items available
    if (!YES_FLAG && !NONE_FLAG && process.stdin.isTTY) {
      const { createInterface } = await import('node:readline');
      const rl = createInterface({ input: process.stdin, output: process.stdout });
      const answer = await new Promise((resolve) => {
        rl.question('  Install from catalog? [number,all,none]: ', (a) => {
          rl.close();
          resolve(a.trim().toLowerCase());
        });
      });
      if (answer && answer !== 'none' && answer !== 'n') {
        let toInstall = [];
        if (answer === 'all' || answer === 'a') {
          toInstall = available;
        } else {
          const nums = answer.split(',').map(s => parseInt(s.trim(), 10)).filter(n => !isNaN(n));
          toInstall = nums.map(n => available[n - 1]).filter(Boolean);
        }
        for (const c of toInstall) {
          console.log(`  Installing ${c.name}...`);
          try {
            execSync(`ldm install ${c.repo}`, { stdio: 'inherit' });
          } catch (e) {
            console.error(`  x Failed to install ${c.name}: ${e.message}`);
          }
        }
      }
    }
    return;
  }

  // Write revert manifest before starting
  const { createRevertManifest } = await import('../lib/safe.mjs');
  const manifestPath = createRevertManifest(
    `ldm install (update ${totalUpdates} extensions)`,
    npmUpdates.map(e => ({
      action: 'update-from-registry',
      name: e.name,
      currentVersion: e.currentVersion,
      latestVersion: e.latestVersion,
      repo: e.catalogRepo,
    }))
  );
  console.log(`  Revert plan saved: ${manifestPath}`);
  console.log('');

  const { setFlags, installFromPath } = await import('../lib/deploy.mjs');
  setFlags({ dryRun: DRY_RUN, jsonOutput: JSON_OUTPUT, origin: 'catalog' }); // #262

  let updated = 0;

  // Update from registry sources (#262, replaces old catalog-based update loop)
  for (const entry of npmUpdates) {
    // CLI self-update is handled by the self-update block at the top of cmdInstallCatalog()
    if (entry.isCLI) continue;

    // CLI-only entries: install directly from npm (#81)
    if (entry.cliOnly) {
      console.log(`  Updating CLI ${entry.name} v${entry.currentVersion} -> v${entry.latestVersion}...`);
      try {
        execSync(`npm install -g ${entry.catalogNpm}@${entry.latestVersion}`, { stdio: 'inherit' });
        updated++;
      } catch (e) {
        console.error(`  x Failed to update CLI ${entry.name}: ${e.message}`);
      }
      continue;
    }

    if (!entry.catalogRepo && !entry.catalogNpm) {
      console.log(`  Skipping ${entry.name}: no catalog repo (install manually with ldm install <org/repo>)`);
      continue;
    }

    // Source resolution chain (#264):
    // 1. npm (when --alpha/--beta or npm package available) - works online, any machine
    // 2. Local private repo (offline, developer machine) - works without internet
    // 3. GitHub clone (fallback) - works online, any machine
    let installSource = null;
    const npmTag = ALPHA_FLAG ? 'alpha' : BETA_FLAG ? 'beta' : null;

    // Try npm first when using alpha/beta tracks or when npm is available
    if (entry.catalogNpm && (npmTag || !entry.catalogRepo)) {
      const ver = npmTag ? `${entry.catalogNpm}@${npmTag}` : `${entry.catalogNpm}@${entry.latestVersion}`;
      installSource = ver;
      console.log(`  Updating ${entry.name} v${entry.currentVersion} -> v${entry.latestVersion} (from npm ${npmTag || 'latest'})...`);
    }

    // Try local private repo (for offline/developer installs)
    if (!installSource && entry.catalogRepo) {
      const repoName = basename(entry.catalogRepo);
      const privateRepoName = repoName + '-private';
      const WORKSPACE = join(HOME, 'wipcomputerinc');
      // Search known repo locations
      const searchDirs = ['repos/ldm-os/devops', 'repos/ldm-os/components', 'repos/ldm-os/utilities', 'repos/ldm-os/apps', 'repos/ldm-os/apis', 'repos/ldm-os/identity'];
      for (const dir of searchDirs) {
        const localPrivate = join(WORKSPACE, dir, privateRepoName);
        const localPublic = join(WORKSPACE, dir, repoName);
        if (existsSync(localPrivate)) {
          installSource = localPrivate;
          console.log(`  Updating ${entry.name} v${entry.currentVersion} -> v${entry.latestVersion} (from local ${privateRepoName})...`);
          break;
        }
        if (existsSync(localPublic)) {
          installSource = localPublic;
          console.log(`  Updating ${entry.name} v${entry.currentVersion} -> v${entry.latestVersion} (from local ${repoName})...`);
          break;
        }
      }
    }

    // Fallback: GitHub clone
    if (!installSource) {
      installSource = entry.catalogRepo;
      console.log(`  Updating ${entry.name} v${entry.currentVersion} -> v${entry.latestVersion} (from ${entry.catalogRepo})...`);
    }

    try {
      execSync(`ldm install ${installSource}`, { stdio: 'inherit' });
      updated++;

      // For parent packages, installFromPath already refreshes each sub-tool
      // registry entry with that sub-tool's own package version. Do not stamp
      // the parent package version onto sub-tools; their versions intentionally
      // differ from the toolbox aggregate version.
      if (entry.isParent && entry.registryMatches) {
        const registry = readJSON(REGISTRY_PATH);
        if (registry?.extensions) {
          let refreshed = 0;
          for (const subTool of entry.registryMatches) {
            if (registry.extensions[subTool]) refreshed++;
          }
          console.log(`  + Refreshed registry for ${refreshed}/${entry.registryMatches.length} sub-tools`);
        }
      }
    } catch (e) {
      console.error(`  x Failed to update ${entry.name}: ${e.message}`);
    }
  }

  // Health check: fix missing CLIs + dead symlinks (#90)
  console.log('');
  console.log('  Running health check...');
  let healthFixes = 0;

  // 1. Check catalog CLIs exist on disk
  for (const comp of components) {
    if (!comp.npm || !comp.cliMatches || comp.cliMatches.length === 0) continue;
    if (!isCatalogItemInstalled(comp)) continue;

    for (const binName of comp.cliMatches) {
      try {
        execSync(`which ${binName} 2>/dev/null`, { encoding: 'utf8' });
      } catch {
        // CLI binary missing. Reinstall from npm.
        console.log(`  ! CLI "${binName}" missing. Reinstalling ${comp.npm}...`);
        try {
          execSync(`npm install -g ${comp.npm}`, { stdio: 'inherit', timeout: 60000 });
          healthFixes++;
          console.log(`  + CLI: ${binName} restored`);
        } catch (e) {
          console.error(`  x Failed to restore ${binName}: ${e.message}`);
        }
      }
    }
  }

  // 2. Check for /tmp/ symlinks in global npm modules
  try {
    const npmPrefix = execSync('npm config get prefix', { encoding: 'utf8', timeout: 5000 }).trim();
    const globalModules = join(npmPrefix, 'lib', 'node_modules', '@wipcomputer');
    if (existsSync(globalModules)) {
      for (const entry of readdirSync(globalModules, { withFileTypes: true })) {
        if (!entry.isSymbolicLink()) continue;
        try {
          const target = readlinkSync(join(globalModules, entry.name));
          if (target.includes('/tmp/') || target.includes('/private/tmp/')) {
            const pkgName = `@wipcomputer/${entry.name}`;
            console.log(`  ! ${pkgName} symlinked to ${target} (will break on reboot). Reinstalling...`);
            try {
              execSync(`npm install -g ${pkgName}`, { stdio: 'inherit', timeout: 60000 });
              healthFixes++;
              console.log(`  + ${pkgName}: replaced /tmp/ symlink with registry install`);
            } catch (e) {
              console.error(`  x Failed to fix ${pkgName}: ${e.message}`);
            }
          }
        } catch {}
      }
    }
  } catch {}

  // 3. Clean orphaned staging dirs (old /tmp/ and new ~/.ldm/tmp/)
  try {
    const tmpDirs = readdirSync('/private/tmp').filter(d => d.startsWith('ldm-install-'));
    if (tmpDirs.length > 0) {
      console.log(`  Cleaning ${tmpDirs.length} orphaned /tmp/ldm-install-* dirs...`);
      for (const d of tmpDirs) {
        try { execSync(`rm -rf "/private/tmp/${d}"`, { stdio: 'pipe', timeout: 10000 }); } catch {}
      }
      healthFixes++;
      console.log(`  + Cleaned ${tmpDirs.length} orphaned /tmp/ clone(s)`);
    }
  } catch {}
  try {
    if (existsSync(LDM_TMP)) {
      const ldmTmpDirs = readdirSync(LDM_TMP).filter(d => d.startsWith('ldm-install-'));
      if (ldmTmpDirs.length > 0) {
        console.log(`  Cleaning ${ldmTmpDirs.length} orphaned ~/.ldm/tmp/ dirs...`);
        for (const d of ldmTmpDirs) {
          try { execSync(`rm -rf "${join(LDM_TMP, d)}"`, { stdio: 'pipe', timeout: 10000 }); } catch {}
        }
        healthFixes++;
        console.log(`  + Cleaned ${ldmTmpDirs.length} orphaned ~/.ldm/tmp/ clone(s)`);
      }
    }
  } catch {}

  if (healthFixes > 0) {
    console.log(`  ${healthFixes} health issue(s) fixed.`);
  } else {
    console.log('  All healthy.');
  }

  // Sync boot hook from npm package (#49)
  if (syncBootHook()) {
    console.log('  + Boot hook updated (sessions, messages, updates now active)');
  }

  // Sync inbox-check hook: UserPromptSubmit hook that surfaces pending
  // bridge messages into CC context on every prompt. Closes the gap
  // between lesa-bridge writes and CC delivery.
  if (syncInboxCheckHook()) {
    console.log('  + Inbox-check hook updated (bridge messages surface automatically)');
  }

  // Sync inbox-rewake hook: Stop hook with asyncRewake that watches
  // ~/.ldm/messages/ in the background and wakes the model when a new
  // bridge message arrives, without requiring user interaction. Layer 1
  // of the April 11 autonomous-push-architecture plan.
  if (syncInboxRewakeHook()) {
    console.log('  + Inbox-rewake hook updated (autonomous push: wakes on new bridge message)');
  }

  // Ensure 1Password SA token is exported in shell profile so Claude Code
  // sessions, MCPs, hooks, cron jobs all inherit it and can op read secrets
  // on demand. Idempotent; no-op if the export line is already present.
  ensureShellProfileSaToken();

  // Deploy git pre-commit hook on every install (not just init)
  const hooksDir = join(LDM_ROOT, 'hooks');
  const preCommitDest = join(hooksDir, 'pre-commit');
  const preCommitSrc = join(__dirname, '..', 'templates', 'hooks', 'pre-commit');
  if (existsSync(preCommitSrc)) {
    if (!existsSync(hooksDir)) mkdirSync(hooksDir, { recursive: true });
    cpSync(preCommitSrc, preCommitDest);
    chmodSync(preCommitDest, 0o755);
  }

  console.log('');
  console.log(`  Updated ${updated}/${totalUpdates} extension(s).`);
  installLog(`ldm install complete: ${updated}/${totalUpdates} updated, ${healthFixes} health fix(es)`);

  // Check if CLI itself is outdated (#29)
  checkCliVersion();

  console.log('');
}

async function cmdUpdateAll() {
  // Delegate to the catalog flow which now has full state awareness
  return cmdInstallCatalog();
}

// ── ldm doctor ──

async function cmdDoctor() {
  console.log('');
  console.log('  ldm doctor');
  console.log('  ────────────────────────────────────');

  // Auto-detect unregistered extensions before checking
  const detected = autoDetectExtensions();
  if (detected > 0) {
    console.log(`  + Auto-detected ${detected} unregistered extension(s)`);
  }

  let issues = 0;

  // 1. Check LDM root
  if (!existsSync(LDM_ROOT)) {
    console.log('  x ~/.ldm/ does not exist. Run: ldm init');
    issues++;
  } else {
    console.log('  + ~/.ldm/ exists');
  }

  // 2. Check version.json
  const version = readJSON(VERSION_PATH);
  if (!version) {
    console.log('  x version.json missing. Run: ldm init');
    issues++;
  } else {
    console.log(`  + version.json: v${version.version} (installed ${version.installed?.split('T')[0]})`);
  }

  // 3. Full system state scan
  const { detectSystemState, reconcileState, formatReconciliation } = await import('../lib/state.mjs');
  const state = detectSystemState();
  const reconciled = reconcileState(state);

  // Show reconciled view
  console.log(formatReconciliation(reconciled, { verbose: true }));

  // Count issues from reconciliation
  const registeredMissing = [];
  for (const [name, entry] of Object.entries(reconciled)) {
    if (entry.status === 'registered-missing') {
      issues++;
      registeredMissing.push(name);
    }
    if (entry.issues.length > 0 && entry.status !== 'installed-unlinked' && entry.status !== 'external') {
      issues += entry.issues.length;
    }
  }

  // --fix: clean up registered-missing entries
  if (FIX_FLAG && registeredMissing.length > 0) {
    const registry = readJSON(REGISTRY_PATH);
    if (registry?.extensions) {
      for (const name of registeredMissing) {
        delete registry.extensions[name];
        console.log(`  + Removed stale registry entry: ${name}`);
        issues--;
      }
      writeFileSync(REGISTRY_PATH, JSON.stringify(registry, null, 2) + '\n');
    }
  }

  // --fix: clean stale hook paths in settings.json (#30)
  if (FIX_FLAG) {
    const hooksCleaned = cleanStaleHooks();
    if (hooksCleaned > 0) {
      issues = Math.max(0, issues - hooksCleaned);
    }
  }

  // --fix: clean registry entries with /tmp/ sources or ldm-install- names (#54)
  if (FIX_FLAG) {
    const registry = readJSON(REGISTRY_PATH);
    if (registry?.extensions) {
      const staleNames = [];
      for (const [name, info] of Object.entries(registry.extensions)) {
        const src = info?.source || '';
        const isTmpSource = src.startsWith('/tmp/') || src.startsWith('/private/tmp/');
        const isTmpName = name.startsWith('ldm-install-');
        if (isTmpSource || isTmpName) {
          staleNames.push(name);
        }
      }
      for (const name of staleNames) {
        delete registry.extensions[name];
        console.log(`  + Removed stale registry entry: ${name} (/tmp/ clone)`);
        issues = Math.max(0, issues - 1);
      }
      if (staleNames.length > 0) {
        writeFileSync(REGISTRY_PATH, JSON.stringify(registry, null, 2) + '\n');
      }
    }
  }

  // --fix: clean stale MCP entries from ~/.claude.json (tmp paths, ldm-install- names)
  if (FIX_FLAG) {
    const ccUserPath = join(HOME, '.claude.json');
    const ccUser = readJSON(ccUserPath);
    if (ccUser?.mcpServers) {
      const staleMcp = [];
      for (const [name, cfg] of Object.entries(ccUser.mcpServers)) {
        const args = cfg.args || [];
        const isTmpPath = args.some(a => a.startsWith('/tmp/') || a.startsWith('/private/tmp/'));
        const isTmpName = name.startsWith('ldm-install-') || name.startsWith('wip-install-');
        if (isTmpPath || isTmpName) staleMcp.push(name);
      }
      for (const name of staleMcp) {
        delete ccUser.mcpServers[name];
        console.log(`  + Removed stale MCP: ${name}`);
        issues = Math.max(0, issues - 1);
      }
      if (staleMcp.length > 0) {
        writeFileSync(ccUserPath, JSON.stringify(ccUser, null, 2) + '\n');
      }
    }
  }

  // --fix: clean stale Claude Code env overrides (Opus 4.6 era) from ~/.claude/settings.json
  if (FIX_FLAG) {
    cleanupStaleClaudeCodeEnv();
  }

  // 3b. MCP health check (Phase 3c)
  //
  // Walk ~/.claude.json#mcpServers. For every entry whose command is node
  // and whose first arg resolves under ~/.ldm/extensions/ or ~/.openclaw/
  // extensions/, verify the file exists and parses. Report any that do not.
  //
  // This catches the failure mode where an extension renamed its MCP file,
  // updated its deployed artifacts, but the old .claude.json entry still
  // points at a path that was rotated into _trash. Surfacing these in
  // doctor makes the class of failure loud instead of silent.
  {
    const ccUserPath = join(HOME, '.claude.json');
    const ccUser = readJSON(ccUserPath);
    const ldmExtRoot = LDM_EXTENSIONS;
    const ocExtRoot = join(HOME, '.openclaw', 'extensions');
    const broken = [];
    if (ccUser?.mcpServers) {
      for (const [name, cfg] of Object.entries(ccUser.mcpServers)) {
        if (cfg?.command !== 'node') continue;
        const args = Array.isArray(cfg.args) ? cfg.args : [];
        const first = args[0];
        if (!first || typeof first !== 'string') continue;
        const underExt = first.startsWith(ldmExtRoot + '/') || first.startsWith(ocExtRoot + '/');
        if (!underExt) continue;
        if (!existsSync(first)) {
          broken.push({ name, path: first, reason: 'missing' });
          continue;
        }
        try {
          execSync(`node --check "${first}"`, { stdio: 'pipe', timeout: 5000 });
        } catch (e) {
          const stderr = (e && e.stderr && e.stderr.toString && e.stderr.toString().trim()) || (e && e.message) || 'unparseable';
          broken.push({ name, path: first, reason: 'unparseable', detail: stderr.split('\n')[0] });
        }
      }
    }
    if (broken.length > 0) {
      for (const b of broken) {
        const detail = b.detail ? ` (${b.detail})` : '';
        console.log(`  ! MCP ${b.name}: ${b.reason} at ${b.path}${detail}`);
      }
      if (FIX_FLAG && ccUser?.mcpServers) {
        for (const b of broken) {
          delete ccUser.mcpServers[b.name];
          console.log(`  + Removed dangling MCP: ${b.name}`);
        }
        writeFileSync(ccUserPath, JSON.stringify(ccUser, null, 2) + '\n');
        // --fix resolved them, do not count as outstanding issues
      } else {
        console.log(`    Run: ldm doctor --fix to remove ${broken.length} dangling MCP entr${broken.length === 1 ? 'y' : 'ies'}`);
        issues += broken.length;
      }
    } else if (ccUser?.mcpServers && Object.keys(ccUser.mcpServers).length > 0) {
      console.log(`  + MCP entries under LDM/OC extensions: all paths exist and parse`);
    }
  }

  // 3c. Cron target health (parallel to crystal doctor's checkCaptureShim)
  //
  // When an extension wires a shim into ~/.ldm/bin/ via cron, the cron
  // line is sticky: it keeps firing even if the shim file goes missing
  // for any reason. crystal doctor catches this for crystal-capture.sh,
  // but any cron line referencing ~/.ldm/bin/<file> is at the same risk
  // class. Walk the crontab and surface broken bin-targeted entries
  // explicitly. Read-only by default; --fix restores known shims from
  // their extension dist when the canonical source is present on disk.
  {
    const ldmBinPrefix = join(LDM_ROOT, 'bin') + '/';
    let crontab = '';
    try {
      crontab = execSync('crontab -l 2>/dev/null', { encoding: 'utf-8' });
    } catch {}
    function expandTilde(p) {
      return p.startsWith('~') ? join(HOME, p.slice(1)) : p;
    }
    function extractCronTarget(line) {
      const trimmed = line.trim();
      if (!trimmed.startsWith('*')) return null;
      const tokens = trimmed.split(/\s+/);
      if (tokens.length < 6) return null;
      const expanded = expandTilde(tokens[5]);
      return expanded.startsWith(ldmBinPrefix) ? expanded : null;
    }
    const cronTargets = new Map();    // path → ['missing'|'not executable']
    const seenTargets = new Set();    // every bin-targeted path we found
    for (const line of crontab.split('\n')) {
      const expanded = extractCronTarget(line);
      if (!expanded) continue;
      seenTargets.add(expanded);
      if (cronTargets.has(expanded)) continue;
      const problems = [];
      if (!existsSync(expanded)) {
        problems.push('missing');
      } else if ((statSync(expanded).mode & 0o111) === 0) {
        problems.push('not executable');
      }
      if (problems.length > 0) cronTargets.set(expanded, problems);
    }
    if (cronTargets.size > 0) {
      // Manifest-driven lookup. Aggregates LDM CLI's wipLdmOs.binFiles
      // and every registered extension's openclaw.plugin.json#binFiles.
      // If aggregation reports a conflict, the lookup stays empty and
      // each broken target becomes "owner unknown" until the conflict
      // is resolved at the package-manifest layer.
      const { aggregateBinManifest } = await import('../lib/bin-manifest.mjs');
      const drManifest = aggregateBinManifest({
        ldmCliRoot: join(__dirname, '..'),
        extensionsRoot: LDM_EXTENSIONS,
        binDir: join(LDM_ROOT, 'bin'),
        registry: readJSON(REGISTRY_PATH) || { extensions: {} },
      });
      const knownSources = {};
      const declarers = {};
      if (drManifest.conflicts.length === 0) {
        for (const e of drManifest.entries) {
          knownSources[e.name] = e.sourcePath;
          declarers[e.name] = e.declarer;
        }
      } else {
        console.log(`  ! bin manifest conflict: ${drManifest.conflicts.length}; restore disabled until resolved`);
      }
      let healed = 0;
      for (const [path, problems] of cronTargets) {
        const detail = problems.join(', ');
        console.log(`  ! cron target ${detail}: ${path}`);
        const base = basename(path);
        const src = knownSources[base];
        if (FIX_FLAG && src && existsSync(src)) {
          try {
            mkdirSync(dirname(path), { recursive: true });
            cpSync(src, path);
            chmodSync(path, 0o755);
            console.log(`  + Restored ${base} from ${src.replace(HOME, '~')}`);
            healed++;
          } catch (e) {
            console.log(`    Restore failed: ${e.message}`);
          }
        } else if (src) {
          console.log(`    Run: ldm doctor --fix to restore from ${src.replace(HOME, '~')}`);
        } else {
          console.log(`    Owner unknown; consult the extension that registered this cron entry`);
        }
      }
      issues += cronTargets.size - healed;
    } else if (seenTargets.size > 0) {
      console.log(`  + Cron targets under ~/.ldm/bin/: ${seenTargets.size} entr${seenTargets.size === 1 ? 'y' : 'ies'}, all exist and executable`);
    }
  }

  // 4. Check sacred locations
  const sacred = [
    { path: join(LDM_ROOT, 'memory'), label: 'memory/' },
    { path: join(LDM_ROOT, 'agents'), label: 'agents/' },
    { path: join(LDM_ROOT, 'state'), label: 'state/' },
    { path: join(LDM_ROOT, 'sessions'), label: 'sessions/' },
    { path: join(LDM_ROOT, 'messages'), label: 'messages/' },
  ];

  for (const s of sacred) {
    if (existsSync(s.path)) {
      console.log(`  + ${s.label} exists`);
    } else {
      console.log(`  ! ${s.label} missing (run: ldm init)`);
      issues++;
    }
  }

  // 5. Check settings.json for hooks
  const settingsPath = join(HOME, '.claude', 'settings.json');
  const settings = readJSON(settingsPath);
  if (settings?.hooks) {
    const hookCount = Object.values(settings.hooks).reduce((sum, arr) => sum + (arr?.length || 0), 0);
    console.log(`  + Claude Code hooks: ${hookCount} configured`);

    // Check for stale hook paths
    let staleHooks = 0;
    for (const [event, hookGroups] of Object.entries(settings.hooks)) {
      if (!Array.isArray(hookGroups)) continue;
      for (const group of hookGroups) {
        for (const h of (group.hooks || [])) {
          if (!h.command) continue;
          const match = h.command.match(/node\s+"?([^"]+)"?\s*$/);
          if (!match) continue;
          const hookPath = match[1];
          const isTmpPath = hookPath.startsWith('/tmp/') || hookPath.startsWith('/private/tmp/');
          if (!existsSync(hookPath) || isTmpPath) {
            staleHooks++;
            if (!FIX_FLAG) {
              const reason = isTmpPath ? '(temp path)' : '(missing)';
              console.log(`  ! Stale hook: ${event} -> ${hookPath} ${reason}`);
            }
          }
        }
      }
    }
    if (staleHooks > 0 && !FIX_FLAG) {
      console.log(`    Run: ldm doctor --fix to clean ${staleHooks} stale hook(s)`);
      issues += staleHooks;
    }
  } else {
    console.log(`  - Claude Code hooks: none configured`);
  }

  // 6. MCP servers
  const mcpCount = Object.keys(state.mcp).length;
  console.log(`  + MCP servers: ${mcpCount} registered`);

  // 7. CLI binaries
  const binCount = Object.keys(state.cliBinaries).length;
  if (binCount > 0) {
    console.log(`  + CLI binaries: ${Object.keys(state.cliBinaries).join(', ')}`);
  }

  // 8. LaunchAgents health check
  const managedAgents = [
    'ai.openclaw.ldm-backup',
    'ai.openclaw.healthcheck',
    'ai.openclaw.gateway',
  ];
  const launchAgentsDir = join(HOME, 'Library', 'LaunchAgents');
  const launchAgentsSrc = join(__dirname, '..', 'shared', 'launchagents');

  // Read gateway token for template comparison
  let doctorGatewayToken = '';
  try {
    const ocConfig = JSON.parse(readFileSync(join(HOME, '.openclaw', 'openclaw.json'), 'utf8'));
    doctorGatewayToken = ocConfig?.gateway?.auth?.token || '';
  } catch {}

  let launchOk = 0;
  let launchIssues = 0;
  for (const label of managedAgents) {
    const plistFile = `${label}.plist`;
    const deployedPath = join(launchAgentsDir, plistFile);
    const srcPath = join(launchAgentsSrc, plistFile);

    if (!existsSync(deployedPath)) {
      console.log(`  x LaunchAgent ${label}: plist missing from ~/Library/LaunchAgents/`);
      launchIssues++;
      continue;
    }

    // Check if deployed plist matches source template (after placeholder substitution)
    if (existsSync(srcPath)) {
      let srcContent = readFileSync(srcPath, 'utf8');
      srcContent = srcContent.replace(/\{\{HOME\}\}/g, HOME);
      srcContent = srcContent.replace(/\{\{OPENCLAW_GATEWAY_TOKEN\}\}/g, doctorGatewayToken);
      const deployedContent = readFileSync(deployedPath, 'utf8');
      if (srcContent !== deployedContent) {
        console.log(`  ! LaunchAgent ${label}: plist out of date (run: ldm install)`);
        launchIssues++;
        continue;
      }
    }

    // Check if loaded via launchctl
    try {
      const result = execSync(`launchctl list 2>/dev/null | grep "${label}"`, { encoding: 'utf8', stdio: ['pipe', 'pipe', 'pipe'] });
      if (result.trim()) {
        launchOk++;
      } else {
        console.log(`  ! LaunchAgent ${label}: plist exists but not loaded`);
        launchIssues++;
      }
    } catch {
      console.log(`  ! LaunchAgent ${label}: plist exists but not loaded`);
      launchIssues++;
    }
  }
  if (launchOk > 0) {
    console.log(`  + LaunchAgents: ${launchOk}/${managedAgents.length} loaded`);
  }
  if (launchIssues > 0) {
    issues += launchIssues;
  }

  console.log('');
  if (issues === 0) {
    console.log('  All checks passed.');
  } else {
    console.log(`  ${issues} issue(s) found.`);
  }
  console.log('');
}

// ── ldm status ──

function cmdStatus() {
  const version = readJSON(VERSION_PATH);
  const registry = readJSON(REGISTRY_PATH);
  const extCount = Object.keys(registry?.extensions || {}).length;

  if (JSON_OUTPUT) {
    console.log(JSON.stringify({
      version: version?.version || null,
      installed: version?.installed || null,
      updated: version?.updated || null,
      extensions: extCount,
      ldmRoot: LDM_ROOT,
    }, null, 2));
    return;
  }

  if (!version) {
    console.log('  LDM OS not installed. Run: ldm init');
    return;
  }

  // Check CLI version against npm
  let cliUpdate = null;
  try {
    const latest = execSync('npm view @wipcomputer/wip-ldm-os version 2>/dev/null', {
      encoding: 'utf8', timeout: 10000,
    }).trim();
    if (latest && semverNewer(latest, PKG_VERSION)) cliUpdate = latest;
  } catch {}

  // Check extensions against npm using registry source info (#262)
  const updates = [];
  for (const [name, info] of Object.entries(registry?.extensions || {})) {
    // Use registry source.npm (v2) or fall back to extension's package.json
    let npmPkg = info?.source?.npm || null;
    if (!npmPkg) {
      const extPkgPath = join(LDM_EXTENSIONS, name, 'package.json');
      const extPkg = readJSON(extPkgPath);
      npmPkg = extPkg?.name;
    }
    if (!npmPkg) continue;
    const currentVersion = info?.installed?.version || info.version;
    if (!currentVersion) continue;
    try {
      const latest = execSync(`npm view ${npmPkg} version 2>/dev/null`, {
        encoding: 'utf8', timeout: 10000,
      }).trim();
      if (latest && semverNewer(latest, currentVersion)) {
        updates.push({ name, current: currentVersion, latest, npm: npmPkg });
      }
    } catch {}
  }

  console.log('');
  console.log(`  LDM OS v${version.version}${cliUpdate ? ` (v${cliUpdate} available)` : ' (latest)'}`);
  console.log(`  Installed: ${version.installed?.split('T')[0]}`);
  console.log(`  Updated:   ${version.updated?.split('T')[0]}`);
  console.log(`  Extensions: ${extCount}${updates.length > 0 ? `, ${updates.length} update(s) available` : ', all up to date'}`);
  console.log(`  Root: ${LDM_ROOT}`);

  if (updates.length > 0) {
    console.log('');
    console.log('  Updates available:');
    for (const u of updates) {
      console.log(`    ${u.name}: v${u.current} -> v${u.latest} (${u.npm})`);
    }
    console.log('');
    console.log('  Run: ldm install');
  }

  if (cliUpdate) {
    console.log(`  CLI update: npm install -g @wipcomputer/wip-ldm-os@${cliUpdate}`);
  }

  console.log('');
}

// ── ldm sessions ──

// ── ldm backup ──

async function cmdBackup() {
  const BACKUP_SCRIPT = join(LDM_ROOT, 'bin', 'ldm-backup.sh');

  if (!existsSync(BACKUP_SCRIPT)) {
    console.error('  x Backup script not found at ' + BACKUP_SCRIPT);
    console.error('  Run: ldm install (deploys the backup script)');
    process.exit(1);
  }

  const backupArgs = [];
  if (DRY_RUN) backupArgs.push('--dry-run');

  // --full is explicit but currently all backups are full (incrementals are Phase 2)
  // Accept it as a no-op so the command reads naturally: ldm backup --full
  const FULL_FLAG = args.includes('--full');

  // --keep N: pass through to backup script
  const keepIndex = args.indexOf('--keep');
  if (keepIndex !== -1 && args[keepIndex + 1]) {
    backupArgs.push('--keep', args[keepIndex + 1]);
  }

  // --pin: mark the latest backup to skip rotation
  const pinIndex = args.indexOf('--pin');
  if (pinIndex !== -1) {
    const reason = args[pinIndex + 1] || 'pinned';
    // Find latest backup dir
    const backupRoot = join(LDM_ROOT, 'backups');
    let dirs = [];
    try {
      dirs = readdirSync(backupRoot)
        .filter(d => d.match(/^20\d\d-\d\d-\d\d--/))
        .sort()
        .reverse();
    } catch {}
    if (dirs.length === 0) {
      console.error('  x No backups found to pin.');
      process.exit(1);
    }
    const latest = dirs[0];
    const pinFile = join(backupRoot, latest, '.pinned');
    writeFileSync(pinFile, `Pinned: ${reason}\nDate: ${new Date().toISOString()}\n`);
    console.log(`  + Pinned backup ${latest}: ${reason}`);
    console.log('  This backup will be skipped during rotation.');
    return;
  }

  // --unpin: remove .pinned marker from the latest (or specified) backup
  const unpinIndex = args.indexOf('--unpin');
  if (unpinIndex !== -1) {
    const backupRoot = join(LDM_ROOT, 'backups');
    let dirs = [];
    try {
      dirs = readdirSync(backupRoot)
        .filter(d => d.match(/^20\d\d-\d\d-\d\d--/))
        .sort()
        .reverse();
    } catch {}
    // Find first pinned backup
    let unpinned = false;
    for (const d of dirs) {
      const pinFile = join(backupRoot, d, '.pinned');
      if (existsSync(pinFile)) {
        unlinkSync(pinFile);
        console.log(`  - Unpinned backup ${d}`);
        unpinned = true;
        break;
      }
    }
    if (!unpinned) {
      console.log('  No pinned backups found.');
    }
    return;
  }

  // --list: show existing backups with pinned status
  const LIST_FLAG = args.includes('--list');
  if (LIST_FLAG) {
    const backupRoot = join(LDM_ROOT, 'backups');
    let dirs = [];
    try {
      dirs = readdirSync(backupRoot)
        .filter(d => d.match(/^20\d\d-\d\d-\d\d--/))
        .sort()
        .reverse();
    } catch {}
    if (dirs.length === 0) {
      console.log('  No backups found.');
      return;
    }
    console.log('');
    console.log('  Backups:');
    for (const d of dirs) {
      const pinFile = join(backupRoot, d, '.pinned');
      const pinned = existsSync(pinFile);
      let size = '?';
      try {
        size = execSync(`du -sh "${join(backupRoot, d)}" | cut -f1`, { encoding: 'utf8', timeout: 10000 }).trim();
      } catch {}
      const marker = pinned ? ' [pinned]' : '';
      console.log(`  ${d}  ${size}${marker}`);
    }
    console.log('');
    return;
  }

  if (FULL_FLAG) {
    console.log('  Running full backup...');
  } else {
    console.log('  Running backup...');
  }
  console.log('');
  try {
    execSync(`bash "${BACKUP_SCRIPT}" ${backupArgs.join(' ')}`, {
      stdio: 'inherit',
      timeout: 600000,
    });
  } catch (e) {
    console.error('  x Backup failed: ' + e.message);
    process.exit(1);
  }
}

// ── ldm sessions ──

async function cmdSessions() {
  const { listSessions } = await import('../lib/sessions.mjs');
  const sessions = listSessions({ includeStale: CLEANUP_FLAG });

  if (CLEANUP_FLAG) {
    // listSessions already cleans stale when includeStale is false.
    // With --cleanup, we list stale ones so user can see them, then re-run without stale.
    const stale = sessions.filter(s => !s.alive);
    if (stale.length > 0) {
      const { deregisterSession } = await import('../lib/sessions.mjs');
      for (const s of stale) {
        deregisterSession(s.name);
      }
      console.log(`  Cleaned ${stale.length} stale session(s).`);
    } else {
      console.log('  No stale sessions found.');
    }
    console.log('');
    return;
  }

  const live = sessions.filter(s => s.alive);

  if (JSON_OUTPUT) {
    console.log(JSON.stringify(live, null, 2));
    return;
  }

  console.log('');
  console.log('  Active Sessions');
  console.log('  ────────────────────────────────────');

  if (live.length === 0) {
    console.log('  No active sessions.');
  } else {
    for (const s of live) {
      const age = timeSince(s.startTime);
      console.log(`  ${s.name}  agent=${s.agentId}  pid=${s.pid}  up=${age}`);
    }
  }

  console.log('');
}

function timeSince(isoString) {
  try {
    const ms = Date.now() - new Date(isoString).getTime();
    const secs = Math.floor(ms / 1000);
    if (secs < 60) return `${secs}s`;
    const mins = Math.floor(secs / 60);
    if (mins < 60) return `${mins}m`;
    const hours = Math.floor(mins / 60);
    if (hours < 24) return `${hours}h ${mins % 60}m`;
    const days = Math.floor(hours / 24);
    return `${days}d ${hours % 24}h`;
  } catch {
    return '?';
  }
}

// ── ldm msg ──

async function cmdMsg() {
  const subcommand = args[1];

  if (!subcommand || subcommand === 'list') {
    return cmdMsgList();
  }
  if (subcommand === 'send') {
    return cmdMsgSend();
  }
  if (subcommand === 'broadcast') {
    return cmdMsgBroadcast();
  }

  console.error(`  Unknown msg subcommand: ${subcommand}`);
  console.error('  Usage: ldm msg [send <to> <body> | list | broadcast <body>]');
  process.exit(1);
}

async function cmdMsgList() {
  const { readMessages } = await import('../lib/messages.mjs');
  const sessionName = process.env.CLAUDE_SESSION_NAME || 'unknown';
  const messages = readMessages(sessionName, { markRead: false });

  if (JSON_OUTPUT) {
    console.log(JSON.stringify(messages, null, 2));
    return;
  }

  console.log('');
  console.log(`  Messages for "${sessionName}"`);
  console.log('  ────────────────────────────────────');

  if (messages.length === 0) {
    console.log('  No pending messages.');
  } else {
    for (const m of messages) {
      const ts = m.timestamp?.split('T')[1]?.split('.')[0] || '';
      console.log(`  [${m.type}] ${ts} from=${m.from}: ${m.body}`);
    }
  }

  console.log('');
}

async function cmdMsgSend() {
  const { sendMessage } = await import('../lib/messages.mjs');
  // args: ['msg', 'send', '<to>', '<body...>']
  const to = args[2];
  const body = args.slice(3).filter(a => !a.startsWith('--')).join(' ');

  if (!to || !body) {
    console.error('  Usage: ldm msg send <to> <body>');
    process.exit(1);
  }

  const sessionName = process.env.CLAUDE_SESSION_NAME || 'ldm-cli';
  const id = sendMessage({ from: sessionName, to, body, type: 'chat' });

  if (id) {
    console.log(`  Message sent to "${to}" (id: ${id})`);
  } else {
    console.error('  x Failed to send message.');
    process.exit(1);
  }
}

async function cmdMsgBroadcast() {
  const { sendMessage } = await import('../lib/messages.mjs');
  // args: ['msg', 'broadcast', '<body...>']
  const body = args.slice(2).filter(a => !a.startsWith('--')).join(' ');

  if (!body) {
    console.error('  Usage: ldm msg broadcast <body>');
    process.exit(1);
  }

  const sessionName = process.env.CLAUDE_SESSION_NAME || 'ldm-cli';
  const id = sendMessage({ from: sessionName, to: 'all', body, type: 'chat' });

  if (id) {
    console.log(`  Broadcast sent (id: ${id})`);
  } else {
    console.error('  x Failed to send broadcast.');
    process.exit(1);
  }
}

// ── ldm updates ──

async function cmdUpdates() {
  if (CHECK_FLAG) {
    // Re-check npm registry
    const { checkForUpdates } = await import('../lib/updates.mjs');
    console.log('  Checking npm for updates...');
    console.log('');
    const result = checkForUpdates();

    if (JSON_OUTPUT) {
      console.log(JSON.stringify(result, null, 2));
      return;
    }

    if (result.updatesAvailable === 0) {
      console.log(`  Checked ${result.checked} extensions. Everything is up to date.`);
    } else {
      console.log(`  Checked ${result.checked} extensions. ${result.updatesAvailable} update(s) available:`);
      console.log('');
      for (const u of result.updates) {
        console.log(`    ${u.name}: ${u.currentVersion} -> ${u.latestVersion} (${u.packageName})`);
      }
      console.log('');
      console.log('  Run: ldm install');
    }
    console.log('');
    return;
  }

  // Show cached results
  const { readUpdateManifest } = await import('../lib/updates.mjs');
  const manifest = readUpdateManifest();

  if (JSON_OUTPUT) {
    console.log(JSON.stringify(manifest || {}, null, 2));
    return;
  }

  console.log('');
  console.log('  Available Updates');
  console.log('  ────────────────────────────────────');

  if (!manifest) {
    console.log('  No update check has been run yet.');
    console.log('  Run: ldm updates --check');
  } else if (manifest.updatesAvailable === 0) {
    console.log(`  Everything is up to date. (checked ${manifest.checkedAt?.split('T')[0] || 'unknown'})`);
  } else {
    console.log(`  ${manifest.updatesAvailable} update(s) available (checked ${manifest.checkedAt?.split('T')[0] || 'unknown'}):`);
    console.log('');
    for (const u of manifest.updates) {
      console.log(`    ${u.name}: ${u.currentVersion} -> ${u.latestVersion}`);
    }
    console.log('');
    console.log('  Run: ldm install');
  }

  console.log('');
}

// ── ldm stack ──

async function cmdStack() {
  const subcommand = args[1];

  if (!subcommand || subcommand === 'list') {
    return cmdStackList();
  }
  if (subcommand === 'install') {
    return cmdStackInstall();
  }

  console.error(`  Unknown stack subcommand: ${subcommand}`);
  console.error('  Usage: ldm stack [list | install <name>]');
  process.exit(1);
}

function loadStacks() {
  return CATALOG.stacks || {};
}

function resolveStack(name) {
  const stacks = loadStacks();
  const stack = stacks[name];
  if (!stack) return null;

  // Resolve "includes" (compose stacks from other stacks)
  let components = [...(stack.components || [])];
  let mcpServers = [...(stack.mcpServers || [])];

  if (stack.includes) {
    for (const inc of stack.includes) {
      const sub = stacks[inc];
      if (sub) {
        components = [...(sub.components || []), ...components];
        mcpServers = [...(sub.mcpServers || []), ...mcpServers];
      }
    }
  }

  // Deduplicate
  components = [...new Set(components)];
  const seenMcp = new Set();
  mcpServers = mcpServers.filter(m => {
    if (seenMcp.has(m.name)) return false;
    seenMcp.add(m.name);
    return true;
  });

  return { ...stack, components, mcpServers };
}

function cmdStackList() {
  const stacks = loadStacks();

  console.log('');
  console.log('  Available Stacks');
  console.log('  ────────────────────────────────────');

  if (Object.keys(stacks).length === 0) {
    console.log('  No stacks defined in catalog.');
    console.log('');
    return;
  }

  for (const [id, stack] of Object.entries(stacks)) {
    const resolved = resolveStack(id);
    console.log(`  ${id}: ${stack.name}`);
    console.log(`    ${stack.description}`);
    if (resolved.components.length > 0) {
      console.log(`    Components:`);
      for (const compId of resolved.components) {
        const entry = findInCatalog(compId);
        console.log(`      - ${entry?.name || compId}`);
      }
    }
    if (resolved.mcpServers.length > 0) {
      console.log(`    MCP Servers:`);
      for (const mcp of resolved.mcpServers) {
        console.log(`      - ${mcp.name}`);
      }
    }
    console.log('');
  }

  console.log('  Install: ldm stack install <name>');
  console.log('  Preview: ldm stack install <name> --dry-run');
  console.log('');
}

async function cmdStackInstall() {
  const stackName = args.slice(2).find(a => !a.startsWith('--'));

  if (!stackName) {
    console.error('  Usage: ldm stack install <name> [--dry-run]');
    console.error('  Run: ldm stack list');
    process.exit(1);
  }

  const stack = resolveStack(stackName);
  if (!stack) {
    console.error(`  Unknown stack: "${stackName}"`);
    console.error('  Run: ldm stack list');
    process.exit(1);
  }

  console.log('');
  console.log(`  Stack: ${stack.name}`);
  console.log(`  ────────────────────────────────────`);
  console.log(`  ${stack.description}`);
  console.log('');

  // Check what's already installed
  const registry = readJSON(REGISTRY_PATH);
  const registeredNames = Object.keys(registry?.extensions || {});

  const ccUserPath = join(HOME, '.claude.json');
  const ccUser = readJSON(ccUserPath);
  const registeredMcp = Object.keys(ccUser?.mcpServers || {});

  // Components
  const componentsToInstall = [];
  const componentsInstalled = [];
  for (const compId of stack.components) {
    const entry = findInCatalog(compId);
    if (!entry) continue;

    // Check if already installed
    const matches = entry.registryMatches || [compId];
    const installed = matches.some(m => registeredNames.includes(m));
    if (installed) {
      componentsInstalled.push(entry);
    } else {
      componentsToInstall.push(entry);
    }
  }

  // MCP servers
  const mcpToInstall = [];
  const mcpInstalled = [];
  for (const mcp of stack.mcpServers) {
    if (registeredMcp.includes(mcp.name)) {
      mcpInstalled.push(mcp);
    } else {
      mcpToInstall.push(mcp);
    }
  }

  // Show status
  if (componentsInstalled.length > 0) {
    console.log(`  Already installed (${componentsInstalled.length}):`);
    for (const c of componentsInstalled) {
      console.log(`    [x] ${c.name}`);
    }
    console.log('');
  }

  if (mcpInstalled.length > 0) {
    console.log(`  MCP servers already registered (${mcpInstalled.length}):`);
    for (const m of mcpInstalled) {
      console.log(`    [x] ${m.name}`);
    }
    console.log('');
  }

  if (componentsToInstall.length > 0) {
    console.log(`  Components to install (${componentsToInstall.length}):`);
    for (const c of componentsToInstall) {
      console.log(`    [ ] ${c.name} (${c.repo})`);
    }
    console.log('');
  }

  if (mcpToInstall.length > 0) {
    console.log(`  MCP servers to add (${mcpToInstall.length}):`);
    for (const m of mcpToInstall) {
      console.log(`    [ ] ${m.name} (${m.command} ${m.args.join(' ')})`);
    }
    console.log('');
  }

  if (componentsToInstall.length === 0 && mcpToInstall.length === 0) {
    console.log('  Everything in this stack is already installed.');
    console.log('');
    return;
  }

  if (DRY_RUN) {
    console.log(`  Would install ${componentsToInstall.length} component(s) and ${mcpToInstall.length} MCP server(s).`);
    console.log('  Dry run complete. No changes made.');
    console.log('');
    return;
  }

  // Install components via ldm install
  let installed = 0;
  for (const c of componentsToInstall) {
    console.log(`  Installing ${c.name}...`);
    try {
      execSync(`ldm install ${c.repo}`, { stdio: 'inherit' });
      installed++;
    } catch (e) {
      console.error(`  x Failed to install ${c.name}: ${e.message}`);
    }
  }

  // Register MCP servers
  let mcpAdded = 0;
  for (const mcp of mcpToInstall) {
    console.log(`  Adding MCP: ${mcp.name}...`);
    try {
      const mcpArgs = mcp.args.map(a => `"${a}"`).join(' ');
      execSync(`claude mcp add --scope user ${mcp.name} -- ${mcp.command} ${mcpArgs}`, { stdio: 'pipe' });
      console.log(`  + MCP: ${mcp.name} registered (user scope)`);
      mcpAdded++;
    } catch (e) {
      // Fallback: write directly to ~/.claude.json
      try {
        const config = readJSON(ccUserPath) || {};
        if (!config.mcpServers) config.mcpServers = {};
        config.mcpServers[mcp.name] = {
          command: mcp.command,
          args: mcp.args,
        };
        writeJSON(ccUserPath, config);
        console.log(`  + MCP: ${mcp.name} registered in ~/.claude.json (fallback)`);
        mcpAdded++;
      } catch (e2) {
        console.error(`  x MCP: ${mcp.name} failed: ${e2.message}`);
      }
    }
  }

  console.log('');
  console.log(`  Done. ${installed} component(s) installed, ${mcpAdded} MCP server(s) added.`);
  console.log('  Restart your session to load new MCP servers.');
  console.log('');
}

// ── ldm catalog show ──

function cmdCatalogShow() {
  const subcommand = args[1];
  const target = args[2];

  if (subcommand === 'show' && target) {
    const entry = loadCatalog().find(c => c.id === target || c.name.toLowerCase() === target.toLowerCase());
    if (!entry) {
      console.error(`  Unknown component: "${target}"`);
      console.error('  Run: ldm catalog');
      process.exit(1);
    }

    console.log('');
    console.log(`  ${entry.name}`);
    console.log('  ────────────────────────────────────');
    console.log(`  ${entry.description}`);
    console.log('');
    console.log(`  Status: ${entry.status}`);
    if (entry.repo) console.log(`  Repo: github.com/${entry.repo}`);
    if (entry.npm) console.log(`  npm: ${entry.npm}`);

    const inst = entry.installs;
    if (inst) {
      console.log('');
      console.log('  What gets installed:');
      if (inst.cli) console.log(`    CLI: ${Array.isArray(inst.cli) ? inst.cli.join(', ') : inst.cli}`);
      if (inst.mcp) console.log(`    MCP tools: ${Array.isArray(inst.mcp) ? inst.mcp.join(', ') : inst.mcp}`);
      if (inst.ocPlugin) console.log(`    OpenClaw plugin: ${inst.ocPlugin}`);
      if (inst.ccHook) console.log(`    CC hooks: ${inst.ccHook}`);
      if (inst.cron) console.log(`    Cron: ${inst.cron}`);
      if (inst.data) console.log(`    Data: ${inst.data}`);
      if (inst.tools) console.log(`    Tools: ${inst.tools}`);
      if (inst.web) console.log(`    Web: ${inst.web}`);
      if (inst.runtime) console.log(`    Runtime: ${inst.runtime}`);
      if (inst.plugins) console.log(`    Plugins: ${inst.plugins}`);
      if (inst.skill) console.log(`    Skill: ${inst.skill}`);
      if (inst.docs) console.log(`    Docs: ${inst.docs}`);
      if (inst.note) console.log(`    Note: ${inst.note}`);
    }

    console.log('');
    return;
  }

  // Default: list all catalog items
  const components = loadCatalog();
  console.log('');
  console.log('  Catalog');
  console.log('  ────────────────────────────────────');
  for (const c of components) {
    console.log(`  ${c.id}: ${c.name} (${c.status})`);
    console.log(`    ${c.description}`);
    console.log('');
  }
  console.log('  Show details: ldm catalog show <name>');
  console.log('');
}

// ── Main ──

async function main() {
  if (!command || command === '--help' || command === '-h') {
    console.log('');
    console.log('  ldm ... LDM OS kernel');
    console.log('');
    console.log('  Usage:');
    console.log('    ldm init                    Scaffold ~/.ldm/ and write version.json');
    console.log('    ldm install <org/repo>      Install from GitHub (clones, detects, deploys)');
    console.log('    ldm install /path/to/repo   Install from local path');
    console.log('    ldm install                 Update all registered extensions');
    console.log('    ldm doctor                  Check health of all extensions');
    console.log('    ldm status                  Show version and extension list');
    console.log('    ldm sessions                List active sessions');
    console.log('    ldm sessions --cleanup      Remove stale session entries');
    console.log('    ldm msg send <to> <body>    Send a message to a session');
    console.log('    ldm msg list                List pending messages');
    console.log('    ldm msg broadcast <body>    Send to all sessions');
    console.log('    ldm stack list               Show available stacks');
    console.log('    ldm stack install <name>     Install a stack (core, web, all)');
    console.log('    ldm backup                  Run a full backup now');
    console.log('    ldm backup --dry-run        Preview what would be backed up (with sizes)');
    console.log('    ldm backup --keep N         Keep last N backups (default: 7)');
    console.log('    ldm backup --pin "reason"   Pin latest backup so rotation skips it');
    console.log('    ldm updates                 Show available updates from cache');
    console.log('    ldm updates --check         Re-check npm registry for updates');
    console.log('');
    console.log('  Flags:');
    console.log('    --dry-run   Show what would happen without making changes');
    console.log('    --json      Output results as JSON');
    console.log('    --cleanup   Remove stale entries (sessions)');
    console.log('    --check     Re-check registry (updates)');
    console.log('');
    console.log('  Interfaces detected:');
    console.log('    CLI        ... package.json bin -> npm install -g');
    console.log('    Module     ... ESM main/exports -> importable');
    console.log('    MCP Server ... mcp-server.mjs -> claude mcp add --scope user');
    console.log('    OpenClaw   ... openclaw.plugin.json -> ~/.ldm/extensions/ + ~/.openclaw/extensions/');
    console.log('    Skill      ... SKILL.md -> ~/.openclaw/skills/<tool>/');
    console.log('    CC Hook    ... guard.mjs or claudeCode.hook -> ~/.claude/settings.json');
    console.log('');
    console.log(`  v${PKG_VERSION}`);
    console.log('');
    process.exit(0);
  }

  // ── ldm enable / disable (#111) ──

  async function cmdEnable() {
    const target = args.slice(1).find(a => !a.startsWith('--'));
    if (!target) {
      console.log('  Usage: ldm enable <extension|stack>');
      console.log('  Example: ldm enable devops-toolbox');
      console.log('  Stacks: core, web, all');
      process.exit(1);
    }

    const { enableExtension } = await import('../lib/deploy.mjs');
    const stacks = loadCatalog()?.stacks || {};
    const components = loadCatalog()?.components || [];

    // Resolve stack to component list
    let names = [target];
    if (stacks[target]) {
      const stack = stacks[target];
      names = stack.components || [];
      if (stack.includes) {
        for (const inc of stack.includes) {
          if (stacks[inc]?.components) names.push(...stacks[inc].components);
        }
      }
    }
    // Map catalog IDs to registry names
    const resolvedNames = [];
    for (const n of names) {
      const comp = components.find(c => c.id === n);
      if (comp) {
        resolvedNames.push(comp.id);
        for (const m of (comp.registryMatches || [])) resolvedNames.push(m);
      } else {
        resolvedNames.push(n);
      }
    }
    const uniqueNames = [...new Set(resolvedNames)];

    const registry = readJSON(REGISTRY_PATH);
    console.log('');
    for (const name of uniqueNames) {
      if (!registry?.extensions?.[name]) continue;
      const result = await enableExtension(name);
      if (result.ok) {
        console.log(`  + ${name}: ${result.reason}`);
      } else {
        console.log(`  ! ${name}: ${result.reason}`);
      }
    }
    console.log('');
  }

  async function cmdDisable() {
    const target = args.slice(1).find(a => !a.startsWith('--'));
    if (!target) {
      console.log('  Usage: ldm disable <extension|stack>');
      process.exit(1);
    }

    const { disableExtension } = await import('../lib/deploy.mjs');
    const stacks = loadCatalog()?.stacks || {};
    const components = loadCatalog()?.components || [];

    let names = [target];
    if (stacks[target]) {
      const stack = stacks[target];
      names = stack.components || [];
      if (stack.includes) {
        for (const inc of stack.includes) {
          if (stacks[inc]?.components) names.push(...stacks[inc].components);
        }
      }
    }
    const resolvedNames = [];
    for (const n of names) {
      const comp = components.find(c => c.id === n);
      if (comp) {
        resolvedNames.push(comp.id);
        for (const m of (comp.registryMatches || [])) resolvedNames.push(m);
      } else {
        resolvedNames.push(n);
      }
    }
    const uniqueNames = [...new Set(resolvedNames)];

    const registry = readJSON(REGISTRY_PATH);
    console.log('');
    for (const name of uniqueNames) {
      if (!registry?.extensions?.[name]) continue;
      const result = disableExtension(name);
      if (result.ok) {
        console.log(`  - ${name}: ${result.reason}`);
      } else {
        console.log(`  ! ${name}: ${result.reason}`);
      }
    }
    console.log('');
  }

  // ── ldm uninstall (#114) ──

  async function cmdUninstall() {
    const keepData = !args.includes('--all');
    const isDryRun = args.includes('--dry-run');

    console.log('');
    console.log('  LDM OS Uninstall');
    console.log('  ────────────────────────────────────');

    if (keepData) {
      console.log('  Your data will be PRESERVED:');
      console.log('    ~/.ldm/memory/     (crystal.db, shared memory)');
      console.log('    ~/.ldm/agents/     (identity, journals, daily logs)');
      console.log('');
      console.log('  Use --all to remove everything including data.');
    } else {
      console.log('  WARNING: --all flag set. ALL data will be removed.');
      console.log('  This includes crystal.db, agent files, journals, everything.');
    }

    console.log('');
    console.log('  Will remove:');

    // 1. MCP servers
    const claudeJsonPath = join(HOME, '.claude.json');
    try {
      const claudeJson = JSON.parse(readFileSync(claudeJsonPath, 'utf8'));
      const mcpNames = Object.keys(claudeJson.mcpServers || {}).filter(n =>
        n.includes('crystal') || n.includes('wip-') || n.includes('memory') ||
        n.includes('grok') || n.includes('lesa') || n.includes('1password')
      );
      if (mcpNames.length > 0) {
        console.log(`    MCP servers: ${mcpNames.join(', ')}`);
      }
    } catch {}

    // 2. CC hooks
    const settingsPath = join(HOME, '.claude', 'settings.json');
    try {
      const settings = JSON.parse(readFileSync(settingsPath, 'utf8'));
      let hookCount = 0;
      for (const [event, entries] of Object.entries(settings.hooks || {})) {
        for (const entry of (Array.isArray(entries) ? entries : [])) {
          for (const h of (entry.hooks || [])) {
            if (h.command?.includes('.ldm') || h.command?.includes('wip-')) hookCount++;
          }
        }
      }
      if (hookCount > 0) console.log(`    CC hooks: ${hookCount} hook(s)`);
    } catch {}

    // 3. Skills
    const skillsDir = join(HOME, '.openclaw', 'skills');
    try {
      const skills = readdirSync(skillsDir).filter(d => d !== '.DS_Store');
      if (skills.length > 0) console.log(`    Skills: ${skills.join(', ')}`);
    } catch {}

    // 4. Cron jobs
    try {
      const crontab = execSync('crontab -l 2>/dev/null', { encoding: 'utf8' });
      const ldmLines = crontab.split('\n').filter(l => l.includes('.ldm') || l.includes('crystal-capture') || l.includes('process-monitor'));
      if (ldmLines.length > 0) console.log(`    Cron jobs: ${ldmLines.length}`);
    } catch {}

    // 5. Global npm packages
    try {
      const npmList = execSync('npm list -g --depth=0 --json 2>/dev/null', { encoding: 'utf8' });
      const deps = JSON.parse(npmList).dependencies || {};
      const wipPkgs = Object.keys(deps).filter(n => n.startsWith('@wipcomputer/'));
      if (wipPkgs.length > 0) console.log(`    npm packages: ${wipPkgs.join(', ')}`);
    } catch {}

    // 6. Directories
    console.log(`    ~/.ldm/extensions/`);
    if (!keepData) {
      console.log(`    ~/.ldm/memory/`);
      console.log(`    ~/.ldm/agents/`);
    }
    console.log(`    ~/.ldm/state/, bin/, hooks/, logs/, sessions/, messages/`);

    if (isDryRun) {
      console.log('');
      console.log('  Dry run. Nothing removed.');
      console.log('');
      return;
    }

    // Confirm
    if (process.stdin.isTTY) {
      const { createInterface } = await import('readline');
      const rl = createInterface({ input: process.stdin, output: process.stdout });
      const answer = await new Promise(resolve => {
        rl.question('\n  Type "uninstall" to confirm: ', resolve);
      });
      rl.close();
      if (answer.trim() !== 'uninstall') {
        console.log('  Cancelled.');
        return;
      }
    }

    console.log('');
    console.log('  Removing...');

    // 1. Unregister MCP servers
    try {
      const claudeJson = JSON.parse(readFileSync(claudeJsonPath, 'utf8'));
      const mcpNames = Object.keys(claudeJson.mcpServers || {}).filter(n =>
        n.includes('crystal') || n.includes('wip-') || n.includes('memory') ||
        n.includes('grok') || n.includes('lesa') || n.includes('1password')
      );
      for (const name of mcpNames) {
        delete claudeJson.mcpServers[name];
      }
      writeFileSync(claudeJsonPath, JSON.stringify(claudeJson, null, 2) + '\n');
      console.log(`  + Removed ${mcpNames.length} MCP server(s)`);
    } catch {}

    // 2. Remove CC hooks
    try {
      const settings = JSON.parse(readFileSync(settingsPath, 'utf8'));
      let removed = 0;
      for (const [event, entries] of Object.entries(settings.hooks || {})) {
        if (!Array.isArray(entries)) continue;
        for (const entry of entries) {
          if (!entry.hooks) continue;
          const before = entry.hooks.length;
          entry.hooks = entry.hooks.filter(h => !h.command?.includes('.ldm') && !h.command?.includes('wip-'));
          removed += before - entry.hooks.length;
        }
        settings.hooks[event] = entries.filter(e => e.hooks?.length > 0);
      }
      writeFileSync(settingsPath, JSON.stringify(settings, null, 2) + '\n');
      console.log(`  + Removed ${removed} CC hook(s)`);
    } catch {}

    // 3. Remove skills
    try {
      const skills = readdirSync(skillsDir).filter(d => d !== '.DS_Store');
      for (const s of skills) {
        execSync(`rm -rf "${join(skillsDir, s)}"`, { stdio: 'pipe' });
      }
      console.log(`  + Removed ${skills.length} skill(s)`);
    } catch {}

    // 4. Remove cron jobs
    try {
      const crontab = execSync('crontab -l 2>/dev/null', { encoding: 'utf8' });
      const filtered = crontab.split('\n').filter(l =>
        !l.includes('.ldm') && !l.includes('crystal-capture') && !l.includes('process-monitor')
      ).join('\n');
      execSync(`echo "${filtered}" | crontab -`, { stdio: 'pipe' });
      console.log('  + Cleaned cron jobs');
    } catch {}

    // 5. Remove npm packages
    try {
      const npmList = execSync('npm list -g --depth=0 --json 2>/dev/null', { encoding: 'utf8' });
      const deps = JSON.parse(npmList).dependencies || {};
      const wipPkgs = Object.keys(deps).filter(n => n.startsWith('@wipcomputer/'));
      for (const pkg of wipPkgs) {
        if (pkg === '@wipcomputer/wip-ldm-os') continue; // uninstall self last
        try { execSync(`npm uninstall -g ${pkg}`, { stdio: 'pipe', timeout: 30000 }); } catch {}
      }
      console.log(`  + Removed ${wipPkgs.length - 1} npm package(s)`);
    } catch {}

    // 6. Remove directories
    const dirsToRemove = ['extensions', 'state', 'bin', 'hooks', 'logs', 'sessions', 'messages', 'shared', '_trash'];
    if (!keepData) {
      dirsToRemove.push('memory', 'agents', 'secrets', 'backups');
    }
    for (const dir of dirsToRemove) {
      const p = join(LDM_ROOT, dir);
      if (existsSync(p)) {
        execSync(`rm -rf "${p}"`, { stdio: 'pipe' });
      }
    }
    // Remove config and version files
    for (const f of ['version.json', 'config.json']) {
      const p = join(LDM_ROOT, f);
      if (existsSync(p)) unlinkSync(p);
    }
    console.log('  + Removed ~/.ldm/ contents');

    if (keepData) {
      console.log('');
      console.log('  Preserved:');
      console.log('    ~/.ldm/memory/   (your data)');
      console.log('    ~/.ldm/agents/   (identity + journals)');
    }

    // 7. Self-uninstall
    console.log('');
    console.log('  To finish, run: npm uninstall -g @wipcomputer/wip-ldm-os');
    console.log('');
    console.log('  LDM OS uninstalled.');
    console.log('');
  }

  // ── ldm worktree ──

  async function cmdWorktree() {
    const sub = args[1] || 'list';

    if (sub === '--help' || sub === '-h') {
      console.log(`
  ldm worktree add <branch>       Create worktree in .worktrees/ (auto-detects repo)
  ldm worktree list                List all worktrees across repos
  ldm worktree clean               Prune worktrees for merged branches
  ldm worktree remove <path>       Remove a specific worktree
`);
      process.exit(0);
    }

    if (sub === 'add') {
      const branchName = args[2];
      if (!branchName) {
        console.error('  Usage: ldm worktree add <branch-name>');
        console.error('  Example: ldm worktree add cc-mini/fix-bug');
        process.exit(1);
      }

      // Auto-detect repo from CWD
      let repoRoot;
      try {
        repoRoot = execSync('git rev-parse --show-toplevel 2>/dev/null', {
          encoding: 'utf8', timeout: 3000
        }).trim();
      } catch {
        console.error('  Not inside a git repo. cd into a repo first.');
        process.exit(1);
      }

      const repoName = basename(repoRoot);
      const branchSuffix = branchName.replace(/\//g, '--');
      const worktreesDir = join(dirname(repoRoot), '.worktrees');
      const worktreePath = join(worktreesDir, `${repoName}--${branchSuffix}`);

      mkdirSync(worktreesDir, { recursive: true });

      console.log(`  Creating worktree for ${repoName}...`);
      console.log(`  Branch: ${branchName}`);
      console.log(`  Path: ${worktreePath}`);

      try {
        execSync(`git worktree add "${worktreePath}" -b "${branchName}"`, {
          cwd: repoRoot, stdio: 'inherit'
        });
        console.log('');
        console.log(`  Done. Work in: ${worktreePath}`);
        console.log(`  When done: ldm worktree remove "${worktreePath}"`);
      } catch (e) {
        console.error(`  Failed: ${e.message}`);
        process.exit(1);
      }
      return;
    }

    if (sub === 'list') {
      // Find all repos and list their worktrees
      const reposBase = process.env.LDM_REPOS || process.cwd();
      let found = 0;

      // Check CWD repo
      try {
        const root = execSync('git rev-parse --show-toplevel 2>/dev/null', {
          encoding: 'utf8', timeout: 3000
        }).trim();
        const result = execSync('git worktree list', {
          cwd: root, encoding: 'utf8', timeout: 5000
        }).trim();
        if (result.split('\n').length > 1) {
          console.log(`  ${basename(root)}:`);
          for (const line of result.split('\n')) {
            console.log(`    ${line}`);
          }
          found++;
        }
      } catch {}

      // Also check .worktrees/ dir
      const worktreesDir = join(dirname(process.cwd()), '.worktrees');
      if (existsSync(worktreesDir)) {
        try {
          const entries = readdirSync(worktreesDir, { withFileTypes: true })
            .filter(d => d.isDirectory());
          if (entries.length > 0) {
            console.log(`  .worktrees/:`);
            for (const d of entries) {
              console.log(`    ${d.name}`);
            }
            found++;
          }
        } catch {}
      }

      if (found === 0) {
        console.log('  No active worktrees found.');
      }
      return;
    }

    if (sub === 'remove') {
      const wtPath = args[2];
      if (!wtPath) {
        console.error('  Usage: ldm worktree remove <path>');
        process.exit(1);
      }
      try {
        // Find the repo root for this worktree
        const root = execSync('git rev-parse --show-toplevel 2>/dev/null', {
          cwd: resolve(wtPath), encoding: 'utf8', timeout: 3000
        }).trim();
        const mainRoot = execSync('git -C "' + root + '" worktree list --porcelain 2>/dev/null', {
          encoding: 'utf8', timeout: 5000
        }).split('\n').find(l => l.startsWith('worktree '))?.replace('worktree ', '');

        execSync(`git worktree remove "${resolve(wtPath)}"`, {
          cwd: mainRoot || root, stdio: 'inherit'
        });
        console.log(`  Removed worktree: ${wtPath}`);
      } catch (e) {
        console.error(`  Failed: ${e.message}`);
        process.exit(1);
      }
      return;
    }

    if (sub === 'clean') {
      console.log('  Pruning stale worktrees...');
      try {
        const root = execSync('git rev-parse --show-toplevel 2>/dev/null', {
          encoding: 'utf8', timeout: 3000
        }).trim();
        execSync('git worktree prune', { cwd: root, stdio: 'inherit' });
        console.log('  Done.');
      } catch (e) {
        console.error(`  Failed: ${e.message}`);
      }
      return;
    }

    console.error(`  Unknown subcommand: ${sub}`);
    console.error('  Run: ldm worktree --help');
    process.exit(1);
  }

  // ── ldm pair ────────────────────────────────────────────────────────
  // Device pairing for Bridge Phase A.
  // Links this machine to the user's Kaleidoscope account via passkey.
  //
  // Flow:
  //   1. Generate a human-readable code (BLUE-FISH-4729)
  //   2. POST the code to wip.computer/api/pair/request
  //   3. User goes to wip.computer/pair on their phone, signs in with passkey, enters code
  //   4. Poll GET /api/pair/status?code=X until approved or expired
  //   5. Store the device token at ~/.ldm/auth/kaleidoscope.json
  //
  // The code is shown in the terminal. The user navigates to the pairing
  // page themselves (CC does NOT open a URL, to prevent phishing).
  // The code expires after 120 seconds.

  async function cmdPair() {
    const PAIR_API = process.env.LDM_PAIR_API || 'https://wip.computer';
    const AUTH_DIR = join(LDM_ROOT, 'auth');
    const TOKEN_PATH = join(AUTH_DIR, 'kaleidoscope.json');

    // Check if already paired
    if (existsSync(TOKEN_PATH)) {
      try {
        const existing = JSON.parse(readFileSync(TOKEN_PATH, 'utf8'));
        if (existing.token) {
          console.log('');
          console.log(`  Already paired as ${existing.userName || 'unknown'}`);
          console.log(`  Paired: ${existing.pairedAt || 'unknown'}`);
          console.log(`  Token: ${existing.token.slice(0, 8)}...`);
          console.log('');
          console.log('  To re-pair, delete ~/.ldm/auth/kaleidoscope.json and run ldm pair again.');
          console.log('');
          return;
        }
      } catch {}
    }

    // Generate code
    const words = [
      'BLUE', 'RED', 'GREEN', 'GOLD', 'GRAY', 'PINK', 'DARK', 'WARM', 'COLD', 'WILD',
      'FISH', 'BIRD', 'WOLF', 'BEAR', 'DEER', 'HAWK', 'FROG', 'LYNX', 'DOVE', 'CROW',
    ];
    const w1 = words[Math.floor(Math.random() * 10)];
    const w2 = words[10 + Math.floor(Math.random() * 10)];
    const num = String(Math.floor(1000 + Math.random() * 9000));
    const code = `${w1}-${w2}-${num}`;

    // Detect device name
    const { hostname } = await import('node:os');
    const deviceName = hostname() || 'unknown';

    // Read agent ID from config
    let agentId = 'cc-mini';
    try {
      const config = JSON.parse(readFileSync(join(LDM_ROOT, 'config.json'), 'utf8'));
      const agents = config.agents || {};
      for (const [id, agent] of Object.entries(agents)) {
        if (agent.harness === 'claude-code') { agentId = id; break; }
      }
    } catch {}

    console.log('');
    console.log('  Pairing code:');
    console.log('');
    console.log(`    ${code}`);
    console.log('');
    console.log('  Go to wip.computer/pair on your phone.');
    console.log('  Sign in with your passkey. Enter the code.');
    console.log('');
    console.log('  Waiting for approval...');

    // Register the code with the server
    try {
      const registerRes = await fetch(`${PAIR_API}/api/pair/request`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, deviceName, agentId }),
      });
      if (!registerRes.ok) {
        const err = await registerRes.text();
        console.error(`  x Failed to register pairing code: ${err}`);
        process.exit(1);
      }
    } catch (err) {
      console.error(`  x Cannot reach ${PAIR_API}: ${err.message}`);
      console.error('  Make sure the server is running.');
      process.exit(1);
    }

    // Poll for approval (every 2 seconds, up to 120 seconds)
    const maxAttempts = 60;
    for (let i = 0; i < maxAttempts; i++) {
      await new Promise(r => setTimeout(r, 2000));

      try {
        const statusRes = await fetch(`${PAIR_API}/api/pair/status?code=${encodeURIComponent(code)}`);
        const data = await statusRes.json();

        if (data.status === 'approved' && data.token) {
          // Store token
          mkdirSync(AUTH_DIR, { recursive: true });
          writeFileSync(TOKEN_PATH, JSON.stringify({
            token: data.token,
            userId: data.userId,
            userName: data.userName,
            deviceName,
            agentId,
            pairedAt: new Date().toISOString(),
            server: PAIR_API,
          }, null, 2) + '\n');

          console.log('');
          console.log(`  ✓ Paired as ${data.userName || 'User'} (${deviceName} / ${agentId})`);
          console.log(`  Token stored at ~/.ldm/auth/kaleidoscope.json`);
          console.log('');
          return;
        }

        if (statusRes.status === 404 || statusRes.status === 410) {
          console.error('');
          console.error('  x Code expired. Run ldm pair again.');
          console.error('');
          process.exit(1);
        }

        // Still pending. Keep polling.
        process.stdout.write('.');
      } catch {
        // Network error. Keep trying.
        process.stdout.write('x');
      }
    }

    console.error('');
    console.error('  x Timed out waiting for approval. Run ldm pair again.');
    console.error('');
    process.exit(1);
  }

  if (command === '--version' || command === '-v') {
    console.log(PKG_VERSION);
    process.exit(0);
  }

  switch (command) {
    case 'init':
      await cmdInit();
      break;
    case 'install':
      await cmdInstall();
      break;
    case 'update':
      // Alias: `ldm update` = `ldm install` (update all registered)
      await cmdUpdateAll();
      break;
    case 'doctor':
      await cmdDoctor();
      break;
    case 'status':
      cmdStatus();
      break;
    case 'sessions':
      await cmdSessions();
      break;
    case 'msg':
      await cmdMsg();
      break;
    case 'stack':
      await cmdStack();
      break;
    case 'catalog':
      cmdCatalogShow();
      break;
    case 'updates':
      await cmdUpdates();
      break;
    case 'enable':
      await cmdEnable();
      break;
    case 'disable':
      await cmdDisable();
      break;
    case 'uninstall':
      await cmdUninstall();
      break;
    case 'worktree':
      await cmdWorktree();
      break;
    case 'backup':
      await cmdBackup();
      break;
    case 'pair':
      await cmdPair();
      break;
    default:
      console.error(`  Unknown command: ${command}`);
      console.error(`  Run: ldm --help`);
      process.exit(1);
  }
}

main().catch(e => {
  console.error(`  x ${e.message}`);
  process.exit(1);
});
