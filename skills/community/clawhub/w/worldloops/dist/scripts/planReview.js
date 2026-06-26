"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const executionPlans_1 = require("../storage/executionPlans");
function printJson(value) {
    console.log(JSON.stringify(value, null, 2));
}
const ALL_STATUSES = ['planned'];
function buildReview(plans) {
    const byStatus = {
        planned: 0,
    };
    for (const p of plans) {
        if (p.status in byStatus) {
            byStatus[p.status]++;
        }
    }
    const highRiskPlans = plans.filter((p) => p.riskLevel === 'high' || p.riskLevel === 'critical');
    let suggestedFocus = null;
    if (highRiskPlans.length > 0) {
        suggestedFocus = `Review ${highRiskPlans.length} high-risk plan${highRiskPlans.length === 1 ? '' : 's'} before considering any execution contract.`;
    }
    else if (byStatus.planned > 0) {
        suggestedFocus = `Inspect ${byStatus.planned} planned execution preview${byStatus.planned === 1 ? '' : 's'} and confirm all steps are understood.`;
    }
    return { total: plans.length, byStatus, highRiskPlans, suggestedFocus };
}
function printHuman(plans) {
    const review = buildReview(plans);
    console.log('Execution Plan Review');
    console.log('');
    console.log(`Total plans: ${review.total}`);
    console.log('');
    console.log('By status');
    for (const status of ALL_STATUSES) {
        console.log(`  ${status}: ${review.byStatus[status]}`);
    }
    if (review.highRiskPlans.length > 0) {
        console.log('');
        console.log('High-risk plans');
        for (const p of review.highRiskPlans) {
            console.log(`  ${p.id}  ${p.templateId}  ${p.riskLevel}  ${p.title}`);
        }
    }
    if (review.suggestedFocus) {
        console.log('');
        console.log('Suggested focus');
        console.log(`  ${review.suggestedFocus}`);
    }
    console.log('');
    console.log('externalWrite: false');
}
function main() {
    const args = process.argv.slice(2);
    const jsonMode = args.includes('--json');
    const plans = (0, executionPlans_1.listExecutionPlans)();
    const review = buildReview(plans);
    if (jsonMode) {
        printJson({
            ok: true,
            source: 'worldloops.local',
            review: {
                total: review.total,
                byStatus: review.byStatus,
                highRiskPlans: review.highRiskPlans.map((p) => ({
                    id: p.id,
                    proposalId: p.proposalId,
                    templateId: p.templateId,
                    riskLevel: p.riskLevel,
                    title: p.title,
                    status: p.status,
                })),
                suggestedFocus: review.suggestedFocus,
            },
            safety: { externalWrite: false },
        });
    }
    else {
        printHuman(plans);
    }
}
main();
//# sourceMappingURL=planReview.js.map