#!/usr/bin/env node

/**
 * 企微 Agent Ops Center — 进程生命周期管理器 (v2.4)
 *
 * 职责：子进程 spawn/monitor/restart，支持全生命周期操作
 * 对比竞品 feishu-evolver-wrapper 的 Lifecycle Manager：
 *   - watchdog + ensure 检查（竞品有，我们补齐）
 *   - 自动重启崩溃/挂起实例
 *   - 状态持久化 + 企微卡片通知
 *
 * 设计原则：
 *   - 纯 Node.js 原生进程管理（不用 crontab）
 *   - 指数退避重启策略（避免 crash loop）
 *   - 每 10 分钟 ensure 检查（与竞品对齐）
 */

const { spawn } = require('child_process');
const { EventEmitter } = require('events');
const http = require('http');

const DEFAULTS = {
  ensureInterval: 10 * 60 * 1000,  // 每 10 分钟 ensure 检查
  maxRestarts: 5,                   // 最大连续重启次数
  restartWindow: 300_000,           // 重启计数窗口 (5 分钟)
  restartBackoffMin: 2_000,         // 最小退避 (2 秒)
  restartBackoffMax: 120_000,       // 最大退避 (2 分钟)
  healthTimeout: 5_000,             // 健康检查超时
  shutdownTimeout: 10_000,          // 优雅关闭超时
};

/**
 * 单个被管进程的状态机：
 *   stopped → starting → running → stopping → stopped
 *            ↘ crashed → restarting → starting
 */
const PROCESS_STATES = {
  STOPPED: 'stopped',
  STARTING: 'starting',
  RUNNING: 'running',
  STOPPING: 'stopping',
  CRASHED: 'crashed',
  RESTARTING: 'restarting',
};

class LifecycleManager extends EventEmitter {
  constructor(config = {}) {
    super();
    this.config = { ...DEFAULTS, ...config };
    /** @type {Map<string, ManagedProcess>} */
    this.processes = new Map();
    this._ensureTimer = null;
    this._stateStore = config.stateStore || null;
    this._notifyEngine = config.notifyEngine || null;
  }

  // ─── 公共 API ──────────────────────────────────────────────

  /**
   * 注册一个被管进程
   * @param {object} procCfg
   * @param {string} procCfg.id - 进程唯一 ID
   * @param {string} procCfg.name - 显示名称
   * @param {string} procCfg.command - 启动命令
   * @param {string[]} [procCfg.args] - 命令参数
   * @param {string} [procCfg.cwd] - 工作目录
   * @param {object} [procCfg.env] - 环境变量
   * @param {string} [procCfg.healthUrl] - 健康检查 URL
   * @param {number} [procCfg.healthInterval] - 健康检查间隔(ms)
   * @param {string} [procCfg.restartPolicy] - 'always'|'on-failure'|'never'
   * @param {number} [procCfg.maxRestarts] - 最大连续重启
   * @param {boolean} [procCfg.autoStart] - 注册后自动启动
   */
  register(procCfg) {
    if (this.processes.has(procCfg.id)) {
      throw new Error(`Process '${procCfg.id}' already registered`);
    }

    const proc = {
      id: procCfg.id,
      name: procCfg.name || procCfg.id,
      command: procCfg.command,
      args: procCfg.args || [],
      cwd: procCfg.cwd || process.cwd(),
      env: { ...process.env, ...(procCfg.env || {}) },
      healthUrl: procCfg.healthUrl || null,
      healthInterval: procCfg.healthInterval || 30_000,
      restartPolicy: procCfg.restartPolicy || 'on-failure',
      maxRestarts: procCfg.maxRestarts || this.config.maxRestarts,
      autoStart: procCfg.autoStart !== false,

      // 运行时状态
      state: PROCESS_STATES.STOPPED,
      child: null,
      restartCount: 0,
      restartWindow: [],    // 重启时间戳窗口
      lastHealthCheck: null,
      lastHealthStatus: null,
      lastError: null,
      startTime: null,
      stopTime: null,
      pid: null,
      _healthTimer: null,
      _restartTimer: null,
    };

    this.processes.set(procCfg.id, proc);

    if (this._stateStore) {
      this._stateStore.setAgentState(procCfg.id, {
        status: proc.state,
        name: proc.name,
        type: 'managed_process',
        failStreak: 0,
        lastCheck: Date.now(),
      });
    }

    return proc;
  }

  /**
   * 启动指定进程
   */
  async start(procId) {
    const proc = this._getProc(procId);
    if (proc.state === PROCESS_STATES.RUNNING || proc.state === PROCESS_STATES.STARTING) {
      return { ok: false, reason: `Process already ${proc.state}` };
    }

    return this._doStart(proc);
  }

  /**
   * 停止指定进程
   * @param {boolean} [graceful=true] - 优雅关闭（SIGTERM）还是强杀（SIGKILL）
   */
  async stop(procId, graceful = true) {
    const proc = this._getProc(procId);
    if (proc.state === PROCESS_STATES.STOPPED || proc.state === PROCESS_STATES.STOPPING) {
      return { ok: false, reason: `Process already ${proc.state}` };
    }

    return this._doStop(proc, graceful);
  }

  /**
   * 重启指定进程
   */
  async restart(procId) {
    const proc = this._getProc(procId);
    await this._doStop(proc, true);
    return this._doStart(proc);
  }

  /**
   * 获取进程状态
   */
  status(procId) {
    if (procId) {
      return this._getProc(procId);
    }
    // 返回所有进程状态摘要
    const list = [];
    for (const [id, p] of this.processes) {
      list.push({
        id: p.id,
        name: p.name,
        state: p.state,
        pid: p.pid,
        restartCount: p.restartCount,
        lastError: p.lastError,
        uptime: p.startTime ? Date.now() - p.startTime : 0,
        lastHealthCheck: p.lastHealthCheck,
        lastHealthStatus: p.lastHealthStatus,
      });
    }
    return list;
  }

  /**
   * ensure：确保进程在运行，不在就启动（watchdog 核心）
   * 供定时任务调用（每 10 分钟一次，与竞品对齐）
   */
  async ensure(procId = null) {
    const results = [];

    const procs = procId
      ? [this._getProc(procId)]
      : Array.from(this.processes.values());

    for (const proc of procs) {
      // 跳过已停止的和手动停止的
      if (proc.state === PROCESS_STATES.STOPPING) continue;

      if (proc.state === PROCESS_STATES.STOPPED || proc.state === PROCESS_STATES.CRASHED) {
        console.log(`[Lifecycle] ensure: 进程 ${proc.name}(${proc.id}) 状态=${proc.state}，自动重启...`);
        const result = await this._doStart(proc);
        result.ensured = true;
        results.push({ id: proc.id, ...result });
      } else {
        // 进程在运行，做一次健康检查
        const healthy = await this._checkHealth(proc);
        proc.lastHealthCheck = Date.now();
        proc.lastHealthStatus = healthy ? 'healthy' : 'unhealthy';
        results.push({ id: proc.id, state: proc.state, healthy, ensured: false });

        if (!healthy && proc.state === PROCESS_STATES.RUNNING) {
          console.log(`[Lifecycle] ensure: 进程 ${proc.name}(${proc.id}) 运行中但健康检查失败，触发重启...`);
          await this._doStop(proc, true);
          const result = await this._doStart(proc);
          results[results.length - 1] = { id: proc.id, ...result, ensured: true, rehealth: true };
        }
      }
    }

    return results;
  }

  /**
   * 按名称/ID 启动（注册 + 启动一步完成）
   */
  async ensureRegistered(procCfgs) {
    const results = [];
    for (const cfg of procCfgs) {
      if (!this.processes.has(cfg.id)) {
        this.register(cfg);
      }
      const result = await this.start(cfg.id);
      results.push({ id: cfg.id, ...result });
    }
    return results;
  }

  /**
   * 停止所有进程
   */
  async stopAll() {
    const results = [];
    for (const [id, proc] of this.processes) {
      if (proc.state === PROCESS_STATES.RUNNING) {
        results.push(await this._doStop(proc, true));
      }
    }
    return results;
  }

  // ─── 定时 ensure ────────────────────────────────────────────

  /**
   * 启动 ensure 定时器（每 10 分钟，与竞品 watchdog 对齐）
   */
  startEnsureLoop() {
    if (this._ensureTimer) return;
    console.log(`[Lifecycle] Ensure 定时器启动（间隔 ${this.config.ensureInterval / 1000}s）`);
    this._ensureTimer = setInterval(async () => {
      try {
        const results = await this.ensure();
        const restarted = results.filter(r => r.ensured);
        if (restarted.length > 0) {
          console.log(`[Lifecycle] ensure 检查完成: ${restarted.length} 个进程自动恢复`);
          this.emit('ensure:restarted', restarted);
        }
      } catch (err) {
        console.error(`[Lifecycle] ensure 异常: ${err.message}`);
      }
    }, this.config.ensureInterval);
  }

  /**
   * 停止 ensure 定时器
   */
  stopEnsureLoop() {
    if (this._ensureTimer) {
      clearInterval(this._ensureTimer);
      this._ensureTimer = null;
    }
  }

  /**
   * 优雅关闭
   */
  async shutdown() {
    this.stopEnsureLoop();
    await this.stopAll();
    // 清除所有定时器
    for (const [id, proc] of this.processes) {
      if (proc._healthTimer) clearInterval(proc._healthTimer);
      if (proc._restartTimer) clearTimeout(proc._restartTimer);
    }
  }

  // ─── 内部方法 ───────────────────────────────────────────────

  _getProc(procId) {
    const proc = this.processes.get(procId);
    if (!proc) throw new Error(`Process '${procId}' not registered`);
    return proc;
  }

  async _doStart(proc) {
    proc.state = PROCESS_STATES.STARTING;
    proc.lastError = null;

    return new Promise((resolve) => {
      try {
        const child = spawn(proc.command, proc.args, {
          cwd: proc.cwd,
          env: proc.env,
          stdio: ['ignore', 'pipe', 'pipe'],
        });

        proc.child = child;
        proc.pid = child.pid;
        proc.startTime = Date.now();

        // stdout 日志
        child.stdout.on('data', (data) => {
          const lines = data.toString().trim();
          if (lines) {
            this.emit('process:stdout', { id: proc.id, name: proc.name, text: lines });
          }
        });

        // stderr 日志
        child.stderr.on('data', (data) => {
          const lines = data.toString().trim();
          if (lines) {
            this.emit('process:stderr', { id: proc.id, name: proc.name, text: lines });
          }
        });

        // 进程退出
        child.on('exit', (code, signal) => {
          proc.pid = null;
          proc.child = null;
          if (proc._healthTimer) {
            clearInterval(proc._healthTimer);
            proc._healthTimer = null;
          }

          const exitOk = code === 0 || signal === 'SIGTERM' || signal === 'SIGINT';

          if (proc.state === PROCESS_STATES.STOPPING) {
            // 正常停止
            proc.state = PROCESS_STATES.STOPPED;
            proc.stopTime = Date.now();
            this.emit('process:stopped', { id: proc.id, name: proc.name, code, signal });
            return;
          }

          // 异常退出
          proc.state = PROCESS_STATES.CRASHED;
          proc.lastError = `exit code=${code}, signal=${signal || 'none'}`;
          this.emit('process:crashed', { id: proc.id, name: proc.name, code, signal });

          // 判断是否重启
          const shouldRestart = this._shouldRestart(proc);
          if (shouldRestart) {
            this._scheduleRestart(proc);
          } else {
            console.log(`[Lifecycle] 进程 ${proc.name}(${proc.id}) 已达最大重启次数，不再重启`);
            this.emit('process:gaveup', { id: proc.id, name: proc.name, restartCount: proc.restartCount });

            // 推送企微告警
            if (this._notifyEngine) {
              const card = this._notifyEngine.alertCard({
                agentId: proc.id,
                agent: { name: proc.name },
                prevStatus: 'running',
                failCount: proc.restartCount,
                error: `进程已崩溃 ${proc.restartCount} 次，放弃自动重启。错误: ${proc.lastError}`,
              });
              this._notifyEngine.setSender && this.emit('lifecycle:card', card);
            }
          }
        });

        // 进程错误（spawn 失败等）
        child.on('error', (err) => {
          proc.lastError = err.message;
          proc.pid = null;
          proc.child = null;
          proc.state = PROCESS_STATES.CRASHED;
          this.emit('process:error', { id: proc.id, name: proc.name, error: err.message });

          const shouldRestart = this._shouldRestart(proc);
          if (shouldRestart) {
            this._scheduleRestart(proc);
          }
        });

        // 短暂延迟后标记为 running（给进程启动时间）
        setTimeout(() => {
          if (proc.state === PROCESS_STATES.STARTING && proc.child) {
            proc.state = PROCESS_STATES.RUNNING;
            this.emit('process:started', { id: proc.id, name: proc.name, pid: proc.pid });

            // 启动健康检查定时器
            if (proc.healthUrl) {
              proc._healthTimer = setInterval(async () => {
                const healthy = await this._checkHealth(proc);
                proc.lastHealthCheck = Date.now();
                proc.lastHealthStatus = healthy ? 'healthy' : 'unhealthy';

                if (!healthy && proc.state === PROCESS_STATES.RUNNING) {
                  this.emit('process:unhealthy', { id: proc.id, name: proc.name });
                }
              }, proc.healthInterval);
            }
          }
        }, 1000);

        resolve({ ok: true, pid: child.pid });
      } catch (err) {
        proc.state = PROCESS_STATES.CRASHED;
        proc.lastError = err.message;
        resolve({ ok: false, error: err.message });
      }
    });
  }

  async _doStop(proc, graceful) {
    if (!proc.child) {
      proc.state = PROCESS_STATES.STOPPED;
      return { ok: true, reason: 'no child process' };
    }

    proc.state = PROCESS_STATES.STOPPING;

    // 清除健康检查
    if (proc._healthTimer) {
      clearInterval(proc._healthTimer);
      proc._healthTimer = null;
    }

    return new Promise((resolve) => {
      const timeout = setTimeout(() => {
        if (proc.child && proc.state === PROCESS_STATES.STOPPING) {
          console.log(`[Lifecycle] 超时，强制结束进程 ${proc.name}(${proc.id})`);
          proc.child.kill('SIGKILL');
        }
      }, this.config.shutdownTimeout);

      proc.child.once('exit', () => {
        clearTimeout(timeout);
        proc.state = PROCESS_STATES.STOPPED;
        proc.stopTime = Date.now();
        resolve({ ok: true, forced: false });
      });

      try {
        proc.child.kill(graceful ? 'SIGTERM' : 'SIGKILL');
      } catch (err) {
        clearTimeout(timeout);
        proc.state = PROCESS_STATES.STOPPED;
        resolve({ ok: true, error: err.message });
      }
    });
  }

  async _checkHealth(proc) {
    if (!proc.healthUrl) return true; // 无健康检查 URL = 假定健康

    return new Promise((resolve) => {
      const req = http.get(proc.healthUrl, { timeout: this.config.healthTimeout }, (res) => {
        const ok = res.statusCode >= 200 && res.statusCode < 400;
        // 消费 response body 避免内存泄漏
        res.resume();
        res.on('end', () => resolve(ok));
        res.on('error', () => resolve(false));
      });
      req.on('error', () => resolve(false));
      req.on('timeout', () => {
        req.destroy();
        resolve(false);
      });
    });
  }

  _shouldRestart(proc) {
    if (proc.restartPolicy === 'never') return false;
    if (proc.state === PROCESS_STATES.STOPPING) return false;

    // 清理过期重启记录
    const now = Date.now();
    const windowStart = now - this.config.restartWindow;
    proc.restartWindow = proc.restartWindow.filter(ts => ts > windowStart);

    // 检查最大重启次数
    if (proc.restartPolicy === 'on-failure' || proc.restartPolicy === 'always') {
      if (proc.restartWindow.length >= proc.maxRestarts) {
        return false;
      }
    }

    return true;
  }

  _scheduleRestart(proc) {
    proc.state = PROCESS_STATES.RESTARTING;
    proc.restartCount++;
    proc.restartWindow.push(Date.now());

    // 指数退避: 2s, 4s, 8s, 16s, 32s, 64s, 120s(max)
    const delay = Math.min(
      this.config.restartBackoffMin * Math.pow(2, proc.restartCount - 1),
      this.config.restartBackoffMax
    );

    console.log(`[Lifecycle] 进程 ${proc.name}(${proc.id}) 将在 ${delay / 1000}s 后第 ${proc.restartCount} 次重启`);

    proc._restartTimer = setTimeout(async () => {
      proc._restartTimer = null;
      await this._doStart(proc);
      this.emit('process:restarted', {
        id: proc.id,
        name: proc.name,
        restartCount: proc.restartCount,
        delay,
      });
    }, delay);
  }
}

module.exports = { LifecycleManager, PROCESS_STATES };
