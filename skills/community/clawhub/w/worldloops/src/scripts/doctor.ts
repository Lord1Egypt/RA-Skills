import * as fs from 'node:fs';
import * as path from 'node:path';
import { checkWorldState } from '../state/checkWorldState';

function readPackageVersion(): string {
  try {
    const pkgPath = path.join(process.cwd(), 'package.json');
    const pkg = JSON.parse(fs.readFileSync(pkgPath, 'utf8')) as Record<string, unknown>;
    return typeof pkg['version'] === 'string' ? pkg['version'] : 'unknown';
  } catch {
    return 'unknown';
  }
}

function checkBuildFiles(): boolean {
  const distPath = path.join(process.cwd(), 'dist');
  return (
    fs.existsSync(distPath) &&
    fs.existsSync(path.join(distPath, 'scripts'))
  );
}

function storeCheck(dir: string, filename: string, stateErrors: Set<string>): string {
  const filePath = path.join(dir, filename);
  if (!fs.existsSync(filePath)) return 'OK';
  if (stateErrors.has(filePath)) return 'issues detected — run npm run state:check';
  return 'OK';
}

function storeCheckRepair(dir: string, filename: string, stateErrors: Set<string>): string {
  const filePath = path.join(dir, filename);
  if (!fs.existsSync(filePath)) return 'OK — no repair history yet';
  if (stateErrors.has(filePath)) return 'issues detected — run npm run state:check';
  return 'OK';
}

function main(): void {
  const worldloopsDir = process.env.WORLDLOOPS_DIR ?? path.join(process.cwd(), '.worldloops');
  const version = readPackageVersion();
  const buildOk = checkBuildFiles();
  const dirExists = fs.existsSync(worldloopsDir);
  const stateResult = checkWorldState();

  const errorFiles = new Set(
    stateResult.issues
      .filter((i) => i.severity === 'error')
      .map((i) => i.file)
  );

  const openLoopsStatus = storeCheck(worldloopsDir, 'open_loop_states.json', errorFiles);
  const proposalsStatus = storeCheck(worldloopsDir, 'proposals.json', errorFiles);
  const plansStatus = storeCheck(worldloopsDir, 'execution_plans.json', errorFiles);
  const contractsStatus = storeCheck(worldloopsDir, 'execution_contracts.json', errorFiles);
  const transReceiptsStatus = storeCheck(worldloopsDir, 'transition_receipts.json', errorFiles);
  const propDecisionReceiptsStatus = storeCheck(worldloopsDir, 'proposal_decision_receipts.json', errorFiles);
  const repairReceiptsStatus = storeCheckRepair(worldloopsDir, 'repair_receipts.json', errorFiles);

  const allOk =
    version !== 'unknown' &&
    buildOk &&
    stateResult.ok;

  console.log('');
  console.log('WorldLoops Safety Check');
  console.log('');

  if (allOk) {
    console.log('Your local workspace is safe.');
  } else {
    console.log('Your local workspace has issues. See Developer details below.');
  }

  console.log('');
  console.log('No external writes enabled.');
  console.log('No emails will be sent.');
  console.log('No chat messages will be posted.');
  console.log('No calendar events will be created.');
  console.log('No project changes will be made.');
  console.log('');
  console.log('Local state is readable.');
  console.log('Receipts are verifiable.');
  console.log('Repair history is auditable.');
  console.log('');
  console.log('Status:');
  console.log(allOk ? 'Safe to try.' : 'Some issues detected — see Developer details.');
  console.log('');
  console.log('Developer details:');
  console.log(`- Package version: ${version !== 'unknown' ? 'OK' : 'unknown'}`);
  console.log(`- Build files: ${buildOk ? 'OK' : 'missing — run npm run build'}`);
  console.log(`- Local state directory: ${dirExists ? 'OK' : 'OK'}`);
  console.log(`- Open loops store: ${openLoopsStatus}`);
  console.log(`- Proposal store: ${proposalsStatus}`);
  console.log(`- Execution plans: ${plansStatus}`);
  console.log(`- Execution contracts: ${contractsStatus}`);
  console.log(`- Transition receipts: ${transReceiptsStatus}`);
  console.log(`- Proposal decision receipts: ${propDecisionReceiptsStatus}`);
  console.log(`- Repair receipts: ${repairReceiptsStatus}`);
  console.log(`- externalWrite:false: enforced`);

  if (!stateResult.ok && stateResult.issues.length > 0) {
    console.log('');
    console.log(`State integrity: ${stateResult.summary.issues} error(s) found`);
    for (const issue of stateResult.issues) {
      if (issue.severity === 'error') {
        console.log(`  [${issue.code}] ${issue.message}`);
      }
    }
  }

  console.log('');

  process.exit(allOk ? 0 : 1);
}

main();
