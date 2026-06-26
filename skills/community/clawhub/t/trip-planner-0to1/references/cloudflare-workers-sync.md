# Cloudflare Workers KV 同步服务（推荐）

零运维、免费额度高、无 CORS 烦恼。适合长期维护多个攻略项目。

## 📊 免费额度（2026 年）

- 10 万次读请求/天
- 1 千次写请求/天
- 1 GB 存储
- 通常个人旅行 Todo 一天 < 20 次写，完全够用

## 🚀 部署步骤

### 1. 安装 Wrangler CLI
```bash
npm install -g wrangler
wrangler login
```

### 2. 创建项目
```bash
mkdir trip-sync-worker && cd trip-sync-worker
wrangler init --yes
```

### 3. 创建 KV namespace
```bash
wrangler kv:namespace create TRIP_KV
# 记下返回的 id，填入下方 wrangler.toml
```

### 4. 编辑 `wrangler.toml`
```toml
name = "trip-sync"
main = "src/index.js"
compatibility_date = "2026-04-24"

[[kv_namespaces]]
binding = "TRIP_KV"
id = "xxxx-你刚才创建的 id-xxxx"
```

### 5. 编辑 `src/index.js`
```js
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const cors = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: cors });
    }

    // 路由：/room/<id>
    const m = url.pathname.match(/^\/room\/([a-zA-Z0-9_-]{1,40})$/);
    if (!m) {
      return new Response('Not Found', { status: 404, headers: cors });
    }
    const roomId = m[1];
    const key = 'room:' + roomId;

    if (request.method === 'GET') {
      const data = await env.TRIP_KV.get(key, 'json');
      return new Response(JSON.stringify(data || { state: null, ts: 0 }), {
        headers: { 'Content-Type': 'application/json', ...cors },
      });
    }

    if (request.method === 'POST') {
      const body = await request.json();
      if (JSON.stringify(body).length > 256 * 1024) {
        return new Response('Payload too large', { status: 413, headers: cors });
      }
      await env.TRIP_KV.put(key, JSON.stringify(body));
      return new Response(JSON.stringify({ ok: true, ts: body.ts || Date.now() }), {
        headers: { 'Content-Type': 'application/json', ...cors },
      });
    }

    return new Response('Method Not Allowed', { status: 405, headers: cors });
  },
};
```

### 6. 部署
```bash
wrangler deploy
# 会输出 URL，如 https://trip-sync.your-subdomain.workers.dev
```

### 7. 前端配置
在 `todo-sync.js` 里：
```js
const SYNC_BACKEND = 'workers';
const WORKERS_CONFIG = {
  baseUrl: 'https://trip-sync.your-subdomain.workers.dev',
};
```

## ✅ 验证

```bash
# 写
curl -X POST https://trip-sync.your-subdomain.workers.dev/room/test123 \
  -H "Content-Type: application/json" \
  -d '{"state":{"u0":true},"ts":1714000000000}'

# 读
curl https://trip-sync.your-subdomain.workers.dev/room/test123
```

## 🔒 增强安全（可选）

如担心房间 ID 被猜中导致数据被改，可以：

### 方式 A：要求带 X-Auth-Token
```js
const AUTH_TOKEN = 'your-secret-token-12345';

if (request.method === 'POST') {
  const token = request.headers.get('X-Auth-Token');
  if (token !== AUTH_TOKEN) {
    return new Response('Forbidden', { status: 403, headers: cors });
  }
  // ...
}
```

### 方式 B：用 Turnstile 防机器人
在前端嵌入 Cloudflare Turnstile，token 随 POST 提交，Worker 校验。

## 📈 监控

Cloudflare Dashboard → Workers & Pages → 你的 Worker → Metrics，可看到：
- 请求量
- 错误率
- CPU 时间
- KV 读写次数

## 🧹 清理旧数据

```bash
# 列出所有 key
wrangler kv:key list --binding=TRIP_KV

# 删除指定 key
wrangler kv:key delete --binding=TRIP_KV "room:old-trip-2025"
```

---

_优点：免费额度充裕、全球边缘节点、自带 HTTPS / CORS、无需维护 VPS。_
_缺点：首次部署需要 Cloudflare 账号 + 熟悉 Wrangler。_
