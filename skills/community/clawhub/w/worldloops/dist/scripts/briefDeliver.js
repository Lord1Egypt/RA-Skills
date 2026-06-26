"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const dailyBriefRunner_1 = require("../dailyBriefRunner");
const prefs_1 = require("../notifications/prefs");
function getFlagValue(flag) {
    const args = process.argv.slice(2);
    const idx = args.indexOf(flag);
    if (idx === -1 || idx + 1 >= args.length)
        return undefined;
    return args[idx + 1];
}
function hasFlag(flag) {
    return process.argv.slice(2).includes(flag);
}
async function main() {
    const inboxDir = getFlagValue('--inbox') ?? dailyBriefRunner_1.DEFAULT_INBOX_DIR;
    const isDryRun = hasFlag('--dry-run');
    const channelFlag = getFlagValue('--channel');
    const prefs = (0, prefs_1.loadPrefs)();
    const channel = channelFlag ?? prefs.dailyBrief.channel ?? prefs_1.DEFAULT_BRIEF_CHANNEL;
    if (channelFlag) {
        const validList = prefs_1.VALID_CHANNELS;
        if (!validList.includes(channelFlag)) {
            console.log(`❌ Unknown delivery channel: "${channelFlag}".`);
            console.log(`Supported channels: ${prefs_1.VALID_CHANNELS.join(', ')}`);
            console.log('');
            console.log('sourceExternalWrite:false');
            console.log('No Gmail, Calendar, or Slack system modified.');
            process.exit(1);
        }
    }
    console.log('🦞 Agent Execution Guard Daily Brief');
    console.log('');
    const results = await (0, dailyBriefRunner_1.processAllSources)(inboxDir);
    const lines = (0, dailyBriefRunner_1.buildBriefLines)(results);
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
main().catch((err) => {
    console.log('🦞 Agent Execution Guard Daily Brief');
    console.log('');
    console.log('❌ Brief deliver failed');
    console.log(err instanceof Error ? err.message : String(err));
    console.log('');
    console.log('sourceExternalWrite:false');
    console.log('No Gmail, Calendar, or Slack system modified.');
    process.exit(1);
});
//# sourceMappingURL=briefDeliver.js.map