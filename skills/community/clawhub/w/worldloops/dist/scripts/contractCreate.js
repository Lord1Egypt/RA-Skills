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
const executionPlans_1 = require("../storage/executionPlans");
const proposals_1 = require("../storage/proposals");
const proposalDecisionReceipts_1 = require("../storage/proposalDecisionReceipts");
const executionContracts_1 = require("../storage/executionContracts");
function printJson(value) {
    console.log(JSON.stringify(value, null, 2));
}
const EXECUTION_BOUNDARY = {
    externalWrite: false,
    allowedBoundary: 'local_commit',
    deniedCapabilities: [
        'sendEmail',
        'createEmailDraft',
        'sendSlackMessage',
        'createCalendarEvent',
        'modifyGitHub',
        'writeExternalSystem',
    ],
    reason: 'Execution contracts are local-only. No external writes are permitted in v1.0.0.',
};
const ROLLBACK_PLAN = {
    available: false,
    reason: 'Rollback execution is not implemented in v1.0.0',
};
function buildPreconditions(proposalId, planId) {
    return [
        {
            id: crypto.randomUUID(),
            description: `Proposal ${proposalId} exists and is approved`,
            satisfied: true,
            required: true,
        },
        {
            id: crypto.randomUUID(),
            description: `Execution plan ${planId} exists with status planned`,
            satisfied: true,
            required: true,
        },
        {
            id: crypto.randomUUID(),
            description: 'A decision receipt confirming approval exists for this proposal',
            satisfied: true,
            required: true,
        },
        {
            id: crypto.randomUUID(),
            description: 'No external write capabilities are required',
            satisfied: true,
            required: true,
        },
    ];
}
function buildRequiredApprovals(proposalId) {
    return [
        {
            id: crypto.randomUUID(),
            role: 'human_reviewer',
            required: true,
            satisfied: true,
            reason: `Proposal ${proposalId} has been approved by a reviewer with a recorded decision receipt.`,
        },
    ];
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
                message: 'Usage: npm run contract:create -- <plan-id> [--json]',
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
    if (plan.status !== 'planned') {
        printJson({
            ok: false,
            error: {
                code: 'EXECUTION_PLAN_NOT_READY',
                message: `Cannot create an execution contract for a plan with status "${plan.status}". Only planned execution plans can become contracts.`,
                currentStatus: plan.status,
                requiredStatus: 'planned',
            },
            safety: { externalWrite: false },
        });
        process.exit(1);
    }
    const proposal = (0, proposals_1.findProposalById)(plan.proposalId);
    if (!proposal) {
        const all = (0, proposals_1.listProposals)();
        printJson({
            ok: false,
            error: {
                code: 'PROPOSAL_NOT_FOUND',
                message: `Proposal not found: ${plan.proposalId}`,
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
                message: `Cannot create an execution contract for a proposal with status "${proposal.status}". Only approved proposals qualify.`,
                currentStatus: proposal.status,
                requiredStatus: 'approved',
            },
            safety: { externalWrite: false },
        });
        process.exit(1);
    }
    const allReceipts = (0, proposalDecisionReceipts_1.loadProposalDecisionReceipts)();
    const approvalReceipt = allReceipts.find((r) => r.proposalId === proposal.id &&
        (r.newStatus === 'approved' || r.decision === 'approve'));
    if (!approvalReceipt) {
        printJson({
            ok: false,
            error: {
                code: 'DECISION_RECEIPT_NOT_FOUND',
                message: `No approval decision receipt found for proposal ${proposal.id}. An explicit approve decision receipt is required to create an execution contract.`,
                proposalId: proposal.id,
                requiredDecision: 'approve',
            },
            safety: { externalWrite: false },
        });
        process.exit(1);
    }
    const now = new Date().toISOString();
    const audit = {
        proposalExists: true,
        proposalApproved: true,
        decisionReceiptExists: true,
        planExists: true,
        planStatus: plan.status,
        externalWrite: false,
    };
    const contract = {
        id: crypto.randomUUID(),
        planId: plan.id,
        proposalId: proposal.id,
        templateId: proposal.templateId,
        title: `Execution Contract: ${proposal.title}`,
        status: 'draft',
        riskLevel: proposal.riskLevel,
        executionBoundary: EXECUTION_BOUNDARY,
        preconditions: buildPreconditions(proposal.id, plan.id),
        requiredApprovals: buildRequiredApprovals(proposal.id),
        rollbackPlan: ROLLBACK_PLAN,
        audit,
        externalWrite: false,
        createdAt: now,
        updatedAt: now,
        source: 'worldloops.local',
    };
    (0, executionContracts_1.saveExecutionContract)(contract);
    if (jsonMode) {
        printJson({
            ok: true,
            source: 'worldloops.local',
            path: (0, executionContracts_1.getExecutionContractsPath)(),
            contract,
            safety: { externalWrite: false },
        });
    }
    else {
        console.log(`Execution contract created: ${contract.id}`);
        console.log(`  Plan:          ${contract.planId}`);
        console.log(`  Proposal:      ${contract.proposalId}`);
        console.log(`  Template:      ${contract.templateId}`);
        console.log(`  Title:         ${contract.title}`);
        console.log(`  Status:        ${contract.status}`);
        console.log(`  Risk level:    ${contract.riskLevel}`);
        console.log(`  externalWrite: false`);
        console.log(`  Created at:    ${contract.createdAt}`);
        console.log(`  Stored at:     ${(0, executionContracts_1.getExecutionContractsPath)()}`);
        console.log('');
        console.log('Contract ≠ External Write. No external writes.');
        console.log('externalWrite: false');
    }
}
main();
//# sourceMappingURL=contractCreate.js.map