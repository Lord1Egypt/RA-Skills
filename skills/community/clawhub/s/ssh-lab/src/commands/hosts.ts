// `ssh-lab hosts` — list all configured servers

import { discoverHosts } from '../ssh/config.js';
import type { CommandResult, HostConfig } from '../types/index.js';

export function hostsCommand(): CommandResult<HostConfig[]> {
  const start = Date.now();
  const hosts = discoverHosts();

  const summary = hosts.length === 0
    ? 'No hosts configured. Add hosts to ~/.ssh/config or run: ssh-lab add <name> <user@host>'
    : `${hosts.length} host(s) found:\n` + hosts.map((h) => {
        const target = h.user ? `${h.user}@${h.hostname}` : h.hostname;
        const port = h.port && h.port !== 22 ? `:${h.port}` : '';
        const tags = h.tags.length ? ` [${h.tags.join(', ')}]` : '';
        const notes = h.notes ? ` — ${h.notes}` : '';
        const source = h.source === 'custom' ? ' (custom)' : '';
        return `  ${h.alias} → ${target}${port}${tags}${notes}${source}`;
      }).join('\n');

  return {
    ok: true,
    command: 'hosts',
    data: hosts,
    summary,
    durationMs: Date.now() - start,
  };
}
