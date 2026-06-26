/**
 * 企微 Agent Connector — 配对服务器（Pairing Server）
 *
 * 作用：作为中心「红娘」协调两个 Connector 之间的 P2P 配对握手。
 * 部署到公网服务器（如 www.hermesai.ltd），所有 Connector 都能访问。
 *
 * 三个核心功能：
 *   1. 生成一次性配对码
 *   2. 配对码验证 + 连接信息交换
 *   3. WebSocket 信令通道（兜底中继）
 *
 * 启动：node pairing-server.js
 * 默认端口：19527
 *
 * API：
 *   POST /pair/generate     → 生成配对码
 *   POST /pair/join          → 使用配对码加入
 *   GET  /pair/status/:code  → 查询配对状态
 *   WS   /ws                 → WebSocket 信令通道
 */

const http = require('http');
const crypto = require('crypto');
const { WebSocketServer, WebSocket } = require('ws');

// ============================================================
// 配置
// ============================================================
const PORT = parseInt(process.env.PAIRING_PORT || '19527', 10);
const HOST = process.env.PAIRING_HOST || '0.0.0.0';
const CODE_EXPIRE_MS = 5 * 60 * 1000;  // 配对码 5 分钟过期
const CODE_LENGTH = 8;                   // 配对码长度（如 A1B2-C3D4）

// ============================================================
// 内存存储
// ============================================================
const pairings = new Map();       // code → { creator, joiner, createdAt, status }
const wsClients = new Map();      // connectorId → WebSocket
const connectorIds = new Map();   // code → [creatorId, joinerId]

// ============================================================
// 工具函数
// ============================================================

function generateCode() {
  const chars = 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789'; // 去掉易混淆的 0/O/1/I
  let code = '';
  const bytes = crypto.randomBytes(CODE_LENGTH);
  for (let i = 0; i < CODE_LENGTH; i++) {
    code += chars[bytes[i] % chars.length];
    if (i === 3) code += '-'; // 中间加横线：A1B2-C3D4
  }
  return code;
}

function generateId() {
  return `conn_${Date.now()}_${crypto.randomBytes(3).toString('hex')}`;
}

function log(level, ...args) {
  const ts = new Date().toLocaleTimeString('zh-CN', { hour12: false });
  console.log(`[${ts}] [${level}]`, ...args);
}

// 清理过期配对
setInterval(() => {
  const now = Date.now();
  for (const [code, pairing] of pairings) {
    if (now - pairing.createdAt > CODE_EXPIRE_MS) {
      // 通知双方配对过期
      for (const cid of [pairing.creator?.id, pairing.joiner?.id].filter(Boolean)) {
        const ws = wsClients.get(cid);
        if (ws && ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify({ type: 'pairing_expired', code }));
        }
      }
      pairings.delete(code);
      connectorIds.delete(code);
      log('INFO', `配对码 ${code} 已过期`);
    }
  }
}, 30000);

// ============================================================
// HTTP 服务器
// ============================================================

const server = http.createServer((req, res) => {
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (req.method === 'OPTIONS') {
    res.writeHead(204);
    res.end();
    return;
  }

  // ========================================
  // GET /health
  // ========================================
  if (req.method === 'GET' && req.url === '/health') {
    res.writeHead(200);
    res.end(JSON.stringify({
      status: 'ok',
      active_pairings: pairings.size,
      connected_clients: wsClients.size,
      uptime: Math.round(process.uptime()),
    }));
    return;
  }

  // ========================================
  // GET /pair/status/:code
  // ========================================
  if (req.method === 'GET' && req.url.startsWith('/pair/status/')) {
    const code = req.url.split('/pair/status/')[1];
    const pairing = pairings.get(code);

    if (!pairing) {
      res.writeHead(404);
      res.end(JSON.stringify({ error: 'pairing_not_found', message: '配对码不存在或已过期' }));
      return;
    }

    res.writeHead(200);
    res.end(JSON.stringify({
      code,
      status: pairing.status, // 'waiting' | 'joined' | 'expired'
      created_at: pairing.createdAt,
      has_joiner: !!pairing.joiner,
    }));
    return;
  }

  // ========================================
  // POST /pair/generate — 生成配对码
  // ========================================
  if (req.method === 'POST' && req.url === '/pair/generate') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        const { connector_id, peer_info } = JSON.parse(body || '{}');

        const code = generateCode();
        const cid = connector_id || generateId();

        pairings.set(code, {
          code,
          creator: { id: cid, peerInfo: peer_info || {} },
          joiner: null,
          status: 'waiting',
          createdAt: Date.now(),
        });
        connectorIds.set(code, [cid]);

        log('INFO', `生成配对码: ${code} (connector: ${cid.slice(0, 10)}...)`);

        res.writeHead(201);
        res.end(JSON.stringify({
          code,
          connector_id: cid,
          expires_in: CODE_EXPIRE_MS / 1000,
          expires_at: new Date(Date.now() + CODE_EXPIRE_MS).toISOString(),
        }));
      } catch (e) {
        res.writeHead(400);
        res.end(JSON.stringify({ error: 'invalid_body', message: e.message }));
      }
    });
    return;
  }

  // ========================================
  // POST /pair/join — 使用配对码加入
  // ========================================
  if (req.method === 'POST' && req.url === '/pair/join') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        const { code, connector_id, peer_info } = JSON.parse(body || '{}');

        if (!code) {
          res.writeHead(400);
          res.end(JSON.stringify({ error: 'missing_code', message: '请提供配对码' }));
          return;
        }

        const pairing = pairings.get(code);
        if (!pairing) {
          res.writeHead(404);
          res.end(JSON.stringify({ error: 'pairing_not_found', message: '配对码不存在或已过期' }));
          return;
        }

        if (pairing.status === 'joined') {
          res.writeHead(409);
          res.end(JSON.stringify({ error: 'already_joined', message: '该配对码已被使用' }));
          return;
        }

        // 记录加入者
        const jid = connector_id || generateId();
        pairing.joiner = { id: jid, peerInfo: peer_info || {} };
        pairing.status = 'joined';
        connectorIds.get(code).push(jid);

        log('INFO', `配对成功: ${code} ← ${jid.slice(0, 10)}...`);

        // 通过 WebSocket 通知创建者
        const creatorWs = wsClients.get(pairing.creator.id);
        if (creatorWs && creatorWs.readyState === WebSocket.OPEN) {
          creatorWs.send(JSON.stringify({
            type: 'peer_joined',
            code,
            peer: {
              id: jid,
              peer_info: pairing.joiner.peerInfo,
            },
          }));
        }

        // 也通知加入者（如果已连接 WS）
        const joinerWs = wsClients.get(jid);
        if (joinerWs && joinerWs.readyState === WebSocket.OPEN) {
          joinerWs.send(JSON.stringify({
            type: 'pairing_confirmed',
            code,
            peer: {
              id: pairing.creator.id,
              peer_info: pairing.creator.peerInfo,
            },
          }));
        }

        res.writeHead(200);
        res.end(JSON.stringify({
          status: 'joined',
          code,
          connector_id: jid,
          peer: {
            id: pairing.creator.id,
            peer_info: pairing.creator.peerInfo,
          },
        }));
      } catch (e) {
        res.writeHead(400);
        res.end(JSON.stringify({ error: 'invalid_body', message: e.message }));
      }
    });
    return;
  }

  // ========================================
  // POST /pair/disconnect — 断开配对
  // ========================================
  if (req.method === 'POST' && req.url === '/pair/disconnect') {
    let body = '';
    req.on('data', chunk => body += chunk);
    req.on('end', () => {
      try {
        const { code, connector_id } = JSON.parse(body || '{}');

        const pairing = pairings.get(code);
        if (!pairing) {
          res.writeHead(404);
          res.end(JSON.stringify({ error: 'not_found' }));
          return;
        }

        // 通知对方
        const peerId = pairing.creator.id === connector_id
          ? pairing.joiner?.id
          : pairing.creator.id;

        if (peerId) {
          const peerWs = wsClients.get(peerId);
          if (peerWs && peerWs.readyState === WebSocket.OPEN) {
            peerWs.send(JSON.stringify({ type: 'peer_disconnected', code }));
          }
        }

        pairings.delete(code);
        connectorIds.delete(code);

        res.writeHead(200);
        res.end(JSON.stringify({ status: 'disconnected' }));
      } catch (e) {
        res.writeHead(400);
        res.end(JSON.stringify({ error: e.message }));
      }
    });
    return;
  }

  // 404
  res.writeHead(404);
  res.end(JSON.stringify({ error: 'not_found' }));
});

// ============================================================
// WebSocket 信令通道
// ============================================================

const wss = new WebSocketServer({ server });

wss.on('connection', (ws, req) => {
  let connectorId = null;

  ws.on('message', (data) => {
    try {
      const msg = JSON.parse(data.toString());

      switch (msg.type) {
        // --- 注册 ---
        case 'register': {
          connectorId = msg.connector_id;
          wsClients.set(connectorId, ws);
          ws.send(JSON.stringify({ type: 'registered', connector_id: connectorId }));
          log('INFO', `WebSocket 客户端注册: ${connectorId.slice(0, 10)}... (在线: ${wsClients.size})`);
          break;
        }

        // --- P2P 信令（offer/answer/ice）---
        case 'signal': {
          const targetId = msg.target_id;
          const targetWs = wsClients.get(targetId);
          if (targetWs && targetWs.readyState === WebSocket.OPEN) {
            targetWs.send(JSON.stringify({
              type: 'signal',
              from_id: connectorId,
              signal_type: msg.signal_type, // 'offer' | 'answer' | 'ice-candidate'
              payload: msg.payload,
            }));
          }
          break;
        }

        // --- 中继消息（直连不通时的兜底）---
        case 'relay': {
          const targetId = msg.target_id;
          const targetWs = wsClients.get(targetId);
          if (targetWs && targetWs.readyState === WebSocket.OPEN) {
            targetWs.send(JSON.stringify({
              type: 'relay',
              from_id: connectorId,
              payload: msg.payload,
            }));
          } else {
            ws.send(JSON.stringify({
              type: 'relay_error',
              target_id: targetId,
              error: 'peer_offline',
            }));
          }
          break;
        }

        default:
          ws.send(JSON.stringify({ type: 'error', message: `未知消息类型: ${msg.type}` }));
      }
    } catch (e) {
      ws.send(JSON.stringify({ type: 'error', message: e.message }));
    }
  });

  ws.on('close', () => {
    if (connectorId) {
      wsClients.delete(connectorId);
      log('INFO', `WebSocket 客户端断开: ${connectorId.slice(0, 10)}... (在线: ${wsClients.size})`);

      // 通知所有相关配对中的对方
      for (const [code, ids] of connectorIds) {
        const peerIdx = ids.indexOf(connectorId);
        if (peerIdx >= 0) {
          const peerId = ids[1 - peerIdx]; // 0→1, 1→0
          const peerWs = wsClients.get(peerId);
          if (peerWs && peerWs.readyState === WebSocket.OPEN) {
            peerWs.send(JSON.stringify({ type: 'peer_disconnected', code }));
          }
        }
      }
    }
  });

  ws.on('error', (err) => {
    log('WARN', `WebSocket 错误: ${err.message}`);
  });
});

// ============================================================
// 启动
// ============================================================

server.listen(PORT, HOST, () => {
  console.log('='.repeat(50));
  console.log('  企微 Agent Connector — 配对服务器');
  console.log('='.repeat(50));
  console.log('');
  console.log(`  HTTP API:  http://${HOST}:${PORT}`);
  console.log(`  WebSocket: ws://${HOST}:${PORT}/ws`);
  console.log(`  配对码过期: ${CODE_EXPIRE_MS / 1000 / 60} 分钟`);
  console.log('');
  console.log('  API 端点:');
  console.log(`    POST /pair/generate   — 生成配对码`);
  console.log(`    POST /pair/join        — 加入配对`);
  console.log(`    GET  /pair/status/:code — 查询状态`);
  console.log(`    POST /pair/disconnect   — 断开配对`);
  console.log(`    WS   /ws                — 信令通道`);
  console.log(`    GET  /health            — 健康检查`);
  console.log('');
  console.log('  按 Ctrl+C 退出');
  console.log('');
});
