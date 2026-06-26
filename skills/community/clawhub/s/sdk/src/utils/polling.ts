import { PollingTimeoutError, SimulationFailedError } from './errors';
import type { SimulationJob } from '../types';

/**
 * Sleep for a given number of milliseconds
 */
export function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

/**
 * Options for polling
 */
export interface PollOptions {
  /** Polling interval in ms */
  interval: number;
  /** Timeout in ms */
  timeout: number;
  /** Optional status callback */
  onStatus?: (status: string, job?: SimulationJob) => void;
}

/**
 * Poll a function until it returns a complete result or times out
 */
export async function pollUntilComplete(
  pollFn: () => Promise<SimulationJob>,
  options: PollOptions
): Promise<SimulationJob> {
  const { interval, timeout, onStatus } = options;
  const startTime = Date.now();
  let lastJob: SimulationJob | undefined;

  while (Date.now() - startTime < timeout) {
    try {
      const job = await pollFn();
      lastJob = job;

      if (onStatus) {
        onStatus(job.status, job);
      }

      if (job.status === 'complete') {
        return job;
      }

      if (job.status === 'error') {
        throw new SimulationFailedError(job.jobId, job.error);
      }

      // Still processing, wait and retry
      await sleep(interval);
    } catch (error) {
      // Re-throw our errors
      if (error instanceof SimulationFailedError) {
        throw error;
      }
      // For other errors, keep polling (could be transient network issues)
      if (onStatus) {
        onStatus('retrying', lastJob);
      }
      await sleep(interval);
    }
  }

  // Timeout reached
  throw new PollingTimeoutError(lastJob?.jobId || 'unknown', timeout);
}
