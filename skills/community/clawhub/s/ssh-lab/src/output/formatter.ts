// Output formatter — three modes: summary (default), json, raw

import type { CommandResult, OutputMode } from '../types/index.js';

export function render<T>(result: CommandResult<T>, mode: OutputMode): void {
  switch (mode) {
    case 'json':
      process.stdout.write(JSON.stringify(result, null, 2) + '\n');
      break;

    case 'raw':
      if (result.raw) {
        process.stdout.write(result.raw + '\n');
      } else if (result.data && typeof result.data === 'string') {
        process.stdout.write(result.data + '\n');
      } else {
        // Fallback to JSON for non-string raw data
        process.stdout.write(JSON.stringify(result.data, null, 2) + '\n');
      }
      break;

    case 'summary':
    default:
      process.stdout.write(result.summary + '\n');
      if (result.error) {
        process.stderr.write(`error[${result.error.code}]: ${result.error.message}\n`);
      }
      break;
  }
}

/** Determine exit code from result.
 * For alert-check: 0=clear, 1=warning, 2=critical */
export function exitCode<T>(result: CommandResult<T>): number {
  if (result.ok) return 0;
  if (result.error?.code === 'ALERT_CRITICAL') return 2;
  return 1;
}
