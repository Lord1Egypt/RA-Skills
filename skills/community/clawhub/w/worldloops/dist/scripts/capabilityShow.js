"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const capabilityBoundary_1 = require("../policy/capabilityBoundary");
function main() {
    console.log(JSON.stringify({
        ok: true,
        source: 'worldloops.local',
        capabilityBoundary: (0, capabilityBoundary_1.getCapabilityBoundary)(),
        safety: { externalWrite: false },
    }, null, 2));
}
main();
//# sourceMappingURL=capabilityShow.js.map