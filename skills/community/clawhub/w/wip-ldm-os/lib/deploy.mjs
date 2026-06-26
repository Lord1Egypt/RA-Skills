/**
 * lib/deploy.mjs
 * Deployment engine for LDM OS extensions.
 * Adapted from wip-universal-installer/install.js with three bugs fixed:
 *   #6: Runs build step for TypeScript extensions
 *   #7: Never rm -rf. Uses incremental copy (deploy to temp, verify, swap).
 *   #8: Respects OpenClaw plugin directory naming from config.
 * Zero external dependencies.
 */

import { execSync } from 'node:child_process';
import {
  existsSync, readFileSync, writeFileSync, copyFileSync, cpSync, mkdirSync,
  lstatSync, readlinkSync, unlinkSync, chmodSync, readdirSync,
  renameSync, rmSync, statSync, symlinkSync,
} from 'node:fs';
import { createHash } from 'node:crypto';
import { join, basename, resolve, dirname } from 'node:path';
import { tmpdir } from 'node:os';
import { detectInterfaces, describeInterfaces, detectToolbox } from './detect.mjs';
import { moveToTrash, appendToManifest } from './safe.mjs';

const HOME = process.env.HOME || '';
const LDM_ROOT = join(HOME, '.ldm');
const LDM_EXTENSIONS = join(LDM_ROOT, 'extensions');
const OC_ROOT = join(HOME, '.openclaw');
const OC_EXTENSIONS = join(OC_ROOT, 'extensions');
const REGISTRY_PATH = join(LDM_EXTENSIONS, 'registry.json');

// ── Logging ──

let DRY_RUN = false;
let JSON_OUTPUT = false;
let INSTALL_ORIGIN = 'manual'; // #262: tracks how an extension was installed

export function setFlags(opts = {}) {
  DRY_RUN = opts.dryRun || false;
  JSON_OUTPUT = opts.jsonOutput || false;
  if (opts.origin) INSTALL_ORIGIN = opts.origin;
}

function log(msg) { if (!JSON_OUTPUT) console.log(`  ${msg}`); }
function ok(msg) { if (!JSON_OUTPUT) console.log(`  + ${msg}`); }
function skip(msg) { if (!JSON_OUTPUT) console.log(`  - ${msg}`); }
function fail(msg) { if (!JSON_OUTPUT) console.error(`  x ${msg}`); }

// ── Helpers ──

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

export function validateSkillFrontmatter(path) {
  let content;
  try {
    content = readFileSync(path, 'utf8');
  } catch (e) {
    return { ok: false, line: 1, message: `cannot read SKILL.md: ${e.message}` };
  }

  const lines = content.split(/\r?\n/);
  if (lines[0] !== '---') {
    return { ok: false, line: 1, message: 'SKILL.md must start with YAML frontmatter' };
  }

  let end = -1;
  for (let i = 1; i < lines.length; i++) {
    if (lines[i] === '---') {
      end = i;
      break;
    }
  }
  if (end === -1) {
    return { ok: false, line: 1, message: 'SKILL.md frontmatter is missing a closing --- marker' };
  }

  for (let i = 1; i < end; i++) {
    const line = lines[i];
    const trimmed = line.trim();
    if (!trimmed || trimmed.startsWith('#') || /^\s/.test(line)) continue;

    const match = /^([A-Za-z0-9_-]+):(?:\s*(.*))?$/.exec(line);
    if (!match) {
      return { ok: false, line: i + 1, message: 'frontmatter line is not a simple key/value mapping' };
    }

    const value = match[2] || '';
    const valueTrimmed = value.trimStart();
    const first = valueTrimmed[0] || '';
    const isQuoted = first === '"' || first === "'";
    const isStructured = first === '[' || first === '{' || first === '|' || first === '>';
    if (valueTrimmed.includes(': ') && !isQuoted && !isStructured) {
      return {
        ok: false,
        line: i + 1,
        message: 'value contains an unquoted colon; quote the scalar value',
      };
    }
  }

  return { ok: true };
}

function ensureBinExecutable(binNames) {
  try {
    const npmPrefix = execSync('npm config get prefix', { encoding: 'utf8' }).trim();
    for (const bin of binNames) {
      const binPath = join(npmPrefix, 'bin', bin);
      try { chmodSync(binPath, 0o755); } catch {}
    }
  } catch {}
}

// ── Registry ──

function loadRegistry() {
  return readJSON(REGISTRY_PATH) || { _format: 'v1', extensions: {} };
}

function saveRegistry(registry) {
  writeJSON(REGISTRY_PATH, registry);
}

// Core extensions are always enabled.
const CORE_EXTENSIONS = new Set(['memory-crystal']);

// ── Harness Detection ──

const LDM_CONFIG_PATH = join(LDM_ROOT, 'config.json');

/**
 * Detect which AI harnesses are installed on this system.
 * Writes results to ~/.ldm/config.json so the installer knows where to deploy.
 */
export function detectHarnesses() {
  const harnesses = {};

  // Claude Code CLI
  const claudeHome = join(HOME, '.claude');
  harnesses['claude-code'] = {
    detected: existsSync(claudeHome),
    home: claudeHome,
    skills: join(claudeHome, 'skills'),
    rules: join(claudeHome, 'rules'),
    settings: join(claudeHome, 'settings.json'),
  };

  // Claude macOS app
  const claudeMacHome = join(HOME, 'Library', 'Application Support', 'Claude');
  harnesses['claude-macos'] = {
    detected: existsSync(claudeMacHome),
    home: claudeMacHome,
  };

  // OpenClaw (Lesa)
  harnesses['openclaw'] = {
    detected: existsSync(OC_ROOT),
    home: OC_ROOT,
    skills: join(OC_ROOT, 'skills'),
    extensions: OC_EXTENSIONS,
  };

  // Codex
  const codexHome = join(HOME, '.codex');
  harnesses['codex'] = {
    detected: existsSync(codexHome),
    home: codexHome,
    skills: join(codexHome, 'skills'),
  };

  // Cursor
  const cursorHome = join(HOME, '.cursor');
  harnesses['cursor'] = {
    detected: existsSync(cursorHome),
    home: cursorHome,
  };

  // Read workspace from existing config
  let workspace = '';
  try {
    const existing = readJSON(LDM_CONFIG_PATH) || {};
    workspace = (existing.workspace || '').replace('~', HOME);
  } catch {}

  // Save to config
  try {
    const existing = readJSON(LDM_CONFIG_PATH) || {};
    existing.harnesses = harnesses;
    writeJSON(LDM_CONFIG_PATH, existing);
  } catch {}

  return { harnesses, workspace };
}

/**
 * Get detected harnesses from config. Runs detection if not cached.
 */
function getHarnesses() {
  try {
    const config = readJSON(LDM_CONFIG_PATH) || {};
    if (config.harnesses) {
      const workspace = (config.workspace || '').replace('~', HOME);
      return { harnesses: config.harnesses, workspace };
    }
  } catch {}
  return detectHarnesses();
}

function updateRegistry(name, info) {
  const registry = loadRegistry();
  const existing = registry.extensions[name];
  const now = new Date().toISOString();

  // Build the v2 registry entry (#262)
  // Merge source info: keep existing source unless new info provides it
  const existingSource = existing?.source;
  let newSource = info._source || existingSource || null;
  // Legacy: info.source was a string (path or URL). Convert to object.
  if (typeof existingSource === 'string' && !newSource) {
    newSource = null; // Drop legacy string source, migration will fix it
  }
  if (typeof info.source === 'string') {
    // Legacy caller passing a string. Don't overwrite structured source.
    if (!newSource || typeof newSource === 'string') newSource = null;
  }

  // Build paths object from ldmPath/ocPath
  const paths = existing?.paths || {};
  if (info.ldmPath) paths.ldm = info.ldmPath;
  if (info.ocPath) paths.openclaw = info.ocPath;
  // Backwards compat: also keep flat ldmPath/ocPath
  const ldmPath = info.ldmPath || existing?.ldmPath || paths.ldm;
  const ocPath = info.ocPath || existing?.ocPath || paths.openclaw;

  // Build installed block
  const installed = existing?.installed || {};
  if (typeof installed === 'object' && installed !== null) {
    installed.version = info.version || installed.version || existing?.version;
    if (!installed.installedAt) installed.installedAt = now;
    installed.updatedAt = now;
  }

  // Origin: keep existing, or use from info, or default to "manual"
  const origin = info._origin || existing?.origin || 'manual';

  registry.extensions[name] = {
    // v2 structured fields (#262)
    source: newSource,
    installed,
    paths,
    interfaces: info.interfaces || existing?.interfaces || [],
    origin,
    // Backwards-compatible flat fields (read by existing code)
    name: info.name || existing?.name || name,
    version: info.version || existing?.version || 'unknown',
    ldmPath,
    ocPath,
    enabled: existing?.enabled ?? true,
    updatedAt: now,
  };
  saveRegistry(registry);
}

/**
 * Build structured source info from a repo path and package.json (#262).
 * Returns { type, repo, npm } or null if we can't determine the source.
 */
function buildSourceInfo(repoPath, pkg) {
  const source = { type: 'github' };
  let hasInfo = false;

  // Extract GitHub repo from package.json repository field
  if (pkg?.repository) {
    const raw = typeof pkg.repository === 'string'
      ? pkg.repository
      : pkg.repository.url || '';
    const ghMatch = raw.match(/github\.com[:/]([^/]+\/[^/.]+)/);
    if (ghMatch) {
      source.repo = ghMatch[1].replace(/\.git$/, '');
      hasInfo = true;
    }
  }

  // Extract npm package name
  if (pkg?.name) {
    source.npm = pkg.name;
    hasInfo = true;
  }

  // If the repo path is itself a git working tree, trust its origin URL.
  // Previously this ran git remote unconditionally, which walks up the
  // directory tree. For npm-sourced installs extracted under ~/.ldm/tmp/
  // (inside the tracked ~/.ldm repo), git happily returned the parent
  // tracking repo's remote (wipcomputer/...-system-private) as the
  // source for every extension. Registry source.repo was therefore
  // unreliable. Now we only consult git if repoPath itself has a .git
  // entry (directory for normal clones, file for worktrees). If it
  // does not, we leave source.repo unset rather than capturing an
  // ancestor's remote.
  if (!source.repo && existsSync(join(repoPath, '.git'))) {
    try {
      const remote = execSync('git remote get-url origin 2>/dev/null', {
        cwd: repoPath,
        encoding: 'utf8',
        timeout: 5000,
      }).trim();
      const ghMatch = remote.match(/github\.com[:/]([^/]+\/[^/.]+)/);
      if (ghMatch) {
        source.repo = ghMatch[1].replace(/\.git$/, '');
        hasInfo = true;
      }
    } catch {}
  }

  return hasInfo ? source : null;
}

// ── Migration detection ──

function findExistingInstalls(toolName, pkg, ocPluginConfig) {
  const matches = [];
  const packageName = pkg?.name;
  const pluginId = ocPluginConfig?.id;

  for (const extDir of [LDM_EXTENSIONS, OC_EXTENSIONS]) {
    if (!existsSync(extDir)) continue;
    let entries;
    try {
      entries = readdirSync(extDir, { withFileTypes: true });
    } catch { continue; }

    for (const entry of entries) {
      if (!entry.isDirectory() && !entry.isSymbolicLink()) continue;
      const dirName = entry.name;
      if (dirName === toolName) continue;
      if (dirName === 'registry.json') continue;

      const dirPath = join(extDir, dirName);

      if (packageName) {
        const dirPkg = readJSON(join(dirPath, 'package.json'));
        if (dirPkg?.name === packageName) {
          if (!matches.some(m => m.dirName === dirName)) {
            matches.push({ dirName, matchType: 'package', path: dirPath });
          }
          continue;
        }
      }

      if (pluginId) {
        const dirPlugin = readJSON(join(dirPath, 'openclaw.plugin.json'));
        if (dirPlugin?.id === pluginId) {
          if (!matches.some(m => m.dirName === dirName)) {
            matches.push({ dirName, matchType: 'plugin-id', path: dirPath });
          }
          continue;
        }
      }
    }
  }

  return matches;
}

// ── Local dependency resolution ──
// Repos with file: dependencies (e.g. memory-crystal -> dream-weaver-protocol)
// fail to build in a clone context where the sibling directory doesn't exist.
// This function resolves those deps from the local LDM installation. No internet needed.

function resolveLocalDeps(repoPath) {
  const pkg = readJSON(join(repoPath, 'package.json'));
  if (!pkg) return;

  const allDeps = { ...pkg.dependencies, ...pkg.optionalDependencies };
  let resolved = 0;

  for (const [name, spec] of Object.entries(allDeps)) {
    if (typeof spec !== 'string' || !spec.startsWith('file:')) continue;

    // This is a file: dependency that won't resolve in a clone
    const extDir = join(LDM_EXTENSIONS, name);
    if (existsSync(extDir)) {
      const targetModules = join(repoPath, 'node_modules', name);
      mkdirSync(join(repoPath, 'node_modules'), { recursive: true });
      // Handle scoped packages (e.g. @scope/name)
      const scopeDir = dirname(targetModules);
      if (scopeDir !== join(repoPath, 'node_modules')) {
        mkdirSync(scopeDir, { recursive: true });
      }
      // Remove existing entry (broken symlink or dir from npm) before creating fresh symlink
      try { rmSync(targetModules, { recursive: true, force: true }); } catch {}
      symlinkSync(extDir, targetModules);
      log(`Linked local dep: ${name} -> ${extDir}`);
      resolved++;
    } else {
      log(`Dep ${name} not installed at ${extDir}, build may fail for this feature`);
    }
  }

  if (resolved > 0) {
    ok(`Resolved ${resolved} file: dep(s) from local LDM installation`);
  }
}

// ── Build step (fix #6) ──

function runBuildIfNeeded(repoPath) {
  const pkg = readJSON(join(repoPath, 'package.json'));
  if (!pkg) return true;

  const hasBuildScript = !!pkg.scripts?.build;
  const distDir = join(repoPath, 'dist');
  const hasPopulatedDist = existsSync(distDir) && readdirSync(distDir).length > 0;

  // Skip build if dist/ already has files (pre-built from npm or GitHub clone).
  if (hasPopulatedDist) {
    log(`Skipping build: dist/ already exists with ${readdirSync(distDir).length} files`);
  } else if (hasBuildScript) {
    log(`Building ${pkg.name || basename(repoPath)}...`);
    try {
      // 1. Install deps first (gets devDependencies like tsup).
      //    npm may warn about unresolvable file: deps but still installs the rest.
      if (!existsSync(join(repoPath, 'node_modules'))) {
        execSync('npm install', { cwd: repoPath, stdio: 'pipe' });
      }

      // 2. Resolve file: deps from local LDM extensions AFTER npm install.
      //    npm install can remove or overwrite symlinks, so this must run second.
      //    Without this, repos like memory-crystal that depend on
      //    file:../dream-weaver-protocol-private fail to build (sibling doesn't exist in clones).
      resolveLocalDeps(repoPath);

      // 3. Build.
      execSync('npm run build', { cwd: repoPath, stdio: 'pipe' });
      ok(`Build complete`);
    } catch (e) {
      fail(`Build failed: ${e.stderr?.toString()?.slice(0, 200) || e.message}`);
      return false;
    }
  }
  return true;
}

// ── Version comparison (fix #7) ──

function compareSemver(a, b) {
  if (!a || !b) return 0;
  if (a === b) return 0;
  const [aBase, aPre] = a.split('-', 2);
  const [bBase, bPre] = b.split('-', 2);
  const pa = aBase.split('.').map(Number);
  const pb = bBase.split('.').map(Number);
  for (let i = 0; i < 3; i++) {
    const na = pa[i] || 0;
    const nb = pb[i] || 0;
    if (na > nb) return 1;
    if (na < nb) return -1;
  }
  // Base versions equal. Stable > prerelease.
  if (!aPre && bPre) return 1;   // a is stable, b is prerelease -> a is newer
  if (aPre && !bPre) return -1;  // a is prerelease, b is stable -> b is newer
  // Both have prereleases. Compare segments.
  if (aPre && bPre) {
    const aSegs = aPre.split('.');
    const bSegs = bPre.split('.');
    for (let i = 0; i < Math.max(aSegs.length, bSegs.length); i++) {
      const as = aSegs[i] || '';
      const bs = bSegs[i] || '';
      const an = Number(as);
      const bn = Number(bs);
      if (!isNaN(an) && !isNaN(bn)) {
        if (an > bn) return 1;
        if (an < bn) return -1;
      } else {
        if (as > bs) return 1;
        if (as < bs) return -1;
      }
    }
  }
  return 0;
}

// Config files that should never be overwritten during updates
const PRESERVE_PATTERNS = [
  'boot-config.json', '.env', '.env.local',
  'config.local.json', 'settings.local.json',
];

function isPreservedFile(filename) {
  return PRESERVE_PATTERNS.some(p => filename === p || filename.endsWith('.local'));
}

// ── Safe deploy (fix #7) ──
// Deploy to temp dir first, then atomic rename. Never rm -rf the live dir.
// Preserves config files from existing installs.

function copyFiltered(src, dest) {
  cpSync(src, dest, {
    recursive: true,
    filter: (s) => !s.includes('.git') && !s.includes('node_modules') && !s.includes('/ai/'),
  });
}

function restorePreservedFiles(oldDir, newDir) {
  if (!existsSync(oldDir)) return;
  try {
    const entries = readdirSync(oldDir);
    for (const entry of entries) {
      if (isPreservedFile(entry)) {
        const oldPath = join(oldDir, entry);
        const newPath = join(newDir, entry);
        if (existsSync(oldPath) && !existsSync(newPath)) {
          cpSync(oldPath, newPath);
          ok(`Preserved config: ${entry}`);
        }
      }
    }
  } catch {}
}

function safeDeployDir(repoPath, destDir, name) {
  const finalPath = join(destDir, name);
  const tempPath = join(tmpdir(), `ldm-deploy-${name}-${Date.now()}`);
  const backupPath = finalPath + '.bak';

  try {
    // 1. Copy to temp
    mkdirSync(tempPath, { recursive: true });
    copyFiltered(repoPath, tempPath);

    // 2. Install deps in temp
    if (existsSync(join(tempPath, 'package.json'))) {
      try {
        execSync('npm install --omit=dev', { cwd: tempPath, stdio: 'pipe' });
      } catch {}
    }

    // 3. Verify staged copy is valid
    if (!existsSync(join(tempPath, 'package.json'))) {
      fail(`Deploy verification failed: no package.json in staged copy`);
      rmSync(tempPath, { recursive: true, force: true });
      return false;
    }

    // 3b. If source has a build script, verify dist/ exists (#69)
    const stagePkg = readJSON(join(tempPath, 'package.json'));
    if (stagePkg?.scripts?.build && !existsSync(join(tempPath, 'dist'))) {
      fail(`Deploy aborted: ${name} has a build script but no dist/. Build failed or was skipped.`);
      rmSync(tempPath, { recursive: true, force: true });
      return false;
    }

    // 4. Swap: old -> backup, temp -> final
    mkdirSync(destDir, { recursive: true });
    if (existsSync(finalPath)) {
      renameSync(finalPath, backupPath);
    }
    renameSync(tempPath, finalPath);

    // 5. Restore preserved config files from old version
    if (existsSync(backupPath)) {
      restorePreservedFiles(backupPath, finalPath);
    }

    // 6. Trash the old version (never delete)
    if (existsSync(backupPath)) {
      const trashed = moveToTrash(backupPath);
      if (trashed) ok(`Old version moved to ${trashed}`);
    }

    return true;
  } catch (e) {
    // Rollback: if temp was moved but something else failed, try to restore backup
    if (!existsSync(finalPath) && existsSync(backupPath)) {
      try { renameSync(backupPath, finalPath); } catch {}
    }
    // Clean up temp if it still exists
    if (existsSync(tempPath)) {
      rmSync(tempPath, { recursive: true, force: true });
    }
    fail(`Deploy failed: ${e.message}`);
    return false;
  }
}

/**
 * Update tools.allow in openclaw.json to include a newly deployed plugin.
 * OpenClaw 2026.4.8+ enforces tools.allow as an exclusive allowlist.
 * Without this, newly installed plugins are blocked from running.
 *
 * This function MUST remain at module top level. Nesting it inside another
 * function puts it out of scope for its call sites in the install handlers
 * and produces a ReferenceError at runtime. See:
 *   ai/product/bugs/installer/2026-04-11--cc-mini--update-tools-allow-reference-error.md
 */
function updateToolsAllow(pluginName) {
  const ocConfigPath = join(OC_ROOT, 'openclaw.json');
  if (!existsSync(ocConfigPath)) return;
  try {
    const raw = readFileSync(ocConfigPath, 'utf8');
    const config = JSON.parse(raw);
    if (!config.tools?.allow || !Array.isArray(config.tools.allow)) return;
    if (config.tools.allow.includes(pluginName)) return;
    config.tools.allow.push(pluginName);
    writeFileSync(ocConfigPath, JSON.stringify(config, null, 2) + '\n');
    log(`Added "${pluginName}" to openclaw.json tools.allow`);
  } catch (e) {
    log(`Warning: failed to update tools.allow for ${pluginName}: ${e.message}`);
  }
}

/**
 * Reconcile tools.allow against plugins.entries in ~/.openclaw/openclaw.json.
 *
 * In OpenClaw 2026.4.8+, any plugin registered in plugins.entries but missing
 * from tools.allow is silently blocked at runtime. Each blocked tool call
 * spawns a root-key approval prompt to the user, flooding iMessage with
 * approve-ids. This was observed on 2026-04-11 for model-provider plugins
 * (anthropic, openai, xai) and imessage, which were enabled in plugins.entries
 * but never added to tools.allow, because the per-plugin updateToolsAllow path
 * only runs during new plugin deploys and the alpha.27/28 ReferenceError had
 * silently dropped those entries anyway.
 *
 * This function is the self-healing step: at install time, walk plugins.entries,
 * find any enabled plugin whose name is not already in tools.allow, and add it.
 * Idempotent. Disabled plugins are skipped. Runs at both ends of installFromPath
 * so a single `ldm install` repairs existing broken state without requiring a
 * new plugin deploy.
 *
 * Background:
 *   ai/product/bugs/code-fka-devopstoolkit/2026-04-11--cc-mini--update-tools-allow-reference-error.md
 *
 * This function MUST remain at module top level, same as updateToolsAllow.
 */
function reconcileToolsAllow() {
  const ocConfigPath = join(OC_ROOT, 'openclaw.json');
  if (!existsSync(ocConfigPath)) return;
  try {
    const raw = readFileSync(ocConfigPath, 'utf8');
    const config = JSON.parse(raw);
    if (!config.plugins?.entries || typeof config.plugins.entries !== 'object') return;
    if (!config.tools?.allow || !Array.isArray(config.tools.allow)) return;

    const enabledPlugins = Object.entries(config.plugins.entries)
      .filter(([, entry]) => entry && entry.enabled !== false)
      .map(([name]) => name);

    const allow = config.tools.allow;
    const missing = enabledPlugins.filter(name => !allow.includes(name));

    if (missing.length === 0) return;

    for (const name of missing) allow.push(name);
    writeFileSync(ocConfigPath, JSON.stringify(config, null, 2) + '\n');
    log(`Reconciled openclaw.json tools.allow: added ${missing.join(', ')}`);
  } catch (e) {
    log(`Warning: failed to reconcile tools.allow: ${e.message}`);
  }
}

// ── OpenClaw plugin naming (fix #8) ──

function resolveOcPluginName(repoPath, toolName) {
  // OpenClaw matches plugins by directory name, not plugin id.
  // Check openclaw.json for existing references to this plugin.
  const ocConfigPath = join(OC_ROOT, 'openclaw.json');
  const ocConfig = readJSON(ocConfigPath);
  if (!ocConfig?.extensions) return toolName;

  const ocPlugin = readJSON(join(repoPath, 'openclaw.plugin.json'));
  if (!ocPlugin?.id) return toolName;

  // Scan openclaw.json extensions array for a matching plugin id
  // and use whatever directory name it expects
  for (const ext of ocConfig.extensions) {
    if (ext.id === ocPlugin.id && ext.path) {
      const existingName = basename(ext.path);
      if (existingName !== toolName) {
        log(`OpenClaw expects plugin at "${existingName}" (not "${toolName}"). Using existing name.`);
        return existingName;
      }
    }
  }

  // Also check if a directory already exists with this plugin's package
  if (existsSync(OC_EXTENSIONS)) {
    try {
      const entries = readdirSync(OC_EXTENSIONS, { withFileTypes: true });
      for (const entry of entries) {
        if (!entry.isDirectory()) continue;
        const dirPlugin = readJSON(join(OC_EXTENSIONS, entry.name, 'openclaw.plugin.json'));
        if (dirPlugin?.id === ocPlugin.id && entry.name !== toolName) {
          log(`OpenClaw has plugin at "${entry.name}" (not "${toolName}"). Using existing name.`);
          return entry.name;
        }
      }
    } catch {}
  }

  return toolName;
}

// ── Install functions ──

function installCLI(repoPath, door) {
  const pkg = readJSON(join(repoPath, 'package.json'));
  const binNames = typeof door.bin === 'string' ? [basename(repoPath)] : Object.keys(door.bin || {});
  const newVersion = pkg?.version;

  // Check if already installed at this version
  if (newVersion && binNames.length > 0) {
    try {
      const installed = execSync(`npm list -g ${pkg.name} --json 2>/dev/null`, { encoding: 'utf8' });
      const data = JSON.parse(installed);
      const deps = data.dependencies || {};
      if (deps[pkg.name]?.version === newVersion) {
        ensureBinExecutable(binNames);
        skip(`CLI: ${binNames.join(', ')} already at v${newVersion}`);
        return true;
      }
    } catch {}
  }

  if (DRY_RUN) {
    ok(`CLI: would install ${binNames.join(', ')} globally (dry run)`);
    return true;
  }

  // Build if needed (fix #6)
  runBuildIfNeeded(repoPath);

  // Prefer registry install over local install (#37).
  // npm install -g . creates symlinks back to the source dir (often /tmp/).
  // npm install -g @scope/pkg copies files. Only fall back to local for unpublished packages.
  const packageName = pkg?.name;
  const packageVersion = pkg?.version;

  if (packageName && packageVersion) {
    try {
      // Check if this version exists on npm
      const npmVersion = execSync(`npm view ${packageName}@${packageVersion} version 2>/dev/null`, {
        encoding: 'utf8',
        timeout: 15000,
      }).trim();

      if (npmVersion === packageVersion) {
        // Install from registry (copies files, no symlinks)
        execSync(`npm install -g ${packageName}@${packageVersion}`, { stdio: 'pipe', timeout: 60000 });
        ensureBinExecutable(binNames);
        ok(`CLI: ${binNames.join(', ')} installed from registry (v${packageVersion})`);
        return true;
      }
    } catch {
      // Registry check failed, fall through
    }

    // Exact version not on npm. Try latest from registry instead of local install (#32, #81)
    try {
      const latestVersion = execSync(`npm view ${packageName} version 2>/dev/null`, {
        encoding: 'utf8', timeout: 15000,
      }).trim();
      if (latestVersion) {
        execSync(`npm install -g ${packageName}@${latestVersion}`, { stdio: 'pipe', timeout: 60000 });
        ensureBinExecutable(binNames);
        ok(`CLI: ${binNames.join(', ')} installed from registry (v${latestVersion}, repo has v${packageVersion})`);
        return true;
      }
    } catch {}
  }

  // Last resort: local install (creates symlinks ... warns user)
  console.log(`  ! Warning: installing locally from ${repoPath} (creates symlinks to source dir)`);
  try {
    execSync('npm install -g .', { cwd: repoPath, stdio: 'pipe' });
    ensureBinExecutable(binNames);
    ok(`CLI: ${binNames.join(', ')} installed locally (symlinked)`);
    return true;
  } catch (e) {
    const stderr = e.stderr?.toString() || '';
    if (stderr.includes('EEXIST')) {
      for (const bin of binNames) {
        try {
          const binPath = execSync('npm config get prefix', { encoding: 'utf8' }).trim() + '/bin/' + bin;
          if (existsSync(binPath) && lstatSync(binPath).isSymbolicLink()) {
            const target = readlinkSync(binPath);
            if (!target.includes(pkg.name.replace(/^@[^/]+\//, ''))) {
              unlinkSync(binPath);
            }
          }
        } catch {}
      }
      try {
        execSync('npm install -g .', { cwd: repoPath, stdio: 'pipe' });
        ensureBinExecutable(binNames);
        ok(`CLI: ${binNames.join(', ')} installed locally (replaced stale symlink)`);
        return true;
      } catch {}
    }
    fail(`CLI: install failed. Run manually: npm install -g ${packageName || '.'}`);
    return false;
  }
}

// Stable content hash over a directory tree. Used by deployExtension to
// decide whether to skip a redeploy. Before this, deployExtension skipped
// when source and deployed had equal versions ... but a prior partial
// install could have bumped the package.json without finishing the copy,
// leaving deployed package.json "current" while other files (guard.mjs,
// core.mjs, etc.) were stale. The 2026-04-20 wip-release 1.9.74 -> 1.9.75
// rollout hit that (source core.mjs had runNpmPublish, deployed didn't,
// both package.jsons reported 1.9.75). Skip only when versions match AND
// content hashes match; otherwise redeploy to heal the drift.
function computeTreeHash(dir) {
  if (!existsSync(dir)) return null;
  const skipNames = new Set([
    '.git', 'node_modules', 'ai', '_trash', '.worktrees', 'logs', 'test', 'tests', '__tests__',
  ]);
  const hash = createHash('sha256');
  function walk(d, rel) {
    let entries;
    try { entries = readdirSync(d, { withFileTypes: true }); }
    catch { return; }
    entries.sort((a, b) => a.name.localeCompare(b.name));
    for (const e of entries) {
      if (skipNames.has(e.name)) continue;
      const p = join(d, e.name);
      const r = rel ? `${rel}/${e.name}` : e.name;
      if (e.isDirectory()) walk(p, r);
      else if (e.isFile()) {
        try {
          hash.update(r);
          hash.update('\0');
          hash.update(readFileSync(p));
          hash.update('\0');
        } catch {}
      }
    }
  }
  walk(dir, '');
  return hash.digest('hex');
}

function deployExtension(repoPath, name) {
  const sourcePkg = readJSON(join(repoPath, 'package.json'));
  const ldmDest = join(LDM_EXTENSIONS, name);
  const installedPkg = readJSON(join(ldmDest, 'package.json'));
  const newVersion = sourcePkg?.version;
  const currentVersion = installedPkg?.version;

  const cmp = compareSemver(newVersion, currentVersion);
  if (newVersion && currentVersion && cmp <= 0) {
    // Versions equal or deployed is newer. Verify content hash before
    // short-circuiting ... a prior partial install could have bumped
    // package.json but not copied the other files, leaving deployed
    // apparently "current" while code is stale.
    const srcHash = computeTreeHash(repoPath);
    const dstHash = computeTreeHash(ldmDest);
    if (srcHash && dstHash && srcHash === dstHash) {
      skip(`LDM: ${name} already at v${currentVersion}${cmp < 0 ? ` (source is older: v${newVersion})` : ''}`);
      // Ensure OC copy exists too
      const ocName = resolveOcPluginName(repoPath, name);
      const ocDest = join(OC_EXTENSIONS, ocName);
      if (!existsSync(ocDest) && !DRY_RUN) {
        mkdirSync(ocDest, { recursive: true });
        cpSync(ldmDest, ocDest, { recursive: true });
        ok(`OpenClaw: synced to ${ocDest}`);
      } else {
        skip(`OpenClaw: ${ocName} already at v${currentVersion}`);
      }
      return true;
    }
    // Content differs despite matching version; fall through to redeploy.
    ok(`LDM: ${name} v${currentVersion} reports same version but content differs; redeploying`);
  }

  if (DRY_RUN) {
    if (currentVersion) {
      ok(`LDM: would upgrade ${name} v${currentVersion} -> v${newVersion} (dry run)`);
    } else {
      ok(`LDM: would deploy ${name} v${newVersion || 'unknown'} to ${ldmDest} (dry run)`);
    }
    ok(`OpenClaw: would deploy (dry run)`);
    return true;
  }

  // Build if needed (fix #6)
  runBuildIfNeeded(repoPath);

  // Safe deploy to LDM (fix #7: no rm -rf)
  if (!safeDeployDir(repoPath, LDM_EXTENSIONS, name)) {
    return false;
  }

  if (currentVersion) {
    ok(`LDM: upgraded ${name} v${currentVersion} -> v${newVersion}`);
  } else {
    ok(`LDM: deployed to ${ldmDest}`);
  }

  // OpenClaw copy (fix #8: respect plugin naming)
  const ocName = resolveOcPluginName(repoPath, name);
  if (!safeDeployDir(ldmDest, OC_EXTENSIONS, ocName)) {
    fail(`OpenClaw: deploy failed for ${ocName}`);
  } else {
    ok(`OpenClaw: deployed to ${join(OC_EXTENSIONS, ocName)}`);
    // Verify openclaw.json references match actual directory
    verifyOcConfig(ocName);
  }

  return true;
}

function verifyOcConfig(pluginDirName) {
  const ocConfigPath = join(OC_ROOT, 'openclaw.json');
  const ocConfig = readJSON(ocConfigPath);
  if (!ocConfig?.extensions) return;

  const pluginPath = join(OC_EXTENSIONS, pluginDirName);
  const pluginJson = readJSON(join(pluginPath, 'openclaw.plugin.json'));
  if (!pluginJson?.id) return;

  // Check if openclaw.json has an entry whose path references a different dir
  for (const ext of ocConfig.extensions) {
    if (ext.id === pluginJson.id) {
      const configDir = basename(ext.path || '');
      if (configDir && configDir !== pluginDirName) {
        log(`Warning: openclaw.json references "${configDir}" but plugin is at "${pluginDirName}"`);
        log(`  Update openclaw.json or rename the directory to match.`);
      }
      return;
    }
  }
}

/**
 * Phase 3b: remove a stale MCP registration for an extension whose current
 * source no longer exposes an MCP interface. Keyed on path, not source
 * metadata (buildSourceInfo is known to capture the parent repo's remote
 * when extraction lands inside another git working tree).
 *
 * Removes the entry from ~/.claude.json#mcpServers if the args path
 * resolves under LDM_EXTENSIONS/<toolName> or OC_EXTENSIONS/<toolName>.
 * No-op if no entry exists or the path points elsewhere.
 */
function unregisterStaleMCP(toolName) {
  const ccUserPath = join(HOME, '.claude.json');
  const ccUser = readJSON(ccUserPath);
  const entry = ccUser?.mcpServers?.[toolName];
  if (!entry) return;

  const firstArg = Array.isArray(entry.args) ? entry.args[0] : null;
  if (!firstArg || typeof firstArg !== 'string') return;

  const ldmExt = join(LDM_EXTENSIONS, toolName);
  const ocExt = join(OC_EXTENSIONS, toolName);
  const pointsHere = firstArg.startsWith(ldmExt + '/') || firstArg.startsWith(ocExt + '/');
  if (!pointsHere) return;

  if (DRY_RUN) {
    ok(`MCP: would unregister stale ${toolName} entry pointing at ${firstArg} (dry run)`);
    return;
  }

  try {
    execSync(`claude mcp remove ${toolName} --scope user`, { stdio: 'pipe' });
    ok(`MCP: unregistered stale ${toolName} entry (source no longer exposes MCP)`);
  } catch {
    // Fallback: direct edit to ~/.claude.json
    try {
      const cfg = readJSON(ccUserPath) || {};
      if (cfg.mcpServers && cfg.mcpServers[toolName]) {
        delete cfg.mcpServers[toolName];
        writeJSON(ccUserPath, cfg);
        ok(`MCP: unregistered stale ${toolName} entry via direct .claude.json edit`);
      }
    } catch (e) {
      log(`Warning: could not unregister stale MCP ${toolName}: ${e.message}`);
    }
  }

  // Also clean OpenClaw side if installed.
  try {
    execSync(`openclaw mcp unset ${toolName}`, { stdio: 'pipe' });
  } catch {
    // Non-fatal. OpenClaw may not be installed, or may not have had this mcp.
  }
}

function registerMCP(repoPath, door, toolName) {
  let rawName = toolName || door.name || basename(repoPath);
  // Strip /tmp/ clone prefixes (ldm-install-, wip-install-)
  rawName = rawName.replace(/^(ldm-install-|wip-install-)/, '');
  const name = rawName.replace(/^@[\w-]+\//, '');
  const ldmServerPath = join(LDM_EXTENSIONS, name, door.file);
  const ldmFallbackPath = join(LDM_EXTENSIONS, basename(repoPath), door.file);
  const repoServerPath = join(repoPath, door.file);
  const mcpPath = existsSync(ldmServerPath) ? ldmServerPath
    : existsSync(ldmFallbackPath) ? ldmFallbackPath
    : repoServerPath;

  // Postcondition: the resolved entrypoint must exist and parse before we
  // touch ~/.claude.json. Previously, if the published tarball did not
  // contain the declared mcp-server file (see wip-1password 0.2.3-alpha.2
  // bug writeup), we still wrote the registration and left a dangling
  // "Failed to connect" entry that was invisible until the user ran
  // `claude mcp list`. Fail loudly instead.
  if (!existsSync(mcpPath)) {
    fail(`MCP: ${name} registration aborted. Resolved path does not exist: ${mcpPath}`);
    fail(`MCP: candidates checked: ${ldmServerPath}, ${ldmFallbackPath}, ${repoServerPath}`);
    fail(`MCP: verify the published package includes "${door.file}" (check files array).`);
    return false;
  }
  try {
    execSync(`node --check "${mcpPath}"`, { stdio: 'pipe', timeout: 5000 });
  } catch (e) {
    const stderr = (e && e.stderr && e.stderr.toString && e.stderr.toString().trim()) || (e && e.message) || 'unknown error';
    fail(`MCP: ${name} registration aborted. Entrypoint failed node --check: ${mcpPath}`);
    fail(`MCP: ${stderr}`);
    return false;
  }

  // Check ~/.claude.json (user-level MCP)
  const ccUserPath = join(HOME, '.claude.json');
  const ccUser = readJSON(ccUserPath);
  const alreadyRegistered = ccUser?.mcpServers?.[name]?.args?.includes(mcpPath);

  if (alreadyRegistered) {
    skip(`MCP: ${name} already registered at ${mcpPath}`);
    return true;
  }

  if (DRY_RUN) {
    ok(`MCP: would register ${name} at user scope (dry run)`);
    return true;
  }

  // Register with Claude Code CLI at user scope
  try {
    try {
      execSync(`claude mcp remove ${name} --scope user`, { stdio: 'pipe' });
    } catch {}
    const envFlag = existsSync(OC_ROOT) ? ` -e OPENCLAW_HOME="${OC_ROOT}"` : '';
    execSync(`claude mcp add --scope user ${name}${envFlag} -- node "${mcpPath}"`, { stdio: 'pipe' });
    ok(`MCP: registered ${name} at user scope`);
  } catch (e) {
    // Fallback: write to ~/.claude.json directly
    try {
      const mcpConfig = readJSON(ccUserPath) || {};
      if (!mcpConfig.mcpServers) mcpConfig.mcpServers = {};
      mcpConfig.mcpServers[name] = {
        command: 'node',
        args: [mcpPath],
      };
      writeJSON(ccUserPath, mcpConfig);
      ok(`MCP: registered ${name} in ~/.claude.json (fallback)`);
    } catch (e2) {
      fail(`MCP: registration failed. ${e.message}`);
      return false;
    }
  }

  // Also register with OpenClaw so the MCP tools are available to all
  // OpenClaw agents (e.g. Lēsa) without exec-approval gates. CC
  // registration alone only gives tools to Claude Code sessions, not
  // to OpenClaw's agent pipeline. Discovered 2026-04-11 when Lēsa
  // lost xAI image gen tools after switching from Grok to Claude CLI.
  try {
    const ocMcpConfig = JSON.stringify({ command: 'node', args: [mcpPath] });
    execSync(`openclaw mcp set ${name} '${ocMcpConfig}'`, { stdio: 'pipe' });
    ok(`MCP: registered ${name} with OpenClaw`);
  } catch {
    // Non-fatal: OpenClaw may not be installed on all machines
  }

  // Add to OpenClaw tools.allow so the MCP tools are pre-authorized
  updateToolsAllow(name);

  return true;
}

/**
 * Install Claude Code hook(s) for an extension.
 *
 * Accepts either a single door object (legacy) or an array of door objects
 * (new in 2026-04-05 for wip-branch-guard 1.9.73 which registers on both
 * PreToolUse and SessionStart). Normalizes to an array and installs each
 * door independently.
 *
 * Returns true if at least one door installed successfully.
 */
function installClaudeCodeHook(repoPath, doorOrDoors) {
  const doors = Array.isArray(doorOrDoors) ? doorOrDoors : [doorOrDoors];
  let anyOk = false;
  for (const door of doors) {
    if (installClaudeCodeHookEvent(repoPath, door)) {
      anyOk = true;
    }
  }
  return anyOk;
}

function installClaudeCodeHookEvent(repoPath, door) {
  const settingsPath = join(HOME, '.claude', 'settings.json');
  let settings = readJSON(settingsPath);

  if (!settings) {
    skip(`Claude Code: no settings.json found`);
    return false;
  }

  const toolName = basename(repoPath);
  const extDir = join(LDM_EXTENSIONS, toolName);
  const installedGuard = join(extDir, 'guard.mjs');

  // Deploy guard.mjs to ~/.ldm/extensions/{toolName}/ (#85: always update, not just when missing)
  // Idempotent across multi-door invocations: two doors on the same repo
  // will both trigger this copy, which is a filesystem no-op after the first.
  //
  // Also recursively copy sibling source subdirectories (e.g. lib/, dist/).
  // Historical behavior only copied guard.mjs + package.json at the root,
  // so a guard.mjs whose imports referenced ./lib/*.mjs loaded fine from
  // source but broke post-install with ERR_MODULE_NOT_FOUND. This caused
  // the wip-branch-guard 1.9.77 incident on 2026-04-20.
  const srcGuard = join(repoPath, 'guard.mjs');
  const SKIP_DIRS_FOR_HOOK = new Set([
    '.git', 'node_modules', 'ai', '_trash', '.worktrees', 'logs', 'test', 'tests', '__tests__',
  ]);
  if (existsSync(srcGuard)) {
    try {
      if (!existsSync(extDir)) mkdirSync(extDir, { recursive: true });
      copyFileSync(srcGuard, installedGuard);
      // Also copy package.json for metadata
      const srcPkg = join(repoPath, 'package.json');
      if (existsSync(srcPkg)) copyFileSync(srcPkg, join(extDir, 'package.json'));
      // Recurse sibling subdirs so nested imports (e.g. ./lib/foo.mjs) load.
      for (const entry of readdirSync(repoPath, { withFileTypes: true })) {
        if (!entry.isDirectory()) continue;
        if (SKIP_DIRS_FOR_HOOK.has(entry.name)) continue;
        const srcDir = join(repoPath, entry.name);
        const destDir = join(extDir, entry.name);
        try { cpSync(srcDir, destDir, { recursive: true }); } catch {}
      }
    } catch (e) {
      // Non-fatal: fall back to source path
    }
  }

  const hookCommand = existsSync(installedGuard)
    ? `node ${installedGuard}`
    : (door.command || `node "${srcGuard}"`);

  const event = door.event || 'PreToolUse';

  if (DRY_RUN) {
    ok(`Claude Code: would add ${event} hook (dry run)`);
    return true;
  }

  if (!settings.hooks) settings.hooks = {};
  if (!settings.hooks[event]) settings.hooks[event] = [];

  // Match existing entries by command path alone (same extension + same
  // event). The previous finder required matcher equality too, so when
  // an extension bumped its matcher (e.g. wip-branch-guard 1.9.78 -> 1.9.79
  // added Read|Glob to enable onboarding), the finder missed the old entry
  // and appended a new one, leaving an orphaned old matcher in settings
  // and doubling hook invocations on overlapping matchers.
  //
  // Now: find by extension dir in the command. Update matcher + command +
  // timeout in place. First pass removes any DUPLICATE entries for the same
  // extension in this event slot (orphan cleanup; catches post-1.9.78
  // duplicates on users who already installed the broken version).
  const doorMatcher = door.matcher || undefined;
  const toolTag = `/${toolName}/`;
  const ownedIdxs = [];
  settings.hooks[event].forEach((entry, i) => {
    const hooks = entry.hooks || [];
    if (hooks.some(h => (h.command || '').includes(toolTag))) ownedIdxs.push(i);
  });
  let removed = 0;
  if (ownedIdxs.length > 1) {
    // Keep the first, remove the rest. Walk right-to-left so earlier indices stay valid.
    for (let j = ownedIdxs.length - 1; j >= 1; j--) {
      settings.hooks[event].splice(ownedIdxs[j], 1);
      removed++;
    }
  }
  const existingIdx = ownedIdxs.length > 0 ? ownedIdxs[0] : -1;

  if (existingIdx !== -1) {
    const existingEntry = settings.hooks[event][existingIdx];
    const existingCmd = existingEntry.hooks?.[0]?.command || '';
    const existingMatcher = existingEntry.matcher || undefined;
    if (existingCmd === hookCommand && existingMatcher === doorMatcher && removed === 0) {
      skip(`Claude Code: ${event} hook already configured`);
      return true;
    }
    existingEntry.matcher = doorMatcher;
    existingEntry.hooks[0].command = hookCommand;
    existingEntry.hooks[0].timeout = door.timeout || 10;
    try {
      writeFileSync(settingsPath, JSON.stringify(settings, null, 2) + '\n');
      const note = removed > 0 ? ` (removed ${removed} orphan entr${removed === 1 ? 'y' : 'ies'})` : '';
      ok(`Claude Code: ${event} hook updated${note}`);
      return true;
    } catch (e) {
      fail(`Claude Code: failed to update settings.json. ${e.message}`);
      return false;
    }
  }

  settings.hooks[event].push({
    matcher: doorMatcher,
    hooks: [{
      type: 'command',
      command: hookCommand,
      timeout: door.timeout || 10,
    }],
  });

  try {
    writeFileSync(settingsPath, JSON.stringify(settings, null, 2) + '\n');
    ok(`Claude Code: ${event} hook added`);
    return true;
  } catch (e) {
    fail(`Claude Code: failed to update settings.json. ${e.message}`);
    return false;
  }
}

function installSkill(repoPath, toolName) {
  const { harnesses, workspace } = getHarnesses();

  // Find SKILL.md source: repo path first, then permanent copy at ~/.ldm/extensions/
  let skillSrc = join(repoPath, 'SKILL.md');
  const permanentSkill = join(LDM_EXTENSIONS, toolName, 'SKILL.md');
  if (!existsSync(skillSrc) && existsSync(permanentSkill)) skillSrc = permanentSkill;
  if (!existsSync(skillSrc)) return false;

  const frontmatter = validateSkillFrontmatter(skillSrc);
  if (!frontmatter.ok) {
    fail(`Skill: invalid SKILL.md frontmatter at ${skillSrc}:${frontmatter.line}: ${frontmatter.message}`);
    return false;
  }

  // Find references/ source: repo path first, then permanent copy
  let refsSrc = join(repoPath, 'references');
  const permanentRefs = join(LDM_EXTENSIONS, toolName, 'references');
  if (!existsSync(refsSrc) && existsSync(permanentRefs)) refsSrc = permanentRefs;

  if (DRY_RUN) {
    const targets = Object.entries(harnesses).filter(([,h]) => h.detected && h.skills).map(([name]) => name);
    ok(`Skill: would deploy ${toolName} to ${targets.join(', ')} (dry run)`);
    return true;
  }

  try {
    const deployed = [];

    // 1. Save permanent copy to ~/.ldm/extensions/<name>/ (survives tmp cleanup)
    const ldmSkillDir = join(LDM_EXTENSIONS, toolName);
    mkdirSync(ldmSkillDir, { recursive: true });
    cpSync(skillSrc, join(ldmSkillDir, 'SKILL.md'));
    if (existsSync(refsSrc) && refsSrc !== permanentRefs) {
      cpSync(refsSrc, join(ldmSkillDir, 'references'), { recursive: true });
    }

    // 2. Deploy to every detected harness that has a skills path
    for (const [name, harness] of Object.entries(harnesses)) {
      if (!harness.detected || !harness.skills) continue;
      const dest = join(harness.skills, toolName);
      mkdirSync(dest, { recursive: true });
      cpSync(skillSrc, join(dest, 'SKILL.md'));
      if (existsSync(refsSrc)) {
        cpSync(refsSrc, join(dest, 'references'), { recursive: true });
      }
      deployed.push(name);
    }

    // 3. Deploy references/ to home (workspace settings/docs/skills/)
    if (existsSync(refsSrc) && workspace && existsSync(workspace)) {
      const homeRefsDest = join(workspace, 'settings', 'docs', 'skills', toolName);
      mkdirSync(homeRefsDest, { recursive: true });
      cpSync(refsSrc, homeRefsDest, { recursive: true });
      deployed.push('home');
    }

    ok(`Skill: ${toolName} deployed to ${deployed.join(', ')}`);
    return true;
  } catch (e) {
    fail(`Skill: deploy failed. ${e.message}`);
    return false;
  }
}

// ── Single tool install ──

export function installSingleTool(toolPath) {
  const { interfaces, pkg } = detectInterfaces(toolPath);
  const ifaceNames = Object.keys(interfaces);

  if (ifaceNames.length === 0) return 0;

  // Derive tool name from package.json, never from /tmp/ clone path
  let toolName = pkg?.name?.replace(/^@\w+\//, '') || basename(toolPath);
  // Strip ldm-install- prefix if it leaked from clone path
  toolName = toolName.replace(/^ldm-install-/, '');

  // Migrate ldm-install-* ghost directories (#96)
  // Old installs used /tmp/ldm-install-<name> as source, which leaked into the directory name.
  // If both ldm-install-<name> and <name> exist, remove the ghost and clean the registry.
  const ghostName = `ldm-install-${toolName}`;
  const ghostPath = join(LDM_EXTENSIONS, ghostName);
  if (existsSync(ghostPath) && ghostName !== toolName) {
    if (!DRY_RUN) {
      const trashDir = join(LDM_ROOT, '_trash', new Date().toISOString().split('T')[0]);
      try {
        mkdirSync(trashDir, { recursive: true });
        const trashDest = join(trashDir, ghostName);
        cpSync(ghostPath, trashDest, { recursive: true });
        rmSync(ghostPath, { recursive: true, force: true });
        // Clean registry
        const registry = loadRegistry();
        if (registry.extensions?.[ghostName]) {
          delete registry.extensions[ghostName];
          saveRegistry(registry);
        }
        log(`Migrated ghost directory: ${ghostName} -> _trash/ (real name: ${toolName})`);
      } catch (e) {
        log(`Warning: could not migrate ${ghostName}: ${e.message}`);
      }
    } else {
      log(`Would migrate ghost directory: ${ghostName} -> _trash/ (real name: ${toolName})`);
    }
  }

  if (!JSON_OUTPUT) {
    console.log('');
    console.log(`  Installing: ${toolName}${DRY_RUN ? ' (dry run)' : ''}`);
    console.log(`  ${'─'.repeat(40)}`);
    log(`Detected ${ifaceNames.length} interface(s): ${ifaceNames.join(', ')}`);
    console.log('');
  }

  if (DRY_RUN && !JSON_OUTPUT) {
    console.log(describeInterfaces(interfaces));

    const existing = findExistingInstalls(toolName, pkg, interfaces.openclaw?.config);
    if (existing.length > 0) {
      console.log('');
      for (const m of existing) {
        log(`Migration: would rename "${m.dirName}" -> "${toolName}" (matched by ${m.matchType})`);
      }
    }

    return ifaceNames.length;
  }

  let installed = 0;

  // Build structured source info for registry (#262)
  const sourceInfo = buildSourceInfo(toolPath, pkg);
  const registryInfo = {
    name: toolName,
    version: pkg?.version || 'unknown',
    source: null, // legacy field, kept for backwards compat
    _source: sourceInfo,  // v2 structured source, consumed by updateRegistry
    _origin: INSTALL_ORIGIN, // #262: "catalog", "manual", or "dependency"
    interfaces: ifaceNames,
  };

  if (interfaces.cli) {
    if (installCLI(toolPath, interfaces.cli)) installed++;
  }

  if (interfaces.openclaw) {
    if (deployExtension(toolPath, toolName)) {
      installed++;
      registryInfo.ldmPath = join(LDM_EXTENSIONS, toolName);
      registryInfo.ocPath = join(OC_EXTENSIONS, toolName);
      // Update tools.allow in openclaw.json so OC 2026.4.8+ doesn't block the plugin
      updateToolsAllow(toolName);
    }
  } else if (interfaces.mcp) {
    const extName = basename(toolPath);
    if (deployExtension(toolPath, extName)) {
      registryInfo.ldmPath = join(LDM_EXTENSIONS, extName);
      registryInfo.ocPath = join(OC_EXTENSIONS, extName);
    }
  }

  // Deploy MCP, hooks, and skills for any extension that is enabled OR already deployed.
  // Extensions installed before the enable/disable system have enabled=false in the registry
  // but are already running (MCP registered, hooks in settings.json). Don't block their updates.
  const registry = loadRegistry();
  const registryEntry = registry.extensions?.[toolName];
  const isEnabled = registryEntry?.enabled ?? CORE_EXTENSIONS.has(toolName);
  const isAlreadyDeployed = registryEntry?.ldmPath && existsSync(registryEntry.ldmPath);

  if (interfaces.mcp) {
    if (isEnabled || isAlreadyDeployed) {
      if (registerMCP(toolPath, interfaces.mcp, toolName)) installed++;
    } else {
      skip(`MCP: ${toolName} not enabled. Run: ldm enable ${toolName}`);
    }
  } else {
    // Phase 3b: source no longer exposes an MCP interface (file renamed,
    // moved to src/, removed, etc). If a prior install registered an MCP
    // whose args point into this extension's directory, un-register it so
    // claude mcp list does not keep a dangling "Failed to connect" entry.
    unregisterStaleMCP(toolName);
  }

  if (interfaces.claudeCodeHook) {
    if (isEnabled || isAlreadyDeployed) {
      if (installClaudeCodeHook(toolPath, interfaces.claudeCodeHook)) installed++;
    } else {
      skip(`Hook: ${toolName} not enabled`);
    }
  }

  if (interfaces.skill) {
    // Skills always deploy. They're instruction files, not running code.
    if (installSkill(toolPath, toolName)) installed++;
  }

  if (interfaces.module) {
    ok(`Module: import from "${interfaces.module.main}"`);
    installed++;
  }

  // Update registry
  if (!DRY_RUN) {
    try {
      mkdirSync(LDM_EXTENSIONS, { recursive: true });
      updateRegistry(toolName, registryInfo);
      ok(`Registry: updated`);
    } catch (e) {
      fail(`Registry: update failed. ${e.message}`);
    }
  }

  return installed;
}

// ── Toolbox install ──

export function installToolbox(repoPath) {
  const subTools = detectToolbox(repoPath);
  if (subTools.length === 0) return { tools: 0, interfaces: 0 };

  const toolboxPkg = readJSON(join(repoPath, 'package.json'));
  const toolboxName = toolboxPkg?.name?.replace(/^@\w+\//, '') || basename(repoPath);

  if (!JSON_OUTPUT) {
    console.log('');
    console.log(`  Toolbox: ${toolboxName}`);
    console.log(`  ${'='.repeat(50)}`);
    log(`Found ${subTools.length} sub-tool(s): ${subTools.map(t => t.name).join(', ')}`);
  }

  let totalInstalled = 0;
  let toolsProcessed = 0;

  for (const subTool of subTools) {
    const count = installSingleTool(subTool.path);
    totalInstalled += count;
    if (count > 0) toolsProcessed++;
  }

  if (!JSON_OUTPUT) {
    console.log('');
    console.log(`  ${'='.repeat(50)}`);
    if (DRY_RUN) {
      console.log(`  Dry run complete. ${toolsProcessed} tool(s) scanned, ${totalInstalled} interface(s) detected.`);
    } else {
      console.log(`  Done. ${toolsProcessed} tool(s), ${totalInstalled} interface(s) processed.`);
    }
    console.log('');
  }

  return { tools: toolsProcessed, interfaces: totalInstalled };
}

// ── Full install pipeline ──

export async function installFromPath(repoPath) {
  // Heal tools.allow before any install runs, so the current session picks up
  // any drift left by earlier broken installs (alpha.27/28 ReferenceError).
  // Idempotent: no-op if plugins.entries and tools.allow are already in sync.
  reconcileToolsAllow();

  const subTools = detectToolbox(repoPath);

  if (subTools.length > 0) {
    const result = installToolbox(repoPath);
    // Heal again after toolbox install in case any plugin was newly registered
    // in plugins.entries but never added to tools.allow by its deploy path.
    reconcileToolsAllow();
    return result;
  }

  const installed = installSingleTool(repoPath);

  if (installed === 0) {
    skip('No installable interfaces detected.');
  } else if (!JSON_OUTPUT) {
    console.log('');
    if (DRY_RUN) {
      console.log('  Dry run complete. No changes made.');
    } else {
      console.log(`  Done. ${installed} interface(s) processed.`);
    }
    console.log('');
  }

  // Final reconcile pass after single-tool install, for the same reason as
  // the toolbox branch above.
  reconcileToolsAllow();

  return { tools: 1, interfaces: installed };
}

// ── Enable / Disable (#111) ──

function unregisterMCP(name) {
  try {
    execSync(`claude mcp remove --scope user ${name} 2>/dev/null`, { stdio: 'pipe', timeout: 10000 });
  } catch {}
  // Also clean ~/.claude.json directly
  const claudeJson = join(HOME, '.claude.json');
  try {
    const config = readJSON(claudeJson);
    if (config?.mcpServers?.[name]) {
      delete config.mcpServers[name];
      writeJSON(claudeJson, config);
    }
  } catch {}
}

function removeClaudeCodeHook(name) {
  const settingsPath = join(HOME, '.claude', 'settings.json');
  try {
    const settings = readJSON(settingsPath);
    if (!settings?.hooks) return;
    let changed = false;
    for (const [event, entries] of Object.entries(settings.hooks)) {
      if (!Array.isArray(entries)) continue;
      for (const entry of entries) {
        if (!entry.hooks || !Array.isArray(entry.hooks)) continue;
        const before = entry.hooks.length;
        entry.hooks = entry.hooks.filter(h => !h.command?.includes(name));
        if (entry.hooks.length < before) changed = true;
      }
      // Remove empty entries
      settings.hooks[event] = entries.filter(e => e.hooks?.length > 0);
    }
    if (changed) writeJSON(settingsPath, settings);
  } catch {}
}

function removeSkill(name) {
  const skillDir = join(OC_ROOT, 'skills', name);
  try {
    if (existsSync(skillDir)) {
      rmSync(skillDir, { recursive: true, force: true });
    }
  } catch {}
}

export async function enableExtension(name) {
  const reg = loadRegistry();
  const entry = reg.extensions?.[name];
  if (!entry) return { ok: false, reason: 'not installed' };
  if (entry.enabled) return { ok: true, reason: 'already enabled' };

  const extPath = entry.ldmPath || join(LDM_EXTENSIONS, name);
  if (!existsSync(extPath)) return { ok: false, reason: 'extension dir missing' };

  const { detectInterfaces } = await import('./detect.mjs');
  const { interfaces } = detectInterfaces(extPath);

  if (interfaces.mcp) registerMCP(extPath, interfaces.mcp, name);
  if (interfaces.claudeCodeHook) installClaudeCodeHook(extPath, interfaces.claudeCodeHook);
  if (interfaces.skill) installSkill(extPath, name);

  entry.enabled = true;
  entry.updatedAt = new Date().toISOString();
  saveRegistry(reg);
  return { ok: true, reason: 'enabled' };
}

export function disableExtension(name) {
  if (CORE_EXTENSIONS.has(name)) return { ok: false, reason: 'core extension, cannot disable' };

  const reg = loadRegistry();
  const entry = reg.extensions?.[name];
  if (!entry) return { ok: false, reason: 'not installed' };
  if (!entry.enabled) return { ok: true, reason: 'already disabled' };

  unregisterMCP(name);
  removeClaudeCodeHook(name);
  removeSkill(name);

  entry.enabled = false;
  entry.updatedAt = new Date().toISOString();
  saveRegistry(reg);
  return { ok: true, reason: 'disabled' };
}

// ── Exports for ldm CLI ──

export { loadRegistry, saveRegistry, updateRegistry, readJSON, writeJSON, runBuildIfNeeded, resolveLocalDeps, buildSourceInfo, CORE_EXTENSIONS };
