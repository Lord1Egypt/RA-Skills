#!/usr/bin/env node
import { spawn } from 'node:child_process';
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

// 1. Prefer existing CLIENT_ID, fallback to overseas skill default Client ID
process.env.CLIENT_ID = process.env.CLIENT_ID || 'rollinggoglobal';

const isWin = process.platform === 'win32';
const scriptDir = path.dirname(fileURLToPath(import.meta.url));
const skillBinDir = path.resolve(scriptDir, '..', 'bin');

// 2. Cross-platform executable resolution (Windows / macOS / Linux)
function resolveExecutable() {
  if (fs.existsSync(skillBinDir)) {
    const localExeName = isWin ? 'rgg.exe' : 'rgg';
    const localPath = path.join(skillBinDir, localExeName);
    if (fs.existsSync(localPath)) {
      return { cmd: localPath, shell: false };
    }
  }

  if (isWin) {
    return { cmd: 'rgg.cmd', shell: true, fallbackCmd: 'rgg' };
  } else {
    return { cmd: 'rgg', shell: false };
  }
}

// 3. Escape arguments containing spaces for Windows cmd.exe
function sanitizeArgs(args) {
  return args.map((arg) => {
    if (typeof arg === 'string' && arg.includes(' ') && !arg.startsWith('"')) {
      return `"${arg}"`;
    }
    return arg;
  });
}

const { cmd, shell, fallbackCmd } = resolveExecutable();

function runChild(targetCmd, useShell) {
  const args = useShell ? sanitizeArgs(process.argv.slice(2)) : process.argv.slice(2);

  const child = spawn(targetCmd, args, {
    stdio: 'inherit',
    env: process.env,
    shell: useShell,
  });

  const onSignal = (sig) => {
    if (child && !child.killed) child.kill(sig);
  };
  process.on('SIGINT', () => onSignal('SIGINT'));
  process.on('SIGTERM', () => onSignal('SIGTERM'));

  child.on('error', (err) => {
    if (err.code === 'ENOENT' && fallbackCmd && targetCmd !== fallbackCmd) {
      runChild(fallbackCmd, true);
    } else {
      console.error(`[rgg wrapper] Failed to execute rgg command (OS: ${process.platform}):`, err.message);
      console.error('Please make sure @rollinggo/hotel-global is installed via "npm install -g @rollinggo/hotel-global@latest" or "python scripts/install.py".');
      process.exit(1);
    }
  });

  child.on('exit', (code, signal) => {
    if (signal) {
      process.kill(process.pid, signal);
    } else {
      process.exit(code || 0);
    }
  });
}

runChild(cmd, shell);
