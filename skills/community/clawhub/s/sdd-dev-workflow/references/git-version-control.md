# Git 版本控制规范

本文档定义 SDD 工作流中强制性的 Git 版本控制策略，确保代码可追溯和可恢复。

---

## 核心原则

> **AI 开发不确定性高 → Git 是安全网**

- ✅ 每个项目**必须**使用 Git 管理
- ✅ 每个小阶段**必须**提交
- ✅ 验收通过后**必须**推送

---

## 初始化规范

### 新项目检查

**触发条件**：项目目录不存在 `.git` 文件夹

**处理流程**：

```bash
# 1. 检查是否已初始化
if [ ! -d ".git" ]; then
  echo "⚠️ 项目未使用 Git 管理"

  # 2. 询问 Git 仓库地址
  # 优先级：用户指定 > 默认工作空间 > 本地初始化
  GIT_REPO="${GIT_REPO:-}"

  if [ -n "$GIT_REPO" ]; then
    # 使用指定仓库
    git clone "$GIT_REPO" .
  else
    # 本地初始化
    git init
    git add .
    git commit -m "chore: 初始化项目结构"
  fi
fi
```

### Git 仓库配置

**默认工作空间**（推荐）：

```
工作空间: ~/openclaw/workspace
工作区:   projects/ (正式) 或 tmp/ (临时)
```

**仓库地址格式**：

| 场景 | 仓库地址 |
|------|----------|
| 正式项目 | `git@github.com:username/project-name.git` |
| 临时项目 | 本地 Git（不推送到远程） |
| 私有仓库 | `git@gitee.com:company/project.git` |

---

## 提交规范

### 提交时机

**必须提交的阶段**：

| 阶段 | 提交信息模板 | 说明 |
|------|-------------|------|
| constitution | `docs: 添加项目宪法` | 宪法定义完成 |
| specify | `docs: 完成规范定义` | speckit.specify 完成 |
| clarify | `docs: 完成需求澄清` | speckit.clarify 完成 |
| plan | `docs: 完成技术规划` | speckit.plan 完成 |
| tasks | `docs: 完成任务分解` | speckit.tasks 完成 |
| analyze | `docs: 完成依赖分析` | speckit.analyze 完成 |
| implement | `feat: 实现核心功能` | 代码实现完成 |
| acceptance | `test: 通过验收测试` | 验收通过 |

### 提交命令

```bash
# 每个阶段完成后执行
git add .
git commit -m "<commit-message>"

# 示例
git add . && git commit -m "docs: 完成规范定义"
```

### Commit 消息规范

**格式**：`<type>: <subject>`

**类型**：

| Type | 用途 |
|------|------|
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `docs` | 文档更新 |
| `refactor` | 重构 |
| `test` | 测试相关 |
| `chore` | 构建/工具 |

**示例**：
- `feat: 实现用户登录接口`
- `fix: 修复数据库连接错误`
- `docs: 更新 API 文档`

---

## 推送规范

### 推送时机

**验收通过后立即推送**：

```bash
# 验收通过后执行
if [ "$ACCEPTANCE_RESULT" = "PASS" ]; then
  # 1. 最终提交
  git add .
  git commit -m "chore: 工作流完成 - $(date +%Y-%m-%d)"

  # 2. 推送到远程（仅正式项目）
  if [ -n "$(git remote -v)" ]; then
    git push origin main
    echo "✅ 已推送到远程仓库"
  fi
fi
```

### 分支策略

**简单项目**（推荐）：
- 单分支：`main`
- 直接在 main 上开发

**复杂项目**：
- 主分支：`main`（受保护）
- 开发分支：`develop`
- 功能分支：`feature/<feature-name>`

---

## 回滚策略

### 常见场景

| 场景 | 命令 | 说明 |
|------|------|------|
| 撤销最近一次提交 | `git reset --soft HEAD~1` | 保留修改 |
| 恢复删除的文件 | `git checkout -- <file>` | 从最新提交恢复 |
| 回退到上一个版本 | `git reset --hard HEAD~1` | 丢弃修改（谨慎） |
| 查看历史记录 | `git log --oneline -10` | 最近 10 次提交 |

### 紧急恢复

**AI 改错代码后恢复**：

```bash
# 1. 查看修改
git status
git diff

# 2. 恢复单个文件
git checkout -- <file>

# 3. 恢复所有修改
git checkout -- .

# 4. 回退到上一个稳定版本
git reset --hard <commit-hash>
```

---

## Git 集成到 SDD 工作流

### Autonomous Agent 模板

```bash
# 在 autonomous agent 任务中增加 Git 步骤

## Git 版本控制（强制）

1. **初始化检查**（Phase 0）
   ```bash
   if [ ! -d ".git" ]; then
     # 询问 Git 仓库地址或使用默认
     GIT_REPO="${GIT_REPO:-}"
     if [ -n "$GIT_REPO" ]; then
       git clone "$GIT_REPO" .
     else
       git init
       git add .
       git commit -m "chore: 初始化项目"
     fi
   fi
   ```

2. **阶段提交**（每个 phase 完成后）
   ```bash
   git add . && git commit -m "docs: 完成 <phase-name>"
   ```

3. **最终推送**（验收通过后）
   ```bash
   if [ "$ACCEPTANCE_RESULT" = "PASS" ]; then
     git add . && git commit -m "chore: 工作流完成"
     [ -n "$(git remote -v)" ] && git push origin main
   fi
   ```
```

---

## 检查清单

**每个阶段完成后**：
- [ ] 执行 `git status` 检查修改
- [ ] 执行 `git add .` 添加修改
- [ ] 执行 `git commit -m "..."` 提交
- [ ] 验证提交：`git log -1`

**验收通过后**：
- [ ] 最终提交
- [ ] 推送到远程（仅正式项目）
- [ ] 验证推送：`git log origin/main -1`

---

## 常见问题

### Q: 临时项目也需要 Git 吗？

**A**: 是的。即使是临时项目，AI 开发的不确定性也需要版本控制。但临时项目**不推送**到远程仓库。

### Q: 如果用户没有提供 Git 仓库地址？

**A**: 使用本地 Git 初始化，不推送到远程。代码仍然有版本控制保护。

### Q: 提交冲突怎么办？

**A**:
```bash
# 1. 查看冲突
git status

# 2. 手动解决冲突后
git add <conflicted-file>
git commit -m "chore: 解决合并冲突"
```

### Q: 误删重要文件怎么办？

**A**:
```bash
# 从 Git 历史恢复
git checkout -- <deleted-file>

# 如果已提交，从上一个版本恢复
git checkout HEAD~1 -- <deleted-file>
```

---

**最后更新**: 2026-03-13
**版本**: v1.0
