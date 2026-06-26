"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
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
function isValidTime(value) {
    return /^\d{1,2}:\d{2}$/.test(value);
}
function main() {
    const time = getFlagValue('--time');
    const channel = getFlagValue('--channel');
    const timezone = getFlagValue('--timezone');
    const sources = getFlagValue('--sources');
    const enabled = hasFlag('--enabled') ? true : hasFlag('--disabled') ? false : undefined;
    const prefs = (0, prefs_1.loadPrefs)();
    const changes = {};
    if (time !== undefined) {
        if (!isValidTime(time)) {
            console.log('❌ Invalid --time value. Use HH:MM format (e.g. 09:00, 08:30).');
            console.log('');
            console.log('externalWrite:false');
            process.exit(1);
        }
        prefs.dailyBrief.time = time;
        changes.time = time;
    }
    if (channel !== undefined) {
        const validList = prefs_1.VALID_CHANNELS;
        if (!validList.includes(channel)) {
            console.log(`❌ Unknown delivery channel: "${channel}".`);
            console.log(`Supported channels: ${prefs_1.VALID_CHANNELS.join(', ')}`);
            console.log('');
            console.log('externalWrite:false');
            process.exit(1);
        }
        prefs.dailyBrief.channel = channel;
        changes.channel = channel;
    }
    if (timezone !== undefined) {
        prefs.dailyBrief.timezone = timezone;
        changes.timezone = timezone;
    }
    if (sources !== undefined) {
        prefs.dailyBrief.sources = sources.split(',').map(s => s.trim()).filter(Boolean);
        changes.sources = prefs.dailyBrief.sources;
    }
    if (enabled !== undefined) {
        prefs.dailyBrief.enabled = enabled;
        changes.enabled = enabled;
    }
    if (Object.keys(changes).length === 0) {
        console.log('No changes. Pass --time HH:MM, --channel <name>, --timezone <tz>, or --sources <list>.');
        console.log('');
        console.log('externalWrite:false');
        return;
    }
    (0, prefs_1.savePrefs)(prefs);
    console.log('🦞 Daily Brief Preferences updated');
    console.log('');
    for (const [key, value] of Object.entries(changes)) {
        const display = Array.isArray(value) ? value.join(', ') : String(value);
        console.log(`  ${key}: ${display}`);
    }
    console.log('');
    console.log('Run "npm run brief:preferences" to see all settings.');
    console.log('');
    console.log('externalWrite:false');
}
main();
//# sourceMappingURL=briefPreferencesSet.js.map