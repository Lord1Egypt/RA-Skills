"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const openLoopStates_1 = require("../storage/openLoopStates");
const stuckLoopPolicy_1 = require("../policy/stuckLoopPolicy");
const capabilityBoundary_1 = require("../policy/capabilityBoundary");
function printJson(value) {
    console.log(JSON.stringify(value, null, 2));
}
function main() {
    const nowIso = new Date().toISOString();
    const loops = (0, openLoopStates_1.loadOpenLoopStates)();
    const transitions = [];
    for (const loop of loops) {
        const evaluation = (0, stuckLoopPolicy_1.evaluateStuckLoop)(loop, nowIso);
        if (!evaluation.shouldTransition) {
            continue;
        }
        const updated = (0, openLoopStates_1.transitionOpenLoopState)(loop.id, evaluation.to, {
            actor: 'worldloops.local',
            note: evaluation.note,
        });
        transitions.push({
            id: loop.id,
            canonicalKey: loop.canonicalKey,
            from: evaluation.from,
            to: evaluation.to,
            reason: evaluation.reason,
            note: evaluation.note,
            updatedAt: updated.updatedAt,
        });
    }
    printJson({
        ok: true,
        source: 'worldloops.local',
        checkedAt: nowIso,
        policy: (0, stuckLoopPolicy_1.getDefaultStuckLoopPolicyConfig)(),
        loopsChecked: loops.length,
        transitionsApplied: transitions.length,
        transitions,
        capabilityBoundary: (0, capabilityBoundary_1.getCapabilityBoundary)(),
        safety: { externalWrite: false },
    });
}
main();
//# sourceMappingURL=loopReconcile.js.map