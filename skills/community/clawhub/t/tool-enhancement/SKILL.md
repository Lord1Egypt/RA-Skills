---
name: tool-enhancement
description: "🚀 55+ 增强工具集 - 为 OpenClaw 赋能。文件操作、Shell执行、Git工作流、网页请求、子Agent调度、分层记忆、终端UI，一应俱全。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🛠️",
        "requires":
          {
            "anyBins": ["python3", "git", "curl"]
          },
        "install": []
      }
  }
---

<div align="center">

# 🛠️ Tool Enhancement

**为 OpenClaw 打造的 55+ 增强工具集**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.2-green.svg)](./SKILL.md)
[![Tools](https://img.shields.io/badge/tools-55+-orange.svg)](#工具总览)

*参考 Claude Code 架构设计 | 支持自然语言调用*

</div>

---

## ✨ 特性

| 特性 | 说明 |
|------|------|
| 🔰 **55+ 工具** | 覆盖文件/Shell/Git/网页/记忆/UI 场景 |
| 🧠 **自然语言** | 智能理解用户意图，自动调用工具 |
| 📦 **统一注册** | 全局 ToolRegistry，工具即插即用 |
| 🔒 **权限控制** | FS_READ / EXECUTE / NETWORK 等权限体系 |
| ⚡ **异步执行** | 所有工具原生 async/await 支持 |
| 🎨 **终端UI** | 表格/进度条/菜单/树形等丰富组件 |

---

## 🚀 快速开始

### 安装

```bash
# 通过 ClawHub 安装（推荐）
clawhub install tool-enhancement

# 或手动克隆
git clone https://github.com/ntaffffff/openclaw-tool-enhancement.git
```

### 基本用法

```bash
# 方式1: 自然语言（推荐）
python3 ~/.openclaw/workspace/skills/tool-enhancement/tools/run_nlp.py "读取 /etc/hostname"

# 方式2: 直接调用工具
python3 ~/.openclaw/workspace/skills/tool-enhancement/tools/run_tool.py file_read path="/etc/hostname"
```

---

## 📖 使用教程

### 在 OpenClaw 对话中直接使用

当用户说以下内容时，AI 会自动调用对应工具：

| 用户说 | 调用的工具 | 示例 |
|--------|-----------|------|
| "读取 /etc/hostname" | file_read | 📄 查看文件内容 |
| "执行 ls -la" | shell_exec | 💻 运行命令 |
| "查看系统信息" | system_info | 💻 系统概况 |
| "天气怎么样" | http_request | 🌤️ 查询天气 |
| "搜索 Python 教程" | web_search | 🔍 网络搜索 |
| "记住今天开会" | memory_remember | 🧠 存储记忆 |
| "git status" | git_status | 📦 Git 状态 |
| "推送代码" | git_push | 📤 代码推送 |

### 代码中调用

```python
import sys
sys.path.insert(0, "~/.openclaw/workspace/skills/tool-enhancement/tools")

from __init__ import load_all_tools, get_registry
import asyncio

async def main():
    # 加载所有工具
    load_all_tools()
    
    # 获取注册表
    registry = get_registry()
    
    # 执行工具
    result = await registry.execute("file_read", path="/etc/hostname")
    print(result.data)  # 输出: dxx

asyncio.run(main())
```

---

## 🛠️ 工具总览

### 📁 文件操作 (9个)

| 工具 | 功能 | 示例 |
|------|------|------|
| `file_read` | 读取文件 | `path="/etc/hostname"` |
| `file_write` | 写入文件 | `path="/tmp/test.txt", content="hello"` |
| `file_edit` | 编辑文件 | `path="/tmp/test.txt", old="a", new="b"` |
| `file_delete` | 删除文件 | `path="/tmp/test.txt"` |
| `file_glob` | 搜索文件 | `pattern="*.py"` |
| `file_copy` | 复制文件 | `src="/a.txt", dst="/b.txt"` |
| `file_move` | 移动文件 | `src="/a.txt", dst="/b.txt"` |
| `file_info` | 文件信息 | `path="/tmp"` |
| `file_list` | 列出目录 | `path="/tmp"` |

### 💻 执行工具 (7个)

| 工具 | 功能 | 示例 |
|------|------|------|
| `shell_exec` | 执行Shell命令 | `command="ls -la"` |
| `shell_background` | 后台执行 | `command="python server.py", detached=True` |
| `process_list` | 列出进程 | - |
| `process_kill` | 终止进程 | `pid=1234` |
| `shell_sudo` | 提权执行 | `command="apt update"` |
| `script_run` | 运行脚本 | `path="/tmp/script.sh"` |
| `system_info` | 系统信息 | - |

### 📦 Git 工具 (8个)

| 工具 | 功能 | 示例 |
|------|------|------|
| `git_status` | 查看状态 | `path="."` |
| `git_log` | 查看日志 | `path=".", max_count=10` |
| `git_diff` | 查看差异 | `path="."` |
| `git_commit` | 提交代码 | `path=".", message="fix: bug"` |
| `git_push` | 推送到远程 | `path="."` |
| `git_pull` | 拉取更新 | `path="."` |
| `git_branch` | 分支操作 | `path="."` |
| `git_remote` | 远程操作 | `path="."` |

### 🌐 网页工具 (5个)

| 工具 | 功能 | 示例 |
|------|------|------|
| `http_request` | HTTP请求 | `url="http://wttr.in/Shanghai"` |
| `web_fetch` | 网页抓取 | `url="https://example.com"` |
| `web_search` | 网络搜索 | `query="Python 教程"` |
| `api_request` | API调用 | `url="https://api.github.com"` |
| `url_parse` | URL解析 | `url="https://a.com/b?c=1"` |

### 🧠 记忆工具 (6个)

| 工具 | 功能 | 示例 |
|------|------|------|
| `memory_remember` | 存储记忆 | `content="重要事项", importance=5` |
| `memory_recall` | 检索记忆 | `query="项目", limit=5` |
| `memory_summarize` | 总结记忆 | `query="上周"` |
| `memory_dream` | 记忆整合 | `dry_run=false` |
| `memory_context` | 上下文记忆 | `query="当前任务"` |
| `memory_stats` | 记忆统计 | - |

### 🤖 Agent 工具 (6个)

| 工具 | 功能 | 示例 |
|------|------|------|
| `agent_spawn` | 启动子Agent | `name="coder", prompt="分析代码"` |
| `agent_delegate` | 委托任务 | `agent_id="xxx", task="..."` |
| `agent_result` | 获取结果 | `task_id="xxx"` |
| `agent_list` | 列出Agent | - |
| `agent_cancel` | 取消Agent | `task_id="xxx"` |
| `coordinator` | 多Agent协调 | `task="...", phases=[...]` |

### 🎨 UI 工具 (8个)

| 工具 | 功能 |
|------|------|
| `ui_spinner` | 加载动画 |
| `ui_progress` | 进度条 |
| `ui_table` | 表格显示 |
| `ui_tree` | 树形结构 |
| `ui_markdown` | Markdown渲染 |
| `ui_status` | 状态显示 |
| `ui_confirm` | 确认对话框 |
| `ui_menu` | 菜单选择 |

### 🔌 MCP 工具 (6个)

| 工具 | 功能 |
|------|------|
| `mcp_list` | 列出MCP服务器 |
| `mcp_discover` | 发现MCP服务 |
| `mcp_call` | 调用MCP工具 |
| `mcp_resource` | 访问MCP资源 |
| `mcp_prompt` | 使用MCP提示词 |
| `mcp_status` | MCP状态 |

---

## 📁 文件结构

```
tool-enhancement/
├── SKILL.md                    # 本文档
├── tools/
│   ├── __init__.py             # 统一加载器
│   ├── schema.py               # 基础类定义
│   ├── run_tool.py             # 命令行工具调用器
│   ├── run_nlp.py              # 自然语言理解器
│   ├── file_tools.py           # 文件操作 (9)
│   ├── exec_tools.py           # 执行工具 (7)
│   ├── git_tools.py            # Git 工具 (8)
│   ├── web_tools.py            # 网页工具 (5)
│   ├── mcp_tools.py            # MCP 工具 (6)
│   ├── agent_tools.py          # Agent 工具 (6)
│   ├── memory_tools.py         # 记忆工具 (6)
│   └── ui_tools.py             # UI 工具 (8)
└── README.md
```

---

## 🤝 贡献

欢迎提交 Issue 和 PR！

---

## 📄 许可证

MIT License

---

<div align="center">

**🌟 喜欢这个工具？请给个 Star！**

</div>