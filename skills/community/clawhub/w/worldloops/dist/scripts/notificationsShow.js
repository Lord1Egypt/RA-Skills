"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const prefs_1 = require("../notifications/prefs");
function printJson(value) {
    console.log(JSON.stringify(value, null, 2));
}
function main() {
    const prefs = (0, prefs_1.loadPrefs)();
    printJson({
        ok: true,
        path: (0, prefs_1.getPrefsPath)(),
        prefs,
        safety: { externalWrite: false },
    });
}
main();
//# sourceMappingURL=notificationsShow.js.map