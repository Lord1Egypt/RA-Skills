#!/usr/bin/env node
/**
 * wip-repo-permissions-hook/guard.mjs
 * PreToolUse:Bash hook for Claude Code.
 * Blocks `gh repo edit --visibility public` unless -private counterpart exists.
 * Same pattern as wip-file-guard/guard.mjs.
 */

import { parseVisibilityCommand, checkPrivateCounterpart } from './core.mjs';

function deny(reason) {
  const output = {
    hookSpecificOutput: {
      hookEventName: 'PreToolUse',
      permissionDecision: 'deny',
      permissionDecisionReason: reason,
    },
  };
  process.stdout.write(JSON.stringify(output));
}

async function main() {
  let raw = '';
  for await (const chunk of process.stdin) {
    raw += chunk;
  }

  let input;
  try {
    input = JSON.parse(raw);
  } catch {
    // Can't parse input, allow by default
    process.exit(0);
  }

  const toolName = input.tool_name || '';
  const toolInput = input.tool_input || {};

  // Only check Bash commands
  if (toolName !== 'Bash') {
    process.exit(0);
  }

  const command = toolInput.command || '';

  // Only check commands that look like visibility changes
  const parsed = parseVisibilityCommand(command);
  if (!parsed) {
    process.exit(0);
  }

  // Check if the repo can be made public
  const result = checkPrivateCounterpart(parsed.org, parsed.repo);

  if (!result.allowed) {
    deny(result.reason);
    process.exit(0);
  }

  // Allowed
  process.exit(0);
}

main().catch(() => process.exit(0));
