import * as path from 'node:path';
import { runAdapterTest } from '../adapter/runAdapterTest';
import { checkWorldState, checkReceipts } from '../state/checkWorldState';

function main(): void {
  const slackFixture = path.join(process.cwd(), 'examples', 'adapters', 'slack-message.json');

  console.log('');
  console.log('Developer Verification');
  console.log('');

  const adapterResult = runAdapterTest(slackFixture);
  const adapterPassed =
    adapterResult.validate === 'passed' &&
    adapterResult.reconcile === 'passed' &&
    adapterResult.openLoopPersisted === true &&
    adapterResult.proposalPersisted === true &&
    adapterResult.idempotency === 'passed' &&
    adapterResult.externalWrite === false;

  console.log(`Adapter signal validation: ${adapterResult.validate}`);
  if (adapterResult.validateErrors) {
    for (const err of adapterResult.validateErrors) {
      console.log(`  error: ${err}`);
    }
  }
  console.log(`Reconcile: ${adapterResult.reconcile}`);
  if (adapterResult.reconcileError) {
    console.log(`  error: ${adapterResult.reconcileError}`);
  }
  console.log(`Open loop persisted: ${String(adapterResult.openLoopPersisted)}`);
  console.log(`Proposal persisted: ${String(adapterResult.proposalPersisted)}`);
  console.log(`Idempotency: ${adapterResult.idempotency}`);

  const stateResult = checkWorldState();
  console.log(`State check: ${stateResult.status}`);

  const receiptsResult = checkReceipts();
  console.log(`Receipts verification: ${receiptsResult.status}`);

  console.log(`externalWrite:false: enforced`);
  console.log('');

  const allPassed = adapterPassed && stateResult.ok && receiptsResult.ok;
  process.exit(allPassed ? 0 : 1);
}

main();
