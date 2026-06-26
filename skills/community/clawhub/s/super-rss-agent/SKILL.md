---
name: super_rss_agent
description: 功能强大的 RSS 订阅管理与阅读工具。用于 (1) 导入/导出 OPML 文件, (2) 管理 RSS 订阅源（支持自动发现）, (3) 扫描并追踪文章的已读/未读状态, (4) 无 RSS 站点的 HTML 抓取回退, (5) 渐进式阅读与文章摘要, (6) 文章搜索与统计, (7) 自动清理旧文章。
---

# Super RSS Agent

在 OpenClaw 中直接管理和消费 RSS 订阅。本 skill 替代传统 RSS 阅读器，提供 AI 驱动的摘要、渐进式阅读、文章追踪和自动化推送。

## 快速开始

```bash
# 添加博客（自动发现 RSS 订阅源）
python3 scripts/super_rss_agent.py add https://example.com --name "我的博客" --category 技术

# 扫描所有订阅，拉取新文章
python3 scripts/super_rss_agent.py scan

# 查看未读文章
python3 scripts/super_rss_agent.py articles

# 搜索文章
python3 scripts/super_rss_agent.py search "AI"

# 标记文章为已读
python3 scripts/super_rss_agent.py read 42

# 列出所有订阅
python3 scripts/super_rss_agent.py list

# 导出为 OPML
python3 scripts/super_rss_agent.py export -o my_feeds.opml
```

所有命令均支持 `--db <路径>` 全局参数指定自定义数据库文件。

## CLI 命令

### `list` - 列出订阅
```bash
super_rss_agent list                          # 列出所有订阅
super_rss_agent list --category Tech          # 按分类筛选
super_rss_agent list --verbose                # 显示订阅源 URL、选择器、上次扫描时间
```

### `add` - 添加订阅
```bash
super_rss_agent add <url>                                   # 从博客 URL 自动发现订阅源
super_rss_agent add <url> --name "我的博客" -c 技术          # 自定义名称和分类
super_rss_agent add <url> --feed-url <feed_url>             # 手动指定订阅源 URL
super_rss_agent add <url> --scrape-selector "article h2 a"  # 设置 HTML 抓取的 CSS 选择器
```

**Feed 自动发现**：输入博客主页 URL 时，代理会自动发现 RSS/Atom 订阅源：
1. 搜索 HTML 中的 `<link rel="alternate">` 标签
2. 尝试常见路径：`/feed`、`/rss`、`/feed.xml`、`/atom.xml` 等

### `remove` - 删除订阅
```bash
super_rss_agent remove "订阅名称"                # 按名称删除（需确认）
super_rss_agent remove "订阅名称" -y             # 跳过确认直接删除
super_rss_agent remove https://example.com/feed.xml  # 按 URL 删除
```

### `update` - 更新订阅信息
```bash
super_rss_agent update "订阅名称" -n "新名称"           # 修改名称
super_rss_agent update "订阅名称" -c "新分类"           # 修改分类
super_rss_agent update "订阅名称" --feed-url <new_url>  # 修改 Feed URL
super_rss_agent update "订阅名称" --url <new_url>       # 修改主页 URL
super_rss_agent update "订阅名称" --scrape-selector ""  # 清除 CSS 选择器
```

### `scan` - 扫描新文章
```bash
super_rss_agent scan                          # 扫描所有订阅
super_rss_agent scan "博客名称"                # 扫描指定博客
super_rss_agent scan --workers 10             # 使用 10 个并发线程
super_rss_agent scan --silent                 # 静默模式（不输出过程信息）
```

扫描器的工作流程：
1. 优先尝试 RSS/Atom 订阅源
2. 如果没有 feed_url，自动发现 Feed 并更新记录
3. 如果配置了 `scrape_selector`，回退到 HTML 抓取
4. 按 URL 自动去重
5. 将新文章存入数据库
6. 扫描完成后自动清理旧的已读文章（可通过 `config` 关闭）

### `articles` - 列出文章
```bash
super_rss_agent articles                      # 显示未读文章（默认每页 50 条）
super_rss_agent articles --all                # 包含已读文章
super_rss_agent articles --blog "博客名称"     # 按博客筛选
super_rss_agent articles --category "技术"     # 按分类筛选
super_rss_agent articles -n 20                # 每页 20 条
super_rss_agent articles --offset 50          # 翻页（跳过前 50 条）
```

### `search` - 搜索文章
```bash
super_rss_agent search "WASM"                 # 按关键词搜索标题和摘要
super_rss_agent search "AI" --all             # 搜索含已读文章
super_rss_agent search "Rust" -c "技术"        # 按分类筛选
super_rss_agent search "安全" -b "博客名称"     # 按博客筛选
super_rss_agent search "AI" -n 100            # 增加结果数量（默认 50）
```

### `read` / `unread` - 标记文章状态
```bash
super_rss_agent read <文章ID>                 # 标记为已读
super_rss_agent unread <文章ID>               # 标记为未读
```

### `read-all` - 全部标记为已读
```bash
super_rss_agent read-all                      # 全部标记为已读（需确认）
super_rss_agent read-all -y                   # 跳过确认
super_rss_agent read-all --blog "博客名称"     # 仅标记指定博客的文章
super_rss_agent read-all --category "技术"     # 仅标记指定分类的文章
```

### `check` - 健康检查
```bash
super_rss_agent check                         # 检查所有订阅源的连通性
```

### `fetch` - 实时拉取内容
```bash
super_rss_agent fetch "订阅名称"               # 拉取最新 5 条
super_rss_agent fetch "订阅名称" -n 10         # 拉取最新 10 条
super_rss_agent fetch "订阅名称" -v            # 显示链接
super_rss_agent fetch "订阅名称" --full-content # 拉取全文（如果订阅源支持）
```

### `digest` - 每日摘要
```bash
super_rss_agent digest                        # 获取今日更新
super_rss_agent digest -d 2                   # 获取近 2 天的更新
super_rss_agent digest -c "AI" --limit 5      # 按分类筛选
```

### `stats` - 订阅统计
```bash
super_rss_agent stats                         # 显示所有订阅的统计信息
super_rss_agent stats --stale-days 60         # 自定义死源检测阈值（默认 90 天）
```

显示内容：总订阅数、总文章数、未读数、数据库大小、按分类分组的各源活跃度和未读积压、疑似死源检测。

### `config` - 查看/修改配置
```bash
super_rss_agent config                        # 列出所有配置
super_rss_agent config auto_purge false       # 关闭自动清理
super_rss_agent config auto_purge_days 30     # 修改清理天数
super_rss_agent config auto_purge --reset     # 恢复默认值
```

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `auto_purge` | `true` | 扫描后是否自动清理旧的已读文章 |
| `auto_purge_days` | `90` | 自动清理多少天前的已读文章 |

### `purge` - 手动清理旧文章
```bash
super_rss_agent purge                         # 清理 90 天前的已读文章（需确认）
super_rss_agent purge -d 30                   # 清理 30 天前
super_rss_agent purge -b "博客名称"            # 仅清理指定博客
super_rss_agent purge --include-unread         # 同时清理未读文章
super_rss_agent purge -y                       # 跳过确认
```

### `test` - 测试订阅
```bash
super_rss_agent test https://example.com       # 测试 URL 是否可以订阅
super_rss_agent test https://example.com --scrape-selector "article h2 a"  # 测试 HTML 抓取
```

执行 5 步诊断：URL 验证 → 连通性测试 → Feed 类型检测 → Feed 自动发现 → 解析并展示样本文章。

### `export` - 导出为 OPML
```bash
super_rss_agent export                        # 导出为 rss_export_YYYYMMDD.opml
super_rss_agent export -o backup.opml         # 指定输出文件名
```

### `import` - 从 OPML 导入
```bash
super_rss_agent import follow.opml            # 从 OPML 文件导入
```

### 命令速查表

| 命令 | 说明 | 常用参数 |
|------|------|---------|
| `list` | 列出所有订阅 | `-c` 分类, `-v` 详细 |
| `add` | 添加订阅 | `-n` 名称, `-c` 分类, `--feed-url`, `--scrape-selector` |
| `remove` | 删除订阅 | `-y` 跳过确认 |
| `update` | 更新订阅信息 | `-n` 名称, `-c` 分类, `--feed-url`, `--url` |
| `check` | 健康检查 | — |
| `scan` | 扫描新文章 | `-w` 线程数, `-s` 静默 |
| `articles` | 列出文章 | `-a` 含已读, `-b` 按博客, `-c` 按分类, `-n` 每页条数, `--offset` |
| `search` | 搜索文章 | `-a` 含已读, `-b` 按博客, `-c` 按分类, `-n` 数量 |
| `read` | 标记已读 | 文章 ID |
| `unread` | 标记未读 | 文章 ID |
| `read-all` | 全部已读 | `-b` 按博客, `-c` 按分类, `-y` 跳过确认 |
| `fetch` | 实时拉取 | `-n` 条数, `-v` 详细, `--full-content` |
| `digest` | 每日摘要 | `-d` 天数, `-n` 条数, `-c` 分类 |
| `stats` | 订阅统计 | `--stale-days` 死源阈值 |
| `config` | 查看/修改配置 | `key`, `value`, `--reset` |
| `purge` | 清理旧文章 | `-d` 天数, `-b` 按博客, `--include-unread`, `-y` |
| `export` | 导出 OPML | `-o` 输出文件 |
| `import` | 导入 OPML | OPML 文件路径 |
| `test` | 测试订阅 | `--scrape-selector` |

## 数据存储

- **数据库**：`<skill-root>/super_rss_agent.db`（SQLite，与 SKILL.md 同级目录）
- **数据表结构**：

```sql
-- 博客/订阅源
blogs(id, name, url, feed_url, category, scrape_selector, last_scanned)

-- 文章（按博客分组追踪）
articles(id, blog_id, title, url, summary, content, published_date, discovered_date, is_read)

-- 配置（key-value 存储）
config(key, value)
```

- 文章按 URL 自动去重（UNIQUE 约束）
- 删除博客时，其下所有文章一并删除（CASCADE）
- 配置存储在 `config` 表中，未修改过的配置项使用代码中的默认值

## 定时自动化（Cron）

通过 OpenClaw 的 cron 工具定时执行 RSS 更新：

### 扫描 + 摘要示例
```json
{
  "schedule": {"kind": "cron", "expr": "0 9 * * *"},
  "payload": {
    "kind": "agentTurn",
    "message": "执行 'super_rss_agent scan' 拉取新文章，然后执行 'super_rss_agent articles --category AI' 列出未读文章并生成摘要"
  },
  "sessionTarget": "isolated"
}
```

### 代理执行流程
当被要求检查 RSS 订阅时，代理会：
1. 执行 `python3 scripts/super_rss_agent.py scan` 拉取并存储新文章
2. 执行 `python3 scripts/super_rss_agent.py articles --category <分类>` 列出未读
3. 如有需要，使用 `web_fetch` 获取文章全文
4. 生成摘要并格式化输出
5. 执行 `python3 scripts/super_rss_agent.py read-all -y` 将已处理的文章标记为已读

## 全文提取

部分 RSS 订阅源通过 `content:encoded`（RSS 2.0）或 `content`（Atom）字段提供文章全文。使用 `--full-content` 参数可直接提取并阅读：

```bash
super_rss_agent fetch "订阅名称" --limit 1 --full-content
```

**工作原理：**
- RSS 2.0 带 `content:encoded` 字段 → 可获取全文
- Atom 带 `content` 字段 → 可获取全文
- 仅有 `description`/`summary` → 只能获取摘要

**说明：**
- 全文提取会自动去除 HTML 标签，提升可读性
- 对于不提供全文的订阅源，可使用 `web_fetch` 或 `browser` 工具作为备选

## 渐进式阅读

本 skill 支持三级渐进式阅读：

**第 1 层 - 标题速览**：通过 `super_rss_agent articles` 快速浏览
**第 2 层 - 摘要概述**：代理通过 `super_rss_agent fetch` 总结感兴趣的文章
**第 3 层 - 全文阅读**：使用 `super_rss_agent fetch --full-content` 或 `web_fetch` 获取完整文章

交互示例：
```
用户："看看我 '技术' 分类的 RSS 有什么新内容"
→ 代理执行：super_rss_agent scan && super_rss_agent articles --category 技术
用户："搜索关于 AI 的文章"
→ 代理执行：super_rss_agent search "AI"
用户："那篇 AI 的文章详细说说"
→ 代理拉取全文并生成摘要
用户："标记为已读"
→ 代理执行：super_rss_agent read <id>
```

## 自动清理机制

每次执行 `scan` 命令后，系统会自动清理超过 `auto_purge_days` 天的已读文章（仅已读，未读文章不受影响）。清理结果在非静默模式下打印一行提示。可通过 `config auto_purge false` 关闭。手动清理使用 `purge` 命令。

## 文件结构

```
super_rss_agent/
├── SKILL.md              # 本文件（AI 代理指令）
├── requirements.txt      # Python 依赖
└── scripts/
    ├── super_rss_agent.py # CLI 入口（19 个子命令）
    ├── storage.py         # SQLite 数据库层
    └── scanner.py         # Feed 解析、自动发现、HTML 抓取、并发扫描
```

## 使用技巧

- 定期执行 `super_rss_agent scan`（或通过 cron 自动执行）保持文章列表最新
- 使用 `super_rss_agent articles` 快速查看新内容收件箱
- 使用 `super_rss_agent search` 按关键词快速检索文章
- 使用 `super_rss_agent stats` 查看订阅统计和死源检测
- 使用 `super_rss_agent check` 定期清理失效的订阅源
- 使用 `super_rss_agent test <url>` 在添加前测试 URL 是否可订阅
- 善用分类功能，按主题组织订阅，实现精准阅读
- 对没有 RSS 的网站，添加时设置 `--scrape-selector` 进行 HTML 抓取
- 配合 `tts` 工具可实现语音新闻播报
- 对 `web_fetch` 无法访问的复杂网站，使用 `browser` 工具
- 优先尝试 `super_rss_agent fetch --full-content`，比 `web_fetch` 更快（对支持的订阅源）
