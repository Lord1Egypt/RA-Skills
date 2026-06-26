import { loadOpenLoopStates, getOpenLoopStatesPath } from '../storage/openLoopStates';
import { getCapabilityBoundary } from '../policy/capabilityBoundary';

const ALLOWED_STATUSES = ['todo', 'doing', 'done', 'snoozed', 'escalated'];
const ALLOWED_SEVERITIES = ['low', 'medium', 'high', 'critical'];

function printJson(value: unknown): void {
  console.log(JSON.stringify(value, null, 2));
}

function truncate(str: string, max: number): string {
  return str.length > max ? str.slice(0, max - 1) + '…' : str;
}

function getFlag(args: string[], flag: string): string | undefined {
  const idx = args.indexOf(flag);
  return idx !== -1 && idx + 1 < args.length ? args[idx + 1] : undefined;
}

function printTable(loops: ReturnType<typeof loadOpenLoopStates>, hasFilters: boolean): void {
  if (loops.length === 0) {
    console.log(hasFilters ? 'No open loops matched the selected filters.' : 'No open loops found.');
    return;
  }

  const cols = {
    id: 36,
    status: 10,
    severity: 8,
    title: 40,
    sourceCount: 7,
    updatedAt: 24,
  };

  const header = [
    'ID'.padEnd(cols.id),
    'STATUS'.padEnd(cols.status),
    'SEVERITY'.padEnd(cols.severity),
    'TITLE'.padEnd(cols.title),
    'SRCS'.padEnd(cols.sourceCount),
    'UPDATED AT',
  ].join('  ');

  const divider = [
    '-'.repeat(cols.id),
    '-'.repeat(cols.status),
    '-'.repeat(cols.severity),
    '-'.repeat(cols.title),
    '-'.repeat(cols.sourceCount),
    '-'.repeat(cols.updatedAt),
  ].join('  ');

  console.log(header);
  console.log(divider);

  for (const loop of loops) {
    const row = [
      loop.id.padEnd(cols.id),
      loop.status.padEnd(cols.status),
      loop.severity.padEnd(cols.severity),
      truncate(loop.title, cols.title).padEnd(cols.title),
      String(loop.sourceSignals.length).padEnd(cols.sourceCount),
      loop.updatedAt,
    ].join('  ');
    console.log(row);
  }
}

function main(): void {
  const args = process.argv.slice(2);
  const jsonMode = args.includes('--json');
  const boundary = getCapabilityBoundary();

  const statusFilter = getFlag(args, '--status');
  const severityFilter = getFlag(args, '--severity');

  if (statusFilter !== undefined && !ALLOWED_STATUSES.includes(statusFilter)) {
    printJson({
      ok: false,
      error: {
        code: 'INVALID_STATUS_FILTER',
        message: `Invalid status filter: ${statusFilter}`,
      },
      allowed: ALLOWED_STATUSES,
      capabilityBoundary: boundary,
    });
    process.exit(1);
  }

  if (severityFilter !== undefined && !ALLOWED_SEVERITIES.includes(severityFilter)) {
    printJson({
      ok: false,
      error: {
        code: 'INVALID_SEVERITY_FILTER',
        message: `Invalid severity filter: ${severityFilter}`,
      },
      allowed: ALLOWED_SEVERITIES,
      capabilityBoundary: boundary,
    });
    process.exit(1);
  }

  let loops = loadOpenLoopStates();

  if (statusFilter !== undefined) {
    loops = loops.filter(l => l.status === statusFilter);
  }
  if (severityFilter !== undefined) {
    loops = loops.filter(l => l.severity === severityFilter);
  }

  const hasFilters = statusFilter !== undefined || severityFilter !== undefined;
  const filters: Record<string, string> = {};
  if (statusFilter !== undefined) filters.status = statusFilter;
  if (severityFilter !== undefined) filters.severity = severityFilter;

  if (jsonMode) {
    const result: Record<string, unknown> = {
      ok: true,
      source: 'worldloops.local',
      path: getOpenLoopStatesPath(),
      count: loops.length,
      loops,
      capabilityBoundary: boundary,
      safety: { externalWrite: false },
    };
    if (hasFilters) result.filters = filters;
    printJson(result);
  } else {
    printTable(loops, hasFilters);
  }
}

main();
