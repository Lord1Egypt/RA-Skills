"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const repairWorldState_1 = require("../state/repairWorldState");
function printJson(value) {
    console.log(JSON.stringify(value, null, 2));
}
function printHuman(receipts) {
    console.log('WorldLoops state:repair:list');
    console.log('============================');
    console.log('');
    console.log(`Repair receipts: ${receipts.length}`);
    if (receipts.length === 0) {
        console.log('');
        console.log('No repair receipts found.');
        console.log('Run `npm run state:repair -- --apply` to create one.');
    }
    else {
        console.log('');
        for (const receipt of receipts) {
            if (typeof receipt !== 'object' || receipt === null)
                continue;
            const r = receipt;
            const summary = r['summary'];
            console.log(`  ID:       ${String(r['id'] ?? 'unknown')}`);
            console.log(`  Created:  ${String(r['createdAt'] ?? 'unknown')}`);
            console.log(`  Mode:     ${String(r['mode'] ?? 'unknown')}`);
            if (summary) {
                console.log(`  Issues:   ${String(summary['issuesObserved'] ?? 0)} observed, ${String(summary['repairableIssues'] ?? 0)} repairable, ${String(summary['nonRepairableIssues'] ?? 0)} non-repairable`);
                console.log(`  Applied:  ${String(summary['repairsApplied'] ?? 0)}`);
            }
            console.log(`  externalWrite: false`);
            console.log('');
        }
    }
}
function main() {
    const args = process.argv.slice(2);
    const jsonMode = args.includes('--json');
    const receipts = (0, repairWorldState_1.loadRepairReceipts)();
    if (jsonMode) {
        printJson(receipts);
    }
    else {
        printHuman(receipts);
    }
    process.exit(0);
}
main();
//# sourceMappingURL=stateRepairList.js.map