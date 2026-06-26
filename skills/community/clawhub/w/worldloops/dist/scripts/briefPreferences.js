"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const prefs_1 = require("../notifications/prefs");
function main() {
    const prefs = (0, prefs_1.loadPrefs)();
    const db = prefs.dailyBrief;
    const time = db.time ?? '09:00';
    const timezone = db.timezone ?? 'UTC';
    const timezoneDisplay = timezone === 'UTC' ? 'local time' : timezone;
    const channel = db.channel ?? prefs_1.DEFAULT_BRIEF_CHANNEL;
    const minSeverity = db.minimumSeverity ?? 'medium';
    const sources = (db.sources ?? ['gmail', 'calendar', 'slack']).join(', ');
    const status = db.enabled ? 'enabled' : 'disabled';
    console.log('🦞 Daily Brief Preferences');
    console.log('');
    console.log(`Schedule:        ${time} ${timezoneDisplay}`);
    console.log(`Delivery channel: ${channel}`);
    console.log(`Min severity:    ${minSeverity}`);
    console.log(`Sources:         ${sources}`);
    console.log(`Status:          ${status}`);
    console.log('');
    console.log('To change:');
    console.log('  npm run brief:preferences:set -- --time 08:30');
    console.log('  npm run brief:preferences:set -- --channel telegram');
    console.log('  npm run brief:preferences:set -- --channel local');
    console.log('  npm run brief:preferences:set -- --channel slack');
    console.log('');
    console.log('Delivery note:');
    console.log('  Actual delivery requires a host scheduler (e.g. OpenClaw).');
    console.log('  WorldLoops does not install cron, launchd, or background daemons.');
    console.log('  Run: npm run brief:deliver');
    console.log('');
    console.log(`Preferences file: ${(0, prefs_1.getPrefsPath)()}`);
    console.log('');
    console.log('externalWrite:false');
}
main();
//# sourceMappingURL=briefPreferences.js.map