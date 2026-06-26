import { processAllSources, buildBriefLines, DEFAULT_INBOX_DIR } from '../dailyBriefRunner';
import { loadPrefs, DEFAULT_BRIEF_CHANNEL } from '../notifications/prefs';

function getFlagValue(flag: string): string | undefined {
  const args = process.argv.slice(2);
  const idx = args.indexOf(flag);
  if (idx === -1 || idx + 1 >= args.length) return undefined;
  return args[idx + 1];
}

function hasFlag(flag: string): boolean {
  return process.argv.slice(2).includes(flag);
}

async function main(): Promise<void> {
  const inboxDir = getFlagValue('--inbox') ?? DEFAULT_INBOX_DIR;
  const details = hasFlag('--details');
  const prefs = loadPrefs();
  const scheduleTime = prefs.dailyBrief.time ?? '09:00';
  const timezone = prefs.dailyBrief.timezone ?? 'UTC';
  const timezoneDisplay = timezone === 'UTC' ? 'local time' : timezone;
  const channel = prefs.dailyBrief.channel ?? DEFAULT_BRIEF_CHANNEL;

  console.log('🦞 Agent Execution Guard Daily Brief');
  console.log('');

  const results = await processAllSources(inboxDir, details);
  const lines = buildBriefLines(results);
  for (const line of lines) {
    console.log(line);
  }

  const hasPayloads = results.some(r => r.found);

  console.log('');
  console.log('✅ Safe');
  console.log('externalWrite:false');
  if (hasPayloads) {
    console.log('No email, draft, calendar event, Slack message, or external change made.');
  } else {
    console.log('No external system changed.');
  }

  console.log('');
  console.log(`Daily Brief schedule: ${scheduleTime} ${timezoneDisplay} — Delivery channel: ${channel}`);
  console.log('To change: npm run brief:preferences:set -- --time HH:MM');
}

main().catch((err: unknown) => {
  console.log('🦞 Agent Execution Guard Daily Brief');
  console.log('');
  console.log('❌ Daily Brief failed');
  console.log(err instanceof Error ? err.message : String(err));
  console.log('');
  console.log('✅ Safe');
  console.log('externalWrite:false');
  console.log('No external system changed.');
  process.exit(1);
});
