# Structuring Git Workflow

AI 编程助手的 Git 工作流规范技能 —— 在关键节点自动设卡，确保分支纪律、结构化 commit 和安全操作。

A Git workflow discipline skill for AI coding assistants — enforces branch discipline, structured commits, and safety checks at every decision point.

---

## 这个技能做什么？ / What does this skill do?

当 AI 帮你写代码时，它会在以下节点主动介入：

| 场景 | AI 的行为 |
|------|----------|
| 开始新功能 | 自动创建 `feature/` 分支，不会直接在 main 上改 |
| 修 Bug | 自动创建 `fix/` 分支 |
| 模块完成 | 主动提醒你 commit，不用你记 |
| 写 commit 信息 | 用统一的 `<type>: <description>` 格式 |
| 危险操作前 | 列 4 点安全检查清单 |
| 推送代码 | commit 和 push 分离，不会自动推 |

When AI writes code for you, this skill intervenes at key moments:

| Trigger | AI's behavior |
|---------|--------------|
| Starting new work | Creates `feature/` or `fix/` branch, never commits to main |
| Module complete | Proactively reminds you to commit |
| Writing commit messages | Uses structured `<type>: <description>` format |
| Destructive operations | Runs a 4-point safety checklist first |
| Pushing code | Keeps commit and push separate, never auto-pushes |

---

## 安装 / Installation

### Claude Code

```bash
# 克隆到 skills 目录
git clone https://github.com/yiiknow/structuring-git-workflow.git ~/.claude/skills/structuring-git-workflow
```

### ClawHub

在 ClawHub 搜索 `structuring-git-workflow`，一键安装。

Search `structuring-git-workflow` on ClawHub and install with one click.

---

## 使用 / Usage

安装后自动生效。AI 在以下时机自动触发技能规则：

- 进入 git 仓库开始工作
- 模块/功能完成时
- commit / push / merge / rebase 前
- 任何危险 git 操作前

**无需手动调用。** 如果你发现 AI 没有遵守规则，可以提醒它："请遵守 structuring-git-workflow 的规则。"

Once installed, the skill activates automatically. The AI follows the rules when:

- Working in any git repository
- Completing a module or feature
- Before committing, pushing, merging, or rebasing
- Before any destructive git operation

**No manual invocation needed.** If the AI isn't following the rules, say: "Follow the structuring-git-workflow rules."

---

## 5 条核心规则 / 5 Core Rules

### 1. 不直接在 main/master 上 commit / Never commit to main

```
feature/<name>   → 新功能 / new features
fix/<name>       → Bug 修复 / bug fixes
refactor/<name>  → 重构 / refactoring
```

### 2. 模块完成主动提醒 / Remind at module boundaries

每完成一个功能单元，AI 主动问 "要 commit 吗？"

After each module, AI proactively asks "Ready to commit?"

### 3. 结构化 commit 信息 / Structured messages

```
<type>: <description>
```

类型 / Types: `feat`, `fix`, `refactor`, `style`, `docs`, `test`, `chore`

可通过项目 CLAUDE.md 自定义格式和语言。

Format and language can be customized via project CLAUDE.md.

### 4. 危险操作前安全检查 / Safety checklist

`reset --hard` / `rebase` / `force push` / `branch -D` 前检查 4 项：

1. 是不是共享分支？→ 别改历史 / Shared branch? Don't rewrite history
2. 有没有未提交的改动？→ 先 stash 或 commit
3. 在正确的分支上吗？→ `git branch` 确认
4. 远端最新吗？→ `git fetch` 先

### 5. Commit 和 Push 分离 / Commit ≠ Push

Commit 累积在本地，验证通过后再问是否 push。不自动推送。

Commits accumulate locally. Push only after verification and user confirmation.

---

## 自定义 / Customization

如果项目有自己的 commit 规范，在项目 `CLAUDE.md` 中写明即可，技能会自动遵循项目规则。

If your project has its own commit convention, define it in `CLAUDE.md` — the skill respects project-level rules over its defaults.

---

## 许可 / License

MIT-0
