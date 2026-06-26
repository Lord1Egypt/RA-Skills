# 🛠️ Tool Enhancement

**为 OpenClaw 打造的 55+ 增强工具集**

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](./LICENSE)
[![Version](https://img.shields.io/badge/version-1.0.0-green.svg)](./SKILL.md)
[![Tools](https://img.shields.io/badge/tools-55+-orange.svg)](#-工具总览)

*参考 Claude Code 架构设计 | 支持自然语言调用*

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

| 用户说 | 调用的工具 |
|--------|-----------|
| "读取 /etc/hostname" | file_read |
| "执行 ls -la" | shell_exec |
| "查看系统信息" | system_info |
| "天气怎么样" | http_request |
| "搜索 Python 教程" | web_search |
| "记住今天开会" | memory_remember |
| "git status" | git_status |
| "推送代码" | git_push |

### 代码中调用

```python
import sys
sys.path.insert(0, "~/.openclaw/workspace/skills/tool-enhancement/tools")

from __init__ import load_all_tools, get_registry
import asyncio

async def main():
    load_all_tools()
    registry = get_registry()
    result = await registry.execute("file_read", path="/etc/hostname")
    print(result.data)

asyncio.run(main())
```

---

## 🛠️ 工具总览

### 📁 文件操作 (9个)
- `file_read`, `file_write`, `file_edit`, `file_delete`
- `file_glob`, `file_copy`, `file_move`, `file_info`, `file_list`

### 💻 执行工具 (7个)
- `shell_exec`, `shell_background`, `process_list`, `process_kill`
- `shell_sudo`, `script_run`, `system_info`

### 📦 Git 工具 (8个)
- `git_status`, `git_log`, `git_diff`, `git_commit`
- `git_push`, `git_pull`, `git_branch`, `git_remote`

### 🌐 网页工具 (5个)
- `http_request`, `web_fetch`, `web_search`, `api_request`, `url_parse`

### 🧠 记忆工具 (6个)
- `memory_remember`, `memory_recall`, `memory_summarize`
- `memory_dream`, `memory_context`, `memory_stats`

### 🤖 Agent 工具 (6个)
- `agent_spawn`, `agent_delegate`, `agent_result`
- `agent_list`, `agent_cancel`, `coordinator`

### 🎨 UI 工具 (8个)
- `ui_spinner`, `ui_progress`, `ui_table`, `ui_tree`
- `ui_markdown`, `ui_status`, `ui_confirm`, `ui_menu`

### 🔌 MCP 工具 (6个)
- `mcp_list`, `mcp_discover`, `mcp_call`
- `mcp_resource`, `mcp_prompt`, `mcp_status`

---

## 📁 文件结构

```
tool-enhancement/
├── SKILL.md                    # OpenClaw Skill 文档
├── README.md                   # 本文档
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