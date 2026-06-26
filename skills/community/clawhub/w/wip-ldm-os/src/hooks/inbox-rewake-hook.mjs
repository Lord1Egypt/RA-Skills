#!/usr/bin/env node
/**
 * LDM OS Inbox Rewake Hook
 *
 * asyncRewake background hook for Claude Code. Watches ~/.ldm/messages/
 * with fs.watch and, when a new message addressed to this agent:session
 * arrives, writes the message as a system-reminder to stderr and exits
 * with code 2. Claude Code's harness wraps the stderr in a system-reminder
 * task-notification that wakes the model if idle or gets injected mid-query
 * if the model is busy. See:
 *
 *   ai/product/plans-prds/bridge/2026-04-11--cc-mini--autonomous-push-architecture.md
 *
 * Attached as a Stop hook with asyncRewake: true. Fires after every CC
 * turn. A lockfile prevents multiple instances from stacking across many
 * Stop events: only the first instance acquires the lock and watches;
 * subsequent instances see the lock held by a live process and exit 0
 * silently. The lock is released when the watching instance exits
 * (message caught, parent dead, hard timeout, or hard cancel).
 *
 * This hook is the "true push" layer 1 from the plan. Layers 2-4
 * (UserPromptSubmit inbox-check hook, SessionStart boot hook, manual
 * lesa_check_inbox) remain as independent fallbacks.
 *
 * Idempotent with inbox-check-hook.mjs: after firing, this hook marks
 * the message file's `read` field to true so the UserPromptSubmit hook
 * on the next user prompt does not re-surface the same message.
 *
 * Zero external dependencies beyond node:fs, node:path, node:os.
 */

import {
  existsSync,
  readFileSync,
  readdirSync,
  writeFileSync,
  unlinkSync,
  watch,
} from 'node:fs';
import { join, basename } from 'node:path';
import { homedir } from 'node:os';

const HOME = homedir();
const MESSAGES_DIR = join(HOME, '.ldm', 'messages');
const LOCK_PATH = join(MESSAGES_DIR, '.rewake.lock');
const LDM_CONFIG_PATH = join(HOME, '.ldm', 'config.json');
const TAG = '[inbox-rewake-hook]';

// Hard safety timeout: the watcher exits after 6 hours no matter what,
// so it cannot leak forever if the parent check or lock cleanup misses.
const HARD_TIMEOUT_MS = 6 * 60 * 60 * 1000;

// Parent CC process liveness check: every minute, verify the parent PID
// is still alive. If the parent died while this background hook is
// running, exit cleanly so we do not orphan.
const PARENT_CHECK_INTERVAL_MS = 60 * 1000;

// ── Helpers (mirror inbox-check-hook.mjs) ──

function readJSON(path) {
  try {
    return JSON.parse(readFileSync(path, 'utf8'));
  } catch {
    return null;
  }
}

function getAgentId() {
  const config = readJSON(LDM_CONFIG_PATH);
  if (config?.agents) {
    for (const [id, agent] of Object.entries(config.agents)) {
      if (agent.harness === 'claude-code') return id;
    }
  }
  return 'cc-mini';
}

function getSessionName(input) {
  // Mirror inbox-check-hook.mjs: CC writes /rename labels to
  // ~/.claude/sessions/<pid>.json, and this hook is spawned fresh by CC
  // so ppid = CC PID. Reading the session file picks up /rename and
  // /resume labels without any env var or restart.
  try {
    const ccSessionPath = join(HOME, '.claude', 'sessions', `${process.ppid}.json`);
    const data = JSON.parse(readFileSync(ccSessionPath, 'utf8'));
    if (data.name && typeof data.name === 'string') {
      return data.name;
    }
  } catch {
    // No session file. Normal for non-CC harnesses.
  }
  return (
    process.env.LDM_SESSION_NAME ||
    process.env.CLAUDE_SESSION_NAME ||
    basename(input?.cwd || process.cwd()) ||
    'default'
  );
}

/**
 * Check if a message's "to" field matches this agent:session.
 * Same logic as inbox-check-hook.mjs so both hooks agree on routing.
 */
function messageMatchesAgent(to, agentId, sessionName) {
  if (!to) return false;
  if (to === '*' || to === 'all') return true;
  if (to === agentId) return true;
  if (to === `${agentId}:*`) return true;
  if (to === `${agentId}:${sessionName}`) return true;
  if (to === sessionName) return true;
  return false;
}

// ── Lock management ──
//
// A single machine may have seven or more concurrent CC sessions, each
// spawning its own rewake hook on every Stop event. Without a lock, we
// accumulate fs.watch handles forever and every new message fires all
// pending hooks simultaneously.
//
// The lock is per-session, keyed by agent:session, so different CC
// sessions do not block each other. The lock file lives at
// ~/.ldm/messages/.rewake.<agent>-<session>.lock and contains the PID
// of the watching process. Subsequent hook spawns in the same session
// see the lock, verify the PID is alive, and exit silently.

function lockPathFor(agentId, sessionName) {
  // Replace any filesystem-unfriendly chars with '-' so session names
  // like "memory:crystal" or "brainstorm (oc)" do not produce invalid
  // filenames. Keeps alphanumerics, dashes, underscores.
  const safe = `${agentId}-${sessionName}`.replace(/[^a-zA-Z0-9._-]/g, '-');
  return join(MESSAGES_DIR, `.rewake.${safe}.lock`);
}

function pidIsAlive(pid) {
  try {
    process.kill(pid, 0); // signal 0 is a liveness probe
    return true;
  } catch {
    return false;
  }
}

function acquireLock(lockPath) {
  try {
    if (existsSync(lockPath)) {
      const raw = readFileSync(lockPath, 'utf8').trim();
      const existing = parseInt(raw, 10);
      if (existing && existing > 0 && pidIsAlive(existing)) {
        return false;
      }
      // Stale lock: previous holder is dead, take over.
      try { unlinkSync(lockPath); } catch {}
    }
  } catch {}

  try {
    writeFileSync(lockPath, String(process.pid));
    return true;
  } catch {
    return false;
  }
}

function releaseLock(lockPath) {
  try {
    if (!existsSync(lockPath)) return;
    const raw = readFileSync(lockPath, 'utf8').trim();
    const pid = parseInt(raw, 10);
    if (pid === process.pid) {
      unlinkSync(lockPath);
    }
  } catch {}
}

// ── Message delivery ──
//
// When a match is found, we:
//   1. Mark the file's `read` field to true (so inbox-check-hook.mjs on
//      the next UserPromptSubmit does not re-surface it).
//   2. Write the formatted message body to stderr.
//   3. Release the lock.
//   4. process.exit(2) to trigger Claude Code's asyncRewake wake path.

function markRead(filePath) {
  try {
    const data = readJSON(filePath);
    if (!data) return;
    data.read = true;
    writeFileSync(filePath, JSON.stringify(data, null, 2) + '\n');
  } catch {
    // Non-fatal. Worst case: inbox-check-hook surfaces the same message
    // on the next UserPromptSubmit. That is still correct behavior; it
    // just means the same message gets two surfaces.
  }
}

/**
 * Batch fire: mark every matching pending file read, then write a
 * single combined payload to stderr and exit code 2. One wake cycle
 * surfaces every message that was pending at the moment we scanned,
 * instead of one wake per message (which costs one model turn each
 * and adds up quickly under load). Shipped in alpha.31 after the
 * canary session reported "each message = one wake = one Opus turn"
 * during the alpha.30 autonomous-push test.
 *
 * Messages are sorted oldest first before output so the reader sees
 * them in the original arrival order.
 *
 * Marks are written before stderr output so that if the process dies
 * mid-fire (SIGKILL, crash), the files are still flagged read and we
 * do not re-deliver the same batch on the next wake.
 */
function fireBatch(matches, lockPath, agentId, sessionName) {
  // Mark read first for atomicity against mid-fire death.
  for (const { filePath } of matches) markRead(filePath);

  matches.sort((a, b) => {
    const ta = a.data.timestamp || '';
    const tb = b.data.timestamp || '';
    return ta.localeCompare(tb);
  });

  const plural = matches.length > 1 ? 's' : '';
  const header =
    `== Bridge Push (autonomous) ==\n` +
    `You have ${matches.length} new message${plural} delivered by the inbox-rewake ` +
    `hook while you were idle. They are addressed to ${agentId}:${sessionName} and ` +
    `are now marked read in the inbox.\n\n`;

  const body = matches
    .map(({ data: m }) => {
      const h =
        `[${m.type || 'chat'}] from ${m.from || 'unknown'} ` +
        `(${m.timestamp || 'no timestamp'}):`;
      return `${h}\n${m.body || '(empty)'}`;
    })
    .join('\n\n---\n\n');

  const footer =
    `\n\nAcknowledge or respond as appropriate. Use lesa_check_inbox or ` +
    `ldm_send_message to continue the thread.`;

  process.stderr.write(header + body + footer);

  const idList = matches
    .map((m) => m.data.id || '(no id)')
    .slice(0, 5)
    .join(', ');
  const trailer = matches.length > 5 ? ` (+${matches.length - 5} more)` : '';
  process.stderr.write(
    `\n${TAG} fired for ${matches.length} message${plural} to ${agentId}:${sessionName}: ${idList}${trailer}\n`,
  );

  releaseLock(lockPath);
  process.exit(2);
}

// ── Main ──

async function main() {
  // Drain stdin even if we ignore it. Hooks receive JSON per the CC
  // hook protocol; we do not need any of the fields here.
  let raw = '';
  try {
    for await (const chunk of process.stdin) raw += chunk;
  } catch {}

  let input = {};
  try { input = JSON.parse(raw); } catch {}

  if (!existsSync(MESSAGES_DIR)) {
    // Nothing to watch. Exit silently. A future install will recreate.
    process.exit(0);
  }

  const agentId = getAgentId();
  const sessionName = getSessionName(input);
  const lockPath = lockPathFor(agentId, sessionName);
  const parentPid = process.ppid;

  // Try to take the lock. If another instance of this session's rewake
  // hook is already watching, exit silently and let them handle it.
  if (!acquireLock(lockPath)) {
    process.stderr.write(
      `${TAG} another live instance holds ${basename(lockPath)}, exiting\n`,
    );
    process.exit(0);
  }

  // Guarantee we release the lock on any exit path.
  process.on('exit', () => releaseLock(lockPath));
  process.on('SIGTERM', () => { releaseLock(lockPath); process.exit(0); });
  process.on('SIGINT',  () => { releaseLock(lockPath); process.exit(0); });
  process.on('uncaughtException', (err) => {
    process.stderr.write(`${TAG} uncaughtException: ${err.message}\n`);
    releaseLock(lockPath);
    process.exit(0);
  });

  // Track which message IDs we have already fired for in this run.
  // fs.watch can fire multiple events for a single file write; the
  // in-memory set prevents duplicate firings in the window between
  // writing `read: true` to disk and the next scan picking it up.
  const seen = new Set();

  function collectPending() {
    const matches = [];
    try {
      const files = readdirSync(MESSAGES_DIR).filter((f) => f.endsWith('.json'));
      for (const file of files) {
        const filePath = join(MESSAGES_DIR, file);
        const data = readJSON(filePath);
        if (!data) continue;
        if (data.read === true) continue;
        if (data.id && seen.has(data.id)) continue;
        if (!messageMatchesAgent(data.to, agentId, sessionName)) continue;
        if (data.id) seen.add(data.id);
        matches.push({ data, filePath });
      }
    } catch {}
    return matches;
  }

  function scanAndFire() {
    const matches = collectPending();
    if (matches.length > 0) {
      // fireBatch marks read, writes stderr, releases lock, and exits
      // the process. Control does not return.
      fireBatch(matches, lockPath, agentId, sessionName);
    }
  }

  // Initial scan: catch any messages that arrived between the previous
  // hook instance exiting and this one starting up. If any match, we
  // fire immediately and exit; the caller never sees this function
  // return.
  scanAndFire();

  // Set up the fs.watch for new messages.
  let watcher;
  try {
    watcher = watch(MESSAGES_DIR, { persistent: true }, (eventType, filename) => {
      if (!filename || !filename.endsWith('.json')) return;
      // Re-scan on every event. fs.watch can coalesce or miss events
      // under load, so scanning the directory is more reliable than
      // trusting the filename argument alone.
      scanAndFire();
    });
  } catch (e) {
    process.stderr.write(`${TAG} fs.watch failed: ${e.message}\n`);
    releaseLock(lockPath);
    process.exit(0);
  }

  // Parent process liveness check. If the CC session that spawned us
  // has exited, stop watching and release the lock.
  const parentCheck = setInterval(() => {
    if (!pidIsAlive(parentPid)) {
      process.stderr.write(`${TAG} parent pid ${parentPid} is dead, exiting\n`);
      clearInterval(parentCheck);
      if (watcher) watcher.close();
      releaseLock(lockPath);
      process.exit(0);
    }
  }, PARENT_CHECK_INTERVAL_MS);

  // Hard safety timeout.
  const hardTimeout = setTimeout(() => {
    process.stderr.write(`${TAG} hard timeout after ${HARD_TIMEOUT_MS / 1000}s\n`);
    clearInterval(parentCheck);
    if (watcher) watcher.close();
    releaseLock(lockPath);
    process.exit(0);
  }, HARD_TIMEOUT_MS);

  // Let the timers keep the event loop alive. If either timer fires or
  // the watcher fires a message match, the process exits and releases
  // the lock.
  process.stderr.write(
    `${TAG} watching ${MESSAGES_DIR} for ${agentId}:${sessionName} (parent pid ${parentPid})\n`,
  );
}

main().catch((err) => {
  process.stderr.write(`${TAG} fatal in main: ${err && err.message}\n`);
  process.exit(0);
});
