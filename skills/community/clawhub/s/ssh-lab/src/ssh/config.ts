// SSH config discovery — uses `ssh -G` for accurate resolution
// Falls back to simple ~/.ssh/config parsing if ssh -G unavailable

import { execSync } from 'node:child_process';
import { readFileSync, existsSync, writeFileSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import type { HostConfig, SshLabConfig } from '../types/index.js';

const SSH_CONFIG_PATH = join(process.env.HOME || '~', '.ssh', 'config');
const SSH_LAB_CONFIG_PATH = process.env.SSH_LAB_CONFIG
  || join(process.env.XDG_CONFIG_HOME || join(process.env.HOME || '~', '.config'), 'ssh-lab', 'config.json');

/** Use `ssh -G <host>` to resolve effective SSH config for a host */
function resolveWithSshG(alias: string): Partial<HostConfig> | null {
  try {
    const output = execSync(`ssh -G ${alias} 2>/dev/null`, {
      encoding: 'utf-8',
      timeout: 5000,
    });

    const config: Record<string, string> = {};
    for (const line of output.split('\n')) {
      const idx = line.indexOf(' ');
      if (idx > 0) {
        const key = line.slice(0, idx).toLowerCase();
        const value = line.slice(idx + 1).trim();
        config[key] = value;
      }
    }

    return {
      alias,
      hostname: config.hostname || alias,
      user: config.user,
      port: config.port ? parseInt(config.port, 10) : undefined,
      identityFile: config.identityfile,
      proxyJump: config.proxyjump && config.proxyjump !== 'none' ? config.proxyjump : undefined,
    };
  } catch {
    return null;
  }
}

/** Parse ~/.ssh/config to extract Host entries (simple fallback) */
function parseSSHConfigFile(): string[] {
  if (!existsSync(SSH_CONFIG_PATH)) return [];

  const content = readFileSync(SSH_CONFIG_PATH, 'utf-8');
  const hosts: string[] = [];

  for (const line of content.split('\n')) {
    const trimmed = line.trim();
    if (/^Host\s+/i.test(trimmed)) {
      const hostNames = trimmed.replace(/^Host\s+/i, '').split(/\s+/);
      for (const h of hostNames) {
        // Skip wildcards and patterns
        if (!h.includes('*') && !h.includes('?') && !h.includes('!') && h !== '') {
          hosts.push(h);
        }
      }
    }
  }

  return hosts;
}

/** Load ssh-lab custom config */
export function loadLabConfig(): SshLabConfig {
  const defaults: SshLabConfig = {
    version: 1,
    defaults: {
      sshTimeoutMs: 15000,
      commandTimeoutMs: 30000,
      maxConcurrency: 5,
      output: 'summary',
    },
    hosts: {},
  };

  if (!existsSync(SSH_LAB_CONFIG_PATH)) return defaults;

  try {
    const content = readFileSync(SSH_LAB_CONFIG_PATH, 'utf-8');
    const parsed = JSON.parse(content) as Partial<SshLabConfig>;
    return {
      ...defaults,
      ...parsed,
      defaults: { ...defaults.defaults, ...parsed.defaults },
      hosts: { ...defaults.hosts, ...parsed.hosts },
    };
  } catch {
    return defaults;
  }
}

/** Save ssh-lab config */
export function saveLabConfig(config: SshLabConfig): void {
  mkdirSync(dirname(SSH_LAB_CONFIG_PATH), { recursive: true });
  writeFileSync(SSH_LAB_CONFIG_PATH, JSON.stringify(config, null, 2) + '\n');
}

/** Discover all configured hosts (SSH config + custom config) */
export function discoverHosts(): HostConfig[] {
  const labConfig = loadLabConfig();
  const sshHosts = parseSSHConfigFile();
  const seen = new Set<string>();
  const hosts: HostConfig[] = [];

  // Custom hosts first (higher priority)
  for (const [alias, override] of Object.entries(labConfig.hosts)) {
    const resolved = resolveWithSshG(alias);
    const host: HostConfig = {
      alias,
      hostname: override.hostname || resolved?.hostname || alias,
      user: override.user || resolved?.user,
      port: override.port || resolved?.port,
      identityFile: override.identityFile || resolved?.identityFile,
      proxyJump: override.proxyJump || resolved?.proxyJump,
      source: 'custom',
      tags: override.tags || [],
      notes: override.notes,
      defaultPath: override.defaultPath,
    };
    hosts.push(host);
    seen.add(alias);
  }

  // SSH config hosts
  for (const alias of sshHosts) {
    if (seen.has(alias)) continue;
    const resolved = resolveWithSshG(alias);
    if (!resolved) continue;

    hosts.push({
      alias,
      hostname: resolved.hostname || alias,
      user: resolved.user,
      port: resolved.port,
      identityFile: resolved.identityFile,
      proxyJump: resolved.proxyJump,
      source: 'ssh-config',
      tags: [],
    });
    seen.add(alias);
  }

  return hosts;
}

/** Resolve a single host by alias */
export function resolveHost(alias: string): HostConfig | null {
  const labConfig = loadLabConfig();
  const override = labConfig.hosts[alias];

  const resolved = resolveWithSshG(alias);
  if (!resolved && !override) return null;

  return {
    alias,
    hostname: override?.hostname || resolved?.hostname || alias,
    user: override?.user || resolved?.user,
    port: override?.port || resolved?.port,
    identityFile: override?.identityFile || resolved?.identityFile,
    proxyJump: override?.proxyJump || resolved?.proxyJump,
    source: override ? 'custom' : 'ssh-config',
    tags: override?.tags || [],
    notes: override?.notes,
    defaultPath: override?.defaultPath,
  };
}

/** Resolve 'all' or a comma-separated list of host aliases */
export function resolveHosts(target: string): HostConfig[] {
  if (target === 'all') return discoverHosts();

  const aliases = target.split(',').map((s) => s.trim()).filter(Boolean);
  const hosts: HostConfig[] = [];

  for (const alias of aliases) {
    const host = resolveHost(alias);
    if (host) hosts.push(host);
  }

  return hosts;
}

export { SSH_LAB_CONFIG_PATH };
