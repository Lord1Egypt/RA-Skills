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
    const details = hasFlag('--details');
    const prefs = (0, prefs_1.loadPrefs)();
    const scheduleTime = prefs.dailyBrief.time ?? '09:00';
    const timezone = prefs.dailyBrief.timezone ?? 'UTC';
    const timezoneDisplay = timezone === 'UTC' ? 'local time' : timezone;
    const channel = prefs.dailyBrief.channel ?? prefs_1.DEFAULT_BRIEF_CHANNEL;
    console.log('🦞 Agent Execution Guard Daily Brief');
    console.log('');
    const results = await (0, dailyBriefRunner_1.processAllSources)(inboxDir, details);
    const lines = (0, dailyBriefRunner_1.buildBriefLines)(results);
    for (const line of lines) {
        console.log(line);
    }
    const hasPayloads = results.some(r => r.found);
    console.log('');
    console.log('✅ Safe');
    console.log('externalWrite:false');
    if (hasPayloads) {
        console.log('No email, draft, calendar event, Slack message, or external change made.');
    }
    else {
        console.log('No external system changed.');
    }
    console.log('');
    console.log(`Daily Brief schedule: ${scheduleTime} ${timezoneDisplay} — Delivery channel: ${channel}`);
    console.log('To change: npm run brief:preferences:set -- --time HH:MM');
}
main().catch((err) => {
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
//# sourceMappingURL=guardDaily.js.map