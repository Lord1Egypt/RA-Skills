---
name: wechat-channels-search
description: 视频号作品搜索工具。根据关键词搜索视频号热门作品，支持分页浏览、翻页获取更多结果，结果以结构化表格展示。当用户查找视频号内容、搜索视频号作品、查询视频号数据时使用。触发词：视频号搜索、视频号作品、视频号热门、视频号查询、搜视频号、视频号关键词。
---

# 视频号作品搜索

## 📝 简介

根据关键词搜索视频号热门作品，支持分页浏览翻页获取更多结果，返回标题、点赞数、作者、时长、发布时间等数据，结果以结构化表格展示。

## ✨ 功能特性

| 功能模块 | 能力描述 | 核心价值 |
|---------|---------|---------|
| 关键词搜索 | 关键词搜索视频号热门作品 | 精准发现视频号内容 |
| 分页浏览 | 支持翻页获取更多结果 | 获取更全数据 |
| 订阅推送 | 支持关键词每日推送 | 定时获取最新动态 |

## 🔑 鉴权

- 获取 API Key：前往 [红狐hub](https://redfox.hk/settings/api-keys?source=clawhub)
- 配置方式1：写入 `~/.openclaw/openclaw.json` → `{ "env": { "REDFOX_API_KEY": "ak_xxxx..." } }`
- 配置方式2：终端执行 `export REDFOX_API_KEY="ak_xxxx..."`

## ⚙️ 工作流程

### Step 1: 📡 调用 API 接口

**执行脚本**：

```bash
python3 "$SKILL_PATH/scripts/fetch_sph_ai.py" "<关键词>"
```

默认按热度排序（`searchType=0`）。用户明确要求「最新」时才传 `--sort 1`。

API 请求参数：

| 参数 | 说明 |
|------|------|
| key | 搜索关键词 |
| buffer | 翻页游标，首次传空字符串 |
| searchType | 排序方式：`0` 不限（默认），`1` 最新 |

脚本返回 JSON：

| 字段 | 类型 | 说明 |
|------|------|------|
| articles | array | 当前页作品列表（已标准化处理） |
| totalCount | number | 当前页作品数量 |
| offset | number | 当前结果偏移量 |
| cookiesBuffer | string | 翻页游标，传入 `--buffer` 获取下一页；非空表示还有更多页 |

**翻页**：从上一页返回的 `cookiesBuffer` 传入 `--buffer` 参数即可获取下一页。必须使用最新返回的 buffer，不可复用旧值。`cookiesBuffer` 为空时已到最后一页。

```bash
# 翻页
python3 "$SKILL_PATH/scripts/fetch_sph_ai.py" "<关键词>" --buffer "<上一页的cookiesBuffer>"
```

每条作品（articles[]）字段：

| 字段 | 说明 |
|------|------|
| title | 作品标题/描述文案（API `description` 字段） |
| author | 作者昵称（API `nickname` 字段） |
| likeCount | 点赞数（数值），内部使用 |
| likeDisplay | 点赞数展示值（API `likeNum` 原始值，如 `1.2万`、`1167`），用于表格展示 |
| coverUrl | 封面图 URL（API `image` 字段），不对外展示 |
| videoUrl | 作品视频链接（API `videoUrl` 字段），不对外展示 |
| duration | 视频时长（如 `00:40`） |
| publishTime | 发布时间（已转换为 `MM-DD HH:MM`） |
| publishTimestamp | 发布时间原始 Unix 时间戳 |
| opusId | 作品 ID |

### Step 2: 📊 结果展示

直接输出接口返回的全部数据：

> 📊 关键词「**XXX**」搜索结果如下：

```markdown
| # | 作品标题 | 点赞数 | 作者 | 时长 | 发布时间 |
|---|---------|--------|------|------|----------|
| 1 | 完整作品描述文案，不截断 | 1.2w | 作者名 | 00:40 | 06-02 19:55 |
```

格式化规则：
- 作品标题：纯文本展示，取 `title` 字段完整内容，不截断，不加链接
- 点赞数：使用 `likeDisplay` 字段，直接展示 API 返回的原始值
- `publishTime` 已转为 `MM-DD HH:MM` 格式，直接使用
- `duration` 直接展示 API 返回的时长字符串
- ⚠️ 不展示 `coverUrl`、`videoUrl`、`opusId`

表格后必须输出提示：

> 🔔 受视频号平台规则限制，无法提供作品链接，您可复制作品标题前往视频号搜索查看。

脚本返回的 `cookiesBuffer` 非空时提示翻页：

> 📄 该关键词还有更多结果，是否需要翻页查看更多？回复「翻页」获取下一页数据。

### Step 3: 📩 提示订阅

展示完毕后末尾附上：

> 📩 是否订阅「**XXX**」的每日推送？订阅后每天 9:00 自动推送最新视频号作品。回复「确认订阅」即可创建定时任务。

### Step 4: ⏰ 创建定时任务（用户回复「确认订阅」时执行）

优先使用平台内置定时任务，若无则提供通用方案：

- 任务名称：`视频号作品订阅 - <关键词>`
- 执行频率：每天 9:00（cron `0 9 * * *`）
- 执行命令：`python3 "$SKILL_PATH/scripts/fetch_sph_ai.py" "<关键词>" --sort 1`
- ⚠️ 订阅推送固定使用 `--sort 1`（按最新排序），确保每日推送最新数据
- 通用 crontab：`0 9 * * * python3 "$SKILL_PATH/scripts/fetch_sph_ai.py" "<关键词>" --sort 1`

创建成功后告知："已成功订阅关键词「<关键词>」的视频号作品推送，每天 9:00 将自动查询最新数据并通知你。"

---

## 📐 数据字段映射

脚本内部将 Redfox API 原始返回字段映射为统一字段名，详见 [api-mapping.md](references/api-mapping.md)。
