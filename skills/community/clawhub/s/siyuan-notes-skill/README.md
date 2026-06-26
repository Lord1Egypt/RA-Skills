# siyuan-notes-skill

**如果你是claude/codex/kimi等等大语言模型请阅读SKILL.md,此文件应由人类阅读**

[Claude Code](https://claude.com/claude-code) 的 [思源笔记](https://b3log.org/siyuan/) 技能 —— 通过自然语言搜索、阅读、编辑和组织笔记。

## 功能特性

- **搜索与阅读** — 全文搜索、长文档自动截断阅读、章节级阅读、文档内搜索
- **创建与编辑** — 创建文档、追加/插入/更新/删除块、替换章节、PMF 批量编辑
- **结构管理** — 笔记本列表、文档树、标题大纲、反向链接、未引用文档
- **安全保护** — 先读后写守卫、乐观锁版本检查、默认只读模式
- **高级功能** — SQL 查询思源 SQLite 数据库、每日笔记、任务、书签、标签

## 环境要求

- **Node.js 18+**（使用内置 `fetch`）
- **思源内核** 运行中且 API 可访问（本地或远程）
- **Claude Code** CLI

## 快速开始

### 1. 安装

```bash
# 作为 Claude Code 技能安装（稳定版）
claude mcp add-skill https://github.com/fanxing-6/siyuan-notes-skill/archive/refs/tags/v1.0.5.tar.gz

# 或使用 main 分支最新版
claude mcp add-skill https://github.com/fanxing-6/siyuan-notes-skill
```

### 2. 配置

在技能目录创建 `.env` 文件（或设置环境变量）：

```bash
SIYUAN_SERVER=http://127.0.0.1:6806
SIYUAN_TOKEN=your-api-token
SIYUAN_ENABLE_WRITE=false   # 设为 true 启用写入操作
```

### 3. 验证

```bash
node index.js check    # 连接检查
node index.js version  # 内核版本
```

## 使用示例

```bash
# 搜索笔记
node index.js search "项目总结" 5

# 阅读文档
node index.js open-doc "20260206204419-vgvxojw" readable

# 创建新文档
printf '## 第一章\n内容' | SIYUAN_ENABLE_WRITE=true node index.js create-doc "笔记本ID" "我的文档"

# 编辑块
printf '更新内容' | SIYUAN_ENABLE_WRITE=true node index.js update-block "块ID"

# SQL 查询
node -e "const s = require('./index.js'); s.executeSiyuanQuery('SELECT * FROM blocks WHERE type=\"d\" LIMIT 5').then(r => console.log(s.formatResults(r)));"
```

## 文档

| 页面 | 说明 |
|------|------|
| [命令参考](Command-Reference) | 所有命令的参数、默认值和示例 |
| [写入安全协议](Write-Safety-Protocol) | 先读后写守卫、版本检查、写入模式 |
| [PMF 规范](PMF-Spec) | 批量编辑用的 Patchable Markdown Format |
| [SQL 参考](SQL-Reference) | 思源 SQLite 表结构、块类型、查询示例 |
| [KaTeX 公式规则](KaTeX-Formula-Rules) | 思源数学公式书写规范 |
| [错误恢复](Error-Recovery) | 常见错误及解决方法 |

## 项目结构

```
siyuan-notes-skill/
├── index.js           # 核心 API 和 CLI 入口
├── cli.js             # CLI 参数解析
├── format-utils.js    # 输出格式化
├── lib/               # 内部模块
│   └── pmf-utils.js   # PMF 解析和补丁
├── SKILL.md           # 面向 LLM 的技能描述
└── docs/              # 详细文档
    ├── command-reference.md
    ├── pmf-spec.md
    └── sql-reference.md
```

## 许可证

MIT
