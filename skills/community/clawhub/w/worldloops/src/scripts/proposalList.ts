import { listProposals, getProposalsPath } from '../storage/proposals';
import type { Proposal } from '../types/proposal';

function printJson(value: unknown): void {
  console.log(JSON.stringify(value, null, 2));
}

function truncate(str: string, max: number): string {
  return str.length > max ? str.slice(0, max - 1) + '…' : str;
}

function printHuman(proposals: Proposal[]): void {
  if (proposals.length === 0) {
    console.log('No proposals found.');
    console.log('');
    console.log('externalWrite: false');
    return;
  }

  const cols = {
    id: 36,
    templateId: 20,
    status: 10,
    riskLevel: 10,
    title: 30,
    createdAt: 24,
  };

  const header = [
    'ID'.padEnd(cols.id),
    'TEMPLATE'.padEnd(cols.templateId),
    'STATUS'.padEnd(cols.status),
    'RISK'.padEnd(cols.riskLevel),
    'TITLE'.padEnd(cols.title),
    'CREATED AT',
  ].join('  ');

  const divider = [
    '-'.repeat(cols.id),
    '-'.repeat(cols.templateId),
    '-'.repeat(cols.status),
    '-'.repeat(cols.riskLevel),
    '-'.repeat(cols.title),
    '-'.repeat(cols.createdAt),
  ].join('  ');

  console.log(header);
  console.log(divider);

  for (const p of proposals) {
    const row = [
      p.id.padEnd(cols.id),
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

  const proposals = listProposals();

  if (jsonMode) {
    printJson({
      ok: true,
      source: 'worldloops.local',
      path: getProposalsPath(),
      count: proposals.length,
      proposals,
      safety: { externalWrite: false },
    });
  } else {
    printHuman(proposals);
  }
}

main();
