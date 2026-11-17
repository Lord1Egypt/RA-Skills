---
name: x-rss-feishu-daily
description: X(Twitter)博主监控→飞书群推送→触发智能体写日报的完整自建流水线。RSSHub(走代理)+Miniflux+自写 relay 中转，Docker Compose 一键部署；内置防 X 风控配置（60~120 分钟轮询、30 分钟缓存、温和刷新脚本）；含飞书开放平台全流程（自建应用、机器人进群、外部群对外共享与版本发布、用户身份 OAuth）；定时维护脚本（每日日报全量重推、温和刷新、token 轮换）与踩坑合集（webhook 内网开关、新订阅不触发 webhook、直写 integrations 表、open_id 跨应用隔离）。Use when the user wants to monitor X/Twitter bloggers and push updates to a Feishu group, build an RSS-to-Feishu daily report pipeline, deploy RSSHub+Miniflux with anti-ban polling, add X bloggers to Feishu push, or troubleshoot Feishu custom app bot/group/external-sharing/OAuth issues.
---

# x-rss-feishu-daily：X 博主监控 → 飞书群推送 → 智能体日报

完整链路（全部自建、Docker 化、已在生产验证）：

```
博主发推 → Miniflux 定时轮询(60~120min) → RSSHub 抓取(走 Clash 代理)
  → webhook → feishu-relay(卡片化) → 飞书群「RSS 推送」
  → @用户本人 → 私有智能体(小蓝虾)以用户身份感知并写日报
```

scripts/ 内含本机验证过的全部文件：`docker-compose.yml`、`relay.py`（推送中转）、`refresh_gently.py`（温和刷新）、`push_daily.py`（日报素材全量重推）、`oauth_login.py`（用户身份 OAuth，可选）。

## 一次性部署

### 1. 飞书自建应用（开放平台 open.feishu.cn）

1. 创建**企业自建应用**（名字随意，如「RSS 信息源」），记录 App ID/Secret
2. **应用能力** → 添加「机器人」
3. **权限管理** → 开通：`im:message`（应用身份，发消息）、`im:chat.members:read`（免审）、用户身份的 `im:message` / `im:chat:readonly` / `im:message.send_as_user`（全部免审）
4. **版本管理与发布** → 创建版本并发布（可用范围≤5 人时免审秒过）
5. 把机器人加进目标群：群设置 → 群机器人 → 添加机器人 → 搜应用名

> 群搜不到机器人：先完全退出飞书客户端重开（配置缓存）；仍不行就原样重发一版强制刷新。
> **外部群**（含外部联系人的群）：必须勾选版本的「允许机器人被添加到外部群中使用」+ 填申请理由 → **需企业管理员审核**。提醒/推送场景直接建普通**内部群**零审核。
> 拿用户/机器人的 open_id 有命名空间坑：open_id 按应用隔离，别的应用报的 ID 你用不了（"open_id cross app"）；群成员接口只返回人不返回 bot。本应用命名空间下群成员的 open_id 用成员接口查。

### 2. Docker 部署（scripts/docker-compose.yml）

```bash
mkdir rss-stack && cd rss-stack   # 把 scripts/ 里的文件拷进来
# .env（勿提交/外传）：
#   TWITTER_AUTH_TOKEN=<你的X登录凭证>
#   MINIFLUX_ADMIN_PASSWORD=<随机密码>
docker compose up -d
```

- RSSHub 宿主端口 1201（容器内 1200）；Miniflux 宿主端口 8088
- **防 X 风控已内置**：Miniflux `SCHEDULER_ROUND_ROBIN_MIN_INTERVAL=60 / MAX=120`（每 feed 60~120 分钟一轮，8 个订阅约 100~200 请求/天，低于真人刷推）；RSSHub `CACHE_EXPIRE=1800`（30 分钟缓存防重复打 X）
- Miniflux 两个内网开关**都必须开**：`FETCHER_ALLOW_PRIVATE_NETWORKS=1`（抓内网 RSSHub）+ `INTEGRATION_ALLOW_PRIVATE_NETWORKS=1`（webhook 发内网 relay）。缺第二个时日志 WARN "connection to private network is blocked" 且无推送
- Miniflux 2.3.3 **没有 webhook API**（/v1/webhooks 404），网页脚本登录也会被拒 → 直写 Postgres：`UPDATE integrations SET webhook_enabled=true, webhook_url='http://feishu-relay:8080/webhook', webhook_secret='<随机串>' WHERE user_id=1;` 然后 `docker restart miniflux`

### 3. X 凭证（auth_token）

浏览器登录 x.com（**建议小号**）→ F12 → Application → Cookies → `https://x.com` → 复制 `auth_token`（32 位十六进制）→ 填 `.env` → `docker compose up -d rsshub`。

- auth_token 等于该账号密码，只存本地
- 失效特征：feed 有频道信息但 **0 条推文**（RSSHub 日志 `error: undefined`），别误判成功
- Clash 侧把 x.com 固定走同一专用节点（IP 跳动比频率更容易触发风控）；偶尔真人登录小号活跃一下

### 4. 订阅博主（注意首推坑）

```bash
# 添加：POST http://127.0.0.1:8088/v1/feeds  {"feed_url":"http://rsshub:1200/twitter/user/<handle>"}
# ⚠️ 创建时会立即首抓，首批条目不算"新条目"→ 不会触发 webhook！
#    补推方法：拉该 feed 的 entries POST 到 relay（见下），或等下轮自然更新
```

### 5. relay 与触发智能体

`relay.py` 收 Miniflux webhook（POST /webhook），把新条目组装成卡片发群，并 @ 触发日报智能体。配置在同目录 `feishu.env`（KEY=VALUE）：

| 键 | 说明 |
|---|---|
| FEISHU_APP_ID / FEISHU_APP_SECRET | 自建应用凭证 |
| FEISHU_CHAT_ID | 推送目标群 oc_xxx（用户 token 列 chats 或建群 API 可得） |
| MINIFLUX_URL / MINIFLUX_ADMIN_USERNAME / MINIFLUX_ADMIN_PASSWORD | relay 查 feed 标题用 |
| REPORT_BOT_OPEN_ID | **日报点名目标**：填"日报智能体以谁的身份工作"的那个用户的 open_id（本应用命名空间）。智能体以用户身份读消息时，@ 用户 = 触发智能体 |
| REPORT_BOT_NAME / REPORT_TRIGGER_COOLDOWN_H | 退化文本点名用名字；自动推送点名冷却（默认 20h≈每天一次，0=每次都点） |
| REPORT_DM_TARGET | **首选触发**：以用户身份（OAuth user_token）私聊日报智能体的 open_id。需先跑 oauth_login.py 生成 user_token.json（已挂载进 relay 容器，token 自动滚动续期）。私聊触发比群内 @ 可靠得多（open_id 跨应用不可用，bot 发的 @ 私有智能体可能解析失败） |

⚠️ **bot 发的 @ 对私有智能体不可靠，且 open_id 跨应用不可用**——所以点名目标是"智能体所依附的用户本人"，智能体以该用户身份感知 @ 并自行触发（方案 A）。若智能体支持 OAuth 用户身份（方案 C），可改用 `oauth_login.py` 拿 user_access_token 直接以用户身份发私聊，触发更稳（注意：用户身份发**外部群**会被拦，私聊/内部群不受限）。

## 定时维护

| 事项 | 频率 | 操作 |
|---|---|---|
| 日常 | 全自动 | 轮询→推卡片→按冷却点名日报，无需人工 |
| 每日日报素材重推 | 需要时 | `python push_daily.py`（读本地 Miniflux 全量重发+必点名，不碰 X） |
| 验证/换 token 后首刷 | 偶尔 | `python refresh_gently.py 60`（逐 feed 刷新、强制间隔，脚本头注释写明仅首灌/换token/核对时用） |
| 新增博主 | 随时 | API 添加 + **手动补推首批**（见上）+ 记得 feed_id |
| B站视频源（可选） | 三前提 | ① 镜像换 `diygod/rsshub:chromium-bundled`（B站路由需无头浏览器）② rsshub 配 `BILIBILI_COOKIE_rssstack`＝登录 Cookie 整串（**SESSDATA 必需，单独 buvid3 无效**；1~3 个月过期重取）③ **出口 IP 必须国内**——Clash 全局/TUN 模式下 B站 API 一律 412 预检（机房 IP 无视 Cookie），需规则模式或 bilibili 直连规则。路由 /bilibili/user/video/:uid；批量并发订阅可能瞬态 503（单独重试即可）；个别 UP 主空间权限受限会 -403（无法监控）。批量脚本 scripts/add_bili.py |
| 抓取失败告警（推荐） | 一次配置 | relay 内置监控线程（MONITOR=1，30 分钟一轮）：≥3 个 X 源连续两轮报错 → 自动发 ⚠️ 告警卡（列异常源+恢复指引）；恢复后自动发 ✅ 通知。告警独立于抓取通道，X 挂了也能发出 |
| 定时场次（推荐） | 一次配置 | relay 内置调度线程：feishu.env `SCHEDULE_TIMES=12:00,17:00`（北京时间），每到场次自动执行「总览源增量卡 → 归档文档（末场）→ 以用户身份私聊智能体触发日报」，状态落盘防重防漏 |
| 飞书文档归档（推荐） | 一次配置 | 机器人 A 开通 space:folder:create + docx:document + drive:drive:readonly + docs:permission.member:create（全免审）→ drive API 建归档文件夹（ARCHIVE_FOLDER_TOKEN）→ `archive_daily.py` 每日建日期命名的文档写入全部素材（按源分节、幂等可重跑），并把文档链接卡发群；文件夹加协作者（docs:permission.member）让用户可打开 |
| Follow Builders 聚合源（可选） | 一次配置 | [follow-builders](https://github.com/zarazhangrui/follow-builders) 提供 26 位 AI 圈 X 账号+6 播客+2 博客的每日聚合 JSON（GitHub Actions 采集，零 X token 消耗）。relay 内置转换桥（FOLLOW_BUILDERS=1 + FB_PROXY 代理）：拉 JSON 转标准 RSS 挂在 /feeds/fb_*.xml，Miniflux 订阅三路；X 聚合放 SKIP+OVERVIEW 出总览卡，播客/博客低频直接增量推卡 |
| AI 热点总览源（可选） | 一次配置 | 高频资讯 RSS（如 aihot.news/feed.xml）单独建分类订阅 → feishu.env 设 `SKIP_FEED_IDS=<feed_id>`（relay 跳过增量防刷屏）+ `OVERVIEW_FEED_ID=<feed_id>`（push_daily 每次追加一张「AI 热点总览」卡） |
| X token 失效 | 数月一次 | 群推送停止/账号异常时：重新取 auth_token 换 `.env` → `docker compose up -d rsshub` → 温和刷新验证 |
| 用户 OAuth token | 30 天 | `oauth_login.py` 重跑一次（或自行实现 refresh_token 滚动续期；换 token 用 v1 两步：auth/v3 拿 app_access_token → 带 Bearer 头调 authen/v1/oidc/access_token；v2 端点不给 refresh_token） |

观察点：群突然没推送 → `docker logs miniflux | grep -i webhook`（有 WARN=权限/网络问题）；`docker logs feishu-relay`（relay 没收到=miniflux 侧问题）。

## 故障排查速查

| 症状 | 原因/处理 |
|---|---|
| feed 有账号信息但 0 推文 | X token 无效（别误判成功）；或刚建订阅尚无更新 |
| webhook 全无、miniflux 日志无 webhook 字样 | integrations 表 webhook_enabled 未开（直写 DB） |
| WARN "connection to private network is blocked" | 两个 ALLOW_PRIVATE_NETWORKS 开关 |
| 群里搜不到机器人 | 未发布版本/可用范围/客户端缓存；原样重发一版刷新 |
| 「不支持加入外部群」 | 对外共享未开，需管理员审核；或改用内部群 |
| 消息 230001 | content 字段必须是把卡片 JSON **再序列化成字符串** |
| 99991672 | 缺 scope，报错里有开通直链；开通后需重发版本（免审 scope 除外） |
| open_id cross app | open_id 按应用隔离，别用别的应用报的 ID |
| 宿主机脚本连 localhost 502/解析失败 | 用 127.0.0.1 + 显式 ProxyHandler({}) 绕过系统代理 |
| 自动化操作 open.feishu.cn | Playwright locator 点击大量超时 → 截图定位 + CUA 坐标点击；登录走二维码 |
