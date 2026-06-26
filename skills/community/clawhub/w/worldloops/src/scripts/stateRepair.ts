import { repairWorldState } from '../state/repairWorldState';
import type { RepairResult, RepairAction } from '../state/repairWorldState';

function printJson(value: unknown): void {
  console.log(JSON.stringify(value, null, 2));
}

function statusLabel(status: RepairAction['status']): string {
  switch (status) {
    case 'applied':
      return 'APPLIED      ';
    case 'planned':
      return 'PLANNED      ';
    case 'skipped':
      return 'SKIPPED      ';
    case 'non_repairable':
      return 'NON-REPAIRABLE';
    default:
      return String(status).padEnd(13);
  }
}

function printHuman(result: RepairResult, isDryRun: boolean): void {
  console.log('WorldLoops state:repair');
  console.log('=======================');
  console.log('');
  console.log(`Mode:                  ${isDryRun ? 'dry-run' : 'apply'}`);
  console.log(`Issues observed:       ${result.summary.issuesObserved}`);
  console.log(`Repairable issues:     ${result.summary.repairableIssues}`);
  console.log(`Non-repairable issues: ${result.summary.nonRepairableIssues}`);
  if (isDryRun) {
    console.log(`Repairs planned:       ${result.summary.repairsPlanned}`);
  } else {
    console.log(`Repairs applied:       ${result.summary.repairsApplied}`);
  }

  if (result.repairs.length > 0) {
    console.log('');
    console.log('Repairs:');
    for (const r of result.repairs) {
      console.log(`  [${statusLabel(r.status)}] ${r.code}`);
      console.log(`    File:    ${r.file}`);
      console.log(`    Message: ${r.message}`);
      if (r.referenceId !== undefined) {
        console.log(`    Ref:     ${r.referenceId}`);
      }
    }
  }

  console.log('');

  if (isDryRun) {
    console.log('No files were modified. This was a dry-run.');
  } else {
    console.log(`Repair receipt: ${result.receipt.id}`);
  }

  console.log(`externalWrite: false`);
}

function main(): void {
  const args = process.argv.slice(2);
  const jsonMode = args.includes('--json');
  const applyMode = args.includes('--apply');
  const dryRunMode = args.includes('--dry-run') || !applyMode;

  const result = repairWorldState({ apply: applyMode });

  if (jsonMode) {
    printJson(result);
  } else {
    printHuman(result, dryRunMode);
  }

  process.exit(0);
}

main();
