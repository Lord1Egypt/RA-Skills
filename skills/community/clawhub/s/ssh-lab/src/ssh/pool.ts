// Concurrency pool — simple semaphore for parallel SSH tasks
// Used by compare, status all, alert check all

/**
 * Run async tasks with bounded concurrency.
 * Returns results in input order; rejections propagate per-slot.
 */
export async function withPool<T>(
  tasks: (() => Promise<T>)[],
  max: number = 5,
): Promise<PromiseSettledResult<T>[]> {
  const results: PromiseSettledResult<T>[] = new Array(tasks.length);
  let cursor = 0;

  async function worker(): Promise<void> {
    while (cursor < tasks.length) {
      const idx = cursor++;
      try {
        results[idx] = { status: 'fulfilled', value: await tasks[idx]() };
      } catch (err) {
        results[idx] = { status: 'rejected', reason: err };
      }
    }
  }

  const workers = Array.from({ length: Math.min(max, tasks.length) }, () => worker());
  await Promise.all(workers);
  return results;
}
