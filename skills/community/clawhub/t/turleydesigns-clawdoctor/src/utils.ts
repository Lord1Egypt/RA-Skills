import { execSync, execFileSync } from 'child_process';
import os from 'os';

export function nowIso(): string {
  return new Date().toISOString();
}

export function nowUtcDisplay(): string {
  return new Date().toISOString().replace('T', ' ').slice(0, 16) + ' UTC';
}

export function hostname(): string {
  return os.hostname();
}

export function runCommand(bin: string, args: string[] = []): { stdout: string; stderr: string; ok: boolean } {
  try {
    const stdout = execFileSync(bin, args, { encoding: 'utf-8', timeout: 15000 });
    return { stdout, stderr: '', ok: true };
  } catch (err: unknown) {
    const e = err as { stdout?: string; stderr?: string };
    return { stdout: e.stdout ?? '', stderr: e.stderr ?? '', ok: false };
  }
}

export function runShell(cmd: string): { stdout: string; stderr: string; ok: boolean } {
  try {
    const stdout = execSync(cmd, { encoding: 'utf-8', timeout: 15000, stdio: ['pipe', 'pipe', 'pipe'] });
    return { stdout, stderr: '', ok: true };
  } catch (err: unknown) {
    const e = err as { stdout?: string; stderr?: string };
    return { stdout: e.stdout ?? '', stderr: e.stderr ?? '', ok: false };
  }
}

export function fileAgeSeconds(mtime: Date): number {
  return (Date.now() - mtime.getTime()) / 1000;
}

export function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

export function formatBytes(bytes: number): string {
  if (bytes < 1024) return `${bytes}B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)}KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)}MB`;
}

export function truncate(str: string, maxLen: number): string {
  if (str.length <= maxLen) return str;
  return str.slice(0, maxLen - 3) + '...';
}
