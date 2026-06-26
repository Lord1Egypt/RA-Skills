"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const openclawIntake_1 = require("../openclawIntake");
function parseArgs() {
    const args = process.argv.slice(2);
    const result = {};
    for (let i = 0; i < args.length; i++) {
        if (args[i] === '--input' && args[i + 1]) {
            result.input = args[++i];
        }
    }
    return result;
}
function main() {
    const { input } = parseArgs();
    if (!input) {
        process.stderr.write('Error: --input is required\n');
        process.stderr.write('Usage: npm run openclaw:intake -- --input scripts/fixtures/openclaw-signal-intake/mixed-observations.json\n');
        process.exit(1);
    }
    let observations;
    try {
        observations = (0, openclawIntake_1.loadObservations)(input);
    }
    catch (err) {
        process.stderr.write(`Error loading observations from ${input}: ${String(err)}\n`);
        process.exit(1);
    }
    const summary = (0, openclawIntake_1.runIntake)(observations);
    console.log(`OpenClaw observed ${summary.total} candidate signals.`);
    console.log('');
    console.log('WorldLoops adjudication:');
    console.log(`- ${summary.accepted} accepted as new open loops`);
    if (summary.state_transition > 0) {
        console.log(`- ${summary.state_transition} state transition${summary.state_transition > 1 ? 's' : ''} applied`);
    }
    console.log(`- ${summary.suppressed} suppressed as noise / no-action / promotional`);
    console.log(`- ${summary.attached_context} attached as related context`);
    console.log(`- ${summary.needs_review} needs review`);
    const acceptedResults = summary.results.filter(r => r.verdict === 'accepted');
    if (acceptedResults.length > 0) {
        console.log('');
        console.log('Open loops created:');
        for (const r of acceptedResults) {
            const transition = summary.results.find(t => t.verdict === 'state_transition' &&
                t.stateTransition?.canonicalKey === `openclaw-${r.observation.source}-${r.observation.sourceId}` &&
                t.stateTransition.transitionApplied);
            if (transition?.stateTransition) {
                const label = transition.stateTransition.note;
                console.log(`- ${r.openLoopTitle} (${label})`);
            }
            else {
                console.log(`- ${r.openLoopTitle}`);
            }
        }
    }
    if (summary.morningBriefLines.length > 0) {
        console.log('');
        console.log('Morning Brief:');
        for (const line of summary.morningBriefLines) {
            console.log(line);
        }
    }
    console.log('');
    console.log('externalWrite:false');
}
main();
//# sourceMappingURL=openclawIntake.js.map