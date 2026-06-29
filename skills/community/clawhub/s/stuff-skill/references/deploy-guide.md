# Cloudflare Pages + D1 部署指南

本指南适用于 PWA 生成器生成的所有应用。技术栈：静态 HTML/CSS/JS + Cloudflare Pages Functions（D1 API）。

---

## 前置条件

1. **Cloudflare 账号**：已登录 [dash.cloudflare.com](https://dash.cloudflare.com)
2. **wrangler CLI**：
   ```bash
   npm install -g wrangler
   wrangler login   # 浏览器完成 OAuth，token 存本地
   ```
3. **项目目录结构**（必须符合此结构，原因见下方踩坑记录）：
   ```
   my-app/
   ├── public/           # 静态文件（index.html, manifest.json, sw.js, icons/）
   │   ├── index.html
   │   ├── manifest.json
   │   ├── sw.js
   │   └── icons/
   ├── functions/        # Cloudflare Pages Functions（API 端点）
   │   └── api/
   │       └── items.js  # GET/POST/DELETE 统一处理
   └── wrangler.toml     # 必须在项目根目录
   ```

---

## Step 1：创建 D1 数据库

```bash
# 创建数据库，记录输出的 database_id
wrangler d1 create my-app-db

# 输出示例：
# ✅ Successfully created DB 'my-app-db'
# [[d1_databases]]
# binding = "DB"
# database_name = "my-app-db"
# database_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"  ← 复制此 ID
```

---

## Step 2：配置 wrangler.toml

在项目根目录创建 `wrangler.toml`：

```toml
name = "my-app"
compatibility_date = "2024-01-01"

[[d1_databases]]
binding = "DB"
database_name = "my-app-db"
database_id = "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"  # 替换为实际 ID
```

或使用 `wrangler.json`（JSON 格式）：

```json
{
  "name": "my-app",
  "compatibility_date": "2024-01-01",
  "d1_databases": [
    {
      "binding": "DB",
      "database_name": "my-app-db",
      "database_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    }
  ]
}
```

---

## Step 3：初始化数据库表

在 `functions/api/items.js` 中，第一次接收请求时自动建表（推荐），或手动执行 SQL：

```bash
# 本地执行 SQL（远程用 --remote）
wrangler d1 execute my-app-db --command "
CREATE TABLE IF NOT EXISTS items (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  status TEXT DEFAULT 'active',
  data TEXT,          -- JSON 存储其余字段
  created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
  updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
"

# 或从 SQL 文件执行
wrangler d1 execute my-app-db --file ./schema.sql
```

---

## Step 4：Pages Functions API 实现

`functions/api/items.js` 示例（处理 GET/POST/DELETE）：

```js
export async function onRequest(context) {
  const { request, env } = context;
  const url = new URL(request.url);

  // 初始化表（幂等）
  await env.DB.exec(`
    CREATE TABLE IF NOT EXISTS items (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      name TEXT NOT NULL,
      status TEXT DEFAULT 'active',
      data TEXT,
      created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
      updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
    )
  `);

  const headers = {
    'Content-Type': 'application/json',
    'Access-Control-Allow-Origin': '*',
  };

  // GET：获取所有记录
  if (request.method === 'GET') {
    const { results } = await env.DB.prepare(
      'SELECT * FROM items ORDER BY created_at DESC'
    ).all();
    // 解析 JSON data 字段
    const items = results.map(row => ({
      ...row,
      ...(row.data ? JSON.parse(row.data) : {})
    }));
    return new Response(JSON.stringify(items), { headers });
  }

  // POST：新增或更新记录
  if (request.method === 'POST') {
    const body = await request.json();
    const { id, name, status, ...rest } = body;
    const data = JSON.stringify(rest);

    if (id) {
      // 更新
      await env.DB.prepare(
        'UPDATE items SET name=?, status=?, data=?, updated_at=CURRENT_TIMESTAMP WHERE id=?'
      ).bind(name, status, data, id).run();
    } else {
      // 新增
      await env.DB.prepare(
        'INSERT INTO items (name, status, data) VALUES (?, ?, ?)'
      ).bind(name, status || 'active', data).run();
    }
    return new Response(JSON.stringify({ ok: true }), { headers });
  }

  // DELETE：删除记录
  if (request.method === 'DELETE') {
    const id = url.searchParams.get('id');
    if (!id) return new Response(JSON.stringify({ error: 'id required' }), { status: 400, headers });
    await env.DB.prepare('DELETE FROM items WHERE id=?').bind(id).run();
    return new Response(JSON.stringify({ ok: true }), { headers });
  }

  return new Response('Method Not Allowed', { status: 405 });
}
```

---

## Step 5：部署

### ⚠️ 关键：必须从项目根目录部署

```bash
# ✅ 正确：在项目根目录执行，指定 public/ 为静态目录
cd /path/to/my-app
npx wrangler pages deploy public --project-name my-app

# ❌ 错误：进入 public/ 再部署
cd /path/to/my-app/public
npx wrangler pages deploy . --project-name my-app
# 后果：functions/ 目录不在此路径下，不会被上传，
#       所有 /api/* 请求会返回 index.html（HTML），而非 JSON
```

### 首次部署（自动创建项目）
```bash
cd /path/to/my-app
npx wrangler pages deploy public --project-name my-app
# 首次会提示选择账号和创建项目，按提示操作即可
```

### 后续部署
```bash
cd /path/to/my-app
npx wrangler pages deploy public --project-name my-app
```

部署完成后 URL 格式：`https://my-app.pages.dev`（几乎即时生效，< 30 秒）

---

## Step 6：Service Worker 版本管理

每次部署前，必须更新 `public/sw.js` 顶部的 CACHE 常量，否则用户会继续使用旧缓存。

```js
// public/sw.js
const CACHE_VERSION = 'v1.2.3';  // ← 每次部署递增
const CACHE_NAME = `my-app-${CACHE_VERSION}`;
const ASSETS = [
  '/',
  '/index.html',
  '/manifest.json',
  // 其他静态资源...
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))
  );
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then(keys =>
      Promise.all(
        keys.filter(k => k !== CACHE_NAME).map(k => caches.delete(k))
      )
    )
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  // API 请求：网络优先，失败时走 localStorage 兜底（前端处理）
  if (event.request.url.includes('/api/')) return;

  // 静态资源：缓存优先
  event.respondWith(
    caches.match(event.request).then(cached =>
      cached || fetch(event.request)
    )
  );
});
```

**推荐实践**：把版本号写入 `package.json` 的 `version` 字段，部署脚本自动同步到 `sw.js`。

---

## Step 7：自定义域名（可选）

1. 在 Cloudflare Dashboard → Pages → 项目 → Custom domains 绑定域名
2. 若域名已在 Cloudflare 托管：自动添加 CNAME，几分钟生效
3. 若域名在其他注册商：手动添加 CNAME 指向 `my-app.pages.dev`

---

## 踩坑记录

### 坑 1：只部署 public/ 导致 API 返回 HTML

**现象**：`fetch('/api/items')` 返回的是 HTML 页面内容，而非 JSON。控制台报 `SyntaxError: Unexpected token '<'`。

**根因**：进入 `public/` 目录后执行 `wrangler pages deploy .`，wrangler 看不到上层的 `functions/` 目录，因此 Pages Functions 没有被上传。Cloudflare 对不存在的路由返回 `index.html`（SPA fallback），导致 `/api/*` 也返回 HTML。

**解决**：永远在项目根目录执行 `wrangler pages deploy public`，而不是在 `public/` 目录里执行 `wrangler pages deploy .`。

### 坑 2：D1 binding 名称大小写敏感

`wrangler.toml` 中 `binding = "DB"` 对应代码中 `env.DB`（大写）。改为 `binding = "db"` 则对应 `env.db`。混用会导致 `TypeError: env.DB is not a function`。

### 坑 3：本地开发无 D1 支持，需用 wrangler dev

直接用浏览器 `file://` 打开无法访问 Functions。本地开发需用：
```bash
npx wrangler pages dev public --d1 DB=my-app-db
```

### 坑 4：iOS Safari standalone 模式下 fetch 跨域限制

PWA 安装到桌面后，iOS Safari 在 standalone 模式下对相对路径 fetch 有特殊处理。始终使用相对路径（`/api/items` 而非 `https://domain.com/api/items`）以避免问题。

---

## 完整部署 Checklist

- [ ] `wrangler login` 完成认证
- [ ] D1 数据库已创建，`database_id` 已写入 `wrangler.toml`
- [ ] `functions/api/items.js` 包含 GET/POST/DELETE 三个端点
- [ ] `public/sw.js` CACHE 版本号已更新
- [ ] 在项目**根目录**执行 `npx wrangler pages deploy public`
- [ ] 部署后访问 `https://my-app.pages.dev` 验证页面加载
- [ ] 访问 `https://my-app.pages.dev/api/items` 验证 API 返回 JSON（不是 HTML）
- [ ] 手机浏览器验证 manifest 安装提示出现

---

## 给用户的部署指南（生成应用后贴给用户）

> 以下内容是给**用户**看的,不是给 Agent。生成应用后,把这段贴给用户作为部署指引。

### 本地模式（零配置,拿来就用）

不需要任何账号,不需要安装任何软件。

1. Agent 会给你生成 3 个文件(`index.html` + `styles.css` + `app.js`)
2. 拖到浏览器里打开 `index.html`,就能用了
3. 数据存在浏览器里,关掉再打开也不会丢
4. 想备份?用应用里的"导出 JSON"功能

**限制:** 只能在一个设备上用。手机和电脑的数据不会同步。

### 云模式（多设备同步）

想在手机和电脑上都能用、数据实时同步?需要部署到云上。

**默认方案:Cloudflare(推荐,免费)**

你需要:
1. 注册一个 [Cloudflare 账号](https://dash.cloudflare.com/sign-up)(免费,不需要绑卡)
2. 电脑上安装 Node.js([nodejs.org](https://nodejs.org/) 下载安装)
3. 打开终端,运行 `npm install -g wrangler`
4. 运行 `wrangler login`,在浏览器里授权

做完这 4 步,告诉 Agent"我 Cloudflare 配好了",Agent 会自动帮你部署。部署完你会拿到一个网址,手机打开就能用。

**其他平台(高级用户)**

如果你熟悉其他平台,也可以部署到:
- **Vercel + Turso** —— 前端开发者常用
- **Netlify + Supabase** —— 功能强大但配置稍多
- **自有服务器** —— 完全自由,需要自己搞定数据库

只需要告诉 Agent 你想用哪个平台,Agent 会适配 API 层。但注意:非 Cloudflare 平台需要你自己有一定技术基础。
