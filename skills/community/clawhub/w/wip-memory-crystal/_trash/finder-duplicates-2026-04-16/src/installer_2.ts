// memory-crystal/installer.ts — Intelligent install and update logic.
// Detects what's installed, deploys CC hooks, configures MCP, handles updates.
// Pure detection + targeted side effects. Never overwrites data.

import { existsSync, readFileSync, writeFileSync, mkdirSync, cpSync, copyFileSync, chmodSync, readdirSync, statSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';
import { ldmPaths, scaffoldLdm, deployCaptureScript, deployBackupScript, installCron, getAgentId } from './ldm.js';

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
  role: 'core' | 'node' | 'standalone';
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
        if (pkg.name === 'memory-crystal') return dir;
      } catch {}
    }
    dir = dirname(dir);
  }
  // Fallback: one level up from thisDir (common case: thisDir is dist/ or src/)
  return dirname(thisDir);
}

export function detectInstallState(): InstallState {
  const ldmExtDir = join(LDM_ROOT, 'extensions', 'memory-crystal');
  const ocExtDir = join(OC_ROOT, 'extensions', 'memory-crystal');
  const paths = ldmPaths();

  // Installed version from LDM extension
  const installedVersion = readVersion(join(ldmExtDir, 'package.json'));

  // Repo version from this package
  const repoRoot = getRepoRoot();
  const repoVersion = readVersion(join(repoRoot, 'package.json')) || '0.0.0';

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

  // Role detection deferred to async callers; use standalone as sync default
  const role: 'core' | 'node' | 'standalone' = 'standalone';

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

  // Try using claude CLI
  try {
    execSync(`claude mcp add --scope user memory-crystal -- node "${mcpServerPath}"`, {
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
        execSync(`claude mcp add --scope user memory-crystal -- node "${mcpServerPath}"`, { encoding: 'utf-8', stdio: 'pipe', timeout: 15000 });
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

  // Step 1: Scaffold LDM (idempotent)
  scaffoldLdm(agentId);
  steps.push(`LDM scaffolded for agent "${agentId}"`);

  // Step 2: Database awareness
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

  // Step 6: Deploy capture + backup scripts
  try {
    deployCaptureScript();
    steps.push('Capture script deployed');
  } catch (err: any) {
    steps.push(`Capture script failed: ${err.message}`);
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
    deployBackupScript();
    steps.push('Backup script deployed');
  } catch (err: any) {
    steps.push(`Backup script failed: ${err.message}`);
  }

  // Step 7: OpenClaw (if detected)
  if (state.ocDetected) {
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

  // Step 8: Role setup
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

  return {
    action: isFresh ? 'installed' : 'updated',
    version: state.repoVersion,
    deployedTo,
    steps,
    dbStatus,
    chunkCount,
  };
}
