# SkillHub Publishing Guide

> SkillHub (skillhub.cn) 是第三方 Skill 发布平台。本指南覆盖 CLI 安装、登录、frontmatter 兼容、dry-run 预检、正式发布、Windows 兼容、故障排查。

## 平台对比

| 维度 | ClawHub | SkillHub |
|------|---------|----------|
| 域名 | clawhub.ai | skillhub.cn |
| frontmatter | name + description | slug + displayName + version + summary + license |
| 版本号 | --version 命令行参数 | frontmatter 内 version 字段 |
| Token 环境变量 | CLAWHUB_TOKEN | SKILLHUB_TOKEN（login 时传入） |
| 发布命令 | clawhub publish（v5.18 现实校准：CLI v0.9.0 实际支持的命令） | skillhub publish |
| 预检 | 无（--dry-run 文档描述但 CLI v0.9.0 未实现） | --dry-run |
| Changelog | --changelog 参数 | --changelog 参数 |
| slug 冲突检查 | clawhub inspect | 409 错误 |
| 实名认证 | 无 | 需实名认证 |
| 审核流程 | 无 | pending_review → 审核通过 |
| Windows 支持 | 原生 | 需 python 直接调用（python3 是 stub） |

## CLI 安装

### Mac/Linux

```bash
curl -fsSL https://skillhub.cn/install/install.sh | bash -s -- --cli-only
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
skillhub --version
```

### Windows

Windows 上 `skillhub` 命令调用 `python3`，但 Windows Store 的 `python3.exe` 是 stub（exit code 9009），需用 `python` 直接调用：

```powershell
# 检查安装
python "%USERPROFILE%\.skillhub\skills_store_cli.py" --version

# 验证输出：skillhub 2026.x.x
```

**Windows 调用约定**：所有 `skillhub <command>` 在 Windows 上替换为：

```powershell
python "%USERPROFILE%\.skillhub\skills_store_cli.py" <command>
```

或用完整 Python 路径：

```powershell
& "C:\Python313\python.exe" "$env:USERPROFILE\.skillhub\skills_store_cli.py" <command>
```

## 登录

> ⚠️ **安全说明**：SkillHub CLI 的 `login` 命令要求通过 `--key` 参数传递 token。即使 token 从环境变量读取，`--key` 参数仍会出现在 process listing 中。这是 CLI 设计的限制，无法完全避免。建议在受控环境（非共享主机）执行 login，执行后清理 shell history。

**Token 来源**：环境变量 `SKILLHUB_TOKEN`（token 格式：`skh_` 开头，配置在用户环境变量中）

```bash
# Mac/Linux — 从环境变量读取
skillhub login --key "$SKILLHUB_TOKEN" --host https://api.skillhub.cn

# Windows — 从环境变量读取到临时变量（v5.17.6 移除 OS 持久存储读取类调用，遵守 SkillSpector Credential Access 约束）
$token = $env:SKILLHUB_TOKEN
python "$env:USERPROFILE\.skillhub\skills_store_cli.py" login --key $token --host https://api.skillhub.cn
Remove-Variable token  # 清除临时变量
```

> ❌ **绝对禁止**：`login --key "skh_real_token_value"` — 在命令中直接写死真实 token 值会被永久记录到 shell history、脚本文件、日志中

**验证登录**：

```bash
skillhub auth whoami
# 输出：userId / handle / role 三行
```

## Frontmatter 兼容

SKILL.md frontmatter 必须同时满足 ClawHub 和 SkillHub 的要求：

```yaml
---
# ClawHub 字段
name: "skill-name"
description: "技能描述，含触发词和 Do NOT scope"

# SkillHub 字段（2026-07 新增）
slug: skill-name-ai          # 全网唯一，建议带 handle 后缀
displayName: Skill Name       # 展示名称
version: 1.0.0                # 版本号（SkillHub 从 frontmatter 读取）
summary: 技能简介             # 一句话概述
license: MIT                  # 开源许可证
---
```

### 字段对应关系

| 用途 | ClawHub 字段 | SkillHub 字段 | 说明 |
|------|-------------|--------------|------|
| 标识 | name | slug | ClawHub 用 name，SkillHub 用 slug |
| 描述 | description | summary | ClawHub 用 description（长文本），SkillHub 用 summary（短文本） |
| 版本 | --version 参数 | version 字段 | ClawHub 从命令行读，SkillHub 从 frontmatter 读 |
| 展示名 | 无 | displayName | SkillHub 独有 |
| 许可证 | 无 | license | SkillHub 独有 |

### slug 命名规则

- **全网唯一**：slug 冲突会报 409 错误
- **建议带 handle 后缀**：如 `skill-publisher-ai`、`web-to-fim-edwardwason`
- **保持一致**：ClawHub 和 SkillHub 用相同的 slug（如果都可用）

## 发布流程

### 1. 确认登录态

```bash
# Mac/Linux
skillhub auth whoami

# Windows
python "%USERPROFILE%\.skillhub\skills_store_cli.py" auth whoami
```

如果未登录，执行 `login` 命令。

### 2. dry-run 预检（必须通过）

```bash
# Mac/Linux
skillhub publish <path> --dry-run

# Windows
python "%USERPROFILE%\.skillhub\skills_store_cli.py" publish <path> --dry-run
```

**预期输出**：`✓ Dry-run passed: <slug>@<version>`

**常见错误**：
- `Error: SKILL.md 缺少 ...` → frontmatter 字段漏填，补齐后重试
- `403 请先完成实名认证` → 浏览器完成实名认证
- `409 slug 已被其他用户占用` → 修改 slug 为全网唯一

### 3. 正式发布

```bash
# Mac/Linux
skillhub publish <path> --changelog "变更说明"

# Windows
python "%USERPROFILE%\.skillhub\skills_store_cli.py" publish <path> --changelog "变更说明"
```

**预期输出**：`✓ Published: skillId=xxxxx status=pending_review`

发布后进入审核流程，审核通过后详情页可见。

### 4. 更新 Skill

更新流程与首次发布一致：
1. 保持 `slug` 不变
2. 递增 `version`（frontmatter 中）
3. 修改其他字段按需
4. `--changelog` 填写版本变更说明
5. 重新 `skillhub publish`

## 安全规则

### Token 保护

- **SKILLHUB_TOKEN 不可硬编码到脚本或文档**：只通过环境变量传递
- **安全扫描必须检查 `skh_` 前缀**：扫描 `skh_[a-f0-9]{64}` 模式的硬编码值
- **login 命令的 --key 参数限制**：SkillHub CLI 要求 `--key` 传 token，即使从环境变量读取，token 仍会短暂出现在 process listing 中。缓解措施：在受控环境执行、执行后清理 history、不在共享主机上运行

### 环境变量配置

```powershell
# Windows 永久设置
[Environment]::SetEnvironmentVariable("SKILLHUB_TOKEN", "skh_your_token_here", "User")
$env:SKILLHUB_TOKEN = "skh_your_token_here"

# Mac/Linux
export SKILLHUB_TOKEN="skh_your_token_here"
```

## 故障排查

### `command not found: skillhub`（Mac/Linux）

```bash
source ~/.zshrc
# 或
~/.local/bin/skillhub --version
```

### `exit code 9009`（Windows）

**原因**：Windows Store 的 `python3.exe` 是 stub，不实际执行 Python。

**修复**：用 `python` 或完整路径替代：

```powershell
python "%USERPROFILE%\.skillhub\skills_store_cli.py" --version
# 或
& "C:\Python313\python.exe" "$env:USERPROFILE\.skillhub\skills_store_cli.py" --version
```

### `401 invalid api key`

Token 已被撤销或失效。重新创建 Token，再执行 `login`。

### `403 请先完成实名认证`

浏览器打开 [skillhub.cn](https://skillhub.cn) → 个人中心 → 实名认证 → 完成人脸核身。

### `409 slug 已被其他用户占用`

修改 SKILL.md frontmatter 中的 `slug` 为全网唯一标识（建议带 handle 后缀）。

### `429 请求过于频繁`

触发了平台限频，等约 1 分钟后重试。

### `400 不允许的文件类型`（v5.1 新增，重要）

**原因**：SkillHub 对上传文件类型有严格限制，以下文件会被拒绝：
- `.gitignore`（dotfile）
- `LICENSE`（无扩展名）
- `.claude-plugin/`（隐藏目录）
- `.github/`（隐藏目录）
- 其他无扩展名文件或 dotfile

**修复**：推荐用临时副本方式发布，避免操作原文件：

```powershell
# 用 robocopy 复制到临时目录（排除不支持的文件）
$skillPath = "<your-skill-path>"
$tempPath = "<parent-dir>\_skillhub_temp"
robocopy $skillPath $tempPath /E /XD .git __pycache__ .clawhub .claude-plugin .github /XF .gitignore LICENSE

# 发布临时副本
python "$env:USERPROFILE\.skillhub\skills_store_cli.py" publish $tempPath --changelog "xxx"

# 清理临时目录
Remove-Item $tempPath -Recurse -Force
```

> **重要**：ClawHub 和 GitHub 允许这些文件，只有 SkillHub 会拒绝。三平台发布时，SkillHub 发布步骤需要单独处理文件类型。

### 发布成功但详情页显示"未找到"

审核还在进行中。前往个人中心 → 我的 Skill 查看实时状态，审核通过后详情页自动可见。

### `argument --key: expected one argument`（Windows PowerShell）

**原因**：PowerShell `$env:SKILLHUB_TOKEN` 在参数传递时可能被吞掉。

**修复**：从环境变量读取到临时变量，传完后清除：

```powershell
# 从环境变量读取 SkillHub 凭证到临时变量
$token = $env:SKILLHUB_TOKEN
python script.py login --key $token --host https://api.skillhub.cn
Remove-Variable token  # 清除临时变量
```

> ⚠️ **CLI 限制**：SkillHub CLI 要求 `--key` 传 token，无法完全避免 process listing 暴露。建议在受控环境执行。绝对禁止把真实 token 值写死在脚本或命令中。
```

## 参考链接

- [SkillHub 官网](https://skillhub.cn)
- [CLI 发布教程](https://skillhub.cn/tutorials#publish-via-cli)
- [Agent 自然语言发布规范](https://skillhub.cn/ai/release.md)
