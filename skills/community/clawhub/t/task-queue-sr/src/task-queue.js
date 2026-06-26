/**
 * TaskQueue v1.1.0 — Async Task Queue for AI Agents
 * Sequential/parallel task execution with retry, priority, dependency chains,
 * per-task timeouts, event hooks, cancel, clear, and run metrics.
 * @author @TheShadowRose
 * @license MIT
 */

const { EventEmitter } = require('events');

class TaskQueue extends EventEmitter {
  /**
   * @param {object} options
   * @param {number} [options.maxRetries=3]        - Default max retries per task
   * @param {number} [options.retryDelay=5000]     - Base delay between retries (ms); multiplied by retry count
   * @param {number} [options.concurrency=1]       - Max tasks running in parallel
   * @param {number} [options.timeout=0]           - Default task timeout in ms (0 = no timeout)
   */
  constructor(options = {}) {
    super();
    this.maxRetries = options.maxRetries || 3;
    this.retryDelay = options.retryDelay || 5000;
    this.concurrency = Math.max(1, options.concurrency || 1);
    this.timeout = options.timeout || 0;
    this.tasks = [];
    this.results = [];
    this.log = [];
    this._paused = false;
    this._running = false;
    this._cancelledIds = new Set();
  }

  /**
   * Add a task to the queue.
   * @param {object} task
   * @param {string}   [task.id]         - Unique ID (auto-generated if omitted)
   * @param {string}   [task.name]       - Human-readable name
   * @param {number}   [task.priority=0] - Lower = higher priority
   * @param {string}   [task.dependsOn]  - ID of a task that must complete first
   * @param {Function} [task.handler]    - async (task) => result
   * @param {number}   [task.maxRetries] - Override global maxRetries for this task
   * @param {number}   [task.timeout]    - Override global timeout for this task (ms)
   * @param {*}        [task.data]       - Arbitrary payload passed through to handler
   */
  add(task) {
    if (this._running) {
      throw new Error('Cannot add tasks while queue is running. Call add() before run().');
    }
    this.tasks.push({
      id: task.id || `task-${Date.now()}-${this.tasks.length + 1}`,
      name: task.task || task.name || 'unnamed',
      priority: task.priority || 0,
      dependsOn: task.dependsOn || null,
      handler: task.handler || null,
      maxRetries: task.maxRetries !== undefined ? task.maxRetries : this.maxRetries,
      timeout: task.timeout !== undefined ? task.timeout : this.timeout,
      data: task.data || null,
      status: 'queued',
      retries: 0,
      result: null,
      error: null,
      startTime: null,
      endTime: null
    });
    return this;
  }

  /**
   * Cancel a queued (not yet started) task by ID.
   * Tasks already running cannot be cancelled.
   * @param {string} id
   */
  cancel(id) {
    this._cancelledIds.add(id);
    const task = this.tasks.find(t => t.id === id);
    if (task && task.status === 'queued') {
      task.status = 'cancelled';
    }
    return this;
  }

  /**
   * Remove all queued tasks (does not affect a running queue).
   */
  clear() {
    this.tasks = this.tasks.filter(t => t.status === 'running');
    return this;
  }

  /** Pause execution after the current task batch completes. */
  pause() { this._paused = true; return this; }

  /** Resume a paused queue. */
  resume() { this._paused = false; return this; }

  /**
   * Run all queued tasks.
   * @param {Function} [executor] - Fallback async (task) => result used when task has no handler
   * @returns {Promise<RunResult>}
   */
  async run(executor) {
    this._running = true;
    this.results = [];
    this.log = [];

    // Drain queue — prevents re-execution on subsequent run() calls
    const tasksToRun = this.tasks.splice(0);
    const total = tasksToRun.length;

    // Sort by priority (lower number = higher priority)
    tasksToRun.sort((a, b) => a.priority - b.priority);

    // Build lookup map for dependency resolution — uses the full pre-drain list
    const taskMap = new Map(tasksToRun.map(t => [t.id, t]));

    const runOne = async (task) => {
      // Skip if cancelled
      if (this._cancelledIds.has(task.id) || task.status === 'cancelled') {
        task.status = 'cancelled';
        this._log(task, 'Cancelled before start');
        this.results.push(this._toResult(task));
        this.emit('task:cancelled', task);
        return;
      }

      // Wait while paused
      while (this._paused) await this._delay(100);

      // Check dependency
      if (task.dependsOn) {
        const dep = taskMap.get(task.dependsOn);
        if (dep) {
          // Wait for dependency to finish (it may be running in a parallel batch)
          while (dep.status === 'running' || dep.status === 'queued') {
            await this._delay(50);
          }
          if (dep.status === 'failed' || dep.status === 'skipped' || dep.status === 'cancelled') {
            task.status = 'skipped';
            this._log(task, `Skipped — dependency "${task.dependsOn}" did not succeed`);
            this.results.push(this._toResult(task));
            this.emit('task:skipped', task);
            return;
          }
        }
      }

      task.status = 'running';
      task.startTime = Date.now();
      this._log(task, 'Started');
      this.emit('task:start', task);

      while (task.retries <= task.maxRetries) {
        try {
          let resultPromise;
          if (task.handler) {
            resultPromise = task.handler(task);
          } else if (executor) {
            resultPromise = executor(task);
          } else {
            resultPromise = Promise.resolve({ message: `Task "${task.name}" queued — no handler or executor provided` });
          }

          // Apply per-task timeout if configured
          if (task.timeout > 0) {
            task.result = await this._withTimeout(resultPromise, task.timeout, task.name);
          } else {
            task.result = await resultPromise;
          }

          task.status = 'success';
          task.endTime = Date.now();
          this._log(task, `Completed in ${task.endTime - task.startTime}ms`);
          this.emit('task:complete', task);
          break;

        } catch (err) {
          task.retries++;
          task.error = err.message;

          if (task.retries <= task.maxRetries) {
            this._log(task, `Retry ${task.retries}/${task.maxRetries}: ${err.message}`);
            this.emit('task:retry', { task, attempt: task.retries, error: err });
            await this._delay(this.retryDelay * task.retries); // Exponential backoff
          } else {
            task.status = 'failed';
            task.endTime = Date.now();
            this._log(task, `Failed after ${task.maxRetries} retries: ${err.message}`);
            this.emit('task:failed', task);
          }
        }
      }

      this.results.push(this._toResult(task));
    };

    // Run with concurrency — parallel batches of size this.concurrency
    for (let i = 0; i < tasksToRun.length; i += this.concurrency) {
      const batch = tasksToRun.slice(i, i + this.concurrency);
      await Promise.all(batch.map(t => runOne(t)));
    }

    this._running = false;
    this._cancelledIds.clear();

    const summary = {
      total,
      success: this.results.filter(r => r.status === 'success').length,
      failed: this.results.filter(r => r.status === 'failed').length,
      skipped: this.results.filter(r => r.status === 'skipped').length,
      cancelled: this.results.filter(r => r.status === 'cancelled').length,
      totalDurationMs: this.results.reduce((sum, r) => sum + (r.duration || 0), 0),
      results: this.results,
      log: this.log
    };

    this.emit('queue:drain', summary);
    return summary;
  }

  /**
   * Status of tasks still in the queue (not yet run).
   */
  getStatus() {
    return {
      queued: this.tasks.length,
      running: this._running,
      paused: this._paused,
      tasks: this.tasks.map(t => ({
        id: t.id,
        name: t.name,
        status: t.status,
        priority: t.priority,
        dependsOn: t.dependsOn || null,
        retries: t.retries
      }))
    };
  }

  /**
   * Metrics from the last completed run.
   */
  getMetrics() {
    if (!this.results.length) return null;
    const durations = this.results
      .filter(r => r.duration != null)
      .map(r => r.duration);

    return {
      total: this.results.length,
      success: this.results.filter(r => r.status === 'success').length,
      failed: this.results.filter(r => r.status === 'failed').length,
      skipped: this.results.filter(r => r.status === 'skipped').length,
      cancelled: this.results.filter(r => r.status === 'cancelled').length,
      avgDurationMs: durations.length
        ? Math.round(durations.reduce((a, b) => a + b, 0) / durations.length)
        : 0,
      maxDurationMs: durations.length ? Math.max(...durations) : 0,
      minDurationMs: durations.length ? Math.min(...durations) : 0,
      totalRetries: this.results.reduce((sum, r) => sum + (r.retries || 0), 0)
    };
  }

  // ─── Internal ─────────────────────────────────────────────────────────────

  _toResult(task) {
    return {
      id: task.id,
      name: task.name,
      status: task.status,
      duration: task.endTime != null && task.startTime != null
        ? task.endTime - task.startTime
        : null,
      result: task.result,
      error: task.error,
      retries: task.retries,
      data: task.data
    };
  }

  _log(task, message) {
    this.log.push({
      timestamp: new Date().toISOString(),
      taskId: task.id,
      taskName: task.name,
      message
    });
  }

  _delay(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  _withTimeout(promise, ms, name) {
    return new Promise((resolve, reject) => {
      const timer = setTimeout(
        () => reject(new Error(`Task "${name}" timed out after ${ms}ms`)),
        ms
      );
      promise
        .then(result => { clearTimeout(timer); resolve(result); })
        .catch(err => { clearTimeout(timer); reject(err); });
    });
  }
}

module.exports = { TaskQueue };
