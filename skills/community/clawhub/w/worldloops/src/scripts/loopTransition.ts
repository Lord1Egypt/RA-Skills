import { findOpenLoopStateById, transitionOpenLoopState } from '../storage/openLoopStates';
import { getCapabilityBoundary } from '../policy/capabilityBoundary';
import type { OpenLoopStatus } from '../types/openLoopState';

const VALID_STATUSES: OpenLoopStatus[] = ['todo', 'doing', 'done', 'snoozed', 'escalated'];

const ALLOWED_TRANSITIONS: Record<OpenLoopStatus, OpenLoopStatus[]> = {
  todo: ['doing'],
  doing: ['done', 'snoozed', 'escalated'],
  snoozed: ['todo'],
  escalated: ['doing'],
  done: [],
};

function printJson(value: unknown): void {
  console.log(JSON.stringify(value, null, 2));
}

function main(): void {
  const args = process.argv.slice(2);

  const id = args[0];
  if (!id) {
    console.error('Usage: npm run loop:transition -- <loopId> <status> [note]');
    console.error('       npm run loop:transition -- <loopId> --to <status> [--dry-run]');
    process.exit(1);
  }

  const dryRun = args.includes('--dry-run');
  const toFlagIndex = args.indexOf('--to');

  let targetStatus: string;
  let note: string | null = null;

  if (toFlagIndex !== -1) {
    targetStatus = args[toFlagIndex + 1] ?? '';
    note = null;
  } else {
    targetStatus = args[1] ?? '';
    const noteParts = args.slice(2).filter((a) => a !== '--dry-run');
    note = noteParts.length > 0 ? noteParts.join(' ') : null;
  }

  if (!targetStatus || !VALID_STATUSES.includes(targetStatus as OpenLoopStatus)) {
    console.error(`Invalid status: ${targetStatus}`);
    console.error(`Valid statuses: ${VALID_STATUSES.join(', ')}`);
    process.exit(1);
  }

  const to = targetStatus as OpenLoopStatus;

  const loop = findOpenLoopStateById(id);

  if (!loop) {
    printJson({
      ok: false,
      error: {
        code: 'LOOP_NOT_FOUND',
        message: `Open loop not found: ${id}`,
      },
      safety: { externalWrite: false },
    });
    process.exit(1);
  }

  const allowed = ALLOWED_TRANSITIONS[loop.status];

  if (!allowed.includes(to)) {
    printJson({
      ok: false,
      error: {
        code: 'INVALID_LOOP_TRANSITION',
        message: `Cannot transition from '${loop.status}' to '${to}'.`,
        allowedTransitions: allowed,
      },
      currentStatus: loop.status,
      capabilityBoundary: getCapabilityBoundary(),
      safety: { externalWrite: false },
    });
    process.exit(1);
  }

  if (dryRun) {
    printJson({
      ok: true,
      dryRun: true,
      source: 'worldloops.local',
      preview: {
        id: loop.id,
        from: loop.status,
        to,
        note,
      },
      capabilityBoundary: getCapabilityBoundary(),
      safety: { externalWrite: false },
    });
    return;
  }

  const updated = transitionOpenLoopState(id, to, {
    actor: 'worldloops.local',
    note,
  });

  printJson({
    ok: true,
    source: 'worldloops.local',
    loop: updated,
    capabilityBoundary: getCapabilityBoundary(),
    safety: { externalWrite: false },
  });
}

main();
