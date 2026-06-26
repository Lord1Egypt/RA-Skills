// `ssh-lab add <name> <user@host>` — add/update custom host config

import { loadLabConfig, saveLabConfig } from '../ssh/config.js';
import type { CommandResult, HostConfig } from '../types/index.js';

interface AddOptions {
  port?: number;
  tags?: string[];
  notes?: string;
  defaultPath?: string;
}

export function addCommand(
  alias: string,
  sshTarget: string,
  options: AddOptions = {}
): CommandResult<HostConfig> {
  const start = Date.now();
  const config = loadLabConfig();

  // Parse user@host
  let user: string | undefined;
  let hostname = sshTarget;

  const atIdx = sshTarget.indexOf('@');
  if (atIdx > 0) {
    user = sshTarget.slice(0, atIdx);
    hostname = sshTarget.slice(atIdx + 1);
  }

  const isUpdate = alias in config.hosts;

  config.hosts[alias] = {
    ...config.hosts[alias],
    alias,
    hostname,
    user,
    port: options.port,
    tags: options.tags || config.hosts[alias]?.tags || [],
    notes: options.notes || config.hosts[alias]?.notes,
    defaultPath: options.defaultPath || config.hosts[alias]?.defaultPath,
    source: 'custom',
  };

  saveLabConfig(config);

  const host = config.hosts[alias] as HostConfig;

  return {
    ok: true,
    command: 'add',
    data: host,
    summary: `${isUpdate ? 'Updated' : 'Added'} host '${alias}' → ${sshTarget}`,
    durationMs: Date.now() - start,
  };
}
