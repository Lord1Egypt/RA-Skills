# super_rss_agent

一款功能强大的 RSS 订阅管理与阅读工具，专为 OpenClaw 设计。本 skill 替代传统 RSS 阅读器，提供 AI 驱动的摘要生成、渐进式阅读、文章追踪和自动化推送。

参照 [blogwatcher](https://github.com/Hyaxia/blogwatcher)（Go）项目的架构设计，使用 Python 实现。

## 功能特性

- **Feed 自动发现**：输入博客主页 URL，自动识别 RSS/Atom 订阅源
- **多格式支持**：RSS 2.0、Atom、RSS 1.0 (RDF) 三种格式统一解析
- **HTML 抓取回退**：对无 RSS 的站点，支持 CSS 选择器抓取文章列表
- **文章追踪**：已读/未读状态管理，按 URL 自动去重
- **OPML 支持**：轻松导入/导出已有订阅
- **订阅管理**：添加、删除、更新、分类管理，一条命令搞定
- **文章搜索**：按关键词快速搜索标题和摘要
- **健康检查**：自动验证订阅源连通性和内容有效性
- **订阅统计**：`stats` 命令总览各源活跃度、未读积压、死源检测
- **订阅测试**：`test` 命令一键诊断 URL 是否可订阅
- **自动清理**：扫描后自动清理 90 天前的已读文章，可通过 `config` 关闭
- **渐进式阅读**：
  - 第 1 层：标题速览
  - 第 2 层：AI 生成感兴趣文章的摘要
  - 第 3 层：深入阅读文章全文
- **并发扫描**：多线程并发拉取，可配置线程数
- **超时保护**：统一 deadline 机制，DNS/请求/下载/扫描全链路超时防护
- **安全防护**：SSRF 防护（内网地址屏蔽）+ XXE 防护（defusedxml）
- **定时自动化**：通过 OpenClaw cron 定时更新和推送摘要
- **AI 原生**：为 AI 代理量身定制，自动浏览、总结和监控信息

## 安装

1. 将本仓库克隆到 OpenClaw 工作区：
   ```bash
   cd ~/.openclaw/workspace/skills
   git clone <仓库地址> super_rss_agent
   ```
2. 安装 Python 依赖：
   ```bash
   pip install -r requirements.txt
   ```
3. OpenClaw 将在下一次会话中自动识别该 skill。

### 依赖说明

| 包名 | 最低版本 | 用途 |
|------|---------|------|
| `requests` | >=2.20.0 | HTTP 请求（重定向、重试、流式下载） |
| `defusedxml` | >=0.7.0 | 安全 XML 解析（XXE 防护） |
| `beautifulsoup4` | >=4.9.0 | HTML 抓取回退（CSS 选择器） |

Python 标准库依赖：`sqlite3`、`argparse`、`socket`、`xml.etree.ElementTree`、`html.parser`、`concurrent.futures`。

## 使用方式

可以直接对 OpenClaw 代理说：
- "导入我的 OPML 文件 `/path/to/follow.opml`"
- "帮我看看 'AI' 分类下的最新资讯"
- "检查一下我所有的 RSS 订阅源是否还能用"
- "每天早上 9 点给我推送 'Tech' 分类的订阅摘要"
- "扫描所有订阅，告诉我有哪些新文章"
- "测试一下 https://example.com 能不能订阅"

## CLI 命令

以下所有命令均通过 `python scripts/super_rss_agent.py` 调用，支持 `--db <路径>` 全局参数指定自定义数据库。

### 订阅管理

```bash
# 添加订阅（自动发现 RSS/Atom 源）
python scripts/super_rss_agent.py add https://example.com --name "我的博客" --category 技术

# 手动指定 feed URL / HTML 抓取选择器
python scripts/super_rss_agent.py add https://example.com --feed-url https://example.com/feed.xml
python scripts/super_rss_agent.py add https://example.com --scrape-selector "article h2 a"

# 列出所有订阅
python scripts/super_rss_agent.py list
python scripts/super_rss_agent.py list --category Tech --verbose

# 删除订阅
python scripts/super_rss_agent.py remove "订阅名称"
python scripts/super_rss_agent.py remove "订阅名称" -y   # 跳过确认

# 更新订阅信息（无需删除重建）
python scripts/super_rss_agent.py update "订阅名称" -n "新名称"
python scripts/super_rss_agent.py update "订阅名称" -c "新分类"
python scripts/super_rss_agent.py update "订阅名称" --feed-url https://example.com/new-feed.xml

# 检查所有订阅源连通性
python scripts/super_rss_agent.py check
```

### 扫描与阅读

```bash
# 扫描所有订阅，拉取新文章
python scripts/super_rss_agent.py scan
python scripts/super_rss_agent.py scan "博客名称"         # 扫描指定博客
python scripts/super_rss_agent.py scan --workers 10       # 10 个并发线程

# 查看未读文章（默认每页 50 条）
python scripts/super_rss_agent.py articles
python scripts/super_rss_agent.py articles --all          # 包含已读
python scripts/super_rss_agent.py articles --category "技术"
python scripts/super_rss_agent.py articles -n 20          # 每页 20 条
python scripts/super_rss_agent.py articles --offset 50    # 翻页

# 搜索文章
python scripts/super_rss_agent.py search "WASM"           # 按关键词搜索
python scripts/super_rss_agent.py search "AI" --all       # 搜索含已读
python scripts/super_rss_agent.py search "Rust" -c "技术"  # 按分类筛选

# 标记文章状态
python scripts/super_rss_agent.py read <文章ID>
python scripts/super_rss_agent.py unread <文章ID>
python scripts/super_rss_agent.py read-all -y             # 全部标记已读
python scripts/super_rss_agent.py read-all --category "技术"
```

### 实时拉取与摘要

```bash
# 实时拉取最新内容
python scripts/super_rss_agent.py fetch "订阅名称"
python scripts/super_rss_agent.py fetch "订阅名称" -n 10 --full-content

# 每日摘要
python scripts/super_rss_agent.py digest                  # 今日更新
python scripts/super_rss_agent.py digest -d 2 -c "AI"     # 近 2 天，按分类筛选
```

### OPML 导入导出

```bash
# 导出为 OPML
python scripts/super_rss_agent.py export -o backup.opml

# 从 OPML 导入
python scripts/super_rss_agent.py import follow.opml
```

### 统计与维护

```bash
# 查看订阅统计（各源文章数、未读积压、死源检测）
python scripts/super_rss_agent.py stats
python scripts/super_rss_agent.py stats --stale-days 60   # 自定义死源阈值

# 手动清理旧文章（默认 90 天前的已读文章）
python scripts/super_rss_agent.py purge
python scripts/super_rss_agent.py purge -d 30             # 清理 30 天前
python scripts/super_rss_agent.py purge -b "博客名称"      # 仅清理指定博客
python scripts/super_rss_agent.py purge --include-unread   # 同时清理未读
python scripts/super_rss_agent.py purge -y                 # 跳过确认

# 查看/修改配置
python scripts/super_rss_agent.py config                   # 列出所有配置
python scripts/super_rss_agent.py config auto_purge false   # 关闭自动清理
python scripts/super_rss_agent.py config auto_purge_days 30 # 修改清理天数
python scripts/super_rss_agent.py config auto_purge --reset # 恢复默认值
```

### 订阅测试

```bash
# 测试 URL 是否可以订阅（只读，不写入数据库）
python scripts/super_rss_agent.py test https://example.com

# 测试 HTML 抓取
python scripts/super_rss_agent.py test https://example.com --scrape-selector "article h2 a"
```

`test` 命令执行 5 步诊断：URL 验证 → 连通性测试 → Feed 类型检测 → Feed 自动发现 → 解析并展示样本文章。

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

## 架构

三文件分层架构，依赖关系单向流动：

```
super_rss_agent.py (CLI 入口，19 个子命令)
  ├── 导入 → storage.py (SQLite 持久化层)
  └── 导入 → scanner.py (网络 I/O + 解析层)
```

`scanner.py` 和 `storage.py` 互不依赖，均为独立模块。

### storage.py — 数据层

- `Storage` 类封装 SQLite 连接，支持上下文管理器（`with` 语句）
- 数据库路径默认为 skill 根目录下的 `super_rss_agent.db`
- 三张表：`blogs`（订阅源）、`articles`（文章）、`config`（配置）
- 使用 WAL 模式提升并发性能，启用外键约束，5 秒 busy timeout
- 文章通过 `url` 字段的 UNIQUE 约束实现自动去重（`INSERT OR IGNORE`）
- 删除博客时其下所有文章一并级联删除（ON DELETE CASCADE）

### scanner.py — 解析与扫描层

- `parse_feed_xml()`：统一解析 RSS 2.0 / Atom / RSS 1.0 (RDF)
- `discover_feed_url()`：从博客主页自动发现 feed（`<link rel="alternate">` + 常见路径探测），带 30 秒总时间预算
- `scrape_articles_html()`：CSS 选择器 HTML 抓取回退
- `scan_blog()` / `scan_all()`：扫描编排，优先 RSS → 自动发现 → HTML 回退；`scan_all` 使用 `ThreadPoolExecutor` 并发
- `fetch_url()`：统一 HTTP 请求入口，带 SSRF 防护、指数退避重试和响应大小限制
- `strip_html()`：安全清理 HTML 标签，跳过 `<script>`/`<style>` 等危险标签

### super_rss_agent.py — CLI 层

- argparse 入口，19 个子命令
- 每个 `cmd_*` 函数为薄封装，业务逻辑委托给 storage/scanner
- Windows 兼容：启动时检测 stdout 编码，必要时包装为 UTF-8

## 数据库结构

```sql
-- 博客/订阅源
CREATE TABLE blogs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    name            TEXT NOT NULL,
    url             TEXT NOT NULL,
    feed_url        TEXT NOT NULL UNIQUE,
    category        TEXT NOT NULL DEFAULT 'Uncategorized',
    scrape_selector TEXT,
    last_scanned    DATETIME
);

-- 文章（按博客分组追踪）
CREATE TABLE articles (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    blog_id         INTEGER NOT NULL,
    title           TEXT NOT NULL,
    url             TEXT NOT NULL UNIQUE,
    summary         TEXT,
    content         TEXT,
    published_date  DATETIME,
    discovered_date DATETIME NOT NULL,
    is_read         INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (blog_id) REFERENCES blogs(id) ON DELETE CASCADE
);

-- 配置（key-value 存储）
CREATE TABLE config (
    key   TEXT PRIMARY KEY,
    value TEXT NOT NULL
);
```

## 配置系统

配置存储在数据库的 `config` 表中。未修改过的配置项使用代码中的默认值，只有用户主动修改过的值才写入数据库。

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `auto_purge` | `true` | 扫描后是否自动清理旧的已读文章 |
| `auto_purge_days` | `90` | 自动清理多少天前的已读文章 |

```bash
# 查看所有配置
super_rss_agent config

# 关闭自动清理
super_rss_agent config auto_purge false

# 恢复默认值
super_rss_agent config auto_purge --reset
```

### 自动清理机制

每次执行 `scan` 命令后，系统会自动清理超过 `auto_purge_days` 天的已读文章（仅已读，未读文章不受影响）。清理结果在非静默模式下打印一行提示。可通过 `config auto_purge false` 关闭。

## 安全机制

### SSRF 防护

所有 HTTP 请求经过 `_validate_url_safe()` 检查，屏蔽以下地址范围：

| 范围 | 说明 |
|------|------|
| `127.0.0.0/8` | 回环地址 |
| `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16` | 私有网络 |
| `169.254.0.0/16` | Link-local / 云元数据 |
| `0.0.0.0/8`, `100.64.0.0/10` | 当前网络 / 共享地址空间 |
| `::1/128`, `fc00::/7`, `fe80::/10` | IPv6 回环/私有/Link-local |

仅允许 `http` 和 `https` 协议。手动跟随重定向并对每个跳转地址重新验证。

### XXE 防护

优先使用 `defusedxml` 进行 XML 解析，禁用外部实体。回退到标准库时使用安全解析模式。

### 输入清理

- CLI 层对用户输入进行文本清理（移除控制字符、截断）
- URL 格式验证 + SSRF 安全验证双重检查
- OPML 导入时逐条验证 URL 格式

## 超时与异常处理

系统在多个层级实现了超时保护，防止单个故障阻塞整体：

### 底层：统一 deadline 机制

`_fetch_once()` 在入口设定时间预算（`deadline`），重定向循环和 `iter_content` 下载共享同一个 deadline：
- 每次重定向前检查剩余时间
- 下载过程中每个 chunk 后检查 deadline
- 超时则立即关闭连接并抛出 `TimeoutError`

### DNS 解析保护

`_validate_url_safe()` 将 `socket.getaddrinfo()` 放入独立线程执行，5 秒超时。DNS 卡死不会阻塞主流程。

### 中间层：发现过程时间预算

`discover_feed_url()` 设有 30 秒总时间预算。在验证候选 URL 和探测常见路径时，每次操作前检查剩余时间，预算耗尽则立即返回。

### 编排层：全局超时

| 场景 | 超时策略 |
|------|---------|
| `scan_all()` | `min(90 × 博客数, 300)` 秒总超时 |
| `cmd_check()` | `min(60 × 博客数, 300)` 秒总超时 |
| `cmd_digest()` 回退 | `min(60 × 博客数, 300)` 秒总超时 |

超时后未完成的任务被标记为错误或静默跳过，不会无限期阻塞。

### 重试策略

- 仅对 429/5xx 状态码和连接超时进行重试（最多 3 次）
- 指数退避：1s → 2s → 4s
- 遵循 429 响应的 `Retry-After` 头部（上限 30 秒）
- `SSRFError`、`ResponseTooLargeError` 等安全错误不重试

### 网络配置常量

| 常量 | 值 | 说明 |
|------|-----|------|
| `REQUEST_TIMEOUT` | 30s | 单次 HTTP 请求超时 |
| `MAX_RESPONSE_BYTES` | 10MB | 响应体大小上限 |
| `MAX_RETRIES` | 3 | 最大重试次数 |
| `DNS_RESOLVE_TIMEOUT` | 5s | DNS 解析超时 |
| `DISCOVER_TIMEOUT` | 30s | Feed 发现总时间预算 |

## 扫描工作流程

```
scan_blog(blog)
│
├── 1. 有 feed_url? ──→ fetch_url() + parse_feed_xml()
│       ↓ 成功则返回
│
├── 2. 有 url? ──→ discover_feed_url() ──→ fetch + parse
│       ↓ 发现成功则更新 blog.feed_url
│
├── 3. 有 scrape_selector? ──→ scrape_articles_html()
│       ↓ 成功则清除之前的 RSS 错误
│
└── 4. 按 URL 去重 ──→ 返回 (ScanResult, articles)
```

`scan_all()` 使用 `ThreadPoolExecutor` 并发执行上述流程，默认 5 个 worker。

扫描完成后，若 `auto_purge` 配置为 `true`（默认），自动清理超过 `auto_purge_days` 天的已读文章。

## 目录结构

```
super_rss_agent/
├── README.md             # 本文件
├── CLAUDE.md             # Claude Code 开发指南
├── SKILL.md              # AI 代理的核心指令文件
├── requirements.txt      # Python 依赖声明
├── super_rss_agent.db    # SQLite 数据库（运行时自动创建）
└── scripts/
    ├── super_rss_agent.py # CLI 入口（19 个子命令）
    ├── storage.py         # SQLite 数据库层（数据持久化）
    └── scanner.py         # Feed 解析、自动发现、HTML 抓取、并发扫描
```

## 开发与验证

本项目没有正式的测试框架，验证依赖语法检查和手动集成测试：

```bash
# 语法检查
python -c "import py_compile; py_compile.compile('scripts/super_rss_agent.py', doraise=True)"
python -c "import py_compile; py_compile.compile('scripts/storage.py', doraise=True)"
python -c "import py_compile; py_compile.compile('scripts/scanner.py', doraise=True)"

# 快速验证 storage 层（内存数据库）
python -c "
import sys; sys.path.insert(0, 'scripts')
from storage import Storage
db = Storage(':memory:')
bid = db.add_blog('Test', 'https://example.com', 'https://example.com/feed.xml', 'Tech')
db.insert_articles(bid, [{'title': 'A', 'url': 'https://example.com/1'}])
print(db.list_articles())
"

# 功能验证
python scripts/super_rss_agent.py test https://blog.rust-lang.org/
python scripts/super_rss_agent.py --help
```
  
### 扩展指南

- **添加新 CLI 命令**：在 `super_rss_agent.py` 中添加 `cmd_xxx` 函数 + argparse 子解析器 + commands 字典注册。业务逻辑放 storage/scanner，CLI 层只做输入解析和输出格式化。
- **修改数据库结构**：在 `storage.py` 的 `_SCHEMA_SQL` 中修改建表语句，注意 SQLite 不支持 `ALTER TABLE DROP COLUMN`。
- **添加新的网络解析逻辑**：在 `scanner.py` 中实现，所有 HTTP 请求必须经过 `fetch_url()` 以确保 SSRF 防护和统一的超时/重试策略。

### 请我喝杯咖啡
- ![License](https://raw.githubusercontent.com/ohyeah521/super_rss_agent/main/img/buymecoffee.jpg)


## 参与贡献

欢迎贡献代码！请随时提交 Pull Request 或创建 Issue 进行讨论。
