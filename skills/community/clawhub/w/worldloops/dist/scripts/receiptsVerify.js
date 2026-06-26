"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const checkWorldState_1 = require("../state/checkWorldState");
function printJson(value) {
    console.log(JSON.stringify(value, null, 2));
}
function severityLabel(severity) {
    if (severity === 'error')
        return 'ERROR';
    if (severity === 'info')
        return 'INFO ';
    return 'WARN ';
}
function printHuman(result) {
    console.log('WorldLoops receipts:verify');
    console.log('==========================');
    console.log('');
    console.log(`Files checked: ${result.summary.filesChecked}`);
    console.log(`Issues:        ${result.summary.issues}`);
    console.log(`Warnings:      ${result.summary.warnings}`);
    console.log(`Repaired:      ${result.summary.repaired}`);
    if (result.issues.length > 0) {
        console.log('');
        console.log('Issues:');
        for (const issue of result.issues) {
            console.log(`  [${severityLabel(issue.severity)}] ${issue.code}`);
            console.log(`    File:    ${issue.file}`);
            console.log(`    Message: ${issue.message}`);
            if (issue.referenceId !== undefined) {
                console.log(`    Ref:     ${issue.referenceId}`);
            }
        }
    }
    console.log('');
    console.log(`Status: ${result.status.toUpperCase()}`);
    console.log('externalWrite: false');
}
function main() {
    const args = process.argv.slice(2);
    const jsonMode = args.includes('--json');
    const result = (0, checkWorldState_1.checkReceipts)();
    if (jsonMode) {
        printJson(result);
    }
    else {
        printHuman(result);
    }
    process.exit(result.ok ? 0 : 1);
}
main();
//# sourceMappingURL=receiptsVerify.js.map