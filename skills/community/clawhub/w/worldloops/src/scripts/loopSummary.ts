import { loadOpenLoopStates } from '../storage/openLoopStates';
import { getCapabilityBoundary } from '../policy/capabilityBoundary';
import type { OpenLoopStatus } from '../types/openLoopState';
import type { MinSeverity } from '../types';

const ALL_STATUSES: OpenLoopStatus[] = ['todo', 'doing', 'done', 'snoozed', 'escalated'];
const ALL_SEVERITIES: MinSeverity[] = ['low', 'medium', 'high', 'critical'];

type StatusCounts = Record<OpenLoopStatus, number>;
type SeverityCounts = Record<MinSeverity, number>;

function buildSummary(loops: ReturnType<typeof loadOpenLoopStates>) {
  const byStatus: StatusCounts = { todo: 0, doing: 0, done: 0, snoozed: 0, escalated: 0 };
  const bySeverity: SeverityCounts = { low: 0, medium: 0, high: 0, critical: 0 };

  for (const loop of loops) {
    byStatus[loop.status]++;
    bySeverity[loop.severity]++;
  }

  return { total: loops.length, byStatus, bySeverity };
}

function main(): void {
  const args = process.argv.slice(2);
  const jsonMode = args.includes('--json');
  const loops = loadOpenLoopStates();
  const summary = buildSummary(loops);

  if (jsonMode) {
    console.log(
      JSON.stringify(
        {
          ok: true,
          summary: {
            total: summary.total,
            byStatus: summary.byStatus,
            bySeverity: summary.bySeverity,
          },
          capabilityBoundary: getCapabilityBoundary(),
        },
        null,
        2
      )
    );
    return;
  }

  console.log('Open loop summary');
  console.log('');
  console.log(`total: ${summary.total}`);
  console.log('');

  if (loops.length === 0) {
    console.log('No open loops found.');
    return;
  }

  console.log('by status:');
  for (const status of ALL_STATUSES) {
    console.log(`  ${status}: ${summary.byStatus[status]}`);
  }
  console.log('');
  console.log('by severity:');
  for (const severity of ALL_SEVERITIES) {
    console.log(`  ${severity}: ${summary.bySeverity[severity]}`);
  }
}

main();
