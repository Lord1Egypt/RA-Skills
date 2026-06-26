---
name: skills-cli
description: High-level helper for managing agent skills using the ClawHub CLI and local skill folders. Use when the user wants to search, install, update, publish, or organize skills via command-line tooling (clawhub) and structured skill directories.
---

# Skills CLI Orchestrator

This skill explains how to **manage skills from the command line**，
结合本地技能目录与 ClawHub CLI，帮用户完成「找技能 / 装技能 / 更技能 / 发技能」的一整套流程。

它可以和 `clawhub-cli` 等更具体的技能配合使用：

- `clawhub-cli`：专门关注 ClawHub CLI 的具体命令。
- `skills-cli`（本 Skill）：站在更上层，帮你**选对命令、选对目录、选对动作**。

## When to Use

自动使用本 Skill 的场景：

- 用户说「管理 skills」、「skills 管理」、「skills cli」、「技能列表」、「安装/卸载/更新 技能」等。
- 用户不确定该用 `clawhub search / install / update / publish / sync` 中的哪一个。
- 用户想知道「本地 skills 放哪、ClawHub 上怎么对应、本地和远端怎么同步」。

如果用户已经明确说「用 clawhub 做某件事」，则优先复用 `clawhub-cli` 里的具体命令说明。

## 基础约定（Conventions）

在使用任何 CLI 前，先假设或确认：

- 当前工作目录（workdir）：通常是包含技能目录的项目根，例如：
   - `skills/`（默认 ClawHub 安装目录）
- 本地技能目录结构统一为：
  - `<skills-root>/<skill-slug>/SKILL.md`
  - 其它支持文件一律放在该目录下。

推荐将「公共 OpenClaw 技能」放在 `skills/` 下。

## 常见任务 / Decision Tree

当用户说「我想管理 skills」时，按以下决策树帮他选择命令：

1. **想找技能？**
   - 用 `clawhub search "关键词"`。
2. **已经知道一个 slug，想安装？**
   - 用 `clawhub install <slug>`。
3. **已经安装了一些技能，想看看有哪些？**
   - 用 `clawhub list` 查看 lockfile 记录。
4. **想把所有已安装技能更新到最新版？**
   - 用 `clawhub update --all`。
5. **只想更新某一个技能？**
   - 用 `clawhub update <slug> [--version <semver>]`。
6. **本地有一个新技能目录，想发布到 ClawHub？**
   - 用 `clawhub publish <path> --slug ... --name ... --version ... [--tags ...]`。
7. **有一批技能目录想批量同步 / 备份？**
   - 用 `clawhub sync --all`。

在回答时，只需要根据用户需求，选出对应分支，并给出具体命令模板。

## 本地技能管理（Local Skills Management）

### 1. 规划技能根目录

根据用户情况，推荐一个根目录：

- 公共 OpenClaw 技能：`skills/`

确保每个技能都在单独子目录下，例如：

- `skills/clawhub-cli/`
- `skills/publish-skills/`

### 2. 检查 / 创建 `SKILL.md`

对于每个技能目录：

1. 检查是否存在 `SKILL.md`。
2. 确认 frontmatter 至少包含：
   - `name`：小写 + 短横线（推荐）。
   - `description`：第三人称，高度概括 + 触发场景。
3. 如果缺少，提示用户补全或由 Agent 生成草稿。

### 3. 与 ClawHub 的对应关系

当某个本地技能需要发布到 ClawHub 时：

- 选定一个 `slug`（通常与目录名相近，例如 `clawhub-cli`）。
- 在 `SKILL.md` 中 `name` 字段可以与 slug 不同（更偏向人类可读）。
- 版本管理通过发布命令的 `--version` 控制。

## ClawHub CLI 管理（Remote Management）

> 具体命令细节由 `clawhub-cli` Skill 负责；本 Skill 负责**选择合适的命令**并组合使用。

### 1. 搜索 & 发现

当用户模糊地描述一个需求时（例如 “数据库备份 skill”）：

1. SSR（简单重述需求），然后建议在本地终端执行：

```bash
clawhub search "database backup"
```

2. 如用户提供更具体关键字或已有 slug，则直接跳到安装或更新。

### 2. 安装 & 卸载

- 安装：

```bash
clawhub install <skill-slug>
```

- （如果未来出现卸载命令）可以在此处补充卸载说明；当前版本主要关注安装 / 更新。

### 3. 更新（单个 / 全部）

- 更新所有：

```bash
clawhub update --all
```

- 更新单个：

```bash
clawhub update <skill-slug>
```

- 需要特定版本时：

```bash
clawhub update <skill-slug> --version <semver>
```

### 4. 发布 / 同步

当用户提到「备份我的 skills」「发到 ClawHub」「同步到远端」时：

- 单个技能：推荐使用 `clawhub publish`（参见 `publish-skills` Skill 的细节）。
- 多个技能：推荐使用 `clawhub sync --all`。

示例（单个技能）：

```bash
clawhub publish ./skills/clawhub-cli \
  --slug clawhub-cli \
  --name "ClawHub CLI Helper" \
  --version 0.1.0 \
  --tags latest
```

示例（批量）：

```bash
clawhub sync --all
```

可根据需要添加：

- `--tags latest`
- `--changelog "Update skills"`
- `--bump patch|minor|major`

## 验证与故障排查（Verification & Troubleshooting）

在给出命令之后，引导用户检查：

1. **CLI 输出**
   - 有没有报错（slug 冲突、未登录、版本号非法等）。
2. **本地记录**
   - 通过 `clawhub list` 查看本地锁文件记录。
3. **远端结果**
   - 让用户在浏览器打开 `clawhub.ai`，按 slug 或名称搜索。

如果命令失败：

- 解释错误类型（例如 slug 已存在 => 换一个 slug 或 bump 版本）。
- 根据错误类型，给出修正后的新命令。

## 使用示例（Examples）

### Example 1：用户说「帮我看看有哪些 skills，可以更新吗？」

Agent 使用本 Skill 的思路：

1. 建议用户在项目根目录执行：

```bash
clawhub list
clawhub update --all
```

2. 说明：
   - 第一条列出当前已安装技能。
   - 第二条把所有技能更新到最新版本。

### Example 2：用户说「我有几个 skills 想备份到 ClawHub」

1. 确认根目录（例如 `skills/`）。
2. 确认每个子目录都包含 `SKILL.md`。
3. 建议用户执行：

```bash
clawhub sync --all
```

4. 告诉用户：
   - 成功后，每个技能都会在 ClawHub 上生成或更新对应版本。
   - 可以在 Web 上按 slug 搜索验证。

