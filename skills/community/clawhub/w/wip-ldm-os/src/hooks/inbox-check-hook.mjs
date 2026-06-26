#!/usr/bin/env node
/**
 * LDM OS Inbox Check Hook
 * UserPromptSubmit hook for Claude Code.
 * Scans ~/.ldm/messages/ for pending messages addressed to this agent
 * and surfaces them as additionalContext before CC responds.
 *
 * Follows guard.mjs pattern: stdin JSON in, stdout JSON out, exit 0 always.
 *
 * As of alpha.31 this hook DOES mark messages as `read: true` after
 * surfacing them. Previously we deferred draining to `lesa_check_inbox`,
 * but that caused a dedup race with `inbox-rewake-hook.mjs`: if layer 2
 * (this hook) surfaced a message without marking it read, then layer 1
 * (the rewake Stop hook) would fire on the same unread message on the
 * next Stop event and re-deliver it, costing another model turn. Marking
 * read here makes the two layers cooperative ... each unread message
 * surfaces exactly once regardless of which layer catches it first.
 *
 * See the dedup diagnosis in:
 *   ai/product/plans-prds/bridge/2026-04-11--cc-mini--autonomous-push-architecture.md
 *
 * Zero external dependencies beyond node:fs and node:path.
 */

import { existsSync, readFileSync, readdirSync, writeFileSync } from 'node:fs';
import { join, basename } from 'node:path';
import { homedir } from 'node:os';

const HOME = homedir();
const MESSAGES_DIR = join(HOME, '.ldm', 'messages');
const LDM_CONFIG_PATH = join(HOME, '.ldm', 'config.json');
const TAG = '[inbox-check-hook]';

// ── Helpers ──

function readJSON(path) {
  try {
    return JSON.parse(readFileSync(path, 'utf8'));
  } catch {
    return null;
  }
}

/**
 * Mark a message file's `read` field to true so the rewake hook and
 * future UserPromptSubmit invocations skip it. Idempotent and best
 * effort; failures are swallowed because they are not fatal ... the
 * worst case is that we re-surface the message once more, which is
 * the old (pre-alpha.31) behavior.
 */
function markRead(filePath) {
  try {
    const data = readJSON(filePath);
    if (!data) return;
    if (data.read === true) return;
    data.read = true;
    writeFileSync(filePath, JSON.stringify(data, null, 2) + '\n');
  } catch {
    // Non-fatal.
  }
}

function getAgentId() {
  // Try LDM config first
  const config = readJSON(LDM_CONFIG_PATH);
  if (config?.agents) {
    // Find the agent entry for this machine's claude-code harness
    for (const [id, agent] of Object.entries(config.agents)) {
      if (agent.harness === 'claude-code') return id;
    }
  }
  return 'cc-mini';
}

function getSessionName(input) {
  // 1. Try CC session file for the parent PID.
  // CC writes /rename labels to ~/.claude/sessions/<pid>.json.
  // This hook is spawned fresh each time by CC, so ppid = CC PID.
  // Reading the session file picks up /rename and /resume labels
  // without any env var or restart.
  try {
    const ccSessionPath = join(HOME, '.claude', 'sessions', `${process.ppid}.json`);
    const data = JSON.parse(readFileSync(ccSessionPath, 'utf8'));
    if (data.name && typeof data.name === 'string') {
      return data.name;
    }
  } catch {
    // No session file. Normal for non-CC harnesses.
  }

  // 2. Env var override
  // 3. CWD basename fallback
  // 4. Default
  return (
    process.env.LDM_SESSION_NAME ||
    process.env.CLAUDE_SESSION_NAME ||
    basename(input?.cwd || process.cwd()) ||
    'default'
  );
}

/**
 * Check if a message's "to" field matches this agent.
 * Supported targets:
 *   - exact agent ID (e.g. "cc-mini")
 *   - agent:session (e.g. "cc-mini:my-session")
 *   - agent:* (e.g. "cc-mini:*" ... all sessions of this agent)
 *   - "*" or "all" ... broadcast to everyone
 *   - exact session name match
 */
function messageMatchesAgent(to, agentId, sessionName) {
  if (!to) return false;

  // Broadcast targets
  if (to === '*' || to === 'all') return true;

  // Exact agent ID
  if (to === agentId) return true;

  // Agent wildcard: "cc-mini:*"
  if (to === `${agentId}:*`) return true;

  // Agent + specific session: "cc-mini:my-session"
  if (to === `${agentId}:${sessionName}`) return true;

  // Direct session name match
  if (to === sessionName) return true;

  return false;
}

// ── Main ──

async function main() {
  let raw = '';
  for await (const chunk of process.stdin) raw += chunk;

  let input;
  try {
    input = JSON.parse(raw);
  } catch {
    // Bad input... exit clean with no context
    process.stdout.write(JSON.stringify({}));
    process.exit(0);
  }

  // Fast exit if messages dir doesn't exist
  if (!existsSync(MESSAGES_DIR)) {
    process.stdout.write(JSON.stringify({}));
    process.exit(0);
  }

  const agentId = getAgentId();
  const sessionName = getSessionName(input);

  // Scan for pending messages
  let files;
  try {
    files = readdirSync(MESSAGES_DIR).filter(f => f.endsWith('.json'));
  } catch {
    process.stdout.write(JSON.stringify({}));
    process.exit(0);
  }

  // Fast exit if no message files
  if (files.length === 0) {
    process.stdout.write(JSON.stringify({}));
    process.exit(0);
  }

  const pending = [];
  const seen = new Set();

  for (const file of files) {
    const fullPath = join(MESSAGES_DIR, file);
    const data = readJSON(fullPath);
    if (!data) continue;

    // Skip already-read messages (if the field exists)
    if (data.read === true) continue;

    // Check if addressed to us
    if (!messageMatchesAgent(data.to, agentId, sessionName)) continue;

    // Deduplicate by message ID
    if (data.id && seen.has(data.id)) continue;
    if (data.id) seen.add(data.id);

    pending.push(data);

    // Mark the message read on disk so the rewake hook (layer 1) does
    // not re-deliver it on the next Stop event and cost another model
    // turn. This was the dedup race observed and reported by the canary
    // session during the alpha.30 autonomous-push test.
    markRead(fullPath);
  }

  // Fast exit if nothing pending
  if (pending.length === 0) {
    process.stdout.write(JSON.stringify({}));
    process.exit(0);
  }

  // Sort by timestamp (oldest first)
  pending.sort((a, b) => (a.timestamp || '').localeCompare(b.timestamp || ''));

  // Format output
  const msgLines = pending
    .map(m => `[${m.type || 'chat'}] from ${m.from || 'unknown'} (${m.timestamp || 'no timestamp'}):\n  ${m.body || '(empty)'}`)
    .join('\n\n');

  const additionalContext =
    `== Pending Messages (${pending.length}) ==\n` +
    `You have ${pending.length} unread message(s). Review them and respond if needed. Use lesa_check_inbox to mark as read when done.\n\n` +
    msgLines;

  const output = {
    hookSpecificOutput: {
      hookEventName: 'UserPromptSubmit',
      additionalContext,
    },
  };

  process.stdout.write(JSON.stringify(output));
  process.stderr.write(`${TAG} ${pending.length} pending message(s) for ${agentId}:${sessionName}\n`);
  process.exit(0);
}

main().catch(() => {
  process.stdout.write(JSON.stringify({}));
  process.exit(0);
});
