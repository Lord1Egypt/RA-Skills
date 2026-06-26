"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
const crypto = __importStar(require("node:crypto"));
const proposals_1 = require("../storage/proposals");
const executionPlans_1 = require("../storage/executionPlans");
function printJson(value) {
    console.log(JSON.stringify(value, null, 2));
}
function makeStep(type, title, description) {
    return {
        id: crypto.randomUUID(),
        title,
        type,
        description,
        externalWrite: false,
    };
}
function buildSteps(templateId, category, riskLevel) {
    const steps = [
        makeStep('review', 'Review approved proposal', `Confirm the approved proposal (templateId: ${templateId}, category: ${category}) is still valid before any further steps.`),
        makeStep('boundary_check', 'Check capability boundary', 'Verify this plan does not require capabilities beyond the local execution boundary. externalWrite must remain false.'),
        makeStep('prepare', 'Prepare dry-run preview', 'Assemble a dry-run description of what execution would require. No external action is taken at this step.'),
    ];
    if (riskLevel === 'high' || riskLevel === 'critical') {
        steps.push(makeStep('dry_run', 'Dry-run validation', `Risk level is "${riskLevel}". Perform an additional dry-run validation pass before marking receipt-ready.`));
    }
    steps.push(makeStep('receipt_ready', 'Mark receipt-ready', 'Record that a local execution plan preview has been generated. This does not execute anything. externalWrite:false.'));
    return steps;
}
function main() {
    const args = process.argv.slice(2);
    const jsonMode = args.includes('--json');
    const proposalId = args.find((a) => !a.startsWith('--'));
    if (!proposalId) {
        printJson({
            ok: false,
            error: {
                code: 'MISSING_PROPOSAL_ID',
                message: 'Usage: npm run plan:create -- <proposal-id> [--json]',
            },
            safety: { externalWrite: false },
        });
        process.exit(1);
    }
    const proposal = (0, proposals_1.findProposalById)(proposalId);
    if (!proposal) {
        const all = (0, proposals_1.listProposals)();
        printJson({
            ok: false,
            error: {
                code: 'PROPOSAL_NOT_FOUND',
                message: `Proposal not found: ${proposalId}`,
                availableProposalIds: all.map((p) => ({ id: p.id, templateId: p.templateId, status: p.status })),
            },
            safety: { externalWrite: false },
        });
        process.exit(1);
    }
    if (proposal.status !== 'approved') {
        printJson({
            ok: false,
            error: {
                code: 'PROPOSAL_NOT_APPROVED',
                message: `Cannot create an execution plan for a proposal with status "${proposal.status}". Only approved proposals can become execution plans.`,
                currentStatus: proposal.status,
                requiredStatus: 'approved',
            },
            safety: { externalWrite: false },
        });
        process.exit(1);
    }
    const now = new Date().toISOString();
    const steps = buildSteps(proposal.templateId, proposal.category, proposal.riskLevel);
    const plan = {
        id: crypto.randomUUID(),
        proposalId: proposal.id,
        templateId: proposal.templateId,
        title: `Execution Plan Preview: ${proposal.title}`,
        status: 'planned',
        riskLevel: proposal.riskLevel,
        steps,
        externalWrite: false,
        createdAt: now,
        updatedAt: now,
        source: 'worldloops.local',
    };
    (0, executionPlans_1.saveExecutionPlan)(plan);
    if (jsonMode) {
        printJson({
            ok: true,
            source: 'worldloops.local',
            path: (0, executionPlans_1.getExecutionPlansPath)(),
            plan,
            safety: { externalWrite: false },
        });
    }
    else {
        console.log(`Execution plan created: ${plan.id}`);
        console.log(`  Proposal:      ${plan.proposalId}`);
        console.log(`  Template:      ${plan.templateId}`);
        console.log(`  Title:         ${plan.title}`);
        console.log(`  Status:        ${plan.status}`);
        console.log(`  Risk level:    ${plan.riskLevel}`);
        console.log(`  Steps:         ${plan.steps.length}`);
        console.log(`  externalWrite: false`);
        console.log(`  Created at:    ${plan.createdAt}`);
        console.log(`  Stored at:     ${(0, executionPlans_1.getExecutionPlansPath)()}`);
        console.log('');
        console.log('Plan ≠ Execution. No external writes.');
        console.log('externalWrite: false');
    }
}
main();
//# sourceMappingURL=planCreate.js.map