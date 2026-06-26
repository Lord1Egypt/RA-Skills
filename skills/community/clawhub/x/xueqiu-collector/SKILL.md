---
name: xueqiu-collector
version: "1.0.0"
description: >
  雪球帖子全量采集 Skill。采集任意雪球用户的全部帖子（含完整正文、图片下载、OCR识别），
  自动做 V4 规则分析（帖子类型/投资相关性/情感/操作意图/主题标签/质量评分），
  结果存入 SQLite 数据库并导出 JSON + Markdown 备份。
  
  触发词：采集雪球、雪球帖子采集、爬取雪球、收集雪球、雪球用户数据、雪球投资记录、
  雪球全量采集、抓取雪球帖子、同步雪球数据、xueqiu、下载雪球、雪球增量采集
  
  适用场景：
  - 用户说"帮我采集某人的雪球帖子"
  - 用户说"同步/更新雪球数据"
  - 用户说"抓取雪球用户帖子"
  - 用户说"雪球有新帖，更新一下"
read_when:
  - 用户需要采集雪球帖子
  - 用户需要分析雪球用户数据
  - 涉及雪球爬取、采集、同步操作
---

# xueqiu-collector — 雪球帖子采集 Skill

## 功能概述

本 Skill 可以采集任意雪球用户的全部帖子，包括：
1. **全量/增量采集** — 自动判断采集模式（首次全量，后续增量）
2. **完整正文提取** — 含 Markdown 格式化、blockquote 评论识别
3. **图片处理** — 下载帖子图片并 OCR 识别内容（winocr/tesseract）
4. **V4 规则分析** — 零 token 消耗，采集即分析：
   - 帖子类型（原创/评论/错误/空内容）
   - 投资相关性（high/medium/low/none）
   - 情感分析（看多/看空/中性）
   - 操作意图（买入/卖出/持有/观察）
   - 主题标签（估值分析/财务分析/操作记录…）
   - 质量评分（1-5分）
5. **数据导出** — SQLite 数据库 + JSON + Markdown（全量及按分类）

## 前置依赖

| 依赖项 | 说明 |
|--------|------|
| `playwright-cli` (npx) | 浏览器自动化，用于页面采集 |
| Edge 浏览器 + 真实 Profile | 挂载登录态，避免触发验证码 |
| Python 3.10+ | 运行采集脚本 |
| `winocr`（可选） | Windows 系统内置 OCR，识别帖子图片文字 |
| SQLite | 数据持久化，系统内置无需安装 |

## 快速开始

```bash
# 0. 环境检测（首次使用必跑！）
py scripts/check_env.py

# 1. 首次运行（不传参数，自动进入配置向导）
py scripts/collect.py
# → 会引导输入昵称和 URL

# 2. 增量采集（推荐，直接传参跳过向导）
py scripts/collect.py --author "用户昵称" --url "https://xueqiu.com/u/7712999844"

# 2. 强制扫描列表找新帖
py scripts/collect.py --author "用户昵称" --url "https://xueqiu.com/u/7712999844" --refresh-list

# 3. 强制重采正文（不重爬列表）
py scripts/collect.py --author "用户昵称" --url "https://xueqiu.com/u/7712999844" --force-collect

# 4. 只采集最新10条
py scripts/collect.py --author "用户昵称" --url "https://xueqiu.com/u/7712999844" --force-collect --latest --limit 10

# 5. 批量规则分析（对已采集的帖子补做V4分析）
py scripts/analyze.py --db "path/to/db.db" --missing
```

## SOP（标准操作流程）

### 场景一：首次采集某用户的全部帖子

```
用户说："帮我采集 @随缘的人生体验 的全部雪球帖子"
```

**步骤：**
1. 确认用户昵称和主页 URL（可从 `https://xueqiu.com/u/{UID}` 格式获取）
2. 确认数据库路径（默认：项目 `db/stock_analysis.db`）
3. 确认输出目录（默认：项目 `data/xueqiu/{昵称}/`）
4. 运行：`py scripts/collect.py --author "昵称" --url "URL" --db "db路径" --out-dir "输出路径"`
5. 等待采集完成，报告统计数据

### 场景二：增量更新（常规日常任务）

```
用户说："同步一下雪球数据" / "雪球有新帖，更新一下"
```

**步骤：**
1. 检查已知配置（从记忆中读取上次的 author + url）
2. 直接运行增量采集：`py scripts/collect.py --author "昵称" --url "URL" --refresh-list`
3. 报告新增帖子数量

### 场景三：补充采集正文

```
用户说："有些帖子只有标题没有正文，帮我补全"
```

**步骤：**
1. 运行：`py scripts/collect.py --author "昵称" --url "URL"`（默认只采集缺正文的帖子）
2. 报告补全数量

### 场景四：对历史帖子做 V4 规则分析

```
用户说："帮我分析一下数据库里的帖子"
```

**步骤：**
1. 运行：`py scripts/analyze.py --db "db路径" --missing`（只分析未分析的）
2. 或全量重分析：`py scripts/analyze.py --db "db路径" --batch`

## 配置说明

### 路径配置（collect.py 参数）

| 参数 | 说明 | 示例 |
|------|------|------|
| `--author` | 用户昵称（用于数据目录隔离） | `随缘的人生体验` |
| `--url` | 雪球主页 URL | `https://xueqiu.com/u/7712999844` |
| `--db` | SQLite 数据库路径 | `db/stock_analysis.db` |
| `--out-dir` | 数据输出根目录 | `data/xueqiu` |
| `--npx` | npx 可执行路径 | `C:\Users\xxx\nodejs\npx.cmd` |
| `--edge-profile` | Edge Profile 路径 | `C:\Users\xxx\AppData\Local\Microsoft\Edge\User Data\Default` |

### 反爬虫配置（内置默认值）

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `MIN_DELAY` | 2.0 秒 | 最小请求间隔 |
| `MAX_DELAY` | 5.0 秒 | 最大请求间隔 |
| `MAX_RETRIES` | 3 | 最大重试次数 |
| `stop_on_no_new` | 3 | 连续 N 页无新帖停止 |

## 输出格式

```
data/xueqiu/{昵称}/
  ├── posts_full.json          全量 JSON（所有帖子，时间倒序）
  ├── posts_full.md            全量 Markdown
  ├── classified/              按分类的 JSON 文件
  │   ├── 腾讯控股.json
  │   ├── 操作日记.json
  │   └── ...
  ├── md/                      按分类的 Markdown 文件
  │   ├── 腾讯控股.md
  │   └── ...
  └── images/                  帖子图片
      ├── 382580032_1.jpg
      └── ...
```

## 数据库表结构（xueqiu_posts）

| 字段 | 类型 | 说明 |
|------|------|------|
| `post_id` | TEXT | 雪球帖子 ID |
| `author` | TEXT | 作者昵称 |
| `author_id` | TEXT | 作者 UID |
| `title` | TEXT | 帖子标题 |
| `content` | TEXT | 列表页摘要 |
| `full_content` | TEXT | 完整正文（Markdown 格式） |
| `category` | TEXT | 分类（腾讯控股/操作日记/宏观分析…） |
| `published_at` | TEXT | 发帖日期（YYYY-MM-DD） |
| `url` | TEXT | 帖子链接 |
| `like_count` | INTEGER | 点赞数 |
| `comment_count` | INTEGER | 评论数 |
| `repost_count` | INTEGER | 转发数 |
| `read_count` | TEXT | 阅读数（含"万"等单位） |
| `image_ocr_text` | TEXT | 图片 OCR 识别内容 |
| `post_type` | TEXT | 帖子类型（original/reply/error/empty） |
| `own_text` | TEXT | 评论帖中用户自己的话 |
| `quote_text` | TEXT | 评论帖引用的原文 |
| `reply_to_post_id` | TEXT | 评论指向的原帖 ID |
| `investment_relevance` | TEXT | 投资相关性（high/medium/low/none） |
| `sentiment` | TEXT | 情感（看多/看空/中性） |
| `trade_intent` | TEXT | 操作意图（买入/卖出/持有/观察/无） |
| `content_type` | TEXT | 内容类型（交易记录/数据分析/深度分析/讨论交流…） |
| `quality_score` | INTEGER | 质量评分（0-5） |
| `summary` | TEXT | 规则摘要（前300字） |
| `topics` | TEXT | 主题标签（JSON 数组） |
| `tags` | TEXT | 提及股票（JSON 数组） |
| `word_count` | INTEGER | 正文字数 |

## 注意事项

1. **浏览器登录态**：首次运行会自动启动 Edge 并导航到目标页面，需确保已登录雪球
2. **采集速度**：内置随机延迟，每条正文 2-5 秒，每20条强制休息 8-12 秒
3. **日志监控**：采集日志保存到 `logs/xueqiu_collect.log`，可用 `py read_log.py` 监控
4. **OCR 支持**：需要安装 `winocr` + `pillow`（`pip install winocr pillow`）
5. **分类关键词**：可在 `references/category_keywords.json` 中自定义股票/主题分类规则

## 踩坑经验

- `playwright-cli eval` 只支持单行 JS，多行会导致序列化失败
- 雪球列表页时间格式多变（昨天/前天/X天前/X小时前/MM-DD/YYYY-MM-DD），已全部处理
- 评论帖有三种格式（A/B/C），`xueqiu_analyzer.py` 已全部覆盖
- Edge Profile 路径含空格时，必须用 Python subprocess 列表方式传参，不能字符串拼接
- CMD 中文路径会乱码，所有含中文路径的启动器必须用 PowerShell + UTF-8
