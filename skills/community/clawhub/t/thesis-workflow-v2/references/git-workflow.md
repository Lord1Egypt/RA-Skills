# Git Workflow & Release Strategy

> **v1 / v2 双版本独立并行策略**
> 最后更新：2026-06-24（v2.0.6 发布时建立）

## 核心原则

**绝对隔离 + 各自演进 + ClawHub 独立 slug + 用户自主选择**

- v1 和 v2 是**两个独立发布的 skill**
- v1 在 ClawHub 用 `thesis-workflow` slug
- v2 在 ClawHub 用 `thesis-workflow-v2` slug
- 安装路径不同，状态文件隔离，互不影响
- **绝不自动合并**

## 为什么需要双版本

| 原因 | 说明 |
|------|------|
| **v2 改动大** | outline-anchored 重构 + 9 HIL + 新 CLI，影响整个框架 |
| **v2 测试不充分** | 当前只有真实 LLM 跑一遍的冒烟测试 |
| **升级风险** | v1 用户升级到 v2 可能导致流程不可用 |
| **可共存** | 测试充分前 v1 继续稳定，v2 并行演进 |

## 分支管理

### 分支结构

```
main       v1.x 长期维护分支（仅 v1 兼容性修复）
v2         v2.x 长期演进分支（v2 主线开发）
fix/v1.x-*  v1 短期修复（base on main，merge 回 main）
fix/v2.x-*  v2 短期修复（base on v2，merge 回 v2）
feature/*   新功能开发（base on 对应主线）
```

### 当前实际状态（2026-06-24）

| 分支 | 状态 | 最新 commit | 远程同步 |
|------|------|------------|----------|
| `main` | v1.7.3 长期 | df14c58 (v1.7.3) | ✅ 已同步 origin |
| `v2`（原 `feature/outline-anchored`）| v2.0.6 | 459e60f (v2.0.6) | ⚠️ 需推 6 个 commit |
| `tag v2.0-base` | v1.7.3 锚点 | df14c58 | ✅ 保留 |

### 分支规则

| 改动类型 | 进哪个分支 | 通过什么流程 |
|---------|-----------|-------------|
| v1 兼容性 bug 修复 | `main` | `fix/v1.x-*` → `main` |
| v1 新功能（不破坏 v1）| `main` 或 `feature/v1-*` | 直接进或 PR |
| v2 改动 | `v2` | `fix/v2.x-*` → `v2` |
| 共享文档（references/）| 各自分支 | 各自维护 |
| 绝不允许 | v2 → main 合并 | **违反双版本隔离原则** |

## 发布流程

### v1 发布（保持现状）

```bash
# 1. 在 main 上准备 v1.x 修复
git checkout main
# 修代码...
git add . && git commit -m "fix(v1.7.4): ..."
git tag v1.7.4

# 2. 推 GitHub
git push origin main --tags

# 3. 发 ClawHub（v1 slug）
cd /tmp  # 重要：从 /tmp 工作目录发布
clawhub skill publish /Users/hehe9737/GitHub/mba-thesis-workflow \
  --slug thesis-workflow \
  --owner hehe973781230 \
  --version 1.7.4 \
  --tags latest \
  --changelog "..."
```

### v2 发布（v2.0.6 起）

```bash
# 1. 在 v2 上准备 v2.x 修复
git checkout v2
# 修代码...
git add . && git commit -m "fix(v2.0.6): ..."
git tag v2.0.6

# 2. 推 GitHub
git push origin v2 --tags

# 3. 发 ClawHub（v2 slug，独立仓库）
cd /tmp  # 重要：从 /tmp 工作目录发布
clawhub skill publish /Users/hehe9737/GitHub/mba-thesis-workflow \
  --slug thesis-workflow-v2 \
  --owner hehe973781230 \
  --version 2.0.6 \
  --tags latest \
  --changelog "..."
```

### 关键差异

| 维度 | v1 | v2 |
|------|-----|-----|
| 分支 | `main` | `v2` |
| ClawHub Slug | `thesis-workflow` | `thesis-workflow-v2` |
| 安装路径 | `~/.openclaw/skills/thesis-workflow/` | `~/.openclaw/skills/thesis-workflow-v2/` |
| 状态文件位置 | `~/.openclaw/workspace/{paper}/` | `~/.openclaw/workspace/{paper_v2}/`（建议加 `_v2` 后缀）|
| 兼容性 | 向后兼容 v1.7.x | **不兼容 v1**，独立测试 |
| 升级风险 | 老用户安全升级 | **自愿升级** + 独立测试 |

## ClawHub 双 Slug 管理

### 当前状态

- `thesis-workflow` (v1) — owner: hehe973781230，latest: v1.7.3
- `thesis-workflow-v2` (v2) — **需新建仓库**

### 申请 thesis-workflow-v2 slug

1. ClawHub 控制台 → New Skill
2. Slug: `thesis-workflow-v2`
3. Owner: `hehe973781230`
4. 初始版本: v2.0.0 (可从 v1.7.7 的代码 import)
5. 之后用 `clawhub skill publish` 更新版本

### 关键命令（从 MEMORY.md 总结）

```bash
# 必须从 /tmp 工作目录发布
cd /tmp && clawhub skill publish /Users/.../thesis-workflow \
  --slug thesis-workflow-v2 \
  --owner hehe973781230 \
  --version 2.0.6 \
  --tags latest \
  --changelog "..."
```

**为什么从 /tmp**：CLI 把 `.` 当 workdir，仓库内发布会触发 "SKILL.md required" 错误。

## CHANGELOG 双版本管理

### 当前文件结构

```
CHANGELOG.md        ← 索引 + 版本线推荐表
CHANGELOG-v1.md     ← v1.0 → v1.7.3 完整历史
CHANGELOG-v2.md     ← v2.0.0 → v2.0.6 + alpha 阶段说明
```

### Alpha 阶段说明（v2 特有）

v1.7.4 / v1.7.5 / v1.7.6 / v1.7.7 **实际为 v2 早期 alpha**：
- 当时在 `feature/outline-anchored` 分支，版本号沿用 v1.7.x
- 正式命名为 v2 后，回溯标记
- git commit hash 保留可追溯
- 在 CHANGELOG-v2.md 顶部说明

## State 文件隔离

### 当前 v2 设计

v2 state 在 `~/.openclaw/workspace/{paper_name}/`：
- `_outline_state.json`
- `_orchestrate_state.json`

v1 也用相同路径。**v1 和 v2 论文如果同名会冲突**。

### 推荐方案

**方案 A：paper_name 加后缀**（简单）
```
v1 论文: paper_name = "A公司_论文_v1"
v2 论文: paper_name = "A公司_论文_v2"
```

**方案 B：环境变量切 root**（更彻底）
```bash
# v1 用户
export THESIS_WORKFLOW_ROOT=~/.openclaw/workspace
# state: ~/.openclaw/workspace/{paper}/

# v2 用户
export THESIS_WORKFLOW_ROOT=~/.openclaw/workspace_v2
# state: ~/.openclaw/workspace_v2/{paper}/
```

**推荐方案 B**，需在 v2 `state_manager_v2.py` 加 env 读取。

## Tag 策略

### 当前

- `v2.0-base` — 指向 v1.7.3，标记"v2 改造前稳定版"

### 推荐

- 保留 `v2.0-base`（v1.7.3 锚点）
- 新增 `v2.0.0` (commit 25b2c3a) — v2 起点
- 新增 `v2.0.6` (commit 459e60f) — v2 当前
- 后续每次发布打 `v2.0.x` / `v1.7.x` tag

## 风险与缓解

| 风险 | 等级 | 缓解措施 |
|------|------|---------|
| ClawHub 仓库权限 | 🔴 高 | v2 用新 slug 需先申请 |
| 文档拆分遗漏 | 🟡 中 | Phase 1 完整检查 |
| main 长期停滞 | 🟢 低 | 文档明确标"v1 永久分支" |
| v2 测试不充分 | 🔴 高 | ClawHub 标"beta/测试版" |
| 双版本用户混淆 | 🟡 中 | README 对比表 + ClawHub description |

## 检查清单（每次发布前）

- [ ] CHANGELOG 完整（含本版本所有改动）
- [ ] README 当前版本号同步
- [ ] SKILL.md frontmatter version 同步
- [ ] 所有测试通过
- [ ] 无敏感信息（grep 检查）
- [ ] 临时文件清理（`/tmp/*`, `~/.openclaw/workspace/test_*`）
- [ ] git tag 已打
- [ ] maintainer review commit
- [ ] 推 GitHub + 发 ClawHub 都做（不只推一个）

## 决策记录

| 日期 | 决策 | 原因 |
|------|------|------|
| 2026-06-24 | v1 / v2 独立发布 | v2 改动大，需独立测试 |
| 2026-06-24 | ClawHub 双 slug | 唯一能做到完全隔离 |
| 2026-06-24 | 拆 CHANGELOG-v1.md + CHANGELOG-v2.md | 文档清晰 |
| 2026-06-24 | v1.7.4-v1.7.7 标记为 v2 alpha | 诚实，但不改 git history（commit hash 保留）|
| 2026-06-24 | main 加 v2 独立声明 | 双向提醒用户 |

## 参考

- MEMORY.md（用户长期记忆）— ClawHub 发布绕过方案
- CHANGELOG-v2.md — v2 完整历史
- references/loop-design.md — v2 loop 设计原理
- references/checklist.md — 学术规范清单（共享）
