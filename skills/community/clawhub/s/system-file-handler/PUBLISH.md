# 发布到 ClawHub

本文说明如何将 `publish-skill` 目录发布到 [clawhub.ai](https://clawhub.ai)。

## 发布前检查

- [ ] `SKILL.md` 存在且 frontmatter 含 `name`、`description`、`version`（semver）
- [ ] `name` 符合 slug 规则：`^[a-z0-9][a-z0-9-]*$`（当前：`go-fs-mcp-skill`）
- [ ] 包内**无** `.exe` 或其他二进制（见 `.clawhubignore`）
- [ ] 总大小 < 50MB
- [ ] `LICENSE` 已包含（MIT-0）
- [ ] `metadata.openclaw.requires.bins` 声明了 `go-fs-mcp-skill` 与 `go-fs-mcp-server`

## 方式一：ClawHub CLI（推荐）

```bash
# 1. 登录
clawhub login

# 2. 预览（可选）
clawhub skill publish ./publish-skill --slug go-fs-mcp-skill --dry-run

# 3. 发布
cd /path/to/go-fs-mcp
clawhub skill publish ./publish-skill \
  --slug go-fs-mcp-skill \
  --name "文件系统 MCP 技能" \
  --version 1.0.0 \
  --changelog "Initial release: Go MCP filesystem skill with 6 tools"
```

后续版本更新时递增 `--version`（如 `1.0.1`）并更新 changelog。

## 方式二：ClawHub 网站上传

1. 登录 <https://clawhub.ai>
2. 进入 Publish / Upload Skill
3. 上传 `publish-skill` 目录中的**文本文件**（或打包为 zip，确保无二进制）
4. 填写 slug：`go-fs-mcp-skill`
5. 版本：`1.0.0`
6. 提交并等待安全扫描通过

## 方式三：sync（多 skill 仓库）

若 go-fs-mcp 作为 skill 目录仓库管理：

```bash
clawhub sync --dry-run --owner <your-handle>
clawhub sync --all --owner <your-handle>
```

需将 `publish-skill` 放在仓库的 `skills/go-fs-mcp-skill/` 下，或调整 sync 路径。

## 用户安装

发布成功后，用户可通过：

```bash
openclaw skills install go-fs-mcp-skill
```

或 ClawHub 页面安装，然后按 [INSTALL.md](INSTALL.md) 构建二进制并配置 `skill.json`。

## 常见问题

| 问题 | 处理 |
|------|------|
| 扫描拒绝：未声明的二进制依赖 | 确认 `SKILL.md` metadata 含 `requires.bins` |
| 扫描拒绝：二进制文件 | 检查 `.clawhubignore`，勿上传 `.exe` |
| slug 无效 | 仅用小写字母、数字、连字符 |
| 版本已存在 | 递增 semver 后重新发布 |
