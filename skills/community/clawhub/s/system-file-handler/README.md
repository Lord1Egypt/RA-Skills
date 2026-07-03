# go-fs-mcp-skill — ClawHub 发布包

本目录是面向 [ClawHub](https://clawhub.ai) 的标准 Skill 发布包，可直接上传或经 CLI 发布。

## 包内文件

| 文件 | 说明 |
|------|------|
| `SKILL.md` | **必需**。ClawHub 主描述与 YAML frontmatter |
| `skill.json` | OpenClaw 运行时配置（安装后需改 `mcp_command`） |
| `skill.wsl.json` / `skill.windows.json` | 环境配置模板 |
| `INSTALL.md` | 从源码构建二进制说明 |
| `PUBLISH.md` | 发布到 ClawHub 的步骤 |
| `LICENSE` | MIT-0 许可证 |
| `.clawhubignore` | 排除二进制等非文本文件 |
| `scripts/` | 构建辅助脚本 |
| `config/` | OpenClaw 配置示例 |

## 重要说明

- ClawHub **仅接受文本文件**（≤ 50MB），**不要**将 `.exe` 或 Linux 二进制放入本目录上传。
- 用户从 ClawHub 安装后，需按 `INSTALL.md` 自行构建 `go-fs-mcp-skill` 与 `go-fs-mcp-server`。
- 完整源码仓库：<https://github.com/go-fs-mcp/go-fs-mcp>

## 快速发布

```bash
cd publish-skill
clawhub login
clawhub skill publish . --slug go-fs-mcp-skill --name "文件系统 MCP 技能" --version 1.0.0 --changelog "Initial release"
```

详见 [PUBLISH.md](PUBLISH.md)。
