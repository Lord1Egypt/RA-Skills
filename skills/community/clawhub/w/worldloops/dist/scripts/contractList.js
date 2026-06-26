"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const executionContracts_1 = require("../storage/executionContracts");
function printJson(value) {
    console.log(JSON.stringify(value, null, 2));
}
function truncate(str, max) {
    return str.length > max ? str.slice(0, max - 1) + '…' : str;
}
function printHuman(contracts) {
    if (contracts.length === 0) {
        console.log('No execution contracts found.');
        console.log('');
        console.log('externalWrite: false');
        return;
    }
    const cols = {
        id: 36,
        planId: 36,
        proposalId: 36,
        templateId: 20,
        status: 8,
        riskLevel: 10,
        title: 30,
        createdAt: 24,
    };
    const header = [
        'ID'.padEnd(cols.id),
        'PLAN ID'.padEnd(cols.planId),
        'PROPOSAL ID'.padEnd(cols.proposalId),
        'TEMPLATE'.padEnd(cols.templateId),
        'STATUS'.padEnd(cols.status),
        'RISK'.padEnd(cols.riskLevel),
        'TITLE'.padEnd(cols.title),
        'CREATED AT',
    ].join('  ');
    const divider = [
        '-'.repeat(cols.id),
        '-'.repeat(cols.planId),
        '-'.repeat(cols.proposalId),
        '-'.repeat(cols.templateId),
        '-'.repeat(cols.status),
        '-'.repeat(cols.riskLevel),
        '-'.repeat(cols.title),
        '-'.repeat(cols.createdAt),
    ].join('  ');
    console.log(header);
    console.log(divider);
    for (const c of contracts) {
        const row = [
            c.id.padEnd(cols.id),
            c.planId.padEnd(cols.planId),
            c.proposalId.padEnd(cols.proposalId),
            c.templateId.padEnd(cols.templateId),
            c.status.padEnd(cols.status),
            c.riskLevel.padEnd(cols.riskLevel),
            truncate(c.title, cols.title).padEnd(cols.title),
            c.createdAt,
        ].join('  ');
        console.log(row);
    }
    console.log('');
    console.log('externalWrite: false');
}
function main() {
    const args = process.argv.slice(2);
    const jsonMode = args.includes('--json');
    const contracts = (0, executionContracts_1.listExecutionContracts)();
    if (jsonMode) {
        printJson({
            ok: true,
            source: 'worldloops.local',
            path: (0, executionContracts_1.getExecutionContractsPath)(),
            count: contracts.length,
            contracts,
            safety: { externalWrite: false },
        });
    }
    else {
        printHuman(contracts);
    }
}
main();
//# sourceMappingURL=contractList.js.map