import { checkReceipts } from '../state/checkWorldState';

function printJson(value: unknown): void {
  console.log(JSON.stringify(value, null, 2));
}

function severityLabel(severity: string): string {
  if (severity === 'error') return 'ERROR';
  if (severity === 'info') return 'INFO ';
  return 'WARN ';
}

function printHuman(result: ReturnType<typeof checkReceipts>): void {
  console.log('WorldLoops receipts:verify');
  console.log('==========================');
  console.log('');
  console.log(`Files checked: ${result.summary.filesChecked}`);
  console.log(`Issues:        ${result.summary.issues}`);
  console.log(`Warnings:      ${result.summary.warnings}`);
  console.log(`Repaired:      ${result.summary.repaired}`);

  if (result.issues.length > 0) {
    console.log('');
    console.log('Issues:');
    for (const issue of result.issues) {
      console.log(`  [${severityLabel(issue.severity)}] ${issue.code}`);
      console.log(`    File:    ${issue.file}`);
      console.log(`    Message: ${issue.message}`);
      if (issue.referenceId !== undefined) {
        console.log(`    Ref:     ${issue.referenceId}`);
      }
    }
  }

  console.log('');
  console.log(`Status: ${result.status.toUpperCase()}`);
  console.log('externalWrite: false');
}

function main(): void {
  const args = process.argv.slice(2);
  const jsonMode = args.includes('--json');

  const result = checkReceipts();

  if (jsonMode) {
    printJson(result);
  } else {
    printHuman(result);
  }

  process.exit(result.ok ? 0 : 1);
}

main();
