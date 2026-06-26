// memory-crystal/ldm.ts — LDM directory scaffolding and path resolution.
// Central module for all LDM directory knowledge. Every other file imports paths from here.
// LDM = Learning Dreaming Machines. ~/.ldm/ is the universal agent home.

import { existsSync, mkdirSync, readFileSync, writeFileSync, copyFileSync, chmodSync, readdirSync, statSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { execSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const HOME = process.env.HOME || '';
const LDM_ROOT = join(HOME, '.ldm');

// ── Agent config ──

export interface AgentConfig {
  agentId: string;
  agent?: string;
  harness?: string;
  model?: string;
  created?: string;
  memoryPaths?: Record<string, string>;
  dreamWeaver?: Record<string, unknown>;
}

export function loadAgentConfig(id: string): AgentConfig | null {
  const cfgPath = join(LDM_ROOT, 'agents', id, 'config.json');
  try {
    if (existsSync(cfgPath)) return JSON.parse(readFileSync(cfgPath, 'utf-8'));
  } catch {}
  return null;
}

export function saveAgentConfig(id: string, config: AgentConfig): void {
  const dir = join(LDM_ROOT, 'agents', id);
  mkdirSync(dir, { recursive: true });
  writeFileSync(join(dir, 'config.json'), JSON.stringify(config, null, 2) + '\n');
}

// ── Agent ID resolution ──

export function getAgentId(harnessHint?: 'claude-code' | 'openclaw'): string {
  if (process.env.CRYSTAL_AGENT_ID) return process.env.CRYSTAL_AGENT_ID;
  const agentsDir = join(LDM_ROOT, 'agents');
  if (existsSync(agentsDir)) {
    try {
      for (const d of readdirSync(agentsDir)) {
        const cfg = loadAgentConfig(d);
        if (!cfg || !cfg.agentId) continue;
        if (!harnessHint) return cfg.agentId;
        if (harnessHint === 'claude-code' && cfg.harness === 'claude-code-cli') return cfg.agentId;
        if (harnessHint === 'openclaw' && cfg.harness === 'openclaw') return cfg.agentId;
      }
    } catch {}
  }
  return harnessHint === 'openclaw' ? 'oc-lesa-mini' : 'cc-mini';
}

// ── Path resolution ──

export interface LdmPaths {
  root: string;           // ~/.ldm
  bin: string;            // ~/.ldm/bin
  secrets: string;        // ~/.ldm/secrets
  state: string;          // ~/.ldm/state
  config: string;         // ~/.ldm/config.json
  crystalDb: string;      // ~/.ldm/memory/crystal.db
  crystalLance: string;   // ~/.ldm/memory/lance/
  agentRoot: string;      // ~/.ldm/agents/{agent_id}
  transcripts: string;    // ~/.ldm/agents/{agent_id}/memory/transcripts/
  sessions: string;       // ~/.ldm/agents/{agent_id}/memory/sessions/
  daily: string;          // ~/.ldm/agents/{agent_id}/memory/daily/
  journals: string;       // ~/.ldm/agents/{agent_id}/memory/journals/
  workspace: string;      // ~/.ldm/agents/{agent_id}/memory/workspace/
}

export function ldmPaths(agentId?: string): LdmPaths {
  const id = agentId || getAgentId();
  const agentRoot = join(LDM_ROOT, 'agents', id);

  return {
    root: LDM_ROOT,
    bin: join(LDM_ROOT, 'bin'),
    secrets: join(LDM_ROOT, 'secrets'),
    state: join(LDM_ROOT, 'state'),
    config: join(LDM_ROOT, 'config.json'),
    crystalDb: join(LDM_ROOT, 'memory', 'crystal.db'),
    crystalLance: join(LDM_ROOT, 'memory', 'lance'),
    agentRoot,
    transcripts: join(agentRoot, 'memory', 'transcripts'),
    sessions: join(agentRoot, 'memory', 'sessions'),
    daily: join(agentRoot, 'memory', 'daily'),
    journals: join(agentRoot, 'memory', 'journals'),
    workspace: join(agentRoot, 'memory', 'workspace'),
  };
}

// ── Config file ──

interface LdmConfig {
  version: string;
  agents: string[];
  createdAt: string;
  updatedAt: string;
}

function loadConfig(): LdmConfig | null {
  const configPath = join(LDM_ROOT, 'config.json');
  try {
    if (existsSync(configPath)) {
      return JSON.parse(readFileSync(configPath, 'utf-8'));
    }
  } catch {}
  return null;
}

function saveConfig(config: LdmConfig): void {
  const configPath = join(LDM_ROOT, 'config.json');
  writeFileSync(configPath, JSON.stringify(config, null, 2) + '\n');
}

// ── Scaffolding ──

export function scaffoldLdm(agentId?: string): LdmPaths {
  const paths = ldmPaths(agentId);

  // Create shared directories
  mkdirSync(join(paths.root, 'memory'), { recursive: true });
  mkdirSync(paths.crystalLance, { recursive: true });
  mkdirSync(paths.bin, { recursive: true });
  mkdirSync(paths.secrets, { recursive: true, mode: 0o700 });
  mkdirSync(paths.state, { recursive: true });

  // Create agent-specific directories
  mkdirSync(paths.transcripts, { recursive: true });
  mkdirSync(paths.sessions, { recursive: true });
  mkdirSync(paths.daily, { recursive: true });
  mkdirSync(paths.journals, { recursive: true });
  mkdirSync(paths.workspace, { recursive: true });

  // Update config.json
  const id = agentId || getAgentId();
  let config = loadConfig();
  if (!config) {
    config = {
      version: '1.0.0',
      agents: [id],
      createdAt: new Date().toISOString(),
      updatedAt: new Date().toISOString(),
    };
  } else {
    if (!config.agents.includes(id)) {
      config.agents.push(id);
    }
    config.updatedAt = new Date().toISOString();
  }
  saveConfig(config);

  return paths;
}

// ── Script deployment ──

/** Copy crystal-capture.sh from the package's scripts/ dir to ~/.ldm/bin/. */
export function deployCaptureScript(): string {
  const paths = ldmPaths();
  mkdirSync(paths.bin, { recursive: true });

  // Resolve the script: check same dir as this file (dist/), then ../scripts/ (repo dev)
  const thisDir = dirname(fileURLToPath(import.meta.url));
  let scriptSrc = join(thisDir, 'crystal-capture.sh');
  if (!existsSync(scriptSrc)) {
    scriptSrc = join(thisDir, '..', 'scripts', 'crystal-capture.sh');
  }
  const scriptDest = join(paths.bin, 'crystal-capture.sh');

  if (!existsSync(scriptSrc)) {
    throw new Error(`crystal-capture.sh not found at ${scriptSrc}`);
  }

  copyFileSync(scriptSrc, scriptDest);
  chmodSync(scriptDest, 0o755);
  return scriptDest;
}

// ── Capture shim integrity ──
// The cron line written by installCron() is sticky. If the shim file at
// ~/.ldm/bin/crystal-capture.sh ever goes missing, cron keeps firing
// against a non-existent path and capture silently dies. These helpers
// let installer + doctor verify and (on explicit request) restore it.

export function captureShimPath(): string {
  return join(ldmPaths().bin, 'crystal-capture.sh');
}

/** Throw if the capture shim is missing or not executable. */
export function verifyCaptureShim(path: string = captureShimPath()): void {
  if (!existsSync(path)) {
    throw new Error(`capture shim missing at ${path}`);
  }
  if ((statSync(path).mode & 0o111) === 0) {
    throw new Error(`capture shim not executable at ${path}`);
  }
}

/**
 * Restore the capture shim from the deployed extension dist path. Used by
 * `crystal doctor --fix` when cron points at a missing target. Does nothing
 * silently: returns the restored path or throws.
 */
export function restoreCaptureShim(): string {
  const src = join(HOME, '.ldm', 'extensions', 'memory-crystal', 'dist', 'crystal-capture.sh');
  if (!existsSync(src)) {
    throw new Error(`canonical script missing at ${src}; run "crystal init"`);
  }
  const dest = captureShimPath();
  mkdirSync(dirname(dest), { recursive: true });
  copyFileSync(src, dest);
  chmodSync(dest, 0o755);
  return dest;
}

// ── Cron management ──

const CRON_TAG = '# crystal-capture';
const CRON_ENTRY = '* * * * * ~/.ldm/bin/crystal-capture.sh >> ~/.ldm/logs/crystal-capture.log 2>&1';

/** Test if a crontab line belongs to crystal-capture (our tag or our entry). */
function isCrystalCaptureLine(line: string): boolean {
  return line === CRON_TAG || (line.includes('crystal-capture.sh') && line.startsWith('*'));
}

/** Install the crystal-capture cron entry. Idempotent: replaces existing entry if present. */
export function installCron(): void {
  // Ensure log directory exists
  mkdirSync(join(HOME, '.ldm', 'logs'), { recursive: true });

  let existing = '';
  try {
    existing = execSync('crontab -l 2>/dev/null', { encoding: 'utf8' });
  } catch {
    // No crontab yet
  }

  // Remove any existing crystal-capture lines (our tag + our entry only)
  const lines = existing.split('\n').filter(line => !isCrystalCaptureLine(line));

  // Add our entry
  lines.push(CRON_TAG);
  lines.push(CRON_ENTRY);

  // Clean up trailing blank lines, ensure final newline
  const newCrontab = lines.filter((l, i, arr) => !(l === '' && i === arr.length - 1)).join('\n') + '\n';
  execSync('crontab -', { input: newCrontab, encoding: 'utf8' });
}

/** Remove the crystal-capture cron entry. */
export function removeCron(): void {
  let existing = '';
  try {
    existing = execSync('crontab -l 2>/dev/null', { encoding: 'utf8' });
  } catch {
    return; // No crontab
  }

  const lines = existing.split('\n').filter(line => !isCrystalCaptureLine(line));
  const newCrontab = lines.join('\n');
  execSync('crontab -', { input: newCrontab, encoding: 'utf8' });
}

// ── Backup script deployment ──

/** Copy ldm-backup.sh from the package's scripts/ dir to ~/.ldm/bin/. */
export function deployBackupScript(): string {
  const paths = ldmPaths();
  mkdirSync(paths.bin, { recursive: true });

  const thisDir = dirname(fileURLToPath(import.meta.url));
  let scriptSrc = join(thisDir, 'ldm-backup.sh');
  if (!existsSync(scriptSrc)) {
    scriptSrc = join(thisDir, '..', 'scripts', 'ldm-backup.sh');
  }
  const scriptDest = join(paths.bin, 'ldm-backup.sh');

  if (!existsSync(scriptSrc)) {
    throw new Error(`ldm-backup.sh not found at ${scriptSrc}`);
  }

  copyFileSync(scriptSrc, scriptDest);
  chmodSync(scriptDest, 0o755);
  return scriptDest;
}

/** Install a LaunchAgent for daily backups at 03:00. */
export function installBackupLaunchAgent(): string {
  const scriptPath = join(ldmPaths().bin, 'ldm-backup.sh');
  if (!existsSync(scriptPath)) {
    throw new Error(`Backup script not found. Run crystal init first.`);
  }

  const launchAgentsDir = join(HOME, 'Library', 'LaunchAgents');
  mkdirSync(launchAgentsDir, { recursive: true });
  const plistPath = join(launchAgentsDir, 'ai.openclaw.ldm-backup.plist');

  const plist = `<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>ai.openclaw.ldm-backup</string>
  <key>ProgramArguments</key>
  <array>
    <string>bash</string>
    <string>${scriptPath}</string>
  </array>
  <key>StartCalendarInterval</key>
  <dict>
    <key>Hour</key>
    <integer>3</integer>
    <key>Minute</key>
    <integer>0</integer>
  </dict>
  <key>StandardOutPath</key>
  <string>${HOME}/.ldm/logs/ldm-backup.log</string>
  <key>StandardErrorPath</key>
  <string>${HOME}/.ldm/logs/ldm-backup.log</string>
</dict>
</plist>`;

  writeFileSync(plistPath, plist);

  // Unload first if already loaded (idempotent)
  try { execSync(`launchctl unload ${plistPath} 2>/dev/null`); } catch {}
  execSync(`launchctl load ${plistPath}`);

  return plistPath;
}

// ── Legacy path resolution ──
// Checks ~/.ldm first, falls back to ~/.openclaw for migration.
// Reads from wherever the file exists. Writes always go to ~/.ldm.

const LEGACY_OC_DIR = join(HOME, '.openclaw');

/** Resolve a path that might exist at the legacy .openclaw location.
 *  Returns the LDM path if the file exists there, otherwise checks legacy.
 *  For writing, always use the ldmPath directly. */
export function resolveStatePath(filename: string): string {
  const paths = ldmPaths();
  const ldmPath = join(paths.state, filename);
  if (existsSync(ldmPath)) return ldmPath;
  const legacyPath = join(LEGACY_OC_DIR, 'memory', filename);
  if (existsSync(legacyPath)) return legacyPath;
  return ldmPath; // default to LDM for new files
}

/** Get the write path for state files (always LDM). */
export function stateWritePath(filename: string): string {
  const paths = ldmPaths();
  const dir = paths.state;
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  return join(dir, filename);
}

/** Resolve a secrets path. Checks ~/.ldm/secrets first, then ~/.openclaw/secrets. */
export function resolveSecretPath(filename: string): string {
  const paths = ldmPaths();
  const ldmPath = join(paths.secrets, filename);
  if (existsSync(ldmPath)) return ldmPath;
  const legacyPath = join(LEGACY_OC_DIR, 'secrets', filename);
  if (existsSync(legacyPath)) return legacyPath;
  return ldmPath; // default to LDM for new files
}

// ── Quick check ──

export function ensureLdm(agentId?: string): LdmPaths {
  const paths = ldmPaths(agentId);

  // Quick check: if agent transcripts dir exists, everything is scaffolded
  if (existsSync(paths.transcripts) && existsSync(paths.config)) {
    return paths;
  }

  return scaffoldLdm(agentId);
}
