#!/usr/bin/env node
/**
 * LDM OS Stop Hook
 * Deregisters session from ~/.ldm/sessions/ when Claude Code session ends.
 * Follows guard.mjs pattern: stdin JSON in, stdout JSON out, exit 0 always.
 */

import { deregisterSession } from '../../lib/sessions.mjs';

async function main() {
  let raw = '';
  for await (const chunk of process.stdin) raw += chunk;

  const sessionName = process.env.CLAUDE_SESSION_NAME || 'unknown';

  try {
    deregisterSession(sessionName);
  } catch {}

  process.stdout.write(JSON.stringify({}));
  process.exit(0);
}

main().catch(() => process.exit(0));
