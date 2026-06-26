"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const prefs_1 = require("../notifications/prefs");
function printJson(value) {
    console.log(JSON.stringify(value, null, 2));
}
function main() {
    const created = (0, prefs_1.initPrefs)();
    printJson({
        ok: true,
        created,
        path: (0, prefs_1.getPrefsPath)(),
        message: created
            ? 'Created default notification_prefs.json'
            : 'notification_prefs.json already exists — no changes made',
        safety: { externalWrite: false },
    });
}
main();
//# sourceMappingURL=notificationsInit.js.map