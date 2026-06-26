// LDM OS Boot Hook Installer
// Follows Memory Crystal installer.ts pattern: detect state, deploy, configure, register.
// Pure ESM, zero dependencies. Never nuke and replace.

import { existsSync, readFileSync, writeFileSync, mkdirSync, copyFileSync, statSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { homedir } from 'node:os';
import { fileURLToPath } from 'node:url';

const HOME = homedir();
const LDM_ROOT = join(HOME, '.ldm');
const BOOT_DIR = join(LDM_ROOT, 'shared', 'boot');
const CC_SETTINGS = join(HOME, '.claude', 'settings.json');
const REGISTRY = join(LDM_ROOT, 'extensions', 'registry.json');

const __dirname = dirname(fileURLToPath(import.meta.url));

// ── Helpers ──

function readJSON(path) {
  try {
    if (existsSync(path)) return JSON.parse(readFileSync(path, 'utf-8'));
  } catch {}
  return null;
}

function writeJSON(path, data) {
  mkdirSync(dirname(path), { recursive: true });
  writeFileSync(path, JSON.stringify(data, null, 2) + '\n');
}

function readVersion(pkgPath) {
  const pkg = readJSON(pkgPath);
  return pkg?.version || null;
}

function getRepoRoot() {
  // Walk up from src/boot/ to find package.json
  let dir = __dirname;
  for (let i = 0; i < 5; i++) {
    const pkgPath = join(dir, 'package.json');
    if (existsSync(pkgPath)) {
      const pkg = readJSON(pkgPath);
      if (pkg?.name === '@wipcomputer/ldm-os') return dir;
    }
    dir = dirname(dir);
  }
  // Fallback: two levels up from src/boot/
  return dirname(dirname(__dirname));
}

// ── Install State Detection ──

export function detectInstallState() {
  const repoRoot = getRepoRoot();
  const repoVersion = readVersion(join(repoRoot, 'package.json')) || '0.0.0';
  const installedVersion = readVersion(join(BOOT_DIR, 'package.json'));

  const hookDeployed = existsSync(join(BOOT_DIR, 'boot-hook.mjs'));
  const configDeployed = existsSync(join(BOOT_DIR, 'boot-config.json'));

  // Check if SessionStart hook is configured in settings.json
  let hookConfigured = false;
  const settings = readJSON(CC_SETTINGS);
  if (settings?.hooks?.SessionStart) {
    const entries = settings.hooks.SessionStart;
    if (Array.isArray(entries)) {
      hookConfigured = entries.some((entry) => {
        const hooks = entry?.hooks;
        if (!Array.isArray(hooks)) return false;
        return hooks.some((h) => h?.command?.includes('boot-hook') || h?.command?.includes('shared/boot'));
      });
    }
  }

  const needsUpdate = installedVersion !== null && installedVersion !== repoVersion;

  return {
    bootDirExists: existsSync(BOOT_DIR),
    hookDeployed,
    hookConfigured,
    configDeployed,
    installedVersion,
    repoVersion,
    needsUpdate,
    isFresh: installedVersion === null,
  };
}

// ── Deployment ──

export function deployToLdm(options = {}) {
  const repoRoot = getRepoRoot();
  const srcBoot = join(repoRoot, 'src', 'boot');
  const steps = [];

  // Create boot directory
  if (!existsSync(BOOT_DIR)) {
    mkdirSync(BOOT_DIR, { recursive: true });
    steps.push('Created ~/.ldm/shared/boot/');
  }

  // Always copy boot-hook.mjs (code updates always deploy)
  const hookSrc = join(srcBoot, 'boot-hook.mjs');
  if (existsSync(hookSrc)) {
    copyFileSync(hookSrc, join(BOOT_DIR, 'boot-hook.mjs'));
    steps.push('Deployed boot-hook.mjs');
  } else {
    steps.push('MISSING: src/boot/boot-hook.mjs (cannot deploy hook)');
  }

  // Copy package.json for version tracking (always update)
  const pkgSrc = join(repoRoot, 'package.json');
  if (existsSync(pkgSrc)) {
    copyFileSync(pkgSrc, join(BOOT_DIR, 'package.json'));
    steps.push('Updated package.json (version tracking)');
  }

  // boot-config.json: only deploy if not present (user customizations survive)
  const configDst = join(BOOT_DIR, 'boot-config.json');
  const configSrc = join(srcBoot, 'boot-config.json');
  if (!existsSync(configDst)) {
    if (existsSync(configSrc)) {
      copyFileSync(configSrc, configDst);
      steps.push('Seeded boot-config.json (new install)');
    }
  } else {
    steps.push('boot-config.json exists (preserved, not overwritten)');
  }

  return steps;
}

// ── Hook Configuration ──

export function configureSessionStartHook() {
  const hookCommand = `node ${join(BOOT_DIR, 'boot-hook.mjs')}`;

  let settings = readJSON(CC_SETTINGS) || {};

  // Ensure hooks.SessionStart exists
  if (!settings.hooks) settings.hooks = {};
  if (!Array.isArray(settings.hooks.SessionStart)) settings.hooks.SessionStart = [];

  // Find existing boot-hook entry
  const existingIdx = settings.hooks.SessionStart.findIndex((entry) => {
    const hooks = entry?.hooks;
    if (!Array.isArray(hooks)) return false;
    return hooks.some((h) =>
      h?.command?.includes('boot-hook') || h?.command?.includes('shared/boot')
    );
  });

  const hookEntry = {
    matcher: '*',
    hooks: [{
      type: 'command',
      command: hookCommand,
      timeout: 15,
    }],
  };

  if (existingIdx >= 0) {
    // Update in place
    settings.hooks.SessionStart[existingIdx] = hookEntry;
    return 'SessionStart hook updated in settings.json';
  } else {
    // Append
    settings.hooks.SessionStart.push(hookEntry);
    writeJSON(CC_SETTINGS, settings);
    return 'SessionStart hook added to settings.json';
  }
}

// ── Registry ──

export function updateRegistry(version) {
  let registry = readJSON(REGISTRY) || { _format: 'v1', extensions: {} };

  registry.extensions['ldm-os-boot'] = {
    name: 'ldm-os-boot',
    version,
    source: getRepoRoot(),
    interfaces: ['claude-code-hook'],
    ldmPath: BOOT_DIR,
    updatedAt: new Date().toISOString(),
  };

  writeJSON(REGISTRY, registry);
  return 'Registry updated';
}

// ── Orchestrator ──

export function runInstallOrUpdate(options = {}) {
  const state = detectInstallState();
  const steps = [];
  const dryRun = options.dryRun || false;

  // Check if already up to date
  if (!state.isFresh && !state.needsUpdate) {
    return {
      action: 'up-to-date',
      version: state.repoVersion,
      steps: [`Already at v${state.repoVersion}. Nothing to do.`],
    };
  }

  const action = state.isFresh ? 'installed' : 'updated';

  if (dryRun) {
    steps.push(`[DRY RUN] Would ${action === 'installed' ? 'install' : 'update'} v${state.repoVersion}`);
    if (state.isFresh) {
      steps.push('[DRY RUN] Would create ~/.ldm/shared/boot/');
      steps.push('[DRY RUN] Would deploy boot-hook.mjs');
      steps.push('[DRY RUN] Would seed boot-config.json');
    } else {
      steps.push(`[DRY RUN] Would update from v${state.installedVersion} to v${state.repoVersion}`);
      steps.push('[DRY RUN] Would update boot-hook.mjs');
      steps.push('[DRY RUN] Would preserve boot-config.json');
    }
    if (!state.hookConfigured) {
      steps.push('[DRY RUN] Would add SessionStart hook to settings.json');
    } else {
      steps.push('[DRY RUN] Would update SessionStart hook in settings.json');
    }
    steps.push('[DRY RUN] Would update registry');
    return { action: 'dry-run', version: state.repoVersion, steps };
  }

  // Step 1: Deploy files
  const deploySteps = deployToLdm();
  steps.push(...deploySteps);

  // Step 2: Configure hook
  try {
    const hookResult = configureSessionStartHook();
    steps.push(hookResult);
  } catch (err) {
    steps.push(`Hook config failed: ${err.message}`);
  }

  // Step 3: Update registry
  try {
    const regResult = updateRegistry(state.repoVersion);
    steps.push(regResult);
  } catch (err) {
    steps.push(`Registry update failed: ${err.message}`);
  }

  return { action, version: state.repoVersion, steps };
}

// ── Format helpers ──

export function formatStatus(state) {
  const lines = [];
  lines.push('LDM OS Boot Hook Status');
  lines.push('');
  lines.push(`  Boot directory:    ${state.bootDirExists ? 'exists' : 'MISSING'}`);
  lines.push(`  Hook deployed:     ${state.hookDeployed ? 'yes' : 'no'}`);
  lines.push(`  Hook configured:   ${state.hookConfigured ? 'yes' : 'no'}`);
  lines.push(`  Config deployed:   ${state.configDeployed ? 'yes' : 'no'}`);
  lines.push(`  Installed version: ${state.installedVersion || 'none'}`);
  lines.push(`  Repo version:      ${state.repoVersion}`);
  lines.push(`  Needs update:      ${state.needsUpdate ? 'YES' : 'no'}`);
  lines.push(`  Fresh install:     ${state.isFresh ? 'YES' : 'no'}`);
  return lines.join('\n');
}

export function formatResult(result) {
  const lines = [];
  lines.push(`Action: ${result.action} (v${result.version})`);
  lines.push('');
  for (const step of result.steps) {
    lines.push(`  ${step}`);
  }
  return lines.join('\n');
}
