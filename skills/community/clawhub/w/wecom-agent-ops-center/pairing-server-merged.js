/**
 * 企微 Agent Connector — 配对服务器 + 消息转换 API（合并版）
 *
 * 作用：
 *   1. P2P 配对信令（生成配对码、加入配对、WebSocket 信令转发）
 *   2. 消息格式转换（企微格式 ↔ 标准 JSON，核心 IP 放云端）
 *
 * 部署：https://www.hermesai.ltd
 *
 * API：
 *   P2P 配对：
 *     POST /pair/generate
 *     POST /pair/join
 *     GET  /pair/status/:code
 *     POST /pair/disconnect
 *     WS   /ws
 *   消息转换：
 *     POST /api/convert/to-standard
 *     POST /api/convert/to-wecom
 *     POST /api/convert/to-wecom-card
 *   健康检查：
 *     GET  /health
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
const AUTH_TOKEN = process.env.CONVERTER_AUTH_TOKEN || '';

// ============================================================
// 认证中间件（简单 token 验证，用于转换 API）
// ============================================================
function auth(req) {
  if (!AUTH_TOKEN) return true; // 未配置 token 则放行（开发模式）
  const token = req.headers['x-api-key'] || '';
  return token === AUTH_TOKEN;
}

// ============================================================
// 内存存储（P2P 配对）
// ============================================================
const pairings = new Map();       // code → { creator, joiner, createdAt, status }
const wsClients = new Map();      // connectorId → WebSocket
const connectorIds = new Map();   // code → [creatorId, joinerId]

// ============================================================
// 工具函数（P2P 配对）
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
// 消息转换函数（核心 IP，放云端保护）
// ============================================================

// 企微帧 → 标准化 JSON
function wecomToStandard(frame) {
  const body = frame.body || {};
  const headers = frame.headers || {};
  const msgId = body.msgid || '';
  const msgType = body.msgtype || 'text';
  const chatType = body.chattype || 'single';

  let content = '';
  switch (msgType) {
    case 'text':
      content = (body.text && body.text.content) || '';
      break;
    case 'mixed': {
      const items = (body.mixed && body.mixed.msg_item) || [];
      content = items
        .filter(item => item.msgtype === 'text')
        .map(item => (item.text && item.text.content) || '')
        .join(' ');
      break;
    }
    case 'voice':
      content = (body.voice && body.voice.content) || '[语音消息]';
      break;
    case 'image':
      content = '[图片消息]';
      break;
    case 'file': {
      const filename = (body.file && body.file.file_name) || 'unknown';
      content = `[文件: ${filename}]`;
      break;
    }
    case 'event': {
      const eventType = (body.event && body.event.eventtype) || 'unknown';
      content = `[事件: ${eventType}]`;
      break;
    }
    case 'stream':
      content = (body.stream && body.stream.content) || '';
      break;
    default:
      content = `[${msgType} 消息]`;
  }

  return {
    msg_id: msgId,
    req_id: headers.req_id || '',
    from: {
      user_id: (body.from && body.from.userid) || '',
      name: (body.from && body.from.name) || '',
      chat_id: body.chatid || '',
      chat_type: chatType,
    },
    content,
    msg_type: msgType,
    timestamp: new Date().toISOString(),
    channel: 'wecom',
  };
}

// 标准化 JSON → 企微回复体
function standardToWecomReply(reply, msgType = 'markdown') {
  const content = reply.content || '';

  if (msgType === 'text') {
    return { msgtype: 'text', text: { content } };
  }

  return { msgtype: 'markdown', markdown: { content } };
}

// 标准化 JSON → 企微模板卡片
function standardToWecomCard(cardData) {
  const card = cardData.card || {};
  const buttons = card.buttons || [];

  const result = {
    msgtype: 'template_card',
    template_card: {
      card_type: 'text_notice',
      main_title: { title: card.title || '通知' },
      emphasis_content: { title: card.emphasis || card.content || '' },
      sub_title_text: card.subtitle || '',
      horizontal_content_list: Object.entries(card.fields || {}).map(
        ([key, value]) => ({ keyname: key, value: String(value) })
      ),
    },
  };

  if (buttons.length > 0) {
    result.template_card.button_list = buttons.map(btn => ({
      text: btn.text,
      style: btn.style || 0,
      key: btn.key,
    }));
  }

  return result;
}

// JSON 解析辅助
function parseBody(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', chunk => { body += chunk; });
    req.on('end', () => {
      try {
        resolve(JSON.parse(body));
      } catch (e) {
        reject(new Error('Invalid JSON: ' + e.message));
      }
    });
    req.on('error', reject);
  });
}

function jsonReply(res, status, data) {
  res.writeHead(status, {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type, x-api-key',
    'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
  });
  res.end(JSON.stringify(data));
}

// ============================================================
// HTTP 服务器（合并 P2P 配对 + 消息转换）
// ============================================================
const server = http.createServer(async (req, res) => {
  // CORS preflight
  if (req.method === 'OPTIONS') {
    res.writeHead(204, {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Headers': 'Content-Type, x-api-key',
      'Access-Control-Allow-Methods': 'POST, GET, OPTIONS',
    });
    res.end();
    return;
  }

  // ========================================
  // GET /health — 健康检查（公开，无认证）
  // ========================================
  if (req.method === 'GET' && req.url === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      status: 'ok',
      service: 'wecom-connector',
      version: '1.1.0',
      active_pairings: pairings.size,
      connected_clients: wsClients.size,
      uptime: Math.round(process.uptime()),
    }));
    return;
  }

  // ========================================
  // 认证（仅转换 API 需要；P2P 配对暂不认证）
  // ========================================
  const isConverterApi = req.url.startsWith('/api/convert/');
  if (isConverterApi && !auth(req)) {
    jsonReply(res, 401, { error: 'Unauthorized', hint: 'Provide x-api-key header' });
    return;
  }

  try {
    // ========================================
    // P2P 配对 API
    // ========================================

    // GET /pair/status/:code
    if (req.method === 'GET' && req.url.startsWith('/pair/status/')) {
      const code = req.url.split('/pair/status/')[1];
      const pairing = pairings.get(code);

      if (!pairing) {
        res.writeHead(404, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ error: 'pairing_not_found', message: '配对码不存在或已过期' }));
        return;
      }

      res.writeHead(200, { 'Content-Type': 'application/json' });
      res.end(JSON.stringify({
        code,
        status: pairing.status,
        created_at: pairing.createdAt,
        has_joiner: !!pairing.joiner,
      }));
      return;
    }

    // POST /pair/generate
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

          res.writeHead(201, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({
            code,
            connector_id: cid,
            expires_in: CODE_EXPIRE_MS / 1000,
            expires_at: new Date(Date.now() + CODE_EXPIRE_MS).toISOString(),
          }));
        } catch (e) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: 'invalid_body', message: e.message }));
        }
      });
      return;
    }

    // POST /pair/join
    if (req.method === 'POST' && req.url === '/pair/join') {
      let body = '';
      req.on('data', chunk => body += chunk);
      req.on('end', () => {
        try {
          const { code, connector_id, peer_info } = JSON.parse(body || '{}');

          if (!code) {
            res.writeHead(400, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'missing_code', message: '请提供配对码' }));
            return;
          }

          const pairing = pairings.get(code);
          if (!pairing) {
            res.writeHead(404, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'pairing_not_found', message: '配对码不存在或已过期' }));
            return;
          }

          if (pairing.status === 'joined') {
            res.writeHead(409, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'already_joined', message: '该配对码已被使用' }));
            return;
          }

          const jid = connector_id || generateId();
          pairing.joiner = { id: jid, peerInfo: peer_info || {} };
          pairing.status = 'joined';
          connectorIds.get(code).push(jid);

          log('INFO', `配对成功: ${code} ← ${jid.slice(0, 10)}...`);

          const creatorWs = wsClients.get(pairing.creator.id);
          if (creatorWs && creatorWs.readyState === WebSocket.OPEN) {
            creatorWs.send(JSON.stringify({
              type: 'peer_joined',
              code,
              peer: { id: jid, peer_info: pairing.joiner.peerInfo },
            }));
          }

          const joinerWs = wsClients.get(jid);
          if (joinerWs && joinerWs.readyState === WebSocket.OPEN) {
            joinerWs.send(JSON.stringify({
              type: 'pairing_confirmed',
              code,
              peer: { id: pairing.creator.id, peer_info: pairing.creator.peerInfo },
            }));
          }

          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({
            status: 'joined',
            code,
            connector_id: jid,
            peer: { id: pairing.creator.id, peer_info: pairing.creator.peerInfo },
          }));
        } catch (e) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: 'invalid_body', message: e.message }));
        }
      });
      return;
    }

    // POST /pair/disconnect
    if (req.method === 'POST' && req.url === '/pair/disconnect') {
      let body = '';
      req.on('data', chunk => body += chunk);
      req.on('end', () => {
        try {
          const { code, connector_id } = JSON.parse(body || '{}');
          const pairing = pairings.get(code);
          if (!pairing) {
            res.writeHead(404, { 'Content-Type': 'application/json' });
            res.end(JSON.stringify({ error: 'not_found' }));
            return;
          }

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

          res.writeHead(200, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ status: 'disconnected' }));
        } catch (e) {
          res.writeHead(400, { 'Content-Type': 'application/json' });
          res.end(JSON.stringify({ error: e.message }));
        }
      });
      return;
    }

    // ========================================
    // 消息转换 API（核心 IP 保护）
    // ========================================

    // POST /api/convert/to-standard — 企微帧 → 标准 JSON
    if (req.method === 'POST' && req.url === '/api/convert/to-standard') {
      const frame = await parseBody(req);
      const result = wecomToStandard(frame);
      jsonReply(res, 200, { ok: true, data: result });
      return;
    }

    // POST /api/convert/to-wecom — Agent 回复 → 企微回复体
    if (req.method === 'POST' && req.url === '/api/convert/to-wecom') {
      const body = await parseBody(req);
      const { reply, msg_type } = body;

      if (!reply) {
        jsonReply(res, 400, { error: 'Missing "reply" field' });
        return;
      }

      const result = standardToWecomReply(reply, msg_type || 'markdown');
      jsonReply(res, 200, { ok: true, data: result });
      return;
    }

    // POST /api/convert/to-wecom-card — Agent 卡片 → 企微模板卡片
    if (req.method === 'POST' && req.url === '/api/convert/to-wecom-card') {
      const cardData = await parseBody(req);
      const result = standardToWecomCard(cardData);
      jsonReply(res, 200, { ok: true, data: result });
      return;
    }

    // 404
    res.writeHead(404, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      error: 'Not found',
      endpoints: {
        pairing: [
          'POST /pair/generate',
          'POST /pair/join',
          'GET  /pair/status/:code',
          'POST /pair/disconnect',
          'WS   /ws',
        ],
        converter: [
          'POST /api/convert/to-standard',
          'POST /api/convert/to-wecom',
          'POST /api/convert/to-wecom-card',
        ],
        health: 'GET  /health',
      },
    }));

  } catch (err) {
    jsonReply(res, 500, { error: err.message });
  }
});

// ============================================================
// WebSocket 服务器（P2P 信令通道）
// ============================================================
const wss = new WebSocketServer({ noServer: true });

server.on('upgrade', (req, socket, head) => {
  if (req.url === '/ws') {
    wss.handleUpgrade(req, socket, head, (ws) => {
      wss.emit('connection', ws, req);
    });
  } else {
    socket.destroy();
  }
});

wss.on('connection', (ws, req) => {
  const urlParams = new URL(req.url, `http://${req.headers.host}`).searchParams;
  const connectorId = urlParams.get('connector_id') || generateId();

  ws.connectorId = connectorId;
  wsClients.set(connectorId, ws);

  log('WS', `客户端连接: ${connectorId.slice(0, 12)}... (在线: ${wsClients.size})`);

  ws.send(JSON.stringify({
    type: 'welcome',
    connector_id: connectorId,
    message: '已连接到配对服务器',
  }));

  ws.on('message', (data) => {
    try {
      const msg = JSON.parse(data.toString());

      // 信令转发：发给目标 connector
      if (msg.target_connector_id && msg.payload) {
        const targetWs = wsClients.get(msg.target_connector_id);
        if (targetWs && targetWs.readyState === WebSocket.OPEN) {
          targetWs.send(JSON.stringify({
            from_connector_id: connectorId,
            payload: msg.payload,
            timestamp: Date.now(),
          }));
          log('WS', `信令转发: ${connectorId.slice(0, 8)} → ${msg.target_connector_id.slice(0, 8)}`);
        } else {
          ws.send(JSON.stringify({ type: 'error', message: '目标 connector 不在线' }));
        }
      }
    } catch (e) {
      log('ERROR', `消息解析失败: ${e.message}`);
    }
  });

  ws.on('close', () => {
    wsClients.delete(connectorId);
    log('WS', `客户端断开: ${connectorId.slice(0, 12)}... (在线: ${wsClients.size})`);
  });

  ws.on('error', (err) => {
    log('ERROR', `WebSocket 错误: ${err.message}`);
  });
});

// ============================================================
// 启动
// ============================================================
server.listen(PORT, HOST, () => {
  console.log(`[wecom-connector] 合并服务启动`);
  console.log(`  地址: http://${HOST}:${PORT}`);
  console.log(`  P2P 配对: POST /pair/...  WS /ws`);
  console.log(`  消息转换: POST /api/convert/...`);
  console.log(`  健康检查: GET  /health`);
  if (AUTH_TOKEN) {
    console.log(`  [转换 API 认证] 已启用 (x-api-key)`);
  } else {
    console.log(`  [转换 API 认证] 未启用（请设置 CONVERTER_AUTH_TOKEN）`);
  }
});
