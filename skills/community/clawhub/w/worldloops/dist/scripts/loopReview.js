"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const openLoopStates_1 = require("../storage/openLoopStates");
const capabilityBoundary_1 = require("../policy/capabilityBoundary");
const ALL_STATUSES = ['todo', 'doing', 'done', 'snoozed', 'escalated'];
const HIGH_SEVERITIES = ['high', 'critical'];
function main() {
    const args = process.argv.slice(2);
    const jsonMode = args.includes('--json');
    const loops = (0, openLoopStates_1.loadOpenLoopStates)();
    const byStatus = {
        todo: 0,
        doing: 0,
        done: 0,
        snoozed: 0,
        escalated: 0,
    };
    for (const loop of loops) {
        byStatus[loop.status]++;
    }
    const highSeverityLoops = loops.filter((l) => HIGH_SEVERITIES.includes(l.severity) && l.status !== 'done');
    const activeCandidates = loops.filter((l) => (l.status === 'doing' || l.status === 'todo') && HIGH_SEVERITIES.includes(l.severity));
    const suggestedFocus = activeCandidates.length > 0 ? activeCandidates[0] : null;
    if (jsonMode) {
        console.log(JSON.stringify({
            ok: true,
            source: 'worldloops.local',
            review: {
                total: loops.length,
                byStatus,
                highSeverityLoops: highSeverityLoops.map((l) => ({
                    id: l.id,
                    status: l.status,
                    severity: l.severity,
                    title: l.title,
                })),
                suggestedFocus: suggestedFocus
                    ? {
                        id: suggestedFocus.id,
                        status: suggestedFocus.status,
                        severity: suggestedFocus.severity,
                        title: suggestedFocus.title,
                    }
                    : null,
            },
            capabilityBoundary: (0, capabilityBoundary_1.getCapabilityBoundary)(),
            safety: { externalWrite: false },
        }, null, 2));
        return;
    }
    console.log('Loop Lifecycle Review');
    console.log('');
    console.log(`Total loops: ${loops.length}`);
    if (loops.length === 0) {
        console.log('');
        console.log('No open loops found.');
        console.log('');
        console.log('externalWrite: false');
        return;
    }
    console.log('');
    console.log('By status:');
    for (const status of ALL_STATUSES) {
        console.log(`  ${status.padEnd(10)} ${byStatus[status]}`);
    }
    console.log('');
    if (highSeverityLoops.length === 0) {
        console.log('High severity loops: none');
    }
    else {
        console.log('High severity loops:');
        for (const l of highSeverityLoops) {
            console.log(`  [${l.status}] ${l.id} — ${l.title} (${l.severity})`);
        }
    }
    console.log('');
    if (suggestedFocus) {
        console.log('Suggested focus:');
        console.log(`  [${suggestedFocus.status}] ${suggestedFocus.id} — ${suggestedFocus.title} (${suggestedFocus.severity})`);
        console.log(`  Inspect: npm run loop:show -- ${suggestedFocus.id}`);
    }
    else {
        console.log('Suggested focus: none (no high-severity active loops)');
    }
    console.log('');
    console.log('externalWrite: false');
}
main();
//# sourceMappingURL=loopReview.js.map