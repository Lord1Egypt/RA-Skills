import * as crypto from 'node:crypto';
import { findProposalById, listProposals, saveProposal } from '../storage/proposals';
import { saveProposalDecisionReceipt } from '../storage/proposalDecisionReceipts';
import type { ProposalStatus } from '../types/proposal';
import type { ProposalDecisionReceipt } from '../types/proposalDecisionReceipt';

const VALID_DECISION_INPUTS = ['approve', 'reject', 'snooze', 'escalate', 'repropose'] as const;
type DecisionInput = (typeof VALID_DECISION_INPUTS)[number];

const DECISION_TO_STATUS: Record<DecisionInput, ProposalStatus> = {
  approve: 'approved',
  reject: 'rejected',
  snooze: 'snoozed',
  escalate: 'escalated',
  repropose: 'proposed',
};

const ALLOWED_DECISIONS_BY_STATUS: Record<ProposalStatus, DecisionInput[]> = {
  proposed: ['approve', 'reject', 'snooze', 'escalate'],
  snoozed: ['repropose'],
  escalated: ['repropose'],
  approved: [],
  rejected: [],
};

function printJson(value: unknown): void {
  console.log(JSON.stringify(value, null, 2));
}

function printHuman(opts: {
  proposalId: string;
  previousStatus: string;
  newStatus: string;
  decision: string;
  receiptId: string;
}): void {
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

function main(): void {
  const args = process.argv.slice(2);
  const jsonMode = args.includes('--json');

  // Parse --decision flag
  let decisionFromFlag: string | undefined;
  const decisionFlagIdx = args.indexOf('--decision');
  const skipIndices = new Set<number>();
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

  const proposal = findProposalById(proposalId);

  if (!proposal) {
    const all = listProposals();
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

  if (!VALID_DECISION_INPUTS.includes(decisionInput as DecisionInput)) {
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

  const typedDecision = decisionInput as DecisionInput;
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
  saveProposal(updatedProposal);

  const receipt: ProposalDecisionReceipt = {
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
  saveProposalDecisionReceipt(receipt);

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
  } else {
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
