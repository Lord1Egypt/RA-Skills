/**
 * 企微 WebSocket 客户端 - 原生 ws 直连（不用有 bug 的 SDK）
 *
 * 关键修复：认证消息使用 bot_id（下划线），而非 SDK 的 botid
 * SDK 参数映射错误导致 errcode 853000，原生 ws 正确传参后 errcode=0
 *
 * 协议：wss://openws.work.weixin.qq.com
 * 参考：https://developer.work.weixin.qq.com/document/path/101039
 */

const WebSocket = require('ws');
const { wecomToStandard } = require('./msg-converter');

class WeComWSClient {
  /**
   * @param {object} opts
   * @param {string} opts.botId      - 智能机器人 bot_id
   * @param {string} opts.botSecret  - 智能机器人 secret
   * @param {string} [opts.wsUrl]    - WebSocket 端点
   */
  constructor({ botId, botSecret, wsUrl = 'wss://openws.work.weixin.qq.com' }) {
    this.botId = botId;
    this.botSecret = botSecret;
    this.wsUrl = wsUrl;

    this._ws = null;
    this._handler = null;        // onMessage callback
    this._connected = false;
    this._authOk = false;
    this._pingTimer = null;
    this._reconnectTimer = null;

    // 统计
    this._messageCount = 0;
    this._errorCount = 0;
    this._lastMessageTime = null;
    this._connectTime = null;

    // 重连控制
    this._reconnectAttempts = 0;
    this._maxReconnect = -1;    // -1 = 无限重连（企微旧session事件可能导致多次断开）
    this._reconnectDelay = 1000; // 起始 1s，指数退避
    this._quickDisconnects = 0;  // 快速断开计数器（10s 内断开算快速）
    this._lastConnectTime = null;
  }

  // ============================================================
  // 公开属性
  // ============================================================
  get isConnected() {
    return this._connected && this._ws && this._ws.readyState === WebSocket.OPEN;
  }

  get stats() {
    return {
      connected: this.isConnected,
      auth_ok: this._authOk,
      message_count: this._messageCount,
      error_count: this._errorCount,
      last_message_time: this._lastMessageTime,
      connect_time: this._connectTime,
      reconnect_attempts: this._reconnectAttempts,
      bot_id: this.botId ? this.botId.slice(0, 8) + '...' : '?',
    };
  }

  // ============================================================
  // 连接管理
  // ============================================================

  /**
   * 建立企微 WebSocket 连接
   * @param {Function} onMessage - async (standardMsg) => void
   * @returns {Promise<boolean>}
   */
  async connect(onMessage) {
    this._handler = onMessage;
    this._reconnectAttempts = 0;

    return this._doConnect();
  }

  async _doConnect() {
    return new Promise((resolve) => {
      try {
        this._ws = new WebSocket(this.wsUrl);
      } catch (e) {
        console.error(`[WS] 创建连接失败: ${e.message}`);
        return resolve(false);
      }

      const timeout = setTimeout(() => {
        if (!this._authOk) {
          console.error('[WS] 认证超时（10s）');
          this._ws.close();
          resolve(false);
        }
      }, 10000);

      this._ws.on('open', () => {
        console.log('[WS] TCP 已连接，发送认证...');
        this._sendAuth();
      });

      this._ws.on('message', (data) => {
        try {
          const frame = JSON.parse(data.toString());
          this._onFrame(frame, timeout, resolve);
        } catch (e) {
          console.error(`[WS] 消息解析失败: ${e.message}`);
        }
      });

      this._ws.on('error', (err) => {
        // 忽略 WebSocket pong 帧错误（服务端同时回 WebSocket pong，opcode 3 非法）
        if (err && err.message && err.message.includes('Invalid WebSocket frame')) {
          return; // 静默忽略
        }
        this._errorCount++;
        console.error(`[WS] 错误: ${err.message}`);
      });

      this._ws.on('close', (code, reason) => {
        clearTimeout(timeout);
        this._connected = false;
        this._authOk = false;
        this._stopPing();
        console.log(`[WS] 已断开 | code=${code} reason=${reason}`);

        // 自动重连
        this._scheduleReconnect();
      });
    });
  }

  // ============================================================
  // 认证
  // ============================================================

  _sendAuth() {
    // 企微智能机器人 WebSocket 协议：订阅命令是 aibot_subscribe，不是 auth！
    // 参考：https://developer.work.weixin.qq.com/document/path/101463
    const reqId = `req_${Date.now()}_${Math.random().toString(36).slice(2, 8)}`;
    this._lastReqId = reqId;
    const authMsg = {
      cmd: 'aibot_subscribe',
      headers: { req_id: reqId },
      body: {
        bot_id: this.botId,        // ✅ bot_id（下划线）
        secret: this.botSecret,
      },
    };
    this._ws.send(JSON.stringify(authMsg));
    console.log(`[WS] → 订阅请求 | bot=${this.botId.slice(0, 8)}... req_id=${reqId}`);
  }

  // ============================================================
  // 帧处理
  // ============================================================

  async _onFrame(frame, timeout, resolve) {
    // aibot_subscribe 响应没有 cmd 字段，通过 errcode 判断
    // 成功响应: {"headers":{"req_id":"..."},"errcode":0,"errmsg":"ok"}
    if (frame.errcode !== undefined && frame.headers && frame.headers.req_id) {
      // 订阅响应
      clearTimeout(timeout);
      const errcode = frame.errcode;
      const errmsg = frame.errmsg || '';

      if (errcode === 0) {
        this._authOk = true;
        this._connected = true;
        this._connectTime = new Date().toISOString();
        this._lastConnectTime = Date.now();  // 记录连接时间用于快速断开检测
        this._reconnectAttempts = 0;
        console.log(`[WS] ✅ 订阅成功 | errcode=${errcode} errmsg="${errmsg}"`);
        this._startPing();
        resolve(true);
      } else {
        console.error(`[WS] ❌ 订阅失败 | errcode=${errcode} errmsg="${errmsg}"`);
        this._ws.close();
        resolve(false);
      }
      return;
    }

    const cmd = frame.cmd;

    if (cmd === 'aibot_msg_callback') {
      // 用户消息
      this._messageCount++;
      this._lastMessageTime = new Date().toISOString();

      const standardMsg = await wecomToStandard(frame);
      // 安全防护：防止 from 缺失（事件帧被当成消息帧处理）
      if (!standardMsg || !standardMsg.from) {
        console.log('[WS] 跳过：消息解析异常，缺少 from 字段');
        return;
      }
      const userId = (standardMsg.from && (standardMsg.from.user_id || standardMsg.from.userid)) || '?';
      const chatId = standardMsg.chat_id || frame.body?.chatid || '?';
      const contentPreview = (standardMsg.content || '').slice(0, 50);

      // 记录最新 chatid（供通知推送使用）
      this._lastChatId = chatId;
      console.log(`[WS] ← 消息 | chatid=${chatId} | from=${userId} | "${contentPreview}"`);

      // 调用外部 handler
      if (this._handler) {
        // 传递原始 frame 以便 reply 时使用 req_id
        this._handler(standardMsg, frame).catch(err => {
          console.error(`[WS] 消息处理异常: ${err.message}`);
        });
      }
      return;
    }

    if (cmd === 'aibot_event_callback') {
      // 事件回调（进入聊天、关注、连接被踢等）
      const body = frame.body || {};
      const eventType = (body.event && body.event.eventtype) || 'unknown';
      const reqId = (frame.headers && frame.headers.req_id) || '';
      console.log(`[WS] ← 事件 | type=${eventType} req_id=${reqId}`);

      // disconnected_event：本连接已被新连接踢掉
      // 不要立即关闭，先打印日志，让重连机制处理
      if (eventType === 'disconnected_event') {
        console.log('[WS] ⚠️ 收到 disconnected_event（可能有其他连接抢占），将持续重连');
        // 不主动关闭，让服务端断开后重连机制自动处理
        return;
      }

      // 可选：通过 handler 通知上层（欢迎语等）
      if (this._handler) {
        const standardMsg = wecomToStandard(frame);
        this._handler(standardMsg, frame).catch(err => {
          console.error(`[WS] 事件处理异常: ${err.message}`);
        });
      }
      return;
    }

    // 其他帧（心跳响应等）
    if (cmd === 'pong') {
      return;
    }

    console.log(`[WS] ← 未知帧 | cmd=${cmd}`);
  }

  // ============================================================
  // 心跳
  // ============================================================

  _startPing() {
    this._stopPing();
    // 企微协议要求：发送 JSON 命令 {"cmd":"ping"}，不是 WebSocket ping 帧
    this._pingTimer = setInterval(() => {
      if (this._ws && this._ws.readyState === WebSocket.OPEN) {
        const pingMsg = {
          cmd: 'ping',
          headers: { req_id: `ping_${Date.now()}_${Math.random().toString(36).slice(2, 8)}` },
        };
        try {
          this._ws.send(JSON.stringify(pingMsg));
        } catch (e) {
          // ignore
        }
      }
    }, 30000); // 每 30 秒
  }

  _stopPing() {
    if (this._pingTimer) {
      clearInterval(this._pingTimer);
      this._pingTimer = null;
    }
  }

  // ============================================================
  // 重连
  // ============================================================

  _scheduleReconnect() {
    if (this._reconnectTimer) return;

    if (this._maxReconnect >= 0 && this._reconnectAttempts >= this._maxReconnect) {
      console.error(`[WS] 已达最大重连次数 (${this._maxReconnect})，停止重连`);
      return;
    }

    // 快速断开检测：连接后 10s 内断开 → 可能是服务端旧 session 冲突 → 加大退避
    const connectDuration = this._lastConnectTime ? Date.now() - this._lastConnectTime : Infinity;
    if (connectDuration < 10000) {
      this._quickDisconnects++;
    } else {
      this._quickDisconnects = 0;
    }

    // 退避策略：正常 1s/2s/4s... 快速断开时 5s 起步翻倍到 120s
    let delay;
    if (this._quickDisconnects > 0) {
      delay = Math.min(5000 * Math.pow(2, this._quickDisconnects - 1), 120000);
      console.log(`[WS] ⚠️ 快速断开 #${this._quickDisconnects}，退避 ${delay/1000}s`);
    } else {
      delay = Math.min(1000 * Math.pow(2, this._reconnectAttempts), 60000);
    }
    this._reconnectAttempts++;

    console.log(`[WS] ${delay/1000}s 后第 ${this._reconnectAttempts} 次重连...`);
    this._reconnectTimer = setTimeout(async () => {
      this._reconnectTimer = null;
      await this._doConnect();
    }, delay);
  }

  // ============================================================
  // 消息发送
  // ============================================================

  /**
   * 被动回复（必须在收到消息的上下文中，使用原始帧的 req_id）
   * @param {object} originalFrame - 原始企微回调帧
   * @param {object} body - 回复消息体（standardToWecomReply 输出）
   */
  reply(originalFrame, body) {
    if (!this.isConnected) {
      console.warn('[WS] 无法回复：未连接');
      return false;
    }

    const reqId = (originalFrame.headers && originalFrame.headers.req_id) || '';
    const replyMsg = {
      cmd: 'aibot_respond_msg',
      headers: { req_id: reqId },
      body: body,
    };

    try {
      this._ws.send(JSON.stringify(replyMsg));
      console.log(`[WS] → 已回复 | req_id=${reqId}`);
      return true;
    } catch (e) {
      console.error(`[WS] 回复失败: ${e.message}`);
      return false;
    }
  }

  /**
   * 主动推送消息（不依赖回调帧）
   *
   * 企微智能机器人 WebSocket 协议支持主动推送：
   * cmd: "aibot_msg_send", body: { chatid, chattype, msgtype, ... }
   *
   * @param {string} chatid - 会话 ID
   * @param {object} body - 消息体
   * @param {number} [chatType=1] - 1=单聊, 2=群聊
   */
  sendMessage(chatid, body, chatType = 1) {
    if (!this.isConnected) {
      console.warn('[WS] 无法推送：未连接');
      return false;
    }

    const pushMsg = {
      cmd: 'aibot_msg_send',
      body: {
        chatid: chatid,
        chattype: chatType,
        ...body,
      },
    };

    try {
      this._ws.send(JSON.stringify(pushMsg));
      console.log(`[WS] → 已推送 | chatid=${chatid.slice(0, 8)}...`);
      return true;
    } catch (e) {
      console.error(`[WS] 推送失败: ${e.message}`);
      return false;
    }
  }

  // ============================================================
  // 断开
  // ============================================================

  async disconnect() {
    this._connected = false;
    this._authOk = false;

    if (this._reconnectTimer) {
      clearTimeout(this._reconnectTimer);
      this._reconnectTimer = null;
    }

    this._stopPing();

    if (this._ws) {
      this._ws.close(1000, 'client disconnect');
      this._ws = null;
    }

    console.log('[WS] 已断开');
  }
}

module.exports = { WeComWSClient };
