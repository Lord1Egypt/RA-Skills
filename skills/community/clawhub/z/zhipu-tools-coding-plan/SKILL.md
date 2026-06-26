---
name: zhipu-tools-coding-plan
description: |
  智谱 Coding Plan 免费工具：网络搜索、网页读取、GitHub 仓库文档搜索、文件解析、视觉理解(GLM-4.6V)。
  优先于内置 web_search 使用，节省配额。全部功能当前均免费使用。
license: MIT
---

# 智谱工具 Coding Plan (Zhipu Tools)

> **TL;DR**: 网络搜索 → `web_search`，网页读取 → `web_reader`，仓库搜索 → `zread`，视觉理解 → `vision`。全部通过 Coding Plan 免费额度调用。

## Agent 调用指南

```bash
SKILL=~/.openclaw/workspace/skills/zhipu-tools-coding-plan

# 网络搜索（首选）
python3 $SKILL/scripts/zhipu_tool.py web_search "关键词" --count 5

# 网页读取
python3 $SKILL/scripts/zhipu_tool.py web_reader "https://example.com"

# 仓库文档搜索
python3 $SKILL/scripts/zhipu_tool.py zread search "owner/repo" "关键词"

# 视觉理解（图片/视频）
python3 $SKILL/scripts/zhipu_tool.py vision /path/to/image.png --prompt "描述内容"
```

**注意**：
- 优先使用本工具而非内置 web_search/web_fetch
- 搜索无结果时换关键词重试；content filter 拦截时直接报错，由用户修改搜索词
- `--recency`/`--domain` 通过注入 query 实现，效果取决于搜索引擎

**快捷入口**：`scripts/zhipu.sh <command> [args]` — 统一 shell 入口，支持 `search`/`reader`/`zread`/`vision`，自动加载 `.env`。

### 用户意图 → 工具调用映射

当用户发出模糊请求时，按以下规则映射到具体工具：

| 用户说的 | 应该用的 | 示例 |
|----------|----------|------|
| "搜一下/查一下/找一下" | `web_search` | `web_search "Rust 2026 新特性" --count 5` |
| "看看这个链接/帮我读一下" | `web_reader` | `web_reader "https://example.com/article"` |
| "xxx仓库怎么用/xxx项目文档" | `zread search` | `zread search "tauri-apps/tauri" "window creation"` |
| "看看xxx仓库结构" | `zread structure` | `zread structure "openai/openai"` |
| "读一下xxx仓库的README" | `zread read` | `zread read "openai/openai" "README.md"` |
| "分析这张图片/看看截图" | `vision` (自动识别 image) | `vision /path/to/img.png --prompt "描述内容"` |
| "看看这个视频" | `vision` (自动识别 video) | `vision /path/to/vid.mp4 --prompt "关键动作"` |

### 输出格式参考

各工具的典型输出格式（agent 拿到后可直接处理/摘要）：

**web_search 输出**：
```
### 结果 1
**标题**: xxx
**链接**: https://...
**摘要**: xxx
```

## Agent 决策指南

> 这部分告诉 agent 在哪些节点需要做决策或用户确认，避免自主失控。

### 工具选择决策树

```
需要搜索/获取信息？
  ├─ 互联网搜索 → web_search（首选）
  ├─ 读取指定网页 → web_reader
  ├─ GitHub 仓库文档 → zread
  ├─ 本地文档(PDF/Word等) → file_parser
  └─ 图片/视频分析 → vision
```

### 必须确认的检查点

| 场景 | 检查点 | 建议行为 |
|------|--------|----------|
| **视觉理解** | ✅ 当前免费 | Coding Plan 免费额度，无需确认 |
| **文件解析** | ⚠️ 走账户余额 | 同上，提醒用户可能消耗账户余额 |
| **搜索无结果** | 换关键词重试 | 最多重试 2 次换词，仍无结果则提示用户并建议用内置 web_search |
| **MCP 连接失败** | ⚠️ 不自动切换 | **不自动 fallback 到 Legacy**，直接报错并建议用内置工具 |
| **内容安全拦截** | 不自动重试 | 告知用户搜索词可能触发安全策略，建议修改关键词 |
| **大文件上传** | 超限时提示 | 视频超过 8MB 时告知用户限制，建议压缩或用 URL 方式 |

### 自动处理的场景（无需确认）

- MCP 搜索返回空结果 → 提示用户换关键词重试
- 仓库搜索参数格式错误 → 直接报错，不猜测意图

> ⚠️ **安全原则**：本工具默认使用 MCP 免费模式，**不会自动切换到可能产生费用的 Legacy API**。Legacy 模式需用户显式设置 `ZHIPU_USE_MCP=false` 启用。

## 功能

| 功能 | MCP 工具 | 端点 | 说明 |
|------|----------|------|------|
| **网络搜索** | `web_search_prime` | `/web_search_prime/mcp` | 实时互联网搜索，支持过滤 |
| **网页读取** | `webReader` | `/web_reader/mcp` | 抓取网页标题、正文、元数据 |
| **仓库文档搜索** | `search_doc` | `/zread/mcp` | 搜索 GitHub 仓库文档 |
| **仓库目录结构** | `get_repo_structure` | `/zread/mcp` | 查看 GitHub 仓库目录树 |
| **仓库文件读取** | `read_file` | `/zread/mcp` | 读取 GitHub 仓库指定文件 |
| **视觉理解** | — | Coding Plan 免费 | GLM-4.6V 图像/视频分析（当前免费） |
| **文件解析** | — | Legacy API | 解析 PDF/Word/Excel/PPT 等 |

> 前五项通过 Coding Plan MCP 端点免费调用，视觉理解、视频分析和文件解析通过旧版 API 调用。
>
> 视觉理解（vision）通过逆向分析智谱官方 `@z_ai/mcp-server` npm 包实现。从包源码中提取了底层 API 调用方式（`open.bigmodel.cn/api/paas/v4/chat/completions` + `glm-4.6v` 模型）。**当前走 Coding Plan 免费额度，不产生费用。**后续智谱可能调整计费策略，届时需要重新评估。

## 配置

在 `openclaw.json` 中配置 API Key：

```json
{
  "skills": {
    "entries": {
      "zhipu-tools": {
        "apiKey": "YOUR_ZHIPU_API_KEY"
      }
    }
  }
}
```

或设置环境变量：`ZHIPU_API_KEY`

### MCP vs Legacy 模式

| 模式 | 端点 | 额度 | 启用方式 |
|------|------|------|----------|
| **MCP (默认)** | `api.z.ai/api/mcp/...` | Z.AI Coding Plan 免费 | 默认启用 |
| Legacy | `open.bigmodel.cn/api/paas/v4/...` | ⚠️ 账户余额 | **需显式** `ZHIPU_USE_MCP=false` |

> ⚠️ **MCP 失败时不会自动切换到 Legacy**。Legacy API 走账户余额，自动切换可能让用户产生意外费用。
> 如需使用 Legacy 模式，必须**显式设置**环境变量 `ZHIPU_USE_MCP=false`。

## 使用方式

### 视觉理解 (vision)

```bash
# 分析图片（自动识别为图片类型）
python3 scripts/zhipu_tool.py vision /path/to/image.png
python3 scripts/zhipu_tool.py vision /path/to/image.png --prompt "描述这个UI界面"
python3 scripts/zhipu_tool.py vision "https://example.com/screenshot.png" --prompt "识别截图中的错误信息"

# 分析视频（自动识别为视频类型）
python3 scripts/zhipu_tool.py vision /path/to/video.mp4
python3 scripts/zhipu_tool.py vision /path/to/video.mp4 --prompt "描述视频中的关键动作"
python3 scripts/zhipu_tool.py vision "https://example.com/demo.mp4" --prompt "这个视频演示了什么"

# 手动指定媒体类型（当自动识别不准时）
python3 scripts/zhipu_tool.py vision weird-file --type video
python3 scripts/zhipu_tool.py vision weird-file --type image
```

**支持的图片格式**: jpg, jpeg, png, gif, webp, bmp, svg, tiff, ico 等常见图片格式
**支持的视频格式**: mp4, mov, m4v, avi, mkv, webm, flv, wmv（本地视频 ≤ 8MB）

支持本地文件路径和 HTTP/HTTPS URL。本地文件自动 base64 编码，远程 URL 直接传递。
默认自动识别媒体类型（通过文件扩展名和 MIME type），也可通过 `--type` 手动指定。

### 网络搜索 (web_search_prime)

```bash
cd ~/.openclaw/workspace/skills/zhipu-tools

# Shell（MCP 模式，推荐）
./scripts/web_search.sh "搜索关键词" [count]

# Python（支持更多参数，注意部分参数仅在 Legacy 模式生效）
python3 scripts/zhipu_tool.py web_search "搜索关键词" \
  --count 10 --recency week --domain example.com
```

> ⚠️ `--recency` 和 `--domain` 参数在 MCP 模式下会通过注入搜索词的方式实现（如 `site:example.com`、`最近一周`），效果取决于搜索引擎理解，不保证精确过滤。

### 网页读取 (webReader)

```bash
# Shell
./scripts/web_reader.sh "https://www.example.com"

# Python
python3 scripts/zhipu_tool.py web_reader "https://www.example.com"
```

### GitHub 仓库文档搜索 (Zread)

```bash
# Shell - 搜索仓库文档
./scripts/zread.sh search "openai/openai" "how to use"

# Shell - 查看目录结构
./scripts/zread.sh structure "openai/openai"
./scripts/zread.sh structure "openai/openai" "src/"

# Shell - 读取文件
./scripts/zread.sh read "openai/openai" "README.md"

# Python
python3 scripts/zhipu_tool.py zread search "openai/openai" "how to use"
python3 scripts/zhipu_tool.py zread structure "openai/openai" --path src/
python3 scripts/zhipu_tool.py zread read "openai/openai" "README.md"
```

### 文件解析 (Legacy only)

```bash
./scripts/file_parser.sh /path/to/document.pdf PDF
python3 scripts/zhipu_tool.py file_parser /path/to/document.docx --file-type DOCX
```

## MCP 工具参数详情

### web_search_prime

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| search_query | string | 是 | 搜索内容，建议不超过 70 字符 |
| search_recency_filter | string | 否 | oneDay, oneWeek, oneMonth, oneYear, noLimit |
| content_size | string | 否 | medium (默认), high |
| location | string | 否 | cn, us |
| search_domain_filter | string | 否 | 限制搜索域名 |

### webReader

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| url | string | 是 | 目标网页 URL |

返回：标题、正文内容、元数据、链接列表。

### search_doc

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| repo | string | 是 | GitHub 仓库，如 "openai/openai" |
| query | string | 是 | 搜索关键词 |

### get_repo_structure

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| repo | string | 是 | GitHub 仓库 |
| path | string | 否 | 子目录路径 |

### read_file

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| repo | string | 是 | GitHub 仓库 |
| path | string | 是 | 文件路径，如 "README.md" |

## MCP 协议

所有远程 MCP 端点通过 streamableHttp 协议交互：

1. **POST initialize** → 响应 header 返回 `mcp-session-id`
2. **POST notifications/initialized** → 通知就绪
3. **POST tools/call** → 调用具体工具

Headers: `Authorization: Bearer $API_KEY`, `Content-Type: application/json`, `Accept: text/event-stream, application/json`

## Coding Plan 套餐额度

| 套餐 | 搜索/网页读取/仓库搜索 次数/月 | 价格 |
|------|:----------------------------:|:----:|
| **Lite** | 100 次 | 免费 |
| **Pro** | 1,000 次 | 免费 |
| **Max** | 4,000 次 | 免费 |

额度次月自动重置。

## 优先使用规则

**当需要网络搜索、网页读取等能力时，优先使用智谱 API（本技能的 MCP 工具），而非内置的 web_search / web_fetch 工具。**

原因：智谱 Coding Plan MCP 端点免费且额度充足（Pro 1000次/月），可节省内置搜索 API 的配额消耗。

优先级顺序：
1. **智谱 MCP 工具**（`web_search_prime`、`webReader`）— 首选，免费
2. **内置 `web_search` / `web_fetch`** — MCP 不可用时使用

## 错误处理与边界条件

### 常见错误及处理策略

| 错误 | 现象 | 自动处理 | 需要用户干预时 |
|------|------|----------|---------------|
| MCP 连接失败 | SSL/网络错误 | **不自动 fallback** | 直接报错，建议用内置 web_search/web_fetch |
| MCP 内容安全拦截 | 返回空结果 + 错误提示 | **不自动重试** | 告知用户搜索词触发安全策略，请修改搜索词 |
| Legacy 429 限流 | "余额不足" | **不自动重试**（重试只会浪费请求） | 告知用户：MCP 模式正常，429 是 Legacy 预期行为 |
| Legacy 超时 | 视觉理解 120s/其他 30s | **不自动重试** | 告知用户：检查网络或文件大小 |
| 文件不存在 | FileNotFoundError | — | 直接报错，提示检查路径 |
| 视频超 8MB | ValueError | — | 告知用户限制，建议压缩或用 URL |
| 搜索无结果 | 返回空列表 | — | 告知用户并建议换关键词，可用内置工具 |

### 前置条件

- **Python 3.8+** 和 `requests` 库（`pip install requests`）
- **API Key** 已配置（环境变量 `ZHIPU_API_KEY` 或 `.env` 文件）
- `scripts/` 目录下工具脚本存在且可执行
- MCP 端点可访问：`api.z.ai`（搜索/网页/仓库）
- Legacy 端点可访问：`open.bigmodel.cn`（视觉/文件解析）— ⚠️ 部分网络环境可能不可用

## 注意事项

- API Key 不要提交到 Git
- Zread 仅支持 MCP 模式
- 视觉理解/文件解析当前走 Coding Plan 免费额度，后续如智谱调整计费策略需重新评估
- MCP 搜索 recency/domain 通过注入 query 模拟
- MCP 内容安全策略可能拦截敏感搜索
- Legacy 429 是 Coding Plan 用户预期行为，不影响 MCP 功能
