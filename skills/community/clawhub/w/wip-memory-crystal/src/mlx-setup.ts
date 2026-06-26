// memory-crystal/mlx-setup.ts — MLX local LLM auto-install for Apple Silicon.
// Detects platform, installs mlx-lm, pulls model, creates LaunchAgent.
// Port 18791 (next to OpenClaw 18789 and Crystal Core 18790).

import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { execSync } from 'node:child_process';
import { join } from 'node:path';
import { homedir } from 'node:os';

const HOME = homedir();
const MLX_PORT = 18791;
const MLX_MODEL = 'mlx-community/Qwen2.5-3B-Instruct-4bit';
const MLX_STATE_FILE = join(HOME, '.ldm', 'state', 'mlx-server.json');
const MLX_PLIST_LABEL = 'ai.ldm.mlx-server';
const MLX_PLIST_PATH = join(HOME, 'Library', 'LaunchAgents', `${MLX_PLIST_LABEL}.plist`);
const MLX_LOG_PATH = '/tmp/mlx-server.log';

export interface MlxState {
  installed: boolean;
  port: number;
  model: string;
  pythonPath: string;
  installedAt: string;
}

export interface MlxStatus {
  platform: 'apple-silicon' | 'intel-mac' | 'linux' | 'other';
  installed: boolean;
  running: boolean;
  port: number;
  model: string | null;
}

// ── Platform Detection ──

export function detectPlatform(): 'apple-silicon' | 'intel-mac' | 'linux' | 'other' {
  const platform = process.platform;
  const arch = process.arch;

  if (platform === 'darwin') {
    return arch === 'arm64' ? 'apple-silicon' : 'intel-mac';
  }
  if (platform === 'linux') return 'linux';
  return 'other';
}

export function canRunMlx(): boolean {
  return detectPlatform() === 'apple-silicon';
}

// ── Python Detection ──

function findPython(): string | null {
  const candidates = ['python3', '/opt/homebrew/bin/python3', '/usr/local/bin/python3'];
  for (const cmd of candidates) {
    try {
      const version = execSync(`${cmd} --version 2>&1`, { encoding: 'utf-8', timeout: 5000 }).trim();
      const match = version.match(/Python (\d+)\.(\d+)/);
      if (match && parseInt(match[1]) >= 3 && parseInt(match[2]) >= 10) {
        // Get the real path (resolve symlinks)
        const realPath = execSync(`which ${cmd} 2>/dev/null`, { encoding: 'utf-8', timeout: 3000 }).trim();
        return realPath || cmd;
      }
    } catch {}
  }
  return null;
}

// ── Package Manager Detection ──

function findInstaller(): 'uv' | 'pip3' | null {
  try {
    execSync('uv --version 2>/dev/null', { encoding: 'utf-8', timeout: 3000 });
    return 'uv';
  } catch {}
  try {
    execSync('pip3 --version 2>/dev/null', { encoding: 'utf-8', timeout: 3000 });
    return 'pip3';
  } catch {}
  return null;
}

// ── MLX-LM Installation ──

export function isMlxLmInstalled(): boolean {
  try {
    execSync('python3 -c "import mlx_lm" 2>/dev/null', { timeout: 5000 });
    return true;
  } catch {
    return false;
  }
}

export function installMlxLm(steps: string[]): boolean {
  const installer = findInstaller();
  if (!installer) {
    steps.push('No pip3 or uv found. Cannot install mlx-lm.');
    return false;
  }

  const cmd = installer === 'uv'
    ? 'uv pip install mlx-lm'
    : 'pip3 install mlx-lm';

  steps.push(`Installing mlx-lm via ${installer}...`);
  try {
    execSync(cmd, { encoding: 'utf-8', timeout: 120000, stdio: 'pipe' });
    steps.push('mlx-lm installed successfully.');
    return true;
  } catch (err: any) {
    // Try --user flag as fallback for pip
    if (installer === 'pip3') {
      try {
        execSync('pip3 install --user mlx-lm', { encoding: 'utf-8', timeout: 120000, stdio: 'pipe' });
        steps.push('mlx-lm installed (--user) successfully.');
        return true;
      } catch {}
    }
    steps.push(`mlx-lm install failed: ${(err as Error).message.slice(0, 200)}`);
    return false;
  }
}

// ── Server Management ──

export function isServerRunning(): boolean {
  try {
    const state = loadState();
    const port = state?.port || MLX_PORT;
    execSync(`curl -s -o /dev/null -w "%{http_code}" http://localhost:${port}/v1/models`, {
      encoding: 'utf-8',
      timeout: 3000,
    });
    return true;
  } catch {
    return false;
  }
}

export function createLaunchAgent(pythonPath: string, steps: string[]): boolean {
  const plist = `<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>Label</key>
  <string>${MLX_PLIST_LABEL}</string>
  <key>ProgramArguments</key>
  <array>
    <string>${pythonPath}</string>
    <string>-m</string>
    <string>mlx_lm.server</string>
    <string>--model</string>
    <string>${MLX_MODEL}</string>
    <string>--port</string>
    <string>${MLX_PORT}</string>
  </array>
  <key>RunAtLoad</key>
  <true/>
  <key>KeepAlive</key>
  <true/>
  <key>StandardOutPath</key>
  <string>${MLX_LOG_PATH}</string>
  <key>StandardErrorPath</key>
  <string>${MLX_LOG_PATH}</string>
</dict>
</plist>`;

  try {
    writeFileSync(MLX_PLIST_PATH, plist);
    execSync(`launchctl load "${MLX_PLIST_PATH}" 2>/dev/null`, { timeout: 5000 });
    steps.push(`LaunchAgent installed at ${MLX_PLIST_PATH}`);
    steps.push(`MLX server will start on port ${MLX_PORT}`);
    return true;
  } catch (err: any) {
    steps.push(`LaunchAgent install failed: ${(err as Error).message}`);
    return false;
  }
}

export function startServer(steps: string[]): boolean {
  try {
    execSync(`launchctl kickstart -kp gui/$(id -u)/${MLX_PLIST_LABEL} 2>/dev/null`, { timeout: 10000 });
    steps.push('MLX server started.');
    return true;
  } catch {
    steps.push('MLX server start failed. Check /tmp/mlx-server.log');
    return false;
  }
}

export function stopServer(): boolean {
  try {
    execSync(`launchctl unload "${MLX_PLIST_PATH}" 2>/dev/null`, { timeout: 5000 });
    return true;
  } catch {
    return false;
  }
}

// ── State Management ──

function loadState(): MlxState | null {
  try {
    if (existsSync(MLX_STATE_FILE)) {
      return JSON.parse(readFileSync(MLX_STATE_FILE, 'utf-8'));
    }
  } catch {}
  return null;
}

function saveState(state: MlxState): void {
  const dir = join(HOME, '.ldm', 'state');
  if (!existsSync(dir)) mkdirSync(dir, { recursive: true });
  writeFileSync(MLX_STATE_FILE, JSON.stringify(state, null, 2) + '\n');
}

// ── Verification ──

export async function verifyServer(steps: string[]): Promise<boolean> {
  const state = loadState();
  const port = state?.port || MLX_PORT;

  // Wait up to 30s for the server to start (model loading takes time)
  for (let i = 0; i < 15; i++) {
    try {
      const resp = await fetch(`http://localhost:${port}/v1/models`, {
        signal: AbortSignal.timeout(2000),
      });
      if (resp.ok) {
        const data = await resp.json() as any;
        const model = data?.data?.[0]?.id || 'unknown';
        steps.push(`MLX server verified: ${model} on port ${port}`);
        return true;
      }
    } catch {}
    await new Promise(r => setTimeout(r, 2000));
  }
  steps.push('MLX server did not respond within 30 seconds. Check /tmp/mlx-server.log');
  return false;
}

// ── Full Setup ──

export async function setupMlx(options?: { yes?: boolean }): Promise<{ ok: boolean; steps: string[] }> {
  const steps: string[] = [];

  // 1. Platform check
  const platform = detectPlatform();
  if (platform !== 'apple-silicon') {
    steps.push(`Platform: ${platform}. MLX requires Apple Silicon. Skipping.`);
    return { ok: false, steps };
  }
  steps.push('Platform: Apple Silicon detected.');

  // 2. Python check
  const pythonPath = findPython();
  if (!pythonPath) {
    steps.push('Python 3.10+ not found. Install via: brew install python3');
    return { ok: false, steps };
  }
  steps.push(`Python: ${pythonPath}`);

  // 3. Install mlx-lm if needed
  if (!isMlxLmInstalled()) {
    if (!options?.yes) {
      steps.push('mlx-lm not installed. Run with --yes to auto-install, or: pip3 install mlx-lm');
      return { ok: false, steps };
    }
    const installed = installMlxLm(steps);
    if (!installed) return { ok: false, steps };
  } else {
    steps.push('mlx-lm: already installed.');
  }

  // 4. Create LaunchAgent
  if (!existsSync(MLX_PLIST_PATH)) {
    const created = createLaunchAgent(pythonPath, steps);
    if (!created) return { ok: false, steps };
  } else {
    steps.push('LaunchAgent: already installed.');
  }

  // 5. Save state
  saveState({
    installed: true,
    port: MLX_PORT,
    model: MLX_MODEL,
    pythonPath,
    installedAt: new Date().toISOString(),
  });

  // 6. Start and verify
  if (!isServerRunning()) {
    startServer(steps);
    steps.push(`Waiting for model to load (~1.5 GB on first run)...`);
    const verified = await verifyServer(steps);
    if (!verified) {
      steps.push('Server started but not yet responding. It may still be downloading the model.');
      steps.push(`Check: tail -f ${MLX_LOG_PATH}`);
    }
  } else {
    steps.push(`MLX server: already running on port ${MLX_PORT}`);
  }

  return { ok: true, steps };
}

// ── Doctor Check ──

export function doctorCheck(): { status: 'ok' | 'warn' | 'fail' | 'skip'; detail: string; fix?: string } {
  const platform = detectPlatform();
  if (platform !== 'apple-silicon') {
    return { status: 'skip', detail: `${platform} (MLX requires Apple Silicon)` };
  }

  const state = loadState();
  if (!state || !state.installed) {
    return {
      status: 'warn',
      detail: 'not installed',
      fix: 'crystal init (will offer MLX setup)',
    };
  }

  if (isServerRunning()) {
    return { status: 'ok', detail: `running on port ${state.port} (${state.model})` };
  }

  // Installed but not running
  if (existsSync(MLX_PLIST_PATH)) {
    return {
      status: 'warn',
      detail: 'installed but not running',
      fix: `launchctl kickstart -kp gui/$(id -u)/${MLX_PLIST_LABEL}`,
    };
  }

  return {
    status: 'warn',
    detail: 'installed but LaunchAgent missing',
    fix: 'crystal init (will recreate LaunchAgent)',
  };
}

// ── Exports for constants ──

export const MLX_CONFIG = {
  port: MLX_PORT,
  model: MLX_MODEL,
  plistPath: MLX_PLIST_PATH,
  logPath: MLX_LOG_PATH,
  stateFile: MLX_STATE_FILE,
} as const;
