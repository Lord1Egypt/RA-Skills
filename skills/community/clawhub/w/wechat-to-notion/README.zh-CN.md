# wechat-to-notion

将微信公众号文章一键保存到 Notion 数据库。自动提取标题、封面、正文内容（段落、标题、图片、代码块、列表），并通过 AI 生成关键词、评论和推荐星级。

## 功能

- **文章抓取** — 解析微信公众号 HTML，提取富文本（加粗/斜体）、代码块、列表、图片
- **智能分析** — AI 自动提取 3-5 个核心关键词，评估可读性与价值，给出 1-5 星推荐评级
- **精选标签** — 3 星及以上自动打上「Featured」标签，方便后续筛选
- **写入 Notion** — 自动检测数据库字段，分批写入内容 blocks，评论写入评论面板
- **字段自适应** — 按字段类型（而非名称）匹配，兼容中英文等任意语言的 Notion 数据库

## 快速开始

### 1. 获取 Notion API Key

1. 前往 [My Integrations](https://notion.so/my-integrations) → **+ New integration** → 复制 key（`ntn_` 开头）
2. 打开目标 Notion 数据库 → **...** → **Connect to** → 选择你的 integration

### 2. 创建 Notion 数据库

数据库需要以下字段（名称可自定义，脚本按类型自动匹配）：

| 字段类型 | 用途 | 示例名称 |
|---------|------|---------|
| Title | 文章标题 | 标题 |
| URL | 文章链接 | 链接 |
| Date | 阅读时间 | 阅读时间 |
| Select | 推荐星级 | 推荐 |
| Multi-select | 关键词标签 | 标签 |

Select 字段建议预设选项：⭐、⭐⭐、⭐⭐⭐、⭐⭐⭐⭐、⭐⭐⭐⭐⭐

### 3. 使用

```bash
# 设置 API Key
export NOTION_API_KEY="ntn_xxx"

# 抓取文章
python3 scripts/fetch_wechat.py <微信文章URL> > /tmp/wx_article.json

# 保存到 Notion
python3 scripts/save_to_notion.py \
  /tmp/wx_article.json \
  <notion_database_url> \
  <微信文章URL> \
  "2026-03-17T10:00:00+08:00" \
  "Claude Code,MCP,Agentic Workflow" \
  "结构清晰，干货密度高，适合想快速上手的开发者" \
  4
```

### 参数说明

| 参数 | 必填 | 说明 |
|------|------|------|
| article_json | 是 | fetch_wechat.py 的输出文件路径 |
| notion_url | 是 | Notion 数据库 URL |
| article_url | 是 | 微信文章原始 URL |
| read_time | 否 | ISO 8601 时间（默认当前时间） |
| keywords | 否 | 逗号分隔的关键词 |
| comment | 否 | 一句话评价（写入评论面板） |
| rating | 否 | 1-5 星推荐评级（≥3 自动加「Featured」标签） |

## 设计理念

本项目的首要目标是作为 [OpenClaw](https://github.com/nicholasgriffintn/OpenClaw) 的 skill 使用——`SKILL.md` 定义了完整的工作流，OpenClaw 会自动管理环境变量注入和工具链检查。

但脚本本身不依赖任何 skill 框架，只需要 `python3` 和 `curl`。因此你也可以将它集成到其他 AI agent 平台（Claude Code、Cursor、Windsurf 等），只要 agent 能读取 `SKILL.md` 中的指令并调用 shell 命令即可。

### 作为 OpenClaw Skill

安装后，在对话中发送微信文章链接即可触发自动化流程：抓取 → AI 分析（关键词 + 评论 + 评级） → 保存到 Notion。

```bash
openclaw config set skills.entries.wechat-to-notion.NOTION_API_KEY "ntn_xxx"
```

### 作为通用 Agent Skill

将本仓库克隆到你的 agent 工作目录，确保 `NOTION_API_KEY` 在环境变量中可用，agent 按照 `SKILL.md` 中的三步流程（fetch → analyze → save）执行即可。无需额外适配。

## 项目结构

```
├── SKILL.md                    # OpenClaw skill 定义
├── README.md                   # English
├── README.zh-CN.md             # 中文
└── scripts/
    ├── fetch_wechat.py         # 微信文章抓取与解析
    └── save_to_notion.py       # Notion 写入（字段检测、分批写入、评论）
```

## License

MIT
