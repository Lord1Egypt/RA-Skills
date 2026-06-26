#!/usr/bin/env node
// poll-and-deliver.js — OpenClaw adapter for shark-exec
// For other runtimes, implement equivalent polling logic using your platform's APIs.
// See shark-exec/SKILL.md "Runtime Adapters" for Claude Code, Codex, Cursor equivalents.

/**
 * shark-exec: poll-and-deliver.js
 *
 * Helper script that reads state/pending.json and prints a summary of
 * all pending background jobs — their age, status, and whether they're
 * past their maxSeconds threshold.
 *
 * This script does NOT poll the actual process or send messages.
 * That work is done by the cron agentTurn. This is purely diagnostic.
 *
 * Usage:
 *   node C:\Users\Admin\clawd\skills\shark-exec\scripts\poll-and-deliver.js
 *   node poll-and-deliver.js [--json]
 */

const fs = require('fs');
const path = require('path');

const STATE_FILE = path.join(__dirname, '..', 'state', 'pending.json');

function formatDuration(ms) {
  const s = Math.floor(ms / 1000);
  if (s < 60) return `${s}s`;
  const m = Math.floor(s / 60);
  const rem = s % 60;
  return `${m}m ${rem}s`;
}

function main() {
  const jsonMode = process.argv.includes('--json');
  const now = Date.now();

  // Read state file
  let state;
  try {
    if (!fs.existsSync(STATE_FILE)) {
      if (jsonMode) {
        console.log(JSON.stringify({ jobs: [], summary: 'No pending.json found' }));
      } else {
        console.log('📭 No pending.json found — no background jobs have been registered.');
      }
      process.exit(0);
    }

    const raw = fs.readFileSync(STATE_FILE, 'utf8');
    state = JSON.parse(raw);
  } catch (err) {
    if (jsonMode) {
      console.log(JSON.stringify({ error: `Failed to read pending.json: ${err.message}` }));
    } else {
      console.error(`❌ Failed to read pending.json: ${err.message}`);
    }
    process.exit(1);
  }

  const jobs = state.jobs || [];

  if (jobs.length === 0) {
    if (jsonMode) {
      console.log(JSON.stringify({ jobs: [], summary: 'No pending jobs' }));
    } else {
      console.log('✅ No pending background jobs.');
    }
    process.exit(0);
  }

  if (jsonMode) {
    const enriched = jobs.map(job => {
      const ageMs = now - job.startedAt;
      const maxMs = job.maxSeconds * 1000;
      return {
        ...job,
        ageMs,
        ageFormatted: formatDuration(ageMs),
        overdue: ageMs > maxMs,
        overdueBy: ageMs > maxMs ? formatDuration(ageMs - maxMs) : null,
      };
    });
    console.log(JSON.stringify({ jobs: enriched, count: enriched.length }, null, 2));
    process.exit(0);
  }

  // Human-readable output
  console.log(`🦈 shark-exec pending jobs: ${jobs.length}\n`);
  console.log('─'.repeat(60));

  for (const job of jobs) {
    const ageMs = now - job.startedAt;
    const maxMs = job.maxSeconds * 1000;
    const overdue = ageMs > maxMs;

    const statusIcon = overdue ? '⚠️ OVERDUE' : '⏳ running';
    const overdueNote = overdue
      ? ` (${formatDuration(ageMs - maxMs)} past limit)`
      : ` (${formatDuration(maxMs - ageMs)} remaining)`;

    console.log(`\n${statusIcon}  ${job.label}`);
    console.log(`  sessionId : ${job.sessionId}`);
    console.log(`  command   : ${job.command}`);
    console.log(`  started   : ${new Date(job.startedAt).toISOString()}`);
    console.log(`  age       : ${formatDuration(ageMs)}`);
    console.log(`  maxSeconds: ${job.maxSeconds}s${overdueNote}`);
    console.log(`  cronJobId : ${job.cronJobId || '(not yet set)'}`);
  }

  console.log('\n' + '─'.repeat(60));
  console.log('\nNote: This script is read-only. The cron agentTurn handles');
  console.log('actual polling, result delivery, and cleanup.');

  if (jobs.some(j => now - j.startedAt > j.maxSeconds * 1000)) {
    console.log('\n⚠️  Some jobs are overdue. The next cron tick should kill them.');
    console.log('   If the cron is not running, check the cronJobId and verify');
    console.log('   the job exists via the OpenClaw cron API.');
  }
}

main();
