# Contributing to MBA/学术论文多Agent协作工作流

> **v1 / v2 双版本独立并行** — 本项目维护两条独立版本线，新贡献者请先读完本文。

## 📑 目录

1. [当前项目状态](#当前项目状态)
2. [v2 不是 v1 的小升级，是重新设计](#-v2-不是-v1-的小升级是重新设计)
3. [分支管理](#分支管理)
4. [命名规范](#命名规范)
5. [提交规范](#提交规范)
6. [测试要求](#测试要求)
7. [发布流程](#发布流程)
8. [CHANGELOG 维护](#changelog-维护)
9. [禁止事项](#禁止事项)

---

## 当前项目状态

| 版本线 | 状态 | ClawHub Slug | 当前 latest | 文档 |
|--------|------|--------------|-------------|------|
| **v1.x**（稳定版）| 长期维护，仅兼容性修复 | `thesis-workflow` | v1.7.3 | [CHANGELOG-v1.md](./CHANGELOG-v1.md) |
| **v2.x**（新框架）| ⚠️ 测试版，独立测试 | `thesis-workflow-v2` | v2.0.6 | [CHANGELOG-v2.md](./CHANGELOG-v2.md) |

### 选型指南

| 场景 | 用哪个版本 |
|------|----------|
| 已有 v1 用户 / 生产环境 | v1.7.3（稳定）|
| 新功能 / outline-anchored / 9 HIL 体验 | v2.0.6（测试）|
| 同时跑多篇论文 | 两个都装，可共存 |

---

## ⚠️ v2 不是 v1 的小升级，是重新设计

**贡献者请务必理解**：v2 框架（outline-anchored）和 v1 框架（双版本）是**不同的设计哲学**，不是 v1 的"feature 增删"。

### v1 核心设计（已被 v2 取代）

```
Phase 1（规划）→ Phase 2（双版本起草）→ Phase 2.5（用户确认）
→ Phase 3（双版本审核）→ Phase 3.5（深度评审）→ Phase 4（整合）→ Phase 5（终审）
→ [Phase 5.1 去AI味] → Phase 5.2（Word 输出）
```

**双版本分工**：
- 版本H（Hermes深度逻辑链）：`hermes chat` 生成长篇深度内容
- 版本O（OpenClaw格式规范）：`sessions_spawn` subagent 生成格式严谨内容
- 同一章节生成 2 份完整内容，用户/Integrator 选择/整合

### v2 核心设计（当前主线）

```
Phase 1（规划）→ Phase 1.3（开题报告归因）→ Phase 2（逐节点写作）
→ Phase 3（整合）→ Phase 5（导出）
```

**outline-anchored + 9 HIL + 单内容生成**：
- 每个节点 1 次 LLM 调用 → 1 份 content + 1 个 key_conclusion
- outline 锚定 + bridge 上下文衔接（保障不离题 + 衔接自然）
- reviewer.py 评审 quality=high/medium/low
- 9 个 HIL hard pause（强人工/Agent 介入）

### 关键差异对比

| 维度 | v1 双版本 | v2 outline-anchored |
|------|----------|---------------------|
| **核心机制** | 同章 2 版本对比 | outline 锚定 + 评审驱动 |
| **Phase 2 输出** | 2 份完整内容（H+O）| 1 份 content + key_conclusion |
| **LLM 调用次数** | 每章 2 次（+ 整合）| 每节点 1 次 |
| **质量保障** | H/O 对比 + 整合方案 | reviewer 评审 + bridge 上下文 |
| **HIL 节点数** | 4 个 | **9 个**（v2.0.6 强化） |
| **章节承接** | 整合阶段拼接 | bridge_paragraph + 虚拟摘要节点 |
| **LLM 注入** | hardcode hermes / sessions_spawn | **llm_func callable**（任意注入）|
| **跳过 Phase 1.3** | ✅ 允许（debug 入口）| ❌ 拦截（v2.0.6 拍板 #1 强制）|
| **B-2 幂等保护** | ❌ 无 | ✅ v2.0.6 新增（防止覆盖）|
| **独立 Reviewer** | ❌ 自审 | ✅ reviewer_func 参数（防自审）|

### 为什么 v2 重构？

1. **简化流程**：双版本成本高，v2 走单内容 + 评审，质量等价
2. **强人/Agent 介入**：v2 的 9 HIL 比 v1 的 4 HIL 更频繁，让用户/Agent 主动控制
3. **标准化 LLM 接入**：v2 的 llm_func callable 让任意 LLM 实现都可注入，v1 强绑 hermes + OpenClaw
4. **outline 锚定**：v2 把"如何写"分解成 outline 节点级，强结构化
5. **可扩展性**：v2 的 outline_parser + state_manager_v2 是独立模块，便于二次开发

### v1 → v2 不是无缝迁移

| 不兼容点 | 说明 |
|---------|------|
| `scripts/orchestrator.py` (v1) | 与 `scripts/orchestrator_v2.py` 接口完全不同 |
| State 文件 | 字段不同（v2 加了 audit_log, content_hint 等）|
| HIL 数量 | 4 → 9，交互点更多 |
| 状态机驱动 | v1 是 cron + 状态文件；v2 是显式 `orchestrate()` 调用 |
| skip_phase1_3 | v1 debug 允许；v2 拦截（强制 reason + operator + audit）|

**迁移建议**：
- 不要直接把 v1 论文 state 跑 v2（不兼容）
- 用 v1 跑完后，导出 md → 人工复审 → 用 v2 重新生成（如有需要）

---

## 分支管理

### 分支结构

```
main       v1.x 长期维护分支（仅 v1 兼容性修复）
v2         v2.x 长期演进分支（v2 主线开发）
fix/v1.x-*  v1 短期修复（base on main，merge 回 main）
fix/v2.x-*  v2 短期修复（base on v2，merge 回 v2）
feature/*   新功能开发（base on 对应主线）
```

### 改动归属规则

| 改动类型 | 进哪个分支 |
|---------|-----------|
| v1 兼容性 bug 修复 | → `main`（或 `fix/v1.x-*` → `main`）|
| v1 新功能（不破坏 v1）| → `main` |
| v2 改动 | → `v2`（或 `fix/v2.x-*` → `v2`）|
| 共享文档（references/）| 各自分支（CHANGELOG 等分开）|
| ❌ v2 → main 合并 | **永不允许**（破坏双版本隔离）|

### 当前实际分支状态

| 分支 | commit | 状态 |
|------|--------|------|
| `main` | df14c58 / 681ae19 | v1.7.3 + v2 声明文档 |
| `v2` | dcc562c | v2.0.6 |
| `tag v2.0-base` | df14c58 | v1.7.3 锚点（保留）|
| `tag v2.0.0 ~ v2.0.6` | 各 commit | v2 版本标签 |

详细设计见 [`docs/git-workflow.md`](./docs/git-workflow.md)（如不存在，见 [`references/git-workflow.md`](./references/git-workflow.md)）。

---

## 命名规范

### 分支命名

| 模式 | 用途 | 示例 |
|------|------|------|
| `fix/v1.x-{描述}` | v1 短期修复 | `fix/v1.7.4-md2docx-bug` |
| `fix/v2.x-{描述}` | v2 短期修复 | `fix/v2.0.7-b2-state-sync` |
| `feature/{描述}` | 新功能 | `feature/bridge-enhancement` |
| `docs/{描述}` | 文档 | `docs/readme-en-update` |

### Commit 消息

遵循 [Conventional Commits](https://www.conventionalcommits.org/)：

```
<type>(<scope>): <subject>

<body>

<footer>
```

**type**：
- `feat` — 新功能
- `fix` — bug 修复
- `docs` — 仅文档
- `refactor` — 重构（无 bug 修复或功能变化）
- `test` — 测试相关
- `chore` — 构建/CI/工具

**scope**（可选）：
- `v1.x` / `v2.0.6` — 版本号（修复 bug 时必填）
- `scripts` / `docs` / `tests` — 影响范围

**示例**：
```
fix(v2.0.6): 补 enforcement + 真实入口

P0 修复：
- skip_phase1_3 入口拦截 + 函数层双层保护
- 新增 scripts/run_workflow.py CLI 真实入口

测试：158 → 172 passed
```

---

## 测试要求

**所有 PR 必须 100% 测试通过**。

```bash
# 跑全部测试
python3 -m pytest scripts/tests/ --tb=line \
  --deselect scripts/tests/test_orchestrator.py::TestReviewDecision::test_continue_decision
```

### 当前已知未修 Bug

1 个预存在的 bug（与 v2 改动无关）：
- `test_orchestrator.py::TestReviewDecision::test_continue_decision` 失败

如果修了，顺手 unblock。

### 写新测试的规范

- 单元测试放 `scripts/tests/test_{module}.py`
- 命名规范：`def test_{feature}_{scenario}`
- 必须用 `unittest.TestCase` + `assertEqual` / `assertTrue` 等
- 涉及 state 文件用临时 paper_name + setUp/tearDown 清理

---

## 发布流程

### ⚠️ 重要：不要用 GitHub Actions

GitHub Actions 部署在 `westcentralus` Azure 区域，到 `clawhub.ai` 的网络 **120秒 timeout**。已验证 6 次发布都因同样错误失败。

**必须从本地用 `clawhub skill publish` 命令直接发布**。

### v1 发布流程

```bash
# 1. 切到 main，准备 v1.x 修复
git checkout main
# ... 修改 + 测试 ...
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

### v2 发布流程

```bash
# 1. 切到 v2，准备 v2.x 修复
git checkout v2
# ... 修改 + 测试 ...
git add . && git commit -m "fix(v2.0.7): ..."
git tag v2.0.7

# 2. 推 GitHub
git push origin v2 --tags

# 3. 发 ClawHub（v2 slug，独立仓库）
cd /tmp  # 重要：从 /tmp 工作目录发布
clawhub skill publish /Users/hehe9737/GitHub/mba-thesis-workflow \
  --slug thesis-workflow-v2 \
  --owner hehe973781230 \
  --version 2.0.7 \
  --tags latest \
  --changelog "..."
```

### 两个要点

1. **从 `/tmp` 工作目录**发布，不能从仓库目录里（CLI 把 `.` 当 workdir 导致 SKILL.md required 错误）
2. **用绝对路径**指定 skill 目录

### 前提

```bash
# 登录（首次）
clawhub login  # 登录为 hehe973781230
```

---

## CHANGELOG 维护

### 文件结构

```
CHANGELOG.md        ← 顶层索引 + 版本线推荐表
CHANGELOG-v1.md     ← v1.x 完整历史
CHANGELOG-v2.md     ← v2.x + alpha 阶段说明
```

### 每次发版必做

1. **CHANGELOG-{v1|v2}.md** 加新版本段
2. **CHANGELOG.md** 索引更新最新版本号
3. **README.md** 顶部双版本推荐表更新（如适用）

### CHANGELOG 模板

```markdown
## [v2.0.7] - 2026-06-XX

### 修复 / 新增

- [P0-1] XXX 修复
- [P0-2] YYY 新增

### 测试

- 修复前：N 个测试通过
- 修复后：N+M 个测试通过
```

---

## 禁止事项

| ❌ 禁止 | 原因 |
|--------|------|
| v2 → main 合并 | 破坏双版本隔离原则 |
| 跳过 Phase 1.3（除非测试场景 + audit log） | 拍板 #1 强制 |
| 直接覆盖 `outline_update_status` 已 completed 节点 | v2.0.6 B-2 幂等保护（用 `force=True` 调试场景）|
| 用同一 `llm_func` 做生成 + 评审（self-review）| v2.0.6 P1-2 独立 Reviewer 警告 |
| 推 GitHub Actions 自动发布 | 120s timeout 必失败 |
| 直接 publish 不先 commit 到本地 | 违反"先本地确认再发布"原则 |
| 推敏感信息（用户姓名/邮箱/电话/真实公司）| 见 `references/checklist.md` |

---

## 检查清单（每次发版前）

- [ ] CHANGELOG 完整
- [ ] README 当前版本号同步
- [ ] SKILL.md frontmatter version 同步
- [ ] 所有测试通过（除已知 bug）
- [ ] 无敏感信息（grep 检查）
- [ ] 临时文件清理（`/tmp/*`, `~/.openclaw/workspace/test_*`）
- [ ] git tag 已打
- [ ] maintainer review commit（v2.0.6 起强制）
- [ ] 推 GitHub + 发 ClawHub 都做

---

## 相关文档

- [README.md](./README.md) — 项目介绍 + 快速开始
- [CHANGELOG.md](./CHANGELOG.md) — 版本索引
- [references/checklist.md](./references/checklist.md) — 学术规范
- [references/loop-design.md](./references/loop-design.md) — Loop 设计原理
- [references/git-workflow.md](./references/git-workflow.md) — 详细分支管理（开发者参考）

---

## 维护者

- Owner: hehe973781230
- ClawHub: https://clawhub.ai/hehe973781230
- GitHub: https://github.com/hehe973781230/thesis-workflow

贡献前有任何疑问，欢迎提 Issue。