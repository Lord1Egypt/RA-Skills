---
name: sdd-dev-workflow
description: "规范驱动开发工作流（SDD + Speckit + Claude Code）。用于复杂软件开发项目。⚠️ 必需环境变量: ZHIPU_API_KEY。可选: GITHUB_TOKEN, ANTHROPIC_API_KEY。当用户需要开发复杂应用、进行多迭代开发项目、使用 sessions_spawn 自动化开发时使用此 skill。"
---

# SDD 开发工作流 Skill

> **快速开始**：见下方 | **安装指南**：[references/installation.md](references/installation.md) | **问题排查**：[references/troubleshooting.md](references/troubleshooting.md)

## 🎯 核心理念

> **用规范驱动开发（SDD）把需求变成结构化的"规范文档"，让 LLM 在准确上下文中输出更符合预期的代码。**

**三大原则**：规范优先 → 规范锚定 → 规范作为源

---

## ⚡ 快速开始

```bash
# 环境检查
~/.openclaw/skills/sdd-dev-workflow/scripts/check-environment.sh

# 创建项目
~/.openclaw/skills/sdd-dev-workflow/scripts/init-project.sh my-project
cd ~/openclaw/workspace/projects/my-project

# 启动开发
claude --permission-mode acceptEdits
```

### Speckit 工作流

```bash
/speckit.constitution 阅读并使用 ~/.openclaw/skills/sdd-dev-workflow/templates/constitution-enterprise.md
/speckit.specify [功能描述]
/speckit.clarify    # ⚠️ 强制执行至少1次
/speckit.plan [技术栈]
/speckit.tasks
/speckit.analyze    # ⚠️ 强制执行至少1次
/speckit.implement 严格遵循宪法 @.specify/memory/constitution.md
```

---

## 🔄 迭代开发流程

> **新项目 vs 迭代**：流程相同，区别仅在于初始化

### 流程对比

| 项目类型 | GitHub 初始化 | Specify | 特性分支 | 验收后 |
|---------|-------------|---------|---------|--------|
| **新项目** | ✅ 需要 | ✅ 初始化 | 自动创建 | 推送 + PR |
| **迭代** | ❌ 跳过 | ✅ 新迭代 | 自动创建 | 推送 + PR |

### 项目初始化（仅新项目）

> **⚠️ 询问用户**：GitHub 仓库如何处理？

**选项 1：新建仓库**
```bash
gh repo create my-project --private --clone
cd my-project
```

**选项 2：关联现有仓库**
```bash
git init
git remote add origin https://github.com/user/existing-repo.git
```

**然后执行 Specify init（仅一次）**：
```bash
specify init . --here --ai claude --force --no-git
```

### 迭代开发（跳过项目初始化）

**已初始化项目，直接创建新迭代**：
- 跳过 GitHub 初始化
- 跳过 `specify init`
- 直接在 Claude Code 执行：`/speckit.specify <功能描述>`

**Specify 序号自动递增**：
```bash
# 检测下一个序号
next_num=$(~/.openclaw/skills/sdd-dev-workflow/scripts/get-next-iteration.sh)
iteration_name="${next_num}-new-feature"
```

**问题修复**：Specify CLI 创建迭代时序号可能重复（001-xxx, 001-yyy），使用 `get-next-iteration.sh` 自动检测最大序号 + 1。

---

## 🔒 Git 版本控制（强制）

> **AI 开发不确定性高 → Git 是安全网**

### 初始化检查

**触发条件**：项目目录不存在 `.git` 文件夹

```bash
# 检查并初始化
if [ ! -d ".git" ]; then
  # 询问 Git 仓库地址或使用默认
  git init
  git add .
  git commit -m "chore: 初始化项目结构"
fi
```

### 提交规范

**每个阶段完成后必须提交**：

| 阶段 | 提交信息 |
|------|----------|
| constitution | `docs: 添加项目宪法` |
| specify | `docs: 完成规范定义` |
| clarify | `docs: 完成需求澄清` |
| implement | `feat: 实现核心功能` |
| acceptance | `test: 通过验收测试` |

```bash
# 每个阶段完成后执行
git add . && git commit -m "<commit-message>"
```

### 验收后自动 PR

**触发条件**：验收通过 + 特性分支（非 main）

```bash
# 检查验收结果
if [ "$ACCEPTANCE_RESULT" = "PASS" ]; then
  # 提交最终变更
  git add . && git commit -m "chore: 工作流完成"

  # 检查是否在特性分支
  current_branch=$(git branch --show-current)
  if [ "$current_branch" != "main" ]; then
    # 推送特性分支
    git push -u origin "$current_branch"

    # 创建 PR
    gh pr create \
      --title "feat: $current_branch" \
      --body "## 变更说明

- 迭代序号：$current_branch
- 验收状态：✅ PASS

## 测试结果

- 语法检查：通过
- 单元测试：通过
- 服务启动：验证成功" \
      --base main
  else
    # main 分支直接推送
    [ -n "$(git remote -v)" ] && git push origin main
  fi
fi
```

详见：[references/git-version-control.md](references/git-version-control.md)

---

## 📦 依赖自动安装（零注意力）

> **完成开发，不为工具停顿**

### 两层依赖策略

| Layer | 类型 | 处理方式 |
|-------|------|----------|
| **Layer 1** | 预装依赖 | 环境检查脚本验证 |
| **Layer 2** | 项目依赖 | 遇到时自动安装 |

### 自动安装逻辑

```bash
# 检测到 ModuleNotFoundError 时自动执行
if error contains "ModuleNotFoundError: No module named 'fastapi'"; then
  pip install fastapi
fi
```

**不询问，直接安装**。

### 预装依赖检查

```bash
~/.openclaw/skills/sdd-dev-workflow/scripts/check-environment.sh
```

详见：[references/dependency-installation.md](references/dependency-installation.md)

---

## ⚠️ 工具链协作方式（必读）

### Specify CLI 的角色

```
Specify CLI         →       Claude Code          →      完成开发
（仅用于初始化）           （执行 /speckit 命令）        （代码实现）
```

**Specify CLI 仅用于初始化**：
- ✅ `specify init` 初始化项目结构（每个项目执行一次）
- ❌ **不支持** clarify/plan/tasks/analyze/implement

**非交互模式**：
```bash
specify init . --here --ai claude --force --no-git
```

**后续所有 /speckit 命令都在 Claude Code 内执行**。

### 权限模式选择

| 模式 | 用途 | 行为 | 安全等级 |
|------|------|------|---------|
| `acceptEdits` | 人工监督开发 | 文件编辑自动批准，bash脚本需确认 | ✅ 推荐 |
| `bypassPermissions` | 自动化 agent | 所有操作自动批准 | ⚠️ 仅限隔离环境 |

**安全建议**：
- **生产环境** → `acceptEdits` + 人工审核
- **隔离测试环境** → `bypassPermissions`（VM/容器）
- **禁止**：在生产服务器使用 `bypassPermissions`

### 最终目标

| ❌ 错误理解 | ✅ 正确理解 |
|------------|------------|
| 生成 spec.md | 完成代码实现 |
| 生成 plan.md | 通过测试验证 |
| 生成 tasks.md | 功能可以运行 |

**完成标准**：
- ✅ 代码已实现（不是文档）
- ✅ 测试已通过
- ✅ 功能可运行

---

## 🚨 子 Agent 强制规则（CRITICAL）

> **核心原则**：子 agent = 流程驱动器（driver），不是代码实现者（implementer）

### 绝对禁止

- ❌ **禁止使用 `write` 工具写代码文件**（`src/**/*.py`, `tests/**/*.py`）
- ❌ **禁止跳过 /speckit.* 命令**

### 必须执行

- ✅ **必须通过 `sdd-driver.sh` 脚本操作**
- ✅ **必须通过 tmux 驱动 Claude Code**

### 意外处理

| 情况 | 可恢复 | 行动 |
|------|--------|------|
| 429 rate limit | ✅ | 等待 5 分钟后重试 |
| timeout | ✅ | 重启会话或增加超时 |
| stuck | ✅ | 重启会话 |
| execution_error | ✅ | 让 Claude Code 修复 |
| template_missing | ❌ | **通知人工** |
| 需要补充上下文 | ❌ | **通知人工** |

详见：[references/autonomous-agent.md](references/autonomous-agent.md)

---

## 📋 Speckit 工作流

```
init → constitution → specify → clarify → plan → tasks → analyze → implement
```

**⚠️ 强制阶段**：clarify ≥1 次，analyze ≥1 次

### 人类介入点

| 阶段 | 介入原因 | 介入方式 |
|------|----------|----------|
| clarify | 需求歧义 | 发送问题 → 等待回复 |
| analyze | 一致性问题 | 发送报告 → 等待确认 |

**介入判断**：信息不完整/疑义 → 转发用户；信息完整 → 自己决策
 补充规范  等待回复
 继续执行  收到后继续
```

#### 自动决策条件（无需介入）

- 信息完整，只是细节缺失
- 常规技术选择（如用 requests 还是 httpx）
- 宪法已有明确规定
- clarify 连续 2 次无问题
- 简单项目，需求明确

#### 需要介入的条件

- 多个方案各有优劣，需要业务决策
- 需求有明显矛盾或冲突
- 涉及外部依赖或资源
- 超出宪法规定的边界
- analyze 发现严重一致性问题

---

## 🏛️ 公共宪法模板

### 使用方式

```bash
# 在 Claude Code 中引用公共宪法
/speckit.constitution 阅读并使用公共宪法模板 ~/.openclaw/skills/sdd-dev-workflow/templates/constitution-enterprise.md
```

**模板位置**：
- `templates/constitution-enterprise.md`（推荐）
- `templates/constitution-lite.md`（精简）

详见：[references/constitution-guide.md](references/constitution-guide.md)

---

## 📁 项目路径规范

### 标准目录结构

```
~/openclaw/workspace/
├── projects/                    # 正式开发项目（长期维护）
├── tmp/                         # 临时项目（验证、测试，可随时清理）
├── docs/                        # 文档（可选，按需创建）
├── research/                    # 深度研究报告
└── memory/                      # 日期日记
```

### 路径规则

| 类型 | 路径 | 示例 |
|------|------|------|
| **正式项目** | `projects/<name>/` | `projects/my-app/` |
| **临时项目** | `tmp/<name>/` | `tmp/test-workflow/` |
| **研究报告** | `research/<topic>/` | `research/ai-sovereignty/` |

### 新项目创建规范

```bash
# ✅ 正式项目
~/.openclaw/skills/sdd-dev-workflow/scripts/init-project.sh my-project

# ✅ 临时项目
~/.openclaw/skills/sdd-dev-workflow/scripts/init-project.sh test-xyz --tmp

# ❌ 错误：在 workspace 根目录创建
cd ~/openclaw/workspace && specify init my-project  # 错误！
```

---

## 🚀 使用子 Agent（推荐）

### 标准流程

1. **启动 Claude Code**（bypassPermissions 模式）
2. **逐阶段执行** SDD 流程（constitution → specify → clarify → plan → tasks → analyze → implement）
3. **验收测试**（py_compile + pytest + uvicorn）
4. **输出结果**（ACCEPTANCE_RESULT: PASS | FAIL）

**关键等待规则**：
- ⏱️ 高峰期（12:00-18:00 GMT+8）GLM-5 响应可能需要 1-5 分钟
- ⏱️ 使用 `process` 工具时，设置 `timeoutMs: 300000`（5分钟）
- ⏱️ 不要在 30 秒内判定为超时

**完成标准**：
- ✅ 代码已实现（不是文档）
- ✅ 测试已通过（至少 1 个核心测试）
- ✅ 功能可运行（服务能启动）

**详细代码模板**：见 [references/autonomous-agent.md](references/autonomous-agent.md)

---

## 🔄 长时间运行 Agent

> **挑战**：上下文丢失、进度中断、状态不可知

**解决方案**：断点续传机制

```
.task-context/
├── progress.json     # 进度跟踪
├── checkpoint.md     # 检查点快照
└── session-log.md    # 会话日志
```

**恢复中断任务**：
```javascript
sessions_spawn({
  task: "继续开发 [项目]，读取 .task-context/checkpoint.md 恢复上下文"
})
```

详见：[references/long-running-agent.md](references/long-running-agent.md)

---

## 📐 开发最佳实践

详见：[references/best-practices.md](references/best-practices.md)

---

## ⚠️ 常见问题

- **Specify CLI 卡住** → 已跳过，使用离线模式
- **429 限流** → 等待 5 分钟后重试
- **ModuleNotFoundError** → 直接 `pip install <module>`
- 详细排查：[references/troubleshooting.md](references/troubleshooting.md)

---

## 📚 参考文档

| 文档 | 用途 |
|------|------|
| [installation.md](references/installation.md) | 安装与初始化 |
| [autonomous-agent.md](references/autonomous-agent.md) | 子 agent 模式 |
| [constitution-guide.md](references/constitution-guide.md) | 宪法模板指南 |
| [acceptance-protocol.md](references/acceptance-protocol.md) | 验收协议规范 |
| [git-version-control.md](references/git-version-control.md) | Git 版本控制 |
| [dependency-installation.md](references/dependency-installation.md) | 依赖自动安装 |
| [troubleshooting.md](references/troubleshooting.md) | 问题排查 |

---

## ⚠️ 安全警告

### 风险评估

| 操作类型 | 风险等级 | 说明 |
|---------|---------|------|
| 环境变量 | 中 | 需要 ZHIPU_API_KEY（必需）、GITHUB_TOKEN（可选） |
| 自动安装 | 中 | 脚本会自动执行 npm install、pip install、apt install |
| Git 操作 | 中 | 自动初始化仓库、提交、推送、创建 PR |
| 文件读写 | 低 | 操作 ~/.openclaw/ 和 ~/openclaw/workspace/ 目录 |
| 权限模式 | 高 | 推荐使用 acceptEdits，bypassPermissions 仅限隔离环境 |

### 使用建议

**✅ 推荐做法**：
- 在 VM/容器中运行
- 使用测试令牌，避免生产凭据
- 使用 `acceptEdits` 模式，人工审核 bash 脚本
- 定期备份 `~/openclaw/workspace/` 目录

**❌ 避免操作**：
- 在生产服务器使用 `bypassPermissions`
- 使用高权限 GitHub 令牌
- 直接运行未经审查的网络脚本

**监控工具**：见 [references/monitoring.md](references/monitoring.md)
