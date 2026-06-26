# 自建轻量同步服务（40 行 Node）

如果你有一台 VPS / 云服务器，用这个最简单的脚本就能跑起来。

## 📄 完整代码：`trip-sync.js`

```js
const http = require('http');
const fs = require('fs');
const path = require('path');

const DATA_DIR = path.join(__dirname, 'data');
if (!fs.existsSync(DATA_DIR)) fs.mkdirSync(DATA_DIR, { recursive: true });

const PORT = 3200;
const MAX_BODY = 256 * 1024;
const ROOM_RE = /^[a-zA-Z0-9_-]{1,40}$/;

const cors = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type',
};

http.createServer((req, res) => {
  if (req.method === 'OPTIONS') { res.writeHead(204, cors); return res.end(); }
  const m = req.url.match(/^\/room\/([^\/\?]+)/);
  if (!m) { res.writeHead(404, cors); return res.end('Not Found'); }
  const roomId = m[1];
  if (!ROOM_RE.test(roomId)) { res.writeHead(400, cors); return res.end('Bad Room ID'); }
  const file = path.join(DATA_DIR, roomId + '.json');

  if (req.method === 'GET') {
    res.writeHead(200, { 'Content-Type': 'application/json', ...cors });
    if (!fs.existsSync(file)) return res.end(JSON.stringify({ state: null, ts: 0 }));
    return res.end(fs.readFileSync(file, 'utf-8'));
  }

  if (req.method === 'POST') {
    let body = '';
    req.on('data', chunk => {
      body += chunk;
      if (body.length > MAX_BODY) { req.destroy(); }
    });
    req.on('end', () => {
      try {
        const obj = JSON.parse(body);
        obj.ts = obj.ts || Date.now();
        fs.writeFileSync(file, JSON.stringify(obj));
        res.writeHead(200, { 'Content-Type': 'application/json', ...cors });
        res.end(JSON.stringify({ ok: true, ts: obj.ts }));
      } catch (e) {
        res.writeHead(400, cors); res.end('Invalid JSON');
      }
    });
    return;
  }

  res.writeHead(405, cors); res.end('Method Not Allowed');
}).listen(PORT, '127.0.0.1', () => console.log('trip-sync listening on 127.0.0.1:' + PORT));
```

## 🚀 部署步骤

### 1. 上传 & 启动
```bash
scp trip-sync.js user@your-server:/home/user/trip-sync/
ssh user@your-server
cd /home/user/trip-sync
node trip-sync.js
# → listening on 127.0.0.1:3200
```

### 2. systemd 守护（推荐）

```ini
# /etc/systemd/system/trip-sync.service
[Unit]
Description=Trip Sync Service
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/home/your-user/trip-sync
ExecStart=/usr/bin/node /home/your-user/trip-sync/trip-sync.js
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable --now trip-sync
sudo systemctl status trip-sync
```

### 3. nginx 反代（加 HTTPS）

```nginx
# /etc/nginx/sites-available/default
location /trip-sync/ {
  rewrite ^/trip-sync/(.*)$ /$1 break;
  proxy_pass http://127.0.0.1:3200;
  proxy_http_version 1.1;
  proxy_set_header Host $host;
  proxy_set_header X-Real-IP $remote_addr;
}
```

重载 nginx：
```bash
sudo nginx -t && sudo systemctl reload nginx
```

### 4. 前端配置

方案 A：直接在 `todo-sync.js` 里配置 `workers` 风格的 baseUrl：
```js
const SYNC_BACKEND = 'workers';
const WORKERS_CONFIG = {
  baseUrl: 'https://your-domain.com/trip-sync',
};
```

方案 B：用 `custom` 后端，自定义路径。

## ✅ 验证

```bash
# 读空房间（应返回 {state:null,ts:0}）
curl https://your-domain.com/trip-sync/room/test123

# 写
curl -X POST https://your-domain.com/trip-sync/room/test123 \
  -H "Content-Type: application/json" \
  -d '{"state":{"u0":true},"ts":1714000000000}'

# 再读（应返回刚才写入的数据）
curl https://your-domain.com/trip-sync/room/test123
```

## 🔒 可选增强

### 加鉴权
在 POST 前加一层 token 校验：
```js
const EXPECTED = process.env.TRIP_TOKEN || '';
if (req.method === 'POST' && req.headers['x-auth-token'] !== EXPECTED) {
  res.writeHead(403, cors); return res.end('Forbidden');
}
```

### 自动备份
```bash
# crontab -e
0 3 * * * tar czf /backup/trip-sync-$(date +\%Y\%m\%d).tar.gz /home/user/trip-sync/data
```

## 📈 为什么只绑 127.0.0.1

`.listen(PORT, '127.0.0.1', ...)` 只监听本地接口，外网打不到，只能经 nginx 反代访问。避免直接暴露 Node 进程、避免跳过 HTTPS。

---

_优点：完全自己掌控，代码透明、易魔改，顺手可加 WebSocket / 评论 / 多房间列表等功能。_
_缺点：要自己维护服务器、证书、监控。_
