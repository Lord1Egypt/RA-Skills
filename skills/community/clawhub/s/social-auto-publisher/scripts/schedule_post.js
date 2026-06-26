#!/usr/bin/env node
/**
 * Scheduled Publishing Scheduler
 * Creates a publishing task at a specified time (via cron mechanism)
 *
 * Usage:
 *   node scripts/schedule_post.js --content-file ./output/post.json --schedule "2026-05-05 20:00" --platforms "xiaohongshu,weibo"
 */

const path = require('path');
const fs = require('fs');

function parseArgs() {
  const args = process.argv.slice(2);
  const opts = {};
  for (let i = 0; i < args.length; i++) {
    if (args[i].startsWith('--')) {
      const key = args[i].replace(/^--/, '');
      const val = args[i + 1] && !args[i + 1].startsWith('--') ? args[i + 1] : 'true';
      opts[key] = val;
      if (val !== 'true') i++;
    }
  }
  return opts;
}

function parseSchedule(scheduleStr) {
  // Supported formats: "2026-05-05 20:00" or "tomorrow 20:00" or "in 2h"
  if (scheduleStr.startsWith('in ')) {
    const match = scheduleStr.match(/^in (\d+)([hmd])$/);
    if (match) {
      const num = parseInt(match[1]);
      const unit = match[2];
      const now = new Date();
      switch (unit) {
        case 'h': now.setHours(now.getHours() + num); break;
        case 'm': now.setMinutes(now.getMinutes() + num); break;
        case 'd': now.setDate(now.getDate() + num); break;
      }
      return now;
    }
  }

  if (scheduleStr.startsWith('tomorrow')) {
    const time = scheduleStr.replace('tomorrow', '').trim();
    const [h, m] = (time || '09:00').split(':').map(Number);
    const d = new Date();
    d.setDate(d.getDate() + 1);
    d.setHours(h, m, 0, 0);
    return d;
  }

  // ISO / "YYYY-MM-DD HH:mm"
  return new Date(scheduleStr.replace(' ', 'T') + ':00');
}

function buildCronJob(contentFile, schedule, platforms) {
  const publishScript = path.join(__dirname, 'publish.js');
  const ts = schedule instanceof Date ? schedule.toISOString() : schedule;

  return {
    name: `social-post-${Date.now()}`,
    schedule: {
      kind: 'at',
      at: ts,
    },
    payload: {
      kind: 'agentTurn',
      message: `Execute social media publishing task:
- Platforms: ${platforms}
- Content file: ${contentFile}
- Command: node ${publishScript} --platforms "${platforms}" --content-file "${contentFile}"

Please execute node ${publishScript} --platforms "${platforms}" --content-file "${contentFile}"`,
    },
    delivery: { mode: 'announce' },
    deleteAfterRun: true,
    enabled: true,
  };
}

function main() {
  const opts = parseArgs();

  if (!opts['content-file'] || !opts.schedule) {
    console.error('Usage: node schedule_post.js --content-file <path> --schedule "YYYY-MM-DD HH:mm" --platforms "xiaohongshu"');
    process.exit(1);
  }

  const contentFile = path.resolve(opts['content-file']);
  if (!fs.existsSync(contentFile)) {
    console.error(`[error] File does not exist: ${contentFile}`);
    process.exit(1);
  }

  const scheduledTime = parseSchedule(opts.schedule);
  if (isNaN(scheduledTime.getTime())) {
    console.error(`[error] Invalid time format: ${opts.schedule}`);
    console.error('  Supported: "2026-05-05 20:00" / "tomorrow 09:00" / "in 2h"');
    process.exit(1);
  }

  const platforms = opts.platforms || 'xiaohongshu';

  const job = buildCronJob(contentFile, scheduledTime, platforms);

  console.log('─── Scheduled Publishing Task ───');
  console.log(`Platform(s): ${platforms}`);
  console.log(`Time: ${scheduledTime.toLocaleString('en-US', { timeZone: 'Asia/Shanghai' })}`);
  console.log(`Content: ${contentFile}`);
  console.log('');
  console.log('Cron Job Configuration (for use with OpenClaw cron):');
  console.log(JSON.stringify(job, null, 2));

  // Output the execution command (for use by AI or cron)
  console.log('');
  console.log('Command to execute at the scheduled time:');
  console.log(`node ${path.join(__dirname, 'publish.js')} --platforms "${platforms}" --content-file "${contentFile}"`);
}

main();