import { findOpenLoopStateById, loadOpenLoopStates } from '../storage/openLoopStates';
import { getCapabilityBoundary } from '../policy/capabilityBoundary';
import type { OpenLoopState } from '../types/openLoopState';

function printJson(value: unknown): void {
  console.log(JSON.stringify(value, null, 2));
}

function printHuman(loop: OpenLoopState): void {
  const source = loop.sourceSignals.length > 0 ? loop.sourceSignals[0].source : '(none)';
  const owner = loop.owner ?? '(none)';
  console.log(`Loop: ${loop.id}`);
  console.log(`  Title:            ${loop.title}`);
  console.log(`  Status:           ${loop.status}`);
  console.log(`  Severity:         ${loop.severity}`);
  console.log(`  Source:           ${source}`);
  console.log(`  Owner:            ${owner}`);
  console.log(`  Reason:           ${loop.adjudication.reason}`);
  console.log(`  Signals:          ${loop.sourceSignals.length}`);
  for (const signal of loop.sourceSignals) {
    console.log(`    - [${signal.source}] ${signal.text}`);
  }
  console.log(`  Suggested action: ${loop.adjudication.action}`);
  console.log(`  externalWrite:    false`);
}

function main(): void {
  const args = process.argv.slice(2);
  const jsonMode = args.includes('--json');
  const loopId = args.find((a) => !a.startsWith('--'));

  if (!loopId) {
    printJson({
      ok: false,
      error: {
        code: 'MISSING_LOOP_ID',
        message: 'Usage: npm run loop:show -- <loopId> [--json]',
      },
      safety: { externalWrite: false },
    });
    process.exit(1);
  }

  const loop = findOpenLoopStateById(loopId);

  if (!loop) {
    const loops = loadOpenLoopStates();

    printJson({
      ok: false,
      error: {
        code: 'LOOP_NOT_FOUND',
        message: `Open loop not found: ${loopId}`,
      },
      availableLoopIds: loops.map((item) => ({
        id: item.id,
        canonicalKey: item.canonicalKey,
        title: item.title,
        status: item.status,
        severity: item.severity,
      })),
      capabilityBoundary: getCapabilityBoundary(),
      safety: { externalWrite: false },
    });
    process.exit(1);
  }

  if (jsonMode) {
    printJson({
      ok: true,
      source: 'worldloops.local',
      loop: {
        id: loop.id,
        canonicalKey: loop.canonicalKey,
        title: loop.title,
        status: loop.status,
        severity: loop.severity,
        owner: loop.owner,
        dueAt: loop.dueAt,
        lastObservedAt: loop.lastObservedAt,
        updatedAt: loop.updatedAt,
        adjudication: loop.adjudication,
        sourceSignals: loop.sourceSignals,
        history: loop.history,
        safety: loop.safety,
      },
      capabilityBoundary: getCapabilityBoundary(),
      safety: { externalWrite: false },
    });
  } else {
    printHuman(loop);
  }
}

main();
