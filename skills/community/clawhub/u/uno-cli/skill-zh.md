---
name: uno-cli
slug: uno-cli
displayName: Uno（2000+ 工具网关）
version: 1.2.1
summary: "pip install uno-cli，然后 uno whoami → uno search → uno call。"
license: MIT
description: "Uno CLI — 虾聊官方出品的 Agent 工具网关，命令行访问 2000+ 真实工具，两步完成：搜索 → 调用。支持 Device Code OAuth（虾聊 SSO）、混合搜索（关键词/语义）、自动鉴权、评分、多账号管理。13 大分类覆盖：搜索、开发、社交、数据、创意、金融、生活、效率、媒体、企业、电商、健康等。使用场景：需要获取实时或精准外部数据（新闻、地图、股票、搜索等）；需要访问外部服务（优惠券，酒店，排队，打车等）；需要访问个人 app（gmail，outlook，notion，slack，企微等）或已有 skills/Cli/MCP 无法满足用户需求时。"
homepage: https://agentools.uno
metadata: {"emoji":"◆","category":"tools","api_base":"https://agentools.uno","version":"1.2.1"}
---

# Uno CLI

> **由虾聊（ClawdChat）官方出品** — 通过命令行使用 2000+ 真实工具。零安装（仅需 Python 3.8+ 标准库）。

## 前置条件

- Python 3.8+（多数系统已预装）
- CLI 脚本已内置：`bin/uno.py` — 无需额外安装

CLI 路径（相对于本文件）：`bin/uno.py`

## Step 1：先查凭证

存的是 **API Key**（`uno_…`），不是浏览器 JWT。路径：`~/.uno/credentials.json`（目录 `0700`，文件 `0600`）。环境变量 `UNO_API_KEY` 盖过文件。

```bash
python bin/uno.py whoami --compact
```

- 成功（姓名 / 邮箱 / 积分）→ 跳过登录
- 失败 → 再走下面的认证
- 同一 OS 用户、同一 `$HOME` → 下次 `whoami` 自动可用。换机器或临时 Cloud Agent 盘不会保留 `~/.uno`

## 认证

`whoami` / `call` 可能打印 `Run: uno login`。不要跑光秃的 `login`——会卡住终端。用 `--start` / `--poll`。

`/device` 页会让用户先在网站登录（若还没登录），再点授权。不要把「打开 URL」当成已经完成。

**`--start` 之后停下来。** 把 `verification_uri_complete` 给用户，等他们说已经授权。**同一轮不要跑 `--poll`。**

使用前先检查凭证是否已存在（`~/.uno/credentials.json`），若不存在则登录一次。

```bash
# 方式 A：两步登录（推荐 Agent 使用 — 非阻塞）
python bin/uno.py login --start
# → 返回 JSON: {"status": "pending", "verification_uri_complete": "https://...", "device_code": "xxx", ...}
# 等用户确认已授权后再：
python bin/uno.py login --poll <device_code>
# → {"success": true, "name": "...", "email": "..."}

# 方式 B：一步交互（终端用户 — 阻塞至授权完成）
python bin/uno.py login

# 方式 C：直接使用 API Key（https://agentools.uno/dashboard?tab=keys）
python bin/uno.py login --key uno_xxxxx

# 多账号切换
python bin/uno.py use                  # 列出所有账号
python bin/uno.py use <名称或邮箱>      # 切换账号

# 退出登录
python bin/uno.py logout
python bin/uno.py logout --all         # 清除所有账号
```

环境变量 `UNO_API_KEY` 优先于文件凭证（适用于 CI）。

### 认证流程说明

Uno 使用 **Device Code 流程**。网站登录页会给出可用的登录方式，不要另造注册链接。

1. `login --start` 从 Uno 服务器获取设备码
2. 把 `verification_uri_complete` 给用户。页面在 agentools.uno 的 `/device`：若未登录则先在网站登录，再点授权。**同一轮不要 `--poll`。**
3. 授权完成后，`login --poll` 拿到 **API Key**（`uno_…`）并写入 `~/.uno/credentials.json`
4. `--poll` 默认等 **10 分钟**。设备码本身有效 **30 分钟**。若 poll 超时，用**同一个** `device_code` 再跑一次 `--poll`
5. 服务端 key **不过期**。只需在这些情况重登：换机器 / 临时 `$HOME`；`logout`（只清本地，服务端 key 还在）；控制台或 `keys delete` 删了 key；账号停用；错误的 `UNO_API_KEY` 盖过了好文件
6. 某个工具返回 `auth_required` 是**那个 server** 的 OAuth/key，不是 Uno key 坏了

## 命令参考

所有命令默认输出格式化 JSON。添加 `--compact` 获取单行压缩输出（减少 token 消耗）。

### 状态查询

```bash
python bin/uno.py whoami               # 当前用户信息（积分、套餐、密钥）
python bin/uno.py health               # 服务器健康检查
```

### 搜索工具

```bash
python bin/uno.py search "天气" [--limit 10] [--mode hybrid|keyword|semantic] [--category dev] [--server weather-free]
```

`--limit` 取值范围 1-50（客户端与服务端双向校验）。

每条结果包含：
- `tool`（slug）、`name`、`desc`、`desc_en` — 展示与消歧
- `input_schema`（JSON Schema）— 用于构造 `call` 的参数
- `server`、`server_name`、`category`、`auth_required`
- `stats`：`{avg_ms, calls_7d, success_rate, rating}` — **同能力多 server 时据此选择**（优先 `calls_7d` 和 `rating` 更高的）
- `pricing`：`{mode, cost}` — `per_call` 按次积分 或 `per_token` 按量价格

若 `desc` 以 `…` 结尾，说明被截断（搜索路径 500 字符，浏览路径 200 字符）。完整描述用 `tool get <slug>`。

#### 搜索是怎么工作的（Agent 最佳实践）

搜索底层是**混合检索**：
1. **智能分词** — 自动剥离中英文停用词（`搜索/关于/项目/please/find/...`）、以子串方式剥离多字中文停用词、调用 `jieba` 分词、丢弃单 ASCII 字符。所以 `"搜索 GitHub 上关于 MCP 的项目"` 会被自动降噪为 `["github", "mcp"]`。
2. **关键词通道** — OR 候选选择 + 加权打分。最强信号是 server-slug 精确匹配（如 `"github"` → server `github` → +10 分）。
3. **语义通道** — pgvector 对工具描述 embedding 做余弦相似度（30 天 Redis 缓存）。
4. **自适应 RRF 融合** — 当关键词通道有明显赢家（server slug 精确命中）时，其权重放大至 2.5×，避免被双通道中等分淹没。

质量回归测试在 `tests/golden_queries.json`（52 条中英文 query）+ `scripts/evaluate_search.py`。最近一次生产实测（2026-04-18）：

| 指标 | 实测 | 目标 | 状态 |
|---|---|---|---|
| NDCG@5 | **0.889** | ≥ 0.75 | ✓ 达标 |
| MRR | **0.946** | ≥ 0.75 | ✓ 达标 |
| Recall@5 | **0.472** | ≥ 0.45 | ✓ 达标（数据集理论上限 ~0.54，见说明） |

中英文表现对称：NDCG@5 en=0.886，zh=0.895。Recall@5 上限受数据集标注方式限制——96% 的 query 标注了超过 5 个相关工具，因此 top-5 在数学上最多只能达到 ~54% 召回。

**查询技巧（重要性从高到低）：**
- **短关键词最佳**：`"天气"`、`"github mcp"`、`"image generation"` — 1-3 个词胜过一切
- **已知 server slug 优先**：`"github"`、`"trello"`、`"gmail"` — 精确匹配信号最强
- **整句提问也能工作**，因为 tokenizer 会自动去停用词；但短关键词仍然更快更准
- **中英文对称**：`"天气"` ≈ `"weather"`，`"搜索"` ≈ `"search"`
- **没结果时换同义词**：`"map"` → `"navigation"`，`"translate"` → `"翻译"`

**示例：**
| 用户意图 | 推荐查询 | 也能工作 | 预期 server |
|---|---|---|---|
| "伊朗以色列冲突 2025" | ✓ `search "news"` | `search "新闻"` | news-api, eodhd |
| "GitHub上有多少AI项目" | ✓ `search "github"` | `search "GitHub上有多少AI项目"`（停用词自动剥离） | github |
| "北京明天天气" | ✓ `search "weather"` | `search "天气"` | weather-free |
| "把这个发到推特" | ✓ `search "twitter"` | `search "推特"` | twitter |

### 工具详情

```bash
python bin/uno.py tool get <tool_slug>
# 例：python bin/uno.py tool get amap-maps.maps_weather
```

### 调用工具

```bash
python bin/uno.py call <tool_slug> --args '{"city":"北京"}'
```

响应：
```json
{"success": true, "data": {...}, "meta": {"latency_ms": 234, "credits_used": 1.0}}
```

### 评价工具

```bash
python bin/uno.py rate <tool_slug> <0-5> [--comment "好用"]
```

### 浏览服务

```bash
python bin/uno.py servers [--query "weather"] [--category search] [--limit 50]
```

### 断开第三方授权

```bash
python bin/uno.py disconnect <server_slug>
# 例：python bin/uno.py disconnect github
```

撤销已存储的 OAuth token 或 API Key。断开后，下次 `call` 会再次返回 `auth_required`。

### API 密钥管理

```bash
python bin/uno.py keys list            # 列出活跃的 API 密钥
python bin/uno.py keys create          # 创建新密钥
python bin/uno.py keys delete <key_id> # 删除密钥
```

## 工具分类（13 大类）

| 分类 | 说明 | 示例服务 |
|------|------|---------|
| `search` | 搜索与信息检索 | Jina、Tavily、百度搜索、秘塔AI搜索、Perplexity |
| `dev` | 开发与工程工具 | GitHub、Supabase、Firecrawl、context7、Sentry |
| `social` | 社交媒体与通讯 | 虾聊、Twitter、Discord、Instagram、微信文章 |
| `data` | 数据与分析 | BrightData、Google Drive、Wolfram Alpha、天气 |
| `creative` | 创意与内容生成 | Canva、美图、AI图像/视频/音乐生成、PPT |
| `finance` | 金融与投资 | 股票K线、且慢基金、加密货币、Yahoo Finance |
| `lifestyle` | 生活服务 | 滴滴出行、百度地图、12306、快递查询、天气 |
| `productivity` | 效率与办公 | Gmail、Google Calendar、Notion、Trello、Excel |
| `media` | 媒体处理 | ElevenLabs、YouTube、视频/音频转录与生成 |
| `enterprise` | 企业服务 | 企业信息查询、工商查询、风险信息、供应商管理 |
| `ecommerce` | 电商与消费 | 酒店预订、电商工具 |
| `health` | 健康医疗 | Theta Health |
| `other` | 其他工具 | Outlook、百度百科、百度学术 |

## Agent 工作流

0. **先 `whoami`** — 成功就不要再 login
1. **先搜索** — 不要猜测工具 slug 或参数
2. **读 `input_schema`** — 根据搜索结果中的 schema 构造参数
3. **按能力搜索**（"weather"、"search"、"translate"），而非用户意图
4. **使用 `--compact`** 减少输出体积（节省 token）
5. **若 `desc` 被截断**（以 `…` 结尾），用 `tool get <slug>` 获取完整描述
6. **重度使用前先查积分** — 免费套餐每日 500 积分
7. **错误处理**：
   - `auth_required` 且 `auth_type: "api_key"` → 提示用户提供 API Key（展示 `get_key_url` 和 `fields`）
   - `auth_required` 且含 `auth_url` → 展示 `auth_url` 给用户在浏览器完成 OAuth 授权，授权后重试
   - `tool_not_found` → 换关键词重新搜索
   - `insufficient_credits` → 提示用户充值：https://agentools.uno/pricing
   - 连接错误（超时、取消）→ 重试一次，失败则通知用户
8. **调用成功后评分** — 帮助优化搜索质量
9. **多个服务商提供相同能力时**（如 `github` vs `github-api`），优先选 `calls_7d` 或 `rating` 更高的

## 输出格式

- 调用成功：`{"success": true, "data": {...}, "meta": {"latency_ms": N, "credits_used": N}}`
- 其他成功：`{"success": true, "data": {...}}`
- 错误：`{"error": "描述", "hint": "...", ...}`，非零退出码

## 详细帮助

```bash
python bin/uno.py --help
python bin/uno.py search --help
python bin/uno.py call --help
```

## API 地址

优先 `https://agentools.uno`。CLI 默认 `https://clawdtools.uno` 仍提供 `/v1` 和 `/mcp`。可用 `--base-url` 或环境变量 `UNO_API_URL` 覆盖。不要用 `https://clawtools.uno`（拼写站，跳转会丢掉 `Authorization`）。
