/**
 * 企微 Agent Connector — P2P 路由器（Connector 端）
 *
 * 负责与配对服务器通信，管理 P2P 配对和消息路由。
 *
 * 用法：
 *   const { P2PRouter } = require('./p2p-router');
 *   const p2p = new P2PRouter({ serverUrl: 'https://www.hermesai.ltd' });
 *   await p2p.connect();
 *   const { code } = await p2p.generateCode();
 *   // ... 对方用 code 加入后 ...
 *   p2p.onPeerMessage((msg) => { ... });
 *   p2p.sendToPeer(peerId, { type: 'purchase_order', ... });
 */

const crypto = require('crypto');
const WebSocket = require('ws');

class P2PRouter {
  constructor(options = {}) {
    this.serverUrl = options.serverUrl || 'https://www.hermesai.ltd';
    this.connectorId = options.connectorId || `conn_${Date.now()}_${crypto.randomBytes(4).toString('hex')}`;
    this.peerInfo = options.peerInfo || { version: '1.0.0', hostname: require('os').hostname() };
    this._ws = null;
    this._peers = new Map();        // peerId → { id, peer_info, channel }
    this._messageHandlers = [];     // 注册的消息处理回调
    this._pairingHandlers = [];     // 注册的配对状态回调
    this._pendingPairings = new Map(); // code → { status, peer }
    this._connected = false;
    this._reconnectTimer = null;
  }

  // ============================================================
  // 连接配对服务器
  // ============================================================

  async connect() {
    const wsUrl = this.serverUrl.replace(/^http/, 'ws') + '/ws';
    console.log(`[P2P] 正在连接配对服务器: ${wsUrl}`);

    return new Promise((resolve) => {
      const timeout = setTimeout(() => {
        console.error('[P2P] 连接超时');
        this._connected = false;
        resolve(false);
      }, 10000);

      this._ws = new WebSocket(wsUrl);

      this._ws.on('open', () => {
        clearTimeout(timeout);
        console.log('[P2P] TCP 已连接，正在注册...');
        this._send({ type: 'register', connector_id: this.connectorId });
      });

      this._ws.on('message', (data) => {
        try {
          const msg = JSON.parse(data.toString());
          this._handleMessage(msg, timeout, resolve);
        } catch (e) {
          console.error('[P2P] 消息解析失败:', e.message);
        }
      });

      this._ws.on('close', () => {
        this._connected = false;
        console.log('[P2P] WebSocket 已断开');
        this._scheduleReconnect();
      });

      this._ws.on('error', (err) => {
        console.error('[P2P] WebSocket 错误:', err.message);
        if (!this._connected) {
          clearTimeout(timeout);
          resolve(false);
        }
      });
    });
  }

  /**
   * 处理来自配对服务器的消息
   */
  _handleMessage(msg, timeout, resolve) {
    switch (msg.type) {
      case 'registered': {
        this._connected = true;
        if (timeout) clearTimeout(timeout);
        console.log(`[P2P] ✅ 已注册到配对服务器 (id: ${this.connectorId.slice(0, 10)}...)`);
        if (resolve) resolve(true);
        break;
      }

      case 'peer_joined': {
        // 对方加入了我们的配对码
        const peer = msg.peer;
        this._peers.set(peer.id, peer);
        this._pendingPairings.set(msg.code, { status: 'connected', peer });

        // 同时保存对方信息以便建立直连通道
        if (peer.peer_info && peer.peer_info.p2p_port) {
          console.log(`[P2P] 对方已加入配对 ${msg.code} | peer=${peer.id.slice(0, 10)}... p2p_port=${peer.peer_info.p2p_port}`);
        } else {
          console.log(`[P2P] 对方已加入配对 ${msg.code} | peer=${peer.id.slice(0, 10)}...`);
        }

        // 尝试建立 P2P 直连通道
        this._establishPeerChannel(peer);

        // 通知回调
        this._pairingHandlers.forEach(h => h({ type: 'peer_joined', code: msg.code, peer }));
        break;
      }

      case 'pairing_confirmed': {
        // 我们用配对码加入成功
        const peer = msg.peer;
        this._peers.set(peer.id, peer);
        this._pendingPairings.set(msg.code, { status: 'connected', peer });

        console.log(`[P2P] 配对 ${msg.code} 确认 | peer=${peer.id.slice(0, 10)}...`);

        // 尝试建立 P2P 直连通道
        this._establishPeerChannel(peer);

        this._pairingHandlers.forEach(h => h({ type: 'pairing_confirmed', code: msg.code, peer }));
        break;
      }

      case 'peer_disconnected': {
        const pairing = this._pendingPairings.get(msg.code);
        if (pairing) {
          this._peers.delete(pairing.peer?.id);
          this._pendingPairings.delete(msg.code);
        }
        console.log(`[P2P] 配对 ${msg.code} 已断开`);
        this._pairingHandlers.forEach(h => h({ type: 'peer_disconnected', code: msg.code }));
        break;
      }

      case 'pairing_expired': {
        this._pendingPairings.delete(msg.code);
        console.log(`[P2P] 配对码 ${msg.code} 已过期`);
        this._pairingHandlers.forEach(h => h({ type: 'pairing_expired', code: msg.code }));
        break;
      }

      case 'relay': {
        // 从服务器中继过来的对方消息（直连不通时的兜底）
        const fromId = msg.from_id;
        console.log(`[P2P] ← 中继消息 from=${fromId.slice(0, 10)}...`);
        this._messageHandlers.forEach(h => h({
          from: fromId,
          payload: msg.payload,
          channel: 'relay',
        }));
        break;
      }

      case 'relay_error': {
        console.warn(`[P2P] 中继失败 → ${msg.target_id.slice(0, 10)}...: ${msg.error}`);
        break;
      }

      case 'signal': {
        // WebRTC 信令（未来扩展）
        console.log(`[P2P] ← 信令: ${msg.signal_type} from=${msg.from_id.slice(0, 10)}...`);
        break;
      }

      default:
        console.log(`[P2P] 未知消息: ${msg.type}`);
    }
  }

  // ============================================================
  // P2P 直连通道建立
  // ============================================================

  /**
   * 尝试与对方建立 P2P 直连通道。
   * 如果对方提供了 p2p_port，尝试 HTTP 直连。
   * 否则走服务器中继。
   */
  async _establishPeerChannel(peer) {
    const p2pPort = peer.peer_info?.p2p_port;
    const p2pHost = peer.peer_info?.p2p_host;

    if (p2pPort && p2pHost) {
      // 尝试建立直连
      console.log(`[P2P] 尝试直连 ${p2pHost}:${p2pPort}...`);
      try {
        // 简单健康检查确认对方可达
        const http = require('http');
        const checkUrl = `http://${p2pHost}:${p2pPort}/health`;
        const ok = await new Promise((resolve) => {
          const req = http.get(checkUrl, { timeout: 3000 }, (res) => {
            resolve(res.statusCode === 200);
          });
          req.on('error', () => resolve(false));
          req.on('timeout', () => { req.destroy(); resolve(false); });
        });

        if (ok) {
          peer.channel = 'direct';
          console.log(`[P2P] ✅ 直连通道建立: ${p2pHost}:${p2pPort}`);
        } else {
          peer.channel = 'relay';
          console.log('[P2P] ⚠️ 直连不可达，走服务器中继');
        }
      } catch (e) {
        peer.channel = 'relay';
        console.log('[P2P] ⚠️ 直连失败，走服务器中继');
      }
    } else {
      peer.channel = 'relay';
      console.log('[P2P] 对方未提供直连端口，走服务器中继');
    }

    this._peers.set(peer.id, peer);
  }

  // ============================================================
  // 配对码操作
  // ============================================================

  /**
   * 生成配对码（我是创建者）
   */
  async generateCode() {
    const body = JSON.stringify({
      connector_id: this.connectorId,
      peer_info: this.peerInfo,
    });

    try {
      const resp = await fetch(`${this.serverUrl}/pair/generate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body,
      });

      if (!resp.ok) {
        const err = await resp.json();
        throw new Error(err.message || `HTTP ${resp.status}`);
      }

      const result = await resp.json();
      this._pendingPairings.set(result.code, { status: 'waiting', peer: null });

      console.log(`[P2P] 配对码: ${result.code} (${result.expires_in}s 有效)`);
      console.log(`[P2P] 分享这个码给对方: ${result.code}`);

      return result;
    } catch (e) {
      console.error('[P2P] 生成配对码失败:', e.message);
      throw e;
    }
  }

  /**
   * 使用配对码加入（我是加入者）
   */
  async joinWithCode(code) {
    const body = JSON.stringify({
      code,
      connector_id: this.connectorId,
      peer_info: this.peerInfo,
    });

    try {
      const resp = await fetch(`${this.serverUrl}/pair/join`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body,
      });

      if (!resp.ok) {
        const err = await resp.json();
        throw new Error(err.message || `HTTP ${resp.status}`);
      }

      const result = await resp.json();
      console.log(`[P2P] ✅ 已加入配对 ${code}`);
      return result;
    } catch (e) {
      console.error('[P2P] 加入配对失败:', e.message);
      throw e;
    }
  }

  /**
   * 查询配对码状态
   */
  async getStatus(code) {
    try {
      const resp = await fetch(`${this.serverUrl}/pair/status/${code}`);
      return await resp.json();
    } catch (e) {
      console.error('[P2P] 查询状态失败:', e.message);
      return null;
    }
  }

  /**
   * 断开配对
   */
  async disconnect(code) {
    const body = JSON.stringify({ code, connector_id: this.connectorId });
    try {
      const resp = await fetch(`${this.serverUrl}/pair/disconnect`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body,
      });
      const result = await resp.json();
      this._pendingPairings.delete(code);
      return result;
    } catch (e) {
      console.error('[P2P] 断开配对失败:', e.message);
      return null;
    }
  }

  // ============================================================
  // P2P 消息收发
  // ============================================================

  /**
   * 发送消息给指定 peer
   */
  sendToPeer(peerId, payload) {
    const peer = this._peers.get(peerId);
    if (!peer) {
      console.warn(`[P2P] peer 不存在: ${peerId.slice(0, 10)}...`);
      return false;
    }

    if (peer.channel === 'direct') {
      // 直连 HTTP 发送
      this._sendDirect(peer, payload);
    } else {
      // 走服务器中继
      this._sendRelay(peerId, payload);
    }
    return true;
  }

  /**
   * 广播消息给所有已配对 peer
   */
  broadcastToPeers(payload) {
    for (const [peerId, peer] of this._peers) {
      this.sendToPeer(peerId, payload);
    }
  }

  _sendDirect(peer, payload) {
    const { p2p_host, p2p_port } = peer.peer_info;
    const http = require('http');
    const body = JSON.stringify({
      from_connector: this.connectorId,
      payload,
    });

    const req = http.request({
      hostname: p2p_host,
      port: p2p_port,
      path: '/p2p/message',
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      timeout: 5000,
    }, (res) => {
      if (res.statusCode !== 200) {
        console.warn(`[P2P] 直连发送失败 HTTP ${res.statusCode}，降级中继`);
        this._sendRelay(peer.id, payload);
      }
    });

    req.on('error', () => {
      console.warn('[P2P] 直连不可达，降级中继');
      peer.channel = 'relay';
      this._sendRelay(peer.id, payload);
    });

    req.write(body);
    req.end();
  }

  _sendRelay(peerId, payload) {
    if (!this._ws || this._ws.readyState !== WebSocket.OPEN) {
      console.warn('[P2P] 信令 WebSocket 未连接，无法中继');
      return;
    }
    this._send({
      type: 'relay',
      target_id: peerId,
      payload,
    });
  }

  // ============================================================
  // 事件注册
  // ============================================================

  /**
   * 注册收到 P2P 消息时的回调
   */
  onPeerMessage(handler) {
    this._messageHandlers.push(handler);
    return () => {
      this._messageHandlers = this._messageHandlers.filter(h => h !== handler);
    };
  }

  /**
   * 注册配对状态变化的回调
   */
  onPairingChange(handler) {
    this._pairingHandlers.push(handler);
    return () => {
      this._pairingHandlers = this._pairingHandlers.filter(h => h !== handler);
    };
  }

  // ============================================================
  // 内部辅助
  // ============================================================

  _send(msg) {
    if (this._ws && this._ws.readyState === WebSocket.OPEN) {
      this._ws.send(JSON.stringify(msg));
    }
  }

  _scheduleReconnect() {
    if (this._reconnectTimer) return;
    this._reconnectTimer = setTimeout(async () => {
      this._reconnectTimer = null;
      console.log('[P2P] 尝试重连配对服务器...');
      await this.connect();
    }, 5000);
  }

  get isConnected() {
    return this._connected;
  }

  get peers() {
    return Array.from(this._peers.values());
  }

  get stats() {
    return {
      connected: this._connected,
      connector_id: this.connectorId,
      server_url: this.serverUrl,
      peers_count: this._peers.size,
      peers: this.peers.map(p => ({
        id: p.id.slice(0, 10),
        channel: p.channel || 'pending',
        hostname: p.peer_info?.hostname,
      })),
      pending_pairings: Array.from(this._pendingPairings.keys()),
    };
  }
}

// ============================================================
// P2P 消息接收端点（对方直连发过来时用）
// 这是一个简单的 HTTP 服务器，接收对方的直连消息
// ============================================================

function startP2PInboundServer(port, onMessage) {
  const http = require('http');
  const server = http.createServer((req, res) => {
    if (req.url === '/health') {
      res.writeHead(200);
      res.end(JSON.stringify({ status: 'ok', type: 'p2p-endpoint' }));
      return;
    }

    if (req.method === 'POST' && req.url === '/p2p/message') {
      let body = '';
      req.on('data', chunk => body += chunk);
      req.on('end', () => {
        try {
          const msg = JSON.parse(body);
          onMessage(msg);
          res.writeHead(200);
          res.end(JSON.stringify({ status: 'received' }));
        } catch (e) {
          res.writeHead(400);
          res.end(JSON.stringify({ error: e.message }));
        }
      });
      return;
    }

    res.writeHead(404);
    res.end();
  });

  server.listen(port, '0.0.0.0', () => {
    console.log(`[P2P] 入站端点: http://0.0.0.0:${port}`);
  });

  return server;
}

module.exports = { P2PRouter, startP2PInboundServer };
