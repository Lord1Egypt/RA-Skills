import { processAllSources, buildBriefLines, DEFAULT_INBOX_DIR } from '../dailyBriefRunner';
import { loadPrefs, VALID_CHANNELS, DEFAULT_BRIEF_CHANNEL } from '../notifications/prefs';

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
  const isDryRun = hasFlag('--dry-run');
  const channelFlag = getFlagValue('--channel');

  const prefs = loadPrefs();
  const channel = channelFlag ?? prefs.dailyBrief.channel ?? DEFAULT_BRIEF_CHANNEL;

  if (channelFlag) {
    const validList = (VALID_CHANNELS as readonly string[]);
    if (!validList.includes(channelFlag)) {
      console.log(`❌ Unknown delivery channel: "${channelFlag}".`);
      console.log(`Supported channels: ${VALID_CHANNELS.join(', ')}`);
      console.log('');
      console.log('sourceExternalWrite:false');
      console.log('No Gmail, Calendar, or Slack system modified.');
      process.exit(1);
    }
  }

  console.log('🦞 Agent Execution Guard Daily Brief');
  console.log('');

  const results = await processAllSources(inboxDir);
  const lines = buildBriefLines(results);
  for (const line of lines) {
    console.log(line);
  }

  console.log('');

  if (isDryRun) {
    console.log('Delivery mode: dry-run');
    console.log('sourceExternalWrite:false');
    console.log('No Gmail, Calendar, or Slack system modified.');
    return;
  }

  if (channel === 'local') {
    console.log('Delivery channel: local');
    console.log('Delivery mode: local output');
    console.log('sourceExternalWrite:false');
    console.log('No Gmail, Calendar, or Slack system modified.');
    return;
  }

  // Remote delivery channels — no integration active in this runtime
  const channelLabel = channel.charAt(0).toUpperCase() + channel.slice(1);
  console.log(`Delivery channel: ${channel}`);
  console.log(`Delivery mode: delivery-ready`);
  console.log(`Delivery-ready: ${channelLabel} delivery is not active in this runtime.`);
  console.log('To enable delivery, configure a host scheduler (e.g. OpenClaw) to call this command.');
  console.log('');
  console.log('sourceExternalWrite:false');
  console.log('No Gmail, Calendar, or Slack system modified.');
}

main().catch((err: unknown) => {
  console.log('🦞 Agent Execution Guard Daily Brief');
  console.log('');
  console.log('❌ Brief deliver failed');
  console.log(err instanceof Error ? err.message : String(err));
  console.log('');
  console.log('sourceExternalWrite:false');
  console.log('No Gmail, Calendar, or Slack system modified.');
  process.exit(1);
});
