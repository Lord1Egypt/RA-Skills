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
const proposalDecisionReceipts_1 = require("../storage/proposalDecisionReceipts");
const VALID_DECISION_INPUTS = ['approve', 'reject', 'snooze', 'escalate', 'repropose'];
const DECISION_TO_STATUS = {
    approve: 'approved',
    reject: 'rejected',
    snooze: 'snoozed',
    escalate: 'escalated',
    repropose: 'proposed',
};
const ALLOWED_DECISIONS_BY_STATUS = {
    proposed: ['approve', 'reject', 'snooze', 'escalate'],
    snoozed: ['repropose'],
    escalated: ['repropose'],
    approved: [],
    rejected: [],
};
function printJson(value) {
    console.log(JSON.stringify(value, null, 2));
}
function printHuman(opts) {
    console.log(`Proposal decision recorded`);
    console.log(`  Proposal:        ${opts.proposalId}`);
    console.log(`  Decision:        ${opts.decision}`);
    console.log(`  Previous status: ${opts.previousStatus}`);
    console.log(`  New status:      ${opts.newStatus}`);
    console.log(`  Receipt:         ${opts.receiptId}`);
    console.log('');
    console.log('Approval is not execution. No external writes.');
    console.log('externalWrite: false');
}
function main() {
    const args = process.argv.slice(2);
    const jsonMode = args.includes('--json');
    // Parse --decision flag
    let decisionFromFlag;
    const decisionFlagIdx = args.indexOf('--decision');
    const skipIndices = new Set();
    if (decisionFlagIdx !== -1 && args[decisionFlagIdx + 1] !== undefined) {
        decisionFromFlag = args[decisionFlagIdx + 1];
        skipIndices.add(decisionFlagIdx);
        skipIndices.add(decisionFlagIdx + 1);
    }
    // Collect positional args
    const positionals = args
        .map((a, i) => ({ a, i }))
        .filter(({ a, i }) => !a.startsWith('--') && !skipIndices.has(i))
        .map(({ a }) => a);
    const proposalId = positionals[0];
    const decisionFromPositional = positionals[1];
    const note = positionals[2] ?? null;
    const decisionInput = decisionFromFlag ?? decisionFromPositional;
    if (!proposalId) {
        printJson({
            ok: false,
            error: {
                code: 'MISSING_PROPOSAL_ID',
                message: 'Usage: npm run proposal:decide -- <proposal-id> <decision> [note] [--json]',
                validDecisions: ['approve', 'reject', 'snooze', 'escalate'],
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
    if (!decisionInput) {
        printJson({
            ok: false,
            error: {
                code: 'MISSING_PROPOSAL_DECISION',
                message: 'A decision is required. Usage: npm run proposal:decide -- <proposal-id> <decision>',
                validDecisions: ['approve', 'reject', 'snooze', 'escalate'],
            },
            currentStatus: proposal.status,
            safety: { externalWrite: false },
        });
        process.exit(1);
    }
    if (!VALID_DECISION_INPUTS.includes(decisionInput)) {
        printJson({
            ok: false,
            error: {
                code: 'INVALID_PROPOSAL_DECISION_VALUE',
                message: `Unknown decision: "${decisionInput}". Must be one of: ${VALID_DECISION_INPUTS.join(', ')}`,
                validDecisions: ['approve', 'reject', 'snooze', 'escalate'],
            },
            currentStatus: proposal.status,
            safety: { externalWrite: false },
        });
        process.exit(1);
    }
    const typedDecision = decisionInput;
    const allowedDecisions = ALLOWED_DECISIONS_BY_STATUS[proposal.status];
    if (!allowedDecisions.includes(typedDecision)) {
        printJson({
            ok: false,
            error: {
                code: 'INVALID_PROPOSAL_DECISION',
                message: `Cannot apply decision "${decisionInput}" to a proposal with status "${proposal.status}".`,
                allowedDecisions,
            },
            currentStatus: proposal.status,
            safety: { externalWrite: false },
        });
        process.exit(1);
    }
    const previousStatus = proposal.status;
    const newStatus = DECISION_TO_STATUS[typedDecision];
    const now = new Date().toISOString();
    const updatedProposal = { ...proposal, status: newStatus, updatedAt: now };
    (0, proposals_1.saveProposal)(updatedProposal);
    const receipt = {
        id: crypto.randomUUID(),
        proposalId: proposal.id,
        templateId: proposal.templateId,
        decision: typedDecision,
        previousStatus,
        newStatus,
        actor: 'worldloops.local',
        note,
        boundaryCrossed: 'local_commit',
        externalWrite: false,
        createdAt: now,
        source: 'worldloops.local',
    };
    (0, proposalDecisionReceipts_1.saveProposalDecisionReceipt)(receipt);
    if (jsonMode) {
        printJson({
            ok: true,
            source: 'worldloops.local',
            proposalId: proposal.id,
            previousStatus,
            newStatus,
            decision: typedDecision,
            receiptId: receipt.id,
            note,
            safety: { externalWrite: false },
        });
    }
    else {
        printHuman({
            proposalId: proposal.id,
            previousStatus,
            newStatus,
            decision: typedDecision,
            receiptId: receipt.id,
        });
    }
}
main();
//# sourceMappingURL=proposalDecide.js.map