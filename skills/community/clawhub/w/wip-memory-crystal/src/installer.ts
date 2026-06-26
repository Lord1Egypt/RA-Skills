// memory-crystal/installer.ts — Intelligent install and update logic.
// Detects what's installed, deploys CC hooks, configures MCP, handles updates.
// Pure detection + targeted side effects. Never overwrites data.

import { existsSync, readFileSync, writeFileSync, mkdirSync, cpSync, copyFileSync, chmodSync, readdirSync, statSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { ldmPaths, scaffoldLdm, deployCaptureScript, installCron, getAgentId, loadAgentConfig, saveAgentConfig, verifyCaptureShim } from './ldm.js';

const HOME = process.env.HOME || '';
const LDM_ROOT = join(HOME, '.ldm');
const OC_ROOT = join(HOME, '.openclaw');
const CC_SETTINGS = join(HOME, '.claude', 'settings.json');
const CC_MCP = join(HOME, '.claude', '.mcp.json');
const OC_MCP = join(OC_ROOT, '.mcp.json');

// ── Install state detection ──

export interface InstallState {
  // What's installed
  ldmExists: boolean;
  crystalDbExists: boolean;
  ccHookDeployed: boolean;
  ccHookConfigured: boolean;
  mcpRegistered: boolean;
  ocDetected: boolean;
  ocPluginDeployed: boolean;
  cronInstalled: boolean;

  // Version info
  installedVersion: string | null;
  repoVersion: string;
  needsUpdate: boolean;

  // Role
  role: 'core' | 'node';
  relayKeyExists: boolean;
}

/** Read version from a package.json, or null if not found. */
function readVersion(pkgPath: string): string | null {
  try {
    if (existsSync(pkgPath)) {
      const pkg = JSON.parse(readFileSync(pkgPath, 'utf-8'));
      return pkg.version || null;
    }
  } catch {}
  return null;
}

/** Get the source directory (dist/ or repo root). */
function getSourceDir(): string {
  const thisDir = dirname(fileURLToPath(import.meta.url));
  // If we're in dist/, the package.json is one level up
  if (existsSync(join(thisDir, '..', 'package.json'))) {
    return thisDir;
  }
  // If running from repo src/, dist is a sibling
  const distDir = join(thisDir, '..', 'dist');
  if (existsSync(distDir)) return distDir;
  return thisDir;
}

/** Get the repo root (where package.json lives). */
function getRepoRoot(): string {
  const thisDir = dirname(fileURLToPath(import.meta.url));
  // Walk up until we find package.json with name "memory-crystal"
  let dir = thisDir;
  for (let i = 0; i < 5; i++) {
    const pkgPath = join(dir, 'package.json');
    if (existsSync(pkgPath)) {
      try {
        const pkg = JSON.parse(readFileSync(pkgPath, 'utf-8'));
        if (pkg.name === '@wipcomputer/memory-crystal') return dir;
      } catch {}
    }
    dir = dirname(dir);
  }
  // Fallback: one level up from thisDir (common case: thisDir is dist/ or src/)
  return dirname(thisDir);
}

/** Compare two semver strings. Returns 1 if a > b, -1 if a < b, 0 if equal. */
function semverCompare(a: string, b: string): number {
  const pa = a.split('.').map(Number);
  const pb = b.split('.').map(Number);
  for (let i = 0; i < 3; i++) {
    if ((pa[i] || 0) > (pb[i] || 0)) return 1;
    if ((pa[i] || 0) < (pb[i] || 0)) return -1;
  }
  return 0;
}

/** Check npm registry for the latest published version. Returns null on failure. */
function getLatestNpmVersion(): string | null {
  const names = ['@wipcomputer/memory-crystal', 'memory-crystal'];
  for (const name of names) {
    try {
      const v = execSync(`npm view ${name} version 2>/dev/null`, { encoding: 'utf-8', timeout: 10000 }).trim();
      if (v) return v;
    } catch {}
  }
  return null;
}

export function detectInstallState(): InstallState {
  const ldmExtDir = join(LDM_ROOT, 'extensions', 'memory-crystal');
  const ocExtDir = join(OC_ROOT, 'extensions', 'memory-crystal');
  const paths = ldmPaths();

  // Installed version from LDM extension
  const installedVersion = readVersion(join(ldmExtDir, 'package.json'));

  // Repo version from this package, or latest from npm if newer
  const repoRoot = getRepoRoot();
  let repoVersion = readVersion(join(repoRoot, 'package.json')) || '0.0.0';
  const npmVersion = getLatestNpmVersion();
  if (npmVersion && semverCompare(npmVersion, repoVersion) > 0) repoVersion = npmVersion;

  // CC hook deployed?
  const ccHookDeployed = existsSync(join(ldmExtDir, 'dist', 'cc-hook.js'));

  // CC hook configured in settings.json?
  let ccHookConfigured = false;
  try {
    if (existsSync(CC_SETTINGS)) {
      const settings = JSON.parse(readFileSync(CC_SETTINGS, 'utf-8'));
      const stopHooks = settings?.hooks?.Stop;
      if (Array.isArray(stopHooks)) {
        ccHookConfigured = stopHooks.some((entry: any) => {
          const hooks = entry?.hooks;
          if (!Array.isArray(hooks)) return false;
          return hooks.some((h: any) => h?.command?.includes('memory-crystal') && h?.command?.includes('cc-hook'));
        });
      }
    }
  } catch {}

  // MCP registered with Claude Code?
  let mcpRegistered = false;
  // Check .mcp.json files (project-level registrations)
  for (const mcpPath of [CC_MCP, OC_MCP, join(process.cwd(), '.mcp.json')]) {
    try {
      if (existsSync(mcpPath)) {
        const config = JSON.parse(readFileSync(mcpPath, 'utf-8'));
        if (config?.mcpServers?.['memory-crystal']) { mcpRegistered = true; break; }
      }
    } catch {}
  }
  // Check user-scope via Claude CLI (claude mcp get returns exit 0 if registered)
  if (!mcpRegistered) {
    try {
      execSync('claude mcp get memory-crystal 2>/dev/null', { encoding: 'utf-8', timeout: 5000, stdio: 'pipe' });
      mcpRegistered = true;
    } catch {}
  }

  // OpenClaw detected?
  const ocDetected = existsSync(join(OC_ROOT, 'openclaw.json'));
  const ocPluginDeployed = existsSync(join(ocExtDir, 'dist', 'openclaw.js'));

  // Cron?
  let cronInstalled = false;
  try {
    const crontab = execSync('crontab -l 2>/dev/null', { encoding: 'utf-8' });
    cronInstalled = crontab.includes('crystal-capture');
  } catch {}

  // Role detection deferred to async callers; use core as sync default
  const role: 'core' | 'node' = 'core';

  const relayKeyExists = existsSync(join(LDM_ROOT, 'secrets', 'crystal-relay-key'));

  return {
    ldmExists: existsSync(LDM_ROOT),
    crystalDbExists: existsSync(paths.crystalDb),
    ccHookDeployed,
    ccHookConfigured,
    mcpRegistered,
    ocDetected,
    ocPluginDeployed,
    cronInstalled,
    installedVersion,
    repoVersion,
    needsUpdate: installedVersion !== null && installedVersion !== repoVersion,
    role,
    relayKeyExists,
  };
}

// ── Deployment functions ──

/** Copy dist/ and package.json to ~/.ldm/extensions/memory-crystal/. */
export function deployToLdm(): { extensionDir: string; version: string } {
  const repoRoot = getRepoRoot();
  const sourceDir = join(repoRoot, 'dist');
  const extDir = join(LDM_ROOT, 'extensions', 'memory-crystal');
  const destDist = join(extDir, 'dist');

  if (!existsSync(sourceDir)) {
    throw new Error(`dist/ not found at ${sourceDir}. Run "npm run build" first.`);
  }

  // Create extension directory
  mkdirSync(destDist, { recursive: true });

  // Copy dist/ contents
  const distFiles = readdirSync(sourceDir);
  for (const file of distFiles) {
    const srcPath = join(sourceDir, file);
    const destPath = join(destDist, file);
    const stat = statSync(srcPath);
    if (stat.isFile()) {
      copyFileSync(srcPath, destPath);
    } else if (stat.isDirectory()) {
      cpSync(srcPath, destPath, { recursive: true });
    }
  }

  // Copy package.json for version tracking
  copyFileSync(join(repoRoot, 'package.json'), join(extDir, 'package.json'));

  // Copy openclaw.plugin.json if it exists
  const pluginJson = join(repoRoot, 'openclaw.plugin.json');
  if (existsSync(pluginJson)) {
    copyFileSync(pluginJson, join(extDir, 'openclaw.plugin.json'));
  }

  // Copy skills/ if present
  const skillsDir = join(repoRoot, 'skills');
  if (existsSync(skillsDir)) {
    cpSync(skillsDir, join(extDir, 'skills'), { recursive: true });
  }

  const version = readVersion(join(extDir, 'package.json')) || 'unknown';
  return { extensionDir: extDir, version };
}

/** Install npm dependencies in the deployed extension directory. */
export function installLdmDeps(): void {
  const extDir = join(LDM_ROOT, 'extensions', 'memory-crystal');
  if (!existsSync(join(extDir, 'package.json'))) {
    throw new Error('package.json not found in LDM extension dir. Deploy first.');
  }
  execSync('npm install --omit=dev', {
    cwd: extDir,
    encoding: 'utf-8',
    stdio: 'pipe',
    timeout: 120000,
  });
}

/** Copy dist/ + skills/ + manifests to ~/.openclaw/extensions/memory-crystal/. */
export function deployToOpenClaw(): { extensionDir: string; version: string } {
  const repoRoot = getRepoRoot();
  const sourceDir = join(repoRoot, 'dist');
  const extDir = join(OC_ROOT, 'extensions', 'memory-crystal');
  const destDist = join(extDir, 'dist');

  if (!existsSync(sourceDir)) {
    throw new Error(`dist/ not found at ${sourceDir}. Run "npm run build" first.`);
  }

  mkdirSync(destDist, { recursive: true });

  // Copy dist/
  const distFiles = readdirSync(sourceDir);
  for (const file of distFiles) {
    const srcPath = join(sourceDir, file);
    const destPath = join(destDist, file);
    const stat = statSync(srcPath);
    if (stat.isFile()) {
      copyFileSync(srcPath, destPath);
    } else if (stat.isDirectory()) {
      cpSync(srcPath, destPath, { recursive: true });
    }
  }

  // Copy package.json, openclaw.plugin.json
  copyFileSync(join(repoRoot, 'package.json'), join(extDir, 'package.json'));
  const pluginJson = join(repoRoot, 'openclaw.plugin.json');
  if (existsSync(pluginJson)) {
    copyFileSync(pluginJson, join(extDir, 'openclaw.plugin.json'));
  }

  // Copy skills/
  const skillsDir = join(repoRoot, 'skills');
  if (existsSync(skillsDir)) {
    cpSync(skillsDir, join(extDir, 'skills'), { recursive: true });
  }

  const version = readVersion(join(extDir, 'package.json')) || 'unknown';
  return { extensionDir: extDir, version };
}

/** Install npm dependencies in the OC extension directory. */
export function installOcDeps(): void {
  const extDir = join(OC_ROOT, 'extensions', 'memory-crystal');
  if (!existsSync(join(extDir, 'package.json'))) {
    throw new Error('package.json not found in OC extension dir. Deploy first.');
  }
  execSync('npm install --omit=dev', {
    cwd: extDir,
    encoding: 'utf-8',
    stdio: 'pipe',
    timeout: 120000,
  });
}

// ── CC Hook configuration ──

/** Add or update the Memory Crystal Stop hook in ~/.claude/settings.json. Merges safely. */
export function configureCCHook(): void {
  const hookCommand = `node ${join(LDM_ROOT, 'extensions', 'memory-crystal', 'dist', 'cc-hook.js')}`;

  let settings: any = {};
  if (existsSync(CC_SETTINGS)) {
    try {
      settings = JSON.parse(readFileSync(CC_SETTINGS, 'utf-8'));
    } catch {
      // If settings.json is corrupted, start fresh but preserve the file content
      throw new Error(`~/.claude/settings.json exists but is not valid JSON. Fix it manually before proceeding.`);
    }
  }

  // Ensure hooks.Stop exists
  if (!settings.hooks) settings.hooks = {};
  if (!Array.isArray(settings.hooks.Stop)) settings.hooks.Stop = [];

  // Find existing memory-crystal hook entry
  const existingIdx = settings.hooks.Stop.findIndex((entry: any) => {
    const hooks = entry?.hooks;
    if (!Array.isArray(hooks)) return false;
    return hooks.some((h: any) => h?.command?.includes('memory-crystal') || h?.command?.includes('cc-hook'));
  });

  const hookEntry = {
    hooks: [{
      type: 'command',
      command: hookCommand,
      timeout: 30,
    }],
  };

  if (existingIdx >= 0) {
    // Update in place
    settings.hooks.Stop[existingIdx] = hookEntry;
  } else {
    // Append
    settings.hooks.Stop.push(hookEntry);
  }

  // Ensure ~/.claude/ exists
  mkdirSync(join(HOME, '.claude'), { recursive: true });
  writeFileSync(CC_SETTINGS, JSON.stringify(settings, null, 2) + '\n');
}

// ── MCP registration ──

/** Register memory-crystal MCP server with Claude Code at user scope. */
export function registerMCPServer(): void {
  const mcpServerPath = join(LDM_ROOT, 'extensions', 'memory-crystal', 'dist', 'mcp-server.js');

  const addCmd = `claude mcp add --scope user -e OPENCLAW_HOME=${OC_ROOT} memory-crystal -- node "${mcpServerPath}"`;

  // Try using claude CLI
  try {
    execSync(addCmd, {
      encoding: 'utf-8',
      stdio: 'pipe',
      timeout: 15000,
    });
    return;
  } catch (err: any) {
    const output = (err.stderr || '') + (err.stdout || '');
    // "already exists" means it's registered. To update the path, remove and re-add.
    if (output.includes('already exists')) {
      try {
        execSync('claude mcp remove memory-crystal --scope user', { encoding: 'utf-8', stdio: 'pipe', timeout: 10000 });
        execSync(addCmd, { encoding: 'utf-8', stdio: 'pipe', timeout: 15000 });
      } catch {
        // If re-add fails, the old registration still works
      }
      return;
    }
    // claude CLI not available; fall through to .mcp.json
  }

  // Fallback: write to ~/.claude/.mcp.json
  let config: any = {};
  if (existsSync(CC_MCP)) {
    try {
      config = JSON.parse(readFileSync(CC_MCP, 'utf-8'));
    } catch {}
  }

  if (!config.mcpServers) config.mcpServers = {};
  config.mcpServers['memory-crystal'] = {
    command: 'node',
    args: [mcpServerPath],
    env: { OPENCLAW_HOME: OC_ROOT },
  };

  mkdirSync(join(HOME, '.claude'), { recursive: true });
  writeFileSync(CC_MCP, JSON.stringify(config, null, 2) + '\n');
}

/** Update OpenClaw .mcp.json to point to the deployed extension. */
export function registerOcMCPServer(): void {
  const mcpServerPath = join(OC_ROOT, 'extensions', 'memory-crystal', 'dist', 'mcp-server.js');

  let config: any = {};
  if (existsSync(OC_MCP)) {
    try {
      config = JSON.parse(readFileSync(OC_MCP, 'utf-8'));
    } catch {}
  }

  if (!config.mcpServers) config.mcpServers = {};
  config.mcpServers['memory-crystal'] = {
    command: 'node',
    args: [mcpServerPath],
    env: { OPENCLAW_HOME: OC_ROOT },
  };

  writeFileSync(OC_MCP, JSON.stringify(config, null, 2) + '\n');
}

// ── Database safety ──

/** Back up crystal.db before deploying new code. Returns the backup path. */
export function backupCrystalDb(): string {
  const paths = ldmPaths();
  const dbPath = paths.crystalDb;

  if (!existsSync(dbPath)) {
    throw new Error(`crystal.db not found at ${dbPath}`);
  }

  const timestamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
  const backupPath = `${dbPath}.pre-update-${timestamp}`;

  copyFileSync(dbPath, backupPath);

  // Also copy WAL and SHM if they exist (SQLite write-ahead log)
  const walPath = dbPath + '-wal';
  const shmPath = dbPath + '-shm';
  if (existsSync(walPath)) copyFileSync(walPath, backupPath + '-wal');
  if (existsSync(shmPath)) copyFileSync(shmPath, backupPath + '-shm');

  // Verify the backup is readable
  const origSize = statSync(dbPath).size;
  const backupSize = statSync(backupPath).size;
  if (backupSize !== origSize) {
    throw new Error(`Backup size mismatch: original ${origSize}, backup ${backupSize}`);
  }

  return backupPath;
}

/** Verify the new code can open and read the existing crystal.db without errors. */
export async function verifyCrystalDbReadable(): Promise<void> {
  const paths = ldmPaths();
  const dbPath = paths.crystalDb;

  if (!existsSync(dbPath)) return; // No DB to verify

  const { default: Database } = await import('better-sqlite3');
  const db = new Database(dbPath, { readonly: true });
  try {
    // Check that the chunks table exists and is readable
    const row = db.prepare('SELECT COUNT(*) as count FROM chunks').get() as any;
    if (typeof row.count !== 'number') {
      throw new Error('chunks table returned unexpected data');
    }

    // Check schema version if tracked
    const tables = db.prepare(
      "SELECT name FROM sqlite_master WHERE type='table'"
    ).all() as any[];
    const tableNames = tables.map((t: any) => t.name);

    if (!tableNames.includes('chunks')) {
      throw new Error('chunks table missing from database');
    }
  } finally {
    db.close();
  }
}

// ── Update display ──

/** Show what changed between versions. Returns a human-readable summary. */
export function formatUpdateSummary(oldVersion: string, newVersion: string): string {
  const lines: string[] = [];
  lines.push(`Updating v${oldVersion} -> v${newVersion}`);
  lines.push('');
  lines.push('What will be updated:');
  lines.push('  - Code in ~/.ldm/extensions/memory-crystal/dist/');
  lines.push('  - Skills in ~/.ldm/extensions/memory-crystal/skills/');
  lines.push('  - package.json (version tracking)');
  lines.push('');
  lines.push('What will NOT be touched:');
  lines.push('  - ~/.ldm/memory/crystal.db (your data)');
  lines.push('  - ~/.ldm/state/* (watermarks, role)');
  lines.push('  - ~/.ldm/secrets/* (relay key)');
  lines.push('  - ~/.ldm/agents/* (agent data)');
  return lines.join('\n');
}

// ── LDM CLI detection ──

/** Check if the ldm CLI is available on PATH. */
function ldmCliAvailable(): boolean {
  try {
    execSync('ldm --version', { stdio: 'pipe', timeout: 5000 });
    return true;
  } catch {
    return false;
  }
}

/** Install LDM OS globally if not already on PATH. */
function bootstrapLdmOs(steps: string[]): boolean {
  try {
    steps.push('Installing LDM OS infrastructure...');
    execSync('npm install -g @wipcomputer/wip-ldm-os', { stdio: 'pipe', timeout: 120000 });
    execSync('ldm --version', { stdio: 'pipe', timeout: 5000 });
    steps.push('LDM OS installed.');
    return true;
  } catch {
    steps.push('LDM OS install skipped (npm offline or permissions issue). Using core mode.');
    return false;
  }
}

/** Run ldm CLI for generic deployment (scaffold, copy to extensions, MCP, hooks). */
function runLdmInstall(repoDir: string): { ok: boolean; steps: string[] } {
  const steps: string[] = [];

  // Ensure LDM is initialized (skip component picker)
  try {
    execSync('ldm init --yes --none', { stdio: 'pipe', timeout: 30000 });
    steps.push('LDM initialized via ldm CLI');
  } catch (err: any) {
    const msg = (err.stderr || err.message || '').toString().trim();
    // "already initialized" is fine
    if (!msg.includes('already')) {
      steps.push(`ldm init warning: ${msg.slice(0, 120)}`);
    }
  }

  // Deploy this repo via ldm install
  try {
    execSync(`ldm install "${repoDir}"`, { stdio: 'pipe', timeout: 60000 });
    steps.push('Generic deployment handled by ldm install (extensions, MCP, hooks)');
    return { ok: true, steps };
  } catch (err: any) {
    const msg = (err.stderr || err.message || '').toString().trim();
    steps.push(`ldm install failed: ${msg.slice(0, 200)}`);
    return { ok: false, steps };
  }
}

// ── Full install/update orchestration ──

export interface InstallResult {
  action: 'installed' | 'updated' | 'up-to-date';
  version: string;
  deployedTo: string[];
  steps: string[];
  dbStatus?: 'existing' | 'imported' | 'fresh' | 'none';
  chunkCount?: number;
}

/** Run the full install or update flow. Returns a summary of what was done. */
export async function runInstallOrUpdate(options: {
  agentId?: string;
  role?: 'core' | 'node';
  pairCode?: string;
  importDb?: string;
  yes?: boolean;
  skipDiscover?: boolean;
}): Promise<InstallResult> {
  const agentId = options.agentId || getAgentId();
  const state = detectInstallState();
  const steps: string[] = [];
  const deployedTo: string[] = [];
  let dbStatus: 'existing' | 'imported' | 'fresh' | 'none' = 'none';
  let chunkCount = 0;

  const isFresh = !state.ldmExists || state.installedVersion === null;
  const isUpdate = !isFresh && state.needsUpdate;

  if (!isFresh && !isUpdate) {
    return {
      action: 'up-to-date',
      version: state.repoVersion,
      deployedTo: [],
      steps: [`Already at v${state.repoVersion}. Nothing to do.`],
    };
  }

  // If npm has a newer version, upgrade globally first then re-run
  if (isUpdate && state.installedVersion) {
    const npmV = getLatestNpmVersion();
    if (npmV && semverCompare(npmV, state.installedVersion) > 0) {
      steps.push(`Upgrading v${state.installedVersion} -> v${npmV} via npm...`);
      try {
        execSync('npm install -g @wipcomputer/memory-crystal 2>&1', { encoding: 'utf-8', timeout: 60000, stdio: 'pipe' });
        steps.push(`Installed @wipcomputer/memory-crystal@${npmV}`);
        steps.push('Continuing with updated code...');
      } catch (err: any) {
        steps.push(`npm upgrade failed: ${(err as Error).message}. Continuing with local code.`);
      }
    }
  }

  // ── LDM CLI delegation ──
  // If ldm CLI is on PATH, use it for generic deployment (scaffold, copy to
  // extensions, MCP registration, hook configuration). Crystal init then only
  // handles MC-specific setup: DB backup, role, pairing, cron, scripts.
  let hasLdmCli = ldmCliAvailable();
  if (!hasLdmCli) {
    hasLdmCli = bootstrapLdmOs(steps);
  }
  let ldmDelegated = false;

  if (hasLdmCli) {
    steps.push('LDM OS detected. Using ldm install for deployment...');
    const repoRoot = getRepoRoot();
    const delegateResult = runLdmInstall(repoRoot);
    steps.push(...delegateResult.steps);

    if (delegateResult.ok) {
      ldmDelegated = true;
      // ldm install handled: scaffold, deploy to extensions, deps, CC hook, MCP, OC deploy
      const ldmExtDir = join(LDM_ROOT, 'extensions', 'memory-crystal');
      if (existsSync(ldmExtDir)) deployedTo.push(ldmExtDir);
      const ocExtDir = join(OC_ROOT, 'extensions', 'memory-crystal');
      if (existsSync(ocExtDir)) deployedTo.push(ocExtDir);
    }
    // If ldm install failed, fall through to self-contained behavior
  }

  // Step 1: Scaffold LDM (idempotent) -- skip if ldm CLI handled it
  if (ldmDelegated) {
    steps.push('Scaffold + agent config handled by ldm CLI');
  } else {
  scaffoldLdm(agentId);
  steps.push(`LDM scaffolded for agent "${agentId}"`);

  // Step 1b: Ensure agentId is in agent config.json
  const existingCfg = loadAgentConfig(agentId);
  if (existingCfg && !existingCfg.agentId) {
    existingCfg.agentId = agentId;
    saveAgentConfig(agentId, existingCfg);
    steps.push(`Added agentId "${agentId}" to existing config.json`);
  } else if (!existingCfg) {
    const harness = agentId.startsWith('oc-') ? 'openclaw' : 'claude-code-cli';
    saveAgentConfig(agentId, {
      agentId,
      agent: agentId.startsWith('oc-') ? agentId.replace(/^oc-/, '').replace(/-[^-]+$/, '') : 'cc',
      harness,
      created: new Date().toISOString().slice(0, 10),
    });
    steps.push(`Created config.json for agent "${agentId}"`);
  }
  } // end of !ldmDelegated scaffold block

  // Step 2: Database awareness (MC-specific, always runs)
  if (state.crystalDbExists) {
    // Existing database found. Report what we see.
    try {
      const { default: Database } = await import('better-sqlite3');
      const db = new Database(ldmPaths().crystalDb, { readonly: true });
      const row = db.prepare('SELECT COUNT(*) as count FROM chunks').get() as any;
      chunkCount = row.count;
      db.close();
      dbStatus = 'existing';
      steps.push(`Existing database found: ${chunkCount.toLocaleString()} chunks in crystal.db`);
    } catch {
      dbStatus = 'existing';
      steps.push('Existing database found (could not read chunk count)');
    }

    // Back up before touching anything
    try {
      const backupPath = backupCrystalDb();
      steps.push(`Database backed up to ${backupPath}`);
    } catch (err: any) {
      steps.push(`Database backup FAILED: ${err.message}`);
      return {
        action: 'up-to-date',
        version: state.repoVersion,
        deployedTo: [],
        steps: [...steps, 'Aborted. Fix the backup issue before retrying.'],
        dbStatus,
      };
    }

    // Verify new code can read existing DB
    try {
      await verifyCrystalDbReadable();
      steps.push('Database read verification passed');
    } catch (err: any) {
      steps.push(`Database read verification FAILED: ${err.message}`);
      return {
        action: 'up-to-date',
        version: state.repoVersion,
        deployedTo: [],
        steps: [...steps, 'Aborted. New code cannot read existing database.'],
        dbStatus,
      };
    }
  } else if (options.importDb) {
    // User provided a database to import
    const importPath = options.importDb;
    if (!existsSync(importPath)) {
      steps.push(`Import path not found: ${importPath}`);
    } else {
      try {
        const paths = ldmPaths();
        mkdirSync(join(paths.root, 'memory'), { recursive: true });
        copyFileSync(importPath, paths.crystalDb);

        // Verify the imported DB
        const { default: Database } = await import('better-sqlite3');
        const db = new Database(paths.crystalDb, { readonly: true });
        const row = db.prepare('SELECT COUNT(*) as count FROM chunks').get() as any;
        chunkCount = row.count;
        db.close();

        dbStatus = 'imported';
        steps.push(`Database imported: ${chunkCount.toLocaleString()} chunks from ${importPath}`);
      } catch (err: any) {
        steps.push(`Database import failed: ${err.message}`);
      }
    }
  } else {
    // Fresh install, no database
    dbStatus = 'fresh';
    steps.push('No existing database. A new one will be created on first capture.');
  }

  // Always sync package.json for version tracking (even if ldm CLI handled deploy)
  if (ldmDelegated) {
    const repoRoot = getRepoRoot();
    const ldmExtDir = join(LDM_ROOT, 'extensions', 'memory-crystal');
    if (existsSync(ldmExtDir)) copyFileSync(join(repoRoot, 'package.json'), join(ldmExtDir, 'package.json'));
    const ocExtDir = join(OC_ROOT, 'extensions', 'memory-crystal');
    if (existsSync(ocExtDir)) copyFileSync(join(repoRoot, 'package.json'), join(ocExtDir, 'package.json'));
    steps.push(`Version synced to v${readVersion(join(repoRoot, 'package.json')) || 'unknown'}`);
  }

  // Generic deployment steps -- skip if ldm CLI handled them
  if (!ldmDelegated) {
  // Step 4: Deploy code to LDM extensions
  const ldmResult = deployToLdm();
  steps.push(`Code deployed to ${ldmResult.extensionDir}`);
  deployedTo.push(ldmResult.extensionDir);

  // Step 3: Install dependencies
  try {
    installLdmDeps();
    steps.push('Dependencies installed (LDM)');
  } catch (err: any) {
    steps.push(`Dependencies install failed (LDM): ${err.message}`);
  }

  // Step 4: Configure CC Stop hook
  try {
    configureCCHook();
    steps.push('CC Stop hook configured in ~/.claude/settings.json');
  } catch (err: any) {
    steps.push(`CC Stop hook config failed: ${err.message}`);
  }

  // Step 5: Register MCP server
  if (!state.mcpRegistered || isUpdate) {
    try {
      registerMCPServer();
      steps.push('MCP server registered with Claude Code');
    } catch (err: any) {
      steps.push(`MCP registration failed: ${err.message}`);
    }
  } else {
    steps.push('MCP server already registered');
  }
  } // end of !ldmDelegated generic deployment block

  // Step 6: Deploy capture + backup scripts (MC-specific, always runs)
  try {
    const dest = deployCaptureScript();
    verifyCaptureShim(dest);
    steps.push(`Capture script deployed: ${dest}`);
  } catch (err: any) {
    steps.push(`Capture script verification FAILED: ${err.message}`);
    throw err;
  }

  if (!state.cronInstalled || isFresh) {
    try {
      installCron();
      steps.push('Cron job installed (every minute)');
    } catch (err: any) {
      steps.push(`Cron install failed: ${err.message}`);
    }
  } else {
    steps.push('Cron job already installed');
  }

  try {
    if (!existsSync(join(ldmPaths().bin, 'ldm-backup.sh'))) {
      throw new Error('expected ~/.ldm/bin/ldm-backup.sh (LDM CLI-owned); run "ldm install" first');
    }
    steps.push('Backup shim verified (LDM CLI-owned)');
  } catch (err: any) {
    steps.push(`Backup shim verify failed: ${err.message}`);
  }

  // Step 6b: MLX local LLM (Apple Silicon only)
  try {
    const { canRunMlx, isMlxLmInstalled, isServerRunning } = await import('./mlx-setup.js');
    if (canRunMlx()) {
      if (isServerRunning()) {
        steps.push('MLX LLM: already running');
      } else if (isMlxLmInstalled()) {
        steps.push('MLX LLM: installed but not running. Start with: launchctl kickstart -kp gui/$(id -u)/ai.ldm.mlx-server');
      } else {
        steps.push('MLX LLM: Apple Silicon detected. Run "crystal mlx setup" to install local LLM for free, fast, offline search quality.');
      }
    }
  } catch {}

  // Step 7: OpenClaw (if detected, skip if ldm CLI handled it)
  if (!ldmDelegated && state.ocDetected) {
    try {
      const ocResult = deployToOpenClaw();
      steps.push(`OC plugin deployed to ${ocResult.extensionDir}`);
      deployedTo.push(ocResult.extensionDir);
    } catch (err: any) {
      steps.push(`OC plugin deploy failed: ${err.message}`);
    }

    try {
      installOcDeps();
      steps.push('Dependencies installed (OC)');
    } catch (err: any) {
      steps.push(`Dependencies install failed (OC): ${err.message}`);
    }

    try {
      registerOcMCPServer();
      steps.push('OC MCP server config updated');
    } catch (err: any) {
      steps.push(`OC MCP config failed: ${err.message}`);
    }
  }

  // Step 8: Interactive role selection (if no flags provided)
  if (!options.role && process.stdin.isTTY) {
    const { createInterface } = await import('readline');
    const rl = createInterface({ input: process.stdin, output: process.stdout });
    const answer = await new Promise<string>(resolve => {
      rl.question('\n  Is this your primary machine (always on), or adding a device?\n  [1] Primary (Crystal Core)\n  [2] Adding a device (Crystal Node)\n  > ', resolve);
    });
    rl.close();
    if (answer.trim() === '2') {
      options.role = 'node';
      // Prompt for pairing code
      const rl2 = createInterface({ input: process.stdin, output: process.stdout });
      options.pairCode = await new Promise<string>(resolve => {
        rl2.question('  Pairing code from Core (run "crystal pair" on Core): ', resolve);
      });
      rl2.close();
    } else {
      options.role = 'core';
    }
  }

  // Step 8b: Role setup
  if (options.role === 'core') {
    try {
      const { promoteToCore } = await import('./role.js');
      promoteToCore();
      steps.push('Role set to Core');
    } catch (err: any) {
      steps.push(`Role setup failed: ${err.message}`);
    }
  } else if (options.role === 'node') {
    try {
      const { demoteToNode } = await import('./role.js');
      demoteToNode();
      steps.push('Role set to Node');
    } catch (err: any) {
      steps.push(`Role setup failed: ${err.message}`);
    }
  }

  // Step 9: Pairing
  if (options.pairCode) {
    try {
      const { pairReceive } = await import('./pair.js');
      pairReceive(options.pairCode);
      steps.push('Pairing code accepted');
    } catch (err: any) {
      steps.push(`Pairing failed: ${err.message}`);
    }
  }

  // Step 10: Relay configuration (for Node or Core with relay)
  if (options.role === 'node' || process.env.CRYSTAL_RELAY_URL) {
    const secretsDir = join(LDM_ROOT, 'secrets');
    const envPath = join(secretsDir, 'crystal-relay.env');

    if (!existsSync(envPath)) {
      const relayUrl = 'https://memory-crystal-relay.wipcomputer.workers.dev';
      let token = '';

      // Try 1Password first
      try {
        const saTokenPath = join(OC_ROOT, 'secrets', 'op-sa-token');
        if (existsSync(saTokenPath)) {
          const saToken = readFileSync(saTokenPath, 'utf8').trim();
          token = execSync(
            `OP_SERVICE_ACCOUNT_TOKEN=${saToken} op item get "Memory Crystal Relay Auth Tokens" --vault "Agent Secrets" --fields label=${agentId}-token --reveal 2>/dev/null`,
            { encoding: 'utf8', timeout: 15000 }
          ).trim();
        }
      } catch {}

      // If no 1Password, prompt
      if (!token && process.stdin.isTTY) {
        const { createInterface } = await import('readline');
        const rl = createInterface({ input: process.stdin, output: process.stdout });
        token = await new Promise<string>(resolve => {
          rl.question('  Relay auth token: ', resolve);
        });
        rl.close();
        token = token.trim();
      }

      if (token) {
        mkdirSync(secretsDir, { recursive: true });
        writeFileSync(envPath, `export CRYSTAL_RELAY_URL=${relayUrl}\nexport CRYSTAL_RELAY_TOKEN=${token}\nexport CRYSTAL_AGENT_ID=${agentId}\n`);
        process.env.CRYSTAL_RELAY_URL = relayUrl;
        process.env.CRYSTAL_RELAY_TOKEN = token;
        steps.push('Relay config written to ~/.ldm/secrets/crystal-relay.env');

        // Offer to add to shell profile
        const shellProfile = join(HOME, '.zshrc');
        const sourceLine = `source ${envPath}`;
        let alreadySourced = false;
        try { alreadySourced = readFileSync(shellProfile, 'utf8').includes(sourceLine); } catch {}

        if (!alreadySourced && process.stdin.isTTY) {
          const { createInterface: createRL } = await import('readline');
          const rl2 = createRL({ input: process.stdin, output: process.stdout });
          const ans = await new Promise<string>(resolve => {
            rl2.question('  Add relay config to ~/.zshrc? [Y/n] ', resolve);
          });
          rl2.close();
          if (ans.trim().toLowerCase() !== 'n') {
            const { appendFileSync } = await import('fs');
            appendFileSync(shellProfile, `\n# Memory Crystal relay\n${sourceLine}\n`);
            steps.push('Added relay source to ~/.zshrc');
          }
        }
      } else {
        steps.push('No relay token. Set CRYSTAL_RELAY_TOKEN manually.');
      }
    } else {
      steps.push('Relay config exists at ~/.ldm/secrets/crystal-relay.env');
    }
  }

  // ── LDM OS tip ──
  if (hasLdmCli) {
    steps.push('Tip: Run "ldm install" to see more components you can add.');
  } else if (!ldmDelegated) {
    steps.push('Tip: Install LDM OS for more components: npm install -g @wipcomputer/wip-ldm-os');
  }

  return {
    action: isFresh ? 'installed' : 'updated',
    version: state.repoVersion,
    deployedTo,
    steps,
    dbStatus,
    chunkCount,
  };
}
