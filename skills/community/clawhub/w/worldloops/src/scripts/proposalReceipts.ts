import { listProposalDecisionReceipts, getProposalDecisionReceiptsPath } from '../storage/proposalDecisionReceipts';
import type { ProposalDecisionReceipt } from '../types/proposalDecisionReceipt';

function printJson(value: unknown): void {
  console.log(JSON.stringify(value, null, 2));
}

function printHuman(receipts: ProposalDecisionReceipt[]): void {
  if (receipts.length === 0) {
    console.log('No proposal decision receipts found.');
    console.log('');
    console.log('externalWrite: false');
    return;
  }

  const cols = {
    id: 36,
    proposalId: 36,
    decision: 12,
    previousStatus: 14,
    newStatus: 12,
    createdAt: 24,
  };

  const header = [
    'RECEIPT ID'.padEnd(cols.id),
    'PROPOSAL ID'.padEnd(cols.proposalId),
    'DECISION'.padEnd(cols.decision),
    'PREV STATUS'.padEnd(cols.previousStatus),
    'NEW STATUS'.padEnd(cols.newStatus),
    'CREATED AT',
  ].join('  ');

  const divider = [
    '-'.repeat(cols.id),
    '-'.repeat(cols.proposalId),
    '-'.repeat(cols.decision),
    '-'.repeat(cols.previousStatus),
    '-'.repeat(cols.newStatus),
    '-'.repeat(cols.createdAt),
  ].join('  ');

  console.log(header);
  console.log(divider);

  for (const r of receipts) {
    const row = [
      r.id.padEnd(cols.id),
      r.proposalId.padEnd(cols.proposalId),
      r.decision.padEnd(cols.decision),
      r.previousStatus.padEnd(cols.previousStatus),
      r.newStatus.padEnd(cols.newStatus),
      r.createdAt,
    ].join('  ');
    console.log(row);
  }

  console.log('');
  console.log('externalWrite: false');
}

function main(): void {
  const args = process.argv.slice(2);
  const jsonMode = args.includes('--json');

  const receipts = listProposalDecisionReceipts();

  if (jsonMode) {
    printJson({
      ok: true,
      source: 'worldloops.local',
      path: getProposalDecisionReceiptsPath(),
      count: receipts.length,
      receipts,
      safety: { externalWrite: false },
    });
  } else {
    printHuman(receipts);
  }
}

main();
