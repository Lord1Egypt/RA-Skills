/**
 * SerialQueue: a lightweight task queue with concurrency=1.
 *
 * Equivalent to `new PQueue({ concurrency: 1 })` but with zero external
 * dependencies. Supports:
 * - Serial execution (FIFO)
 * - `add(fn)` to enqueue a task (returns the task's result promise)
 * - `onIdle()` to wait until all queued tasks have completed
 * - `pause()` / `start()` to suspend/resume execution
 * - `size` to check pending task count
 * - Optional debug logger for enqueue/dequeue/complete diagnostics
 */

/**
 * @template T
 * @typedef {() => Promise<T>} Task
 */

/**
 * @typedef {Object} QueueEntry
 * @property {Task} task
 * @property {(value: unknown) => void} resolve
 * @property {(reason: unknown) => void} reject
 */

export class SerialQueue {
  /** Human-readable name for logging / diagnostics. */
  name;
  queue = [];
  running = false;
  paused = false;
  idleResolvers = [];
  /** Optional debug logger — receives diagnostic messages for enqueue/dequeue/complete. */
  debugFn;

  /**
   * @param {string} [name]
   */
  constructor(name = "unnamed") {
    this.name = name;
  }

  /** Set a debug logger for queue diagnostics. */
  /** @param {(msg: string) => void} fn */
  setDebugLogger(fn) {
    this.debugFn = fn;
  }

  /** Number of tasks waiting to be executed. */
  get size() {
    return this.queue.length;
  }

  /** Whether a task is currently executing. */
  get pending() {
    return this.running;
  }

  /**
   * Add a task to the queue. Returns the task's result promise.
   * @template T
   * @param {Task<T>} task
   * @returns {Promise<T>}
   */
  add(task) {
    return new Promise((resolve, reject) => {
      this.queue.push({
        task,
        resolve,
        reject,
      });
      this.debugFn?.(`[queue:${this.name}] enqueued, pending=${this.queue.length}, running=${this.running}`);
      this.drain();
    });
  }

  /** Pause the queue. Currently running task will finish, but no new tasks start. */
  pause() {
    this.paused = true;
  }

  /** Resume the queue after pause(). */
  start() {
    this.paused = false;
    this.drain();
  }

  /** Returns a promise that resolves when all queued tasks have completed. */
  onIdle() {
    if (this.queue.length === 0 && !this.running) {
      return Promise.resolve();
    }
    return new Promise((resolve) => {
      this.idleResolvers.push(resolve);
    });
  }

  /** Clear all pending (not yet started) tasks. */
  clear() {
    for (const entry of this.queue) {
      entry.reject(new Error("Queue cleared"));
    }
    this.queue = [];
  }

  drain() {
    if (this.running || this.paused || this.queue.length === 0) return;

    const entry = this.queue.shift();
    this.running = true;

    this.debugFn?.(`[queue:${this.name}] dequeued, starting execution (remaining=${this.queue.length})`);

    entry
      .task()
      .then((result) => entry.resolve(result))
      .catch((err) => entry.reject(err))
      .finally(() => {
        this.running = false;
        this.debugFn?.(`[queue:${this.name}] task completed (remaining=${this.queue.length})`);
        if (this.queue.length === 0) {
          // Notify idle waiters
          const resolvers = this.idleResolvers;
          this.idleResolvers = [];
          for (const resolve of resolvers) resolve();
        } else {
          this.drain();
        }
      });
  }
}
