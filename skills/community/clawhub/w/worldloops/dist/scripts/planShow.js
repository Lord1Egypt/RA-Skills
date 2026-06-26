"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const executionPlans_1 = require("../storage/executionPlans");
function printJson(value) {
    console.log(JSON.stringify(value, null, 2));
}
function printHuman(plan) {
    console.log(`Execution Plan: ${plan.id}`);
    console.log(`  Proposal:      ${plan.proposalId}`);
    console.log(`  Template:      ${plan.templateId}`);
    console.log(`  Title:         ${plan.title}`);
    console.log(`  Status:        ${plan.status}`);
    console.log(`  Risk level:    ${plan.riskLevel}`);
    console.log(`  externalWrite: false`);
    console.log(`  Created at:    ${plan.createdAt}`);
    console.log(`  Updated at:    ${plan.updatedAt}`);
    console.log(`  Source:        ${plan.source}`);
    console.log('');
    console.log('  Steps:');
    for (const step of plan.steps) {
        console.log(`    [${step.type}] ${step.title}`);
        console.log(`      ${step.description}`);
        console.log(`      externalWrite: false`);
    }
    console.log('');
    console.log('externalWrite: false');
}
function main() {
    const args = process.argv.slice(2);
    const jsonMode = args.includes('--json');
    const planId = args.find((a) => !a.startsWith('--'));
    if (!planId) {
        printJson({
            ok: false,
            error: {
                code: 'MISSING_PLAN_ID',
                message: 'Usage: npm run plan:show -- <plan-id> [--json]',
            },
            safety: { externalWrite: false },
        });
        process.exit(1);
    }
    const plan = (0, executionPlans_1.findExecutionPlanById)(planId);
    if (!plan) {
        const all = (0, executionPlans_1.listExecutionPlans)();
        printJson({
            ok: false,
            error: {
                code: 'EXECUTION_PLAN_NOT_FOUND',
                message: `Execution plan not found: ${planId}`,
                availablePlanIds: all.map((p) => ({ id: p.id, proposalId: p.proposalId, status: p.status })),
            },
            safety: { externalWrite: false },
        });
        process.exit(1);
    }
    if (jsonMode) {
        printJson({
            ok: true,
            source: 'worldloops.local',
            plan,
            safety: { externalWrite: false },
        });
    }
    else {
        printHuman(plan);
    }
}
main();
//# sourceMappingURL=planShow.js.map