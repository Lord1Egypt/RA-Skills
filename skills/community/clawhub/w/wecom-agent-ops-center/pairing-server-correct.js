/**
 * 企微 Agent Connector — 配对服务器 + 消息转换 API（合并版 v1.1.1）
 *
 * 修复：req.url 被代理改成完整 URL 的兼容处理
 * 部署：https://www.hermesai.ltd
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
  // 兼容 req.url 被代理改成完整 URL 的情况（如 http://host:port/path）
  let urlPath = req.url.split('?')[0];
  try {
    if (urlPath.startsWith('http')) {
      const u = new URL(urlPath);
      urlPath = u.pathname;
    }
  } catch (e) {}

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
  if (req.method === 'GET' && urlPath === '/health') {
    res.writeHead(200, { 'Content-Type': 'application/json' });
    res.end(JSON.stringify({
      status: 'ok',
      service: 'wecom-connector',
      version: '1.1.1',
      active_pairings: pairings.size,
      connected_clients: wsClients.size,
      uptime: Math.round(process.uptime()),
    }));
    return;
  }

  // ========================================
  // 认证（仅转换 API 需要；P2P 配对暂不认证）
  // ========================================
  const isConverterApi = urlPath.startsWith('/api/convert/');
  if (isConverterApi && !auth(req)) {
    jsonReply(res, 401, { error: 'Unauthorized', hint: 'Provide x-api-key header' });
    return;
  }

  // ========================================
  // P2P 配对 API
  // ========================================

  // POST /pair/generate
  if (req.method === 'POST' && urlPath === '/pair/generate') {
    try {
      const body = await parseBody(req);
      const connectorId = body.connector_id || generateId();
      const code = generateCode();

      // 避免碰撞
      while (pairings.has(code)) {
        code = generateCode();
      }

      pairings.set(code, {
        code,
        creator: { id: connectorId, info: body.connector_info || {} },
        joiner: null,
        createdAt: Date.now(),
        status: 'waiting',
      });
      connectorIds.set(code, [connectorId, null]);

      log('INFO', `生成配对码 ${code} for ${connectorId}`);
      jsonReply(res, 200, {
        code,
        connector_id: connectorId,
        expire_in: Math.round(CODE_EXPIRE_MS / 1000),
      });
    } catch (e) {
      jsonReply(res, 400, { error: e.message });
    }
    return;
  }

  // POST /pair/join
  if (req.method === 'POST' && urlPath === '/pair/join') {
    try {
      const body = await parseBody(req);
      const { code, connector_id, connector_info } = body;

      if (!pairings.has(code)) {
        jsonReply(res, 404, { error: 'Pairing code not found or expired' });
        return;
      }

      const pairing = pairings.get(code);
      if (pairing.status !== 'waiting') {
        jsonReply(res, 409, { error: 'Pairing already completed or expired' });
        return;
      }

      pairing.joiner = { id: connector_id || generateId(), info: connector_info || {} };
      pairing.status = 'connected';
      connectorIds.set(code, [pairing.creator.id, pairing.joiner.id]);

      // 通知双方（如果在线）
      const notify = (cid) => {
        const ws = wsClients.get(cid);
        if (ws && ws.readyState === WebSocket.OPEN) {
          ws.send(JSON.stringify({ type: 'pairing_success', code, peer: pairing.joiner }));
        }
      };
      notify(pairing.creator.id);

      log('INFO', `配对成功 ${code}: ${pairing.creator.id} ↔ ${pairing.joiner.id}`);
      jsonReply(res, 200, {
        code,
        peer: pairing.creator,
        status: 'connected',
      });
    } catch (e) {
      jsonReply(res, 400, { error: e.message });
    }
    return;
  }

  // GET /pair/status/:code
  const statusMatch = urlPath.match(/^\/pair\/status\/([A-Z0-9\-]+)$/);
  if (req.method === 'GET' && statusMatch) {
    const code = statusMatch[1];
    if (!pairings.has(code)) {
      jsonReply(res, 404, { error: 'Not found' });
      return;
    }
    const pairing = pairings.get(code);
    jsonReply(res, 200, {
      code,
      status: pairing.status,
      creator_online: wsClients.has(pairing.creator?.id),
      joiner_online: pairing.joiner ? wsClients.has(pairing.joiner.id) : false,
      created_at: new Date(pairing.createdAt).toISOString(),
    });
    return;
  }

  // POST /pair/disconnect
  if (req.method === 'POST' && urlPath === '/pair/disconnect') {
    try {
      const body = await parseBody(req);
      const { code } = body;
      if (pairings.has(code)) {
        const pairing = pairings.get(code);
        for (const cid of [pairing.creator?.id, pairing.joiner?.id].filter(Boolean)) {
          const ws = wsClients.get(cid);
          if (ws && ws.readyState === WebSocket.OPEN) {
            ws.send(JSON.stringify({ type: 'pairing_disconnected', code }));
          }
        }
        pairings.delete(code);
        connectorIds.delete(code);
        log('INFO', `配对断开 ${code}`);
      }
      jsonReply(res, 200, { ok: true });
    } catch (e) {
      jsonReply(res, 400, { error: e.message });
    }
    return;
  }

  // ========================================
  // 消息转换 API（核心 IP，云端保护）
  // ========================================

  // POST /api/convert/to-standard
  if (req.method === 'POST' && urlPath === '/api/convert/to-standard') {
    try {
      const frame = await parseBody(req);
      const standard = wecomToStandard(frame);
      jsonReply(res, 200, { ok: true, standard });
    } catch (e) {
      jsonReply(res, 400, { ok: false, error: e.message });
    }
    return;
  }

  // POST /api/convert/to-wecom
  if (req.method === 'POST' && urlPath === '/api/convert/to-wecom') {
    try {
      const body = await parseBody(req);
      const reply = body.reply || {};
      const msgType = body.msg_type || 'markdown';
      const wecom = standardToWecomReply(reply, msgType);
      jsonReply(res, 200, { ok: true, wecom });
    } catch (e) {
      jsonReply(res, 400, { ok: false, error: e.message });
    }
    return;
  }

  // POST /api/convert/to-wecom-card
  if (req.method === 'POST' && urlPath === '/api/convert/to-wecom-card') {
    try {
      const body = await parseBody(req);
      const card = standardToWecomCard(body);
      jsonReply(res, 200, { ok: true, wecom: card });
    } catch (e) {
      jsonReply(res, 400, { ok: false, error: e.message });
    }
    return;
  }

  // ========================================
  // 404
  // ========================================
  jsonReply(res, 404, {
    error: 'Not found',
    endpoints: {
      pairing: ['POST /pair/generate', 'POST /pair/join', 'GET  /pair/status/:code', 'POST /pair/disconnect', 'WS   /ws'],
      converter: ['POST /api/convert/to-standard', 'POST /api/convert/to-wecom', 'POST /api/convert/to-wecom-card'],
      health: 'GET  /health',
    },
  });
});

// ============================================================
// WebSocket 服务器（P2P 信令）
// ============================================================
const wss = new WebSocketServer({ noServer: true });

server.on('upgrade', (req, socket, head) => {
  // 兼容 req.url 被代理改成完整 URL
  let urlPath = req.url.split('?')[0];
  try {
    if (urlPath.startsWith('http')) {
      const u = new URL(urlPath);
      urlPath = u.pathname;
    }
  } catch (e) {}

  if (urlPath === '/ws') {
    wss.handleUpgrade(req, socket, head, (ws) => {
      wss.emit('connection', ws, req);
    });
  } else {
    socket.destroy();
  }
});

wss.on('connection', (ws, req) => {
  const connectorId = new URL('http://x' + req.url).searchParams.get('id') || generateId();
  ws.connectorId = connectorId;
  wsClients.set(connectorId, ws);

  log('WS', `客户端连接: ${connectorId}（在线: ${wsClients.size}）`);

  ws.on('message', (data) => {
    try {
      const msg = JSON.parse(data);
      // P2P 信令转发逻辑
      if (msg.type === 'peer_message' && msg.to) {
        const targetWs = wsClients.get(msg.to);
        if (targetWs && targetWs.readyState === WebSocket.OPEN) {
          targetWs.send(JSON.stringify({
            type: 'peer_message',
            from: connectorId,
            payload: msg.payload,
            timestamp: Date.now(),
          }));
        }
      }
    } catch (e) {
      log('ERROR', `消息解析失败: ${e.message}`);
    }
  });

  ws.on('close', () => {
    wsClients.delete(connectorId);
    log('WS', `客户端断开: ${connectorId}（在线: ${wsClients.size}）`);
  });
});

// ============================================================
// 启动
// ============================================================
server.listen(PORT, HOST, () => {
  console.log('[wecom-connector] 合并服务启动');
  console.log(`  地址: http://${HOST}:${PORT}`);
  console.log('  P2P 配对: POST /pair/...  WS /ws');
  console.log('  消息转换: POST /api/convert/...');
  console.log('  健康检查: GET /health');
  console.log(`  [转换 API 认证] ${AUTH_TOKEN ? '已启用（x-api-key）' : '未启用（开发模式）'}`);
});
