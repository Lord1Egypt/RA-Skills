// Cloudflare Worker — 爪爪 v7
// 编号自增 + 自动清理 + 多 bridge 路由 + 好友请求 + 信令 + 聊天降级
// 部署: wrangler deploy

const CORS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, PUT, POST, DELETE, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};
const HOUR = 3600000;
const DAY = 86400000;

// ─── 分片：每 8 人一个 DO ─────────────────────────────
function getShard(uid) { return Math.floor((parseInt(uid) || 0) / 8); }
function getRoom(env, uid) {
  const id = env.CHAT_ROOM.idFromName('shard-' + getShard(uid));
  return env.CHAT_ROOM.get(id);
}

// ─── 注册（编号自增）─────────────────────────────────
async function handleRegister(request, env) {
  if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: CORS });
  if (request.method !== 'GET') return new Response('Method not allowed', { status: 405, headers: CORS });

  const id = env.CHAT_ROOM.idFromName('shard-0');
  const room = env.CHAT_ROOM.get(id);
  return room.fetch(new Request('https://internal/register', { method: 'GET' }));
}

// ─── 好友请求 ─────────────────────────────────────────
async function handleFriend(request, env) {
  if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: CORS });
  const url = new URL(request.url);
  const uid = url.searchParams.get('uid');
  if (!uid) return new Response(JSON.stringify({ error: 'uid required' }), { status: 400, headers: { ...CORS, 'Content-Type': 'application/json' } });
  const key = `friend_${uid}`;
  if (request.method === 'GET') { return new Response(await env.ZZ_STORE.get(key) || '[]', { headers: { ...CORS, 'Content-Type': 'application/json' } }); }
  if (request.method === 'DELETE') { await env.ZZ_STORE.put(key, '[]'); return new Response(JSON.stringify({ ok: true }), { headers: { ...CORS, 'Content-Type': 'application/json' } }); }
  if (request.method === 'PUT') {
    const body = await request.json();
    const raw = await env.ZZ_STORE.get(key);
    const list = raw ? JSON.parse(raw) : [];
    if (!list.some(r => r.from === body.from)) { list.push(body); if (list.length > 50) list.splice(0, list.length - 50); await env.ZZ_STORE.put(key, JSON.stringify(list)); }
    return new Response(JSON.stringify({ ok: true }), { headers: { ...CORS, 'Content-Type': 'application/json' } });
  }
  return new Response('Method not allowed', { status: 405, headers: CORS });
}

// ─── WebRTC 信令 ──────────────────────────────────────
async function handleSignaling(request, env) {
  if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: CORS });
  const url = new URL(request.url);
  const uid = url.searchParams.get('uid');
  if (!uid) return new Response(JSON.stringify({ error: 'uid required' }), { status: 400, headers: { ...CORS, 'Content-Type': 'application/json' } });
  const key = `signal_${uid}`;
  if (request.method === 'GET') { return new Response(await env.ZZ_STORE.get(key) || '[]', { headers: { ...CORS, 'Content-Type': 'application/json' } }); }
  if (request.method === 'POST') { const body = await request.json(); const raw = await env.ZZ_STORE.get(key); const q = raw ? JSON.parse(raw) : []; q.push(body); if (q.length > 30) q.splice(0, q.length - 30); await env.ZZ_STORE.put(key, JSON.stringify(q)); return new Response(JSON.stringify({ ok: true }), { headers: { ...CORS, 'Content-Type': 'application/json' } }); }
  if (request.method === 'DELETE') { await env.ZZ_STORE.put(key, '[]'); return new Response(JSON.stringify({ ok: true }), { headers: { ...CORS, 'Content-Type': 'application/json' } }); }
  return new Response('Method not allowed', { status: 405, headers: CORS });
}

// ─── 聊天降级 ─────────────────────────────────────────
async function handleChat(request, env) {
  if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: CORS });
  const url = new URL(request.url);
  const uid = url.searchParams.get('uid');
  if (!uid) return new Response(JSON.stringify({ error: 'uid required' }), { status: 400, headers: { ...CORS, 'Content-Type': 'application/json' } });
  const key = `chat_${uid}`;
  if (request.method === 'GET') { return new Response(await env.ZZ_STORE.get(key) || '[]', { headers: { ...CORS, 'Content-Type': 'application/json' } }); }
  if (request.method === 'PUT') { const body = await request.json(); const raw = await env.ZZ_STORE.get(key); const q = raw ? JSON.parse(raw) : []; q.push(body); if (q.length > 100) q.splice(0, q.length - 100); await env.ZZ_STORE.put(key, JSON.stringify(q)); return new Response(JSON.stringify({ ok: true }), { headers: { ...CORS, 'Content-Type': 'application/json' } }); }
  if (request.method === 'DELETE') { await env.ZZ_STORE.put(key, '[]'); return new Response(JSON.stringify({ ok: true }), { headers: { ...CORS, 'Content-Type': 'application/json' } }); }
  return new Response('Method not allowed', { status: 405, headers: CORS });
}

// ─── 清理（每天跑一次）────────────────────────────────
async function handleCleanup(env) {
  const now = Date.now();
  let cursor;
  let deleted = 0;
  let checked = 0;
  let listed;
  do {
    listed = await env.ZZ_STORE.list({ prefix: 'user_', cursor });
    for (const key of listed.keys) {
      checked++;
      try {
        const user = JSON.parse(await env.ZZ_STORE.get(key.name));
        const uid = key.name.replace('user_', '');
        let shouldDelete = false;
        if (!user.lastActive && (now - user.created > HOUR)) shouldDelete = true; // 1h未发消息
        if (user.lastActive && (now - user.lastActive > DAY)) shouldDelete = true; // 24h不活跃
        if (shouldDelete) {
          await env.ZZ_STORE.delete(key.name);
          await env.ZZ_STORE.delete(`friend_${uid}`);
          await env.ZZ_STORE.delete(`signal_${uid}`);
          await env.ZZ_STORE.delete(`chat_${uid}`);
          deleted++;
        }
      } catch {}
    }
    cursor = listed.cursor;
  } while (!listed.list_complete);
  return { checked, deleted };
}

// ─── OpenClaw Durable Object ──────────────────────────
export class ChatRoom {
  constructor(state, env) {
    this.state = state;
    this.env = env;
    this.bridges = {};
    this.phones = {};
    this.pendingMsg = {};
  }

  async fetch(request) {
    const url = new URL(request.url);

    // 重置编号计数器
    if (url.pathname.includes('/reset')) {
      await this.state.storage.put('counter', 0);
      return new Response(JSON.stringify({ ok: true, counter: 0 }), { headers: { ...CORS, 'Content-Type': 'application/json' } });
    }

    // 注册端点（编号自增）
    if (url.pathname.includes('/register')) {
      const nextId = (await this.state.storage.get('counter') || 0) + 1;
      await this.state.storage.put('counter', nextId);
      const uid = String(nextId);
      await this.env.ZZ_STORE.put(`user_${uid}`, JSON.stringify({ created: Date.now(), lastActive: 0 }));
      return new Response(JSON.stringify({ id: uid }), { headers: { ...CORS, 'Content-Type': 'application/json' } });
    }

    // 清理端点（cron 调用）
    if (url.pathname.includes('/cleanup')) {
      const result = await handleCleanup(this.env);
      return new Response(JSON.stringify(result), { headers: { ...CORS, 'Content-Type': 'application/json' } });
    }

    if (request.headers.get('Upgrade') === 'websocket') {
      const [client, server] = Object.values(new WebSocketPair());
      await this.handleSession(server, url.searchParams);
      return new Response(null, { status: 101, webSocket: client });
    }
    if (request.method === 'OPTIONS') return new Response(null, { status: 204, headers: CORS });

    // 更新活跃时间
    const uid = url.searchParams.get('uid');
    if (uid) await touchUser(this.env, uid);

    if (request.method === 'GET') {
      if (uid && this.pendingMsg[uid]) {
        return new Response(JSON.stringify(this.pendingMsg[uid]), { headers: { ...CORS, 'Content-Type': 'application/json' } });
      }
      return new Response(JSON.stringify({ from:'', to:'', content:'', msg_id:'', ts:0, isImage:false }), { headers: { ...CORS, 'Content-Type': 'application/json' } });
    }

    if (request.method === 'PUT') {
      const body = await request.json();
      const to = body.to;
      // 只存 bridge 的回复到 pendingMsg，手机自己的消息不存
      if (to && body.from && body.from.startsWith('D')) this.pendingMsg[to] = body;
      // 更新活跃时间
      if (body.from) await touchUser(this.env, body.from);
      if (to) await touchUser(this.env, to);
      // 消息发给目标 bridge
      const targetBridge = this.bridges['D' + to];
      if (targetBridge && body.content) {
        try { targetBridge.send(JSON.stringify(body)); } catch {}
      }
      // bridge 回复推给手机
      if (to && this.phones[to]) try { this.phones[to].send(JSON.stringify(body)); } catch {}
      return new Response(JSON.stringify({ ok: true }), { headers: { ...CORS, 'Content-Type': 'application/json' } });
    }
    return new Response('Not found', { status: 404 });
  }

  handleSession(ws, params) {
    ws.accept();
    const role = params.get('role');
    const uid = params.get('uid');

    if (role === 'bridge') {
      const bridgeKey = 'D' + (uid || '0');
      this.bridges[bridgeKey] = ws;
      if (uid) touchUser(this.env, uid);
    } else if (uid) {
      this.phones[uid] = ws;
      touchUser(this.env, uid);
      if (this.pendingMsg[uid] && this.pendingMsg[uid].content) {
        try { ws.send(JSON.stringify(this.pendingMsg[uid])); } catch {}
      }
    }

    ws.addEventListener('message', (e) => {
      try {
        const data = JSON.parse(e.data);
        if (role === 'bridge') {
          const to = data.to;
          if (to) this.pendingMsg[to] = data;
          if (to && this.phones[to]) try { this.phones[to].send(JSON.stringify(data)); } catch {}
        } else {
          const to = data.to || '';
          if (data.from) touchUser(this.env, data.from);
          const targetBridge = this.bridges['D' + to];
          if (targetBridge) {
            try { targetBridge.send(JSON.stringify(data)); } catch {}
          } else {
            for (const bKey of Object.keys(this.bridges)) {
              try { this.bridges[bKey].send(JSON.stringify(data)); } catch {}
            }
          }
        }
      } catch {}
    });

    ws.addEventListener('close', () => {
      if (role === 'bridge') { delete this.bridges['D' + (uid || '0')]; }
      else if (uid) { delete this.phones[uid]; }
    });
    ws.addEventListener('error', () => {
      if (role === 'bridge') { delete this.bridges['D' + (uid || '0')]; }
      else if (uid) { delete this.phones[uid]; }
    });
  }
}

// 更新用户活跃时间
async function touchUser(env, uid) {
  if (!uid || uid.startsWith('D')) return;
  try {
    const raw = await env.ZZ_STORE.get(`user_${uid}`);
    if (raw) {
      const user = JSON.parse(raw);
      if (!user.lastActive) {
        user.lastActive = Date.now();
        await env.ZZ_STORE.put(`user_${uid}`, JSON.stringify(user));
      }
    }
  } catch {}
}

// ─── 入口 ─────────────────────────────────────────────
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    if (url.pathname.includes('/register')) return handleRegister(request, env);
    if (url.pathname.includes('/signal')) return handleSignaling(request, env);
    if (url.pathname.includes('/friend')) return handleFriend(request, env);
    if (url.pathname.includes('/chat')) return handleChat(request, env);
    // 按 uid 分片到不同 DO
    let uid = url.searchParams.get('uid');
    if (!uid) try { const body = await request.clone().json(); uid = body.to || body.from; } catch {}
    const room = getRoom(env, uid || '0');
    return room.fetch(request);
  },
  // Cron trigger：每天清理
  async scheduled(event, env) {
    const result = await handleCleanup(env);
    console.log(`[cleanup] checked=${result.checked} deleted=${result.deleted}`);
  }
};
