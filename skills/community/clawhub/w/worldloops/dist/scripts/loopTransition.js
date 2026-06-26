"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const openLoopStates_1 = require("../storage/openLoopStates");
const capabilityBoundary_1 = require("../policy/capabilityBoundary");
const VALID_STATUSES = ['todo', 'doing', 'done', 'snoozed', 'escalated'];
const ALLOWED_TRANSITIONS = {
    todo: ['doing'],
    doing: ['done', 'snoozed', 'escalated'],
    snoozed: ['todo'],
    escalated: ['doing'],
    done: [],
};
function printJson(value) {
    console.log(JSON.stringify(value, null, 2));
}
function main() {
    const args = process.argv.slice(2);
    const id = args[0];
    if (!id) {
        console.error('Usage: npm run loop:transition -- <loopId> <status> [note]');
        console.error('       npm run loop:transition -- <loopId> --to <status> [--dry-run]');
        process.exit(1);
    }
    const dryRun = args.includes('--dry-run');
    const toFlagIndex = args.indexOf('--to');
    let targetStatus;
    let note = null;
    if (toFlagIndex !== -1) {
        targetStatus = args[toFlagIndex + 1] ?? '';
        note = null;
    }
    else {
        targetStatus = args[1] ?? '';
        const noteParts = args.slice(2).filter((a) => a !== '--dry-run');
        note = noteParts.length > 0 ? noteParts.join(' ') : null;
    }
    if (!targetStatus || !VALID_STATUSES.includes(targetStatus)) {
        console.error(`Invalid status: ${targetStatus}`);
        console.error(`Valid statuses: ${VALID_STATUSES.join(', ')}`);
        process.exit(1);
    }
    const to = targetStatus;
    const loop = (0, openLoopStates_1.findOpenLoopStateById)(id);
    if (!loop) {
        printJson({
            ok: false,
            error: {
                code: 'LOOP_NOT_FOUND',
                message: `Open loop not found: ${id}`,
            },
            safety: { externalWrite: false },
        });
        process.exit(1);
    }
    const allowed = ALLOWED_TRANSITIONS[loop.status];
    if (!allowed.includes(to)) {
        printJson({
            ok: false,
            error: {
                code: 'INVALID_LOOP_TRANSITION',
                message: `Cannot transition from '${loop.status}' to '${to}'.`,
                allowedTransitions: allowed,
            },
            currentStatus: loop.status,
            capabilityBoundary: (0, capabilityBoundary_1.getCapabilityBoundary)(),
            safety: { externalWrite: false },
        });
        process.exit(1);
    }
    if (dryRun) {
        printJson({
            ok: true,
            dryRun: true,
            source: 'worldloops.local',
            preview: {
                id: loop.id,
                from: loop.status,
                to,
                note,
            },
            capabilityBoundary: (0, capabilityBoundary_1.getCapabilityBoundary)(),
            safety: { externalWrite: false },
        });
        return;
    }
    const updated = (0, openLoopStates_1.transitionOpenLoopState)(id, to, {
        actor: 'worldloops.local',
        note,
    });
    printJson({
        ok: true,
        source: 'worldloops.local',
        loop: updated,
        capabilityBoundary: (0, capabilityBoundary_1.getCapabilityBoundary)(),
        safety: { externalWrite: false },
    });
}
main();
//# sourceMappingURL=loopTransition.js.map