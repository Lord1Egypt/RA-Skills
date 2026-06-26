---
name: wewe-rss-reader
description: "微信公众号文章阅读技能。当用户发来公众号文章链接、需要阅读理解文章内容时使用。通过本地部署的 WeWe RSS 服务获取文章全文并转为纯文本。Requires: 无（调用本地 REST API，首次部署见 references/deployment.md）。"
metadata: {"openclaw":{"emoji":"📖","requires":{"anyBins":[]}}}
---

# wewe-rss-reader

微信公众号文章阅读。当用户发来文章链接或需要查询已订阅公众号的文章时使用。

## API 基础信息

- **API 地址**: `http://localhost:4001`
- **wewe-rss 容器**: `http://localhost:4000`（Web UI）
- **AUTH_CODE**: `wewe-rss-2026`

## 核心 API

### 获取单篇文章内容（最常用）

```
GET /api/articles/:id
```
返回纯文本内容（最多前15000字）。`:id` 是文章 URL 中 `mp.weixin.qq.com/s/` 后面的部分。

**示例**：用户发来链接 `https://mp.weixin.qq.com/s/udSpp7eMqwiRo5yVShRzLw`
→ 调用 `GET /api/articles/udSpp7eMqwiRo5yVShRzLw`
→ 直接获得文章纯文本内容

### 通过 URL 订阅公众号

```
POST /api/subscribe
Content-Type: application/json
body: {"url": "文章链接"}
```
从文章链接自动识别并订阅该公众号，返回订阅结果。

### 列出已订阅公众号

```
GET /api/feeds
```

### 列出某公众号文章

```
GET /api/articles?feedId=MP_ID&limit=10
```

### 手动刷新订阅

```
POST /api/refresh/:feedId
POST /api/refresh-all
```

## 使用流程

**场景1：用户发来文章链接**
1. 从 URL 提取文章 ID（如 `https://mp.weixin.qq.com/s/udSpp7eMqwiRo5yVShRzLw` → ID 是 `udSpp7eMqwiRo5yVShRzLw`）
2. 直接调用 `GET /api/articles/:id` 获取正文
3. 即可对文章内容进行阅读理解

**场景2：用户要求查询某公众号最新文章**
1. `GET /api/feeds` 确认已订阅
2. `GET /api/articles?feedId=<MP_ID>&limit=5` 获取文章列表
3. 如需正文，`GET /api/articles/:id`

**场景3：用户想订阅新公众号**
1. 用户需提供该公众号的**任意文章链接**（不是公众号主页链接）
2. `POST /api/subscribe` body: `{"url": "文章链接"}`
3. 返回订阅成功/已存在

## 登录流程（微信读书授权）

> 微信读书账号用于抓取公众号内容。若账号已登录且有效（参考 health 检查），无需每次操作。
> 账号失效后会收到 "暂无可用读书账号" 错误，此时需要重新登录。

### 完整登录流程

```
# Step 1: 发起登录
POST /api/login/start
→ 返回 {"uuid": "...", "confirmUrl": "https://..."}

# Step 2: 发送二维码图片到飞书
→ 把 confirmUrl 作为图片请求 URL（或生成二维码图片）发送到飞书群
→ 通知用户扫码

# Step 3: 轮询等待登录完成（自动）
GET /api/login/status/<uuid>
→ status=authorized 表示登录成功 → 继续执行
→ status=waiting 表示等待中 → 继续轮询
→ 超过 5 分钟视为过期，报错让用户重新发起
```

**轮询间隔**：每 5 秒一次，不要快发。

**自动完成**：用户扫完码后，status 会自动变成 `authorized`，全程无需用户额外确认。

**发送图片到飞书**：用 `message` 工具将登录 URL 对应的二维码图片发送到飞书群，通知用户扫码。图片发送由调用方 agent 负责（参考飞书发送图片规范）。

## Agent Rules

- 收到文章链接时，优先直接调用 `/api/articles/:id` 获取内容，而非要求用户提供更多信息
- 获取到正文后，直接进行阅读理解，不需要额外确认
- 如调用失败（返回空/报错），先检查 wewe-rss 容器是否运行：`curl http://localhost:4001/api/health`
- 如容器未运行：在 `~/.openclaw/workspace/wewe-rss/` 目录下 `docker compose up -d`
