# 安装说明

从 ClawHub 或本地安装本 Skill 后，需完成以下步骤才能正常使用。

## 1. 获取源码

```bash
git clone https://github.com/go-fs-mcp/go-fs-mcp.git
cd go-fs-mcp
```

若已在本 monorepo 中，可跳过 clone。

## 2. 构建二进制

### WSL / Linux

```bash
export GOPROXY=https://goproxy.cn,direct   # 国内可选
go mod tidy
go build -o go-fs-mcp-server/go-fs-mcp-server ./go-fs-mcp-server/cmd/server
go build -o go-fs-mcp-skill/go-fs-mcp-skill ./go-fs-mcp-skill/cmd/skill
chmod +x go-fs-mcp-server/go-fs-mcp-server go-fs-mcp-skill/go-fs-mcp-skill
```

或使用本包脚本（在 go-fs-mcp 仓库根目录执行）：

```bash
bash publish-skill/scripts/build.sh
```

### Windows

```powershell
cd e:\github\go-fs-mcp
$env:GOPROXY = "https://goproxy.cn,direct"
go mod tidy
go build -o go-fs-mcp-server\go-fs-mcp-server.exe .\go-fs-mcp-server\cmd\server
go build -o go-fs-mcp-skill\go-fs-mcp-skill.exe .\go-fs-mcp-skill\cmd\skill
```

或：

```powershell
.\publish-skill\scripts\build.ps1
```

## 3. 放置二进制

将构建产物复制到 OpenClaw Skill 安装目录（与 `skill.json` 同级），或确保在 PATH 中：

```bash
# 示例：OpenClaw 全局 skill 目录
SKILL_DIR=~/.openclaw/skills/go-fs-mcp-skill
cp go-fs-mcp-server/go-fs-mcp-server "$SKILL_DIR/"
cp go-fs-mcp-skill/go-fs-mcp-skill "$SKILL_DIR/"
chmod +x "$SKILL_DIR/go-fs-mcp-server" "$SKILL_DIR/go-fs-mcp-skill"
```

Windows 对应复制 `.exe` 到 skill 目录。

## 4. 配置 skill.json

编辑 Skill 目录下的 `skill.json`：

| 字段 | 说明 |
|------|------|
| `config.mcp_command` | **go-fs-mcp-server 绝对路径**（必填） |
| `config.mcp_args` | 固定 `[]` |
| `config.timeout` | 超时秒数，默认 `10` |
| `openclaw.entry` | `go-fs-mcp-skill`（Linux）或 `go-fs-mcp-skill.exe`（Windows） |

可直接复制模板：

```bash
# WSL
cp skill.wsl.json skill.json
# 编辑 mcp_command 为实际路径

# Windows
copy skill.windows.json skill.json
```

## 5. 本地验证

```bash
cd "$SKILL_DIR"
./go-fs-mcp-skill '{"toolName":"list_directory","params":{"path":"/mnt/e/github/go-fs-mcp"}}'
```

期望：`"success": true`

PowerShell 推荐管道：

```powershell
'{"toolName":"list_directory","params":{"path":"e:/github/go-fs-mcp"}}' | .\go-fs-mcp-skill.exe
```

## 6. 启用 OpenClaw

```bash
openclaw gateway restart
openclaw skills list
openclaw skills info go-fs-mcp-skill
```

在对话中使用触发词，例如：`列出 /mnt/e/github/go-fs-mcp 目录内容`
