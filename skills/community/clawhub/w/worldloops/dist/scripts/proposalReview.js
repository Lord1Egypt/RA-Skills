"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const proposals_1 = require("../storage/proposals");
function printJson(value) {
    console.log(JSON.stringify(value, null, 2));
}
const ALL_STATUSES = ['proposed', 'approved', 'rejected', 'snoozed', 'escalated'];
function buildReview(proposals) {
    const byStatus = {
        proposed: 0,
        approved: 0,
        rejected: 0,
        snoozed: 0,
        escalated: 0,
    };
    for (const p of proposals) {
        if (p.status in byStatus) {
            byStatus[p.status]++;
        }
    }
    const highRiskProposals = proposals.filter((p) => p.status === 'proposed' && (p.riskLevel === 'high' || p.riskLevel === 'critical'));
    let suggestedFocus = null;
    if (byStatus.proposed > 0) {
        suggestedFocus = `Review ${byStatus.proposed} proposed item${byStatus.proposed === 1 ? '' : 's'} that still need${byStatus.proposed === 1 ? 's' : ''} a decision.`;
    }
    return { total: proposals.length, byStatus, highRiskProposals, suggestedFocus };
}
function printHuman(proposals) {
    const review = buildReview(proposals);
    console.log('Proposal Review');
    console.log('');
    console.log(`Total proposals: ${review.total}`);
    console.log('');
    console.log('By status');
    for (const status of ALL_STATUSES) {
        console.log(`  ${status}: ${review.byStatus[status]}`);
    }
    if (review.highRiskProposals.length > 0) {
        console.log('');
        console.log('High-risk proposals (proposed)');
        for (const p of review.highRiskProposals) {
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
    const proposals = (0, proposals_1.listProposals)();
    const review = buildReview(proposals);
    if (jsonMode) {
        printJson({
            ok: true,
            source: 'worldloops.local',
            review: {
                total: review.total,
                byStatus: review.byStatus,
                highRiskProposals: review.highRiskProposals.map((p) => ({
                    id: p.id,
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
        printHuman(proposals);
    }
}
main();
//# sourceMappingURL=proposalReview.js.map