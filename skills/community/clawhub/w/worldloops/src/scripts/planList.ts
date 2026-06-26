import { listExecutionPlans, getExecutionPlansPath } from '../storage/executionPlans';
import type { ExecutionPlan } from '../types/executionPlan';

function printJson(value: unknown): void {
  console.log(JSON.stringify(value, null, 2));
}

function truncate(str: string, max: number): string {
  return str.length > max ? str.slice(0, max - 1) + '…' : str;
}

function printHuman(plans: ExecutionPlan[]): void {
  if (plans.length === 0) {
    console.log('No execution plans found.');
    console.log('');
    console.log('externalWrite: false');
    return;
  }

  const cols = {
    id: 36,
    proposalId: 36,
    templateId: 20,
    status: 8,
    riskLevel: 10,
    title: 30,
    createdAt: 24,
  };

  const header = [
    'ID'.padEnd(cols.id),
    'PROPOSAL ID'.padEnd(cols.proposalId),
    'TEMPLATE'.padEnd(cols.templateId),
    'STATUS'.padEnd(cols.status),
    'RISK'.padEnd(cols.riskLevel),
    'TITLE'.padEnd(cols.title),
    'CREATED AT',
  ].join('  ');

  const divider = [
    '-'.repeat(cols.id),
    '-'.repeat(cols.proposalId),
    '-'.repeat(cols.templateId),
    '-'.repeat(cols.status),
    '-'.repeat(cols.riskLevel),
    '-'.repeat(cols.title),
    '-'.repeat(cols.createdAt),
  ].join('  ');

  console.log(header);
  console.log(divider);

  for (const p of plans) {
    const row = [
      p.id.padEnd(cols.id),
      p.proposalId.padEnd(cols.proposalId),
      p.templateId.padEnd(cols.templateId),
      p.status.padEnd(cols.status),
      p.riskLevel.padEnd(cols.riskLevel),
      truncate(p.title, cols.title).padEnd(cols.title),
      p.createdAt,
    ].join('  ');
    console.log(row);
  }

  console.log('');
  console.log('externalWrite: false');
}

function main(): void {
  const args = process.argv.slice(2);
  const jsonMode = args.includes('--json');

  const plans = listExecutionPlans();

  if (jsonMode) {
    printJson({
      ok: true,
      source: 'worldloops.local',
      path: getExecutionPlansPath(),
      count: plans.length,
      plans,
      safety: { externalWrite: false },
    });
  } else {
    printHuman(plans);
  }
}

main();
