import { loadTransitionReceipts, getTransitionReceiptsPath } from '../storage/transitionReceipts';
import { getCapabilityBoundary } from '../policy/capabilityBoundary';

function printJson(value: unknown): void {
  console.log(JSON.stringify(value, null, 2));
}

function main(): void {
  const receipts = loadTransitionReceipts();
  printJson({
    ok: true,
    source: 'worldloops.local',
    path: getTransitionReceiptsPath(),
    count: receipts.length,
    receipts,
    capabilityBoundary: getCapabilityBoundary(),
    safety: { externalWrite: false },
  });
}

main();
