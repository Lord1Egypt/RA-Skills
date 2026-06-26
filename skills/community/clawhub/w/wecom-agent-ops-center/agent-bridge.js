/**
 * Agent 桥接层 - 将标准化 JSON 转发到用户 Agent 的 HTTP 端点
 *
 * 职责：
 * 1. POST 标准化 JSON → Agent HTTP 端点
 * 2. 接收 Agent 的 JSON 响应
 * 3. 重试 / 超时处理
 */

class AgentBridge {
  /**
   * @param {object} opts
   * @param {string} opts.endpoint  - Agent HTTP URL
   * @param {number} [opts.timeout] - 超时秒数（默认 30）
   * @param {number} [opts.retry]   - 重试次数（默认 3）
   */
  constructor({ endpoint, timeout = 30, retry = 3 }) {
    this.endpoint = endpoint;
    this.timeout = timeout * 1000; // 转为毫秒
    this.retry = retry;

    this._callCount = 0;
    this._errorCount = 0;
    this._totalLatencyMs = 0;
  }

  get stats() {
    const avgLatency = this._callCount > 0
      ? Math.round(this._totalLatencyMs / this._callCount)
      : 0;
    return {
      endpoint: this.endpoint,
      calls: this._callCount,
      errors: this._errorCount,
      avg_latency_ms: avgLatency,
    };
  }

  /**
   * 转发消息到 Agent 端点
   * @param {object} standardMsg - 标准化 JSON
   * @returns {Promise<object|null>} Agent 回复，或 null
   */
  async forward(standardMsg) {
    let lastError = null;

    for (let attempt = 0; attempt < this.retry; attempt++) {
      try {
        const controller = new AbortController();
        const timeoutId = setTimeout(() => controller.abort(), this.timeout);

        const start = Date.now();
        const resp = await fetch(this.endpoint, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(standardMsg),
          signal: controller.signal,
        });
        clearTimeout(timeoutId);

        const latency = Date.now() - start;
        this._callCount++;
        this._totalLatencyMs += latency;

        if (resp.status === 200) {
          const reply = await resp.json();
          console.log(`[Agent] → 响应 | ${resp.status} | ${latency}ms | ${JSON.stringify(reply).slice(0, 80)}`);
          return reply;
        } else if (resp.status === 204) {
          // Agent 不想回复（只看不说）
          console.log(`[Agent] → 无回复 (204)`);
          return null;
        } else {
          lastError = `HTTP ${resp.status}`;
          console.warn(`[Agent] 错误: ${resp.status} (第 ${attempt + 1} 次)`);
        }
      } catch (e) {
        if (e.name === 'AbortError') {
          lastError = '超时';
          console.warn(`[Agent] 超时 (${this.timeout / 1000}s) (第 ${attempt + 1} 次)`);
        } else if (e.cause && e.cause.code === 'ECONNREFUSED') {
          lastError = '连接被拒绝';
          console.warn(`[Agent] 不可达: ${this.endpoint} (第 ${attempt + 1} 次)`);
        } else {
          lastError = e.message.slice(0, 80);
          console.error(`[Agent] 异常: ${e.message} (第 ${attempt + 1} 次)`);
        }
      }

      // 退避：1s, 2s, 3s...
      if (attempt < this.retry - 1) {
        await new Promise(r => setTimeout(r, (attempt + 1) * 1000));
      }
    }

    this._errorCount++;
    console.error(`[Agent] 转发失败 (${this.retry} 次重试后): ${lastError}`);
    return null;
  }
}

module.exports = { AgentBridge };
