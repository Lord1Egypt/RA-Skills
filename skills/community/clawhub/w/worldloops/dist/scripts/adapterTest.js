"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const runAdapterTest_1 = require("../adapter/runAdapterTest");
const args = process.argv.slice(2);
const filePath = args.find((a) => !a.startsWith('--'));
const jsonMode = args.includes('--json');
function printJson(value) {
    console.log(JSON.stringify(value, null, 2));
}
function didPass(result) {
    return (result.validate === 'passed' &&
        result.reconcile === 'passed' &&
        result.openLoopPersisted === true &&
        result.proposalPersisted === true &&
        result.idempotency === 'passed' &&
        result.externalWrite === false);
}
function printReport(result) {
    console.log('Adapter compatibility report\n');
    console.log(`file: ${result.file}`);
    console.log(`validate: ${result.validate}`);
    if (result.validateErrors) {
        for (const err of result.validateErrors) {
            console.log(`  error: ${err}`);
        }
    }
    console.log(`reconcile: ${result.reconcile} (mode: ${result.reconcileMode})`);
    if (result.reconcileError) {
        console.log(`  error: ${result.reconcileError}`);
    }
    console.log(`openLoopPersisted: ${result.openLoopPersisted}`);
    console.log(`proposalPersisted: ${result.proposalPersisted}`);
    console.log(`idempotency: ${result.idempotency}`);
    console.log(`externalWrite: ${result.externalWrite}`);
    if (result.reconcileMode === 'local_heuristic') {
        console.log('note: adapter:test uses a local heuristic — results may differ from the live API');
    }
}
if (!filePath) {
    if (jsonMode) {
        printJson({
            ok: false,
            error: {
                code: 'MISSING_FILE',
                message: 'Usage: npm run adapter:test -- <path-to-adapter-signal.json> [--json]',
            },
            safety: { externalWrite: false },
        });
    }
    else {
        console.error('Usage: npm run adapter:test -- <path-to-adapter-signal.json> [--json]');
    }
    process.exit(1);
}
const result = (0, runAdapterTest_1.runAdapterTest)(filePath);
if (jsonMode) {
    printJson({
        ok: didPass(result),
        report: result,
        safety: { externalWrite: false },
    });
}
else {
    printReport(result);
}
if (!didPass(result)) {
    process.exit(1);
}
//# sourceMappingURL=adapterTest.js.map