"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const proposalTemplates_1 = require("../data/proposalTemplates");
function printJson(value) {
    console.log(JSON.stringify(value, null, 2));
}
function printHuman(templates) {
    console.log('Proposal Templates');
    console.log('');
    console.log(`Available templates: ${templates.length}`);
    console.log('');
    for (const t of templates) {
        console.log(`  ${t.id}`);
        console.log(`    Title:          ${t.title}`);
        console.log(`    Description:    ${t.description}`);
        console.log(`    Category:       ${t.category}`);
        console.log(`    Risk level:     ${t.riskLevel}`);
        console.log(`    externalWrite:  false`);
        console.log(`    requiredReview: true`);
        console.log('');
    }
    console.log('externalWrite: false');
}
function main() {
    const args = process.argv.slice(2);
    const jsonMode = args.includes('--json');
    if (jsonMode) {
        printJson({
            ok: true,
            source: 'worldloops.local',
            count: proposalTemplates_1.PROPOSAL_TEMPLATES.length,
            templates: proposalTemplates_1.PROPOSAL_TEMPLATES,
            safety: { externalWrite: false },
        });
    }
    else {
        printHuman(proposalTemplates_1.PROPOSAL_TEMPLATES);
    }
}
main();
//# sourceMappingURL=proposalTemplates.js.map