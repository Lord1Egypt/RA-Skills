---
name: yuque-mcp-tool
description: >
  通过 MCP 协议在 AI 客户端中读取语雀文档。支持读取渲染内容、转换 Markdown、列出知识库文档。
  兼容 Claude Desktop、Cursor、WorkBuddy 等主流 MCP 客户端。
description_en: >
  Read Yuque documents in AI clients via MCP protocol. Supports reading rendered content,
  converting to Markdown, and listing knowledge base docs. Compatible with Claude Desktop,
  Cursor, WorkBuddy, and other MCP clients.
version: 1.0.0
category: 编程
category_en: Development
author: andy8663
email: andy8663@126.com
license: MIT
homepage: https://github.com/andy8663/yuque-mcp-tool
repository: https://github.com/andy8663/yuque-mcp-tool.git
platforms:
  - claude-desktop
  - cursor
  - workbuddy
  - qclaw
  - generic-mcp
tags:
  - yuque
  - mcp
  - 文档读取
  - markdown
  - 知识库
  - document-reading
  - knowledge-base
tags_en:
  - yuque
  - mcp
  - document-reading
  - markdown
  - knowledge-base
---

# Yuque MCP Tool

---

## 中文文档

### 简介

Yuque MCP Tool 是一个基于 Session Cookie 的语雀 MCP (Model Context Protocol) 服务器。安装后，AI Agent 可以直接读取你的语雀文档内容，无需手动复制粘贴。

**适用场景：**
- 让 AI 读取语雀知识库中的技术文档、产品需求、会议纪要
- 将语雀文档批量转换为 Markdown 格式
- 快速浏览知识库的文档目录结构

### 提供的工具

| 工具名 | 参数 | 说明 |
|--------|------|------|
| `yuque_read` | `url`（必填） | 读取语雀文档，返回渲染后的文本内容 |
| `yuque_read_markdown` | `url`（必填），`include_stats`（可选，布尔值） | **推荐**。读取 Lake/API 源内容并转换为 Markdown，保留表格、PlantUML/Mermaid 图表、代码块、图片、链接和画板摘要 |
| `yuque_list_docs` | `repo_slug`（必填），`host`（可选） | 列出知识库中的所有文档 |

### 安装

```bash
# 方式一：pip 安装（推荐）
pip install yuque-mcp-tool

# 安装 Playwright 浏览器（可选，用于渲染 JS 页面）
python -m playwright install chromium

# 方式二：从源码安装
git clone https://github.com/andy8663/yuque-mcp-tool.git
cd yuque-mcp-tool
pip install -e .
```

### 获取语雀 Session Cookie

**方法一：Application 面板（推荐）**

1. 登录 [语雀](https://www.yuque.com)
2. 按 `F12` 打开浏览器开发者工具
3. 切换到 **Application**（应用）面板
4. 左侧展开 **Cookies** → 点击 `https://www.yuque.com`
5. 找到 `_yuque_session`，复制其 **Value** 列的值

**方法二：Console 命令**

1. 登录 [语雀](https://www.yuque.com)
2. 按 `F12` → 在 **Console** 中输入：
   ```javascript
   document.cookie.split('; ').find(c => c.startsWith('_yuque_session=')).split('=')[1]
   ```
3. 复制输出的值

> ⚠️ 如果 `_yuque_session` 被标记为 `HttpOnly`，方法二无效，请使用方法一。
>
> Session 有效期约 30 天，过期后需重新获取。

### 配置 MCP 客户端

在 MCP 客户端的配置文件中添加以下内容：

```json
{
  "mcpServers": {
    "yuque": {
      "command": "yuque-mcp",
      "env": {
        "YUQUE_SESSION": "YOUR_YUQUE_SESSION",
        "YUQUE_HOST": "https://www.yuque.com"
      }
    }
  }
}
```

**各客户端配置文件位置：**

| 客户端 | 配置文件路径 |
|--------|-------------|
| Claude Desktop (macOS) | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Claude Desktop (Windows) | `%APPDATA%\Claude\claude_desktop_config.json` |
| Cursor | `.cursor/mcp.json`（项目根目录） |
| WorkBuddy | MCP 配置文件 |
| 通用 MCP 客户端 | 参考客户端文档 |

> 如果未通过 `pip install` 安装，可将 `command` 改为 `python`，`args` 设为 `["-m", "yuque_mcp"]`。

### 环境变量

| 变量名 | 必填 | 默认值 | 说明 |
|--------|------|--------|------|
| `YUQUE_SESSION` | 是 | — | 语雀 Session Cookie（`_yuque_session` 的值） |
| `YUQUE_HOST` | 否 | `https://www.yuque.com` | 默认语雀主机，用于补全短路径 URL |
| `YUQUE_BROWSER_CHANNEL` | 否 | — | Playwright 浏览器通道，如 `chrome` |
| `YUQUE_CHROMIUM_EXECUTABLE` | 否 | — | Chromium/Chrome 可执行文件绝对路径 |
| `YUQUE_RENDER_MODE` | 否 | `auto` | 渲染模式：`auto`（自动）、`off`（关闭）、`force`（强制 Playwright） |

### 使用示例

**读取文档为 Markdown（推荐）：**
```
帮我读取这个语雀文档：https://www.yuque.com/cc9c0g/rebell/hf0gch
```

**列出知识库文档：**
```
列出语雀知识库 cc9c0g/rebell 里的所有文档
```

**读取渲染内容：**
```
读取这个语雀页面的内容：https://ogtd9v.yuque.com/org/wiki/hf0gch
```

### 常见问题

**Session 无效 / 读取失败**：重新登录语雀，获取新的 `_yuque_session` 值并更新配置。

**Playwright 渲染失败**：设置 `YUQUE_BROWSER_CHANNEL=chrome` 使用系统 Chrome。

**团队/空间子域名**：文档在团队子域名下（如 `ogtd9v.yuque.com`）时，设置 `YUQUE_HOST` 为常用子域名，或直接传完整 URL。

### 技术栈

aiohttp + Playwright（可选渲染）+ BeautifulSoup4

### License

MIT License — 详见 [LICENSE](https://github.com/andy8663/yuque-mcp-tool/blob/main/LICENSE)

---

## English Documentation

### Overview

Yuque MCP Tool is a session-cookie-based MCP (Model Context Protocol) server for Yuque documents. Once installed, your AI Agent can read Yuque documents directly — no manual copy-paste needed.

**Use cases:**
- Let AI read technical docs, product requirements, and meeting notes from Yuque
- Batch convert Yuque documents to Markdown format
- Quickly browse the document tree of a knowledge base

### Available Tools

| Tool | Parameters | Description |
|------|-----------|-------------|
| `yuque_read` | `url` (required) | Read a Yuque document and return the rendered text content |
| `yuque_read_markdown` | `url` (required), `include_stats` (optional, boolean) | **Recommended.** Read the Lake/API source content and convert to Markdown, preserving tables, PlantUML/Mermaid diagrams, code blocks, images, links, and board summaries |
| `yuque_list_docs` | `repo_slug` (required), `host` (optional) | List all documents in a Yuque repository |

### Installation

```bash
# Option 1: pip install (recommended)
pip install yuque-mcp-tool

# Install Playwright browser (optional, for JS page rendering)
python -m playwright install chromium

# Option 2: install from source
git clone https://github.com/andy8663/yuque-mcp-tool.git
cd yuque-mcp-tool
pip install -e .
```

### Getting Your Session Cookie

**Method 1: Application Panel (Recommended)**

1. Log in to [Yuque](https://www.yuque.com)
2. Press `F12` to open browser DevTools
3. Switch to the **Application** tab
4. Expand **Cookies** → click `https://www.yuque.com`
5. Find `_yuque_session` and copy its **Value**

**Method 2: Console Command**

1. Log in to [Yuque](https://www.yuque.com)
2. Press `F12` → in the **Console**, run:
   ```javascript
   document.cookie.split('; ').find(c => c.startsWith('_yuque_session=')).split('=')[1]
   ```
3. Copy the output value

> ⚠️ If `_yuque_session` is marked as `HttpOnly`, Method 2 will not work — use Method 1 instead.
>
> The session cookie is valid for approximately 30 days.

### MCP Client Configuration

Add the following to your MCP client's configuration file:

```json
{
  "mcpServers": {
    "yuque": {
      "command": "yuque-mcp",
      "env": {
        "YUQUE_SESSION": "YOUR_YUQUE_SESSION",
        "YUQUE_HOST": "https://www.yuque.com"
      }
    }
  }
}
```

**Configuration file locations by client:**

| Client | Config File Path |
|--------|-----------------|
| Claude Desktop (macOS) | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| Claude Desktop (Windows) | `%APPDATA%\Claude\claude_desktop_config.json` |
| Cursor | `.cursor/mcp.json` (project root) |
| WorkBuddy | MCP configuration file |
| Generic MCP Client | Refer to client documentation |

> If not installed via `pip install`, set `command` to `python` and `args` to `["-m", "yuque_mcp"]`.

### Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `YUQUE_SESSION` | Yes | — | Yuque session cookie (`_yuque_session` value) |
| `YUQUE_HOST` | No | `https://www.yuque.com` | Default Yuque host for short-path URL completion |
| `YUQUE_BROWSER_CHANNEL` | No | — | Playwright browser channel, e.g. `chrome` |
| `YUQUE_CHROMIUM_EXECUTABLE` | No | — | Absolute path to a Chromium/Chrome executable |
| `YUQUE_RENDER_MODE` | No | `auto` | Rendering mode: `auto`, `off`, or `force` |

### Usage Examples

**Read a document as Markdown (recommended):**
```
Read this Yuque document: https://www.yuque.com/cc9c0g/rebell/hf0gch
```

**List documents in a knowledge base:**
```
List all documents in Yuque repository cc9c0g/rebell
```

**Read rendered content:**
```
Read the content of this Yuque page: https://ogtd9v.yuque.com/org/wiki/hf0gch
```

### FAQ

**Invalid Session / Read Failure**: Re-log in to Yuque, obtain a new `_yuque_session` value, and update your configuration.

**Playwright Rendering Failure**: Set `YUQUE_BROWSER_CHANNEL=chrome` to use the system Chrome.

**Team / Workspace Subdomains**: If documents are on a team subdomain (e.g. `ogtd9v.yuque.com`), set `YUQUE_HOST` to your common subdomain, or pass full document URLs directly.

### Tech Stack

aiohttp + Playwright (optional rendering) + BeautifulSoup4

### License

MIT License — see [LICENSE](https://github.com/andy8663/yuque-mcp-tool/blob/main/LICENSE)
