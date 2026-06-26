// memory-crystal/doctor.ts — Crystal Doctor: full health check.
// Runs 10 checks and returns status + fix suggestions.
//
// Usage: crystal doctor

import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs';
import { execSync } from 'node:child_process';
import { join } from 'node:path';
import { detectRole } from './role.js';
import { ldmPaths, resolveStatePath, captureShimPath, restoreCaptureShim } from './ldm.js';
import { isBridgeInstalled, isBridgeRegistered } from './bridge.js';

const HOME = process.env.HOME || '';

export interface DoctorCheck {
  name: string;
  status: 'ok' | 'warn' | 'fail';
  detail: string;
  fix?: string;
  /** Optional heal action invoked by `crystal doctor --fix`. Returns a status string. */
  heal?: () => string;
}

export async function runDoctor(): Promise<DoctorCheck[]> {
  const checks: DoctorCheck[] = [];
  const role = detectRole();
  const paths = ldmPaths();

  // 1. Version + deployment
  checks.push(checkVersion());

  // 2. Role
  checks.push({
    name: 'Role',
    status: 'ok',
    detail: `${role.role} (${role.source})`,
  });

  // 3. Database
  checks.push(await checkDatabase(paths.crystalDb));

  // 4. Embedding provider
  checks.push(checkEmbeddingProvider(role.role));

  // 5. Capture cron
  checks.push(checkCaptureShim());

  // 6. CC Stop hook
  checks.push(checkCCHook());

  // 7. Relay config
  checks.push(checkRelayConfig(role));

  // 8. MCP server (memory-crystal)
  checks.push(checkMcpServer());

  // 9. Backup
  checks.push(checkBackup());

  // 10. Bridge
  checks.push(checkBridge());

  // 11. LDM directory
  checks.push(checkLdmDirectory(paths));

  // 12. Private mode
  checks.push(checkPrivateMode());

  // 13. MLX local LLM
  try {
    const { doctorCheck } = await import('./mlx-setup.js');
    const mlx = doctorCheck();
    if (mlx.status !== 'skip') {
      checks.push({ name: 'MLX LLM', status: mlx.status, detail: mlx.detail, fix: mlx.fix });
    }
  } catch {}

  return checks;
}

// ── Helpers ──

/** Check if 1Password SA token can resolve the OpenAI API key at runtime. */
function checkOpEmbeddings(): DoctorCheck | null {
  const saTokenLdm = join(HOME, '.ldm', 'secrets', 'op-sa-token');
  const saTokenOc = join(HOME, '.openclaw', 'secrets', 'op-sa-token');
  if (!existsSync(saTokenLdm) && !existsSync(saTokenOc)) return null;
  const saTokenPath = existsSync(saTokenLdm) ? saTokenLdm : saTokenOc;
  try {
    const saToken = readFileSync(saTokenPath, 'utf-8').trim();
    const result = execSync('op read "op://Agent Secrets/OpenAI API/api key" 2>/dev/null', {
      encoding: 'utf-8',
      env: { ...process.env, OP_SERVICE_ACCOUNT_TOKEN: saToken },
      timeout: 10000,
    }).trim();
    if (result) {
      return { name: 'Embeddings', status: 'ok', detail: 'openai (via 1Password)' };
    }
  } catch {
    return {
      name: 'Embeddings',
      status: 'warn',
      detail: '1Password SA token found but op read failed',
      fix: 'Check that op CLI is installed and SA token is valid',
    };
  }
  return null;
}

// ── Individual checks ──

function checkVersion(): DoctorCheck {
  const ldmExtPkg = join(HOME, '.ldm', 'extensions', 'memory-crystal', 'package.json');
  const ocExtPkg = join(HOME, '.openclaw', 'extensions', 'memory-crystal', 'package.json');

  let installedVersion: string | null = null;
  try {
    if (existsSync(ldmExtPkg)) {
      const pkg = JSON.parse(readFileSync(ldmExtPkg, 'utf-8'));
      installedVersion = pkg.version;
    }
  } catch {}

  if (!installedVersion) {
    return {
      name: 'Version',
      status: 'warn',
      detail: 'not deployed to ~/.ldm/extensions/memory-crystal/',
      fix: 'crystal init',
    };
  }

  // Check OC deployment
  let ocVersion: string | null = null;
  try {
    if (existsSync(ocExtPkg)) {
      const pkg = JSON.parse(readFileSync(ocExtPkg, 'utf-8'));
      ocVersion = pkg.version;
    }
  } catch {}

  const locations: string[] = [`LDM v${installedVersion}`];
  if (ocVersion) locations.push(`OC v${ocVersion}`);

  // Check for version mismatch between LDM and OC
  if (ocVersion && ocVersion !== installedVersion) {
    return {
      name: 'Version',
      status: 'warn',
      detail: `${locations.join(', ')} (version mismatch)`,
      fix: 'crystal update',
    };
  }

  return {
    name: 'Version',
    status: 'ok',
    detail: locations.join(', '),
  };
}

function checkCCHook(): DoctorCheck {
  const settingsPath = join(HOME, '.claude', 'settings.json');
  try {
    if (existsSync(settingsPath)) {
      const settings = JSON.parse(readFileSync(settingsPath, 'utf-8'));
      const stopHooks = settings?.hooks?.Stop;
      if (Array.isArray(stopHooks)) {
        const found = stopHooks.some((entry: any) => {
          const hooks = entry?.hooks;
          if (!Array.isArray(hooks)) return false;
          return hooks.some((h: any) => h?.command?.includes('memory-crystal') && h?.command?.includes('cc-hook'));
        });
        if (found) {
          return { name: 'CC Hook', status: 'ok', detail: 'Stop hook configured' };
        }
      }
    }
  } catch {}

  return {
    name: 'CC Hook',
    status: 'warn',
    detail: 'Stop hook not configured in ~/.claude/settings.json',
    fix: 'crystal init',
  };
}

async function checkDatabase(dbPath: string): Promise<DoctorCheck> {
  if (!existsSync(dbPath)) {
    return {
      name: 'Database',
      status: 'fail',
      detail: 'crystal.db not found',
      fix: 'crystal init',
    };
  }

  try {
    const { default: Database } = await import('better-sqlite3');
    const db = new Database(dbPath, { readonly: true });
    const row = db.prepare('SELECT COUNT(*) as count FROM chunks').get() as any;
    db.close();
    return {
      name: 'Database',
      status: 'ok',
      detail: `${row.count.toLocaleString()} chunks`,
    };
  } catch (err: any) {
    return {
      name: 'Database',
      status: 'warn',
      detail: `exists but could not read: ${err.message}`,
    };
  }
}

function checkEmbeddingProvider(role: string): DoctorCheck {
  const hasOpenAI = !!process.env.OPENAI_API_KEY;
  const hasGoogle = !!process.env.GOOGLE_API_KEY && process.env.CRYSTAL_EMBEDDING_PROVIDER === 'google';
  const hasOllama = process.env.CRYSTAL_EMBEDDING_PROVIDER === 'ollama';

  if (hasOpenAI || hasGoogle || hasOllama) {
    const provider = hasOllama ? 'ollama' : hasGoogle ? 'google' : 'openai';
    return {
      name: 'Embeddings',
      status: 'ok',
      detail: provider,
    };
  }

  // Check 1Password SA token (the runtime resolution path used by cron/hooks)
  const opResult = checkOpEmbeddings();
  if (opResult) return opResult;

  // Nodes don't need local embeddings (Core handles it)
  if (role === 'node') {
    return {
      name: 'Embeddings',
      status: 'ok',
      detail: 'not needed (node mode, Core handles embeddings)',
    };
  }

  return {
    name: 'Embeddings',
    status: 'fail',
    detail: 'no embedding provider configured',
    fix: 'Set OPENAI_API_KEY, or CRYSTAL_EMBEDDING_PROVIDER=ollama',
  };
}

function checkCaptureCron(): DoctorCheck {
  try {
    const crontab = execSync('crontab -l 2>/dev/null', { encoding: 'utf-8' });
    if (crontab.includes('crystal-capture')) {
      return { name: 'Capture', status: 'ok', detail: 'cron installed' };
    }
  } catch {}

  return {
    name: 'Capture',
    status: 'warn',
    detail: 'cron not found',
    fix: 'crystal init',
  };
}

function checkRelayConfig(role: ReturnType<typeof detectRole>): DoctorCheck {
  if (role.role === 'core' && !role.relayUrl) {
    return { name: 'Relay', status: 'ok', detail: 'not needed (core, no relay configured)' };
  }

  if (role.role === 'node') {
    if (!role.relayUrl) {
      return { name: 'Relay', status: 'fail', detail: 'node mode but CRYSTAL_RELAY_URL not set', fix: 'Set CRYSTAL_RELAY_URL in shell profile' };
    }
    if (!role.relayToken) {
      return { name: 'Relay', status: 'fail', detail: 'node mode but CRYSTAL_RELAY_TOKEN not set', fix: 'Set CRYSTAL_RELAY_TOKEN in shell profile' };
    }
    if (!role.relayKeyExists) {
      return { name: 'Relay', status: 'fail', detail: 'encryption key not found', fix: 'crystal pair --code <string from Core>' };
    }
    return { name: 'Relay', status: 'ok', detail: `node -> ${role.relayUrl}` };
  }

  // Core
  if (!role.relayKeyExists) {
    return { name: 'Relay', status: 'warn', detail: 'Core mode but no relay key (no nodes can sync)', fix: 'crystal pair' };
  }
  return { name: 'Relay', status: 'ok', detail: 'Core with relay key' };
}

function checkMcpServer(): DoctorCheck {
  // Check .mcp.json files (project-level registrations)
  const candidates = [
    join(HOME, '.claude', '.mcp.json'),       // user-level (legacy)
    join(HOME, '.openclaw', '.mcp.json'),      // OpenClaw project-level
    join(process.cwd(), '.mcp.json'),          // current project
  ];

  for (const mcpPath of candidates) {
    try {
      if (existsSync(mcpPath)) {
        const config = JSON.parse(readFileSync(mcpPath, 'utf-8'));
        if (config.mcpServers && config.mcpServers['memory-crystal']) {
          return { name: 'MCP Server', status: 'ok', detail: `memory-crystal registered (${mcpPath.replace(HOME, '~')})` };
        }
      }
    } catch {}
  }

  // Check user-scope registration via Claude Code CLI
  try {
    const result = execSync('claude mcp get memory-crystal 2>&1', { encoding: 'utf-8', timeout: 5000 });
    // If the command succeeds (no error), the server is registered
    if (!result.includes('not found') && !result.includes('error')) {
      return { name: 'MCP Server', status: 'ok', detail: 'memory-crystal registered (user scope)' };
    }
  } catch {}

  return {
    name: 'MCP Server',
    status: 'warn',
    detail: 'memory-crystal not registered with Claude Code',
    fix: 'claude mcp add --scope user memory-crystal -- node ~/.ldm/extensions/memory-crystal/dist/mcp-server.js',
  };
}

function checkBackup(): DoctorCheck {
  const plistPath = join(HOME, 'Library', 'LaunchAgents', 'ai.openclaw.ldm-backup.plist');
  if (existsSync(plistPath)) {
    return { name: 'Backup', status: 'ok', detail: 'LaunchAgent installed' };
  }

  // Check cron fallback
  try {
    const crontab = execSync('crontab -l 2>/dev/null', { encoding: 'utf-8' });
    if (crontab.includes('ldm-backup') || (crontab.includes('LDMDevTools') && crontab.includes('backup'))) {
      return { name: 'Backup', status: 'ok', detail: 'cron installed' };
    }
  } catch {}

  // Check if backup files exist (may run through LDM Dev Tools or other path)
  const backupsDir = join(HOME, '.ldm', 'backups');
  if (existsSync(backupsDir)) {
    try {
      const entries = readdirSync(backupsDir).filter((e: string) => !e.startsWith('.'));
      if (entries.length > 0) return { name: 'Backup', status: 'ok', detail: `${entries.length} backup(s) in ~/.ldm/backups/` };
    } catch {}
  }

  return {
    name: 'Backup',
    status: 'warn',
    detail: 'not configured',
    fix: 'crystal backup setup',
  };
}

function checkBridge(): DoctorCheck {
  const installed = isBridgeInstalled();
  const registered = isBridgeRegistered();

  if (installed && registered) {
    return { name: 'Bridge', status: 'ok', detail: 'installed and registered' };
  }
  if (installed && !registered) {
    return { name: 'Bridge', status: 'warn', detail: 'installed but not registered', fix: 'crystal bridge setup' };
  }
  return {
    name: 'Bridge',
    status: 'warn',
    detail: 'not installed',
    fix: 'npm install -g lesa-bridge && crystal bridge setup',
  };
}

function checkLdmDirectory(paths: ReturnType<typeof ldmPaths>): DoctorCheck {
  const missing: string[] = [];
  if (!existsSync(paths.root)) missing.push('~/.ldm');
  if (!existsSync(join(paths.root, 'memory'))) missing.push('memory/');
  if (!existsSync(paths.state)) missing.push('state/');
  if (!existsSync(paths.bin)) missing.push('bin/');
  if (!existsSync(paths.transcripts)) missing.push('transcripts/');

  if (missing.length === 0) {
    return { name: 'LDM Directory', status: 'ok', detail: 'intact' };
  }

  return {
    name: 'LDM Directory',
    status: 'fail',
    detail: `missing: ${missing.join(', ')}`,
    fix: 'crystal init',
  };
}

function checkPrivateMode(): DoctorCheck {
  const statePath = resolveStatePath('memory-capture-state.json');
  try {
    if (existsSync(statePath)) {
      const state = JSON.parse(readFileSync(statePath, 'utf-8'));
      if (state.enabled === false) {
        return { name: 'Private Mode', status: 'warn', detail: 'capture disabled (private mode ON)' };
      }
    }
  } catch {}
  return { name: 'Private Mode', status: 'ok', detail: 'capture enabled' };
}

// ── Capture shim integrity ──
// The cron line installCron() writes is sticky. If the shim file ever goes
// missing (e.g. shared ~/.ldm/bin clobbered by another installer, manual
// rm, or a restore from a backup that predated capture deployment), cron
// keeps firing against a non-existent target and capture silently dies.
// Distinguish three failure modes so doctor's diagnostic class is correct.
export function checkCaptureShim(): DoctorCheck {
  let crontab = '';
  try {
    crontab = execSync('crontab -l 2>/dev/null', { encoding: 'utf-8' });
  } catch {}

  if (!crontab.includes('crystal-capture')) {
    return {
      name: 'Capture',
      status: 'warn',
      detail: 'cron missing',
      fix: 'crystal init',
    };
  }

  const cronLine = crontab.split('\n').find(l => l.trim().startsWith('*') && l.includes('crystal-capture.sh')) || '';
  const target = extractCronTarget(cronLine) || captureShimPath();
  const isCanonical = target === captureShimPath();
  if (!existsSync(target)) {
    return {
      name: 'Capture',
      status: 'fail',
      detail: `cron installed but target missing: ${target}`,
      fix: isCanonical ? 'crystal doctor --fix  (or: crystal init)' : 'crystal init  (cron points at non-canonical path)',
      heal: isCanonical ? () => `restored ${restoreCaptureShim()}` : undefined,
    };
  }
  if ((statSync(target).mode & 0o111) === 0) {
    return {
      name: 'Capture',
      status: 'fail',
      detail: `cron target exists but not executable: ${target}`,
      fix: isCanonical ? 'crystal doctor --fix  (or: chmod +x the target)' : 'crystal init  (cron points at non-canonical path)',
      heal: isCanonical ? () => `restored ${restoreCaptureShim()}` : undefined,
    };
  }

  return { name: 'Capture', status: 'ok', detail: `cron + target ok: ${target}` };
}

/**
 * Extract the script path from a crystal-capture crontab line. The line
 * format from installCron() is `* * * * * <path> >> <log> 2>&1`. We pull
 * the first path-shaped token after the timing fields and resolve a
 * leading `~` to HOME. Returns null if the line is unparseable.
 */
export function extractCronTarget(line: string): string | null {
  const tokens = line.trim().split(/\s+/);
  if (tokens.length < 6) return null;
  const path = tokens[5];
  if (!path || !path.includes('crystal-capture.sh')) return null;
  return path.startsWith('~') ? join(HOME, path.slice(1)) : path;
}
