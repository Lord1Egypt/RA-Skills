#!/usr/bin/env node
// LDM OS Boot Sequence Hook
// SessionStart hook for Claude Code.
// Reads boot files and injects them into context via additionalContext.
// Follows guard.mjs pattern: stdin JSON in, stdout JSON out, exit 0 always.

import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join, dirname, resolve, basename } from 'node:path';
import { homedir } from 'node:os';
import { fileURLToPath } from 'node:url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const HOME = homedir();
const TAG = '[boot-hook]';

function resolvePath(p) {
  if (p.startsWith('~/')) return join(HOME, p.slice(2));
  return p;
}

function readFileSafe(filePath) {
  try {
    const resolved = resolvePath(filePath);
    if (!existsSync(resolved)) return null;
    return readFileSync(resolved, 'utf-8');
  } catch {
    return null;
  }
}

function listDirSafe(dirPath) {
  try {
    const resolved = resolvePath(dirPath);
    if (!existsSync(resolved)) return [];
    return readdirSync(resolved).sort();
  } catch {
    return [];
  }
}

// Per-step default line caps applied when boot-config.json does not set
// maxLines for the step. Keyed by the step key in config.steps. Any of these
// can be overridden per-step via a maxLines value in boot-config.json.
// Lives in code (not just the config template) because the installer preserves
// an existing user boot-config.json, so config-template changes never reach
// existing installs. Defaults must ride along with the hook.
const DEFAULT_MAX_LINES = {
  sharedContext: 80,
  soul: 80,
  context: 60,
  repoLocations: 80,
};

// Default staleness cutoffs. Overridable via top-level config keys
// (stalenessDays, dailyLogStalenessDays) or per-step keys of the same name.
const DEFAULT_STALENESS_DAYS = 14; // most-recent strategy (journals)
const DEFAULT_DAILY_LOG_STALENESS_DAYS = 2; // daily-logs strategy guard

function resolveMaxLines(key, step) {
  if (step.maxLines != null) return step.maxLines;
  if (DEFAULT_MAX_LINES[key] != null) return DEFAULT_MAX_LINES[key];
  return null;
}

// Returns { text, capped }. When truncation happens, the marker names the
// full path so a future reader can pull the rest.
function truncateTop(content, maxLines, fullPath) {
  if (!maxLines || !content) return { text: content, capped: false };
  const lines = content.split('\n');
  if (lines.length <= maxLines) return { text: content, capped: false };
  const where = fullPath || '(path unknown)';
  const marker = `\n[... truncated at ${maxLines} of ${lines.length} lines. Read the rest: ${where} ...]`;
  return { text: lines.slice(0, maxLines).join('\n') + marker, capped: true };
}

function truncateBottom(content, maxLines, fullPath) {
  if (!maxLines || !content) return { text: content, capped: false };
  const lines = content.split('\n');
  if (lines.length <= maxLines) return { text: content, capped: false };
  const where = fullPath || '(path unknown)';
  const marker = `[... showing last ${maxLines} of ${lines.length} lines. Read the rest: ${where} ...]\n`;
  return { text: marker + lines.slice(-maxLines).join('\n'), capped: true };
}

// Extract a YYYY-MM-DD prefix from a filename, or null if none.
function dateStrFromName(fileName) {
  const m = /^(\d{4}-\d{2}-\d{2})/.exec(fileName || '');
  return m ? m[1] : null;
}

// Whole-day difference (todayStr - dateStr) in days. Both are YYYY-MM-DD.
// Positive means dateStr is in the past. null if either is unparseable.
function ageInDays(dateStr, todayStr) {
  const a = Date.parse(`${dateStr}T00:00:00Z`);
  const b = Date.parse(`${todayStr}T00:00:00Z`);
  if (Number.isNaN(a) || Number.isNaN(b)) return null;
  return Math.round((b - a) / 86400000);
}

function getTodayAndYesterday(timezone) {
  const now = new Date();
  const formatter = new Intl.DateTimeFormat('en-CA', {
    timeZone: timezone,
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
  });
  const today = formatter.format(now);

  const yesterday = new Date(now);
  yesterday.setDate(yesterday.getDate() - 1);
  const yesterdayStr = formatter.format(yesterday);

  return { today, yesterday: yesterdayStr };
}

function findMostRecent(dirPath) {
  const files = listDirSafe(dirPath);
  // Filter to .md files with date-like names, sort descending
  const dated = files
    .filter(f => f.endsWith('.md') && /^\d{4}-\d{2}-\d{2}/.test(f))
    .sort()
    .reverse();

  if (dated.length > 0) return dated[0];

  // Fallback: any .md file, most recent by name
  const mds = files.filter(f => f.endsWith('.md')).sort().reverse();
  return mds[0] || null;
}

function loadConfig() {
  const configPath = join(__dirname, 'boot-config.json');
  try {
    return JSON.parse(readFileSync(configPath, 'utf-8'));
  } catch {
    process.stderr.write(`${TAG} boot-config.json not found, using hardcoded defaults\n`);
    return null;
  }
}

function getDefaultConfig() {
  return {
    agentId: 'cc-mini',
    timezone: 'America/Los_Angeles',
    maxTotalLines: 2000,
    stalenessDays: DEFAULT_STALENESS_DAYS,
    dailyLogStalenessDays: DEFAULT_DAILY_LOG_STALENESS_DAYS,
    steps: {
      sharedContext: { path: '~/.openclaw/workspace/SHARED-CONTEXT.md', label: 'SHARED-CONTEXT.md', stepNumber: 2, critical: true },
      journals: { dir: '~/.ldm/agents/cc-mini/memory/journals', label: 'Most Recent CC Journal (Legacy)', stepNumber: 3, maxLines: 80, strategy: 'most-recent' },
      workspaceDailyLogs: { dir: '~/.openclaw/workspace/memory', label: 'Workspace Daily Logs', stepNumber: 4, maxLines: 40, strategy: 'daily-logs', days: ['today', 'yesterday'] },
      fullHistory: { label: 'Full History', stepNumber: 5, reminder: 'Read on cold start: team/cc-mini/documents/cc-full-history.md' },
      context: { path: '~/.ldm/agents/cc-mini/CONTEXT.md', label: 'CC CONTEXT.md', stepNumber: 6, critical: true },
      soul: { path: '~/.ldm/agents/cc-mini/SOUL.md', label: 'CC SOUL.md', stepNumber: 7 },
      ccJournals: { dir: '~/.ldm/agents/cc-mini/memory/journals', label: 'Most Recent CC Journal', stepNumber: 8, maxLines: 80, strategy: 'most-recent' },
      ccDailyLog: { dir: '~/.ldm/agents/cc-mini/memory/daily', label: 'CC Daily Log', stepNumber: 9, maxLines: 60, strategy: 'daily-logs', days: ['today', 'yesterday'] },
      repoLocations: { path: '~/.claude/projects/-Users-lesa--openclaw/memory/repo-locations.md', label: 'repo-locations.md', stepNumber: 10, critical: true },
    },
  };
}

function processStep(key, step, dates, config) {
  // Reminder-only step (e.g. full history)
  if (step.reminder) {
    return { content: step.reminder, loaded: true, fileName: null, capped: false, stale: false };
  }

  const maxLines = resolveMaxLines(key, step);

  // Single file step
  if (step.path) {
    const resolved = resolvePath(step.path);
    const content = readFileSafe(step.path);
    if (!content) return { content: null, loaded: false, fileName: resolved, capped: false, stale: false };
    const { text, capped } = truncateTop(content, maxLines, resolved);
    return { content: text, loaded: true, fileName: resolved, capped, stale: false };
  }

  // Directory-based step
  if (step.dir) {
    if (step.strategy === 'most-recent') {
      const fileName = findMostRecent(step.dir);
      if (!fileName) return { content: null, loaded: false, fileName: resolvePath(step.dir), capped: false, stale: false };
      const fullPath = join(resolvePath(step.dir), fileName);
      const content = readFileSafe(fullPath);
      if (!content) return { content: null, loaded: false, fileName: fullPath, capped: false, stale: false };

      // Staleness cutoff: if the newest file is older than the cutoff, do not
      // inject its body. Emit a single line with the path and date instead.
      const stalenessDays = step.stalenessDays ?? config.stalenessDays ?? DEFAULT_STALENESS_DAYS;
      const fileDate = dateStrFromName(fileName);
      const age = fileDate ? ageInDays(fileDate, dates.today) : null;
      if (age != null && age > stalenessDays) {
        const line = `[stale: newest file is ${fileDate} (${age}d old, cutoff ${stalenessDays}d). Body not injected. Read if needed: ${fullPath}]`;
        return { content: line, loaded: true, fileName, capped: false, stale: true };
      }

      const { text, capped } = truncateTop(content, maxLines, fullPath);
      return { content: text, loaded: true, fileName, capped, stale: false };
    }

    if (step.strategy === 'daily-logs') {
      const dailyStalenessDays = step.dailyLogStalenessDays ?? config.dailyLogStalenessDays ?? DEFAULT_DAILY_LOG_STALENESS_DAYS;
      const parts = [];
      let anyLoaded = false;
      let anyCapped = false;
      let anyStale = false;
      for (const day of (step.days || ['today'])) {
        const dateStr = day === 'today' ? dates.today : dates.yesterday;
        const fileName = `${dateStr}.md`;
        const fullPath = join(resolvePath(step.dir), fileName);
        const content = readFileSafe(fullPath);
        if (!content) continue;
        anyLoaded = true;

        // Guard: a day file dated older than the cutoff should not normally
        // happen (days are today/yesterday), but if it does, emit path-only.
        const age = ageInDays(dateStr, dates.today);
        if (age != null && age > dailyStalenessDays) {
          parts.push(`--- ${day} (${dateStr}) ---\n[stale: ${age}d old, cutoff ${dailyStalenessDays}d. Body not injected. Read if needed: ${fullPath}]`);
          anyStale = true;
          continue;
        }

        const { text, capped } = truncateBottom(content, maxLines, fullPath);
        if (capped) anyCapped = true;
        parts.push(`--- ${day} (${dateStr}) ---\n${text}`);
      }
      if (!anyLoaded) return { content: null, loaded: false, fileName: resolvePath(step.dir), capped: false, stale: false };
      return { content: parts.join('\n\n'), loaded: true, fileName: null, capped: anyCapped, stale: anyStale };
    }
  }

  return { content: null, loaded: false, fileName: null, capped: false, stale: false };
}

async function main() {
  const startTime = Date.now();
  let raw = '';
  for await (const chunk of process.stdin) {
    raw += chunk;
  }

  let input;
  try {
    input = JSON.parse(raw);
  } catch {
    process.exit(0);
  }

  const config = loadConfig() || getDefaultConfig();
  const dates = getTodayAndYesterday(config.timezone || 'America/Los_Angeles');

  const sections = [];
  const loaded = [];
  const skipped = [];
  const cappedSteps = [];
  const staleSteps = [];
  let totalLines = 0;

  // Sort steps by stepNumber
  const stepEntries = Object.entries(config.steps).sort(
    ([, a], [, b]) => (a.stepNumber || 0) - (b.stepNumber || 0)
  );

  for (const [key, step] of stepEntries) {
    const result = processStep(key, step, dates, config);

    if (result.loaded && result.content) {
      const criticalTag = step.critical ? ' (CRITICAL)' : '';
      const fileTag = result.fileName ? `: ${result.fileName}` : '';
      const header = `== [Step ${step.stepNumber}] ${step.label}${criticalTag}${fileTag} ==`;
      sections.push(`${header}\n${result.content}`);
      loaded.push(`Step ${step.stepNumber}: ${step.label}`);
      totalLines += result.content.split('\n').length;
      if (result.capped) cappedSteps.push(`Step ${step.stepNumber}`);
      if (result.stale) staleSteps.push(`Step ${step.stepNumber}`);
    } else {
      skipped.push(`Step ${step.stepNumber}: ${step.label}`);
      if (result.fileName) {
        process.stderr.write(`${TAG} skipped step ${step.stepNumber}: ${result.fileName} not found\n`);
      }
    }

    // Safety cap
    if (totalLines > (config.maxTotalLines || 2000)) {
      process.stderr.write(`${TAG} hit line cap at ${totalLines} lines, stopping\n`);
      break;
    }
  }

  // ── Register session (fire-and-forget, Phase 2) ──
  try {
    const { registerSession } = await import('../../lib/sessions.mjs');
    const agentId = config?.agentId || 'unknown';
    const sessionName = process.env.LDM_SESSION_NAME || process.env.CLAUDE_SESSION_NAME || basename(input?.cwd || process.cwd()) || 'default';
    // Register with agent--session naming convention
    registerSession({
      name: `${agentId}--${sessionName}`,
      agentId,
      pid: process.ppid || process.pid,
      meta: { cwd: input?.cwd, sessionName },
    });
  } catch {}

  // ── Check pending messages (Phase 3: boot hook delivery) ──
  // Scans ~/.ldm/messages/ for messages addressed to this agent.
  // Supports targeting: "cc-mini", "cc-mini:session", "cc-mini:*", "*", "all".
  // Does NOT mark as read. The MCP check_inbox tool handles that.
  try {
    const { readMessages } = await import('../../lib/messages.mjs');
    const agentId = config?.agentId || 'cc-mini';
    const sessionName = process.env.LDM_SESSION_NAME || process.env.CLAUDE_SESSION_NAME || basename(input?.cwd || process.cwd()) || 'default';

    // Read messages using the existing lib/messages.mjs.
    // It filters by exact sessionName or "all" broadcast.
    // We also need to check for agent-level targeting (e.g. "cc-mini", "cc-mini:*").
    const directMessages = readMessages(sessionName, { markRead: false });
    const agentMessages = readMessages(agentId, { markRead: false });
    const agentSessionMessages = readMessages(`${agentId}:${sessionName}`, { markRead: false });
    const agentBroadcast = readMessages(`${agentId}:*`, { markRead: false });
    const globalBroadcast = readMessages('*', { markRead: false });

    // Deduplicate by message ID
    const seen = new Set();
    const allPending = [];
    for (const msg of [...directMessages, ...agentMessages, ...agentSessionMessages, ...agentBroadcast, ...globalBroadcast]) {
      if (msg.id && seen.has(msg.id)) continue;
      if (msg.id) seen.add(msg.id);
      allPending.push(msg);
    }

    // Sort by timestamp
    allPending.sort((a, b) => (a.timestamp || '').localeCompare(b.timestamp || ''));

    if (allPending.length > 0) {
      const msgLines = allPending.map(m => `  [${m.type || 'chat'}] from ${m.from}: ${m.body}`).join('\n');
      sections.push(`== Pending Messages (${allPending.length}) ==\nYou have ${allPending.length} pending message(s). Use check_inbox to read and acknowledge them.\n${msgLines}`);
    }
  } catch {}

  // ── Check for updates ──
  try {
    const { readUpdateManifest } = await import('../../lib/updates.mjs');
    const manifest = readUpdateManifest();
    if (manifest?.updatesAvailable > 0) {
      const updateLines = manifest.updates
        .map(u => `  ${u.name}: ${u.currentVersion} -> ${u.latestVersion}`)
        .join('\n');
      sections.push(`== Updates Available (${manifest.updatesAvailable}) ==\n${updateLines}\nRun: ldm install`);
    }
  } catch {}

  const elapsed = Date.now() - startTime;
  const footer = `== Boot complete. Loaded ${loaded.length} sections in ${elapsed}ms. ==`;
  if (skipped.length > 0) {
    sections.push(`${footer}\nSkipped: ${skipped.join(', ')}`);
  } else {
    sections.push(footer);
  }

  // Body first, then a one-line payload summary so future slowness triage is
  // trivial: total bytes/lines injected, which steps were line-capped, and
  // which were skipped as stale (path-only).
  const bodyText =
    `== LDM OS BOOT SEQUENCE (loaded automatically by SessionStart hook) ==\n\n` +
    sections.join('\n\n');
  const payloadBytes = Buffer.byteLength(bodyText, 'utf-8');
  const payloadLines = bodyText.split('\n').length;
  const summary =
    `== Boot payload: ${payloadBytes} bytes, ${payloadLines} lines, ${loaded.length} sections. ` +
    `Capped: ${cappedSteps.length ? cappedSteps.join(', ') : 'none'}. ` +
    `Stale/path-only: ${staleSteps.length ? staleSteps.join(', ') : 'none'}. ` +
    `Missing: ${skipped.length ? skipped.length : 'none'}. ==`;

  const additionalContext = `${bodyText}\n\n${summary}`;

  const output = {
    hookSpecificOutput: {
      hookEventName: 'SessionStart',
      additionalContext,
    },
  };

  process.stdout.write(JSON.stringify(output));
  process.stderr.write(`${TAG} loaded ${loaded.length} sections, ${payloadBytes} bytes in ${elapsed}ms\n`);
  process.exit(0);
}

main().catch((err) => {
  process.stderr.write(`${TAG} fatal: ${err.message}\n`);
  process.exit(0);
});
