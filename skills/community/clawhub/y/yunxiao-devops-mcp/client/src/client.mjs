/**
 * MCP SSE 客户端 - 面向 AI agent 优化
 *
 * 特性：
 * 1. 连接复用 - 保持 SSE 长连接
 * 2. 可靠响应 - 每个请求独立 Promise，避免响应串台
 * 3. 自动重连 - SSE 断线后自动重连
 * 4. 纯 JSON 输出 - stdout 仅输出结构化数据，日志走 stderr
 */

import { createParser } from 'eventsource-parser';

export class YunxiaoMCPClient {
  /**
   * @param {object} options
   * @param {string} [options.baseUrl='http://localhost:3000']
   * @param {number} [options.maxRetries=3]
   * @param {number} [options.retryDelay=1000] - ms
   * @param {number} [options.requestTimeout=60000] - ms
   * @param {boolean} [options.debug=false]
   */
  constructor({
    baseUrl = 'http://localhost:3000',
    maxRetries = 3,
    retryDelay = 1000,
    requestTimeout = 60000,
    debug = false,
  } = {}) {
    this.baseUrl = baseUrl.replace(/\/+$/, '');
    this.maxRetries = maxRetries;
    this.retryDelay = retryDelay;
    this.requestTimeout = requestTimeout;
    this.debug = debug;

    this.sessionId = null;
    this.messageEndpoint = null;
    this.tools = [];

    this._requestId = 0;
    this._pendingRequests = new Map(); // id -> { resolve, reject, timer }
    this._sseAbort = null;
    this._sseReady = null; // { resolve, reject }
    this._connected = false;
    this._initialized = false;
  }

  _log(msg) {
    if (this.debug) {
      console.error(`[yunxiao] ${msg}`);
    }
  }

  /**
   * 连接并初始化 MCP 会话
   * @returns {Promise<boolean>}
   */
  async connect() {
    this._log(`connecting to ${this.baseUrl}/sse`);

    // 启动 SSE 监听
    const ready = new Promise((resolve, reject) => {
      this._sseReady = { resolve, reject };
    });

    this._startSseLoop();

    // 等待 SSE endpoint 就绪
    const timeout = setTimeout(() => {
      if (this._sseReady) {
        this._sseReady.reject(new Error('SSE connection timeout'));
        this._sseReady = null;
      }
    }, 10000);

    try {
      await ready;
    } catch (e) {
      this._log(`SSE connection failed: ${e.message}`);
      clearTimeout(timeout);
      await this.close();
      return false;
    }
    clearTimeout(timeout);

    if (!this.messageEndpoint) {
      this._log('failed to obtain session');
      await this.close();
      return false;
    }

    // MCP 初始化握手
    const initResult = await this._sendRequest('initialize', {
      protocolVersion: '2024-11-05',
      capabilities: {},
      clientInfo: { name: 'yunxiao-mcp-client', version: '0.2.0' },
    });

    if (!initResult) {
      this._log('MCP initialize failed');
      await this.close();
      return false;
    }

    this._log('MCP session initialized');
    this._initialized = true;

    // 获取工具列表
    const toolsResult = await this._sendRequest('tools/list');
    if (toolsResult && toolsResult.tools) {
      this.tools = toolsResult.tools.map((t) => ({
        name: t.name,
        description: t.description || '',
        inputSchema: t.inputSchema || {},
      }));
      this._log(`discovered ${this.tools.length} tools`);
    }

    this._connected = true;
    return true;
  }

  /**
   * 列出所有工具
   * @returns {Array<{name: string, description: string, inputSchema: object}>}
   */
  listTools() {
    return this.tools;
  }

  /**
   * 调用 MCP 工具
   * @param {string} toolName
   * @param {object} [args={}]
   * @returns {Promise<any>}
   */
  async callTool(toolName, args = {}) {
    const result = await this._sendRequest('tools/call', {
      name: toolName,
      arguments: args,
    });

    if (!result) return null;

    // 提取 content 中的文本并尝试解析为 JSON
    const content = result.content;
    if (Array.isArray(content)) {
      let text = '';
      for (const block of content) {
        if (block.type === 'text') {
          text += block.text || '';
        }
      }
      const trimmed = text.trim();
      if (trimmed.startsWith('[') || trimmed.startsWith('{')) {
        try {
          return JSON.parse(trimmed);
        } catch {
          // not JSON, return raw text
        }
      }
      return text;
    }

    return result;
  }

  /**
   * 关闭连接
   */
  async close() {
    this._connected = false;
    if (this._sseAbort) {
      this._sseAbort.abort();
      this._sseAbort = null;
    }
    // reject all pending requests
    for (const [id, pending] of this._pendingRequests) {
      clearTimeout(pending.timer);
      pending.reject(new Error('client closed'));
    }
    this._pendingRequests.clear();
  }

  // ---- internal ----

  _nextRequestId() {
    return ++this._requestId;
  }

  _startSseLoop() {
    this._sseAbort = new AbortController();
    this._runSseLoop(this._sseAbort.signal);
  }

  async _runSseLoop(signal) {
    while (!signal.aborted) {
      try {
        const response = await fetch(`${this.baseUrl}/sse`, {
          headers: { Accept: 'text/event-stream' },
          signal,
        });

        if (!response.ok) {
          throw new Error(`SSE HTTP ${response.status}`);
        }

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        const parser = createParser({
          onEvent: (event) => {
            if (event.event === 'endpoint') {
              this.messageEndpoint = event.data;
              const match = event.data.match(/sessionId=([^&]+)/);
              if (match) this.sessionId = match[1];
              this._log(`session: ${this.sessionId}`);
              if (this._sseReady) {
                this._sseReady.resolve();
                this._sseReady = null;
              }
            } else if (event.event === 'message') {
              try {
                const data = JSON.parse(event.data);
                this._dispatchResponse(data);
              } catch {
                // ignore non-JSON messages
              }
            }
          },
        });

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          parser.feed(decoder.decode(value, { stream: true }));
        }
      } catch (e) {
        if (signal.aborted) break;
        if (this._connected) {
          this._log(`SSE disconnected, reconnecting... (${e.message})`);
          await this._sleep(1000);
        } else {
          if (this._sseReady) {
            this._sseReady.reject(e);
            this._sseReady = null;
          }
          break;
        }
      }
    }
  }

  _dispatchResponse(data) {
    const reqId = data.id;
    if (reqId == null) return;

    const pending = this._pendingRequests.get(reqId);
    if (pending) {
      clearTimeout(pending.timer);
      this._pendingRequests.delete(reqId);

      if (data.error) {
        pending.reject(new Error(JSON.stringify(data.error)));
      } else {
        pending.resolve(data.result);
      }
    }
  }

  /**
   * 发送 JSON-RPC 请求并等待响应
   * @param {string} method
   * @param {object} [params]
   * @returns {Promise<any>}
   */
  async _sendRequest(method, params = undefined) {
    if (!this.messageEndpoint) return null;

    const requestId = this._nextRequestId();
    const payload = {
      jsonrpc: '2.0',
      id: requestId,
      method,
    };
    if (params !== undefined) {
      payload.params = params;
    }

    const url = `${this.baseUrl}${this.messageEndpoint}`;

    // 创建响应 Promise
    const responsePromise = new Promise((resolve, reject) => {
      const timer = setTimeout(() => {
        this._pendingRequests.delete(requestId);
        reject(new Error(`request timeout (id=${requestId})`));
      }, this.requestTimeout);

      this._pendingRequests.set(requestId, { resolve, reject, timer });
    });

    // 带重试的 POST 请求
    for (let attempt = 0; attempt < this.maxRetries; attempt++) {
      try {
        const response = await fetch(url, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(payload),
        });

        if (response.status === 200 || response.status === 202) {
          // POST 成功，等待 SSE 回传响应
          try {
            return await responsePromise;
          } catch (e) {
            this._log(`request error (${method}): ${e.message}`);
            return null;
          }
        } else {
          this._log(`POST status: ${response.status}`);
        }
      } catch (e) {
        if (attempt < this.maxRetries - 1) {
          await this._sleep(this.retryDelay * (attempt + 1));
          continue;
        }
        this._log(`request failed (${method}): ${e.message}`);
        // 清理 pending
        const pending = this._pendingRequests.get(requestId);
        if (pending) {
          clearTimeout(pending.timer);
          this._pendingRequests.delete(requestId);
        }
        return null;
      }
    }

    return null;
  }

  _sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
}

/**
 * 创建并连接客户端
 * @param {string} [baseUrl='http://localhost:3000']
 * @param {object} [options]
 * @param {boolean} [options.debug=false]
 * @returns {Promise<YunxiaoMCPClient>}
 */
export async function createClient(baseUrl = 'http://localhost:3000', options = {}) {
  const client = new YunxiaoMCPClient({ baseUrl, ...options });
  await client.connect();
  return client;
}
