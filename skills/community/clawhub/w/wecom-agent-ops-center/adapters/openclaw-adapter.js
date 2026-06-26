#!/usr/bin/env node

/**
 * 企微 Agent Ops Center — OpenClaw 适配器
 * 架构位置：L0 数据源适配层
 *
 * 专为 OpenClaw 自托管用户设计
 * 监控维度：
 *   - 健康检查：OpenClaw 自托管实例 HTTP API
 *   - 自托管稳定性：进程存活、磁盘空间、版本兼容
 *   - 资源采集：CPU/内存/磁盘（自托管特有）
 *   - 版本追踪：升级前后快照对比
 *
 * OpenClaw vs WorkBuddy 关键差异：
 *   - OpenClaw 是用户自己部署的服务器应用
 *   - 稳定性风险更高（服务器宕机、依赖冲突、磁盘满）
 *   - 需要自托管级别的监控维度
 */

const { BaseAdapter } = require('./base-adapter');
const { execSync } = require('child_process');

const DEFAULTS = {
  healthPath: '/health',
  healthInterval: 20_000,     // 自托管更频繁检查（20s vs 30s）
  healthTimeout: 10_000,
  resourceInterval: 30_000,   // 资源采集更频繁
  diskCheckInterval: 300_000, // 磁盘检查每 5 分钟
  versionCheck: true,         // 是否追踪版本
};

class OpenClawAdapter extends BaseAdapter {
  constructor(config) {
    super(config);
    this.options    = { ...DEFAULTS, ...(config.options || {}) };
    this.apiKey     = config.apiKey || config.agent?.apiKey || '';
    this.selfHosted = config.agent?.selfHosted !== undefined ? config.agent.selfHosted : true;
    this.version    = config.agent?.version || 'unknown';
    this.healthUrl  = config.healthUrl || `${this.endpoint}${this.options.healthPath}`;

    // 自托管特有状态
    this._lastVersion   = this.version;
    this._versionHistory = [{ version: this.version, timestamp: Date.now() }];
  }

  // ─── 注册 ──────────────────────────────────────────────────

  async register() {
    const base = await super.register();

    // 检测安装方式
    let installType = 'unknown';
    try {
      execSync('which pm2', { stdio: 'ignore' });
      installType = 'pm2';
    } catch {
      try {
        execSync('which systemctl', { stdio: 'ignore' });
        installType = 'systemd';
      } catch {
        installType = 'manual';
      }
    }

    console.log(`[OpenClawAdapter:${this.id}] Detected install type: ${installType}, version: ${this.version}`);
    return {
      ...base,
      selfHosted: true,
      installType,
      version: this.version,
    };
  }

  // ─── 健康检查 ──────────────────────────────────────────────

  setupHealthCheck() {
    const interval = this.options.healthInterval;
    console.log(`[OpenClawAdapter:${this.id}] Health check every ${interval / 1000}s → ${this.healthUrl}`);

    this._addInterval(async () => {
      const result = await this._httpHealthCheck(this.healthUrl, this.options.healthTimeout);
      this.emit('health', {
        agentId: this.agentId,
        agentName: this.agentName,
        adapterType: this.type,
        healthy: result.healthy,
        latency: result.latency,
        status: result.status,
        statusCode: result.statusCode,
        error: result.error,
        selfHosted: true,
        version: this.version,
      });
    }, interval);
  }

  // ─── 资源采集 ──────────────────────────────────────────────

  setupResourceCollector() {
    // 1. API 资源指标
    const resInterval = this.options.resourceInterval;
    console.log(`[OpenClawAdapter:${this.id}] Resource collection every ${resInterval / 1000}s`);

    this._addInterval(async () => {
      try {
        const res = await this._fetchResourceMetrics();
        if (res) {
          this.emit('resource', {
            agentId: this.agentId,
            agentName: this.agentName,
            adapterType: this.type,
            timestamp: Date.now(),
            selfHosted: true,
            ...res,
          });
        }
      } catch (err) {
        console.debug(`[OpenClawAdapter:${this.id}] Resource fetch failed: ${err.message}`);
      }
    }, resInterval);

    // 2. 磁盘空间（自托管特有）
    if (this.selfHosted) {
      const diskInterval = this.options.diskCheckInterval;
      console.log(`[OpenClawAdapter:${this.id}] Disk check every ${diskInterval / 1000}s`);

      this._addInterval(() => {
        try {
          const disk = this._checkDiskSpace();
          if (disk) {
            this.emit('resource', {
              agentId: this.agentId,
              agentName: this.agentName,
              adapterType: this.type,
              timestamp: Date.now(),
              metric: 'disk',
              selfHosted: true,
              ...disk,
            });

            // 磁盘空间告警（< 10%）
            if (disk.usedPercent > 90) {
              this.emit('alert', {
                agentId: this.agentId,
                agentName: this.agentName,
                type: 'disk_critical',
                message: `磁盘空间不足！已用 ${disk.usedPercent}%，剩余 ${disk.available}`,
                severity: 'critical',
              });
            } else if (disk.usedPercent > 80) {
              this.emit('alert', {
                agentId: this.agentId,
                agentName: this.agentName,
                type: 'disk_warning',
                message: `磁盘空间预警：已用 ${disk.usedPercent}%`,
                severity: 'warning',
              });
            }
          }
        } catch (err) {
          console.debug(`[OpenClawAdapter:${this.id}] Disk check failed: ${err.message}`);
        }
      }, diskInterval);
    }

    // 3. 版本追踪
    if (this.options.versionCheck) {
      this._addInterval(async () => {
        try {
          const newVersion = await this._checkVersion();
          if (newVersion && newVersion !== this._lastVersion) {
            const change = {
              from: this._lastVersion,
              to: newVersion,
              timestamp: Date.now(),
            };
            this._versionHistory.push(change);
            this._lastVersion = newVersion;
            this.version = newVersion;

            console.log(`[OpenClawAdapter:${this.id}] Version changed: ${change.from} → ${change.to}`);

            this.emit('version_change', {
              agentId: this.agentId,
              agentName: this.agentName,
              ...change,
            });
          }
        } catch (err) {
          console.debug(`[OpenClawAdapter:${this.id}] Version check failed: ${err.message}`);
        }
      }, 600_000); // 每 10 分钟
    }
  }

  // ─── 任务监听 ──────────────────────────────────────────────

  setupTaskListener() {
    // OpenClaw 的任务事件由 TaskTracker 的 HTTP API 接收
    console.log(`[OpenClawAdapter:${this.id}] Task events handled by TaskTracker API`);
  }

  // ─── Agent 信息查询 ────────────────────────────────────────

  async queryAgentInfo() {
    const base = await super.queryAgentInfo();
    return {
      ...base,
      selfHosted: this.selfHosted,
      version: this.version,
      versionHistory: this._versionHistory,
      platform: 'openclaw-self-hosted',
      features: ['health_check', 'task_tracking', 'resource_monitoring', 'disk_monitoring', 'version_tracking'],
    };
  }

  /**
   * 获取版本历史
   */
  getVersionHistory() {
    return [...this._versionHistory];
  }

  // ─── 内部方法 ──────────────────────────────────────────────

  async _fetchResourceMetrics() {
    const headers = {};
    if (this.apiKey) {
      headers['Authorization'] = `Bearer ${this.apiKey}`;
    }

    const endpoints = [
      `${this.endpoint}/api/resources`,
      `${this.endpoint}/api/stats`,
      `${this.endpoint}/status`,
    ];

    for (const url of endpoints) {
      try {
        const controller = new AbortController();
        const timer = setTimeout(() => controller.abort(), 5000);

        const response = await fetch(url, {
          method: 'GET',
          headers,
          signal: controller.signal,
        });
        clearTimeout(timer);

        if (response.ok) {
          const data = await response.json();
          return {
            cpu: data.cpu || data.cpuPercent || null,
            memory: data.memory || data.memPercent || null,
            memoryUsed: data.memoryUsed || data.memUsed || null,
            memoryTotal: data.memoryTotal || data.memTotal || null,
            queueDepth: data.queueDepth || data.queue || null,
            concurrency: data.concurrency || data.concurrent || null,
            uptime: data.uptime || null,
            raw: data,
          };
        }
      } catch (err) {
        continue;
      }
    }

    return null;
  }

  /**
   * 检查磁盘空间（自托管）
   */
  _checkDiskSpace() {
    try {
      // macOS / Linux: df -h /
      const output = execSync("df -h / | tail -1", { encoding: 'utf-8' }).trim();
      const parts = output.split(/\s+/);
      // Parts: Filesystem  Size  Used  Avail  Capacity  Mounted
      if (parts.length >= 5) {
        const usedPercent = parseInt(parts[4].replace('%', ''));
        return {
          filesystem: parts[0],
          size: parts[1],
          used: parts[2],
          available: parts[3],
          usedPercent,
        };
      }
    } catch (err) {
      console.debug(`[OpenClawAdapter:${this.id}] Disk check not available: ${err.message}`);
    }
    return null;
  }

  /**
   * 检查 OpenClaw 版本
   */
  async _checkVersion() {
    // 尝试从 API 获取版本
    const headers = {};
    if (this.apiKey) {
      headers['Authorization'] = `Bearer ${this.apiKey}`;
    }

    try {
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), 5000);

      const response = await fetch(`${this.endpoint}/api/version`, {
        method: 'GET',
        headers,
        signal: controller.signal,
      });
      clearTimeout(timer);

      if (response.ok) {
        const data = await response.json();
        return data.version || data.appVersion || null;
      }
    } catch (err) {
      // 版本检查不是关键路径
    }

    // 尝试从 /status 获取
    try {
      const controller = new AbortController();
      const timer = setTimeout(() => controller.abort(), 5000);
      const response = await fetch(`${this.endpoint}/status`, {
        signal: controller.signal,
      });
      clearTimeout(timer);
      if (response.ok) {
        const data = await response.json();
        return data.version || null;
      }
    } catch (err) {
      // ignore
    }

    return null;
  }
}

module.exports = { OpenClawAdapter };
