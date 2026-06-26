"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const prefs_1 = require("../notifications/prefs");
function printJson(value) {
    console.log(JSON.stringify(value, null, 2));
}
function coerceValue(raw) {
    if (raw === 'true')
        return true;
    if (raw === 'false')
        return false;
    const n = Number(raw);
    if (!Number.isNaN(n) && raw.trim() !== '')
        return n;
    return raw;
}
function main() {
    const args = process.argv.slice(2);
    if (args.length < 2) {
        printJson({
            ok: false,
            error: {
                code: 'MISSING_ARGS',
                message: 'Usage: notifications:set <dotPath> <value>   e.g. dailyBrief.time 09:00',
            },
            safety: { externalWrite: false },
        });
        process.exit(1);
    }
    const [dotPath, rawValue] = args;
    const value = coerceValue(rawValue);
    const prefs = (0, prefs_1.loadPrefs)();
    (0, prefs_1.setDotPath)(prefs, dotPath, value);
    (0, prefs_1.savePrefs)(prefs);
    printJson({
        ok: true,
        set: { [dotPath]: value },
        safety: { externalWrite: false },
    });
}
main();
//# sourceMappingURL=notificationsSet.js.map