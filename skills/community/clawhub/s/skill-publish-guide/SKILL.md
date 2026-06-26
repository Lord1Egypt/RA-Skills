---
name: skill-publish-guide
description: "Guide for publishing and managing skills on ClawHub. Use when the user wants to publish, update, delete, or manage skills on ClawHub. 当用户需要发布、更新、删除或管理 ClawHub 上的技能时使用此技能。"
env:
  CLAWHUB_SITE: "Optional. Override ClawHub site URL for custom registry."
  CLAWHUB_REGISTRY: "Optional. Override registry API URL."
always: false
---

# ClawHub Publisher - Publish & Manage Skills on ClawHub

# ClawHub 发布器 - 在 ClawHub 上发布和管理技能

---

## Prerequisites / 前提条件

1. **clawhub CLI** must be installed. Verify with `clawhub -V`.
   **clawhub CLI** 必须已安装。用 `clawhub -V` 验证。

2. You must be logged in. Check with `clawhub whoami`. If not logged in, run `clawhub login`.
   必须已登录。用 `clawhub whoami` 检查。未登录则运行 `clawhub login`。

3. GitHub account must be at least 1 week old to publish.
   GitHub 账户需创建至少一周才能发布。

---

## SKILL.md Format / SKILL.md 格式

Every skill must have a `SKILL.md` file with YAML frontmatter:
每个技能必须包含带 YAML frontmatter 的 `SKILL.md` 文件：

```markdown
---
name: my-skill
description: "Short description of what this skill does / 技能简短描述"
env:
  MY_API_KEY: "Optional. Description of the env var / 可选。环境变量说明"
always: false
---

# Skill Title

Instructions and documentation here...
```

### Frontmatter Fields / Frontmatter 字段

| Field / 字段 | Required / 必填 | Description / 说明 |
|---|---|---|
| `name` | ✅ | Skill identifier, lowercase + hyphens / 技能标识符，小写+短横线 |
| `description` | ✅ | Short description for discovery / 用于搜索发现的简短描述 |
| `env` | ⬜ | Environment variables the skill needs / 技能所需的环境变量 |
| `always` | ⬜ | Whether skill stays loaded (default: false) / 是否常驻加载（默认 false） |

### Directory Structure / 目录结构

```
my-skill/
├── SKILL.md          # Required / 必需
├── scripts/          # Optional, helper scripts / 可选，辅助脚本
├── rules/            # Optional, reference files / 可选，参考文件
└── ...
```

**Important / 注意**:
- Do NOT include `.git`, `LICENSE`, `.DS_Store`, or binary files / 不要包含 `.git`、`LICENSE`、`.DS_Store` 或二进制文件
- Only text files are allowed / 只允许文本文件

---

## Publishing Workflow / 发布流程

### Step 1: Prepare / 准备

Ensure the skill folder contains a valid `SKILL.md` with proper frontmatter.
确保技能文件夹包含有效的 `SKILL.md` 和正确的 frontmatter。

### Step 2: Validate / 验证

Before publishing, verify:
发布前验证以下内容：

- [ ] `name` in frontmatter matches the `--slug` you plan to use / frontmatter 中的 `name` 与计划的 `--slug` 一致
- [ ] `description` is clear and includes trigger keywords / `description` 清晰且包含触发关键词
- [ ] All env vars used in commands are declared in `env` section / 命令中使用的环境变量都在 `env` 中声明
- [ ] No binary files, `.git`, or `LICENSE` in the folder / 文件夹中无二进制文件、`.git` 或 `LICENSE`
- [ ] No interactive prompts (AI Agent cannot answer y/n) / 无交互式提示（AI Agent 无法回答 y/n）

### Step 3: Publish / 发布

```bash
clawhub publish <path> \
  --slug <slug> \
  --name "<Display Name>" \
  --version <semver> \
  --tags latest \
  --no-input
```

**Parameters / 参数**:

| Param / 参数 | Required / 必填 | Description / 说明 |
|---|---|---|
| `<path>` | ✅ | Path to skill folder / 技能文件夹路径 |
| `--slug` | ✅ | URL identifier (lowercase + hyphens only) / URL 标识符（仅小写+短横线） |
| `--name` | ✅ | Display name / 显示名称 |
| `--version` | ✅ | Semantic version (e.g., `1.0.0`) / 语义化版本号 |
| `--tags` | ⬜ | Comma-separated tags (default: `latest`) / 逗号分隔的标签 |
| `--no-input` | ⬜ | Skip interactive prompts / 跳过交互提示 |

**Example / 示例**:
```bash
clawhub publish ./my-skill \
  --slug my-skill \
  --name "My Skill" \
  --version 1.0.0 \
  --tags latest \
  --no-input
```

### Step 4: Verify / 确认

After publishing, the skill enters security scan (usually takes a few minutes):
发布后技能进入安全扫描（通常需要几分钟）：

```bash
# Check skill status / 检查技能状态
clawhub inspect <slug>
```

If you see "Skill is hidden while security scan is pending", wait and retry.
如果看到"Skill is hidden while security scan is pending"，等待后重试。

---

## Updating a Skill / 更新技能

To update, publish with an **incremented version number**:
更新时需**升级版本号**：

```bash
clawhub publish ./my-skill \
  --slug my-skill \
  --name "My Skill" \
  --version 1.0.1 \
  --tags latest \
  --no-input
```

**Important / 注意**: The same version cannot be republished. If you delete a skill and republish, you must use a new version number.
同一版本号不可重复发布。删除后重新发布也必须使用新版本号。

---

## Deleting a Skill / 删除技能

```bash
clawhub delete <slug> --yes
```

**Warning / 警告**: Deletion is soft-delete. After deletion, the same version number cannot be reused for the same slug.
删除为软删除。删除后同一 slug 的同一版本号不可复用。

---

## Common Issues & Solutions / 常见问题与解决

| Error / 错误 | Cause / 原因 | Solution / 解决 |
|---|---|---|
| `Slug must be lowercase` | Slug contains uppercase / Slug 含大写 | Use lowercase + hyphens / 使用小写+短横线 |
| `Version already exists` | Same slug+version published before / 同 slug+版本已发布过 | Increment version / 升版本号 |
| `Remove non-text files` | Folder contains `.git`, `LICENSE`, binaries / 含非文本文件 | Remove those files / 删除这些文件 |
| `GitHub API rate limit exceeded` | Too many requests / 请求太频繁 | Wait 10 minutes / 等待 10 分钟 |
| `Connection lost while action was in flight` | Network issue or too many files / 网络问题或文件过多 | Retry with fewer files / 精简文件后重试 |
| Security scan flagged missing env declaration / 安全扫描标记缺少 env 声明 | Commands use env vars not declared in frontmatter / 命令使用了未在 frontmatter 中声明的环境变量 | Add `env` section to frontmatter / 在 frontmatter 中添加 `env` |
| Security scan flagged curl\|bash / 安全扫描标记 curl\|bash | Install script uses `curl \| bash` / 安装脚本使用 `curl \| bash` | Add security warning, recommend Homebrew/source build / 添加安全提示，推荐 Homebrew/源码构建 |

---

## Security Best Practices / 安全最佳实践

When writing a SKILL.md, follow these guidelines to pass ClawHub security review:
编写 SKILL.md 时，遵循以下准则以通过 ClawHub 安全审核：

1. **Declare all env vars** / 声明所有环境变量: If any command requires an API key or secret, declare it in the `env` section of frontmatter. Explain what it's for and whether it's optional.
   如果命令需要 API key 或密钥，在 frontmatter 的 `env` 中声明，说明用途和是否可选。

2. **Avoid curl|bash as primary install method** / 避免将 curl|bash 作为主要安装方式: Recommend Homebrew, Scoop, or source build first. If including a curl|bash script, add a security warning.
   优先推荐 Homebrew、Scoop 或源码构建。如包含 curl|bash 脚本，添加安全提示。

3. **No interactive prompts** / 无交互提示: AI Agents cannot answer y/n questions. All operations must be completable via command-line arguments.
   AI Agent 无法回答 y/n 问题。所有操作必须能通过命令行参数完成。

4. **Document network operations** / 说明网络操作: If the skill includes HTTP requests, DNS lookups, port scanning, etc., note this clearly so users are aware.
   如果技能包含 HTTP 请求、DNS 查询、端口扫描等，明确说明让用户知晓。

5. **Document credential storage** / 说明凭据存储: If the skill stores secrets locally (password vault, API keys), explain the encryption method and storage location.
   如果技能在本地存储密钥（密码保险库、API key），说明加密方式和存储位置。

6. **No binary files in skill bundle** / 技能包中不含二进制文件: Only include text files (Markdown, JSON, YAML, scripts). Binary files will be rejected.
   只包含文本文件（Markdown、JSON、YAML、脚本）。二进制文件会被拒绝。

---

## CLI Reference / CLI 命令参考

```bash
# Authentication / 认证
clawhub login                           # Login via browser / 浏览器登录
clawhub login --token <token>           # Login with API token / 用 API token 登录
clawhub logout                          # Logout / 登出
clawhub whoami                          # Check current identity / 查看当前身份

# Publish / 发布
clawhub publish <path> --slug <slug> --name "<name>" --version <ver>
                                        # Publish a skill / 发布技能

# Verify / 确认
clawhub inspect <slug>                  # View skill metadata / 查看技能元数据

# Delete & Restore / 删除与恢复
clawhub delete <slug> --yes             # Soft-delete a skill / 软删除技能
clawhub undelete <slug>                 # Restore deleted skill / 恢复已删除技能

# Batch / 批量
clawhub sync --all                      # Sync all local skills / 同步所有本地技能
clawhub sync --dry-run                  # Preview without uploading / 预览不上传
```
