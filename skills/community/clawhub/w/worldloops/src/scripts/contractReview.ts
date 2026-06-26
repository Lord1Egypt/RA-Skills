import { listExecutionContracts } from '../storage/executionContracts';
import type { ExecutionContract, ExecutionContractStatus } from '../types/executionContract';

function printJson(value: unknown): void {
  console.log(JSON.stringify(value, null, 2));
}

const ALL_STATUSES: ExecutionContractStatus[] = ['draft'];

function buildReview(contracts: ExecutionContract[]) {
  const byStatus: Record<ExecutionContractStatus, number> = {
    draft: 0,
  };

  for (const c of contracts) {
    if (c.status in byStatus) {
      byStatus[c.status]++;
    }
  }

  const highRiskContracts = contracts.filter(
    (c) => c.riskLevel === 'high' || c.riskLevel === 'critical'
  );

  let suggestedFocus: string | null = null;
  if (highRiskContracts.length > 0) {
    suggestedFocus = `Review ${highRiskContracts.length} high-risk contract${highRiskContracts.length === 1 ? '' : 's'} before any future execution layer is considered.`;
  } else if (byStatus.draft > 0) {
    suggestedFocus = `Inspect ${byStatus.draft} draft contract${byStatus.draft === 1 ? '' : 's'} and confirm all boundaries and preconditions are understood.`;
  }

  return { total: contracts.length, byStatus, highRiskContracts, suggestedFocus };
}

function printHuman(contracts: ExecutionContract[]): void {
  const review = buildReview(contracts);

  console.log('Execution Contract Review');
  console.log('');
  console.log(`Total contracts: ${review.total}`);
  console.log('');
  console.log('By status');
  for (const status of ALL_STATUSES) {
    console.log(`  ${status}: ${review.byStatus[status]}`);
  }

  if (review.highRiskContracts.length > 0) {
    console.log('');
    console.log('High-risk contracts');
    for (const c of review.highRiskContracts) {
      console.log(`  ${c.id}  ${c.templateId}  ${c.riskLevel}  ${c.title}`);
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

function main(): void {
  const args = process.argv.slice(2);
  const jsonMode = args.includes('--json');

  const contracts = listExecutionContracts();
  const review = buildReview(contracts);

  if (jsonMode) {
    printJson({
      ok: true,
      source: 'worldloops.local',
      review: {
        total: review.total,
        byStatus: review.byStatus,
        highRiskContracts: review.highRiskContracts.map((c) => ({
          id: c.id,
          planId: c.planId,
          proposalId: c.proposalId,
          templateId: c.templateId,
          riskLevel: c.riskLevel,
          title: c.title,
          status: c.status,
        })),
        suggestedFocus: review.suggestedFocus,
      },
      safety: { externalWrite: false },
    });
  } else {
    printHuman(contracts);
  }
}

main();
