---
name: go-fs-mcp-skill
description: 通过 MCP stdio 提供文件系统操作（列出目录、读写文件、创建目录、删除与移动），由独立 go-fs-mcp-server 执行实际 IO。
version: 1.0.0
homepage: https://github.com/go-fs-mcp/go-fs-mcp
metadata: {"openclaw":{"emoji":"📁","homepage":"https://github.com/go-fs-mcp/go-fs-mcp","requires":{"bins":["go-fs-mcp-skill","go-fs-mcp-server"],"config":["skill.json"]},"install":[{"kind":"go","package":"github.com/go-fs-mcp/go-fs-mcp-server/cmd/server@latest","bins":["go-fs-mcp-server"]},{"kind":"go","package":"github.com/go-fs-mcp/go-fs-mcp-skill/cmd/skill@latest","bins":["go-fs-mcp-skill"]}]}}
---

# 文件系统 MCP 技能（Go 版）

当用户需要列出目录、读取/写入文件、创建文件夹、删除或移动文件时使用本 Skill。

本 Skill **不直接操作文件**，仅做参数校验与 MCP 转发；实际 IO 由 `go-fs-mcp-server` 完成。

## 架构

```
OpenClaw 对话
    → go-fs-mcp-skill（参数校验 + JSON 封装）
        → go-fs-mcp-server（MCP stdio，6 个文件 Tool）
            → 文件系统
```

## 触发词

- 列出目录
- 读取文件
- 写入文件
- 创建文件夹
- 删除文件
- 移动文件

在对话中使用自然语言并带上路径即可，例如：

```
列出 /mnt/e/github/go-fs-mcp 目录内容
```

```
读取 /mnt/e/github/go-fs-mcp/README.md
```

## MCP 工具映射

| toolName | 必填 params | 说明 |
|----------|-------------|------|
| `list_directory` | `path` | 列出目录 |
| `read_file` | `path` | 读取 UTF-8 文本 |
| `write_file` | `path`, `content` | 写入/覆盖文件 |
| `create_directory` | `path` | 创建多级目录 |
| `delete_file` | `path` | 删除文件或目录 |
| `move_file` | `source`, `destination` | 移动/重命名 |

## 安装依赖（二进制）

从 [go-fs-mcp](https://github.com/go-fs-mcp/go-fs-mcp) 源码构建两个二进制，并放入本 Skill 目录或加入 PATH：

```bash
git clone https://github.com/go-fs-mcp/go-fs-mcp.git
cd go-fs-mcp
go build -o go-fs-mcp-server/go-fs-mcp-server ./go-fs-mcp-server/cmd/server
go build -o go-fs-mcp-skill/go-fs-mcp-skill ./go-fs-mcp-skill/cmd/skill
```

也可使用本目录下的 `scripts/build.sh` 或 `scripts/build.ps1`（需已 clone 完整仓库）。

详细步骤见 [INSTALL.md](INSTALL.md)。

## 配置 skill.json

安装后编辑本目录下的 `skill.json`，将 `config.mcp_command` 改为 **go-fs-mcp-server 的绝对路径**：

**WSL 示例：**

```json
"config": {
  "mcp_command": "/home/user/.openclaw/skills/go-fs-mcp-skill/go-fs-mcp-server",
  "mcp_args": [],
  "timeout": 10
}
```

**Windows 示例：**

```json
"config": {
  "mcp_command": "e:\\github\\go-fs-mcp\\go-fs-mcp-server\\go-fs-mcp-server.exe",
  "mcp_args": [],
  "timeout": 10
}
```

也可复制环境模板：`skill.wsl.json` 或 `skill.windows.json`。

## CLI 调用格式

```bash
go-fs-mcp-skill '{"toolName":"list_directory","params":{"path":"/path/to/dir"}}'
```

成功返回：

```json
{"success":true,"message":"MCP 工具 list_directory 执行成功","data":{"toolName":"list_directory","result":"..."}}
```

## OpenClaw 启用

在 `~/.openclaw/openclaw.json` 顶层添加：

```json
{
  "skills": {
    "entries": {
      "go-fs-mcp-skill": { "enabled": true }
    }
  }
}
```

安装后执行 `openclaw gateway restart`。

完整操作流程见仓库 [docs/OPERATIONS.md](https://github.com/go-fs-mcp/go-fs-mcp/blob/main/docs/OPERATIONS.md)。
